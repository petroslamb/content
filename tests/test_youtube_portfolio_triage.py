from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_youtube_portfolio_triage as triage  # noqa: E402


class YouTubePortfolioTriageTests(unittest.TestCase):
    def test_title_normalization_removes_format_wrappers(self) -> None:
        self.assertEqual(
            triage.normalize_title(
                "The Binding Gap | A Cinematic Research Brief #research"
            ),
            "the binding gap",
        )
        self.assertEqual(
            triage.normalize_title("The Binding Gap: Explainer TL;DR"),
            "the binding gap",
        )

    def test_non_public_video_remains_inventory_only(self) -> None:
        item = triage.triage_video(
            {
                "video_id": "PRIVATE",
                "title": "Untitled video",
                "privacy_status": "private",
                "format": "short",
            },
            {"status": "missing"},
        )

        self.assertEqual(item["evidence_state"], "INVENTORY_ONLY")
        self.assertIn("INVENTORY_ONLY_NON_PUBLIC", item["triage_flags"])
        self.assertIn("UNTITLED_TEST_OR_DRAFT_TITLE", item["triage_flags"])

    def test_shared_caption_is_a_warning_not_an_unlisting_decision(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            caption_path = Path(tmpdir) / "caption.srt"
            caption_path.write_text(
                "1\n00:00:00,000 --> 00:00:02,000\nA bounded claim.\n",
                encoding="utf-8",
            )
            ledger = {
                "channel": {"channel_id": "CHANNEL123", "title": "Rooted Layers"},
                "created_at": "2026-08-22T00:00:00+00:00",
                "videos": [
                    {
                        "video_id": video_id,
                        "title": "Same title",
                        "privacy_status": "public",
                        "format": "cinematic",
                        "duration_seconds": 180,
                        "description": "Description",
                        "thumbnail_url": "thumb.jpg",
                    }
                    for video_id in ("A", "B")
                ],
            }
            content = {
                "items": {
                    video_id: {
                        "status": "present",
                        "match_confidence": "high",
                        "srt_path": str(caption_path),
                    }
                    for video_id in ("A", "B")
                }
            }

            result = triage.build_triage(ledger, content)

        self.assertEqual(len(result["duplicate_title_groups"]), 1)
        self.assertEqual(len(result["shared_caption_groups"]), 1)
        self.assertIn("never authorizes unlisting", result["shared_caption_groups"][0]["warning"])
        self.assertNotIn("score", result)


if __name__ == "__main__":
    unittest.main()
