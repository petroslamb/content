#!/usr/bin/env python3
"""Prepare overlay-remaster Shorts manifests and a crosswalk report."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any


DEFAULT_PACKAGES = ["action", "memory", "multi-agent", "reasoning"]
DEFAULT_PUBLISH_TIMES = ["06:00:00", "07:30:00"]
DEFAULT_CTA = "Full cinematic brief in Related Video"
DEFAULT_PLAYLIST_ID = "PL8lPx5mgRhhbMQQ70d-C4dAKKKPzCd5Hd"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")


def parse_date(value: str | None) -> date:
    if value:
        return date.fromisoformat(value)
    return datetime.now(timezone.utc).date() + timedelta(days=1)


def publish_at_for(index: int, start_date: date) -> str:
    day = start_date + timedelta(days=index // len(DEFAULT_PUBLISH_TIMES))
    clock = time.fromisoformat(DEFAULT_PUBLISH_TIMES[index % len(DEFAULT_PUBLISH_TIMES)])
    return datetime.combine(day, clock, tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


def candidate_srts(video_dir: Path, package_key: str) -> list[Path]:
    preferred = [
        video_dir / f"operating_agents_{package_key.replace('-', '_')}_cinematic.srt",
        video_dir / f"{package_key}_auto_captions.srt",
    ]
    return [path for path in preferred if path.exists()] + sorted(video_dir.glob("*.srt"))


def upload_items_by_slug(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    items: dict[str, dict[str, Any]] = {}
    for item in report.get("items", []):
        path = Path(item.get("video_path") or item.get("portrait_file") or "")
        stem = path.stem.removesuffix("_portrait")
        slug = stem.split("-", 1)[1] if "-" in stem else stem
        if slug:
            items[slug] = item
    return items


def build_package_remaster(
    *,
    repo_root: Path,
    package_key: str,
    run_id: str,
    start_date: date,
    global_offset: int,
    clips_per_package: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    rollout_dir = (
        repo_root
        / "publications"
        / "autonomous-agents"
        / "essays"
        / package_key
        / "artifacts"
        / "video"
        / "daily-cinematic-rollout"
    )
    video_dir = rollout_dir.parent
    source_manifest_path = rollout_dir / "shorts_manifest.json"
    upload_report_path = rollout_dir / "shorts_upload_report.json"
    source_manifest = load_json(source_manifest_path)
    upload_report = load_json(upload_report_path)
    source_video = repo_root / source_manifest["source_video"]
    srt_candidates = candidate_srts(video_dir, package_key)
    source_srt = srt_candidates[0] if srt_candidates else None

    if not source_video.exists():
        raise FileNotFoundError(f"Missing source video for {package_key}: {source_video}")
    if not source_srt:
        raise FileNotFoundError(f"Missing SRT for {package_key} in {video_dir}")

    uploaded = upload_items_by_slug(upload_report)
    clips = deepcopy(source_manifest.get("clips", [])[:clips_per_package])
    if len(clips) != clips_per_package:
        raise RuntimeError(f"{package_key} has {len(clips)} clips, expected {clips_per_package}")

    remaster_dir = rollout_dir / run_id
    remaster_manifest_path = remaster_dir / "shorts_manifest.json"
    crosswalk_items: list[dict[str, Any]] = []
    for clip_index, clip in enumerate(clips):
        slug = clip["slug"]
        old_item = uploaded.get(slug)
        if not old_item:
            raise RuntimeError(f"Missing uploaded old Short for {package_key}/{slug}")
        publish_at = publish_at_for(global_offset + clip_index, start_date)
        clip["publish_at"] = publish_at
        clip.setdefault("hook", clip["title"])
        clip.setdefault("cta", DEFAULT_CTA)
        crosswalk_items.append(
            {
                "package": f"autonomous-agents/essays/{package_key}",
                "package_key": package_key,
                "slug": slug,
                "title": clip["title"],
                "publish_at": publish_at,
                "source_manifest": str(source_manifest_path.relative_to(repo_root)),
                "remaster_manifest": str(remaster_manifest_path.relative_to(repo_root)),
                "source_video": str(source_video.relative_to(repo_root)),
                "source_srt": str(source_srt.relative_to(repo_root)),
                "old_video_id": old_item.get("video_id"),
                "old_url": old_item.get("url"),
                "old_video_path": old_item.get("video_path"),
                "new_video_id": None,
                "new_url": None,
                "new_video_path": str((remaster_dir / "portrait" / f"{clip_index + 1:02d}-{slug}_portrait.mp4").relative_to(repo_root)),
                "new_upload_report": str((remaster_dir / "shorts_upload_report.json").relative_to(repo_root)),
                "old_status_target": "unlisted",
                "studio_related_verified": False,
                "ready_to_unlist_old": False,
            }
        )

    remaster_manifest = {
        "source_video": str(source_video.relative_to(repo_root)),
        "source_srt": str(source_srt.relative_to(repo_root)),
        "playlist_id": source_manifest.get("playlist_id") or upload_report.get("playlist_id") or DEFAULT_PLAYLIST_ID,
        "related_video_id": source_manifest.get("related_video_id") or upload_report.get("related_video", {}).get("id"),
        "full_video_url": source_manifest.get("full_video_url") or upload_report.get("related_video", {}).get("url"),
        "essay_url": source_manifest.get("essay_url"),
        "secondary_video_url": source_manifest.get("secondary_video_url"),
        "overlay": {
            "enabled": True,
            "source": "cinematic_srt",
            "source_srt": str(source_srt.relative_to(repo_root)),
            "render_strategy": "top_hook_spoken_subtitles_bottom_cta",
            "default_cta": DEFAULT_CTA,
            "caption_wrap_width": 30,
            "hook_max_words": 9,
            "quality_check": {
                "sample_frames_per_short": 3,
                "require_top_hook": True,
                "require_spoken_subtitles": True,
                "require_bottom_cta": True,
            },
        },
        "clips": clips,
    }
    write_json(remaster_manifest_path, remaster_manifest)
    return remaster_manifest, crosswalk_items


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare an overlay-remaster backfill pilot.")
    parser.add_argument("--run-id", default="remastered-overlays-2026-04-28")
    parser.add_argument("--start-date", help="First UTC publish date, YYYY-MM-DD. Defaults to tomorrow UTC.")
    parser.add_argument("--clips-per-package", type=int, default=2)
    parser.add_argument(
        "--package",
        dest="packages",
        action="append",
        choices=DEFAULT_PACKAGES,
        help="Operating Agents essay package key. Repeat to override the default pilot set.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("experiments/youtube-cinematic-rollout/overlay_remaster_backfill_pilot.json"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = Path.cwd()
    packages = args.packages or DEFAULT_PACKAGES
    start_date = parse_date(args.start_date)
    crosswalk: list[dict[str, Any]] = []
    manifests: list[dict[str, Any]] = []

    for package_index, package_key in enumerate(packages):
        manifest, items = build_package_remaster(
            repo_root=repo_root,
            package_key=package_key,
            run_id=args.run_id,
            start_date=start_date,
            global_offset=package_index * args.clips_per_package,
            clips_per_package=args.clips_per_package,
        )
        manifests.append(
            {
                "package_key": package_key,
                "manifest": str(
                    (
                        repo_root
                        / "publications"
                        / "autonomous-agents"
                        / "essays"
                        / package_key
                        / "artifacts"
                        / "video"
                        / "daily-cinematic-rollout"
                        / args.run_id
                        / "shorts_manifest.json"
                    ).relative_to(repo_root)
                ),
                "clip_count": len(manifest["clips"]),
                "source_srt": manifest["source_srt"],
            }
        )
        crosswalk.extend(items)

    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "workflow": "overlay_remaster_backfill_pilot",
        "run_id": args.run_id,
        "publish_start_date": start_date.isoformat(),
        "publish_cadence": "2 per UTC day at 06:00 and 07:30",
        "old_status_target": "unlisted",
        "default_cta": DEFAULT_CTA,
        "packages": manifests,
        "items": crosswalk,
    }
    write_json(args.report, report)
    print(json.dumps({"report": str(args.report), "item_count": len(crosswalk), "packages": manifests}, indent=2))


if __name__ == "__main__":
    main()
