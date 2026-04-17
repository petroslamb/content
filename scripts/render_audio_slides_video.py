from __future__ import annotations

import argparse
import json
import math
import subprocess
import tempfile
from pathlib import Path

from PIL import Image


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


def resolve_image_path(slides_dir: Path, segment: dict) -> Path:
    image_path = segment.get("image_path")
    if image_path:
        return Path(image_path).resolve()
    return (slides_dir / segment["image"]).resolve()


def validate_segments(
    slides_dir: Path, segments: list[dict], audio_duration: float
) -> list[dict]:
    if not segments:
        raise ValueError("Cue sheet has no segments.")

    parsed = sorted(
        (
            {
                "image": segment["image"],
                "image_path": resolve_image_path(slides_dir, segment),
                "start": parse_timestamp(segment["start"]),
            }
            for segment in segments
        ),
        key=lambda item: (item["start"], item["image"], str(item["image_path"])),
    )

    validated = []
    for index, item in enumerate(parsed):
        start = item["start"]
        if index + 1 < len(segments):
            end = parsed[index + 1]["start"]
        else:
            end = audio_duration
        if end <= start:
            raise ValueError(f"Segment {item['image']} has non-increasing timestamps.")
        validated.append(
            {
                "image": item["image"],
                "image_path": item["image_path"],
                "start": start,
                "end": end,
            }
        )
    return validated


def build_concat_file(image_map: dict[Path, Path], segments: list[dict]) -> str:
    lines: list[str] = []
    for segment in segments:
        duration = segment["end"] - segment["start"]
        path = image_map[segment["image_path"]]
        lines.append(f"file '{path}'")
        lines.append(f"duration {duration:.3f}")
    # Repeat the final file once more because ffmpeg concat expects the last frame to be re-declared.
    lines.append(f"file '{image_map[segments[-1]['image_path']]}'")
    return "\n".join(lines) + "\n"


def preprocess_slide_images(
    segments: list[dict], width: int, height: int, output_dir: Path
) -> dict[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    image_map: dict[Path, Path] = {}
    for index, source in enumerate(sorted({segment["image_path"] for segment in segments})):
        target = output_dir / f"{index:04d}_{source.name}"
        with Image.open(source) as image:
            rgb = image.convert("RGB")
            rgb.thumbnail((width, height), Image.LANCZOS)
            frame = Image.new("RGB", (width, height), "black")
            offset = ((width - rgb.width) // 2, (height - rgb.height) // 2)
            frame.paste(rgb, offset)
            frame.save(target)
        image_map[source] = target.resolve()
    return image_map


def render_video(cues_path: Path, output_path: Path, fps: int, width: int, height: int) -> None:
    cues = load_cues(cues_path)
    audio_path = Path(cues["audio"])
    slides_dir = Path(cues["slides_dir"])
    audio_duration = ffprobe_duration_seconds(audio_path)
    segments = validate_segments(slides_dir, cues["segments"], audio_duration)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="render-audio-slides-video-") as tmpdir:
        tmpdir_path = Path(tmpdir)
        prepared_slide_map = preprocess_slide_images(
            segments, width, height, tmpdir_path / "slides"
        )
        concat_text = build_concat_file(prepared_slide_map, segments)

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
                    "-t",
                    f"{audio_duration:.3f}",
                    "-vf",
                    "format=yuv420p",
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
