from __future__ import annotations

import argparse
import json
from pathlib import Path

from replace_course_video import (
    ensure_playlist_entry,
    fetch_video,
    find_playlist_items,
    load_youtube,
    remove_playlist_entries,
    upload_replacement,
)
from sync_operating_agents_crosslinks import (
    METADATA_FILE,
    build_series_items,
    build_full_episode_block,
    build_tldr_block,
    fetch_video_snippet,
    load_metadata,
    update_video_description,
    with_navigation_block,
)


MEDIA_BY_SLUG = {
    "memory": Path(
        "/Users/petros/Projects/content/autonomous-agent-blueprint/essays/memory/artifacts/video/Operating Agents II - Timed Slides.mp4"
    ),
    "reasoning": Path(
        "/Users/petros/Projects/content/autonomous-agent-blueprint/essays/reasoning/artifacts/video/Operating Agents III - Timed Slides.mp4"
    ),
    "multi-agent": Path(
        "/Users/petros/Projects/content/autonomous-agent-blueprint/essays/multi-agent/artifacts/video/Operating Agents IV - Timed Slides.mp4"
    ),
    "safety": Path(
        "/Users/petros/Projects/content/autonomous-agent-blueprint/essays/safety/artifacts/video/Operating Agents V - Timed Slides.mp4"
    ),
    "optimization": Path(
        "/Users/petros/Projects/content/autonomous-agent-blueprint/essays/optimization/artifacts/video/Operating Agents Bonus - Timed Slides.mp4"
    ),
}


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Replace the remaining Operating Agents course videos, update metadata, "
            "and resync course/TL;DR description navigation."
        )
    )
    parser.add_argument(
        "--metadata-file",
        type=Path,
        default=METADATA_FILE,
        help="Metadata JSON file to update in place.",
    )
    parser.add_argument(
        "--course-playlist-id",
        default="PL8lPx5mgRhhZiKRR-cLl7YJd6GXhcbZAr",
        help="Operating Agents course playlist ID.",
    )
    parser.add_argument(
        "--start-chapter",
        type=int,
        default=2,
        help="First chapter number to replace. Default: 2",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Perform YouTube writes. Without this flag, the script only prints the plan.",
    )
    return parser.parse_args()


def update_description_template(template: str, old_url: str, new_url: str) -> str:
    return template.replace(old_url, new_url)


def sync_navigation_blocks(youtube, metadata: dict, course_playlist_id: str, apply: bool) -> list[dict]:
    series_items = build_series_items(youtube, metadata)
    results = []

    for index, item in enumerate(series_items):
        next_item = series_items[index + 1] if index + 1 < len(series_items) else None
        full_snippet = fetch_video_snippet(youtube, item["full_episode_video_id"])
        tldr_snippet = fetch_video_snippet(youtube, item["tldr_video_id"])

        full_block = build_full_episode_block(item, next_item, course_playlist_id)
        tldr_block = build_tldr_block(item, next_item, course_playlist_id)

        full_description = with_navigation_block(full_snippet.get("description", ""), full_block)
        tldr_description = with_navigation_block(tldr_snippet.get("description", ""), tldr_block)

        update_video_description(
            youtube,
            item["full_episode_video_id"],
            full_snippet,
            full_description,
            dry_run=not apply,
        )
        update_video_description(
            youtube,
            item["tldr_video_id"],
            tldr_snippet,
            tldr_description,
            dry_run=not apply,
        )

        results.append(
            {
                "chapter": item["chapter"],
                "full_episode_video_id": item["full_episode_video_id"],
                "tldr_video_id": item["tldr_video_id"],
                "applied": apply,
            }
        )

    return results


def main():
    args = parse_args()
    metadata = load_metadata() if args.metadata_file == METADATA_FILE else json.loads(args.metadata_file.read_text())
    course_playlist_id = args.course_playlist_id
    results = []

    youtube = load_youtube() if args.apply else None

    for position, item in enumerate(metadata["items"], start=0):
        chapter = item["chapter"]
        if chapter < args.start_chapter:
            continue

        slug = item["slug"]
        media_path = MEDIA_BY_SLUG[slug]
        old_video_id = item["full_episode_video_id"]
        old_url = item["full_episode_url"]

        result = {
            "chapter": chapter,
            "slug": slug,
            "old_video_id": old_video_id,
            "media_path": str(media_path),
            "playlist_position": position,
        }

        if args.apply:
            old_video = fetch_video(youtube, old_video_id)
            new_video_id = upload_replacement(youtube, old_video, media_path)
            new_playlist_item_id = ensure_playlist_entry(
                youtube, course_playlist_id, new_video_id, position
            )
            removed_playlist_item_ids = remove_playlist_entries(
                youtube, course_playlist_id, old_video_id
            )

            new_url = f"https://www.youtube.com/watch?v={new_video_id}"
            item["full_episode_video_id"] = new_video_id
            item["full_episode_url"] = new_url
            item["description_template"] = update_description_template(
                item["description_template"], old_url, new_url
            )

            result.update(
                {
                    "new_video_id": new_video_id,
                    "new_playlist_item_id": new_playlist_item_id,
                    "removed_playlist_item_ids": removed_playlist_item_ids,
                }
            )
        else:
            result["planned_new_url_field"] = "<new-video-id-after-upload>"

        results.append(result)

    navigation_results = []
    if args.apply:
        args.metadata_file.write_text(json.dumps(metadata, indent=2) + "\n")
        navigation_results = sync_navigation_blocks(
            youtube, metadata, course_playlist_id, apply=True
        )

    print(
        json.dumps(
            {
                "apply": args.apply,
                "course_playlist_id": course_playlist_id,
                "replacements": results,
                "navigation_sync": navigation_results,
                "metadata_file": str(args.metadata_file),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
