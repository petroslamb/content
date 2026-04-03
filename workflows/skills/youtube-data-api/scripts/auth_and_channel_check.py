from __future__ import annotations

import json

from youtube_common import build_youtube


def main() -> None:
    youtube = build_youtube(interactive=True)
    response = (
        youtube.channels()
        .list(part="snippet,contentDetails,statistics", mine=True)
        .execute()
    )

    items = response.get("items", [])
    if not items:
        raise RuntimeError("No channel returned for the authenticated account.")

    channel = items[0]
    uploads_playlist_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]

    print(
        json.dumps(
            {
                "channel_id": channel["id"],
                "title": channel["snippet"]["title"],
                "uploads_playlist_id": uploads_playlist_id,
                "subscriber_count": channel["statistics"].get("subscriberCount"),
                "video_count": channel["statistics"].get("videoCount"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
