from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
REPO_ROOT = SCRIPT_DIR.parents[3]

CLIENT_SECRETS_FILE = REPO_ROOT / ".youtube" / "client_secret.json"
TOKEN_FILE = REPO_ROOT / ".youtube" / "token.json"
METADATA_FILE = SKILL_ROOT / "references" / "operating_agents_tldr_metadata.json"
SHORTS_DESCRIPTION_TEMPLATE_FILE = (
    SKILL_ROOT / "references" / "shorts_description_template.md"
)

DEFAULT_SHORTS_DRAFTS_PLAYLIST_ID = "PL8lPx5mgRhhZtQzAegVjLEqD5v12GWrOw"
DEFAULT_OPERATING_AGENTS_COURSE_PLAYLIST_ID = "PL8lPx5mgRhhZiKRR-cLl7YJd6GXhcbZAr"


def load_credentials(interactive: bool = False) -> Credentials:
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except RefreshError:
            creds = None
        else:
            TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
            TOKEN_FILE.write_text(creds.to_json())
            return creds

    if not interactive:
        if not TOKEN_FILE.exists():
            raise FileNotFoundError(
                f"Missing OAuth token cache at {TOKEN_FILE}. "
                f"Run {SCRIPT_DIR / 'auth_and_channel_check.py'} first."
            )
        raise RuntimeError(
            f"Could not refresh OAuth token at {TOKEN_FILE}. "
            f"Run {SCRIPT_DIR / 'auth_and_channel_check.py'} to refresh auth."
        )

    if not CLIENT_SECRETS_FILE.exists():
        raise FileNotFoundError(
            f"Missing OAuth client secrets file at {CLIENT_SECRETS_FILE}. "
            "Download a Google Cloud desktop-app OAuth client and place it there."
        )

    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS_FILE), SCOPES)
    creds = flow.run_local_server(port=0)
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(creds.to_json())
    return creds


def build_youtube(interactive: bool = False):
    return build("youtube", "v3", credentials=load_credentials(interactive=interactive))


def load_metadata(path: Path = METADATA_FILE) -> dict:
    return json.loads(path.read_text())


def fetch_playlist_items(youtube, playlist_id: str, part: str = "snippet") -> list[dict]:
    items = []
    page_token = None
    while True:
        response = (
            youtube.playlistItems()
            .list(
                part=part,
                playlistId=playlist_id,
                maxResults=50,
                pageToken=page_token,
            )
            .execute()
        )
        items.extend(response.get("items", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            return items


def get_video_details(youtube, video_id: str, part: str = "snippet,status") -> dict | None:
    response = youtube.videos().list(part=part, id=video_id).execute()
    items = response.get("items", [])
    return items[0] if items else None


def find_video_by_title(youtube, title: str) -> str | None:
    response = (
        youtube.search()
        .list(part="snippet", forMine=True, type="video", maxResults=50, q=title)
        .execute()
    )
    for item in response.get("items", []):
        if item["snippet"]["title"] == title:
            return item["id"]["videoId"]
    return None


def find_shorts_draft_playlist(youtube) -> str | None:
    response = youtube.playlists().list(part="snippet", mine=True, maxResults=50).execute()

    candidates = []
    for playlist in response.get("items", []):
        title = playlist["snippet"]["title"].lower()
        if "shorts" in title and ("draft" in title or "private" in title):
            candidates.append(playlist)

    for playlist in candidates:
        title = playlist["snippet"]["title"].lower()
        if "shorts draft" in title or "shorts drafts" in title:
            return playlist["id"]

    if candidates:
        return candidates[0]["id"]
    return None


def parse_utc_date(value: str) -> date:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
