---
workflow_id: youtube_channel_ops
workflow_kind: module
stability: canonical
workflow_group: operations
runner_mode: guided
default_skill: youtube-data-api
launch_templates: []
required_context:
  - authenticated YouTube channel access or repo auth check path
  - target video ids, playlist ids, or caption targets when mutation is requested
  - local package or series context when the operation is tied to tracked content
expected_outputs:
  - verified channel/auth state or a bounded channel-side maintenance result
  - local record of the mutation target or blocker when the task is package-linked
done_when:
  - the requested channel inspection or bounded maintenance action is complete, or the exact blocker is recorded with the next safe step
approval_gate: required_before_channel_mutation
---

# YouTube Channel Ops

This is the tracked canonical workflow for authenticated YouTube channel operations in this repo: OAuth verification, managed caption recovery, playlist diagnostics, and Shorts maintenance.

Use this workflow for general channel state. Switch to the series workflow only when the task is clearly about Operating Agents.

## Evidence-Backed Defaults

- Verify auth first with the repo check script before assuming the token is healthy.
- Prefer read-only inspection before mutating playlists or metadata.
- `manualSortRequired` is a YouTube Studio precondition, not a script bug. Fix the playlist mode in Studio before retrying order writes.
- Do not spend time trying to automate modern end-screen tiles. This repo relies on description blocks and playlist order instead.
- If writes fail with `quotaExceeded`, continue local prep or subtitle recovery instead of blocking the whole task.
- Inspect repo-specific scripts before running them when they carry hardcoded playlist IDs, dates, or promo text.

## Canonical Flow

### 1. Verify OAuth And Current Channel State

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/auth_and_channel_check.py
```

This can open a browser on first run, writes `.youtube/token.json`, and prints current channel metadata.

### 2. Recover Managed Captions When Needed

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/download_video_captions.py \
  --video-id <VIDEO_ID> \
  --output <path/to/output.srt>
```

Default output is `srt`. The script prefers English `asr` and falls back to watch-page recovery on some 403 paths.

If you only have local audio and need YouTube to generate the timestamps first, use the temporary upload path:

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/recover_transcript_via_temporary_upload.py \
  --audio-path <path/to/audio.m4a-or-mp3> \
  --image-path <path/to/still-image.png> \
  --title "<temporary video title>" \
  --output <path/to/output.srt>
```

This creates an unlisted upload by default, waits for automatic captions, downloads the `.srt`, and deletes the temporary video unless you pass `--keep-video`.

### 3. Diagnose Playlist State Or Shorts State

Use the read-first scripts for inspection:

- `list_draft_shorts_today.py`
- `diagnose_shorts_playlist.py`
- `check_duplicates.py`

Use the mutating scripts only after confirming scope:

- `remove_duplicate_playlist_entries.py`
- `update_shorts_descriptions.py`

These mutating scripts default to dry-run. Add `--apply` only when the user clearly wants the channel write.

### 4. Upload Publication Longform And TL;DR Bundles

When a publication package has both a finished longform MP4 and a TL;DR companion, use the bundle uploader instead of treating them as unrelated one-off uploads:

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/upload_publication_video_bundle.py \
  --longform-file <longform.mp4> \
  --longform-title "<longform title>" \
  --longform-summary "<longform summary>" \
  --longform-playlist-id <VISUAL_DEEP_DIVES_PLAYLIST_ID> \
  --tldr-file <tldr.mp4> \
  --tldr-title "<tldr title>" \
  --tldr-summary "<tldr summary>" \
  --tldr-playlist-id <SUMMARIES_PLAYLIST_ID> \
  --essay-url <canonical essay url> \
  --chapters-file <chapters.txt> \
  --pin-to-top
```

The script is dry-run by default. Add `--apply` only when the titles, summaries, playlist ids, and essay URL are settled.

### 5. Upload Publication Shorts To The Channel

Treat Shorts distribution as its own downstream workflow surface. The validated boundary is:

1. portrait masters already exist under the package
2. upload them
3. add them to the target Shorts playlist
4. set the related-video field to the canonical long-form upload

Use the package wrapper for this path:

```bash
.venv/bin/python scripts/upload_publication_shorts.py \
  --package <publication-package-path-under-publications> \
  --main-video-id <LONGFORM_VIDEO_ID> \
  --playlist-id <SHORTS_PLAYLIST_ID> \
  --essay-url <canonical-essay-url> \
  --full-video-url <longform-youtube-url> \
  --tldr-url <tldr-youtube-url> \
  --apply
```

This script is dry-run by default. It preflights every local clip for `1080x1920`, audio, and YouTube-safe duration; uploads every `*.mp4` in `artifacts/video/shorts/portrait/`; adds them to the target playlist; attempts to set the long-form video as the Shorts related video through the API; and writes an upload report with playlist item IDs, public URLs, related-video update results, local probe data, and YouTube readback status.

The API related-video update is not enough for final verification. For scheduled Shorts, open each Short in YouTube Studio, set the right-side `Related video` card to the intended long-form or cinematic upload, save, wait for the save state to fully settle before leaving the page, then reload the same edit page and confirm the card still shows the intended title. Treat this reload-persistent Studio state as the source of truth before marking the upload batch complete.

If there is no canonical essay URL, pass `--essay-url none`, `--essay-url skip`, or `--essay-url omit`. The uploader will leave the `Original essay` line out of the description rather than publishing a placeholder.

If the package has a `shorts_manifest.json`, pass it so the upload uses:

- explicit titles and summaries
- stable ordering
- optional scheduled release times via `publishAt`

```bash
.venv/bin/python scripts/upload_publication_shorts.py \
  --package <publication-package-path-under-publications> \
  --main-video-id <LONGFORM_VIDEO_ID> \
  --playlist-id <SHORTS_PLAYLIST_ID> \
  --essay-url <canonical-essay-url> \
  --full-video-url <longform-youtube-url> \
  --tldr-url <tldr-youtube-url> \
  --manifest <shorts_manifest.json> \
  --apply
```

For scheduled release, set explicit UTC `publish_at` values in the manifest. A practical default is `2` to `3` Shorts per day at fixed local times rather than dumping the batch all at once.

Do not merge this with Shorts creation logic in the same workflow surface. Keep `clip selection -> portrait conversion/render` as the upstream phase, and treat upload-plus-linking as the downstream phase that can be frozen and reused independently.

For ad hoc clips that arrive outside the package folder, use the local clip wrapper:

```bash
.venv/bin/python scripts/upload_ad_hoc_shorts.py \
  <mp4-file-or-directory> \
  --main-video-id <LONGFORM_VIDEO_ID> \
  --playlist-id <SHORTS_PLAYLIST_ID> \
  --full-video-url <longform-youtube-url> \
  --report-file <path/to/upload_report.json> \
  --apply
```

If those inputs are still landscape, add `--convert-from-landscape --work-dir <portrait-output-dir>` to produce portrait masters before upload. The same preflight and report behavior applies.

### 6. Run The Weekly Analytics Decision Loop

Use the analytics loop after production, upload, and related-video verification have settled. This is a recommendation-only workflow: it reads YouTube Data API, YouTube Analytics API, and YouTube Reporting API state; writes local reports; and never edits titles, descriptions, visibility, playlists, related-video settings, uploads, or channel publishing state.

Refresh the metrics ledger:

```bash
.venv/bin/python scripts/fetch_youtube_analytics.py --since-days 30
```

Sync delayed bulk Reporting API exports, including thumbnail reach and card fields when files are available:

```bash
.venv/bin/python scripts/sync_youtube_reporting_reports.py --since-days 30
```

Build the weekly recommendation report:

```bash
.venv/bin/python scripts/build_youtube_decision_report.py
```

Build the local review dashboard:

```bash
.venv/bin/python scripts/build_youtube_analytics_dashboard.py
```

The default outputs are:

- `experiments/youtube-analytics/metrics_ledger.json`
- `experiments/youtube-analytics/reporting_jobs.json`
- `experiments/youtube-analytics/reporting_downloads/`
- `experiments/youtube-analytics/weekly_reports/YYYY-MM-DD.md`
- `experiments/youtube-analytics/weekly_reports/YYYY-MM-DD.json`
- `experiments/youtube-analytics/dashboard/index.html`

If the cached OAuth token predates Analytics access, the fetch script will stop with a reauth instruction. Run:

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/auth_and_channel_check.py
```

The report buckets videos into `scale`, `clip_more`, `remaster`, `retitle`, `hook_problem`, `funnel_winner`, and `ignore`. Treat those as production recommendations only. Title changes, unlisting, remasters, uploads, and related-video fixes remain separate confirmed workflows.

Thumbnail impressions and CTR come from Reporting API reach jobs, not the targeted Analytics API query path. If `reporting_downloads/` has no reach CSVs yet, rerun the sync later; Google generates Reporting API files asynchronously after the job exists.

Studio-only observations can be filled into the ledger manually when needed: related-video clicks, card/end-screen clicks, retention notes, thumbnail/title observations, and Studio related-video verification.

### 7. Branch To The Correct Next Workflow

- If the task is local slide/audio/caption production, move to [`../youtube-production/README.md`](../youtube-production/README.md).
- If the task is the Operating Agents course or TL;DR series, move to [`../youtube-series-operating-agents/README.md`](../youtube-series-operating-agents/README.md).

## Related Surfaces

- [`../skills/youtube-data-api/`](../skills/youtube-data-api/): broad execution-focused YouTube automation skill.
- [`../skills/youtube-shorts-maintenance/`](../skills/youtube-shorts-maintenance/): focused Shorts maintenance overlay.
- [`../../scripts/README.md`](../../scripts/README.md): render-pipeline scripts used when channel work hands off to local production.
