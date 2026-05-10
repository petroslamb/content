#!/usr/bin/env python3
"""Validate that root docs match the package.json pre-review check bundle."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_JSON = REPO_ROOT / "package.json"
ROOT_README = REPO_ROOT / "README.md"
ACTIVE_VALIDATION_HEADING = "Active validation entrypoints:"
COMMAND_RE = re.compile(r"`([^`]+)`")


def load_check_chain() -> list[str]:
    data = json.loads(PACKAGE_JSON.read_text())
    scripts = data.get("scripts", {})
    check_script = scripts.get("check")
    if not isinstance(check_script, str) or not check_script.strip():
        raise ValueError("package.json is missing scripts.check.")

    commands = [part.strip() for part in check_script.split("&&")]
    invalid = [command for command in commands if not command.startswith("npm run ")]
    if invalid:
        raise ValueError(
            "scripts.check should be a simple 'npm run ... && ...' chain; unsupported entries: "
            + ", ".join(invalid)
        )
    return commands


def read_active_validation_entries() -> list[str]:
    lines = ROOT_README.read_text().splitlines()
    start_index = None
    for index, line in enumerate(lines):
        if line.strip() == ACTIVE_VALIDATION_HEADING:
            start_index = index + 1
            break
    if start_index is None:
        raise ValueError(f"README.md is missing '{ACTIVE_VALIDATION_HEADING}'.")

    entries: list[str] = []
    for line in lines[start_index:]:
        stripped = line.strip()
        if not stripped:
            if entries:
                break
            continue
        if not stripped.startswith("- "):
            if entries:
                break
            continue
        match = COMMAND_RE.search(stripped)
        if match:
            entries.append(match.group(1))
    return entries


def main() -> int:
    errors: list[str] = []
    try:
        check_chain = load_check_chain()
        documented_entries = read_active_validation_entries()
    except Exception as exc:
        print(f"validation-surface-docs: {exc}", file=sys.stderr)
        return 1

    documented_set = set(documented_entries)
    missing = [command for command in check_chain if command not in documented_set]
    if missing:
        errors.append(
            "README.md Active validation entrypoints is missing commands from package.json scripts.check: "
            + ", ".join(missing)
        )

    check_scripts = {command.removeprefix("npm run ") for command in check_chain}
    unknown = [
        command
        for command in documented_entries
        if command.startswith("npm run check:")
        and command.removeprefix("npm run ") not in check_scripts
    ]
    if unknown:
        errors.append(
            "README.md Active validation entrypoints lists check commands not present in package.json scripts.check: "
            + ", ".join(unknown)
        )

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(
        "validation-surface-docs: README.md documents package.json scripts.check entries: "
        + ", ".join(check_chain)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
