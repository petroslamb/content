from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from youtube_common import (
    DEFAULT_SHORTS_DRAFTS_PLAYLIST_ID,
    SHORTS_DESCRIPTION_TEMPLATE_FILE,
    build_youtube,
    fetch_playlist_items,
    get_video_details,
    parse_utc_date,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Update descriptions for draft/private Shorts uploaded on a given UTC date."
    )
    parser.add_argument(
        "--playlist-id",
        default=DEFAULT_SHORTS_DRAFTS_PLAYLIST_ID,
        help="Playlist ID to inspect. Default: repo Shorts drafts playlist.",
    )
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="UTC upload date in YYYY-MM-DD format. Default: today.",
    )
    parser.add_argument(
        "--description-file",
        type=Path,
        default=SHORTS_DESCRIPTION_TEMPLATE_FILE,
        help="Path to the replacement description text.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write updated descriptions. Without this flag, print the update plan only.",
    )
    return parser.parse_args()


def update_video_description(youtube, video_id: str, description_text: str) -> None:
    video = get_video_details(youtube, video_id)
    if not video:
        raise RuntimeError(f"Video {video_id} not found")

    snippet = video["snippet"]
    payload = {
        "title": snippet["title"],
        "description": description_text,
        "categoryId": snippet.get("categoryId", "22"),
    }
    if "defaultLanguage" in snippet:
        payload["defaultLanguage"] = snippet["defaultLanguage"]
    if "tags" in snippet:
        payload["tags"] = snippet["tags"]

    youtube.videos().update(
        part="snippet",
        body={"id": video_id, "snippet": payload},
    ).execute()


def main():
    args = parse_args()
    target_date = date.fromisoformat(args.date)
    description_text = args.description_file.read_text().strip()
    youtube = build_youtube()

    playlist_items = fetch_playlist_items(youtube, args.playlist_id, part="snippet")
    unique_video_ids = {
        item["snippet"]["resourceId"]["videoId"] for item in playlist_items
    }

    videos_to_update = []
    for video_id in sorted(unique_video_ids):
        details = get_video_details(youtube, video_id)
        if not details:
            continue

        status = details["status"]["privacyStatus"]
        published_at = details["snippet"]["publishedAt"]
        if status not in ("draft", "private"):
            continue
        if parse_utc_date(published_at) != target_date:
            continue

        videos_to_update.append(
            {
                "video_id": video_id,
                "title": details["snippet"]["title"],
                "published_at": published_at,
            }
        )

    if args.apply:
        for video in videos_to_update:
            update_video_description(youtube, video["video_id"], description_text)

    print(
        json.dumps(
            {
                "playlist_id": args.playlist_id,
                "date": target_date.isoformat(),
                "description_file": str(args.description_file),
                "applied": args.apply,
                "updated_count": len(videos_to_update),
                "videos": videos_to_update,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
