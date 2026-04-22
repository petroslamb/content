#!/usr/bin/env python3
"""Validate the modular workflow model contracts and lightweight evaluation fixtures."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

from harness import build_stage_resolution, build_workflow_resolution, evaluate_gate
from lifecycle import (
    REPO_ROOT,
    STAGES,
    load_all_workflow_contracts,
    load_gate_contracts,
    load_pipeline_profiles,
    load_workflow_contract,
)


FIXTURES_PATH = REPO_ROOT / "scripts" / "workflow_model_fixtures.yaml"
LOGS_DIR = REPO_ROOT / "reviewable-runs" / "logs"


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text()) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path.relative_to(REPO_ROOT)}")
    return data


def check_contracts(errors: list[str]) -> None:
    workflows = load_all_workflow_contracts()
    load_gate_contracts()
    load_pipeline_profiles()
    for stage in STAGES:
        contract = load_workflow_contract(stage)
        metadata = contract["metadata"]
        if metadata["workflow_kind"] != "stage":
            errors.append(f"Stage workflow '{stage}' is not marked workflow_kind: stage.")
        if metadata.get("stage_binding") != stage:
            errors.append(f"Stage workflow '{stage}' does not bind stage_binding: {stage}.")
    if "topic_discovery" not in workflows:
        errors.append("Workflow registry is missing topic_discovery.")
    if "post_ceiling_pivot" not in workflows:
        errors.append("Workflow registry is missing post_ceiling_pivot.")


def check_topic_packets(fixtures: dict, errors: list[str]) -> None:
    for fixture in fixtures.get("topic_packets", []):
        packet_path = (REPO_ROOT / fixture["packet"]).resolve()
        result = evaluate_gate(fixture["gate"], packet_path=packet_path)
        if result["status"] != fixture["expected_status"]:
            errors.append(
                f"Topic packet fixture {fixture['packet']} expected status {fixture['expected_status']}, got {result['status']}."
            )
        if result["decision"] != fixture["expected_decision"]:
            errors.append(
                f"Topic packet fixture {fixture['packet']} expected decision {fixture['expected_decision']}, got {result['decision']}."
            )


def check_route_fixtures(fixtures: dict, errors: list[str]) -> None:
    for fixture in fixtures.get("route_checks", []):
        resolution = build_stage_resolution(fixture["package"], fixture["stage"])
        if resolution.get("pipeline_profile") != fixture["expected_pipeline_profile"]:
            errors.append(
                f"{fixture['package']} stage {fixture['stage']} expected pipeline_profile {fixture['expected_pipeline_profile']}, got {resolution.get('pipeline_profile')}."
            )
        if fixture.get("expected_packet_phase") and resolution.get("packet_phase") != fixture["expected_packet_phase"]:
            errors.append(
                f"{fixture['package']} stage {fixture['stage']} expected packet_phase {fixture['expected_packet_phase']}, got {resolution.get('packet_phase')}."
            )
        if fixture.get("expected_recommended_workflow") and fixture["expected_recommended_workflow"] not in resolution.get("recommended_workflows", []):
            errors.append(
                f"{fixture['package']} stage {fixture['stage']} is missing recommended workflow {fixture['expected_recommended_workflow']}."
            )
        if fixture.get("expected_overlay_candidate") and fixture["expected_overlay_candidate"] not in resolution.get("overlay_candidates", []):
            errors.append(
                f"{fixture['package']} stage {fixture['stage']} is missing overlay candidate {fixture['expected_overlay_candidate']}."
            )
        if fixture.get("expected_active_overlay") and resolution.get("active_overlay") != fixture["expected_active_overlay"]:
            errors.append(
                f"{fixture['package']} stage {fixture['stage']} expected active_overlay {fixture['expected_active_overlay']}, got {resolution.get('active_overlay')}."
            )
        if fixture.get("expected_overlay_phase") and resolution.get("overlay_phase") != fixture["expected_overlay_phase"]:
            errors.append(
                f"{fixture['package']} stage {fixture['stage']} expected overlay_phase {fixture['expected_overlay_phase']}, got {resolution.get('overlay_phase')}."
            )
        if fixture.get("expected_next_overlay_action") and resolution.get("next_overlay_action") != fixture["expected_next_overlay_action"]:
            errors.append(
                f"{fixture['package']} stage {fixture['stage']} expected next_overlay_action {fixture['expected_next_overlay_action']}, got {resolution.get('next_overlay_action')}."
            )
        if fixture.get("expected_overlay_route") and resolution.get("overlay_route") != fixture["expected_overlay_route"]:
            errors.append(
                f"{fixture['package']} stage {fixture['stage']} expected overlay_route {fixture['expected_overlay_route']}, got {resolution.get('overlay_route')}."
            )
        expected_overlay_validator = fixture.get("expected_overlay_validator_substring")
        if expected_overlay_validator and expected_overlay_validator not in (resolution.get("overlay_recommended_validator") or ""):
            errors.append(
                f"{fixture['package']} stage {fixture['stage']} expected overlay validator containing {expected_overlay_validator}, got {resolution.get('overlay_recommended_validator')}."
            )
        expected_gate = fixture.get("expected_gate")
        if expected_gate:
            gate_status = resolution.get("gate_statuses", {}).get(expected_gate["gate_id"])
            if gate_status is None:
                errors.append(
                    f"{fixture['package']} stage {fixture['stage']} is missing gate status {expected_gate['gate_id']}."
                )
                continue
            if gate_status["status"] != expected_gate["status"] or gate_status["decision"] != expected_gate["decision"]:
                errors.append(
                    f"{fixture['package']} stage {fixture['stage']} gate {expected_gate['gate_id']} expected {expected_gate['status']}/{expected_gate['decision']}, got {gate_status['status']}/{gate_status['decision']}."
                )


def check_workflow_resolution_fixtures(fixtures: dict, errors: list[str]) -> None:
    for fixture in fixtures.get("workflow_resolution_checks", []):
        packet_path = None
        if fixture.get("packet"):
            packet_path = (REPO_ROOT / fixture["packet"]).resolve()
        resolution = build_workflow_resolution(
            fixture["workflow"],
            package_arg=fixture.get("package"),
            packet_path=packet_path,
        )
        if fixture.get("expected_can_execute") is not None and resolution.get("can_execute") != fixture["expected_can_execute"]:
            errors.append(
                f"Workflow {fixture['workflow']} expected can_execute {fixture['expected_can_execute']}, got {resolution.get('can_execute')}."
            )
        if fixture.get("expected_overlay_phase") and resolution.get("overlay_phase") != fixture["expected_overlay_phase"]:
            errors.append(
                f"Workflow {fixture['workflow']} expected overlay_phase {fixture['expected_overlay_phase']}, got {resolution.get('overlay_phase')}."
            )
        if fixture.get("expected_next_overlay_action") and resolution.get("next_overlay_action") != fixture["expected_next_overlay_action"]:
            errors.append(
                f"Workflow {fixture['workflow']} expected next_overlay_action {fixture['expected_next_overlay_action']}, got {resolution.get('next_overlay_action')}."
            )
        if fixture.get("expected_overlay_route") and resolution.get("overlay_route") != fixture["expected_overlay_route"]:
            errors.append(
                f"Workflow {fixture['workflow']} expected overlay_route {fixture['expected_overlay_route']}, got {resolution.get('overlay_route')}."
            )
        if fixture.get("expected_active_overlay_root") and resolution.get("active_overlay_root") != fixture["expected_active_overlay_root"]:
            errors.append(
                f"Workflow {fixture['workflow']} expected active_overlay_root {fixture['expected_active_overlay_root']}, got {resolution.get('active_overlay_root')}."
            )
        expected_validator = fixture.get("expected_validator_substring")
        if expected_validator and expected_validator not in (resolution.get("recommended_validator") or ""):
            errors.append(
                f"Workflow {fixture['workflow']} expected validator containing {expected_validator}, got {resolution.get('recommended_validator')}."
            )
        expected_gates = fixture.get("expected_recommended_gates", [])
        missing_gates = [gate_id for gate_id in expected_gates if gate_id not in resolution.get("recommended_gates", [])]
        if missing_gates:
            errors.append(
                f"Workflow {fixture['workflow']} is missing recommended gates: {', '.join(missing_gates)}."
            )


def check_gate_fixtures(fixtures: dict, errors: list[str]) -> None:
    for fixture in fixtures.get("gate_checks", []):
        result = evaluate_gate(fixture["gate"], package_arg=fixture["package"])
        if result["status"] != fixture["expected_status"]:
            errors.append(
                f"Gate {fixture['gate']} for {fixture['package']} expected status {fixture['expected_status']}, got {result['status']}."
            )
        if fixture.get("expected_decision") and result["decision"] != fixture["expected_decision"]:
            errors.append(
                f"Gate {fixture['gate']} for {fixture['package']} expected decision {fixture['expected_decision']}, got {result['decision']}."
            )


def check_validator_coverage(fixtures: dict, errors: list[str]) -> None:
    for fixture in fixtures.get("validator_coverage", []):
        contract = load_workflow_contract(fixture["workflow"])
        validators = contract["metadata"].get("validator_commands", [])
        if not any(fixture["validator_substring"] in command for command in validators):
            errors.append(
                f"Workflow {fixture['workflow']} is missing validator coverage for {fixture['validator_substring']}."
            )


def check_run_record_completeness(fixtures: dict, errors: list[str]) -> None:
    retained = fixtures.get("retained_examples", {})
    log_fixtures = retained.get("logs", [])
    artifact_fixtures = retained.get("artifacts", [])

    kinds = set()
    for fixture in log_fixtures:
        path = (REPO_ROOT / fixture["path"]).resolve()
        if not path.exists():
            errors.append(f"Retained workflow-model log is missing: {fixture['path']}")
            continue
        data = json.loads(path.read_text())
        kind = data.get("kind")
        expected_kind = fixture.get("kind")
        if expected_kind and kind != expected_kind:
            errors.append(
                f"Retained workflow-model log {fixture['path']} expected kind {expected_kind}, got {kind}."
            )
        if data.get("schema_version") != 2:
            errors.append(
                f"Retained workflow-model log {fixture['path']} must use schema_version 2."
            )
        if isinstance(kind, str):
            kinds.add(kind)

    required_kinds = {"workflow_launch_pack", "workflow_run", "gate_check", "harness_launch_pack"}
    missing = sorted(required_kinds - kinds)
    if missing:
        errors.append(
            "Retained workflow-model examples are missing required log kinds: " + ", ".join(missing)
        )

    for fixture in artifact_fixtures:
        path = (REPO_ROOT / fixture["path"]).resolve()
        if not path.exists():
            label = fixture.get("label") or fixture["path"]
            errors.append(f"Retained workflow-model artifact is missing: {label}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the modular workflow model and evaluation fixtures.")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    errors: list[str] = []
    try:
        fixtures = load_yaml(FIXTURES_PATH)
        check_contracts(errors)
        check_topic_packets(fixtures, errors)
        check_route_fixtures(fixtures, errors)
        check_workflow_resolution_fixtures(fixtures, errors)
        check_gate_fixtures(fixtures, errors)
        check_validator_coverage(fixtures, errors)
        check_run_record_completeness(fixtures, errors)
    except Exception as exc:
        errors.append(str(exc))

    payload = {
        "success": not errors,
        "errors": errors,
        "validated_files": [
            "harness_contract.yaml",
            "gate_contracts.yaml",
            "pipeline_profiles.yaml",
            "scripts/workflow_model_fixtures.yaml",
        ],
    }

    if args.format == "json":
        print(json.dumps(payload, indent=2))
        if errors:
            sys.exit(1)
        return

    if errors:
        print("Workflow model validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    print("Workflow model validation passed.")


if __name__ == "__main__":
    main()
