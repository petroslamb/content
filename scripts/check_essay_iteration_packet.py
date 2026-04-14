#!/usr/bin/env python3
"""
Validate the package-local essay-iteration packet.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml

from essay_iteration_support import (
    ARCHIVE_ANCHOR_FIELDS,
    BLUEPRINT_HEADINGS,
    CANDIDATE_LIMITS_HEADINGS,
    CANDIDATE_REFERENCES_HEADINGS,
    DECISION_BODY_HEADINGS,
    DECISION_FRONTMATTER_FIELDS,
    PASSAGE_ANCHOR_FIELDS,
    REVIEW_BODY_HEADINGS,
    REVIEW_FRONTMATTER_FIELDS,
    SCORECARD_BODY_HEADINGS,
    SCORECARD_FRONTMATTER_FIELDS,
    build_packet_paths,
    resolve_live_draft,
)
from lifecycle import REPO_ROOT, load_status_ref, split_frontmatter


REQUIRED_PACKET_OUTPUTS = {
    "manifest",
    "blueprint",
    "candidate",
    "replacement_review",
    "atlas_scorecard",
    "decision",
}


def load_packet_manifest(package_key: str) -> tuple[dict, dict]:
    manifest_ref, status_data = load_status_ref(package_key)
    live_draft_path = resolve_live_draft(manifest_ref.package_path, status_data)
    if live_draft_path is None:
        raise FileNotFoundError(f"Package '{manifest_ref.package_key}' is missing a resolvable live draft.")

    revision = status_data.get("revision", 1)
    if not isinstance(revision, int):
        raise ValueError(f"Package '{manifest_ref.package_key}' has a non-integer revision.")

    packet_paths = build_packet_paths(live_draft_path, revision)
    manifest_path = packet_paths["manifest"]
    if not manifest_path.exists():
        raise FileNotFoundError(
            f"Essay-iteration packet manifest does not exist for '{manifest_ref.package_key}': {manifest_path}"
        )
    return json.loads(manifest_path.read_text()), status_data


def parse_markdown_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text()
    frontmatter_text, body = split_frontmatter(text)
    frontmatter = yaml.safe_load(frontmatter_text) or {}
    if not isinstance(frontmatter, dict):
        raise ValueError(f"Frontmatter in {path} must be a mapping.")
    return frontmatter, body


def validate_required_headings(text: str, headings: list[str], label: str, errors: list[str]) -> None:
    for heading in headings:
        if heading not in text:
            errors.append(f"{label} is missing required heading '{heading}'.")


def validate_required_fields(frontmatter: dict, fields: list[str], label: str, errors: list[str]) -> None:
    for field in fields:
        if field not in frontmatter:
            errors.append(f"{label} frontmatter is missing required field '{field}'.")


def validate_nonempty_fields(frontmatter: dict, fields: list[str], label: str, errors: list[str]) -> None:
    for field in fields:
        value = frontmatter.get(field)
        if value in (None, "", []):
            errors.append(f"{label} frontmatter field '{field}' must be filled in.")


def validate_candidate_sections(candidate_text: str, errors: list[str]) -> None:
    if not any(heading in candidate_text for heading in CANDIDATE_LIMITS_HEADINGS):
        errors.append("Candidate draft is missing a limits or borders section.")
    if not any(heading in candidate_text for heading in CANDIDATE_REFERENCES_HEADINGS):
        errors.append("Candidate draft is missing a references or endmatter section.")


def validate_voice_rules(candidate_text: str, voice_rules_path: Path, errors: list[str]) -> None:
    rules = yaml.safe_load(voice_rules_path.read_text()) or {}
    banned_literals = rules.get("banned_literals", [])
    banned_regex = rules.get("banned_regex", [])

    for literal in banned_literals:
        if literal and literal in candidate_text:
            errors.append(f"Candidate draft violates voice rule literal '{literal}'.")

    for pattern in banned_regex:
        if pattern and re.search(pattern, candidate_text):
            errors.append(f"Candidate draft violates voice rule regex '{pattern}'.")


def parse_publication_power(value: object) -> float | None:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def validate_packet(packet: dict) -> list[str]:
    errors: list[str] = []
    output_paths = packet.get("output_paths", {})
    missing_outputs = sorted(REQUIRED_PACKET_OUTPUTS - set(output_paths.keys()))
    if missing_outputs:
        errors.append(f"Packet manifest is missing output paths: {', '.join(missing_outputs)}")
        return errors

    resolved_outputs = {name: (REPO_ROOT / relpath).resolve() for name, relpath in output_paths.items()}
    for name, path in resolved_outputs.items():
        if not path.exists():
            errors.append(f"Packet output '{name}' does not exist: {path}")

    if errors:
        return errors

    live_draft_path = (REPO_ROOT / packet["live_draft_path"]).resolve()
    candidate_path = (REPO_ROOT / packet["candidate_path"]).resolve()
    if not live_draft_path.exists():
        errors.append(f"Live draft does not exist: {live_draft_path}")
    if live_draft_path == candidate_path:
        errors.append("Candidate path must differ from the live draft path.")

    blueprint_text = resolved_outputs["blueprint"].read_text()
    validate_required_headings(blueprint_text, BLUEPRINT_HEADINGS, "Blueprint", errors)

    candidate_text = candidate_path.read_text()
    validate_candidate_sections(candidate_text, errors)

    voice_rules_relpath = packet.get("input_paths", {}).get("voice_rules_path")
    if not voice_rules_relpath:
        errors.append("Packet manifest is missing input_paths.voice_rules_path.")
    else:
        validate_voice_rules(candidate_text, (REPO_ROOT / voice_rules_relpath).resolve(), errors)

    review_frontmatter, review_body = parse_markdown_frontmatter(resolved_outputs["replacement_review"])
    validate_required_fields(review_frontmatter, REVIEW_FRONTMATTER_FIELDS, "Replacement review", errors)
    validate_required_headings(review_body, REVIEW_BODY_HEADINGS, "Replacement review", errors)

    scorecard_frontmatter, scorecard_body = parse_markdown_frontmatter(resolved_outputs["atlas_scorecard"])
    validate_required_fields(scorecard_frontmatter, SCORECARD_FRONTMATTER_FIELDS, "Atlas scorecard", errors)
    validate_required_headings(scorecard_body, SCORECARD_BODY_HEADINGS, "Atlas scorecard", errors)
    validate_nonempty_fields(scorecard_frontmatter, PASSAGE_ANCHOR_FIELDS, "Atlas scorecard", errors)
    validate_nonempty_fields(scorecard_frontmatter, ARCHIVE_ANCHOR_FIELDS, "Atlas scorecard", errors)

    decision_frontmatter, decision_body = parse_markdown_frontmatter(resolved_outputs["decision"])
    validate_required_fields(decision_frontmatter, DECISION_FRONTMATTER_FIELDS, "Decision", errors)
    validate_required_headings(decision_body, DECISION_BODY_HEADINGS, "Decision", errors)

    judgment_policy = packet.get("judgment_policy", "unrestricted")
    publication_power = parse_publication_power(scorecard_frontmatter.get("publication_power"))
    if judgment_policy == "draft_only":
        if publication_power is not None and publication_power >= 9:
            errors.append("Draft-only packet may not claim Publication Power 9 or above.")
        if decision_frontmatter.get("promotion_allowed") is True:
            errors.append("Draft-only packet may not allow promotion in the decision file.")
        if decision_frontmatter.get("recommendation") == "promote_candidate":
            errors.append("Draft-only packet may not recommend promote_candidate.")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a package-local essay-iteration packet.")
    parser.add_argument("--package", required=True, help="Leaf package path relative to publications/")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    try:
        packet, _ = load_packet_manifest(args.package)
        errors = validate_packet(packet)
    except Exception as exc:
        payload = {"success": False, "errors": [str(exc)]}
        if args.format == "json":
            print(json.dumps(payload, indent=2))
        else:
            print("Essay-iteration packet validation failed:")
            print(f"  - {exc}")
        raise SystemExit(1)

    payload = {
        "success": not errors,
        "packet_manifest_path": packet.get("packet_manifest_path"),
        "errors": errors,
    }
    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        if errors:
            print("Essay-iteration packet validation failed:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("Essay-iteration packet validation passed.")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
