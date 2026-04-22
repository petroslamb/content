#!/usr/bin/env python3
"""
Shared helpers for the Codex-facing harness surface.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

import yaml

from audit_package import audit_package, resolve_evidence_root
from check_research_exit_gate import validate_research_exit_gate
from essay_iteration_support import (
    ARCHIVE_ANCHOR_FIELDS,
    BLUEPRINT_HEADINGS,
    CEILING_REPORT_BODY_HEADINGS,
    CEILING_REPORT_FRONTMATTER_FIELDS,
    DECISION_REQUIRED_FOLLOW_THROUGH_PLACEHOLDER,
    NORTH_STAR_ESCALATION_SCHEMA_VERSION,
    PACKET_SCHEMA_VERSION,
    PASSAGE_ANCHOR_FIELDS,
    PREWRITE_BODY_HEADINGS,
    PREWRITE_FRONTMATTER_FIELDS,
    build_packet_paths,
    candidate_text_looks_scaffold,
    describe_packet_paths,
    packet_schema_version,
    resolve_companion_path,
    resolve_evidence_surface as resolve_essay_evidence_surface,
    resolve_governing_brief_path,
    resolve_leaf_readme,
    resolve_live_draft,
    resolve_nearest_blueprint_path,
    resolve_parent_package_path,
    resolve_parent_package_readme,
    resolve_review_artifact_paths,
)
from lifecycle import (
    PUBLICATIONS_DIR,
    REPO_ROOT,
    STAGES,
    load_all_workflow_contracts,
    load_gate_contracts,
    load_pipeline_profiles,
    load_status_ref,
    load_workflow_contract,
    split_frontmatter,
)
from package_lifecycle import inspect_package_lifecycle
from research_exit_support import build_research_exit_gate_path, resolve_research_exit_gate_path


PACKAGE_JSON_PATH = REPO_ROOT / "package.json"
HARNESS_CONTRACT_PATH = REPO_ROOT / "harness_contract.yaml"
HARNESS_POLICY_PATH = REPO_ROOT / "harness_policy.yaml"
LOGS_DIR = REPO_ROOT / "reviewable-runs" / "logs"

REQUIRED_NPM_SCRIPTS = {
    "check",
    "check:essay-prewrite",
    "check:essay-iteration",
    "check:package-lifecycle",
    "check:workflow-model",
    "gate:check",
    "stage:next",
    "stage:resolve",
    "stage:run",
    "package:init",
    "workflow:resolve",
    "workflow:run",
    "check:harness",
}

POLICY_SECTIONS = {
    "read_only_allowed",
    "local_write_allowed",
    "auto_mark_done_allowed",
    "approval_required",
    "disallowed_without_explicit_user_request",
}

PATH_LIKE_SUFFIXES = (
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".pdf",
    ".txt",
    ".html",
    ".csv",
)

CLAIM_BOUNDARY_PATTERNS = (
    "*claim*authorization*.md",
    "*claim*state*.md",
    "*evidence*authorization*.md",
    "*contradiction*register*.md",
    "*provenance*.md",
    "*provenance*.json",
    "*ledger*.md",
)

RELEASE_GATE_PATTERNS = (
    "*release-gate*.md",
    "release-gate.md",
    "*publication-readiness*.md",
)

PIVOT_REFRAME_PATTERNS = (
    "*post-ceiling-reframe*.md",
)

CEILING_REPORT_PATTERNS = (
    "*ceiling-report-r*.md",
    "*ceiling-report*.md",
)

PIVOT_PROCESS_CAPTURE_PATTERNS = (
    "*process-capture*.md",
)

PIVOT_GROUNDING_PATTERNS = (
    "*pivot-grounding-review*.md",
)

PIVOT_SLATE_PATTERNS = (
    "*pivot-slate*.md",
)

PIVOT_NEXT_CANDIDATE_PATTERNS = (
    "*next-pivot-candidate*.md",
)

PIVOT_RESEARCH_DELTA_PATTERNS = (
    "*research-delta*.md",
)

PIVOT_CONSEQUENCE_PATTERNS = (
    "*consequence-pass*.md",
    "*consequence-pressure*.md",
)

PIVOT_COMPARATIVE_RERANK_PATTERNS = (
    "*comparative-rerank*.md",
)

PIVOT_DECISION_PATTERNS = (
    "*pivot-decision*.md",
)

PIVOT_NORTH_STAR_PATTERNS = (
    "*pivot-north-star-viability*.md",
)

PIVOT_BLOCKER_PATTERNS = (
    "*pivot-blocker*.md",
)


def repo_relpath(path: Path | None) -> str | None:
    if path is None:
        return None
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def load_yaml_file(path: Path) -> dict:
    data = yaml.safe_load(path.read_text()) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def load_package_scripts() -> dict[str, str]:
    package_json = json.loads(PACKAGE_JSON_PATH.read_text())
    scripts = package_json.get("scripts", {})
    if not isinstance(scripts, dict):
        raise ValueError("package.json scripts must be a JSON object.")
    return {str(key): str(value) for key, value in scripts.items()}


def load_harness_policy() -> dict:
    return load_yaml_file(HARNESS_POLICY_PATH)


def validate_harness_policy(policy: dict) -> list[str]:
    errors: list[str] = []
    missing = POLICY_SECTIONS - set(policy.keys())
    if missing:
        errors.append(f"harness_policy.yaml missing sections: {', '.join(sorted(missing))}")

    for section in POLICY_SECTIONS & set(policy.keys()):
        if not isinstance(policy[section], dict):
            errors.append(f"harness_policy.yaml section '{section}' must be a mapping.")

    stage_sections = [
        ("approval_required", "stages"),
        ("auto_mark_done_allowed", "denied_stages"),
        ("disallowed_without_explicit_user_request", "stages"),
    ]
    for section, key in stage_sections:
        values = policy.get(section, {}).get(key, [])
        if values is None:
            continue
        if not isinstance(values, list):
            errors.append(f"harness_policy.yaml {section}.{key} must be a list.")
            continue
        unknown = sorted(set(values) - set(STAGES))
        if unknown:
            errors.append(
                f"harness_policy.yaml {section}.{key} references unknown stages: {', '.join(unknown)}"
            )

    runner_modes = policy.get("auto_mark_done_allowed", {}).get("runner_modes", [])
    if runner_modes and not isinstance(runner_modes, list):
        errors.append("harness_policy.yaml auto_mark_done_allowed.runner_modes must be a list.")

    return errors


def build_harness_contract() -> dict:
    scripts = load_package_scripts()
    workflow_contracts = {}
    for workflow_id, workflow_contract in load_all_workflow_contracts().items():
        metadata = workflow_contract["metadata"]
        workflow_contracts[workflow_id] = {
            "workflow_doc": repo_relpath(workflow_contract["path"]),
            "workflow_kind": metadata["workflow_kind"],
            "stage_binding": metadata.get("stage_binding"),
            "stability": metadata["stability"],
            "runner_mode": metadata["runner_mode"],
            "launch_mode": metadata["launch_mode"],
            "default_skill": metadata["default_skill"],
            "approval_gate": metadata["approval_gate"],
            "required_context": metadata["required_context"],
            "expected_outputs": metadata["expected_outputs"],
            "done_when": metadata["done_when"],
            "launch_templates": metadata["launch_templates"],
            "packet_templates": metadata["packet_templates"],
            "validator_commands": metadata["validator_commands"],
            "judgment_policy": metadata["judgment_policy"],
            "prohibited_moves": metadata["prohibited_moves"],
        }
    stage_contracts = {stage: workflow_contracts[stage] for stage in STAGES}

    command_surface = {}
    for name in sorted(REQUIRED_NPM_SCRIPTS | {"status", "run"}):
        command_surface[name] = {
            "entrypoint": f"npm run {name}",
            "script": scripts.get(name),
        }

    return {
        "version": 2,
        "harness_target": "codex",
        "autonomy_scope": "local-first",
        "policy_file": "harness_policy.yaml",
        "sources_of_truth": {
            "lifecycle": "scripts/lifecycle.py",
            "workflow_frontmatter": "workflows/*/README.md",
            "gate_contracts": "gate_contracts.yaml",
            "pipeline_profiles": "pipeline_profiles.yaml",
            "package_state": "publications/**/status.yaml",
            "npm_scripts": "package.json",
        },
        "paths": {
            "publications_dir": "publications",
            "workflows_dir": "workflows",
            "logs_dir": "reviewable-runs/logs",
        },
        "interfaces": command_surface,
        "package_init": {
            "default_first_stage": "research",
            "accepted_inputs": [
                "--idea",
                "--slug",
                "--from-topic-packet",
            ],
            "status_config_fields": [
                "markdown_path",
                "discovery_packet_path",
            ],
            "scaffold": [
                "README.md",
                "<slug>.md",
                "status.yaml",
                "papers/",
                "papers/markdown/",
                "papers/index.md",
                "artifacts/",
                "archive/",
            ],
        },
        "lifecycle": {
            "stage_order": STAGES,
            "stages": stage_contracts,
        },
        "workflows": workflow_contracts,
        "gates": load_gate_contracts(),
        "pipeline_profiles": load_pipeline_profiles(),
    }


def find_package_readme(package_path: Path) -> Path | None:
    candidate = package_path / "README.md"
    if candidate.exists():
        return candidate
    return None


def resolve_config_value(status_data: dict, key: str) -> str | int | bool | None:
    return status_data.get("config", {}).get(key)


def resolve_config_context(status_data: dict, key: str) -> dict:
    value = resolve_config_value(status_data, key)
    name = f"config.{key}"
    if value in (None, ""):
        return {"name": name, "status": "missing", "blocking": True}

    if isinstance(value, str) and not value.startswith("http"):
        candidate = REPO_ROOT / value
        if candidate.exists():
            return {
                "name": name,
                "status": "resolved",
                "blocking": False,
                "value": repo_relpath(candidate),
            }
        if value.endswith(PATH_LIKE_SUFFIXES) or "/" in value:
            return {"name": name, "status": "missing", "blocking": True, "value": value}

    return {"name": name, "status": "resolved", "blocking": False, "value": value}


def resolve_markdown_path(package_path: Path, status_data: dict) -> Path | None:
    return resolve_live_draft(package_path, status_data)


def resolve_artifacts_dir(package_path: Path, status_data: dict) -> Path | None:
    artifacts_path = resolve_config_value(status_data, "artifacts_path")
    if isinstance(artifacts_path, str):
        candidate = REPO_ROOT / artifacts_path
        if candidate.exists():
            return candidate
    candidate = package_path / "artifacts"
    if candidate.exists():
        return candidate
    return None


def resolve_evidence_dir(package_path: Path, status_data: dict) -> Path | None:
    evidence_root, _ = resolve_evidence_root(package_path, status_data)
    if evidence_root and evidence_root.exists():
        return evidence_root
    return None


def resolve_reference_surface(package_path: Path, status_data: dict) -> Path | None:
    evidence_root = resolve_evidence_dir(package_path, status_data)
    if not evidence_root:
        return None

    for relpath in ["index.md", "papers/index.md", "sources/index.md", "source-index.md"]:
        candidate = evidence_root / relpath
        if candidate.exists():
            return candidate
    return evidence_root


def resolve_notebook_identifier(status_data: dict) -> str | None:
    for key in ["notebooklm_notebook_id", "notebooklm_notebook_title", "notebook_title"]:
        value = resolve_config_value(status_data, key)
        if isinstance(value, (str, int)) and str(value).strip():
            return str(value)
    return None


def find_first_matching_file(root: Path, suffixes: tuple[str, ...]) -> Path | None:
    if not root.exists():
        return None
    for candidate in sorted(root.rglob("*")):
        if candidate.is_file() and candidate.suffix.lower() in suffixes:
            return candidate
    return None


def find_preferred_matching_file(root: Path, suffixes: tuple[str, ...]) -> Path | None:
    if not root.exists():
        return None
    suffix_priority = {suffix.lower(): index for index, suffix in enumerate(suffixes)}
    candidates = [
        candidate
        for candidate in sorted(root.rglob("*"))
        if candidate.is_file() and candidate.suffix.lower() in suffixes
    ]
    if not candidates:
        return None
    return min(
        candidates,
        key=lambda candidate: (
            suffix_priority.get(candidate.suffix.lower(), len(suffixes)),
            str(candidate),
        ),
    )


def parse_research_direction(package_path: Path) -> str | None:
    readme = resolve_leaf_readme(package_path)
    if not readme:
        return None
    for line in readme.read_text().splitlines():
        if line.startswith("Current idea:"):
            return line.split(":", 1)[1].strip()
        if line.startswith("Research direction:"):
            return line.split(":", 1)[1].strip()
    return None


def has_intake_candidates(package_path: Path) -> bool:
    papers_dir = package_path / "papers"
    if not papers_dir.exists():
        return False
    ignored = {
        papers_dir / "index.md",
    }
    for candidate in papers_dir.rglob("*"):
        if candidate.is_dir():
            continue
        if candidate in ignored:
            continue
        if candidate.parent == papers_dir / "markdown":
            continue
        return True
    return False


def is_idea_only_package(package_path: Path, status_data: dict) -> bool:
    if any(stage_data.get("done") for stage_data in status_data.get("stages", {}).values()):
        return False
    if has_intake_candidates(package_path):
        return False
    if not find_package_readme(package_path):
        return False
    return resolve_markdown_path(package_path, status_data) is not None


def next_stage_for_package(package_path: Path, status_data: dict) -> str | None:
    if is_idea_only_package(package_path, status_data):
        return "research"
    for stage in STAGES:
        if not status_data.get("stages", {}).get(stage, {}).get("done", False):
            return stage
    return None


def resolve_context_item(item: str, package_path: Path, status_data: dict) -> dict:
    if item.startswith("config."):
        return resolve_config_context(status_data, item.split(".", 1)[1])

    if item == "package README or leaf README":
        readme = resolve_leaf_readme(package_path)
        if readme:
            return {"name": item, "status": "resolved", "blocking": False, "value": repo_relpath(readme)}
        return {"name": item, "status": "missing", "blocking": True}

    if item == "leaf package README":
        readme = resolve_leaf_readme(package_path)
        if readme:
            return {"name": item, "status": "resolved", "blocking": False, "value": repo_relpath(readme)}
        return {"name": item, "status": "missing", "blocking": True}

    if item == "parent umbrella README when present":
        readme = resolve_parent_package_readme(package_path, status_data)
        if readme:
            return {"name": item, "status": "resolved", "blocking": False, "value": repo_relpath(readme)}
        return {"name": item, "status": "advisory", "blocking": False}

    if item == "companion when present":
        companion = resolve_companion_path(package_path)
        if companion:
            return {"name": item, "status": "resolved", "blocking": False, "value": repo_relpath(companion)}
        return {"name": item, "status": "advisory", "blocking": False}

    if item == "nearest blueprint when present":
        blueprint = resolve_nearest_blueprint_path(package_path, status_data)
        if blueprint:
            return {"name": item, "status": "resolved", "blocking": False, "value": repo_relpath(blueprint)}
        return {"name": item, "status": "advisory", "blocking": False}

    if item == "governing brief from config.blueprint_path or fallback blueprint":
        governing_brief = resolve_governing_brief_path(package_path, status_data)
        if governing_brief:
            return {"name": item, "status": "resolved", "blocking": False, "value": repo_relpath(governing_brief)}
        return {"name": item, "status": "missing", "blocking": True}

    if item == "nearest review artifacts when present":
        review_artifacts = resolve_review_artifact_paths(package_path, status_data)
        if review_artifacts:
            return {
                "name": item,
                "status": "resolved",
                "blocking": False,
                "value": [repo_relpath(path) for path in review_artifacts],
            }
        return {"name": item, "status": "advisory", "blocking": False}

    if item == "current research question or thesis direction":
        direction = parse_research_direction(package_path)
        if direction:
            return {"name": item, "status": "resolved", "blocking": False, "value": direction}
        return {"name": item, "status": "missing", "blocking": True}

    if item == "package evidence surface for shortlisted papers":
        evidence_root = resolve_evidence_dir(package_path, status_data)
        if evidence_root:
            return {"name": item, "status": "resolved", "blocking": False, "value": repo_relpath(evidence_root)}
        return {"name": item, "status": "missing", "blocking": True}

    if item == "target evidence surface or source index":
        reference_surface = resolve_reference_surface(package_path, status_data)
        if reference_surface:
            return {"name": item, "status": "resolved", "blocking": False, "value": repo_relpath(reference_surface)}
        return {"name": item, "status": "missing", "blocking": True}

    if item == "paper files or source URLs to intake":
        if has_intake_candidates(package_path):
            return {"name": item, "status": "resolved", "blocking": False, "value": repo_relpath(package_path / "papers")}
        return {"name": item, "status": "missing", "blocking": True}

    if item == "canonical live draft":
        markdown_path = resolve_markdown_path(package_path, status_data)
        if markdown_path:
            return {"name": item, "status": "resolved", "blocking": False, "value": repo_relpath(markdown_path)}
        return {"name": item, "status": "missing", "blocking": True}

    if item == "package artifact surface with NotebookLM or local media outputs":
        artifacts_dir = resolve_artifacts_dir(package_path, status_data)
        if artifacts_dir:
            return {"name": item, "status": "resolved", "blocking": False, "value": repo_relpath(artifacts_dir)}
        return {"name": item, "status": "missing", "blocking": True}

    if item == "current references and supporting links":
        reference_surface = resolve_reference_surface(package_path, status_data)
        if reference_surface:
            return {"name": item, "status": "resolved", "blocking": False, "value": repo_relpath(reference_surface)}
        return {"name": item, "status": "missing", "blocking": True}

    if item == "target NotebookLM notebook id or exact title":
        notebook_id = resolve_notebook_identifier(status_data)
        if notebook_id:
            return {"name": item, "status": "resolved", "blocking": False, "value": notebook_id}
        return {"name": item, "status": "missing", "blocking": True}

    if item == "destination artifacts directory":
        artifacts_dir = resolve_artifacts_dir(package_path, status_data)
        if artifacts_dir:
            return {"name": item, "status": "resolved", "blocking": False, "value": repo_relpath(artifacts_dir)}
        return {"name": item, "status": "missing", "blocking": True}

    if item == "existing Substack draft or publish target":
        post_id = resolve_config_value(status_data, "substack_post_id")
        if post_id is not None:
            return {"name": item, "status": "resolved", "blocking": False, "value": f"substack_post_id={post_id}"}
        slug = resolve_config_value(status_data, "substack_slug")
        if slug:
            return {"name": item, "status": "resolved", "blocking": False, "value": f"substack_slug={slug}"}
        return {"name": item, "status": "missing", "blocking": True}

    if item == "repo root environment with archive scripts available":
        archive_script = REPO_ROOT / "scripts" / "sync_substack_archive.py"
        if archive_script.exists() and PACKAGE_JSON_PATH.exists():
            return {"name": item, "status": "resolved", "blocking": False, "value": repo_relpath(archive_script)}
        return {"name": item, "status": "missing", "blocking": True}

    if item == "up-to-date publication metadata or recently published post":
        metadata_path = REPO_ROOT / "publication_strategy_and_archive" / "substack_archive" / "metadata.json"
        if metadata_path.exists():
            return {"name": item, "status": "resolved", "blocking": False, "value": repo_relpath(metadata_path)}
        return {"name": item, "status": "missing", "blocking": True}

    if item == "canonical audio narration":
        search_root = resolve_artifacts_dir(package_path, status_data) or package_path
        audio_path = find_first_matching_file(search_root, (".mp3", ".m4a", ".wav"))
        if audio_path:
            return {"name": item, "status": "resolved", "blocking": False, "value": repo_relpath(audio_path)}
        return {"name": item, "status": "missing", "blocking": True}

    if item == "slide images or PDFs":
        search_root = resolve_artifacts_dir(package_path, status_data) or package_path
        slide_path = find_first_matching_file(search_root, (".pdf", ".png", ".jpg", ".jpeg"))
        if slide_path:
            return {"name": item, "status": "resolved", "blocking": False, "value": repo_relpath(slide_path)}
        return {"name": item, "status": "missing", "blocking": True}

    if item == "timed captions or transcript inputs":
        search_root = resolve_artifacts_dir(package_path, status_data) or package_path
        transcript_path = find_preferred_matching_file(
            search_root, (".srt", ".vtt", ".txt", ".json")
        )
        if transcript_path:
            return {"name": item, "status": "resolved", "blocking": False, "value": repo_relpath(transcript_path)}
        return {"name": item, "status": "missing", "blocking": True}

    return {"name": item, "status": "advisory", "blocking": False}


def resolve_required_context(package_path: Path, status_data: dict, required_context: list[str]) -> list[dict]:
    return [resolve_context_item(item, package_path, status_data) for item in required_context]


def workflow_requires_approval(workflow_id: str, metadata: dict, policy: dict) -> bool:
    if metadata.get("approval_gate") != "none":
        return True
    approval_stages = policy.get("approval_required", {}).get("stages", [])
    stage_binding = metadata.get("stage_binding")
    return stage_binding in approval_stages or workflow_id in approval_stages


def compute_workflow_capabilities(
    workflow_id: str,
    metadata: dict,
    required_context: list[dict],
    policy: dict,
) -> tuple[bool, bool, list[str]]:
    blocking_issues = []
    missing_context = [item["name"] for item in required_context if item["status"] == "missing" and item.get("blocking")]
    blocking_issues.extend(f"Missing required context: {item}" for item in missing_context)

    requires_approval = workflow_requires_approval(workflow_id, metadata, policy)
    scaffold_only_execute = (
        metadata["runner_mode"] == "hybrid" and metadata["launch_mode"] == "scaffold_only"
    )
    runner_allows_execute = metadata["runner_mode"] == "scripted" or scaffold_only_execute

    if not runner_allows_execute:
        blocking_issues.append(
            f"Runner mode '{metadata['runner_mode']}' with launch_mode '{metadata['launch_mode']}' is not directly executable in Phase 1.5; resolve it or emit a launch pack."
        )

    approval_blocks_execute = requires_approval and not scaffold_only_execute

    if metadata.get("stage_binding") in policy.get("approval_required", {}).get("stages", []) and approval_blocks_execute:
        blocking_issues.append(
            f"Policy requires explicit approval before unattended execution of '{workflow_id}'."
        )

    can_execute = (
        runner_allows_execute
        and not missing_context
        and not approval_blocks_execute
    )
    return requires_approval, can_execute, blocking_issues


def compute_stage_capabilities(stage: str, metadata: dict, required_context: list[dict], policy: dict) -> tuple[bool, bool, list[str]]:
    return compute_workflow_capabilities(stage, metadata, required_context, policy)


def auto_mark_done_allowed(stage: str, metadata: dict, policy: dict) -> bool:
    allowed_modes = policy.get("auto_mark_done_allowed", {}).get("runner_modes", [])
    denied_stages = set(policy.get("auto_mark_done_allowed", {}).get("denied_stages", []))
    return metadata["runner_mode"] in allowed_modes and stage not in denied_stages


def build_stage_suggested_commands(package_key: str, stage: str, can_execute: bool) -> list[str]:
    commands = [
        f"npm run stage:resolve -- --package {package_key} --stage {stage} --format json",
    ]
    if can_execute:
        commands.append(
            f"npm run stage:run -- --package {package_key} --stage {stage} --format json"
        )
    else:
        commands.append(
            f"npm run stage:resolve -- --package {package_key} --stage {stage} --emit-launch-pack --format json"
        )
    return commands


def workflow_recommended_gates(workflow_id: str) -> list[str]:
    mapping = {
        "topic_discovery": ["topic_viability"],
        "research": ["research_exit"],
        "essay_iteration": ["essay_prewrite", "replacement_north_star"],
        "post_ceiling_pivot": ["pivot_research_grounding", "pivot_north_star_viability"],
        "release_gate": ["release_readiness"],
        "article_polish": ["release_readiness"],
        "substack_publishing": ["release_readiness"],
        "distribution": ["release_readiness"],
    }
    return mapping.get(workflow_id, [])


def build_workflow_suggested_commands(
    workflow_id: str,
    can_execute: bool,
    package_key: str | None = None,
    packet_path: Path | None = None,
) -> list[str]:
    suffix = []
    if package_key:
        suffix.extend(["--package", package_key])
    if packet_path:
        suffix.extend(["--packet", repo_relpath(packet_path)])
    suffix_args = " " + " ".join(suffix) if suffix else ""
    commands = [
        f"npm run workflow:resolve -- --workflow {workflow_id}{suffix_args} --format json",
    ]
    commands.append(
        f"npm run workflow:run -- --workflow {workflow_id}{suffix_args} --format json"
    )
    if not can_execute:
        commands.append(
            f"npm run workflow:run -- --workflow {workflow_id}{suffix_args} --emit-launch-pack --format json"
        )
    return commands


def open_required_context(required_context: list[str]) -> list[dict]:
    return [{"name": item, "status": "open", "blocking": False} for item in required_context]


def build_resolution_args(package_key: str, status_data: dict) -> dict:
    config = status_data.get("config", {})
    package_path = f"publications/{package_key}"
    return {
        "package_key": package_key,
        "package_name": package_key.split("/")[-1],
        "package_path": package_path,
        "publication": status_data.get("publication", package_key.split("/")[-1]),
        **config,
    }


def render_command_templates(templates: list[str], package_key: str, status_data: dict) -> list[str]:
    resolved_args = build_resolution_args(package_key, status_data)
    commands = []
    for template in templates:
        commands.append(template.format(**resolved_args))
    return commands


def resolve_packet_template_paths(packet_templates: list[str]) -> list[str]:
    resolved: list[str] = []
    for template in packet_templates:
        candidate = (REPO_ROOT / template).resolve()
        resolved.append(repo_relpath(candidate))
    return resolved


def build_package_context_paths(package_path: Path, status_data: dict) -> dict:
    live_draft = resolve_markdown_path(package_path, status_data)
    leaf_readme = resolve_leaf_readme(package_path)
    parent_path = resolve_parent_package_path(package_path, status_data)
    parent_readme = resolve_parent_package_readme(package_path, status_data)
    companion = resolve_companion_path(package_path)
    governing_brief = resolve_governing_brief_path(package_path, status_data)
    blueprint = resolve_nearest_blueprint_path(package_path, status_data)
    review_artifacts = resolve_review_artifact_paths(package_path, status_data)
    evidence_surface = resolve_essay_evidence_surface(package_path, status_data)

    return {
        "live_draft_path": repo_relpath(live_draft),
        "leaf_readme_path": repo_relpath(leaf_readme),
        "parent_package_path": repo_relpath(parent_path),
        "parent_package_readme_path": repo_relpath(parent_readme),
        "companion_path": repo_relpath(companion),
        "governing_brief_path": repo_relpath(governing_brief),
        "nearest_blueprint_path": repo_relpath(blueprint),
        "review_artifact_paths": [repo_relpath(path) for path in review_artifacts],
        "evidence_surface_path": repo_relpath(evidence_surface),
    }


def find_package_artifact(package_path: Path, patterns: tuple[str, ...]) -> Path | None:
    for pattern in patterns:
        for candidate in sorted(package_path.glob(pattern)):
            if candidate.is_file():
                return candidate
    return None


def find_package_artifacts(package_path: Path, patterns: tuple[str, ...]) -> list[Path]:
    matches: list[Path] = []
    for pattern in patterns:
        for candidate in sorted(package_path.glob(pattern)):
            if candidate.is_file() and candidate not in matches:
                matches.append(candidate)
    return matches


def find_active_pivot_artifact(package_path: Path, patterns: tuple[str, ...]) -> Path | None:
    search_roots = [
        package_path,
        package_path / "pivot",
        package_path / "pivot" / "active",
    ]
    for search_root in search_roots:
        if not search_root.exists():
            continue
        for pattern in patterns:
            for candidate in sorted(search_root.glob(pattern)):
                if candidate.is_file():
                    return candidate
    return None


def load_local_status_data(package_path: Path) -> dict:
    status_path = package_path / "status.yaml"
    if not status_path.exists():
        return {}
    data = yaml.safe_load(status_path.read_text()) or {}
    return data if isinstance(data, dict) else {}


def package_kind(package_path: Path) -> str | None:
    data = load_local_status_data(package_path)
    kind = data.get("kind")
    return kind if isinstance(kind, str) else None


def configured_leaf_packages(package_path: Path) -> list[str]:
    data = load_local_status_data(package_path)
    config = data.get("config")
    if not isinstance(config, dict):
        return []
    leaf_packages = config.get("leaf_packages")
    if not isinstance(leaf_packages, list):
        return []
    return [item for item in leaf_packages if isinstance(item, str)]


def count_local_markdown_papers(package_path: Path) -> int:
    markdown_dir = package_path / "papers" / "markdown"
    if not markdown_dir.exists():
        return 0
    return sum(1 for candidate in markdown_dir.rglob("*.md") if candidate.is_file())


def claim_boundary_surface_paths(package_path: Path) -> list[Path]:
    return find_package_artifacts(package_path, CLAIM_BOUNDARY_PATTERNS)


def claim_boundary_surface_required(package_path: Path, status_data: dict) -> bool:
    if claim_boundary_surface_paths(package_path):
        return True
    if resolve_review_artifact_paths(package_path, status_data):
        return True
    return count_local_markdown_papers(package_path) >= 5


def extract_markdown_section(text: str, heading: str) -> str | None:
    lines = text.splitlines()
    needle = heading.strip()
    start = None
    for idx, line in enumerate(lines):
        if line.strip() == needle:
            start = idx + 1
            break
    if start is None:
        return None

    end = len(lines)
    for idx in range(start, len(lines)):
        if idx != start and lines[idx].startswith("## "):
            end = idx
            break
    return "\n".join(lines[start:end]).strip()


def _extract_label_value(section_text: str, label: str) -> str | None:
    pattern = re.compile(rf"^\s*(?:[-*]\s*)?{re.escape(label)}:\s*(.*)$", re.MULTILINE)
    match = pattern.search(section_text)
    if not match:
        return None
    value = match.group(1).strip()
    if value:
        return value

    lines = section_text.splitlines()
    for idx, line in enumerate(lines):
        if re.match(rf"^\s*(?:[-*]\s*)?{re.escape(label)}:\s*$", line):
            for follow in lines[idx + 1 :]:
                stripped = follow.strip()
                if not stripped:
                    continue
                if stripped.startswith("- "):
                    return stripped[2:].strip()
                if ":" in stripped and not stripped.startswith("`"):
                    break
                return stripped
    return None


def _extract_label_list(section_text: str, label: str) -> list[str]:
    lines = section_text.splitlines()
    for idx, line in enumerate(lines):
        if re.match(rf"^\s*(?:[-*]\s*)?{re.escape(label)}:\s*$", line):
            items: list[str] = []
            for follow in lines[idx + 1 :]:
                stripped = follow.strip()
                if not stripped:
                    if items:
                        break
                    continue
                if stripped.startswith("- "):
                    if stripped.endswith(":") and items:
                        break
                    items.append(stripped[2:].strip())
                    continue
                if ":" in stripped and items:
                    break
                if ":" in stripped and not items:
                    break
                if items:
                    break
            return items
    return []


def parse_topic_packet(packet_path: Path) -> dict:
    text = packet_path.read_text()
    handoff_section = extract_markdown_section(text, "## 06. Handoff Decision") or ""
    return {
        "packet_path": repo_relpath(packet_path),
        "decision": _extract_label_value(handoff_section, "Decision"),
        "rationale": _extract_label_value(handoff_section, "Rationale"),
        "proposed_slug": _extract_label_value(handoff_section, "Proposed slug"),
        "one_sentence_promise": _extract_label_value(handoff_section, "One-sentence promise"),
        "first_research_question": _extract_label_value(handoff_section, "First research question"),
        "expected_evidence_surface": _extract_label_value(handoff_section, "Expected evidence surface"),
        "initial_paper_shortlist": _extract_label_list(handoff_section, "Initial paper shortlist"),
        "near_misses_and_blocked_framings": _extract_label_list(handoff_section, "Near-misses and blocked framings"),
    }


def parse_markdown_packet_file(path: Path) -> tuple[dict, str]:
    text = path.read_text()
    frontmatter_text, body = split_frontmatter(text)
    frontmatter = yaml.safe_load(frontmatter_text) or {}
    if not isinstance(frontmatter, dict):
        raise ValueError(f"Frontmatter in {path} must be a mapping.")
    return frontmatter, body


def has_required_headings(text: str, headings: list[str]) -> bool:
    return all(heading in text for heading in headings)


def has_required_fields(frontmatter: dict, fields: list[str]) -> bool:
    return all(field in frontmatter for field in fields)


def stop_iteration_triggered(
    review_frontmatter: dict,
    decision_frontmatter: dict,
    review_body: str = "",
    decision_body: str = "",
) -> bool:
    if review_frontmatter.get("north_star_verdict") != "below_north_star":
        return False
    return (
        review_frontmatter.get("continue_iteration") is False
        or decision_frontmatter.get("rewrite_mode") == "stop_flagship_iteration"
        or decision_frontmatter.get("stop_gate_status") == "fired"
        or "stop_flagship_iteration" in decision_body
        or "stop flagship iteration" in decision_body.lower()
        or "stop flagship iteration" in review_body.lower()
    )


def ceiling_report_is_complete(packet: dict, review_frontmatter: dict) -> tuple[bool, Path | None, dict | None]:
    output_paths = packet.get("output_paths", {})
    relpath = output_paths.get("ceiling_report")
    if not isinstance(relpath, str):
        return False, None, None
    path = (REPO_ROOT / relpath).resolve()
    if not path.exists():
        return False, path, None
    try:
        frontmatter, body = parse_markdown_packet_file(path)
    except Exception:
        return False, path, None

    if not has_required_fields(frontmatter, CEILING_REPORT_FRONTMATTER_FIELDS):
        return False, path, frontmatter
    if not has_required_headings(body, CEILING_REPORT_BODY_HEADINGS):
        return False, path, frontmatter

    if frontmatter.get("ceiling_verdict") != "object_ceiling":
        return False, path, frontmatter
    if frontmatter.get("effort_verdict") in {None, "", "pending"}:
        return False, path, frontmatter
    if frontmatter.get("next_route") in {None, "", "pending"}:
        return False, path, frontmatter
    if frontmatter.get("dominant_blocker_slug") != review_frontmatter.get("dominant_blocker_slug"):
        return False, path, frontmatter

    expected_paths = {
        "live_draft_path": packet.get("live_draft_path"),
        "terminal_candidate_path": packet.get("candidate_path"),
        "terminal_replacement_review_path": output_paths.get("replacement_review"),
        "terminal_decision_path": output_paths.get("decision"),
    }
    for field, expected in expected_paths.items():
        if not isinstance(expected, str) or frontmatter.get(field) != expected:
            return False, path, frontmatter
        resolved = (REPO_ROOT / expected).resolve()
        if not resolved.exists():
            return False, path, frontmatter

    return True, path, frontmatter


def resolve_pivot_donor_report(package_path: Path) -> dict:
    ceiling_report_path = find_package_artifact(package_path, CEILING_REPORT_PATTERNS)
    reframe_path = find_package_artifact(package_path, PIVOT_REFRAME_PATTERNS)
    process_capture_path = find_package_artifact(package_path, PIVOT_PROCESS_CAPTURE_PATTERNS)
    if ceiling_report_path is not None:
        return {
            "mode": "ceiling_report",
            "ceiling_report_path": ceiling_report_path,
            "reframe_path": None,
            "process_capture_path": None,
        }
    return {
        "mode": "legacy_pair",
        "ceiling_report_path": None,
        "reframe_path": reframe_path,
        "process_capture_path": process_capture_path,
    }


def resolve_post_ceiling_pivot_progress(package_path: Path) -> dict:
    overlay_root = package_path
    status_kind = package_kind(package_path)
    leaf_packages = configured_leaf_packages(package_path)

    slate_path = find_active_pivot_artifact(package_path, PIVOT_SLATE_PATTERNS)
    grounding_path = find_active_pivot_artifact(package_path, PIVOT_GROUNDING_PATTERNS)
    next_candidate_path = find_active_pivot_artifact(package_path, PIVOT_NEXT_CANDIDATE_PATTERNS)
    research_delta_path = find_active_pivot_artifact(package_path, PIVOT_RESEARCH_DELTA_PATTERNS)
    consequence_path = find_active_pivot_artifact(package_path, PIVOT_CONSEQUENCE_PATTERNS)
    comparative_rerank_path = find_active_pivot_artifact(package_path, PIVOT_COMPARATIVE_RERANK_PATTERNS)
    north_star_path = find_active_pivot_artifact(package_path, PIVOT_NORTH_STAR_PATTERNS)
    decision_path = find_active_pivot_artifact(package_path, PIVOT_DECISION_PATTERNS)
    blocker_path = find_active_pivot_artifact(package_path, PIVOT_BLOCKER_PATTERNS)

    progress = {
        "active_overlay_root": repo_relpath(overlay_root),
        "overlay_phase": None,
        "next_overlay_action": None,
        "overlay_route": None,
        "recommended_validator": None,
        "pivot_slate_path": repo_relpath(slate_path),
        "grounding_review_path": repo_relpath(grounding_path),
        "next_candidate_path": repo_relpath(next_candidate_path),
        "research_delta_path": repo_relpath(research_delta_path),
        "consequence_pressure_path": repo_relpath(consequence_path),
        "comparative_rerank_path": repo_relpath(comparative_rerank_path),
        "north_star_viability_path": repo_relpath(north_star_path),
        "pivot_decision_path": repo_relpath(decision_path),
        "pivot_blocker_path": repo_relpath(blocker_path),
    }

    if status_kind != "umbrella":
        progress["overlay_phase"] = "upgrade_to_umbrella"
        progress["next_overlay_action"] = "upgrade_to_umbrella_and_create_donor_leaf"
        progress["recommended_validator"] = "npm run check:package-lifecycle -- --package <package>"
        return progress

    if not leaf_packages:
        progress["overlay_phase"] = "initialize_donor_leaf"
        progress["next_overlay_action"] = "initialize_donor_leaf"
        progress["recommended_validator"] = "npm run check:package-lifecycle -- --package <package>"
        return progress

    if slate_path is None:
        progress["overlay_phase"] = "build_pivot_slate"
        progress["next_overlay_action"] = "write_pivot_slate"
        progress["recommended_validator"] = "npm run gate:check -- --gate pivot_research_grounding --package <package>"
        return progress

    if grounding_path is None:
        progress["overlay_phase"] = "ground_candidates"
        progress["next_overlay_action"] = "write_pivot_grounding_review"
        progress["recommended_validator"] = "npm run gate:check -- --gate pivot_research_grounding --package <package>"
        return progress

    grounding_verdict = parse_pivot_grounding_verdict(grounding_path)
    progress["grounding_verdict"] = grounding_verdict

    if next_candidate_path is None:
        progress["overlay_phase"] = "select_live_candidate"
        progress["next_overlay_action"] = "write_next_pivot_candidate"
        progress["recommended_validator"] = "npm run gate:check -- --gate pivot_research_grounding --package <package>"
        return progress

    if grounding_verdict in {"blocked_hypothesis", "provisional_candidate"}:
        if research_delta_path is None:
            progress["overlay_phase"] = "write_research_delta"
            progress["next_overlay_action"] = "write_candidate_research_delta"
            progress["recommended_validator"] = "npm run gate:check -- --gate pivot_research_grounding --package <package>"
            return progress
        progress["overlay_phase"] = "write_research_delta"
        progress["next_overlay_action"] = "continue_candidate_research"
        progress["recommended_validator"] = "npm run gate:check -- --gate pivot_research_grounding --package <package>"
        return progress

    if grounding_verdict == "clear_lead_candidate":
        if research_delta_path is None:
            progress["overlay_phase"] = "write_research_delta"
            progress["next_overlay_action"] = "write_candidate_research_delta"
            progress["recommended_validator"] = "npm run gate:check -- --gate pivot_research_grounding --package <package>"
            return progress
        if north_star_path is None:
            progress["overlay_phase"] = "run_north_star_viability"
            progress["next_overlay_action"] = "write_north_star_viability"
            progress["recommended_validator"] = "npm run gate:check -- --gate pivot_north_star_viability --package <package>"
            return progress

    if grounding_verdict == "research_grounded_but_not_north_star_viable":
        north_star_verdict = parse_pivot_north_star_verdict(north_star_path) if north_star_path else None
        post_block_route = parse_pivot_post_block_route(decision_path) if decision_path else None
        progress["north_star_verdict"] = north_star_verdict
        progress["overlay_route"] = post_block_route
        if north_star_path is None:
            progress["overlay_phase"] = "run_north_star_viability"
            progress["next_overlay_action"] = "write_north_star_viability"
            progress["recommended_validator"] = "npm run gate:check -- --gate pivot_north_star_viability --package <package>"
            return progress
        if consequence_path is None:
            progress["overlay_phase"] = "run_consequence_pressure"
            progress["next_overlay_action"] = "write_consequence_pressure"
            progress["recommended_validator"] = "npm run gate:check -- --gate pivot_north_star_viability --package <package>"
            return progress
        if comparative_rerank_path is None:
            progress["overlay_phase"] = "run_comparative_rerank"
            progress["next_overlay_action"] = "write_comparative_rerank"
            progress["recommended_validator"] = "npm run gate:check -- --gate pivot_north_star_viability --package <package>"
            return progress
        if post_block_route == "keep_as_strong_narrower_doctrine_object":
            if len(leaf_packages) < 2:
                progress["overlay_phase"] = "initialize_narrower_leaf"
                progress["next_overlay_action"] = "initialize_narrower_doctrine_leaf"
                progress["recommended_validator"] = "npm run check:package-lifecycle -- --package <package>"
                return progress
            progress["overlay_phase"] = "post_block_route_settled"
            progress["next_overlay_action"] = "hold_for_narrower_doctrine_write_or_later_larger_successor"
            progress["recommended_validator"] = "npm run gate:check -- --gate pivot_north_star_viability --package <package>"
            return progress
        if post_block_route == "restart_pivot_search_later":
            progress["overlay_phase"] = "post_block_route_settled"
            progress["next_overlay_action"] = "await_materially_larger_successor_seam_before_restarting_pivot_search"
            progress["recommended_validator"] = "npm run gate:check -- --gate pivot_research_grounding --package <package>"
            return progress
        progress["overlay_phase"] = "decide_post_block_route"
        progress["next_overlay_action"] = "decide_narrow_or_restart_pivot_search"
        progress["recommended_validator"] = "npm run gate:check -- --gate pivot_north_star_viability --package <package>"
        return progress

    if grounding_verdict == "pivot_cleared_for_north_star_attempt":
        north_star_verdict = parse_pivot_north_star_verdict(north_star_path) if north_star_path else None
        progress["north_star_verdict"] = north_star_verdict
        if north_star_path is None:
            progress["overlay_phase"] = "run_north_star_viability"
            progress["next_overlay_action"] = "write_north_star_viability"
            progress["recommended_validator"] = "npm run gate:check -- --gate pivot_north_star_viability --package <package>"
            return progress
        if north_star_verdict == "north_star_viable":
            if len(leaf_packages) < 2:
                progress["overlay_phase"] = "initialize_successor_leaf"
                progress["next_overlay_action"] = "initialize_successor_leaf"
                progress["recommended_validator"] = "npm run check:package-lifecycle -- --package <package>"
                return progress
            progress["overlay_phase"] = "successor_leaf_ready"
            progress["next_overlay_action"] = "handoff_to_successor_leaf_for_flagship_iteration"
            progress["recommended_validator"] = "npm run gate:check -- --gate pivot_north_star_viability --package <package>"
            return progress
        progress["overlay_phase"] = "run_north_star_viability"
        progress["next_overlay_action"] = "resolve_north_star_viability_gap"
        progress["recommended_validator"] = "npm run gate:check -- --gate pivot_north_star_viability --package <package>"
        return progress

    progress["overlay_phase"] = "ground_candidates"
    progress["next_overlay_action"] = "resolve_pivot_state"
    progress["recommended_validator"] = "npm run gate:check -- --gate pivot_research_grounding --package <package>"
    return progress


def resolve_essay_iteration_progress(package_key: str, package_path: Path, status_data: dict) -> dict:
    validator_prewrite = f"npm run check:essay-prewrite -- --package {package_key}"
    validator_full = f"npm run check:essay-iteration -- --package {package_key}"
    defaults = {
        "packet_phase": None,
        "next_packet_action": None,
        "recommended_validator": None,
    }

    live_draft = resolve_markdown_path(package_path, status_data)
    revision = status_data.get("revision")
    if live_draft is None or not isinstance(revision, int):
        return {
            **defaults,
            "packet_phase": "seed_packet",
            "next_packet_action": "seed_or_refresh_packet",
            "recommended_validator": validator_prewrite,
        }

    packet_paths = build_packet_paths(live_draft, revision)
    manifest_path = packet_paths["manifest"]
    if not manifest_path.exists():
        return {
            **defaults,
            "packet_phase": "seed_packet",
            "next_packet_action": "seed_or_refresh_packet",
            "recommended_validator": validator_prewrite,
        }

    try:
        packet = json.loads(manifest_path.read_text())
    except json.JSONDecodeError:
        return {
            **defaults,
            "packet_phase": "seed_packet",
            "next_packet_action": "refresh_packet_scaffold",
            "recommended_validator": validator_prewrite,
        }

    output_paths = packet.get("output_paths", {})
    try:
        schema_version = packet_schema_version(packet)
    except ValueError:
        schema_version = 0

    if schema_version < PACKET_SCHEMA_VERSION or "prewrite_gate" not in output_paths:
        return {
            **defaults,
            "packet_phase": "run_prewrite_gate",
            "next_packet_action": "refresh_packet_scaffold_then_run_prewrite_gate",
            "recommended_validator": validator_prewrite,
        }

    blueprint_relpath = output_paths.get("blueprint")
    if not isinstance(blueprint_relpath, str):
        return {
            **defaults,
            "packet_phase": "harden_blueprint",
            "next_packet_action": "repair_packet_manifest_then_harden_blueprint",
            "recommended_validator": validator_prewrite,
        }

    blueprint_path = (REPO_ROOT / blueprint_relpath).resolve()
    if not blueprint_path.exists():
        return {
            **defaults,
            "packet_phase": "harden_blueprint",
            "next_packet_action": "write_or_refresh_blueprint",
            "recommended_validator": validator_prewrite,
        }

    blueprint_text = blueprint_path.read_text()
    if not has_required_headings(blueprint_text, BLUEPRINT_HEADINGS):
        return {
            **defaults,
            "packet_phase": "harden_blueprint",
            "next_packet_action": "complete_blueprint_contract",
            "recommended_validator": validator_prewrite,
        }

    prewrite_relpath = output_paths.get("prewrite_gate")
    if not isinstance(prewrite_relpath, str):
        return {
            **defaults,
            "packet_phase": "run_prewrite_gate",
            "next_packet_action": "refresh_packet_scaffold_then_run_prewrite_gate",
            "recommended_validator": validator_prewrite,
        }

    prewrite_path = (REPO_ROOT / prewrite_relpath).resolve()
    if not prewrite_path.exists():
        return {
            **defaults,
            "packet_phase": "run_prewrite_gate",
            "next_packet_action": "fill_prewrite_gate",
            "recommended_validator": validator_prewrite,
        }

    try:
        prewrite_frontmatter, prewrite_body = parse_markdown_packet_file(prewrite_path)
    except Exception:
        return {
            **defaults,
            "packet_phase": "run_prewrite_gate",
            "next_packet_action": "repair_prewrite_gate",
            "recommended_validator": validator_prewrite,
        }

    if not has_required_fields(prewrite_frontmatter, PREWRITE_FRONTMATTER_FIELDS) or not has_required_headings(
        prewrite_body, PREWRITE_BODY_HEADINGS
    ):
        return {
            **defaults,
            "packet_phase": "run_prewrite_gate",
            "next_packet_action": "complete_prewrite_gate",
            "recommended_validator": validator_prewrite,
        }

    writability_verdict = prewrite_frontmatter.get("writability_verdict")
    if writability_verdict == "pending":
        return {
            **defaults,
            "packet_phase": "run_prewrite_gate",
            "next_packet_action": "complete_prewrite_gate",
            "recommended_validator": validator_prewrite,
        }
    if writability_verdict == "not_yet_writable":
        return {
            **defaults,
            "packet_phase": "resolve_prewrite_blocker",
            "next_packet_action": "resolve_dominant_prewrite_blocker",
            "recommended_validator": validator_prewrite,
        }
    if writability_verdict != "writable" or prewrite_frontmatter.get("candidate_authorized") is not True:
        return {
            **defaults,
            "packet_phase": "run_prewrite_gate",
            "next_packet_action": "repair_prewrite_gate_verdict",
            "recommended_validator": validator_prewrite,
        }

    candidate_relpath = packet.get("candidate_path")
    if not isinstance(candidate_relpath, str):
        return {
            **defaults,
            "packet_phase": "draft_candidate",
            "next_packet_action": "repair_packet_manifest_then_write_bounded_candidate",
            "recommended_validator": validator_full,
        }

    candidate_path = (REPO_ROOT / candidate_relpath).resolve()
    if not candidate_path.exists() or candidate_text_looks_scaffold(candidate_path.read_text()):
        return {
            **defaults,
            "packet_phase": "draft_candidate",
            "next_packet_action": "write_bounded_candidate",
            "recommended_validator": validator_full,
        }

    review_relpath = output_paths.get("replacement_review")
    if not isinstance(review_relpath, str):
        return {
            **defaults,
            "packet_phase": "review_candidate",
            "next_packet_action": "repair_packet_manifest_then_fill_replacement_review",
            "recommended_validator": validator_full,
        }

    review_path = (REPO_ROOT / review_relpath).resolve()
    try:
        review_frontmatter, review_body = parse_markdown_packet_file(review_path)
    except Exception:
        return {
            **defaults,
            "packet_phase": "review_candidate",
            "next_packet_action": "fill_replacement_review",
            "recommended_validator": validator_full,
        }

    if review_frontmatter.get("replacement_verdict") == "pending" or review_frontmatter.get("north_star_verdict") == "pending":
        return {
            **defaults,
            "packet_phase": "review_candidate",
            "next_packet_action": "fill_replacement_review",
            "recommended_validator": validator_full,
        }

    scorecard_relpath = output_paths.get("atlas_scorecard")
    if not isinstance(scorecard_relpath, str):
        return {
            **defaults,
            "packet_phase": "score_candidate",
            "next_packet_action": "repair_packet_manifest_then_fill_scorecard",
            "recommended_validator": validator_full,
        }

    scorecard_path = (REPO_ROOT / scorecard_relpath).resolve()
    try:
        scorecard_frontmatter, _ = parse_markdown_packet_file(scorecard_path)
    except Exception:
        return {
            **defaults,
            "packet_phase": "score_candidate",
            "next_packet_action": "fill_scorecard",
            "recommended_validator": validator_full,
        }

    if any(scorecard_frontmatter.get(field) in (None, "", []) for field in PASSAGE_ANCHOR_FIELDS + ARCHIVE_ANCHOR_FIELDS):
        return {
            **defaults,
            "packet_phase": "score_candidate",
            "next_packet_action": "fill_scorecard",
            "recommended_validator": validator_full,
        }

    decision_relpath = output_paths.get("decision")
    if not isinstance(decision_relpath, str):
        return {
            **defaults,
            "packet_phase": "fill_decision",
            "next_packet_action": "repair_packet_manifest_then_fill_decision",
            "recommended_validator": validator_full,
        }

    decision_path = (REPO_ROOT / decision_relpath).resolve()
    try:
        decision_frontmatter, decision_body = parse_markdown_packet_file(decision_path)
    except Exception:
        return {
            **defaults,
            "packet_phase": "fill_decision",
            "next_packet_action": "fill_decision",
            "recommended_validator": validator_full,
        }

    if (
        decision_body.find(DECISION_REQUIRED_FOLLOW_THROUGH_PLACEHOLDER) != -1
        or decision_frontmatter.get("requires_human_approval") is not True
    ):
        return {
            **defaults,
            "packet_phase": "fill_decision",
            "next_packet_action": "fill_decision",
            "recommended_validator": validator_full,
        }

    if stop_iteration_triggered(review_frontmatter, decision_frontmatter, review_body, decision_body):
        ceiling_report_ready, _, _ = ceiling_report_is_complete(packet, review_frontmatter)
        if not ceiling_report_ready:
            return {
                **defaults,
                "packet_phase": "write_ceiling_report",
                "next_packet_action": "write_ceiling_report",
                "recommended_validator": validator_full,
            }

    from check_essay_iteration_packet import validate_packet

    if not validate_packet(packet, phase="full"):
        recommendation = decision_frontmatter.get("recommendation")
        north_star_verdict = review_frontmatter.get("north_star_verdict")
        continue_iteration = review_frontmatter.get("continue_iteration")
        rewrite_mode = decision_frontmatter.get("rewrite_mode")
        stop_gate_status = decision_frontmatter.get("stop_gate_status")
        stop_iteration = stop_iteration_triggered(review_frontmatter, decision_frontmatter, review_body, decision_body)

        if recommendation == "revise_candidate" and not stop_iteration:
            next_action = "write_next_candidate_revision"
            if north_star_verdict == "below_north_star":
                next_action = "harden_blueprint_then_write_next_candidate"
            return {
                **defaults,
                "packet_phase": "draft_candidate",
                "next_packet_action": next_action,
                "recommended_validator": validator_full,
            }

        return {
            **defaults,
            "packet_phase": "ready_for_human_review",
            "next_packet_action": "request_human_review",
            "recommended_validator": validator_full,
        }

    return {
        **defaults,
        "packet_phase": "fill_decision",
        "next_packet_action": "resolve_remaining_packet_validation_errors",
        "recommended_validator": validator_full,
    }


def base_gate_payload(gate_id: str) -> dict:
    contract = load_gate_contracts()[gate_id]
    return {
        "gate_id": gate_id,
        "status": "blocked",
        "blocking": True,
        "decision": "unresolved",
        "required_artifacts": contract["required_artifacts"],
        "missing_artifacts": [],
        "recommended_workflow": contract["recommended_workflow"],
        "recommended_validator": contract["recommended_validator"],
        "proof_mode": contract["proof_mode"],
        "details": {},
    }


def evaluate_topic_viability_gate(packet_path: Path | None) -> dict:
    payload = base_gate_payload("topic_viability")
    if packet_path is None:
        payload["decision"] = "missing_topic_packet"
        payload["missing_artifacts"] = ["topic-discovery packet"]
        return payload
    if not packet_path.exists():
        payload["decision"] = "missing_topic_packet"
        payload["missing_artifacts"] = [repo_relpath(packet_path)]
        return payload

    parsed = parse_topic_packet(packet_path)
    decision = parsed.get("decision")
    payload["details"] = parsed
    if decision != "package_init_ready":
        payload["decision"] = decision or "missing_handoff_decision"
        if decision == "post_ceiling_pivot":
            payload["recommended_workflow"] = "post_ceiling_pivot"
        return payload

    missing = [
        name
        for name in ["proposed_slug", "one_sentence_promise", "first_research_question"]
        if not parsed.get(name)
    ]
    if missing:
        payload["decision"] = "package_init_ready_missing_handoff_fields"
        payload["missing_artifacts"] = missing
        return payload

    payload["status"] = "pass"
    payload["blocking"] = False
    payload["decision"] = "package_init_ready"
    payload["recommended_workflow"] = "research"
    return payload


def evaluate_research_exit_gate(package_key: str, package_path: Path, status_data: dict) -> dict:
    revision = status_data.get("revision", 1)
    resolved_gate_path = resolve_research_exit_gate_path(package_path, revision if isinstance(revision, int) else 1)
    payload = base_gate_payload("research_exit")
    payload["details"] = {
        "research_exit_gate_path": repo_relpath(
            resolved_gate_path if resolved_gate_path is not None else build_research_exit_gate_path(package_path, revision if isinstance(revision, int) else 1)
        ),
        "governing_brief_path": repo_relpath(resolve_governing_brief_path(package_path, status_data)),
        "evidence_surface_path": repo_relpath(resolve_essay_evidence_surface(package_path, status_data)),
        "claim_boundary_paths": [repo_relpath(path) for path in claim_boundary_surface_paths(package_path)],
    }

    missing_artifacts: list[str] = []
    if resolve_governing_brief_path(package_path, status_data) is None:
        missing_artifacts.append("governing blueprint or brief")
    if resolve_essay_evidence_surface(package_path, status_data) is None:
        missing_artifacts.append("local evidence surface")

    gate_errors, gate_path = validate_research_exit_gate(package_key)
    if gate_path is not None and not gate_path.exists():
        missing_artifacts.append("research-exit gate artifact")

    boundary_required = claim_boundary_surface_required(package_path, status_data)
    boundary_paths = claim_boundary_surface_paths(package_path)
    if boundary_required and not boundary_paths:
        missing_artifacts.append("claim-boundary surface")

    payload["missing_artifacts"] = missing_artifacts
    if gate_errors:
        payload["decision"] = "research_exit_blocked"
        payload["details"]["errors"] = gate_errors
        if "local evidence surface" in missing_artifacts or has_intake_candidates(package_path):
            payload["recommended_workflow"] = "paper_intake"
        elif "claim-boundary surface" in missing_artifacts:
            payload["recommended_workflow"] = "evidence_authorization"
        else:
            payload["recommended_workflow"] = "research"
        return payload

    payload["status"] = "pass"
    payload["blocking"] = False
    payload["decision"] = "ready_for_essay_iteration"
    payload["recommended_workflow"] = "essay_iteration"
    return payload


def evaluate_essay_prewrite_gate(package_key: str, package_path: Path, status_data: dict) -> dict:
    payload = base_gate_payload("essay_prewrite")
    progress = resolve_essay_iteration_progress(package_key, package_path, status_data)
    payload["details"] = progress
    phase = progress.get("packet_phase")
    decision = progress.get("next_packet_action")
    if phase in {
        "draft_candidate",
        "review_candidate",
        "score_candidate",
        "fill_decision",
        "write_ceiling_report",
        "ready_for_human_review",
    }:
        payload["status"] = "pass"
        payload["blocking"] = False
        payload["decision"] = "writable"
        return payload
    if phase == "resolve_prewrite_blocker":
        payload["decision"] = "not_yet_writable"
    else:
        payload["decision"] = decision or "run_prewrite_gate"
    if phase == "seed_packet":
        payload["missing_artifacts"] = ["essay-iteration packet manifest"]
    elif phase == "harden_blueprint":
        payload["missing_artifacts"] = ["hardened blueprint"]
    else:
        payload["missing_artifacts"] = ["essay prewrite gate"]
    return payload


def evaluate_replacement_north_star_gate(package_key: str, package_path: Path, status_data: dict) -> dict:
    payload = base_gate_payload("replacement_north_star")
    live_draft = resolve_markdown_path(package_path, status_data)
    revision = status_data.get("revision")
    if live_draft is None or not isinstance(revision, int):
        payload["decision"] = "missing_packet_context"
        payload["missing_artifacts"] = ["essay-iteration packet manifest"]
        return payload

    packet_paths = build_packet_paths(live_draft, revision)
    manifest_path = packet_paths["manifest"]
    if not manifest_path.exists():
        payload["decision"] = "missing_packet_manifest"
        payload["missing_artifacts"] = ["essay-iteration packet manifest"]
        return payload

    try:
        packet = json.loads(manifest_path.read_text())
    except json.JSONDecodeError:
        payload["decision"] = "invalid_packet_manifest"
        payload["missing_artifacts"] = [repo_relpath(manifest_path)]
        return payload

    review_path = packet_paths["replacement_review"]
    decision_path = packet_paths["decision"]
    if not review_path.exists():
        payload["decision"] = "missing_replacement_review"
        payload["missing_artifacts"] = ["replacement review"]
        return payload
    if not decision_path.exists():
        payload["decision"] = "missing_promotion_decision"
        payload["missing_artifacts"] = ["promotion decision"]
        return payload

    try:
        review_frontmatter, review_body = parse_markdown_packet_file(review_path)
        decision_frontmatter, decision_body = parse_markdown_packet_file(decision_path)
    except Exception as exc:
        payload["decision"] = "invalid_review_packet"
        payload["details"] = {"error": str(exc)}
        return payload

    north_star_verdict = review_frontmatter.get("north_star_verdict")
    payload["details"] = {
        "north_star_verdict": north_star_verdict,
        "replacement_verdict": review_frontmatter.get("replacement_verdict"),
        "continue_iteration": review_frontmatter.get("continue_iteration"),
        "rewrite_mode": decision_frontmatter.get("rewrite_mode"),
        "stop_gate_status": decision_frontmatter.get("stop_gate_status"),
        "packet_manifest_path": repo_relpath(manifest_path),
    }

    if north_star_verdict in {None, "", "pending"}:
        payload["decision"] = "pending_review"
        return payload

    if north_star_verdict not in {"below_north_star"}:
        payload["status"] = "pass"
        payload["blocking"] = False
        payload["decision"] = "clears_north_star"
        return payload

    stop_iteration = stop_iteration_triggered(review_frontmatter, decision_frontmatter, review_body, decision_body)
    if stop_iteration:
        ceiling_report_ready, ceiling_report_path, ceiling_report_frontmatter = ceiling_report_is_complete(packet, review_frontmatter)
        payload["details"]["ceiling_report_path"] = repo_relpath(ceiling_report_path)
        if ceiling_report_frontmatter is not None:
            payload["details"]["ceiling_verdict"] = ceiling_report_frontmatter.get("ceiling_verdict")
            payload["details"]["effort_verdict"] = ceiling_report_frontmatter.get("effort_verdict")
            payload["details"]["next_route"] = ceiling_report_frontmatter.get("next_route")
        if not ceiling_report_ready:
            payload["decision"] = "object_ceiling_report_missing"
            payload["recommended_workflow"] = "essay_iteration"
            payload["missing_artifacts"] = ["ceiling report"]
            return payload
        payload["decision"] = "object_ceiling"
        if ceiling_report_frontmatter and ceiling_report_frontmatter.get("next_route") == "post_ceiling_pivot":
            payload["recommended_workflow"] = "post_ceiling_pivot"
            payload["details"]["overlay_candidate"] = "post_ceiling_pivot"
        else:
            payload["recommended_workflow"] = "essay_iteration"
        return payload

    payload["decision"] = "revise_same_object"
    payload["recommended_workflow"] = "essay_iteration"
    return payload


def parse_release_gate_verdict(path: Path) -> str | None:
    verdict = None
    for line in path.read_text().splitlines():
        if line.strip().startswith("Verdict:"):
            verdict = line.split(":", 1)[1].strip()
            if verdict:
                return verdict
    return verdict


def evaluate_release_readiness_gate(package_path: Path, status_data: dict) -> dict:
    payload = base_gate_payload("release_readiness")
    artifact = find_package_artifact(package_path, RELEASE_GATE_PATTERNS)
    payload["details"] = {
        "release_gate_path": repo_relpath(artifact),
        "live_draft_path": repo_relpath(resolve_markdown_path(package_path, status_data)),
    }
    if resolve_markdown_path(package_path, status_data) is None:
        payload["missing_artifacts"].append("canonical live draft")
    if artifact is None:
        payload["decision"] = "missing_release_gate"
        payload["missing_artifacts"].append("release-gate checklist or decision note")
        return payload

    verdict = parse_release_gate_verdict(artifact)
    payload["details"]["release_verdict"] = verdict
    if verdict == "release_ready":
        payload["status"] = "pass"
        payload["blocking"] = False
        payload["decision"] = "release_ready"
        return payload
    if verdict == "release_ready_after_minor_fixes":
        payload["decision"] = "minor_fixes_remaining"
    else:
        payload["decision"] = "release_blocked"
    payload["recommended_workflow"] = "release_gate"
    return payload


def parse_pivot_grounding_verdict(path: Path) -> str | None:
    section = extract_markdown_section(path.read_text(), "## Grounding Verdict")
    if not section:
        return None
    for line in section.splitlines():
        stripped = line.strip().strip("`")
        if stripped:
            return stripped
    return None


def parse_pivot_north_star_verdict(path: Path) -> str | None:
    section = extract_markdown_section(path.read_text(), "## North-Star Verdict")
    if not section:
        return None
    for line in section.splitlines():
        stripped = line.strip().strip("`")
        if stripped:
            return stripped
    return None


def parse_pivot_post_block_route(path: Path) -> str | None:
    section = extract_markdown_section(path.read_text(), "## Post-Block Route")
    if not section:
        return None
    for line in section.splitlines():
        stripped = line.strip().strip("`")
        if stripped:
            return stripped
    return None


def evaluate_pivot_research_grounding_gate(package_path: Path) -> dict:
    payload = base_gate_payload("pivot_research_grounding")
    donor_report = resolve_pivot_donor_report(package_path)
    grounding_path = find_active_pivot_artifact(package_path, PIVOT_GROUNDING_PATTERNS)
    decision_path = find_active_pivot_artifact(package_path, PIVOT_DECISION_PATTERNS)
    payload["details"] = {
        "donor_report_mode": donor_report["mode"],
        "ceiling_report_path": repo_relpath(donor_report["ceiling_report_path"]),
        "reframe_path": repo_relpath(donor_report["reframe_path"]),
        "process_capture_path": repo_relpath(donor_report["process_capture_path"]),
        "grounding_review_path": repo_relpath(grounding_path),
        "pivot_decision_path": repo_relpath(decision_path),
    }
    if donor_report["mode"] == "ceiling_report":
        if donor_report["ceiling_report_path"] is None:
            payload["missing_artifacts"].append("ceiling report")
        else:
            try:
                donor_frontmatter, _ = parse_markdown_packet_file(donor_report["ceiling_report_path"])
            except Exception:
                payload["decision"] = "invalid_ceiling_report"
                return payload
            payload["details"]["ceiling_verdict"] = donor_frontmatter.get("ceiling_verdict")
            payload["details"]["next_route"] = donor_frontmatter.get("next_route")
            if donor_frontmatter.get("ceiling_verdict") != "object_ceiling":
                payload["decision"] = "ceiling_report_not_settled"
                return payload
            if donor_frontmatter.get("next_route") != "post_ceiling_pivot":
                payload["decision"] = "ceiling_report_routes_elsewhere"
                payload["recommended_workflow"] = "essay_iteration"
                return payload
    else:
        if donor_report["reframe_path"] is None:
            payload["missing_artifacts"].append("post-ceiling reframe")
        if donor_report["process_capture_path"] is None:
            payload["missing_artifacts"].append("process capture")
    if grounding_path is None:
        payload["missing_artifacts"].append("pivot grounding review")
    if decision_path is None:
        payload["missing_artifacts"].append("pivot decision or live candidate status")
    if payload["missing_artifacts"]:
        payload["decision"] = "missing_pivot_artifacts"
        return payload

    verdict = parse_pivot_grounding_verdict(grounding_path)
    payload["details"]["grounding_verdict"] = verdict
    if verdict in {"research_grounded_but_not_north_star_viable", "pivot_cleared_for_north_star_attempt"}:
        payload["status"] = "pass"
        payload["blocking"] = False
        payload["decision"] = verdict
        return payload

    payload["decision"] = verdict or "grounding_not_cleared"
    return payload


def evaluate_pivot_north_star_viability_gate(package_path: Path) -> dict:
    payload = base_gate_payload("pivot_north_star_viability")
    grounding_path = find_active_pivot_artifact(package_path, PIVOT_GROUNDING_PATTERNS)
    decision_path = find_active_pivot_artifact(package_path, PIVOT_DECISION_PATTERNS)
    north_star_path = find_active_pivot_artifact(package_path, PIVOT_NORTH_STAR_PATTERNS)
    payload["details"] = {
        "grounding_review_path": repo_relpath(grounding_path),
        "pivot_decision_path": repo_relpath(decision_path),
        "north_star_viability_path": repo_relpath(north_star_path),
    }
    if grounding_path is None:
        payload["missing_artifacts"].append("pivot grounding review")
    if decision_path is None:
        payload["missing_artifacts"].append("pivot decision")
    if north_star_path is None:
        payload["missing_artifacts"].append("pivot north-star viability gate")
    if payload["missing_artifacts"]:
        payload["decision"] = "missing_pivot_artifacts"
        return payload

    grounding_verdict = parse_pivot_grounding_verdict(grounding_path)
    payload["details"]["grounding_verdict"] = grounding_verdict
    viability_verdict = parse_pivot_north_star_verdict(north_star_path) if north_star_path else None
    payload["details"]["north_star_verdict"] = viability_verdict

    decision_text = decision_path.read_text()
    decision_clears = (
        "pivot_cleared_for_north_star_attempt" in decision_text
        or "go_for_pivot" in decision_text
        or "cleared pivot" in decision_text.lower()
    )

    if grounding_verdict not in {
        "research_grounded_but_not_north_star_viable",
        "pivot_cleared_for_north_star_attempt",
    }:
        payload["decision"] = "grounding_not_cleared"
        return payload

    if viability_verdict == "north_star_viable" and decision_clears:
        payload["status"] = "pass"
        payload["blocking"] = False
        payload["decision"] = "north_star_viable"
        return payload

    if viability_verdict == "north_star_viable":
        payload["decision"] = "north_star_viable_pending_pivot_decision"
        return payload

    if viability_verdict == "not_north_star_viable" or grounding_verdict == "research_grounded_but_not_north_star_viable":
        payload["decision"] = "research_grounded_but_not_north_star_viable"
    else:
        payload["decision"] = "north_star_viability_not_cleared"
    return payload


def evaluate_gate(gate_id: str, package_arg: str | None = None, packet_path: Path | None = None) -> dict:
    if gate_id == "topic_viability":
        return evaluate_topic_viability_gate(packet_path)

    if package_arg is None:
        raise ValueError(f"Gate '{gate_id}' requires --package.")
    manifest_ref, status_data = load_status_ref(package_arg)
    package_path = manifest_ref.package_path

    if gate_id == "research_exit":
        return evaluate_research_exit_gate(manifest_ref.package_key, package_path, status_data)
    if gate_id == "essay_prewrite":
        return evaluate_essay_prewrite_gate(manifest_ref.package_key, package_path, status_data)
    if gate_id == "replacement_north_star":
        return evaluate_replacement_north_star_gate(manifest_ref.package_key, package_path, status_data)
    if gate_id == "pivot_research_grounding":
        return evaluate_pivot_research_grounding_gate(package_path)
    if gate_id == "pivot_north_star_viability":
        return evaluate_pivot_north_star_viability_gate(package_path)
    if gate_id == "release_readiness":
        return evaluate_release_readiness_gate(package_path, status_data)
    raise KeyError(f"Unknown gate '{gate_id}'")


def determine_pipeline_profile(
    package_path: Path,
    status_data: dict,
    stage: str,
    gate_statuses: dict[str, dict] | None = None,
) -> str:
    profiles = load_pipeline_profiles()
    gate_statuses = gate_statuses or {}
    north_star_gate = gate_statuses.get("replacement_north_star", {})
    if (
        north_star_gate.get("decision") == "object_ceiling"
        and north_star_gate.get("details", {}).get("next_route") == "post_ceiling_pivot"
    ):
        profile_id = "post_ceiling_successor"
    else:
        active_stage = next_stage_for_package(package_path, status_data)
        if active_stage == stage:
            profile_id = "article_default"
        else:
            profile_id = "midstream_revision"
    if profile_id not in profiles:
        raise ValueError(f"Pipeline profile '{profile_id}' is not defined.")
    return profile_id


def stage_gate_ids(stage: str) -> list[str]:
    if stage == "research":
        return ["research_exit"]
    if stage == "essay_iteration":
        return ["essay_prewrite", "replacement_north_star"]
    if stage in {"article_polish", "substack_publishing", "distribution"}:
        return ["release_readiness"]
    return []


def build_stage_gate_statuses(package_key: str, stage: str) -> dict[str, dict]:
    statuses = {}
    for gate_id in stage_gate_ids(stage):
        statuses[gate_id] = evaluate_gate(gate_id, package_arg=package_key)
    return statuses


def build_stage_recommended_workflows(
    package_path: Path,
    status_data: dict,
    stage: str,
    gate_statuses: dict[str, dict],
    pipeline_profile: str,
) -> list[str]:
    profile = load_pipeline_profiles()[pipeline_profile]
    fallback_routes = profile.get("fallback_routes", {})
    recommended: list[str] = []

    def push(workflow_id: str | None) -> None:
        if not workflow_id:
            return
        if workflow_id not in recommended:
            recommended.append(workflow_id)

    if stage == "research":
        push("research")
        gate = gate_statuses.get("research_exit")
        if gate:
            if gate.get("blocking"):
                push(fallback_routes.get("research_exit"))
            push(gate.get("recommended_workflow"))
        if has_intake_candidates(package_path):
            push("paper_intake")
        if (
            gate
            and "claim-boundary surface" in gate.get("missing_artifacts", [])
        ):
            push("evidence_authorization")
        return recommended

    if stage == "essay_iteration":
        push("essay_iteration")
        prewrite = gate_statuses.get("essay_prewrite")
        north_star = gate_statuses.get("replacement_north_star")
        if prewrite and prewrite.get("decision") == "not_yet_writable":
            if prewrite.get("blocking"):
                push(fallback_routes.get("essay_prewrite"))
            if claim_boundary_surface_required(package_path, status_data) and not claim_boundary_surface_paths(package_path):
                push("evidence_authorization")
        if north_star:
            if north_star.get("blocking"):
                push(fallback_routes.get("replacement_north_star"))
            push(north_star.get("recommended_workflow"))
        return recommended

    if stage in {"article_polish", "substack_publishing", "distribution"}:
        push("article_polish" if stage == "article_polish" else stage)
        release_gate = gate_statuses.get("release_readiness")
        if release_gate:
            if release_gate.get("blocking"):
                push(fallback_routes.get("release_readiness"))
            push(release_gate.get("recommended_workflow"))
        return recommended

    push(stage)
    return recommended


def build_overlay_candidates(stage: str, gate_statuses: dict[str, dict]) -> list[str]:
    overlays: list[str] = []
    if stage == "essay_iteration":
        north_star = gate_statuses.get("replacement_north_star")
        if (
            north_star
            and north_star.get("decision") == "object_ceiling"
            and north_star.get("details", {}).get("next_route") == "post_ceiling_pivot"
        ):
            overlays.append("post_ceiling_pivot")
    return overlays


def build_effective_route_summary(
    package_path: Path,
    status_data: dict,
    stage: str,
    stage_metadata: dict,
    policy: dict,
    can_execute: bool,
    requires_approval: bool,
    active_overlay: str | None,
    overlay_progress: dict,
    packet_progress: dict,
) -> dict:
    if not active_overlay:
        return {
            "effective_workflow": stage,
            "effective_workflow_kind": stage_metadata["workflow_kind"],
            "effective_workflow_doc": repo_relpath(load_workflow_contract(stage)["path"]),
            "effective_next_action": packet_progress.get("next_packet_action"),
            "effective_route": overlay_progress.get("overlay_route"),
            "effective_can_execute": can_execute,
            "effective_requires_approval": requires_approval,
            "effective_approval_gate": stage_metadata["approval_gate"],
        }

    overlay_contract = load_workflow_contract(active_overlay)
    overlay_metadata = overlay_contract["metadata"]
    overlay_required_context = resolve_required_context(
        package_path,
        status_data,
        overlay_metadata["required_context"],
    )
    overlay_requires_approval, overlay_can_execute, _ = compute_workflow_capabilities(
        active_overlay,
        overlay_metadata,
        overlay_required_context,
        policy,
    )
    return {
        "effective_workflow": active_overlay,
        "effective_workflow_kind": overlay_metadata["workflow_kind"],
        "effective_workflow_doc": repo_relpath(overlay_contract["path"]),
        "effective_next_action": overlay_progress.get("next_overlay_action"),
        "effective_route": overlay_progress.get("overlay_route"),
        "effective_can_execute": overlay_can_execute,
        "effective_requires_approval": overlay_requires_approval,
        "effective_approval_gate": overlay_metadata["approval_gate"],
    }

def build_stage_resolution(package_arg: str, stage: str) -> dict:
    manifest_ref, status_data = load_status_ref(package_arg)
    workflow_contract = load_workflow_contract(stage)
    metadata = workflow_contract["metadata"]
    policy = load_harness_policy()
    required_context = resolve_required_context(
        manifest_ref.package_path,
        status_data,
        metadata["required_context"],
    )
    requires_approval, can_execute, blocking_issues = compute_stage_capabilities(
        stage,
        metadata,
        required_context,
        policy,
    )
    lifecycle_report = inspect_package_lifecycle(manifest_ref.package_key)
    if stage == "essay_iteration":
        for issue in lifecycle_report["issues"]:
            if issue["blocking"]:
                blocking_issues.append(issue["message"])
        if any(issue["blocking"] for issue in lifecycle_report["issues"]):
            can_execute = False
    gate_statuses = build_stage_gate_statuses(manifest_ref.package_key, stage)
    for gate_id, gate_status in gate_statuses.items():
        if gate_status.get("blocking"):
            blocking_issues.append(
                f"Gate '{gate_id}' is blocked: {gate_status.get('decision')}."
            )
    pipeline_profile = determine_pipeline_profile(
        manifest_ref.package_path,
        status_data,
        stage,
        gate_statuses,
    )
    recommended_workflows = build_stage_recommended_workflows(
        manifest_ref.package_path,
        status_data,
        stage,
        gate_statuses,
        pipeline_profile,
    )
    overlay_candidates = build_overlay_candidates(stage, gate_statuses)
    active_overlay = None
    overlay_progress = {
        "active_overlay": None,
        "overlay_phase": None,
        "next_overlay_action": None,
        "overlay_route": None,
        "overlay_recommended_validator": None,
        "active_overlay_root": None,
    }
    if "post_ceiling_pivot" in overlay_candidates:
        active_overlay = "post_ceiling_pivot"
        resolved_overlay = resolve_post_ceiling_pivot_progress(manifest_ref.package_path)
        overlay_progress = {
            "active_overlay": active_overlay,
            "overlay_phase": resolved_overlay.get("overlay_phase"),
            "next_overlay_action": resolved_overlay.get("next_overlay_action"),
            "overlay_route": resolved_overlay.get("overlay_route"),
            "overlay_recommended_validator": resolved_overlay.get("recommended_validator"),
            "active_overlay_root": resolved_overlay.get("active_overlay_root"),
        }
    package_context_paths = build_package_context_paths(manifest_ref.package_path, status_data)
    packet_paths = {}
    packet_progress = {
        "packet_phase": None,
        "next_packet_action": None,
        "recommended_validator": None,
    }
    if stage == "essay_iteration":
        live_draft = resolve_markdown_path(manifest_ref.package_path, status_data)
        revision = status_data.get("revision")
        packet_paths = describe_packet_paths(live_draft, revision if isinstance(revision, int) else None)
        packet_progress = resolve_essay_iteration_progress(
            manifest_ref.package_key,
            manifest_ref.package_path,
            status_data,
        )
    effective_route = build_effective_route_summary(
        manifest_ref.package_path,
        status_data,
        stage,
        metadata,
        policy,
        can_execute,
        requires_approval,
        active_overlay,
        overlay_progress,
        packet_progress,
    )

    result = {
        "package": manifest_ref.package_key,
        "revision": status_data.get("revision", 1),
        "stage": stage,
        "runner_mode": metadata["runner_mode"],
        "launch_mode": metadata["launch_mode"],
        "approval_gate": metadata["approval_gate"],
        "requires_approval": requires_approval,
        "can_execute": can_execute,
        "blocking_issues": blocking_issues,
        "required_context": required_context,
        "suggested_commands": build_stage_suggested_commands(manifest_ref.package_key, stage, can_execute),
        "log_target": "reviewable-runs/logs/",
        "workflow_doc": repo_relpath(workflow_contract["path"]),
        "workflow_kind": metadata["workflow_kind"],
        "stage_binding": metadata.get("stage_binding"),
        "stability": metadata["stability"],
        "default_skill": metadata["default_skill"],
        "launch_templates": metadata["launch_templates"],
        "packet_templates": resolve_packet_template_paths(metadata["packet_templates"]),
        "validator_commands": render_command_templates(metadata["validator_commands"], manifest_ref.package_key, status_data),
        "judgment_policy": metadata["judgment_policy"],
        "prohibited_moves": metadata["prohibited_moves"],
        "expected_outputs": metadata["expected_outputs"],
        "done_when": metadata["done_when"],
        "package_audit": audit_package(manifest_ref.package_key),
        "lifecycle_report": lifecycle_report,
        "auto_mark_done_allowed": auto_mark_done_allowed(stage, metadata, policy),
        "current_state": status_data.get("stages", {}).get(stage, {"done": False, "last_updated": None}),
        "package_context_paths": package_context_paths,
        "pipeline_profile": pipeline_profile,
        "recommended_workflows": recommended_workflows,
        "gate_statuses": gate_statuses,
        "overlay_candidates": overlay_candidates,
        "packet_paths": packet_paths,
        **packet_progress,
        **overlay_progress,
        **effective_route,
    }
    if active_overlay:
        overlay_commands = build_workflow_suggested_commands(
            active_overlay,
            False,
            package_key=manifest_ref.package_key,
        )
        for command in overlay_commands:
            if command not in result["suggested_commands"]:
                result["suggested_commands"].append(command)
    return result


def build_workflow_resolution(
    workflow_id: str,
    package_arg: str | None = None,
    packet_path: Path | None = None,
) -> dict:
    workflow_contract = load_workflow_contract(workflow_id)
    metadata = workflow_contract["metadata"]
    policy = load_harness_policy()

    manifest_ref = None
    status_data = None
    package_context_paths = {}
    blocking_issues: list[str] = []

    if package_arg is not None:
        manifest_ref, status_data = load_status_ref(package_arg)
        required_context = resolve_required_context(
            manifest_ref.package_path,
            status_data,
            metadata["required_context"],
        )
        package_context_paths = build_package_context_paths(manifest_ref.package_path, status_data)
    elif workflow_id == "topic_discovery":
        required_context = open_required_context(metadata["required_context"])
    else:
        raise ValueError(f"Workflow '{workflow_id}' requires --package.")

    requires_approval, can_execute, capability_blockers = compute_workflow_capabilities(
        workflow_id,
        metadata,
        required_context,
        policy,
    )
    blocking_issues.extend(capability_blockers)

    recommended_gates = workflow_recommended_gates(workflow_id)
    suggested_commands = build_workflow_suggested_commands(
        workflow_id,
        can_execute,
        package_key=manifest_ref.package_key if manifest_ref else None,
        packet_path=packet_path,
    )
    if manifest_ref is not None:
        for gate_id in recommended_gates:
            suggested_commands.append(
                f"npm run gate:check -- --gate {gate_id} --package {manifest_ref.package_key} --format json"
            )
    elif packet_path is not None and "topic_viability" in recommended_gates:
        suggested_commands.append(
            f"npm run gate:check -- --gate topic_viability --packet {repo_relpath(packet_path)} --format json"
        )

    packet_details = parse_topic_packet(packet_path) if packet_path and packet_path.exists() else None
    overlay_progress = {
        "overlay_phase": None,
        "next_overlay_action": None,
        "overlay_route": None,
        "recommended_validator": None,
        "active_overlay_root": None,
    }
    if workflow_id == "post_ceiling_pivot" and manifest_ref is not None:
        resolved_overlay = resolve_post_ceiling_pivot_progress(manifest_ref.package_path)
        overlay_progress = {
            "overlay_phase": resolved_overlay.get("overlay_phase"),
            "next_overlay_action": resolved_overlay.get("next_overlay_action"),
            "overlay_route": resolved_overlay.get("overlay_route"),
            "recommended_validator": resolved_overlay.get("recommended_validator"),
            "active_overlay_root": resolved_overlay.get("active_overlay_root"),
        }
    return {
        "workflow_id": workflow_id,
        "workflow_doc": repo_relpath(workflow_contract["path"]),
        "workflow_kind": metadata["workflow_kind"],
        "stage_binding": metadata.get("stage_binding"),
        "stability": metadata["stability"],
        "package": manifest_ref.package_key if manifest_ref else None,
        "approval_gate": metadata["approval_gate"],
        "requires_approval": requires_approval,
        "can_execute": can_execute,
        "blocking_issues": blocking_issues,
        "required_context": required_context,
        "expected_outputs": metadata["expected_outputs"],
        "validator_commands": render_command_templates(
            metadata["validator_commands"],
            manifest_ref.package_key,
            status_data,
        )
        if manifest_ref and status_data
        else metadata["validator_commands"],
        "launch_templates": render_command_templates(
            metadata["launch_templates"],
            manifest_ref.package_key,
            status_data,
        )
        if manifest_ref and status_data
        else metadata["launch_templates"],
        "packet_templates": resolve_packet_template_paths(metadata["packet_templates"]),
        "suggested_commands": suggested_commands,
        "recommended_gates": recommended_gates,
        "package_context_paths": package_context_paths,
        "topic_packet_details": packet_details,
        "log_target": "reviewable-runs/logs/",
        **overlay_progress,
    }


def emit_launch_pack(resolution: dict) -> Path:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    package_id = resolution["package"].replace("/", "__")
    log_path = LOGS_DIR / f"{timestamp}_{package_id}_{resolution['stage']}_launch-pack.json"
    payload = {
        "kind": "harness_launch_pack",
        "schema_version": 2,
        "timestamp": timestamp,
        "run_id": f"{timestamp}_{package_id}_{resolution['stage']}_launch-pack",
        "task_brief": (
            f"Advance package '{resolution['package']}' through the "
            f"'{resolution['stage']}' stage using '{resolution['workflow_doc']}'."
        ),
        "boundary": {
            "type": "handoff",
            "reason": "Launch pack prepares a bounded guided run; it does not execute the stage.",
            "external_side_effect": False,
            "approval_gate": resolution["approval_gate"],
            "approval_required": resolution["requires_approval"],
            "approval_status": "pending_if_stage_executes" if resolution["requires_approval"] else "not_required",
        },
        "task": {
            "objective": f"Prepare a bounded launch packet for package '{resolution['package']}' stage '{resolution['stage']}'.",
            "stop_condition": "Launch pack written to reviewable-runs/logs/.",
            "non_goals": [
                "Do not claim the stage was executed.",
                "Do not treat this launch pack as approval for external mutation.",
            ],
        },
        "package": resolution["package"],
        "stage": resolution["stage"],
        "workflow_doc": resolution["workflow_doc"],
        "runner_mode": resolution["runner_mode"],
        "launch_mode": resolution["launch_mode"],
        "approval_gate": resolution["approval_gate"],
        "required_context": resolution["required_context"],
        "suggested_commands": resolution["suggested_commands"],
        "suggested_skill": resolution["default_skill"],
        "package_context_paths": resolution["package_context_paths"],
        "packet_paths": resolution["packet_paths"],
        "expected_outputs": resolution["expected_outputs"],
        "done_when": resolution["done_when"],
        "packet_templates": resolution["packet_templates"],
        "validator_commands": resolution["validator_commands"],
        "judgment_policy": resolution["judgment_policy"],
        "prohibited_moves": resolution["prohibited_moves"],
        "blocking_issues": resolution["blocking_issues"],
        "verification": {
            "checks": [
                {
                    "name": "launch_pack_written",
                    "result": "pass",
                    "notes": repo_relpath(log_path),
                }
            ],
            "residual_risk": "The launch pack is only an entry packet for guided work. Review the final run separately.",
        },
    }
    log_path.write_text(json.dumps(payload, indent=2) + "\n")
    return log_path


def emit_workflow_launch_pack(resolution: dict) -> Path:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    package_id = (resolution.get("package") or "no-package").replace("/", "__")
    workflow_id = resolution["workflow_id"]
    log_path = LOGS_DIR / f"{timestamp}_{package_id}_{workflow_id}_workflow-launch-pack.json"
    payload = {
        "kind": "workflow_launch_pack",
        "schema_version": 2,
        "timestamp": timestamp,
        "run_id": f"{timestamp}_{package_id}_{workflow_id}_workflow-launch-pack",
        "package": resolution.get("package"),
        "workflow_id": workflow_id,
        "workflow_kind": resolution["workflow_kind"],
        "workflow_doc": resolution["workflow_doc"],
        "boundary": {
            "type": "handoff",
            "reason": "Workflow launch pack prepares a bounded workflow run; it does not claim the workflow completed.",
            "external_side_effect": False,
            "approval_gate": resolution["approval_gate"],
            "approval_required": resolution["requires_approval"],
            "approval_status": "pending_if_workflow_executes" if resolution["requires_approval"] else "not_required",
        },
        "task": {
            "objective": f"Prepare a bounded launch packet for workflow '{workflow_id}'.",
            "stop_condition": "Workflow launch pack written to reviewable-runs/logs/.",
            "non_goals": [
                "Do not claim the workflow completed.",
                "Do not treat this launch pack as approval for external mutation.",
            ],
        },
        "required_context": resolution["required_context"],
        "suggested_commands": resolution["suggested_commands"],
        "expected_outputs": resolution["expected_outputs"],
        "blocking_issues": resolution["blocking_issues"],
        "recommended_gates": resolution["recommended_gates"],
        "verification": {
            "checks": [
                {
                    "name": "workflow_launch_pack_written",
                    "result": "pass",
                    "notes": repo_relpath(log_path),
                }
            ],
            "residual_risk": "This log is only a workflow launch packet. Review the resulting run or gate decision separately.",
        },
    }
    log_path.write_text(json.dumps(payload, indent=2) + "\n")
    return log_path


def log_workflow_run(resolution: dict, action: str, success: bool, output: str, commands: list[str]) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    package_id = (resolution.get("package") or "no-package").replace("/", "__")
    workflow_id = resolution["workflow_id"]
    log_path = LOGS_DIR / f"{timestamp}_{package_id}_{workflow_id}_{action}.json"
    output_limit = 6000
    payload = {
        "kind": "workflow_run",
        "schema_version": 2,
        "timestamp": timestamp,
        "run_id": f"{timestamp}_{package_id}_{workflow_id}_{action}",
        "package": resolution.get("package"),
        "workflow_id": workflow_id,
        "workflow_kind": resolution["workflow_kind"],
        "action": action,
        "success": success,
        "boundary": {
            "type": "local workflow operation",
            "reason": "Workflow execution stays inside the local repo contract unless the approval gate explicitly authorizes something stronger.",
            "external_side_effect": False,
            "approval_gate": resolution["approval_gate"],
            "approval_required": resolution["requires_approval"],
            "approval_status": "not_recorded_in_log" if resolution["requires_approval"] else "not_required",
        },
        "task": {
            "objective": f"Run workflow '{workflow_id}'.",
            "stop_condition": "Workflow command finished and a run log was written.",
            "non_goals": [
                "Do not treat this routine workflow log as retained proof by itself.",
            ],
        },
        "execution": {
            "commands": commands,
            "output_excerpt": output[-output_limit:],
            "output_truncated": len(output) > output_limit,
        },
        "evidence": {
            "workflow_doc": resolution["workflow_doc"],
            "required_context": resolution["required_context"],
            "expected_outputs": resolution["expected_outputs"],
            "recommended_gates": resolution["recommended_gates"],
        },
        "verification": {
            "checks": [
                {
                    "name": "command_exit_status",
                    "result": "pass" if success else "fail",
                    "notes": "Workflow command or launch-pack emission result.",
                },
                {
                    "name": "workflow_log_written",
                    "result": "pass",
                    "notes": repo_relpath(log_path),
                },
            ],
            "residual_risk": "This is a bounded workflow run log. Preserve a stronger proof packet separately if the run becomes decision-critical.",
        },
        "failure_or_risk": {
            "actual_failure": None if success else "Workflow command failed; inspect output_excerpt.",
            "possible_failures": [
                "A guided workflow was mistaken for hidden execution.",
                "A local workflow log was mistaken for approval to mutate an external system.",
            ],
        },
        "workflow_doc": resolution["workflow_doc"],
    }
    log_path.write_text(json.dumps(payload, indent=2) + "\n")
    return repo_relpath(log_path)


def log_gate_check(gate_result: dict, package: str | None, packet_path: Path | None) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    package_id = (package or "no-package").replace("/", "__")
    gate_id = gate_result["gate_id"]
    log_path = LOGS_DIR / f"{timestamp}_{package_id}_{gate_id}_gate-check.json"
    payload = {
        "kind": "gate_check",
        "schema_version": 2,
        "timestamp": timestamp,
        "run_id": f"{timestamp}_{package_id}_{gate_id}_gate-check",
        "package": package,
        "gate_id": gate_id,
        "packet_path": repo_relpath(packet_path),
        "boundary": {
            "type": "gate evaluation",
            "reason": "Gate checks record movement decisions without mutating package state by themselves.",
            "external_side_effect": False,
            "approval_required": False,
            "approval_status": "not_required",
        },
        "task": {
            "objective": f"Evaluate gate '{gate_id}'.",
            "stop_condition": "Gate result recorded in reviewable-runs/logs/.",
            "non_goals": [
                "Do not mutate lifecycle state from the gate check alone.",
            ],
        },
        "decision": gate_result["decision"],
        "status": gate_result["status"],
        "required_artifacts": gate_result["required_artifacts"],
        "missing_artifacts": gate_result["missing_artifacts"],
        "recommended_workflow": gate_result["recommended_workflow"],
        "recommended_validator": gate_result["recommended_validator"],
        "proof_mode": gate_result["proof_mode"],
        "verification": {
            "checks": [
                {
                    "name": "gate_check_written",
                    "result": "pass",
                    "notes": repo_relpath(log_path),
                }
            ],
            "residual_risk": "Gate checks capture the current bounded decision, but the underlying artifacts still need normal human review when the stakes are high.",
        },
    }
    log_path.write_text(json.dumps(payload, indent=2) + "\n")
    return repo_relpath(log_path)


def slugify_idea(idea: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", idea.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    if not slug:
        raise ValueError("Could not derive a slug from the provided idea.")
    return slug


def title_from_slug(slug: str) -> str:
    return slug.replace("-", " ").title()


def init_package_manifest(
    package_path: Path,
    markdown_relpath: str,
    discovery_packet_path: Path | None = None,
) -> dict:
    stages = {stage: {"done": False, "last_updated": None} for stage in STAGES}
    config = {
        "markdown_path": markdown_relpath,
    }
    if discovery_packet_path is not None:
        config["discovery_packet_path"] = repo_relpath(discovery_packet_path)
    return {
        "kind": "leaf",
        "publication": package_path.name,
        "revision": 1,
        "config": config,
        "stages": stages,
    }


def initialize_package(
    idea: str | None,
    slug: str | None = None,
    topic_packet_path: Path | None = None,
) -> dict:
    packet = None
    if topic_packet_path is not None:
        packet = parse_topic_packet(topic_packet_path)
        if packet.get("decision") != "package_init_ready":
            raise ValueError(
                "Topic packet must resolve to Decision: package_init_ready before package:init --from-topic-packet."
            )

    effective_idea = (idea or packet.get("one_sentence_promise") if packet else None) or ""
    effective_idea = effective_idea.strip()
    if not effective_idea:
        raise ValueError("initialize_package requires --idea or a topic packet with a one-sentence promise.")

    package_slug = slug or (packet.get("proposed_slug") if packet else None) or slugify_idea(effective_idea)
    package_path = PUBLICATIONS_DIR / package_slug
    if package_path.exists():
        raise FileExistsError(f"Package already exists: publications/{package_slug}")

    markdown_name = f"{package_slug}.md"
    markdown_relpath = f"publications/{package_slug}/{markdown_name}"

    (package_path / "papers" / "markdown").mkdir(parents=True)
    (package_path / "artifacts").mkdir()
    (package_path / "archive").mkdir()

    title = title_from_slug(package_slug)
    readme_lines = [
        f"# {title}",
        "",
        f"Current idea: {effective_idea}",
        "",
        "This package was initialized for the Phase 1.5 harness flow.",
        "",
        "## Canonical Surfaces",
        "",
        f"- live draft: `{markdown_name}`",
        "- papers: `papers/`",
        "- artifacts: `artifacts/`",
        "- archive: `archive/`",
        "",
    ]
    if packet is not None:
        readme_lines.extend(
            [
                "## Discovery Handoff",
                "",
                f"- discovery packet: `{repo_relpath(topic_packet_path)}`",
                f"- one-sentence promise: {packet.get('one_sentence_promise') or effective_idea}",
                f"- first research question: {packet.get('first_research_question') or 'TBD'}",
            ]
        )
        shortlist = packet.get("initial_paper_shortlist") or []
        if shortlist:
            readme_lines.extend(["- initial paper shortlist:"])
            for item in shortlist:
                readme_lines.append(f"  - {item}")
        blocked = packet.get("near_misses_and_blocked_framings") or []
        if blocked:
            readme_lines.extend(["- near-misses and blocked framings:"])
            for item in blocked:
                readme_lines.append(f"  - {item}")
        readme_lines.append("")
    (package_path / "README.md").write_text("\n".join(readme_lines))

    draft_lines = [
        f"# {title}",
        "",
        "> Initialized by `package:init`.",
        "",
        "## Working Thesis",
        "",
        packet.get("one_sentence_promise") if packet else effective_idea,
        "",
    ]
    if packet is not None:
        draft_lines.extend(
            [
                "## First Research Question",
                "",
                packet.get("first_research_question") or "TBD",
                "",
            ]
        )
    (package_path / markdown_name).write_text("\n".join(draft_lines))

    (package_path / "papers" / "index.md").write_text(
        "\n".join(
            [
                "# Paper Index",
                "",
                "No papers have been admitted into this package yet.",
                "",
            ]
        )
    )

    status = init_package_manifest(package_path, markdown_relpath, discovery_packet_path=topic_packet_path)
    (package_path / "status.yaml").write_text(
        yaml.safe_dump(status, default_flow_style=False, sort_keys=False)
    )

    next_stage = next_stage_for_package(package_path, status) or "research"
    return {
        "package": package_slug,
        "package_path": f"publications/{package_slug}",
        "markdown_path": markdown_relpath,
        "status_path": f"publications/{package_slug}/status.yaml",
        "next_stage": next_stage,
        "suggested_command": f"npm run stage:next -- --package {package_slug} --format json",
    }
