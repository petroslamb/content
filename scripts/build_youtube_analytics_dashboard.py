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


def compact_classification(classification: dict[str, Any]) -> dict[str, Any]:
    metrics = classification.get("metrics") or {}
    categories = classification.get("categories") or ["ignore"]
    reasons = classification.get("reasons") or []
    reasons_by_category = {
        category: reasons[index]
        for index, category in enumerate(categories)
        if index < len(reasons)
    }
    return {
        "video_id": classification.get("video_id"),
        "title": classification.get("title"),
        "url": classification.get("url"),
        "format": classification.get("format") or "unknown",
        "package": classification.get("package") or "unknown",
        "published_at": classification.get("published_at"),
        "selected_window": classification.get("selected_window"),
        "categories": categories,
        "reasons": reasons,
        "reasons_by_category": reasons_by_category,
        "recommended_actions": classification.get("recommended_actions") or [],
        "actions_by_category": classification.get("actions_by_category") or {},
        "manual_fields_missing": classification.get("manual_fields_missing") or [],
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


def summarize_findings(report_summary: dict[str, Any]) -> dict[str, Any]:
    compact = [compact_classification(item) for item in report_summary.get("classifications") or []]
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


def build_dashboard_payload(
    ledger: dict[str, Any],
    report_summary: dict[str, Any],
    reporting_jobs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    videos = ledger.get("videos") or []
    format_counts = Counter(video.get("format") or "unknown" for video in videos)
    privacy_counts = Counter(video.get("privacy_status") or "unknown" for video in videos)
    package_counts = Counter(video.get("package") or "unknown" for video in videos)
    findings = summarize_findings(report_summary)

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

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
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
        },
        "distributions": {
            "formats": sorted_counter(format_counts),
            "privacy": sorted_counter(privacy_counts),
            "top_packages": sorted_counter(package_counts, limit=15),
            "traffic_sources_7d": summarize_traffic(videos),
            "creator_content_type_7d": summarize_content_type(videos),
        },
        "coverage": {
            "windows": summarize_windows(videos),
            "metrics": summarize_metric_availability(videos),
            "manual_fields": summarize_manual_availability(videos),
        },
        "reporting_jobs": reporting_job_rows,
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
      width: min(1480px, calc(100vw - 32px));
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

    h1 {
      margin: 0;
      font-size: 30px;
      line-height: 1.15;
      letter-spacing: 0;
    }

    h2 {
      margin: 0 0 12px;
      font-size: 18px;
      letter-spacing: 0;
    }

    h3 {
      margin: 0 0 10px;
      font-size: 15px;
      letter-spacing: 0;
    }

    .meta {
      color: var(--muted);
      font-size: 13px;
      margin-top: 8px;
    }

    .status-strip {
      display: flex;
      flex-wrap: wrap;
      justify-content: flex-end;
      gap: 8px;
    }

    .badge {
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

    .panel {
      display: none;
    }

    .panel.active {
      display: block;
    }

    .grid {
      display: grid;
      gap: 12px;
    }

    .grid.stats {
      grid-template-columns: repeat(6, minmax(140px, 1fr));
      margin-bottom: 14px;
    }

    .grid.two {
      grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    }

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
      margin-bottom: 12px;
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
      min-width: 760px;
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

    tr:last-child td {
      border-bottom: 0;
    }

    a {
      color: var(--blue);
      text-decoration: none;
    }

    a:hover {
      text-decoration: underline;
    }

    .muted {
      color: var(--muted);
    }

    .finding-list {
      display: grid;
      gap: 10px;
    }

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

    .finding-title {
      font-weight: 700;
      margin-bottom: 6px;
    }

    .metric-row {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 8px;
    }

    .metric-chip {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 5px 7px;
      background: #fbfcfa;
      color: var(--muted);
      font-size: 12px;
    }

    .category-section {
      margin-bottom: 16px;
    }

    .empty {
      border: 1px dashed var(--line);
      border-radius: 8px;
      padding: 16px;
      color: var(--muted);
      background: rgba(255, 255, 255, 0.7);
    }

    @media (max-width: 1100px) {
      .grid.stats { grid-template-columns: repeat(3, minmax(140px, 1fr)); }
      .grid.two { grid-template-columns: 1fr; }
    }

    @media (max-width: 720px) {
      .shell { width: min(100vw - 20px, 1480px); padding-top: 14px; }
      header { grid-template-columns: 1fr; }
      .status-strip { justify-content: flex-start; }
      .grid.stats { grid-template-columns: repeat(2, minmax(120px, 1fr)); }
      .toolbar { grid-template-columns: 1fr; }
      .finding { grid-template-columns: 1fr; }
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
      <button class="tab active" data-tab="overview">Overview</button>
      <button class="tab" data-tab="findings">Findings</button>
      <button class="tab" data-tab="videos">Videos</button>
      <button class="tab" data-tab="gaps">Data Gaps</button>
    </nav>

    <section class="panel active" id="overview"></section>
    <section class="panel" id="findings"></section>
    <section class="panel" id="videos"></section>
    <section class="panel" id="gaps"></section>
  </div>

  <script type="application/json" id="dashboard-data">__DASHBOARD_JSON__</script>
  <script>
    const data = JSON.parse(document.getElementById("dashboard-data").textContent);
    const decisionOrder = ["scale", "funnel_winner", "clip_more", "retitle", "hook_problem", "remaster", "ignore"];
    const categoryLabels = {
      scale: "Scale",
      funnel_winner: "Funnel Winner",
      clip_more: "Clip More",
      retitle: "Retitle",
      hook_problem: "Hook Problem",
      remaster: "Remaster",
      ignore: "Ignore"
    };

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

    function simpleTable(headers, rows) {
      return `
        <div class="table-wrap">
          <table>
            <thead><tr>${headers.map((head) => `<th>${escapeHtml(head)}</th>`).join("")}</tr></thead>
            <tbody>${rows.join("") || `<tr><td colspan="${headers.length}" class="muted">No rows.</td></tr>`}</tbody>
          </table>
        </div>
      `;
    }

    function renderMeta() {
      const ledger = data.ledger || {};
      const report = data.report || {};
      document.getElementById("dashboard-meta").textContent =
        `Report ${report.report_date || "-"} | analytics through ${ledger.analytics_end_date || "-"} | generated ${data.generated_at || "-"}`;
      const readOnly = report.read_only && ledger.read_only ? "Read-only" : "Check mode";
      const reachReady = data.totals.ctr_videos > 0 ? "CTR ready" : "CTR pending";
      document.getElementById("status-strip").innerHTML = [
        `<span class="badge">${readOnly}</span>`,
        `<span class="badge">${reachReady}</span>`,
        `<span class="badge">${fmtNumber(data.totals.actionable_videos)} action items</span>`
      ].join("");
    }

    function renderOverview() {
      const totals = data.totals;
      const windows = data.coverage.windows;
      const metricRows = Object.entries(data.coverage.metrics).map(([name, count]) =>
        `<tr><td>${escapeHtml(name)}</td><td>${fmtNumber(count)}</td></tr>`
      );
      const formatRows = data.distributions.formats.map((row) =>
        `<tr><td>${escapeHtml(row.name)}</td><td>${fmtNumber(row.count)}</td></tr>`
      );
      const privacyRows = data.distributions.privacy.map((row) =>
        `<tr><td>${escapeHtml(row.name)}</td><td>${fmtNumber(row.count)}</td></tr>`
      );
      const packageRows = data.distributions.top_packages.map((row) =>
        `<tr><td>${escapeHtml(row.name)}</td><td>${fmtNumber(row.count)}</td></tr>`
      );
      const windowRows = Object.entries(windows).map(([label, row]) =>
        `<tr><td>${escapeHtml(label)}</td><td>${fmtNumber(row.usable)}</td><td>${fmtNumber(row.with_views)}</td><td>${fmtNumber(row.missing)}</td></tr>`
      );
      const trafficRows = data.distributions.traffic_sources_7d.map((row) =>
        `<tr><td>${escapeHtml(row.source)}</td><td>${fmtNumber(row.views)}</td></tr>`
      );

      document.getElementById("overview").innerHTML = `
        <div class="grid stats">
          ${stat("Videos", fmtNumber(totals.videos))}
          ${stat("Action Items", fmtNumber(totals.actionable_videos))}
          ${stat("Traffic Source Coverage", fmtNumber(totals.traffic_source_videos))}
          ${stat("Daily Metric Coverage", fmtNumber(totals.daily_metric_videos))}
          ${stat("Reach Impressions Ready", fmtNumber(totals.reach_impression_videos))}
          ${stat("CTR Ready", fmtNumber(totals.ctr_videos))}
        </div>
        <div class="grid two">
          <div class="card"><h2>Analytics Windows</h2>${simpleTable(["Window", "Usable", "With Views", "Missing"], windowRows)}</div>
          <div class="card"><h2>Metric Availability</h2>${simpleTable(["Metric", "Rows"], metricRows)}</div>
          <div class="card"><h2>Formats</h2>${simpleTable(["Format", "Videos"], formatRows)}</div>
          <div class="card"><h2>Privacy</h2>${simpleTable(["Privacy", "Videos"], privacyRows)}</div>
          <div class="card"><h2>Top Packages</h2>${simpleTable(["Package", "Videos"], packageRows)}</div>
          <div class="card"><h2>Traffic Sources</h2>${simpleTable(["7d Source", "Views"], trafficRows)}</div>
        </div>
      `;
    }

    function findingCard(item, category) {
      const metrics = item.metrics || {};
      const reason = (item.reasons_by_category || {})[category] || (item.reasons && item.reasons.length ? item.reasons[0] : "");
      const action = (item.actions_by_category || {})[category] || (item.recommended_actions && item.recommended_actions.length ? item.recommended_actions[0] : "");
      return `
        <article class="finding">
          <div>
            <div class="finding-title">${linkFor(item)}</div>
            <div class="muted">${escapeHtml(reason)}</div>
            <div>${escapeHtml(action)}</div>
            <div class="metric-row">
              <span class="metric-chip">${escapeHtml(item.selected_window || "-")}</span>
              <span class="metric-chip">${fmtNumber(metrics.views)} views</span>
              <span class="metric-chip">${fmtNumber(metrics.views_per_day, 1)}/day</span>
              <span class="metric-chip">${fmtPercent(metrics.averageViewPercentage)} avg viewed</span>
              <span class="metric-chip">${fmtPercent(metrics.videoThumbnailImpressionsClickRate)} CTR</span>
            </div>
          </div>
          <div>${(item.categories || [category]).map(badge).join(" ")}</div>
        </article>
      `;
    }

    function renderFindings() {
      const summaryRows = decisionOrder.map((category) =>
        `<tr><td>${badge(category)}</td><td>${fmtNumber((data.findings.summary_counts || {})[category] || 0)}</td></tr>`
      );
      const sections = decisionOrder
        .filter((category) => category !== "ignore")
        .map((category) => {
          const rows = (data.findings.by_category[category] || []);
          const body = rows.length
            ? `<div class="finding-list">${rows.map((item) => findingCard(item, category)).join("")}</div>`
            : `<div class="empty">No videos in this bucket.</div>`;
          return `<section class="category-section"><h2>${escapeHtml(categoryLabels[category])}</h2>${body}</section>`;
        })
        .join("");

      document.getElementById("findings").innerHTML = `
        <div class="grid two">
          <div class="card"><h2>Decision Counts</h2>${simpleTable(["Bucket", "Videos"], summaryRows)}</div>
          <div class="card">
            <h2>Current Read</h2>
            <p class="muted">The report is recommendation-only. CTR-dependent buckets stay conservative until reach reports populate thumbnail impressions and CTR.</p>
            <div class="metric-row">
              <span class="metric-chip">${fmtNumber(data.findings.action_items.length)} actionable</span>
              <span class="metric-chip">${fmtNumber(data.findings.ignored_count)} waiting</span>
              <span class="metric-chip">${fmtNumber(data.totals.ctr_videos)} with CTR</span>
            </div>
          </div>
        </div>
        <div style="margin-top: 16px;">${sections}</div>
      `;
    }

    function renderVideos() {
      const classifications = data.findings.classifications || [];
      const formatOptions = [...new Set(classifications.map((item) => item.format || "unknown"))].sort();
      document.getElementById("videos").innerHTML = `
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
        <div id="video-table"></div>
      `;
      const renderTable = () => {
        const search = document.getElementById("video-search").value.toLowerCase();
        const category = document.getElementById("category-filter").value;
        const format = document.getElementById("format-filter").value;
        const rows = classifications
          .filter((item) => !category || (item.categories || []).includes(category))
          .filter((item) => !format || item.format === format)
          .filter((item) => {
            const haystack = `${item.title || ""} ${item.package || ""} ${item.video_id || ""}`.toLowerCase();
            return !search || haystack.includes(search);
          })
          .map((item) => {
            const metrics = item.metrics || {};
            return `<tr>
              <td>${linkFor(item)}<div class="muted">${escapeHtml(item.video_id || "")}</div></td>
              <td>${(item.categories || []).map(badge).join(" ")}</td>
              <td>${escapeHtml(item.format || "-")}</td>
              <td>${escapeHtml(item.package || "-")}</td>
              <td>${escapeHtml(item.selected_window || "-")}</td>
              <td>${fmtNumber(metrics.views)}</td>
              <td>${fmtNumber(metrics.views_per_day, 1)}</td>
              <td>${fmtPercent(metrics.averageViewPercentage)}</td>
              <td>${fmtNumber(metrics.videoThumbnailImpressions)}</td>
              <td>${fmtPercent(metrics.videoThumbnailImpressionsClickRate)}</td>
            </tr>`;
          });
        document.getElementById("video-table").innerHTML = simpleTable(
          ["Video", "Buckets", "Format", "Package", "Window", "Views", "V/day", "Avg Viewed", "Impr.", "CTR"],
          rows
        );
      };
      ["video-search", "category-filter", "format-filter"].forEach((id) => {
        document.getElementById(id).addEventListener("input", renderTable);
      });
      renderTable();
    }

    function renderGaps() {
      const missingRows = data.findings.manual_missing_counts.map((row) =>
        `<tr><td>${escapeHtml(row.name)}</td><td>${fmtNumber(row.count)}</td></tr>`
      );
      const manualRows = Object.entries(data.coverage.manual_fields).map(([field, count]) =>
        `<tr><td>${escapeHtml(field)}</td><td>${fmtNumber(count)}</td></tr>`
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
      const queryNotes = (data.ledger.query_notes || []).map((note) => `<li>${escapeHtml(note)}</li>`).join("");
      const sync = data.ledger.reporting_api_sync || {};

      document.getElementById("gaps").innerHTML = `
        <div class="grid two">
          <div class="card"><h2>Missing Fields In Findings</h2>${simpleTable(["Field", "Videos"], missingRows)}</div>
          <div class="card"><h2>Manual Field Coverage</h2>${simpleTable(["Field", "Videos"], manualRows)}</div>
          <div class="card">
            <h2>Reporting API Sync</h2>
            <div class="metric-row">
              <span class="metric-chip">Merged ${escapeHtml(sync.merged_at || "-")}</span>
              <span class="metric-chip">${fmtNumber(sync.source_file_count)} files</span>
              <span class="metric-chip">${fmtNumber(sync.videos_updated)} videos updated</span>
            </div>
          </div>
          <div class="card">
            <h2>Query Notes</h2>
            ${queryNotes ? `<ul>${queryNotes}</ul>` : `<div class="empty">No API query errors recorded.</div>`}
          </div>
        </div>
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

    renderMeta();
    renderOverview();
    renderFindings();
    renderVideos();
    renderGaps();
    setupTabs();
  </script>
</body>
</html>
"""


if __name__ == "__main__":
    raise SystemExit(main())
