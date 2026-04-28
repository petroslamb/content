from __future__ import annotations

import json
from datetime import date, datetime
from collections.abc import Iterable
from pathlib import Path

from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

YOUTUBE_FORCE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
YOUTUBE_ANALYTICS_READONLY_SCOPE = "https://www.googleapis.com/auth/yt-analytics.readonly"

SCOPES = [
    YOUTUBE_FORCE_SSL_SCOPE,
    YOUTUBE_READONLY_SCOPE,
    YOUTUBE_ANALYTICS_READONLY_SCOPE,
]

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


class OAuthReauthRequired(RuntimeError):
    """Raised when the cached OAuth token lacks scopes required by this repo."""


def _normalise_scopes(scopes: Iterable[str] | None = None) -> list[str]:
    return list(scopes or SCOPES)


def _reauth_command() -> str:
    return f".venv/bin/python {SCRIPT_DIR / 'auth_and_channel_check.py'}"


def token_file_scopes(token_file: Path = TOKEN_FILE) -> set[str] | None:
    if not token_file.exists():
        return None
    try:
        payload = json.loads(token_file.read_text())
    except json.JSONDecodeError:
        return None
    scopes = payload.get("scopes")
    if isinstance(scopes, str):
        return set(scopes.split())
    if isinstance(scopes, list):
        return {str(scope) for scope in scopes}
    scope = payload.get("scope")
    if isinstance(scope, str):
        return set(scope.split())
    return None


def missing_oauth_scopes(
    required_scopes: Iterable[str] | None = None,
    token_file: Path = TOKEN_FILE,
) -> list[str]:
    cached_scopes = token_file_scopes(token_file)
    if cached_scopes is None:
        return []
    return sorted(set(_normalise_scopes(required_scopes)) - cached_scopes)


def reauth_required_message(missing_scopes: Iterable[str]) -> str:
    missing = ", ".join(missing_scopes)
    return (
        f"OAuth token at {TOKEN_FILE} is missing required YouTube scopes: {missing}. "
        f"Re-run channel auth with: {_reauth_command()}"
    )


def load_credentials(
    interactive: bool = False,
    scopes: Iterable[str] | None = None,
) -> Credentials:
    required_scopes = _normalise_scopes(scopes)
    creds = None
    missing_scopes = missing_oauth_scopes(required_scopes)

    if TOKEN_FILE.exists() and missing_scopes and not interactive:
        raise OAuthReauthRequired(reauth_required_message(missing_scopes))

    if TOKEN_FILE.exists() and not missing_scopes:
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), required_scopes)

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
                f"Run {_reauth_command()} first."
            )
        raise RuntimeError(
            f"Could not refresh OAuth token at {TOKEN_FILE}. "
            f"Run {_reauth_command()} to refresh auth."
        )

    if not CLIENT_SECRETS_FILE.exists():
        raise FileNotFoundError(
            f"Missing OAuth client secrets file at {CLIENT_SECRETS_FILE}. "
            "Download a Google Cloud desktop-app OAuth client and place it there."
        )

    flow = InstalledAppFlow.from_client_secrets_file(
        str(CLIENT_SECRETS_FILE),
        required_scopes,
    )
    creds = flow.run_local_server(port=0)
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(creds.to_json())
    return creds


def build_youtube(
    interactive: bool = False,
    scopes: Iterable[str] | None = None,
):
    return build(
        "youtube",
        "v3",
        credentials=load_credentials(interactive=interactive, scopes=scopes),
    )


def build_youtube_analytics(interactive: bool = False):
    return build(
        "youtubeAnalytics",
        "v2",
        credentials=load_credentials(interactive=interactive, scopes=SCOPES),
    )


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
