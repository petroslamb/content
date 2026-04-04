from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
import time
from pathlib import Path

from googleapiclient.http import MediaFileUpload

from download_video_captions import download_via_watch_page
from youtube_common import build_youtube


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Upload a temporary unlisted video from local audio plus a still image, "
            "wait for automatic captions, download them, and optionally delete the video."
        )
    )
    parser.add_argument("--audio-path", required=True, type=Path)
    parser.add_argument("--image-path", required=True, type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--description",
        default="Temporary upload for transcript recovery. This video will be removed.",
    )
    parser.add_argument(
        "--privacy-status",
        choices=["private", "unlisted", "public"],
        default="unlisted",
    )
    parser.add_argument("--category-id", default="27")
    parser.add_argument("--poll-interval", type=int, default=120)
    parser.add_argument("--timeout", type=int, default=5400)
    parser.add_argument("--language", default="en")
    parser.add_argument(
        "--track-kind",
        choices=["asr", "standard", "any"],
        default="asr",
    )
    parser.add_argument(
        "--keep-video",
        action="store_true",
        help="Do not delete the uploaded video after transcript recovery.",
    )
    return parser.parse_args()


def preprocess_still_image(image_path: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(image_path),
            "-vf",
            "scale='min(1280,iw)':-2",
            "-frames:v",
            "1",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def build_static_video(audio_path: Path, image_path: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    preprocessed_image = output_path.with_suffix(".jpg")
    preprocess_still_image(image_path, preprocessed_image)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-i",
            str(preprocessed_image),
            "-i",
            str(audio_path),
            "-vf",
            "fps=1,format=yuv420p",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-tune",
            "stillimage",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            "-shortest",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def upload_video(youtube, media_path: Path, title: str, description: str, privacy_status: str, category_id: str) -> str:
    media = MediaFileUpload(str(media_path), chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "categoryId": category_id,
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": False,
            },
        },
        media_body=media,
    )

    response = None
    while response is None:
        _, response = request.next_chunk()
    return response["id"]


def get_processing_status(youtube, video_id: str) -> str | None:
    response = (
        youtube.videos()
        .list(part="processingDetails,status", id=video_id)
        .execute()
    )
    items = response.get("items", [])
    if not items:
        return None
    details = items[0].get("processingDetails", {})
    return details.get("processingStatus") or items[0].get("status", {}).get("uploadStatus")


def poll_for_captions(youtube, video_id: str, language: str, track_kind: str, poll_interval: int, timeout: int) -> tuple[list[dict], str | None]:
    deadline = time.time() + timeout
    last_processing = None
    while time.time() < deadline:
        response = youtube.captions().list(part="id,snippet", videoId=video_id).execute()
        items = response.get("items", [])
        if items:
            return items, last_processing
        last_processing = get_processing_status(youtube, video_id)
        time.sleep(poll_interval)
    raise TimeoutError(
        f"Timed out after {timeout}s waiting for captions on video {video_id}. "
        f"Last processing status: {last_processing or 'unknown'}"
    )


def choose_caption(items: list[dict], language: str, track_kind: str) -> dict:
    def track_priority(item: dict) -> tuple[int, int]:
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

    return sorted(items, key=track_priority)[0]


def download_caption_text(youtube, video_id: str, caption_id: str, language: str, track_kind: str) -> str:
    try:
        return youtube.captions().download(id=caption_id, tfmt="srt").execute().decode("utf-8")
    except Exception:
        return download_via_watch_page(video_id, language, track_kind, "srt")


def delete_video(youtube, video_id: str) -> None:
    youtube.videos().delete(id=video_id).execute()


def main():
    args = parse_args()
    youtube = build_youtube()

    video_id: str | None = None
    caption_track: dict | None = None
    processing_status: str | None = None

    try:
        with tempfile.TemporaryDirectory(prefix="youtube-transcript-recovery-") as tmpdir:
            temp_media_path = Path(tmpdir) / f"{args.output.stem}.mp4"
            build_static_video(args.audio_path, args.image_path, temp_media_path)
            video_id = upload_video(
                youtube,
                temp_media_path,
                args.title,
                args.description,
                args.privacy_status,
                args.category_id,
            )
            items, processing_status = poll_for_captions(
                youtube,
                video_id,
                args.language,
                args.track_kind,
                args.poll_interval,
                args.timeout,
            )
            caption_track = choose_caption(items, args.language, args.track_kind)
            content = download_caption_text(
                youtube,
                video_id,
                caption_track["id"],
                args.language,
                args.track_kind,
            )
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(content)

            result = {
                "video_id": video_id,
                "output": str(args.output),
                "caption_track_id": caption_track["id"],
                "caption_language": caption_track["snippet"].get("language"),
                "caption_kind": caption_track["snippet"].get("trackKind"),
                "processing_status": processing_status,
                "deleted_video": not args.keep_video,
            }
            if not args.keep_video:
                delete_video(youtube, video_id)
            print(json.dumps(result, indent=2))
    except Exception:
        if video_id and not args.keep_video:
            try:
                delete_video(youtube, video_id)
            except Exception:
                pass
        raise


if __name__ == "__main__":
    main()
