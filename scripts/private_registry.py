#!/usr/bin/env python3
"""Helpers for local private metadata overlays.

The public repository must not track restricted NotebookLM IDs, owner URLs, or
channel-side operational state. Local tools can still resolve those values from
CONTENT_PRIVATE_DIR, which defaults to the ignored `.private/` directory.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_URL_PREFIX = "https://notebooklm.google.com/notebook/"


def private_dir() -> Path:
    configured = os.environ.get("CONTENT_PRIVATE_DIR", ".private")
    path = Path(configured)
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path


def notebook_registry_path() -> Path:
    return private_dir() / "notebooklm_registry.yaml"


def load_yaml_mapping(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected YAML mapping at {path}")
    return data


def write_yaml_mapping(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")


def load_notebook_registry(required: bool = False) -> dict[str, Any]:
    path = notebook_registry_path()
    if not path.exists():
        if required:
            raise FileNotFoundError(f"Missing private NotebookLM registry at {path}")
        return {}
    return load_yaml_mapping(path)


def repo_relpath(path: Path) -> str:
    resolved = path if path.is_absolute() else REPO_ROOT / path
    return resolved.resolve().relative_to(REPO_ROOT).as_posix()


def notebook_url(notebook_id: str) -> str:
    return f"{NOTEBOOK_URL_PREFIX}{notebook_id}"


def _entry_notebooks(entry: dict[str, Any] | None, slug: str | None = None) -> list[dict[str, Any]]:
    if not isinstance(entry, dict):
        return []
    if slug and isinstance(entry.get("posts"), dict) and isinstance(entry["posts"].get(slug), dict):
        entry = entry["posts"][slug]
    notebooks: list[dict[str, Any]] = []
    primary = entry.get("primary")
    if isinstance(primary, dict):
        notebooks.append({**primary, "role": primary.get("role") or "primary"})
    for related in entry.get("related") or []:
        if isinstance(related, dict):
            notebooks.append({**related, "role": related.get("role") or "related"})
    return notebooks


def resolve_notebooks_for_status(
    status_path: Path,
    status_data: dict[str, Any] | None = None,
    slug: str | None = None,
) -> list[dict[str, Any]]:
    """Resolve private NotebookLM entries for a public status manifest."""

    registry = load_notebook_registry(required=False)
    if not registry:
        return []

    status_relpath = repo_relpath(status_path)
    status_entry = next(
        (entry for entry in registry.get("statuses") or [] if entry.get("status_path") == status_relpath),
        None,
    )
    if slug and isinstance(registry.get("posts"), dict) and isinstance(registry["posts"].get(slug), dict):
        notebooks = _entry_notebooks(registry["posts"][slug])
        if notebooks:
            return notebooks

    notebooks = _entry_notebooks(status_entry, slug=slug)
    if notebooks:
        return notebooks

    config = (status_data or {}).get("config") if isinstance(status_data, dict) else {}
    title = config.get("notebooklm_notebook_title") if isinstance(config, dict) else None
    if title:
        title_text = str(title).strip()
        for entry in registry.get("statuses") or []:
            for notebook in _entry_notebooks(entry):
                if str(notebook.get("title", "")).strip() == title_text:
                    return [notebook]
            for post_entry in (entry.get("posts") or {}).values() if isinstance(entry, dict) else []:
                for notebook in _entry_notebooks(post_entry):
                    if str(notebook.get("title", "")).strip() == title_text:
                        return [notebook]
    return []


def resolve_primary_notebook_for_status(
    status_path: Path,
    status_data: dict[str, Any] | None = None,
    slug: str | None = None,
) -> dict[str, Any] | None:
    for notebook in resolve_notebooks_for_status(status_path, status_data=status_data, slug=slug):
        if notebook.get("role") == "primary":
            return notebook
    notebooks = resolve_notebooks_for_status(status_path, status_data=status_data, slug=slug)
    return notebooks[0] if notebooks else None


def upsert_primary_notebook_for_status(
    status_path: Path,
    package: str,
    notebook_id: str,
    title: str,
) -> dict[str, Any]:
    registry = load_notebook_registry(required=False)
    if not registry:
        registry = {
            "schema_version": 1,
            "source": "local private NotebookLM registry",
            "statuses": [],
            "posts": {},
        }
    registry["updated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    status_relpath = repo_relpath(status_path)
    statuses = registry.setdefault("statuses", [])
    entry = next((item for item in statuses if item.get("status_path") == status_relpath), None)
    if not isinstance(entry, dict):
        entry = {"status_path": status_relpath, "package": package}
        statuses.append(entry)
    entry["primary"] = {
        "role": "primary",
        "id": notebook_id,
        "title": title,
        "url": notebook_url(notebook_id),
    }
    write_yaml_mapping(notebook_registry_path(), registry)
    return entry["primary"]
