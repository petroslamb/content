from __future__ import annotations

import argparse
import json
from datetime import date

from youtube_common import (
    build_youtube,
    fetch_playlist_items,
    find_shorts_draft_playlist,
    get_video_details,
    parse_utc_date,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="List draft/private Shorts uploaded on a given UTC date."
    )
    parser.add_argument(
        "--playlist-id",
        help="Playlist ID to inspect. If omitted, search for a Shorts drafts playlist.",
    )
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="UTC upload date in YYYY-MM-DD format. Default: today.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print results as JSON.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    target_date = date.fromisoformat(args.date)
    youtube = build_youtube()

    playlist_id = args.playlist_id or find_shorts_draft_playlist(youtube)
    if not playlist_id:
        raise RuntimeError(
            "Could not find a playlist containing both 'shorts' and 'draft' in the title."
        )

    playlist_items = fetch_playlist_items(youtube, playlist_id, part="snippet")

    draft_shorts = []
    for item in playlist_items:
        video_id = item["snippet"]["resourceId"]["videoId"]
        title = item["snippet"]["title"]

        video_details = get_video_details(youtube, video_id)
        if not video_details:
            continue

        privacy_status = video_details.get("status", {}).get("privacyStatus")
        published_at = video_details["snippet"]["publishedAt"]

        if privacy_status not in ("draft", "private"):
            continue
        if parse_utc_date(published_at) != target_date:
            continue

        draft_shorts.append(
            {
                "video_id": video_id,
                "title": title,
                "published_at": published_at,
                "url": f"https://www.youtube.com/watch?v={video_id}",
            }
        )

    if args.json:
        print(
            json.dumps(
                {
                    "playlist_id": playlist_id,
                    "date": target_date.isoformat(),
                    "count": len(draft_shorts),
                    "items": draft_shorts,
                },
                indent=2,
            )
        )
        return

    print(f"Playlist ID: {playlist_id}")
    print(f"Results: {len(draft_shorts)} draft/private Shorts uploaded on {target_date}")

    if not draft_shorts:
        print("No matching videos found.")
        return

    for index, video in enumerate(draft_shorts, start=1):
        print(f"\n{index}. {video['title']}")
        print(f"   Video ID: {video['video_id']}")
        print(f"   Published: {video['published_at']}")
        print(f"   URL: {video['url']}")


if __name__ == "__main__":
    main()
