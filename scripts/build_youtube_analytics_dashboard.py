#!/usr/bin/env python3
"""Build a static local dashboard for YouTube analytics decisions."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER_PATH = REPO_ROOT / "experiments" / "youtube-analytics" / "metrics_ledger.json"
DEFAULT_WEEKLY_REPORT_DIR = REPO_ROOT / "experiments" / "youtube-analytics" / "weekly_reports"
DEFAULT_REPORTING_JOBS_PATH = REPO_ROOT / "experiments" / "youtube-analytics" / "reporting_jobs.json"
DEFAULT_OUTPUT_PATH = REPO_ROOT / "experiments" / "youtube-analytics" / "dashboard" / "index.html"

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


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


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


def summarize_metric_availability(videos: list[dict[str, Any]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for video in videos:
        for window in (video.get("analytics_windows") or {}).values():
            metrics = window.get("metrics") or {}
            for metric_name in CORE_METRICS:
                if number(metrics.get(metric_name)) is not None:
                    counts[metric_name] += 1
    return {metric_name: counts.get(metric_name, 0) for metric_name in CORE_METRICS}


def summarize_manual_availability(videos: list[dict[str, Any]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for video in videos:
        observations = video.get("manual_observations") or {}
        for field in MANUAL_FIELDS:
            if observations.get(field) is not None:
                counts[field] += 1
    return {field: counts.get(field, 0) for field in MANUAL_FIELDS}


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


def compact_classification(
    classification: dict[str, Any],
    source_video: dict[str, Any] | None = None,
) -> dict[str, Any]:
    metrics = classification.get("metrics") or {}
    source_video = source_video or {}
    observations = source_video.get("manual_observations") or {}
    categories = classification.get("categories") or ["ignore"]
    reasons = classification.get("reasons") or []
    reasons_by_category = {
        category: reasons[index]
        for index, category in enumerate(categories)
        if index < len(reasons)
    }
    source_reports = source_video.get("source_reports") or []
    click_metrics = known_clicks(observations)
    horizon_metrics = build_horizon_metrics(source_video)
    return {
        "video_id": classification.get("video_id"),
        "title": classification.get("title"),
        "url": classification.get("url"),
        "format": classification.get("format") or "unknown",
        "package": classification.get("package") or "unknown",
        "published_at": classification.get("published_at"),
        "privacy_status": source_video.get("privacy_status"),
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
            **click_metrics,
            "card_impressions": number(observations.get("card_impressions")),
            "card_teaser_clicks": number(observations.get("card_teaser_clicks")),
            "card_teaser_impressions": number(observations.get("card_teaser_impressions")),
            "card_click_rate": number(observations.get("card_click_rate")),
            "card_teaser_click_rate": number(observations.get("card_teaser_click_rate")),
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
) -> dict[str, Any]:
    video_lookup = {video.get("video_id"): video for video in videos or []}
    compact = [
        compact_classification(item, video_lookup.get(item.get("video_id")))
        for item in report_summary.get("classifications") or []
    ]
    by_category: dict[str, list[dict[str, Any]]] = {category: [] for category in DECISION_ORDER}
    missing_fields: Counter[str] = Counter()
    for item in compact:
        for category in item["categories"]:
            by_category.setdefault(category, []).append(item)
        for field in item["manual_fields_missing"]:
            missing_fields[field] += 1

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
    }
    for item in findings.get("classifications") or []:
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
) -> dict[str, Any]:
    videos = ledger.get("videos") or []
    format_counts = Counter(video.get("format") or "unknown" for video in videos)
    privacy_counts = Counter(video.get("privacy_status") or "unknown" for video in videos)
    package_counts = Counter(video.get("package") or "unknown" for video in videos)
    findings = summarize_findings(report_summary, videos)
    action_lanes = build_action_lanes(findings)
    package_rollups_by_horizon = build_package_rollups_by_horizon(findings)
    funnel_rollups = build_funnel_rollups(findings)
    horizon_summaries = build_horizon_summaries(findings)
    traffic_sources_by_horizon = summarize_traffic_by_horizon(videos)

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

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(REPO_ROOT),
        "ledger": {
            "created_at": ledger.get("created_at"),
            "analytics_end_date": ledger.get("analytics_end_date"),
            "read_only": ledger.get("read_only", True),
            "query_notes": ledger.get("query_notes") or [],
            "reporting_api_sync": ledger.get("reporting_api_sync") or {},
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
            "reach_status_text": "Reach reports ready" if reach_ready else "CTR and impressions pending",
            "latest_reach_report_end_time": next(
                (
                    job.get("latest_report_end_time")
                    for job in reach_jobs
                    if job.get("latest_report_end_time")
                ),
                None,
            ),
        },
        "readable_field_labels": READABLE_FIELD_LABELS,
        "horizons": HORIZONS,
        "horizon_summaries": horizon_summaries,
        "action_lanes": action_lanes,
        "package_rollups": package_rollups_by_horizon["weekly"],
        "package_rollups_by_horizon": package_rollups_by_horizon,
        "funnel_rollups": funnel_rollups,
        "sort_defaults": {
            "videos": {"key": "score", "direction": "desc"},
            "packages": {"key": "action_items", "direction": "desc"},
        },
        "data_gap_groups": build_data_gap_groups(findings),
        "ui_defaults": {
            "default_tab": "action-board",
            "default_horizon": "weekly",
            "show_empty_buckets": False,
        },
        "findings": findings,
    }


def build_html(payload: dict[str, Any]) -> str:
    safe_json = json.dumps(payload, sort_keys=False).replace("</", "<\\/")
    return DASHBOARD_HTML.replace("__DASHBOARD_JSON__", safe_json)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER_PATH)
    parser.add_argument("--report", type=Path, default=None)
    parser.add_argument("--reporting-jobs", type=Path, default=DEFAULT_REPORTING_JOBS_PATH)
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

    payload = build_dashboard_payload(ledger, report_summary, reporting_jobs)
    html = build_html(payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html)

    payload_output = args.payload_output or args.output.with_name("dashboard_payload.json")
    write_json(payload_output, payload)
    print(f"Wrote dashboard: {args.output}")
    print(f"Wrote payload: {payload_output}")
    return 0


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
      --bg: #f6f7f4;
      --panel: #ffffff;
      --ink: #17202a;
      --muted: #5f6b78;
      --line: #d9ded8;
      --blue: #1d5fd1;
      --green: #187a45;
      --orange: #b65d00;
      --red: #b3261e;
      --teal: #047481;
      --violet: #6650a4;
      --shadow: 0 1px 2px rgba(23, 32, 42, 0.08);
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.45;
    }

    .shell {
      width: min(1500px, calc(100vw - 32px));
      margin: 0 auto;
      padding: 24px 0 36px;
    }

    header {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 20px;
      align-items: end;
      margin-bottom: 18px;
    }

    h1 { margin: 0; font-size: 30px; line-height: 1.15; letter-spacing: 0; }
    h2 { margin: 0 0 12px; font-size: 18px; letter-spacing: 0; }
    h3 { margin: 0 0 10px; font-size: 15px; letter-spacing: 0; }
    p { margin: 0 0 10px; }

    .meta {
      color: var(--muted);
      font-size: 13px;
      margin-top: 8px;
    }

    .status-strip, .metric-row, .quick-filters {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .status-strip { justify-content: flex-end; }
    .metric-row { margin-top: 8px; }

    .badge, .metric-chip, .check-chip {
      display: inline-flex;
      align-items: center;
      min-height: 26px;
      padding: 3px 8px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: #f9faf8;
      color: var(--muted);
      font-size: 12px;
      white-space: nowrap;
    }

    .check-chip { gap: 6px; cursor: pointer; }
    .check-chip input { width: auto; min-height: auto; margin: 0; }
    .horizon-control {
      display: inline-flex;
      flex-wrap: wrap;
      gap: 4px;
      padding: 4px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfcfa;
    }
    .horizon-btn {
      appearance: none;
      min-height: 30px;
      border: 1px solid transparent;
      border-radius: 6px;
      background: transparent;
      color: var(--muted);
      cursor: pointer;
      font: inherit;
      font-size: 13px;
      padding: 5px 9px;
    }
    .horizon-btn.active {
      background: var(--panel);
      border-color: var(--line);
      color: var(--ink);
      box-shadow: var(--shadow);
    }
    .badge.scale, .badge.funnel_winner { color: var(--green); border-color: rgba(24, 122, 69, 0.28); background: #eef8f1; }
    .badge.clip_more, .badge.remaster { color: var(--teal); border-color: rgba(4, 116, 129, 0.28); background: #edf8f9; }
    .badge.retitle { color: var(--orange); border-color: rgba(182, 93, 0, 0.28); background: #fff5e8; }
    .badge.hook_problem { color: var(--red); border-color: rgba(179, 38, 30, 0.28); background: #fff0ee; }
    .badge.ignore { color: var(--muted); }

    .tabs {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      border-bottom: 1px solid var(--line);
      margin-bottom: 16px;
    }

    .tab {
      appearance: none;
      border: 1px solid transparent;
      border-bottom: 0;
      border-radius: 8px 8px 0 0;
      background: transparent;
      color: var(--muted);
      cursor: pointer;
      font: inherit;
      min-height: 38px;
      padding: 8px 12px;
    }

    .tab.active {
      background: var(--panel);
      border-color: var(--line);
      color: var(--ink);
      box-shadow: var(--shadow);
    }

    .panel { display: none; }
    .panel.active { display: block; }
    .grid { display: grid; gap: 12px; }
    .grid.stats { grid-template-columns: repeat(6, minmax(140px, 1fr)); margin-bottom: 14px; }
    .grid.two { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); }
    .grid.three { grid-template-columns: repeat(3, minmax(0, 1fr)); }

    .card {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
      padding: 14px;
    }

    .stat-value {
      display: block;
      font-size: 28px;
      font-weight: 700;
      line-height: 1;
      margin-bottom: 6px;
    }

    .stat-label {
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .toolbar {
      display: grid;
      grid-template-columns: minmax(220px, 1fr) 180px 180px;
      gap: 10px;
      margin-bottom: 10px;
    }

    input, select {
      width: 100%;
      min-height: 38px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      color: var(--ink);
      font: inherit;
      padding: 8px 10px;
    }

    .table-wrap {
      overflow-x: auto;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      box-shadow: var(--shadow);
    }

    table {
      border-collapse: collapse;
      width: 100%;
      min-width: 900px;
      font-size: 13px;
    }

    th, td {
      border-bottom: 1px solid var(--line);
      padding: 9px 10px;
      text-align: left;
      vertical-align: top;
    }

    th {
      background: #eef1ef;
      color: #35404c;
      font-size: 12px;
      font-weight: 700;
      position: sticky;
      top: 0;
      z-index: 1;
    }

    tr:last-child td { border-bottom: 0; }
    tr.row-hook_problem td:first-child { border-left: 4px solid var(--red); }
    tr.row-remaster td:first-child, tr.row-clip_more td:first-child { border-left: 4px solid var(--teal); }
    tr.row-scale td:first-child, tr.row-funnel_winner td:first-child { border-left: 4px solid var(--green); }
    tr.row-retitle td:first-child { border-left: 4px solid var(--orange); }

    .sort-btn {
      appearance: none;
      border: 0;
      background: transparent;
      color: inherit;
      cursor: pointer;
      font: inherit;
      font-weight: 700;
      padding: 0;
      text-align: left;
    }

    a { color: var(--blue); text-decoration: none; }
    a:hover { text-decoration: underline; }
    .muted { color: var(--muted); }
    .small { font-size: 12px; }

    .bar-list { display: grid; gap: 9px; }
    .bar-row {
      display: grid;
      grid-template-columns: minmax(120px, 1fr) minmax(120px, 2fr) auto;
      gap: 10px;
      align-items: center;
      font-size: 13px;
    }

    .bar-track {
      height: 9px;
      border-radius: 999px;
      background: #e8ece8;
      overflow: hidden;
    }

    .bar-fill {
      height: 100%;
      width: var(--bar-width);
      background: var(--blue);
    }

    .bar-fill.green { background: var(--green); }
    .bar-fill.orange { background: var(--orange); }
    .bar-fill.red { background: var(--red); }
    .bar-fill.teal { background: var(--teal); }
    .bar-fill.violet { background: var(--violet); }

    .lane-list, .finding-list { display: grid; gap: 10px; }
    .lane-section { margin-bottom: 16px; }

    .finding {
      display: grid;
      grid-template-columns: 1fr minmax(160px, auto);
      gap: 12px;
      align-items: start;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      padding: 12px;
      box-shadow: var(--shadow);
    }

    .finding-title { font-weight: 700; margin-bottom: 6px; }
    .finding.hook_problem { border-left: 4px solid var(--red); }
    .finding.remaster, .finding.clip_more { border-left: 4px solid var(--teal); }
    .finding.scale, .finding.funnel_winner { border-left: 4px solid var(--green); }
    .finding.retitle { border-left: 4px solid var(--orange); }
    .finding.ignore { border-left: 4px solid var(--line); }

    .empty {
      border: 1px dashed var(--line);
      border-radius: 8px;
      padding: 16px;
      color: var(--muted);
      background: rgba(255, 255, 255, 0.7);
    }

    .summary-action {
      border-left: 4px solid var(--blue);
      padding-left: 12px;
      margin-top: 10px;
    }

    @media (max-width: 1100px) {
      .grid.stats { grid-template-columns: repeat(3, minmax(140px, 1fr)); }
      .grid.two, .grid.three { grid-template-columns: 1fr; }
    }

    @media (max-width: 720px) {
      .shell { width: min(100vw - 20px, 1500px); padding-top: 14px; }
      header { grid-template-columns: 1fr; }
      .status-strip { justify-content: flex-start; }
      .grid.stats { grid-template-columns: repeat(2, minmax(120px, 1fr)); }
      .toolbar { grid-template-columns: 1fr; }
      .finding { grid-template-columns: 1fr; }
      .bar-row { grid-template-columns: 1fr; gap: 4px; }
      h1 { font-size: 24px; }
    }
  </style>
</head>
<body>
  <div class="shell">
    <header>
      <div>
        <h1>YouTube Analytics Dashboard</h1>
        <div class="meta" id="dashboard-meta"></div>
      </div>
      <div class="status-strip" id="status-strip"></div>
    </header>

    <nav class="tabs" aria-label="Dashboard tabs">
      <button class="tab active" data-tab="action-board">Action Board</button>
      <button class="tab" data-tab="overview">Overview</button>
      <button class="tab" data-tab="videos">Videos</button>
      <button class="tab" data-tab="gaps">Data Gaps</button>
    </nav>

    <section class="panel active" id="action-board"></section>
    <section class="panel" id="overview"></section>
    <section class="panel" id="videos"></section>
    <section class="panel" id="gaps"></section>
  </div>

  <script type="application/json" id="dashboard-data">__DASHBOARD_JSON__</script>
  <script>
    const data = JSON.parse(document.getElementById("dashboard-data").textContent);
    const decisionOrder = ["scale", "funnel_winner", "clip_more", "retitle", "hook_problem", "remaster", "ignore"];
    const laneOrder = ["do_now", "waiting_for_ctr", "needs_studio_check", "watch"];
    const categoryLabels = {
      scale: "Scale",
      funnel_winner: "Funnel Winner",
      clip_more: "Clip More",
      retitle: "Retitle",
      hook_problem: "Hook Problem",
      remaster: "Remaster",
      ignore: "Ignore"
    };
    const laneColor = {
      do_now: "green",
      waiting_for_ctr: "orange",
      needs_studio_check: "violet",
      watch: "teal"
    };
    const horizonOrder = ["daily", "weekly", "monthly"];
    let currentHorizon = ((data.ui_defaults || {}).default_horizon || "weekly");
    let showEmptyBuckets = Boolean((data.ui_defaults || {}).show_empty_buckets);
    let videoSort = { ...((data.sort_defaults || {}).videos || { key: "score", direction: "desc" }) };

    function escapeHtml(value) {
      return String(value ?? "").replace(/[&<>"']/g, (char) => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
      })[char]);
    }

    function fmtNumber(value, digits = 0) {
      if (value === null || value === undefined || Number.isNaN(Number(value))) return "-";
      return new Intl.NumberFormat(undefined, { maximumFractionDigits: digits }).format(Number(value));
    }

    function fmtPercent(value) {
      if (value === null || value === undefined || Number.isNaN(Number(value))) return "-";
      return `${fmtNumber(value, 1)}%`;
    }

    function labelFor(field) {
      return (data.readable_field_labels || {})[field] || field;
    }

    function linkFor(item) {
      const title = escapeHtml(item.title || item.video_id || "Untitled");
      if (!item.url) return title;
      return `<a href="${escapeHtml(item.url)}" target="_blank" rel="noreferrer">${title}</a>`;
    }

    function badge(category) {
      return `<span class="badge ${escapeHtml(category)}">${escapeHtml(categoryLabels[category] || category)}</span>`;
    }

    function stat(label, value) {
      return `<div class="card"><span class="stat-value">${escapeHtml(value)}</span><span class="stat-label">${escapeHtml(label)}</span></div>`;
    }

    function horizonMeta() {
      return (data.horizons || {})[currentHorizon] || { label: currentHorizon, description: "" };
    }

    function metricFor(item) {
      const row = ((item.horizon_metrics || {})[currentHorizon] || {});
      return row.metrics || item.metrics || {};
    }

    function horizonRangeFor(item) {
      const row = ((item.horizon_metrics || {})[currentHorizon] || {});
      if (currentHorizon === "daily") return row.day || "latest day";
      if (row.start_date && row.end_date) return `${row.start_date} to ${row.end_date}`;
      return horizonMeta().label || currentHorizon;
    }

    function horizonControl() {
      return `
        <div class="horizon-control" aria-label="Metric horizon">
          ${horizonOrder.map((key) => {
            const meta = (data.horizons || {})[key] || { label: key };
            return `<button class="horizon-btn ${key === currentHorizon ? "active" : ""}" data-horizon="${escapeHtml(key)}">${escapeHtml(meta.label)}</button>`;
          }).join("")}
        </div>
      `;
    }

    function bindHorizonControls() {
      document.querySelectorAll("[data-horizon]").forEach((button) => {
        button.addEventListener("click", () => {
          currentHorizon = button.dataset.horizon;
          renderDashboardSections();
        });
      });
    }

    function simpleTable(headers, rows) {
      return `
        <div class="table-wrap">
          <table>
            <thead><tr>${headers.map((head) => `<th>${head}</th>`).join("")}</tr></thead>
            <tbody>${rows.join("") || `<tr><td colspan="${headers.length}" class="muted">No rows.</td></tr>`}</tbody>
          </table>
        </div>
      `;
    }

    function barList(rows, options = {}) {
      const labelKey = options.labelKey || "name";
      const valueKey = options.valueKey || "count";
      const color = options.color || "blue";
      const max = Math.max(...rows.map((row) => Number(row[valueKey]) || 0), 1);
      return `<div class="bar-list">${
        rows.map((row) => {
          const value = Number(row[valueKey]) || 0;
          const width = Math.max(2, Math.round(value / max * 100));
          return `
            <div class="bar-row">
              <div title="${escapeHtml(row[labelKey])}">${escapeHtml(row[labelKey])}</div>
              <div class="bar-track"><div class="bar-fill ${escapeHtml(color)}" style="--bar-width: ${width}%"></div></div>
              <div>${fmtNumber(value, options.digits || 0)}</div>
            </div>
          `;
        }).join("")
      }</div>`;
    }

    function sourceLinks(item) {
      const links = item.source_report_links || [];
      if (!links.length) return "";
      return `<div class="small muted">Source: ${
        links.slice(0, 2).map((link) => `<a href="${escapeHtml(link.url)}">${escapeHtml(link.label)}</a>`).join(", ")
      }${links.length > 2 ? ` +${links.length - 2}` : ""}</div>`;
    }

    function strongestAction() {
      const doNow = ((data.action_lanes || {}).do_now || {}).items || [];
      return doNow[0] || (data.findings.action_items || [])[0] || null;
    }

    function renderMeta() {
      const ledger = data.ledger || {};
      const report = data.report || {};
      document.getElementById("dashboard-meta").textContent =
        `Report ${report.report_date || "-"} | analytics through ${ledger.analytics_end_date || "-"} | generated ${data.generated_at || "-"}`;
      const readOnly = report.read_only && ledger.read_only ? "Read-only" : "Check mode";
      document.getElementById("status-strip").innerHTML = [
        `<span class="badge">${readOnly}</span>`,
        `<span class="badge">${escapeHtml(horizonMeta().label)} view</span>`,
        `<span class="badge">${escapeHtml((data.reporting_status || {}).reach_status_text || "CTR pending")}</span>`,
        `<span class="badge">${fmtNumber(data.totals.actionable_videos)} action items</span>`,
        `<span class="badge">${fmtNumber(data.totals.waiting_for_ctr)} waiting for CTR</span>`
      ].join("");
    }

    function findingCard(item, context) {
      const category = context || item.primary_category || "ignore";
      const metrics = metricFor(item);
      const reason = (item.reasons_by_category || {})[category] || (item.reasons && item.reasons.length ? item.reasons[0] : "");
      const action = (item.actions_by_category || {})[category] || (item.recommended_actions && item.recommended_actions.length ? item.recommended_actions[0] : "");
      return `
        <article class="finding ${escapeHtml(item.primary_category || category)}">
          <div>
            <div class="finding-title">${linkFor(item)}</div>
            <div class="muted">${escapeHtml(reason || "No report reason recorded.")}</div>
            <div>${escapeHtml(action || "Keep watching until a stronger signal appears.")}</div>
            ${sourceLinks(item)}
            <div class="metric-row">
              <span class="metric-chip">${escapeHtml(horizonMeta().label)}: ${escapeHtml(horizonRangeFor(item))}</span>
              <span class="metric-chip">${fmtNumber(metrics.views)} views</span>
              <span class="metric-chip">${fmtNumber(metrics.views_per_day, 1)}/day</span>
              <span class="metric-chip">${fmtPercent(metrics.averageViewPercentage)} avg viewed</span>
              <span class="metric-chip">${fmtPercent(metrics.videoThumbnailImpressionsClickRate)} CTR</span>
              <span class="metric-chip">${fmtNumber((item.funnel || {}).known_downstream_clicks)} downstream clicks</span>
            </div>
          </div>
          <div>${(item.categories || [category]).map(badge).join(" ")}</div>
        </article>
      `;
    }

    function renderActionBoard() {
      const lanes = data.action_lanes || {};
      const strongest = strongestAction();
      const summary = (data.horizon_summaries || {})[currentHorizon] || {};
      const decisionRows = decisionOrder
        .filter((category) => showEmptyBuckets || ((data.findings.summary_counts || {})[category] || 0) > 0)
        .map((category) => ({ name: categoryLabels[category] || category, count: (data.findings.summary_counts || {})[category] || 0 }));
      const laneSections = laneOrder.map((key) => {
        const lane = lanes[key] || { label: key, description: "", items: [] };
        if (!showEmptyBuckets && !lane.items.length) return "";
        const body = lane.items.length
          ? `<div class="lane-list">${lane.items.slice(0, key === "watch" ? 12 : 20).map((item) => findingCard(item)).join("")}</div>`
          : `<div class="empty">No videos in this lane.</div>`;
        return `
          <section class="lane-section">
            <h2>${escapeHtml(lane.label)} <span class="badge">${fmtNumber(lane.count || 0)}</span></h2>
            <p class="muted">${escapeHtml(lane.description || "")}</p>
            ${body}
          </section>
        `;
      }).join("");

      document.getElementById("action-board").innerHTML = `
        <div class="card" style="margin-bottom: 12px;">
          <div style="display: flex; justify-content: space-between; gap: 12px; align-items: center; flex-wrap: wrap;">
            <div>
              <h2 style="margin-bottom: 4px;">${escapeHtml(horizonMeta().label)} Decision View</h2>
              <div class="muted">${escapeHtml(horizonMeta().description || "")}</div>
            </div>
            ${horizonControl()}
          </div>
        </div>
        <div class="grid two">
          <div class="card">
            <h2>${escapeHtml(horizonMeta().label)} Snapshot</h2>
            <div class="metric-row">
              <span class="metric-chip">${fmtNumber(summary.total_views)} views</span>
              <span class="metric-chip">${fmtNumber(summary.total_watch_time_minutes)} watch minutes</span>
              <span class="metric-chip">${fmtPercent(summary.average_view_percentage)} avg viewed</span>
              <span class="metric-chip">${fmtNumber(summary.videos_with_metrics)} videos with data</span>
              <span class="metric-chip">${fmtNumber(data.totals.actionable_videos)} actionable</span>
              <span class="metric-chip">${fmtNumber(data.totals.waiting_for_ctr)} blocked by CTR</span>
              <span class="metric-chip">${fmtNumber(data.totals.needs_studio_check)} need Studio check</span>
              <span class="metric-chip">${escapeHtml((data.reporting_status || {}).reach_status_text || "-")}</span>
            </div>
            ${strongest ? `
              <div class="summary-action">
                <div class="muted">Strongest current action</div>
                <div class="finding-title">${linkFor(strongest)}</div>
                <div>${escapeHtml((strongest.recommended_actions || [])[0] || "Review this item.")}</div>
              </div>
            ` : `<div class="empty">No action items crossed the current thresholds.</div>`}
          </div>
          <div class="card">
            <h2>Decision Counts</h2>
            ${barList(decisionRows, { labelKey: "name", valueKey: "count", color: "teal" })}
            <div class="metric-row">
              <label class="check-chip"><input id="show-empty-buckets" type="checkbox" ${showEmptyBuckets ? "checked" : ""}> Show empty buckets</label>
            </div>
          </div>
        </div>
        <div style="margin-top: 16px;">${laneSections}</div>
      `;
      document.getElementById("show-empty-buckets").addEventListener("change", (event) => {
        showEmptyBuckets = event.target.checked;
        renderDashboardSections();
      });
      bindHorizonControls();
    }

    function renderOverview() {
      const totals = data.totals;
      const summary = (data.horizon_summaries || {})[currentHorizon] || {};
      const metricRows = Object.entries(data.coverage.metrics).map(([name, count]) => ({ name: labelFor(name), count }));
      const decisionRows = decisionOrder.map((category) => ({ name: categoryLabels[category] || category, count: (data.findings.summary_counts || {})[category] || 0 }));
      const packageRows = ((data.package_rollups_by_horizon || {})[currentHorizon] || data.package_rollups || []).slice(0, 10).map((row) => ({
        package: row.package,
        action_items: row.action_items,
        total_views: row.total_views,
        average_view_percentage: row.average_view_percentage
      }));
      const packageTableRows = packageRows.map((row) => `
        <tr>
          <td>${escapeHtml(row.package)}</td>
          <td>${fmtNumber(row.action_items)}</td>
          <td>${fmtNumber(row.total_views)}</td>
          <td>${fmtPercent(row.average_view_percentage)}</td>
        </tr>
      `);
      const sync = data.ledger.reporting_api_sync || {};
      const traffic = ((data.distributions.traffic_sources_by_horizon || {})[currentHorizon] || {});
      document.getElementById("overview").innerHTML = `
        <div class="card" style="margin-bottom: 12px;">
          <div style="display: flex; justify-content: space-between; gap: 12px; align-items: center; flex-wrap: wrap;">
            <div>
              <h2 style="margin-bottom: 4px;">Overview: ${escapeHtml(horizonMeta().label)}</h2>
              <div class="muted">${escapeHtml(horizonMeta().description || "")}</div>
            </div>
            ${horizonControl()}
          </div>
        </div>
        <div class="grid stats">
          ${stat("Videos", fmtNumber(totals.videos))}
          ${stat(`${horizonMeta().label} Views`, fmtNumber(summary.total_views))}
          ${stat("Watch Minutes", fmtNumber(summary.total_watch_time_minutes))}
          ${stat("Avg Viewed", fmtPercent(summary.average_view_percentage))}
          ${stat("Videos With Data", fmtNumber(summary.videos_with_metrics))}
          ${stat("Reach Impressions Ready", fmtNumber(totals.reach_impression_videos))}
        </div>
        <div class="grid three">
          <div class="card"><h2>Status</h2>
            <p>Analytics fresh through <strong>${escapeHtml(data.ledger.analytics_end_date || "-")}</strong>.</p>
            <p>${escapeHtml((data.reporting_status || {}).reach_status_text || "CTR pending")}.</p>
            <p class="muted">Reporting sync last merged ${escapeHtml(sync.merged_at || "-")} from ${fmtNumber(sync.source_file_count)} files.</p>
          </div>
          <div class="card"><h2>Formats</h2>${barList(data.distributions.formats || [], { color: "blue" })}</div>
          <div class="card"><h2>Decision Counts</h2>${barList(decisionRows, { color: "teal" })}</div>
          <div class="card"><h2>${escapeHtml(traffic.label || "Traffic Sources")}</h2>${traffic.note ? `<p class="muted">${escapeHtml(traffic.note)}</p>` : ""}${barList(traffic.sources || [], { labelKey: "source", valueKey: "views", color: "green" })}</div>
          <div class="card"><h2>Metric Coverage</h2>${barList(metricRows, { color: "violet" })}</div>
          <div class="card"><h2>Funnel Snapshot</h2>
            <div class="metric-row">
              <span class="metric-chip">${fmtNumber((data.funnel_rollups.totals || {}).shorts_with_related)} Shorts with related video</span>
              <span class="metric-chip">${fmtNumber((data.funnel_rollups.totals || {}).known_downstream_clicks)} known downstream clicks</span>
              <span class="metric-chip">${fmtNumber((data.funnel_rollups.totals || {}).total_card_clicks)} card clicks</span>
            </div>
          </div>
        </div>
        <div class="card" style="margin-top: 12px;">
          <h2>Package Rollups: ${escapeHtml(horizonMeta().label)}</h2>
          ${simpleTable(["Package", "Action Items", "Views", "Avg Viewed"], packageTableRows)}
        </div>
      `;
      bindHorizonControls();
    }

    function sortValue(item, key) {
      const metrics = metricFor(item);
      if (key === "score") return Number(item.score) || 0;
      if (key === "views") return Number(metrics.views) || 0;
      if (key === "views_per_day") return Number(metrics.views_per_day) || 0;
      if (key === "avg_viewed") return Number(metrics.averageViewPercentage) || 0;
      if (key === "subs") return Number(metrics.subscribersGained) || 0;
      if (key === "impressions") return Number(metrics.videoThumbnailImpressions) || 0;
      if (key === "ctr") return Number(metrics.videoThumbnailImpressionsClickRate) || 0;
      return String(item[key] || "").toLowerCase();
    }

    function matchesQuickFilter(item, filter) {
      const metrics = metricFor(item);
      if (filter === "actionable") return (item.categories || []).some((category) => category !== "ignore");
      if (filter === "shorts") return item.format === "short";
      if (filter === "cinematic") return item.format === "cinematic";
      if (filter === "missing_ctr") return metrics.videoThumbnailImpressions === null || metrics.videoThumbnailImpressionsClickRate === null;
      if (filter === "has_related") return Boolean(item.related_video);
      if (filter === "young") return item.data_age_days !== null && item.data_age_days !== undefined && item.data_age_days < 2;
      return true;
    }

    function renderVideos() {
      const classifications = data.findings.classifications || [];
      const formatOptions = [...new Set(classifications.map((item) => item.format || "unknown"))].sort();
      document.getElementById("videos").innerHTML = `
        <div class="card" style="margin-bottom: 12px;">
          <div style="display: flex; justify-content: space-between; gap: 12px; align-items: center; flex-wrap: wrap;">
            <div>
              <h2 style="margin-bottom: 4px;">Videos: ${escapeHtml(horizonMeta().label)}</h2>
              <div class="muted">Metric columns and sorting use the selected horizon.</div>
            </div>
            ${horizonControl()}
          </div>
        </div>
        <div class="toolbar">
          <input id="video-search" type="search" placeholder="Search title, package, or video ID">
          <select id="category-filter">
            <option value="">All decision buckets</option>
            ${decisionOrder.map((category) => `<option value="${escapeHtml(category)}">${escapeHtml(categoryLabels[category])}</option>`).join("")}
          </select>
          <select id="format-filter">
            <option value="">All formats</option>
            ${formatOptions.map((format) => `<option value="${escapeHtml(format)}">${escapeHtml(format)}</option>`).join("")}
          </select>
        </div>
        <div class="quick-filters" style="margin-bottom: 12px;">
          <label class="check-chip"><input type="checkbox" data-quick-filter="actionable"> Actionable only</label>
          <label class="check-chip"><input type="checkbox" data-quick-filter="shorts"> Shorts</label>
          <label class="check-chip"><input type="checkbox" data-quick-filter="cinematic"> Cinematic</label>
          <label class="check-chip"><input type="checkbox" data-quick-filter="missing_ctr"> Missing CTR</label>
          <label class="check-chip"><input type="checkbox" data-quick-filter="has_related"> Has related video</label>
          <label class="check-chip"><input type="checkbox" data-quick-filter="young"> New or too young</label>
        </div>
        <div id="video-table"></div>
      `;
      const renderTable = () => {
        const search = document.getElementById("video-search").value.toLowerCase();
        const category = document.getElementById("category-filter").value;
        const format = document.getElementById("format-filter").value;
        const quickFilters = [...document.querySelectorAll("[data-quick-filter]:checked")].map((input) => input.dataset.quickFilter);
        const sorted = classifications
          .filter((item) => !category || (item.categories || []).includes(category))
          .filter((item) => !format || item.format === format)
          .filter((item) => quickFilters.every((filter) => matchesQuickFilter(item, filter)))
          .filter((item) => {
            const haystack = `${item.title || ""} ${item.package || ""} ${item.video_id || ""}`.toLowerCase();
            return !search || haystack.includes(search);
          })
          .sort((a, b) => {
            const av = sortValue(a, videoSort.key);
            const bv = sortValue(b, videoSort.key);
            const direction = videoSort.direction === "asc" ? 1 : -1;
            if (av < bv) return -1 * direction;
            if (av > bv) return 1 * direction;
            return 0;
          });
        const rows = sorted.map((item) => {
          const metrics = metricFor(item);
          return `<tr class="row-${escapeHtml(item.primary_category || "ignore")}">
            <td>${linkFor(item)}<div class="muted">${escapeHtml(item.video_id || "")}</div>${sourceLinks(item)}</td>
            <td>${(item.categories || []).map(badge).join(" ")}</td>
            <td>${escapeHtml(item.format || "-")}</td>
            <td>${escapeHtml(item.package || "-")}</td>
            <td>${escapeHtml(horizonRangeFor(item))}</td>
            <td>${fmtNumber(metrics.views)}</td>
            <td>${fmtNumber(metrics.views_per_day, 1)}</td>
            <td>${fmtPercent(metrics.averageViewPercentage)}</td>
            <td>${fmtNumber(metrics.subscribersGained)}</td>
            <td>${fmtNumber(metrics.videoThumbnailImpressions)}</td>
            <td>${fmtPercent(metrics.videoThumbnailImpressionsClickRate)}</td>
          </tr>`;
        });
        const headers = [
          "Video",
          "Buckets",
          "Format",
          "Package",
          "Range",
          `<button class="sort-btn" data-sort="views">Views</button>`,
          `<button class="sort-btn" data-sort="views_per_day">V/day</button>`,
          `<button class="sort-btn" data-sort="avg_viewed">Avg Viewed</button>`,
          `<button class="sort-btn" data-sort="subs">Subs</button>`,
          `<button class="sort-btn" data-sort="impressions">Impr.</button>`,
          `<button class="sort-btn" data-sort="ctr">CTR</button>`
        ];
        document.getElementById("video-table").innerHTML = simpleTable(headers, rows);
        document.querySelectorAll("[data-sort]").forEach((button) => {
          button.addEventListener("click", () => {
            const key = button.dataset.sort;
            videoSort = {
              key,
              direction: videoSort.key === key && videoSort.direction === "desc" ? "asc" : "desc"
            };
            renderTable();
          });
        });
      };
      ["video-search", "category-filter", "format-filter"].forEach((id) => {
        document.getElementById(id).addEventListener("input", renderTable);
      });
      document.querySelectorAll("[data-quick-filter]").forEach((input) => {
        input.addEventListener("change", renderTable);
      });
      bindHorizonControls();
      renderTable();
    }

    function renderGaps() {
      const groupCards = Object.entries(data.data_gap_groups || {}).map(([key, group]) => {
        const rows = (group.fields || []).map((field) => `
          <tr>
            <td>${escapeHtml(field.label)}</td>
            <td>${fmtNumber(field.missing_count)}</td>
            <td>${escapeHtml(field.reporting_job || "-")}</td>
          </tr>
        `);
        return `<div class="card"><h2>${escapeHtml(group.label)}</h2>${simpleTable(["Field", "Missing", "Unlocked By"], rows)}</div>`;
      }).join("");
      const manualRows = Object.entries(data.coverage.manual_fields).map(([field, count]) =>
        `<tr><td>${escapeHtml(labelFor(field))}</td><td>${fmtNumber(count)}</td></tr>`
      );
      const jobRows = data.reporting_jobs.map((job) =>
        `<tr>
          <td>${escapeHtml(job.key)}</td>
          <td>${escapeHtml(job.name || "")}</td>
          <td>${fmtNumber(job.available_report_count)}</td>
          <td>${fmtNumber(job.downloaded_report_count)}</td>
          <td>${escapeHtml(job.latest_report_end_time || "-")}</td>
          <td>${escapeHtml(job.purpose || "")}</td>
        </tr>`
      );
      const parentRows = (data.funnel_rollups.parents || []).slice(0, 12).map((parent) => `
        <tr>
          <td>${parent.parent_url ? `<a href="${escapeHtml(parent.parent_url)}" target="_blank" rel="noreferrer">${escapeHtml(parent.parent_id)}</a>` : escapeHtml(parent.parent_id)}</td>
          <td>${fmtNumber(parent.short_count)}</td>
          <td>${fmtNumber(parent.known_downstream_clicks)}</td>
          <td>${fmtNumber(parent.card_clicks)}</td>
          <td>${fmtNumber(parent.related_video_clicks)}</td>
        </tr>
      `);
      const queryNotes = (data.ledger.query_notes || []).map((note) => `<li>${escapeHtml(note)}</li>`).join("");
      const sync = data.ledger.reporting_api_sync || {};

      document.getElementById("gaps").innerHTML = `
        <div class="grid three">${groupCards}</div>
        <div class="grid two" style="margin-top: 12px;">
          <div class="card"><h2>Manual Field Coverage</h2>${simpleTable(["Field", "Videos"], manualRows)}</div>
          <div class="card">
            <h2>Reporting API Sync</h2>
            <div class="metric-row">
              <span class="metric-chip">Merged ${escapeHtml(sync.merged_at || "-")}</span>
              <span class="metric-chip">${fmtNumber(sync.source_file_count)} files</span>
              <span class="metric-chip">${fmtNumber(sync.videos_updated)} videos updated</span>
            </div>
            <h3 style="margin-top: 14px;">Query Notes</h3>
            ${queryNotes ? `<ul>${queryNotes}</ul>` : `<div class="empty">No API query errors recorded.</div>`}
          </div>
        </div>
        <div class="card" style="margin-top: 12px;"><h2>Funnel Diagnostics</h2>${simpleTable(["Parent", "Related Shorts", "Known Clicks", "Card Clicks", "Related Clicks"], parentRows)}</div>
        <div class="card" style="margin-top: 12px;"><h2>Reporting Jobs</h2>${simpleTable(["Key", "Name", "Available", "Downloaded", "Latest", "Purpose"], jobRows)}</div>
      `;
    }

    function setupTabs() {
      document.querySelectorAll(".tab").forEach((button) => {
        button.addEventListener("click", () => {
          document.querySelectorAll(".tab").forEach((tab) => tab.classList.remove("active"));
          document.querySelectorAll(".panel").forEach((panel) => panel.classList.remove("active"));
          button.classList.add("active");
          document.getElementById(button.dataset.tab).classList.add("active");
        });
      });
    }

    function renderDashboardSections() {
      renderMeta();
      renderActionBoard();
      renderOverview();
      renderVideos();
      renderGaps();
    }

    renderDashboardSections();
    setupTabs();
  </script>
</body>
</html>
"""


if __name__ == "__main__":
    raise SystemExit(main())
