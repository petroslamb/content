from __future__ import annotations

import argparse
import json
import math
import subprocess
import tempfile
from pathlib import Path


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def ffprobe_duration_seconds(media_path: Path) -> float:
    output = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(media_path),
        ]
    )
    return float(output)


def format_timestamp(seconds: float) -> str:
    millis = int(round(seconds * 1000))
    hours, remainder = divmod(millis, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def parse_timestamp(value: str) -> float:
    hhmmss, millis = value.split(".")
    hours, minutes, seconds = [int(part) for part in hhmmss.split(":")]
    return hours * 3600 + minutes * 60 + seconds + int(millis) / 1000


def sorted_slides(slides_dir: Path) -> list[Path]:
    slides = sorted(
        [path for path in slides_dir.iterdir() if path.suffix.lower() in {".png", ".jpg", ".jpeg"}]
    )
    if not slides:
        raise FileNotFoundError(f"No slide images found in {slides_dir}")
    return slides


def build_template(audio_path: Path, slides_dir: Path) -> dict:
    slides = sorted_slides(slides_dir)
    duration = ffprobe_duration_seconds(audio_path)
    step = duration / len(slides)
    segments = []
    for index, slide in enumerate(slides):
        segments.append(
            {
                "image": slide.name,
                "start": format_timestamp(index * step),
                "note": "",
            }
        )
    return {
        "audio": str(audio_path),
        "slides_dir": str(slides_dir),
        "segments": segments,
    }


def load_cues(cues_path: Path) -> dict:
    return json.loads(cues_path.read_text())


def validate_segments(segments: list[dict], audio_duration: float) -> list[tuple[str, float, float]]:
    if not segments:
        raise ValueError("Cue sheet has no segments.")

    parsed = sorted(
        ((segment["image"], parse_timestamp(segment["start"])) for segment in segments),
        key=lambda item: (item[1], item[0]),
    )

    validated = []
    for index, (image, start) in enumerate(parsed):
        if index + 1 < len(segments):
            end = parsed[index + 1][1]
        else:
            end = audio_duration
        if end <= start:
            raise ValueError(f"Segment {image} has non-increasing timestamps.")
        validated.append((image, start, end))
    return validated


def build_concat_file(slides_dir: Path, segments: list[tuple[str, float, float]]) -> str:
    lines: list[str] = []
    for image, start, end in segments:
        duration = end - start
        path = (slides_dir / image).resolve()
        lines.append(f"file '{path}'")
        lines.append(f"duration {duration:.3f}")
    # Repeat the final file once more because ffmpeg concat expects the last frame to be re-declared.
    lines.append(f"file '{(slides_dir / segments[-1][0]).resolve()}'")
    return "\n".join(lines) + "\n"


def render_video(cues_path: Path, output_path: Path, fps: int, width: int, height: int) -> None:
    cues = load_cues(cues_path)
    audio_path = Path(cues["audio"])
    slides_dir = Path(cues["slides_dir"])
    audio_duration = ffprobe_duration_seconds(audio_path)
    segments = validate_segments(cues["segments"], audio_duration)
    concat_text = build_concat_file(slides_dir, segments)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as handle:
        handle.write(concat_text)
        concat_path = Path(handle.name)

    try:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_path),
                "-i",
                str(audio_path),
                "-vf",
                f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
                f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
                "-r",
                str(fps),
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-shortest",
                str(output_path),
            ],
            check=True,
        )
    finally:
        concat_path.unlink(missing_ok=True)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Render a narrated slideshow video from an MP3, slide images, and a cue sheet."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    template = subparsers.add_parser("template", help="Generate a draft cue sheet.")
    template.add_argument("--audio", required=True, type=Path)
    template.add_argument("--slides-dir", required=True, type=Path)
    template.add_argument("--output", required=True, type=Path)

    render = subparsers.add_parser("render", help="Render an MP4 from a cue sheet.")
    render.add_argument("--cues", required=True, type=Path)
    render.add_argument("--output", required=True, type=Path)
    render.add_argument("--fps", type=int, default=30)
    render.add_argument("--width", type=int, default=1920)
    render.add_argument("--height", type=int, default=1080)

    return parser.parse_args()


def main():
    args = parse_args()
    if args.command == "template":
        template = build_template(args.audio, args.slides_dir)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(template, indent=2) + "\n")
        print(args.output)
        return

    if args.command == "render":
        render_video(args.cues, args.output, args.fps, args.width, args.height)
        print(args.output)
        return

    raise ValueError(f"Unsupported command {args.command}")


if __name__ == "__main__":
    main()
