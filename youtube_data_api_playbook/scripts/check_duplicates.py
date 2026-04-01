from __future__ import annotations

from datetime import datetime
from pathlib import Path
from collections import Counter, defaultdict

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
TOKEN_FILE = Path(".youtube/token.json")
PLAYLIST_ID = "PL8lPx5mgRhhZtQzAegVjLEqD5v12GWrOw"
TARGET_DATE = "2026-03-31"


def load_youtube():
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    return build("youtube", "v3", credentials=creds)


def get_all_playlist_items(youtube, playlist_id: str) -> list[dict]:
    items = []
    page_token = None
    while True:
        response = (
            youtube.playlistItems()
            .list(part="snippet", playlistId=playlist_id, maxResults=50, pageToken=page_token)
            .execute()
        )
        items.extend(response.get("items", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            break
    return items


def get_video_details(youtube, video_id: str) -> dict | None:
    response = youtube.videos().list(part="snippet,status", id=video_id).execute()
    items = response.get("items", [])
    return items[0] if items else None


def main():
    youtube = load_youtube()
    playlist_items = get_all_playlist_items(youtube, PLAYLIST_ID)

    # Map video ID to title and full item info
    video_info = {}
    for item in playlist_items:
        video_id = item["snippet"]["resourceId"]["videoId"]
        title = item["snippet"]["title"]
        video_info[video_id] = title

    video_ids = list(video_info.keys())

    print(f"Total playlist items: {len(video_ids)}")
    print(f"Unique video IDs: {len(set(video_ids))}")

    # Count frequencies of each video ID in the playlist items
    counter = Counter()
    for item in playlist_items:
        video_id = item["snippet"]["resourceId"]["videoId"]
        counter[video_id] += 1

    duplicates = {vid: count for vid, count in counter.items() if count > 1}

    if duplicates:
        print(f"\nDuplicates ({len(duplicates)} videos appear multiple times):")
        for video_id, count in counter.most_common():
            if count > 1:
                title = video_info.get(video_id, "Unknown")
                print(f"  '{title}' ({video_id}): {count} times")
    else:
        print("\nNo duplicates found.")


if __name__ == "__main__":
    main()
