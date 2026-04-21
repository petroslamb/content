#!/usr/bin/env python3
"""
Shared lifecycle guardrails for package-stage and governing-brief checks.
"""

from __future__ import annotations

from pathlib import Path
import re

from essay_iteration_support import (
    build_packet_paths,
    repo_relpath,
    resolve_live_draft,
    resolve_nearest_blueprint_path,
)
from lifecycle import STAGES, load_status_ref


STAGE_LABEL_ALIASES = {
    "paper_intake": {"paper intake"},
    "research": {"research", "research and paper intake", "paper intake and research"},
    "essay_iteration": {"essay iteration"},
    "notebooklm_artifacts": {"notebooklm artifacts"},
    "article_polish": {"article polish"},
    "substack_publishing": {"substack publishing"},
    "archive_sync": {"archive sync"},
    "youtube_production": {"youtube production"},
    "distribution": {"distribution"},
}

CURRENT_STAGE_RE = re.compile(r"^\s*[-*]?\s*Current stage:\s*(.+?)\s*$", re.IGNORECASE)


def normalize_stage_label(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.strip().lower()).strip()


def current_stage_from_status(status_data: dict) -> str | None:
    stages = status_data.get("stages", {})
    for stage in STAGES:
        if not stages.get(stage, {}).get("done", False):
            return stage
    return None


def parse_readme_current_stage(package_path: Path) -> str | None:
    readme_path = package_path / "README.md"
    if not readme_path.exists():
        return None
    for line in readme_path.read_text().splitlines():
        match = CURRENT_STAGE_RE.match(line)
        if match:
            return match.group(1).strip()
    return None


def _within_package(package_path: Path, candidate: Path) -> bool:
    try:
        candidate.resolve().relative_to(package_path.resolve())
        return True
    except ValueError:
        return False


def resolve_blueprint_config_path(package_path: Path, status_data: dict) -> dict:
    config = status_data.get("config", {})
    raw_value = config.get("blueprint_path")
    result = {
        "config_value": raw_value,
        "config_path": None,
        "config_issue": None,
    }

    if raw_value in (None, ""):
        result["config_issue"] = "missing"
        return result

    if not isinstance(raw_value, str):
        result["config_issue"] = "invalid_type"
        return result

    candidate = (package_path / raw_value).resolve()
    if not _within_package(package_path, candidate):
        result["config_issue"] = "out_of_package"
        return result
    if not candidate.exists():
        result["config_issue"] = "missing_file"
        return result

    result["config_path"] = candidate
    return result


def resolve_governing_brief(package_path: Path, status_data: dict) -> dict:
    config_resolution = resolve_blueprint_config_path(package_path, status_data)
    config_path = config_resolution["config_path"]
    if config_path is not None:
        return {
            **config_resolution,
            "path": config_path,
            "source": "config",
        }

    fallback_path = resolve_nearest_blueprint_path(package_path, status_data)
    if fallback_path is not None:
        return {
            **config_resolution,
            "path": fallback_path,
            "source": "fallback",
        }

    return {
        **config_resolution,
        "path": None,
        "source": None,
    }


def resolve_packet_manifest_path(package_path: Path, status_data: dict) -> Path | None:
    live_draft_path = resolve_live_draft(package_path, status_data)
    revision = status_data.get("revision", 1)
    if live_draft_path is None or not isinstance(revision, int):
        return None
    return build_packet_paths(live_draft_path, revision)["manifest"]


def _issue(code: str, severity: str, message: str, *, blocking: bool = False) -> dict:
    return {
        "code": code,
        "severity": severity,
        "blocking": blocking,
        "message": message,
    }


def inspect_package_lifecycle(package_arg: str) -> dict:
    manifest_ref, status_data = load_status_ref(package_arg)
    package_path = manifest_ref.package_path
    current_stage = current_stage_from_status(status_data)
    readme_stage = parse_readme_current_stage(package_path)
    governing_brief = resolve_governing_brief(package_path, status_data)
    packet_manifest_path = resolve_packet_manifest_path(package_path, status_data)
    packet_scaffold_exists = bool(packet_manifest_path and packet_manifest_path.exists())
    issues: list[dict] = []

    if readme_stage and current_stage is not None:
        normalized_stage = normalize_stage_label(readme_stage)
        accepted = STAGE_LABEL_ALIASES.get(current_stage, {normalize_stage_label(current_stage)})
        if normalized_stage not in accepted:
            issues.append(
                _issue(
                    "readme_stage_mismatch",
                    "warning",
                    "Package README Current stage does not match the next lifecycle stage implied by status.yaml.",
                )
            )

    config_issue = governing_brief["config_issue"]
    if config_issue == "out_of_package":
        issues.append(
            _issue(
                "blueprint_path_out_of_package",
                "warning",
                "config.blueprint_path resolves outside the package root.",
            )
        )
    elif config_issue == "invalid_type":
        issues.append(
            _issue(
                "blueprint_path_invalid_type",
                "warning",
                "config.blueprint_path must be a package-relative string when present.",
            )
        )

    research_done = bool(status_data.get("stages", {}).get("research", {}).get("done", False))
    if research_done and governing_brief["config_path"] is None:
        if config_issue == "missing":
            issues.append(
                _issue(
                    "research_missing_blueprint_path",
                    "warning",
                    "research is marked done but status.yaml does not provide a resolvable config.blueprint_path.",
                )
            )
        elif config_issue == "missing_file":
            issues.append(
                _issue(
                    "research_blueprint_path_missing_file",
                    "warning",
                    "research is marked done but config.blueprint_path points to a missing file.",
                )
            )
        elif config_issue == "out_of_package":
            issues.append(
                _issue(
                    "research_blueprint_path_out_of_package",
                    "warning",
                    "research is marked done but config.blueprint_path leaves the package root.",
                )
            )
        elif config_issue == "invalid_type":
            issues.append(
                _issue(
                    "research_blueprint_path_invalid_type",
                    "warning",
                    "research is marked done but config.blueprint_path is not a package-relative string.",
                )
            )

    if current_stage == "essay_iteration" and governing_brief["path"] is None:
        issues.append(
            _issue(
                "essay_iteration_missing_governing_brief",
                "warning",
                "essay_iteration is the next stage, but no governing brief resolves from config.blueprint_path or the legacy blueprint fallback.",
                blocking=True,
            )
        )

    if current_stage == "essay_iteration" and not packet_scaffold_exists:
        issues.append(
            _issue(
                "essay_iteration_missing_packet_scaffold",
                "warning",
                "essay_iteration is the next stage, but the current revision has no packet scaffold manifest beside the live draft.",
            )
        )

    if current_stage == "research" and packet_scaffold_exists:
        issues.append(
            _issue(
                "research_has_packet_scaffold",
                "warning",
                "The current revision already has an essay-iteration packet scaffold while status.yaml still reports research as the next stage.",
            )
        )

    return {
        "package": manifest_ref.package_key,
        "current_stage": current_stage,
        "readme_current_stage": readme_stage,
        "governing_brief_path": repo_relpath(governing_brief["path"]),
        "governing_brief_source": governing_brief["source"],
        "blueprint_path_config": governing_brief["config_value"],
        "packet_manifest_path": repo_relpath(packet_manifest_path),
        "packet_scaffold_exists": packet_scaffold_exists,
        "issues": issues,
        "warning_count": len(issues),
        "blocking_count": sum(1 for issue in issues if issue["blocking"]),
    }
