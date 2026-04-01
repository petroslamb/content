from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
TOKEN_FILE = Path(".youtube/token.json")

# Target date (today)
TARGET_DATE = date(2026, 3, 31)


def load_youtube():
    """Authenticate and build YouTube API client."""
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    return build("youtube", "v3", credentials=creds)


def find_shorts_draft_playlist(youtube) -> str | None:
    """Find the playlist with 'shorts' and 'draft' in the title."""
    print("Searching for 'Shorts Drafts' playlist...")

    response = (
        youtube.playlists()
        .list(part="snippet", mine=True, maxResults=50)
        .execute()
    )

    candidates = []
    for playlist in response.get("items", []):
        title = playlist["snippet"]["title"].lower()
        if "shorts" in title and ("draft" in title or "private" in title):
            candidates.append(playlist)

    if candidates:
        # Prefer exact match
        for playlist in candidates:
            title_lower = playlist["snippet"]["title"].lower()
            if "shorts draft" in title_lower or "shorts drafts" in title_lower:
                playlist_id = playlist["id"]
                print(f"Found playlist: '{playlist['snippet']['title']}' (ID: {playlist_id})")
                return playlist_id

        # Otherwise return first match
        playlist = candidates[0]
        playlist_id = playlist["id"]
        print(f"Found playlist: '{playlist['snippet']['title']}' (ID: {playlist_id})")
        return playlist_id

    print("No playlist with 'shorts' and 'draft' or 'private' in the title found. Available playlists:")
    for playlist in response.get("items", []):
        print(f"  - {playlist['snippet']['title']}")

    return None


def get_all_playlist_items(youtube, playlist_id: str) -> list[dict]:
    """Retrieve all video items from a playlist (handles pagination)."""
    items = []
    page_token = None

    while True:
        response = (
            youtube.playlistItems()
            .list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=page_token,
            )
            .execute()
        )

        items.extend(response.get("items", []))

        page_token = response.get("nextPageToken")
        if not page_token:
            break

    return items


def get_video_details(youtube, video_id: str) -> dict | None:
    """Fetch full video details including status and publishedAt."""
    response = (
        youtube.videos()
        .list(part="snippet,status", id=video_id)
        .execute()
    )

    items = response.get("items", [])
    return items[0] if items else None


def is_uploaded_today(published_at: str) -> bool:
    """Check if the publishedAt timestamp is today."""
    # YouTube API returns ISO 8601 format: "2026-03-31T12:34:56Z"
    published_date = datetime.fromisoformat(published_at.replace("Z", "+00:00")).date()
    return published_date == TARGET_DATE


def main():
    youtube = load_youtube()

    # Step 1: Find the "Shorts Drafts" playlist
    playlist_id = find_shorts_draft_playlist(youtube)
    if not playlist_id:
        print("\nError: Could not find a playlist containing both 'shorts' and 'draft' in the title.")
        return

    # Step 2: Get all videos from the playlist
    print(f"\nFetching videos from playlist...")
    playlist_items = get_all_playlist_items(youtube, playlist_id)
    print(f"Found {len(playlist_items)} total videos in playlist.")

    # Step 3: Filter for draft status and today's date
    draft_shorts_today = []
    print("\nChecking video details...")

    for item in playlist_items:
        video_id = item["snippet"]["resourceId"]["videoId"]
        title = item["snippet"]["title"]

        video_details = get_video_details(youtube, video_id)
        if not video_details:
            print(f"  Warning: Could not fetch details for video '{title}' ({video_id})")
            continue

        status = video_details.get("status", {})
        privacy_status = status.get("privacyStatus")
        published_at = video_details["snippet"]["publishedAt"]

        # Check if not public and uploaded today
        # "draft" means unpublished, "private" means uploaded but not public (often used for drafts/scheduling)
        if privacy_status in ("draft", "private") and is_uploaded_today(published_at):
            draft_shorts_today.append(
                {
                    "video_id": video_id,
                    "title": title,
                    "published_at": published_at,
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                }
            )

    # Step 4: Output results
    print("\n" + "=" * 80)
    print(f"RESULTS: {len(draft_shorts_today)} draft shorts uploaded today ({TARGET_DATE})")
    print("=" * 80)

    if draft_shorts_today:
        print("\nList of draft shorts:")
        for i, video in enumerate(draft_shorts_today, 1):
            print(f"\n{i}. {video['title']}")
            print(f"   Video ID: {video['video_id']}")
            print(f"   Published: {video['published_at']}")
            print(f"   URL: {video['url']}")
    else:
        print("\nNo draft shorts found uploaded today.")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
