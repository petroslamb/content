#!/usr/bin/env python3
"""Unlist old Shorts after verified overlay remaster uploads."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


sys.path.insert(0, str(Path(__file__).parent.parent / "workflows" / "skills" / "youtube-data-api" / "scripts"))

try:
    from youtube_common import build_youtube, get_video_details
except ImportError:
    print("ERROR: Could not import YouTube helpers. Run from the repo root with dependencies installed.")
    sys.exit(1)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")


def upload_items_for_report(report_path: Path) -> dict[str, dict[str, Any]]:
    if not report_path.exists():
        return {}
    report = load_json(report_path)
    return {item.get("video_path", ""): item for item in report.get("items", [])}


def eligible_items(repo_root: Path, crosswalk: dict[str, Any], *, require_studio_verified: bool) -> list[dict[str, Any]]:
    uploads_cache: dict[str, dict[str, dict[str, Any]]] = {}
    eligible: list[dict[str, Any]] = []
    for item in crosswalk.get("items", []):
        report_path = repo_root / item["new_upload_report"]
        cache_key = str(report_path)
        if cache_key not in uploads_cache:
            uploads_cache[cache_key] = upload_items_for_report(report_path)
        upload = uploads_cache[cache_key].get(item["new_video_path"])
        if not upload:
            continue
        if require_studio_verified and not item.get("studio_related_verified"):
            continue
        readback = upload.get("youtube_readback", {})
        if readback.get("upload_status") not in {"uploaded", "processed"}:
            continue
        if readback.get("privacy_status") != "public":
            continue
        if item.get("old_status_target") != "unlisted":
            continue
        eligible.append({**item, "new_video_id": upload["video_id"], "new_url": upload.get("url")})
    return eligible


def set_video_unlisted(youtube: Any, video_id: str) -> dict[str, Any]:
    current = get_video_details(youtube, video_id, part="snippet,status,localizations")
    if not current:
        raise RuntimeError(f"Video not found: {video_id}")
    status = dict(current.get("status", {}))
    status["privacyStatus"] = "unlisted"
    status["selfDeclaredMadeForKids"] = status.get("selfDeclaredMadeForKids", False)
    youtube.videos().update(part="status", body={"id": video_id, "status": status}).execute()
    readback = get_video_details(youtube, video_id, part="snippet,status")
    return {
        "video_id": video_id,
        "previous_privacy_status": current.get("status", {}).get("privacyStatus"),
        "new_privacy_status": readback.get("status", {}).get("privacyStatus") if readback else None,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Unlist old Shorts after overlay remaster verification.")
    parser.add_argument("--crosswalk", type=Path, required=True)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("experiments/youtube-cinematic-rollout/overlay_remaster_unlist_report.json"),
    )
    parser.add_argument("--skip-studio-verification-gate", action="store_true")
    parser.add_argument("--apply", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = Path.cwd()
    crosswalk = load_json(args.crosswalk)
    items = eligible_items(
        repo_root,
        crosswalk,
        require_studio_verified=not args.skip_studio_verification_gate,
    )
    plan = [
        {
            "package_key": item["package_key"],
            "slug": item["slug"],
            "old_video_id": item["old_video_id"],
            "old_url": item["old_url"],
            "new_video_id": item["new_video_id"],
            "new_url": item["new_url"],
            "target_status": "unlisted",
        }
        for item in items
    ]
    print(json.dumps({"planned_count": len(plan), "items": plan}, indent=2))
    if not args.apply:
        print("Dry run only. Add --apply to unlist old videos.")
        return
    if not plan:
        raise SystemExit("No eligible old Shorts to unlist.")

    youtube = build_youtube()
    results = []
    for item in plan:
        results.append({**item, **set_video_unlisted(youtube, item["old_video_id"])})
    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "workflow": "overlay_remaster_old_shorts_unlist",
        "crosswalk": str(args.crosswalk),
        "updated_count": len(results),
        "items": results,
    }
    write_json(args.report, report)
    print(f"Unlist report written to: {args.report}")


if __name__ == "__main__":
    main()
