from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_DIR = REPO_ROOT / "publication_strategy_and_archive" / "substack_archive"
POST_MAP_PATH = REPO_ROOT / "publication_strategy_and_archive" / "post_map.yaml"
METADATA_PATH = ARCHIVE_DIR / "metadata.json"
README_PATH = REPO_ROOT / "README.md"
README_MAP_START = "<!-- GENERATED_PUBLICATION_MAP:START -->"
README_MAP_END = "<!-- GENERATED_PUBLICATION_MAP:END -->"


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping at {path}")
    return data


def load_post_map(path: Path = POST_MAP_PATH) -> dict[str, dict[str, Any]]:
    data = load_yaml(path)
    posts = data.get("posts") or {}
    if not isinstance(posts, dict):
        raise ValueError(f"Expected 'posts' mapping in {path}")
    normalized: dict[str, dict[str, Any]] = {}
    for slug, entry in posts.items():
        if not isinstance(entry, dict):
            raise ValueError(f"Expected mapping for post '{slug}' in {path}")
        normalized[slug] = entry
    return normalized


def render_publication_mapping_table(post_map: dict[str, dict[str, Any]]) -> str:
    lines = [
        "| Substack Publication | Repository Folder |",
        "| :--- | :--- |",
    ]
    for slug, entry in post_map.items():
        title = str(entry.get("title", slug))
        research_folder = entry.get("research_folder")
        if research_folder in (None, "", "."):
            folder_cell = "*(N/A / Root)*"
        else:
            normalized = str(research_folder).rstrip("/") + "/"
            folder_cell = f"`{normalized}`"
        lines.append(f"| **{title}** | {folder_cell} |")
    return "\n".join(lines)


def replace_generated_section(
    text: str,
    new_body: str,
    start_marker: str = README_MAP_START,
    end_marker: str = README_MAP_END,
) -> str:
    start = text.find(start_marker)
    end = text.find(end_marker)
    if start == -1 or end == -1 or end < start:
        raise ValueError("README publication mapping markers not found")
    before = text[: start + len(start_marker)]
    after = text[end:]
    return f"{before}\n{new_body}\n{after}"


def write_readme_publication_map(
    post_map: dict[str, dict[str, Any]],
    readme_path: Path = README_PATH,
) -> None:
    current = readme_path.read_text(encoding="utf-8")
    rendered = render_publication_mapping_table(post_map)
    updated = replace_generated_section(current, rendered)
    if updated != current:
        readme_path.write_text(updated, encoding="utf-8")
