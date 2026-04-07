#!/usr/bin/env python3
"""
Upload Publication TL;DR videos to a YouTube playlist.
Run from project root: .venv/bin/python scripts/upload_publication_tldrs.py --package <package_name> --playlist-id <id> --video-url <main_video_url>
"""

import os
import sys
import argparse
from pathlib import Path

# Add the youtube skill scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'workflows' / 'skills' / 'youtube-data-api' / 'scripts'))

try:
    from youtube_common import build_youtube
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
except ImportError:
    print("ERROR: Could not import YouTube client libraries. Make sure you are running from the project root.")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Upload publication TL;DR videos to a YouTube playlist.")
    parser.add_argument("--package", required=True, help="Package name (e.g., binding-gap)")
    parser.add_argument("--playlist-id", required=True, help="YouTube playlist ID for summaries")
    parser.add_argument("--video-url", required=True, help="Main video URL for the essay")
    parser.add_argument("--privacy", default="public", choices=["public", "unlisted", "private"], help="Privacy status (default: public)")
    args = parser.parse_args()

    youtube = build_youtube()
    playlist_id = args.playlist_id
    main_video_url = args.video_url

    artifacts_dir = Path('publications') / args.package / 'artifacts' / 'video'
    if not artifacts_dir.exists():
        print(f"ERROR: Video artifacts directory not found: {artifacts_dir}")
        sys.exit(1)

    # Find potential TL;DR videos
    video_files = list(artifacts_dir.glob('*_cinematic.mp4')) + list(artifacts_dir.glob('*_explainer.mp4')) + list(artifacts_dir.glob('*_tldr.mp4'))
    
    if not video_files:
        print(f"No TL;DR (.mp4) files found in {artifacts_dir}")
        sys.exit(0)

    print(f"Found {len(video_files)} TL;DR video(s) to upload\n")

    for video_path in video_files:
        filename = video_path.name
        # Derive title from filename
        package_title = args.package.replace('-', ' ').title()
        if 'cinematic' in filename.lower():
            title = f"{package_title}: Cinematic TL;DR"
        elif 'explainer' in filename.lower():
            title = f"{package_title}: Explainer TL;DR"
        else:
            title = f"{package_title} TL;DR"

        description = f"""TL;DR video summary of the "{package_title}" essay.

Main video (full essay): {main_video_url}

This short video provides a visual overview of the key concepts.
Watch the full video for the complete exposition."""

        print(f"Uploading {filename} as '{title}'...")

        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': ['AI', 'research', 'TL;DR', args.package.replace('-', ' ')],
                'categoryId': '27'  # Education
            },
            'status': {
                'privacyStatus': args.privacy
            }
        }

        media = MediaFileUpload(
            str(video_path),
            mimetype='video/mp4',
            chunksize=-1,
            resumable=True
        )

        request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            try:
                status, response = request.next_chunk()
                if status:
                    print(f"  Upload progress: {int(status.progress() * 100)}%")
            except HttpError as e:
                print(f"  An HTTP error occurred: {e}")
                raise

        video_id = response['id']
        print(f"  Uploaded! Video ID: {video_id}")

        # Add to playlist
        try:
            youtube.playlistItems().insert(
                part='snippet',
                body={
                    'snippet': {
                        'playlistId': playlist_id,
                        'position': 0,
                        'resourceId': {
                            'kind': 'youtube#video',
                            'videoId': video_id
                        }
                    }
                }
            ).execute()
            print(f"  Added to playlist '{playlist_id}' at position 0")
        except HttpError as e:
            print(f"  Could not add to playlist (this is optional): {e}")

    print("All uploads complete!")

if __name__ == '__main__':
    main()
