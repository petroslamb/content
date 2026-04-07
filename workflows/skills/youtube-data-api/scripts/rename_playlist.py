from __future__ import annotations
import sys
import argparse
from pathlib import Path

# Add script directory to sys.path for common imports
script_dir = Path(__file__).resolve().parent
if str(script_dir) not in sys.path:
    sys.path.append(str(script_dir))

from youtube_common import build_youtube

def parse_args():
    parser = argparse.ArgumentParser(description="Rename a YouTube playlist.")
    parser.add_argument("--playlist-id", required=True, help="ID of the playlist to rename.")
    parser.add_argument("--title", required=True, help="New title for the playlist.")
    parser.add_argument("--description", help="New description for the playlist.")
    parser.add_argument("--apply", action="store_true", help="Execute the changes.")
    return parser.parse_args()

def rename_playlist(youtube, playlist_id: str, title: str, description: str = None):
    body = {
        "id": playlist_id,
        "snippet": {
            "title": title
        }
    }
    if description:
        body["snippet"]["description"] = description

    request = youtube.playlists().update(
        part="snippet",
        body=body
    )
    response = request.execute()
    return response

def main():
    args = parse_args()
    youtube = build_youtube()

    print(f"Renaming playlist {args.playlist_id}:")
    print(f" - New Title:       {args.title}")
    if args.description:
        print(f" - New Description: {args.description}")

    if not args.apply:
        print("\nDry run. Use --apply to execute.")
        return

    response = rename_playlist(youtube, args.playlist_id, args.title, args.description)
    print(f"Done! Playlist updated: {response['snippet']['title']}")

if __name__ == "__main__":
    main()
