#!/usr/bin/env python3
"""Poll YouTube caption availability and write the first downloadable track."""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "workflows" / "skills" / "youtube-data-api" / "scripts"))

from download_video_captions import choose_caption, download_via_watch_page  # noqa: E402
from googleapiclient.errors import HttpError  # noqa: E402
from youtube_common import build_youtube  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Wait for a YouTube caption track, then download it.")
    parser.add_argument("--video-id", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--language", default="en", help="Preferred caption language code. Default: en")
    parser.add_argument(
        "--track-kind",
        choices=["asr", "standard", "any"],
        default="asr",
        help="Prefer automatic captions, standard captions, or any available track.",
    )
    parser.add_argument("--format", choices=["srt", "vtt"], default="srt")
    parser.add_argument("--interval", type=int, default=600, help="Seconds between attempts. Default: 600.")
    parser.add_argument("--timeout", type=int, default=7200, help="Maximum seconds to wait. Default: 7200.")
    return parser.parse_args()


def log(message: str) -> None:
    print(f"[{datetime.now(timezone.utc).isoformat()}] {message}", flush=True)


def download_once(*, video_id: str, output: Path, language: str, track_kind: str, fmt: str) -> None:
    youtube = build_youtube()
    try:
        caption = choose_caption(youtube, video_id, language, track_kind)
        request = youtube.captions().download(id=caption["id"], tfmt=fmt)
        content = request.execute()
    except HttpError as exc:
        status_code = getattr(exc, "status_code", None)
        response_status = getattr(getattr(exc, "resp", None), "status", None)
        if status_code != 403 and response_status != 403:
            raise
        content = download_via_watch_page(video_id, language, track_kind, fmt)

    output.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        output.write_bytes(content)
    else:
        output.write_text(content, encoding="utf-8")


def main() -> None:
    args = parse_args()
    if args.interval <= 0:
        raise SystemExit("ERROR: --interval must be positive.")
    if args.timeout < 0:
        raise SystemExit("ERROR: --timeout must be zero or positive.")

    deadline = time.monotonic() + args.timeout
    attempt = 1
    while True:
        try:
            download_once(
                video_id=args.video_id,
                output=args.output,
                language=args.language,
                track_kind=args.track_kind,
                fmt=args.format,
            )
            log(f"downloaded captions to {args.output}")
            return
        except Exception as exc:  # Caption availability errors vary by API and watch-page fallback.
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise SystemExit(f"ERROR: captions not available after {attempt} attempts: {exc}") from exc
            sleep_for = min(args.interval, max(0, int(remaining)))
            log(f"attempt {attempt} failed for {args.video_id}: {exc}; sleeping {sleep_for}s")
            time.sleep(sleep_for)
            attempt += 1


if __name__ == "__main__":
    main()
