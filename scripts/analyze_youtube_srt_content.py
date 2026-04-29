#!/usr/bin/env python3
"""Analyze local SRT files for YouTube video content rubric fields."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER_PATH = REPO_ROOT / "experiments" / "youtube-analytics" / "metrics_ledger.json"
DEFAULT_OUTPUT_PATH = REPO_ROOT / "experiments" / "youtube-analytics" / "content_rubric.json"
STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "for",
    "from",
    "how",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "was",
    "what",
    "when",
    "where",
    "why",
    "with",
    "you",
}
CTA_TERMS = {"full", "brief", "video", "watch", "related", "below", "description", "review"}
SPECIFICITY_TERMS = {
    "because",
    "when",
    "without",
    "system",
    "systems",
    "agent",
    "agents",
    "model",
    "models",
    "failure",
    "design",
    "control",
    "memory",
    "planning",
    "policy",
    "risk",
}


@dataclass
class Cue:
    start: float
    end: float
    text: str


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n")


def normalize_tokens(value: str | None) -> list[str]:
    if not value:
        return []
    return [
        token
        for token in re.findall(r"[a-z0-9][a-z0-9'-]*", value.lower())
        if token not in STOP_WORDS and len(token) > 2
    ]


def slug_tokens(value: str | None) -> set[str]:
    return set(normalize_tokens((value or "").replace("_", " ").replace("-", " ")))


def srt_timestamp_seconds(value: str) -> float:
    match = re.fullmatch(r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})", value.strip())
    if not match:
        raise ValueError(f"Invalid SRT timestamp: {value}")
    hours, minutes, seconds, millis = (int(part) for part in match.groups())
    return hours * 3600 + minutes * 60 + seconds + millis / 1000


def parse_srt_text(text: str) -> list[Cue]:
    cues: list[Cue] = []
    blocks = re.split(r"\n\s*\n", text.strip())
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        time_index = next((index for index, line in enumerate(lines) if "-->" in line), None)
        if time_index is None:
            continue
        start_text, end_text = [part.strip().split(" ")[0] for part in lines[time_index].split("-->", 1)]
        start = srt_timestamp_seconds(start_text)
        end = srt_timestamp_seconds(end_text)
        cue_text = " ".join(lines[time_index + 1 :])
        cue_text = re.sub(r"<[^>]+>", "", cue_text).strip()
        if cue_text:
            cues.append(Cue(start=start, end=end, text=cue_text))
    return cues


def analyze_srt(path: Path, *, title: str | None = None) -> dict[str, Any]:
    try:
        cues = parse_srt_text(path.read_text(errors="replace"))
    except Exception as exc:
        return {"status": "malformed", "srt_path": str(path), "error": str(exc)}
    if not cues:
        return {"status": "malformed", "srt_path": str(path), "error": "No parseable cues"}

    full_text = " ".join(cue.text for cue in cues)
    first_15_text = " ".join(cue.text for cue in cues if cue.start < 15)
    tail_start = max(cue.end for cue in cues) - 25
    tail_text = " ".join(cue.text for cue in cues if cue.start >= tail_start)
    title_tokens = set(normalize_tokens(title))
    transcript_tokens = set(normalize_tokens(full_text))
    first_tokens = normalize_tokens(first_15_text)
    title_overlap = (
        len(title_tokens & transcript_tokens) / len(title_tokens)
        if title_tokens
        else None
    )
    specificity_counter = Counter()
    for token in normalize_tokens(full_text):
        if token in SPECIFICITY_TERMS or re.search(r"\d", token):
            specificity_counter[token] += 1
    acronym_count = len(re.findall(r"\b[A-Z]{2,}\b", full_text))
    duration = max(cue.end for cue in cues)
    sentence_count = max(len(re.findall(r"[.!?](?:\s|$)", full_text)), 1)
    return {
        "status": "present",
        "srt_path": str(path),
        "cue_count": len(cues),
        "transcript_duration_seconds": duration,
        "first_spoken_line": cues[0].text,
        "hook_delay_seconds": cues[0].start,
        "first_15s_word_count": len(first_tokens),
        "specificity_hint_count": sum(specificity_counter.values()) + acronym_count,
        "specificity_hints": [item[0] for item in specificity_counter.most_common(8)],
        "title_transcript_overlap": title_overlap,
        "claim_density_per_minute": sentence_count / (duration / 60) if duration else None,
        "closing_cta_presence": any(term in set(normalize_tokens(tail_text)) for term in CTA_TERMS),
    }


def candidate_srt_paths(video: dict[str, Any], *, root: Path = REPO_ROOT) -> list[Path]:
    candidates: list[Path] = []
    seen: set[Path] = set()
    for source in video.get("source_reports") or []:
        source_path = root / source
        for directory in [source_path.parent, source_path.parent.parent]:
            if directory.exists():
                for path in directory.rglob("*.srt"):
                    if path not in seen:
                        candidates.append(path)
                        seen.add(path)
    package = video.get("package")
    if package and package != "unknown":
        package_dir = root / "publications" / package
        if package_dir.exists():
            for path in package_dir.rglob("*.srt"):
                if path not in seen:
                    candidates.append(path)
                    seen.add(path)
    if not candidates:
        for path in (root / "publications").glob("**/*.srt"):
            if path not in seen:
                candidates.append(path)
                seen.add(path)
    return candidates


def score_srt_candidate(video: dict[str, Any], path: Path) -> tuple[int, str]:
    title_tokens = slug_tokens(video.get("title"))
    package_tokens = slug_tokens(video.get("package"))
    path_tokens = slug_tokens(" ".join(path.parts))
    score = 0
    score += len(title_tokens & path_tokens) * 3
    score += len(package_tokens & path_tokens) * 5
    if str(video.get("video_id") or "") in str(path):
        score += 20
    name = path.name.lower()
    if score > 0 and ((video.get("format") == "short" and "auto_captions" in name) or "cinematic" in name):
        score += 2
    confidence = "high" if score >= 12 else "medium" if score >= 5 else "low"
    return score, confidence


def map_srt_for_video(video: dict[str, Any], *, root: Path = REPO_ROOT) -> dict[str, Any]:
    candidates = candidate_srt_paths(video, root=root)
    if not candidates:
        return {"status": "missing", "reason": "No local SRT candidates found"}
    scored = sorted(
        ((score_srt_candidate(video, path), path) for path in candidates),
        key=lambda item: item[0][0],
        reverse=True,
    )
    (score, confidence), best = scored[0]
    if score <= 0:
        return {"status": "missing", "reason": "No plausible local SRT match found"}
    analysis = analyze_srt(best, title=video.get("title"))
    analysis["match_score"] = score
    analysis["match_confidence"] = confidence
    analysis["candidate_count"] = len(candidates)
    return analysis


def build_content_rubric(ledger: dict[str, Any], *, root: Path = REPO_ROOT) -> dict[str, Any]:
    videos = ledger.get("videos") or []
    items = {
        video.get("video_id"): map_srt_for_video(video, root=root)
        for video in videos
        if video.get("video_id")
    }
    status_counts = Counter(item.get("status") or "missing" for item in items.values())
    return {
        "generated_from": "local_srt",
        "video_count": len(items),
        "status_counts": dict(status_counts),
        "items": items,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_content_rubric(load_json(args.ledger))
    write_json(args.output, payload)
    print(f"Wrote content rubric: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
