#!/usr/bin/env python3
"""
Upload publication Shorts from a package portrait folder, add them to a target
playlist, and set the related long-form video reference when possible.

Run from project root:
  .venv/bin/python scripts/upload_publication_shorts.py \
    --package <package_name> \
    --main-video-id <main_video_id> \
    --playlist-id <shorts_playlist_id> \
    --essay-url <canonical_essay_url> \
    --full-video-url <longform_video_url> \
    [--tldr-url <tldr_video_url>] \
    [--apply]
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
    parser = argparse.ArgumentParser(description="Upload publication shorts to YouTube.")
    parser.add_argument("--package", required=True, help="Package name (e.g., binding-gap)")
    parser.add_argument("--main-video-id", required=True, help="Main long-form video ID for the Shorts related-video field")
    parser.add_argument("--playlist-id", required=True, help="Target Shorts playlist ID")
    parser.add_argument("--essay-url", required=True, help="Canonical essay URL")
    parser.add_argument("--full-video-url", required=True, help="Public URL for the long-form video")
    parser.add_argument("--tldr-url", help="Optional public URL for the TL;DR companion")
    parser.add_argument("--privacy", default="public", choices=["public", "unlisted", "private"], help="Privacy status (default: public)")
    parser.add_argument("--apply", action="store_true", help="Upload and mutate YouTube state. Without this, print the plan only.")
    args = parser.parse_args()

    youtube = build_youtube()
    main_video_id = args.main_video_id
    main_video_url = f'https://www.youtube.com/watch?v={main_video_id}'

    shorts_dir = Path('publications') / args.package / 'artifacts' / 'video' / 'shorts' / 'portrait'
    if not shorts_dir.exists():
        print(f"ERROR: Shorts directory not found: {shorts_dir}")
        sys.exit(1)

    video_files = sorted(shorts_dir.glob('*.mp4'))
    if not video_files:
        print(f"No .mp4 files found in {shorts_dir}")
        sys.exit(0)

    print(f"Found {len(video_files)} short(s) to upload")
    print(f"Target playlist: {args.playlist_id}")
    print(f"Related long-form video: {main_video_url}")
    if not args.apply:
        print("\nDry run only. Add --apply to upload and write YouTube state.")
        for video_path in video_files:
            title = video_path.stem.replace('_portrait', '').replace('_', ' ')
            print(f" - {title} #shorts <- {video_path.name}")
        return

    print()

    for video_path in video_files:
        # Create title from filename (remove _portrait.mp4)
        title = video_path.stem.replace('_portrait', '').replace('_', ' ')
        full_title = f"{title} #shorts"

        # Guess tags from package name or filename
        tags = ['AI', 'research', 'shorts']
        tags.extend(args.package.split('-'))
        
        description_lines = [
            f"{title}",
            "",
            "Short clip from a Rooted Layers long-form research video.",
            "",
            f"Original essay: {args.essay_url}",
            f"Full visual deep dive: {args.full_video_url}",
        ]
        if args.tldr_url:
            description_lines.append(f"TL;DR video: {args.tldr_url}")
        description_lines.extend(
            [
                "",
                f"#{args.package.replace('-', '').replace('/', '')} #ai #research #shorts",
            ]
        )
        description = "\n".join(description_lines)

        print(f"Uploading: {full_title}")
        print(f"From: {video_path.name}")

        body = {
            'snippet': {
                'title': full_title,
                'description': description,
                'tags': tags,
                'categoryId': '27',  # Education
                'defaultLanguage': 'en'
            },
            'status': {
                'privacyStatus': args.privacy,
                'selfDeclaredMadeForKids': False
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
                print(f"  Upload failed: {e}")
                raise

        video_id = response['id']
        print(f"  Uploaded! Video ID: {video_id}")
        print(f"  URL: https://www.youtube.com/watch?v={video_id}")

        try:
            youtube.playlistItems().insert(
                part='snippet',
                body={
                    'snippet': {
                        'playlistId': args.playlist_id,
                        'resourceId': {'kind': 'youtube#video', 'videoId': video_id},
                    }
                },
            ).execute()
            print(f"  Added to playlist: {args.playlist_id}")
        except HttpError as e:
            print(f"  Could not add to playlist: {e}")

        # Update video to set relatedVideoIds (promote main video as related)
        try:
            youtube.videos().update(
                part='status',
                body={
                    'id': video_id,
                    'status': {
                        'privacyStatus': args.privacy,
                        'relatedVideoIds': [main_video_id]
                    }
                }
            ).execute()
            print(f"  Set related video: {main_video_id}")
        except HttpError as e:
            print(f"  Could not set related video (this is optional): {e}")

        print()

    print("All shorts upload complete!")

if __name__ == '__main__':
    main()
