from __future__ import annotations

import argparse
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
TOKEN_FILE = Path(".youtube/token.json")


def load_youtube():
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    return build("youtube", "v3", credentials=creds)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download a caption track for a YouTube video you can manage."
    )
    parser.add_argument("--video-id", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--language",
        default="en",
        help="Preferred caption language code. Default: en",
    )
    parser.add_argument(
        "--track-kind",
        choices=["asr", "standard", "any"],
        default="asr",
        help="Prefer automatic captions, standard captions, or any available track.",
    )
    parser.add_argument(
        "--format",
        choices=["srt", "vtt"],
        default="srt",
        help="Caption download format. Default: srt",
    )
    return parser.parse_args()


def track_priority(item: dict, language: str, track_kind: str) -> tuple[int, int]:
    snippet = item["snippet"]
    language_rank = 0 if snippet.get("language") == language else 1
    kind = snippet.get("trackKind", "")
    if track_kind == "any":
        kind_rank = 0
    elif track_kind == "asr":
        kind_rank = 0 if kind == "asr" else 1
    else:
        kind_rank = 0 if kind != "asr" else 1
    return language_rank, kind_rank


def choose_caption(youtube, video_id: str, language: str, track_kind: str) -> dict:
    response = youtube.captions().list(part="id,snippet", videoId=video_id).execute()
    items = response.get("items", [])
    if not items:
        raise RuntimeError(f"No caption tracks found for video {video_id}.")
    return sorted(items, key=lambda item: track_priority(item, language, track_kind))[0]


def scrape_caption_track(video_id: str, language: str, track_kind: str) -> str:
    html = urllib.request.urlopen(f"https://www.youtube.com/watch?v={video_id}").read().decode(
        "utf-8", "ignore"
    )
    match = re.search(r'"captionTracks":(\[.*?\])', html)
    if not match:
        raise RuntimeError(f"Could not find captionTracks on watch page for {video_id}")
    tracks = json.loads(match.group(1))

    def sort_key(track: dict):
        lang_rank = 0 if track.get("languageCode") == language else 1
        kind = track.get("kind", "")
        if track_kind == "any":
            kind_rank = 0
        elif track_kind == "asr":
            kind_rank = 0 if kind == "asr" else 1
        else:
            kind_rank = 0 if kind != "asr" else 1
        return lang_rank, kind_rank

    track = sorted(tracks, key=sort_key)[0]
    return track["baseUrl"].replace("\\u0026", "&")


def download_via_watch_page(video_id: str, language: str, track_kind: str, fmt: str) -> str:
    base_url = scrape_caption_track(video_id, language, track_kind)
    parsed = urllib.parse.urlparse(base_url)
    query = urllib.parse.parse_qs(parsed.query)
    query["fmt"] = [fmt]
    url = urllib.parse.urlunparse(parsed._replace(query=urllib.parse.urlencode(query, doseq=True)))
    return urllib.request.urlopen(url).read().decode("utf-8", "ignore")


def main():
    args = parse_args()
    youtube = load_youtube()
    try:
        caption = choose_caption(youtube, args.video_id, args.language, args.track_kind)
        request = youtube.captions().download(id=caption["id"], tfmt=args.format)
        content = request.execute()
    except HttpError as exc:
        if getattr(exc, "status_code", None) != 403 and exc.resp.status != 403:
            raise
        content = download_via_watch_page(
            args.video_id, args.language, args.track_kind, args.format
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        args.output.write_bytes(content)
    else:
        args.output.write_text(content)
    print(args.output)


if __name__ == "__main__":
    main()
