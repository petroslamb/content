"""
Remove duplicate video entries from a YouTube playlist.

This script keeps only the first occurrence of each video (by video ID)
and removes all subsequent duplicates from the specified playlist.
"""

from __future__ import annotations

from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
TOKEN_FILE = Path(".youtube/token.json")
# "Shorts drafts" playlist
PLAYLIST_ID = "PL8lPx5mgRhhZtQzAegVjLEqD5v12GWrOw"


def load_youtube():
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    return build("youtube", "v3", credentials=creds)


def get_all_playlist_items(youtube, playlist_id: str) -> list[dict]:
    """Retrieve all items from the playlist with full details including playlistItem IDs."""
    items = []
    page_token = None
    while True:
        response = (
            youtube.playlistItems()
            .list(
                part="id,snippet",
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


def remove_duplicates(youtube, playlist_items: list[dict]) -> list[dict]:
    """
    Remove duplicate video entries.

    Returns a list of removed items with their video IDs, titles, and playlistItem IDs.
    """
    seen_video_ids = set()
    removed_items = []
    items_to_keep = []

    for item in playlist_items:
        video_id = item["snippet"]["resourceId"]["videoId"]
        title = item["snippet"]["title"]
        playlist_item_id = item["id"]

        if video_id in seen_video_ids:
            # Duplicate found - remove from playlist
            print(f"Removing duplicate: '{title}' ({video_id})")
            removed_items.append(
                {
                    "playlist_item_id": playlist_item_id,
                    "video_id": video_id,
                    "title": title,
                }
            )
            # Actually delete from playlist
            youtube.playlistItems().delete(id=playlist_item_id).execute()
        else:
            seen_video_ids.add(video_id)
            items_to_keep.append(item)

    return removed_items


def main():
    youtube = load_youtube()

    print(f"Fetching all items from playlist '{PLAYLIST_ID}'...")
    all_items = get_all_playlist_items(youtube, PLAYLIST_ID)
    print(f"Total items before cleanup: {len(all_items)}")

    if len(all_items) <= 1:
        print("No duplicates possible in a playlist with 0 or 1 items.")
        return

    print("\nRemoving duplicates (keeping first occurrence of each video)...\n")
    removed = remove_duplicates(youtube, all_items)

    print(f"\n{'=' * 80}")
    print(f"Cleanup complete!")
    print(f"  Items removed: {len(removed)}")
    print(f"  Items remaining: {len(all_items) - len(removed)}")
    print(f"{'=' * 80}\n")

    if removed:
        print("Removed duplicate entries:")
        for item in removed:
            print(f"  - {item['title']} (Video ID: {item['video_id']})")
    else:
        print("No duplicates were found.")


if __name__ == "__main__":
    main()
