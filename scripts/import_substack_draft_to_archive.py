#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import substack
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt

from archive_utils import ARCHIVE_DIR, METADATA_PATH, REPO_ROOT, load_post_map, write_readme_publication_map
from sync_substack_archive import render_html_snapshot, write_text_if_changed

DEFAULT_COOKIE_PATH = Path("/tmp/substack_cookie_string.txt")
PUBLICATION_URL = "https://lambpetros.substack.com"
LOCAL_IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_IMAGE_PATTERN = re.compile(r'(<img[^>]+src=")([^"]+)(")')
MD = MarkdownIt()


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_cookie_string(path: Path) -> str:
    cookie = path.read_text(encoding="utf-8").strip()
    if not cookie:
        raise SystemExit(f"Cookie file is empty: {path}")
    return cookie


def load_metadata() -> list[dict]:
    if not METADATA_PATH.exists():
        return []
    return json.loads(METADATA_PATH.read_text(encoding="utf-8"))


def save_metadata(entries: list[dict]) -> None:
    entries.sort(key=lambda item: item["post_date"], reverse=True)
    METADATA_PATH.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def localized_asset_name(source_path: Path) -> str:
    digest = hashlib.sha256(str(source_path.resolve()).encode("utf-8")).hexdigest()[:16]
    return f"asset-{digest}{source_path.suffix.lower()}"


def copy_local_assets(markdown_text: str, markdown_path: Path, assets_dir: Path) -> tuple[str, list[str]]:
    copied_assets: list[str] = []

    def replace_markdown(match: re.Match[str]) -> str:
        alt_text, target = match.groups()
        if re.match(r"^[a-z]+://", target):
            return match.group(0)
        source_path = (markdown_path.parent / target).resolve()
        if not source_path.exists() or not source_path.is_file():
            return match.group(0)
        filename = localized_asset_name(source_path)
        shutil.copy2(source_path, assets_dir / filename)
        copied_assets.append(filename)
        escaped_alt = alt_text.replace("]", "\\]")
        return f"![{escaped_alt}](assets/{filename})"

    localized = LOCAL_IMAGE_PATTERN.sub(replace_markdown, markdown_text)

    def replace_html(match: re.Match[str]) -> str:
        prefix, target, suffix = match.groups()
        if re.match(r"^[a-z]+://", target):
            return match.group(0)
        source_path = (markdown_path.parent / target).resolve()
        if not source_path.exists() or not source_path.is_file():
            return match.group(0)
        filename = localized_asset_name(source_path)
        shutil.copy2(source_path, assets_dir / filename)
        copied_assets.append(filename)
        return f'{prefix}assets/{quote(filename)}{suffix}'

    localized = HTML_IMAGE_PATTERN.sub(replace_html, localized)
    return localized, sorted(set(copied_assets))


def content_hash(draft: dict, localized_markdown: str, canonical_url: str) -> str:
    payload = {
        "id": draft.get("id"),
        "title": draft.get("draft_title") or draft.get("title"),
        "slug": draft.get("slug"),
        "canonical_url": canonical_url,
        "post_date": draft.get("post_date"),
        "draft_updated_at": draft.get("draft_updated_at"),
        "is_published": draft.get("is_published"),
        "markdown": localized_markdown,
    }
    serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def import_draft(args: argparse.Namespace) -> None:
    cookie = load_cookie_string(Path(args.cookie_path))
    api = substack.Api(cookies_string=cookie, publication_url=args.publication_url)
    draft = api.get_draft(args.post_id)

    title = draft.get("draft_title") or draft.get("title")
    slug = draft.get("slug")
    post_date = str(draft.get("post_date") or iso_now()).split("T")[0]
    canonical_url = f"{args.publication_url.rstrip('/')}/p/{slug}"
    markdown_path = (REPO_ROOT / args.markdown).resolve()
    markdown_body = markdown_path.read_text(encoding="utf-8").strip() + "\n"

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    assets_dir = ARCHIVE_DIR / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    localized_markdown, _copied_assets = copy_local_assets(markdown_body, markdown_path, assets_dir)

    filename_stem = f"{post_date}_{slug}"
    md_relative = Path("publication_strategy_and_archive") / "substack_archive" / f"{filename_stem}.md"
    html_relative = Path("publication_strategy_and_archive") / "substack_archive" / f"{filename_stem}.html"
    md_path = REPO_ROOT / md_relative
    html_path = REPO_ROOT / html_relative

    archive_markdown = f"# {title}\n\nDate: {post_date}\nURL: {canonical_url}\n\n{localized_markdown.strip()}\n"
    html_body = MD.render(localized_markdown)
    soup = BeautifulSoup(html_body, "html.parser")
    archive_html = render_html_snapshot(title, post_date, canonical_url, soup)

    write_text_if_changed(md_path, archive_markdown)
    write_text_if_changed(html_path, archive_html)

    metadata = load_metadata()
    metadata = [entry for entry in metadata if entry.get("slug") != slug]
    metadata.append(
        {
            "slug": slug,
            "title": title,
            "url": canonical_url,
            "post_date": draft.get("post_date") or iso_now(),
            "audience": draft.get("audience"),
            "fetched_at": iso_now(),
            "content_hash": content_hash(draft, localized_markdown, canonical_url),
            "md_path": md_relative.as_posix(),
            "html_path": html_relative.as_posix(),
            "hero_image": None,
            "mirror_enabled": bool(draft.get("is_published")) and draft.get("audience") == "everyone",
        }
    )
    save_metadata(metadata)
    write_readme_publication_map(load_post_map())

    print(f"Imported draft {args.post_id} -> {md_relative}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import an unpublished Substack draft into the tracked archive.")
    parser.add_argument("--post-id", required=True, type=int)
    parser.add_argument("--markdown", required=True, help="Canonical local markdown path relative to the repo root")
    parser.add_argument("--publication-url", default=PUBLICATION_URL)
    parser.add_argument("--cookie-path", default=str(DEFAULT_COOKIE_PATH))
    return parser.parse_args()


if __name__ == "__main__":
    import_draft(parse_args())
