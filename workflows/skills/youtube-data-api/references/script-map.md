# Script Map

Use this file when deciding which local YouTube script to run and how risky it is.

## Read-Only Or Mostly Read-Only

### `auth_and_channel_check.py`

- Purpose: verify OAuth, create or refresh `.youtube/token.json`, and print current channel metadata.
- Inputs: `.youtube/client_secret.json` on first run.
- Writes: token cache only.
- Use first when auth is unknown.

### `download_video_captions.py`

- Purpose: download captions for a managed video.
- Key args: `--video-id`, `--output`, optional `--language`, `--track-kind`, `--format`.
- Behavior: tries the Data API first, then falls back to watch-page caption track recovery on 403.

### `recover_transcript_via_temporary_upload.py`

- Purpose: wrap local audio with a still image, upload it as a temporary video, wait for automatic captions, download the resulting `.srt`, and remove the temporary upload.
- Key args: `--audio-path`, `--image-path`, `--title`, `--output`, optional `--privacy-status`, optional `--poll-interval`, optional `--timeout`.
- Risk: uploads and deletes a YouTube video. Leave `--keep-video` on only when you intentionally want to inspect the upload later.

### `check_duplicates.py`

- Purpose: report duplicate video IDs in a playlist.
- Key args: optional `--playlist-id`.

### `diagnose_shorts_playlist.py`

- Purpose: inspect a playlist and summarize privacy statuses and upload dates.
- Key args: optional `--playlist-id`.

### `list_draft_shorts_today.py`

- Purpose: find the Shorts drafts playlist dynamically, then report draft/private uploads for a target UTC date.
- Key args: optional `--playlist-id`, optional `--date`, optional `--json`.

## Mutating

### `remove_duplicate_playlist_entries.py`

- Purpose: plan or remove duplicate playlist items from a playlist.
- Key args: optional `--playlist-id`, optional `--apply`.
- Risk: destructive playlist write only when `--apply` is present.

### `update_shorts_descriptions.py`

- Purpose: plan or replace descriptions for draft/private Shorts uploaded on a target date.
- Key args: optional `--playlist-id`, optional `--date`, optional `--description-file`, optional `--apply`.
- Risk: destructive metadata overwrite only when `--apply` is present.
- Default template: `references/shorts_description_template.md`.

### `upload_operating_agents_tldrs.py`

- Purpose: upload TL;DR videos listed in metadata, add them to the target playlist, and update the full-episode descriptions.
- Inputs: `references/operating_agents_tldr_metadata.json`.
- Key args: optional `--metadata-file`, optional `--playlist-id`, optional `--privacy-status`, optional `--apply`.
- Risk: uploads videos, edits descriptions, and inserts playlist items only when `--apply` is present.

### `sync_operating_agents_playlist_order.py`

- Purpose: compare playlist order with local metadata and optionally rewrite positions.
- Safe mode: default output is a plan.
- Write mode: add `--apply`.

### `sync_operating_agents_crosslinks.py`

- Purpose: rebuild managed navigation blocks in Operating Agents descriptions.
- Inputs: metadata JSON plus current video snippets from YouTube.
- Safe mode: default behavior is dry-run.
- Write mode: add `--apply`.

### `replace_course_video.py`

- Purpose: plan or upload a new full-course video, preserve metadata, place it into the playlist, and remove the old playlist entry.
- Key args: `--old-video-id`, `--media-path`, `--playlist-id`, `--position`, optional `--apply`.
- Risk: uploads a new video and deletes old playlist entries for the prior video ID only when `--apply` is present.
- Important: the old YouTube video object still exists unless separately archived or deleted.

### `replace_remaining_course_videos.py`

- Purpose: batch-replace the remaining Operating Agents full-course chapters and resync navigation.
- Safe mode: default output is a JSON plan.
- Write mode: add `--apply`.
- Caveat: media paths and course defaults are hardcoded for this repo and this series.
