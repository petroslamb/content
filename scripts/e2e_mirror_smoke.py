from __future__ import annotations

import contextlib
import json
import os
import socket
import tempfile
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from archive_utils import METADATA_PATH, load_post_map
from check_mirror import (
    AI_DISCLOSURE,
    PROFESSIONAL_PROFILE_URL,
    load_and_validate_portfolio_manifest,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
MIRROR_OUTPUT = REPO_ROOT / "publication_strategy_and_archive" / "mirror" / "_site"


def normalize_path_prefix(raw: str) -> str:
    if not raw or raw == "/":
        return "/"
    return f"/{raw.strip('/')}/"


def with_prefix(path_prefix: str, route_path: str) -> str:
    normalized = route_path if route_path.startswith("/") else f"/{route_path}"
    if path_prefix == "/":
        return normalized
    return f"{path_prefix.rstrip('/')}{normalized}"


def expected_site_root(path_prefix: str) -> str:
    site_url = (os.environ.get("MIRROR_SITE_URL") or "https://petroslamb.github.io/content").rstrip("/")
    site_path = urlparse(site_url).path or "/"
    if site_path != "/":
        return normalize_path_prefix(site_path)
    return path_prefix


def normalized_internal_route(path_prefix: str, route_path: str) -> str:
    normalized = route_path if route_path.startswith("/") else f"/{route_path}"
    for prefix in (path_prefix, expected_site_root(path_prefix)):
        if prefix != "/" and normalized.startswith(prefix):
            return "/" + normalized[len(prefix) :].lstrip("/")
    return normalized


def first_mirrored_post() -> dict[str, object]:
    manifest = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    post_map = load_post_map()
    for entry in manifest:
        if entry.get("mirror_enabled"):
            mapped = post_map.get(str(entry["slug"]), {})
            merged = dict(entry)
            if mapped.get("title"):
                merged["title"] = mapped["title"]
            return merged
    raise SystemExit("No mirrored posts found in metadata.json")


def mirrored_posts() -> list[dict[str, object]]:
    manifest = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    return [entry for entry in manifest if entry.get("mirror_enabled")]


@contextlib.contextmanager
def server_root_for_prefix(path_prefix: str):
    if path_prefix == "/":
        yield MIRROR_OUTPUT
        return

    with tempfile.TemporaryDirectory(prefix="mirror-e2e-") as temp_dir:
        temp_root = Path(temp_dir)
        mount_target = temp_root / path_prefix.strip("/")
        mount_target.parent.mkdir(parents=True, exist_ok=True)
        os.symlink(MIRROR_OUTPUT, mount_target, target_is_directory=True)
        yield temp_root


@contextlib.contextmanager
def serve_directory(root: Path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]

    handler = partial(SimpleHTTPRequestHandler, directory=str(root))
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def assert_ok(response: requests.Response, label: str) -> None:
    if response.status_code != 200:
        raise SystemExit(f"{label} returned {response.status_code}: {response.url}")


def main() -> None:
    if not MIRROR_OUTPUT.exists():
        raise SystemExit("Mirror output is missing. Run npm run build:mirror first.")

    path_prefix = normalize_path_prefix(os.environ.get("ELEVENTY_PATH_PREFIX", "/").strip())
    post = first_mirrored_post()
    public_mirror_posts = mirrored_posts()
    portfolio = load_and_validate_portfolio_manifest(public_mirror_posts)
    slug = str(post["slug"])
    title = str(post["title"])
    expected_root_path = expected_site_root(path_prefix)

    with server_root_for_prefix(path_prefix) as serve_root, serve_directory(serve_root) as origin:
        homepage_path = with_prefix(path_prefix, "/")
        archive_path = with_prefix(path_prefix, "/archive/")
        atlas_path = with_prefix(path_prefix, "/editorial-atlas/")
        post_path = with_prefix(path_prefix, f"/posts/{slug}/")
        feed_path = with_prefix(path_prefix, "/feed.xml")

        homepage = requests.get(f"{origin}{homepage_path}", timeout=10)
        archive = requests.get(f"{origin}{archive_path}", timeout=10)
        atlas_page = requests.get(f"{origin}{atlas_path}", timeout=10)
        post_page = requests.get(f"{origin}{post_path}", timeout=10)
        feed = requests.get(f"{origin}{feed_path}", timeout=10)

        assert_ok(homepage, "Homepage")
        assert_ok(archive, "Archive page")
        assert_ok(atlas_page, "Editorial atlas page")
        assert_ok(post_page, "Post page")
        assert_ok(feed, "Feed")

        soup = BeautifulSoup(homepage.text, "html.parser")
        canonical = soup.find("link", rel="canonical")
        if canonical is None or not canonical.get("href"):
            raise SystemExit("Homepage is missing a canonical link")
        canonical_path = urlparse(canonical["href"]).path or "/"
        if canonical_path != expected_root_path:
            raise SystemExit(
                f"Homepage canonical path mismatch: expected {expected_root_path}, got {canonical_path}"
            )

        archive_link = None
        atlas_link = None
        professional_profile_link = None
        for anchor in soup.find_all("a", href=True):
            parsed_path = normalized_internal_route(path_prefix, urlparse(anchor["href"]).path)
            if parsed_path == "/archive/":
                archive_link = anchor
            if parsed_path == "/editorial-atlas/":
                atlas_link = anchor
            if (
                anchor["href"] == PROFESSIONAL_PROFILE_URL
                and anchor.get_text(" ", strip=True) == "Professional profile"
            ):
                professional_profile_link = anchor
        if archive_link is None:
            raise SystemExit("Homepage is missing the archive navigation link")
        if atlas_link is not None:
            raise SystemExit("Homepage must not link to the editorial atlas")
        if professional_profile_link is None:
            raise SystemExit("Homepage is missing the Professional profile CTA")
        if AI_DISCLOSURE not in soup.get_text(" ", strip=True):
            raise SystemExit("Homepage is missing the exact AI assistance disclosure")

        expected_by_tier = portfolio["expected"]
        assert isinstance(expected_by_tier, dict)
        for tier in ("FLAGSHIP", "SUPPORTING"):
            cards = soup.select(f'[data-portfolio-tier="{tier}"]')
            expected_items = expected_by_tier[tier]
            rendered_ids = [card.get("data-portfolio-artifact") for card in cards]
            expected_ids = [item["artifact_id"] for item in expected_items]
            if rendered_ids != expected_ids:
                raise SystemExit(
                    f"Homepage {tier.lower()} cards do not match the manifest: "
                    f"expected {expected_ids}, got {rendered_ids}"
                )
            for card, expected_item in zip(cards, expected_items, strict=True):
                links = {anchor.get("href") for anchor in card.find_all("a", href=True)}
                if expected_item["url"] not in links:
                    raise SystemExit(
                        f"Portfolio card does not reach canonical essay: "
                        f"{expected_item['artifact_id']}"
                    )

        archive_soup = BeautifulSoup(archive.text, "html.parser")
        archive_text = archive_soup.get_text(" ", strip=True)
        if title not in archive_text:
            raise SystemExit(f"Archive page does not contain mirrored post title: {title}")
        archive_cards = archive_soup.select("[data-post-card]")
        if len(archive_cards) != len(public_mirror_posts):
            raise SystemExit(
                "Archive page does not preserve every public mirrored essay: "
                f"expected {len(public_mirror_posts)}, got {len(archive_cards)}"
            )

        atlas_soup = BeautifulSoup(atlas_page.text, "html.parser")
        atlas_text = atlas_soup.get_text(" ", strip=True)
        if "Published essays as a navigable editorial system" not in atlas_text:
            raise SystemExit("Editorial atlas page is missing the expected page heading")
        expected_tabs = {"overview", "compare", "moves"}
        found_tabs = {
            button.get("data-tab")
            for button in atlas_soup.select(".atlas-tab-btn[data-tab]")
            if button.get("data-tab")
        }
        if not expected_tabs.issubset(found_tabs):
            raise SystemExit(
                "Editorial atlas page is missing the expected tab labels "
                f"(found {sorted(found_tabs)})"
            )

        post_soup = BeautifulSoup(post_page.text, "html.parser")
        if "Read on Substack" not in post_soup.get_text(" ", strip=True):
            raise SystemExit(f"Post page for {slug} is missing the Substack source link")

        if "<rss" not in feed.text:
            raise SystemExit("Feed output is not valid RSS")

    print(
        json.dumps(
            {
                "smoke_tested_slug": slug,
                "path_prefix": path_prefix,
                "checked_routes": [
                    homepage_path,
                    archive_path,
                    atlas_path,
                    post_path,
                    feed_path,
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
