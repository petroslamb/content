#!/usr/bin/env python3
"""
Sync From Archive: Pull a published Substack archive snapshot into a publication package.

For single-publication packages, copies the archive markdown as the canonical live draft.
For umbrella packages, creates a slug subfolder and places the snapshot there.

Usage:
  .venv/bin/python scripts/sync_from_archive.py --package neural-architectures --slug neural-architecture-design-as-a-compositional-32e
"""

import argparse
import json
import shutil
import sys
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_DIR = REPO_ROOT / "publication_strategy_and_archive" / "substack_archive"
METADATA_PATH = ARCHIVE_DIR / "metadata.json"
POST_MAP_PATH = REPO_ROOT / "publication_strategy_and_archive" / "post_map.yaml"
PUBLICATIONS_DIR = REPO_ROOT / "publications"


def load_metadata():
    with open(METADATA_PATH) as f:
        return json.load(f)


def load_post_map():
    with open(POST_MAP_PATH) as f:
        return yaml.safe_load(f)


def find_archive_entry(metadata, slug):
    for entry in metadata:
        if entry["slug"] == slug:
            return entry
    return None


def find_slugs_for_package(post_map, package_name):
    """Return all slugs that map to this package via post_map.yaml."""
    package_path = f"publications/{package_name}"
    slugs = []
    for slug, info in post_map.get("posts", {}).items():
        if info.get("research_folder", "").rstrip("/") == package_path:
            slugs.append(slug)
    return slugs


def is_umbrella(package_path):
    """Check if this is an umbrella package by looking at the README."""
    readme = package_path / "README.md"
    if not readme.exists():
        return False
    text = readme.read_text().lower()
    return "umbrella" in text


def load_status(package_path):
    status_path = package_path / "status.yaml"
    if not status_path.exists():
        return None
    with open(status_path) as f:
        return yaml.safe_load(f)


def save_status(package_path, data):
    status_path = package_path / "status.yaml"
    with open(status_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def sync_slug(package_path, slug, archive_entry, umbrella):
    """Copy the archive snapshot into the package."""
    archive_md = REPO_ROOT / archive_entry["md_path"]
    if not archive_md.exists():
        print(f"ERROR: Archive file not found: {archive_md}")
        return None

    if umbrella:
        # Umbrella: create a subfolder for this slug
        dest_dir = package_path / slug
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / f"{slug}.md"
    else:
        # Single-publication: place at package root
        dest_path = package_path / f"{slug}.md"

    # If destination exists and is different, archive the old one
    if dest_path.exists():
        old_content = dest_path.read_text()
        new_content = archive_md.read_text()
        if old_content == new_content:
            print(f"  Already in sync: {dest_path.relative_to(REPO_ROOT)}")
            return dest_path
        # Archive the old version
        archive_dir = package_path / "archive"
        archive_dir.mkdir(exist_ok=True)
        archive_dest = archive_dir / f"{slug}_pre_rev.md"
        shutil.copy2(dest_path, archive_dest)
        print(f"  Archived previous: {archive_dest.relative_to(REPO_ROOT)}")

    shutil.copy2(archive_md, dest_path)
    print(f"  Synced: {archive_md.relative_to(REPO_ROOT)} -> {dest_path.relative_to(REPO_ROOT)}")
    return dest_path


def main():
    parser = argparse.ArgumentParser(description="Sync a Substack archive snapshot into a publication package.")
    parser.add_argument("--package", required=True, help="Package name (e.g., neural-architectures)")
    parser.add_argument("--slug", help="Specific Substack slug to sync. Required for umbrella packages with multiple posts.")
    parser.add_argument("--list-slugs", action="store_true", help="List available slugs for this package and exit.")
    args = parser.parse_args()

    package_path = PUBLICATIONS_DIR / args.package
    if not package_path.exists():
        print(f"ERROR: Package not found: {package_path}")
        sys.exit(1)

    metadata = load_metadata()
    post_map = load_post_map()
    available_slugs = find_slugs_for_package(post_map, args.package)

    if not available_slugs:
        print(f"ERROR: No slugs found in post_map.yaml for package '{args.package}'")
        sys.exit(1)

    if args.list_slugs:
        print(f"Slugs for '{args.package}':")
        for s in available_slugs:
            entry = find_archive_entry(metadata, s)
            title = entry["title"] if entry else "(not in archive)"
            print(f"  {s} — {title}")
        sys.exit(0)

    umbrella = is_umbrella(package_path)

    # Determine which slug(s) to sync
    if args.slug:
        if args.slug not in available_slugs:
            print(f"ERROR: Slug '{args.slug}' not found for package '{args.package}'")
            print(f"Available: {', '.join(available_slugs)}")
            sys.exit(1)
        target_slugs = [args.slug]
    elif len(available_slugs) == 1:
        target_slugs = available_slugs
    else:
        print(f"ERROR: Package '{args.package}' has multiple slugs. Use --slug to specify:")
        for s in available_slugs:
            entry = find_archive_entry(metadata, s)
            title = entry["title"] if entry else "(not in archive)"
            print(f"  {s} — {title}")
        sys.exit(1)

    # Load status for config updates
    status_data = load_status(package_path)

    for slug in target_slugs:
        entry = find_archive_entry(metadata, slug)
        if not entry:
            print(f"WARNING: Slug '{slug}' not found in archive metadata.json, skipping.")
            continue

        print(f"\nSyncing '{slug}' ({entry['title']}):")
        dest_path = sync_slug(package_path, slug, entry, umbrella)

        if dest_path and status_data:
            # Update config
            if "config" not in status_data:
                status_data["config"] = {}

            config = status_data["config"]

            # Set markdown_path (relative to repo root)
            config["markdown_path"] = str(dest_path.relative_to(REPO_ROOT))

            # Extract post_id from URL (slug is in the URL)
            # We don't have post_id in metadata, so we store the slug and URL for lookup
            config["substack_slug"] = slug
            config["substack_url"] = "https://lambpetros.substack.com"

            save_status(package_path, status_data)
            print(f"  Updated config in status.yaml")

    print("\nSync complete.")


if __name__ == "__main__":
    main()
