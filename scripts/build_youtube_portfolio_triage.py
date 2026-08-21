#!/usr/bin/env python3
"""Build deterministic, non-scoring YouTube portfolio triage evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = REPO_ROOT / "experiments" / "youtube-analytics" / "metrics_ledger.json"
DEFAULT_CONTENT = REPO_ROOT / "experiments" / "youtube-analytics" / "content_rubric.json"
DEFAULT_OUTPUT = (
    REPO_ROOT
    / "publication_strategy_and_archive"
    / "portfolio"
    / "youtube_triage.json"
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_title(title: str | None) -> str:
    value = (title or "").lower()
    value = re.sub(r"#\w+", " ", value)
    value = re.sub(
        r"\b(a visual deep research dive|a cinematic research brief|a shallow dive|explainer tl;dr|course tl;dr|tl;dr)\b",
        " ",
        value,
    )
    value = re.sub(r"\b(part|issue|lesson)\s+[ivx0-9]+\b", " ", value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def local_caption_hash(item: dict[str, Any]) -> str | None:
    path_value = item.get("srt_path")
    if not path_value:
        return None
    path = Path(path_value)
    if not path.is_absolute():
        path = REPO_ROOT / path
    if not path.exists() or not path.is_file():
        return None
    return sha256_path(path)


def family_id(video: dict[str, Any]) -> str:
    package = str(video.get("package") or "").strip("/")
    if package:
        return f"package:{package}"
    normalized = normalize_title(video.get("title"))
    return f"title:{normalized or video.get('video_id')}"


def triage_video(video: dict[str, Any], caption: dict[str, Any]) -> dict[str, Any]:
    visibility = str(video.get("privacy_status") or "unknown").lower()
    title = str(video.get("title") or "")
    caption_status = caption.get("status") or "missing"
    caption_confidence = caption.get("match_confidence")
    duration = video.get("duration_seconds")
    flags: list[str] = []
    if visibility != "public":
        flags.append("INVENTORY_ONLY_NON_PUBLIC")
    if not title.strip() or re.search(r"\b(untitled|test|draft)\b", title, re.I):
        flags.append("UNTITLED_TEST_OR_DRAFT_TITLE")
    if video.get("format") in {"short", "tldr"}:
        flags.append("DERIVATIVE_FORMAT")
    if caption_status != "present":
        flags.append("MISSING_CAPTION_EVIDENCE")
    elif caption_confidence not in {"high", None}:
        flags.append("CAPTION_MATCH_REQUIRES_REVIEW")
    if not video.get("description"):
        flags.append("MISSING_DESCRIPTION_IN_LEDGER")
    if not video.get("thumbnail_url") and not video.get("thumbnails"):
        flags.append("MISSING_THUMBNAIL_IN_LEDGER")

    if visibility != "public":
        evidence_state = "INVENTORY_ONLY"
    elif caption_status != "present":
        evidence_state = "INSUFFICIENT_CAPTION_EVIDENCE"
    elif caption_confidence not in {"high", None}:
        evidence_state = "CAPTION_EVIDENCE_UNCERTAIN"
    elif video.get("format") == "short" or (isinstance(duration, (int, float)) and duration < 120):
        evidence_state = "DERIVATIVE_REVIEW_ONLY"
    else:
        evidence_state = "ELIGIBLE_FOR_DEEP_REVIEW"

    return {
        "video_id": video.get("video_id"),
        "title": title,
        "normalized_title": normalize_title(title),
        "url": video.get("url"),
        "current_visibility": visibility,
        "format": video.get("format"),
        "duration_seconds": duration,
        "published_at": video.get("published_at"),
        "family_id": family_id(video),
        "package": video.get("package"),
        "related_video": video.get("related_video"),
        "playlists": video.get("playlists") or [],
        "description_present": bool(video.get("description")),
        "thumbnail_present": bool(video.get("thumbnail_url") or video.get("thumbnails")),
        "caption": {
            "status": caption_status,
            "match_confidence": caption_confidence,
            "srt_path": caption.get("srt_path"),
            "sha256": local_caption_hash(caption),
            "cue_count": caption.get("cue_count"),
            "transcript_duration_seconds": caption.get("transcript_duration_seconds"),
        },
        "evidence_state": evidence_state,
        "triage_flags": flags,
        "metrics": video.get("analytics_windows") or {},
    }


def build_triage(ledger: dict[str, Any], content: dict[str, Any]) -> dict[str, Any]:
    captions = content.get("items") or {}
    items = [
        triage_video(video, captions.get(video.get("video_id"), {}))
        for video in ledger.get("videos") or []
        if video.get("video_id")
    ]
    items.sort(key=lambda item: item["video_id"])

    normalized_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    caption_hash_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    family_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        normalized_groups[item["normalized_title"]].append(item)
        caption_hash = item["caption"].get("sha256")
        if caption_hash:
            caption_hash_groups[caption_hash].append(item)
        family_groups[item["family_id"]].append(item)

    duplicate_title_groups = [
        {
            "normalized_title": normalized,
            "video_ids": [item["video_id"] for item in group],
            "titles": sorted({item["title"] for item in group}),
            "requires_manual_representative": True,
        }
        for normalized, group in sorted(normalized_groups.items())
        if normalized and len(group) > 1
    ]
    shared_caption_groups = [
        {
            "caption_sha256": digest,
            "video_ids": [item["video_id"] for item in group],
            "match_confidences": [item["caption"].get("match_confidence") for item in group],
            "warning": (
                "Shared local transcript evidence may indicate a duplicate or an "
                "ambiguous heuristic match; it never authorizes unlisting by itself."
            ),
        }
        for digest, group in sorted(caption_hash_groups.items())
        if len(group) > 1
    ]
    families = [
        {
            "family_id": key,
            "video_ids": [item["video_id"] for item in group],
            "public_video_ids": [
                item["video_id"] for item in group if item["current_visibility"] == "public"
            ],
            "formats": sorted({str(item.get("format") or "unknown") for item in group}),
        }
        for key, group in sorted(family_groups.items())
    ]

    return {
        "schema_version": 1,
        "created_at": utc_now(),
        "decision_method": "deterministic_non_scoring_triage",
        "selection_rule": (
            "Triage flags organize evidence only. Selection and visibility decisions "
            "require concrete anchors and stated confidence; uncertainty defaults to KEEP_PUBLIC."
        ),
        "channel": ledger.get("channel"),
        "youtube_snapshot_timestamp": ledger.get("created_at"),
        "video_count": len(items),
        "visibility_counts": dict(Counter(item["current_visibility"] for item in items)),
        "format_counts": dict(Counter(str(item.get("format") or "unknown") for item in items)),
        "evidence_state_counts": dict(Counter(item["evidence_state"] for item in items)),
        "duplicate_title_groups": duplicate_title_groups,
        "shared_caption_groups": shared_caption_groups,
        "families": families,
        "items": items,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--content", type=Path, default=DEFAULT_CONTENT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    content = json.loads(args.content.read_text(encoding="utf-8"))
    payload = build_triage(ledger, content)
    payload["sources"] = {
        "ledger": {"path": str(args.ledger), "sha256": sha256_path(args.ledger)},
        "content": {"path": str(args.content), "sha256": sha256_path(args.content)},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(payload['items'])} YouTube triage records to {args.output}")


if __name__ == "__main__":
    main()
