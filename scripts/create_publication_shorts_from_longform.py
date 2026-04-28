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
import os
import re
import shutil
import subprocess
import textwrap
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from convert_landscape_videos_to_portrait import convert_video, ffprobe_duration_seconds


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


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text())


@dataclass(frozen=True)
class CaptionCue:
    start: float
    end: float
    text: str


def timestamp_to_seconds(value: str) -> float:
    normalized = value.strip().replace(",", ".")
    hours, minutes, seconds = normalized.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def seconds_to_ass_timestamp(value: float) -> str:
    centiseconds = max(0, int(round(value * 100)))
    seconds, cs = divmod(centiseconds, 100)
    minutes, sec = divmod(seconds, 60)
    hours, minute = divmod(minutes, 60)
    return f"{hours}:{minute:02d}:{sec:02d}.{cs:02d}"


def parse_srt(path: Path) -> list[CaptionCue]:
    content = path.read_text(encoding="utf-8-sig")
    blocks = re.split(r"\n\s*\n", content.strip())
    cues: list[CaptionCue] = []
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        time_line = next((line for line in lines if "-->" in line), "")
        if not time_line:
            continue
        time_index = lines.index(time_line)
        match = re.match(r"(?P<start>\S+)\s+-->\s+(?P<end>\S+)", time_line)
        if not match:
            continue
        text = " ".join(lines[time_index + 1 :])
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            cues.append(
                CaptionCue(
                    start=timestamp_to_seconds(match.group("start")),
                    end=timestamp_to_seconds(match.group("end")),
                    text=text,
                )
            )
    return sorted(cues, key=lambda cue: (cue.start, cue.end))


def escape_ass_text(value: str) -> str:
    return (
        value.replace("\\", r"\\")
        .replace("{", "(")
        .replace("}", ")")
        .replace("\n", r"\N")
    )


def wrap_ass_text(value: str, width: int, max_lines: int) -> str:
    lines = textwrap.wrap(
        re.sub(r"\s+", " ", value).strip(),
        width=width,
        break_long_words=False,
        break_on_hyphens=False,
    )
    if len(lines) > max_lines:
        lines = lines[: max_lines - 1] + [" ".join(lines[max_lines - 1 :])]
    return r"\N".join(escape_ass_text(line) for line in lines)


def caption_events_for_clip(
    cues: list[CaptionCue],
    clip_start: float,
    clip_end: float,
) -> list[CaptionCue]:
    boundaries = {clip_start, clip_end}
    for cue in cues:
        if cue.end <= clip_start or cue.start >= clip_end:
            continue
        boundaries.add(max(cue.start, clip_start))
        boundaries.add(min(cue.end, clip_end))

    events: list[CaptionCue] = []
    sorted_boundaries = sorted(boundaries)
    for start, end in zip(sorted_boundaries, sorted_boundaries[1:]):
        if end - start < 0.35:
            continue
        active = [cue for cue in cues if cue.start <= start < cue.end]
        if not active:
            continue
        cue = max(active, key=lambda item: (item.start, item.end))
        relative_start = start - clip_start
        relative_end = end - clip_start
        if events and events[-1].text == cue.text and abs(events[-1].end - relative_start) < 0.05:
            events[-1] = CaptionCue(events[-1].start, relative_end, events[-1].text)
            continue
        events.append(CaptionCue(relative_start, relative_end, cue.text))
    return events


def write_overlay_ass(
    output_path: Path,
    duration: float,
    width: int,
    height: int,
    hook: str,
    cta: str,
    captions: list[CaptionCue],
    caption_wrap_width: int,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "[Script Info]",
        "Title: Publication Short overlay",
        "ScriptType: v4.00+",
        "WrapStyle: 0",
        "ScaledBorderAndShadow: yes",
        f"PlayResX: {width}",
        f"PlayResY: {height}",
        "",
        "[V4+ Styles]",
        (
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
            "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
            "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
            "Alignment, MarginL, MarginR, MarginV, Encoding"
        ),
        (
            "Style: Hook,Arial,72,&H00FFFFFF,&H000000FF,&HAA000000,&H66000000,"
            "-1,0,0,0,100,100,0,0,1,5,1,8,76,76,130,1"
        ),
        (
            "Style: Caption,Arial,58,&H00FFFFFF,&H000000FF,&H00000000,&HAA000000,"
            "-1,0,0,0,100,100,0,0,1,5,1,2,80,80,555,1"
        ),
        (
            "Style: CTA,Arial,42,&H00FFFFFF,&H000000FF,&H00000000,&H66000000,"
            "-1,0,0,0,100,100,0,0,1,4,1,2,100,100,300,1"
        ),
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    end = seconds_to_ass_timestamp(duration)
    lines.append(
        f"Dialogue: 1,0:00:00.00,{end},Hook,,0,0,0,,"
        f"{wrap_ass_text(hook, width=24, max_lines=3)}"
    )
    lines.append(
        f"Dialogue: 1,0:00:00.00,{end},CTA,,0,0,0,,"
        f"{wrap_ass_text(cta, width=34, max_lines=2)}"
    )
    for cue in captions:
        lines.append(
            "Dialogue: 2,"
            f"{seconds_to_ass_timestamp(cue.start)},"
            f"{seconds_to_ass_timestamp(cue.end)},"
            "Caption,,0,0,0,,"
            f"{wrap_ass_text(cue.text, width=caption_wrap_width, max_lines=3)}"
        )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def resolve_font_path() -> Path | None:
    candidates = [
        Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
        Path("/Library/Fonts/Arial Bold.ttf"),
        Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
        Path("/System/Library/Fonts/Helvetica.ttc"),
    ]
    return next((path for path in candidates if path.exists()), None)


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    font_path = resolve_font_path()
    if font_path:
        return ImageFont.truetype(str(font_path), size=size)
    return ImageFont.load_default(size=size)


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, stroke_width: int) -> int:
    left, _, right, _ = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    return right - left


def wrap_lines_by_pixels(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.ImageFont,
    max_width: int,
    max_lines: int,
    stroke_width: int,
) -> list[str]:
    words = re.sub(r"\s+", " ", text).strip().split()
    if not words:
        return []
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        candidate = " ".join([*current, word])
        if not current or text_width(draw, candidate, font, stroke_width) <= max_width:
            current.append(word)
            continue
        lines.append(" ".join(current))
        current = [word]
    if current:
        lines.append(" ".join(current))
    if len(lines) > max_lines:
        lines = lines[: max_lines - 1] + [" ".join(lines[max_lines - 1 :])]
    return lines


def draw_text_block(
    image: Image.Image,
    text: str,
    font_size: int,
    max_width: int,
    anchor_y: int,
    vertical_anchor: str,
    max_lines: int,
    line_spacing: int,
    stroke_width: int,
    background: tuple[int, int, int, int],
) -> None:
    canvas_width, _ = image.size
    draw = ImageDraw.Draw(image)
    font = load_font(font_size)
    lines = wrap_lines_by_pixels(draw, text, font, max_width, max_lines, stroke_width)
    if not lines:
        return

    boxes = [draw.textbbox((0, 0), line, font=font, stroke_width=stroke_width) for line in lines]
    line_heights = [bottom - top for _, top, _, bottom in boxes]
    line_widths = [right - left for left, _, right, _ in boxes]
    block_height = sum(line_heights) + line_spacing * (len(lines) - 1)
    block_width = max(line_widths)
    if vertical_anchor == "bottom":
        y = anchor_y - block_height
    elif vertical_anchor == "center":
        y = anchor_y - block_height // 2
    else:
        y = anchor_y

    padding_x = 28
    padding_y = 18
    x0 = (canvas_width - block_width) // 2 - padding_x
    x1 = (canvas_width + block_width) // 2 + padding_x
    y0 = y - padding_y
    y1 = y + block_height + padding_y
    if background[3] > 0:
        draw.rounded_rectangle((x0, y0, x1, y1), radius=18, fill=background)

    cursor_y = y
    for line, line_height in zip(lines, line_heights):
        line_width = text_width(draw, line, font, stroke_width)
        x = (canvas_width - line_width) // 2
        draw.text(
            (x, cursor_y),
            line,
            font=font,
            fill=(255, 255, 255, 255),
            stroke_width=stroke_width,
            stroke_fill=(0, 0, 0, 235),
        )
        cursor_y += line_height + line_spacing


def draw_text_overlay(
    output_path: Path,
    canvas_width: int,
    canvas_height: int,
    text: str,
    font_size: int,
    max_width: int,
    anchor_y: int,
    vertical_anchor: str,
    max_lines: int,
    line_spacing: int,
    stroke_width: int,
    background: tuple[int, int, int, int],
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))
    draw_text_block(
        image=image,
        text=text,
        font_size=font_size,
        max_width=max_width,
        anchor_y=anchor_y,
        vertical_anchor=vertical_anchor,
        max_lines=max_lines,
        line_spacing=line_spacing,
        stroke_width=stroke_width,
        background=background,
    )
    image.save(output_path)


def write_overlay_images(
    output_dir: Path,
    width: int,
    height: int,
    hook: str,
    cta: str,
    captions: list[CaptionCue],
) -> list[tuple[Path, float | None, float | None]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    for existing in output_dir.glob("*.png"):
        existing.unlink()

    overlays: list[tuple[Path, float | None, float | None]] = []
    hook_path = output_dir / "hook.png"
    draw_text_overlay(
        output_path=hook_path,
        canvas_width=width,
        canvas_height=height,
        text=hook,
        font_size=74,
        max_width=920,
        anchor_y=126,
        vertical_anchor="top",
        max_lines=3,
        line_spacing=8,
        stroke_width=4,
        background=(0, 0, 0, 90),
    )
    overlays.append((hook_path, None, None))

    cta_path = output_dir / "cta.png"
    draw_text_overlay(
        output_path=cta_path,
        canvas_width=width,
        canvas_height=height,
        text=cta,
        font_size=44,
        max_width=860,
        anchor_y=1635,
        vertical_anchor="bottom",
        max_lines=2,
        line_spacing=6,
        stroke_width=3,
        background=(0, 0, 0, 140),
    )
    overlays.append((cta_path, None, None))

    for index, cue in enumerate(captions, start=1):
        caption_path = output_dir / f"caption-{index:03d}.png"
        draw_text_overlay(
            output_path=caption_path,
            canvas_width=width,
            canvas_height=height,
            text=cue.text,
            font_size=60,
            max_width=920,
            anchor_y=1370,
            vertical_anchor="bottom",
            max_lines=3,
            line_spacing=6,
            stroke_width=4,
            background=(0, 0, 0, 125),
        )
        overlays.append((caption_path, cue.start, cue.end))
    return overlays


def write_composite_overlay_image(
    output_path: Path,
    width: int,
    height: int,
    hook: str,
    cta: str,
    caption: str | None,
) -> None:
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_text_block(
        image=image,
        text=hook,
        font_size=74,
        max_width=920,
        anchor_y=126,
        vertical_anchor="top",
        max_lines=3,
        line_spacing=8,
        stroke_width=4,
        background=(0, 0, 0, 90),
    )
    draw_text_block(
        image=image,
        text=cta,
        font_size=44,
        max_width=860,
        anchor_y=1635,
        vertical_anchor="bottom",
        max_lines=2,
        line_spacing=6,
        stroke_width=3,
        background=(0, 0, 0, 140),
    )
    if caption:
        draw_text_block(
            image=image,
            text=caption,
            font_size=60,
            max_width=920,
            anchor_y=1370,
            vertical_anchor="bottom",
            max_lines=3,
            line_spacing=6,
            stroke_width=4,
            background=(0, 0, 0, 125),
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)


def overlay_segments(duration: float, captions: list[CaptionCue]) -> list[tuple[float, float, str | None]]:
    segments: list[tuple[float, float, str | None]] = []
    cursor = 0.0
    for cue in captions:
        start = max(0.0, min(duration, cue.start))
        end = max(0.0, min(duration, cue.end))
        if end - start < 0.05:
            continue
        if start - cursor > 0.05:
            segments.append((cursor, start, None))
        segments.append((max(start, cursor), end, cue.text))
        cursor = max(cursor, end)
    if duration - cursor > 0.05:
        segments.append((cursor, duration, None))
    return segments or [(0.0, duration, None)]


def quote_ffconcat_path(path: Path) -> str:
    return str(path.resolve()).replace("'", "'\\''")


def write_overlay_video(
    output_dir: Path,
    width: int,
    height: int,
    fps: int,
    duration: float,
    hook: str,
    cta: str,
    captions: list[CaptionCue],
) -> tuple[Path, int]:
    output_dir.mkdir(parents=True, exist_ok=True)
    for existing in output_dir.glob("segment-*.png"):
        existing.unlink()
    overlay_video = output_dir / "overlay.mov"
    concat_path = output_dir / "overlay.ffconcat"
    if overlay_video.exists():
        overlay_video.unlink()

    segments = overlay_segments(duration, captions)
    concat_lines = ["ffconcat version 1.0"]
    last_image: Path | None = None
    for index, (start, end, caption) in enumerate(segments):
        image_path = output_dir / f"segment-{index:03d}.png"
        write_composite_overlay_image(
            output_path=image_path,
            width=width,
            height=height,
            hook=hook,
            cta=cta,
            caption=caption,
        )
        concat_lines.append(f"file '{quote_ffconcat_path(image_path)}'")
        concat_lines.append(f"duration {end - start:.6f}")
        last_image = image_path
    if last_image:
        concat_lines.append(f"file '{quote_ffconcat_path(last_image)}'")
    concat_path.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")
    run(
        [
            FFMPEG_BIN,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_path),
            "-t",
            f"{duration:.3f}",
            "-vf",
            f"fps={fps},format=rgba",
            "-an",
            "-c:v",
            "qtrle",
            str(overlay_video),
        ]
    )
    return overlay_video, len(segments)


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
            FFMPEG_BIN,
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
    parser.add_argument(
        "--srt-file",
        type=Path,
        help="Timed SRT captions for the source video. Required when --burn-in-subtitles is used.",
    )
    parser.add_argument(
        "--burn-in-subtitles",
        action="store_true",
        help="Burn top hooks, spoken subtitles, and a related-video CTA into each portrait Short.",
    )
    parser.add_argument(
        "--overlay-dir",
        type=Path,
        help="Directory for generated ASS overlay files. Defaults next to the manifest.",
    )
    parser.add_argument(
        "--default-cta",
        default="Full cinematic brief in Related Video",
        help="Bottom CTA used when a clip does not define cta in the manifest.",
    )
    parser.add_argument("--caption-wrap-width", type=int, default=30)
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
    overlay_dir = args.overlay_dir or (base_dir / "overlays")
    if args.burn_in_subtitles and not args.srt_file:
        raise SystemExit("--srt-file is required with --burn-in-subtitles")
    caption_cues = parse_srt(args.srt_file) if args.burn_in_subtitles and args.srt_file else []

    results: list[dict] = []
    for index, clip in enumerate(clips, start=1):
        slug = clip["slug"]
        stem = f"{index:02d}-{slug}"
        landscape_path = landscape_dir / f"{stem}.mp4"
        portrait_path = portrait_dir / f"{stem}_portrait.mp4"
        clip_overlay_dir = overlay_dir / stem if args.burn_in_subtitles else None
        overlay_video: Path | None = None
        overlay_count = 0

        extract_clip(
            input_path=args.video_file,
            output_path=landscape_path,
            start=clip["start"],
            end=clip["end"],
            crf=args.clip_crf,
            audio_bitrate=args.portrait_audio_bitrate,
        )
        if clip_overlay_dir:
            clip_start = timestamp_to_seconds(clip["start"])
            clip_end = timestamp_to_seconds(clip["end"])
            overlay_video, overlay_count = write_overlay_video(
                output_dir=clip_overlay_dir,
                width=args.portrait_width,
                height=args.portrait_height,
                fps=args.portrait_fps,
                duration=clip_end - clip_start,
                hook=clip.get("hook") or clip.get("top_hook") or clip["title"],
                cta=clip.get("cta") or args.default_cta,
                captions=caption_events_for_clip(caption_cues, clip_start, clip_end),
            )
        convert_video(
            input_path=landscape_path,
            output_path=portrait_path,
            width=args.portrait_width,
            height=args.portrait_height,
            fps=args.portrait_fps,
            video_bitrate=args.portrait_video_bitrate,
            audio_bitrate=args.portrait_audio_bitrate,
            overlay_video=overlay_video,
        )
        results.append(
            {
                "slug": slug,
                "title": clip["title"],
                "hook": clip.get("hook") or clip.get("top_hook") or clip["title"],
                "cta": clip.get("cta") or args.default_cta if args.burn_in_subtitles else None,
                "landscape_path": str(landscape_path),
                "portrait_path": str(portrait_path),
                "overlay_path": str(clip_overlay_dir) if clip_overlay_dir else None,
                "overlay_count": overlay_count,
                "landscape_duration": ffprobe_duration_seconds(landscape_path),
                "portrait_duration": ffprobe_duration_seconds(portrait_path),
                "publish_at": clip.get("publish_at"),
            }
        )

    print(json.dumps({"manifest": str(args.manifest), "clips": results}, indent=2))


if __name__ == "__main__":
    main()
