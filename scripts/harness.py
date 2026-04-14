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
from essay_iteration_support import (
    describe_packet_paths,
    resolve_companion_path,
    resolve_evidence_surface as resolve_essay_evidence_surface,
    resolve_leaf_readme,
    resolve_live_draft,
    resolve_nearest_blueprint_path,
    resolve_parent_package_path,
    resolve_parent_package_readme,
    resolve_review_artifact_paths,
)
from lifecycle import PUBLICATIONS_DIR, REPO_ROOT, STAGES, load_status_ref, load_workflow_contract


PACKAGE_JSON_PATH = REPO_ROOT / "package.json"
HARNESS_CONTRACT_PATH = REPO_ROOT / "harness_contract.yaml"
HARNESS_POLICY_PATH = REPO_ROOT / "harness_policy.yaml"
LOGS_DIR = REPO_ROOT / "reviewable-runs" / "logs"

REQUIRED_NPM_SCRIPTS = {
    "check:essay-iteration",
    "stage:next",
    "stage:resolve",
    "stage:run",
    "package:init",
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
    stage_contracts = {}
    for stage in STAGES:
        workflow_contract = load_workflow_contract(stage)
        metadata = workflow_contract["metadata"]
        stage_contracts[stage] = {
            "workflow_doc": repo_relpath(workflow_contract["path"]),
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

    command_surface = {}
    for name in sorted(REQUIRED_NPM_SCRIPTS | {"status", "run"}):
        command_surface[name] = {
            "entrypoint": f"npm run {name}",
            "script": scripts.get(name),
        }

    return {
        "version": 1,
        "harness_target": "codex",
        "autonomy_scope": "local-first",
        "policy_file": "harness_policy.yaml",
        "sources_of_truth": {
            "lifecycle": "scripts/lifecycle.py",
            "workflow_frontmatter": "workflows/*/README.md",
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
        transcript_path = find_first_matching_file(search_root, (".srt", ".vtt", ".txt", ".json"))
        if transcript_path:
            return {"name": item, "status": "resolved", "blocking": False, "value": repo_relpath(transcript_path)}
        return {"name": item, "status": "missing", "blocking": True}

    return {"name": item, "status": "advisory", "blocking": False}


def resolve_required_context(package_path: Path, status_data: dict, required_context: list[str]) -> list[dict]:
    return [resolve_context_item(item, package_path, status_data) for item in required_context]


def stage_requires_approval(stage: str, metadata: dict, policy: dict) -> bool:
    if metadata.get("approval_gate") != "none":
        return True
    approval_stages = policy.get("approval_required", {}).get("stages", [])
    return stage in approval_stages


def compute_stage_capabilities(stage: str, metadata: dict, required_context: list[dict], policy: dict) -> tuple[bool, bool, list[str]]:
    blocking_issues = []
    missing_context = [item["name"] for item in required_context if item["status"] == "missing" and item.get("blocking")]
    blocking_issues.extend(f"Missing required context: {item}" for item in missing_context)

    requires_approval = stage_requires_approval(stage, metadata, policy)
    scaffold_only_execute = (
        metadata["runner_mode"] == "hybrid" and metadata["launch_mode"] == "scaffold_only"
    )
    runner_allows_execute = metadata["runner_mode"] == "scripted" or scaffold_only_execute

    if not runner_allows_execute:
        blocking_issues.append(
            f"Runner mode '{metadata['runner_mode']}' with launch_mode '{metadata['launch_mode']}' is not directly executable in Phase 1.5; resolve it or emit a launch pack."
        )

    approval_blocks_execute = requires_approval and not scaffold_only_execute

    if stage in policy.get("approval_required", {}).get("stages", []) and approval_blocks_execute:
        blocking_issues.append(
            f"Policy requires explicit approval before unattended execution of '{stage}'."
        )

    can_execute = (
        runner_allows_execute
        and not missing_context
        and not approval_blocks_execute
    )
    return requires_approval, can_execute, blocking_issues


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
    blueprint = resolve_nearest_blueprint_path(package_path, status_data)
    review_artifacts = resolve_review_artifact_paths(package_path, status_data)
    evidence_surface = resolve_essay_evidence_surface(package_path, status_data)

    return {
        "live_draft_path": repo_relpath(live_draft),
        "leaf_readme_path": repo_relpath(leaf_readme),
        "parent_package_path": repo_relpath(parent_path),
        "parent_package_readme_path": repo_relpath(parent_readme),
        "companion_path": repo_relpath(companion),
        "nearest_blueprint_path": repo_relpath(blueprint),
        "review_artifact_paths": [repo_relpath(path) for path in review_artifacts],
        "evidence_surface_path": repo_relpath(evidence_surface),
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
    package_context_paths = build_package_context_paths(manifest_ref.package_path, status_data)
    packet_paths = {}
    if stage == "essay_iteration":
        live_draft = resolve_markdown_path(manifest_ref.package_path, status_data)
        revision = status_data.get("revision")
        packet_paths = describe_packet_paths(live_draft, revision if isinstance(revision, int) else None)

    return {
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
        "default_skill": metadata["default_skill"],
        "launch_templates": metadata["launch_templates"],
        "packet_templates": resolve_packet_template_paths(metadata["packet_templates"]),
        "validator_commands": render_command_templates(metadata["validator_commands"], manifest_ref.package_key, status_data),
        "judgment_policy": metadata["judgment_policy"],
        "prohibited_moves": metadata["prohibited_moves"],
        "expected_outputs": metadata["expected_outputs"],
        "done_when": metadata["done_when"],
        "package_audit": audit_package(manifest_ref.package_key),
        "auto_mark_done_allowed": auto_mark_done_allowed(stage, metadata, policy),
        "current_state": status_data.get("stages", {}).get(stage, {"done": False, "last_updated": None}),
        "package_context_paths": package_context_paths,
        "packet_paths": packet_paths,
    }


def emit_launch_pack(resolution: dict) -> Path:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    package_id = resolution["package"].replace("/", "__")
    log_path = LOGS_DIR / f"{timestamp}_{package_id}_{resolution['stage']}_launch-pack.json"
    payload = {
        "kind": "harness_launch_pack",
        "timestamp": timestamp,
        "task_brief": (
            f"Advance package '{resolution['package']}' through the "
            f"'{resolution['stage']}' stage using '{resolution['workflow_doc']}'."
        ),
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
    }
    log_path.write_text(json.dumps(payload, indent=2) + "\n")
    return log_path


def slugify_idea(idea: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", idea.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    if not slug:
        raise ValueError("Could not derive a slug from the provided idea.")
    return slug


def title_from_slug(slug: str) -> str:
    return slug.replace("-", " ").title()


def init_package_manifest(package_path: Path, markdown_relpath: str) -> dict:
    stages = {stage: {"done": False, "last_updated": None} for stage in STAGES}
    return {
        "kind": "leaf",
        "publication": package_path.name,
        "revision": 1,
        "config": {
            "markdown_path": markdown_relpath,
        },
        "stages": stages,
    }


def initialize_package(idea: str, slug: str | None = None) -> dict:
    package_slug = slug or slugify_idea(idea)
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
        f"Current idea: {idea.strip()}",
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
    (package_path / "README.md").write_text("\n".join(readme_lines))

    draft_lines = [
        f"# {title}",
        "",
        "> Initialized by `package:init`.",
        "",
        "## Working Thesis",
        "",
        idea.strip(),
        "",
    ]
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

    status = init_package_manifest(package_path, markdown_relpath)
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
