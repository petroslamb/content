# YouTube Analytics

Recommendation-only analytics state for YouTube follow-through decisions.

The operational channel workflow lives in [`../../workflows/youtube-channel-ops/README.md`](../../workflows/youtube-channel-ops/README.md). The scripts are documented in [`../../scripts/README.md`](../../scripts/README.md).

## Weekly Sync Loop

Run the loop in this order:

```bash
.venv/bin/python scripts/fetch_youtube_analytics.py --since-days 30
.venv/bin/python scripts/sync_youtube_reporting_reports.py --since-days 30
.venv/bin/python scripts/build_youtube_decision_report.py
.venv/bin/python scripts/build_youtube_analytics_dashboard.py
```

The first command uses the YouTube Data API and YouTube Analytics API for recent/repo-known video inventory, views, watch time, average view duration, average viewed percentage, engagement, traffic sources, and creator content type.

The second command uses the YouTube Reporting API bulk CSV exports. It downloads generated daily reports and merges them into `metrics_ledger.json`. Reporting API files are delayed; newly created jobs may show `0` reports until Google generates daily/backfill files.

The third command builds the recommendation report from the merged ledger. It does not call YouTube.

The fourth command builds a static local dashboard from the ledger and latest weekly report. It does not call YouTube.

## State Files

- `decision_rules.yaml`: local classification rules for recommendation reports
- `reporting_jobs.json`: Reporting API job registry for channel bulk exports
- `metrics_ledger.json`: generated read-only metrics ledger when analytics fetches run
- `reporting_downloads/`: generated Reporting API CSV downloads
- `weekly_reports/`: generated recommendation reports
- `dashboard/`: generated local dashboard HTML and embedded payload

## Reporting Jobs

Current channel jobs:

- `channel_basic_a3` / User activity: user activity plus aggregate card click fields
- `channel_reach_basic_a1` / Reach basic: per-video thumbnail impressions and thumbnail CTR
- `channel_reach_combined_a1` / Reach combined: thumbnail reach by traffic source and device

The reach jobs were created on 2026-04-28. They may take time to produce downloadable CSVs. Once files appear, `sync_youtube_reporting_reports.py` will merge `video_thumbnail_impressions` and `video_thumbnail_impressions_ctr` into the ledger.

If a new environment has no reach jobs, run:

```bash
.venv/bin/python scripts/sync_youtube_reporting_reports.py --ensure-jobs --no-download --no-merge
```

## Boundary

This layer should recommend actions, not mutate videos or channel publishing state. Uploads, playlist edits, related-video fixes, and privacy/scheduling changes still require the YouTube workflow approval boundaries and live API or Studio readback where relevant.

Creating Reporting API jobs is configuration for Google bulk exports, not a video/channel mutation. Keep it explicit with `--ensure-jobs`.
