#!/usr/bin/env python3
"""Sync overlay-remaster crosswalk items from generated upload reports."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n")


def upload_by_video_path(report_path: Path) -> dict[str, dict[str, Any]]:
    if not report_path.exists():
        return {}
    report = load_json(report_path)
    return {item.get("video_path", ""): item for item in report.get("items", [])}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync overlay remaster upload IDs into the crosswalk.")
    parser.add_argument("--crosswalk", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    crosswalk = load_json(args.crosswalk)
    repo_root = Path.cwd()
    uploads_cache: dict[str, dict[str, dict[str, Any]]] = {}
    synced = 0
    missing: list[dict[str, str]] = []

    for item in crosswalk.get("items", []):
        report_path = repo_root / item["new_upload_report"]
        cache_key = str(report_path)
        if cache_key not in uploads_cache:
            uploads_cache[cache_key] = upload_by_video_path(report_path)
        upload = uploads_cache[cache_key].get(item["new_video_path"])
        if not upload:
            missing.append({"package_key": item["package_key"], "slug": item["slug"]})
            continue
        item["new_video_id"] = upload.get("video_id")
        item["new_url"] = upload.get("url")
        item["new_youtube_readback"] = upload.get("youtube_readback")
        item["new_playlist_readback"] = upload.get("playlist_readback")
        item["ready_to_unlist_old"] = bool(
            item.get("new_video_id")
            and item.get("new_youtube_readback", {}).get("upload_status") in {"uploaded", "processed"}
            and item.get("new_youtube_readback", {}).get("privacy_status") == "public"
            and item.get("studio_related_verified")
        )
        synced += 1

    crosswalk["updated_at"] = datetime.now(timezone.utc).isoformat()
    crosswalk["uploaded_count"] = synced
    crosswalk["missing_uploads"] = missing
    write_json(args.crosswalk, crosswalk)
    print(json.dumps({"crosswalk": str(args.crosswalk), "synced": synced, "missing": missing}, indent=2))


if __name__ == "__main__":
    main()
