from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import rooted_layers_portfolio as portfolio  # noqa: E402


def artifact(
    artifact_id: str,
    *,
    platform: str = "SUBSTACK",
    tier: str = "ARCHIVE",
    homepage_section: str | None = None,
    homepage_order: int | None = None,
    lineage: str = "RESOLVED",
    risk: str = "LOW",
    target_visibility: str = "UNCHANGED",
    current_visibility: str = "PUBLIC",
    relationships: list[dict] | None = None,
) -> dict:
    platform_id = artifact_id.removeprefix("substack:").removeprefix("youtube:")
    current_url = (
        f"https://lambpetros.substack.com/p/{platform_id}"
        if platform == "SUBSTACK"
        else f"https://www.youtube.com/watch?v={platform_id}"
    )
    return {
        "artifact_id": artifact_id,
        "platform": platform,
        "platform_id": platform_id,
        "title": artifact_id,
        "current_url": current_url,
        "current_visibility": current_visibility,
        "family_id": "family:test",
        "relationships": relationships or [],
        "selection_tier": tier,
        "editorial_action": "KEEP" if platform == "SUBSTACK" else "NONE",
        "target_visibility": target_visibility,
        "homepage": {"section": homepage_section, "order": homepage_order},
        "provenance": {
            "status": "DOCUMENTED",
            "documented_contribution": "Original synthesis and implementation evidence.",
        },
        "source_lineage": {"status": lineage, "notes": "Checked."},
        "factual_risk": {"status": risk, "notes": "Bounded."},
        "evidence_anchors": ["publication_strategy_and_archive/source.md#anchor"],
        "rationale": "Concrete technical value.",
        "confidence": "HIGH",
        "approval_status": "PENDING",
        "application_status": "NOT_APPLIED",
    }


def manifest(artifacts: list[dict]) -> dict:
    flagships = sorted(
        (
            (item["homepage"]["order"], item["artifact_id"])
            for item in artifacts
            if item["homepage"]["section"] == "FLAGSHIP"
        )
    )
    supporting = sorted(
        (
            (item["homepage"]["order"], item["artifact_id"])
            for item in artifacts
            if item["homepage"]["section"] == "SUPPORTING"
        )
    )
    selected = [
        item["platform_id"]
        for item in artifacts
        if item["platform"] == "YOUTUBE" and item["selection_tier"] != "ARCHIVE"
    ]
    unlists = [
        item["platform_id"]
        for item in artifacts
        if item["platform"] == "YOUTUBE" and item["target_visibility"] == "UNLIST"
    ]
    return {
        "schema_version": 1,
        "portfolio_version": "2026-08-22.1",
        "generated_at": "2026-08-22T00:00:00+00:00",
        "source_snapshot": "corpus_snapshot.json",
        "source_snapshot_sha256": "a" * 64,
        "professional_profile_url": portfolio.PROFILE_URL,
        "mirror_url": portfolio.MIRROR_URL,
        "ai_disclosure": portfolio.DISCLOSURE,
        "homepage": {
            "flagship_artifact_ids": [item_id for _, item_id in flagships],
            "supporting_artifact_ids": [item_id for _, item_id in supporting],
        },
        "youtube": {
            "expected_channel_id": "CHANNEL123",
            "expected_channel_title": "Rooted Layers",
            "expected_uploads_playlist_id": "UPLOADS",
            "snapshot_timestamp": "2026-08-22T00:00:00+00:00",
            "source_ledger_sha256": "b" * 64,
            "selected_video_ids": selected,
            "unlist_video_ids": unlists,
            "playlist": {
                "title": portfolio.PLAYLIST_TITLE,
                "create_or_update": len(selected) >= 2,
                "surface_on_channel_homepage": len(selected) >= 2,
            },
        },
        "artifacts": artifacts,
        "unresolved_questions": [],
    }


def approve_mutation_artifacts(data: dict) -> None:
    selected = set(data["youtube"]["selected_video_ids"])
    unlisted = set(data["youtube"]["unlist_video_ids"])
    for item in data["artifacts"]:
        if (
            item["homepage"]["section"] is not None
            or item["platform_id"] in selected
            or item["platform_id"] in unlisted
        ):
            item["approval_status"] = "APPROVED"
            item["application_status"] = "NOT_APPLIED"


def release_gate(
    data: dict,
    *,
    manifest_path: Path,
    approval_path: Path,
    manifest_sha256: str,
) -> dict:
    youtube = data["youtube"]
    dimensions = {
        name: {"required": True, "approved": True}
        for name in ("quality", "external_mutation", "lifecycle_movement", "promotion")
    }
    return {
        "kind": "review_gate",
        "schema_version": 1,
        "gate_id": "release_readiness-test",
        "status": "resolved",
        "gate_type": "external_mutation",
        "gate_contract": "release_readiness",
        "workflow": {"workflow_id": portfolio.WORKFLOW_ID},
        "decision": {
            "decided_at": "2026-08-22T01:00:00+00:00",
            "decided_by": "Petros",
            "outcome": "approve",
            "quality_approved": True,
            "external_mutation_approved": True,
            "lifecycle_movement_approved": True,
            "promotion_approved": True,
            "approval_dimensions": dimensions,
        },
        "portfolio_authorization": {
            "schema_version": 1,
            "manifest_path": str(manifest_path),
            "manifest_sha256": manifest_sha256,
            "approval_path": str(approval_path),
            "approval_manifest_sha256": manifest_sha256,
            "source_snapshot_path": data["source_snapshot"],
            "source_snapshot_sha256": data["source_snapshot_sha256"],
            "expected_channel_id": youtube["expected_channel_id"],
            "expected_channel_title": youtube["expected_channel_title"],
            "expected_uploads_playlist_id": youtube["expected_uploads_playlist_id"],
            "snapshot_timestamp": youtube["snapshot_timestamp"],
            "source_ledger_sha256": youtube["source_ledger_sha256"],
        },
    }


def write_bound_documents(root: Path, data: dict) -> tuple[Path, Path, Path]:
    channel = {
        "channel_id": "CHANNEL123",
        "title": "Rooted Layers",
        "uploads_playlist_id": "UPLOADS",
    }
    ledger_path = root / "ledger.json"
    ledger = {
        "created_at": "2026-08-22T00:00:00+00:00",
        "channel": channel,
        "source": {"scope": "all_channel"},
        "videos": [],
    }
    ledger_path.write_text(json.dumps(ledger), encoding="utf-8")
    ledger_sha256 = portfolio.sha256_bytes(ledger_path.read_bytes())
    snapshot_path = root / "corpus_snapshot.json"
    snapshot = {
        "schema_version": 1,
        "sources": {
            "youtube_ledger": {
                "path": str(ledger_path),
                "sha256": ledger_sha256,
            }
        },
        "youtube": {
            "snapshot_timestamp": ledger["created_at"],
            "channel": channel,
        },
    }
    snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")
    data["source_snapshot"] = str(snapshot_path)
    data["source_snapshot_sha256"] = portfolio.sha256_bytes(
        snapshot_path.read_bytes()
    )
    data["youtube"].update(
        {
            "expected_channel_id": channel["channel_id"],
            "expected_channel_title": channel["title"],
            "expected_uploads_playlist_id": channel["uploads_playlist_id"],
            "snapshot_timestamp": ledger["created_at"],
            "source_ledger_sha256": ledger_sha256,
        }
    )
    manifest_path = root / "manifest.yaml"
    manifest_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    digest = portfolio.sha256_bytes(manifest_path.read_bytes())
    approval_path = root / "approval.yaml"
    approval = {
        "schema_version": 1,
        "status": "APPROVED",
        "manifest_sha256": digest,
        "approved_at": "2026-08-22T01:00:00+00:00",
        "approved_by": "Petros",
    }
    approval_path.write_text(yaml.safe_dump(approval, sort_keys=False), encoding="utf-8")
    gate_path = root / "reviewable-runs" / "gates" / "release-readiness.yaml"
    gate_path.parent.mkdir(parents=True, exist_ok=True)
    gate_path.write_text(
        yaml.safe_dump(
            release_gate(
                data,
                manifest_path=manifest_path,
                approval_path=approval_path,
                manifest_sha256=digest,
            ),
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return manifest_path, approval_path, gate_path


class RootedLayersPortfolioTests(unittest.TestCase):
    def test_valid_manifest_allows_zero_selected_items(self) -> None:
        data = manifest([artifact("substack:archive-post")])

        self.assertEqual(portfolio.validate_manifest_data(data), [])

    def test_preapproval_allows_pending_but_apply_ready_rejects_mutation_states(self) -> None:
        selected = artifact(
            "youtube:VIDEO1",
            platform="YOUTUBE",
            tier="SUPPORTING",
        )
        data = manifest([selected])

        self.assertEqual(portfolio.validate_manifest_data(data), [])
        errors = portfolio.validate_manifest_data(
            data,
            validation_mode="apply-ready",
        )

        self.assertTrue(any("not APPROVED" in error for error in errors))
        self.assertIn("apply-ready validation requires approval.yaml", errors)
        self.assertTrue(any("release_readiness" in error for error in errors))

    def test_apply_ready_requires_exact_approval_and_durable_release_gate(self) -> None:
        selected = artifact(
            "youtube:VIDEO1",
            platform="YOUTUBE",
            tier="SUPPORTING",
        )
        second = artifact(
            "youtube:VIDEO2",
            platform="YOUTUBE",
            tier="SUPPORTING",
        )
        data = manifest([selected, second])
        approve_mutation_artifacts(data)
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path, approval_path, gate_path = write_bound_documents(
                Path(tmpdir), data
            )

            with mock.patch.object(portfolio, "REPO_ROOT", Path(tmpdir)):
                result = portfolio.validate_manifest(
                    manifest_path,
                    approval_path,
                    gate_path,
                    validation_mode="apply-ready",
                )

        self.assertTrue(result["valid"], result["errors"])

    def test_apply_ready_rejects_stale_or_deferred_release_gate(self) -> None:
        data = manifest([artifact("substack:archive-post")])
        approve_mutation_artifacts(data)
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            manifest_path, approval_path, gate_path = write_bound_documents(root, data)
            gate = yaml.safe_load(gate_path.read_text(encoding="utf-8"))
            gate["status"] = "pending"
            gate["decision"]["outcome"] = "defer"
            gate["portfolio_authorization"]["manifest_sha256"] = "0" * 64
            gate_path.write_text(yaml.safe_dump(gate, sort_keys=False), encoding="utf-8")

            with mock.patch.object(portfolio, "REPO_ROOT", root):
                result = portfolio.validate_manifest(
                    manifest_path,
                    approval_path,
                    gate_path,
                    validation_mode="apply-ready",
                )

        self.assertFalse(result["valid"])
        self.assertTrue(any("status must equal resolved" in error for error in result["errors"]))
        self.assertTrue(any("outcome must equal approve" in error for error in result["errors"]))
        self.assertTrue(any("manifest digest" in error for error in result["errors"]))

    def test_apply_ready_rejects_gate_outside_durable_gate_store(self) -> None:
        data = manifest([artifact("substack:archive-post")])
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            manifest_path, approval_path, gate_path = write_bound_documents(root, data)
            outside_gate = root / "copied-gate.yaml"
            outside_gate.write_text(gate_path.read_text(encoding="utf-8"), encoding="utf-8")

            with mock.patch.object(portfolio, "REPO_ROOT", root):
                result = portfolio.validate_manifest(
                    manifest_path,
                    approval_path,
                    outside_gate,
                    validation_mode="apply-ready",
                )

        self.assertFalse(result["valid"])
        self.assertTrue(
            any("stored under reviewable-runs/gates" in error for error in result["errors"])
        )

    def test_rejects_duplicate_selected_unlist_ids_and_overlap(self) -> None:
        retained = artifact(
            "youtube:VIDEO1",
            platform="YOUTUBE",
            tier="SUPPORTING",
        )
        duplicate = manifest([retained])
        duplicate["youtube"]["selected_video_ids"] = ["VIDEO1", "VIDEO1"]
        duplicate["youtube"]["playlist"]["create_or_update"] = True
        errors = portfolio.validate_manifest_data(duplicate)
        self.assertIn("youtube.selected_video_ids contains duplicates", errors)

        unlisted = artifact(
            "youtube:VIDEO2",
            platform="YOUTUBE",
            target_visibility="UNLIST",
            relationships=[
                {"type": "DUPLICATES", "target_artifact_id": "youtube:VIDEO1"}
            ],
        )
        duplicate_unlist = manifest([retained, unlisted])
        duplicate_unlist["youtube"]["unlist_video_ids"] = ["VIDEO2", "VIDEO2"]
        errors = portfolio.validate_manifest_data(duplicate_unlist)
        self.assertIn("youtube.unlist_video_ids contains duplicates", errors)

        overlap = manifest([retained])
        overlap["youtube"]["unlist_video_ids"] = ["VIDEO1"]
        errors = portfolio.validate_manifest_data(overlap)
        self.assertIn("selected videos cannot also be unlisted", errors)

    def test_source_ledger_hash_timestamp_and_channel_are_fail_closed(self) -> None:
        data = manifest([artifact("substack:archive-post")])
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            manifest_path, _, _ = write_bound_documents(root, data)
            data["youtube"]["source_ledger_sha256"] = "0" * 64
            data["youtube"]["snapshot_timestamp"] = "2026-08-22T02:00:00+00:00"
            data["youtube"]["expected_uploads_playlist_id"] = "WRONG"
            manifest_path.write_text(
                yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
            )

            result = portfolio.validate_manifest(manifest_path)

        self.assertFalse(result["valid"])
        self.assertTrue(any("ledger digest" in error for error in result["errors"]))
        self.assertTrue(any("snapshot timestamp" in error for error in result["errors"]))
        self.assertTrue(any("uploads_playlist_id" in error for error in result["errors"]))

    def test_manifest_is_read_once_and_applied_object_matches_digested_bytes(self) -> None:
        data = manifest([artifact("substack:archive-post")])
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            manifest_path, _, _ = write_bound_documents(root, data)
            original_bytes = manifest_path.read_bytes()
            original_digest = portfolio.sha256_bytes(original_bytes)
            original_read_bytes = Path.read_bytes
            manifest_reads = 0

            def read_once_then_drift(path: Path) -> bytes:
                nonlocal manifest_reads
                raw = original_read_bytes(path)
                if path.resolve() == manifest_path.resolve():
                    manifest_reads += 1
                    if manifest_reads == 1:
                        path.write_text("schema_version: 999\n", encoding="utf-8")
                return raw

            with mock.patch.object(Path, "read_bytes", read_once_then_drift):
                parsed, result = portfolio.validate_manifest_document(manifest_path)

        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["manifest_sha256"], original_digest)
        self.assertEqual(parsed["portfolio_version"], "2026-08-22.1")
        self.assertEqual(manifest_reads, 1)

    def test_rejects_duplicate_ids_and_more_than_four_flagships(self) -> None:
        items = [
            artifact(
                f"substack:post-{index}",
                tier="FLAGSHIP",
                homepage_section="FLAGSHIP",
                homepage_order=index,
            )
            for index in range(1, 6)
        ]
        items.append(dict(items[0]))
        data = manifest(items)

        errors = portfolio.validate_manifest_data(data)

        self.assertTrue(any("duplicate artifact_id" in error for error in errors))
        self.assertIn("homepage exceeds four flagship essays", errors)

    def test_rejects_unresolved_flagship_missing_evidence_and_bad_placement(self) -> None:
        item = artifact(
            "substack:flagship",
            tier="FLAGSHIP",
            homepage_section="FLAGSHIP",
            homepage_order=1,
            lineage="CONFLICT",
            risk="UNRESOLVED_HIGH",
        )
        item["evidence_anchors"] = []
        data = manifest([item])
        data["homepage"]["flagship_artifact_ids"] = []

        errors = portfolio.validate_manifest_data(data)

        self.assertTrue(any("evidence_anchors" in error for error in errors))
        self.assertTrue(any("source lineage" in error for error in errors))
        self.assertTrue(any("high factual risk" in error for error in errors))
        self.assertTrue(any("do not match artifact placements" in error for error in errors))

    def test_rejects_invalid_visibility_transition(self) -> None:
        item = artifact(
            "youtube:VIDEO1",
            platform="YOUTUBE",
            target_visibility="UNLIST",
            current_visibility="PRIVATE",
        )
        data = manifest([item])

        errors = portfolio.validate_manifest_data(data)

        self.assertTrue(any("UNLIST requires current_visibility PUBLIC" in error for error in errors))

    def test_approval_digest_detects_manifest_drift(self) -> None:
        data = manifest([artifact("substack:archive-post")])
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "manifest.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            approval = {
                "schema_version": 1,
                "status": "APPROVED",
                "manifest_sha256": portfolio.sha256_bytes(path.read_bytes()),
                "approved_at": "2026-08-22T00:00:00+00:00",
                "approved_by": "Petros",
            }
            self.assertEqual(
                portfolio.validate_manifest_data(
                    data,
                    manifest_path=path,
                    manifest_sha256=approval["manifest_sha256"],
                    approval=approval,
                ),
                [],
            )
            path.write_text(path.read_text() + "# drift\n", encoding="utf-8")

            errors = portfolio.validate_manifest_data(
                data,
                manifest_path=path,
                manifest_sha256=portfolio.sha256_bytes(path.read_bytes()),
                approval=approval,
            )

        self.assertTrue(any("digest" in error for error in errors))

    def test_snapshot_inventory_is_public_only_and_requires_verified_channel(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            metadata_path = root / "metadata.json"
            metadata_path.write_text(
                json.dumps(
                    [
                        {"slug": "public", "audience": "everyone"},
                        {"slug": "paid", "audience": "only_paid"},
                        {"slug": "draft", "audience": "draft"},
                    ]
                ),
                encoding="utf-8",
            )
            post_map_path = root / "post_map.yaml"
            post_map_path.write_text(
                yaml.safe_dump(
                    {
                        "posts": {
                            "public": {"status": "published"},
                            "mapped-only": {"status": "published"},
                        }
                    }
                ),
                encoding="utf-8",
            )
            completeness_path = root / "completeness.json"
            completeness_path.write_text(
                json.dumps({"complete": True, "source_failures": [], "prune_allowed": True}),
                encoding="utf-8",
            )
            ledger_path = root / "ledger.json"
            ledger_path.write_text(
                json.dumps(
                    {
                        "created_at": "2026-08-22T00:00:00+00:00",
                        "channel": {
                            "channel_id": "CHANNEL123",
                            "title": "Rooted Layers",
                            "uploads_playlist_id": "UPLOADS",
                        },
                        "source": {"scope": "all_channel"},
                        "videos": [
                            {"video_id": "PUBLIC", "privacy_status": "public"},
                            {"video_id": "PRIVATE", "privacy_status": "private"},
                        ],
                        "channel_playlists": [],
                    }
                ),
                encoding="utf-8",
            )
            content_path = root / "content.json"
            content_path.write_text(
                json.dumps({"items": {"PUBLIC": {"status": "present"}}}),
                encoding="utf-8",
            )

            snapshot = portfolio.build_snapshot(
                metadata_path=metadata_path,
                post_map_path=post_map_path,
                completeness_path=completeness_path,
                youtube_ledger_path=ledger_path,
                youtube_content_path=content_path,
            )

        self.assertEqual(snapshot["substack"]["public_post_count"], 1)
        self.assertEqual(snapshot["substack"]["published_map_only_slugs"], ["mapped-only"])
        self.assertEqual(snapshot["youtube"]["visibility_counts"], {"public": 1, "private": 1})


if __name__ == "__main__":
    unittest.main()
