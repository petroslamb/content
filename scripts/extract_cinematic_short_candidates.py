#!/usr/bin/env python3
"""Extract candidate Shorts windows from a cinematic SRT with novelty hints."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CaptionBlock:
    index: int
    start_seconds: float
    end_seconds: float
    start_timestamp: str
    end_timestamp: str
    text: str


WORD_RE = re.compile(r"[a-z0-9']+")
PUNCTUATION_END_RE = re.compile(r"[.!?][\"']?$")

HOOK_MARKERS = {
    "why",
    "when",
    "how",
    "but",
    "because",
    "instead",
    "actually",
    "really",
    "not",
    "more",
    "less",
    "same",
    "different",
    "breaks",
    "fails",
    "won",
}

ARC_MARKERS = {
    "because",
    "but",
    "so",
    "therefore",
    "instead",
    "that",
    "which",
    "means",
    "then",
}

SHARE_MARKERS = {
    "why",
    "how",
    "not",
    "instead",
    "same",
    "different",
    "broken",
    "wiring",
    "control",
    "memory",
    "agent",
    "agents",
    "ai",
    "model",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract candidate Shorts windows from a cinematic SRT.")
    parser.add_argument("--package", required=True, help="Package path under publications, e.g. illusion-of-swarm")
    parser.add_argument("--srt-file", type=Path, required=True, help="Timed SRT captions for the cinematic video.")
    parser.add_argument("--output", type=Path, required=True, help="Where to write the candidate report JSON.")
    parser.add_argument("--min-seconds", type=float, default=35.0)
    parser.add_argument("--target-seconds", type=float, default=90.0)
    parser.add_argument("--max-seconds", type=float, default=120.0)
    parser.add_argument("--limit", type=int, default=24, help="Maximum candidate windows to keep after dedupe.")
    return parser.parse_args()


def repo_package_path(package_arg: str) -> Path:
    package = Path(package_arg)
    if package.exists():
        return package
    candidate = Path("publications") / package
    if candidate.exists():
        return candidate
    raise SystemExit(f"ERROR: Package path not found: {package_arg}")


def parse_timestamp(value: str) -> float:
    hours, minutes, rest = value.split(":")
    seconds, millis = rest.replace(",", ".").split(".")
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(millis[:3]) / 1000.0


def format_timestamp(seconds: float) -> str:
    millis_total = round(seconds * 1000)
    hours, rem = divmod(millis_total, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, millis = divmod(rem, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def parse_srt(path: Path) -> list[CaptionBlock]:
    raw = path.read_text(encoding="utf-8")
    blocks: list[CaptionBlock] = []
    for chunk in re.split(r"\n\s*\n", raw.strip()):
        lines = [line.strip("\ufeff") for line in chunk.splitlines() if line.strip()]
        if len(lines) < 3:
            continue
        try:
            index = int(lines[0])
        except ValueError:
            continue
        if "-->" not in lines[1]:
            continue
        start_raw, end_raw = [part.strip() for part in lines[1].split("-->")]
        text = " ".join(lines[2:]).strip()
        text = re.sub(r"\s+", " ", text)
        blocks.append(
            CaptionBlock(
                index=index,
                start_seconds=parse_timestamp(start_raw),
                end_seconds=parse_timestamp(end_raw),
                start_timestamp=format_timestamp(parse_timestamp(start_raw)),
                end_timestamp=format_timestamp(parse_timestamp(end_raw)),
                text=text,
            )
        )
    if not blocks:
        raise SystemExit(f"ERROR: No caption blocks parsed from {path}")
    return blocks


def normalize_tokens(text: str) -> list[str]:
    return [token for token in WORD_RE.findall(text.lower()) if len(token) > 2]


def sentence_like_end(text: str) -> bool:
    return bool(PUNCTUATION_END_RE.search(text.strip()))


def load_existing_shorts(package_path: Path) -> list[dict[str, str]]:
    existing: list[dict[str, str]] = []
    for manifest_path in sorted(package_path.glob("artifacts/video/**/shorts_manifest.json")):
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        for clip in data.get("clips", []):
            existing.append(
                {
                    "source": str(manifest_path),
                    "slug": str(clip.get("slug", "")),
                    "title": str(clip.get("title", "")),
                    "summary": str(clip.get("summary", "")),
                }
            )
    return existing


def jaccard_similarity(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def novelty_score(text: str, existing: list[dict[str, str]]) -> tuple[int, dict[str, Any] | None]:
    candidate_tokens = set(normalize_tokens(text))
    if not existing or not candidate_tokens:
        return 5, None
    best_match: dict[str, Any] | None = None
    best_similarity = 0.0
    for item in existing:
        item_text = " ".join([item["slug"], item["title"], item["summary"]])
        similarity = jaccard_similarity(candidate_tokens, set(normalize_tokens(item_text)))
        if similarity > best_similarity:
            best_similarity = similarity
            best_match = {
                "similarity": round(similarity, 3),
                "title": item["title"],
                "slug": item["slug"],
                "source": item["source"],
            }
    if best_similarity < 0.12:
        return 5, best_match
    if best_similarity < 0.2:
        return 4, best_match
    if best_similarity < 0.3:
        return 3, best_match
    if best_similarity < 0.4:
        return 2, best_match
    return 1, best_match


def clamp_score(value: int) -> int:
    return max(1, min(5, value))


def hook_strength(text: str) -> int:
    first_slice = " ".join(normalize_tokens(text)[:18])
    tokens = set(normalize_tokens(first_slice))
    score = 1
    if any(marker in tokens for marker in HOOK_MARKERS):
        score += 2
    if any(char.isdigit() for char in first_slice):
        score += 1
    if len(first_slice.split()) <= 14:
        score += 1
    return clamp_score(score)


def standalone_clarity(text: str) -> int:
    lowered = text.lower()
    pronouns = sum(lowered.count(token) for token in (" it ", " this ", " that ", " they ", " these "))
    score = 3
    if pronouns <= 2:
        score += 1
    if pronouns == 0:
        score += 1
    if len(text.split()) > 180:
        score -= 1
    return clamp_score(score)


def clip_arc_score(text: str, duration_seconds: float) -> int:
    tokens = set(normalize_tokens(text))
    score = 2
    if 45 <= duration_seconds <= 80:
        score += 2
    elif 35 <= duration_seconds <= 100:
        score += 1
    if any(marker in tokens for marker in ARC_MARKERS):
        score += 1
    return clamp_score(score)


def shareability_score(text: str) -> int:
    tokens = set(normalize_tokens(text))
    score = 1
    if any(marker in tokens for marker in SHARE_MARKERS):
        score += 2
    if any(char.isdigit() for char in text):
        score += 1
    if len(text) < 420:
        score += 1
    return clamp_score(score)


def suggest_slug(text: str) -> str:
    tokens = [token for token in normalize_tokens(text) if token not in {"the", "and", "with", "from", "into"}]
    return "-".join(tokens[:8]) or "candidate-window"


def build_window(blocks: list[CaptionBlock], start_index: int, end_index: int, existing: list[dict[str, str]]) -> dict[str, Any]:
    selected = blocks[start_index : end_index + 1]
    text = " ".join(block.text for block in selected).strip()
    text = re.sub(r"\s+", " ", text)
    duration_seconds = selected[-1].end_seconds - selected[0].start_seconds
    novelty, novelty_match = novelty_score(text, existing)
    scores = {
        "hook_strength": hook_strength(text),
        "standalone_clarity": standalone_clarity(text),
        "novelty_vs_existing_channel_shorts": novelty,
        "clip_arc_and_compression": clip_arc_score(text, duration_seconds),
        "rewatch_shareability": shareability_score(text),
    }
    total_score = sum(scores.values())
    if total_score >= 22:
        band = "approved_candidate"
    elif total_score >= 20:
        band = "reserve_candidate"
    else:
        band = "reject_candidate"
    return {
        "start": selected[0].start_timestamp,
        "end": selected[-1].end_timestamp,
        "start_seconds": round(selected[0].start_seconds, 3),
        "end_seconds": round(selected[-1].end_seconds, 3),
        "duration_seconds": round(duration_seconds, 3),
        "excerpt": text,
        "suggested_slug": suggest_slug(text),
        "score_breakdown": scores,
        "total_score": total_score,
        "heuristic_band": band,
        "novelty_match": novelty_match,
        "source_caption_range": [selected[0].index, selected[-1].index],
    }


def choose_end_index(blocks: list[CaptionBlock], start_index: int, min_seconds: float, target_seconds: float, max_seconds: float) -> int | None:
    best_index: int | None = None
    best_rank: tuple[float, int] | None = None
    start_seconds = blocks[start_index].start_seconds
    for end_index in range(start_index, len(blocks)):
        duration = blocks[end_index].end_seconds - start_seconds
        if duration > max_seconds:
            break
        if duration < min_seconds:
            continue
        punctuation_bonus = 0 if sentence_like_end(blocks[end_index].text) else 1
        rank = (abs(duration - target_seconds), punctuation_bonus)
        if best_rank is None or rank < best_rank:
            best_rank = rank
            best_index = end_index
    return best_index


def overlap_ratio(left: dict[str, Any], right: dict[str, Any]) -> float:
    start = max(float(left["start_seconds"]), float(right["start_seconds"]))
    end = min(float(left["end_seconds"]), float(right["end_seconds"]))
    if end <= start:
        return 0.0
    overlap = end - start
    left_duration = float(left["end_seconds"]) - float(left["start_seconds"])
    right_duration = float(right["end_seconds"]) - float(right["start_seconds"])
    shorter = min(left_duration, right_duration) or 1.0
    return overlap / shorter


def dedupe_candidates(candidates: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    ordered = sorted(candidates, key=lambda item: (-item["total_score"], item["duration_seconds"], item["start"]))
    kept: list[dict[str, Any]] = []
    for candidate in ordered:
        if any(overlap_ratio(candidate, existing) >= 0.75 for existing in kept):
            continue
        kept.append(candidate)
        if len(kept) >= limit:
            break
    return sorted(kept, key=lambda item: item["start"])


def build_candidates(
    blocks: list[CaptionBlock],
    existing: list[dict[str, str]],
    min_seconds: float,
    target_seconds: float,
    max_seconds: float,
    limit: int,
) -> list[dict[str, Any]]:
    raw_candidates: list[dict[str, Any]] = []
    for start_index in range(len(blocks)):
        end_index = choose_end_index(blocks, start_index, min_seconds, target_seconds, max_seconds)
        if end_index is None:
            continue
        candidate = build_window(blocks, start_index, end_index, existing)
        raw_candidates.append(candidate)
    return dedupe_candidates(raw_candidates, limit)


def main() -> None:
    args = parse_args()
    package_path = repo_package_path(args.package)
    blocks = parse_srt(args.srt_file)
    existing = load_existing_shorts(package_path)
    candidates = build_candidates(
        blocks=blocks,
        existing=existing,
        min_seconds=args.min_seconds,
        target_seconds=args.target_seconds,
        max_seconds=args.max_seconds,
        limit=args.limit,
    )
    payload = {
        "package": str(package_path),
        "srt_file": str(args.srt_file),
        "existing_short_count": len(existing),
        "candidate_count": len(candidates),
        "rubric_note": "Use these candidates as a transcript-derived shortlist. Final approval still requires manual rubric scoring against the high-bar thresholds.",
        "thresholds": {
            "approved_min": 22,
            "reserve_min": 20,
        },
        "candidates": candidates,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
