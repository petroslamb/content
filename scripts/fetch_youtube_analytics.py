#!/usr/bin/env python3
"""Fetch read-only YouTube Analytics metrics into a local decision ledger."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

YOUTUBE_SKILL_SCRIPTS = (
    Path(__file__).resolve().parents[1]
    / "workflows"
    / "skills"
    / "youtube-data-api"
    / "scripts"
)
sys.path.insert(0, str(YOUTUBE_SKILL_SCRIPTS))

try:
    from googleapiclient.errors import HttpError
    from youtube_common import (
        OAuthReauthRequired,
        build_youtube,
        build_youtube_analytics,
    )
except ImportError as exc:  # pragma: no cover - exercised by operator use.
    print(
        "ERROR: Could not import YouTube client libraries. "
        "Run from the project root with the repo virtual environment.",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER_PATH = REPO_ROOT / "experiments" / "youtube-analytics" / "metrics_ledger.json"
WATCH_WINDOWS = {
    "24h": 1,
    "72h": 3,
    "7d": 7,
    "28d": 28,
}
ANALYTICS_METRICS = [
    "views",
    "engagedViews",
    "estimatedMinutesWatched",
    "averageViewDuration",
    "averageViewPercentage",
    "likes",
    "comments",
    "shares",
    "subscribersGained",
    "videoThumbnailImpressions",
    "videoThumbnailImpressionsClickRate",
]
CORE_ANALYTICS_METRICS = [
    "views",
    "estimatedMinutesWatched",
    "averageViewDuration",
    "averageViewPercentage",
    "likes",
    "comments",
    "shares",
    "subscribersGained",
]
TRAFFIC_SOURCE_METRICS = ["views", "estimatedMinutesWatched"]
MANUAL_OBSERVATION_FIELDS = [
    "related_video_clicks",
    "card_clicks",
    "end_screen_clicks",
    "retention_notes",
    "thumbnail_title_observations",
    "studio_related_verified",
]
IGNORED_DIR_NAMES = {
    ".git",
    ".venv",
    ".youtube",
    "node_modules",
    "__pycache__",
}
VIDEO_URL_TEMPLATE = "https://www.youtube.com/watch?v={video_id}"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n")


def parse_iso_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def date_from_iso_datetime(value: str | None) -> str | None:
    parsed = parse_iso_datetime(value)
    if not parsed:
        return None
    return parsed.date().isoformat()


def parse_iso8601_duration_seconds(value: str | None) -> float | None:
    if not value:
        return None
    match = re.fullmatch(
        r"P(?:(?P<days>\d+(?:\.\d+)?)D)?"
        r"(?:T(?:(?P<hours>\d+(?:\.\d+)?)H)?"
        r"(?:(?P<minutes>\d+(?:\.\d+)?)M)?"
        r"(?:(?P<seconds>\d+(?:\.\d+)?)S)?)?",
        value,
    )
    if not match:
        return None
    days = float(match.group("days") or 0)
    hours = float(match.group("hours") or 0)
    minutes = float(match.group("minutes") or 0)
    seconds = float(match.group("seconds") or 0)
    return days * 86400 + hours * 3600 + minutes * 60 + seconds


def extract_video_id_from_url(value: str | None) -> str | None:
    if not value:
        return None
    patterns = [
        r"[?&]v=([A-Za-z0-9_-]{6,})",
        r"youtu\.be/([A-Za-z0-9_-]{6,})",
        r"/shorts/([A-Za-z0-9_-]{6,})",
    ]
    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            return match.group(1)
    return None


def relative_path(path: Path, root: Path = REPO_ROOT) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def infer_package_from_path(path: Path, repo_root: Path = REPO_ROOT) -> str | None:
    try:
        parts = path.relative_to(repo_root).parts
    except ValueError:
        return None
    if not parts or parts[0] != "publications":
        return None
    if "artifacts" not in parts:
        return "/".join(parts[1:-1]) or None
    artifact_index = parts.index("artifacts")
    return "/".join(parts[1:artifact_index]) or None


def infer_topic(package: str | None) -> str | None:
    if not package:
        return None
    return package.rstrip("/").split("/")[-1]


def infer_format(
    *,
    title: str | None,
    duration_seconds: float | None,
    report_path: Path | None = None,
    workflow: str | None = None,
    video_path: str | None = None,
) -> str:
    haystack = " ".join(
        value.lower()
        for value in [
            title or "",
            workflow or "",
            str(report_path or ""),
            video_path or "",
        ]
    )
    if "#shorts" in haystack or "shorts" in haystack or "portrait" in haystack:
        return "short"
    if "tldr" in haystack or "tl;dr" in haystack:
        return "tldr"
    if "cinematic" in haystack:
        return "cinematic"
    if duration_seconds is not None and duration_seconds <= 180:
        return "short"
    return "unknown"


def iter_upload_report_paths(repo_root: Path) -> list[Path]:
    paths: list[Path] = []
    for path in repo_root.rglob("*upload_report*.json"):
        if any(part in IGNORED_DIR_NAMES for part in path.parts):
            continue
        paths.append(path)
    return sorted(paths)


def merge_video_record(
    records: dict[str, dict[str, Any]],
    record: dict[str, Any],
) -> None:
    video_id = record.get("video_id")
    if not video_id:
        return
    existing = records.setdefault(video_id, {"video_id": video_id})
    for key, value in record.items():
        if key == "source_reports":
            continue
        if value not in (None, "", [], {}):
            existing[key] = value
    existing_reports = set(existing.get("source_reports", []))
    existing_reports.update(record.get("source_reports", []))
    existing["source_reports"] = sorted(existing_reports)


def related_video_from_report(report: dict[str, Any]) -> dict[str, Any] | None:
    candidates = [
        report.get("related_video"),
        report.get("related_longform"),
        report.get("secondary_link"),
    ]
    if report.get("main_video_id") or report.get("main_video_url"):
        candidates.append(
            {
                "id": report.get("main_video_id"),
                "url": report.get("main_video_url"),
                "label": "Main video",
            }
        )
    linked_primary = report.get("linked_videos", {}).get("primary")
    if linked_primary:
        candidates.append(linked_primary)
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        video_id = candidate.get("id") or extract_video_id_from_url(candidate.get("url"))
        if video_id:
            return {
                "id": video_id,
                "url": candidate.get("url") or VIDEO_URL_TEMPLATE.format(video_id=video_id),
                "label": candidate.get("label"),
            }
    return None


def video_record_from_upload_report(
    report_path: Path,
    report: dict[str, Any],
    *,
    repo_root: Path = REPO_ROOT,
) -> list[dict[str, Any]]:
    package = report.get("package") or infer_package_from_path(report_path, repo_root)
    workflow = report.get("workflow")
    source_report = relative_path(report_path, repo_root)
    related_video = related_video_from_report(report)
    records: list[dict[str, Any]] = []

    if isinstance(report.get("video"), dict):
        video = report["video"]
        video_id = video.get("id") or extract_video_id_from_url(video.get("url"))
        readback = video.get("youtube_readback", {})
        duration = readback.get("duration")
        duration_seconds = parse_iso8601_duration_seconds(duration)
        records.append(
            {
                "video_id": video_id,
                "title": report.get("title"),
                "url": video.get("url"),
                "published_at": readback.get("published_at") or report.get("publish_at"),
                "privacy_status": readback.get("privacy_status") or report.get("upload_privacy"),
                "duration": duration,
                "duration_seconds": duration_seconds,
                "format": infer_format(
                    title=report.get("title"),
                    duration_seconds=duration_seconds,
                    report_path=report_path,
                    workflow=workflow,
                    video_path=report.get("video_source_file"),
                ),
                "package": package,
                "topic": infer_topic(package),
                "workflow": workflow,
                "related_video": related_video,
                "source_reports": [source_report],
            }
        )

    for item in report.get("items", []):
        if not isinstance(item, dict):
            continue
        video_id = item.get("video_id") or extract_video_id_from_url(item.get("url"))
        readback = item.get("youtube_readback", {})
        probe = item.get("probe", {})
        duration_seconds = (
            probe.get("duration")
            or probe.get("format_duration")
            or parse_iso8601_duration_seconds(readback.get("duration"))
        )
        records.append(
            {
                "video_id": video_id,
                "title": item.get("title"),
                "url": item.get("url"),
                "published_at": readback.get("published_at") or item.get("publish_at"),
                "scheduled_publish_at": item.get("publish_at"),
                "privacy_status": readback.get("privacy_status"),
                "duration": readback.get("duration"),
                "duration_seconds": duration_seconds,
                "format": infer_format(
                    title=item.get("title"),
                    duration_seconds=duration_seconds,
                    report_path=report_path,
                    workflow=workflow,
                    video_path=item.get("video_path") or item.get("portrait_file"),
                ),
                "package": package,
                "topic": infer_topic(package),
                "workflow": workflow,
                "related_video": related_video,
                "source_reports": [source_report],
            }
        )
    return [record for record in records if record.get("video_id")]


def collect_upload_report_videos(repo_root: Path = REPO_ROOT) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for report_path in iter_upload_report_paths(repo_root):
        try:
            report = json.loads(report_path.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(report, dict):
            continue
        for record in video_record_from_upload_report(
            report_path,
            report,
            repo_root=repo_root,
        ):
            merge_video_record(records, record)
    return records


def normalize_analytics_rows(response: dict[str, Any]) -> list[dict[str, Any]]:
    headers = [header.get("name") for header in response.get("columnHeaders", [])]
    normalized: list[dict[str, Any]] = []
    for row in response.get("rows", []) or []:
        normalized.append(dict(zip(headers, row)))
    return normalized


def chunked(values: list[str], size: int) -> list[list[str]]:
    return [values[index : index + size] for index in range(0, len(values), size)]


def query_analytics(
    analytics: Any,
    *,
    start_date: str,
    end_date: str,
    video_ids: list[str],
    metrics: list[str],
    dimensions: str = "video",
) -> tuple[list[dict[str, Any]], str | None]:
    rows: list[dict[str, Any]] = []
    for batch in chunked(video_ids, 50):
        try:
            response = (
                analytics.reports()
                .query(
                    ids="channel==MINE",
                    startDate=start_date,
                    endDate=end_date,
                    metrics=",".join(metrics),
                    dimensions=dimensions,
                    filters="video==" + ",".join(batch),
                )
                .execute()
            )
        except HttpError as exc:
            return [], str(exc)
        rows.extend(normalize_analytics_rows(response))
    return rows, None


def fetch_recent_channel_uploads(
    youtube: Any,
    *,
    since_days: int,
    limit: int,
) -> dict[str, dict[str, Any]]:
    cutoff = utc_now() - timedelta(days=since_days)
    channels_response = (
        youtube.channels()
        .list(part="contentDetails", mine=True, maxResults=1)
        .execute()
    )
    channel_items = channels_response.get("items", [])
    if not channel_items:
        return {}
    uploads_playlist_id = (
        channel_items[0]
        .get("contentDetails", {})
        .get("relatedPlaylists", {})
        .get("uploads")
    )
    if not uploads_playlist_id:
        return {}

    records: dict[str, dict[str, Any]] = {}
    page_token = None
    while len(records) < limit:
        response = (
            youtube.playlistItems()
            .list(
                part="snippet",
                playlistId=uploads_playlist_id,
                maxResults=min(50, limit - len(records)),
                pageToken=page_token,
            )
            .execute()
        )
        stop = False
        for item in response.get("items", []):
            snippet = item.get("snippet", {})
            video_id = snippet.get("resourceId", {}).get("videoId")
            if not video_id:
                continue
            published_at = parse_iso_datetime(snippet.get("publishedAt"))
            if published_at and published_at < cutoff:
                stop = True
                break
            records[video_id] = {
                "video_id": video_id,
                "title": snippet.get("title"),
                "url": VIDEO_URL_TEMPLATE.format(video_id=video_id),
                "published_at": snippet.get("publishedAt"),
                "format": infer_format(
                    title=snippet.get("title"),
                    duration_seconds=None,
                    workflow="youtube_recent_upload",
                ),
                "workflow": "youtube_recent_upload",
                "source_reports": [],
            }
        page_token = response.get("nextPageToken")
        if stop or not page_token:
            break
    return records


def fetch_video_details(youtube: Any, video_ids: list[str]) -> dict[str, dict[str, Any]]:
    details: dict[str, dict[str, Any]] = {}
    for batch in chunked(video_ids, 50):
        response = (
            youtube.videos()
            .list(
                part="snippet,status,contentDetails,statistics",
                id=",".join(batch),
                maxResults=50,
            )
            .execute()
        )
        for item in response.get("items", []):
            details[item["id"]] = item
    return details


def apply_video_details(record: dict[str, Any], detail: dict[str, Any] | None) -> None:
    if not detail:
        record.setdefault("data_api_found", False)
        return
    snippet = detail.get("snippet", {})
    status = detail.get("status", {})
    content_details = detail.get("contentDetails", {})
    statistics = detail.get("statistics", {})
    duration = content_details.get("duration")
    duration_seconds = parse_iso8601_duration_seconds(duration)
    record.update(
        {
            "data_api_found": True,
            "title": snippet.get("title") or record.get("title"),
            "published_at": snippet.get("publishedAt") or record.get("published_at"),
            "privacy_status": status.get("privacyStatus") or record.get("privacy_status"),
            "duration": duration or record.get("duration"),
            "duration_seconds": duration_seconds
            if duration_seconds is not None
            else record.get("duration_seconds"),
            "data_api_statistics": statistics,
        }
    )
    record["format"] = infer_format(
        title=record.get("title"),
        duration_seconds=record.get("duration_seconds"),
        workflow=record.get("workflow"),
    )


def empty_window(
    *,
    start_date: str,
    end_date: str,
    metrics: list[str],
    reason: str | None = None,
) -> dict[str, Any]:
    return {
        "start_date": start_date,
        "end_date": end_date,
        "metrics": {metric: None for metric in metrics},
        "missing": True,
        "missing_reason": reason,
    }


def build_analytics_windows(
    analytics: Any,
    *,
    video_ids: list[str],
    end_date: str,
) -> tuple[
    dict[str, dict[str, dict[str, Any]]],
    dict[str, list[dict[str, Any]]],
    dict[str, list[dict[str, Any]]],
    dict[str, list[dict[str, Any]]],
    list[dict[str, Any]],
]:
    windows_by_video: dict[str, dict[str, dict[str, Any]]] = {
        video_id: {} for video_id in video_ids
    }
    daily_by_video: dict[str, list[dict[str, Any]]] = defaultdict(list)
    traffic_by_video: dict[str, list[dict[str, Any]]] = defaultdict(list)
    content_type_by_video: dict[str, list[dict[str, Any]]] = defaultdict(list)
    query_notes: list[dict[str, Any]] = []
    end = datetime.fromisoformat(end_date).date()

    for label, days in WATCH_WINDOWS.items():
        start_date = (end - timedelta(days=days - 1)).isoformat()
        rows, error = query_analytics(
            analytics,
            start_date=start_date,
            end_date=end_date,
            video_ids=video_ids,
            metrics=ANALYTICS_METRICS,
        )
        metrics_used = ANALYTICS_METRICS
        if error:
            fallback_rows, fallback_error = query_analytics(
                analytics,
                start_date=start_date,
                end_date=end_date,
                video_ids=video_ids,
                metrics=CORE_ANALYTICS_METRICS,
            )
            query_notes.append(
                {
                    "window": label,
                    "query": "video_metrics",
                    "metrics": ANALYTICS_METRICS,
                    "error": error,
                    "fallback_metrics": CORE_ANALYTICS_METRICS,
                    "fallback_error": fallback_error,
                }
            )
            rows = fallback_rows
            error = fallback_error
            metrics_used = CORE_ANALYTICS_METRICS

        rows_by_video = {str(row.get("video")): row for row in rows}
        for video_id in video_ids:
            row = rows_by_video.get(video_id)
            if not row:
                windows_by_video[video_id][label] = empty_window(
                    start_date=start_date,
                    end_date=end_date,
                    metrics=metrics_used,
                    reason=error or "analytics_lag_or_no_rows",
                )
                continue
            windows_by_video[video_id][label] = {
                "start_date": start_date,
                "end_date": end_date,
                "metrics": {metric: row.get(metric) for metric in metrics_used},
                "missing": False,
                "missing_reason": None,
            }

        daily_rows, daily_error = query_analytics(
            analytics,
            start_date=start_date,
            end_date=end_date,
            video_ids=video_ids,
            metrics=CORE_ANALYTICS_METRICS,
            dimensions="video,day",
        )
        if daily_error:
            query_notes.append(
                {
                    "window": label,
                    "query": "daily_video_metrics",
                    "error": daily_error,
                }
            )
        else:
            for row in daily_rows:
                daily_by_video[str(row.get("video"))].append(
                    {
                        "window": label,
                        "day": row.get("day"),
                        "metrics": {
                            metric: row.get(metric)
                            for metric in CORE_ANALYTICS_METRICS
                        },
                    }
                )

        traffic_rows, traffic_error = query_analytics(
            analytics,
            start_date=start_date,
            end_date=end_date,
            video_ids=video_ids,
            metrics=TRAFFIC_SOURCE_METRICS,
            dimensions="video,insightTrafficSourceType",
        )
        if traffic_error:
            query_notes.append(
                {
                    "window": label,
                    "query": "traffic_sources",
                    "error": traffic_error,
                }
            )
        else:
            for row in traffic_rows:
                traffic_by_video[str(row.get("video"))].append(
                    {
                        "window": label,
                        "source_type": row.get("insightTrafficSourceType"),
                        "views": row.get("views"),
                        "estimatedMinutesWatched": row.get("estimatedMinutesWatched"),
                    }
                )

        content_type_rows, content_type_error = query_analytics(
            analytics,
            start_date=start_date,
            end_date=end_date,
            video_ids=video_ids,
            metrics=["views"],
            dimensions="video,creatorContentType",
        )
        if content_type_error:
            query_notes.append(
                {
                    "window": label,
                    "query": "creator_content_type",
                    "error": content_type_error,
                }
            )
        else:
            for row in content_type_rows:
                content_type_by_video[str(row.get("video"))].append(
                    {
                        "window": label,
                        "creatorContentType": row.get("creatorContentType"),
                        "views": row.get("views"),
                    }
                )

    return (
        windows_by_video,
        daily_by_video,
        traffic_by_video,
        content_type_by_video,
        query_notes,
    )


def add_manual_fields(record: dict[str, Any]) -> None:
    record["manual_observations"] = {
        field: record.get("manual_observations", {}).get(field)
        if isinstance(record.get("manual_observations"), dict)
        else None
        for field in MANUAL_OBSERVATION_FIELDS
    }


def build_ledger(
    *,
    youtube: Any,
    analytics: Any,
    since_days: int,
    video_ids: list[str],
    from_upload_reports: bool,
    recent_limit: int,
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    records: dict[str, dict[str, Any]] = {}
    if from_upload_reports:
        records.update(collect_upload_report_videos(repo_root))
    for video_id in video_ids:
        merge_video_record(
            records,
            {
                "video_id": video_id,
                "url": VIDEO_URL_TEMPLATE.format(video_id=video_id),
                "workflow": "explicit_video_id",
                "source_reports": [],
            },
        )
    for record in fetch_recent_channel_uploads(
        youtube,
        since_days=since_days,
        limit=recent_limit,
    ).values():
        merge_video_record(records, record)

    sorted_video_ids = sorted(records)
    details = fetch_video_details(youtube, sorted_video_ids)
    for video_id in sorted_video_ids:
        apply_video_details(records[video_id], details.get(video_id))

    analytics_end_date = (utc_now().date() - timedelta(days=1)).isoformat()
    (
        windows_by_video,
        daily_by_video,
        traffic_by_video,
        content_type_by_video,
        query_notes,
    ) = build_analytics_windows(
        analytics,
        video_ids=sorted_video_ids,
        end_date=analytics_end_date,
    )

    videos: list[dict[str, Any]] = []
    for video_id in sorted_video_ids:
        record = records[video_id]
        record.setdefault("url", VIDEO_URL_TEMPLATE.format(video_id=video_id))
        record.setdefault("package", None)
        record.setdefault("topic", infer_topic(record.get("package")))
        record.setdefault("related_video", None)
        record["analytics_windows"] = windows_by_video.get(video_id, {})
        record["daily_metrics"] = daily_by_video.get(video_id, [])
        record["traffic_sources"] = traffic_by_video.get(video_id, [])
        record["creator_content_type"] = content_type_by_video.get(video_id, [])
        add_manual_fields(record)
        videos.append(record)

    return {
        "created_at": utc_now().isoformat(),
        "workflow": "youtube_analytics_decision_loop",
        "read_only": True,
        "source": {
            "since_days": since_days,
            "from_upload_reports": from_upload_reports,
            "explicit_video_ids": video_ids,
            "recent_limit": recent_limit,
        },
        "analytics_end_date": analytics_end_date,
        "windows": WATCH_WINDOWS,
        "manual_observation_fields": MANUAL_OBSERVATION_FIELDS,
        "query_notes": query_notes,
        "videos": videos,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch read-only YouTube Analytics metrics into a local ledger."
    )
    parser.add_argument("--since-days", type=int, default=30)
    parser.add_argument(
        "--video-id",
        action="append",
        default=[],
        help="Specific video ID to include. Repeat or pass comma-separated IDs.",
    )
    parser.add_argument(
        "--from-upload-reports",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Include videos found in repo upload reports.",
    )
    parser.add_argument(
        "--recent-limit",
        type=int,
        default=100,
        help="Maximum recent channel uploads to discover.",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_LEDGER_PATH)
    return parser.parse_args()


def flatten_video_ids(values: list[str]) -> list[str]:
    video_ids: list[str] = []
    for value in values:
        video_ids.extend(part.strip() for part in value.split(",") if part.strip())
    return sorted(set(video_ids))


def main() -> None:
    args = parse_args()
    try:
        youtube = build_youtube()
        analytics = build_youtube_analytics()
        payload = build_ledger(
            youtube=youtube,
            analytics=analytics,
            since_days=args.since_days,
            video_ids=flatten_video_ids(args.video_id),
            from_upload_reports=args.from_upload_reports,
            recent_limit=args.recent_limit,
        )
    except OAuthReauthRequired as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2) from exc
    write_json(args.output, payload)
    print(f"Wrote {len(payload['videos'])} video records to {relative_path(args.output)}")


if __name__ == "__main__":
    main()
