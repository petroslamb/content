#!/usr/bin/env python3
"""Sync YouTube Reporting API CSV exports into the analytics ledger."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
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
    from google.auth.transport.requests import AuthorizedSession
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from youtube_common import OAuthReauthRequired, SCOPES, load_credentials
except ImportError as exc:  # pragma: no cover - exercised by operator use.
    print(
        "ERROR: Could not import YouTube client libraries. "
        "Run from the project root with the repo virtual environment.",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT_DIR = REPO_ROOT / "experiments" / "youtube-analytics"
DEFAULT_LEDGER_PATH = EXPERIMENT_DIR / "metrics_ledger.json"
DEFAULT_REGISTRY_PATH = EXPERIMENT_DIR / "reporting_jobs.json"
DEFAULT_DOWNLOAD_DIR = EXPERIMENT_DIR / "reporting_downloads"

REPORTING_JOB_DEFINITIONS = {
    "channel_basic_a3": {
        "name": "User activity",
        "purpose": "Daily bulk user activity plus aggregate card click fields.",
    },
    "channel_reach_basic_a1": {
        "name": "Reach basic",
        "purpose": "Daily per-video thumbnail impressions and thumbnail CTR.",
    },
    "channel_reach_combined_a1": {
        "name": "Reach combined",
        "purpose": "Daily thumbnail reach broken down by traffic source and device.",
    },
}
DEFAULT_REPORT_TYPES = list(REPORTING_JOB_DEFINITIONS)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n")


def relative_path(path: Path, root: Path = REPO_ROOT) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def parse_report_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y%m%d").date()
    except ValueError:
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
        except ValueError:
            return None


def parse_iso_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
        except ValueError:
            return None


def parse_iso_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def number(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def percent_rate(value: Any) -> float | None:
    converted = number(value)
    if converted is None:
        return None
    if 0 < converted <= 1:
        return converted * 100
    return converted


def add_sum(target: dict[str, float], key: str, value: Any) -> None:
    converted = number(value)
    if converted is None:
        return
    target[key] = target.get(key, 0.0) + converted


def add_weighted_average(
    target: dict[str, float],
    value_key: str,
    value: Any,
    weight: Any,
    *,
    sum_weight_as: str | None = None,
) -> None:
    converted_value = number(value)
    converted_weight = number(weight)
    if converted_value is None or converted_weight is None or converted_weight <= 0:
        return
    target[f"_{value_key}_weighted"] = (
        target.get(f"_{value_key}_weighted", 0.0)
        + converted_value * converted_weight
    )
    target[f"_{value_key}_weight"] = target.get(f"_{value_key}_weight", 0.0) + converted_weight
    if sum_weight_as:
        target[sum_weight_as] = target.get(sum_weight_as, 0.0) + converted_weight


def add_weighted_percent_average(
    target: dict[str, float],
    value_key: str,
    value: Any,
    weight: Any,
    *,
    sum_weight_as: str | None = None,
) -> None:
    add_weighted_average(
        target,
        value_key,
        percent_rate(value),
        weight,
        sum_weight_as=sum_weight_as,
    )


def finalize_weighted_average(
    target: dict[str, float],
    value_key: str,
) -> None:
    weighted = target.pop(f"_{value_key}_weighted", None)
    weight = target.pop(f"_{value_key}_weight", None)
    if weighted is not None and weight:
        target[value_key] = weighted / weight


def reporting_client():
    creds = load_credentials(scopes=SCOPES)
    return build("youtubereporting", "v1", credentials=creds), creds


def list_jobs(reporting) -> list[dict[str, Any]]:
    jobs: list[dict[str, Any]] = []
    page_token = None
    while True:
        response = reporting.jobs().list(pageToken=page_token).execute()
        jobs.extend(response.get("jobs", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            return jobs


def ensure_reporting_jobs(
    reporting,
    report_types: list[str],
) -> list[dict[str, Any]]:
    jobs = list_jobs(reporting)
    by_type = {job.get("reportTypeId"): job for job in jobs}
    for report_type_id in report_types:
        if report_type_id in by_type:
            continue
        definition = REPORTING_JOB_DEFINITIONS[report_type_id]
        job = (
            reporting.jobs()
            .create(
                body={
                    "reportTypeId": report_type_id,
                    "name": definition["name"],
                }
            )
            .execute()
        )
        jobs.append(job)
        by_type[report_type_id] = job
    return jobs


def list_reports(reporting, job_id: str) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    page_token = None
    while True:
        response = (
            reporting.jobs()
            .reports()
            .list(jobId=job_id, pageToken=page_token)
            .execute()
        )
        reports.extend(response.get("reports", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            return reports


def latest_reports_by_start_time(reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for report in reports:
        key = report.get("startTime") or report.get("id")
        existing = latest.get(key)
        if not existing:
            latest[key] = report
            continue
        current_created = parse_iso_datetime(report.get("createTime")) or datetime.min.replace(tzinfo=timezone.utc)
        existing_created = parse_iso_datetime(existing.get("createTime")) or datetime.min.replace(tzinfo=timezone.utc)
        if current_created > existing_created:
            latest[key] = report
    return sorted(latest.values(), key=lambda item: item.get("startTime") or "")


def report_start_date(report: dict[str, Any]) -> date | None:
    return parse_iso_date(report.get("startTime"))


def report_file_path(
    download_dir: Path,
    report_type_id: str,
    report: dict[str, Any],
) -> Path:
    start = report_start_date(report)
    date_prefix = start.isoformat() if start else "unknown-date"
    report_id = report.get("id")
    return download_dir / report_type_id / f"{date_prefix}_{report_id}.csv"


def download_report_csv(
    session: AuthorizedSession,
    report: dict[str, Any],
    output_path: Path,
) -> bool:
    if output_path.exists():
        return False
    output_path.parent.mkdir(parents=True, exist_ok=True)
    response = session.get(report["downloadUrl"])
    response.raise_for_status()
    output_path.write_text(response.text)
    return True


def parse_csv_file(path: Path, report_type_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            row["report_type_id"] = report_type_id
            row["source_file"] = relative_path(path)
            rows.append(row)
    return rows


def parse_downloaded_rows(download_dir: Path, report_types: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for report_type_id in report_types:
        for path in sorted((download_dir / report_type_id).glob("*.csv")):
            rows.extend(parse_csv_file(path, report_type_id))
    return rows


def parse_report_paths(paths: list[tuple[str, Path]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for report_type_id, path in paths:
        if path.exists():
            rows.extend(parse_csv_file(path, report_type_id))
    return rows


def window_contains_day(window: dict[str, Any], row_day: date) -> bool:
    start = parse_iso_date(window.get("start_date"))
    end = parse_iso_date(window.get("end_date"))
    if not start or not end:
        return False
    return start <= row_day <= end


def aggregate_reporting_rows_for_video(
    rows: list[dict[str, Any]],
    video: dict[str, Any],
) -> dict[str, dict[str, dict[str, float]]]:
    video_id = video.get("video_id")
    windows = video.get("analytics_windows") or {}
    aggregates: dict[str, dict[str, dict[str, float]]] = defaultdict(
        lambda: defaultdict(dict)
    )

    for row in rows:
        if row.get("video_id") != video_id:
            continue
        row_day = parse_report_date(row.get("date"))
        if not row_day:
            continue
        report_type_id = row.get("report_type_id")
        for label, window in windows.items():
            if not window_contains_day(window, row_day):
                continue
            aggregate = aggregates[label][report_type_id]
            if report_type_id in {"channel_reach_basic_a1", "channel_reach_combined_a1"}:
                add_weighted_percent_average(
                    aggregate,
                    "videoThumbnailImpressionsClickRate",
                    row.get("video_thumbnail_impressions_ctr"),
                    row.get("video_thumbnail_impressions"),
                    sum_weight_as="videoThumbnailImpressions",
                )
            elif report_type_id == "channel_basic_a3":
                add_sum(aggregate, "card_clicks", row.get("card_clicks"))
                add_sum(aggregate, "card_impressions", row.get("card_impressions"))
                add_weighted_percent_average(
                    aggregate,
                    "card_click_rate",
                    row.get("card_click_rate"),
                    row.get("card_impressions"),
                )
                add_sum(aggregate, "card_teaser_clicks", row.get("card_teaser_clicks"))
                add_sum(
                    aggregate,
                    "card_teaser_impressions",
                    row.get("card_teaser_impressions"),
                )
                add_weighted_percent_average(
                    aggregate,
                    "card_teaser_click_rate",
                    row.get("card_teaser_click_rate"),
                    row.get("card_teaser_impressions"),
                )
            elif report_type_id.startswith("channel_end_screens_"):
                add_sum(
                    aggregate,
                    "end_screen_clicks",
                    row.get("end_screen_element_clicks"),
                )
                add_sum(
                    aggregate,
                    "end_screen_impressions",
                    row.get("end_screen_element_impressions"),
                )
                add_weighted_percent_average(
                    aggregate,
                    "end_screen_click_rate",
                    row.get("end_screen_element_click_rate"),
                    row.get("end_screen_element_impressions"),
                )

    for window_aggregates in aggregates.values():
        for aggregate in window_aggregates.values():
            for key in [
                "videoThumbnailImpressionsClickRate",
                "card_click_rate",
                "card_teaser_click_rate",
                "end_screen_click_rate",
            ]:
                finalize_weighted_average(aggregate, key)
    return aggregates


def merge_reporting_rows_into_ledger(
    ledger: dict[str, Any],
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    merged_at = utc_now().isoformat()
    source_files = sorted({row.get("source_file") for row in rows if row.get("source_file")})
    videos_updated = 0

    for video in ledger.get("videos", []):
        aggregates = aggregate_reporting_rows_for_video(rows, video)
        if not aggregates:
            continue
        videos_updated += 1
        reporting_api = video.setdefault("reporting_api", {})
        reporting_api["merged_at"] = merged_at
        reporting_api["source_files"] = source_files

        observations = video.setdefault("manual_observations", {})
        for label, window_aggregates in aggregates.items():
            window = (video.get("analytics_windows") or {}).get(label)
            if not window:
                continue
            metrics = window.setdefault("metrics", {})

            reach = (
                window_aggregates.get("channel_reach_basic_a1")
                or window_aggregates.get("channel_reach_combined_a1")
            )
            if reach:
                if "videoThumbnailImpressions" in reach:
                    metrics["videoThumbnailImpressions"] = reach["videoThumbnailImpressions"]
                    observations["video_thumbnail_impressions"] = reach["videoThumbnailImpressions"]
                if "videoThumbnailImpressionsClickRate" in reach:
                    metrics["videoThumbnailImpressionsClickRate"] = reach[
                        "videoThumbnailImpressionsClickRate"
                    ]
                    observations["video_thumbnail_ctr"] = reach[
                        "videoThumbnailImpressionsClickRate"
                    ]

            basic = window_aggregates.get("channel_basic_a3")
            if basic:
                for key in [
                    "card_clicks",
                    "card_impressions",
                    "card_click_rate",
                    "card_teaser_clicks",
                    "card_teaser_impressions",
                    "card_teaser_click_rate",
                ]:
                    if key in basic:
                        observations[key] = basic[key]

            end_screens = next(
                (
                    value
                    for report_type_id, value in window_aggregates.items()
                    if report_type_id.startswith("channel_end_screens_")
                ),
                None,
            )
            if end_screens:
                for key in [
                    "end_screen_clicks",
                    "end_screen_impressions",
                    "end_screen_click_rate",
                ]:
                    if key in end_screens:
                        observations[key] = end_screens[key]

    ledger["reporting_api_sync"] = {
        "merged_at": merged_at,
        "source_file_count": len(source_files),
        "videos_updated": videos_updated,
    }
    return ledger


def registry_payload(
    *,
    registry: dict[str, Any],
    jobs: list[dict[str, Any]],
    reports_by_job: dict[str, list[dict[str, Any]]],
    downloaded_by_job: dict[str, list[str]],
) -> dict[str, Any]:
    payload = dict(registry)
    payload.setdefault("workflow", "youtube_analytics_reporting_sync")
    payload["updated_at"] = utc_now().isoformat()
    payload.setdefault("jobs", {})

    for job in jobs:
        report_type_id = job.get("reportTypeId")
        if report_type_id not in REPORTING_JOB_DEFINITIONS:
            continue
        reports = reports_by_job.get(job["id"], [])
        payload["jobs"][report_type_id] = {
            "job_id": job.get("id"),
            "name": job.get("name"),
            "report_type_id": report_type_id,
            "created_at": job.get("createTime"),
            "purpose": REPORTING_JOB_DEFINITIONS[report_type_id]["purpose"],
            "last_checked_at": payload["updated_at"],
            "available_report_count": len(reports),
            "downloaded_report_count": len(downloaded_by_job.get(job["id"], [])),
            "latest_report_end_time": max(
                (report.get("endTime") for report in reports if report.get("endTime")),
                default=None,
            ),
        }
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download YouTube Reporting API CSVs and merge them into the analytics ledger."
    )
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY_PATH)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER_PATH)
    parser.add_argument("--output", type=Path, help="Defaults to overwriting --ledger.")
    parser.add_argument("--download-dir", type=Path, default=DEFAULT_DOWNLOAD_DIR)
    parser.add_argument("--since-days", type=int, default=30)
    parser.add_argument(
        "--report-type",
        action="append",
        choices=sorted(REPORTING_JOB_DEFINITIONS),
        help="Report type to sync. Repeat to override defaults.",
    )
    parser.add_argument(
        "--ensure-jobs",
        action="store_true",
        help="Create missing Reporting API jobs for selected report types.",
    )
    parser.add_argument(
        "--no-download",
        action="store_true",
        help="Only list jobs/reports and update the registry.",
    )
    parser.add_argument(
        "--no-merge",
        action="store_true",
        help="Download reports without merging them into the metrics ledger.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report_types = args.report_type or DEFAULT_REPORT_TYPES
    try:
        reporting, creds = reporting_client()
        jobs = (
            ensure_reporting_jobs(reporting, report_types)
            if args.ensure_jobs
            else list_jobs(reporting)
        )
    except OAuthReauthRequired as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2) from exc
    except HttpError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(3) from exc

    jobs = [job for job in jobs if job.get("reportTypeId") in report_types]
    cutoff = utc_now().date() - timedelta(days=args.since_days)
    session = AuthorizedSession(creds)
    reports_by_job: dict[str, list[dict[str, Any]]] = {}
    downloaded_by_job: dict[str, list[str]] = defaultdict(list)
    selected_report_paths: list[tuple[str, Path]] = []

    for job in jobs:
        reports = latest_reports_by_start_time(
            [
                report
                for report in list_reports(reporting, job["id"])
            if not report_start_date(report) or report_start_date(report) >= cutoff
            ]
        )
        reports_by_job[job["id"]] = reports
        if args.no_download:
            continue
        for report in reports:
            path = report_file_path(args.download_dir, job["reportTypeId"], report)
            downloaded = download_report_csv(session, report, path)
            if downloaded or path.exists():
                downloaded_by_job[job["id"]].append(relative_path(path))
                selected_report_paths.append((job["reportTypeId"], path))

    registry = registry_payload(
        registry=load_json(args.registry),
        jobs=jobs,
        reports_by_job=reports_by_job,
        downloaded_by_job=downloaded_by_job,
    )
    write_json(args.registry, registry)

    merged_count = 0
    if not args.no_merge and args.ledger.exists():
        ledger = load_json(args.ledger)
        rows = parse_report_paths(selected_report_paths)
        merge_reporting_rows_into_ledger(ledger, rows)
        write_json(args.output or args.ledger, ledger)
        merged_count = ledger.get("reporting_api_sync", {}).get("videos_updated", 0)

    print(
        "Synced "
        f"{sum(len(reports) for reports in reports_by_job.values())} reports across "
        f"{len(jobs)} jobs; merged reporting data into {merged_count} videos."
    )
    print(f"Registry: {relative_path(args.registry)}")
    if not args.no_download:
        print(f"Downloads: {relative_path(args.download_dir)}")


if __name__ == "__main__":
    main()
