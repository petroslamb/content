#!/usr/bin/env python3
"""
Upload The Binding Gap TL;DR videos to the Rooted Layers Summaries playlist.
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
    playlist_id = 'PL8lPx5mgRhhan7OgyGo3Ostthkbr0v6n6'
    main_video_url = 'https://www.youtube.com/watch?v=cBrtKPp4kqw'

    video_files = [
        'publications/binding-gap/artifacts/video/The_Binding_Gap_cinematic.mp4',
        'publications/binding-gap/artifacts/video/The_Binding_Gap_explainer.mp4'
    ]

    for video_path in video_files:
        video_path = Path(video_path)
        if not video_path.exists():
            print(f"ERROR: {video_path} does not exist")
            continue

        filename = video_path.name
        # Derive title from filename
        if 'cinematic' in filename.lower():
            title = 'The Binding Gap: Cinematic TL;DR'
        elif 'explainer' in filename.lower():
            title = 'The Binding Gap: Explainer TL;DR'
        else:
            title = 'The Binding Gap TL;DR'

        description = f"""TL;DR video summary of "The Binding Gap" essay.

Main video (full essay): {main_video_url}

This short video provides a visual overview of the key concepts.
Watch the full video for the complete exposition."""

        print(f"Uploading {filename} as '{title}'...")

        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': ['AI', 'binding gap', 'language models', 'research', 'TL;DR'],
                'categoryId': '27'  # Education
            },
            'status': {
                'privacyStatus': 'public'
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

    print("All uploads complete!")

if __name__ == '__main__':
    main()
