#!/usr/bin/env python3
"""Validate the canonical package-local research-exit gate artifact."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

from essay_iteration_support import resolve_evidence_surface, resolve_governing_brief_path
from lifecycle import REPO_ROOT, load_status_ref, split_frontmatter
from research_exit_support import (
    CLAIM_BOUNDARY_STATUSES,
    RESEARCH_EXIT_BODY_HEADINGS,
    RESEARCH_EXIT_FRONTMATTER_FIELDS,
    RESEARCH_EXIT_VERDICTS,
    build_research_exit_gate_path,
    resolve_research_exit_gate_path,
    valid_blocker_slug,
)


def parse_markdown_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text()
    frontmatter_text, body = split_frontmatter(text)
    frontmatter = yaml.safe_load(frontmatter_text) or {}
    if not isinstance(frontmatter, dict):
        raise ValueError(f"Frontmatter in {path} must be a mapping.")
    return frontmatter, body


def validate_required_fields(frontmatter: dict, fields: list[str], errors: list[str]) -> None:
    missing = [field for field in fields if field not in frontmatter]
    if missing:
        errors.append("Research-exit gate is missing required frontmatter fields: " + ", ".join(missing))


def validate_required_headings(body: str, headings: list[str], errors: list[str]) -> None:
    missing = [heading for heading in headings if heading not in body]
    if missing:
        errors.append("Research-exit gate is missing required headings: " + ", ".join(missing))


def validate_research_exit_gate(package_arg: str) -> tuple[list[str], Path | None]:
    manifest_ref, status_data = load_status_ref(package_arg)
    revision = status_data.get("revision", 1)
    if not isinstance(revision, int):
        return (["status.yaml revision must be an integer."], None)

    gate_path = resolve_research_exit_gate_path(manifest_ref.package_path, revision)
    if gate_path is None:
        expected_path = build_research_exit_gate_path(manifest_ref.package_path, revision)
        return ([f"Research-exit gate is missing: {expected_path.relative_to(REPO_ROOT).as_posix()}"], expected_path)

    errors: list[str] = []
    try:
        frontmatter, body = parse_markdown_frontmatter(gate_path)
    except Exception as exc:
        return ([f"Failed to parse research-exit gate: {exc}"], gate_path)

    validate_required_fields(frontmatter, RESEARCH_EXIT_FRONTMATTER_FIELDS, errors)
    validate_required_headings(body, RESEARCH_EXIT_BODY_HEADINGS, errors)

    verdict = frontmatter.get("research_exit_verdict")
    if verdict not in RESEARCH_EXIT_VERDICTS:
        errors.append(
            "research_exit_verdict must be one of: "
            + ", ".join(sorted(RESEARCH_EXIT_VERDICTS))
            + "."
        )

    claim_boundary_status = frontmatter.get("claim_boundary_status")
    if claim_boundary_status not in CLAIM_BOUNDARY_STATUSES:
        errors.append(
            "claim_boundary_status must be one of: "
            + ", ".join(sorted(CLAIM_BOUNDARY_STATUSES))
            + "."
        )

    claim_boundary_paths = frontmatter.get("claim_boundary_paths")
    if not isinstance(claim_boundary_paths, list):
        errors.append("claim_boundary_paths must be a list.")

    follow_on_research_triggers = frontmatter.get("follow_on_research_triggers")
    if not isinstance(follow_on_research_triggers, list):
        errors.append("follow_on_research_triggers must be a list.")

    expected_governing_brief = resolve_governing_brief_path(manifest_ref.package_path, status_data)
    expected_evidence_surface = resolve_evidence_surface(manifest_ref.package_path, status_data)
    governing_brief_path = frontmatter.get("governing_brief_path")
    evidence_surface_path = frontmatter.get("evidence_surface_path")

    if expected_governing_brief is not None:
        expected_rel = expected_governing_brief.relative_to(REPO_ROOT).as_posix()
        if governing_brief_path != expected_rel:
            errors.append(
                "governing_brief_path does not match the package's resolvable governing brief."
            )

    if expected_evidence_surface is not None:
        expected_rel = expected_evidence_surface.relative_to(REPO_ROOT).as_posix()
        if evidence_surface_path != expected_rel:
            errors.append(
                "evidence_surface_path does not match the package's resolvable evidence surface."
            )

    blocker_slug = frontmatter.get("dominant_blocker_slug", "")
    if verdict == "pending":
        errors.append("research_exit_verdict must be settled before the gate passes.")
    elif verdict == "ready_for_essay_iteration":
        if claim_boundary_status not in {"satisfied", "not_required"}:
            errors.append(
                "ready_for_essay_iteration requires claim_boundary_status to be 'satisfied' or 'not_required'."
            )
        if blocker_slug not in ("", None):
            errors.append("ready_for_essay_iteration may not keep a dominant_blocker_slug.")
    elif verdict == "not_ready":
        if not valid_blocker_slug(blocker_slug):
            errors.append("not_ready requires a non-empty kebab-case dominant_blocker_slug.")

    return errors, gate_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the canonical package-local research-exit gate artifact.")
    parser.add_argument("--package", required=True, help="Leaf package path relative to publications/")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    try:
        errors, gate_path = validate_research_exit_gate(args.package)
    except (FileNotFoundError, ValueError, KeyError) as exc:
        errors = [str(exc)]
        gate_path = None

    payload = {
        "success": not errors,
        "errors": errors,
        "gate_path": gate_path.relative_to(REPO_ROOT).as_posix() if gate_path else None,
    }

    if args.format == "json":
        print(json.dumps(payload, indent=2))
        if errors:
            sys.exit(1)
        return

    if errors:
        print("Research-exit gate validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    print(f"Research-exit gate validation passed: {payload['gate_path']}")


if __name__ == "__main__":
    main()
