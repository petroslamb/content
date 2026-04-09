#!/usr/bin/env python3
"""
Create publication Shorts from a long-form video using a manifest of timed clips.

Run from project root:
  .venv/bin/python scripts/create_publication_shorts_from_longform.py \
    --video-file <longform.mp4> \
    --manifest <shorts_manifest.json>
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from convert_landscape_videos_to_portrait import convert_video, ffprobe_duration_seconds


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text())


def extract_clip(
    input_path: Path,
    output_path: Path,
    start: str,
    end: str,
    crf: int,
    audio_bitrate: str,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            start,
            "-to",
            end,
            "-i",
            str(input_path),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            str(crf),
            "-c:a",
            "aac",
            "-b:a",
            audio_bitrate,
            "-movflags",
            "+faststart",
            str(output_path),
        ]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create landscape and portrait Shorts clips from a long-form publication video."
    )
    parser.add_argument("--video-file", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument(
        "--landscape-dir",
        type=Path,
        help="Override output directory for landscape clips. Defaults next to the manifest.",
    )
    parser.add_argument(
        "--portrait-dir",
        type=Path,
        help="Override output directory for portrait clips. Defaults next to the manifest.",
    )
    parser.add_argument("--portrait-width", type=int, default=1080)
    parser.add_argument("--portrait-height", type=int, default=1920)
    parser.add_argument("--portrait-fps", type=int, default=24)
    parser.add_argument("--portrait-video-bitrate", default="6M")
    parser.add_argument("--portrait-audio-bitrate", default="192k")
    parser.add_argument("--clip-crf", type=int, default=18)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest = load_manifest(args.manifest)
    clips = manifest.get("clips", [])
    if not clips:
        raise SystemExit(f"No clips found in manifest: {args.manifest}")

    base_dir = args.manifest.parent
    landscape_dir = args.landscape_dir or (base_dir / "landscape")
    portrait_dir = args.portrait_dir or (base_dir / "portrait")

    results: list[dict] = []
    for index, clip in enumerate(clips, start=1):
        slug = clip["slug"]
        stem = f"{index:02d}-{slug}"
        landscape_path = landscape_dir / f"{stem}.mp4"
        portrait_path = portrait_dir / f"{stem}_portrait.mp4"

        extract_clip(
            input_path=args.video_file,
            output_path=landscape_path,
            start=clip["start"],
            end=clip["end"],
            crf=args.clip_crf,
            audio_bitrate=args.portrait_audio_bitrate,
        )
        convert_video(
            input_path=landscape_path,
            output_path=portrait_path,
            width=args.portrait_width,
            height=args.portrait_height,
            fps=args.portrait_fps,
            video_bitrate=args.portrait_video_bitrate,
            audio_bitrate=args.portrait_audio_bitrate,
        )
        results.append(
            {
                "slug": slug,
                "title": clip["title"],
                "landscape_path": str(landscape_path),
                "portrait_path": str(portrait_path),
                "landscape_duration": ffprobe_duration_seconds(landscape_path),
                "portrait_duration": ffprobe_duration_seconds(portrait_path),
                "publish_at": clip.get("publish_at"),
            }
        )

    print(json.dumps({"manifest": str(args.manifest), "clips": results}, indent=2))


if __name__ == "__main__":
    main()
