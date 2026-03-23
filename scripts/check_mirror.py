from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from archive_utils import (
    METADATA_PATH,
    POST_MAP_PATH,
    README_PATH,
    ARCHIVE_DIR,
    load_post_map,
    render_publication_mapping_table,
    replace_generated_section,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
MIRROR_OUTPUT = REPO_ROOT / "publication_strategy_and_archive" / "mirror" / "_site"
PATH_PREFIX = os.environ.get("ELEVENTY_PATH_PREFIX", "/").strip()


def normalize_path_prefix(raw: str) -> str:
    if not raw or raw == "/":
        return "/"
    return f"/{raw.strip('/')}/"


def required_file_target(root: Path, href_path: str) -> Path:
    candidate = root / href_path.lstrip("/")
    if candidate.is_dir():
        return candidate / "index.html"
    if candidate.suffix:
        return candidate
    return candidate / "index.html"


def validate_metadata() -> list[dict[str, str]]:
    manifest = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    required_keys = {
        "slug",
        "title",
        "url",
        "post_date",
        "audience",
        "fetched_at",
        "content_hash",
        "md_path",
        "html_path",
        "hero_image",
        "mirror_enabled",
    }
    seen = set()
    for entry in manifest:
        missing = required_keys.difference(entry)
        if missing:
            raise SystemExit(f"Metadata entry missing keys {sorted(missing)}: {entry}")
        slug = entry["slug"]
        if slug in seen:
            raise SystemExit(f"Duplicate slug in metadata.json: {slug}")
        seen.add(slug)
        for key in ("md_path", "html_path"):
            target = REPO_ROOT / entry[key]
            if not target.exists():
                raise SystemExit(f"Missing archive file referenced by metadata: {target}")
        if entry["hero_image"]:
            hero = REPO_ROOT / entry["hero_image"]
            if not hero.exists():
                raise SystemExit(f"Missing hero image referenced by metadata: {hero}")
    return manifest


def validate_archive_assets(manifest: list[dict[str, str]]) -> None:
    for entry in manifest:
        markdown_path = REPO_ROOT / entry["md_path"]
        content = markdown_path.read_text(encoding="utf-8")
        for token in content.split("("):
            if not token.startswith("assets/"):
                continue
            asset_name = token.split(")", 1)[0]
            asset_path = markdown_path.parent / asset_name
            if not asset_path.exists():
                raise SystemExit(f"Broken local asset reference in {markdown_path}: {asset_name}")


def validate_readme_generation(post_map: dict[str, dict[str, str]]) -> None:
    current = README_PATH.read_text(encoding="utf-8")
    expected = replace_generated_section(current, render_publication_mapping_table(post_map))
    if current != expected:
        raise SystemExit("README publication mapping section is out of date with post_map.yaml")


def iter_built_html_files() -> list[Path]:
    return sorted(MIRROR_OUTPUT.rglob("*.html"))


def normalize_internal_path(link_path: str) -> str:
    prefix = normalize_path_prefix(PATH_PREFIX)
    if prefix != "/" and link_path.startswith(prefix):
        return "/" + link_path[len(prefix) :].lstrip("/")
    return link_path


def validate_built_links() -> None:
    if not MIRROR_OUTPUT.exists():
        raise SystemExit("Mirror output directory is missing. Run npm run build:mirror first.")
    html_files = iter_built_html_files()
    if not html_files:
        raise SystemExit("Mirror build output contains no HTML files.")

    for html_file in html_files:
        soup = BeautifulSoup(html_file.read_text(encoding="utf-8"), "html.parser")
        for element in soup.find_all(src=True) + soup.find_all(href=True):
            attr = "src" if element.has_attr("src") else "href"
            value = element.get(attr, "")
            if not value or value.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
                continue
            parsed = urlparse(value)
            if parsed.scheme in {"http", "https"}:
                continue

            path_value = parsed.path or ""
            if not path_value:
                continue
            if path_value.startswith("/"):
                normalized = normalize_internal_path(path_value)
                target = required_file_target(MIRROR_OUTPUT, normalized)
            else:
                target = required_file_target(html_file.parent, path_value)

            if not target.exists():
                raise SystemExit(f"Broken built link in {html_file}: {value} -> {target}")


def main() -> None:
    if not POST_MAP_PATH.exists():
        raise SystemExit(f"Missing post map: {POST_MAP_PATH}")
    if not ARCHIVE_DIR.exists():
        raise SystemExit(f"Missing archive directory: {ARCHIVE_DIR}")

    manifest = validate_metadata()
    validate_archive_assets(manifest)
    validate_readme_generation(load_post_map())
    validate_built_links()
    print(
        json.dumps(
            {
                "checked_posts": len(manifest),
                "checked_html_files": len(iter_built_html_files()),
                "path_prefix": normalize_path_prefix(PATH_PREFIX),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
