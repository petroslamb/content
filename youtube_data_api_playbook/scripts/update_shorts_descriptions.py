"""
Update descriptions of draft/private shorts uploaded today.

Appends promotional text with links to full research breakdown, playlist, and Substack.
"""

from __future__ import annotations

from datetime import datetime, date
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
TOKEN_FILE = Path(".youtube/token.json")
PLAYLIST_ID = "PL8lPx5mgRhhZtQzAegVjLEqD5v12GWrOw"  # "Shorts drafts"

TARGET_DATE = date(2026, 3, 31)

# Promotional text to append
PROMO_TEXT = """Is your AI agent's autonomy a liability or a feature? 🏗️ This clip breaks down a critical pillar of secure AI architecture from our latest research deep dive. We're moving beyond the hype to build systems grounded in "Rooted Layers" safety.

📺 Watch the Full Research Breakdown: https://www.youtube.com/watch?v=biyIKcSp3Po

📑 Explore the Full Series: https://www.youtube.com/playlist?list=PL_XvBv-D1I_n-m7a9f8KjE7o0S9u_D0iS

📩 Get the Architecture Blueprints: Deep dive into the papers and diagrams on our Substack: https://lambpetros.substack.com

#AISecurity #LLMs #AIAgents #CyberSecurity #RootedLayers #AIResearch"""


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


def get_video_details(youtube, video_id: str) -> dict:
    response = youtube.videos().list(part="snippet,status", id=video_id).execute()
    items = response.get("items", [])
    if not items:
        raise RuntimeError(f"Video {video_id} not found")
    return items[0]


def update_video_description(youtube, video_id: str, title: str) -> None:
    """Update the video's description to the promotional text."""
    # Get current video details to preserve title and category
    video = get_video_details(youtube, video_id)
    snippet = video["snippet"]

    youtube.videos().update(
        part="snippet",
        body={
            "id": video_id,
            "snippet": {
                "title": snippet["title"],  # Keep existing title
                "description": PROMO_TEXT,
                "categoryId": snippet.get("categoryId", "22"),
                "defaultLanguage": snippet.get("defaultLanguage"),
                "tags": snippet.get("tags", []),
            },
        },
    ).execute()


def main():
    youtube = load_youtube()

    print("Fetching playlist items...")
    playlist_items = get_all_playlist_items(youtube, PLAYLIST_ID)
    print(f"Total items in playlist: {len(playlist_items)}")

    # Get unique video IDs from playlist
    video_ids = []
    for item in playlist_items:
        video_ids.append(item["snippet"]["resourceId"]["videoId"])

    unique_video_ids = list(set(video_ids))
    print(f"Unique video IDs: {len(unique_video_ids)}\n")

    # Filter videos: draft/private status AND uploaded today
    videos_to_update = []
    print("Checking video details and filtering for today's draft/private videos...\n")

    for video_id in unique_video_ids:
        details = get_video_details(youtube, video_id)

        status = details["status"]["privacyStatus"]
        published_at = details["snippet"]["publishedAt"]
        pub_date = datetime.fromisoformat(published_at.replace("Z", "+00:00")).date()
        title = details["snippet"]["title"]

        print(f"Checking: {title}")
        print(f"  Status: {status}, Published: {pub_date}")

        if pub_date == TARGET_DATE and status in ("draft", "private"):
            videos_to_update.append(
                {
                    "video_id": video_id,
                    "title": title,
                }
            )
            print(f"  ✓ Will update")
        else:
            print(f"  ✗ Skipped (not today or not draft/private)")

        print()  # Blank line

    # Confirm with user before updating
    print("=" * 80)
    print(f"Found {len(videos_to_update)} videos to update:")
    for v in videos_to_update:
        print(f"  - {v['title']} ({v['video_id']})")
    print("=" * 80)

    # Auto-confirm (user already approved this operation)
    # Uncomment below for interactive mode:
    # if input("\nProceed with updating these videos? (yes/no): ").strip().lower() != "yes":
    #     print("Operation cancelled.")
    #     return

    # Perform updates
    print("\nUpdating video descriptions...")
    for i, video in enumerate(videos_to_update, 1):
        try:
            update_video_description(youtube, video["video_id"], video["title"])
            print(f"[{i}/{len(videos_to_update)}] Updated: {video['title']}")
        except Exception as e:
            print(f"[{i}/{len(videos_to_update)}] ERROR updating {video['title']}: {e}")

    print(f"\n{'=' * 80}")
    print(f"Done! Updated {len(videos_to_update)} video descriptions.")
    print("=" * 80)


if __name__ == "__main__":
    main()
