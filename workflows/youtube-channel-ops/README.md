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

### 3. Diagnose Playlist State Or Shorts State

Use the read-first scripts for inspection:

- `list_draft_shorts_today.py`
- `diagnose_shorts_playlist.py`
- `check_duplicates.py`

Use the mutating scripts only after confirming scope:

- `remove_duplicate_playlist_entries.py`
- `update_shorts_descriptions.py`

These mutating scripts default to dry-run. Add `--apply` only when the user clearly wants the channel write.

### 4. Branch To The Correct Next Workflow

- If the task is local slide/audio/caption production, move to [`../youtube-production/README.md`](../youtube-production/README.md).
- If the task is the Operating Agents course or TL;DR series, move to [`../youtube-series-operating-agents/README.md`](../youtube-series-operating-agents/README.md).

## Related Surfaces

- [`../skills/youtube-data-api/`](../skills/youtube-data-api/): broad execution-focused YouTube automation skill.
- [`../skills/youtube-shorts-maintenance/`](../skills/youtube-shorts-maintenance/): focused Shorts maintenance overlay.
- [`../../scripts/README.md`](../../scripts/README.md): render-pipeline scripts used when channel work hands off to local production.
