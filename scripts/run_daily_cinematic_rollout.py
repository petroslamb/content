#!/usr/bin/env python3
"""Manage the evergreen cinematic rollout backlog, scheduling, and run ledger."""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync the evergreen cinematic rollout backlog and scheduling state.")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("experiments/youtube-cinematic-rollout/backlog_manifest.yaml"),
        help="Backlog manifest YAML. Defaults to experiments/youtube-cinematic-rollout/backlog_manifest.yaml",
    )
    parser.add_argument(
        "--ledger",
        type=Path,
        help="Optional release-ledger override. Defaults to the path named in the manifest.",
    )
    parser.add_argument("--apply", action="store_true", help="Write manifest and ledger updates. Without this, print the plan only.")
    return parser.parse_args()


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def load_existing_cinematic_assets(path: Path) -> tuple[set[str], dict[str, dict[str, Any]]]:
    data = load_yaml(path)
    completed = {
        str(item["package"]).replace("publications/", "").rstrip("/")
        for item in data.get("assets", [])
        if item.get("asset_kind") == "cinematic"
    }
    pending = {
        str(item["package"]).replace("publications/", "").rstrip("/"): item
        for item in data.get("pending_assets", [])
        if item.get("asset_kind") == "cinematic"
    }
    return completed, pending


@dataclass
class DiscoveredPublication:
    package: str
    status_path: str
    markdown_path: str | None
    notebook_id: str
    notebook_title: str | None
    essay_url: str | None
    notebook_source_status: str | None = None


def derive_essay_url(config: dict[str, Any]) -> str | None:
    substack_url = config.get("substack_url")
    substack_slug = config.get("substack_slug")
    if not substack_url or not substack_slug:
        return None
    return f"{str(substack_url).rstrip('/')}/p/{substack_slug}"


def discover_publications() -> list[DiscoveredPublication]:
    results: list[DiscoveredPublication] = []
    seen_packages: set[str] = set()
    for status_path in sorted(Path("publications").glob("**/status.yaml")):
        data = load_yaml(status_path)
        config = data.get("config") or {}
        stages = data.get("stages") or {}
        if not stages.get("substack_publishing", {}).get("done"):
            continue
        notebook_id = config.get("notebooklm_notebook_id")
        if not notebook_id:
            continue

        kind = data.get("kind")
        package_path = status_path.parent.relative_to(Path.cwd() / "publications" if status_path.is_absolute() else Path("publications")).as_posix()
        effective_status_path = status_path
        notebook_source_status = None
        markdown_path = config.get("markdown_path")
        if kind == "umbrella" and config.get("default_leaf_package"):
            package_path = str(config["default_leaf_package"])
            notebook_source_status = status_path.as_posix()
            leaf_status_path = Path("publications") / package_path / "status.yaml"
            if leaf_status_path.exists():
                effective_status_path = leaf_status_path

        if package_path in seen_packages:
            continue
        seen_packages.add(package_path)
        results.append(
            DiscoveredPublication(
                package=package_path,
                status_path=effective_status_path.as_posix(),
                markdown_path=str(markdown_path) if markdown_path else None,
                notebook_id=str(notebook_id),
                notebook_title=str(config.get("notebooklm_notebook_title")) if config.get("notebooklm_notebook_title") else None,
                essay_url=derive_essay_url(config),
                notebook_source_status=notebook_source_status,
            )
        )
    return results


def slug_key(package: str) -> str:
    return package.replace("/", "_").replace("-", "_")


def humanize_title(value: str) -> str:
    return " ".join(part.capitalize() for part in value.replace("-", " ").replace("_", " ").split())


def read_markdown_title(markdown_path: str | None) -> str | None:
    if not markdown_path:
        return None
    path = Path(markdown_path)
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def default_cinematic_copy(title_hint: str) -> tuple[str, str, str]:
    title = title_hint
    hook = f"This cinematic brief introduces the main structural claim behind {title_hint} without forcing viewers to know the essay first."
    summary = (
        f"This cinematic brief is the discovery surface for {title_hint}.\n\n"
        "Use it to land the core causal move quickly, then point viewers toward the full research breakdown."
    )
    return title, hook, summary


def relative_video_root(package: str) -> Path:
    return Path("publications") / package / "artifacts" / "video"


def build_auto_entry(discovered: DiscoveredPublication, pending_reason: str | None) -> dict[str, Any]:
    markdown_title = read_markdown_title(discovered.markdown_path) or humanize_title(Path(discovered.package).name)
    title, hook, summary = default_cinematic_copy(markdown_title)
    video_root = relative_video_root(discovered.package)
    stem = discovered.package.replace("/", "_").replace("-", "_")
    state = "blocked_rate_limited" if pending_reason else "queued"
    return {
        "package": discovered.package,
        "status_path": discovered.status_path,
        **({"notebook_source_status": discovered.notebook_source_status} if discovered.notebook_source_status else {}),
        "markdown_path": discovered.markdown_path,
        "notebook_id": discovered.notebook_id,
        "notebook_title": discovered.notebook_title,
        "essay_url": discovered.essay_url,
        "secondary_link": {
            "kind": "essay",
            "label": "Full research breakdown",
            "video_id": None,
            "url": discovered.essay_url,
        },
        "cinematic": {
            "title": title,
            "hook": hook,
            "summary": summary,
            "video_file": str(video_root / f"{stem}_cinematic.mp4"),
            "output_srt": str(video_root / f"{stem}_cinematic.srt"),
            "upload_report": str(video_root / f"{stem}_cinematic_upload_report.json"),
            "youtube_video_id": None,
            "youtube_url": None,
            "published_at": None,
            "state": state,
            "retry_state": {
                "attempts": 0 if not pending_reason else 1,
                "last_attempted_at": None,
                "last_error": pending_reason,
            },
        },
        "shorts": {
            "workspace_dir": str(video_root / "daily-cinematic-rollout"),
            "candidate_report": str(video_root / "daily-cinematic-rollout" / "candidate_report.json"),
            "manifest_path": str(video_root / "daily-cinematic-rollout" / "shorts_manifest.json"),
            "upload_report": str(video_root / "daily-cinematic-rollout" / "shorts_upload_report.json"),
            "state": "pending_cinematic",
            "approved_clips": [],
            "reserve_clips": [],
            "rejected_clips": [],
            "next_publish_at": None,
            "last_scheduled_at": None,
        },
    }


def sync_discovery(manifest: dict[str, Any]) -> list[str]:
    experiment = manifest["experiment"]
    completed, pending = load_existing_cinematic_assets(Path(experiment["existing_video_map"]))
    publications = manifest.setdefault("publications", {})
    rollout_order = manifest.setdefault("rollout_order", [])
    existing_packages = {entry["package"] for entry in publications.values()}
    added_keys: list[str] = []
    for discovered in discover_publications():
        if discovered.package in completed or discovered.package in existing_packages:
            continue
        key = slug_key(discovered.package)
        pending_reason = pending.get(discovered.package, {}).get("reason")
        publications[key] = build_auto_entry(discovered, pending_reason)
        rollout_order.append(key)
        added_keys.append(key)
        existing_packages.add(discovered.package)
    return added_keys


def run_notebooklm_auth_check() -> tuple[bool, str]:
    result = subprocess.run(
        [".venv/bin/notebooklm", "auth", "check", "--test"],
        capture_output=True,
        text=True,
        check=False,
    )
    output = "\n".join(part for part in (result.stdout.strip(), result.stderr.strip()) if part).strip()
    ok = result.returncode == 0
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    if ok:
        for line in reversed(lines):
            if "valid" in line.lower() or "pass" in line.lower():
                return ok, line
        return ok, "Authentication check passed."
    condensed = " | ".join(lines[-5:]) if lines else "NotebookLM authentication check failed."
    return ok, condensed


def parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def classify_entry(entry: dict[str, Any]) -> None:
    cinematic = entry.get("cinematic", {})
    shorts = entry.get("shorts", {})
    state = cinematic.get("state", "queued")
    output_srt = Path(cinematic.get("output_srt", ""))
    manifest_path = Path(shorts.get("manifest_path", ""))
    upload_report = Path(shorts.get("upload_report", ""))
    workspace_dir = Path(shorts.get("workspace_dir", ""))
    portrait_dir = workspace_dir / "portrait"
    approved = shorts.get("approved_clips", []) or []

    if state == "no_shorts_approved":
        shorts["state"] = "no_shorts_approved"
        return

    if cinematic.get("generation_task_id") and not cinematic.get("youtube_video_id"):
        cinematic["state"] = "generation_pending"
        shorts["state"] = "pending_cinematic"
        return

    if cinematic.get("youtube_video_id"):
        if not output_srt.exists():
            cinematic["state"] = "captions_pending"
            shorts["state"] = "pending_captions"
        elif not approved:
            cinematic["state"] = "shorts_selection_pending"
            shorts["state"] = "selection_pending"
        elif manifest_path.exists() and upload_report.exists():
            cinematic["state"] = "completed"
            shorts["state"] = "completed"
        elif manifest_path.exists() and any(portrait_dir.glob("*.mp4")):
            cinematic["state"] = "shorts_upload_pending"
            shorts["state"] = "upload_pending"
        elif manifest_path.exists():
            cinematic["state"] = "shorts_render_pending"
            shorts["state"] = "render_pending"
        else:
            cinematic["state"] = "shorts_schedule_pending"
            shorts["state"] = "schedule_pending"
        return

    if state not in {"blocked_rate_limited", "blocked_auth_expired", "retryable_error"}:
        cinematic["state"] = "queued"


def generation_candidate_keys(manifest: dict[str, Any]) -> list[str]:
    states = set(manifest["experiment"]["states"]["generation_blocking"])
    keys: list[str] = []
    for key in manifest.get("rollout_order", []):
        state = manifest["publications"][key]["cinematic"].get("state")
        if state in states:
            keys.append(key)
    return keys


def in_flight_keys(manifest: dict[str, Any]) -> list[str]:
    states = set(manifest["experiment"]["states"]["in_flight"])
    keys: list[str] = []
    for key in manifest.get("rollout_order", []):
        state = manifest["publications"][key]["cinematic"].get("state")
        if state in states:
            keys.append(key)
    return keys


def render_publish_at(date_value: datetime, slot: str, tz_name: str) -> str:
    tz = ZoneInfo(tz_name)
    hours, minutes = [int(part) for part in slot.split(":")]
    local_dt = datetime(date_value.year, date_value.month, date_value.day, hours, minutes, tzinfo=tz)
    return local_dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def schedule_approved_clips(manifest: dict[str, Any]) -> int:
    defaults = manifest["experiment"]["defaults"]
    slot_times = defaults["shorts_slot_times"]
    tz_name = defaults["timezone"]
    not_before_date = defaults.get("shorts_not_before_date")
    min_start_day = None
    if not_before_date:
        min_start_day = datetime.fromisoformat(str(not_before_date)).date()
    publications = manifest["publications"]
    rollout_order = manifest["rollout_order"]
    changed = 0

    daily_clip_map: dict[datetime, list[tuple[str, int]]] = {}
    for key in rollout_order:
        entry = publications[key]
        approved = entry.get("shorts", {}).get("approved_clips", []) or []
        published_at = parse_iso(entry.get("cinematic", {}).get("published_at"))
        if not approved or not published_at:
            continue
        start_day = published_at.astimezone(ZoneInfo(tz_name)).date() + timedelta(days=1)
        if min_start_day and start_day < min_start_day:
            start_day = min_start_day
        for clip_index, clip in enumerate(approved):
            if clip.get("publish_at"):
                continue
            clip_day = datetime.combine(start_day + timedelta(days=clip_index), datetime.min.time())
            daily_clip_map.setdefault(clip_day, []).append((key, clip_index))

    for clip_day in sorted(daily_clip_map):
        clips_for_day = sorted(
            daily_clip_map[clip_day],
            key=lambda item: manifest["rollout_order"].index(item[0]),
        )
        for slot_index, (key, clip_index) in enumerate(clips_for_day):
            if slot_index >= len(slot_times):
                break
            entry = publications[key]
            clip = entry["shorts"]["approved_clips"][clip_index]
            clip["publish_at"] = render_publish_at(clip_day, slot_times[slot_index], tz_name)
            entry["shorts"]["last_scheduled_at"] = now_utc().isoformat()
            changed += 1

    for key in rollout_order:
        approved = publications[key].get("shorts", {}).get("approved_clips", []) or []
        future_times = [clip.get("publish_at") for clip in approved if clip.get("publish_at")]
        publications[key]["shorts"]["next_publish_at"] = min(future_times) if future_times else None
    return changed


def shorts_manifest_clip_payload(clip: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "slug": clip["slug"],
        "title": clip["title"],
        "summary": clip.get("summary", ""),
        "start": clip["start"],
        "end": clip["end"],
        "publish_at": clip.get("publish_at"),
        "score_total": clip.get("total_score"),
        "score_breakdown": clip.get("score_breakdown"),
    }
    hook = clip.get("hook") or clip.get("top_hook")
    if hook:
        payload["hook"] = hook
    if clip.get("cta"):
        payload["cta"] = clip["cta"]
    return payload


def shorts_overlay_payload(manifest: dict[str, Any], cinematic: dict[str, Any]) -> dict[str, Any] | None:
    defaults = manifest["experiment"].get("defaults", {})
    overlay = defaults.get("shorts_overlay") or {}
    if not overlay.get("enabled", False):
        return None
    return {
        "enabled": True,
        "source": overlay.get("source", "cinematic_srt"),
        "source_srt": cinematic.get("output_srt"),
        "render_strategy": overlay.get("render_strategy", "top_hook_spoken_subtitles_bottom_cta"),
        "default_cta": overlay.get("default_cta", "Full cinematic brief in Related Video"),
        "caption_wrap_width": int(overlay.get("caption_wrap_width", 30)),
        "hook_max_words": int(overlay.get("hook_max_words", 9)),
        "quality_check": overlay.get("quality_check", {}),
    }


def materialize_shorts_manifests(manifest: dict[str, Any]) -> list[str]:
    publications = manifest["publications"]
    changed_paths: list[str] = []
    for key, entry in publications.items():
        approved = entry.get("shorts", {}).get("approved_clips", []) or []
        if not approved:
            continue
        cinematic = entry.get("cinematic", {})
        if not cinematic.get("youtube_video_id") or not cinematic.get("youtube_url"):
            continue
        manifest_path = Path(entry["shorts"]["manifest_path"])
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        overlay = shorts_overlay_payload(manifest, cinematic)
        payload = {
            "source_video": cinematic["video_file"],
            "source_srt": cinematic.get("output_srt"),
            "related_video_id": cinematic["youtube_video_id"],
            "essay_url": entry.get("essay_url"),
            "full_video_url": cinematic["youtube_url"],
            "secondary_video_url": entry.get("secondary_link", {}).get("url"),
            "playlist_id": manifest["experiment"]["playlists"]["shorts"]["id"],
            "clips": [shorts_manifest_clip_payload(clip) for clip in approved],
        }
        if overlay:
            payload["overlay"] = overlay
        new_text = json.dumps(payload, indent=2) + "\n"
        current_text = manifest_path.read_text(encoding="utf-8") if manifest_path.exists() else None
        if current_text != new_text:
            manifest_path.write_text(new_text, encoding="utf-8")
            changed_paths.append(str(manifest_path))
    return changed_paths


def append_ledger(ledger_path: Path, summary: dict[str, Any]) -> None:
    lines = [
        "",
        f"### {summary['run_started']}",
        "",
        f"- NotebookLM auth: `{summary['notebooklm_auth']}`",
    ]
    if summary.get("auth_message"):
        lines.append(f"- Auth detail: `{summary['auth_message']}`")
    if summary.get("added_keys"):
        lines.append(f"- Added backlog entries: {', '.join(f'`{key}`' for key in summary['added_keys'])}")
    if summary.get("in_flight"):
        lines.append(f"- In-flight first: {', '.join(f'`{key}`' for key in summary['in_flight'])}")
    if summary.get("next_new"):
        lines.append(f"- Next generation candidates: {', '.join(f'`{key}`' for key in summary['next_new'])}")
    if summary.get("manifest_paths"):
        lines.append(f"- Materialized Shorts manifests: {', '.join(f'`{path}`' for path in summary['manifest_paths'])}")
    if summary.get("scheduled_clip_count"):
        lines.append(f"- Newly scheduled approved clips: `{summary['scheduled_clip_count']}`")
    if summary.get("blocked_auth_key"):
        lines.append(f"- Hard auth gate: backlog stays pinned at `{summary['blocked_auth_key']}` until `.venv/bin/notebooklm login` succeeds.")
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def main() -> None:
    args = parse_args()
    manifest = load_yaml(args.manifest)
    added_keys = sync_discovery(manifest)
    for entry in manifest.get("publications", {}).values():
        classify_entry(entry)
    auth_ok, auth_message = run_notebooklm_auth_check()
    generation_keys = generation_candidate_keys(manifest)
    blocked_auth_key = generation_keys[0] if (not auth_ok and generation_keys) else None
    if blocked_auth_key:
        blocked_entry = manifest["publications"][blocked_auth_key]
        blocked_entry["cinematic"]["state"] = "blocked_auth_expired"
        retry_state = blocked_entry["cinematic"].setdefault("retry_state", {})
        retry_state["last_attempted_at"] = now_utc().isoformat()
        retry_state["last_error"] = auth_message or "NotebookLM authentication check failed."
        retry_state["attempts"] = int(retry_state.get("attempts", 0)) + 1

    scheduled_clip_count = schedule_approved_clips(manifest)
    manifest_paths = materialize_shorts_manifests(manifest)

    in_flight = in_flight_keys(manifest)
    if in_flight:
        next_new: list[str] = []
    else:
        next_new = (
            [blocked_auth_key]
            if blocked_auth_key
            else generation_candidate_keys(manifest)[: int(manifest["experiment"]["defaults"]["max_new_cinematics_per_run"])]
        )

    summary = {
        "run_started": now_utc().isoformat(),
        "manifest": str(args.manifest),
        "ledger": str(args.ledger or manifest["experiment"]["release_ledger"]),
        "notebooklm_auth": "ok" if auth_ok else "blocked_auth_expired",
        "auth_message": auth_message,
        "added_keys": added_keys,
        "in_flight": in_flight,
        "next_new": next_new,
        "blocked_auth_key": blocked_auth_key,
        "scheduled_clip_count": scheduled_clip_count,
        "manifest_paths": manifest_paths,
    }

    print(json.dumps(summary, indent=2))

    if not args.apply:
        return

    write_yaml(args.manifest, manifest)
    ledger_path = args.ledger or Path(manifest["experiment"]["release_ledger"])
    append_ledger(ledger_path, summary)


if __name__ == "__main__":
    main()
