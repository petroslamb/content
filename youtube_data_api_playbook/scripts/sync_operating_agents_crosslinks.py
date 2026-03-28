from __future__ import annotations

import argparse
import json
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
TOKEN_FILE = Path(".youtube/token.json")
METADATA_FILE = Path("youtube_data_api_playbook/operating_agents_tldr_metadata.json")
MAX_DESCRIPTION_LEN = 5000
START_MARKER = "== Operating Agents navigation =="
END_MARKER = "== /Operating Agents navigation =="


def load_youtube():
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    return build("youtube", "v3", credentials=creds)


def load_metadata():
    return json.loads(METADATA_FILE.read_text())


def find_video_by_title(youtube, title: str):
    resp = (
        youtube.search()
        .list(part="snippet", forMine=True, type="video", maxResults=50, q=title)
        .execute()
    )
    for item in resp.get("items", []):
        if item["snippet"]["title"] == title:
            return item["id"]["videoId"]
    return None


def fetch_video_snippet(youtube, video_id: str):
    resp = youtube.videos().list(part="snippet", id=video_id).execute()
    items = resp.get("items", [])
    if not items:
        raise RuntimeError(f"Could not find video {video_id}")
    return items[0]["snippet"]


def strip_navigation_block(description: str) -> str:
    if START_MARKER not in description or END_MARKER not in description:
        return description.strip()

    start = description.index(START_MARKER)
    end = description.index(END_MARKER) + len(END_MARKER)
    cleaned = (description[:start] + description[end:]).strip()
    return cleaned


def with_navigation_block(description: str, block: str) -> str:
    base = strip_navigation_block(description)
    parts = [base] if base else []
    parts.append(f"{START_MARKER}\n{block}\n{END_MARKER}")
    combined = "\n\n".join(parts).strip()
    if len(combined) > MAX_DESCRIPTION_LEN:
        raise ValueError(
            f"Description would exceed {MAX_DESCRIPTION_LEN} characters after adding navigation block."
        )
    return combined


def build_full_episode_block(item: dict, next_item: dict | None, course_playlist_id: str | None):
    lines = [
        f"Watch the visual TL;DR: {item['tldr_url']}",
        f"Continue with the next full chapter: {next_item['full_episode_url']}"
        if next_item
        else "Continue with the Operating Agents course playlist below.",
    ]
    if course_playlist_id:
        lines.append(
            f"Operating Agents course playlist: https://www.youtube.com/playlist?list={course_playlist_id}"
        )
    lines.append(
        f"Operating Agents TL;DR playlist: https://www.youtube.com/playlist?list={item['tldr_playlist_id']}"
    )
    return "\n".join(lines)


def build_tldr_block(item: dict, next_item: dict | None, course_playlist_id: str | None):
    lines = [
        f"Watch the full chapter: {item['full_episode_url']}",
        f"Continue with the next TL;DR: {next_item['tldr_url']}"
        if next_item
        else "Continue with the Operating Agents TL;DR playlist below.",
    ]
    if course_playlist_id:
        lines.append(
            f"Operating Agents course playlist: https://www.youtube.com/playlist?list={course_playlist_id}"
        )
    lines.append(
        f"Operating Agents TL;DR playlist: https://www.youtube.com/playlist?list={item['tldr_playlist_id']}"
    )
    return "\n".join(lines)


def update_video_description(youtube, video_id: str, snippet: dict, new_description: str, dry_run: bool):
    if dry_run:
        return

    payload = {
        "categoryId": snippet.get("categoryId", "27"),
        "title": snippet["title"],
        "description": new_description,
    }
    if "defaultLanguage" in snippet:
        payload["defaultLanguage"] = snippet["defaultLanguage"]
    if "tags" in snippet:
        payload["tags"] = snippet["tags"]

    youtube.videos().update(
        part="snippet",
        body={"id": video_id, "snippet": payload},
    ).execute()


def build_series_items(youtube, metadata: dict):
    playlist_id = metadata["playlist_id"]
    items = []
    for item in metadata["items"]:
        tldr_video_id = find_video_by_title(youtube, item["full_title"])
        if not tldr_video_id:
            raise RuntimeError(f"Could not find TL;DR upload for title: {item['full_title']}")

        series_item = dict(item)
        series_item["tldr_video_id"] = tldr_video_id
        series_item["tldr_url"] = f"https://www.youtube.com/watch?v={tldr_video_id}"
        series_item["tldr_playlist_id"] = playlist_id
        items.append(series_item)
    return items


def parse_args():
    parser = argparse.ArgumentParser(
        description="Sync Operating Agents description cross-links using the YouTube Data API."
    )
    parser.add_argument(
        "--course-playlist-id",
        help="Optional playlist ID for the main Operating Agents course playlist.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write updates to YouTube. Without this flag, the script only prints the planned changes.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    youtube = load_youtube()
    metadata = load_metadata()
    series_items = build_series_items(youtube, metadata)
    results = []

    for index, item in enumerate(series_items):
        next_item = series_items[index + 1] if index + 1 < len(series_items) else None

        full_snippet = fetch_video_snippet(youtube, item["full_episode_video_id"])
        tldr_snippet = fetch_video_snippet(youtube, item["tldr_video_id"])

        full_block = build_full_episode_block(item, next_item, args.course_playlist_id)
        tldr_block = build_tldr_block(item, next_item, args.course_playlist_id)

        full_description = with_navigation_block(
            full_snippet.get("description", ""), full_block
        )
        tldr_description = with_navigation_block(
            tldr_snippet.get("description", ""), tldr_block
        )

        update_video_description(
            youtube,
            item["full_episode_video_id"],
            full_snippet,
            full_description,
            dry_run=not args.apply,
        )
        update_video_description(
            youtube,
            item["tldr_video_id"],
            tldr_snippet,
            tldr_description,
            dry_run=not args.apply,
        )

        results.append(
            {
                "chapter": item["chapter"],
                "full_episode_video_id": item["full_episode_video_id"],
                "tldr_video_id": item["tldr_video_id"],
                "full_episode_title": full_snippet["title"],
                "tldr_title": tldr_snippet["title"],
                "full_episode_navigation_block": full_block,
                "tldr_navigation_block": tldr_block,
                "applied": args.apply,
            }
        )

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
