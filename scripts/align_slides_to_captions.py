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
class CaptionBlock:
    index: int
    start: str
    end: str
    text: str
    tokens: list[str]


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout


def normalize(text: str) -> list[str]:
    lowered = text.lower()
    cleaned = re.sub(r"[^a-z0-9\s]", " ", lowered)
    return [token for token in cleaned.split() if len(token) >= 3 and token not in STOPWORDS]


def ocr_slide(slide_path: Path) -> str:
    return run(["tesseract", str(slide_path), "stdout"])


def sorted_slides(slides_dir: Path) -> list[Path]:
    slides = sorted(
        [path for path in slides_dir.iterdir() if path.suffix.lower() in {".png", ".jpg", ".jpeg"}]
    )
    if not slides:
        raise FileNotFoundError(f"No slide images found in {slides_dir}")
    return slides


def validate_support_slides_dir(primary_slides_dir: Path, support_slides_dir: Path) -> None:
    primary_names = {slide.name for slide in sorted_slides(primary_slides_dir)}
    support_names = {slide.name for slide in sorted_slides(support_slides_dir)}
    missing = sorted(primary_names - support_names)
    if missing:
        raise FileNotFoundError(
            f"Support slides directory {support_slides_dir} is missing slide files required by "
            f"{primary_slides_dir}: {', '.join(missing[:5])}"
        )


def parse_srt(srt_path: Path) -> list[CaptionBlock]:
    raw = srt_path.read_text()
    blocks = [block.strip() for block in re.split(r"\n\s*\n", raw) if block.strip()]
    parsed: list[CaptionBlock] = []
    for block in blocks:
        lines = block.splitlines()
        if len(lines) < 3 or "-->" not in lines[1]:
            continue
        start, end = [part.strip().replace(",", ".") for part in lines[1].split("-->")]
        text = " ".join(line.strip() for line in lines[2:] if line.strip())
        parsed.append(
            CaptionBlock(
                index=len(parsed),
                start=start,
                end=end,
                text=text,
                tokens=normalize(text),
            )
        )
    return parsed


def score_window(slide_tokens: list[str], window: list[CaptionBlock]) -> float:
    if not slide_tokens:
        return 0.0
    window_tokens: list[str] = []
    for block in window:
        window_tokens.extend(block.tokens)
    if not window_tokens:
        return 0.0

    slide_counts = Counter(slide_tokens)
    window_counts = Counter(window_tokens)
    overlap = sum(min(slide_counts[token], window_counts[token]) for token in slide_counts)
    coverage = overlap / max(1, len(slide_tokens))
    density = overlap / max(1, len(window_tokens))
    return coverage * 0.8 + density * 0.2


def find_best_window(
    slide_tokens: list[str], captions: list[CaptionBlock], min_index: int
) -> tuple[int, int, float]:
    best_start = min_index
    best_end = min(min_index + 1, len(captions))
    best_score = -1.0

    for start in range(min_index, len(captions)):
        for width in range(1, 8):
            end = start + width
            if end > len(captions):
                break
            score = score_window(slide_tokens, captions[start:end])
            if score > best_score:
                best_start = start
                best_end = end
                best_score = score
    return best_start, best_end, best_score


def align(
    slides_dir: Path, captions_path: Path, support_slides_dirs: list[Path] | None = None
) -> dict:
    support_slides_dirs = support_slides_dirs or []
    for support_slides_dir in support_slides_dirs:
        validate_support_slides_dir(slides_dir, support_slides_dir)

    captions = parse_srt(captions_path)
    slides = sorted_slides(slides_dir)

    segments = []
    min_index = 0
    for slide in slides:
        ocr_texts = [ocr_slide(slide)]
        for support_slides_dir in support_slides_dirs:
            ocr_texts.append(ocr_slide(support_slides_dir / slide.name))
        combined_ocr_text = "\n".join(text for text in ocr_texts if text.strip())
        slide_tokens = normalize(combined_ocr_text)
        start_idx, end_idx, score = find_best_window(slide_tokens, captions, min_index)
        matched = captions[start_idx:end_idx]
        start = matched[0].start if matched else "00:00:00.000"
        segments.append(
            {
                "image": slide.name,
                "start": start,
                "caption_start_index": start_idx,
                "caption_end_index": max(start_idx, end_idx - 1),
                "match_score": round(score, 4),
                "ocr_excerpt": " ".join(combined_ocr_text.split())[:280],
                "ocr_source_count": len(ocr_texts),
                "matched_captions": [block.text for block in matched],
            }
        )
        min_index = max(start_idx + 1, end_idx - 1)

    return {
        "captions": str(captions_path),
        "slides_dir": str(slides_dir),
        "support_slides_dirs": [str(path) for path in support_slides_dirs],
        "segments": segments,
    }


def parse_args():
    parser = argparse.ArgumentParser(
        description="Draft slide-change timestamps by matching slide OCR against timed caption blocks."
    )
    parser.add_argument("--slides-dir", required=True, type=Path)
    parser.add_argument(
        "--support-slides-dir",
        action="append",
        type=Path,
        help="Optional additional slide directory with matching filenames to contribute complementary OCR.",
    )
    parser.add_argument("--captions", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main():
    args = parse_args()
    alignment = align(args.slides_dir, args.captions, args.support_slides_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(alignment, indent=2) + "\n")
    print(args.output)


if __name__ == "__main__":
    main()
