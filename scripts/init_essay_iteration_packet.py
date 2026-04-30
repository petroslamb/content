#!/usr/bin/env python3
"""
Initialize the package-local essay-iteration packet for a leaf publication package.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from string import Template

from essay_iteration_support import (
    ARCHIVE_ANCHOR_FIELDS,
    BLUEPRINT_HEADINGS,
    CANDIDATE_LIMITS_HEADINGS,
    CANDIDATE_REFERENCES_HEADINGS,
    CEILING_REPORT_BODY_HEADINGS,
    CEILING_REPORT_FRONTMATTER_FIELDS,
    DECISION_BODY_HEADINGS,
    DECISION_FRONTMATTER_FIELDS,
    ESCALATION_BLUEPRINT_HEADINGS,
    ESCALATION_DECISION_BODY_HEADINGS,
    ESCALATION_DECISION_FRONTMATTER_FIELDS,
    ESCALATION_REVIEW_BODY_HEADINGS,
    ESCALATION_REVIEW_FRONTMATTER_FIELDS,
    NORTH_STAR_ESCALATION_SCHEMA_VERSION,
    PACKET_TEMPLATE_TARGETS,
    PACKET_SCHEMA_VERSION,
    PASSAGE_ANCHOR_FIELDS,
    PREWRITE_BODY_HEADINGS,
    PREWRITE_FRONTMATTER_FIELDS,
    REVIEW_BODY_HEADINGS,
    REVIEW_FRONTMATTER_FIELDS,
    SCORECARD_BODY_HEADINGS,
    SCORECARD_FRONTMATTER_FIELDS,
    build_packet_paths,
    repo_relpath,
    resolve_companion_path,
    resolve_evidence_surface,
    resolve_governing_brief_path,
    resolve_leaf_readme,
    resolve_live_draft,
    resolve_nearest_blueprint_path,
    resolve_parent_package_readme,
    resolve_review_artifact_paths,
)
from harness import build_resolution_args, render_command_templates
from lifecycle import REPO_ROOT, load_status_ref, load_workflow_contract


VOICE_RULES_PATH = REPO_ROOT / "workflows" / "essay-iteration" / "voice_rules.yaml"


def load_template_text(template_path: Path) -> str:
    return template_path.read_text()


def should_write(path: Path, force: bool) -> bool:
    if not path.exists():
        return True
    if force:
        return True
    return not path.read_text().strip()


def write_template(path: Path, template_text: str, render_values: dict[str, object], force: bool) -> str:
    if not should_write(path, force):
        return "kept"
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = Template(template_text).safe_substitute(
        {key: "" if value is None else str(value) for key, value in render_values.items()}
    )
    path.write_text(rendered)
    return "written"


def build_packet_manifest(
    package_key: str,
    package_path: Path,
    status_data: dict,
    workflow_contract: dict,
) -> dict:
    live_draft_path = resolve_live_draft(package_path, status_data)
    if live_draft_path is None:
        raise FileNotFoundError(f"Package '{package_key}' is missing a resolvable live draft.")

    revision = status_data.get("revision", 1)
    if not isinstance(revision, int):
        raise ValueError(f"Package '{package_key}' has a non-integer revision in status.yaml.")

    packet_paths = build_packet_paths(live_draft_path, revision)
    metadata = workflow_contract["metadata"]
    packet_relpaths = {
        name: repo_relpath(path)
        for name, path in packet_paths.items()
    }

    leaf_readme = resolve_leaf_readme(package_path)
    parent_readme = resolve_parent_package_readme(package_path, status_data)
    companion = resolve_companion_path(package_path)
    configured_blueprint_value = status_data.get("config", {}).get("blueprint_path")
    configured_blueprint = None
    if isinstance(configured_blueprint_value, str) and configured_blueprint_value.strip():
        candidate = (package_path / configured_blueprint_value.strip()).resolve()
        try:
            candidate.relative_to(package_path.resolve())
        except ValueError:
            candidate = None
        if candidate is not None and candidate.exists():
            configured_blueprint = candidate
    governing_brief = resolve_governing_brief_path(package_path, status_data)
    nearest_blueprint = resolve_nearest_blueprint_path(package_path, status_data)
    review_artifacts = resolve_review_artifact_paths(package_path, status_data)
    evidence_surface = resolve_evidence_surface(package_path, status_data)
    if governing_brief is None:
        raise FileNotFoundError(
            f"Package '{package_key}' is missing a governing brief. "
            "Resolve config.blueprint_path or add a legacy blueprint/plan file."
        )

    packet_template_paths = {
        PACKET_TEMPLATE_TARGETS[Path(template).name]: repo_relpath((REPO_ROOT / template).resolve())
        for template in metadata["packet_templates"]
        if Path(template).name in PACKET_TEMPLATE_TARGETS
    }

    manifest = {
        "kind": "essay_iteration_packet",
        "package": package_key,
        "revision": revision,
        "packet_schema_version": PACKET_SCHEMA_VERSION,
        "workflow_doc": repo_relpath(workflow_contract["path"]),
        "judgment_policy": metadata["judgment_policy"],
        "live_draft_path": repo_relpath(live_draft_path),
        "candidate_path": packet_relpaths["candidate"],
        "packet_manifest_path": packet_relpaths["manifest"],
        "validator_commands": render_command_templates(metadata["validator_commands"], package_key, status_data),
        "prohibited_moves": metadata["prohibited_moves"],
        "archive_anchor_requirements": [
            "one nearby archive anchor",
            "one stronger archive anchor",
            "one weaker archive anchor",
        ],
        "input_paths": {
            "live_draft_path": repo_relpath(live_draft_path),
            "leaf_readme_path": repo_relpath(leaf_readme),
            "parent_package_readme_path": repo_relpath(parent_readme),
            "companion_path": repo_relpath(companion),
            "governing_brief_path": repo_relpath(governing_brief),
            "review_artifact_paths": [repo_relpath(path) for path in review_artifacts],
            "evidence_surface_path": repo_relpath(evidence_surface),
            "voice_rules_path": repo_relpath(VOICE_RULES_PATH),
        },
        "output_paths": packet_relpaths,
        "packet_templates": packet_template_paths,
        "required_sections": {
            "blueprint_headings": BLUEPRINT_HEADINGS,
            "prewrite_frontmatter_fields": PREWRITE_FRONTMATTER_FIELDS,
            "prewrite_body_headings": PREWRITE_BODY_HEADINGS,
            "review_frontmatter_fields": REVIEW_FRONTMATTER_FIELDS,
            "review_body_headings": REVIEW_BODY_HEADINGS,
            "scorecard_frontmatter_fields": SCORECARD_FRONTMATTER_FIELDS,
            "scorecard_body_headings": SCORECARD_BODY_HEADINGS,
            "decision_frontmatter_fields": DECISION_FRONTMATTER_FIELDS,
            "decision_body_headings": DECISION_BODY_HEADINGS,
            "ceiling_report_frontmatter_fields": CEILING_REPORT_FRONTMATTER_FIELDS,
            "ceiling_report_body_headings": CEILING_REPORT_BODY_HEADINGS,
            "candidate_limits_headings": CANDIDATE_LIMITS_HEADINGS,
            "candidate_references_headings": CANDIDATE_REFERENCES_HEADINGS,
            "archive_anchor_fields": ARCHIVE_ANCHOR_FIELDS,
            "passage_anchor_fields": PASSAGE_ANCHOR_FIELDS,
            "conditional_escalation_sections": {
                "trigger": {
                    "packet_schema_version_at_least": NORTH_STAR_ESCALATION_SCHEMA_VERSION,
                    "north_star_verdict": "below_north_star",
                    "recommendation": "revise_candidate",
                },
                "blueprint_headings": ESCALATION_BLUEPRINT_HEADINGS,
                "review_frontmatter_fields": ESCALATION_REVIEW_FRONTMATTER_FIELDS,
                "review_body_headings": ESCALATION_REVIEW_BODY_HEADINGS,
                "decision_frontmatter_fields": ESCALATION_DECISION_FRONTMATTER_FIELDS,
                "decision_body_headings": ESCALATION_DECISION_BODY_HEADINGS,
            },
        },
    }

    if nearest_blueprint and nearest_blueprint == governing_brief and configured_blueprint is None:
        manifest["input_paths"]["nearest_blueprint_path"] = repo_relpath(nearest_blueprint)

    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize the package-local essay-iteration packet.")
    parser.add_argument("--package", required=True, help="Leaf package path relative to publications/")
    parser.add_argument("--force", action="store_true", help="Overwrite existing non-empty packet files.")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    manifest_ref, status_data = load_status_ref(args.package)
    workflow_contract = load_workflow_contract("essay_iteration")
    live_draft_path = resolve_live_draft(manifest_ref.package_path, status_data)
    if live_draft_path is None:
        raise SystemExit(f"Package '{manifest_ref.package_key}' is missing config.markdown_path or the file does not exist.")

    packet_manifest = build_packet_manifest(
        manifest_ref.package_key,
        manifest_ref.package_path,
        status_data,
        workflow_contract,
    )
    packet_paths = build_packet_paths(live_draft_path, packet_manifest["revision"])

    render_values = {
        **build_resolution_args(manifest_ref.package_key, status_data),
        "revision": packet_manifest["revision"],
        "judgment_policy": packet_manifest["judgment_policy"],
        "live_draft_path": packet_manifest["live_draft_path"],
        "candidate_path": packet_manifest["output_paths"]["candidate"],
        "replacement_review_path": packet_manifest["output_paths"]["replacement_review"],
        "decision_path": packet_manifest["output_paths"]["decision"],
        "packet_manifest_path": packet_manifest["packet_manifest_path"],
    }

    file_status: dict[str, str] = {}
    for template in workflow_contract["metadata"]["packet_templates"]:
        template_path = (REPO_ROOT / template).resolve()
        target_name = PACKET_TEMPLATE_TARGETS.get(Path(template).name)
        if target_name is None:
            continue
        target_path = packet_paths[target_name]
        file_status[target_name] = write_template(
            target_path,
            load_template_text(template_path),
            render_values,
            args.force,
        )

    packet_paths["manifest"].parent.mkdir(parents=True, exist_ok=True)
    packet_paths["manifest"].write_text(json.dumps(packet_manifest, indent=2) + "\n")
    file_status["manifest"] = "written"

    payload = {
        "success": True,
        "package": manifest_ref.package_key,
        "packet_manifest_path": packet_manifest["packet_manifest_path"],
        "output_paths": packet_manifest["output_paths"],
        "file_status": file_status,
    }
    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(f"Initialized essay-iteration packet for {manifest_ref.package_key}")
        print(f"Packet manifest: {packet_manifest['packet_manifest_path']}")
        for name, status in file_status.items():
            print(f"  - {name}: {status}")


if __name__ == "__main__":
    main()
