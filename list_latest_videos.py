#!/usr/bin/env python3
"""
List the 5 latest videos from your YouTube channel.
Run from the project root: .venv/bin/python list_latest_videos.py
"""

import sys
from pathlib import Path

# Add the scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'workflows' / 'skills' / 'youtube-data-api' / 'scripts'))

from youtube_common import build_youtube
import json

def main():
    youtube = build_youtube()
    response = youtube.search().list(
        part='snippet',
        forMine=True,
        type='video',
        maxResults=5,
        order='date'
    ).execute()

    videos = []
    for item in response.get('items', []):
        videos.append({
            'video_id': item['id']['videoId'],
            'title': item['snippet']['title'],
            'published_at': item['snippet']['publishedAt'],
            'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        })

    print(json.dumps(videos, indent=2))

if __name__ == '__main__':
    main()
