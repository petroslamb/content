from __future__ import annotations

import json
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube"]
TOKEN_FILE = Path(".youtube/token.json")
METADATA_FILE = Path("youtube_data_api_playbook/operating_agents_tldr_metadata.json")
MAX_DESCRIPTION_LEN = 5000


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


def upload_video(youtube, item: dict):
    existing = find_video_by_title(youtube, item["full_title"])
    if existing:
        return existing, True

    media = MediaFileUpload(item["local_video_path"], chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": item["full_title"],
                "description": item["description_template"],
                "categoryId": "27",
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
            },
        },
        media_body=media,
    )

    response = None
    while response is None:
        _, response = request.next_chunk()

    return response["id"], False


def add_to_playlist(youtube, playlist_id: str, video_id: str):
    # avoid duplicates
    page = None
    while True:
        resp = (
            youtube.playlistItems()
            .list(part="snippet", playlistId=playlist_id, maxResults=50, pageToken=page)
            .execute()
        )
        for item in resp.get("items", []):
            if item["snippet"]["resourceId"]["videoId"] == video_id:
                return
        page = resp.get("nextPageToken")
        if not page:
            break

    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id,
                },
            }
        },
    ).execute()


def update_full_episode_description(youtube, full_video_id: str, tldr_url: str):
    resp = youtube.videos().list(part="snippet", id=full_video_id).execute()
    items = resp.get("items", [])
    if not items:
        raise RuntimeError(f"Could not find full episode {full_video_id}")
    video = items[0]
    snippet = video["snippet"]
    line = f"Watch the visual TL;DR: {tldr_url}"
    description = snippet.get("description", "")

    lines = description.splitlines()
    if lines and lines[0].startswith("Watch the visual TL;DR: "):
        lines[0] = line
        new_description = "\n".join(lines)
    else:
        new_description = f"{line}\n\n{description}".strip()

    if len(new_description) > MAX_DESCRIPTION_LEN:
        new_description = new_description[: MAX_DESCRIPTION_LEN - 3].rstrip() + "..."

    update_snippet = {
        "categoryId": snippet.get("categoryId", "27"),
        "title": snippet["title"],
        "description": new_description,
    }
    if "defaultLanguage" in snippet:
        update_snippet["defaultLanguage"] = snippet["defaultLanguage"]
    if "tags" in snippet:
        update_snippet["tags"] = snippet["tags"]

    youtube.videos().update(
        part="snippet",
        body={"id": full_video_id, "snippet": update_snippet},
    ).execute()


def main():
    youtube = load_youtube()
    metadata = load_metadata()
    playlist_id = metadata["playlist_id"]
    results = []

    for item in metadata["items"]:
        video_id, existed = upload_video(youtube, item)
        add_to_playlist(youtube, playlist_id, video_id)
        tldr_url = f"https://www.youtube.com/watch?v={video_id}"
        update_full_episode_description(youtube, item["full_episode_video_id"], tldr_url)
        results.append(
            {
                "chapter": item["chapter"],
                "title": item["full_title"],
                "video_id": video_id,
                "url": tldr_url,
                "existing": existed,
            }
        )

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
