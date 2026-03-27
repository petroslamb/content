from __future__ import annotations

import json
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube"]
CLIENT_SECRETS_FILE = Path(".youtube/client_secret.json")
TOKEN_FILE = Path(".youtube/token.json")


def load_credentials() -> Credentials:
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        if not CLIENT_SECRETS_FILE.exists():
            raise FileNotFoundError(
                f"Missing OAuth client secrets file at {CLIENT_SECRETS_FILE}. "
                "Download an OAuth client for Desktop app from Google Cloud and place it there."
            )

        flow = InstalledAppFlow.from_client_secrets_file(
            str(CLIENT_SECRETS_FILE), SCOPES
        )
        creds = flow.run_local_server(port=0)

    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(creds.to_json())
    return creds


def main() -> None:
    creds = load_credentials()
    youtube = build("youtube", "v3", credentials=creds)

    response = (
        youtube.channels()
        .list(part="snippet,contentDetails,statistics", mine=True)
        .execute()
    )

    items = response.get("items", [])
    if not items:
        raise RuntimeError("No channel returned for the authenticated account.")

    channel = items[0]
    uploads_playlist_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]

    print(
        json.dumps(
            {
                "channel_id": channel["id"],
                "title": channel["snippet"]["title"],
                "uploads_playlist_id": uploads_playlist_id,
                "subscriber_count": channel["statistics"].get("subscriberCount"),
                "video_count": channel["statistics"].get("videoCount"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
