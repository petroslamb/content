#!/usr/bin/env python3
"""
Advisory Package Auditor: Scans a publication package for structural health
based on the "Scaffold Hypothesis" (workflows/package-normalization/README.md).
"""

import argparse
import os
import re
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLICATIONS_DIR = REPO_ROOT / "publications"

def load_status(package_path):
    status_path = package_path / "status.yaml"
    if not status_path.exists():
        return None
    with open(status_path) as f:
        return yaml.safe_load(f)

def scan_for_urls(markdown_path):
    if not markdown_path.exists():
        return set()
    text = markdown_path.read_text()
    # Simple regex for common academic/source URLs
    urls = re.findall(r'https?://(?:papers\.nips\.cc|arxiv\.org|pdf|transformer-circuits\.pub)[^\s\)]+', text)
    return set(urls)

def audit_package(package_name):
    package_path = PUBLICATIONS_DIR / package_name
    if not package_path.exists():
        return {"id": "error", "message": f"Package '{package_name}' not found."}

    status = load_status(package_path)
    if not status:
        return {"id": "warning", "message": "Missing 'status.yaml' manifest."}

    config = status.get("config", {})
    ignore = config.get("ignore_scaffold_audit", [])
    
    report = {
        "package": package_name,
        "revision": status.get("revision", 1),
        "checks": [],
        "evidence_drift": []
    }

    # 1. Structural Checks
    dirs_to_check = {
        "sources": "Evidence layer for research materials",
        "artifacts": "Output layer for media/production assets",
        "archive": "Historical draft history"
    }

    for d, desc in dirs_to_check.items():
        if d in ignore:
            continue
        # Check both the directory and the old 'papers' folder for backward compat during transition
        p = package_path / d
        if not p.is_dir():
            if d == "sources" and (package_path / "papers").is_dir():
                report["checks"].append({"status": "INFO", "message": f"Legacy folder 'papers/' found. Consider renaming to 'sources/'."})
            else:
                report["checks"].append({"status": "WARNING", "message": f"Missing '{d}/' directory. ({desc})"})
        else:
            report["checks"].append({"status": "PASS", "message": f"'{d}/' directory present."})

    # 2. Pointer Checks
    md_path_str = config.get("markdown_path")
    if md_path_str:
        md_path = REPO_ROOT / md_path_str
        if not md_path.exists():
            report["checks"].append({"status": "FAIL", "message": f"config.markdown_path points to missing file: {md_path_str}"})
        else:
            report["checks"].append({"status": "PASS", "message": f"Live draft link valid: {md_path.name}"})
            
            # 3. Evidence Discovery (Citation Drift)
            found_urls = scan_for_urls(md_path)
            if found_urls:
                # Check sources/markdown for matches (very rough heuristic check for now)
                sources_dir = package_path / "sources" / "markdown"
                if not sources_dir.exists():
                    sources_dir = package_path / "papers" / "markdown" # Compat
                
                if sources_dir.exists():
                    local_count = len(list(sources_dir.glob("*.md")))
                    if len(found_urls) > local_count + 2: # Buffer for non-paper URLs
                         report["evidence_drift"].append(f"Draft cites {len(found_urls)} external links, but only {local_count} local sources found.")
                else:
                    report["evidence_drift"].append(f"Draft cites {len(found_urls)} external links, but no local sources directory found.")
    else:
        report["checks"].append({"status": "WARNING", "message": "Missing 'config.markdown_path' in status.yaml"})

    return report

def print_report(report):
    print(f"\nPRE-FLIGHT ADVISORY: {report['package']} (Rev {report['revision']})")
    print("-" * 50)
    for c in report["checks"]:
        color = ""
        if c["status"] == "PASS": color = "\033[92m" # Green
        elif c["status"] == "WARNING": color = "\033[93m" # Yellow
        elif c["status"] == "FAIL": color = "\033[91m" # Red
        elif c["status"] == "INFO": color = "\033[94m" # Blue
        
        print(f"{color}[{c['status']}]\033[0m {c['message']}")

    if report["evidence_drift"]:
        print("\n\033[96mEVIDENCE DISCOVERY:\033[0m")
        for d in report["evidence_drift"]:
            print(f"  {d}")
    print("-" * 50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit a publication package.")
    parser.add_argument("--package", required=True, help="Package name")
    parser.add_argument("--quiet", action="store_true", help="Only show warnings/fails")
    args = parser.parse_args()

    report = audit_package(args.package)
    print_report(report)
