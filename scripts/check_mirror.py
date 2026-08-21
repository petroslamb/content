from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.parse import urlparse

import yaml
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
from editorial_atlas_utils import (
    ATLAS_DATA_PATH as GENERATED_ATLAS_DATA_PATH,
    EDITORIAL_ATLAS_DIR,
    ensure_checked_in_atlas_matches_generated,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
MIRROR_OUTPUT = REPO_ROOT / "publication_strategy_and_archive" / "mirror" / "_site"
PORTFOLIO_MANIFEST_PATH = Path(
    os.environ.get(
        "PORTFOLIO_MANIFEST_PATH",
        REPO_ROOT
        / "publication_strategy_and_archive"
        / "portfolio"
        / "portfolio_manifest.yaml",
    )
)
EDITORIAL_ATLAS_DATA_PATH = GENERATED_ATLAS_DATA_PATH
PATH_PREFIX = os.environ.get("ELEVENTY_PATH_PREFIX", "/").strip()
SITE_URL = os.environ.get("MIRROR_SITE_URL", "https://petroslamb.github.io/content").rstrip("/")
PROFESSIONAL_PROFILE_URL = "https://petroslamb.github.io/peterlamb/"
AI_DISCLOSURE = (
    "Rooted Layers is a historical archive of research and engineering work "
    "developed with AI-assisted research, drafting, and media workflows. The "
    "selected pieces are highlighted for their technical arguments, source "
    "trails, and documented engineering contribution."
)


def normalize_path_prefix(raw: str) -> str:
    if not raw or raw == "/":
        return "/"
    return f"/{raw.strip('/')}/"


def configured_site_path_prefix() -> str:
    site_path = urlparse(SITE_URL).path or "/"
    return normalize_path_prefix(site_path)


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


def load_and_validate_portfolio_manifest(
    metadata: list[dict[str, str]],
) -> dict[str, object]:
    if not PORTFOLIO_MANIFEST_PATH.exists():
        raise SystemExit(
            f"Missing portfolio manifest: {PORTFOLIO_MANIFEST_PATH}. "
            "Generate the reviewed decision layer before building the mirror."
        )

    portfolio = yaml.safe_load(PORTFOLIO_MANIFEST_PATH.read_text(encoding="utf-8")) or {}
    if portfolio.get("professional_profile_url") != PROFESSIONAL_PROFILE_URL:
        raise SystemExit(
            "Portfolio manifest professional_profile_url must equal "
            f"{PROFESSIONAL_PROFILE_URL}"
        )
    if portfolio.get("ai_disclosure") != AI_DISCLOSURE:
        raise SystemExit("Portfolio manifest does not contain the exact AI disclosure")

    homepage = portfolio.get("homepage")
    artifacts = portfolio.get("artifacts")
    if not isinstance(homepage, dict):
        raise SystemExit("Portfolio manifest homepage must be an object")
    if not isinstance(artifacts, list):
        raise SystemExit("Portfolio manifest artifacts must be a list")

    artifacts_by_id: dict[str, dict[str, object]] = {}
    for artifact in artifacts:
        if not isinstance(artifact, dict) or not artifact.get("artifact_id"):
            raise SystemExit("Every portfolio artifact must have an artifact_id")
        artifact_id = str(artifact["artifact_id"])
        if artifact_id in artifacts_by_id:
            raise SystemExit(f"Duplicate portfolio artifact_id: {artifact_id}")
        artifacts_by_id[artifact_id] = artifact

    metadata_by_slug = {str(entry["slug"]): entry for entry in metadata}
    post_map = load_post_map()
    selected_ids: set[str] = set()
    expected: dict[str, list[dict[str, object]]] = {
        "FLAGSHIP": [],
        "SUPPORTING": [],
    }
    for tier, key in (
        ("FLAGSHIP", "flagship_artifact_ids"),
        ("SUPPORTING", "supporting_artifact_ids"),
    ):
        artifact_ids = homepage.get(key, [])
        if not isinstance(artifact_ids, list):
            raise SystemExit(f"Portfolio homepage.{key} must be a list")
        if len(artifact_ids) > 4:
            raise SystemExit(f"Portfolio homepage exceeds four {tier.lower()} essays")
        if len(set(artifact_ids)) != len(artifact_ids):
            raise SystemExit(f"Portfolio homepage.{key} contains duplicate ids")

        for order, raw_artifact_id in enumerate(artifact_ids, start=1):
            artifact_id = str(raw_artifact_id)
            if artifact_id in selected_ids:
                raise SystemExit(
                    f"Portfolio artifact appears in more than one homepage tier: {artifact_id}"
                )
            selected_ids.add(artifact_id)
            artifact = artifacts_by_id.get(artifact_id)
            if artifact is None:
                raise SystemExit(
                    f"Portfolio homepage references unknown artifact: {artifact_id}"
                )
            if artifact.get("platform") != "SUBSTACK":
                raise SystemExit(
                    f"Portfolio homepage artifact must be SUBSTACK: {artifact_id}"
                )
            if artifact.get("selection_tier") != tier:
                raise SystemExit(
                    f"Portfolio homepage artifact {artifact_id} must be tier {tier}"
                )
            placement = artifact.get("homepage") or {}
            if not isinstance(placement, dict):
                raise SystemExit(f"Portfolio artifact homepage must be an object: {artifact_id}")
            if placement.get("section") != tier or placement.get("order") != order:
                raise SystemExit(
                    f"Portfolio homepage order disagrees with artifact placement: {artifact_id}"
                )

            slug = str(artifact.get("platform_id") or "")
            post = metadata_by_slug.get(slug)
            if post is None or not post.get("mirror_enabled"):
                raise SystemExit(
                    f"Selected portfolio essay has no enabled mirror entry: {artifact_id}"
                )
            if artifact.get("current_url") != post.get("url"):
                raise SystemExit(
                    f"Selected portfolio essay URL drifted from archive metadata: {artifact_id}"
                )
            annotation = placement.get("annotation") or artifact.get("rationale")
            if not isinstance(annotation, str) or not annotation.strip():
                raise SystemExit(
                    f"Selected portfolio essay is missing a homepage annotation: {artifact_id}"
                )
            expected[tier].append(
                {
                    "artifact_id": artifact_id,
                    "slug": slug,
                    "title": post_map.get(slug, {}).get("title") or post["title"],
                    "url": post["url"],
                    "annotation": annotation.strip(),
                }
            )

    for artifact_id, artifact in artifacts_by_id.items():
        placement = artifact.get("homepage") or {}
        if not isinstance(placement, dict):
            continue
        if placement.get("section") in expected and artifact_id not in selected_ids:
            raise SystemExit(
                f"Portfolio artifact has an unmanifested homepage placement: {artifact_id}"
            )

    return {
        "manifest": portfolio,
        "expected": expected,
    }


def validate_editorial_atlas() -> None:
    if not EDITORIAL_ATLAS_DIR.exists():
        raise SystemExit(f"Missing editorial atlas directory: {EDITORIAL_ATLAS_DIR}")
    if not EDITORIAL_ATLAS_DATA_PATH.exists():
        raise SystemExit(f"Missing editorial atlas data: {EDITORIAL_ATLAS_DATA_PATH}")

    atlas = ensure_checked_in_atlas_matches_generated()
    
    models = atlas.get("models", {})
    if not models:
        raise SystemExit("Editorial atlas data must contain at least one model")

    essay_required = {
        "title",
        "traction",
        "craft",
        "publication_power",
        "debate",
        "precision",
        "synthesis",
        "utility",
        "confidence",
        "short_label",
        "moves",
        "opening",
        "thesis_lock",
        "development",
        "borders",
        "ending",
        "reference_handling",
    }

    for model_id, model_data in models.items():
        essays = model_data.get("essays", [])
        drafts = model_data.get("drafts", [])
        
        if not essays:
            raise SystemExit(f"Model {model_id} has no essays")
        if not drafts:
            raise SystemExit(f"Model {model_id} has no drafts")

        # Validate each essay across all models for schema compliance
        for essay in essays:
            missing = essay_required.difference(essay)
            if missing:
                raise SystemExit(f"Editorial atlas essay missing keys {sorted(missing)} in model {model_id}: {essay.get('title', essay)}")
            if not isinstance(essay["moves"], list):
                raise SystemExit(f"Editorial atlas essay moves must be a list in model {model_id}: {essay['title']}")

        for draft in drafts:
            for key in ("title", "current_position", "target_position", "pulls", "resists"):
                if key not in draft:
                    raise SystemExit(f"Editorial atlas draft missing key '{key}' in model {model_id}: {draft}")
            for position_key in ("current_position", "target_position"):
                position = draft[position_key]
                required = {"traction", "craft", "debate", "precision", "synthesis", "utility"}
                missing = required.difference(position)
                if missing:
                    raise SystemExit(
                        f"Editorial atlas draft {position_key} missing keys {sorted(missing)} in model {model_id}: {draft['title']}"
                    )
            if not isinstance(draft["pulls"], list) or not draft["pulls"]:
                raise SystemExit(f"Editorial atlas draft pulls must be a non-empty list in model {model_id}: {draft['title']}")
            for pull in draft["pulls"]:
                for key in ("essay", "section", "desired_strength"):
                    if key not in pull:
                        raise SystemExit(f"Editorial atlas draft pull missing '{key}' in model {model_id}: {draft['title']}")


def validate_archive_assets(manifest: list[dict[str, str]]) -> None:
    for entry in manifest:
        markdown_path = REPO_ROOT / entry["md_path"]
        content = markdown_path.read_text(encoding="utf-8")
        for token in content.split("("):
            if not token.startswith("assets/"):
                continue
            asset_name = token.split(")", 1)[0]
            if ' "' in asset_name:
                asset_name = asset_name.split(' "', 1)[0]
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
    for prefix in (normalize_path_prefix(PATH_PREFIX), configured_site_path_prefix()):
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


def validate_editorial_atlas_route() -> None:
    target = required_file_target(MIRROR_OUTPUT, "/editorial-atlas/")
    if not target.exists():
        raise SystemExit("Built mirror is missing /editorial-atlas/index.html")


def validate_global_disclosure() -> None:
    for html_file in iter_built_html_files():
        relative_parts = html_file.relative_to(MIRROR_OUTPUT).parts
        if relative_parts and relative_parts[0] == "raw":
            continue
        soup = BeautifulSoup(html_file.read_text(encoding="utf-8"), "html.parser")
        disclosure = soup.select_one(".site-footer__disclosure")
        if disclosure is None or disclosure.get_text(" ", strip=True) != AI_DISCLOSURE:
            raise SystemExit(
                f"Built mirror page is missing the exact global AI disclosure: {html_file}"
            )


def validate_curated_homepage(
    portfolio: dict[str, object],
) -> None:
    homepage_path = MIRROR_OUTPUT / "index.html"
    if not homepage_path.exists():
        raise SystemExit("Built mirror is missing its homepage")
    soup = BeautifulSoup(homepage_path.read_text(encoding="utf-8"), "html.parser")
    page_text = soup.get_text(" ", strip=True)

    if AI_DISCLOSURE not in page_text:
        raise SystemExit("Homepage is missing the exact global AI disclosure")
    profile_links = [
        anchor
        for anchor in soup.find_all("a", href=PROFESSIONAL_PROFILE_URL)
        if anchor.get_text(" ", strip=True) == "Professional profile"
    ]
    if not profile_links:
        raise SystemExit("Homepage is missing the Professional profile primary CTA")
    primary_cta = soup.select_one(".hero__actions > a.button:not(.button--ghost)")
    if primary_cta is None or primary_cta.get("href") != PROFESSIONAL_PROFILE_URL:
        raise SystemExit("Professional profile must be the primary homepage CTA")

    if "Recent additions" in page_text:
        raise SystemExit("Homepage must not contain Recent additions")
    if soup.select_one(".hero__stats") is not None:
        raise SystemExit("Homepage must not contain archive statistics")
    for anchor in soup.find_all("a", href=True):
        if normalize_internal_path(urlparse(anchor["href"]).path) == "/editorial-atlas/":
            raise SystemExit("Editorial atlas must not be promoted or linked on the homepage")

    archive_links = [
        anchor
        for anchor in soup.find_all("a", href=True)
        if normalize_internal_path(urlparse(anchor["href"]).path) == "/archive/"
    ]
    if not archive_links:
        raise SystemExit("Homepage is missing a link to the complete archive")

    expected_by_tier = portfolio["expected"]
    assert isinstance(expected_by_tier, dict)
    for tier in ("FLAGSHIP", "SUPPORTING"):
        expected_items = expected_by_tier[tier]
        cards = soup.select(f'[data-portfolio-tier="{tier}"]')
        rendered_ids = [card.get("data-portfolio-artifact") for card in cards]
        expected_ids = [item["artifact_id"] for item in expected_items]
        if rendered_ids != expected_ids:
            raise SystemExit(
                f"Rendered {tier.lower()} order does not match the portfolio manifest: "
                f"expected {expected_ids}, got {rendered_ids}"
            )
        for card, expected_item in zip(cards, expected_items, strict=True):
            if expected_item["title"] not in card.get_text(" ", strip=True):
                raise SystemExit(
                    f"Homepage card title mismatch for {expected_item['artifact_id']}"
                )
            if expected_item["annotation"] not in card.get_text(" ", strip=True):
                raise SystemExit(
                    f"Homepage annotation mismatch for {expected_item['artifact_id']}"
                )
            hrefs = {anchor.get("href") for anchor in card.find_all("a", href=True)}
            if expected_item["url"] not in hrefs:
                raise SystemExit(
                    f"Homepage card is missing its canonical Substack link: "
                    f"{expected_item['artifact_id']}"
                )
            if not any(
                anchor.get_text(" ", strip=True) == "Evidence trail"
                for anchor in card.find_all("a", href=True)
            ):
                raise SystemExit(
                    f"Homepage card is missing its evidence link: {expected_item['artifact_id']}"
                )

    all_cards = soup.select("[data-portfolio-artifact]")
    expected_count = sum(len(items) for items in expected_by_tier.values())
    if len(all_cards) != expected_count:
        raise SystemExit("Homepage contains portfolio cards not authorized by the manifest")

    skip_link = soup.select_one('a.skip-link[href="#main-content"]')
    main = soup.select_one('main#main-content[tabindex="-1"]')
    if skip_link is None or main is None:
        raise SystemExit("Homepage is missing the keyboard skip-link contract")
    viewport = soup.find("meta", attrs={"name": "viewport"})
    if viewport is None or "width=device-width" not in viewport.get("content", ""):
        raise SystemExit("Homepage is missing the responsive viewport contract")

    stylesheet = MIRROR_OUTPUT / "assets" / "styles.css"
    styles = stylesheet.read_text(encoding="utf-8") if stylesheet.exists() else ""
    if ":focus-visible" not in styles:
        raise SystemExit("Mirror stylesheet is missing visible keyboard focus styles")
    if "@media (max-width:" not in styles:
        raise SystemExit("Mirror stylesheet is missing its mobile layout breakpoint")


def validate_archive_preservation(metadata: list[dict[str, str]]) -> None:
    mirrored = [entry for entry in metadata if entry.get("mirror_enabled")]
    archive_path = MIRROR_OUTPUT / "archive" / "index.html"
    if not archive_path.exists():
        raise SystemExit("Built mirror is missing the complete archive page")
    archive_soup = BeautifulSoup(archive_path.read_text(encoding="utf-8"), "html.parser")
    archive_cards = archive_soup.select("[data-post-card]")
    if len(archive_cards) != len(mirrored):
        raise SystemExit(
            "Complete archive does not contain every enabled public mirror entry: "
            f"expected {len(mirrored)}, got {len(archive_cards)}"
        )

    for entry in mirrored:
        slug = str(entry["slug"])
        post_path = MIRROR_OUTPUT / "posts" / slug / "index.html"
        if not post_path.exists():
            raise SystemExit(f"Built mirror is missing selected archive route: {slug}")
        post_soup = BeautifulSoup(post_path.read_text(encoding="utf-8"), "html.parser")
        canonical = post_soup.find("link", rel="canonical")
        if canonical is None or canonical.get("href") != entry["url"]:
            raise SystemExit(
                f"Mirrored essay canonical URL must remain on Substack: {slug}"
            )


def main() -> None:
    if not POST_MAP_PATH.exists():
        raise SystemExit(f"Missing post map: {POST_MAP_PATH}")
    if not ARCHIVE_DIR.exists():
        raise SystemExit(f"Missing archive directory: {ARCHIVE_DIR}")

    manifest = validate_metadata()
    portfolio = load_and_validate_portfolio_manifest(manifest)
    validate_editorial_atlas()
    validate_archive_assets(manifest)
    validate_readme_generation(load_post_map())
    validate_built_links()
    validate_editorial_atlas_route()
    validate_global_disclosure()
    validate_curated_homepage(portfolio)
    validate_archive_preservation(manifest)
    print(
        json.dumps(
            {
                "checked_posts": len(manifest),
                "checked_html_files": len(iter_built_html_files()),
                "checked_editorial_atlas": True,
                "checked_portfolio_homepage": True,
                "flagship_count": len(portfolio["expected"]["FLAGSHIP"]),
                "supporting_count": len(portfolio["expected"]["SUPPORTING"]),
                "generated_editorial_atlas": str(EDITORIAL_ATLAS_DATA_PATH),
                "path_prefix": normalize_path_prefix(PATH_PREFIX),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
