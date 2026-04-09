from __future__ import annotations

import argparse
import json
from pathlib import Path

from googleapiclient.http import MediaFileUpload

from youtube_common import build_youtube


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Upload a publication longform video plus a TL;DR companion, "
            "add them to their playlists, cross-link the descriptions, and optionally "
            "pin the playlist entries to the top."
        )
    )
    parser.add_argument("--longform-file", required=True, type=Path)
    parser.add_argument("--longform-title", required=True)
    parser.add_argument("--longform-summary", required=True)
    parser.add_argument("--longform-playlist-id", required=True)
    parser.add_argument("--tldr-file", required=True, type=Path)
    parser.add_argument("--tldr-title", required=True)
    parser.add_argument("--tldr-summary", required=True)
    parser.add_argument("--tldr-playlist-id", required=True)
    parser.add_argument("--essay-url", required=True)
    parser.add_argument(
        "--chapters-file",
        type=Path,
        help="Optional plaintext file containing YouTube chapter timestamps for the longform description.",
    )
    parser.add_argument(
        "--privacy-status",
        choices=["private", "unlisted", "public"],
        default="public",
    )
    parser.add_argument(
        "--pin-to-top",
        action="store_true",
        help="Move uploaded playlist items to position 0 after insert.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Execute the uploads and metadata writes. Without this flag, print the plan only.",
    )
    return parser.parse_args()


def upload_video(youtube, file_path: Path, title: str, description: str, privacy_status: str) -> str:
    media = MediaFileUpload(str(file_path), mimetype="video/mp4", chunksize=1024 * 1024, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "categoryId": "27",
                "tags": ["AI", "research", "deep learning", "education"],
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
        status, response = request.next_chunk()
        if status:
            print(json.dumps({"uploading": file_path.name, "progress": round(status.progress() * 100, 1)}))
    return response["id"]


def add_to_playlist(youtube, playlist_id: str, video_id: str) -> str:
    response = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id},
            }
        },
    ).execute()
    return response["id"]


def move_playlist_item_to_top(youtube, playlist_id: str, playlist_item_id: str, video_id: str) -> None:
    youtube.playlistItems().update(
        part="snippet",
        body={
            "id": playlist_item_id,
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id},
                "position": 0,
            },
        },
    ).execute()


def update_description(youtube, video_id: str, title: str, description: str) -> None:
    youtube.videos().update(
        part="snippet",
        body={
            "id": video_id,
            "snippet": {
                "title": title,
                "description": description,
                "categoryId": "27",
                "tags": ["AI", "research", "deep learning", "education"],
            },
        },
    ).execute()


def longform_description(summary: str, essay_url: str, tldr_url: str, chapters: str) -> str:
    parts = [summary, "", "Original essay:", essay_url, "", "TL;DR video:", tldr_url]
    if chapters.strip():
        parts.extend(["", "Chapters", chapters.strip()])
    return "\n".join(parts).strip()


def tldr_description(summary: str, essay_url: str, longform_url: str) -> str:
    return "\n".join(
        [
            summary,
            "",
            "Original essay:",
            essay_url,
            "",
            "Full visual deep dive:",
            longform_url,
        ]
    ).strip()


def main() -> None:
    args = parse_args()
    chapters = args.chapters_file.read_text().strip() if args.chapters_file else ""

    plan = {
        "longform_file": str(args.longform_file),
        "longform_title": args.longform_title,
        "longform_playlist_id": args.longform_playlist_id,
        "tldr_file": str(args.tldr_file),
        "tldr_title": args.tldr_title,
        "tldr_playlist_id": args.tldr_playlist_id,
        "essay_url": args.essay_url,
        "chapters_included": bool(chapters),
        "privacy_status": args.privacy_status,
        "pin_to_top": args.pin_to_top,
    }
    print(json.dumps({"plan": plan}, indent=2))

    if not args.apply:
        return

    youtube = build_youtube()

    initial_tldr_description = "\n".join(
        [args.tldr_summary, "", "Original essay:", args.essay_url]
    ).strip()
    tldr_id = upload_video(
        youtube,
        args.tldr_file,
        args.tldr_title,
        initial_tldr_description,
        args.privacy_status,
    )
    tldr_playlist_item_id = add_to_playlist(youtube, args.tldr_playlist_id, tldr_id)
    if args.pin_to_top:
        move_playlist_item_to_top(youtube, args.tldr_playlist_id, tldr_playlist_item_id, tldr_id)
    tldr_url = f"https://www.youtube.com/watch?v={tldr_id}"

    full_description = longform_description(args.longform_summary, args.essay_url, tldr_url, chapters)
    longform_id = upload_video(
        youtube,
        args.longform_file,
        args.longform_title,
        full_description,
        args.privacy_status,
    )
    longform_playlist_item_id = add_to_playlist(youtube, args.longform_playlist_id, longform_id)
    if args.pin_to_top:
        move_playlist_item_to_top(youtube, args.longform_playlist_id, longform_playlist_item_id, longform_id)
    longform_url = f"https://www.youtube.com/watch?v={longform_id}"

    final_tldr_description = tldr_description(args.tldr_summary, args.essay_url, longform_url)
    update_description(youtube, tldr_id, args.tldr_title, final_tldr_description)

    print(
        json.dumps(
            {
                "longform_video_id": longform_id,
                "longform_url": longform_url,
                "tldr_video_id": tldr_id,
                "tldr_url": tldr_url,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
