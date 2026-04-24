from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path


def resolve_binary(name: str) -> str:
    candidates = [
        os.environ.get(name.upper()),
        shutil.which(name),
        f"/opt/homebrew/bin/{name}",
        f"/usr/local/bin/{name}",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    raise FileNotFoundError(f"Could not find required binary: {name}")


FFMPEG_BIN = resolve_binary("ffmpeg")
FFPROBE_BIN = resolve_binary("ffprobe")


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def ffprobe_duration_seconds(path: Path) -> float:
    result = subprocess.run(
        [
            FFPROBE_BIN,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def convert_video(
    input_path: Path,
    output_path: Path,
    width: int,
    height: int,
    fps: int,
    video_bitrate: str,
    audio_bitrate: str,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    filter_graph = (
        f"[0:v]split=2[bg][fg];"
        f"[bg]scale={width}:{height}:force_original_aspect_ratio=increase,"
        f"crop={width}:{height},boxblur=20:10[bgv];"
        f"[fg]scale={width}:{height}:force_original_aspect_ratio=decrease[fgv];"
        f"[bgv][fgv]overlay=(W-w)/2:(H-h)/2,format=yuv420p[v]"
    )
    run(
        [
            FFMPEG_BIN,
            "-y",
            "-i",
            str(input_path),
            "-filter_complex",
            filter_graph,
            "-map",
            "[v]",
            "-map",
            "0:a?",
            "-r",
            str(fps),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-profile:v",
            "high",
            "-level:v",
            "4.1",
            "-b:v",
            video_bitrate,
            "-maxrate",
            video_bitrate,
            "-bufsize",
            "16M",
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
        description=(
            "Convert landscape MP4 clips into vertical 9:16 versions for Shorts-style uploads "
            "by centering the original frame over a blurred portrait background."
        )
    )
    parser.add_argument("inputs", nargs="+", type=Path, help="Input files or directories.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory where portrait MP4 files will be written.",
    )
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1920)
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--video-bitrate", default="6M")
    parser.add_argument("--audio-bitrate", default="192k")
    parser.add_argument(
        "--suffix",
        default="_portrait",
        help="Suffix appended to the output stem before .mp4.",
    )
    return parser.parse_args()


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


def main() -> None:
    args = parse_args()
    videos = collect_inputs(args.inputs)
    for input_path in videos:
        output_path = args.output_dir / f"{input_path.stem}{args.suffix}.mp4"
        convert_video(
            input_path=input_path,
            output_path=output_path,
            width=args.width,
            height=args.height,
            fps=args.fps,
            video_bitrate=args.video_bitrate,
            audio_bitrate=args.audio_bitrate,
        )
        print(
            f"{output_path}\tduration={ffprobe_duration_seconds(output_path):.3f}s"
        )


if __name__ == "__main__":
    main()
