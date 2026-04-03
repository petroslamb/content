from __future__ import annotations

import argparse
import json
from pathlib import Path

from googleapiclient.http import MediaFileUpload

from youtube_common import (
    METADATA_FILE,
    build_youtube,
    find_video_by_title,
    load_metadata as load_metadata_file,
)

MAX_DESCRIPTION_LEN = 5000


def load_metadata(path: Path = METADATA_FILE) -> dict:
    return load_metadata_file(path)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Upload Operating Agents TL;DR videos from local metadata."
    )
    parser.add_argument(
        "--metadata-file",
        type=Path,
        default=METADATA_FILE,
        help="Metadata JSON file to use. Default: skill reference metadata.",
    )
    parser.add_argument(
        "--playlist-id",
        help="Override the TL;DR playlist ID in the metadata file.",
    )
    parser.add_argument(
        "--privacy-status",
        choices=["private", "unlisted", "public"],
        default="public",
        help="Privacy status for newly uploaded videos. Default: public.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Upload videos and update YouTube state. Without this flag, print the plan only.",
    )
    return parser.parse_args()


def upload_video(youtube, item: dict, privacy_status: str) -> str:
    media = MediaFileUpload(item["local_video_path"], chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": item["full_title"],
                "description": item["description_template"],
                "categoryId": "27",
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": False,
            },
        },
        media_body=media,
    )

    response = None
    while response is None:
        _, response = request.next_chunk()
    return response["id"]


def add_to_playlist(youtube, playlist_id: str, video_id: str):
    page = None
    while True:
        response = (
            youtube.playlistItems()
            .list(part="snippet", playlistId=playlist_id, maxResults=50, pageToken=page)
            .execute()
        )
        for item in response.get("items", []):
            if item["snippet"]["resourceId"]["videoId"] == video_id:
                return
        page = response.get("nextPageToken")
        if not page:
            break

    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id,
                },
            }
        },
    ).execute()


def update_full_episode_description(youtube, full_video_id: str, tldr_url: str):
    response = youtube.videos().list(part="snippet", id=full_video_id).execute()
    items = response.get("items", [])
    if not items:
        raise RuntimeError(f"Could not find full episode {full_video_id}")

    video = items[0]
    snippet = video["snippet"]
    line = f"Watch the visual TL;DR: {tldr_url}"
    description = snippet.get("description", "")

    lines = description.splitlines()
    if lines and lines[0].startswith("Watch the visual TL;DR: "):
        lines[0] = line
        new_description = "\n".join(lines)
    else:
        new_description = f"{line}\n\n{description}".strip()

    if len(new_description) > MAX_DESCRIPTION_LEN:
        new_description = new_description[: MAX_DESCRIPTION_LEN - 3].rstrip() + "..."

    update_snippet = {
        "categoryId": snippet.get("categoryId", "27"),
        "title": snippet["title"],
        "description": new_description,
    }
    if "defaultLanguage" in snippet:
        update_snippet["defaultLanguage"] = snippet["defaultLanguage"]
    if "tags" in snippet:
        update_snippet["tags"] = snippet["tags"]

    youtube.videos().update(
        part="snippet",
        body={"id": full_video_id, "snippet": update_snippet},
    ).execute()


def main():
    args = parse_args()
    youtube = build_youtube()
    metadata = load_metadata(args.metadata_file)
    playlist_id = args.playlist_id or metadata["playlist_id"]
    results = []

    for item in metadata["items"]:
        existing_video_id = find_video_by_title(youtube, item["full_title"])
        if existing_video_id:
            video_id = existing_video_id
            existed = True
        elif args.apply:
            video_id = upload_video(youtube, item, args.privacy_status)
            existed = False
        else:
            video_id = "<new-video-id-after-upload>"
            existed = False

        tldr_url = (
            f"https://www.youtube.com/watch?v={video_id}"
            if existed or args.apply
            else "<new-video-url-after-upload>"
        )

        if args.apply:
            add_to_playlist(youtube, playlist_id, video_id)
            update_full_episode_description(youtube, item["full_episode_video_id"], tldr_url)

        results.append(
            {
                "chapter": item["chapter"],
                "title": item["full_title"],
                "video_id": video_id,
                "url": tldr_url,
                "existing": existed,
                "applied": args.apply,
            }
        )

    print(
        json.dumps(
            {
                "metadata_file": str(args.metadata_file),
                "playlist_id": playlist_id,
                "privacy_status": args.privacy_status,
                "applied": args.apply,
                "results": results,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
