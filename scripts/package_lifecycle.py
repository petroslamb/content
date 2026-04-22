#!/usr/bin/env python3
"""
Shared lifecycle guardrails for package-stage and governing-brief checks.
"""

from __future__ import annotations

import json
from pathlib import Path
import re

import yaml

from essay_iteration_support import (
    PACKET_SCHEMA_VERSION,
    build_packet_paths,
    candidate_text_looks_scaffold,
    packet_schema_version,
    repo_relpath,
    resolve_live_draft,
    resolve_nearest_blueprint_path,
)
from lifecycle import STAGES, load_status_ref, split_frontmatter


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


def parse_markdown_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text()
    frontmatter_text, body = split_frontmatter(text)
    frontmatter = yaml.safe_load(frontmatter_text) or {}
    if not isinstance(frontmatter, dict):
        raise ValueError(f"Frontmatter in {path} must be a mapping.")
    return frontmatter, body


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
    prewrite_gate_path: Path | None = None
    prewrite_gate_verdict: str | None = None
    ceiling_report_path: Path | None = None
    ceiling_report_verdict: str | None = None
    candidate_opened_before_prewrite_clearance = False
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

    if current_stage == "essay_iteration" and packet_scaffold_exists and packet_manifest_path is not None:
        try:
            packet = json.loads(packet_manifest_path.read_text())
            output_paths = packet.get("output_paths", {})
            schema_version = packet_schema_version(packet)
        except (json.JSONDecodeError, ValueError):
            packet = {}
            output_paths = {}
            schema_version = 0

        prewrite_relpath = output_paths.get("prewrite_gate")
        if schema_version < PACKET_SCHEMA_VERSION or not isinstance(prewrite_relpath, str):
            issues.append(
                _issue(
                    "essay_iteration_prewrite_gate_missing",
                    "warning",
                    "essay_iteration packet exists, but it has no canonical prewrite gate. Refresh the packet scaffold to the current schema and fill the prewrite gate before claiming draft readiness.",
                )
            )
        else:
            prewrite_gate_path = (Path(__file__).resolve().parents[1] / prewrite_relpath).resolve()
            if not prewrite_gate_path.exists():
                issues.append(
                    _issue(
                        "essay_iteration_prewrite_gate_missing",
                        "warning",
                        "essay_iteration packet exists, but the prewrite-gate artifact is missing.",
                    )
                )
            else:
                try:
                    prewrite_frontmatter, _ = parse_markdown_frontmatter(prewrite_gate_path)
                    prewrite_gate_verdict = prewrite_frontmatter.get("writability_verdict")
                except ValueError:
                    prewrite_frontmatter = {}
                    prewrite_gate_verdict = None

                if prewrite_gate_verdict in (None, "", "pending"):
                    issues.append(
                        _issue(
                            "essay_iteration_prewrite_gate_missing",
                            "warning",
                            "essay_iteration packet exists, but the prewrite gate is still unresolved or left at pending.",
                        )
                    )
                elif prewrite_gate_verdict == "not_yet_writable":
                    issues.append(
                        _issue(
                            "essay_iteration_prewrite_gate_blocked",
                            "warning",
                            "essay_iteration prewrite gate says the package is not yet writable. Resolve the dominant blocker before opening or clearing a candidate.",
                        )
                    )

                candidate_relpath = packet.get("candidate_path")
                if isinstance(candidate_relpath, str):
                    candidate_path = (Path(__file__).resolve().parents[1] / candidate_relpath).resolve()
                    if candidate_path.exists() and not candidate_text_looks_scaffold(candidate_path.read_text()):
                        if prewrite_gate_verdict != "writable":
                            candidate_opened_before_prewrite_clearance = True
                            issues.append(
                                _issue(
                                    "essay_iteration_candidate_opened_before_prewrite_clearance",
                                    "warning",
                                    "A bounded candidate has been opened before the essay prewrite gate cleared writability.",
                                )
                            )

                review_relpath = output_paths.get("replacement_review")
                decision_relpath = output_paths.get("decision")
                ceiling_report_relpath = output_paths.get("ceiling_report")
                stop_gate_fired = False
                if isinstance(review_relpath, str) and isinstance(decision_relpath, str):
                    review_path = (Path(__file__).resolve().parents[1] / review_relpath).resolve()
                    decision_path = (Path(__file__).resolve().parents[1] / decision_relpath).resolve()
                    if review_path.exists() and decision_path.exists():
                        try:
                            review_frontmatter, _ = parse_markdown_frontmatter(review_path)
                            decision_frontmatter, _ = parse_markdown_frontmatter(decision_path)
                            stop_gate_fired = (
                                review_frontmatter.get("north_star_verdict") == "below_north_star"
                                and (
                                    review_frontmatter.get("continue_iteration") is False
                                    or decision_frontmatter.get("rewrite_mode") == "stop_flagship_iteration"
                                    or decision_frontmatter.get("stop_gate_status") == "fired"
                                )
                            )
                        except ValueError:
                            stop_gate_fired = False

                if stop_gate_fired:
                    if schema_version < PACKET_SCHEMA_VERSION or not isinstance(ceiling_report_relpath, str):
                        issues.append(
                            _issue(
                                "essay_iteration_ceiling_report_missing",
                                "warning",
                                "The stop gate fired, but the current packet has no canonical ceiling report. Refresh the packet scaffold to the current schema and fill the donor report before routing into pivot work.",
                            )
                        )
                    else:
                        ceiling_report_path = (Path(__file__).resolve().parents[1] / ceiling_report_relpath).resolve()
                        if not ceiling_report_path.exists():
                            issues.append(
                                _issue(
                                    "essay_iteration_ceiling_report_missing",
                                    "warning",
                                    "The stop gate fired, but the ceiling-report artifact is missing.",
                                )
                            )
                        else:
                            try:
                                ceiling_report_frontmatter, _ = parse_markdown_frontmatter(ceiling_report_path)
                                ceiling_report_verdict = ceiling_report_frontmatter.get("ceiling_verdict")
                            except ValueError:
                                ceiling_report_frontmatter = {}
                                ceiling_report_verdict = None

                            if ceiling_report_verdict in (None, "", "pending"):
                                issues.append(
                                    _issue(
                                        "essay_iteration_ceiling_report_missing",
                                        "warning",
                                        "The stop gate fired, but the ceiling report is still unresolved or left at pending.",
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
        "prewrite_gate_path": repo_relpath(prewrite_gate_path),
        "prewrite_gate_verdict": prewrite_gate_verdict,
        "ceiling_report_path": repo_relpath(ceiling_report_path),
        "ceiling_report_verdict": ceiling_report_verdict,
        "candidate_opened_before_prewrite_clearance": candidate_opened_before_prewrite_clearance,
        "issues": issues,
        "warning_count": len(issues),
        "blocking_count": sum(1 for issue in issues if issue["blocking"]),
    }
