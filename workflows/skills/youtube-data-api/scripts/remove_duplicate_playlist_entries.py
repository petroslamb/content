from __future__ import annotations

import argparse
import json

from youtube_common import (
    DEFAULT_SHORTS_DRAFTS_PLAYLIST_ID,
    build_youtube,
    fetch_playlist_items,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Remove duplicate video entries from a playlist."
    )
    parser.add_argument(
        "--playlist-id",
        default=DEFAULT_SHORTS_DRAFTS_PLAYLIST_ID,
        help="Playlist ID to clean. Default: repo Shorts drafts playlist.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Delete duplicate playlist entries. Without this flag, print the cleanup plan only.",
    )
    return parser.parse_args()


def remove_duplicates(youtube, playlist_items: list[dict], apply: bool) -> list[dict]:
    seen_video_ids = set()
    removed_items = []

    for item in playlist_items:
        video_id = item["snippet"]["resourceId"]["videoId"]
        title = item["snippet"]["title"]
        playlist_item_id = item["id"]

        if video_id in seen_video_ids:
            removed_items.append(
                {
                    "playlist_item_id": playlist_item_id,
                    "video_id": video_id,
                    "title": title,
                }
            )
            if apply:
                youtube.playlistItems().delete(id=playlist_item_id).execute()
            continue

        seen_video_ids.add(video_id)

    return removed_items


def main():
    args = parse_args()
    youtube = build_youtube()
    all_items = fetch_playlist_items(youtube, args.playlist_id, part="id,snippet")
    removed = remove_duplicates(youtube, all_items, apply=args.apply)

    print(
        json.dumps(
            {
                "playlist_id": args.playlist_id,
                "applied": args.apply,
                "total_items": len(all_items),
                "removed_count": len(removed),
                "remaining_count": len(all_items) - len(removed),
                "removed_items": removed,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
