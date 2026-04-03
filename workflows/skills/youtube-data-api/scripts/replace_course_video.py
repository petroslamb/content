from __future__ import annotations

import argparse
import json
from pathlib import Path

from googleapiclient.http import MediaFileUpload

from youtube_common import build_youtube


def load_youtube():
    return build_youtube()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Upload a replacement video with preserved metadata and swap it into a playlist."
    )
    parser.add_argument("--old-video-id", required=True)
    parser.add_argument("--media-path", required=True, type=Path)
    parser.add_argument("--playlist-id", required=True)
    parser.add_argument(
        "--position",
        type=int,
        default=0,
        help="Playlist position for the replacement video. Default: 0",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Upload the replacement and update playlist entries. Without this flag, print the plan only.",
    )
    return parser.parse_args()


def fetch_video(youtube, video_id: str) -> dict:
    items = youtube.videos().list(part="snippet,status", id=video_id).execute().get("items", [])
    if not items:
        raise RuntimeError(f"Could not find video {video_id}")
    return items[0]


def upload_replacement(youtube, old_video: dict, media_path: Path) -> str:
    snippet = old_video["snippet"]
    status = old_video["status"]
    body = {
        "snippet": {
            "title": snippet["title"],
            "description": snippet.get("description", ""),
            "categoryId": snippet.get("categoryId", "22"),
        },
        "status": {
            "privacyStatus": status.get("privacyStatus", "public"),
            "selfDeclaredMadeForKids": status.get("selfDeclaredMadeForKids", False),
            "embeddable": status.get("embeddable", True),
            "publicStatsViewable": status.get("publicStatsViewable", True),
            "license": status.get("license", "youtube"),
        },
    }
    if "defaultLanguage" in snippet:
        body["snippet"]["defaultLanguage"] = snippet["defaultLanguage"]
    if "tags" in snippet:
        body["snippet"]["tags"] = snippet["tags"]

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(str(media_path), chunksize=-1, resumable=True),
    )
    response = None
    while response is None:
        _, response = request.next_chunk()
    return response["id"]


def find_playlist_items(youtube, playlist_id: str, video_id: str) -> list[dict]:
    matches = []
    page = None
    while True:
        response = (
            youtube.playlistItems()
            .list(part="id,snippet", playlistId=playlist_id, maxResults=50, pageToken=page)
            .execute()
        )
        for item in response.get("items", []):
            if item["snippet"]["resourceId"]["videoId"] == video_id:
                matches.append(item)
        page = response.get("nextPageToken")
        if not page:
            return matches


def ensure_playlist_entry(youtube, playlist_id: str, video_id: str, position: int) -> str:
    matches = find_playlist_items(youtube, playlist_id, video_id)
    if matches:
        return matches[0]["id"]
    response = (
        youtube.playlistItems()
        .insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "position": position,
                    "resourceId": {"kind": "youtube#video", "videoId": video_id},
                }
            },
        )
        .execute()
    )
    return response["id"]


def remove_playlist_entries(youtube, playlist_id: str, video_id: str) -> list[str]:
    removed = []
    for item in find_playlist_items(youtube, playlist_id, video_id):
        youtube.playlistItems().delete(id=item["id"]).execute()
        removed.append(item["id"])
    return removed


def main():
    args = parse_args()
    youtube = load_youtube()
    old_video = fetch_video(youtube, args.old_video_id)

    if not args.apply:
        print(
            json.dumps(
                {
                    "apply": False,
                    "old_video_id": args.old_video_id,
                    "old_title": old_video["snippet"]["title"],
                    "media_path": str(args.media_path),
                    "playlist_id": args.playlist_id,
                    "playlist_position": args.position,
                    "planned_new_url_field": "<new-video-id-after-upload>",
                },
                indent=2,
            )
        )
        return

    new_video_id = upload_replacement(youtube, old_video, args.media_path)
    new_playlist_item_id = ensure_playlist_entry(
        youtube, args.playlist_id, new_video_id, args.position
    )
    removed_playlist_item_ids = remove_playlist_entries(
        youtube, args.playlist_id, args.old_video_id
    )
    print(
        json.dumps(
            {
                "apply": True,
                "old_video_id": args.old_video_id,
                "new_video_id": new_video_id,
                "playlist_id": args.playlist_id,
                "new_playlist_item_id": new_playlist_item_id,
                "removed_playlist_item_ids": removed_playlist_item_ids,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
