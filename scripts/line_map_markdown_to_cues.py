from __future__ import annotations

import argparse
import json
import re
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
    "okay",
    "really",
    "now",
    "then",
}


@dataclass
class CaptionBlock:
    index: int
    start: str
    end: str
    text: str
    tokens: list[str]


@dataclass
class SlideMapRow:
    image: str
    line_start: int
    line_end: int
    rationale: str


def normalize(text: str) -> list[str]:
    lowered = text.lower()
    cleaned = re.sub(r"[^a-z0-9\s]", " ", lowered)
    return [token for token in cleaned.split() if len(token) >= 3 and token not in STOPWORDS]


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


def parse_map(markdown_path: Path) -> list[SlideMapRow]:
    rows: list[SlideMapRow] = []
    pattern = re.compile(
        r"^\|\s*`(?P<image>slide-\d+\.(?:png|jpg|jpeg))`\s*\|\s*`(?P<start>\d+)-(?P<end>\d+)`\s*\|\s*(?P<why>.+?)\s*\|\s*$"
    )
    for line in markdown_path.read_text().splitlines():
        match = pattern.match(line)
        if not match:
            continue
        rows.append(
            SlideMapRow(
                image=match.group("image"),
                line_start=int(match.group("start")),
                line_end=int(match.group("end")),
                rationale=match.group("why"),
            )
        )
    if not rows:
        raise ValueError(f"No slide mapping rows found in {markdown_path}")
    return rows


def load_numbered_transcript(path: Path) -> dict[int, str]:
    line_map: dict[int, str] = {}
    for raw in path.read_text().splitlines():
        match = re.match(r"^\s*(\d+)\t?(.*)$", raw)
        if not match:
            continue
        line_no = int(match.group(1))
        text = match.group(2).strip()
        line_map[line_no] = text
    return line_map


def transcript_excerpt(line_map: dict[int, str], start: int, end: int, max_tokens: int = 32) -> str:
    parts: list[str] = []
    for line_no in range(start, end + 1):
        text = line_map.get(line_no, "").strip()
        if text:
            parts.append(text)
        if len(normalize(" ".join(parts))) >= max_tokens:
            break
    return " ".join(parts)


def subsequence_score(needle: list[str], haystack: list[str]) -> float:
    if not needle or not haystack:
        return 0.0
    matched = 0
    pos = 0
    for token in needle:
        while pos < len(haystack) and haystack[pos] != token:
            pos += 1
        if pos == len(haystack):
            break
        matched += 1
        pos += 1
    return matched / len(needle)


def overlap_score(needle: list[str], haystack: list[str]) -> float:
    if not needle or not haystack:
        return 0.0
    needle_set = set(needle)
    haystack_set = set(haystack)
    return len(needle_set & haystack_set) / len(needle_set)


def find_caption_start(
    excerpt: str, captions: list[CaptionBlock], min_index: int
) -> tuple[int, float, list[str]]:
    excerpt_tokens = normalize(excerpt)[:18]
    if not excerpt_tokens:
        return min_index, 0.0, []

    best_idx = min_index
    best_score = -1.0
    best_window_text: list[str] = []

    for start_idx in range(min_index, len(captions)):
        for width in range(1, 7):
            end_idx = min(len(captions), start_idx + width)
            window = captions[start_idx:end_idx]
            window_tokens: list[str] = []
            for block in window:
                window_tokens.extend(block.tokens)
            if not window_tokens:
                continue
            seq = subsequence_score(excerpt_tokens, window_tokens)
            overlap = overlap_score(excerpt_tokens, window_tokens)
            score = seq * 0.75 + overlap * 0.25
            if score > best_score:
                best_idx = start_idx
                best_score = score
                best_window_text = [block.text for block in window]
            if score >= 0.98:
                return best_idx, best_score, best_window_text
    return best_idx, best_score, best_window_text


def infer_audio_path(chapter_dir: Path) -> Path:
    audio_dir = chapter_dir / "artifacts" / "audio"
    for suffix in ("*.mp3", "*.m4a", "*.wav"):
        candidates = sorted(audio_dir.glob(suffix))
        if candidates:
            return candidates[0]
    raise FileNotFoundError(f"No audio file found in {audio_dir}")


def infer_slides_dir(chapter_dir: Path) -> Path:
    slides_root = chapter_dir / "artifacts" / "slides"
    candidates = sorted([path for path in slides_root.iterdir() if path.is_dir()])
    if not candidates:
        raise FileNotFoundError(f"No slide directory found in {slides_root}")
    return candidates[0]


def build_cues(map_path: Path, captions_path: Path, transcript_path: Path, chapter_dir: Path) -> dict:
    rows = parse_map(map_path)
    rows = sorted(rows, key=lambda row: (row.line_start, row.image))
    captions = parse_srt(captions_path)
    line_map = load_numbered_transcript(transcript_path)

    segments = []
    min_caption_index = 0
    for row in rows:
        excerpt = transcript_excerpt(line_map, row.line_start, row.line_end)
        caption_index, score, matched = find_caption_start(excerpt, captions, min_caption_index)
        start = captions[caption_index].start if captions else "00:00:00.000"
        segments.append(
            {
                "image": row.image,
                "start": start,
                "note": f"Transcript lines {row.line_start:04d}-{row.line_end:04d}.",
                "match_score": round(score, 4),
                "excerpt": excerpt,
                "matched_captions": matched,
            }
        )
        min_caption_index = caption_index

    return {
        "audio": str(infer_audio_path(chapter_dir).relative_to(Path.cwd())),
        "slides_dir": str(infer_slides_dir(chapter_dir).relative_to(Path.cwd())),
        "captions": str(captions_path.relative_to(Path.cwd())),
        "map": str(map_path.relative_to(Path.cwd())),
        "segments": segments,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a verified slide-to-transcript markdown map plus local SRT captions into a cue-sheet JSON."
    )
    parser.add_argument("--map", required=True, type=Path)
    parser.add_argument("--captions", required=True, type=Path)
    parser.add_argument("--transcript", required=True, type=Path)
    parser.add_argument("--chapter-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cues = build_cues(args.map, args.captions, args.transcript, args.chapter_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(cues, indent=2) + "\n")
    print(args.output)


if __name__ == "__main__":
    main()
