#!/usr/bin/env python3
"""
Initialize status.yaml for publication packages.

By default this initializes top-level publication packages. Use --package for a
specific nested leaf package or --recursive to discover README-backed package
directories recursively.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from lifecycle import PUBLICATIONS_DIR, STAGES, resolve_package_path


IGNORED_SEGMENTS = {
    "archive",
    "artifacts",
    "papers",
    "sources",
    "reference",
    "implementation",
    "notes",
    "core",
    "distribution",
    "socials",
}

STAGE_DEFAULTS = {
    "done": False,
    "last_updated": None,
}


def discover_packages(recursive: bool) -> list[Path]:
    pattern = "**/README.md" if recursive else "*/README.md"
    packages = []
    for readme in sorted(PUBLICATIONS_DIR.glob(pattern)):
        rel_parts = readme.parent.relative_to(PUBLICATIONS_DIR).parts
        if any(part in IGNORED_SEGMENTS for part in rel_parts):
            continue
        packages.append(readme.parent)
    return packages


def manifest_template(package_path: Path) -> dict:
    rel_parts = package_path.relative_to(PUBLICATIONS_DIR).parts
    data = {
        "kind": "leaf",
        "publication": package_path.name,
        "revision": 1,
        "stages": {},
        "config": {},
    }
    if len(rel_parts) > 1:
        data["parent_package"] = rel_parts[0]
    for stage in STAGES:
        data["stages"][stage] = dict(STAGE_DEFAULTS)
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize status.yaml for publication packages.")
    parser.add_argument("--package", help="Package path relative to publications/")
    parser.add_argument("--recursive", action="store_true", help="Discover package README directories recursively.")
    args = parser.parse_args()

    if args.package:
        packages = [resolve_package_path(args.package)]
    else:
        packages = discover_packages(args.recursive)

    print(f"Initializing status for {len(packages)} package(s)...")

    for package in packages:
        status_file = package / "status.yaml"
        if status_file.exists():
            print(f"  Skipping {package.relative_to(PUBLICATIONS_DIR)} (status.yaml already exists)")
            continue

        data = manifest_template(package)
        with open(status_file, "w") as handle:
            yaml.dump(data, handle, default_flow_style=False, sort_keys=False)
        print(f"  Initialized {package.relative_to(PUBLICATIONS_DIR)}/status.yaml")

    print("\nInitialization complete.")


if __name__ == "__main__":
    main()
