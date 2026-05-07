#!/usr/bin/env python3
"""
Shared helpers for essay-iteration packet discovery, scaffolding, and validation.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

import yaml

from lifecycle import PUBLICATIONS_DIR, REPO_ROOT, load_status


PACKET_SCHEMA_VERSION = 4
NORTH_STAR_ESCALATION_SCHEMA_VERSION = 2

BLUEPRINT_PATTERNS = ("*blueprint*.md", "*plan*.md")
REVIEW_PATTERNS = ("*review*.md", "*scorecard*.md", "*claims*.md", "*rubric*.md")

BLUEPRINT_HEADINGS = [
    "## Promise",
    "## Spine",
    "## Paragraph burden",
    "## Evidence burden",
    "## Cut order",
    "## Failure triggers",
]

PREWRITE_FRONTMATTER_FIELDS = [
    "kind",
    "package",
    "revision",
    "judgment_policy",
    "live_draft_path",
    "candidate_path",
    "writability_verdict",
    "candidate_authorized",
    "dominant_blocker_slug",
    "supporting_artifact_paths",
]

PREWRITE_BODY_HEADINGS = [
    "## Promise",
    "## Spine",
    "## Paragraph burden",
    "## Evidence burden",
    "## Cut order",
    "## Failure triggers",
    "## Claim-State Gate",
    "## Writability Verdict",
    "## Required Follow-Through",
]

PREWRITE_WRITABILITY_VERDICTS = {
    "pending",
    "writable",
    "not_yet_writable",
}

CEILING_REPORT_FRONTMATTER_FIELDS = [
    "kind",
    "package",
    "revision",
    "live_draft_path",
    "terminal_candidate_path",
    "terminal_replacement_review_path",
    "terminal_decision_path",
    "dominant_blocker_slug",
    "ceiling_verdict",
    "effort_verdict",
    "next_route",
]

CEILING_REPORT_BODY_HEADINGS = [
    "## Verdict",
    "## Iteration Chronology",
    "## Blocker Timeline",
    "## Effort Audit",
    "## What Survived",
    "## What Did Not Survive",
    "## Lessons Learned",
    "## Next Route",
]

CEILING_REPORT_VERDICTS = {
    "pending",
    "object_ceiling",
    "not_ceiling",
}

CEILING_REPORT_EFFORT_VERDICTS = {
    "pending",
    "hard_enough",
    "not_hard_enough",
    "inconclusive",
}

CEILING_REPORT_NEXT_ROUTES = {
    "pending",
    "post_ceiling_pivot",
    "publish_non_flagship",
    "shelve",
}

ESCALATION_BLUEPRINT_HEADINGS = [
    "## Opening Lab",
    "## Object Decision",
    "## Body / Support / Footnote Ledger",
    "## Second-Pass Bet",
]

REVIEW_FRONTMATTER_FIELDS = [
    "kind",
    "package",
    "revision",
    "judgment_policy",
    "live_draft_path",
    "candidate_path",
    "replacement_verdict",
    "north_star_verdict",
]

ESCALATION_REVIEW_FRONTMATTER_FIELDS = [
    "dominant_blocker_slug",
    "continue_iteration",
]

REVIEW_BODY_HEADINGS = [
    "## Findings",
    "## Prioritized Issues",
    "## Scorecard",
    "## Replacement Verdict",
    "## North-Star Verdict",
    "## Main Blockers",
]

ESCALATION_REVIEW_BODY_HEADINGS = [
    "## Dominant Blocker",
    "## North-Star Delta",
    "## Continue Or Stop",
    "## If Continue, What Gets Cut",
]

SCORECARD_FRONTMATTER_FIELDS = [
    "kind",
    "package",
    "revision",
    "judgment_policy",
    "candidate_path",
    "opening_anchor",
    "middle_anchor",
    "ending_anchor",
    "nearby_archive_anchor",
    "stronger_archive_anchor",
    "weaker_archive_anchor",
    "traction",
    "craft",
    "publication_power",
    "next_score_blocker",
]

SCORECARD_BODY_HEADINGS = [
    "## Whole-Draft Rationale",
    "## Opening Anchor",
    "## Middle Anchor",
    "## Ending Anchor",
    "## Archive Anchors",
    "## Direct Dimensions",
    "## Traction",
    "## Craft",
    "## Publication Power",
    "## Next-score Blocker",
]

DECISION_FRONTMATTER_FIELDS = [
    "kind",
    "package",
    "revision",
    "judgment_policy",
    "live_draft_path",
    "candidate_path",
    "recommendation",
    "promotion_allowed",
    "requires_human_approval",
]

ESCALATION_DECISION_FRONTMATTER_FIELDS = [
    "rewrite_mode",
    "stop_gate_status",
]

DECISION_BODY_HEADINGS = [
    "## Recommendation",
    "## Promotion Gate",
    "## Required Follow-Through",
]

ESCALATION_DECISION_BODY_HEADINGS = [
    "## Escalation Decision",
    "## Rewrite Mode",
    "## Stop Gate For Next Pass",
]

ARCHIVE_ANCHOR_FIELDS = [
    "nearby_archive_anchor",
    "stronger_archive_anchor",
    "weaker_archive_anchor",
]

PASSAGE_ANCHOR_FIELDS = [
    "opening_anchor",
    "middle_anchor",
    "ending_anchor",
]

CANDIDATE_LIMITS_HEADINGS = [
    "## Limits",
    "## Borders",
    "## What This Will Not Fix",
    "## What This Essay Will Not Claim",
]

CANDIDATE_REFERENCES_HEADINGS = [
    "## References",
    "## Endmatter",
    "## Sources",
    "## Further Reading",
]

PACKET_TEMPLATE_TARGETS = {
    "hardened_blueprint_template.md": "blueprint",
    "prewrite_gate_template.md": "prewrite_gate",
    "candidate_template.md": "candidate",
    "cold_replacement_review_template.md": "replacement_review",
    "atlas_live_draft_scorecard_template.md": "atlas_scorecard",
    "promotion_decision_template.md": "decision",
    "ceiling_report_template.md": "ceiling_report",
}

ESCALATION_STOP_GATE_STATUSES = {
    "inactive",
    "armed",
    "fired",
}

DOMINANT_BLOCKER_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

CANDIDATE_SCAFFOLD_MARKERS = [
    "# Working Title",
    "Write the candidate here.",
    "## Limits",
    "State the boundaries, counterpressure, or what the essay will not claim.",
    "## References",
    "Include real endmatter or references, not just a companion pointer.",
]

DECISION_REQUIRED_FOLLOW_THROUGH_PLACEHOLDER = (
    "List the next concrete actions required before the stage can be marked done."
)

CANDIDATE_TEMPLATE_TAIL_MARKERS = [
    "State the boundaries, counterpressure, or what the essay will not claim.",
    "Include real endmatter or references, not just a companion pointer.",
    "Use author-year citations in the body where sources carry claims.",
    "For cited papers, prefer h4 headings linked to the arXiv paper or canonical source",
]

AGENT_CONTRACT_RESULT_OUTPUT_KEYS = (
    "cold_replacement_review_agent_result",
    "cold_review_result",
    "cold_replacement_review_result",
    "replacement_review_result",
    "agent_result",
)

AGENT_CONTRACT_INTEGRATION_OUTPUT_KEYS = (
    "cold_replacement_review_integration_decision",
    "integration_decision",
    "replacement_integration_decision",
    "cold_review_integration_decision",
    "agent_integration_decision",
)

ALLOWED_COLD_REVIEW_RESULT_VERDICTS = {
    "pass",
}

ALLOWED_REPLACEMENT_INTEGRATION_DECISIONS = {
    "accept",
    "accept_pass",
    "accepted",
    "accept_result",
    "integrate",
    "approve_replacement_gate",
    "clears_replacement_gate",
}


def repo_relpath(path: Path | None) -> str | None:
    if path is None:
        return None
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def resolve_config_path(status_data: dict, key: str) -> Path | None:
    value = status_data.get("config", {}).get(key)
    if not isinstance(value, str) or not value.strip():
        return None
    candidate = (REPO_ROOT / value).resolve()
    if candidate.exists():
        return candidate
    return None


def packet_schema_version(packet: dict) -> int:
    version = packet.get("packet_schema_version", 1)
    if not isinstance(version, int):
        raise ValueError("Packet manifest field 'packet_schema_version' must be an integer.")
    return version


def escalation_mode_active(
    packet: dict,
    review_frontmatter: dict,
    decision_frontmatter: dict,
) -> bool:
    return (
        packet_schema_version(packet) >= NORTH_STAR_ESCALATION_SCHEMA_VERSION
        and review_frontmatter.get("north_star_verdict") == "below_north_star"
        and decision_frontmatter.get("recommendation") == "revise_candidate"
    )


def valid_dominant_blocker_slug(value: object) -> bool:
    return isinstance(value, str) and bool(DOMINANT_BLOCKER_SLUG_RE.fullmatch(value))


def candidate_text_looks_scaffold(text: str) -> bool:
    return all(marker in text for marker in CANDIDATE_SCAFFOLD_MARKERS)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _markdown_h2_sections(text: str) -> list[tuple[str, str, int]]:
    matches = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", text))
    sections: list[tuple[str, str, int]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        line_number = text.count("\n", 0, match.start()) + 1
        sections.append((f"## {match.group(1).strip()}", text[start:end].strip(), line_number))
    return sections


def _candidate_endmatter_group(heading: str) -> str | None:
    if heading in CANDIDATE_LIMITS_HEADINGS:
        return "limits"
    if heading in CANDIDATE_REFERENCES_HEADINGS:
        return "references"
    return None


def candidate_scaffold_residue_findings(text: str) -> list[str]:
    findings: list[str] = []
    sections = _markdown_h2_sections(text)
    grouped: dict[str, list[tuple[str, str, int]]] = {"limits": [], "references": []}
    for heading, body, line_number in sections:
        group = _candidate_endmatter_group(heading)
        if group is not None:
            grouped[group].append((heading, body, line_number))

    for group, matches in grouped.items():
        if len(matches) > 1:
            line_numbers = ", ".join(str(line_number) for _, _, line_number in matches)
            findings.append(f"Candidate draft repeats {group} endmatter sections at lines {line_numbers}.")

    first_references = grouped["references"][0][2] if grouped["references"] else None
    if first_references is not None:
        for heading, body, line_number in grouped["limits"] + grouped["references"]:
            if line_number <= first_references:
                continue
            if any(marker in body for marker in CANDIDATE_TEMPLATE_TAIL_MARKERS):
                findings.append(
                    f"Candidate draft has template-tail scaffold residue after completed references at line {line_number} ({heading})."
                )

    return findings


def candidate_text_has_scaffold_residue(text: str) -> bool:
    return bool(candidate_scaffold_residue_findings(text))


def _extract_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    lines = text.splitlines()
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return "\n".join(lines[1:idx]), "\n".join(lines[idx + 1 :])
    return "", text


def load_agent_contract_metadata(path: Path) -> dict:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text())
    else:
        text = path.read_text()
        frontmatter_text, body = _extract_frontmatter(text)
        if frontmatter_text:
            data = yaml.safe_load(frontmatter_text) or {}
        elif path.suffix.lower() in {".yaml", ".yml"}:
            data = yaml.safe_load(text) or {}
        else:
            data = {}
        if isinstance(data, dict) and "body" not in data:
            data = {**data, "body": body}
    if not isinstance(data, dict):
        raise ValueError(f"Agent contract artifact must be a mapping: {path}")
    return data


def _first_string(*values: object) -> str | None:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _normalize_hash(value: object) -> str | None:
    if isinstance(value, dict):
        return _normalize_hash(value.get("sha256"))
    if not isinstance(value, str) or not value.strip():
        return None
    normalized = value.strip()
    if normalized.startswith("sha256:"):
        normalized = normalized.split(":", 1)[1]
    if re.fullmatch(r"[0-9a-fA-F]{64}", normalized):
        return normalized.lower()
    return None


def _metadata_source_hash(metadata: dict, logical_name: str, relpath: str | None) -> str | None:
    direct_keys = [
        f"{logical_name}_hash",
        f"{logical_name}_sha256",
        f"{logical_name}_path_hash",
    ]
    for key in direct_keys:
        found = _normalize_hash(metadata.get(key))
        if found:
            return found

    source_hashes = metadata.get("source_hashes")
    if isinstance(source_hashes, dict):
        keys = [
            logical_name,
            f"{logical_name}_path",
            f"{logical_name}_draft",
            f"{logical_name}_manifest",
        ]
        if relpath:
            keys.append(relpath)
        for key in keys:
            found = _normalize_hash(source_hashes.get(key))
            if found:
                return found

    sources = metadata.get("sources")
    if isinstance(sources, list):
        for item in sources:
            if not isinstance(item, dict):
                continue
            item_name = item.get("id") or item.get("name") or item.get("logical_name")
            item_path = item.get("path")
            if item_name != logical_name and (not relpath or item_path != relpath):
                continue
            found = _normalize_hash(item.get("hash") or item.get("sha256"))
            if found:
                return found
    return None


def _metadata_path(metadata: dict, logical_name: str) -> str | None:
    aliases = {
        "packet": ("packet_manifest_path", "packet_path", "manifest_path"),
        "live_draft": ("live_draft_path",),
        "candidate": ("candidate_path", "candidate_draft_path"),
    }
    return _first_string(*(metadata.get(key) for key in aliases[logical_name]))


def _metadata_package_matches(metadata: dict, packet: dict) -> bool:
    package = packet.get("package")
    value = metadata.get("package")
    if value == package:
        return True
    if isinstance(value, dict):
        return value.get("path") == f"publications/{package}" or value.get("package") == package
    return False


def _metadata_workflow_id(metadata: dict) -> str | None:
    workflow = metadata.get("workflow")
    if isinstance(workflow, dict):
        return _first_string(workflow.get("workflow_id"))
    return _first_string(metadata.get("workflow_id"))


def _metadata_declares_path(metadata: dict, logical_name: str, expected: object) -> tuple[bool, str | None]:
    if not isinstance(expected, str):
        return False, None
    actual = _metadata_path(metadata, logical_name)
    if actual is not None:
        return actual == expected, actual

    source_hashes = metadata.get("source_hashes")
    if isinstance(source_hashes, dict) and expected in source_hashes:
        return True, expected

    sources = metadata.get("sources")
    if isinstance(sources, list):
        for item in sources:
            if not isinstance(item, dict):
                continue
            item_path = item.get("path")
            item_id = item.get("id") or item.get("name") or item.get("logical_name")
            if item_path == expected and (item_id in {None, logical_name} or _metadata_source_hash(metadata, logical_name, expected)):
                return True, expected
    return False, None


def _request_matches_replacement_packet(data: dict, packet: dict) -> bool:
    if data.get("kind") != "subagent_request":
        return False
    workflow = data.get("workflow")
    if not isinstance(workflow, dict):
        return False
    if workflow.get("workflow_id") != "essay_iteration" or workflow.get("step_id") != "run_cold_replacement_review":
        return False
    if not _metadata_package_matches(data, packet):
        return False

    expected_manifest = packet.get("packet_manifest_path") or packet.get("output_paths", {}).get("manifest")
    if not isinstance(expected_manifest, str):
        return False

    source_hashes = data.get("source_hashes")
    if isinstance(source_hashes, dict) and expected_manifest in source_hashes:
        return True

    allowed_inputs = data.get("allowed_input_paths")
    if isinstance(allowed_inputs, list):
        for item in allowed_inputs:
            if not isinstance(item, dict):
                continue
            paths = item.get("paths")
            if isinstance(paths, list) and expected_manifest in paths:
                return True
            if item.get("expected_path") == expected_manifest:
                return True
    return False


def _latest_replacement_agent_request(packet: dict) -> tuple[Path, dict] | None:
    requests_dir = REPO_ROOT / "reviewable-runs" / "subagent-requests"
    if not requests_dir.exists():
        return None

    matches: list[tuple[float, str, Path, dict]] = []
    for path in sorted([*requests_dir.glob("*.yaml"), *requests_dir.glob("*.yml")]):
        try:
            data = yaml.safe_load(path.read_text()) or {}
        except Exception:
            continue
        if not isinstance(data, dict) or not _request_matches_replacement_packet(data, packet):
            continue
        matches.append((path.stat().st_mtime, path.name, path, data))
    if not matches:
        return None
    _, _, path, data = max(matches)
    return path, data


def _contract_paths_from_latest_request(packet: dict) -> dict[str, Path]:
    found = _latest_replacement_agent_request(packet)
    if found is None:
        return {}
    request_path, request_data = found
    expected = request_data.get("expected_artifacts")
    if not isinstance(expected, dict):
        return {"request": request_path}

    paths: dict[str, Path] = {"request": request_path}
    result_path = expected.get("result_path")
    if isinstance(result_path, str) and result_path.strip():
        paths["cold_review_result"] = (REPO_ROOT / result_path).resolve()
    integration_path = expected.get("integration_decision_path")
    if isinstance(integration_path, str) and integration_path.strip():
        paths["integration_decision"] = (REPO_ROOT / integration_path).resolve()
    return paths


def _contract_path_from_output_keys(packet: dict, output_keys: tuple[str, ...]) -> Path | None:
    output_paths = packet.get("output_paths", {})
    if not isinstance(output_paths, dict):
        return None
    for key in output_keys:
        relpath = output_paths.get(key)
        if isinstance(relpath, str) and relpath.strip():
            return (REPO_ROOT / relpath).resolve()
    return None


def _contract_path_from_nested_contract(packet: dict, path_keys: tuple[str, ...]) -> Path | None:
    candidates = [
        packet.get("agent_contract"),
        packet.get("agent_contracts", {}).get("run_cold_replacement_review")
        if isinstance(packet.get("agent_contracts"), dict)
        else None,
    ]
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        for key in path_keys:
            relpath = candidate.get(key)
            if isinstance(relpath, str) and relpath.strip():
                return (REPO_ROOT / relpath).resolve()
        result = candidate.get("result")
        if isinstance(result, dict):
            for key in path_keys:
                relpath = result.get(key)
                if isinstance(relpath, str) and relpath.strip():
                    return (REPO_ROOT / relpath).resolve()
        integration = candidate.get("integration_decision")
        if isinstance(integration, dict):
            for key in path_keys:
                relpath = integration.get(key)
                if isinstance(relpath, str) and relpath.strip():
                    return (REPO_ROOT / relpath).resolve()
    return None


def resolve_replacement_agent_contract_paths(packet: dict) -> dict[str, Path]:
    result_path = _contract_path_from_output_keys(packet, AGENT_CONTRACT_RESULT_OUTPUT_KEYS)
    if result_path is None:
        result_path = _contract_path_from_nested_contract(
            packet,
            ("result_path", "cold_review_result_path", "cold_replacement_review_result_path"),
        )

    integration_path = _contract_path_from_output_keys(packet, AGENT_CONTRACT_INTEGRATION_OUTPUT_KEYS)
    if integration_path is None:
        integration_path = _contract_path_from_nested_contract(
            packet,
            ("integration_decision_path", "decision_path"),
        )

    request_paths = _contract_paths_from_latest_request(packet)
    if result_path is None:
        result_path = request_paths.get("cold_review_result")
    if integration_path is None:
        integration_path = request_paths.get("integration_decision")

    if result_path is None or integration_path is None:
        candidate_relpath = packet.get("candidate_path")
        revision = packet.get("revision")
        if isinstance(candidate_relpath, str) and isinstance(revision, int):
            candidate_path = (REPO_ROOT / candidate_relpath).resolve()
            stem = re.sub(r"-candidate-r\d+$", "", candidate_path.stem)
            if result_path is None:
                result_path = candidate_path.with_name(f"{stem}-cold-replacement-review-result-r{revision}.md")
            if integration_path is None:
                integration_path = candidate_path.with_name(f"{stem}-replacement-integration-decision-r{revision}.md")

    return {
        "request": request_paths.get("request", REPO_ROOT / "__missing_agent_request__"),
        "cold_review_result": result_path if result_path is not None else REPO_ROOT / "__missing_cold_review_result__",
        "integration_decision": integration_path
        if integration_path is not None
        else REPO_ROOT / "__missing_integration_decision__",
    }


def _validate_contract_identity(
    metadata: dict,
    label: str,
    packet: dict,
    artifact_path: Path,
    errors: list[str],
) -> None:
    package = packet.get("package")
    revision = packet.get("revision")
    if not _metadata_package_matches(metadata, packet):
        errors.append(f"{label} package must match packet package '{package}': {repo_relpath(artifact_path)}")
    if "revision" in metadata and metadata.get("revision") != revision:
        errors.append(f"{label} revision must match packet revision '{revision}': {repo_relpath(artifact_path)}")

    workflow_id = _metadata_workflow_id(metadata)
    if workflow_id not in (None, "", "essay_iteration"):
        errors.append(f"{label} workflow_id must be essay_iteration: {repo_relpath(artifact_path)}")

    expected_paths = {
        "packet": packet.get("packet_manifest_path") or packet.get("output_paths", {}).get("manifest"),
        "live_draft": packet.get("live_draft_path"),
        "candidate": packet.get("candidate_path"),
    }
    for logical_name, expected in expected_paths.items():
        declared, actual = _metadata_declares_path(metadata, logical_name, expected)
        if actual is None:
            errors.append(f"{label} must declare {logical_name} path: {repo_relpath(artifact_path)}")
        elif not declared:
            errors.append(
                f"{label} {logical_name} path is stale or mismatched: expected {expected}, got {actual}."
            )


def _validate_contract_hashes(
    metadata: dict,
    label: str,
    packet: dict,
    artifact_path: Path,
    current_hashes: dict[str, str],
    errors: list[str],
) -> None:
    expected_paths = {
        "packet": packet.get("packet_manifest_path") or packet.get("output_paths", {}).get("manifest"),
        "live_draft": packet.get("live_draft_path"),
        "candidate": packet.get("candidate_path"),
    }
    for logical_name, expected_hash in current_hashes.items():
        declared_hash = _metadata_source_hash(metadata, logical_name, expected_paths.get(logical_name))
        if declared_hash is None:
            errors.append(f"{label} must declare current {logical_name} sha256: {repo_relpath(artifact_path)}")
        elif declared_hash != expected_hash:
            errors.append(
                f"{label} {logical_name} sha256 is stale: expected sha256:{expected_hash}, got sha256:{declared_hash}."
            )


def _result_identifier(metadata: dict, path: Path) -> str | None:
    return _first_string(
        metadata.get("result_id"),
        metadata.get("request_id"),
        metadata.get("agent_result_id"),
        repo_relpath(path),
    )


def _integration_references_result(integration_metadata: dict, result_metadata: dict, result_path: Path) -> bool:
    result_relpath = repo_relpath(result_path)
    path_references = [
        integration_metadata.get("result_path"),
        integration_metadata.get("cold_review_result_path"),
        integration_metadata.get("cold_replacement_review_result_path"),
        integration_metadata.get("accepted_result_path"),
    ]
    if any(path == result_relpath for path in path_references):
        return True

    result_id = _result_identifier(result_metadata, result_path)
    id_references = [
        integration_metadata.get("result_id"),
        integration_metadata.get("accepted_result_id"),
        integration_metadata.get("agent_result_id"),
    ]
    if result_id is not None and any(value == result_id for value in id_references):
        return True

    accepted_result_ids = integration_metadata.get("accepted_result_ids")
    return isinstance(accepted_result_ids, list) and result_id in accepted_result_ids


def validate_replacement_agent_contract(
    packet: dict,
    *,
    require_present: bool,
    require_allowed: bool,
) -> tuple[list[str], dict]:
    errors: list[str] = []
    contract_paths = resolve_replacement_agent_contract_paths(packet)
    request_path = contract_paths["request"]
    result_path = contract_paths["cold_review_result"]
    integration_path = contract_paths["integration_decision"]
    details: dict = {
        "agent_request_path": repo_relpath(request_path),
        "cold_review_result_path": repo_relpath(result_path),
        "integration_decision_path": repo_relpath(integration_path),
    }

    result_exists = result_path.exists()
    integration_exists = integration_path.exists()
    if not result_exists or not integration_exists:
        if require_present or result_exists or integration_exists:
            if not result_exists:
                errors.append(f"Missing independent cold-review result artifact: {repo_relpath(result_path)}")
            if not integration_exists:
                errors.append(f"Missing integration decision artifact: {repo_relpath(integration_path)}")
        return errors, details

    try:
        result_metadata = load_agent_contract_metadata(result_path)
        integration_metadata = load_agent_contract_metadata(integration_path)
    except Exception as exc:
        errors.append(f"Invalid replacement agent contract artifact: {exc}")
        return errors, details

    details["cold_review_verdict"] = result_metadata.get("verdict")
    details["integration_decision"] = integration_metadata.get("decision")

    current_paths = {
        "packet": packet.get("packet_manifest_path") or packet.get("output_paths", {}).get("manifest"),
        "live_draft": packet.get("live_draft_path"),
        "candidate": packet.get("candidate_path"),
    }
    current_hashes: dict[str, str] = {}
    for logical_name, relpath in current_paths.items():
        if not isinstance(relpath, str):
            errors.append(f"Packet is missing {logical_name} path for replacement agent contract validation.")
            continue
        path = (REPO_ROOT / relpath).resolve()
        if not path.exists():
            errors.append(f"Packet {logical_name} path does not exist for replacement agent contract validation: {path}")
            continue
        current_hashes[logical_name] = file_sha256(path)
    details["current_hashes"] = {key: f"sha256:{value}" for key, value in current_hashes.items()}

    _validate_contract_identity(result_metadata, "Cold-review result", packet, result_path, errors)
    _validate_contract_identity(integration_metadata, "Integration decision", packet, integration_path, errors)
    _validate_contract_hashes(result_metadata, "Cold-review result", packet, result_path, current_hashes, errors)
    _validate_contract_hashes(
        integration_metadata,
        "Integration decision",
        packet,
        integration_path,
        current_hashes,
        errors,
    )

    if not _integration_references_result(integration_metadata, result_metadata, result_path):
        errors.append("Integration decision must identify the accepted cold-review result by path or result_id.")

    if require_allowed:
        verdict = result_metadata.get("verdict")
        if verdict not in ALLOWED_COLD_REVIEW_RESULT_VERDICTS:
            errors.append(
                "Cold-review result verdict must be one of: "
                + ", ".join(sorted(ALLOWED_COLD_REVIEW_RESULT_VERDICTS))
                + "."
            )
        decision = integration_metadata.get("decision")
        if decision not in ALLOWED_REPLACEMENT_INTEGRATION_DECISIONS:
            errors.append(
                "Integration decision must be one of: "
                + ", ".join(sorted(ALLOWED_REPLACEMENT_INTEGRATION_DECISIONS))
                + "."
            )

    return errors, details


def resolve_live_draft(package_path: Path, status_data: dict) -> Path | None:
    markdown_path = resolve_config_path(status_data, "markdown_path")
    if markdown_path and markdown_path.exists():
        return markdown_path
    return None


def resolve_leaf_readme(package_path: Path) -> Path | None:
    candidate = package_path / "README.md"
    if candidate.exists():
        return candidate
    return None


def resolve_parent_package_path(package_path: Path, status_data: dict) -> Path | None:
    candidates: list[Path] = []
    parent_package = status_data.get("parent_package")
    if isinstance(parent_package, str) and parent_package.strip():
        candidates.append((PUBLICATIONS_DIR / parent_package.strip()).resolve())

    parent_dir = package_path.resolve().parent
    if parent_dir != PUBLICATIONS_DIR:
        candidates.append(parent_dir)

    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.exists() and candidate != package_path.resolve():
            return candidate
    return None


def resolve_parent_package_readme(package_path: Path, status_data: dict) -> Path | None:
    parent_path = resolve_parent_package_path(package_path, status_data)
    if not parent_path:
        return None
    candidate = parent_path / "README.md"
    if candidate.exists():
        return candidate
    return None


def resolve_review_context_roots(package_path: Path, status_data: dict) -> list[Path]:
    roots: list[Path] = [package_path]
    parent_path = resolve_parent_package_path(package_path, status_data)
    if parent_path:
        roots.extend([parent_path, parent_path / "claims"])
        parent_status = load_status(parent_path) or {}
        leaf_packages = parent_status.get("config", {}).get("leaf_packages", [])
        if isinstance(leaf_packages, list):
            for leaf in leaf_packages:
                if isinstance(leaf, str) and leaf.strip():
                    roots.append((PUBLICATIONS_DIR / leaf.strip()).resolve())

    deduped: list[Path] = []
    seen: set[Path] = set()
    for root in roots:
        resolved = root.resolve()
        if resolved in seen or not resolved.exists():
            continue
        seen.add(resolved)
        deduped.append(root)
    return deduped


def resolve_companion_path(package_path: Path) -> Path | None:
    candidate = package_path / "companion.md"
    if candidate.exists():
        return candidate
    return None


def resolve_evidence_surface(package_path: Path, status_data: dict) -> Path | None:
    configured = resolve_config_path(status_data, "evidence_path")
    if configured:
        return configured

    candidates = [
        package_path / "papers" / "index.md",
        package_path / "papers",
    ]

    parent_path = resolve_parent_package_path(package_path, status_data)
    if parent_path:
        candidates.extend(
            [
                parent_path / "papers" / "index.md",
                parent_path / "papers",
            ]
        )

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _glob_direct_files(root: Path, patterns: tuple[str, ...]) -> list[Path]:
    if not root.exists():
        return []
    matches: list[Path] = []
    seen: set[Path] = set()
    for pattern in patterns:
        for candidate in sorted(root.glob(pattern)):
            if not candidate.is_file() or candidate in seen:
                continue
            seen.add(candidate)
            matches.append(candidate)
    return matches


def _glob_packet_surface_files(root: Path, patterns: tuple[str, ...]) -> list[Path]:
    matches = _glob_direct_files(root, patterns)
    iterations_root = root / "iterations"
    if iterations_root.exists():
        for revision_dir in sorted(iterations_root.glob("r*")):
            if revision_dir.is_dir():
                matches.extend(_glob_direct_files(revision_dir, patterns))

    deduped: list[Path] = []
    seen: set[Path] = set()
    for match in matches:
        if match in seen:
            continue
        seen.add(match)
        deduped.append(match)
    return deduped


def _revision_sort_key(path: Path) -> tuple[int, str]:
    match = re.search(r"-r(\d+)\.md$", path.name)
    if match:
        return (int(match.group(1)), path.name)
    return (0, path.name)


def resolve_nearest_blueprint_path(package_path: Path, status_data: dict) -> Path | None:
    for root in filter(None, [package_path, resolve_parent_package_path(package_path, status_data)]):
        matches = _glob_packet_surface_files(root, BLUEPRINT_PATTERNS)
        if matches:
            return max(matches, key=_revision_sort_key)
    return None


def resolve_governing_brief_path(package_path: Path, status_data: dict) -> Path | None:
    config = status_data.get("config", {})
    configured = config.get("blueprint_path")
    if isinstance(configured, str) and configured.strip():
        candidate = (package_path / configured.strip()).resolve()
        try:
            candidate.relative_to(package_path.resolve())
        except ValueError:
            candidate = None
        if candidate is not None and candidate.exists():
            return candidate
    return resolve_nearest_blueprint_path(package_path, status_data)


def resolve_review_artifact_paths(package_path: Path, status_data: dict) -> list[Path]:
    matches: list[Path] = []
    seen: set[Path] = set()
    for root in resolve_review_context_roots(package_path, status_data):
        for candidate in _glob_packet_surface_files(root, REVIEW_PATTERNS):
            if candidate in seen:
                continue
            seen.add(candidate)
            matches.append(candidate)
    return sorted(matches, key=_revision_sort_key, reverse=True)


def build_packet_paths(live_draft_path: Path, revision: int) -> dict[str, Path]:
    draft_stem = live_draft_path.stem
    root = live_draft_path.parent
    legacy_paths = {
        "manifest": root / f"{draft_stem}-essay-iteration-packet-r{revision}.json",
        "blueprint": root / f"{draft_stem}-blueprint-r{revision}.md",
        "prewrite_gate": root / f"{draft_stem}-prewrite-gate-r{revision}.md",
        "candidate": root / f"{draft_stem}-candidate-r{revision}.md",
        "replacement_review": root / f"{draft_stem}-replacement-review-r{revision}.md",
        "atlas_scorecard": root / f"{draft_stem}-atlas-scorecard-r{revision}.md",
        "decision": root / f"{draft_stem}-decision-r{revision}.md",
        "ceiling_report": root / f"{draft_stem}-ceiling-report-r{revision}.md",
    }
    packet_root = root / "iterations" / f"r{revision}"
    iteration_paths = {
        name: packet_root / path.name
        for name, path in legacy_paths.items()
    }
    if any(path.exists() for path in iteration_paths.values()):
        return iteration_paths
    if any(path.exists() for path in legacy_paths.values()):
        return legacy_paths
    return iteration_paths


def describe_packet_paths(live_draft_path: Path | None, revision: int | None) -> dict[str, str]:
    if live_draft_path is None or revision is None:
        return {}
    return {
        name: repo_relpath(path)
        for name, path in build_packet_paths(live_draft_path, revision).items()
    }
