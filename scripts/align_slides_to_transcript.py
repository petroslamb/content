from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "to",
    "of",
    "in",
    "on",
    "for",
    "with",
    "is",
    "it",
    "this",
    "that",
    "as",
    "at",
    "by",
    "from",
    "be",
    "are",
    "we",
    "you",
    "they",
    "their",
    "our",
    "your",
    "can",
    "not",
    "into",
    "than",
    "when",
    "what",
    "how",
    "why",
    "which",
    "will",
    "but",
    "if",
    "do",
    "does",
    "did",
    "have",
    "has",
    "had",
    "so",
    "these",
    "those",
    "just",
    "also",
    "today",
    "right",
    "yeah",
}


@dataclass
class Paragraph:
    index: int
    raw: str
    start_char: int
    end_char: int
    tokens: list[str]


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout


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
    ).strip()
    return float(output)


def format_timestamp(seconds: float) -> str:
    millis = int(round(seconds * 1000))
    hours, remainder = divmod(millis, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def normalize(text: str) -> list[str]:
    lowered = text.lower()
    cleaned = re.sub(r"[^a-z0-9\s]", " ", lowered)
    tokens = [token for token in cleaned.split() if len(token) >= 3 and token not in STOPWORDS]
    return tokens


def ocr_slide(slide_path: Path) -> str:
    return run(["tesseract", str(slide_path), "stdout"])


def load_paragraphs(transcript_path: Path) -> tuple[str, list[Paragraph]]:
    raw = transcript_path.read_text()
    blocks = [block.strip() for block in re.split(r"\n\s*\n", raw) if block.strip()]
    paragraphs: list[Paragraph] = []
    cursor = 0
    for index, block in enumerate(blocks):
        start = raw.find(block, cursor)
        end = start + len(block)
        cursor = end
        paragraphs.append(
            Paragraph(
                index=index,
                raw=block,
                start_char=start,
                end_char=end,
                tokens=normalize(block),
            )
        )
    return raw, paragraphs


def sorted_slides(slides_dir: Path) -> list[Path]:
    slides = sorted([path for path in slides_dir.iterdir() if path.suffix.lower() in {".png", ".jpg", ".jpeg"}])
    if not slides:
        raise FileNotFoundError(f"No slide images found in {slides_dir}")
    return slides


def score_window(slide_tokens: list[str], paragraph_window: list[Paragraph]) -> float:
    if not slide_tokens:
        return 0.0
    window_tokens: list[str] = []
    for paragraph in paragraph_window:
        window_tokens.extend(paragraph.tokens)
    if not window_tokens:
        return 0.0

    slide_counts = Counter(slide_tokens)
    window_counts = Counter(window_tokens)
    overlap = sum(min(slide_counts[token], window_counts[token]) for token in slide_counts)
    coverage = overlap / max(1, len(slide_tokens))
    density = overlap / max(1, len(window_tokens))
    return coverage * 0.8 + density * 0.2


def find_best_window(slide_tokens: list[str], paragraphs: list[Paragraph], min_index: int) -> tuple[int, int, float]:
    best_start = min_index
    best_end = min(min_index + 1, len(paragraphs))
    best_score = -1.0

    for start in range(min_index, len(paragraphs)):
        for width in range(1, 4):
            end = start + width
            if end > len(paragraphs):
                break
            score = score_window(slide_tokens, paragraphs[start:end])
            if score > best_score:
                best_start = start
                best_end = end
                best_score = score
    return best_start, best_end, best_score


def align(slides_dir: Path, transcript_path: Path, audio_path: Path) -> dict:
    transcript_text, paragraphs = load_paragraphs(transcript_path)
    duration = ffprobe_duration_seconds(audio_path)
    slides = sorted_slides(slides_dir)

    segments = []
    min_index = 0
    for slide in slides:
        ocr_text = ocr_slide(slide)
        slide_tokens = normalize(ocr_text)
        start_idx, end_idx, score = find_best_window(slide_tokens, paragraphs, min_index)
        matched = paragraphs[start_idx:end_idx]
        anchor_char = matched[0].start_char if matched else 0
        timestamp = format_timestamp((anchor_char / max(1, len(transcript_text))) * duration)

        segments.append(
            {
                "image": slide.name,
                "start": timestamp,
                "match_score": round(score, 4),
                "ocr_excerpt": " ".join(ocr_text.split())[:280],
                "matched_paragraphs": [paragraph.raw for paragraph in matched],
            }
        )
        min_index = start_idx

    return {
        "audio": str(audio_path),
        "slides_dir": str(slides_dir),
        "transcript": str(transcript_path),
        "segments": segments,
    }


def parse_args():
    parser = argparse.ArgumentParser(
        description="Align slide images to an untimestamped transcript using OCR and lexical overlap."
    )
    parser.add_argument("--audio", required=True, type=Path)
    parser.add_argument("--slides-dir", required=True, type=Path)
    parser.add_argument("--transcript", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main():
    args = parse_args()
    alignment = align(args.slides_dir, args.transcript, args.audio)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(alignment, indent=2) + "\n")
    print(args.output)


if __name__ == "__main__":
    main()
