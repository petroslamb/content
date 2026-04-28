#!/usr/bin/env python3
"""Build a weekly recommendation-only YouTube decision report."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER_PATH = REPO_ROOT / "experiments" / "youtube-analytics" / "metrics_ledger.json"
DEFAULT_RULES_PATH = REPO_ROOT / "experiments" / "youtube-analytics" / "decision_rules.yaml"
DEFAULT_REPORT_DIR = REPO_ROOT / "experiments" / "youtube-analytics" / "weekly_reports"
DECISION_ORDER = [
    "scale",
    "funnel_winner",
    "clip_more",
    "retitle",
    "hook_problem",
    "remaster",
    "ignore",
]
WINDOW_DAYS = {
    "24h": 1,
    "72h": 3,
    "7d": 7,
    "28d": 28,
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n")


def load_rules(path: Path = DEFAULT_RULES_PATH) -> dict[str, Any]:
    return yaml.safe_load(path.read_text()) or {}


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def number(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def metric(window: dict[str, Any] | None, name: str) -> float | None:
    if not window:
        return None
    return number(window.get("metrics", {}).get(name))


def select_window(
    video: dict[str, Any],
    preferred_window: str = "7d",
) -> tuple[str | None, dict[str, Any] | None]:
    windows = video.get("analytics_windows") or {}
    ordered = [preferred_window, "28d", "7d", "72h", "24h"]
    seen: set[str] = set()
    for label in ordered:
        if label in seen:
            continue
        seen.add(label)
        window = windows.get(label)
        if window and not window.get("missing"):
            return label, window
    if preferred_window in windows:
        return preferred_window, windows[preferred_window]
    for label, window in windows.items():
        return label, window
    return None, None


def views_per_day(views: float | None, label: str | None) -> float | None:
    if views is None or not label:
        return None
    days = WINDOW_DAYS.get(label)
    if not days:
        return None
    return views / days


def per_1000(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return numerator / denominator * 1000


def manual_value(video: dict[str, Any], key: str) -> Any:
    observations = video.get("manual_observations")
    if not isinstance(observations, dict):
        return None
    return observations.get(key)


def is_remastered(video: dict[str, Any]) -> bool:
    reports = " ".join(video.get("source_reports") or []).lower()
    return "remastered-overlays" in reports or "overlay" in reports


def add_decision(
    result: dict[str, Any],
    category: str,
    reason: str,
    action: str,
) -> None:
    if category not in result["categories"]:
        result["categories"].append(category)
    result["reasons"].append(reason)
    result["recommended_actions"].append(action)


def classification_sort_key(classification: dict[str, Any]) -> tuple[int, float]:
    categories = classification.get("categories") or ["ignore"]
    priority = min(DECISION_ORDER.index(category) for category in categories if category in DECISION_ORDER)
    return priority, -(classification.get("score") or 0)


def classify_video(
    video: dict[str, Any],
    rules: dict[str, Any],
    *,
    as_of_date: date,
) -> dict[str, Any]:
    preferred_window = rules.get("preferred_window", "7d")
    minimum_data_age_days = int(rules.get("minimum_data_age_days", 2))
    thresholds = rules.get("thresholds", {})
    selected_label, selected_window = select_window(video, preferred_window)
    views = metric(selected_window, "views")
    watch_time = metric(selected_window, "estimatedMinutesWatched")
    avg_view_duration = metric(selected_window, "averageViewDuration")
    avg_view_percentage = metric(selected_window, "averageViewPercentage")
    impressions = metric(selected_window, "videoThumbnailImpressions")
    ctr = metric(selected_window, "videoThumbnailImpressionsClickRate")
    subscribers = metric(selected_window, "subscribersGained")
    vpd = views_per_day(views, selected_label)
    subscribers_per_1000_views = per_1000(subscribers, views)
    published_at = parse_date(video.get("published_at"))
    data_age_days = (as_of_date - published_at).days if published_at else None
    format_name = video.get("format") or "unknown"
    topic = video.get("topic") or video.get("package") or "this topic"

    result: dict[str, Any] = {
        "video_id": video.get("video_id"),
        "title": video.get("title"),
        "url": video.get("url"),
        "format": format_name,
        "package": video.get("package"),
        "topic": topic,
        "published_at": video.get("published_at"),
        "selected_window": selected_label,
        "data_age_days": data_age_days,
        "categories": [],
        "reasons": [],
        "recommended_actions": [],
        "metrics": {
            "views": views,
            "views_per_day": vpd,
            "estimatedMinutesWatched": watch_time,
            "averageViewDuration": avg_view_duration,
            "averageViewPercentage": avg_view_percentage,
            "videoThumbnailImpressions": impressions,
            "videoThumbnailImpressionsClickRate": ctr,
            "subscribersGained": subscribers,
            "subscribers_per_1000_views": subscribers_per_1000_views,
        },
        "manual_fields_missing": [],
        "score": 0.0,
    }

    if data_age_days is not None and data_age_days < minimum_data_age_days:
        add_decision(
            result,
            "ignore",
            f"Only {data_age_days} days old; minimum data age is {minimum_data_age_days}.",
            "Wait for a fuller weekly window before acting.",
        )
        return result

    if not selected_window or selected_window.get("missing"):
        add_decision(
            result,
            "ignore",
            "No usable Analytics row was available for the preferred windows.",
            "Leave it in the ledger and re-check next week.",
        )
        return result

    min_views_for_signal = thresholds.get("min_views_for_signal", 50)
    low_signal_reason = None
    if views is None or views < min_views_for_signal:
        low_signal_reason = (
            f"Views are below the signal floor ({views or 0:g} < {min_views_for_signal})."
        )

    scale = thresholds.get("scale", {})
    if (
        vpd is not None
        and avg_view_percentage is not None
        and vpd >= scale.get("views_per_day", 100)
        and avg_view_percentage >= scale.get("average_view_percentage", 55)
        and (
            subscribers_per_1000_views is None
            or subscribers_per_1000_views >= scale.get("subscribers_per_1000_views", 1.0)
        )
    ):
        add_decision(
            result,
            "scale",
            (
                f"{selected_label} performance clears the scale bar: "
                f"{vpd:.1f} views/day and {avg_view_percentage:.1f}% average viewed."
            ),
            f"Make another {format_name} on {topic} with a similar promise and pacing.",
        )

    clip_more = thresholds.get("clip_more", {})
    if (
        format_name in set(clip_more.get("parent_formats", ["cinematic", "longform", "tldr"]))
        and vpd is not None
        and avg_view_percentage is not None
        and vpd >= clip_more.get("views_per_day", 25)
        and avg_view_percentage >= clip_more.get("average_view_percentage", 40)
    ):
        add_decision(
            result,
            "clip_more",
            (
                f"The parent video is holding attention at {avg_view_percentage:.1f}% "
                f"with {vpd:.1f} views/day."
            ),
            "Extract more Shorts from this parent before moving to a new topic.",
        )

    retitle = thresholds.get("retitle", {})
    if (
        impressions is not None
        and ctr is not None
        and impressions >= retitle.get("min_impressions", 250)
        and ctr < retitle.get("weak_ctr", 3.0)
    ):
        add_decision(
            result,
            "retitle",
            f"Packaging is getting impressions ({impressions:g}) but CTR is only {ctr:.2f}%.",
            "Draft a sharper title/thumbnail variant before changing the video.",
        )

    hook_problem = thresholds.get("hook_problem", {})
    if (
        views is not None
        and avg_view_percentage is not None
        and views >= hook_problem.get("min_views", 75)
        and avg_view_percentage < hook_problem.get("average_view_percentage_below", 35)
    ):
        add_decision(
            result,
            "hook_problem",
            f"Viewers are starting the video, but average viewed is {avg_view_percentage:.1f}%.",
            "Rewrite the first three seconds before producing another variant.",
        )

    remaster = thresholds.get("remaster", {})
    old_format = format_name == "short" and not is_remastered(video)
    if (
        old_format
        and vpd is not None
        and vpd >= remaster.get("views_per_day", 15)
        and (
            avg_view_percentage is None
            or avg_view_percentage < remaster.get("average_view_percentage_below", 45)
            or (ctr is not None and ctr < remaster.get("ctr_below", 4.0))
        )
    ):
        add_decision(
            result,
            "remaster",
            "The topic has some demand, but the Short is still in an older or weaker package.",
            "Queue this Short for the overlay remaster workflow instead of unlisting it immediately.",
        )

    funnel_winner = thresholds.get("funnel_winner", {})
    related_clicks = number(manual_value(video, "related_video_clicks"))
    card_clicks = number(manual_value(video, "card_clicks"))
    end_screen_clicks = number(manual_value(video, "end_screen_clicks"))
    total_known_clicks = sum(value or 0 for value in [related_clicks, card_clicks, end_screen_clicks])
    if total_known_clicks >= funnel_winner.get("min_known_clicks", 3):
        add_decision(
            result,
            "funnel_winner",
            f"Manual Studio fields show {total_known_clicks:g} known downstream clicks.",
            "Keep the related-video target and build more Shorts that point to this parent.",
        )

    if video.get("related_video") and related_clicks is None:
        result["manual_fields_missing"].append("related_video_clicks")
    for field in ["card_clicks", "end_screen_clicks", "retention_notes"]:
        if manual_value(video, field) is None:
            result["manual_fields_missing"].append(field)

    if not result["categories"]:
        reason = (
            low_signal_reason
            or "Metrics are present but do not cross a conservative action threshold."
        )
        add_decision(
            result,
            "ignore",
            reason,
            "Keep it in the weekly ledger and wait for a stronger pattern.",
        )

    result["score"] = sum(
        value or 0
        for value in [
            (vpd or 0) * 2,
            avg_view_percentage,
            subscribers_per_1000_views,
            total_known_clicks * 10,
        ]
    )
    return result


def classify_ledger(
    ledger: dict[str, Any],
    rules: dict[str, Any],
    *,
    as_of_date: date,
) -> list[dict[str, Any]]:
    classifications = [
        classify_video(video, rules, as_of_date=as_of_date)
        for video in ledger.get("videos", [])
    ]
    return sorted(classifications, key=classification_sort_key)


def md_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def fmt_number(value: Any, suffix: str = "") -> str:
    parsed = number(value)
    if parsed is None:
        return "-"
    if abs(parsed) >= 1000:
        return f"{parsed:,.0f}{suffix}"
    if parsed == int(parsed):
        return f"{parsed:.0f}{suffix}"
    return f"{parsed:.1f}{suffix}"


def action_line(classification: dict[str, Any]) -> str:
    category = next(
        (category for category in DECISION_ORDER if category in classification["categories"]),
        "ignore",
    )
    action = classification["recommended_actions"][0]
    title = md_escape(classification.get("title") or classification.get("video_id"))
    url = classification.get("url")
    linked_title = f"[{title}]({url})" if url else title
    metrics = classification["metrics"]
    return (
        f"- `{category}`: {linked_title} - {action} "
        f"({fmt_number(metrics.get('views'))} views, "
        f"{fmt_number(metrics.get('views_per_day'))}/day, "
        f"{fmt_number(metrics.get('averageViewPercentage'), '%')} avg viewed)."
    )


def report_table_rows(
    classifications: list[dict[str, Any]],
    *,
    display_category: str | None = None,
) -> list[str]:
    rows = [
        "| Decision | Video | Window | Views | V/day | Avg viewed | CTR | Action |",
        "| :--- | :--- | :--- | ---: | ---: | ---: | ---: | :--- |",
    ]
    for classification in classifications:
        category = display_category or next(
            (
                candidate
                for candidate in DECISION_ORDER
                if candidate in classification["categories"]
            ),
            "ignore",
        )
        metrics = classification["metrics"]
        title = md_escape(classification.get("title") or classification.get("video_id"))
        url = classification.get("url")
        linked_title = f"[{title}]({url})" if url else title
        rows.append(
            "| "
            + " | ".join(
                [
                    f"`{category}`",
                    linked_title,
                    md_escape(classification.get("selected_window")),
                    fmt_number(metrics.get("views")),
                    fmt_number(metrics.get("views_per_day")),
                    fmt_number(metrics.get("averageViewPercentage"), "%"),
                    fmt_number(metrics.get("videoThumbnailImpressionsClickRate"), "%"),
                    md_escape(classification["recommended_actions"][0]),
                ]
            )
            + " |"
        )
    return rows


def analytics_blocker_from_notes(query_notes: list[dict[str, Any]]) -> str | None:
    note_text = "\n".join(
        str(note.get("error") or note.get("fallback_error") or "")
        for note in query_notes
    )
    if "accessNotConfigured" in note_text or "has not been used in project" in note_text:
        match = re.search(r"https://console\.developers\.google\.com/\S+", note_text)
        link = match.group(0).rstrip('".') if match else "Google Cloud API Library"
        return f"YouTube Analytics API is disabled for this OAuth project. Enable it here: {link}"
    if "insufficientPermissions" in note_text or "insufficient authentication scopes" in note_text:
        return (
            "The cached OAuth token lacks Analytics scopes. Re-run: "
            ".venv/bin/python workflows/skills/youtube-data-api/scripts/auth_and_channel_check.py"
        )
    return None


def build_markdown_report(
    *,
    ledger: dict[str, Any],
    classifications: list[dict[str, Any]],
    report_date: date,
    summary_counts: dict[str, int],
) -> str:
    actionable = [
        item
        for item in classifications
        if any(category != "ignore" for category in item["categories"])
    ]
    missing_manual = [
        item for item in classifications if item.get("manual_fields_missing")
    ]
    query_notes = ledger.get("query_notes") or []
    analytics_blocker = analytics_blocker_from_notes(query_notes)
    lines = [
        f"# YouTube Analytics Decision Report - {report_date.isoformat()}",
        "",
        "Recommendation-only report. It does not edit titles, descriptions, visibility, playlists, uploads, or related-video settings.",
        "",
        "## Summary",
        "",
        f"- Ledger created: `{ledger.get('created_at')}`",
        f"- Analytics end date: `{ledger.get('analytics_end_date')}`",
        f"- Videos reviewed: `{len(classifications)}`",
        f"- Decision counts: "
        + ", ".join(f"`{key}` {value}" for key, value in summary_counts.items()),
    ]
    if analytics_blocker:
        lines.append(f"- Analytics blocker: {analytics_blocker}")
    lines.extend(["", "## Top Recommended Actions", ""])

    if analytics_blocker:
        lines.append("- No recommendations were made because Analytics API metrics were unavailable.")
    elif actionable:
        lines.extend(action_line(item) for item in actionable[:12])
    else:
        lines.append("- No videos crossed the conservative action thresholds.")

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for classification in classifications:
        for category in classification["categories"]:
            grouped[category].append(classification)

    for category in DECISION_ORDER:
        lines.extend(["", f"## {category.replace('_', ' ').title()}", ""])
        rows = grouped.get(category, [])
        if not rows:
            lines.append("- No videos in this bucket.")
            continue
        lines.extend(report_table_rows(rows, display_category=category))

    lines.extend(["", "## Missing Manual Fields", ""])
    if not missing_manual:
        lines.append("- No missing manual fields were flagged.")
    else:
        for item in missing_manual[:20]:
            title = item.get("title") or item.get("video_id")
            lines.append(
                f"- {md_escape(title)}: "
                + ", ".join(f"`{field}`" for field in item["manual_fields_missing"])
            )

    lines.extend(["", "## Data Quality Notes", ""])
    if query_notes:
        if analytics_blocker:
            lines.append(f"- {analytics_blocker}")
        for note in query_notes[:12]:
            lines.append(
                f"- `{note.get('window')}` `{note.get('query')}`: "
                f"{md_escape(note.get('error') or note.get('fallback_error'))}"
            )
    else:
        lines.append("- No API query errors were recorded in the ledger.")
    return "\n".join(lines) + "\n"


def build_summary(
    *,
    ledger: dict[str, Any],
    classifications: list[dict[str, Any]],
    report_date: date,
) -> dict[str, Any]:
    counts: Counter[str] = Counter()
    for classification in classifications:
        for category in classification["categories"]:
            counts[category] += 1
    summary_counts = {category: counts.get(category, 0) for category in DECISION_ORDER}
    query_notes = ledger.get("query_notes") or []
    analytics_blocker = analytics_blocker_from_notes(query_notes)
    return {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "report_date": report_date.isoformat(),
        "workflow": "youtube_analytics_decision_loop",
        "read_only": True,
        "source_ledger_created_at": ledger.get("created_at"),
        "analytics_end_date": ledger.get("analytics_end_date"),
        "analytics_blocker": analytics_blocker,
        "summary_counts": summary_counts,
        "top_actions": [
            {
                "video_id": item["video_id"],
                "title": item["title"],
                "categories": item["categories"],
                "recommended_actions": item["recommended_actions"],
                "metrics": item["metrics"],
            }
            for item in classifications
            if any(category != "ignore" for category in item["categories"])
        ][:12],
        "classifications": classifications,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a weekly recommendation-only YouTube decision report."
    )
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER_PATH)
    parser.add_argument("--rules", type=Path, default=DEFAULT_RULES_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_REPORT_DIR)
    parser.add_argument(
        "--report-date",
        default=datetime.now(timezone.utc).date().isoformat(),
        help="Report date in YYYY-MM-DD format.",
    )
    parser.add_argument("--json-output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report_date = date.fromisoformat(args.report_date)
    ledger = load_json(args.ledger)
    rules = load_rules(args.rules)
    classifications = classify_ledger(ledger, rules, as_of_date=report_date)
    summary = build_summary(
        ledger=ledger,
        classifications=classifications,
        report_date=report_date,
    )
    report_path = args.output_dir / f"{report_date.isoformat()}.md"
    json_path = args.json_output or report_path.with_suffix(".json")
    markdown = build_markdown_report(
        ledger=ledger,
        classifications=classifications,
        report_date=report_date,
        summary_counts=summary["summary_counts"],
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(markdown)
    write_json(json_path, summary)
    print(f"Wrote {report_path}")
    print(f"Wrote {json_path}")


if __name__ == "__main__":
    main()
