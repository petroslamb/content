#!/usr/bin/env python3
"""
Upload Publication Shorts to YouTube with main video reference.
Run from project root: .venv/bin/python scripts/upload_publication_shorts.py --package <package_name> --video-id <main_video_id>
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
    parser.add_argument("--video-id", required=True, help="Main video ID for the essay")
    parser.add_argument("--privacy", default="public", choices=["public", "unlisted", "private"], help="Privacy status (default: public)")
    args = parser.parse_args()

    youtube = build_youtube()
    main_video_id = args.video_id
    main_video_url = f'https://www.youtube.com/watch?v={main_video_id}'

    shorts_dir = Path('publications') / args.package / 'artifacts' / 'video' / 'shorts' / 'portrait'
    if not shorts_dir.exists():
        print(f"ERROR: Shorts directory not found: {shorts_dir}")
        sys.exit(1)

    video_files = sorted(shorts_dir.glob('*.mp4'))
    if not video_files:
        print(f"No .mp4 files found in {shorts_dir}")
        sys.exit(0)

    print(f"Found {len(video_files)} short(s) to upload\n")

    for video_path in video_files:
        # Create title from filename (remove _portrait.mp4)
        title = video_path.stem.replace('_portrait', '').replace('_', ' ')
        full_title = f"{title} #shorts"

        # Guess tags from package name or filename
        tags = ['AI', 'research', 'shorts']
        tags.extend(args.package.split('-'))
        
        description = f"""{title}

This is a short excerpt from the "{args.package.replace('-', ' ').title()}" essay.

Main video (full essay): {main_video_url}

#{args.package.replace('-', '')} #ai #research #shorts"""

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
