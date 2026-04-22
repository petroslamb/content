#!/usr/bin/env python3
"""Shared lifecycle, workflow, gate, and profile helpers."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLICATIONS_DIR = REPO_ROOT / "publications"
WORKFLOWS_DIR = REPO_ROOT / "workflows"
GATE_CONTRACTS_PATH = REPO_ROOT / "gate_contracts.yaml"
PIPELINE_PROFILES_PATH = REPO_ROOT / "pipeline_profiles.yaml"

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

WORKFLOW_REQUIRED_KEYS = [
    "workflow_id",
    "workflow_kind",
    "stability",
    "runner_mode",
    "default_skill",
    "launch_templates",
    "required_context",
    "expected_outputs",
    "done_when",
    "approval_gate",
]

WORKFLOW_OPTIONAL_DEFAULTS = {
    "stage_binding": None,
    "launch_mode": "none",
    "packet_templates": [],
    "validator_commands": [],
    "judgment_policy": "unrestricted",
    "prohibited_moves": [],
}

VALID_WORKFLOW_KINDS = {
    "stage",
    "module",
    "overlay",
}

VALID_WORKFLOW_STABILITY = {
    "canonical",
    "experimental",
}

VALID_RUNNER_MODES = {
    "guided",
    "scripted",
    "hybrid",
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

GATE_REQUIRED_KEYS = [
    "description",
    "scope",
    "required_artifacts",
    "recommended_workflow",
    "recommended_validator",
    "proof_mode",
]

PROFILE_REQUIRED_KEYS = [
    "description",
    "ordered_workflows",
    "required_gates",
    "allowed_entry_workflows",
    "fallback_routes",
]


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


def workflow_doc_paths() -> list[Path]:
    return sorted(
        path
        for path in WORKFLOWS_DIR.glob("*/README.md")
        if path.parent.name != "skills"
    )


def _validate_list(metadata: dict, workflow_path: Path, key: str) -> None:
    if not isinstance(metadata.get(key), list):
        raise ValueError(
            f"Workflow doc {workflow_path.relative_to(REPO_ROOT)} must define {key} as a list."
        )


def _load_workflow_contract_from_path(workflow_path: Path) -> dict:
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

    metadata = {**WORKFLOW_OPTIONAL_DEFAULTS, **metadata}
    workflow_id = metadata["workflow_id"]
    workflow_kind = metadata["workflow_kind"]
    stability = metadata["stability"]
    stage_binding = metadata.get("stage_binding")

    if not isinstance(workflow_id, str) or not workflow_id.strip():
        raise ValueError(
            f"Workflow doc {workflow_path.relative_to(REPO_ROOT)} must define a non-empty workflow_id."
        )

    if workflow_kind not in VALID_WORKFLOW_KINDS:
        raise ValueError(
            f"Workflow doc {workflow_path.relative_to(REPO_ROOT)} has invalid workflow_kind '{workflow_kind}'."
        )

    if stability not in VALID_WORKFLOW_STABILITY:
        raise ValueError(
            f"Workflow doc {workflow_path.relative_to(REPO_ROOT)} has invalid stability '{stability}'."
        )

    if workflow_kind == "stage":
        if stage_binding not in STAGES:
            raise ValueError(
                f"Workflow doc {workflow_path.relative_to(REPO_ROOT)} must bind stage workflows to one of: {', '.join(STAGES)}."
            )
        if workflow_id != stage_binding:
            raise ValueError(
                f"Workflow doc {workflow_path.relative_to(REPO_ROOT)} declares workflow_id '{workflow_id}' "
                f"but stage_binding '{stage_binding}'. Stage workflows must keep workflow_id == stage_binding."
            )
    elif stage_binding is not None:
        raise ValueError(
            f"Workflow doc {workflow_path.relative_to(REPO_ROOT)} may not set stage_binding unless workflow_kind is 'stage'."
        )

    runner_mode = metadata["runner_mode"]
    if runner_mode not in VALID_RUNNER_MODES:
        raise ValueError(
            f"Workflow doc {workflow_path.relative_to(REPO_ROOT)} has invalid runner_mode '{runner_mode}'."
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

    for key in ["required_context", "expected_outputs", "done_when"]:
        _validate_list(metadata, workflow_path, key)

    for key in ["launch_templates", "packet_templates", "validator_commands", "prohibited_moves"]:
        _validate_list(metadata, workflow_path, key)

    if metadata["default_skill"] is not None and not isinstance(metadata["default_skill"], str):
        raise ValueError(
            f"Workflow doc {workflow_path.relative_to(REPO_ROOT)} must define default_skill as a string or null."
        )

    return {
        "workflow_id": workflow_id,
        "path": workflow_path,
        "metadata": metadata,
        "body": body,
    }


@lru_cache(maxsize=1)
def load_all_workflow_contracts() -> dict[str, dict]:
    contracts: dict[str, dict] = {}
    stage_paths: dict[str, Path] = {}
    for workflow_path in workflow_doc_paths():
        contract = _load_workflow_contract_from_path(workflow_path)
        workflow_id = contract["workflow_id"]
        if workflow_id in contracts:
            raise ValueError(
                f"Duplicate workflow_id '{workflow_id}' in {workflow_path.relative_to(REPO_ROOT)} "
                f"and {contracts[workflow_id]['path'].relative_to(REPO_ROOT)}."
            )
        contracts[workflow_id] = contract
        stage_binding = contract["metadata"].get("stage_binding")
        if stage_binding is not None:
            if stage_binding in stage_paths:
                raise ValueError(
                    f"Multiple workflows bind the stage '{stage_binding}': "
                    f"{stage_paths[stage_binding].relative_to(REPO_ROOT)} and {workflow_path.relative_to(REPO_ROOT)}."
                )
            stage_paths[stage_binding] = workflow_path

    missing_stage_bindings = [stage for stage in STAGES if stage not in stage_paths]
    if missing_stage_bindings:
        raise ValueError(
            "Missing stage-bound workflow docs for stages: " + ", ".join(missing_stage_bindings)
        )

    return contracts


def stage_workflow_paths() -> dict[str, str]:
    paths: dict[str, str] = {}
    for contract in load_all_workflow_contracts().values():
        stage_binding = contract["metadata"].get("stage_binding")
        if stage_binding is not None:
            paths[stage_binding] = contract["path"].relative_to(REPO_ROOT).as_posix()
    return paths


def resolve_workflow_path(workflow_id: str) -> Path:
    try:
        return load_all_workflow_contracts()[workflow_id]["path"]
    except KeyError as exc:
        raise KeyError(f"Unknown workflow '{workflow_id}'") from exc


def load_workflow_contract(workflow_id: str) -> dict:
    try:
        return load_all_workflow_contracts()[workflow_id]
    except KeyError as exc:
        raise KeyError(f"Unknown workflow '{workflow_id}'") from exc


def load_stage_workflow_contract(stage: str) -> dict:
    contract = load_workflow_contract(stage)
    metadata = contract["metadata"]
    if metadata.get("workflow_kind") != "stage" or metadata.get("stage_binding") != stage:
        raise ValueError(f"Workflow '{stage}' is not a valid stage-bound workflow.")
    return contract


def _load_mapping_yaml(path: Path, label: str) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"{label} file not found: {path.relative_to(REPO_ROOT)}")
    data = yaml.safe_load(path.read_text()) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{label} file must be a mapping: {path.relative_to(REPO_ROOT)}")
    return data


@lru_cache(maxsize=1)
def load_gate_contracts() -> dict[str, dict]:
    data = _load_mapping_yaml(GATE_CONTRACTS_PATH, "Gate contract")
    gates = data.get("gates", {})
    if not isinstance(gates, dict):
        raise ValueError("gate_contracts.yaml must define a top-level 'gates' mapping.")

    contracts: dict[str, dict] = {}
    for gate_id, contract in sorted(gates.items()):
        if not isinstance(contract, dict):
            raise ValueError(f"Gate '{gate_id}' must be a mapping.")
        missing = [key for key in GATE_REQUIRED_KEYS if key not in contract]
        if missing:
            raise ValueError(
                f"Gate '{gate_id}' is missing required keys: {', '.join(missing)}"
            )
        if contract["scope"] not in {"packet", "package"}:
            raise ValueError(f"Gate '{gate_id}' has invalid scope '{contract['scope']}'.")
        for key in ["required_artifacts"]:
            if not isinstance(contract[key], list):
                raise ValueError(f"Gate '{gate_id}' field '{key}' must be a list.")
        contracts[gate_id] = contract
    return contracts


@lru_cache(maxsize=1)
def load_pipeline_profiles() -> dict[str, dict]:
    data = _load_mapping_yaml(PIPELINE_PROFILES_PATH, "Pipeline profile")
    profiles = data.get("profiles", {})
    if not isinstance(profiles, dict):
        raise ValueError("pipeline_profiles.yaml must define a top-level 'profiles' mapping.")

    workflow_ids = set(load_all_workflow_contracts().keys())
    gate_ids = set(load_gate_contracts().keys())
    contracts: dict[str, dict] = {}
    for profile_id, contract in sorted(profiles.items()):
        if not isinstance(contract, dict):
            raise ValueError(f"Pipeline profile '{profile_id}' must be a mapping.")
        missing = [key for key in PROFILE_REQUIRED_KEYS if key not in contract]
        if missing:
            raise ValueError(
                f"Pipeline profile '{profile_id}' is missing required keys: {', '.join(missing)}"
            )
        for key in ["ordered_workflows", "required_gates", "allowed_entry_workflows"]:
            if not isinstance(contract[key], list):
                raise ValueError(f"Pipeline profile '{profile_id}' field '{key}' must be a list.")
        if not isinstance(contract["fallback_routes"], dict):
            raise ValueError(f"Pipeline profile '{profile_id}' field 'fallback_routes' must be a mapping.")

        unknown_workflows = sorted(set(contract["ordered_workflows"]) - workflow_ids)
        if unknown_workflows:
            raise ValueError(
                f"Pipeline profile '{profile_id}' references unknown workflows: {', '.join(unknown_workflows)}"
            )
        unknown_entry = sorted(set(contract["allowed_entry_workflows"]) - workflow_ids)
        if unknown_entry:
            raise ValueError(
                f"Pipeline profile '{profile_id}' references unknown allowed-entry workflows: {', '.join(unknown_entry)}"
            )
        unknown_gates = sorted(set(contract["required_gates"]) - gate_ids)
        if unknown_gates:
            raise ValueError(
                f"Pipeline profile '{profile_id}' references unknown gates: {', '.join(unknown_gates)}"
            )
        fallback_unknown = sorted(
            key for key, value in contract["fallback_routes"].items()
            if key not in gate_ids or (isinstance(value, str) and value not in workflow_ids and value not in {"stay_put", "overlay"})
        )
        if fallback_unknown:
            raise ValueError(
                f"Pipeline profile '{profile_id}' has unknown fallback route references: {', '.join(fallback_unknown)}"
            )
        contracts[profile_id] = contract
    return contracts
