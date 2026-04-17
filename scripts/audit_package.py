#!/usr/bin/env python3
"""
Advisory Package Auditor: scans a publication package for structural health
based on the scaffold workflow.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from lifecycle import REPO_ROOT, load_status_ref, resolve_package_path


def scan_for_urls(markdown_path: Path) -> set[str]:
    if not markdown_path.exists():
        return set()
    text = markdown_path.read_text()
    urls = re.findall(r"https?://(?:papers\.nips\.cc|arxiv\.org|pdf|transformer-circuits\.pub)[^\s\)]+", text)
    return set(urls)


def resolve_evidence_root(package_path: Path, status_data: dict) -> tuple[Path | None, str]:
    config = status_data.get("config", {})
    evidence_path = config.get("evidence_path")
    if evidence_path:
        resolved = (REPO_ROOT / evidence_path).resolve()
        return resolved, f"Configured evidence path: {evidence_path}"

    shared_evidence_path = config.get("shared_evidence_path")
    if shared_evidence_path:
        resolved = (REPO_ROOT / shared_evidence_path).resolve()
        return resolved, f"Shared evidence path: {shared_evidence_path}"

    for dirname in ["sources", "papers"]:
        candidate = package_path / dirname
        if candidate.is_dir():
            return candidate, f"Local evidence directory: {dirname}/"
    return None, "No evidence directory configured"


def count_local_sources(evidence_root: Path) -> int:
    for dirname in ["markdown", "sources/markdown", "papers/markdown"]:
        candidate = evidence_root / dirname
        if candidate.exists():
            return len(list(candidate.glob("*.md")))
    return len([path for path in evidence_root.rglob("*.md") if not any(part.startswith(".") for part in path.parts)])


def audit_umbrella_config(package_path: Path, status_data: dict, report: dict) -> None:
    config = status_data.get("config", {})
    leaf_packages = config.get("leaf_packages") or []
    default_leaf = config.get("default_leaf_package")

    if not leaf_packages and not default_leaf:
        report["checks"].append(
            {
                "status": "WARNING",
                "message": "Umbrella manifest should name 'config.leaf_packages' or 'config.default_leaf_package'.",
            }
        )
        return

    if default_leaf:
        leaf_path = REPO_ROOT / "publications" / default_leaf
        if leaf_path.exists():
            report["checks"].append({"status": "PASS", "message": f"Default leaf resolves: {default_leaf}"})
        else:
            report["checks"].append({"status": "FAIL", "message": f"Default leaf path is missing: {default_leaf}"})

    for leaf in leaf_packages:
        leaf_path = REPO_ROOT / "publications" / leaf
        if leaf_path.exists():
            report["checks"].append({"status": "PASS", "message": f"Leaf package resolves: {leaf}"})
        else:
            report["checks"].append({"status": "FAIL", "message": f"Leaf package path is missing: {leaf}"})


def audit_package(package_arg: str) -> dict:
    try:
        manifest_ref, status_data = load_status_ref(package_arg)
    except FileNotFoundError:
        package_path = resolve_package_path(package_arg)
        return {"id": "warning", "message": f"Missing 'status.yaml' manifest in {package_path.relative_to(REPO_ROOT)}."}
    except ValueError as exc:
        return {"id": "error", "message": str(exc)}

    package_path = manifest_ref.package_path
    config = status_data.get("config", {})
    ignore = set(config.get("ignore_scaffold_audit", []))
    package_kind = status_data.get("kind", "leaf")

    report = {
        "package": manifest_ref.package_key,
        "kind": package_kind,
        "revision": status_data.get("revision", 1),
        "checks": [],
        "evidence_drift": [],
    }

    if (package_path / "README.md").exists():
        report["checks"].append({"status": "PASS", "message": "Package README present."})
    else:
        report["checks"].append({"status": "WARNING", "message": "Missing package README."})

    evidence_root, evidence_label = resolve_evidence_root(package_path, status_data)
    if evidence_root:
        if evidence_root.exists():
            report["checks"].append({"status": "PASS", "message": evidence_label})
        else:
            report["checks"].append({"status": "FAIL", "message": f"{evidence_label} does not exist."})
    else:
        report["checks"].append({"status": "WARNING", "message": "Missing local or shared evidence directory."})

    for dirname, description in {
        "artifacts": "Output layer for media and production assets",
        "archive": "Historical draft history",
    }.items():
        if dirname in ignore:
            continue
        candidate = package_path / dirname
        if candidate.is_dir():
            report["checks"].append({"status": "PASS", "message": f"'{dirname}/' directory present."})
        else:
            report["checks"].append({"status": "WARNING", "message": f"Missing '{dirname}/' directory. ({description})"})

    if package_kind == "umbrella":
        audit_umbrella_config(package_path, status_data, report)
        if not config.get("markdown_path"):
            report["checks"].append({"status": "INFO", "message": "Umbrella manifest does not require 'config.markdown_path'."})
            return report

    markdown_path_str = config.get("markdown_path")
    if not markdown_path_str:
        report["checks"].append({"status": "WARNING", "message": "Missing 'config.markdown_path' in status.yaml"})
        return report

    markdown_path = REPO_ROOT / markdown_path_str
    if not markdown_path.exists():
        report["checks"].append({"status": "FAIL", "message": f"config.markdown_path points to missing file: {markdown_path_str}"})
        return report

    report["checks"].append({"status": "PASS", "message": f"Live draft link valid: {markdown_path.name}"})

    found_urls = scan_for_urls(markdown_path)
    if found_urls and evidence_root and evidence_root.exists():
        local_count = count_local_sources(evidence_root)
        if len(found_urls) > local_count + 2:
            report["evidence_drift"].append(
                f"Draft cites {len(found_urls)} external links, but only {local_count} local source markdown files were found."
            )
    elif found_urls and not evidence_root:
        report["evidence_drift"].append(
            f"Draft cites {len(found_urls)} external links, but no local or shared evidence directory is configured."
        )

    return report


def print_report(report: dict) -> None:
    if "id" in report and report["id"] in {"error", "warning"}:
        color = "\033[91m" if report["id"] == "error" else "\033[93m"
        print(f"{color}[{report['id'].upper()}]\033[0m {report['message']}")
        return

    print(f"PRE-FLIGHT ADVISORY: {report['package']} (Rev {report.get('revision', 1)})")
    print("-" * 50)
    for check in report["checks"]:
        color = ""
        if check["status"] == "PASS":
            color = "\033[92m"
        elif check["status"] == "WARNING":
            color = "\033[93m"
        elif check["status"] == "FAIL":
            color = "\033[91m"
        elif check["status"] == "INFO":
            color = "\033[94m"
        print(f"{color}[{check['status']}]\033[0m {check['message']}")

    if report["evidence_drift"]:
        print("\n\033[96mEVIDENCE DISCOVERY:\033[0m")
        for item in report["evidence_drift"]:
            print(f"  {item}")
    print("-" * 50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit a publication package.")
    parser.add_argument("--package", required=True, help="Package path relative to publications/")
    args = parser.parse_args()

    report = audit_package(args.package)
    print_report(report)
