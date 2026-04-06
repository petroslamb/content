from __future__ import annotations
import sys
import argparse
import json
from pathlib import Path

# Add script directory to sys.path for common imports
script_dir = Path(__file__).resolve().parent
if str(script_dir) not in sys.path:
    sys.path.append(str(script_dir))

from googleapiclient.http import MediaFileUpload
from youtube_common import build_youtube


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create a YouTube playlist and upload a video."
    )
    parser.add_argument("--video-title", required=True, help="Title of the video.")
    parser.add_argument(
        "--video-description", required=True, help="Description of the video."
    )
    parser.add_argument(
        "--video-file", type=Path, required=True, help="Path to the video file."
    )
    parser.add_argument(
        "--playlist-title", required=True, help="Title of the playlist."
    )
    parser.add_argument(
        "--playlist-description", required=True, help="Description of the playlist."
    )
    parser.add_argument(
        "--privacy-status",
        choices=["private", "unlisted", "public"],
        default="public",
        help="Privacy status for video and playlist. Default: public.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Execute the changes. Without this, only the plan is printed.",
    )
    return parser.parse_args()


def find_playlist_by_title(youtube, title: str) -> str | None:
    request = youtube.playlists().list(part="snippet", mine=True, maxResults=50)
    response = request.execute()
    for item in response.get("items", []):
        if item["snippet"]["title"] == title:
            return item["id"]
    return None


def create_playlist(youtube, title: str, description: str, privacy_status: str) -> str:
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {"title": title, "description": description},
            "status": {"privacyStatus": privacy_status},
        },
    )
    response = request.execute()
    return response["id"]


def upload_video(
    youtube, file_path: Path, title: str, description: str, privacy_status: str
) -> str:
    media = MediaFileUpload(str(file_path), chunksize=1024 * 1024, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "categoryId": "27",  # Education
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": False,
            },
        },
        media_body=media,
    )

    response = None
    print(f"Uploading {file_path.name}...")
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%", end="\r")
    print("\nUpload complete.")
    return response["id"]


def add_to_playlist(youtube, playlist_id: str, video_id: str):
    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id},
            }
        },
    ).execute()


def main():
    args = parse_args()
    youtube = build_youtube()

    print(f"Plan:")
    print(f" - Playlist: '{args.playlist_title}'")
    print(f" - Video:    '{args.video_title}'")
    print(f" - File:      {args.video_file}")
    print(f" - Privacy:   {args.privacy_status}")

    playlist_id = find_playlist_by_title(youtube, args.playlist_title)
    if playlist_id:
        print(f" - Action: Use existing playlist {playlist_id}")
    else:
        print(f" - Action: Create new playlist")

    if not args.apply:
        print("\nDry run. Use --apply to execute.")
        return

    if not playlist_id:
        playlist_id = create_playlist(
            youtube,
            args.playlist_title,
            args.playlist_description,
            args.privacy_status,
        )
        print(f"Created playlist: {playlist_id}")

    video_id = upload_video(
        youtube,
        args.video_file,
        args.video_title,
        args.video_description,
        args.privacy_status,
    )
    print(f"Uploaded video: {video_id}")

    add_to_playlist(youtube, playlist_id, video_id)
    print(f"Added video to playlist.")

    print(f"\nDone! Video URL: https://www.youtube.com/watch?v={video_id}")


if __name__ == "__main__":
    main()
