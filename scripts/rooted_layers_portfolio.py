#!/usr/bin/env python3
"""Build and validate the governed Rooted Layers portfolio decision layer."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO_ROOT = REPO_ROOT / "publication_strategy_and_archive" / "portfolio"
DEFAULT_MANIFEST = PORTFOLIO_ROOT / "portfolio_manifest.yaml"
DEFAULT_SNAPSHOT = PORTFOLIO_ROOT / "corpus_snapshot.json"
DEFAULT_REPORT = PORTFOLIO_ROOT / "ROOTED_LAYERS_DECISIONS.md"
DEFAULT_APPROVAL = PORTFOLIO_ROOT / "approval.yaml"
ARCHIVE_METADATA = (
    REPO_ROOT / "publication_strategy_and_archive" / "substack_archive" / "metadata.json"
)
SUBSTACK_COMPLETENESS = (
    REPO_ROOT
    / "publication_strategy_and_archive"
    / "substack_archive"
    / "completeness_report.json"
)
POST_MAP = REPO_ROOT / "publication_strategy_and_archive" / "post_map.yaml"
YOUTUBE_LEDGER = REPO_ROOT / "experiments" / "youtube-analytics" / "metrics_ledger.json"
YOUTUBE_CONTENT = REPO_ROOT / "experiments" / "youtube-analytics" / "content_rubric.json"

DISCLOSURE = (
    "Rooted Layers is a historical archive of research and engineering work "
    "developed with AI-assisted research, drafting, and media workflows. The "
    "selected pieces are highlighted for their technical arguments, source "
    "trails, and documented engineering contribution."
)
PROFILE_URL = "https://petroslamb.github.io/peterlamb/"
MIRROR_URL = "https://petroslamb.github.io/content/"
PLAYLIST_TITLE = "Selected Rooted Layers — AI Systems & Engineering"

SELECTION_TIERS = {"FLAGSHIP", "SUPPORTING", "ARCHIVE"}
EDITORIAL_ACTIONS = {"KEEP", "REWRITE_CANDIDATE", "MERGE_CANDIDATE", "NONE"}
TARGET_VISIBILITIES = {"UNCHANGED", "UNLIST"}
CURRENT_VISIBILITIES = {"PUBLIC", "UNLISTED", "PRIVATE"}
RELATIONSHIP_TYPES = {
    "DERIVED_FROM",
    "DUPLICATES",
    "REVISES",
    "EMBEDS",
    "SAME_SERIES",
}
CONFIDENCE_LEVELS = {"HIGH", "MEDIUM", "LOW"}
FACTUAL_RISKS = {"LOW", "MEDIUM", "HIGH", "UNRESOLVED_HIGH"}
APPROVAL_STATUSES = {"PENDING", "APPROVED", "REJECTED"}
APPLICATION_STATUSES = {"NOT_APPLIED", "APPLIED", "FAILED", "ROLLED_BACK"}
VALIDATION_MODES = {"preapproval", "apply-ready"}
RELEASE_GATE_CONTRACT = "release_readiness"
WORKFLOW_ID = "rooted_layers_portfolio_cleanup"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path.resolve())


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def read_manifest_document(path: Path) -> tuple[bytes, dict[str, Any], str]:
    """Read, parse, and digest one immutable manifest byte buffer."""
    raw = path.read_bytes()
    value = yaml.safe_load(raw)
    if not isinstance(value, dict):
        raise ValueError("manifest must contain a YAML object")
    return raw, value, sha256_bytes(raw)


def manifest_digest(path: Path) -> str:
    """Return the digest of the exact manifest bytes presented for approval."""
    return sha256_path(path)


def _resolve_declared_path(value: str, manifest_path: Path) -> Path:
    declared = Path(value)
    if declared.is_absolute():
        return declared
    repo_candidate = REPO_ROOT / declared
    if repo_candidate.exists():
        return repo_candidate
    return manifest_path.parent / declared


def source_record(path: Path) -> dict[str, Any]:
    return {
        "path": relative(path),
        "sha256": sha256_path(path),
        "modified_at": datetime.fromtimestamp(
            path.stat().st_mtime, timezone.utc
        ).isoformat(),
    }


def build_snapshot(
    *,
    metadata_path: Path = ARCHIVE_METADATA,
    post_map_path: Path = POST_MAP,
    completeness_path: Path = SUBSTACK_COMPLETENESS,
    youtube_ledger_path: Path = YOUTUBE_LEDGER,
    youtube_content_path: Path = YOUTUBE_CONTENT,
) -> dict[str, Any]:
    required = [
        metadata_path,
        post_map_path,
        completeness_path,
        youtube_ledger_path,
        youtube_content_path,
    ]
    missing = [relative(path) for path in required if not path.exists()]
    if missing:
        raise ValueError("snapshot sources missing: " + ", ".join(missing))

    metadata = read_json(metadata_path)
    post_map = (read_yaml(post_map_path) or {}).get("posts", {})
    completeness = read_json(completeness_path)
    ledger = read_json(youtube_ledger_path)
    content = read_json(youtube_content_path)

    if not completeness.get("complete"):
        raise ValueError("Substack completeness report is not complete")
    if completeness.get("source_failures"):
        raise ValueError("Substack completeness report contains source failures")

    public_posts = [
        post
        for post in metadata
        if str(post.get("audience", "")).lower() == "everyone"
    ]
    published_map = {
        slug: entry
        for slug, entry in post_map.items()
        if str(entry.get("status", "")).lower() == "published"
    }
    public_slugs = {post.get("slug") for post in public_posts}
    mapped_slugs = set(published_map)

    channel = ledger.get("channel") or {}
    if not all(
        channel.get(key)
        for key in ("channel_id", "title", "uploads_playlist_id")
    ):
        raise ValueError(
            "YouTube ledger lacks the exact channel id, title, or uploads playlist id; "
            "refresh it with the authenticated all-channel collector"
        )
    if ledger.get("source", {}).get("scope") != "all_channel":
        raise ValueError("YouTube ledger is not an all-channel snapshot")

    videos = ledger.get("videos", [])
    content_items = content.get("items", {})
    visibility_counts: dict[str, int] = {}
    for video in videos:
        visibility = str(video.get("privacy_status") or "unknown").lower()
        visibility_counts[visibility] = visibility_counts.get(visibility, 0) + 1

    content_status_counts: dict[str, int] = {}
    for item in content_items.values():
        status = str(item.get("status") or "unknown")
        content_status_counts[status] = content_status_counts.get(status, 0) + 1

    return {
        "schema_version": 1,
        "created_at": utc_now(),
        "read_only": True,
        "sources": {
            "substack_metadata": source_record(metadata_path),
            "substack_post_map": source_record(post_map_path),
            "substack_completeness": source_record(completeness_path),
            "youtube_ledger": source_record(youtube_ledger_path),
            "youtube_content_evidence": source_record(youtube_content_path),
        },
        "substack": {
            "public_post_count": len(public_posts),
            "published_post_map_count": len(published_map),
            "public_slugs": sorted(slug for slug in public_slugs if slug),
            "published_map_only_slugs": sorted(mapped_slugs - public_slugs),
            "archive_only_slugs": sorted(public_slugs - mapped_slugs),
            "completeness": completeness,
        },
        "youtube": {
            "snapshot_timestamp": ledger.get("created_at"),
            "channel": channel,
            "video_count": len(videos),
            "visibility_counts": visibility_counts,
            "playlist_count": len(ledger.get("channel_playlists", [])),
            "content_evidence_count": len(content_items),
            "content_status_counts": content_status_counts,
        },
    }


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _required_text(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} must be non-empty text")


def _required_sha256(value: Any, label: str, errors: list[str]) -> None:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        errors.append(f"{label} must be a lowercase 64-character SHA-256")


def validate_manifest_data(
    manifest: dict[str, Any],
    *,
    manifest_path: Path | None = None,
    manifest_sha256: str | None = None,
    approval: dict[str, Any] | None = None,
    approval_path: Path | None = None,
    release_readiness: dict[str, Any] | None = None,
    release_readiness_path: Path | None = None,
    validation_mode: str = "preapproval",
) -> list[str]:
    errors: list[str] = []
    if validation_mode not in VALIDATION_MODES:
        return [f"validation_mode must be one of {sorted(VALIDATION_MODES)}"]
    if manifest.get("schema_version") != 1:
        errors.append("schema_version must equal 1")
    _required_text(manifest.get("portfolio_version"), "portfolio_version", errors)
    _required_text(manifest.get("generated_at"), "generated_at", errors)
    _required_text(manifest.get("source_snapshot"), "source_snapshot", errors)
    _required_sha256(
        manifest.get("source_snapshot_sha256"),
        "source_snapshot_sha256",
        errors,
    )
    if manifest.get("professional_profile_url") != PROFILE_URL:
        errors.append(f"professional_profile_url must equal {PROFILE_URL}")
    if manifest.get("mirror_url") != MIRROR_URL:
        errors.append(f"mirror_url must equal {MIRROR_URL}")
    if manifest.get("ai_disclosure") != DISCLOSURE:
        errors.append("ai_disclosure does not match the approved global disclosure")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        return errors + ["artifacts must be a list"]
    artifacts_by_id: dict[str, dict[str, Any]] = {}
    platform_ids: set[tuple[Any, Any]] = set()
    for index, artifact in enumerate(artifacts):
        label = f"artifacts[{index}]"
        if not isinstance(artifact, dict):
            errors.append(f"{label} must be an object")
            continue
        artifact_id = artifact.get("artifact_id")
        _required_text(artifact_id, f"{label}.artifact_id", errors)
        if isinstance(artifact_id, str):
            if artifact_id in artifacts_by_id:
                errors.append(f"duplicate artifact_id: {artifact_id}")
            artifacts_by_id[artifact_id] = artifact
        for key in ("platform", "platform_id", "title", "current_url", "family_id"):
            _required_text(artifact.get(key), f"{label}.{key}", errors)
        if artifact.get("platform") not in {"SUBSTACK", "YOUTUBE"}:
            errors.append(f"{label}.platform must be SUBSTACK or YOUTUBE")
        platform_key = (artifact.get("platform"), artifact.get("platform_id"))
        if all(isinstance(value, str) and value for value in platform_key):
            if platform_key in platform_ids:
                errors.append(
                    f"duplicate {platform_key[0]} platform_id: {platform_key[1]}"
                )
            platform_ids.add(platform_key)
        if artifact.get("selection_tier") not in SELECTION_TIERS:
            errors.append(f"{label}.selection_tier is invalid")
        if artifact.get("editorial_action") not in EDITORIAL_ACTIONS:
            errors.append(f"{label}.editorial_action is invalid")
        if artifact.get("target_visibility") not in TARGET_VISIBILITIES:
            errors.append(f"{label}.target_visibility is invalid")
        if artifact.get("current_visibility") not in CURRENT_VISIBILITIES:
            errors.append(f"{label}.current_visibility is invalid")
        if artifact.get("confidence") not in CONFIDENCE_LEVELS:
            errors.append(f"{label}.confidence is invalid")
        if artifact.get("approval_status") not in APPROVAL_STATUSES:
            errors.append(f"{label}.approval_status is invalid")
        if artifact.get("application_status") not in APPLICATION_STATUSES:
            errors.append(f"{label}.application_status is invalid")
        _required_text(artifact.get("rationale"), f"{label}.rationale", errors)
        if not artifact.get("evidence_anchors"):
            errors.append(f"{label}.evidence_anchors must not be empty")
        risk = artifact.get("factual_risk") or {}
        if not isinstance(risk, dict) or risk.get("status") not in FACTUAL_RISKS:
            errors.append(f"{label}.factual_risk.status is invalid")
        provenance = artifact.get("provenance") or {}
        if not isinstance(provenance, dict):
            errors.append(f"{label}.provenance must be an object")
        else:
            _required_text(provenance.get("status"), f"{label}.provenance.status", errors)
            _required_text(
                provenance.get("documented_contribution"),
                f"{label}.provenance.documented_contribution",
                errors,
            )
        lineage = artifact.get("source_lineage") or {}
        if not isinstance(lineage, dict):
            errors.append(f"{label}.source_lineage must be an object")
        else:
            _required_text(lineage.get("status"), f"{label}.source_lineage.status", errors)

        homepage = artifact.get("homepage") or {}
        section = homepage.get("section")
        order = homepage.get("order")
        if section not in {None, "FLAGSHIP", "SUPPORTING"}:
            errors.append(f"{label}.homepage.section is invalid")
        if section is None and order is not None:
            errors.append(f"{label}.homepage.order must be null without a section")
        if section is not None and (not isinstance(order, int) or order < 1):
            errors.append(f"{label}.homepage.order must be a positive integer")
        if section is not None and artifact.get("selection_tier") != section:
            errors.append(f"{label}.homepage.section must match selection_tier")
        if section is not None and artifact.get("platform") != "SUBSTACK":
            errors.append(f"{label}: only Substack essays may be placed on the homepage")

        if artifact.get("target_visibility") == "UNLIST":
            if artifact.get("platform") != "YOUTUBE":
                errors.append(f"{label}: only YouTube artifacts may be unlisted")
            if artifact.get("current_visibility") != "PUBLIC":
                errors.append(f"{label}: UNLIST requires current_visibility PUBLIC")
            if not artifact.get("relationships"):
                errors.append(f"{label}: UNLIST requires a relationship to retained evidence")
        if artifact.get("platform") == "SUBSTACK" and not str(
            artifact.get("current_url", "")
        ).startswith("https://lambpetros.substack.com/"):
            errors.append(f"{label}: Substack current_url must remain canonical")

        if artifact.get("selection_tier") == "FLAGSHIP":
            if lineage.get("status") != "RESOLVED":
                errors.append(f"{label}: flagship source lineage must be RESOLVED")
            if risk.get("status") in {"HIGH", "UNRESOLVED_HIGH"}:
                errors.append(f"{label}: flagship has unresolved high factual risk")
            if artifact.get("confidence") == "LOW":
                errors.append(f"{label}: flagship confidence cannot be LOW")

        relationships = artifact.get("relationships")
        if not isinstance(relationships, list):
            errors.append(f"{label}.relationships must be a list")
        else:
            for rel_index, relationship in enumerate(relationships):
                rel_label = f"{label}.relationships[{rel_index}]"
                if not isinstance(relationship, dict):
                    errors.append(f"{rel_label} must be an object")
                    continue
                if relationship.get("type") not in RELATIONSHIP_TYPES:
                    errors.append(f"{rel_label}.type is invalid")
                _required_text(relationship.get("target_artifact_id"), f"{rel_label}.target_artifact_id", errors)

    for artifact_id, artifact in artifacts_by_id.items():
        for relationship in artifact.get("relationships") or []:
            target = relationship.get("target_artifact_id")
            if target not in artifacts_by_id:
                errors.append(f"{artifact_id} relationship target does not exist: {target}")
            if target == artifact_id:
                errors.append(f"{artifact_id} cannot relate to itself")

    homepage = manifest.get("homepage") or {}
    flagship_ids = homepage.get("flagship_artifact_ids") or []
    supporting_ids = homepage.get("supporting_artifact_ids") or []
    if len(flagship_ids) > 4:
        errors.append("homepage exceeds four flagship essays")
    if len(supporting_ids) > 4:
        errors.append("homepage exceeds four supporting essays")
    if len(set(flagship_ids)) != len(flagship_ids):
        errors.append("homepage flagship ids contain duplicates")
    if len(set(supporting_ids)) != len(supporting_ids):
        errors.append("homepage supporting ids contain duplicates")
    if set(flagship_ids) & set(supporting_ids):
        errors.append("an artifact cannot be both flagship and supporting")

    placements: dict[str, list[tuple[int, str]]] = {"FLAGSHIP": [], "SUPPORTING": []}
    for artifact_id, artifact in artifacts_by_id.items():
        placement = artifact.get("homepage") or {}
        section = placement.get("section")
        if section in placements:
            placements[section].append((placement.get("order"), artifact_id))
    for section, expected_ids in (
        ("FLAGSHIP", flagship_ids),
        ("SUPPORTING", supporting_ids),
    ):
        actual_ids = [artifact_id for _, artifact_id in sorted(placements[section])]
        if actual_ids != expected_ids:
            errors.append(
                f"homepage {section.lower()} ids do not match artifact placements: "
                f"expected {expected_ids}, found {actual_ids}"
            )

    youtube = manifest.get("youtube") or {}
    selected_ids = youtube.get("selected_video_ids") or []
    unlist_ids = youtube.get("unlist_video_ids") or []
    playlist = youtube.get("playlist") or {}
    for key in (
        "expected_channel_id",
        "expected_channel_title",
        "expected_uploads_playlist_id",
        "snapshot_timestamp",
        "source_ledger_sha256",
    ):
        if key == "source_ledger_sha256":
            _required_sha256(youtube.get(key), f"youtube.{key}", errors)
        else:
            _required_text(youtube.get(key), f"youtube.{key}", errors)
    if not isinstance(selected_ids, list):
        errors.append("youtube.selected_video_ids must be a list")
        selected_ids = []
    if not isinstance(unlist_ids, list):
        errors.append("youtube.unlist_video_ids must be a list")
        unlist_ids = []
    if any(not isinstance(video_id, str) or not video_id for video_id in selected_ids):
        errors.append("youtube.selected_video_ids must contain non-empty strings")
    if any(not isinstance(video_id, str) or not video_id for video_id in unlist_ids):
        errors.append("youtube.unlist_video_ids must contain non-empty strings")
    if len(set(selected_ids)) != len(selected_ids):
        errors.append("youtube.selected_video_ids contains duplicates")
    if len(set(unlist_ids)) != len(unlist_ids):
        errors.append("youtube.unlist_video_ids contains duplicates")
    if playlist.get("title") != PLAYLIST_TITLE:
        errors.append("YouTube playlist title is invalid")
    if playlist.get("create_or_update") != (len(selected_ids) >= 2):
        errors.append("playlist create_or_update must be true exactly when at least two videos are selected")
    if set(selected_ids) & set(unlist_ids):
        errors.append("selected videos cannot also be unlisted")
    youtube_artifacts = {
        artifact.get("platform_id"): artifact
        for artifact in artifacts
        if isinstance(artifact, dict) and artifact.get("platform") == "YOUTUBE"
    }
    for video_id in selected_ids:
        artifact = youtube_artifacts.get(video_id)
        if not artifact:
            errors.append(f"selected YouTube video is absent from artifacts: {video_id}")
        elif artifact.get("current_visibility") != "PUBLIC" or artifact.get("target_visibility") != "UNCHANGED":
            errors.append(f"selected YouTube video must remain public: {video_id}")
    for video_id in unlist_ids:
        artifact = youtube_artifacts.get(video_id)
        if not artifact:
            errors.append(f"unlisted YouTube video is absent from artifacts: {video_id}")
        elif artifact.get("target_visibility") != "UNLIST":
            errors.append(f"YouTube unlist list disagrees with artifact: {video_id}")
    declared_unlists = {
        artifact.get("platform_id")
        for artifact in artifacts
        if isinstance(artifact, dict)
        and artifact.get("platform") == "YOUTUBE"
        and artifact.get("target_visibility") == "UNLIST"
    }
    if declared_unlists != set(unlist_ids):
        errors.append("youtube.unlist_video_ids does not exactly match artifact targets")

    if validation_mode == "apply-ready":
        mutation_artifact_ids = list(flagship_ids) + list(supporting_ids)
        mutation_artifact_ids.extend(
            artifact["artifact_id"]
            for video_id in [*selected_ids, *unlist_ids]
            if (artifact := youtube_artifacts.get(video_id)) is not None
        )
        for artifact_id in mutation_artifact_ids:
            artifact = artifacts_by_id.get(artifact_id)
            if artifact is None:
                continue
            if artifact.get("approval_status") != "APPROVED":
                errors.append(
                    f"apply-ready mutation artifact is not APPROVED: {artifact_id}"
                )
            if artifact.get("application_status") != "NOT_APPLIED":
                errors.append(
                    "apply-ready mutation artifact application_status must be "
                    f"NOT_APPLIED: {artifact_id}"
                )

    questions = manifest.get("unresolved_questions") or []
    if not isinstance(questions, list):
        errors.append("unresolved_questions must be a list")
    elif len(questions) > 10:
        errors.append("unresolved_questions exceeds the ten-question limit")

    if approval is not None:
        if manifest_sha256 is None:
            errors.append("approval validation requires the immutable manifest digest")
        else:
            if approval.get("schema_version") != 1:
                errors.append("approval.schema_version must equal 1")
            _required_sha256(
                approval.get("manifest_sha256"),
                "approval.manifest_sha256",
                errors,
            )
            if approval.get("status") != "APPROVED":
                errors.append("approval status is not APPROVED")
            if approval.get("manifest_sha256") != manifest_sha256:
                errors.append(
                    "approval manifest digest does not match the exact current manifest"
                )
            _required_text(approval.get("approved_at"), "approval.approved_at", errors)
            _required_text(approval.get("approved_by"), "approval.approved_by", errors)
    elif validation_mode == "apply-ready":
        errors.append("apply-ready validation requires approval.yaml")

    if release_readiness is not None:
        errors.extend(
            validate_release_readiness_data(
                release_readiness,
                manifest=manifest,
                manifest_path=manifest_path,
                manifest_sha256=manifest_sha256,
                approval=approval,
                approval_path=approval_path,
                release_readiness_path=release_readiness_path,
            )
        )
    elif validation_mode == "apply-ready":
        errors.append(
            "apply-ready validation requires a durable release_readiness gate artifact"
        )

    return errors


def _declared_path_matches(value: Any, expected: Path, manifest_path: Path) -> bool:
    if not isinstance(value, str) or not value:
        return False
    return _resolve_declared_path(value, manifest_path).resolve() == expected.resolve()


def validate_release_readiness_data(
    gate: dict[str, Any],
    *,
    manifest: dict[str, Any],
    manifest_path: Path | None,
    manifest_sha256: str | None,
    approval: dict[str, Any] | None,
    approval_path: Path | None,
    release_readiness_path: Path | None,
) -> list[str]:
    """Validate the durable release gate and its portfolio-specific binding."""
    errors: list[str] = []
    if gate.get("kind") != "review_gate":
        errors.append("release_readiness.kind must equal review_gate")
    _required_text(gate.get("gate_id"), "release_readiness.gate_id", errors)
    if gate.get("schema_version") != 1:
        errors.append("release_readiness.schema_version must equal 1")
    if gate.get("retained_example") is True:
        errors.append("release_readiness retained examples cannot authorize rollout")
    if gate.get("status") != "resolved":
        errors.append("release_readiness.status must equal resolved")
    if gate.get("gate_contract") != RELEASE_GATE_CONTRACT:
        errors.append("release_readiness.gate_contract must equal release_readiness")
    if gate.get("gate_type") != "external_mutation":
        errors.append("release_readiness.gate_type must equal external_mutation")
    if release_readiness_path is None:
        errors.append("release_readiness validation requires the gate artifact path")
    else:
        gate_store = (REPO_ROOT / "reviewable-runs" / "gates").resolve()
        try:
            release_readiness_path.resolve().relative_to(gate_store)
        except ValueError:
            errors.append(
                "release_readiness gate artifact must be stored under reviewable-runs/gates"
            )
    workflow = gate.get("workflow") or {}
    if workflow.get("workflow_id") != WORKFLOW_ID:
        errors.append(
            f"release_readiness.workflow.workflow_id must equal {WORKFLOW_ID}"
        )

    decision = gate.get("decision") or {}
    if decision.get("outcome") != "approve":
        errors.append("release_readiness decision outcome must equal approve")
    _required_text(decision.get("decided_at"), "release_readiness.decision.decided_at", errors)
    _required_text(decision.get("decided_by"), "release_readiness.decision.decided_by", errors)
    dimensions = (
        "quality",
        "external_mutation",
        "lifecycle_movement",
        "promotion",
    )
    dimension_fields = {
        "quality": "quality_approved",
        "external_mutation": "external_mutation_approved",
        "lifecycle_movement": "lifecycle_movement_approved",
        "promotion": "promotion_approved",
    }
    dimension_data = decision.get("approval_dimensions") or {}
    for dimension in dimensions:
        if decision.get(dimension_fields[dimension]) is not True:
            errors.append(
                f"release_readiness.decision.{dimension_fields[dimension]} must be true"
            )
        values = dimension_data.get(dimension) or {}
        if values.get("required") is not True or values.get("approved") is not True:
            errors.append(
                "release_readiness.decision.approval_dimensions."
                f"{dimension} must be required and approved"
            )

    binding = gate.get("portfolio_authorization") or {}
    if binding.get("schema_version") != 1:
        errors.append("release_readiness.portfolio_authorization.schema_version must equal 1")
    if binding.get("manifest_sha256") != manifest_sha256:
        errors.append("release_readiness manifest digest does not match exact manifest bytes")
    if binding.get("approval_manifest_sha256") != manifest_sha256:
        errors.append("release_readiness approval digest does not match exact manifest bytes")
    if binding.get("source_snapshot_sha256") != manifest.get("source_snapshot_sha256"):
        errors.append("release_readiness source snapshot digest does not match manifest")
    youtube = manifest.get("youtube") or {}
    for key in (
        "expected_channel_id",
        "expected_channel_title",
        "expected_uploads_playlist_id",
        "snapshot_timestamp",
        "source_ledger_sha256",
    ):
        if binding.get(key) != youtube.get(key):
            errors.append(f"release_readiness {key} does not match manifest")
    if manifest_path is None:
        errors.append("release_readiness validation requires manifest_path")
    else:
        if not _declared_path_matches(
            binding.get("manifest_path"), manifest_path, manifest_path
        ):
            errors.append("release_readiness manifest_path does not match")
        source_value = manifest.get("source_snapshot")
        if isinstance(source_value, str) and source_value:
            expected_snapshot = _resolve_declared_path(source_value, manifest_path)
            if not _declared_path_matches(
                binding.get("source_snapshot_path"),
                expected_snapshot,
                manifest_path,
            ):
                errors.append("release_readiness source_snapshot_path does not match")
        if approval_path is None:
            errors.append("release_readiness validation requires approval_path")
        elif not _declared_path_matches(
            binding.get("approval_path"), approval_path, manifest_path
        ):
            errors.append("release_readiness approval_path does not match")
    if approval is None:
        errors.append("release_readiness validation requires approval.yaml")
    elif binding.get("approval_manifest_sha256") != approval.get("manifest_sha256"):
        errors.append("release_readiness approval binding disagrees with approval.yaml")
    return errors


def validate_snapshot_binding(
    manifest: dict[str, Any], manifest_path: Path
) -> list[str]:
    """Reconcile the manifest, corpus snapshot, and exact ledger bytes."""
    errors: list[str] = []
    snapshot_value = manifest.get("source_snapshot")
    snapshot_digest = manifest.get("source_snapshot_sha256")
    if not isinstance(snapshot_value, str) or not snapshot_value:
        return ["source_snapshot must be non-empty text"]
    snapshot_path = _resolve_declared_path(snapshot_value, manifest_path)
    try:
        snapshot_bytes = snapshot_path.read_bytes()
        snapshot = json.loads(snapshot_bytes)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"could not read source snapshot {relative(snapshot_path)}: {type(exc).__name__}"]
    actual_snapshot_digest = sha256_bytes(snapshot_bytes)
    if snapshot_digest != actual_snapshot_digest:
        errors.append("source_snapshot_sha256 does not match the exact corpus snapshot bytes")
    if not isinstance(snapshot, dict) or snapshot.get("schema_version") != 1:
        errors.append("source snapshot must be a schema_version 1 JSON object")
        return errors

    manifest_youtube = manifest.get("youtube") or {}
    snapshot_youtube = snapshot.get("youtube") or {}
    snapshot_channel = snapshot_youtube.get("channel") or {}
    channel_keys = {
        "expected_channel_id": "channel_id",
        "expected_channel_title": "title",
        "expected_uploads_playlist_id": "uploads_playlist_id",
    }
    for manifest_key, channel_key in channel_keys.items():
        if manifest_youtube.get(manifest_key) != snapshot_channel.get(channel_key):
            errors.append(
                f"manifest youtube.{manifest_key} does not match corpus snapshot channel.{channel_key}"
            )
    if manifest_youtube.get("snapshot_timestamp") != snapshot_youtube.get(
        "snapshot_timestamp"
    ):
        errors.append("manifest YouTube snapshot timestamp does not match corpus snapshot")

    ledger_record = (snapshot.get("sources") or {}).get("youtube_ledger") or {}
    ledger_path_value = ledger_record.get("path")
    ledger_digest = ledger_record.get("sha256")
    if not isinstance(ledger_path_value, str) or not ledger_path_value:
        errors.append("corpus snapshot lacks sources.youtube_ledger.path")
        return errors
    if not isinstance(ledger_digest, str) or not ledger_digest:
        errors.append("corpus snapshot lacks sources.youtube_ledger.sha256")
        return errors
    if manifest_youtube.get("source_ledger_sha256") != ledger_digest:
        errors.append("manifest YouTube ledger digest does not match corpus snapshot")
    ledger_path = _resolve_declared_path(ledger_path_value, manifest_path)
    try:
        ledger_bytes = ledger_path.read_bytes()
        ledger = json.loads(ledger_bytes)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(
            f"could not read YouTube ledger {relative(ledger_path)}: {type(exc).__name__}"
        )
        return errors
    if sha256_bytes(ledger_bytes) != ledger_digest:
        errors.append("corpus snapshot YouTube ledger digest does not match exact ledger bytes")
    ledger_channel = ledger.get("channel") or {}
    for manifest_key, channel_key in channel_keys.items():
        if manifest_youtube.get(manifest_key) != ledger_channel.get(channel_key):
            errors.append(
                f"manifest youtube.{manifest_key} does not match ledger channel.{channel_key}"
            )
    if manifest_youtube.get("snapshot_timestamp") != ledger.get("created_at"):
        errors.append("manifest YouTube snapshot timestamp does not match ledger created_at")
    if (ledger.get("source") or {}).get("scope") != "all_channel":
        errors.append("YouTube ledger source scope must equal all_channel")
    return errors


def validate_manifest_document(
    path: Path,
    approval_path: Path | None = None,
    release_readiness_path: Path | None = None,
    *,
    validation_mode: str = "preapproval",
) -> tuple[dict[str, Any], dict[str, Any]]:
    _, manifest, digest = read_manifest_document(path)
    approval = None
    approval_sha256 = None
    if approval_path is not None:
        if not approval_path.exists():
            raise ValueError(f"approval file not found: {approval_path}")
        approval_bytes = approval_path.read_bytes()
        approval_sha256 = sha256_bytes(approval_bytes)
        approval = yaml.safe_load(approval_bytes)
        if not isinstance(approval, dict):
            raise ValueError("approval must contain a YAML object")
    release_readiness = None
    release_readiness_sha256 = None
    if release_readiness_path is not None:
        if not release_readiness_path.exists():
            raise ValueError(
                f"release_readiness gate artifact not found: {release_readiness_path}"
            )
        release_readiness_bytes = release_readiness_path.read_bytes()
        release_readiness_sha256 = sha256_bytes(release_readiness_bytes)
        release_readiness = yaml.safe_load(release_readiness_bytes)
        if not isinstance(release_readiness, dict):
            raise ValueError("release_readiness gate must contain a YAML object")
    errors = validate_manifest_data(
        manifest,
        manifest_path=path,
        manifest_sha256=digest,
        approval=approval,
        approval_path=approval_path,
        release_readiness=release_readiness,
        release_readiness_path=release_readiness_path,
        validation_mode=validation_mode,
    )
    errors.extend(validate_snapshot_binding(manifest, path))
    result = {
        "valid": not errors,
        "manifest": relative(path),
        "manifest_sha256": digest,
        "approval": relative(approval_path) if approval_path else None,
        "approval_sha256": approval_sha256,
        "release_readiness": (
            relative(release_readiness_path) if release_readiness_path else None
        ),
        "release_readiness_sha256": release_readiness_sha256,
        "validation_mode": validation_mode,
        "errors": errors,
    }
    return manifest, result


def validate_manifest(
    path: Path,
    approval_path: Path | None = None,
    release_readiness_path: Path | None = None,
    *,
    validation_mode: str = "preapproval",
) -> dict[str, Any]:
    _, result = validate_manifest_document(
        path,
        approval_path,
        release_readiness_path,
        validation_mode=validation_mode,
    )
    return result


def generate_decision_report_document(manifest_path: Path) -> tuple[str, str]:
    manifest, validation = validate_manifest_document(manifest_path)
    if not validation["valid"]:
        raise ValueError(
            "manifest is invalid:\n- " + "\n- ".join(validation["errors"])
        )
    artifacts = {item["artifact_id"]: item for item in manifest["artifacts"]}
    digest = validation["manifest_sha256"]

    lines = [
        "# Rooted Layers Portfolio Decision Report",
        "",
        f"Manifest version: `{manifest['portfolio_version']}`  ",
        f"Exact manifest SHA-256: `{digest}`  ",
        "Approval state: **PENDING — no public changes are authorized**",
        "",
        "## Proposed Homepage",
        "",
        "### Flagship",
        "",
    ]
    flagship_ids = manifest["homepage"].get("flagship_artifact_ids") or []
    supporting_ids = manifest["homepage"].get("supporting_artifact_ids") or []
    if not flagship_ids:
        lines.append("No essay currently meets the flagship bar.")
    for artifact_id in flagship_ids:
        item = artifacts[artifact_id]
        lines.append(f"- [{item['title']}]({item['current_url']}) — {item['rationale']}")
    lines.extend(["", "### Supporting", ""])
    if not supporting_ids:
        lines.append("No supporting essay is currently proposed.")
    for artifact_id in supporting_ids:
        item = artifacts[artifact_id]
        lines.append(f"- [{item['title']}]({item['current_url']}) — {item['rationale']}")

    youtube = manifest["youtube"]
    video_by_id = {
        item["platform_id"]: item
        for item in manifest["artifacts"]
        if item["platform"] == "YOUTUBE"
    }
    lines.extend(["", "## Proposed YouTube Playlist", ""])
    selected = youtube.get("selected_video_ids") or []
    if len(selected) < 2:
        lines.append("No playlist will be created because fewer than two videos meet the bar.")
    else:
        lines.append(f"Title: **{PLAYLIST_TITLE}**")
        lines.append("")
        for video_id in selected:
            item = video_by_id[video_id]
            lines.append(f"- [{item['title']}]({item['current_url']})")

    lines.extend(["", "## Exact YouTube Visibility Changes", ""])
    unlists = youtube.get("unlist_video_ids") or []
    if not unlists:
        lines.append("No visibility changes are proposed.")
    for video_id in unlists:
        item = video_by_id[video_id]
        lines.append(
            f"- `public → unlisted` [{item['title']}]({item['current_url']}) — "
            f"{item['rationale']}"
        )

    lines.extend(["", "## Unresolved Evidence", ""])
    unresolved = [
        item
        for item in manifest["artifacts"]
        if (item.get("source_lineage") or {}).get("status") != "RESOLVED"
        or (item.get("factual_risk") or {}).get("status") in {"HIGH", "UNRESOLVED_HIGH"}
    ]
    if not unresolved:
        lines.append("None affecting the proposed selections.")
    for item in unresolved:
        lines.append(f"- **{item['title']}** — {item['source_lineage'].get('notes', 'Unresolved')}")

    lines.extend(["", "## Questions Requiring A Decision", ""])
    questions = manifest.get("unresolved_questions") or []
    if not questions:
        lines.append("None.")
    for index, question in enumerate(questions, start=1):
        lines.append(f"{index}. {question}")

    lines.extend(
        [
            "",
            "## Approval Boundary",
            "",
            "One approval must cover this exact digest, the mirror changes, the "
            "professional-site publication link, playlist action, and every listed "
            "YouTube unlisting. Any manifest edit changes the digest and invalidates approval.",
            "",
        ]
    )
    return "\n".join(lines), digest


def generate_decision_report(manifest_path: Path) -> str:
    rendered, _ = generate_decision_report_document(manifest_path)
    return rendered


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    snapshot = subparsers.add_parser("snapshot", help="Build the read-only corpus snapshot")
    snapshot.add_argument("--output", type=Path, default=DEFAULT_SNAPSHOT)

    validate = subparsers.add_parser("validate", help="Validate a portfolio manifest")
    validate.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    validate.add_argument("--approval", type=Path)
    validate.add_argument("--release-readiness", type=Path)
    validate.add_argument(
        "--mode",
        choices=sorted(VALIDATION_MODES),
        default="preapproval",
        help="preapproval permits pending mutation states; apply-ready requires exact approvals",
    )

    report = subparsers.add_parser("report", help="Render the human decision report")
    report.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    report.add_argument("--output", type=Path, default=DEFAULT_REPORT)

    digest = subparsers.add_parser("digest", help="Print the exact manifest SHA-256")
    digest.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "snapshot":
        snapshot = build_snapshot()
        write_json(args.output, snapshot)
        print(json.dumps({"output": relative(args.output), "snapshot": snapshot}, indent=2))
        return
    if args.command == "validate":
        result = validate_manifest(
            args.manifest,
            args.approval,
            args.release_readiness,
            validation_mode=args.mode,
        )
        print(json.dumps(result, indent=2))
        if not result["valid"]:
            raise SystemExit(1)
        return
    if args.command == "report":
        rendered, digest = generate_decision_report_document(args.manifest)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(json.dumps({"output": relative(args.output), "manifest_sha256": digest}, indent=2))
        return
    if args.command == "digest":
        print(manifest_digest(args.manifest))


if __name__ == "__main__":
    main()
