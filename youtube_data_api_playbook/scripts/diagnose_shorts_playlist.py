from __future__ import annotations

from datetime import datetime
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
TOKEN_FILE = Path(".youtube/token.json")


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
    playlist_id = "PL8lPx5mgRhhZtQzAegVjLEqD5v12GWrOw"  # "Shorts drafts"

    print(f"Analyzing playlist: Shorts drafts\n")

    playlist_items = get_all_playlist_items(youtube, playlist_id)
    print(f"Total videos in playlist: {len(playlist_items)}\n")

    status_counts = {}
    date_counts = {}
    draft_videos = []

    for item in playlist_items:
        video_id = item["snippet"]["resourceId"]["videoId"]
        title = item["snippet"]["title"]

        video_details = get_video_details(youtube, video_id)
        if not video_details:
            continue

        status = video_details.get("status", {}).get("privacyStatus", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1

        published_at = video_details["snippet"]["publishedAt"]
        pub_date = datetime.fromisoformat(published_at.replace("Z", "+00:00")).date()
        date_str = pub_date.isoformat()
        date_counts[date_str] = date_counts.get(date_str, 0) + 1

        if status == "draft":
            draft_videos.append(
                {
                    "video_id": video_id,
                    "title": title,
                    "published_at": published_at,
                    "date": date_str,
                }
            )

    print("Privacy Status Distribution:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")

    print("\nUpload Date Distribution:")
    for date_str, count in sorted(date_counts.items()):
        print(f"  {date_str}: {count}")

    print(f"\nDraft videos in playlist: {len(draft_videos)}")
    if draft_videos:
        print("\nDraft videos:")
        for v in draft_videos:
            print(f"  - {v['title']} (ID: {v['video_id']}, Date: {v['date']})")


if __name__ == "__main__":
    main()
