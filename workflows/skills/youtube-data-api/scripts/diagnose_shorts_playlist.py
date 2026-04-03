from __future__ import annotations

import argparse

from youtube_common import (
    DEFAULT_SHORTS_DRAFTS_PLAYLIST_ID,
    build_youtube,
    fetch_playlist_items,
    get_video_details,
    parse_utc_date,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Inspect a Shorts drafts playlist and summarize statuses and upload dates."
    )
    parser.add_argument(
        "--playlist-id",
        default=DEFAULT_SHORTS_DRAFTS_PLAYLIST_ID,
        help="Playlist ID to inspect. Default: repo Shorts drafts playlist.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    youtube = build_youtube()

    print(f"Analyzing playlist: {args.playlist_id}\n")
    playlist_items = fetch_playlist_items(youtube, args.playlist_id, part="snippet")
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
        date_str = parse_utc_date(published_at).isoformat()
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
        for video in draft_videos:
            print(f"  - {video['title']} (ID: {video['video_id']}, Date: {video['date']})")


if __name__ == "__main__":
    main()
