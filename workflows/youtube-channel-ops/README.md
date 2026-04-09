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

This script is dry-run by default. It uploads every `*.mp4` in `artifacts/video/shorts/portrait/`, adds them to the target playlist, and attempts to set the long-form video as the Shorts related video through the API.

Do not merge this with Shorts creation logic in the same workflow surface. Keep `clip selection -> portrait conversion/render` as the upstream phase, and treat upload-plus-linking as the downstream phase that can be frozen and reused independently.

### 6. Branch To The Correct Next Workflow

- If the task is local slide/audio/caption production, move to [`../youtube-production/README.md`](../youtube-production/README.md).
- If the task is the Operating Agents course or TL;DR series, move to [`../youtube-series-operating-agents/README.md`](../youtube-series-operating-agents/README.md).

## Related Surfaces

- [`../skills/youtube-data-api/`](../skills/youtube-data-api/): broad execution-focused YouTube automation skill.
- [`../skills/youtube-shorts-maintenance/`](../skills/youtube-shorts-maintenance/): focused Shorts maintenance overlay.
- [`../../scripts/README.md`](../../scripts/README.md): render-pipeline scripts used when channel work hands off to local production.
