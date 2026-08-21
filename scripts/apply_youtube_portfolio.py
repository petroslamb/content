#!/usr/bin/env python3
"""Dry-run or apply the approved Rooted Layers YouTube portfolio manifest."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO_ROOT = REPO_ROOT / "publication_strategy_and_archive" / "portfolio"
DEFAULT_MANIFEST = PORTFOLIO_ROOT / "portfolio_manifest.yaml"
DEFAULT_APPROVAL = PORTFOLIO_ROOT / "approval.yaml"
YOUTUBE_SKILL_SCRIPTS = (
    REPO_ROOT / "workflows" / "skills" / "youtube-data-api" / "scripts"
)
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(YOUTUBE_SKILL_SCRIPTS))

import rooted_layers_portfolio as portfolio  # noqa: E402
from youtube_common import build_youtube  # noqa: E402


MAX_BATCH_SIZE = 25
DEFAULT_CANARY_SIZE = 5


class PortfolioYouTubeError(RuntimeError):
    """Raised when a fail-closed YouTube portfolio condition is violated."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def chunks(items: list[str], size: int) -> Iterable[list[str]]:
    if not 1 <= size <= MAX_BATCH_SIZE:
        raise ValueError(f"batch size must be between 1 and {MAX_BATCH_SIZE}")
    for index in range(0, len(items), size):
        yield items[index : index + size]


def safe_error(exc: BaseException) -> str:
    """Return report-safe error text without serializing auth responses or secrets."""
    if isinstance(exc, PortfolioYouTubeError):
        return f"{type(exc).__name__}: {exc}"
    return f"{type(exc).__name__}: external YouTube operation failed; details omitted"


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _write_exclusive_durable_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        _fsync_directory(path.parent)
    except FileExistsError as exc:
        raise PortfolioYouTubeError(f"journal already exists: {path}") from exc


def _replace_durable_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
        _fsync_directory(path.parent)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


class InProgressJournal:
    """Durable atomic snapshots retained separately from the immutable final report."""

    def __init__(self, path: Path, final_report_path: Path):
        self.path = path
        self.final_report_path = final_report_path
        self.sequence = 0
        self.started = False

    def checkpoint(
        self,
        report: dict[str, Any],
        event: str,
        *,
        final_report_written: bool = False,
    ) -> None:
        self.sequence += 1
        payload = {
            "schema_version": 1,
            "checkpoint_sequence": self.sequence,
            "checkpointed_at": utc_now(),
            "event": event,
            "final_report": str(self.final_report_path.resolve()),
            "final_report_written": final_report_written,
            "report": report,
        }
        if not self.started:
            _write_exclusive_durable_json(self.path, payload)
            self.started = True
        else:
            _replace_durable_json(self.path, payload)


def authenticated_channel(youtube: Any) -> dict[str, Any]:
    response = (
        youtube.channels()
        .list(part="snippet,contentDetails", mine=True, maxResults=1)
        .execute()
    )
    items = response.get("items", [])
    if len(items) != 1:
        raise PortfolioYouTubeError("could not resolve exactly one authenticated channel")
    item = items[0]
    return {
        "channel_id": item.get("id"),
        "title": item.get("snippet", {}).get("title"),
        "uploads_playlist_id": (
            item.get("contentDetails", {})
            .get("relatedPlaylists", {})
            .get("uploads")
        ),
    }


def verify_channel(youtube: Any, expected: dict[str, Any]) -> dict[str, Any]:
    live = authenticated_channel(youtube)
    expected_id = expected.get("expected_channel_id")
    expected_title = expected.get("expected_channel_title")
    expected_uploads = expected.get("expected_uploads_playlist_id")
    for key, value in (
        ("expected_channel_id", expected_id),
        ("expected_channel_title", expected_title),
        ("expected_uploads_playlist_id", expected_uploads),
    ):
        if not isinstance(value, str) or not value:
            raise PortfolioYouTubeError(f"manifest lacks {key}")
    if live.get("channel_id") != expected_id:
        raise PortfolioYouTubeError(
            f"authenticated channel mismatch: expected {expected_id}, found {live.get('channel_id')}"
        )
    if live.get("title") != expected_title:
        raise PortfolioYouTubeError(
            f"authenticated channel title mismatch: expected {expected_title!r}, "
            f"found {live.get('title')!r}"
        )
    if live.get("uploads_playlist_id") != expected_uploads:
        raise PortfolioYouTubeError(
            "authenticated uploads playlist mismatch: "
            f"expected {expected_uploads!r}, found {live.get('uploads_playlist_id')!r}"
        )
    return live


def fetch_video_statuses(
    youtube: Any,
    video_ids: list[str],
    *,
    expected_channel_id: str | None = None,
    found: dict[str, dict[str, Any]] | None = None,
) -> dict[str, dict[str, Any]]:
    if found is None:
        found = {}
    for batch in chunks(video_ids, MAX_BATCH_SIZE):
        response = (
            youtube.videos()
            .list(part="snippet,status", id=",".join(batch), maxResults=len(batch))
            .execute()
        )
        for item in response.get("items", []):
            found[item["id"]] = item
    missing = sorted(set(video_ids) - set(found))
    if missing:
        raise PortfolioYouTubeError(
            "videos missing from authenticated channel read: " + ", ".join(missing)
        )
    if expected_channel_id:
        foreign = sorted(
            video_id
            for video_id, item in found.items()
            if item.get("snippet", {}).get("channelId") != expected_channel_id
        )
        if foreign:
            raise PortfolioYouTubeError(
                "videos do not belong to the approved channel: " + ", ".join(foreign)
            )
    return found


def writable_unlisted_status(current: dict[str, Any]) -> dict[str, Any]:
    status = current.get("status", {})
    updated: dict[str, Any] = {"privacyStatus": "unlisted"}
    for key in (
        "license",
        "embeddable",
        "publicStatsViewable",
        "selfDeclaredMadeForKids",
    ):
        if key in status:
            updated[key] = status[key]
    return updated


def visibility_plan(
    youtube: Any,
    manifest: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    channel = verify_channel(youtube, manifest.get("youtube") or {})
    video_ids = list((manifest.get("youtube") or {}).get("unlist_video_ids") or [])
    artifact_by_video = {
        item.get("platform_id"): item
        for item in manifest.get("artifacts", [])
        if item.get("platform") == "YOUTUBE"
    }
    statuses = (
        fetch_video_statuses(
            youtube,
            video_ids,
            expected_channel_id=channel["channel_id"],
        )
        if video_ids
        else {}
    )
    planned: list[dict[str, Any]] = []
    for video_id in video_ids:
        artifact = artifact_by_video.get(video_id)
        if artifact is None:
            raise PortfolioYouTubeError(f"manifest artifact missing for video {video_id}")
        expected = str(artifact.get("current_visibility", "")).lower()
        target = str(artifact.get("target_visibility", "")).lower()
        if expected != "public" or target != "unlist":
            raise PortfolioYouTubeError(
                f"unsafe transition in manifest for {video_id}: {expected} -> {target}"
            )
        current = statuses[video_id]
        live = current.get("status", {}).get("privacyStatus")
        if live != expected:
            raise PortfolioYouTubeError(
                f"stale before-state for {video_id}: expected {expected}, found {live}"
            )
        planned.append(
            {
                "video_id": video_id,
                "title": current.get("snippet", {}).get("title") or artifact.get("title"),
                "url": artifact.get("current_url"),
                "expected_before": expected,
                "target_after": "unlisted",
                "rationale": artifact.get("rationale"),
                "rollback_visibility": expected,
                "expected_channel_id": channel["channel_id"],
                "expected_channel": {
                    "expected_channel_id": channel["channel_id"],
                    "expected_channel_title": channel["title"],
                    "expected_uploads_playlist_id": channel[
                        "uploads_playlist_id"
                    ],
                },
            }
        )
    return channel, planned


def prepare_visibility_update(
    youtube: Any, video_id: str, *, expected_channel_id: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    current = (
        youtube.videos()
        .list(part="snippet,status", id=video_id, maxResults=1)
        .execute()
        .get("items", [])
    )
    if len(current) != 1:
        raise PortfolioYouTubeError(f"video disappeared before mutation: {video_id}")
    live_channel = current[0].get("snippet", {}).get("channelId")
    if live_channel != expected_channel_id:
        raise PortfolioYouTubeError(
            f"video changed channel ownership before mutation: {video_id}"
        )
    live = current[0].get("status", {}).get("privacyStatus")
    if live != "public":
        raise PortfolioYouTubeError(
            f"state drift immediately before mutation for {video_id}: {live}"
        )
    body = {"id": video_id, "status": writable_unlisted_status(current[0])}
    before = {
        "video_id": video_id,
        "channel_id": live_channel,
        "before_visibility": live,
        "requested_visibility": "unlisted",
    }
    return before, body


def update_visibility(
    youtube: Any, video_id: str, *, expected_channel_id: str
) -> dict[str, Any]:
    before, body = prepare_visibility_update(
        youtube,
        video_id,
        expected_channel_id=expected_channel_id,
    )
    youtube.videos().update(part="status", body=body).execute()
    return before


def verify_unlisted(
    youtube: Any,
    video_ids: list[str],
    *,
    expected_channel_id: str | None = None,
    results: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    statuses: dict[str, dict[str, Any]] = {}
    fetch_error: Exception | None = None
    try:
        fetch_video_statuses(
            youtube,
            video_ids,
            expected_channel_id=expected_channel_id,
            found=statuses,
        )
    except Exception as exc:
        fetch_error = exc
    if results is None:
        results = []
    mismatch: tuple[str, Any] | None = None
    for video_id in video_ids:
        if video_id not in statuses:
            continue
        privacy = statuses[video_id].get("status", {}).get("privacyStatus")
        results.append(
            {
                "video_id": video_id,
                "readback_visibility": privacy,
                "matched": privacy == "unlisted",
            }
        )
        if privacy != "unlisted" and mismatch is None:
            mismatch = (video_id, privacy)
    if mismatch is not None:
        video_id, privacy = mismatch
        raise PortfolioYouTubeError(
            f"readback mismatch for {video_id}: expected unlisted, found {privacy}"
        )
    if fetch_error is not None:
        raise fetch_error
    return results


def apply_visibility_batches(
    youtube: Any,
    plan: list[dict[str, Any]],
    *,
    expected_channel_id: str | None = None,
    expected_channel: dict[str, Any] | None = None,
    canary_size: int = DEFAULT_CANARY_SIZE,
    state: dict[str, Any] | None = None,
    checkpoint: Callable[[str], None] | None = None,
) -> list[dict[str, Any]]:
    if not plan:
        return []
    if expected_channel_id is None:
        expected_channel_id = plan[0].get("expected_channel_id")
    if expected_channel is None:
        candidate = plan[0].get("expected_channel")
        if isinstance(candidate, dict):
            expected_channel = candidate
    if not isinstance(expected_channel_id, str) or not expected_channel_id:
        raise PortfolioYouTubeError(
            "visibility application requires the approved expected channel id"
        )
    if not isinstance(expected_channel, dict):
        raise PortfolioYouTubeError(
            "visibility application requires the full approved channel identity"
        )
    if not 1 <= canary_size <= MAX_BATCH_SIZE:
        raise PortfolioYouTubeError(
            f"canary size must be between 1 and {MAX_BATCH_SIZE}"
        )
    ids = [item["video_id"] for item in plan]
    first_size = min(canary_size, len(ids))
    batch_ids = [ids[:first_size], *list(chunks(ids[first_size:], MAX_BATCH_SIZE))]
    if state is None:
        state = {"batches": [], "operations": [], "rollback": []}
    results = state.setdefault("batches", [])
    operations = state.setdefault("operations", [])
    state.setdefault("remote_state_uncertain", False)
    rollback_by_video = {
        item["video_id"]: item for item in state.setdefault("rollback", [])
    }
    for item in rollback_by_video.values():
        item.setdefault("mutation_attempted", False)
        item.setdefault("mutation_succeeded", False)
        item.setdefault("readback_visibility", None)
        item.setdefault("readback_matched", None)
    for batch_number, batch in enumerate(batch_ids, start=1):
        if not batch:
            continue
        started_at = utc_now()
        batch_record = {
            "batch_number": batch_number,
            "canary": batch_number == 1,
            "started_at": started_at,
            "completed_at": None,
            "status": "STARTED",
            "video_ids": batch,
            "operation_indexes": [],
            "readback": [],
            "error": None,
        }
        results.append(batch_record)
        readback_checkpoint_attempted = False
        try:
            for video_id in batch:
                operation = {
                    "operation_index": len(operations),
                    "action": "set_visibility_unlisted",
                    "video_id": video_id,
                    "started_at": utc_now(),
                    "completed_at": None,
                    "mutation_attempted": False,
                    "mutation_succeeded": False,
                    "mutation_outcome": "NOT_ATTEMPTED",
                    "before_visibility": "public",
                    "requested_visibility": "unlisted",
                    "readback_visibility": None,
                    "readback_matched": None,
                    "error": None,
                }
                operations.append(operation)
                batch_record["operation_indexes"].append(operation["operation_index"])
                try:
                    verify_channel(youtube, expected_channel)
                    before, body = prepare_visibility_update(
                        youtube,
                        video_id,
                        expected_channel_id=expected_channel_id,
                    )
                    operation["before_visibility"] = before["before_visibility"]
                    operation["mutation_attempted"] = True
                    operation["mutation_succeeded"] = None
                    operation["mutation_outcome"] = "UNKNOWN"
                    rollback = rollback_by_video.get(video_id)
                    if rollback is not None:
                        rollback["mutation_attempted"] = True
                        rollback["mutation_succeeded"] = None
                    if checkpoint is not None:
                        checkpoint(
                            f"visibility_mutation_{operation['operation_index']}_attempting"
                        )
                    youtube.videos().update(part="status", body=body).execute()
                    operation["mutation_succeeded"] = True
                    operation["mutation_outcome"] = "SUCCEEDED"
                    operation["completed_at"] = utc_now()
                    if rollback is not None:
                        rollback["mutation_succeeded"] = True
                    if checkpoint is not None:
                        checkpoint(
                            f"visibility_mutation_{operation['operation_index']}_succeeded"
                        )
                except Exception as exc:
                    operation["completed_at"] = utc_now()
                    operation["error"] = safe_error(exc)
                    rollback = rollback_by_video.get(video_id)
                    if rollback is not None:
                        rollback["mutation_attempted"] = operation[
                            "mutation_attempted"
                        ]
                        rollback["mutation_succeeded"] = operation[
                            "mutation_succeeded"
                        ]
                    if operation["mutation_attempted"]:
                        state["remote_state_uncertain"] = True
                    raise
            readback = verify_unlisted(
                youtube,
                batch,
                expected_channel_id=expected_channel_id,
                results=batch_record["readback"],
            )
            readback_by_video = {item["video_id"]: item for item in readback}
            for operation_index in batch_record["operation_indexes"]:
                operation = operations[operation_index]
                result = readback_by_video[operation["video_id"]]
                operation["readback_visibility"] = result["readback_visibility"]
                operation["readback_matched"] = result["matched"]
                rollback = rollback_by_video.get(operation["video_id"])
                if rollback is not None:
                    rollback["readback_visibility"] = result["readback_visibility"]
                    rollback["readback_matched"] = result["matched"]
            if any(
                operations[index]["mutation_succeeded"] is True
                and operations[index]["readback_visibility"] is None
                for index in batch_record["operation_indexes"]
            ):
                state["remote_state_uncertain"] = True
            batch_record["status"] = "VERIFIED"
            batch_record["completed_at"] = utc_now()
            if checkpoint is not None:
                readback_checkpoint_attempted = True
                checkpoint(f"visibility_batch_{batch_number}_readback_verified")
        except Exception as exc:
            readback_by_video = {
                item["video_id"]: item for item in batch_record["readback"]
            }
            for operation_index in batch_record["operation_indexes"]:
                operation = operations[operation_index]
                result = readback_by_video.get(operation["video_id"])
                if result is None:
                    continue
                operation["readback_visibility"] = result["readback_visibility"]
                operation["readback_matched"] = result["matched"]
                rollback = rollback_by_video.get(operation["video_id"])
                if rollback is not None:
                    rollback["readback_visibility"] = result["readback_visibility"]
                    rollback["readback_matched"] = result["matched"]
            if any(
                (
                    operations[index]["mutation_succeeded"] is None
                    or (
                        operations[index]["mutation_succeeded"] is True
                        and operations[index]["readback_visibility"] is None
                    )
                )
                for index in batch_record["operation_indexes"]
            ):
                state["remote_state_uncertain"] = True
            batch_record["status"] = "STOPPED"
            batch_record["completed_at"] = utc_now()
            batch_record["error"] = safe_error(exc)
            if (
                checkpoint is not None
                and batch_record["readback"]
                and not readback_checkpoint_attempted
            ):
                readback_checkpoint_attempted = True
                checkpoint(f"visibility_batch_{batch_number}_readback_stopped")
            raise
    return results


def list_owned_playlists(youtube: Any) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    page_token = None
    while True:
        response = (
            youtube.playlists()
            .list(
                part="snippet,status,contentDetails",
                mine=True,
                maxResults=50,
                pageToken=page_token,
            )
            .execute()
        )
        items.extend(response.get("items", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            return items


def playlist_items(
    youtube: Any,
    playlist_id: str,
    *,
    items: list[dict[str, Any]] | None = None,
    checkpoint: Callable[[str], None] | None = None,
    checkpoint_event: str = "playlist_items_readback",
) -> list[dict[str, Any]]:
    if items is None:
        items = []
    page_token = None
    while True:
        response = (
            youtube.playlistItems()
            .list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=page_token,
            )
            .execute()
        )
        items.extend(response.get("items", []))
        if checkpoint is not None:
            checkpoint(f"{checkpoint_event}_page")
        page_token = response.get("nextPageToken")
        if not page_token:
            return items


def verify_selected_videos(
    youtube: Any,
    manifest: dict[str, Any],
    channel: dict[str, Any],
) -> list[dict[str, Any]]:
    youtube_config = manifest.get("youtube") or {}
    desired = list(youtube_config.get("selected_video_ids") or [])
    artifact_by_video = {
        item.get("platform_id"): item
        for item in manifest.get("artifacts", [])
        if item.get("platform") == "YOUTUBE"
    }
    statuses = (
        fetch_video_statuses(
            youtube,
            desired,
            expected_channel_id=channel["channel_id"],
        )
        if desired
        else {}
    )
    verified: list[dict[str, Any]] = []
    for video_id in desired:
        artifact = artifact_by_video.get(video_id)
        if artifact is None:
            raise PortfolioYouTubeError(
                f"manifest artifact missing for selected video {video_id}"
            )
        if (
            artifact.get("current_visibility") != "PUBLIC"
            or artifact.get("target_visibility") != "UNCHANGED"
        ):
            raise PortfolioYouTubeError(
                f"selected video is not approved as PUBLIC/UNCHANGED: {video_id}"
            )
        current = statuses[video_id]
        privacy = current.get("status", {}).get("privacyStatus")
        if privacy != "public":
            raise PortfolioYouTubeError(
                f"selected video is no longer public: {video_id} ({privacy})"
            )
        verified.append(
            {
                "video_id": video_id,
                "channel_id": current.get("snippet", {}).get("channelId"),
                "title": current.get("snippet", {}).get("title"),
                "visibility": privacy,
                "manifest_target": "UNCHANGED",
            }
        )
    return verified


def _playlist_item_before_state(item: dict[str, Any]) -> dict[str, Any]:
    snippet = item.get("snippet", {})
    return {
        "playlist_item_id": item.get("id"),
        "video_id": snippet.get("resourceId", {}).get("videoId"),
        "position": snippet.get("position"),
        "title": snippet.get("title"),
        "video_owner_channel_id": snippet.get("videoOwnerChannelId"),
    }


def playlist_plan(youtube: Any, manifest: dict[str, Any]) -> dict[str, Any]:
    channel = verify_channel(youtube, manifest.get("youtube") or {})
    youtube_config = manifest.get("youtube") or {}
    desired = list(youtube_config.get("selected_video_ids") or [])
    verified_selected = verify_selected_videos(youtube, manifest, channel)
    config = youtube_config.get("playlist") or {}
    should_exist = bool(config.get("create_or_update"))
    title = config.get("title")
    if should_exist != (len(desired) >= 2):
        raise PortfolioYouTubeError(
            "playlist is permitted only when at least two videos meet the selection bar"
        )
    matches = [
        item
        for item in list_owned_playlists(youtube)
        if item.get("snippet", {}).get("title") == title
    ]
    if len(matches) > 1:
        raise PortfolioYouTubeError(f"multiple owned playlists have the exact title {title!r}")
    existing = matches[0] if matches else None
    if existing and existing.get("status", {}).get("privacyStatus") != "public":
        raise PortfolioYouTubeError(
            "an existing selected-work playlist is not public; refusing to change its visibility"
        )
    current_items = playlist_items(youtube, existing["id"]) if existing else []
    current_items.sort(key=lambda item: item.get("snippet", {}).get("position", 0))
    current_ids = [
        item.get("snippet", {}).get("resourceId", {}).get("videoId")
        for item in current_items
    ]
    retained_video_ids: set[str] = set()
    remove_playlist_item_ids: list[str] = []
    for item in current_items:
        video_id = item.get("snippet", {}).get("resourceId", {}).get("videoId")
        item_id = item.get("id")
        if video_id not in desired or video_id in retained_video_ids:
            if not item_id:
                raise PortfolioYouTubeError(
                    "playlist before-state contains an item without an id"
                )
            remove_playlist_item_ids.append(item_id)
        else:
            retained_video_ids.add(video_id)
    before_items = [_playlist_item_before_state(item) for item in current_items]
    return {
        "enabled": should_exist,
        "title": title,
        "channel": channel,
        "verified_selected_videos": verified_selected,
        "existing_playlist_id": existing.get("id") if existing else None,
        "desired_video_ids": desired,
        "current_video_ids": current_ids,
        "create": should_exist and existing is None,
        "remove_playlist_item_ids": remove_playlist_item_ids,
        "add_video_ids": [video_id for video_id in desired if video_id not in current_ids],
        "reorder_required": bool(existing and current_ids != desired),
        "surface_on_channel_homepage": bool(config.get("surface_on_channel_homepage")),
        "studio_surface_automation": "DEFERRED_TO_AUTHENTICATED_STUDIO",
        "before_state": {
            "playlist_existed": existing is not None,
            "playlist": (
                {
                    "playlist_id": existing.get("id"),
                    "snippet": existing.get("snippet", {}),
                    "status": existing.get("status", {}),
                    "content_details": existing.get("contentDetails", {}),
                }
                if existing
                else None
            ),
            "items": before_items,
        },
    }


def create_playlist(youtube: Any, title: str) -> str:
    response = (
        youtube.playlists()
        .insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": (
                        "A selective Rooted Layers portfolio of AI systems and engineering work."
                    ),
                },
                "status": {"privacyStatus": "public"},
            },
        )
        .execute()
    )
    playlist_id = response.get("id")
    if not playlist_id:
        raise PortfolioYouTubeError("playlist creation returned no playlist id")
    return playlist_id


def verify_playlist_before_state(youtube: Any, plan: dict[str, Any]) -> None:
    """Reject playlist drift between the read-only plan and the first mutation."""
    before = plan.get("before_state") or {}
    playlists = list_owned_playlists(youtube)
    expected_id = plan.get("existing_playlist_id")
    title_matches = [
        item
        for item in playlists
        if item.get("snippet", {}).get("title") == plan.get("title")
    ]
    if expected_id is None:
        if title_matches:
            raise PortfolioYouTubeError(
                "playlist appeared after planning; refusing to create a duplicate"
            )
        return
    if len(title_matches) != 1 or title_matches[0].get("id") != expected_id:
        raise PortfolioYouTubeError(
            "another exact-title playlist appeared after planning"
        )
    matches = [item for item in playlists if item.get("id") == expected_id]
    if len(matches) != 1:
        raise PortfolioYouTubeError(
            "selected-work playlist disappeared or duplicated after planning"
        )
    live = matches[0]
    expected_playlist = before.get("playlist") or {}
    if live.get("snippet", {}).get("title") != plan.get("title"):
        raise PortfolioYouTubeError("selected-work playlist title drifted after planning")
    if live.get("status", {}).get("privacyStatus") != "public":
        raise PortfolioYouTubeError(
            "selected-work playlist visibility drifted after planning"
        )
    if live.get("snippet", {}).get("description") != (
        expected_playlist.get("snippet") or {}
    ).get("description"):
        raise PortfolioYouTubeError(
            "selected-work playlist description drifted after planning"
        )
    live_items = playlist_items(youtube, expected_id)
    live_items.sort(key=lambda item: item.get("snippet", {}).get("position", 0))
    normalized_live = [_playlist_item_before_state(item) for item in live_items]
    expected_items = before.get("items") or []
    comparable_keys = ("playlist_item_id", "video_id", "position")
    live_membership = [
        {key: item.get(key) for key in comparable_keys} for item in normalized_live
    ]
    expected_membership = [
        {key: item.get(key) for key in comparable_keys} for item in expected_items
    ]
    if live_membership != expected_membership:
        raise PortfolioYouTubeError(
            "selected-work playlist membership or order drifted after planning"
        )


def reconcile_playlist(
    youtube: Any,
    plan: dict[str, Any],
    *,
    manifest: dict[str, Any],
    state: dict[str, Any] | None = None,
    checkpoint: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    if state is None:
        state = playlist_application_state(plan)
    if not plan["enabled"]:
        state.update(
            {
                "status": "NOOP",
                "completed_at": utc_now(),
                "reason": "fewer_than_two_selected_videos",
            }
        )
        return state
    playlist_id = plan.get("existing_playlist_id")
    operations = state["operations"]

    def mutate(action: str, target: dict[str, Any], callback: Any) -> Any:
        operation = {
            "operation_index": len(operations),
            "action": action,
            "target": target,
            "started_at": utc_now(),
            "completed_at": None,
            "mutation_attempted": True,
            "mutation_succeeded": None,
            "mutation_outcome": "UNKNOWN",
            "response": None,
            "error": None,
        }
        operations.append(operation)
        try:
            if checkpoint is not None:
                checkpoint(
                    f"playlist_mutation_{operation['operation_index']}_attempting"
                )
            response = callback()
            operation["completed_at"] = utc_now()
            operation["mutation_succeeded"] = True
            operation["mutation_outcome"] = "SUCCEEDED"
            if isinstance(response, dict):
                operation["response"] = {
                    key: response.get(key) for key in ("id", "kind") if key in response
                }
            elif isinstance(response, str):
                operation["response"] = {"id": response}
            state["changed"] = True
            if checkpoint is not None:
                checkpoint(
                    f"playlist_mutation_{operation['operation_index']}_succeeded"
                )
            return response
        except Exception as exc:
            operation["completed_at"] = utc_now()
            operation["error"] = safe_error(exc)
            state["remote_state_uncertain"] = True
            raise

    try:
        # Re-verify ownership and PUBLIC/UNCHANGED state immediately before mutation.
        live_channel = verify_channel(youtube, manifest.get("youtube") or {})
        verify_selected_videos(youtube, manifest, live_channel)
        verify_playlist_before_state(youtube, plan)
        if not playlist_id:
            playlist_id = mutate(
                "create_public_playlist",
                {"title": plan["title"], "privacy_status": "public"},
                lambda: create_playlist(youtube, plan["title"]),
            )
            state["created"] = True
            state["playlist_id"] = playlist_id
            state["rollback"]["created_playlist_id"] = playlist_id
            if checkpoint is not None:
                checkpoint("playlist_created_state_recorded")
        for item_id in plan["remove_playlist_item_ids"]:
            before_item = next(
                (
                    item
                    for item in plan["before_state"]["items"]
                    if item["playlist_item_id"] == item_id
                ),
                None,
            )
            mutate(
                "remove_playlist_item",
                {"playlist_item_id": item_id, "before": before_item},
                lambda item_id=item_id: youtube.playlistItems()
                .delete(id=item_id)
                .execute(),
            )

        state["intermediate_items_after_removals"] = []
        existing_items = playlist_items(
            youtube,
            playlist_id,
            items=state["intermediate_items_after_removals"],
            checkpoint=checkpoint,
            checkpoint_event="playlist_intermediate_readback",
        )
        existing_by_video = {
            item.get("snippet", {}).get("resourceId", {}).get("videoId"): item
            for item in existing_items
        }
        for position, video_id in enumerate(plan["desired_video_ids"]):
            existing = existing_by_video.get(video_id)
            snippet = {
                "playlistId": playlist_id,
                "position": position,
                "resourceId": {"kind": "youtube#video", "videoId": video_id},
            }
            if existing and existing.get("snippet", {}).get("position") != position:
                mutate(
                    "reorder_playlist_item",
                    {
                        "playlist_item_id": existing.get("id"),
                        "video_id": video_id,
                        "before_position": existing.get("snippet", {}).get("position"),
                        "requested_position": position,
                    },
                    lambda existing=existing, snippet=snippet: youtube.playlistItems()
                    .update(
                        part="snippet",
                        body={"id": existing["id"], "snippet": snippet},
                    )
                    .execute(),
                )
            elif not existing:
                mutate(
                    "insert_playlist_item",
                    {"video_id": video_id, "requested_position": position},
                    lambda snippet=snippet: youtube.playlistItems()
                    .insert(part="snippet", body={"snippet": snippet})
                    .execute(),
                )

        state["readback_items"] = []
        readback_items = playlist_items(
            youtube,
            playlist_id,
            items=state["readback_items"],
            checkpoint=checkpoint,
            checkpoint_event="playlist_final_readback",
        )
        readback_ids = [
            item.get("snippet", {}).get("resourceId", {}).get("videoId")
            for item in sorted(
                readback_items,
                key=lambda item: item.get("snippet", {}).get("position", 0),
            )
        ]
        state["readback_video_ids"] = readback_ids
        state["readback_matched"] = readback_ids == plan["desired_video_ids"]
        if not state["readback_matched"]:
            raise PortfolioYouTubeError(
                f"playlist readback mismatch: expected {plan['desired_video_ids']}, found {readback_ids}"
            )
        state["status"] = "VERIFIED"
        state["completed_at"] = utc_now()
        state["url"] = f"https://www.youtube.com/playlist?list={playlist_id}"
        if checkpoint is not None:
            checkpoint("playlist_readback_verified")
        return state
    except Exception as exc:
        state["status"] = "STOPPED"
        state["completed_at"] = utc_now()
        state["error"] = safe_error(exc)
        if state.get("readback_matched") is None and state.get("changed"):
            state["remote_state_uncertain"] = True
        raise


def playlist_application_state(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "STARTED",
        "started_at": utc_now(),
        "completed_at": None,
        "changed": False,
        "created": False,
        "playlist_id": plan.get("existing_playlist_id"),
        "operations": [],
        "before_state": plan.get("before_state"),
        "rollback": {
            "automatic": False,
            "requires_separate_authorization": True,
            "restore_before_state": plan.get("before_state"),
            "created_playlist_id": None,
            "note": (
                "Use this exact before-state for an explicitly authorized rollback; "
                "never auto-delete a created remote playlist."
            ),
        },
        "readback_video_ids": None,
        "readback_matched": None,
        "remote_state_uncertain": False,
        "error": None,
    }


def default_report_path(operation: str, digest: str) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return PORTFOLIO_ROOT / "applications" / f"{stamp}_{operation}_{digest[:12]}.json"


def default_journal_path(report_path: Path) -> Path:
    return report_path.with_name(f"{report_path.name}.in-progress.json")


def write_immutable_report(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        _fsync_directory(path.parent)
    except FileExistsError as exc:
        raise PortfolioYouTubeError(f"application report already exists: {path}") from exc


def bounded_canary_size(value: str) -> int:
    try:
        size = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("canary size must be an integer") from exc
    if not 1 <= size <= MAX_BATCH_SIZE:
        raise argparse.ArgumentTypeError(
            f"canary size must be between 1 and {MAX_BATCH_SIZE}"
        )
    return size


def validate_output_paths(
    args: argparse.Namespace,
    report_path: Path,
    journal_path: Path,
) -> None:
    resolved_report = report_path.resolve()
    resolved_journal = journal_path.resolve()
    protected = {args.manifest.resolve()}
    if args.apply:
        protected.add(args.approval.resolve())
        if args.release_readiness is not None:
            protected.add(args.release_readiness.resolve())
    if resolved_report == resolved_journal:
        raise PortfolioYouTubeError("--report and --journal must be different paths")
    if resolved_report in protected or resolved_journal in protected:
        raise PortfolioYouTubeError(
            "report and journal paths must not overwrite an authorization input"
        )
    if report_path.exists():
        raise PortfolioYouTubeError(f"application report already exists: {report_path}")
    if journal_path.exists():
        raise PortfolioYouTubeError(
            f"in-progress journal already exists; reconcile it before a new run: {journal_path}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "operation",
        choices=("visibility", "playlist", "all"),
        help="Approved YouTube portfolio operation to inspect or execute",
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--approval", type=Path, default=DEFAULT_APPROVAL)
    parser.add_argument(
        "--release-readiness",
        type=Path,
        help="Resolved digest-bound release_readiness review gate; required with --apply",
    )
    parser.add_argument("--report", type=Path)
    parser.add_argument("--journal", type=Path)
    parser.add_argument(
        "--canary-size",
        type=bounded_canary_size,
        default=DEFAULT_CANARY_SIZE,
    )
    parser.add_argument("--apply", action="store_true", help="Apply externally; default is read-only dry-run")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.apply and args.release_readiness is None:
        raise SystemExit("--apply requires --release-readiness")
    approval_path = args.approval if args.apply else None
    gate_path = args.release_readiness if args.apply else None
    manifest, validation = portfolio.validate_manifest_document(
        args.manifest,
        approval_path,
        gate_path,
        validation_mode="apply-ready" if args.apply else "preapproval",
    )
    if not validation["valid"]:
        raise SystemExit("Invalid portfolio manifest:\n- " + "\n- ".join(validation["errors"]))
    digest = validation["manifest_sha256"]
    report_path = args.report or default_report_path(args.operation, digest)
    journal_path = args.journal or default_journal_path(report_path)
    validate_output_paths(args, report_path, journal_path)
    report: dict[str, Any] = {
        "schema_version": 2,
        "created_at": utc_now(),
        "completed_at": None,
        "operation": args.operation,
        "mode": "apply" if args.apply else "dry_run",
        "manifest": str(args.manifest.resolve()),
        "manifest_sha256": digest,
        "approval": str(args.approval.resolve()) if args.apply else None,
        "approval_sha256": validation.get("approval_sha256"),
        "release_readiness": (
            str(args.release_readiness.resolve()) if args.apply else None
        ),
        "release_readiness_sha256": validation.get(
            "release_readiness_sha256"
        ),
        "source_snapshot_sha256": manifest.get("source_snapshot_sha256"),
        "source_ledger_sha256": (manifest.get("youtube") or {}).get(
            "source_ledger_sha256"
        ),
        "in_progress_journal": str(journal_path.resolve()),
        "last_checkpoint": None,
        "status": "STARTED",
        "stage": "INITIALIZED",
        "channel": None,
        "visibility": None,
        "playlist": None,
        "error": None,
    }
    journal = InProgressJournal(journal_path, report_path)

    def checkpoint(event: str) -> None:
        report["last_checkpoint"] = event
        journal.checkpoint(report, event)

    try:
        checkpoint("initialized_before_authentication")
        report["stage"] = "AUTHENTICATING"
        youtube = build_youtube()
        report["stage"] = "VERIFYING_CHANNEL"
        channel = verify_channel(youtube, manifest.get("youtube") or {})
        report["channel"] = channel
        planned_playlist = None
        planned_visibility: list[dict[str, Any]] = []
        if args.operation in {"playlist", "all"}:
            report["stage"] = "PLANNING_PLAYLIST"
            planned_playlist = playlist_plan(youtube, manifest)
            report["playlist"] = {"plan": planned_playlist, "application": None}
        if args.operation in {"visibility", "all"}:
            report["stage"] = "PLANNING_VISIBILITY"
            _, planned_visibility = visibility_plan(youtube, manifest)
            report["visibility"] = {
                "planned_count": len(planned_visibility),
                "plan": planned_visibility,
                "batches": [],
                "operations": [],
                "rollback": [
                    {
                        "video_id": item["video_id"],
                        "restore_visibility": item["rollback_visibility"],
                        "only_if_current_visibility": "unlisted",
                        "mutation_attempted": False,
                        "mutation_succeeded": False,
                        "readback_visibility": None,
                        "readback_matched": None,
                    }
                    for item in planned_visibility
                ],
            }
        # Finish every requested live preflight before the first mutation.
        if args.apply:
            if planned_playlist is not None:
                report["stage"] = "APPLYING_PLAYLIST"
                application = playlist_application_state(planned_playlist)
                report["playlist"]["application"] = application
                reconcile_playlist(
                    youtube,
                    planned_playlist,
                    manifest=manifest,
                    state=application,
                    checkpoint=checkpoint,
                )
            if args.operation in {"visibility", "all"}:
                report["stage"] = "APPLYING_VISIBILITY"
                apply_visibility_batches(
                    youtube,
                    planned_visibility,
                    expected_channel_id=channel["channel_id"],
                    expected_channel=manifest.get("youtube") or {},
                    canary_size=args.canary_size,
                    state=report["visibility"],
                    checkpoint=checkpoint,
                )
        report["status"] = "APPLIED" if args.apply else "DRY_RUN_VERIFIED"
        report["stage"] = "COMPLETED"
    except BaseException as exc:
        report["status"] = "STOPPED"
        report["error"] = safe_error(exc)
        report["completed_at"] = utc_now()
        try:
            checkpoint("stopped_before_immutable_report")
        except BaseException as journal_exc:
            report["journal_error"] = safe_error(journal_exc)
        write_immutable_report(report_path, report)
        try:
            journal.checkpoint(
                report,
                "immutable_stopped_report_written",
                final_report_written=True,
            )
        except BaseException:
            pass
        print(json.dumps(report, indent=2, ensure_ascii=False))
        if isinstance(exc, (KeyboardInterrupt, SystemExit)):
            raise
        raise SystemExit(f"STOPPED; see immutable report: {report_path}") from None
    report["completed_at"] = utc_now()
    checkpoint("final_state_before_immutable_report")
    write_immutable_report(report_path, report)
    journal.checkpoint(
        report,
        "immutable_final_report_written",
        final_report_written=True,
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
