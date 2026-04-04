#!/usr/bin/env python3
"""
Upload Binding Gap Shorts to YouTube with main video reference.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'workflows' / 'skills' / 'youtube-data-api' / 'scripts'))

from youtube_common import build_youtube
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

def main():
    youtube = build_youtube()
    main_video_id = 'cBrtKPp4kqw'  # The Binding Gap (podcast version) - main essay video
    main_video_url = f'https://www.youtube.com/watch?v={main_video_id}'

    shorts_dir = Path('publications/binding-gap/artifacts/video/shorts/portrait')
    video_files = sorted(shorts_dir.glob('*.mp4'))

    print(f"Found {len(video_files)} short(s) to upload\n")

    for video_path in video_files:
        # Create title from filename (remove _portrait.mp4)
        title = video_path.stem.replace('_portrait', '').replace('_', ' ')
        full_title = f"{title} #shorts"

        description = f"""{title}

This is a short excerpt from "The Binding Gap" essay.

Main video (full essay): {main_video_url}

#bindinggap #ai #llm #research #shorts"""

        print(f"Uploading: {full_title}")
        print(f"From: {video_path.name}")

        body = {
            'snippet': {
                'title': full_title,
                'description': description,
                'tags': ['AI', 'binding gap', 'language models', 'LLM', 'research', 'shorts'],
                'categoryId': '27',  # Education
                'defaultLanguage': 'en'
            },
            'status': {
                'privacyStatus': 'public',
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
                        'privacyStatus': 'public',
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
