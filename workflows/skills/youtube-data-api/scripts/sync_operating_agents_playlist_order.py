from __future__ import annotations

import argparse
import json
from pathlib import Path

from youtube_common import (
    METADATA_FILE,
    build_youtube,
    find_video_by_title,
    load_metadata as load_metadata_file,
)


def load_metadata(path: Path = METADATA_FILE) -> dict:
    return load_metadata_file(path)


def fetch_playlist_items(youtube, playlist_id: str):
    items = []
    page = None
    while True:
        response = (
            youtube.playlistItems()
            .list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=page,
            )
            .execute()
        )
        items.extend(response.get("items", []))
        page = response.get("nextPageToken")
        if not page:
            return items


def order_map(items: list[dict]):
    return {
        item["snippet"]["resourceId"]["videoId"]: {
            "playlist_item_id": item["id"],
            "position": item["snippet"]["position"],
            "title": item["snippet"]["title"],
        }
        for item in items
    }


def update_positions(youtube, playlist_id: str, desired_video_ids: list[str], apply: bool):
    playlist_items = fetch_playlist_items(youtube, playlist_id)
    current = order_map(playlist_items)
    results = []

    missing = [video_id for video_id in desired_video_ids if video_id not in current]
    if missing:
        raise RuntimeError(f"Playlist {playlist_id} is missing expected videos: {missing}")

    for position, video_id in enumerate(desired_video_ids):
        current_item = current[video_id]
        results.append(
            {
                "video_id": video_id,
                "title": current_item["title"],
                "from_position": current_item["position"],
                "to_position": position,
                "changed": current_item["position"] != position,
            }
        )
        if not apply or current_item["position"] == position:
            continue

        youtube.playlistItems().update(
            part="snippet",
            body={
                "id": current_item["playlist_item_id"],
                "snippet": {
                    "playlistId": playlist_id,
                    "position": position,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id,
                    },
                },
            },
        ).execute()

    return results


def parse_args():
    parser = argparse.ArgumentParser(
        description="Sync Operating Agents playlist ordering from local metadata."
    )
    parser.add_argument(
        "--metadata-file",
        type=Path,
        default=METADATA_FILE,
        help="Metadata JSON file to use. Default: skill reference metadata.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write updates to YouTube. Without this flag, the script only prints the planned reorder.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    youtube = build_youtube()
    metadata = load_metadata(args.metadata_file)

    tldr_video_ids = []
    for item in metadata["items"]:
        tldr_video_id = find_video_by_title(youtube, item["full_title"])
        if not tldr_video_id:
            raise RuntimeError(f"Could not find TL;DR upload for title: {item['full_title']}")
        tldr_video_ids.append(tldr_video_id)

    full_video_ids = [item["full_episode_video_id"] for item in metadata["items"]]

    results = {
        "applied": args.apply,
        "metadata_file": str(args.metadata_file),
        "course_playlist_id": metadata["course_playlist_id"],
        "tldr_playlist_id": metadata["playlist_id"],
        "course_playlist_changes": update_positions(
            youtube,
            metadata["course_playlist_id"],
            full_video_ids,
            apply=args.apply,
        ),
        "tldr_playlist_changes": update_positions(
            youtube,
            metadata["playlist_id"],
            tldr_video_ids,
            apply=args.apply,
        ),
    }
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
