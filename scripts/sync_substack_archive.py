from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
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
ARCHIVE_PAGE_LIMIT = 50
MAX_ARCHIVE_PAGES = 1_000
COMPLETENESS_REPORT_PATH = ARCHIVE_DIR / "completeness_report.json"
USER_AGENT = "RootedLayersMirror/1.0 (+https://github.com/petroslamb/content)"
REMOTE_IMAGE_LINK = re.compile(r"\[\!\[([^\]]*)\]\((assets\/[^)]+)\)\]\((https?:\/\/[^)]+)\)")
LOCAL_ASSET_REFERENCE = re.compile(r"assets\/([A-Za-z0-9._-]+)")


@dataclass
class DiscoveryOutcome:
    posts: list[dict[str, str]]
    post_map: dict[str, dict[str, Any]]
    sources: dict[str, dict[str, Any]]

    @property
    def complete(self) -> bool:
        return all(bool(source.get("complete")) for source in self.sources.values())

    def as_report(self) -> dict[str, Any]:
        failures = [
            {
                "source": name,
                "error": source.get("error") or "source did not complete",
            }
            for name, source in self.sources.items()
            if not source.get("complete")
        ]
        return {
            "complete": self.complete,
            "unique_post_count": len(self.posts),
            "sources": self.sources,
            "failures": failures,
        }


def normalize_slug(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    return path.split("/")[-1]


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_error(exc: Exception) -> str:
    return f"{type(exc).__name__}: {exc}"


def discover_rss_posts(
    session: requests.Session,
    base_url: str,
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    rss_url = f"{base_url.rstrip('/')}{RSS_PATH}"
    discovered: dict[str, dict[str, str]] = {}
    report: dict[str, Any] = {
        "success": False,
        "complete": False,
        "item_count": 0,
        "error": None,
    }
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
    except (requests.RequestException, ET.ParseError, TypeError, ValueError) as exc:
        report["error"] = source_error(exc)
        report["item_count"] = len(discovered)
        return list(discovered.values()), report

    report["success"] = True
    report["complete"] = True
    report["item_count"] = len(discovered)
    return list(discovered.values()), report


def discover_archive_api_posts(
    session: requests.Session,
    base_url: str,
    *,
    page_limit: int = ARCHIVE_PAGE_LIMIT,
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    archive_url = f"{base_url.rstrip('/')}{ARCHIVE_API_PATH}"
    discovered: dict[str, dict[str, str]] = {}
    seen_page_fingerprints: set[tuple[str, ...]] = set()
    report: dict[str, Any] = {
        "success": False,
        "complete": False,
        "item_count": 0,
        "pages_fetched": 0,
        "termination": None,
        "error": None,
    }

    if page_limit <= 0:
        report["error"] = "page_limit must be positive"
        return [], report

    offset = 0
    for _ in range(MAX_ARCHIVE_PAGES):
        try:
            response = session.get(
                archive_url,
                params={"sort": "new", "search": "", "offset": offset, "limit": page_limit},
                timeout=30,
            )
            response.raise_for_status()
            page = response.json()
            if not isinstance(page, list):
                raise ValueError(f"Unexpected archive response shape at offset {offset}")

            normalized_page: list[dict[str, str]] = []
            for post in page:
                if not isinstance(post, dict) or not post.get("slug"):
                    raise ValueError(f"Archive entry at offset {offset} is missing a slug")
                slug = str(post["slug"])
                canonical_url = post.get("canonical_url") or f"{base_url.rstrip('/')}/p/{slug}"
                normalized_page.append(
                    {
                        "slug": slug,
                        "url": str(canonical_url),
                        "published_at": str(post.get("post_date") or ""),
                    }
                )
        except (requests.RequestException, TypeError, ValueError) as exc:
            report["error"] = source_error(exc)
            report["termination"] = "request_failed"
            break

        report["success"] = True
        report["pages_fetched"] += 1
        if not normalized_page:
            report["complete"] = True
            report["termination"] = "empty_page"
            break

        fingerprint = tuple(post["slug"] for post in normalized_page)
        if fingerprint in seen_page_fingerprints:
            report["error"] = f"Repeated archive page at offset {offset}; pagination did not advance"
            report["termination"] = "repeated_page"
            break
        seen_page_fingerprints.add(fingerprint)

        for post in normalized_page:
            discovered.setdefault(post["slug"], post)

        if len(normalized_page) < page_limit:
            report["complete"] = True
            report["termination"] = "short_page"
            break
        offset += page_limit
    else:
        report["error"] = f"Archive pagination exceeded {MAX_ARCHIVE_PAGES} pages"
        report["termination"] = "page_limit_exceeded"

    report["item_count"] = len(discovered)
    return list(discovered.values()), report


def published_post_map_posts(
    post_map: dict[str, dict[str, Any]],
    base_url: str,
) -> list[dict[str, str]]:
    return [
        {
            "slug": slug,
            "url": f"{base_url.rstrip('/')}/p/{slug}",
            "published_at": "",
        }
        for slug, entry in post_map.items()
        if entry.get("status") == "published"
    ]


def merge_discovered_posts(*sources: list[dict[str, str]]) -> list[dict[str, str]]:
    merged: dict[str, dict[str, str]] = {}
    for posts in sources:
        for post in posts:
            slug = post["slug"]
            if slug not in merged:
                merged[slug] = dict(post)
                continue
            for key in ("url", "published_at"):
                if not merged[slug].get(key) and post.get(key):
                    merged[slug][key] = post[key]
    return list(merged.values())


def discover_posts(
    session: requests.Session,
    base_url: str,
    *,
    post_map: dict[str, dict[str, Any]] | None = None,
    archive_page_limit: int = ARCHIVE_PAGE_LIMIT,
) -> DiscoveryOutcome:
    rss_posts, rss_report = discover_rss_posts(session, base_url)
    archive_posts, archive_report = discover_archive_api_posts(
        session,
        base_url,
        page_limit=archive_page_limit,
    )

    post_map_report: dict[str, Any] = {
        "success": False,
        "complete": False,
        "item_count": 0,
        "error": None,
    }
    resolved_post_map: dict[str, dict[str, Any]] = {}
    try:
        resolved_post_map = load_post_map() if post_map is None else post_map
        if not isinstance(resolved_post_map, dict):
            raise ValueError("Expected post_map to be a mapping")
        mapped_posts = published_post_map_posts(resolved_post_map, base_url)
        post_map_report["success"] = True
        post_map_report["complete"] = True
        post_map_report["item_count"] = len(mapped_posts)
    except Exception as exc:  # A local source failure must make cleanup fail closed.
        mapped_posts = []
        post_map_report["error"] = source_error(exc)

    posts = merge_discovered_posts(rss_posts, archive_posts, mapped_posts)
    return DiscoveryOutcome(
        posts=posts,
        post_map=resolved_post_map,
        sources={
            "rss": rss_report,
            "archive_api": archive_report,
            "post_map": post_map_report,
        },
    )


def merge_with_published_post_map(
    discovered_posts: list[dict[str, str]],
    post_map: dict[str, dict[str, Any]],
    base_url: str,
) -> list[dict[str, str]]:
    return merge_discovered_posts(
        discovered_posts,
        published_post_map_posts(post_map, base_url),
    )


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


def load_existing_manifest() -> tuple[dict[str, dict[str, Any]], str | None]:
    if not METADATA_PATH.exists():
        return {}, None
    try:
        raw_manifest = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
        if not isinstance(raw_manifest, list):
            raise ValueError("Expected metadata.json to contain a list")
        existing_manifest: dict[str, dict[str, Any]] = {}
        for entry in raw_manifest:
            if not isinstance(entry, dict):
                raise ValueError("Expected every metadata.json entry to be an object")
            slug = slug_from_manifest_entry(entry)
            if slug:
                existing_manifest[slug] = entry
        return existing_manifest, None
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        return {}, source_error(exc)


def sync_archive(base_url: str, output_dir: Path, summary_path: Path | None) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    assets_dir = output_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    discovery = discover_posts(session, base_url)
    discovered_posts = discovery.posts
    post_map = discovery.post_map
    existing_manifest, existing_manifest_error = load_existing_manifest()
    desired_assets: set[str] = set()
    expected_stems: set[str] = set()
    manifest: list[dict[str, Any]] = []
    updated_slugs: list[str] = []
    unchanged_slugs: list[str] = []
    missing_post_map: list[str] = []
    fetch_failures: list[dict[str, str]] = []
    excluded_non_public: list[dict[str, str]] = []

    seen_slugs: set[str] = set()
    for discovered in discovered_posts:
        slug = discovered["slug"]
        if slug in seen_slugs:
            continue
        seen_slugs.add(slug)
        try:
            post = fetch_post(session, base_url, slug)
        except Exception as exc:  # A per-post source failure must block cleanup.
            fetch_failures.append({"slug": slug, "error": source_error(exc)})
            continue
        audience = str(post.get("audience") or "").lower()
        if audience != "everyone":
            excluded_non_public.append({"slug": slug, "audience": audience or "unknown"})
            continue
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

    cleanup_blockers: list[str] = []
    if not discovery.complete:
        cleanup_blockers.append("discovery_incomplete")
    if fetch_failures:
        cleanup_blockers.append("post_fetch_incomplete")
    if existing_manifest_error:
        cleanup_blockers.append("existing_manifest_unreadable")
    has_existing_post_files = any(output_dir.glob("*.md")) or any(output_dir.glob("*.html"))
    if not discovered_posts and (existing_manifest or has_existing_post_files):
        cleanup_blockers.append("empty_discovery_against_existing_archive")
    cleanup_performed = not cleanup_blockers

    preserved_manifest_slugs: list[str] = []
    if not cleanup_performed:
        manifest_slugs = {str(entry.get("slug") or "") for entry in manifest}
        for slug, entry in existing_manifest.items():
            if slug in manifest_slugs:
                continue
            manifest.append(entry)
            preserved_manifest_slugs.append(slug)

    manifest.sort(key=lambda item: str(item.get("post_date") or ""), reverse=True)
    if cleanup_performed:
        removed_files = cleanup_stale_post_files(output_dir, expected_stems)
        removed_assets = cleanup_stale_assets(assets_dir, desired_assets)
    else:
        removed_files = []
        removed_assets = []

    metadata_content = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    write_text_if_changed(METADATA_PATH, metadata_content)
    post_map_complete = bool(discovery.sources["post_map"].get("complete"))
    if post_map_complete:
        write_readme_publication_map(post_map)

    discovery_report = discovery.as_report()
    source_failures = list(discovery_report["failures"])
    source_failures.extend(
        {
            "source": f"post:{failure['slug']}",
            "error": failure["error"],
        }
        for failure in fetch_failures
    )
    if existing_manifest_error:
        source_failures.append(
            {"source": "existing_manifest", "error": existing_manifest_error}
        )
    summary = {
        "generated_at": iso_now(),
        "base_url": base_url,
        "complete": not cleanup_blockers,
        "inventory_scope": "public_substack_posts_only",
        "discovered_count": len(discovered_posts),
        "discovery": discovery_report,
        "source_failures": source_failures,
        "post_fetch_failures": fetch_failures,
        "excluded_non_public": excluded_non_public,
        "manifest_count": len(manifest),
        "updated_slugs": updated_slugs,
        "unchanged_slugs": unchanged_slugs,
        "removed_files": removed_files,
        "removed_assets": removed_assets,
        "prune_allowed": cleanup_performed,
        "cleanup": {
            "performed": cleanup_performed,
            "blockers": cleanup_blockers,
        },
        "existing_manifest_error": existing_manifest_error,
        "preserved_manifest_slugs": sorted(preserved_manifest_slugs),
        "readme_publication_map_refreshed": post_map_complete,
        "missing_post_map": sorted(missing_post_map),
        "mirror_enabled_count": sum(1 for item in manifest if item.get("mirror_enabled")),
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
        default=str(COMPLETENESS_REPORT_PATH),
        help="Path for the machine-readable completeness report",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary_path = Path(args.summary_path).resolve() if args.summary_path else None
    summary = sync_archive(args.base_url, Path(args.output_dir).resolve(), summary_path)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if not summary.get("complete"):
        raise SystemExit("Substack refresh is incomplete; archive cleanup remained fail-closed.")


if __name__ == "__main__":
    main()
