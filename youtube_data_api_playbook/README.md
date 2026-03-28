# YouTube Data API Playbook

This folder documents the YouTube Data API workflow used in this repository:

- how we authenticate with OAuth 2.0
- how we inspect the current channel
- how we create and manage playlists
- how we add or remove playlist items
- where local credentials should live
- which starter scripts exist for future automation

## Environment

Use the repo-local virtual environment:

```bash
.venv/bin/python -c "from googleapiclient.discovery import build; print('ok')"
```

Install or refresh dependencies with:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

The standard Python stack is:

- `google-api-python-client`: the actual client for calling YouTube Data API methods such as `channels.list`, `videos.insert`, `videos.update`, `playlists.insert`, and `playlistItems.insert`
- `google-auth-oauthlib`: the OAuth helper used for local user login and consent flows via `InstalledAppFlow`
- `google-auth-httplib2`: auth transport support used alongside the Google client stack

These packages are already tracked in the root [requirements.txt](/Users/petros/Projects/content/requirements.txt).

## Credentials

Channel-writing operations require OAuth 2.0 client credentials from Google Cloud.

Expected local paths:

- OAuth client secrets: `.youtube/client_secret.json`
- OAuth token cache: `.youtube/token.json`

Both paths are gitignored. Treat them as credentials.

Service accounts are not supported for YouTube Data API channel actions.

Use an API key only for simple public read-only requests. Use OAuth 2.0 for anything that touches your account or channel, including uploads, playlist creation, metadata edits, and other write operations.

Google's older `oauth2client` library is deprecated. This repository uses `google-auth` and `google-auth-oauthlib`.

## Minimal Pattern

The standard local-auth pattern looks like this:

```python
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

flow = InstalledAppFlow.from_client_secrets_file(".youtube/client_secret.json", SCOPES)
creds = flow.run_local_server(port=0)

youtube = build("youtube", "v3", credentials=creds)
```

That is the same shape used by the starter script in this folder.

## Starter Script

Run the starter auth and channel check:

```bash
.venv/bin/python youtube_data_api_playbook/scripts/auth_and_channel_check.py
```

What it does:

- loads `.youtube/client_secret.json`
- runs the local OAuth flow if needed
- caches the resulting token in `.youtube/token.json`
- calls `channels.list(..., mine=True)`
- prints your channel title, channel ID, and uploads playlist ID

## Current Scope

The starter script uses:

```text
https://www.googleapis.com/auth/youtube.force-ssl
```

This scope covers the write-capable operations used in this repo, including caption listing and download for videos you manage.

## Useful API Resources

- `channels.list`: inspect the authenticated channel
- `videos.insert`: upload a video
- `videos.update`: edit video metadata
- `playlists.insert`: create a playlist
- `playlists.update`: edit playlist metadata
- `playlistItems.insert`: add a video to a playlist
- `playlistItems.delete`: remove a video from a playlist
- `search.list`: search public YouTube resources

## Playlist-Centered Workflow

For this repository, the most useful early automation target is playlist management:

- create a playlist for a series
- update its title and description
- add a set of video IDs in order
- treat podcast or course organization as a playlist-centered workflow where possible

The YouTube Studio-specific podcast/course flags may still require browser automation, but playlists and playlist items are first-class Data API resources and are a good starting layer for automation.

## Next Likely Scripts

- `create_playlist.py`
- `add_videos_to_playlist.py`
- `update_video_metadata.py`
- `list_channel_playlists.py`

Those are not scaffolded yet. Start with the auth script first.

## Operating Agents Cross-Link Sync

The current Data API does not expose the modern YouTube Studio end-screen editor, so you cannot programmatically set the in-player "suggested next video" targets for a series using this library.

The supported fallback in this repo is description-based series navigation:

```bash
.venv/bin/python youtube_data_api_playbook/scripts/sync_operating_agents_crosslinks.py \
  --course-playlist-id <OPERATING_AGENTS_COURSE_PLAYLIST_ID>
```

This script:

- discovers the uploaded Operating Agents TL;DR videos by exact title
- updates each full episode description with a link to its TL;DR, the next full chapter, and the relevant playlists
- updates each TL;DR description with a link back to the full chapter, the next TL;DR, and the relevant playlists
- uses marker blocks so reruns replace the managed navigation section instead of duplicating it

It runs in dry-run mode by default and prints the planned navigation blocks. Add `--apply` to write the changes:

```bash
.venv/bin/python youtube_data_api_playbook/scripts/sync_operating_agents_crosslinks.py \
  --course-playlist-id <OPERATING_AGENTS_COURSE_PLAYLIST_ID> \
  --apply
```

## Operating Agents Playlist Order Sync

Use the local metadata to keep both Operating Agents playlists in chapter order:

```bash
.venv/bin/python youtube_data_api_playbook/scripts/sync_operating_agents_playlist_order.py
```

This script:

- treats the metadata item order as the source of truth
- syncs the full course playlist to chapter order
- syncs the TL;DR playlist to chapter order
- prints the current and desired positions before any write

Add `--apply` to write the new positions:

```bash
.venv/bin/python youtube_data_api_playbook/scripts/sync_operating_agents_playlist_order.py --apply
```

## Operating Agents Course Replacement Workflow

The full-course replacements now use the same local ingredients in each chapter folder:

- `artifacts/audio/*.mp3`
- `artifacts/slides/<deck-name>/slide-*.png`
- `artifacts/transcript_*_full.txt`
- `artifacts/video/`

The workflow used for `Action` and the later chapters is:

1. Download YouTube's automatic caption track from the currently live course video.
2. OCR the slide deck and use transcript overlap only as a draft alignment signal.
3. Verify the draft by looking at the actual slide images and fix semantic ordering issues.
4. Convert the verified slide swaps into a cue sheet with caption timestamps.
5. Render the replacement MP4 from the audio and cue sheet.
6. Upload a replacement full-course video with the same metadata as the current one.
7. Swap the playlist entry to the new video ID.
8. Update local metadata and rerun cross-link sync so TL;DR and course descriptions point to the replacement video.

When the YouTube Data API quota is exhausted, the local production workflow can still continue. The critical distinction is:

- Data API quota is needed for caption API calls, uploads, and playlist/video writes.
- Local alignment, OCR review, cue generation, and rendering do not need Data API quota.
- Subtitle recovery can fall back to `yt-dlp`, which does not consume YouTube Data API quota.

Useful commands:

```bash
# Download the managed caption track for a course video.
.venv/bin/python youtube_data_api_playbook/scripts/download_video_captions.py \
  --video-id <CURRENT_FULL_VIDEO_ID> \
  --output <chapter>/artifacts/video/<slug>_auto_captions.srt

# If the local SRT is empty or the Data API quota is exhausted, recover the
# automatic subtitle track through yt-dlp instead.
.venv/bin/pip install yt-dlp
.venv/bin/yt-dlp \
  --skip-download \
  --write-auto-sub \
  --sub-lang en \
  --convert-subs srt \
  -o <chapter>/artifacts/video/<slug>_auto_captions.%(ext)s \
  "https://www.youtube.com/watch?v=<CURRENT_FULL_VIDEO_ID>"

# Render the verified slideshow cut.
.venv/bin/python scripts/render_audio_slides_video.py render \
  --cues <chapter>/artifacts/video/<slug>_cues_youtube_verified.json \
  --output <chapter>/artifacts/video/<TITLE>.mp4 \
  --fps 2

# Convert a verified markdown line map plus timed captions into a cue sheet.
.venv/bin/python scripts/line_map_markdown_to_cues.py \
  --map <chapter>/artifacts/video/<slug>_slide_transcript_map_ocr_verified.md \
  --captions <chapter>/artifacts/video/<slug>_auto_captions.srt \
  --transcript <chapter>/artifacts/transcript_<Chapter Title>_numbered.txt \
  --chapter-dir <chapter-root> \
  --output <chapter>/artifacts/video/<slug>_cues_from_srt.json

# Upload a replacement and swap it into the course playlist.
.venv/bin/python youtube_data_api_playbook/scripts/replace_course_video.py \
  --old-video-id <CURRENT_FULL_VIDEO_ID> \
  --media-path <chapter>/artifacts/video/<TITLE>.mp4 \
  --playlist-id <OPERATING_AGENTS_COURSE_PLAYLIST_ID> \
  --position <chapter_position>
```

Notes:

- The replacement upload creates a new YouTube video ID. YouTube does not replace media in place.
- Keep the old full video out of the course playlist once the replacement is live, but expect the old video object to continue existing unless you explicitly archive or delete it.
- After replacement, update [operating_agents_tldr_metadata.json](/Users/petros/Projects/content/youtube_data_api_playbook/operating_agents_tldr_metadata.json) and rerun [sync_operating_agents_crosslinks.py](/Users/petros/Projects/content/youtube_data_api_playbook/scripts/sync_operating_agents_crosslinks.py) so the TL;DR descriptions and course descriptions resolve to the new full-video IDs.
- Some chapter folders may contain zero-byte `*_auto_captions.srt` placeholders from failed earlier downloads. Check file size before using them as timing anchors.
- The verified cue-sheet builder sorts slides by mapped transcript order rather than slide filename order, because some decks are sequenced differently from the spoken chapter.
