from __future__ import annotations

import argparse
from collections import Counter

from youtube_common import (
    DEFAULT_SHORTS_DRAFTS_PLAYLIST_ID,
    build_youtube,
    fetch_playlist_items,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Report duplicate video IDs in a playlist."
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
    playlist_items = fetch_playlist_items(youtube, args.playlist_id, part="snippet")

    counter = Counter()
    titles = {}
    for item in playlist_items:
        video_id = item["snippet"]["resourceId"]["videoId"]
        counter[video_id] += 1
        titles.setdefault(video_id, item["snippet"]["title"])

    print(f"Playlist ID: {args.playlist_id}")
    print(f"Total playlist items: {len(playlist_items)}")
    print(f"Unique video IDs: {len(counter)}")

    duplicates = {video_id: count for video_id, count in counter.items() if count > 1}
    if not duplicates:
        print("\nNo duplicates found.")
        return

    print(f"\nDuplicates ({len(duplicates)} videos appear multiple times):")
    for video_id, count in counter.most_common():
        if count > 1:
            print(f"  '{titles.get(video_id, 'Unknown')}' ({video_id}): {count} times")


if __name__ == "__main__":
    main()
