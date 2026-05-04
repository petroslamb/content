#!/usr/bin/env python3
"""Build a static local dashboard for YouTube analytics decisions."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER_PATH = REPO_ROOT / "experiments" / "youtube-analytics" / "metrics_ledger.json"
DEFAULT_WEEKLY_REPORT_DIR = REPO_ROOT / "experiments" / "youtube-analytics" / "weekly_reports"
DEFAULT_REPORTING_JOBS_PATH = REPO_ROOT / "experiments" / "youtube-analytics" / "reporting_jobs.json"
DEFAULT_CONTENT_RUBRIC_PATH = REPO_ROOT / "experiments" / "youtube-analytics" / "content_rubric.json"
DEFAULT_EXPERIMENT_REGISTRY_PATH = REPO_ROOT / "experiments" / "youtube-analytics" / "experiment_registry.yaml"
DEFAULT_SNAPSHOT_DIR = REPO_ROOT / "experiments" / "youtube-analytics" / "snapshots"
DEFAULT_OUTPUT_PATH = REPO_ROOT / "experiments" / "youtube-analytics" / "dashboard" / "index.html"
DEFAULT_RELEASE_TIMEZONE = "Europe/Athens"

DECISION_ORDER = [
    "scale",
    "funnel_winner",
    "clip_more",
    "retitle",
    "hook_problem",
    "remaster",
    "ignore",
]
WINDOW_ORDER = ["24h", "72h", "7d", "28d"]
HORIZONS = {
    "daily": {
        "label": "Daily",
        "description": "Latest per-day row available from YouTube Analytics.",
        "window": None,
        "days": 1,
    },
    "weekly": {
        "label": "Weekly",
        "description": "7-day Analytics window.",
        "window": "7d",
        "days": 7,
    },
    "monthly": {
        "label": "28 Days",
        "description": "28-day Analytics window, matching the Studio-style month view.",
        "window": "28d",
        "days": 28,
    },
}
DAILY_WINDOW_PRIORITY = {
    "24h": 0,
    "72h": 1,
    "7d": 2,
    "28d": 3,
}
CORE_METRICS = [
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
MANUAL_FIELDS = [
    "related_video_clicks",
    "card_clicks",
    "card_impressions",
    "card_teaser_clicks",
    "card_teaser_impressions",
    "card_click_rate",
    "card_teaser_click_rate",
    "end_screen_clicks",
    "retention_notes",
    "thumbnail_title_observations",
    "studio_related_verified",
]
READABLE_FIELD_LABELS = {
    "video_thumbnail_impressions": "Thumbnail impressions",
    "thumbnail_impressions": "Thumbnail impressions",
    "video_thumbnail_ctr": "Thumbnail CTR",
    "thumbnail_ctr": "Thumbnail CTR",
    "related_video_clicks": "Related-video clicks",
    "card_clicks": "Card clicks",
    "card_impressions": "Card impressions",
    "card_teaser_clicks": "Card teaser clicks",
    "card_teaser_impressions": "Card teaser impressions",
    "card_click_rate": "Card click rate",
    "card_teaser_click_rate": "Card teaser click rate",
    "end_screen_clicks": "End-screen clicks",
    "retention_notes": "Retention notes",
    "thumbnail_title_observations": "Thumbnail/title observations",
    "studio_related_verified": "Studio related-video verification",
    "source_reports": "Source reports",
    "package": "Package metadata",
    "format": "Format metadata",
    "playlists": "Playlist metadata",
    "views": "Views",
    "engagedViews": "Engaged views",
    "estimatedMinutesWatched": "Watch time",
    "averageViewDuration": "Average view duration",
    "averageViewPercentage": "Average viewed",
    "likes": "Likes",
    "comments": "Comments",
    "shares": "Shares",
    "subscribersGained": "Subscribers gained",
    "videoThumbnailImpressions": "Thumbnail impressions",
    "videoThumbnailImpressionsClickRate": "Thumbnail CTR",
}
FIELD_GROUPS = {
    "api_pending": [
        "video_thumbnail_impressions",
        "video_thumbnail_ctr",
        "card_clicks",
        "card_impressions",
        "card_teaser_clicks",
        "card_teaser_impressions",
    ],
    "studio_manual": [
        "related_video_clicks",
        "end_screen_clicks",
        "retention_notes",
        "thumbnail_title_observations",
        "studio_related_verified",
    ],
    "workflow_metadata": [
        "source_reports",
        "package",
        "format",
        "playlists",
    ],
}
FIELD_UNLOCKS = {
    "video_thumbnail_impressions": "channel_reach_basic_a1",
    "video_thumbnail_ctr": "channel_reach_basic_a1",
    "card_clicks": "channel_basic_a3",
    "card_impressions": "channel_basic_a3",
    "card_teaser_clicks": "channel_basic_a3",
    "card_teaser_impressions": "channel_basic_a3",
}
DO_NOW_CATEGORIES = {"scale", "funnel_winner", "clip_more", "hook_problem", "remaster"}
CTR_FIELDS = {"video_thumbnail_impressions", "video_thumbnail_ctr"}
STUDIO_CHECK_FIELDS = {
    "related_video_clicks",
    "end_screen_clicks",
    "retention_notes",
    "thumbnail_title_observations",
    "studio_related_verified",
}
MIN_THUMBNAIL_CTR_SAMPLE = 50
HELP_TEXT = {
    "actionable_videos": "Videos whose current data crossed a recommendation threshold.",
    "videos_with_thumbnail_impressions": "Videos with thumbnail impression rows hydrated from the YouTube Reporting API.",
    "videos_with_ctr": "Videos with thumbnail CTR rows hydrated from the YouTube Reporting API.",
    "shorts_thumbnail_impressions": "For Shorts, thumbnail impressions are classic registered thumbnail exposures. They do not represent every Shorts-feed exposure.",
    "shorts_feed_views": "Views from the YouTube Analytics SHORTS traffic source. These can be much higher than thumbnail impressions because Shorts-feed viewing is not always a thumbnail click.",
    "tiny_thumbnail_sample": f"CTR is treated as directional only after at least {MIN_THUMBNAIL_CTR_SAMPLE} thumbnail impressions. Below that, it is too noisy for packaging decisions.",
    "known_funnel_clicks": "Known clicks into another video from related-video clicks, cards, or end screens. This excludes normal YouTube related-video traffic views.",
    "related_video_traffic_views": "Views whose YouTube Analytics traffic source is RELATED_VIDEO.",
    "metric_coverage": "How many videos have this metric in at least one selected Analytics/Reporting window.",
    "package_rollups": "Repo publication package grouping inferred from local upload reports and paths, not a YouTube grouping.",
    "playlist_rollups": "Performance for videos in the dashboard scope grouped by YouTube playlist membership.",
    "playlist_inventory": "Full channel playlist inventory from the YouTube Data API, including playlists with no currently analyzed videos.",
    "subscriber_traffic": "YouTube traffic source SUBSCRIBER: views from feeds on the YouTube homepage or YouTube subscription features.",
    "release_timezone": f"Release cohorts use local publish time in {DEFAULT_RELEASE_TIMEZONE}.",
    "srt_hook": "Transcript-derived hook speed from first spoken timestamp and first-15s word count.",
    "srt_promise": "Transcript/title overlap: how much the transcript appears to pay off the title promise.",
    "srt_specificity": "Transcript specificity based on concrete mechanism terms, numbers, and acronyms.",
    "srt_density": "Approximate claim/sentence density per minute from local SRT cues.",
    "srt_payoff": "Whether the closing transcript contains a detectable CTA/payoff phrase.",
    "srt_coverage": "Local SRT match status, file confidence, or missing/malformed reason.",
    "daily_delta": "Change since the previous analytics refresh. Use this to spot momentum, not lifetime performance.",
    "daily_movement": "Change computed from YouTube Analytics daily rows. This uses the latest available Analytics day, which can lag real time by a few days.",
    "experiment_registry": "Tracked production or packaging experiment with a hypothesis, cohort, start date, target metric, and current read.",
    "packaging_lab": "Packaging issue means YouTube showed the video, but the title or thumbnail did not convert enough viewers.",
    "funnel_map": "Known funnel value combines API card/end-screen clicks, manual related clicks, and Analytics related-video traffic where available.",
    "topic_clusters": "Topic cluster inferred from title, package, and transcript terms. Use this to compare content themes, not individual videos.",
    "release_time_lab": f"Release cohort compares videos by local publish time in {DEFAULT_RELEASE_TIMEZONE}. Treat small samples as directional only.",
    "production_queue": "Ranked next action based on current performance, confidence, production leverage, and missing-data risk.",
    "confidence": "Signal confidence: Strong signal, Directional, Too young, Missing CTR, or Needs Studio/manual data.",
    "views_day_movers": "Videos whose views/day changed the most since the previous refresh.",
    "ctr_movers": "Videos whose thumbnail CTR changed the most since the previous refresh.",
    "retention_movers": "Videos whose average viewed percentage changed the most since the previous refresh.",
    "subscriber_movers": "Videos whose subscribers gained changed the most since the previous refresh.",
    "funnel_movers": "Videos whose known funnel clicks or related-video traffic moved since the previous refresh.",
    "high_impression_low_ctr": "The video received enough thumbnail impressions to judge packaging, but CTR is weak.",
    "low_impression_high_retention": "The video keeps viewers once they arrive, but has not received much classic thumbnail distribution.",
    "shorts_feed_thumbnail_mismatch": "Shorts-feed views are present while registered thumbnail impressions are tiny. Use Shorts traffic and retention, not thumbnail CTR, for this read.",
    "title_too_broad": "The title has low specificity and may not signal a concrete mechanism or payoff.",
    "title_too_long": "The title is long enough that it may truncate or dilute the promise.",
    "weak_thumbnail_metadata": "Thumbnail, impression, or CTR metadata is missing or too weak for a clean packaging read.",
}
LENGTH_BANDS = {
    "short": {"target_min": 25, "target_max": 45, "acceptable_max": 60, "label": "25-45s target"},
    "cinematic": {"target_min": 180, "target_max": 360, "acceptable_max": 480, "label": "3-6m target"},
    "tldr": {"target_min": 300, "target_max": 600, "acceptable_max": 900, "label": "5-10m target"},
    "podcast": {"target_min": 1200, "target_max": 5400, "acceptable_max": 7200, "label": "archive/funnel"},
    "unknown": {"target_min": 25, "target_max": 600, "acceptable_max": 900, "label": "unknown format"},
}
QUEUE_ACTION_LABELS = {
    "make_sequel": "Make follow-up",
    "clip_more": "Clip more",
    "thumbnail_review": "Fix packaging",
    "retitle": "Retitle / reframe",
    "remaster": "Remaster",
    "wait": "Wait for data",
    "ignore": "Watch only",
}
PRODUCTION_ACTIONS = {"make_sequel", "clip_more"}
FIX_ACTIONS = {"thumbnail_review", "retitle", "remaster"}
WATCH_ACTIONS = {"wait", "ignore"}
TITLE_STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "for",
    "from",
    "how",
    "in",
    "into",
    "is",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "why",
    "with",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def load_content_rubric(path: Path = DEFAULT_CONTENT_RUBRIC_PATH) -> dict[str, Any]:
    if not path.exists():
        return {
            "generated_from": "local_srt",
            "video_count": 0,
            "status_counts": {},
            "items": {},
        }
    return load_json(path)


def load_experiment_registry(path: Path = DEFAULT_EXPERIMENT_REGISTRY_PATH) -> dict[str, Any]:
    if not path.exists():
        return {"source_path": str(path), "experiments": []}
    raw = yaml.safe_load(path.read_text()) or {}
    experiments = raw.get("experiments") if isinstance(raw, dict) else raw
    if not isinstance(experiments, list):
        experiments = []
    normalized = []
    for index, experiment in enumerate(experiments):
        if not isinstance(experiment, dict):
            continue
        experiment_id = experiment.get("id") or f"experiment_{index + 1}"
        video_ids = experiment.get("video_ids") or experiment.get("cohort_video_ids") or []
        normalized.append(
            {
                "id": experiment_id,
                "name": experiment.get("name") or experiment_id.replace("_", " ").title(),
                "type": experiment.get("type") or experiment.get("experiment_type") or "manual",
                "status": experiment.get("status") or "planned",
                "hypothesis": experiment.get("hypothesis") or "",
                "video_ids": [str(video_id) for video_id in video_ids],
                "start_date": str(experiment.get("start_date") or ""),
                "metric_target": experiment.get("metric_target") or "",
                "notes": experiment.get("notes") or "",
            }
        )
    return {"source_path": str(path), "experiments": normalized}


def load_previous_snapshot(snapshot_dir: Path = DEFAULT_SNAPSHOT_DIR) -> dict[str, Any] | None:
    latest = snapshot_dir / "latest.json"
    if latest.exists():
        return load_json(latest)
    snapshots = sorted(path for path in snapshot_dir.glob("*.json") if path.name != "latest.json")
    if not snapshots:
        return None
    return load_json(snapshots[-1])


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n")


def number(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_iso_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def release_timing_from_published_at(
    value: str | None,
    *,
    timezone_name: str = DEFAULT_RELEASE_TIMEZONE,
) -> dict[str, Any] | None:
    parsed = parse_iso_datetime(value)
    if not parsed:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    local = parsed.astimezone(ZoneInfo(timezone_name))
    hour = local.hour
    if 5 <= hour < 12:
        daypart = "morning"
    elif 12 <= hour < 17:
        daypart = "afternoon"
    elif 17 <= hour < 22:
        daypart = "evening"
    else:
        daypart = "overnight"
    return {
        "published_at_utc": parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "timezone": timezone_name,
        "local_iso": local.isoformat(),
        "weekday": local.strftime("%A"),
        "weekday_index": local.weekday(),
        "hour": hour,
        "hour_label": f"{hour:02d}:00",
        "daypart": daypart,
    }


def format_duration(seconds: Any) -> str:
    value = number(seconds)
    if value is None:
        return "-"
    value = int(round(value))
    minutes, secs = divmod(value, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def length_fit(format_name: str | None, duration_seconds: Any) -> dict[str, Any]:
    seconds = number(duration_seconds)
    band = LENGTH_BANDS.get(format_name or "unknown", LENGTH_BANDS["unknown"])
    if seconds is None:
        return {
            "bucket": "missing",
            "label": "Duration missing",
            "target": band["label"],
            "severity": "gap",
            "duration_label": "-",
        }
    if seconds < band["target_min"]:
        bucket = "short"
        label = "Shorter than target"
        severity = "watch"
    elif seconds <= band["target_max"]:
        bucket = "target"
        label = "In target band"
        severity = "good"
    elif seconds <= band["acceptable_max"]:
        bucket = "acceptable_long"
        label = "Long but acceptable"
        severity = "watch"
    else:
        bucket = "too_long"
        label = "Long for format"
        severity = "risk"
    if format_name == "podcast":
        label = "Archive/funnel length"
        severity = "neutral"
    return {
        "bucket": bucket,
        "label": label,
        "target": band["label"],
        "severity": severity,
        "duration_label": format_duration(seconds),
    }


def title_profile(title: str | None) -> dict[str, Any]:
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9'-]*", title or "")
    meaningful = [word.lower() for word in words if word.lower() not in TITLE_STOP_WORDS]
    specificity = len(set(meaningful)) + len(re.findall(r"\b[A-Z]{2,}\b|\d+", title or ""))
    return {
        "character_count": len(title or ""),
        "word_count": len(words),
        "has_question": "?" in (title or "") or (words[:1] and words[0].lower() in {"why", "how", "what"}),
        "specificity_score": specificity,
    }


def sorted_counter(counter: Counter[str], limit: int | None = None) -> list[dict[str, Any]]:
    items = [{"name": key, "count": value} for key, value in counter.most_common(limit)]
    return items


def latest_report_path(report_dir: Path = DEFAULT_WEEKLY_REPORT_DIR) -> Path | None:
    reports = sorted(report_dir.glob("*.json"))
    return reports[-1] if reports else None


def selected_metric(video: dict[str, Any], metric_name: str, preferred_window: str = "7d") -> float | None:
    windows = video.get("analytics_windows") or {}
    for label in [preferred_window, "28d", "72h", "24h"]:
        window = windows.get(label)
        if not window or window.get("missing"):
            continue
        return number((window.get("metrics") or {}).get(metric_name))
    return None


def normalize_metrics(
    metrics: dict[str, Any] | None,
    *,
    days: int,
) -> dict[str, float | None]:
    metrics = metrics or {}
    views = number(metrics.get("views"))
    subscribers = number(metrics.get("subscribersGained"))
    return {
        "views": views,
        "views_per_day": views / days if views is not None and days else None,
        "estimatedMinutesWatched": number(metrics.get("estimatedMinutesWatched")),
        "averageViewDuration": number(metrics.get("averageViewDuration")),
        "averageViewPercentage": number(metrics.get("averageViewPercentage")),
        "likes": number(metrics.get("likes")),
        "comments": number(metrics.get("comments")),
        "shares": number(metrics.get("shares")),
        "subscribersGained": subscribers,
        "subscribers_per_1000_views": subscribers / views * 1000 if subscribers is not None and views else None,
        "videoThumbnailImpressions": number(metrics.get("videoThumbnailImpressions")),
        "videoThumbnailImpressionsClickRate": number(metrics.get("videoThumbnailImpressionsClickRate")),
    }


def window_horizon_metrics(video: dict[str, Any], window_label: str, days: int) -> dict[str, Any]:
    window = (video.get("analytics_windows") or {}).get(window_label)
    if not window or window.get("missing"):
        return {
            "available": False,
            "window": window_label,
            "start_date": (window or {}).get("start_date"),
            "end_date": (window or {}).get("end_date"),
            "metrics": normalize_metrics(None, days=days),
        }
    return {
        "available": True,
        "window": window_label,
        "start_date": window.get("start_date"),
        "end_date": window.get("end_date"),
        "metrics": normalize_metrics(window.get("metrics"), days=days),
    }


def latest_daily_horizon_metrics(video: dict[str, Any]) -> dict[str, Any]:
    by_day = daily_rows_by_day(video)
    if not by_day:
        return {
            "available": False,
            "window": "daily",
            "day": None,
            "metrics": normalize_metrics(None, days=1),
        }
    day = max(by_day)
    row = by_day[day]
    return {
        "available": True,
        "window": row.get("window"),
        "day": day,
        "metrics": normalize_metrics(row.get("metrics"), days=1),
    }


def daily_rows_by_day(video: dict[str, Any]) -> dict[str, dict[str, Any]]:
    by_day: dict[str, dict[str, Any]] = {}
    for row in video.get("daily_metrics") or []:
        day = row.get("day")
        if not day:
            continue
        existing = by_day.get(day)
        current_priority = DAILY_WINDOW_PRIORITY.get(str(row.get("window")), 99)
        existing_priority = DAILY_WINDOW_PRIORITY.get(str((existing or {}).get("window")), 99)
        if existing is None or current_priority < existing_priority:
            by_day[day] = row
    return by_day


def build_horizon_metrics(video: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        "daily": latest_daily_horizon_metrics(video),
        "weekly": window_horizon_metrics(video, "7d", 7),
        "monthly": window_horizon_metrics(video, "28d", 28),
    }


def summarize_windows(videos: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    coverage: dict[str, dict[str, int]] = {}
    for label in WINDOW_ORDER:
        present = 0
        usable = 0
        with_views = 0
        missing = 0
        for video in videos:
            window = (video.get("analytics_windows") or {}).get(label)
            if not window:
                continue
            present += 1
            if window.get("missing"):
                missing += 1
                continue
            usable += 1
            if number((window.get("metrics") or {}).get("views")) is not None:
                with_views += 1
        coverage[label] = {
            "present": present,
            "usable": usable,
            "with_views": with_views,
            "missing": missing,
        }
    return coverage


def summarize_metric_availability(videos: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    counts: Counter[str] = Counter()
    for video in videos:
        observations = video.get("manual_observations") or {}
        for metric_name in CORE_METRICS:
            fallback = None
            if metric_name == "videoThumbnailImpressions":
                fallback = observations.get("video_thumbnail_impressions")
            elif metric_name == "videoThumbnailImpressionsClickRate":
                fallback = observations.get("video_thumbnail_ctr")
            if selected_metric(video, metric_name) is not None or number(fallback) is not None:
                counts[metric_name] += 1
    total = len(videos)
    return {
        metric_name: {
            "count": counts.get(metric_name, 0),
            "total": total,
            "percent": counts.get(metric_name, 0) / total * 100 if total else None,
        }
        for metric_name in CORE_METRICS
    }


def summarize_manual_availability(videos: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    counts: Counter[str] = Counter()
    for video in videos:
        observations = video.get("manual_observations") or {}
        for field in MANUAL_FIELDS:
            if observations.get(field) is not None:
                counts[field] += 1
    total = len(videos)
    return {
        field: {
            "count": counts.get(field, 0),
            "total": total,
            "percent": counts.get(field, 0) / total * 100 if total else None,
        }
        for field in MANUAL_FIELDS
    }


def summarize_traffic(videos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    totals: Counter[str] = Counter()
    for video in videos:
        for row in video.get("traffic_sources") or []:
            if row.get("window") == "7d":
                totals[str(row.get("source_type") or "unknown")] += int(number(row.get("views")) or 0)
    if not totals:
        for video in videos:
            for row in video.get("traffic_sources") or []:
                totals[str(row.get("source_type") or "unknown")] += int(number(row.get("views")) or 0)
    return [{"source": key, "views": value} for key, value in totals.most_common(12)]


def summarize_content_type(videos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    totals: Counter[str] = Counter()
    for video in videos:
        for row in video.get("creator_content_type") or []:
            if row.get("window") == "7d":
                totals[str(row.get("creatorContentType") or "unknown")] += int(number(row.get("views")) or 0)
    if not totals:
        for video in videos:
            for row in video.get("creator_content_type") or []:
                totals[str(row.get("creatorContentType") or "unknown")] += int(number(row.get("views")) or 0)
    return [{"content_type": key, "views": value} for key, value in totals.most_common()]


def source_report_links(source_reports: list[str]) -> list[dict[str, str]]:
    links: list[dict[str, str]] = []
    for report in source_reports:
        path = Path(report)
        absolute = path if path.is_absolute() else REPO_ROOT / path
        links.append(
            {
                "label": path.name,
                "path": str(path),
                "url": absolute.as_uri(),
            }
        )
    return links


def primary_category(item: dict[str, Any]) -> str:
    categories = item.get("categories") or ["ignore"]
    for category in DECISION_ORDER:
        if category in categories:
            return category
    return categories[0]


def known_clicks(observations: dict[str, Any]) -> dict[str, float]:
    related = number(observations.get("related_video_clicks")) or 0
    card = number(observations.get("card_clicks")) or 0
    end_screen = number(observations.get("end_screen_clicks")) or 0
    return {
        "related_video_clicks": related,
        "card_clicks": card,
        "end_screen_clicks": end_screen,
        "known_downstream_clicks": related + card + end_screen,
    }


def compact_playlist(playlist: dict[str, Any]) -> dict[str, Any]:
    playlist_id = playlist.get("id") or playlist.get("playlist_id")
    title = playlist.get("title") or playlist.get("playlist_title") or playlist_id or "Untitled playlist"
    return {
        "id": playlist_id,
        "title": title,
        "url": f"https://www.youtube.com/playlist?list={playlist_id}" if playlist_id else None,
        "position": playlist.get("position"),
        "privacy_status": playlist.get("privacy_status"),
    }


def compact_playlists(video: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        compact_playlist(playlist)
        for playlist in video.get("playlists") or []
        if isinstance(playlist, dict)
    ]


def classification_horizon_metrics(classification: dict[str, Any]) -> dict[str, dict[str, Any]]:
    selected_window = classification.get("selected_window") or "7d"
    horizon_for_window = {"24h": "daily", "72h": "daily", "7d": "weekly", "28d": "monthly"}
    selected_horizon = horizon_for_window.get(str(selected_window), "weekly")
    horizons = {
        key: {
            "available": False,
            "window": config.get("window"),
            "start_date": None,
            "end_date": None,
            "day": None,
            "metrics": {},
        }
        for key, config in HORIZONS.items()
    }
    horizons[selected_horizon] = {
        "available": True,
        "window": selected_window,
        "start_date": None,
        "end_date": None,
        "day": None,
        "metrics": classification.get("metrics") or {},
    }
    return horizons


def compact_classification(
    classification: dict[str, Any],
    source_video: dict[str, Any] | None = None,
    snapshot_item: dict[str, Any] | None = None,
    *,
    use_ledger_metrics: bool = False,
) -> dict[str, Any]:
    metrics = classification.get("metrics") or {}
    source_video = source_video or {}
    snapshot_item = snapshot_item or {}
    observations = source_video.get("manual_observations") or {}
    categories = classification.get("categories") or ["ignore"]
    reasons = classification.get("reasons") or []
    reasons_by_category = {
        category: reasons[index]
        for index, category in enumerate(categories)
        if index < len(reasons)
    }
    source_reports = source_video.get("source_reports") or []
    click_metrics = known_clicks(observations) if use_ledger_metrics else {}
    snapshot_funnel = {} if use_ledger_metrics else (snapshot_item.get("funnel") or {})
    horizon_metrics = (
        build_horizon_metrics(source_video)
        if use_ledger_metrics
        else snapshot_item.get("horizon_metrics") or classification_horizon_metrics(classification)
    )
    traffic_sources = (source_video.get("traffic_sources") if use_ledger_metrics else snapshot_item.get("traffic_sources")) or []
    playlists = compact_playlists(source_video)
    duration_seconds = number(source_video.get("duration_seconds"))
    release_timing = source_video.get("release_timing") or release_timing_from_published_at(
        classification.get("published_at") or source_video.get("published_at")
    )
    fit = length_fit(classification.get("format") or source_video.get("format"), duration_seconds)
    return {
        "video_id": classification.get("video_id"),
        "title": classification.get("title"),
        "url": classification.get("url"),
        "format": classification.get("format") or "unknown",
        "format_source": source_video.get("format_source") or "unknown",
        "discovery_sources": source_video.get("discovery_sources") or [],
        "package": classification.get("package") or "unknown",
        "playlists": playlists,
        "primary_playlist": playlists[0] if playlists else None,
        "published_at": classification.get("published_at"),
        "release_timing": release_timing,
        "privacy_status": source_video.get("privacy_status"),
        "duration_seconds": duration_seconds,
        "duration_label": format_duration(duration_seconds),
        "length_fit": fit,
        "thumbnail_url": source_video.get("thumbnail_url") or snapshot_item.get("thumbnail_url"),
        "thumbnails": source_video.get("thumbnails") or [],
        "title_profile": title_profile(classification.get("title")),
        "traffic_sources": traffic_sources,
        "shorts_feed_views": traffic_source_views_for_item(
            {"traffic_sources": traffic_sources},
            "SHORTS",
            horizon_window="7d",
        ),
        "selected_window": classification.get("selected_window"),
        "data_age_days": classification.get("data_age_days"),
        "categories": categories,
        "primary_category": primary_category({"categories": categories}),
        "reasons": reasons,
        "reasons_by_category": reasons_by_category,
        "recommended_actions": classification.get("recommended_actions") or [],
        "actions_by_category": classification.get("actions_by_category") or {},
        "manual_fields_missing": classification.get("manual_fields_missing") or [],
        "related_video": source_video.get("related_video") or classification.get("related_video"),
        "source_reports": source_reports,
        "source_report_links": source_report_links(source_reports),
        "horizon_metrics": horizon_metrics,
        "funnel": {
            **snapshot_funnel,
            **click_metrics,
            "card_impressions": number(observations.get("card_impressions")) if use_ledger_metrics else snapshot_funnel.get("card_impressions"),
            "card_teaser_clicks": number(observations.get("card_teaser_clicks")) if use_ledger_metrics else snapshot_funnel.get("card_teaser_clicks"),
            "card_teaser_impressions": number(observations.get("card_teaser_impressions")) if use_ledger_metrics else snapshot_funnel.get("card_teaser_impressions"),
            "card_click_rate": number(observations.get("card_click_rate")) if use_ledger_metrics else snapshot_funnel.get("card_click_rate"),
            "card_teaser_click_rate": number(observations.get("card_teaser_click_rate")) if use_ledger_metrics else snapshot_funnel.get("card_teaser_click_rate"),
        },
        "score": number(classification.get("score")) or 0,
        "metrics": {
            "views": number(metrics.get("views")),
            "views_per_day": number(metrics.get("views_per_day")),
            "estimatedMinutesWatched": number(metrics.get("estimatedMinutesWatched")),
            "averageViewDuration": number(metrics.get("averageViewDuration")),
            "averageViewPercentage": number(metrics.get("averageViewPercentage")),
            "videoThumbnailImpressions": number(metrics.get("videoThumbnailImpressions")),
            "videoThumbnailImpressionsClickRate": number(metrics.get("videoThumbnailImpressionsClickRate")),
            "subscribersGained": number(metrics.get("subscribersGained")),
            "subscribers_per_1000_views": number(metrics.get("subscribers_per_1000_views")),
        },
    }


def summarize_findings(
    report_summary: dict[str, Any],
    videos: list[dict[str, Any]] | None = None,
    snapshot_payload: dict[str, Any] | None = None,
    *,
    use_ledger_metrics: bool = False,
) -> dict[str, Any]:
    video_lookup = {video.get("video_id"): video for video in videos or []}
    snapshot_lookup = {
        item.get("video_id"): item
        for item in ((snapshot_payload or {}).get("findings") or {}).get("classifications") or []
    }
    compact = [
        compact_classification(
            item,
            video_lookup.get(item.get("video_id")),
            snapshot_lookup.get(item.get("video_id")),
            use_ledger_metrics=use_ledger_metrics,
        )
        for item in report_summary.get("classifications") or []
    ]
    by_category: dict[str, list[dict[str, Any]]] = {category: [] for category in DECISION_ORDER}
    missing_fields: Counter[str] = Counter()
    for item in compact:
        for category in item["categories"]:
            by_category.setdefault(category, []).append(item)
        for field in item["manual_fields_missing"]:
            missing_fields[field] += 1
        if not item.get("source_reports"):
            missing_fields["source_reports"] += 1
        if not item.get("package") or item.get("package") == "unknown":
            missing_fields["package"] += 1
        if not item.get("format") or item.get("format") == "unknown":
            missing_fields["format"] += 1
        if not item.get("playlists"):
            missing_fields["playlists"] += 1

    action_items = [
        item
        for item in compact
        if any(category != "ignore" for category in item["categories"])
    ]
    action_items.sort(key=lambda item: item.get("score") or 0, reverse=True)
    ignored = [item for item in compact if item["categories"] == ["ignore"]]

    return {
        "summary_counts": report_summary.get("summary_counts") or {},
        "top_actions": report_summary.get("top_actions") or [],
        "action_items": action_items,
        "ignored_count": len(ignored),
        "by_category": by_category,
        "manual_missing_counts": sorted_counter(missing_fields),
        "classifications": compact,
    }


def build_action_lanes(findings: dict[str, Any]) -> dict[str, dict[str, Any]]:
    lanes = {
        "do_now": {
            "label": "Do Now",
            "description": "Recommendations with enough current signal to act on.",
            "items": [],
        },
        "waiting_for_ctr": {
            "label": "Waiting For CTR",
            "description": "Videos where packaging judgment is blocked by missing impressions or CTR.",
            "items": [],
        },
        "needs_studio_check": {
            "label": "Needs Studio Check",
            "description": "Videos missing Studio-only observations or downstream click fields.",
            "items": [],
        },
        "watch": {
            "label": "Watch",
            "description": "Young, low-signal, or otherwise non-actionable videos.",
            "items": [],
        },
    }
    for item in findings.get("classifications") or []:
        categories = set(item.get("categories") or [])
        missing = set(item.get("manual_fields_missing") or [])
        metrics = item.get("metrics") or {}
        if categories & DO_NOW_CATEGORIES and metrics.get("views") is not None:
            lanes["do_now"]["items"].append(item)
        if missing & CTR_FIELDS:
            lanes["waiting_for_ctr"]["items"].append(item)
        if missing & STUDIO_CHECK_FIELDS:
            lanes["needs_studio_check"]["items"].append(item)
        if categories == {"ignore"}:
            lanes["watch"]["items"].append(item)

    for lane in lanes.values():
        lane["items"].sort(key=lambda item: item.get("score") or 0, reverse=True)
        lane["count"] = len(lane["items"])
    return lanes


def item_metrics_for_horizon(item: dict[str, Any], horizon: str) -> dict[str, Any]:
    horizon_metrics = (item.get("horizon_metrics") or {}).get(horizon)
    if horizon_metrics:
        return horizon_metrics.get("metrics") or {}
    return item.get("metrics") or {}


def build_package_rollups(findings: dict[str, Any], *, horizon: str = "weekly") -> list[dict[str, Any]]:
    rollups: dict[str, dict[str, Any]] = {}
    for item in findings.get("classifications") or []:
        package = item.get("package") or "unknown"
        metrics = item_metrics_for_horizon(item, horizon)
        row = rollups.setdefault(
            package,
            {
                "package": package,
                "video_count": 0,
                "action_items": 0,
                "total_views": 0.0,
                "average_view_percentage_sum": 0.0,
                "average_view_percentage_count": 0,
                "categories": Counter(),
            },
        )
        row["video_count"] += 1
        row["categories"].update(item.get("categories") or ["ignore"])
        if any(category != "ignore" for category in item.get("categories") or []):
            row["action_items"] += 1
        views = number(metrics.get("views"))
        if views is not None:
            row["total_views"] += views
        avg_viewed = number(metrics.get("averageViewPercentage"))
        if avg_viewed is not None:
            row["average_view_percentage_sum"] += avg_viewed
            row["average_view_percentage_count"] += 1

    rows = []
    for row in rollups.values():
        count = row.pop("average_view_percentage_count")
        avg_sum = row.pop("average_view_percentage_sum")
        categories = row.pop("categories")
        row["average_view_percentage"] = avg_sum / count if count else None
        row["category_counts"] = dict(categories)
        rows.append(row)
    return sorted(rows, key=lambda item: (item["action_items"], item["total_views"]), reverse=True)


def build_package_rollups_by_horizon(findings: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    return {
        horizon: build_package_rollups(findings, horizon=horizon)
        for horizon in HORIZONS
    }


def playlist_names_for_item(item: dict[str, Any]) -> list[dict[str, Any]]:
    playlists = item.get("playlists") or []
    if not playlists:
        return [{"id": None, "title": "No playlist", "url": None}]
    return playlists


def build_playlist_rollups(findings: dict[str, Any], *, horizon: str = "weekly") -> list[dict[str, Any]]:
    rollups: dict[str, dict[str, Any]] = {}
    for item in findings.get("classifications") or []:
        metrics = item_metrics_for_horizon(item, horizon)
        for playlist in playlist_names_for_item(item):
            playlist_id = playlist.get("id")
            title = playlist.get("title") or playlist_id or "No playlist"
            key = playlist_id or title
            row = rollups.setdefault(
                key,
                {
                    "playlist_id": playlist_id,
                    "playlist": title,
                    "url": playlist.get("url"),
                    "video_count": 0,
                    "action_items": 0,
                    "total_views": 0.0,
                    "average_view_percentage_sum": 0.0,
                    "average_view_percentage_count": 0,
                    "categories": Counter(),
                },
            )
            row["video_count"] += 1
            row["categories"].update(item.get("categories") or ["ignore"])
            if any(category != "ignore" for category in item.get("categories") or []):
                row["action_items"] += 1
            views = number(metrics.get("views"))
            if views is not None:
                row["total_views"] += views
            avg_viewed = number(metrics.get("averageViewPercentage"))
            if avg_viewed is not None:
                row["average_view_percentage_sum"] += avg_viewed
                row["average_view_percentage_count"] += 1

    rows = []
    for row in rollups.values():
        count = row.pop("average_view_percentage_count")
        avg_sum = row.pop("average_view_percentage_sum")
        categories = row.pop("categories")
        row["average_view_percentage"] = avg_sum / count if count else None
        row["category_counts"] = dict(categories)
        rows.append(row)
    return sorted(rows, key=lambda item: (item["action_items"], item["total_views"], item["video_count"]), reverse=True)


def build_playlist_rollups_by_horizon(findings: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    return {
        horizon: build_playlist_rollups(findings, horizon=horizon)
        for horizon in HORIZONS
    }


def build_horizon_summaries(findings: dict[str, Any]) -> dict[str, dict[str, Any]]:
    summaries: dict[str, dict[str, Any]] = {}
    for horizon in HORIZONS:
        videos_with_metrics = 0
        total_views = 0.0
        total_watch_time = 0.0
        total_subscribers = 0.0
        avg_viewed_sum = 0.0
        avg_viewed_count = 0
        for item in findings.get("classifications") or []:
            horizon_row = (item.get("horizon_metrics") or {}).get(horizon) or {}
            metrics = horizon_row.get("metrics") or {}
            views = number(metrics.get("views"))
            if views is not None:
                videos_with_metrics += 1
                total_views += views
            total_watch_time += number(metrics.get("estimatedMinutesWatched")) or 0
            total_subscribers += number(metrics.get("subscribersGained")) or 0
            avg_viewed = number(metrics.get("averageViewPercentage"))
            if avg_viewed is not None:
                avg_viewed_sum += avg_viewed
                avg_viewed_count += 1
        summaries[horizon] = {
            "label": HORIZONS[horizon]["label"],
            "description": HORIZONS[horizon]["description"],
            "videos_with_metrics": videos_with_metrics,
            "total_views": total_views,
            "total_watch_time_minutes": total_watch_time,
            "total_subscribers_gained": total_subscribers,
            "average_view_percentage": avg_viewed_sum / avg_viewed_count if avg_viewed_count else None,
        }
    return summaries


def summarize_traffic_for_window(videos: list[dict[str, Any]], window: str) -> list[dict[str, Any]]:
    totals: Counter[str] = Counter()
    for video in videos:
        for row in video.get("traffic_sources") or []:
            if row.get("window") == window:
                totals[str(row.get("source_type") or "unknown")] += int(number(row.get("views")) or 0)
    return [{"source": key, "views": value} for key, value in totals.most_common(12)]


def summarize_traffic_by_horizon(videos: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        "daily": {
            "label": "72h traffic-source proxy",
            "note": "YouTube does not always expose a populated latest-day traffic-source mix; this uses the shortest available 72h source window.",
            "sources": summarize_traffic_for_window(videos, "72h"),
        },
        "weekly": {
            "label": "7d traffic sources",
            "note": None,
            "sources": summarize_traffic_for_window(videos, "7d"),
        },
        "monthly": {
            "label": "28d traffic sources",
            "note": None,
            "sources": summarize_traffic_for_window(videos, "28d"),
        },
    }


def build_funnel_rollups(findings: dict[str, Any]) -> dict[str, Any]:
    parent_rollups: dict[str, dict[str, Any]] = {}
    shorts_with_related: list[dict[str, Any]] = []
    totals = {
        "shorts_with_related": 0,
        "videos_with_card_clicks": 0,
        "total_related_video_clicks": 0.0,
        "total_card_clicks": 0.0,
        "total_end_screen_clicks": 0.0,
        "known_downstream_clicks": 0.0,
        "related_video_traffic_views": 0.0,
    }
    for item in findings.get("classifications") or []:
        related_traffic_views = sum(
            number(row.get("views")) or 0
            for row in item.get("traffic_sources") or []
            if row.get("window") == "7d" and row.get("source_type") == "RELATED_VIDEO"
        )
        totals["related_video_traffic_views"] += related_traffic_views
        related = item.get("related_video") or {}
        if not related:
            continue
        funnel = item.get("funnel") or {}
        clicks = number(funnel.get("known_downstream_clicks")) or 0
        totals["known_downstream_clicks"] += clicks
        totals["total_related_video_clicks"] += number(funnel.get("related_video_clicks")) or 0
        totals["total_card_clicks"] += number(funnel.get("card_clicks")) or 0
        totals["total_end_screen_clicks"] += number(funnel.get("end_screen_clicks")) or 0
        if number(funnel.get("card_clicks")):
            totals["videos_with_card_clicks"] += 1
        if item.get("format") == "short":
            totals["shorts_with_related"] += 1
            shorts_with_related.append(item)

        parent_id = related.get("id") or related.get("video_id") or related.get("url") or "unknown"
        parent = parent_rollups.setdefault(
            parent_id,
            {
                "parent_id": parent_id,
                "parent_url": related.get("url"),
                "source_count": 0,
                "short_count": 0,
                "known_downstream_clicks": 0.0,
                "card_clicks": 0.0,
                "related_video_clicks": 0.0,
                "end_screen_clicks": 0.0,
                "sources": [],
            },
        )
        parent["source_count"] += 1
        if item.get("format") == "short":
            parent["short_count"] += 1
        parent["known_downstream_clicks"] += clicks
        parent["card_clicks"] += number(funnel.get("card_clicks")) or 0
        parent["related_video_clicks"] += number(funnel.get("related_video_clicks")) or 0
        parent["end_screen_clicks"] += number(funnel.get("end_screen_clicks")) or 0
        parent["sources"].append(
            {
                "video_id": item.get("video_id"),
                "title": item.get("title"),
                "url": item.get("url"),
                "format": item.get("format"),
                "known_downstream_clicks": clicks,
            }
        )

    return {
        "totals": totals,
        "parents": sorted(
            parent_rollups.values(),
            key=lambda item: (item["known_downstream_clicks"], item["source_count"]),
            reverse=True,
        ),
        "shorts_with_related": sorted(
            shorts_with_related,
            key=lambda item: ((item.get("funnel") or {}).get("known_downstream_clicks") or 0, item.get("score") or 0),
            reverse=True,
        ),
    }


def traffic_mix_for_item(item: dict[str, Any], *, horizon_window: str = "7d") -> list[dict[str, Any]]:
    rows = [
        row
        for row in item.get("traffic_sources") or []
        if row.get("window") == horizon_window
    ]
    total = sum(number(row.get("views")) or 0 for row in rows)
    compact = []
    for row in sorted(rows, key=lambda source: number(source.get("views")) or 0, reverse=True)[:5]:
        views = number(row.get("views")) or 0
        compact.append(
            {
                "source": row.get("source_type") or "unknown",
                "views": views,
                "share": views / total * 100 if total else None,
            }
        )
    return compact


def traffic_source_views_for_item(
    item: dict[str, Any],
    source_type: str,
    *,
    horizon_window: str = "7d",
) -> float:
    return sum(
        number(row.get("views")) or 0
        for row in item.get("traffic_sources") or []
        if row.get("window") == horizon_window and row.get("source_type") == source_type
    )


def weekly_shorts_feed_views(item: dict[str, Any]) -> float:
    return traffic_source_views_for_item(item, "SHORTS", horizon_window="7d")


def thumbnail_ctr_is_usable(item: dict[str, Any], impressions: float | None) -> bool:
    if impressions is None:
        return False
    if item.get("format") == "short" and weekly_shorts_feed_views(item) > 0:
        return impressions >= MIN_THUMBNAIL_CTR_SAMPLE
    return impressions >= MIN_THUMBNAIL_CTR_SAMPLE


def is_shorts_thumbnail_mismatch(item: dict[str, Any], impressions: float | None) -> bool:
    return (
        item.get("format") == "short"
        and weekly_shorts_feed_views(item) > 0
        and impressions is not None
        and impressions < MIN_THUMBNAIL_CTR_SAMPLE
    )


def axis_status(label: str, status: str, detail: str, value: Any = None) -> dict[str, Any]:
    return {
        "label": label,
        "status": status,
        "detail": detail,
        "value": value,
    }


def build_rubric_item(
    item: dict[str, Any],
    *,
    content_item: dict[str, Any] | None = None,
) -> dict[str, Any]:
    metrics = item.get("metrics") or {}
    impressions = number(metrics.get("videoThumbnailImpressions"))
    ctr = number(metrics.get("videoThumbnailImpressionsClickRate"))
    shorts_views = weekly_shorts_feed_views(item)
    tiny_shorts_thumbnail_sample = is_shorts_thumbnail_mismatch(item, impressions)
    views_per_day = number(metrics.get("views_per_day"))
    avg_viewed = number(metrics.get("averageViewPercentage"))
    avg_duration = number(metrics.get("averageViewDuration"))
    length = item.get("length_fit") or {}
    release_timing = item.get("release_timing") or {}
    title = item.get("title_profile") or {}
    funnel = item.get("funnel") or {}
    content_item = content_item or {"status": "missing"}

    if impressions is None or ctr is None:
        discovery = axis_status("Discovery", "gap", "CTR/impression reporting is still missing.")
    elif tiny_shorts_thumbnail_sample:
        discovery = axis_status(
            "Discovery",
            "watch",
            f"{shorts_views:g} Shorts-feed views with only {impressions:g} thumbnail impressions; CTR is not a packaging read.",
        )
    elif not thumbnail_ctr_is_usable(item, impressions):
        discovery = axis_status("Discovery", "watch", "Too few thumbnail impressions for a reliable CTR read.")
    elif impressions >= 500 and ctr < 3:
        discovery = axis_status("Discovery", "risk", "High impressions with weak CTR points to packaging.")
    elif views_per_day is not None and views_per_day >= 20:
        discovery = axis_status("Discovery", "good", "Views/day is showing current demand.")
    else:
        discovery = axis_status("Discovery", "watch", "Discovery signal is still modest.")

    if avg_viewed is None:
        retention = axis_status("Retention", "gap", "Average viewed is unavailable.")
    elif avg_viewed < 30:
        retention = axis_status("Retention", "risk", "Average viewed is weak for the selected window.")
    elif avg_viewed >= 55:
        retention = axis_status("Retention", "good", "Retention is strong enough to study or scale.")
    else:
        retention = axis_status("Retention", "watch", "Retention is acceptable but not a standout.")

    thumbnail_status = "gap" if not item.get("thumbnail_url") else "watch"
    if tiny_shorts_thumbnail_sample:
        thumbnail_status = "watch"
    elif impressions is not None and ctr is not None and impressions >= 500 and ctr < 3:
        thumbnail_status = "risk"
    elif ctr is not None and ctr >= 5 and thumbnail_ctr_is_usable(item, impressions):
        thumbnail_status = "good"
    if tiny_shorts_thumbnail_sample:
        packaging_detail = f"{impressions:g} thumbnail impressions vs {shorts_views:g} Shorts-feed views."
    else:
        packaging_detail = f"{title.get('word_count', 0)} title words, {title.get('character_count', 0)} chars."
    packaging = axis_status(
        "Thumbnail/Packaging",
        thumbnail_status,
        packaging_detail,
    )

    content_status = content_item.get("status") or "missing"
    if content_status != "present":
        content_axis = axis_status("Content Quality", "gap", "No matched local SRT analysis yet.")
        hook_axis = axis_status("Hook Speed", "gap", "No local transcript available for hook timing.")
        promise_axis = axis_status("Promise Match", "gap", "No transcript/title overlap available.")
        specificity_axis = axis_status("Specificity", "gap", "No transcript specificity signal available.")
        density_axis = axis_status("Claim Density", "gap", "No transcript density signal available.")
        payoff_axis = axis_status("Payoff/CTA", "gap", "No closing transcript available.")
        transcript_axis = axis_status(
            "Transcript Coverage",
            "gap",
            content_item.get("reason") or content_item.get("error") or "No matched local SRT.",
        )
    else:
        hook_delay = number(content_item.get("hook_delay_seconds")) or 0
        first_words = number(content_item.get("first_15s_word_count")) or 0
        overlap = number(content_item.get("title_transcript_overlap"))
        specificity_count = number(content_item.get("specificity_hint_count")) or 0
        transcript_seconds = number(content_item.get("transcript_duration_seconds")) or 0
        specificity_per_minute = specificity_count / (transcript_seconds / 60) if transcript_seconds else None
        density = number(content_item.get("claim_density_per_minute"))
        if hook_delay > 3 or first_words < 20:
            status = "risk"
            detail = "Hook starts slowly or has low first-15s density."
        elif overlap is not None and overlap >= 0.4:
            status = "good"
            detail = "Transcript aligns with the title promise early."
        else:
            status = "watch"
            detail = "Transcript is present; content signal is moderate."
        content_axis = axis_status("Content Quality", status, detail)
        if hook_delay <= 1.5 and first_words >= 20:
            hook_axis = axis_status("Hook Speed", "good", f"Starts at {hook_delay:.1f}s with {first_words:.0f} words in 15s.")
        elif hook_delay > 3 or first_words < 15:
            hook_axis = axis_status("Hook Speed", "risk", f"Starts at {hook_delay:.1f}s with only {first_words:.0f} words in 15s.")
        else:
            hook_axis = axis_status("Hook Speed", "watch", f"Starts at {hook_delay:.1f}s with {first_words:.0f} words in 15s.")
        if overlap is None:
            promise_axis = axis_status("Promise Match", "gap", "Title overlap could not be computed.")
        elif overlap >= 0.45:
            promise_axis = axis_status("Promise Match", "good", f"{overlap * 100:.0f}% of title terms appear in the transcript.")
        elif overlap < 0.2:
            promise_axis = axis_status("Promise Match", "risk", f"Only {overlap * 100:.0f}% title/transcript overlap.")
        else:
            promise_axis = axis_status("Promise Match", "watch", f"{overlap * 100:.0f}% title/transcript overlap.")
        if specificity_per_minute is None:
            specificity_axis = axis_status("Specificity", "gap", "Specificity rate unavailable.")
        elif specificity_per_minute >= 3:
            specificity_axis = axis_status("Specificity", "good", f"{specificity_per_minute:.1f} specificity hints/min.")
        elif specificity_per_minute < 1:
            specificity_axis = axis_status("Specificity", "risk", f"{specificity_per_minute:.1f} specificity hints/min.")
        else:
            specificity_axis = axis_status("Specificity", "watch", f"{specificity_per_minute:.1f} specificity hints/min.")
        if density is None:
            density_axis = axis_status("Claim Density", "gap", "Claim density unavailable.")
        elif 5 <= density <= 16:
            density_axis = axis_status("Claim Density", "good", f"{density:.1f} claims/minute.")
        elif density < 3:
            density_axis = axis_status("Claim Density", "risk", f"{density:.1f} claims/minute.")
        else:
            density_axis = axis_status("Claim Density", "watch", f"{density:.1f} claims/minute.")
        payoff_axis = axis_status(
            "Payoff/CTA",
            "good" if content_item.get("closing_cta_presence") else "watch",
            "Closing CTA detected." if content_item.get("closing_cta_presence") else "No closing CTA detected in local SRT.",
        )
        transcript_axis = axis_status(
            "Transcript Coverage",
            "good" if content_item.get("match_confidence") in {"high", "medium"} else "watch",
            f"{content_item.get('match_confidence', 'unknown')} match: {content_item.get('srt_path', '-')}",
        )

    downstream_clicks = number(funnel.get("known_downstream_clicks")) or 0
    if not item.get("related_video"):
        funnel_status = "gap"
        funnel_detail = "No related-video target recorded."
    elif downstream_clicks >= 3:
        funnel_status = "good"
        funnel_detail = "Known downstream clicks are present."
    else:
        funnel_status = "watch"
        funnel_detail = "Related target exists, but downstream click evidence is low or missing."

    leverage = "ignore"
    for category in ["scale", "clip_more", "funnel_winner", "retitle", "hook_problem", "remaster"]:
        if category in (item.get("categories") or []):
            leverage = category
            break

    axes = {
        "discovery": discovery,
        "retention": retention,
        "length_fit": axis_status("Length Fit", length.get("severity") or "gap", length.get("label") or "Duration missing"),
        "release_timing": axis_status(
            "Release Timing",
            "watch",
            f"{release_timing.get('weekday', 'Unknown')} {release_timing.get('hour_label', '-')}, {release_timing.get('daypart', 'unknown')}",
        ),
        "thumbnail_packaging": packaging,
        "content_quality": content_axis,
        "hook_speed": hook_axis,
        "promise_match": promise_axis,
        "specificity": specificity_axis,
        "claim_density": density_axis,
        "payoff_cta": payoff_axis,
        "transcript_coverage": transcript_axis,
        "funnel_value": axis_status("Funnel Value", funnel_status, funnel_detail),
        "production_leverage": axis_status(
            "Production Leverage",
            "good" if leverage in {"scale", "clip_more", "funnel_winner"} else "risk" if leverage in {"retitle", "hook_problem", "remaster"} else "watch",
            leverage.replace("_", " ").title(),
        ),
    }

    why = []
    if discovery["status"] == "risk":
        why.append(discovery["detail"])
    if retention["status"] == "risk":
        why.append(retention["detail"])
    if length.get("severity") == "risk":
        why.append(f"Duration {item.get('duration_label')} is outside the {length.get('target')} band.")
    if content_axis["status"] == "risk":
        why.append(content_axis["detail"])
    for content_risk_axis in [hook_axis, promise_axis, specificity_axis, density_axis]:
        if content_risk_axis["status"] == "risk" and content_risk_axis["detail"] not in why:
            why.append(content_risk_axis["detail"])
    if not why:
        why.append((item.get("reasons") or ["No single risk dominates; keep monitoring the combined signal."])[0])

    return {
        "video_id": item.get("video_id"),
        "title": item.get("title"),
        "url": item.get("url"),
        "format": item.get("format"),
        "package": item.get("package"),
        "discovery_sources": item.get("discovery_sources") or [],
        "primary_category": item.get("primary_category"),
        "categories": item.get("categories") or [],
        "thumbnail_url": item.get("thumbnail_url"),
        "duration_seconds": item.get("duration_seconds"),
        "duration_label": item.get("duration_label"),
        "length_fit": length,
        "release_timing": release_timing,
        "metrics": metrics,
        "traffic_mix": traffic_mix_for_item(item),
        "shorts_feed_views": shorts_views,
        "title_profile": title,
        "content": content_item,
        "funnel": funnel,
        "related_video": item.get("related_video"),
        "score": item.get("score") or 0,
        "axes": axes,
        "why": why,
        "source_report_links": item.get("source_report_links") or [],
        "playlists": item.get("playlists") or [],
    }


def build_rubric(findings: dict[str, Any], content_rubric: dict[str, Any]) -> dict[str, Any]:
    content_items = content_rubric.get("items") or {}
    items = [
        build_rubric_item(item, content_item=content_items.get(item.get("video_id")))
        for item in findings.get("classifications") or []
    ]
    axis_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for item in items:
        for axis_key, axis in (item.get("axes") or {}).items():
            axis_counts[axis_key][axis.get("status") or "gap"] += 1
    return {
        "items": sorted(items, key=lambda item: (item.get("score") or 0), reverse=True),
        "axis_counts": {key: dict(value) for key, value in axis_counts.items()},
        "content_summary": content_rubric.get("status_counts") or {},
    }


def build_release_rollups(findings: dict[str, Any], *, horizon: str = "weekly") -> dict[str, list[dict[str, Any]]]:
    by_weekday: dict[str, dict[str, Any]] = {}
    by_hour: dict[str, dict[str, Any]] = {}
    by_daypart: dict[str, dict[str, Any]] = {}

    def add(row_map: dict[str, dict[str, Any]], key: str, metrics: dict[str, Any]) -> None:
        row = row_map.setdefault(
            key,
            {
                "name": key,
                "count": 0,
                "views": 0.0,
                "average_view_percentage_sum": 0.0,
                "average_view_percentage_count": 0,
                "ctr_sum": 0.0,
                "ctr_count": 0,
            },
        )
        row["count"] += 1
        row["views"] += number(metrics.get("views")) or 0
        avg = number(metrics.get("averageViewPercentage"))
        if avg is not None:
            row["average_view_percentage_sum"] += avg
            row["average_view_percentage_count"] += 1
        ctr = number(metrics.get("videoThumbnailImpressionsClickRate"))
        impressions = number(metrics.get("videoThumbnailImpressions"))
        if ctr is not None and thumbnail_ctr_is_usable(item, impressions):
            row["ctr_sum"] += ctr
            row["ctr_count"] += 1

    for item in findings.get("classifications") or []:
        timing = item.get("release_timing") or {}
        metrics = item_metrics_for_horizon(item, horizon)
        if not timing:
            continue
        add(by_weekday, timing.get("weekday") or "Unknown", metrics)
        add(by_hour, timing.get("hour_label") or "Unknown", metrics)
        add(by_daypart, timing.get("daypart") or "unknown", metrics)

    def finalize(rows: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
        output = []
        for row in rows.values():
            avg_count = row.pop("average_view_percentage_count")
            avg_sum = row.pop("average_view_percentage_sum")
            ctr_count = row.pop("ctr_count")
            ctr_sum = row.pop("ctr_sum")
            row["average_view_percentage"] = avg_sum / avg_count if avg_count else None
            row["ctr"] = ctr_sum / ctr_count if ctr_count else None
            output.append(row)
        return sorted(output, key=lambda item: (item["views"], item["count"]), reverse=True)

    return {
        "weekday": finalize(by_weekday),
        "hour": finalize(by_hour),
        "daypart": finalize(by_daypart),
    }


def build_length_rollups(findings: dict[str, Any], *, horizon: str = "weekly") -> list[dict[str, Any]]:
    rollups: dict[str, dict[str, Any]] = {}
    for item in findings.get("classifications") or []:
        fit = item.get("length_fit") or {}
        key = fit.get("bucket") or "missing"
        metrics = item_metrics_for_horizon(item, horizon)
        row = rollups.setdefault(key, {"name": fit.get("label") or key, "count": 0, "views": 0.0})
        row["count"] += 1
        row["views"] += number(metrics.get("views")) or 0
    return sorted(rollups.values(), key=lambda row: (row["views"], row["count"]), reverse=True)


def weekly_related_traffic_views(item: dict[str, Any]) -> float:
    return sum(
        number(row.get("views")) or 0
        for row in item.get("traffic_sources") or []
        if row.get("window") == "7d" and row.get("source_type") == "RELATED_VIDEO"
    )


def missing_ctr(item: dict[str, Any], *, horizon: str = "weekly") -> bool:
    metrics = item_metrics_for_horizon(item, horizon)
    return (
        number(metrics.get("videoThumbnailImpressions")) is None
        or number(metrics.get("videoThumbnailImpressionsClickRate")) is None
    )


def confidence_label(item: dict[str, Any], *, horizon: str = "weekly") -> str:
    metrics = item_metrics_for_horizon(item, horizon)
    missing = set(item.get("manual_fields_missing") or [])
    if item.get("data_age_days") is not None and number(item.get("data_age_days")) < 2:
        return "Too young"
    views = number(metrics.get("views")) or 0
    impressions = number(metrics.get("videoThumbnailImpressions")) or 0
    shorts_feed = weekly_shorts_feed_views(item) if item.get("format") == "short" else 0
    if views >= 100 or impressions >= 500 or shorts_feed >= 100:
        return "Strong signal"
    if missing_ctr(item, horizon=horizon):
        return "Missing CTR"
    if missing & STUDIO_CHECK_FIELDS:
        return "Directional"
    return "Directional"


def with_confidence(item: dict[str, Any], *, horizon: str = "weekly") -> dict[str, Any]:
    return {**item, "confidence": confidence_label(item, horizon=horizon)}


def delta_metric(item: dict[str, Any], metric_key: str, *, horizon: str = "weekly") -> float | None:
    if metric_key == "known_downstream_clicks":
        return number((item.get("funnel") or {}).get("known_downstream_clicks"))
    if metric_key == "related_video_traffic_views":
        return weekly_related_traffic_views(item)
    metrics = item_metrics_for_horizon(item, horizon)
    return number(metrics.get(metric_key))


def classification_lookup(snapshot_or_findings: dict[str, Any]) -> dict[str, dict[str, Any]]:
    findings = snapshot_or_findings.get("findings") if isinstance(snapshot_or_findings, dict) else None
    classifications = (findings or snapshot_or_findings).get("classifications") if isinstance(findings or snapshot_or_findings, dict) else []
    return {
        item.get("video_id"): item
        for item in classifications or []
        if item.get("video_id")
    }


def build_delta_rows(
    current_items: list[dict[str, Any]],
    previous_lookup: dict[str, dict[str, Any]],
    *,
    metric_key: str,
    horizon: str = "weekly",
    limit: int = 20,
) -> list[dict[str, Any]]:
    rows = []
    for item in current_items:
        previous = previous_lookup.get(item.get("video_id"))
        if not previous:
            continue
        current_value = delta_metric(item, metric_key, horizon=horizon)
        previous_value = delta_metric(previous, metric_key, horizon=horizon)
        if current_value is None or previous_value is None:
            continue
        delta = current_value - previous_value
        if delta == 0:
            continue
        rows.append(
            {
                "video_id": item.get("video_id"),
                "title": item.get("title"),
                "url": item.get("url"),
                "format": item.get("format"),
                "package": item.get("package"),
                "primary_category": item.get("primary_category"),
                "categories": item.get("categories") or [],
                "confidence": confidence_label(item, horizon=horizon),
                "metric": metric_key,
                "current": current_value,
                "previous": previous_value,
                "delta": delta,
                "percent_change": delta / previous_value * 100 if previous_value else None,
                "metrics": item_metrics_for_horizon(item, horizon),
                "thumbnail_url": item.get("thumbnail_url"),
            }
        )
    return sorted(rows, key=lambda row: abs(row["delta"]), reverse=True)[:limit]


def build_delta_summary(
    findings: dict[str, Any],
    previous_snapshot: dict[str, Any] | None,
    *,
    horizon: str = "weekly",
) -> dict[str, Any]:
    groups = {
        "views_day_movers": {
            "label": "Views/day movers",
            "metric": "views_per_day",
            "tooltip_key": "views_day_movers",
            "items": [],
        },
        "ctr_movers": {
            "label": "CTR movers",
            "metric": "videoThumbnailImpressionsClickRate",
            "tooltip_key": "ctr_movers",
            "items": [],
        },
        "retention_movers": {
            "label": "Retention movers",
            "metric": "averageViewPercentage",
            "tooltip_key": "retention_movers",
            "items": [],
        },
        "subscriber_movers": {
            "label": "Subscriber movers",
            "metric": "subscribersGained",
            "tooltip_key": "subscriber_movers",
            "items": [],
        },
        "funnel_movers": {
            "label": "Funnel movers",
            "metric": "known_downstream_clicks",
            "tooltip_key": "funnel_movers",
            "items": [],
        },
    }
    if not previous_snapshot:
        return {
            "status": "no_previous_snapshot",
            "description": "No previous refresh snapshot is available yet.",
            "previous_generated_at": None,
            "default_group": "views_day_movers",
            "groups": groups,
            "largest_movement": None,
        }
    previous_lookup = classification_lookup(previous_snapshot)
    current_items = findings.get("classifications") or []
    for group in groups.values():
        group["items"] = build_delta_rows(
            current_items,
            previous_lookup,
            metric_key=group["metric"],
            horizon=horizon,
        )
        group["count"] = len(group["items"])
    largest = None
    for group_key, group in groups.items():
        for row in group["items"]:
            candidate = {**row, "group": group_key, "group_label": group["label"]}
            if largest is None or abs(candidate["delta"]) > abs(largest["delta"]):
                largest = candidate
    return {
        "status": "ready",
        "description": "Largest meaningful movement since the previous refresh.",
        "previous_generated_at": previous_snapshot.get("generated_at"),
        "default_group": "views_day_movers",
        "groups": groups,
        "largest_movement": largest,
    }


def daily_period_metrics(
    by_day: dict[str, dict[str, Any]],
    days: list[str],
) -> dict[str, Any] | None:
    rows = [by_day[day] for day in days if day in by_day]
    if not rows:
        return None
    views = sum(number((row.get("metrics") or {}).get("views")) or 0 for row in rows)
    watch_minutes = sum(number((row.get("metrics") or {}).get("estimatedMinutesWatched")) or 0 for row in rows)
    subscribers = sum(number((row.get("metrics") or {}).get("subscribersGained")) or 0 for row in rows)
    likes = sum(number((row.get("metrics") or {}).get("likes")) or 0 for row in rows)
    weighted_pct_sum = 0.0
    weighted_pct_views = 0.0
    pct_values = []
    for row in rows:
        metrics = row.get("metrics") or {}
        row_views = number(metrics.get("views")) or 0
        pct = number(metrics.get("averageViewPercentage"))
        if pct is not None:
            pct_values.append(pct)
            if row_views:
                weighted_pct_sum += pct * row_views
                weighted_pct_views += row_views
    day_count = max(len(days), 1)
    return {
        "days_with_rows": len(rows),
        "period_days": day_count,
        "views": views,
        "views_per_day": views / day_count,
        "estimatedMinutesWatched": watch_minutes,
        "averageViewDuration": watch_minutes * 60 / views if views else None,
        "averageViewPercentage": (
            weighted_pct_sum / weighted_pct_views
            if weighted_pct_views
            else sum(pct_values) / len(pct_values)
            if pct_values
            else None
        ),
        "likes": likes,
        "subscribersGained": subscribers,
    }


def daily_comparison_value(metrics: dict[str, Any] | None, metric_key: str) -> float | None:
    if metrics is None:
        if metric_key in {"views", "views_per_day", "estimatedMinutesWatched", "likes", "subscribersGained"}:
            return 0.0
        return None
    return number(metrics.get(metric_key))


def build_daily_movement_rows(
    items: list[dict[str, Any]],
    video_lookup: dict[str, dict[str, Any]],
    *,
    current_days: list[str],
    previous_days: list[str],
    metric_key: str,
    limit: int = 20,
) -> list[dict[str, Any]]:
    rows = []
    for item in items:
        video = video_lookup.get(item.get("video_id"))
        if not video:
            continue
        by_day = daily_rows_by_day(video)
        if not by_day:
            continue
        current_metrics = daily_period_metrics(by_day, current_days)
        previous_metrics = daily_period_metrics(by_day, previous_days)
        if current_metrics is None and previous_metrics is None:
            continue
        current_value = daily_comparison_value(current_metrics, metric_key)
        previous_value = daily_comparison_value(previous_metrics, metric_key)
        if current_value is None or previous_value is None:
            continue
        delta = current_value - previous_value
        if delta == 0:
            continue
        rows.append(
            {
                "video_id": item.get("video_id"),
                "title": item.get("title"),
                "url": item.get("url"),
                "format": item.get("format"),
                "package": item.get("package"),
                "primary_category": item.get("primary_category"),
                "categories": item.get("categories") or [],
                "confidence": confidence_label(item),
                "metric": metric_key,
                "current": current_value,
                "previous": previous_value,
                "delta": delta,
                "percent_change": delta / previous_value * 100 if previous_value else None,
                "current_days_with_rows": (current_metrics or {}).get("days_with_rows", 0),
                "previous_days_with_rows": (previous_metrics or {}).get("days_with_rows", 0),
                "thumbnail_url": item.get("thumbnail_url"),
            }
        )
    return sorted(rows, key=lambda row: abs(row["delta"]), reverse=True)[:limit]


def build_daily_movement_summary(
    videos: list[dict[str, Any]],
    findings: dict[str, Any],
) -> dict[str, Any]:
    all_days = sorted(
        {
            day
            for video in videos
            for day in daily_rows_by_day(video)
        }
    )
    groups = {
        "latest_day_views": {
            "label": "Latest day views",
            "metric": "views",
            "items": [],
        },
        "latest_day_retention": {
            "label": "Latest day retention",
            "metric": "averageViewPercentage",
            "items": [],
        },
        "three_day_views_per_day": {
            "label": "3-day views/day",
            "metric": "views_per_day",
            "items": [],
        },
        "seven_day_views_per_day": {
            "label": "7-day views/day",
            "metric": "views_per_day",
            "items": [],
        },
    }
    if len(all_days) < 2:
        return {
            "status": "insufficient_daily_rows",
            "description": "Not enough Analytics daily rows are available yet.",
            "latest_day": all_days[-1] if all_days else None,
            "groups": groups,
            "largest_movement": None,
        }
    video_lookup = {video.get("video_id"): video for video in videos}
    items = findings.get("classifications") or []
    latest_day = all_days[-1]
    previous_day = all_days[-2]
    period_specs = {
        "latest_day_views": ([latest_day], [previous_day]),
        "latest_day_retention": ([latest_day], [previous_day]),
        "three_day_views_per_day": (all_days[-3:], all_days[-6:-3]),
        "seven_day_views_per_day": (all_days[-7:], all_days[-14:-7]),
    }
    for group_key, group in groups.items():
        current_days, previous_days = period_specs[group_key]
        if not current_days or not previous_days:
            continue
        group["current_days"] = current_days
        group["previous_days"] = previous_days
        group["items"] = build_daily_movement_rows(
            items,
            video_lookup,
            current_days=current_days,
            previous_days=previous_days,
            metric_key=group["metric"],
        )
        group["count"] = len(group["items"])
    largest = None
    for group_key, group in groups.items():
        for row in group["items"]:
            candidate = {**row, "group": group_key, "group_label": group["label"]}
            if largest is None or abs(candidate["delta"]) > abs(largest["delta"]):
                largest = candidate
    return {
        "status": "ready",
        "description": "Movement computed from recent YouTube Analytics daily rows.",
        "latest_day": latest_day,
        "previous_day": previous_day,
        "available_day_count": len(all_days),
        "available_days": all_days,
        "default_group": "seven_day_views_per_day" if groups["seven_day_views_per_day"]["items"] else "latest_day_views",
        "groups": groups,
        "largest_movement": largest,
    }


def build_packaging_lab(findings: dict[str, Any], *, horizon: str = "weekly") -> dict[str, Any]:
    buckets = {
        "high_impression_low_ctr": {
            "label": "High impressions / low CTR",
            "tooltip_key": "high_impression_low_ctr",
            "items": [],
        },
        "low_impression_high_retention": {
            "label": "Low impressions / high retention",
            "tooltip_key": "low_impression_high_retention",
            "items": [],
        },
        "shorts_feed_thumbnail_mismatch": {
            "label": "Shorts feed / thumbnail mismatch",
            "tooltip_key": "shorts_feed_thumbnail_mismatch",
            "items": [],
        },
        "title_too_broad": {
            "label": "Title too broad",
            "tooltip_key": "title_too_broad",
            "items": [],
        },
        "title_too_long": {
            "label": "Title too long",
            "tooltip_key": "title_too_long",
            "items": [],
        },
        "weak_thumbnail_metadata": {
            "label": "Weak thumbnail metadata",
            "tooltip_key": "weak_thumbnail_metadata",
            "items": [],
        },
    }
    for item in findings.get("classifications") or []:
        metrics = item_metrics_for_horizon(item, horizon)
        impressions = number(metrics.get("videoThumbnailImpressions"))
        ctr = number(metrics.get("videoThumbnailImpressionsClickRate"))
        retention = number(metrics.get("averageViewPercentage"))
        profile = item.get("title_profile") or {}
        enriched = with_confidence(item, horizon=horizon)
        shorts_mismatch = is_shorts_thumbnail_mismatch(item, impressions)
        if impressions is not None and impressions >= 500 and ctr is not None and ctr < 3:
            buckets["high_impression_low_ctr"]["items"].append(enriched)
        if shorts_mismatch:
            buckets["shorts_feed_thumbnail_mismatch"]["items"].append(enriched)
        if (
            not shorts_mismatch
            and impressions is not None
            and impressions < 150
            and retention is not None
            and retention >= 55
        ):
            buckets["low_impression_high_retention"]["items"].append(enriched)
        if (profile.get("specificity_score") or 0) <= 4 or (profile.get("word_count") or 0) <= 4:
            buckets["title_too_broad"]["items"].append(enriched)
        if (profile.get("character_count") or 0) >= 85 or (profile.get("word_count") or 0) >= 14:
            buckets["title_too_long"]["items"].append(enriched)
        if not item.get("thumbnail_url") or impressions is None or ctr is None:
            buckets["weak_thumbnail_metadata"]["items"].append(enriched)
    for bucket in buckets.values():
        bucket["items"].sort(
            key=lambda row: (
                number(item_metrics_for_horizon(row, horizon).get("videoThumbnailImpressions")) or 0,
                number(item_metrics_for_horizon(row, horizon).get("views")) or 0,
            ),
            reverse=True,
        )
        bucket["count"] = len(bucket["items"])
    return {"default_bucket": "high_impression_low_ctr", "buckets": buckets}


def build_funnel_map(findings: dict[str, Any], funnel_rollups: dict[str, Any]) -> dict[str, Any]:
    buckets = {
        "shorts_to_related": {
            "label": "Shorts -> related target",
            "items": [],
        },
        "card_clicks": {
            "label": "Card clicks",
            "items": [],
        },
        "end_screen_clicks": {
            "label": "End-screen clicks",
            "items": [],
        },
        "related_video_traffic": {
            "label": "Related-video traffic",
            "items": [],
        },
        "parent_receivers": {
            "label": "Parent video receivers",
            "items": funnel_rollups.get("parents") or [],
        },
    }
    for item in findings.get("classifications") or []:
        funnel = item.get("funnel") or {}
        related_traffic = weekly_related_traffic_views(item)
        enriched = {
            **with_confidence(item),
            "related_video_traffic_views": related_traffic,
        }
        if item.get("format") == "short" and item.get("related_video"):
            buckets["shorts_to_related"]["items"].append(enriched)
        if number(funnel.get("card_clicks")):
            buckets["card_clicks"]["items"].append(enriched)
        if number(funnel.get("end_screen_clicks")):
            buckets["end_screen_clicks"]["items"].append(enriched)
        if related_traffic:
            buckets["related_video_traffic"]["items"].append(enriched)
    for key, bucket in buckets.items():
        if key == "parent_receivers":
            bucket["count"] = len(bucket["items"])
            continue
        bucket["items"].sort(
            key=lambda row: (
                number((row.get("funnel") or {}).get("known_downstream_clicks")) or 0,
                number(row.get("related_video_traffic_views")) or 0,
            ),
            reverse=True,
        )
        bucket["count"] = len(bucket["items"])
    return {
        "default_bucket": "shorts_to_related",
        "tooltip_key": "funnel_map",
        "totals": funnel_rollups.get("totals") or {},
        "buckets": buckets,
    }


TOPIC_KEYWORDS = {
    "agents": ["agent", "agents", "autonomous", "autonomy"],
    "memory": ["memory", "recall", "context", "forget"],
    "safety": ["safety", "security", "trust", "risk", "guardrail", "alignment"],
    "optimization": ["optimization", "optimize", "scheduler", "search", "performance"],
    "reasoning": ["reasoning", "scaffold", "plan", "deliberation", "logic"],
    "action": ["action", "act", "tool", "control", "execute"],
    "multi-agent": ["multi-agent", "swarm", "orchestration", "coordination", "agents"],
    "architecture": ["architecture", "scaffold", "system", "design", "pattern"],
    "confidence debt": ["confidence", "debt", "calibration", "uncertainty"],
    "neural architecture": ["neural", "architecture", "compositional", "circuit"],
    "binding gap": ["binding", "gap", "representation"],
    "course": ["course", "lesson", "curriculum", "rooted"],
    "podcast": ["podcast", "conversation", "interview"],
}


def topic_cluster_for_item(item: dict[str, Any], content_item: dict[str, Any] | None = None) -> str:
    content_item = content_item or {}
    hints = " ".join(str(value) for value in content_item.get("specificity_hints") or [])
    text = f"{item.get('title') or ''} {item.get('package') or ''} {hints}".lower()
    scores = {}
    for topic, terms in TOPIC_KEYWORDS.items():
        scores[topic] = sum(1 for term in terms if term in text)
    best_topic, best_score = max(scores.items(), key=lambda pair: pair[1])
    if best_score:
        return best_topic
    package = str(item.get("package") or "").strip("/")
    if package and package != "unknown":
        return package.split("/")[0].replace("-", " ")
    return "unknown"


def build_topic_clusters(
    findings: dict[str, Any],
    content_rubric: dict[str, Any],
    *,
    horizon: str = "weekly",
) -> dict[str, Any]:
    content_items = content_rubric.get("items") or {}
    clusters: dict[str, dict[str, Any]] = {}
    for item in findings.get("classifications") or []:
        content_item = content_items.get(item.get("video_id")) or {}
        cluster_name = topic_cluster_for_item(item, content_item)
        metrics = item_metrics_for_horizon(item, horizon)
        row = clusters.setdefault(
            cluster_name,
            {
                "cluster": cluster_name,
                "video_count": 0,
                "action_items": 0,
                "views": 0.0,
                "views_per_day": 0.0,
                "retention_sum": 0.0,
                "retention_count": 0,
                "ctr_sum": 0.0,
                "ctr_count": 0,
                "subscribers_gained": 0.0,
                "production_queue_pressure": 0,
                "top_videos": [],
            },
        )
        row["video_count"] += 1
        row["action_items"] += 1 if any(category != "ignore" for category in item.get("categories") or []) else 0
        row["views"] += number(metrics.get("views")) or 0
        row["views_per_day"] += number(metrics.get("views_per_day")) or 0
        row["subscribers_gained"] += number(metrics.get("subscribersGained")) or 0
        row["production_queue_pressure"] += len([category for category in item.get("categories") or [] if category != "ignore"])
        retention = number(metrics.get("averageViewPercentage"))
        if retention is not None:
            row["retention_sum"] += retention
            row["retention_count"] += 1
        ctr = number(metrics.get("videoThumbnailImpressionsClickRate"))
        impressions = number(metrics.get("videoThumbnailImpressions"))
        if ctr is not None and thumbnail_ctr_is_usable(item, impressions):
            row["ctr_sum"] += ctr
            row["ctr_count"] += 1
        row["top_videos"].append(
            {
                "video_id": item.get("video_id"),
                "title": item.get("title"),
                "url": item.get("url"),
                "views": number(metrics.get("views")) or 0,
                "primary_category": item.get("primary_category"),
            }
        )
    rows = []
    for row in clusters.values():
        retention_count = row.pop("retention_count")
        retention_sum = row.pop("retention_sum")
        ctr_count = row.pop("ctr_count")
        ctr_sum = row.pop("ctr_sum")
        row["average_view_percentage"] = retention_sum / retention_count if retention_count else None
        row["ctr"] = ctr_sum / ctr_count if ctr_count else None
        row["top_videos"] = sorted(row["top_videos"], key=lambda video: video["views"], reverse=True)[:5]
        rows.append(row)
    return {
        "default_sort": "views",
        "tooltip_key": "topic_clusters",
        "clusters": sorted(rows, key=lambda row: (row["views"], row["action_items"]), reverse=True),
    }


def build_release_time_lab(findings: dict[str, Any], *, horizon: str = "weekly") -> dict[str, Any]:
    items = findings.get("classifications") or []
    by_format = {}
    for format_name in sorted({item.get("format") or "unknown" for item in items}):
        by_format[format_name] = build_release_rollups(
            {"classifications": [item for item in items if (item.get("format") or "unknown") == format_name]},
            horizon=horizon,
        )
    young_excluded = [
        item
        for item in items
        if item.get("data_age_days") is None or number(item.get("data_age_days")) >= 2
    ]
    return {
        "timezone": DEFAULT_RELEASE_TIMEZONE,
        "default_mode": "weekday",
        "tooltip_key": "release_time_lab",
        "all": build_release_rollups(findings, horizon=horizon),
        "by_format": by_format,
        "young_excluded": build_release_rollups({"classifications": young_excluded}, horizon=horizon),
        "insights": build_release_time_insights(findings, horizon=horizon),
    }


def best_release_cohort(rows: list[dict[str, Any]], *, min_count: int = 2) -> dict[str, Any] | None:
    eligible = [row for row in rows if (row.get("count") or 0) >= min_count]
    if not eligible:
        eligible = rows
    if not eligible:
        return None
    best = max(eligible, key=lambda row: (number(row.get("views")) or 0) / max(number(row.get("count")) or 1, 1))
    return {
        **best,
        "views_per_video": (number(best.get("views")) or 0) / max(number(best.get("count")) or 1, 1),
        "sample_warning": (best.get("count") or 0) < min_count,
    }


def build_release_time_insights(findings: dict[str, Any], *, horizon: str = "weekly") -> dict[str, Any]:
    rollups = build_release_rollups(findings, horizon=horizon)
    weekday = best_release_cohort(rollups.get("weekday") or [])
    hour = best_release_cohort(rollups.get("hour") or [])
    daypart = best_release_cohort(rollups.get("daypart") or [])
    return {
        "timezone": DEFAULT_RELEASE_TIMEZONE,
        "horizon": horizon,
        "best_weekday": weekday,
        "best_hour": hour,
        "best_daypart": daypart,
        "summary": (
            f"{(daypart or {}).get('name', 'No daypart')} is the strongest current daypart by views/video."
            if daypart
            else "Not enough release-time data for a directional read."
        ),
    }


def recommended_queue_action(item: dict[str, Any], *, horizon: str = "weekly") -> tuple[str, str]:
    metrics = item_metrics_for_horizon(item, horizon)
    impressions = number(metrics.get("videoThumbnailImpressions"))
    ctr = number(metrics.get("videoThumbnailImpressionsClickRate"))
    categories = set(item.get("categories") or [])
    if impressions is not None and impressions >= 500 and ctr is not None and ctr < 3:
        return "thumbnail_review", "YouTube has shown it enough times; packaging conversion is the constraint."
    if "retitle" in categories:
        return "retitle", "CTR/packaging signal points to title or promise work."
    if "remaster" in categories:
        return "remaster", "Topic has demand but the Short likely needs the overlay remaster format."
    if "clip_more" in categories:
        return "clip_more", "Parent performance suggests more Shorts can be extracted."
    if categories & {"scale", "funnel_winner"}:
        return "make_sequel", "Current performance is strong enough to produce a related follow-up."
    if "hook_problem" in categories:
        return "remaster" if item.get("format") == "short" else "retitle", "Viewers start but retention weakens; fix hook/expectation match."
    if item.get("data_age_days") is not None and number(item.get("data_age_days")) < 2:
        return "wait", "The video is too young for a fair read."
    if missing_ctr(item, horizon=horizon):
        return "wait", "CTR/impressions are still missing, so packaging judgment should wait."
    return "ignore", "No useful production action is currently indicated."


def build_production_queue(findings: dict[str, Any], *, horizon: str = "weekly") -> dict[str, Any]:
    priority = {
        "thumbnail_review": 700,
        "retitle": 650,
        "remaster": 600,
        "clip_more": 520,
        "make_sequel": 500,
        "wait": 120,
        "ignore": 0,
    }
    rows = []
    for item in findings.get("classifications") or []:
        metrics = item_metrics_for_horizon(item, horizon)
        action, reason = recommended_queue_action(item, horizon=horizon)
        confidence = confidence_label(item, horizon=horizon)
        score = (
            priority[action]
            + (number(metrics.get("views_per_day")) or 0) * 10
            + (number(metrics.get("views")) or 0) / 100
            + (number(metrics.get("averageViewPercentage")) or 0)
            + (number(metrics.get("subscribersGained")) or 0) * 20
        )
        if confidence in {"Missing CTR", "Needs Studio/manual data", "Too young"}:
            score -= 50
        rows.append(
            {
                "video_id": item.get("video_id"),
                "title": item.get("title"),
                "url": item.get("url"),
                "format": item.get("format"),
                "package": item.get("package"),
                "primary_category": item.get("primary_category"),
                "categories": item.get("categories") or [],
                "thumbnail_url": item.get("thumbnail_url"),
                "traffic_sources": item.get("traffic_sources") or [],
                "shorts_feed_views": weekly_shorts_feed_views(item),
                "action": action,
                "reason": reason,
                "confidence": confidence,
                "score": score,
                "metrics": metrics,
            }
        )
    rows.sort(
        key=lambda row: (
            0 if row["action"] not in WATCH_ACTIONS else 1,
            -(row["score"] or 0),
        )
    )
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        buckets[row["action"]].append(row)
    return {
        "default_action": "all",
        "tooltip_key": "production_queue",
        "items": rows,
        "buckets": {key: value for key, value in buckets.items()},
    }


def build_experiments(registry: dict[str, Any], findings: dict[str, Any], *, horizon: str = "weekly") -> dict[str, Any]:
    lookup = {item.get("video_id"): item for item in findings.get("classifications") or []}
    active_statuses = {"active", "running", "in_progress"}
    status_order = {"active": 0, "running": 0, "in_progress": 0, "planned": 1, "paused": 2, "completed": 3, "archived": 4}
    experiments = []
    for experiment in registry.get("experiments") or []:
        cohort = [lookup[video_id] for video_id in experiment.get("video_ids") or [] if video_id in lookup]
        metrics_rows = [item_metrics_for_horizon(item, horizon) for item in cohort]
        total_views = sum(number(metrics.get("views")) or 0 for metrics in metrics_rows)
        total_views_per_day = sum(number(metrics.get("views_per_day")) or 0 for metrics in metrics_rows)
        total_subscribers = sum(number(metrics.get("subscribersGained")) or 0 for metrics in metrics_rows)
        retention_values = [number(metrics.get("averageViewPercentage")) for metrics in metrics_rows if number(metrics.get("averageViewPercentage")) is not None]
        ctr_values = [
            number(metrics.get("videoThumbnailImpressionsClickRate"))
            for item, metrics in zip(cohort, metrics_rows)
            if number(metrics.get("videoThumbnailImpressionsClickRate")) is not None
            and thumbnail_ctr_is_usable(item, number(metrics.get("videoThumbnailImpressions")))
        ]
        status = str(experiment.get("status") or "planned")
        experiments.append(
            {
                **experiment,
                "active": status in active_statuses,
                "cohort_found": len(cohort),
                "cohort_missing": [video_id for video_id in experiment.get("video_ids") or [] if video_id not in lookup],
                "current_read": {
                    "video_count": len(cohort),
                    "views": total_views,
                    "views_per_day": total_views_per_day,
                    "average_view_percentage": sum(retention_values) / len(retention_values) if retention_values else None,
                    "ctr": sum(ctr_values) / len(ctr_values) if ctr_values else None,
                    "subscribers_gained": total_subscribers,
                },
                "videos": [
                    {
                        "video_id": item.get("video_id"),
                        "title": item.get("title"),
                        "url": item.get("url"),
                        "primary_category": item.get("primary_category"),
                    }
                    for item in cohort
                ],
            }
        )
    experiments.sort(key=lambda item: (status_order.get(item.get("status"), 9), item.get("start_date") or ""), reverse=False)
    return {
        "source_path": registry.get("source_path"),
        "default_filter": "active",
        "tooltip_key": "experiment_registry",
        "experiments": experiments,
        "counts": dict(Counter(experiment.get("status") or "planned" for experiment in experiments)),
    }


def repo_relative(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def load_weekly_report_summaries(report_dir: Path = DEFAULT_WEEKLY_REPORT_DIR) -> list[dict[str, Any]]:
    reports = []
    for path in sorted(report_dir.glob("*.json")):
        payload = load_json(path)
        reports.append(
            {
                "path": repo_relative(path),
                "report_date": payload.get("report_date") or path.stem,
                "payload": payload,
            }
        )
    reports.sort(key=lambda item: item["report_date"], reverse=True)
    return reports


def load_snapshot_records(snapshot_dir: Path = DEFAULT_SNAPSHOT_DIR) -> list[dict[str, Any]]:
    records = []
    for path in sorted(snapshot_dir.glob("*.json")):
        if path.name == "latest.json":
            continue
        try:
            payload = load_json(path)
        except json.JSONDecodeError:
            continue
        records.append(
            {
                "path": repo_relative(path),
                "generated_at": payload.get("generated_at") or "",
                "report_date": (payload.get("report") or {}).get("report_date"),
                "payload": payload,
            }
        )
    records.sort(key=lambda item: (item.get("generated_at") or "", item.get("path") or ""))
    return records


def previous_snapshot_for_report(
    report_date: str | None,
    snapshot_records: list[dict[str, Any]],
) -> dict[str, Any] | None:
    if not report_date:
        return None
    matching_indexes = [
        index
        for index, record in enumerate(snapshot_records)
        if record.get("report_date") == report_date
    ]
    if matching_indexes:
        index = matching_indexes[-1]
        if index > 0:
            return snapshot_records[index - 1]["payload"]
        return None
    earlier = [
        record
        for record in snapshot_records
        if record.get("report_date") and str(record["report_date"]) < str(report_date)
    ]
    return earlier[-1]["payload"] if earlier else None


def latest_snapshot_for_report(
    report_date: str | None,
    snapshot_records: list[dict[str, Any]],
) -> dict[str, Any] | None:
    if not report_date:
        return None
    matching = [
        record["payload"]
        for record in snapshot_records
        if record.get("report_date") == report_date
    ]
    return matching[-1] if matching else None


def metric_pack(item: dict[str, Any], *, horizon: str) -> dict[str, Any]:
    metrics = item_metrics_for_horizon(item, horizon)
    return {
        "views": number(metrics.get("views")),
        "views_per_day": number(metrics.get("views_per_day")),
        "estimatedMinutesWatched": number(metrics.get("estimatedMinutesWatched")),
        "averageViewDuration": number(metrics.get("averageViewDuration")),
        "averageViewPercentage": number(metrics.get("averageViewPercentage")),
        "likes": number(metrics.get("likes")),
        "comments": number(metrics.get("comments")),
        "shares": number(metrics.get("shares")),
        "subscribersGained": number(metrics.get("subscribersGained")),
        "subscribers_per_1000_views": number(metrics.get("subscribers_per_1000_views")),
        "videoThumbnailImpressions": number(metrics.get("videoThumbnailImpressions")),
        "videoThumbnailImpressionsClickRate": number(metrics.get("videoThumbnailImpressionsClickRate")),
    }


def compact_horizon_metrics(item: dict[str, Any]) -> dict[str, Any]:
    compact = {}
    for horizon in HORIZONS:
        source = (item.get("horizon_metrics") or {}).get(horizon) or {}
        compact[horizon] = {
            "available": bool(source.get("available")),
            "window": source.get("window"),
            "start_date": source.get("start_date"),
            "end_date": source.get("end_date"),
            "day": source.get("day"),
            "metrics": metric_pack(item, horizon=horizon),
            "confidence": confidence_label(item, horizon=horizon),
        }
    return compact


def item_primary_action_text(item: dict[str, Any], action: str) -> str:
    if item.get("actions_by_category"):
        categories = item.get("categories") or []
        for category in categories:
            action_text = (item.get("actions_by_category") or {}).get(category)
            if action_text:
                return action_text
    if item.get("recommended_actions"):
        return item["recommended_actions"][0]
    if action == "make_sequel":
        return "Produce a related follow-up while the topic is warm."
    if action == "thumbnail_review":
        return "Draft a sharper title and thumbnail variant before changing the video."
    if action == "remaster":
        return "Queue a remaster instead of treating this as a failed topic."
    if action == "retitle":
        return "Rewrite the title/promise and review the opening hook."
    if action == "wait":
        return "Wait for a fuller data window before acting."
    return "Keep it in the watchlist until a stronger pattern appears."


def item_caveats(item: dict[str, Any], *, horizon: str = "weekly") -> list[str]:
    metrics = item_metrics_for_horizon(item, horizon)
    impressions = number(metrics.get("videoThumbnailImpressions"))
    caveats = []
    missing = set(item.get("manual_fields_missing") or [])
    if item.get("data_age_days") is not None and number(item.get("data_age_days")) < 2:
        caveats.append("too young for a fair read")
    if missing_ctr(item, horizon=horizon):
        caveats.append("CTR/impression data missing")
    elif impressions is not None and impressions < MIN_THUMBNAIL_CTR_SAMPLE:
        caveats.append("tiny thumbnail sample; use retention and traffic source")
    if missing & STUDIO_CHECK_FIELDS:
        caveats.append("Studio downstream fields missing")
    return caveats


def compact_queue_item(row: dict[str, Any], *, source_item: dict[str, Any] | None = None) -> dict[str, Any]:
    item = source_item or row
    action = row.get("action") or recommended_queue_action(item)[0]
    return {
        "video_id": item.get("video_id"),
        "title": item.get("title"),
        "url": item.get("url"),
        "format": item.get("format"),
        "package": item.get("package"),
        "topic": item.get("topic") or item.get("package"),
        "primary_category": item.get("primary_category"),
        "categories": item.get("categories") or [],
        "thumbnail_url": item.get("thumbnail_url"),
        "published_at": item.get("published_at"),
        "data_age_days": item.get("data_age_days"),
        "action": action,
        "action_label": QUEUE_ACTION_LABELS.get(action, action.replace("_", " ").title()),
        "reason": row.get("reason") or "",
        "next_step": item_primary_action_text(item, action),
        "confidence": row.get("confidence") or confidence_label(item),
        "caveats": item_caveats(item),
        "score": number(row.get("score")) or number(item.get("score")) or 0,
        "shorts_feed_views": number(row.get("shorts_feed_views")) or weekly_shorts_feed_views(item),
        "horizon_metrics": compact_horizon_metrics(item),
        "funnel": item.get("funnel") or {},
    }


def compact_video_item(item: dict[str, Any]) -> dict[str, Any]:
    action, reason = recommended_queue_action(item)
    return compact_queue_item(
        {
            "action": action,
            "reason": reason,
            "confidence": confidence_label(item),
            "score": item.get("score") or 0,
            "shorts_feed_views": weekly_shorts_feed_views(item),
        },
        source_item=item,
    )


def evidence_text(item: dict[str, Any], *, horizon: str = "weekly") -> str:
    metrics = item_metrics_for_horizon(item, horizon)
    parts = []
    views = number(metrics.get("views"))
    vpd = number(metrics.get("views_per_day"))
    retention = number(metrics.get("averageViewPercentage"))
    subscribers = number(metrics.get("subscribersGained"))
    impressions = number(metrics.get("videoThumbnailImpressions"))
    ctr = number(metrics.get("videoThumbnailImpressionsClickRate"))
    if views is not None:
        parts.append(f"{views:g} views")
    if vpd is not None:
        parts.append(f"{vpd:.1f}/day")
    if retention is not None:
        parts.append(f"{retention:.1f}% avg viewed")
    if subscribers:
        parts.append(f"+{subscribers:g} subs")
    if item.get("format") == "short":
        shorts_views = weekly_shorts_feed_views(item)
        if shorts_views:
            parts.append(f"{shorts_views:g} Shorts-feed views")
    if impressions is not None and ctr is not None and impressions >= MIN_THUMBNAIL_CTR_SAMPLE:
        parts.append(f"{impressions:g} impressions at {ctr:.1f}% CTR")
    return " | ".join(parts) if parts else "No usable metric row yet."


def build_decision_memos(
    findings: dict[str, Any],
    queue: dict[str, Any],
    *,
    horizon: str = "weekly",
    limit: int = 5,
) -> list[dict[str, Any]]:
    lookup = {item.get("video_id"): item for item in findings.get("classifications") or []}
    actionable_rows = [
        row
        for row in queue.get("items") or []
        if row.get("action") not in WATCH_ACTIONS
    ]
    memos = []
    seen: set[str] = set()
    for row in actionable_rows:
        source = lookup.get(row.get("video_id")) or row
        compact = compact_queue_item(row, source_item=source)
        compact["decision"] = compact["action_label"]
        compact["evidence"] = evidence_text(source, horizon=horizon)
        memos.append(compact)
        seen.add(compact["video_id"])
        if len(memos) >= limit:
            break

    if len(memos) < 3:
        for row in queue.get("items") or []:
            if row.get("video_id") in seen or row.get("action") != "ignore":
                continue
            source = lookup.get(row.get("video_id")) or row
            compact = compact_queue_item(row, source_item=source)
            compact["decision"] = "Watch momentum"
            compact["evidence"] = evidence_text(source, horizon=horizon)
            memos.append(compact)
            if len(memos) >= min(limit, 3):
                break
    return memos


def queue_sections(findings: dict[str, Any], queue: dict[str, Any]) -> dict[str, dict[str, Any]]:
    lookup = {item.get("video_id"): item for item in findings.get("classifications") or []}

    def compact_rows(actions: set[str], limit: int) -> list[dict[str, Any]]:
        rows = []
        for row in queue.get("items") or []:
            if row.get("action") not in actions:
                continue
            source = lookup.get(row.get("video_id")) or row
            rows.append(compact_queue_item(row, source_item=source))
            if len(rows) >= limit:
                break
        return rows

    return {
        "production": {
            "label": "Production queue",
            "description": "Make more of what is working.",
            "items": compact_rows(PRODUCTION_ACTIONS, 12),
        },
        "fix": {
            "label": "Fix queue",
            "description": "Repair packaging, hook, or format before producing another variant.",
            "items": compact_rows(FIX_ACTIONS, 16),
        },
        "watchlist": {
            "label": "Watchlist",
            "description": "Momentum or low-signal items that should not displace action items.",
            "items": compact_rows(WATCH_ACTIONS, 20),
        },
    }


def compact_rollup_rows(rows: list[dict[str, Any]], *, limit: int = 12) -> list[dict[str, Any]]:
    return rows[:limit]


def build_report_state(
    ledger: dict[str, Any],
    report_summary: dict[str, Any],
    reporting_jobs: dict[str, Any] | None,
    content_rubric: dict[str, Any],
    experiment_registry: dict[str, Any],
    source_snapshot: dict[str, Any] | None,
    previous_snapshot: dict[str, Any] | None,
    *,
    use_ledger_metrics: bool = False,
) -> dict[str, Any]:
    videos = ledger.get("videos") or []
    findings = summarize_findings(
        report_summary,
        videos,
        source_snapshot,
        use_ledger_metrics=use_ledger_metrics,
    )
    queue = build_production_queue(findings, horizon="weekly")
    funnel_rollups = build_funnel_rollups(findings)
    package_rollups = build_package_rollups_by_horizon(findings)
    playlist_rollups = build_playlist_rollups_by_horizon(findings)
    release_lab = build_release_time_lab(findings, horizon="weekly")
    topic_clusters = build_topic_clusters(findings, content_rubric, horizon="weekly")
    experiments = build_experiments(experiment_registry, findings, horizon="weekly")
    reporting_job_rows = [
        {
            "key": key,
            "name": job.get("name"),
            "report_type_id": job.get("report_type_id"),
            "available_report_count": job.get("available_report_count", 0),
            "downloaded_report_count": job.get("downloaded_report_count", 0),
            "latest_report_end_time": job.get("latest_report_end_time"),
            "purpose": job.get("purpose"),
        }
        for key, job in sorted(((reporting_jobs or {}).get("jobs") or {}).items())
    ]
    compact_videos = [compact_video_item(item) for item in findings.get("classifications") or []]
    return {
        "report": {
            "report_date": report_summary.get("report_date"),
            "created_at": report_summary.get("created_at"),
            "analytics_end_date": report_summary.get("analytics_end_date"),
            "read_only": report_summary.get("read_only", True),
        },
        "summary_counts": findings.get("summary_counts") or {},
        "totals": {
            "videos": len(findings.get("classifications") or []),
            "actionable_videos": len(findings.get("action_items") or []),
            "ignored_count": findings.get("ignored_count", 0),
            "waiting_for_ctr": sum(1 for item in compact_videos if "CTR/impression data missing" in item.get("caveats", [])),
            "needs_studio_check": sum(1 for item in compact_videos if "Studio downstream fields missing" in item.get("caveats", [])),
        },
        "horizon_summaries": build_horizon_summaries(findings),
        "decision_memos": build_decision_memos(findings, queue, horizon="weekly"),
        "queues": queue_sections(findings, queue),
        "videos": compact_videos,
        "reports": {
            "delta_summary": build_delta_summary(findings, previous_snapshot, horizon="weekly"),
            "daily_movement": build_daily_movement_summary(videos, findings),
        },
        "evidence": {
            "package_rollups_by_horizon": {key: compact_rollup_rows(value) for key, value in package_rollups.items()},
            "playlist_rollups_by_horizon": {key: compact_rollup_rows(value) for key, value in playlist_rollups.items()},
            "traffic_sources_by_horizon": summarize_traffic_by_horizon(findings.get("classifications") or []),
            "coverage": {
                "windows": summarize_windows(videos),
                "metrics": summarize_metric_availability(videos),
                "manual_fields": summarize_manual_availability(videos),
            },
            "reporting_jobs": reporting_job_rows,
            "release_time_lab": release_lab,
            "topic_clusters": {
                **topic_clusters,
                "clusters": compact_rollup_rows(topic_clusters.get("clusters") or [], limit=12),
            },
            "experiments": {
                **experiments,
                "experiments": compact_rollup_rows(experiments.get("experiments") or [], limit=12),
            },
            "funnel_rollups": funnel_rollups,
        },
    }


def build_report_states(
    ledger: dict[str, Any],
    report_summaries: list[dict[str, Any]],
    reporting_jobs: dict[str, Any] | None,
    content_rubric: dict[str, Any],
    experiment_registry: dict[str, Any],
    snapshot_records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    states = []
    newest_report_date = max((report.get("report_date") or "" for report in report_summaries), default="")
    for report in report_summaries:
        payload = report["payload"]
        report_date = report.get("report_date")
        source_snapshot = latest_snapshot_for_report(report_date, snapshot_records)
        previous_snapshot = previous_snapshot_for_report(report.get("report_date"), snapshot_records)
        state = build_report_state(
            ledger,
            payload,
            reporting_jobs,
            content_rubric,
            experiment_registry,
            source_snapshot,
            previous_snapshot,
            use_ledger_metrics=(report_date == newest_report_date),
        )
        state["source_path"] = report.get("path")
        states.append(state)
    states.sort(key=lambda item: (item.get("report") or {}).get("report_date") or "", reverse=True)
    return states


def compact_snapshot_payload(payload: dict[str, Any]) -> dict[str, Any]:
    classifications = []
    for item in (payload.get("findings") or {}).get("classifications") or []:
        classifications.append(
            {
                "video_id": item.get("video_id"),
                "title": item.get("title"),
                "url": item.get("url"),
                "format": item.get("format"),
                "package": item.get("package"),
                "primary_category": item.get("primary_category"),
                "categories": item.get("categories") or [],
                "horizon_metrics": item.get("horizon_metrics") or {},
                "funnel": item.get("funnel") or {},
                "traffic_sources": item.get("traffic_sources") or [],
                "thumbnail_url": item.get("thumbnail_url"),
            }
        )
    return {
        "generated_at": payload.get("generated_at"),
        "report": payload.get("report") or {},
        "ledger": payload.get("ledger") or {},
        "totals": payload.get("totals") or {},
        "horizon_summaries": payload.get("horizon_summaries") or {},
        "findings": {"classifications": classifications},
        "funnel_rollups": payload.get("funnel_rollups") or {},
    }


def build_playlist_inventory(
    ledger: dict[str, Any],
    findings: dict[str, Any],
    *,
    horizon: str = "weekly",
) -> list[dict[str, Any]]:
    stats: dict[str, dict[str, Any]] = {}
    for item in findings.get("classifications") or []:
        metrics = item_metrics_for_horizon(item, horizon)
        for playlist in item.get("playlists") or []:
            playlist_id = playlist.get("id")
            if not playlist_id:
                continue
            row = stats.setdefault(
                playlist_id,
                {
                    "in_scope_video_count": 0,
                    "action_items": 0,
                    "total_views": 0.0,
                },
            )
            row["in_scope_video_count"] += 1
            row["total_views"] += number(metrics.get("views")) or 0
            if any(category != "ignore" for category in item.get("categories") or []):
                row["action_items"] += 1

    inventory = []
    for playlist in ledger.get("channel_playlists") or []:
        playlist_id = playlist.get("id")
        stat = stats.get(playlist_id, {})
        item_count = number(playlist.get("item_count"))
        in_scope = stat.get("in_scope_video_count", 0)
        inventory.append(
            {
                "playlist_id": playlist_id,
                "playlist": playlist.get("title") or playlist_id or "Untitled playlist",
                "url": playlist.get("url"),
                "privacy_status": playlist.get("privacy_status"),
                "item_count": item_count,
                "observed_item_count": playlist.get("observed_item_count"),
                "in_scope_video_count": in_scope,
                "missing_from_scope_count": max(item_count - in_scope, 0) if item_count is not None else None,
                "action_items": stat.get("action_items", 0),
                "total_views": stat.get("total_views", 0.0),
            }
        )
    return sorted(
        inventory,
        key=lambda row: (
            row.get("item_count") or 0,
            row.get("in_scope_video_count") or 0,
            row.get("playlist") or "",
        ),
        reverse=True,
    )


def build_data_gap_groups(findings: dict[str, Any]) -> dict[str, dict[str, Any]]:
    missing_counts = {
        row["name"]: row["count"]
        for row in findings.get("manual_missing_counts") or []
    }
    groups: dict[str, dict[str, Any]] = {}
    for group_key, fields in FIELD_GROUPS.items():
        groups[group_key] = {
            "label": {
                "api_pending": "API pending",
                "studio_manual": "Studio/manual",
                "workflow_metadata": "Workflow metadata",
            }[group_key],
            "fields": [
                {
                    "name": field,
                    "label": READABLE_FIELD_LABELS.get(field, field),
                    "missing_count": missing_counts.get(field, 0),
                    "reporting_job": FIELD_UNLOCKS.get(field),
                }
                for field in fields
            ],
        }
    return groups


def build_dashboard_payload(
    ledger: dict[str, Any],
    report_summary: dict[str, Any],
    reporting_jobs: dict[str, Any] | None = None,
    content_rubric: dict[str, Any] | None = None,
    experiment_registry: dict[str, Any] | None = None,
    previous_snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    videos = ledger.get("videos") or []
    format_counts = Counter(video.get("format") or "unknown" for video in videos)
    privacy_counts = Counter(video.get("privacy_status") or "unknown" for video in videos)
    package_counts = Counter(video.get("package") or "unknown" for video in videos)
    playlist_counts: Counter[str] = Counter()
    for video in videos:
        playlists = compact_playlists(video)
        if not playlists:
            playlist_counts["No playlist"] += 1
            continue
        for playlist in playlists:
            playlist_counts[playlist["title"]] += 1
    findings = summarize_findings(report_summary, videos)
    action_lanes = build_action_lanes(findings)
    package_rollups_by_horizon = build_package_rollups_by_horizon(findings)
    playlist_rollups_by_horizon = build_playlist_rollups_by_horizon(findings)
    playlist_inventory_by_horizon = {
        horizon: build_playlist_inventory(ledger, findings, horizon=horizon)
        for horizon in HORIZONS
    }
    funnel_rollups = build_funnel_rollups(findings)
    horizon_summaries = build_horizon_summaries(findings)
    traffic_sources_by_horizon = summarize_traffic_by_horizon(videos)
    content_rubric = content_rubric or load_content_rubric()
    rubric = build_rubric(findings, content_rubric)
    daily_movement = build_daily_movement_summary(videos, findings)
    release_rollups_by_horizon = {
        horizon: build_release_rollups(findings, horizon=horizon)
        for horizon in HORIZONS
    }
    length_rollups_by_horizon = {
        horizon: build_length_rollups(findings, horizon=horizon)
        for horizon in HORIZONS
    }
    experiment_registry = experiment_registry or load_experiment_registry()
    delta_summary = build_delta_summary(findings, previous_snapshot, horizon="weekly")
    packaging_lab = build_packaging_lab(findings, horizon="weekly")
    funnel_map = build_funnel_map(findings, funnel_rollups)
    topic_clusters = build_topic_clusters(findings, content_rubric, horizon="weekly")
    release_time_lab = build_release_time_lab(findings, horizon="weekly")
    production_queue = build_production_queue(findings, horizon="weekly")
    experiments = build_experiments(experiment_registry, findings, horizon="weekly")

    reach_impression_videos = sum(
        1
        for video in videos
        if selected_metric(video, "videoThumbnailImpressions") is not None
        or (video.get("manual_observations") or {}).get("video_thumbnail_impressions") is not None
    )
    ctr_videos = sum(
        1
        for video in videos
        if selected_metric(video, "videoThumbnailImpressionsClickRate") is not None
        or (video.get("manual_observations") or {}).get("video_thumbnail_ctr") is not None
    )

    jobs = reporting_jobs.get("jobs") if reporting_jobs else {}
    reporting_job_rows = [
        {
            "key": key,
            "name": job.get("name"),
            "report_type_id": job.get("report_type_id"),
            "available_report_count": job.get("available_report_count", 0),
            "downloaded_report_count": job.get("downloaded_report_count", 0),
            "latest_report_end_time": job.get("latest_report_end_time"),
            "purpose": job.get("purpose"),
        }
        for key, job in sorted((jobs or {}).items())
    ]
    reach_jobs = [
        job
        for job in reporting_job_rows
        if str(job.get("report_type_id") or "").startswith("channel_reach")
    ]
    reach_ready = any((job.get("available_report_count") or 0) > 0 for job in reach_jobs)
    reach_hydration_gap = reach_ready and reach_impression_videos == 0
    warnings = []
    if reach_hydration_gap:
        warnings.append(
            {
                "key": "reporting_reach_not_hydrated",
                "message": "Reach reports are available, but no videos have thumbnail impressions/CTR hydrated into the ledger.",
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(REPO_ROOT),
        "ledger": {
            "created_at": ledger.get("created_at"),
            "analytics_end_date": ledger.get("analytics_end_date"),
            "read_only": ledger.get("read_only", True),
            "query_notes": ledger.get("query_notes") or [],
            "reporting_api_sync": ledger.get("reporting_api_sync") or {},
            "source": ledger.get("source") or {},
        },
        "report": {
            "report_date": report_summary.get("report_date"),
            "created_at": report_summary.get("created_at"),
            "analytics_end_date": report_summary.get("analytics_end_date"),
            "read_only": report_summary.get("read_only", True),
        },
        "totals": {
            "videos": len(videos),
            "actionable_videos": len(findings["action_items"]),
            "traffic_source_videos": sum(1 for video in videos if video.get("traffic_sources")),
            "content_type_videos": sum(1 for video in videos if video.get("creator_content_type")),
            "daily_metric_videos": sum(1 for video in videos if video.get("daily_metrics")),
            "playlist_videos": sum(1 for video in videos if video.get("playlists")),
            "related_video_targets": sum(1 for video in videos if video.get("related_video")),
            "reach_impression_videos": reach_impression_videos,
            "ctr_videos": ctr_videos,
            "waiting_for_ctr": action_lanes["waiting_for_ctr"]["count"],
            "needs_studio_check": action_lanes["needs_studio_check"]["count"],
        },
        "distributions": {
            "formats": sorted_counter(format_counts),
            "privacy": sorted_counter(privacy_counts),
            "top_packages": sorted_counter(package_counts, limit=15),
            "top_playlists": sorted_counter(playlist_counts, limit=15),
            "traffic_sources_7d": summarize_traffic(videos),
            "traffic_sources_by_horizon": traffic_sources_by_horizon,
            "creator_content_type_7d": summarize_content_type(videos),
        },
        "coverage": {
            "windows": summarize_windows(videos),
            "metrics": summarize_metric_availability(videos),
            "manual_fields": summarize_manual_availability(videos),
        },
        "reporting_jobs": reporting_job_rows,
        "reporting_status": {
            "reach_ready": reach_ready,
            "reach_hydration_gap": reach_hydration_gap,
            "reach_status_text": (
                "Reach reports need merge"
                if reach_hydration_gap
                else "Reach reports ready"
                if reach_ready
                else "CTR and impressions pending"
            ),
            "latest_reach_report_end_time": next(
                (
                    job.get("latest_report_end_time")
                    for job in reach_jobs
                    if job.get("latest_report_end_time")
                ),
                None,
            ),
        },
        "warnings": warnings,
        "help_text": HELP_TEXT,
        "readable_field_labels": READABLE_FIELD_LABELS,
        "horizons": HORIZONS,
        "horizon_summaries": horizon_summaries,
        "action_lanes": action_lanes,
        "delta_summary": delta_summary,
        "daily_movement": daily_movement,
        "experiments": experiments,
        "packaging_lab": packaging_lab,
        "funnel_map": funnel_map,
        "topic_clusters": topic_clusters,
        "release_time_lab": release_time_lab,
        "production_queue": production_queue,
        "rubric": rubric,
        "package_rollups": package_rollups_by_horizon["weekly"],
        "package_rollups_by_horizon": package_rollups_by_horizon,
        "playlist_rollups": playlist_rollups_by_horizon["weekly"],
        "playlist_rollups_by_horizon": playlist_rollups_by_horizon,
        "playlist_inventory": playlist_inventory_by_horizon["weekly"],
        "playlist_inventory_by_horizon": playlist_inventory_by_horizon,
        "funnel_rollups": funnel_rollups,
        "release_rollups_by_horizon": release_rollups_by_horizon,
        "length_rollups_by_horizon": length_rollups_by_horizon,
        "sort_defaults": {
            "videos": {"key": "useful", "direction": "desc"},
            "rubric": {"key": "useful", "direction": "desc"},
            "packages": {"key": "action_items", "direction": "desc"},
        },
        "data_gap_groups": build_data_gap_groups(findings),
        "ui_defaults": {
            "default_tab": "overview",
            "default_horizon": "weekly",
            "show_empty_buckets": False,
        },
        "findings": findings,
    }


def build_html(payload: dict[str, Any]) -> str:
    safe_json = json.dumps(payload, sort_keys=False).replace("</", "<\\/")
    return DASHBOARD_HTML.replace("__DASHBOARD_JSON__", safe_json)


def build_operator_html_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Return only the state the static browser UI needs."""
    return {
        "generated_at": payload.get("generated_at"),
        "repo_root": payload.get("repo_root"),
        "default_report_date": payload.get("default_report_date"),
        "report_states": payload.get("report_states") or [],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER_PATH)
    parser.add_argument("--report", type=Path, default=None)
    parser.add_argument("--reporting-jobs", type=Path, default=DEFAULT_REPORTING_JOBS_PATH)
    parser.add_argument("--content-rubric", type=Path, default=DEFAULT_CONTENT_RUBRIC_PATH)
    parser.add_argument("--experiment-registry", type=Path, default=DEFAULT_EXPERIMENT_REGISTRY_PATH)
    parser.add_argument("--previous-snapshot", type=Path, default=None)
    parser.add_argument("--snapshot-dir", type=Path, default=DEFAULT_SNAPSHOT_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--payload-output", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ledger = load_json(args.ledger)
    report_path = args.report or latest_report_path(DEFAULT_WEEKLY_REPORT_DIR)
    if report_path is None:
        raise SystemExit("No weekly report JSON found. Run build_youtube_decision_report.py first.")
    report_summary = load_json(report_path)
    reporting_jobs = load_json(args.reporting_jobs) if args.reporting_jobs.exists() else None
    content_rubric = load_content_rubric(args.content_rubric)
    experiment_registry = load_experiment_registry(args.experiment_registry)
    if args.previous_snapshot:
        previous_snapshot = load_json(args.previous_snapshot)
    else:
        previous_snapshot = load_previous_snapshot(args.snapshot_dir)

    payload = build_dashboard_payload(
        ledger,
        report_summary,
        reporting_jobs,
        content_rubric,
        experiment_registry,
        previous_snapshot,
    )
    report_summaries = load_weekly_report_summaries(DEFAULT_WEEKLY_REPORT_DIR)
    if not report_summaries:
        report_summaries = [
            {
                "path": repo_relative(report_path),
                "report_date": report_summary.get("report_date") or report_path.stem,
                "payload": report_summary,
            }
        ]
    report_states = build_report_states(
        ledger,
        report_summaries,
        reporting_jobs,
        content_rubric,
        experiment_registry,
        load_snapshot_records(args.snapshot_dir),
    )
    payload["report_states"] = report_states
    payload["default_report_date"] = (
        (report_states[0].get("report") or {}).get("report_date")
        if report_states
        else report_summary.get("report_date")
    )
    html = build_html(build_operator_html_payload(payload))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html)

    payload_output = args.payload_output or args.output.with_name("dashboard_payload.json")
    write_json(payload_output, payload)
    print(f"Wrote dashboard: {args.output}")
    print(f"Wrote payload: {payload_output}")
    return 0


# Operator dashboard HTML template. The old inventory-style dashboard was intentionally removed.

DASHBOARD_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,">
  <title>YouTube Analytics Dashboard</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f5f6f3;
      --panel: #ffffff;
      --panel-soft: #f9faf7;
      --ink: #151b22;
      --muted: #5f6875;
      --line: #d9ded7;
      --blue: #1d5fd1;
      --green: #137344;
      --orange: #a85600;
      --red: #b3261e;
      --teal: #047481;
      --violet: #6750a4;
      --shadow: 0 1px 2px rgba(21, 27, 34, 0.08);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.42;
    }
    .shell { width: min(1380px, calc(100vw - 28px)); margin: 0 auto; padding: 18px 0 34px; }
    header { display: grid; gap: 14px; margin-bottom: 14px; }
    h1 { margin: 0; font-size: 26px; line-height: 1.1; letter-spacing: 0; }
    h2 { margin: 0 0 10px; font-size: 18px; letter-spacing: 0; }
    h3 { margin: 0 0 8px; font-size: 14px; letter-spacing: 0; }
    p { margin: 0 0 9px; }
    a { color: var(--blue); text-decoration: none; }
    a:hover { text-decoration: underline; }
    .muted { color: var(--muted); }
    .small { font-size: 12px; }
    .top-line { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 18px; align-items: start; }
    .meta { color: var(--muted); font-size: 13px; margin-top: 6px; }
    .controls, .report-strip, .tabs, .chips { display: flex; flex-wrap: wrap; gap: 8px; }
    .controls { justify-content: flex-end; align-items: center; }
    .report-strip { padding: 10px; border: 1px solid var(--line); border-radius: 8px; background: var(--panel); box-shadow: var(--shadow); }
    button, input, select {
      font: inherit;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      color: var(--ink);
    }
    button { min-height: 34px; padding: 6px 10px; cursor: pointer; }
    button.active { border-color: var(--blue); box-shadow: inset 0 0 0 1px var(--blue); }
    input, select { width: 100%; min-height: 38px; padding: 8px 10px; }
    .tabs { border-bottom: 1px solid var(--line); margin: 4px 0 14px; }
    .tab { border-bottom: 0; border-radius: 8px 8px 0 0; background: transparent; color: var(--muted); }
    .tab.active { background: var(--panel); color: var(--ink); box-shadow: var(--shadow); }
    .panel { display: none; }
    .panel.active { display: block; }
    .card {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
      padding: 14px;
    }
    .grid { display: grid; gap: 12px; }
    .grid.two { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); }
    .grid.three { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .hero-grid { display: grid; grid-template-columns: minmax(0, 1.35fr) minmax(320px, 0.65fr); gap: 12px; align-items: start; }
    .memo-list, .queue-list { display: grid; gap: 10px; }
    .memo {
      display: grid;
      grid-template-columns: 128px minmax(0, 1fr);
      gap: 12px;
      border: 1px solid var(--line);
      border-left: 4px solid var(--blue);
      border-radius: 8px;
      background: var(--panel);
      padding: 12px;
      box-shadow: var(--shadow);
    }
    .memo.make_sequel, .memo.clip_more { border-left-color: var(--green); }
    .memo.thumbnail_review, .memo.retitle { border-left-color: var(--orange); }
    .memo.remaster { border-left-color: var(--teal); }
    .memo.wait, .memo.ignore { border-left-color: var(--line); }
    .thumb {
      width: 128px;
      aspect-ratio: 16 / 9;
      border: 1px solid var(--line);
      border-radius: 6px;
      object-fit: cover;
      background: #e8ece8;
    }
    .memo-title { font-weight: 750; margin-bottom: 4px; }
    .decision { color: var(--muted); font-size: 12px; font-weight: 750; text-transform: uppercase; }
    .next-step { margin-top: 8px; font-weight: 650; }
    .chip, .badge {
      display: inline-flex;
      align-items: center;
      min-height: 25px;
      padding: 3px 8px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: var(--panel-soft);
      color: var(--muted);
      font-size: 12px;
      white-space: nowrap;
    }
    .badge.scale, .badge.funnel_winner { color: var(--green); background: #edf8f1; border-color: rgba(19, 115, 68, 0.28); }
    .badge.retitle, .badge.hook_problem { color: var(--orange); background: #fff6e8; border-color: rgba(168, 86, 0, 0.28); }
    .badge.remaster, .badge.clip_more { color: var(--teal); background: #edf8f9; border-color: rgba(4, 116, 129, 0.28); }
    .stat-grid { display: grid; grid-template-columns: repeat(2, minmax(120px, 1fr)); gap: 10px; }
    .stat { background: var(--panel-soft); border: 1px solid var(--line); border-radius: 8px; padding: 12px; }
    .stat-value { display: block; font-size: 26px; font-weight: 800; line-height: 1; margin-bottom: 5px; }
    .stat-label { color: var(--muted); font-size: 12px; text-transform: uppercase; }
    .section-head { display: flex; justify-content: space-between; gap: 10px; align-items: baseline; margin: 16px 0 10px; }
    .queue-card { border-left: 4px solid var(--line); }
    .queue-card.production { border-left-color: var(--green); }
    .queue-card.fix { border-left-color: var(--orange); }
    .queue-card.watchlist { border-left-color: var(--violet); }
    .queue-item { padding: 9px 0; border-top: 1px solid var(--line); }
    .queue-item:first-child { border-top: 0; padding-top: 0; }
    .toolbar { display: grid; grid-template-columns: minmax(220px, 1fr) 180px 180px; gap: 10px; margin-bottom: 10px; }
    .table-wrap { overflow-x: auto; border: 1px solid var(--line); border-radius: 8px; background: var(--panel); box-shadow: var(--shadow); }
    table { border-collapse: collapse; width: 100%; min-width: 760px; font-size: 13px; }
    th, td { border-bottom: 1px solid var(--line); padding: 9px 10px; text-align: left; vertical-align: top; }
    th { background: #eef1ee; color: #35404c; font-size: 12px; }
    tr:last-child td { border-bottom: 0; }
    .empty { border: 1px dashed var(--line); border-radius: 8px; padding: 14px; color: var(--muted); background: rgba(255,255,255,0.65); }
    .bar-row { display: grid; grid-template-columns: minmax(120px, 1fr) minmax(120px, 2fr) auto; gap: 10px; align-items: center; margin: 7px 0; font-size: 13px; }
    .bar-track { height: 9px; border-radius: 999px; overflow: hidden; background: #e7ebe6; }
    .bar-fill { height: 100%; width: var(--bar-width); background: var(--teal); }
    .evidence-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
    @media (max-width: 980px) {
      .top-line, .hero-grid, .grid.two, .grid.three, .evidence-grid { grid-template-columns: 1fr; }
      .controls { justify-content: flex-start; }
    }
    @media (max-width: 680px) {
      .shell { width: min(100vw - 18px, 1380px); padding-top: 12px; }
      h1 { font-size: 22px; }
      .memo { grid-template-columns: 1fr; }
      .thumb { width: 100%; max-width: 320px; }
      .toolbar { grid-template-columns: 1fr; }
      .stat-grid { grid-template-columns: 1fr; }
      .bar-row { grid-template-columns: 1fr; gap: 4px; }
    }
  </style>
</head>
<body>
  <div class="shell">
    <header>
      <div class="top-line">
        <div>
          <h1>YouTube Analytics Dashboard</h1>
          <div class="meta" id="dashboard-meta"></div>
        </div>
        <div class="controls" id="horizon-controls"></div>
      </div>
      <div class="report-strip" id="report-strip" aria-label="Report switcher"></div>
      <nav class="tabs" aria-label="Dashboard tabs">
        <button class="tab active" data-tab="decisions">Decisions</button>
        <button class="tab" data-tab="videos">Videos</button>
        <button class="tab" data-tab="reports">Reports</button>
        <button class="tab" data-tab="evidence">Evidence/Data</button>
      </nav>
    </header>
    <main>
      <section class="panel active" id="decisions"></section>
      <section class="panel" id="videos"></section>
      <section class="panel" id="reports"></section>
      <section class="panel" id="evidence"></section>
    </main>
  </div>

  <script type="application/json" id="dashboard-data">__DASHBOARD_JSON__</script>
  <script>
    const payload = JSON.parse(document.getElementById("dashboard-data").textContent);
    const reportStates = payload.report_states || [];
    const stateByDate = Object.fromEntries(reportStates.map((state) => [((state.report || {}).report_date || ""), state]));
    const horizonOrder = ["daily", "weekly", "monthly"];
    const horizonLabels = { daily: "Daily", weekly: "Weekly", monthly: "28 Days" };
    let currentHorizon = "weekly";
    let activeTab = "decisions";
    let activeReportDate = initialReportDate();

    function initialReportDate() {
      const params = new URLSearchParams((window.location.hash || "").replace(/^#/, ""));
      const requested = params.get("report");
      if (requested && stateByDate[requested]) return requested;
      return payload.default_report_date || ((reportStates[0] || {}).report || {}).report_date || "";
    }
    function state() { return stateByDate[activeReportDate] || reportStates[0] || {}; }
    function esc(value) {
      return String(value ?? "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]));
    }
    function num(value, digits = 0) {
      if (value === null || value === undefined || Number.isNaN(Number(value))) return "-";
      return Number(value).toLocaleString(undefined, { maximumFractionDigits: digits });
    }
    function pct(value) {
      if (value === null || value === undefined || Number.isNaN(Number(value))) return "-";
      return `${num(value, 1)}%`;
    }
    function metric(item, horizon = currentHorizon) {
      return (((item.horizon_metrics || {})[horizon] || {}).metrics || {});
    }
    function itemLink(item) {
      const title = esc(item.title || item.video_id || "Untitled");
      return item.url ? `<a href="${esc(item.url)}" target="_blank" rel="noreferrer">${title}</a>` : title;
    }
    function thumb(item) {
      return item.thumbnail_url ? `<img class="thumb" src="${esc(item.thumbnail_url)}" alt="">` : `<div class="thumb" aria-hidden="true"></div>`;
    }
    function badges(item) {
      return (item.categories || [item.primary_category || "ignore"]).map((category) => `<span class="badge ${esc(category)}">${esc(category.replace("_", " "))}</span>`).join(" ");
    }
    function evidenceLine(item) {
      const m = metric(item);
      const parts = [];
      if (m.views !== null && m.views !== undefined) parts.push(`${num(m.views)} views`);
      if (m.views_per_day !== null && m.views_per_day !== undefined) parts.push(`${num(m.views_per_day, 1)}/day`);
      if (m.averageViewPercentage !== null && m.averageViewPercentage !== undefined) parts.push(`${pct(m.averageViewPercentage)} avg viewed`);
      if (m.subscribersGained) parts.push(`+${num(m.subscribersGained)} subs`);
      if (item.format === "short" && item.shorts_feed_views) parts.push(`${num(item.shorts_feed_views)} Shorts-feed views`);
      if ((m.videoThumbnailImpressions || 0) >= 50 && m.videoThumbnailImpressionsClickRate !== null && m.videoThumbnailImpressionsClickRate !== undefined) {
        parts.push(`${num(m.videoThumbnailImpressions)} impressions at ${pct(m.videoThumbnailImpressionsClickRate)} CTR`);
      }
      return parts.join(" | ") || "No usable metric row yet.";
    }
    function caveatChips(item) {
      const caveats = item.caveats || [];
      return caveats.length ? `<div class="chips">${caveats.map((caveat) => `<span class="chip">${esc(caveat)}</span>`).join("")}</div>` : "";
    }
    function summaryStat(label, value, formatter = num) {
      return `<div class="stat"><span class="stat-value">${formatter(value)}</span><span class="stat-label">${esc(label)}</span></div>`;
    }
    function table(headers, rows) {
      if (!rows.length) return `<div class="empty">No rows for this view.</div>`;
      return `<div class="table-wrap"><table><thead><tr>${headers.map((h) => `<th>${h}</th>`).join("")}</tr></thead><tbody>${rows.join("")}</tbody></table></div>`;
    }
    function bars(rows, labelKey, valueKey) {
      const max = Math.max(...rows.map((row) => Number(row[valueKey]) || 0), 1);
      return rows.map((row) => {
        const value = Number(row[valueKey]) || 0;
        return `<div class="bar-row"><div>${esc(row[labelKey] || row.name || "-")}</div><div class="bar-track"><div class="bar-fill" style="--bar-width:${Math.max(2, Math.round(value / max * 100))}%"></div></div><div>${num(value)}</div></div>`;
      }).join("") || `<div class="empty">No data.</div>`;
    }

    function setReport(date) {
      if (!stateByDate[date]) return;
      activeReportDate = date;
      const params = new URLSearchParams((window.location.hash || "").replace(/^#/, ""));
      params.set("report", date);
      window.history.replaceState(null, "", `#${params.toString()}`);
      renderAll();
    }
    function setHorizon(horizon) {
      currentHorizon = horizon;
      renderAll();
    }
    function setTab(tab) {
      activeTab = tab;
      document.querySelectorAll(".tab").forEach((button) => button.classList.toggle("active", button.dataset.tab === tab));
      document.querySelectorAll(".panel").forEach((panel) => panel.classList.toggle("active", panel.id === tab));
      renderActivePanel();
    }

    function renderChrome() {
      const s = state();
      const report = s.report || {};
      const summary = (s.horizon_summaries || {})[currentHorizon] || {};
      document.getElementById("dashboard-meta").textContent = `Report ${report.report_date || "-"} | analytics through ${report.analytics_end_date || "-"} | ${horizonLabels[currentHorizon]} view`;
      document.getElementById("horizon-controls").innerHTML = horizonOrder.map((horizon) =>
        `<button class="${horizon === currentHorizon ? "active" : ""}" data-horizon="${horizon}">${esc(horizonLabels[horizon])}</button>`
      ).join("");
      document.querySelectorAll("[data-horizon]").forEach((button) => button.addEventListener("click", () => setHorizon(button.dataset.horizon)));
      document.getElementById("report-strip").innerHTML = reportStates.map((reportState) => {
        const reportDate = (reportState.report || {}).report_date || "";
        const counts = reportState.summary_counts || {};
        const label = `${reportDate} | ${num(reportState.totals?.actionable_videos || 0)} actions | ${num((reportState.horizon_summaries?.weekly || {}).total_views || 0)} views`;
        return `<button class="${reportDate === activeReportDate ? "active" : ""}" data-report="${esc(reportDate)}">${esc(label)}</button>`;
      }).join("");
      document.querySelectorAll("[data-report]").forEach((button) => button.addEventListener("click", () => setReport(button.dataset.report)));
    }

    function memoCard(item) {
      return `<article class="memo ${esc(item.action || "")}">
        ${thumb(item)}
        <div>
          <div class="decision">${esc(item.decision || item.action_label || "Decision")}</div>
          <div class="memo-title">${itemLink(item)}</div>
          <div class="muted">${esc(evidenceLine(item))}</div>
          <div class="next-step">${esc(item.next_step || "Review this item.")}</div>
          <div class="chips" style="margin-top:8px;">
            <span class="chip">${esc(item.confidence || "Directional")}</span>
            <span class="chip">${esc(item.format || "unknown")}</span>
            ${badges(item)}
          </div>
          ${caveatChips(item)}
        </div>
      </article>`;
    }

    function queueCard(key, queue) {
      const items = queue.items || [];
      return `<section class="card queue-card ${esc(key)}">
        <div class="section-head" style="margin-top:0;"><div><h2>${esc(queue.label || key)}</h2><p class="muted">${esc(queue.description || "")}</p></div><span class="chip">${num(items.length)}</span></div>
        <div class="queue-list">${items.slice(0, key === "watchlist" ? 8 : 6).map((item) => `
          <div class="queue-item">
            <div class="memo-title">${itemLink(item)}</div>
            <div class="small muted">${esc(item.action_label || "")} | ${esc(evidenceLine(item))}</div>
            <div class="small">${esc(item.next_step || "")}</div>
          </div>
        `).join("") || `<div class="empty">No items.</div>`}</div>
      </section>`;
    }

    function renderDecisions() {
      const s = state();
      const summary = (s.horizon_summaries || {})[currentHorizon] || {};
      const memos = s.decision_memos || [];
      document.getElementById("decisions").innerHTML = `
        <div class="hero-grid">
          <section class="card">
            <h2>What to do next</h2>
            <div class="memo-list">${memos.slice(0, 5).map(memoCard).join("") || `<div class="empty">No decision memos crossed the current thresholds.</div>`}</div>
          </section>
          <aside class="card">
            <h2>${esc(horizonLabels[currentHorizon])} summary</h2>
            <div class="stat-grid">
              ${summaryStat("views", summary.total_views)}
              ${summaryStat("watch minutes", summary.total_watch_time_minutes)}
              ${summaryStat("avg viewed", summary.average_view_percentage, pct)}
              ${summaryStat("videos with data", summary.videos_with_metrics)}
              ${summaryStat("actionable", s.totals?.actionable_videos || 0)}
              ${summaryStat("watch only", s.totals?.ignored_count || 0)}
            </div>
          </aside>
        </div>
        <div class="grid three" style="margin-top:12px;">
          ${queueCard("production", (s.queues || {}).production || {})}
          ${queueCard("fix", (s.queues || {}).fix || {})}
          ${queueCard("watchlist", (s.queues || {}).watchlist || {})}
        </div>
      `;
    }

    function renderVideos() {
      const s = state();
      const videos = s.videos || [];
      document.getElementById("videos").innerHTML = `
        <div class="card" style="margin-bottom:12px;">
          <h2>Video inspection</h2>
          <p class="muted">Compact table for checking one video without turning the dashboard into the default view.</p>
        </div>
        <div class="toolbar">
          <input id="video-search" type="search" placeholder="Search title, package, video id">
          <select id="video-action">
            <option value="">All actions</option>
            <option value="make_sequel">Make follow-up</option>
            <option value="thumbnail_review">Fix packaging</option>
            <option value="retitle">Retitle / reframe</option>
            <option value="remaster">Remaster</option>
            <option value="wait">Wait for data</option>
            <option value="ignore">Watch only</option>
          </select>
          <select id="video-format"><option value="">All formats</option>${[...new Set(videos.map((v) => v.format || "unknown"))].sort().map((f) => `<option value="${esc(f)}">${esc(f)}</option>`).join("")}</select>
        </div>
        <div id="video-table"></div>
      `;
      const draw = () => {
        const q = document.getElementById("video-search").value.toLowerCase();
        const action = document.getElementById("video-action").value;
        const format = document.getElementById("video-format").value;
        const rows = videos
          .filter((item) => !q || `${item.title || ""} ${item.package || ""} ${item.video_id || ""}`.toLowerCase().includes(q))
          .filter((item) => !action || item.action === action)
          .filter((item) => !format || (item.format || "unknown") === format)
          .slice(0, 80)
          .map((item) => {
            const m = metric(item);
            return `<tr>
              <td>${itemLink(item)}<div class="small muted">${esc(item.video_id || "")}</div></td>
              <td>${esc(item.action_label || "")}<div class="small muted">${esc(item.confidence || "")}</div></td>
              <td>${num(m.views)}</td>
              <td>${num(m.views_per_day, 1)}</td>
              <td>${pct(m.averageViewPercentage)}</td>
              <td>${m.videoThumbnailImpressions !== null && m.videoThumbnailImpressions !== undefined ? `${num(m.videoThumbnailImpressions)} / ${pct(m.videoThumbnailImpressionsClickRate)}` : "-"}</td>
              <td>${esc((item.caveats || []).join("; "))}</td>
            </tr>`;
          });
        document.getElementById("video-table").innerHTML = table(["Video", "Action", "Views", "V/day", "Avg viewed", "Impr / CTR", "Caveats"], rows);
      };
      ["video-search", "video-action", "video-format"].forEach((id) => document.getElementById(id).addEventListener("input", draw));
      draw();
    }

    function movementTable(group) {
      const rows = (group.items || []).slice(0, 8).map((item) => `
        <tr><td>${itemLink(item)}</td><td>${esc(item.confidence || "-")}</td><td>${num(item.current, 1)}</td><td>${num(item.previous, 1)}</td><td>${num(item.delta, 1)}</td></tr>
      `);
      return table(["Video", "Confidence", "Current", "Previous", "Delta"], rows);
    }

    function renderReports() {
      const s = state();
      const delta = ((s.reports || {}).delta_summary || {});
      const groups = delta.groups || {};
      const counts = s.summary_counts || {};
      document.getElementById("reports").innerHTML = `
        <div class="grid two">
          <section class="card">
            <h2>Report ${esc((s.report || {}).report_date || "-")}</h2>
            <p class="muted">Analytics through ${esc((s.report || {}).analytics_end_date || "-")}.</p>
            <div class="chips">
              ${Object.entries(counts).map(([key, value]) => `<span class="chip">${esc(key.replace("_", " "))}: ${num(value)}</span>`).join("")}
            </div>
          </section>
          <section class="card">
            <h2>Previous snapshot comparison</h2>
            <p>${esc(delta.description || "No previous snapshot is available for this report.")}</p>
            <p class="muted small">Previous: ${esc(delta.previous_generated_at || "-")}</p>
          </section>
        </div>
        <div class="grid two" style="margin-top:12px;">
          <section class="card"><h2>Views/day movement</h2>${movementTable(groups.views_day_movers || {})}</section>
          <section class="card"><h2>Subscriber movement</h2>${movementTable(groups.subscriber_movers || {})}</section>
        </div>
      `;
    }

    function renderEvidence() {
      const s = state();
      const evidence = s.evidence || {};
      const packages = ((evidence.package_rollups_by_horizon || {})[currentHorizon] || []).map((row) =>
        `<tr><td>${esc(row.package || "-")}</td><td>${num(row.video_count)}</td><td>${num(row.action_items)}</td><td>${num(row.total_views)}</td><td>${pct(row.average_view_percentage)}</td></tr>`
      );
      const playlists = ((evidence.playlist_rollups_by_horizon || {})[currentHorizon] || []).map((row) =>
        `<tr><td>${row.url ? `<a href="${esc(row.url)}" target="_blank" rel="noreferrer">${esc(row.playlist || "-")}</a>` : esc(row.playlist || "-")}</td><td>${num(row.video_count)}</td><td>${num(row.action_items)}</td><td>${num(row.total_views)}</td></tr>`
      );
      const traffic = (((evidence.traffic_sources_by_horizon || {})[currentHorizon] || {}).sources || []);
      const jobs = (evidence.reporting_jobs || []).map((job) =>
        `<tr><td>${esc(job.report_type_id || job.key)}</td><td>${num(job.available_report_count)}</td><td>${num(job.downloaded_report_count)}</td><td>${esc(job.latest_report_end_time || "-")}</td></tr>`
      );
      const metrics = Object.entries(((evidence.coverage || {}).metrics || {})).slice(0, 12).map(([name, row]) => ({ name, count: row.count || 0 }));
      const topics = (((evidence.topic_clusters || {}).clusters || [])).map((row) =>
        `<tr><td>${esc(row.cluster || "-")}</td><td>${num(row.video_count)}</td><td>${num(row.action_items)}</td><td>${num(row.views)}</td><td>${pct(row.average_view_percentage)}</td></tr>`
      );
      const experiments = (((evidence.experiments || {}).experiments || [])).map((row) =>
        `<tr><td>${esc(row.name || row.id || "-")}</td><td>${esc(row.status || "-")}</td><td>${num((row.current_read || {}).video_count)}</td><td>${num((row.current_read || {}).views)}</td><td>${pct((row.current_read || {}).average_view_percentage)}</td></tr>`
      );
      document.getElementById("evidence").innerHTML = `
        <div class="evidence-grid">
          <section class="card"><h2>Metric coverage</h2>${bars(metrics, "name", "count")}</section>
          <section class="card"><h2>Traffic sources</h2>${bars(traffic, "source", "views")}</section>
          <section class="card"><h2>Packages</h2>${table(["Package", "Videos", "Actions", "Views", "Avg viewed"], packages)}</section>
          <section class="card"><h2>Playlists</h2>${table(["Playlist", "Videos", "Actions", "Views"], playlists)}</section>
          <section class="card"><h2>Reporting jobs</h2>${table(["Report type", "Available", "Downloaded", "Latest end"], jobs)}</section>
          <section class="card"><h2>Topic clusters</h2>${table(["Cluster", "Videos", "Actions", "Views", "Avg viewed"], topics)}</section>
          <section class="card"><h2>Experiments</h2>${table(["Experiment", "Status", "Videos", "Views", "Avg viewed"], experiments)}</section>
          <section class="card"><h2>Release timing</h2><p>${esc((((evidence.release_time_lab || {}).insights || {}).summary) || "Not enough release-time data for a directional read.")}</p><p class="muted small">Timezone: ${esc((evidence.release_time_lab || {}).timezone || "Europe/Athens")}</p></section>
        </div>
      `;
    }

    function renderActivePanel() {
      if (activeTab === "decisions") renderDecisions();
      if (activeTab === "videos") renderVideos();
      if (activeTab === "reports") renderReports();
      if (activeTab === "evidence") renderEvidence();
    }
    function renderAll() {
      renderChrome();
      renderActivePanel();
    }
    document.querySelectorAll(".tab").forEach((button) => button.addEventListener("click", () => setTab(button.dataset.tab)));
    window.addEventListener("hashchange", () => {
      const next = initialReportDate();
      if (next !== activeReportDate) {
        activeReportDate = next;
        renderAll();
      }
    });
    renderAll();
  </script>
</body>
</html>
"""


if __name__ == "__main__":
    raise SystemExit(main())
