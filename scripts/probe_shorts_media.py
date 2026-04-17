#!/usr/bin/env python3
"""Probe local Shorts masters before upload."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


def run_ffprobe(path: Path) -> dict[str, Any]:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-show_streams",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def parse_duration(value: Any) -> float | None:
    if value in {None, "N/A", ""}:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_frame_rate(value: str | None) -> float | None:
    if not value or value == "0/0":
        return None
    try:
        return float(Fraction(value))
    except (ValueError, ZeroDivisionError):
        return None


def probe_short(
    path: Path,
    *,
    width: int = 1080,
    height: int = 1920,
    max_duration: float = 180.0,
    require_audio: bool = True,
) -> dict[str, Any]:
    data = run_ffprobe(path)
    streams = data.get("streams", [])
    video = next((stream for stream in streams if stream.get("codec_type") == "video"), None)
    audio = next((stream for stream in streams if stream.get("codec_type") == "audio"), None)
    format_duration = parse_duration(data.get("format", {}).get("duration"))
    video_duration = parse_duration(video.get("duration")) if video else None
    audio_duration = parse_duration(audio.get("duration")) if audio else None
    duration_values = [
        value
        for value in [format_duration, video_duration, audio_duration]
        if value is not None
    ]
    duration = max(duration_values) if duration_values else 0.0

    errors: list[str] = []
    warnings: list[str] = []
    if not video:
        errors.append("missing video stream")
    else:
        if video.get("width") != width or video.get("height") != height:
            errors.append(
                f"expected {width}x{height}, found {video.get('width')}x{video.get('height')}"
            )
        frame_rate = parse_frame_rate(video.get("r_frame_rate"))
        if frame_rate is None:
            warnings.append("could not parse frame rate")

    if require_audio and not audio:
        errors.append("missing audio stream")

    if duration > max_duration:
        errors.append(f"duration {duration:.3f}s exceeds {max_duration:.3f}s")
    if not duration_values:
        errors.append("could not determine duration")

    return {
        "path": str(path),
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "video": {
            "codec": video.get("codec_name") if video else None,
            "width": video.get("width") if video else None,
            "height": video.get("height") if video else None,
            "r_frame_rate": video.get("r_frame_rate") if video else None,
            "duration": video_duration,
        },
        "audio": {
            "codec": audio.get("codec_name") if audio else None,
            "duration": audio_duration,
        },
        "format_duration": format_duration,
        "duration": duration,
    }


def probe_files(
    paths: list[Path],
    *,
    width: int = 1080,
    height: int = 1920,
    max_duration: float = 180.0,
    require_audio: bool = True,
) -> list[dict[str, Any]]:
    return [
        probe_short(
            path,
            width=width,
            height=height,
            max_duration=max_duration,
            require_audio=require_audio,
        )
        for path in paths
    ]


def collect_inputs(items: list[Path]) -> list[Path]:
    videos: list[Path] = []
    for item in items:
        if item.is_dir():
            videos.extend(sorted(path for path in item.iterdir() if path.suffix.lower() == ".mp4"))
        elif item.suffix.lower() == ".mp4":
            videos.append(item)
    if not videos:
        raise FileNotFoundError("No MP4 input files found.")
    return videos


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe local portrait Shorts files before upload.")
    parser.add_argument("inputs", nargs="+", type=Path, help="MP4 files or directories to probe.")
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1920)
    parser.add_argument("--max-duration", type=float, default=180.0)
    parser.add_argument("--allow-missing-audio", action="store_true")
    parser.add_argument("--json", action="store_true", help="Print structured JSON output.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = collect_inputs(args.inputs)
    results = probe_files(
        paths,
        width=args.width,
        height=args.height,
        max_duration=args.max_duration,
        require_audio=not args.allow_missing_audio,
    )

    if args.json:
        print(json.dumps({"items": results}, indent=2))
    else:
        for item in results:
            status = "OK" if item["ok"] else "FAIL"
            print(
                f"{status}\t{item['path']}\t"
                f"{item['video']['width']}x{item['video']['height']}\t"
                f"{item['duration']:.3f}s\t"
                f"audio={item['audio']['codec'] or 'none'}"
            )
            for error in item["errors"]:
                print(f"  error: {error}")
            for warning in item["warnings"]:
                print(f"  warning: {warning}")

    if any(not item["ok"] for item in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
