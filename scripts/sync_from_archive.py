#!/usr/bin/env python3
"""
Sync a published Substack archive snapshot into a publication package.

Leaf packages can sync directly from their configured slug. Umbrella packages
can still bootstrap slug subfolders with --slug.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import yaml

from lifecycle import REPO_ROOT, load_status, package_key_for_path, resolve_package_path, save_status


ARCHIVE_DIR = REPO_ROOT / "publication_strategy_and_archive" / "substack_archive"
METADATA_PATH = ARCHIVE_DIR / "metadata.json"
POST_MAP_PATH = REPO_ROOT / "publication_strategy_and_archive" / "post_map.yaml"


def load_metadata() -> list[dict]:
    with open(METADATA_PATH) as handle:
        return json.load(handle)


def load_post_map() -> dict:
    with open(POST_MAP_PATH) as handle:
        return yaml.safe_load(handle)


def find_archive_entry(metadata: list[dict], slug: str) -> dict | None:
    for entry in metadata:
        if entry["slug"] == slug:
            return entry
    return None


def find_slugs_for_package(post_map: dict, package_key: str) -> list[str]:
    repo_path = f"publications/{package_key}"
    slugs = []
    for slug, info in post_map.get("posts", {}).items():
        if info.get("research_folder", "").rstrip("/") == repo_path:
            slugs.append(slug)
    return slugs


def is_umbrella(package_path: Path) -> bool:
    readme = package_path / "README.md"
    if not readme.exists():
        return False
    return "umbrella" in readme.read_text().lower()


def dedupe(values: list[str]) -> list[str]:
    seen = set()
    output = []
    for value in values:
        if value and value not in seen:
            output.append(value)
            seen.add(value)
    return output


def determine_destination_path(package_path: Path, slug: str, umbrella: bool, status_data: dict | None) -> Path:
    if umbrella:
        destination_dir = package_path / slug
        destination_dir.mkdir(parents=True, exist_ok=True)
        return destination_dir / f"{slug}.md"

    markdown_path = status_data.get("config", {}).get("markdown_path") if status_data else None
    if markdown_path:
        return (REPO_ROOT / markdown_path).resolve()
    return package_path / f"{slug}.md"


def sync_slug(package_path: Path, slug: str, archive_entry: dict, umbrella: bool, status_data: dict | None) -> Path | None:
    archive_markdown = REPO_ROOT / archive_entry["md_path"]
    if not archive_markdown.exists():
        print(f"ERROR: Archive file not found: {archive_markdown}")
        return None

    destination_path = determine_destination_path(package_path, slug, umbrella, status_data)
    destination_path.parent.mkdir(parents=True, exist_ok=True)

    if destination_path.exists():
        old_content = destination_path.read_text()
        new_content = archive_markdown.read_text()
        if old_content == new_content:
            print(f"  Already in sync: {destination_path.relative_to(REPO_ROOT)}")
            return destination_path
        archive_dir = package_path / "archive"
        archive_dir.mkdir(exist_ok=True)
        archive_destination = archive_dir / f"{slug}_pre_rev.md"
        shutil.copy2(destination_path, archive_destination)
        print(f"  Archived previous: {archive_destination.relative_to(REPO_ROOT)}")

    shutil.copy2(archive_markdown, destination_path)
    print(f"  Synced: {archive_markdown.relative_to(REPO_ROOT)} -> {destination_path.relative_to(REPO_ROOT)}")
    return destination_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync a Substack archive snapshot into a publication package.")
    parser.add_argument("--package", required=True, help="Package path relative to publications/")
    parser.add_argument("--slug", help="Specific Substack slug to sync")
    parser.add_argument("--list-slugs", action="store_true", help="List available slugs and exit")
    args = parser.parse_args()

    try:
        package_path = resolve_package_path(args.package)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    if not package_path.exists():
        print(f"ERROR: Package not found: {package_path}")
        sys.exit(1)

    package_key = package_key_for_path(package_path)
    status_data = load_status(package_path)
    metadata = load_metadata()
    post_map = load_post_map()

    configured_slug = None
    if status_data:
        configured_slug = status_data.get("config", {}).get("substack_slug")

    available_slugs = dedupe([configured_slug] + find_slugs_for_package(post_map, package_key))

    if args.list_slugs:
        if not available_slugs:
            print(f"No slugs found for '{package_key}'.")
            return
        print(f"Slugs for '{package_key}':")
        for slug in available_slugs:
            entry = find_archive_entry(metadata, slug)
            title = entry["title"] if entry else "(not in archive)"
            print(f"  {slug} - {title}")
        return

    umbrella = is_umbrella(package_path)

    if args.slug:
        target_slugs = [args.slug]
    elif len(available_slugs) == 1:
        target_slugs = available_slugs
    elif len(available_slugs) > 1:
        print(f"ERROR: Package '{package_key}' has multiple candidate slugs. Use --slug to specify one:")
        for slug in available_slugs:
            entry = find_archive_entry(metadata, slug)
            title = entry["title"] if entry else "(not in archive)"
            print(f"  {slug} - {title}")
        sys.exit(1)
    else:
        print(
            f"ERROR: No slug was provided or discovered for '{package_key}'. "
            "Set config.substack_slug in status.yaml or pass --slug."
        )
        sys.exit(1)

    for slug in target_slugs:
        entry = find_archive_entry(metadata, slug)
        if not entry:
            print(f"WARNING: Slug '{slug}' not found in archive metadata.json, skipping.")
            continue

        print(f"\nSyncing '{slug}' ({entry['title']}):")
        destination_path = sync_slug(package_path, slug, entry, umbrella, status_data)

        if destination_path and status_data:
            config = status_data.setdefault("config", {})
            config["markdown_path"] = str(destination_path.relative_to(REPO_ROOT))
            config["substack_slug"] = slug
            config["substack_url"] = "https://lambpetros.substack.com"
            save_status(package_path, status_data)
            print("  Updated config in status.yaml")

    print("\nSync complete.")


if __name__ == "__main__":
    main()
