#!/usr/bin/env python3
"""
Validate the tracked harness contract and policy surfaces.
"""

from __future__ import annotations

import argparse
import json
import sys

import yaml

from harness import (
    HARNESS_CONTRACT_PATH,
    REQUIRED_NPM_SCRIPTS,
    build_harness_contract,
    load_harness_policy,
    load_package_scripts,
    load_yaml_file,
    validate_harness_policy,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the tracked harness contract and policy surfaces.")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--print-expected", action="store_true", help="Print the generated harness_contract.yaml payload and exit.")
    args = parser.parse_args()

    expected_contract = build_harness_contract()
    if args.print_expected:
        print(yaml.safe_dump(expected_contract, default_flow_style=False, sort_keys=False))
        return

    errors: list[str] = []
    if not HARNESS_CONTRACT_PATH.exists():
        errors.append("harness_contract.yaml is missing.")
        tracked_contract = None
    else:
        tracked_contract = load_yaml_file(HARNESS_CONTRACT_PATH)
        if tracked_contract != expected_contract:
            errors.append("harness_contract.yaml is out of date with the generated contract.")

    try:
        policy = load_harness_policy()
        errors.extend(validate_harness_policy(policy))
    except Exception as exc:  # pragma: no cover - surfaced in CLI response
        errors.append(f"Failed to load harness_policy.yaml: {exc}")

    try:
        package_scripts = load_package_scripts()
        missing_scripts = sorted(REQUIRED_NPM_SCRIPTS - set(package_scripts.keys()))
        if missing_scripts:
            errors.append(f"package.json is missing required harness scripts: {', '.join(missing_scripts)}")
    except Exception as exc:  # pragma: no cover - surfaced in CLI response
        errors.append(f"Failed to load package.json scripts: {exc}")

    payload = {
        "success": not errors,
        "errors": errors,
        "validated_files": [
            "harness_contract.yaml",
            "harness_policy.yaml",
            "gate_contracts.yaml",
            "pipeline_profiles.yaml",
            "package.json",
        ],
    }

    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        if errors:
            print("Harness validation failed:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
        print("Harness validation passed.")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
