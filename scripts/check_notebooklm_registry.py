#!/usr/bin/env python3
"""
Validate NotebookLM notebook mappings for publication packages.

The public repository stores non-sensitive NotebookLM titles in package
status.yaml files. Restricted notebook IDs and owner URLs live in the private
overlay at CONTENT_PRIVATE_DIR/notebooklm_registry.yaml, defaulting to the
ignored `.private/notebooklm_registry.yaml`.
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
from private_registry import NOTEBOOK_URL_PREFIX, load_notebook_registry, resolve_notebooks_for_status


REPO_ROOT = Path(__file__).resolve().parents[1]
POST_MAP_PATH = REPO_ROOT / "publication_strategy_and_archive" / "post_map.yaml"
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


def collect_public_notebooks_from_status(status_data: dict[str, Any], slug: str) -> tuple[list[dict[str, Any]], str | None]:
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
            notebooks.append({"title": primary.get("title", ""), "role": "primary"})
        for related in entry.get("related") or []:
            notebooks.append({"title": related.get("title", ""), "role": "related"})
        return notebooks, None

    if config.get("no_notebook_found"):
        return [], None

    primary_title = config.get("notebooklm_notebook_title")
    if not primary_title:
        return [], "missing config.notebooklm_notebook_title or no_notebook_found"

    notebooks = [{"title": str(primary_title), "role": "primary"}]
    for related in config.get("notebooklm_related_notebooks") or []:
        notebooks.append({"title": related.get("title", ""), "role": "related"})
    return notebooks, None


def validate_public_notebook_entry(notebook: dict[str, Any], context: str) -> list[str]:
    errors: list[str] = []
    if notebook.get("id") or notebook.get("url"):
        errors.append(f"{context}: public status must not track restricted NotebookLM id/url")
    if not str(notebook.get("title", "")).strip():
        errors.append(f"{context}: missing title")
    return errors


def validate_private_notebook_entry(notebook: dict[str, Any], context: str) -> list[str]:
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
    private_registry = load_notebook_registry(required=args.live)
    has_private_registry = bool(private_registry)
    errors: list[str] = []
    notebook_ids: set[str] = set()
    public_notebook_count = 0

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
        notebooks, error = collect_public_notebooks_from_status(status_data, slug)
        if error:
            errors.append(f"{context}: {error}")
            continue

        for notebook in notebooks:
            role = notebook.get("role", "notebook")
            nb_context = f"{context}:{role}"
            errors.extend(validate_public_notebook_entry(notebook, nb_context))
            public_notebook_count += 1

        private_notebooks = resolve_notebooks_for_status(status_path, status_data=status_data, slug=slug)
        if has_private_registry:
            if notebooks and not private_notebooks:
                errors.append(f"{context}: missing private NotebookLM registry entry")
            for notebook in private_notebooks:
                role = notebook.get("role", "notebook")
                nb_context = f"{context}:private:{role}"
                errors.extend(validate_private_notebook_entry(notebook, nb_context))
                if notebook.get("id"):
                    notebook_ids.add(str(notebook["id"]))

    if args.live and notebook_ids:
        errors.extend(validate_live(notebook_ids))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    private_suffix = f", {len(notebook_ids)} private notebook IDs" if has_private_registry else ", private registry not present"
    live_suffix = " with live NotebookLM resolution" if args.live else ""
    print(
        f"NotebookLM registry OK: {len(post_map)} post_map entries, "
        f"{public_notebook_count} public notebook titles{private_suffix}{live_suffix}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
