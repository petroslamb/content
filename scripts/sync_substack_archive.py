from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify

from archive_utils import ARCHIVE_DIR, METADATA_PATH, load_post_map, write_readme_publication_map

BASE_URL = "https://lambpetros.substack.com"
RSS_PATH = "/feed"
ARCHIVE_API_PATH = "/api/v1/archive"
POST_API_PATH = "/api/v1/posts/{slug}"
USER_AGENT = "RootedLayersMirror/1.0 (+https://github.com/petroslamb/content)"
REMOTE_IMAGE_LINK = re.compile(r"\[\!\[([^\]]*)\]\((assets\/[^)]+)\)\]\((https?:\/\/[^)]+)\)")
LOCAL_ASSET_REFERENCE = re.compile(r"assets\/([A-Za-z0-9._-]+)")


def normalize_slug(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    return path.split("/")[-1]


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def discover_posts(session: requests.Session, base_url: str) -> list[dict[str, str]]:
    rss_url = f"{base_url.rstrip('/')}{RSS_PATH}"
    discovered: dict[str, dict[str, str]] = {}
    try:
        response = session.get(rss_url, timeout=30)
        response.raise_for_status()
        root = ET.fromstring(response.text)
        for item in root.findall("./channel/item"):
            link = item.findtext("link", "").strip()
            if not link or "/p/" not in link:
                continue
            slug = normalize_slug(link)
            pub_date = item.findtext("pubDate", "").strip()
            published_at = ""
            if pub_date:
                published_at = parsedate_to_datetime(pub_date).astimezone(timezone.utc).isoformat()
            discovered[slug] = {
                "slug": slug,
                "url": link,
                "published_at": published_at,
            }
    except (requests.RequestException, ET.ParseError):
        discovered = {}
    if discovered:
        return list(discovered.values())

    archive_url = f"{base_url.rstrip('/')}{ARCHIVE_API_PATH}"
    response = session.get(
        archive_url,
        params={"sort": "new", "search": "", "offset": 0, "limit": 50},
        timeout=30,
    )
    response.raise_for_status()
    posts = response.json()
    fallback: list[dict[str, str]] = []
    for post in posts:
        canonical_url = post.get("canonical_url") or f"{base_url.rstrip('/')}/p/{post['slug']}"
        fallback.append(
            {
                "slug": post["slug"],
                "url": canonical_url,
                "published_at": post.get("post_date", ""),
            }
        )
    return fallback


def fetch_post(session: requests.Session, base_url: str, slug: str) -> dict[str, Any]:
    url = f"{base_url.rstrip('/')}{POST_API_PATH.format(slug=slug)}"
    response = session.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, dict):
        raise ValueError(f"Unexpected response shape for slug '{slug}'")
    return data


def slug_from_manifest_entry(entry: dict[str, Any]) -> str | None:
    if entry.get("slug"):
        return str(entry["slug"])
    if entry.get("url"):
        return normalize_slug(str(entry["url"]))
    md_path = entry.get("md_path")
    if md_path:
        stem = Path(str(md_path)).stem
        if "_" in stem:
            return stem.split("_", 1)[1]
    return None


def extension_for_url(url: str, content_type: str | None) -> str:
    parsed_path = urlparse(url).path
    suffix = Path(parsed_path).suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}:
        return suffix
    if content_type:
        guessed = mimetypes.guess_extension(content_type.split(";")[0].strip())
        if guessed:
            if guessed == ".jpe":
                return ".jpg"
            return guessed
    return ".bin"


def download_asset(
    session: requests.Session,
    assets_dir: Path,
    original_url: str,
    base_url: str,
    desired_assets: set[str],
) -> str | None:
    if not original_url:
        return None
    resolved_url = urljoin(base_url.rstrip("/") + "/", original_url)
    digest = hashlib.sha256(resolved_url.encode("utf-8")).hexdigest()[:16]
    temp_ext = Path(urlparse(resolved_url).path).suffix.lower()
    temp_name = f"asset-{digest}{temp_ext or ''}"

    existing_matches = list(assets_dir.glob(f"asset-{digest}.*"))
    if existing_matches:
        desired_assets.add(existing_matches[0].name)
        return f"assets/{existing_matches[0].name}"

    response = session.get(resolved_url, timeout=30)
    response.raise_for_status()
    extension = extension_for_url(resolved_url, response.headers.get("Content-Type"))
    filename = f"asset-{digest}{extension}"
    target = assets_dir / filename
    target.write_bytes(response.content)
    desired_assets.add(filename)
    return f"assets/{filename}"


def localize_rich_media(
    session: requests.Session,
    post: dict[str, Any],
    assets_dir: Path,
    base_url: str,
    desired_assets: set[str],
) -> tuple[BeautifulSoup, str | None]:
    soup = BeautifulSoup(post.get("body_html") or "", "html.parser")
    hero_local = None
    hero_candidates = [
        post.get("hero_image"),
        post.get("cover_image"),
        post.get("podcast_episode_image_url"),
        post.get("podcast_art_url"),
    ]

    for img in soup.find_all("img"):
        source = img.get("src")
        if not source:
            continue
        local_path = download_asset(session, assets_dir, source, base_url, desired_assets)
        if not local_path:
            continue
        if hero_local is None:
            hero_local = local_path
        img["src"] = local_path
        if img.has_attr("srcset"):
            del img["srcset"]
        parent = img.parent
        if getattr(parent, "name", None) == "a" and parent.get("href", "").startswith("http"):
            parent["href"] = local_path

    if hero_local is None:
        for candidate in hero_candidates:
            if not candidate:
                continue
            hero_local = download_asset(session, assets_dir, candidate, base_url, desired_assets)
            if hero_local:
                break

    for link in soup.find_all("a"):
        href = link.get("href", "")
        if href.startswith("/") and not href.startswith("//"):
            link["href"] = urljoin(base_url.rstrip("/") + "/", href)

    return soup, hero_local


def render_html_snapshot(title: str, post_date: str, canonical_url: str, soup: BeautifulSoup) -> str:
    styles = """
<style>
body {
  margin: 0;
  background: #f6f1e7;
  color: #1f1a14;
  font-family: "IBM Plex Sans", "Avenir Next", sans-serif;
}
main {
  max-width: 820px;
  margin: 0 auto;
  padding: 48px 24px 72px;
}
h1 {
  font-family: "Iowan Old Style", "Palatino Linotype", serif;
  font-size: clamp(2.3rem, 3vw, 3.7rem);
  line-height: 1.05;
  margin-bottom: 0.4em;
}
.meta {
  color: #5f5548;
  font-size: 0.95rem;
  margin-bottom: 2rem;
}
img {
  display: block;
  max-width: 100%;
  height: auto;
  margin: 1.5rem auto;
  border-radius: 16px;
}
a {
  color: #1f4b6e;
}
pre, code {
  font-family: "IBM Plex Mono", monospace;
}
blockquote {
  margin: 1.8rem 0;
  padding-left: 1rem;
  border-left: 3px solid #b07a44;
  color: #5f5548;
}
</style>
""".strip()
    return (
        "<!doctype html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "  <meta charset=\"utf-8\">\n"
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        f"  <title>{title}</title>\n"
        f"{styles}\n"
        "</head>\n"
        "<body>\n"
        "  <main>\n"
        f"    <h1>{title}</h1>\n"
        f"    <p class=\"meta\">Published {post_date} · <a href=\"{canonical_url}\">Read on Substack</a></p>\n"
        f"    {soup}\n"
        "  </main>\n"
        "</body>\n"
        "</html>\n"
    )


def clean_markdown(markdown: str) -> str:
    markdown = markdown.replace("\r\n", "\n")
    markdown = REMOTE_IMAGE_LINK.sub(r"![\1](\2)", markdown)
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    return markdown.strip() + "\n"


def render_markdown_snapshot(
    title: str,
    post_date: str,
    canonical_url: str,
    soup: BeautifulSoup,
) -> str:
    markdown_body = markdownify(
        str(soup),
        heading_style="ATX",
        bullets="-",
        escape_underscores=False,
    )
    return clean_markdown(
        f"# {title}\n\nDate: {post_date}\nURL: {canonical_url}\n\n{markdown_body}"
    )


def compute_content_hash(post: dict[str, Any]) -> str:
    payload = {
        "title": post.get("title"),
        "subtitle": post.get("subtitle"),
        "description": post.get("description"),
        "canonical_url": post.get("canonical_url"),
        "post_date": post.get("post_date"),
        "updated_at": post.get("updated_at"),
        "audience": post.get("audience"),
        "cover_image": post.get("cover_image"),
        "hero_image": post.get("hero_image"),
        "body_html": post.get("body_html"),
    }
    serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def write_text_if_changed(path: Path, content: str) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def collect_markdown_assets(markdown_path: Path) -> set[str]:
    if not markdown_path.exists():
        return set()
    content = markdown_path.read_text(encoding="utf-8")
    return set(LOCAL_ASSET_REFERENCE.findall(content))


def has_missing_markdown_assets(markdown_path: Path, assets_dir: Path) -> bool:
    return any(not (assets_dir / asset_name).exists() for asset_name in collect_markdown_assets(markdown_path))


def cleanup_stale_post_files(output_dir: Path, expected_stems: set[str]) -> list[str]:
    removed: list[str] = []
    for candidate in output_dir.glob("*"):
        if candidate.is_dir():
            continue
        if candidate.name == ".DS_Store":
            candidate.unlink()
            removed.append(candidate.name)
            continue
        if candidate.suffix.lower() not in {".md", ".html"}:
            continue
        if candidate.stem not in expected_stems:
            candidate.unlink()
            removed.append(candidate.name)
    return removed


def cleanup_stale_assets(assets_dir: Path, desired_assets: set[str]) -> list[str]:
    removed: list[str] = []
    for candidate in assets_dir.iterdir():
        if candidate.is_dir():
            continue
        if candidate.name == ".DS_Store" or candidate.name not in desired_assets:
            candidate.unlink()
            removed.append(candidate.name)
    return removed


def sync_archive(base_url: str, output_dir: Path, summary_path: Path | None) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    assets_dir = output_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    discovered_posts = discover_posts(session, base_url)
    existing_manifest = {}
    if METADATA_PATH.exists():
        try:
            for entry in json.loads(METADATA_PATH.read_text(encoding="utf-8")):
                slug = slug_from_manifest_entry(entry)
                if slug:
                    existing_manifest[slug] = entry
        except json.JSONDecodeError:
            existing_manifest = {}

    post_map = load_post_map()
    desired_assets: set[str] = set()
    expected_stems: set[str] = set()
    manifest: list[dict[str, Any]] = []
    updated_slugs: list[str] = []
    unchanged_slugs: list[str] = []
    missing_post_map: list[str] = []

    seen_slugs: set[str] = set()
    for discovered in discovered_posts:
        slug = discovered["slug"]
        if slug in seen_slugs:
            continue
        seen_slugs.add(slug)
        post = fetch_post(session, base_url, slug)
        content_hash = compute_content_hash(post)
        post_date = (post.get("post_date") or discovered["published_at"]).split("T")[0]
        canonical_url = post.get("canonical_url") or discovered["url"]
        filename_stem = f"{post_date}_{slug}"
        expected_stems.add(filename_stem)
        md_relative = Path("publication_strategy_and_archive") / "substack_archive" / f"{filename_stem}.md"
        html_relative = Path("publication_strategy_and_archive") / "substack_archive" / f"{filename_stem}.html"
        md_path = output_dir / f"{filename_stem}.md"
        html_path = output_dir / f"{filename_stem}.html"

        existing = existing_manifest.get(slug)
        files_exist = md_path.exists() and html_path.exists()
        needs_render = (
            not files_exist
            or not existing
            or existing.get("content_hash") != content_hash
            or has_missing_markdown_assets(md_path, assets_dir)
        )

        hero_local = existing.get("hero_image") if existing else None
        if needs_render:
            soup, localized_hero = localize_rich_media(session, post, assets_dir, base_url, desired_assets)
            hero_local = (
                str(
                    Path("publication_strategy_and_archive")
                    / "substack_archive"
                    / localized_hero
                )
                if localized_hero
                else None
            )
            html_changed = write_text_if_changed(
                html_path,
                render_html_snapshot(post["title"], post_date, canonical_url, soup),
            )
            md_changed = write_text_if_changed(
                md_path,
                render_markdown_snapshot(post["title"], post_date, canonical_url, soup),
            )
            if html_changed or md_changed or not existing:
                updated_slugs.append(slug)
        else:
            if hero_local:
                desired_assets.add(Path(hero_local).name)
            desired_assets.update(collect_markdown_assets(md_path))
            unchanged_slugs.append(slug)

        if slug not in post_map:
            missing_post_map.append(slug)

        manifest.append(
            {
                "slug": slug,
                "title": post.get("title"),
                "url": canonical_url,
                "post_date": post.get("post_date") or discovered["published_at"],
                "audience": post.get("audience"),
                "fetched_at": iso_now() if needs_render or not existing else existing.get("fetched_at", iso_now()),
                "content_hash": content_hash,
                "md_path": md_relative.as_posix(),
                "html_path": html_relative.as_posix(),
                "hero_image": hero_local,
                "mirror_enabled": post.get("audience") == "everyone" and md_path.exists() and html_path.exists(),
            }
        )

    manifest.sort(key=lambda item: item["post_date"], reverse=True)
    removed_files = cleanup_stale_post_files(output_dir, expected_stems)
    removed_assets = cleanup_stale_assets(assets_dir, desired_assets)

    metadata_content = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    write_text_if_changed(METADATA_PATH, metadata_content)
    write_readme_publication_map(post_map)

    summary = {
        "generated_at": iso_now(),
        "base_url": base_url,
        "discovered_count": len(discovered_posts),
        "manifest_count": len(manifest),
        "updated_slugs": updated_slugs,
        "unchanged_slugs": unchanged_slugs,
        "removed_files": removed_files,
        "removed_assets": removed_assets,
        "missing_post_map": sorted(missing_post_map),
        "mirror_enabled_count": sum(1 for item in manifest if item["mirror_enabled"]),
    }
    if summary_path:
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync public Substack posts into the tracked archive.")
    parser.add_argument("--base-url", default=BASE_URL, help="Publication base URL")
    parser.add_argument(
        "--output-dir",
        default=str(ARCHIVE_DIR),
        help="Target archive directory",
    )
    parser.add_argument(
        "--summary-path",
        default="",
        help="Optional path for a machine-readable sync summary",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary_path = Path(args.summary_path).resolve() if args.summary_path else None
    summary = sync_archive(args.base_url, Path(args.output_dir).resolve(), summary_path)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
