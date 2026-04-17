---
name: youtube-data-api
description: Use when Codex needs to work with the repository's YouTube Data API automation for OAuth setup, authenticated channel inspection, caption download, playlist maintenance, Shorts draft review, or Operating Agents upload and replacement workflows under workflows/skills/youtube-data-api/.
---

# YouTube Data API

Use this skill for the repo's existing YouTube automation, not for generic YouTube advice. Prefer the local scripts in `workflows/skills/youtube-data-api/scripts/` over rewriting API calls from scratch.

## Working Rules

1. Run everything from the repo root with the repo-local environment: `.venv/bin/python ...`.
2. Expect credentials at `.youtube/client_secret.json` and `.youtube/token.json`. Treat both as secrets.
3. Verify auth with `workflows/skills/youtube-data-api/scripts/auth_and_channel_check.py` before assuming the token is valid.
4. Prefer read-only inspection first. Run mutating scripts only when the user clearly wants a channel change.
5. Treat scripts with hardcoded playlist IDs, target dates, or promotional copy as one-off repo operations. Read them before running them.
6. For Operating Agents workflows, treat `workflows/skills/youtube-data-api/references/operating_agents_tldr_metadata.json` as the local source of truth for ordering and cross-links.
7. When the YouTube Data API quota is exhausted, continue local alignment and rendering work, and switch subtitle recovery to `yt-dlp` instead of blocking the whole workflow.
8. For slide/audio/transcript alignment and narrated MP4 rendering, switch to the companion `youtube-slide-video-pipeline` skill instead of loading that workflow into this broader API skill.

## Choose The Workflow

### OAuth And Channel Check

Use this first when auth is unverified or the user wants the current channel identity:

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/auth_and_channel_check.py
```

This script can open a local browser for OAuth on first run, writes `.youtube/token.json`, and prints channel metadata as JSON.

### Caption Download

Use this when the user needs captions for a managed video:

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/download_video_captions.py \
  --video-id <VIDEO_ID> \
  --output <path/to/output.srt>
```

Notes:

- Default output format is `srt`.
- Default track preference is English `asr`.
- The script falls back to scraping the watch page if the captions download API returns 403.

### Local Slide And Audio Production

Use the companion `youtube-slide-video-pipeline` skill for OCR-backed alignment, cue-sheet verification, subtitle recovery, and slideshow rendering. Keep this skill focused on auth, managed captions, playlist state, and upload or replacement operations.

### Playlist Diagnostics And Cleanup

Use these scripts for repo-specific Shorts playlist maintenance:

- `list_draft_shorts_today.py`: inspect current draft uploads for a given date.
- `diagnose_shorts_playlist.py`: inspect status and upload-date distribution for a playlist.
- `check_duplicates.py`: report duplicate video IDs in a playlist.
- `remove_duplicate_playlist_entries.py`: plan or apply duplicate cleanup for playlist items.
- `update_shorts_descriptions.py`: plan or apply description updates from a template file.

These scripts now accept explicit playlist/date inputs, and the mutating ones default to dry-run.

### Publication Longform Plus TL;DR Uploads

Use this when a publication package has a finished longform video, a TL;DR companion, target playlists, and a canonical essay URL:

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/upload_publication_video_bundle.py \
  --longform-file <longform.mp4> \
  --longform-title "<longform title>" \
  --longform-summary "<one-paragraph summary>" \
  --longform-playlist-id <VISUAL_DEEP_DIVES_PLAYLIST_ID> \
  --tldr-file <tldr.mp4> \
  --tldr-title "<tldr title>" \
  --tldr-summary "<short summary>" \
  --tldr-playlist-id <SUMMARIES_PLAYLIST_ID> \
  --essay-url <substack-or-canonical-essay-url> \
  --chapters-file <chapters.txt> \
  --pin-to-top
```

The script is dry-run by default. Add `--apply` to upload both videos, add them to playlists, cross-link the descriptions, and pin them to the top of their playlists when requested.

### Publication Shorts Distribution

Use this after the portrait Shorts masters already exist inside a package. Keep this downstream from Shorts creation; do not mix clip-selection logic into this step.

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

This wrapper is dry-run by default. It preflights every local portrait clip for `1080x1920`, audio, and a default maximum duration of `180` seconds; uploads all portrait Shorts in the package folder; adds them to the target playlist; attempts to set the long-form upload as the Shorts related video; then writes a structured upload report with local probe data, playlist item IDs, public URLs, and YouTube readback status.

Use `--essay-url none`, `--essay-url skip`, or `--essay-url omit` when there is no canonical essay URL and the description should omit the `Original essay` line.

If a package has `artifacts/video/shorts/shorts_manifest.json`, pass `--manifest` so the wrapper uses explicit titles, summaries, and optional `publishAt` schedule times instead of inferring everything from filenames.

For one-off downloaded or locally edited clips that are not in the canonical package Shorts folder, use the ad hoc wrapper instead of pasting custom upload code:

```bash
.venv/bin/python scripts/upload_ad_hoc_shorts.py \
  <portrait-mp4-or-directory> \
  --main-video-id <LONGFORM_VIDEO_ID> \
  --playlist-id <SHORTS_PLAYLIST_ID> \
  --full-video-url <longform-youtube-url> \
  --report-file <path/to/upload_report.json> \
  --apply
```

When the inputs are still landscape clips, add `--convert-from-landscape --work-dir <portrait-output-dir>` so the script first renders `1080x1920` portrait masters using the repo's blurred-background conversion.

### Operating Agents Uploads, Ordering, And Replacements

Use the Operating Agents scripts when the user is working on the course or TL;DR series:

- `upload_operating_agents_tldrs.py`: plan or apply TL;DR uploads from local metadata, add them to the target playlist, and prepend TL;DR links to the full episodes.
- `sync_operating_agents_playlist_order.py`: compare current playlist order with metadata order, then reorder with `--apply`.
- `sync_operating_agents_crosslinks.py`: rebuild managed navigation blocks in descriptions. It is dry-run by default; add `--apply` to write changes.
- `replace_course_video.py`: plan or apply a replacement full-course upload, playlist swap, and old playlist-entry removal.
- `replace_remaining_course_videos.py`: batch replacement helper for the remaining chapters. It is repo-specific and depends on hardcoded media paths.

After any replacement that changes a full video ID, update local metadata and rerun description sync.

## Reference Map

Read only the reference file you need:

- `../../../workflows/youtube-channel-ops/README.md`: tracked canonical channel-operations workflow for auth, captions, playlist diagnostics, and Shorts maintenance.
- `../../../workflows/youtube-series-operating-agents/README.md`: tracked canonical series workflow when the task is specifically about Operating Agents.
- `references/script-map.md`: command inventory, safety classification, and script-specific caveats.
- `references/operating-agents-workflows.md`: replacement flow, quota fallback, and sequence for Operating Agents course updates.
- `references/rollout-lessons.md`: recovered constraints from prior YouTube runs that explain why certain API paths or safety checks exist.
