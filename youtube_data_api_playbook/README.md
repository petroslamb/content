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

SCOPES = ["https://www.googleapis.com/auth/youtube"]

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
https://www.googleapis.com/auth/youtube
```

This is the broad write-capable scope that covers the common channel operations we are likely to automate next.

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
