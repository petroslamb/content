from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import requests

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import sync_substack_archive as sync  # noqa: E402


class FakeResponse:
    def __init__(
        self,
        *,
        text: str = "",
        payload: object = None,
        error: Exception | None = None,
    ) -> None:
        self.text = text
        self.payload = payload
        self.error = error

    def raise_for_status(self) -> None:
        if self.error:
            raise self.error

    def json(self) -> object:
        return self.payload


class ScriptedSession:
    def __init__(
        self,
        *,
        rss: FakeResponse | Exception | None = None,
        archive: list[FakeResponse | Exception] | None = None,
    ) -> None:
        self.headers: dict[str, str] = {}
        self.rss = rss
        self.archive = list(archive or [])
        self.archive_offsets: list[int] = []

    def get(self, url: str, *, params: dict | None = None, timeout: int = 30) -> FakeResponse:
        del timeout
        if url.endswith(sync.RSS_PATH):
            if isinstance(self.rss, Exception):
                raise self.rss
            if self.rss is None:
                raise AssertionError("Unexpected RSS request")
            return self.rss
        if url.endswith(sync.ARCHIVE_API_PATH):
            self.archive_offsets.append(int((params or {})["offset"]))
            if not self.archive:
                raise AssertionError("Unexpected archive request")
            result = self.archive.pop(0)
            if isinstance(result, Exception):
                raise result
            return result
        raise AssertionError(f"Unexpected URL: {url}")


def rss_document(*slugs: str) -> str:
    items = "".join(
        (
            "<item>"
            f"<link>https://example.substack.com/p/{slug}</link>"
            "<pubDate>Wed, 01 Jan 2025 00:00:00 GMT</pubDate>"
            "</item>"
        )
        for slug in slugs
    )
    return f"<rss><channel>{items}</channel></rss>"


def archive_post(slug: str) -> dict[str, str]:
    return {
        "slug": slug,
        "canonical_url": f"https://example.substack.com/p/{slug}",
        "post_date": "2025-01-01T00:00:00Z",
    }


class SubstackDiscoveryTests(unittest.TestCase):
    maxDiff = None

    def test_cli_defaults_to_tracked_completeness_report(self) -> None:
        with mock.patch.object(sys, "argv", ["sync_substack_archive.py"]):
            args = sync.parse_args()

        self.assertEqual(Path(args.summary_path), sync.COMPLETENESS_REPORT_PATH)

    def test_cli_returns_failure_when_refresh_is_incomplete(self) -> None:
        with (
            mock.patch.object(
                sys,
                "argv",
                [
                    "sync_substack_archive.py",
                    "--output-dir",
                    "/tmp/archive",
                    "--summary-path",
                    "/tmp/report.json",
                ],
            ),
            mock.patch.object(sync, "sync_archive", return_value={"complete": False}),
            self.assertRaisesRegex(SystemExit, "refresh is incomplete"),
        ):
            sync.main()

    def test_archive_api_paginates_until_an_empty_page(self) -> None:
        session = ScriptedSession(
            archive=[
                FakeResponse(payload=[archive_post("a"), archive_post("b")]),
                FakeResponse(payload=[archive_post("c"), archive_post("d")]),
                FakeResponse(payload=[]),
            ]
        )

        posts, report = sync.discover_archive_api_posts(
            session,
            "https://example.substack.com",
            page_limit=2,
        )

        self.assertEqual([post["slug"] for post in posts], ["a", "b", "c", "d"])
        self.assertEqual(session.archive_offsets, [0, 2, 4])
        self.assertTrue(report["success"])
        self.assertTrue(report["complete"])
        self.assertEqual(report["pages_fetched"], 3)
        self.assertEqual(report["termination"], "empty_page")

    def test_discovery_unions_rss_all_archive_pages_and_published_post_map(self) -> None:
        session = ScriptedSession(
            rss=FakeResponse(text=rss_document("rss-only", "shared")),
            archive=[
                FakeResponse(payload=[archive_post("shared"), archive_post("api-only")]),
            ],
        )
        post_map = {
            "api-only": {"status": "published"},
            "map-only": {"status": "published"},
            "draft-only": {"status": "draft"},
        }

        outcome = sync.discover_posts(
            session,
            "https://example.substack.com",
            post_map=post_map,
        )

        self.assertEqual(
            [post["slug"] for post in outcome.posts],
            ["rss-only", "shared", "api-only", "map-only"],
        )
        self.assertTrue(outcome.complete)
        self.assertEqual(outcome.sources["rss"]["item_count"], 2)
        self.assertEqual(outcome.sources["archive_api"]["item_count"], 2)
        self.assertEqual(outcome.sources["post_map"]["item_count"], 2)
        self.assertEqual(outcome.as_report()["failures"], [])

    def test_repeated_archive_page_stops_and_marks_source_incomplete(self) -> None:
        repeated_page = [archive_post("a"), archive_post("b")]
        session = ScriptedSession(
            archive=[
                FakeResponse(payload=repeated_page),
                FakeResponse(payload=repeated_page),
            ]
        )

        posts, report = sync.discover_archive_api_posts(
            session,
            "https://example.substack.com",
            page_limit=2,
        )

        self.assertEqual([post["slug"] for post in posts], ["a", "b"])
        self.assertEqual(session.archive_offsets, [0, 2])
        self.assertTrue(report["success"])
        self.assertFalse(report["complete"])
        self.assertEqual(report["termination"], "repeated_page")
        self.assertIn("pagination did not advance", report["error"])

    def test_partial_archive_failure_preserves_successful_pages_and_reports_failure(self) -> None:
        session = ScriptedSession(
            archive=[
                FakeResponse(payload=[archive_post("a"), archive_post("b")]),
                requests.HTTPError("archive unavailable"),
            ]
        )

        posts, report = sync.discover_archive_api_posts(
            session,
            "https://example.substack.com",
            page_limit=2,
        )

        self.assertEqual([post["slug"] for post in posts], ["a", "b"])
        self.assertTrue(report["success"])
        self.assertFalse(report["complete"])
        self.assertEqual(report["termination"], "request_failed")
        self.assertIn("archive unavailable", report["error"])

    def test_rss_failure_does_not_hide_other_sources_but_blocks_completeness(self) -> None:
        session = ScriptedSession(
            rss=requests.HTTPError("feed forbidden"),
            archive=[FakeResponse(payload=[archive_post("api-only")])],
        )

        outcome = sync.discover_posts(
            session,
            "https://example.substack.com",
            post_map={"map-only": {"status": "published"}},
        )

        self.assertEqual([post["slug"] for post in outcome.posts], ["api-only", "map-only"])
        self.assertFalse(outcome.complete)
        self.assertFalse(outcome.sources["rss"]["success"])
        self.assertFalse(outcome.sources["rss"]["complete"])
        self.assertEqual(outcome.as_report()["failures"][0]["source"], "rss")

    def test_post_map_load_failure_is_reported_and_blocks_completeness(self) -> None:
        session = ScriptedSession(
            rss=FakeResponse(text=rss_document("rss-only")),
            archive=[FakeResponse(payload=[archive_post("api-only")])],
        )

        with mock.patch.object(sync, "load_post_map", side_effect=ValueError("invalid map")):
            outcome = sync.discover_posts(
                session,
                "https://example.substack.com",
            )

        self.assertEqual([post["slug"] for post in outcome.posts], ["rss-only", "api-only"])
        self.assertFalse(outcome.complete)
        self.assertFalse(outcome.sources["post_map"]["success"])
        self.assertFalse(outcome.sources["post_map"]["complete"])
        self.assertIn("invalid map", outcome.sources["post_map"]["error"])

    def test_incomplete_discovery_never_prunes_files_assets_or_manifest_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "substack_archive"
            assets_dir = output_dir / "assets"
            assets_dir.mkdir(parents=True)
            stale_markdown = output_dir / "2024-01-01_old.md"
            stale_html = output_dir / "2024-01-01_old.html"
            stale_asset = assets_dir / "asset-old.jpg"
            stale_markdown.write_text("# Old\n", encoding="utf-8")
            stale_html.write_text("<h1>Old</h1>\n", encoding="utf-8")
            stale_asset.write_bytes(b"old")

            metadata_path = output_dir / "metadata.json"
            metadata_path.write_text(
                json.dumps(
                    [
                        {
                            "slug": "old",
                            "title": "Old",
                            "url": "https://example.substack.com/p/old",
                            "post_date": "2024-01-01T00:00:00Z",
                            "audience": "everyone",
                            "fetched_at": "2024-01-01T00:00:00Z",
                            "content_hash": "old-hash",
                            "md_path": "publication_strategy_and_archive/substack_archive/2024-01-01_old.md",
                            "html_path": "publication_strategy_and_archive/substack_archive/2024-01-01_old.html",
                            "hero_image": "publication_strategy_and_archive/substack_archive/assets/asset-old.jpg",
                            "mirror_enabled": True,
                        }
                    ]
                ),
                encoding="utf-8",
            )
            outcome = sync.DiscoveryOutcome(
                posts=[
                    {
                        "slug": "new",
                        "url": "https://example.substack.com/p/new",
                        "published_at": "2025-01-01T00:00:00Z",
                    }
                ],
                post_map={"new": {"status": "published"}},
                sources={
                    "rss": {
                        "success": False,
                        "complete": False,
                        "item_count": 0,
                        "error": "HTTPError: feed forbidden",
                    },
                    "archive_api": {
                        "success": True,
                        "complete": True,
                        "item_count": 1,
                        "pages_fetched": 1,
                        "termination": "short_page",
                        "error": None,
                    },
                    "post_map": {
                        "success": True,
                        "complete": True,
                        "item_count": 1,
                        "error": None,
                    },
                },
            )
            fetched_post = {
                "slug": "new",
                "title": "New",
                "canonical_url": "https://example.substack.com/p/new",
                "post_date": "2025-01-01T00:00:00Z",
                "updated_at": "2025-01-01T00:00:00Z",
                "audience": "everyone",
                "body_html": "<p>New public post.</p>",
            }
            summary_path = output_dir / "completeness_report.json"

            with (
                mock.patch.object(sync, "METADATA_PATH", metadata_path),
                mock.patch.object(sync, "discover_posts", return_value=outcome),
                mock.patch.object(sync, "fetch_post", return_value=fetched_post),
                mock.patch.object(sync, "write_readme_publication_map"),
            ):
                summary = sync.sync_archive(
                    "https://example.substack.com",
                    output_dir,
                    summary_path,
                )

            self.assertTrue(stale_markdown.exists())
            self.assertTrue(stale_html.exists())
            self.assertTrue(stale_asset.exists())
            self.assertFalse(summary["prune_allowed"])
            self.assertFalse(summary["cleanup"]["performed"])
            self.assertIn("discovery_incomplete", summary["cleanup"]["blockers"])
            self.assertEqual(summary["removed_files"], [])
            self.assertEqual(summary["removed_assets"], [])
            self.assertEqual(summary["preserved_manifest_slugs"], ["old"])
            self.assertEqual(json.loads(summary_path.read_text(encoding="utf-8")), summary)
            self.assertEqual(
                {entry["slug"] for entry in json.loads(metadata_path.read_text(encoding="utf-8"))},
                {"new", "old"},
            )

    def test_non_public_posts_are_excluded_before_rendering(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "substack_archive"
            (output_dir / "assets").mkdir(parents=True)
            metadata_path = output_dir / "metadata.json"
            metadata_path.write_text("[]\n", encoding="utf-8")
            outcome = sync.DiscoveryOutcome(
                posts=[
                    {
                        "slug": "paid",
                        "url": "https://example.substack.com/p/paid",
                        "published_at": "2025-01-01T00:00:00Z",
                    }
                ],
                post_map={"paid": {"status": "published"}},
                sources={
                    name: {"success": True, "complete": True, "item_count": 1, "error": None}
                    for name in ("rss", "archive_api", "post_map")
                },
            )
            paid_post = {
                "slug": "paid",
                "title": "Paid",
                "canonical_url": "https://example.substack.com/p/paid",
                "post_date": "2025-01-01T00:00:00Z",
                "audience": "only_paid",
                "body_html": "<p>Subscriber content.</p>",
            }

            with (
                mock.patch.object(sync, "METADATA_PATH", metadata_path),
                mock.patch.object(sync, "discover_posts", return_value=outcome),
                mock.patch.object(sync, "fetch_post", return_value=paid_post),
                mock.patch.object(sync, "localize_rich_media") as localize,
                mock.patch.object(sync, "write_readme_publication_map"),
            ):
                summary = sync.sync_archive(
                    "https://example.substack.com",
                    output_dir,
                    output_dir / "completeness_report.json",
                )

            localize.assert_not_called()
            self.assertTrue(summary["complete"])
            self.assertEqual(summary["inventory_scope"], "public_substack_posts_only")
            self.assertEqual(
                summary["excluded_non_public"],
                [{"slug": "paid", "audience": "only_paid"}],
            )
            self.assertEqual(json.loads(metadata_path.read_text(encoding="utf-8")), [])

    def test_post_fetch_failure_blocks_pruning_and_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "substack_archive"
            assets_dir = output_dir / "assets"
            assets_dir.mkdir(parents=True)
            old_markdown = output_dir / "2024-01-01_old.md"
            old_markdown.write_text("# Old\n", encoding="utf-8")
            old_html = output_dir / "2024-01-01_old.html"
            old_html.write_text("<h1>Old</h1>\n", encoding="utf-8")
            metadata_path = output_dir / "metadata.json"
            old_entry = {
                "slug": "old",
                "title": "Old",
                "url": "https://example.substack.com/p/old",
                "post_date": "2024-01-01T00:00:00Z",
                "audience": "everyone",
                "fetched_at": "2024-01-01T00:00:00Z",
                "content_hash": "old-hash",
                "md_path": "publication_strategy_and_archive/substack_archive/2024-01-01_old.md",
                "html_path": "publication_strategy_and_archive/substack_archive/2024-01-01_old.html",
                "hero_image": None,
                "mirror_enabled": True,
            }
            metadata_path.write_text(json.dumps([old_entry]), encoding="utf-8")
            outcome = sync.DiscoveryOutcome(
                posts=[
                    {
                        "slug": "old",
                        "url": "https://example.substack.com/p/old",
                        "published_at": "2024-01-01T00:00:00Z",
                    }
                ],
                post_map={"old": {"status": "published"}},
                sources={
                    name: {"success": True, "complete": True, "item_count": 1, "error": None}
                    for name in ("rss", "archive_api", "post_map")
                },
            )

            with (
                mock.patch.object(sync, "METADATA_PATH", metadata_path),
                mock.patch.object(sync, "discover_posts", return_value=outcome),
                mock.patch.object(sync, "fetch_post", side_effect=requests.HTTPError("post unavailable")),
                mock.patch.object(sync, "write_readme_publication_map"),
            ):
                summary = sync.sync_archive(
                    "https://example.substack.com",
                    output_dir,
                    output_dir / "completeness_report.json",
                )

            self.assertFalse(summary["complete"])
            self.assertFalse(summary["prune_allowed"])
            self.assertIn("post_fetch_incomplete", summary["cleanup"]["blockers"])
            self.assertEqual(summary["preserved_manifest_slugs"], ["old"])
            self.assertEqual(summary["source_failures"][0]["source"], "post:old")
            self.assertTrue(old_markdown.exists())
            self.assertTrue(old_html.exists())


if __name__ == "__main__":
    unittest.main()
