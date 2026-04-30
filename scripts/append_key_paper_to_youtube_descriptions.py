#!/usr/bin/env python3
"""Append one curated key-paper line to selected YouTube video descriptions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
YOUTUBE_SKILL_SCRIPTS = REPO_ROOT / "workflows" / "skills" / "youtube-data-api" / "scripts"
if str(YOUTUBE_SKILL_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(YOUTUBE_SKILL_SCRIPTS))

from youtube_common import build_youtube, get_video_details  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append a curated key-paper line to selected YouTube video descriptions."
    )
    parser.add_argument("--manifest", type=Path, required=True, help="YAML manifest listing target videos and append lines.")
    parser.add_argument("--report-file", type=Path, help="Optional JSON report output path.")
    parser.add_argument("--apply", action="store_true", help="Write updated descriptions. Without this flag, print the plan only.")
    return parser.parse_args()


def load_manifest(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def render_new_description(existing: str, append_line: str) -> tuple[str, bool]:
    base = existing.rstrip()
    if append_line in base.splitlines():
        return base, False
    separator = "\n\n" if base else ""
    return f"{base}{separator}{append_line}", True


def update_video_description(youtube: Any, video_id: str, description_text: str) -> None:
    video = get_video_details(youtube, video_id)
    if not video:
        raise RuntimeError(f"Video {video_id} not found")

    snippet = video["snippet"]
    payload = {
        "title": snippet["title"],
        "description": description_text,
        "categoryId": snippet.get("categoryId", "22"),
    }
    if "defaultLanguage" in snippet:
        payload["defaultLanguage"] = snippet["defaultLanguage"]
    if "tags" in snippet:
        payload["tags"] = snippet["tags"]

    youtube.videos().update(
        part="snippet",
        body={"id": video_id, "snippet": payload},
    ).execute()


def main() -> None:
    args = parse_args()
    manifest = load_manifest(args.manifest)
    targets = manifest.get("targets", [])
    youtube = build_youtube()
    results: list[dict[str, Any]] = []

    for target in targets:
        video_id = target["video_id"]
        append_line = target["append_line"].strip()
        details = get_video_details(youtube, video_id)
        if not details:
            results.append({"key": target["key"], "video_id": video_id, "status": "missing"})
            continue

        snippet = details["snippet"]
        existing = snippet.get("description", "")
        new_description, changed = render_new_description(existing, append_line)
        result = {
            "key": target["key"],
            "variant": target.get("variant"),
            "video_id": video_id,
            "title": snippet.get("title"),
            "privacy_status": details.get("status", {}).get("privacyStatus"),
            "append_line": append_line,
            "changed": changed,
            "applied": bool(args.apply and changed),
        }
        if args.apply and changed:
            update_video_description(youtube, video_id, new_description)
            refreshed = get_video_details(youtube, video_id)
            refreshed_description = refreshed["snippet"].get("description", "")
            result["verified"] = append_line in refreshed_description.splitlines()
            result["description_length"] = len(refreshed_description)
        else:
            result["verified"] = append_line in new_description.splitlines()
            result["description_length"] = len(new_description)
        results.append(result)

    payload = {
        "manifest": str(args.manifest),
        "applied": args.apply,
        "target_count": len(targets),
        "results": results,
    }
    if args.report_file:
        args.report_file.parent.mkdir(parents=True, exist_ok=True)
        args.report_file.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
