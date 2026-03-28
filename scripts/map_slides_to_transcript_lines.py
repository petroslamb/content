from __future__ import annotations

import argparse
import json
import re
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
    "really",
}


@dataclass
class TranscriptBlock:
    start_line: int
    end_line: int
    raw: str
    tokens: list[str]


def normalize(text: str) -> list[str]:
    lowered = text.lower()
    cleaned = re.sub(r"[^a-z0-9\s]", " ", lowered)
    return [token for token in cleaned.split() if len(token) >= 3 and token not in STOPWORDS]


def load_blocks(numbered_transcript: Path) -> list[TranscriptBlock]:
    blocks: list[TranscriptBlock] = []
    current_lines: list[tuple[int, str]] = []
    for raw_line in numbered_transcript.read_text().splitlines():
        match = re.match(r"\s*(\d+)\t?(.*)", raw_line)
        if not match:
            continue
        line_no = int(match.group(1))
        text = match.group(2).strip()
        if text:
            current_lines.append((line_no, text))
        elif current_lines:
            raw = " ".join(line for _, line in current_lines)
            blocks.append(
                TranscriptBlock(
                    start_line=current_lines[0][0],
                    end_line=current_lines[-1][0],
                    raw=raw,
                    tokens=normalize(raw),
                )
            )
            current_lines = []

    if current_lines:
        raw = " ".join(line for _, line in current_lines)
        blocks.append(
            TranscriptBlock(
                start_line=current_lines[0][0],
                end_line=current_lines[-1][0],
                raw=raw,
                tokens=normalize(raw),
            )
        )
    return blocks


def sorted_ocr_files(ocr_dir: Path) -> list[Path]:
    files = sorted(ocr_dir.glob("slide-*.txt"))
    if not files:
        raise FileNotFoundError(f"No OCR files found in {ocr_dir}")
    return files


def score_window(slide_tokens: list[str], block_window: list[TranscriptBlock]) -> float:
    if not slide_tokens:
        return 0.0
    window_tokens: list[str] = []
    for block in block_window:
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
    slide_tokens: list[str], blocks: list[TranscriptBlock], min_index: int
) -> tuple[int, int, float]:
    best_start = min_index
    best_end = min(min_index + 1, len(blocks))
    best_score = -1.0
    for start in range(min_index, len(blocks)):
        for width in range(1, 7):
            end = start + width
            if end > len(blocks):
                break
            score = score_window(slide_tokens, blocks[start:end])
            if score > best_score:
                best_start = start
                best_end = end
                best_score = score
    return best_start, best_end, best_score


def build_mapping(numbered_transcript: Path, ocr_dir: Path) -> dict:
    blocks = load_blocks(numbered_transcript)
    mappings = []
    min_index = 0
    for ocr_file in sorted_ocr_files(ocr_dir):
        ocr_text = ocr_file.read_text()
        slide_tokens = normalize(ocr_text)
        start_idx, end_idx, score = find_best_window(slide_tokens, blocks, min_index)
        matched = blocks[start_idx:end_idx]
        mappings.append(
            {
                "slide": ocr_file.with_suffix(".png").name,
                "proposed_line_start": matched[0].start_line if matched else 1,
                "proposed_line_end": matched[-1].end_line if matched else 1,
                "match_score": round(score, 4),
                "ocr_excerpt": " ".join(ocr_text.split())[:280],
                "matched_blocks": [block.raw for block in matched],
            }
        )
        min_index = start_idx
    return {
        "numbered_transcript": str(numbered_transcript),
        "ocr_dir": str(ocr_dir),
        "mappings": mappings,
    }


def parse_args():
    parser = argparse.ArgumentParser(
        description="Draft slide-to-transcript line ranges from OCR and a numbered transcript."
    )
    parser.add_argument("--numbered-transcript", required=True, type=Path)
    parser.add_argument("--ocr-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main():
    args = parse_args()
    result = build_mapping(args.numbered_transcript, args.ocr_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(args.output)


if __name__ == "__main__":
    main()
