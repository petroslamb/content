from __future__ import annotations

import argparse
import json
from pathlib import Path

from align_slides_to_captions import align, sorted_slides, validate_support_slides_dir
from render_audio_slides_video import (
    ffprobe_duration_seconds,
    format_timestamp,
    parse_timestamp,
    render_video,
)


def repo_relative(path: Path) -> str:
    path = path.resolve()
    cwd = Path.cwd().resolve()
    try:
        return str(path.relative_to(cwd))
    except ValueError:
        return str(path)


def validate_render_slides_dir(ocr_slides_dir: Path, render_slides_dir: Path) -> None:
    ocr_names = {slide.name for slide in sorted_slides(ocr_slides_dir)}
    render_names = {slide.name for slide in sorted_slides(render_slides_dir)}
    missing = sorted(ocr_names - render_names)
    if missing:
        raise FileNotFoundError(
            f"Render slides directory {render_slides_dir} is missing slide files required by "
            f"{ocr_slides_dir}: {', '.join(missing[:5])}"
        )


def effective_segment_start(segments: list[dict], index: int) -> float:
    if index == 0:
        return 0.0
    return parse_timestamp(segments[index]["start"])


def build_cues(
    audio_path: Path,
    captions_path: Path,
    ocr_slides_dir: Path,
    support_slides_dirs: list[Path],
    render_slides_dirs: list[Path],
) -> dict:
    alignment = align(ocr_slides_dir, captions_path, support_slides_dirs)
    audio_duration = ffprobe_duration_seconds(audio_path)
    segments: list[dict] = []
    for index, segment in enumerate(alignment["segments"]):
        section_start = effective_segment_start(alignment["segments"], index)
        if index + 1 < len(alignment["segments"]):
            section_end = parse_timestamp(alignment["segments"][index + 1]["start"])
        else:
            section_end = audio_duration

        for variant_index, render_slides_dir in enumerate(render_slides_dirs):
            variant_start = section_start + (
                (section_end - section_start) * variant_index / len(render_slides_dirs)
            )
            segments.append(
                {
                    "image": segment["image"],
                    "image_path": repo_relative((render_slides_dir / segment["image"]).resolve()),
                    "start": format_timestamp(variant_start),
                    "note": (
                        "Caption-first draft from slide OCR. "
                        f"Caption window {segment['caption_start_index']:04d}-{segment['caption_end_index']:04d}. "
                        f"Render variant: {render_slides_dir.name}."
                    ),
                    "match_score": segment["match_score"],
                    "ocr_excerpt": segment["ocr_excerpt"],
                    "matched_captions": segment["matched_captions"],
                    "caption_start_index": segment["caption_start_index"],
                    "caption_end_index": segment["caption_end_index"],
                    "render_variant": render_slides_dir.name,
                }
            )

    return {
        "audio": repo_relative(audio_path),
        "captions": repo_relative(captions_path),
        "slides_dir": repo_relative(render_slides_dirs[0]),
        "alignment_source_slides_dir": repo_relative(ocr_slides_dir),
        "alignment_support_slides_dirs": [repo_relative(path) for path in support_slides_dirs],
        "render_variant_slides_dirs": [repo_relative(path) for path in render_slides_dirs],
        "segments": segments,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Draft a caption-aligned slideshow cue sheet from local slides plus a timed SRT, "
            "and optionally render the MP4 in one step."
        )
    )
    parser.add_argument("--audio", required=True, type=Path)
    parser.add_argument("--captions", required=True, type=Path)
    parser.add_argument("--slides-dir", required=True, type=Path)
    parser.add_argument(
        "--support-slides-dir",
        action="append",
        type=Path,
        help="Optional additional slide directory with matching filenames to contribute complementary OCR.",
    )
    parser.add_argument(
        "--render-slides-dir",
        action="append",
        type=Path,
        help=(
            "Optional render slide directory. Repeat this flag to interleave multiple slide decks "
            "that share the same filenames as --slides-dir."
        ),
    )
    parser.add_argument("--output-cues", required=True, type=Path)
    parser.add_argument("--output-video", type=Path)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    support_slides_dirs = args.support_slides_dir or []
    render_slides_dirs = args.render_slides_dir or [args.slides_dir]
    for support_slides_dir in support_slides_dirs:
        validate_support_slides_dir(args.slides_dir, support_slides_dir)
    for render_slides_dir in render_slides_dirs:
        validate_render_slides_dir(args.slides_dir, render_slides_dir)

    cues = build_cues(
        args.audio,
        args.captions,
        args.slides_dir,
        support_slides_dirs,
        render_slides_dirs,
    )
    args.output_cues.parent.mkdir(parents=True, exist_ok=True)
    args.output_cues.write_text(json.dumps(cues, indent=2) + "\n")

    if args.output_video:
        render_video(args.output_cues, args.output_video, args.fps, args.width, args.height)
        print(json.dumps({"cues": str(args.output_cues), "video": str(args.output_video)}, indent=2))
        return

    print(args.output_cues)


if __name__ == "__main__":
    main()
