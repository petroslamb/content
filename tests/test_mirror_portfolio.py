from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import check_mirror as mirror  # noqa: E402


def metadata_entry(slug: str) -> dict[str, object]:
    return {
        "slug": slug,
        "title": slug.replace("-", " ").title(),
        "url": f"https://lambpetros.substack.com/p/{slug}",
        "mirror_enabled": True,
    }


def portfolio_artifact(
    slug: str,
    *,
    tier: str = "FLAGSHIP",
    order: int = 1,
) -> dict[str, object]:
    return {
        "artifact_id": f"substack:{slug}",
        "platform": "SUBSTACK",
        "platform_id": slug,
        "current_url": f"https://lambpetros.substack.com/p/{slug}",
        "selection_tier": tier,
        "rationale": f"Why {slug} matters for technical review.",
        "homepage": {"section": tier, "order": order},
    }


def portfolio_manifest(artifacts: list[dict[str, object]]) -> dict[str, object]:
    flagships = sorted(
        (
            (int(artifact["homepage"]["order"]), str(artifact["artifact_id"]))
            for artifact in artifacts
            if artifact["homepage"]["section"] == "FLAGSHIP"
        )
    )
    supporting = sorted(
        (
            (int(artifact["homepage"]["order"]), str(artifact["artifact_id"]))
            for artifact in artifacts
            if artifact["homepage"]["section"] == "SUPPORTING"
        )
    )
    return {
        "professional_profile_url": mirror.PROFESSIONAL_PROFILE_URL,
        "ai_disclosure": mirror.AI_DISCLOSURE,
        "homepage": {
            "flagship_artifact_ids": [artifact_id for _, artifact_id in flagships],
            "supporting_artifact_ids": [artifact_id for _, artifact_id in supporting],
        },
        "artifacts": artifacts,
    }


class MirrorPortfolioManifestTests(unittest.TestCase):
    def validate(
        self,
        manifest: dict[str, object],
        metadata: list[dict[str, object]],
    ) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest_path = Path(temp_dir) / "portfolio_manifest.yaml"
            manifest_path.write_text(
                yaml.safe_dump(manifest, sort_keys=False),
                encoding="utf-8",
            )
            with (
                mock.patch.object(mirror, "PORTFOLIO_MANIFEST_PATH", manifest_path),
                mock.patch.object(mirror, "load_post_map", return_value={}),
            ):
                return mirror.load_and_validate_portfolio_manifest(metadata)

    def test_allows_zero_homepage_selections(self) -> None:
        result = self.validate(portfolio_manifest([]), [])

        self.assertEqual(result["expected"]["FLAGSHIP"], [])
        self.assertEqual(result["expected"]["SUPPORTING"], [])

    def test_preserves_manifest_order_and_annotations(self) -> None:
        artifacts = [
            portfolio_artifact("one", tier="FLAGSHIP", order=1),
            portfolio_artifact("two", tier="SUPPORTING", order=1),
        ]

        result = self.validate(
            portfolio_manifest(artifacts),
            [metadata_entry("one"), metadata_entry("two")],
        )

        self.assertEqual(
            [item["artifact_id"] for item in result["expected"]["FLAGSHIP"]],
            ["substack:one"],
        )
        self.assertEqual(
            result["expected"]["SUPPORTING"][0]["annotation"],
            "Why two matters for technical review.",
        )

    def test_rejects_more_than_four_flagships(self) -> None:
        artifacts = [
            portfolio_artifact(f"post-{index}", order=index)
            for index in range(1, 6)
        ]

        with self.assertRaisesRegex(SystemExit, "exceeds four flagship essays"):
            self.validate(
                portfolio_manifest(artifacts),
                [metadata_entry(f"post-{index}") for index in range(1, 6)],
            )

    def test_rejects_homepage_placement_not_in_ordered_ids(self) -> None:
        artifact = portfolio_artifact("hidden-placement")
        manifest = portfolio_manifest([])
        manifest["artifacts"] = [artifact]

        with self.assertRaisesRegex(SystemExit, "unmanifested homepage placement"):
            self.validate(manifest, [metadata_entry("hidden-placement")])

    def test_rejects_substack_url_drift(self) -> None:
        artifact = portfolio_artifact("url-drift")
        artifact["current_url"] = "https://lambpetros.substack.com/p/old-url"

        with self.assertRaisesRegex(SystemExit, "URL drifted"):
            self.validate(portfolio_manifest([artifact]), [metadata_entry("url-drift")])


if __name__ == "__main__":
    unittest.main()
