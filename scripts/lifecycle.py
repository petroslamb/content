#!/usr/bin/env python3
"""
Shared lifecycle constants and helpers for publication package manifests and
workflow contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLICATIONS_DIR = REPO_ROOT / "publications"
WORKFLOWS_DIR = REPO_ROOT / "workflows"

STAGES = [
    "paper_intake",
    "research",
    "essay_iteration",
    "notebooklm_artifacts",
    "article_polish",
    "substack_publishing",
    "archive_sync",
    "youtube_production",
    "distribution",
]

DEPENDENCY_MAP = {
    "substack_publishing": ["article_polish"],
    "archive_sync": ["substack_publishing"],
    "youtube_production": ["essay_iteration"],
    "distribution": ["substack_publishing"],
}

STAGE_WORKFLOW_PATHS = {
    "paper_intake": "workflows/paper-intake/README.md",
    "research": "workflows/alphaxiv-research/README.md",
    "essay_iteration": "workflows/essay-iteration/README.md",
    "notebooklm_artifacts": "workflows/notebooklm-artifacts/README.md",
    "article_polish": "workflows/article-polish/README.md",
    "substack_publishing": "workflows/substack-publishing/README.md",
    "archive_sync": "workflows/substack-archive-sync/README.md",
    "youtube_production": "workflows/youtube-production/README.md",
    "distribution": "workflows/distribution/README.md",
}

WORKFLOW_REQUIRED_KEYS = [
    "workflow_id",
    "runner_mode",
    "default_skill",
    "launch_templates",
    "required_context",
    "expected_outputs",
    "done_when",
    "approval_gate",
]

WORKFLOW_OPTIONAL_DEFAULTS = {
    "launch_mode": "none",
    "packet_templates": [],
    "validator_commands": [],
    "judgment_policy": "unrestricted",
    "prohibited_moves": [],
}

VALID_LAUNCH_MODES = {
    "none",
    "scaffold_only",
    "local_mutation",
    "external_mutation",
}

VALID_JUDGMENT_POLICIES = {
    "unrestricted",
    "draft_only",
    "conditional_promote",
    "full_promote",
}


@dataclass(frozen=True)
class ManifestRef:
    package_key: str
    package_path: Path
    status_path: Path


def coerce_package_key(package_arg: str) -> str:
    package_key = package_arg.strip().strip("/")
    if package_key.startswith("publications/"):
        package_key = package_key[len("publications/") :]
    return package_key


def resolve_package_path(package_arg: str) -> Path:
    package_key = coerce_package_key(package_arg)
    if not package_key:
        raise ValueError("Package path cannot be empty.")
    package_path = (PUBLICATIONS_DIR / package_key).resolve()
    try:
        package_path.relative_to(PUBLICATIONS_DIR)
    except ValueError as exc:
        raise ValueError(f"Package path must stay within {PUBLICATIONS_DIR}") from exc
    if not package_path.exists():
        raise ValueError(f"Package path does not exist: publications/{package_key}")
    return package_path


def package_key_for_path(package_path: Path) -> str:
    return package_path.resolve().relative_to(PUBLICATIONS_DIR).as_posix()


def status_path_for_package(package_path: Path) -> Path:
    return package_path / "status.yaml"


def manifest_ref(package_path: Path) -> ManifestRef:
    package_path = package_path.resolve()
    return ManifestRef(
        package_key=package_key_for_path(package_path),
        package_path=package_path,
        status_path=status_path_for_package(package_path),
    )


def load_status(package_path: Path) -> dict | None:
    status_path = status_path_for_package(package_path)
    if not status_path.exists():
        return None
    with open(status_path, "r") as handle:
        return yaml.safe_load(handle)


def save_status(package_path: Path, data: dict) -> None:
    status_path = status_path_for_package(package_path)
    with open(status_path, "w") as handle:
        yaml.dump(data, handle, default_flow_style=False, sort_keys=False)


def load_status_ref(package_arg: str) -> tuple[ManifestRef, dict]:
    package_path = resolve_package_path(package_arg)
    status_data = load_status(package_path)
    if status_data is None:
        raise FileNotFoundError(f"No status.yaml found for package '{coerce_package_key(package_arg)}'")
    return manifest_ref(package_path), status_data


def iter_status_refs() -> list[ManifestRef]:
    refs = []
    for status_path in sorted(PUBLICATIONS_DIR.glob("**/status.yaml")):
        package_path = status_path.parent.resolve()
        refs.append(manifest_ref(package_path))
    return refs


def is_leaf_manifest(status_data: dict) -> bool:
    return status_data.get("kind", "leaf") == "leaf"


def iter_leaf_status_refs() -> list[tuple[ManifestRef, dict]]:
    refs = []
    for ref in iter_status_refs():
        status_data = load_status(ref.package_path)
        if status_data and is_leaf_manifest(status_data):
            refs.append((ref, status_data))
    return refs


def resolve_workflow_path(stage: str) -> Path:
    if stage not in STAGE_WORKFLOW_PATHS:
        raise KeyError(f"Unknown stage '{stage}'")
    return REPO_ROOT / STAGE_WORKFLOW_PATHS[stage]


def split_frontmatter(text: str) -> tuple[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("Workflow doc is missing YAML frontmatter.")
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            frontmatter = "\n".join(lines[1:idx])
            body = "\n".join(lines[idx + 1 :])
            if text.endswith("\n"):
                body += "\n"
            return frontmatter, body
    raise ValueError("Workflow doc frontmatter is missing a closing '---' line.")


def load_workflow_contract(stage: str) -> dict:
    workflow_path = resolve_workflow_path(stage)
    if not workflow_path.exists():
        raise FileNotFoundError(f"Workflow doc not found for stage '{stage}': {workflow_path}")

    text = workflow_path.read_text()
    frontmatter_text, body = split_frontmatter(text)
    metadata = yaml.safe_load(frontmatter_text) or {}
    if not isinstance(metadata, dict):
        raise ValueError(
            f"Workflow doc {workflow_path.relative_to(REPO_ROOT)} frontmatter must be a mapping."
        )

    missing = [key for key in WORKFLOW_REQUIRED_KEYS if key not in metadata]
    if missing:
        raise ValueError(
            f"Workflow doc {workflow_path.relative_to(REPO_ROOT)} is missing required keys: {', '.join(missing)}"
        )

    if metadata["workflow_id"] != stage:
        raise ValueError(
            f"Workflow doc {workflow_path.relative_to(REPO_ROOT)} declares workflow_id "
            f"'{metadata['workflow_id']}', expected '{stage}'."
        )

    metadata = {**WORKFLOW_OPTIONAL_DEFAULTS, **metadata}

    runner_mode = metadata["runner_mode"]
    if runner_mode not in {"guided", "scripted", "hybrid"}:
        raise ValueError(
            f"Workflow doc {workflow_path.relative_to(REPO_ROOT)} has invalid runner_mode '{runner_mode}'."
        )

    launch_templates = metadata.get("launch_templates") or []
    if not isinstance(launch_templates, list):
        raise ValueError(
            f"Workflow doc {workflow_path.relative_to(REPO_ROOT)} must define launch_templates as a list."
        )

    launch_mode = metadata["launch_mode"]
    if launch_mode not in VALID_LAUNCH_MODES:
        raise ValueError(
            f"Workflow doc {workflow_path.relative_to(REPO_ROOT)} has invalid launch_mode '{launch_mode}'."
        )

    judgment_policy = metadata["judgment_policy"]
    if judgment_policy not in VALID_JUDGMENT_POLICIES:
        raise ValueError(
            f"Workflow doc {workflow_path.relative_to(REPO_ROOT)} has invalid judgment_policy '{judgment_policy}'."
        )

    for list_key in ["required_context", "expected_outputs", "done_when"]:
        if not isinstance(metadata[list_key], list):
            raise ValueError(
                f"Workflow doc {workflow_path.relative_to(REPO_ROOT)} must define {list_key} as a list."
            )

    for list_key in ["packet_templates", "validator_commands", "prohibited_moves"]:
        if not isinstance(metadata[list_key], list):
            raise ValueError(
                f"Workflow doc {workflow_path.relative_to(REPO_ROOT)} must define {list_key} as a list."
            )

    return {
        "stage": stage,
        "path": workflow_path,
        "metadata": metadata,
        "body": body,
    }
