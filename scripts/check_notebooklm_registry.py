#!/usr/bin/env python3
"""
Validate NotebookLM notebook mappings for publication packages.

The registry is intentionally split across package status.yaml files so the
notebook pointer travels with the publication lifecycle manifest. This check
walks post_map.yaml and verifies that each publication entry has either a
NotebookLM mapping or an explicit no-notebook note.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
POST_MAP_PATH = REPO_ROOT / "publication_strategy_and_archive" / "post_map.yaml"
NOTEBOOK_URL_PREFIX = "https://notebooklm.google.com/notebook/"
UUID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
)


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping at {path}")
    return data


def notebook_url(notebook_id: str) -> str:
    return f"{NOTEBOOK_URL_PREFIX}{notebook_id}"


def collect_notebooks_from_status(status_data: dict[str, Any], slug: str) -> tuple[list[dict[str, Any]], str | None]:
    config = status_data.get("config") or {}
    if not isinstance(config, dict):
        return [], "status.yaml config is not a mapping"

    post_mappings = config.get("notebooklm_posts") or {}
    if post_mappings:
        entry = post_mappings.get(slug)
        if not entry:
            return [], f"missing config.notebooklm_posts.{slug}"
        if entry.get("no_notebook_found"):
            return [], None
        notebooks: list[dict[str, Any]] = []
        primary = entry.get("primary")
        if primary:
            notebooks.append({**primary, "role": "primary"})
        for related in entry.get("related") or []:
            notebooks.append({**related, "role": "related"})
        return notebooks, None

    if config.get("no_notebook_found"):
        return [], None

    primary_id = config.get("notebooklm_notebook_id")
    if not primary_id:
        return [], "missing config.notebooklm_notebook_id or no_notebook_found"

    notebooks = [
        {
            "id": str(primary_id),
            "title": config.get("notebooklm_notebook_title", ""),
            "url": config.get("notebooklm_notebook_url", ""),
            "role": "primary",
        }
    ]
    for related in config.get("notebooklm_related_notebooks") or []:
        notebooks.append({**related, "role": "related"})
    return notebooks, None


def validate_notebook_entry(notebook: dict[str, Any], context: str) -> list[str]:
    errors: list[str] = []
    notebook_id = str(notebook.get("id", "")).strip()
    url = str(notebook.get("url", "")).strip()
    title = str(notebook.get("title", "")).strip()

    if not UUID_PATTERN.match(notebook_id):
        errors.append(f"{context}: invalid NotebookLM UUID '{notebook_id}'")
    if url != notebook_url(notebook_id):
        errors.append(f"{context}: URL does not match ID ({url!r})")
    if not title:
        errors.append(f"{context}: missing title")
    return errors


def extract_json(raw: str) -> dict[str, Any]:
    start = raw.find("{")
    if start == -1:
        raise ValueError(raw.strip() or "empty output")
    return json.loads(raw[start:])


def run_notebooklm_json(args: list[str]) -> dict[str, Any]:
    result = subprocess.run(
        [str(REPO_ROOT / ".venv/bin/notebooklm"), *args],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stdout.strip())
    data = extract_json(result.stdout)
    if data.get("error"):
        raise RuntimeError(data.get("message") or json.dumps(data))
    return data


def validate_live(notebook_ids: set[str]) -> list[str]:
    errors: list[str] = []
    for notebook_id in sorted(notebook_ids):
        try:
            metadata = run_notebooklm_json(["metadata", "-n", notebook_id, "--json"])
            artifacts = run_notebooklm_json(["artifact", "list", "-n", notebook_id, "--json"])
        except Exception as exc:  # noqa: BLE001 - command output is the useful failure here.
            errors.append(f"{notebook_id}: NotebookLM CLI lookup failed: {exc}")
            continue
        if metadata.get("id") != notebook_id:
            errors.append(f"{notebook_id}: metadata returned {metadata.get('id')!r}")
        if artifacts.get("notebook_id") != notebook_id:
            errors.append(f"{notebook_id}: artifact list returned {artifacts.get('notebook_id')!r}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate publication NotebookLM registry mappings.")
    parser.add_argument("--live", action="store_true", help="Resolve every notebook ID through the NotebookLM CLI.")
    args = parser.parse_args()

    post_map = load_yaml(POST_MAP_PATH).get("posts") or {}
    errors: list[str] = []
    notebook_ids: set[str] = set()

    for slug, entry in post_map.items():
        context = f"post_map.yaml:{slug}"
        research_folder = entry.get("research_folder")
        if research_folder in (None, ""):
            errors.append(f"{context}: missing research_folder")
            continue
        if research_folder == ".":
            notebook_note = entry.get("notebooklm") or {}
            if not notebook_note.get("no_notebook_found"):
                errors.append(f"{context}: root entry needs notebooklm.no_notebook_found")
            continue

        status_path = REPO_ROOT / str(research_folder).rstrip("/") / "status.yaml"
        if not status_path.exists():
            errors.append(f"{context}: missing status manifest at {status_path.relative_to(REPO_ROOT)}")
            continue

        status_data = load_yaml(status_path)
        notebooks, error = collect_notebooks_from_status(status_data, slug)
        if error:
            errors.append(f"{context}: {error}")
            continue

        for notebook in notebooks:
            role = notebook.get("role", "notebook")
            nb_context = f"{context}:{role}"
            errors.extend(validate_notebook_entry(notebook, nb_context))
            if notebook.get("id"):
                notebook_ids.add(str(notebook["id"]))

    if args.live and notebook_ids:
        errors.extend(validate_live(notebook_ids))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    live_suffix = " with live NotebookLM resolution" if args.live else ""
    print(f"NotebookLM registry OK: {len(post_map)} post_map entries, {len(notebook_ids)} notebook IDs{live_suffix}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
