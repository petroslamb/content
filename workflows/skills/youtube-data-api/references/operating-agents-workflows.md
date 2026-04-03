# Operating Agents Workflows

Use this file when the task is about the Operating Agents course, TL;DR uploads, playlist order, or full-video replacements.

## Source Of Truth

- Local metadata lives at `workflows/skills/youtube-data-api/references/operating_agents_tldr_metadata.json`.
- Use metadata order as the canonical chapter order for both the course playlist and the TL;DR playlist.
- After a replacement upload changes a full-video ID, update the metadata before resyncing navigation.

## Description Navigation Sync

Use this when full and TL;DR descriptions need consistent next-step links:

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/sync_operating_agents_crosslinks.py \
  --course-playlist-id <COURSE_PLAYLIST_ID>
```

Add `--apply` only when the user wants the write:

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/sync_operating_agents_crosslinks.py \
  --course-playlist-id <COURSE_PLAYLIST_ID> \
  --apply
```

The script manages a marked navigation block, so reruns replace the block instead of duplicating it.

Constraint:

- This workflow exists because end-screen automation is not available through the current Data API surface.

## Playlist Order Sync

Use this when the playlists drift from chapter order:

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/sync_operating_agents_playlist_order.py
```

This prints the current and desired positions. Add `--apply` to rewrite positions.

Important:

- If the write fails with `manualSortRequired`, switch the playlist to manual sorting in YouTube Studio first.

## Single-Video Replacement Flow

Use this when one full-course chapter already has a rendered MP4 and needs a new YouTube upload:

1. Download the current caption track for the live video, or recover subtitles through `yt-dlp` if quota is exhausted.
2. Verify the slide-to-transcript mapping against the actual slide images.
3. Build or confirm a cue sheet.
4. Render the replacement MP4.
5. Run `replace_course_video.py` with the old video ID, rendered media path, playlist ID, and target position.
6. Update `operating_agents_tldr_metadata.json` with the new full video ID and URL.
7. Rerun cross-link sync.

Example:

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/replace_course_video.py \
  --old-video-id <CURRENT_FULL_VIDEO_ID> \
  --media-path <chapter>/artifacts/video/<TITLE>.mp4 \
  --playlist-id <OPERATING_AGENTS_COURSE_PLAYLIST_ID> \
  --position <chapter_position> \
  --apply
```

## Batch Replacement Flow

Use `replace_remaining_course_videos.py` only for the repo's established remaining-chapters batch flow. It depends on hardcoded chapter slugs and media paths.

Default behavior prints a JSON plan:

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/replace_remaining_course_videos.py
```

Add `--apply` only when the media paths, metadata file, and target playlist are confirmed.

## Quota Exhaustion Fallback

The YouTube Data API quota is required for uploads and channel writes, but not for local alignment and rendering.

When quota is exhausted:

1. Keep working on OCR review, transcript verification, cue generation, and rendering.
2. Recover automatic subtitles with `yt-dlp` instead of the captions API.
3. Resume API-dependent upload and playlist steps after quota is available again.

If a write script returns `quotaExceeded`, do not retry blindly in a tight loop. Finish the local prep work and return the blocked state clearly.

Recovery command:

```bash
.venv/bin/yt-dlp \
  --skip-download \
  --write-auto-sub \
  --sub-lang en \
  --convert-subs srt \
  -o "autonomous-agent-blueprint/essays/<slug>/artifacts/video/<slug>_auto_captions.%(ext)s" \
  "https://www.youtube.com/watch?v=<FULL_VIDEO_ID>"
```

If `yt-dlp` writes `<slug>_auto_captions.en.srt`, rename it to the chapter-standard filename before building cue sheets.
