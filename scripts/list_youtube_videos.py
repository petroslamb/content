#!/usr/bin/env python3
"""
List videos from your YouTube channel.
Run from the project root: .venv/bin/python scripts/list_youtube_videos.py
"""

import os
import sys
import argparse
import json
from pathlib import Path

# Add the youtube skill scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'workflows' / 'skills' / 'youtube-data-api' / 'scripts'))

try:
    from youtube_common import build_youtube
except ImportError:
    print("ERROR: Could not import youtube_common. Make sure you are running from the project root.")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="List videos from your YouTube channel.")
    parser.add_argument("--results", type=int, default=5, help="Number of results to return (default: 5)")
    parser.add_argument("--order", type=str, default="date", choices=["date", "rating", "relevance", "title", "videoCount", "viewCount"], help="Order of results (default: date)")
    args = parser.parse_args()

    youtube = build_youtube()
    response = youtube.search().list(
        part='snippet',
        forMine=True,
        type='video',
        maxResults=args.results,
        order=args.order
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
