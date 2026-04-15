from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import harness  # noqa: E402
import essay_iteration_support  # noqa: E402


def create_temp_leaf_package(package_dir: Path) -> str:
    package_dir.mkdir(parents=True, exist_ok=True)
    package_key = package_dir.name
    draft_path = package_dir / f"{package_key}.md"
    (package_dir / "papers").mkdir(exist_ok=True)
    (package_dir / "papers" / "index.md").write_text("# Paper Index\n")
    (package_dir / "README.md").write_text(f"# {package_key}\n")
    draft_path.write_text(f"# {package_key}\n\n## Limits\n\n## References\n")

    status = {
        "kind": "leaf",
        "publication": package_key,
        "revision": 1,
        "config": {
            "markdown_path": f"publications/{package_key}/{package_key}.md",
        },
        "stages": {
            stage: {"done": False, "last_updated": None}
            for stage in harness.STAGES
        },
    }
    (package_dir / "status.yaml").write_text(yaml.safe_dump(status, sort_keys=False))
    return package_key


def write_frontmatter_markdown(path: Path, frontmatter: dict, body: str) -> None:
    path.write_text(
        "---\n"
        + yaml.safe_dump(frontmatter, sort_keys=False).strip()
        + "\n---\n"
        + body
    )


class EssayIterationPacketTests(unittest.TestCase):
    maxDiff = None

    def run_init(self, package_key: str, force: bool = False) -> dict:
        command = [
            sys.executable,
            "scripts/init_essay_iteration_packet.py",
            "--package",
            package_key,
            "--format",
            "json",
        ]
        if force:
            command.append("--force")
        result = subprocess.run(
            command,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        return json.loads(result.stdout)

    def run_validator(self, package_key: str, expect_success: bool) -> dict:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/check_essay_iteration_packet.py",
                "--package",
                package_key,
                "--format",
                "json",
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if expect_success:
            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        return json.loads(result.stdout)

    def set_revision(self, package_dir: Path, revision: int) -> None:
        status_path = package_dir / "status.yaml"
        status = yaml.safe_load(status_path.read_text())
        status["revision"] = revision
        status_path.write_text(yaml.safe_dump(status, sort_keys=False))

    def load_packet(
        self,
        package_dir: Path,
        package_key: str,
        revision: int = 1,
    ) -> tuple[dict, dict[str, Path]]:
        manifest_path = package_dir / f"{package_key}-essay-iteration-packet-r{revision}.json"
        packet = json.loads(manifest_path.read_text())
        outputs = {
            name: (REPO_ROOT / relpath).resolve()
            for name, relpath in packet["output_paths"].items()
        }
        return packet, outputs

    def write_packet_manifest(
        self,
        package_dir: Path,
        package_key: str,
        revision: int,
        packet: dict,
    ) -> None:
        manifest_path = package_dir / f"{package_key}-essay-iteration-packet-r{revision}.json"
        manifest_path.write_text(json.dumps(packet, indent=2))

    def populate_valid_packet(
        self,
        package_dir: Path,
        package_key: str,
        *,
        revision: int = 1,
        schema_version: int | None = 2,
        north_star_verdict: str = "below_target",
        recommendation: str = "revise_candidate",
        dominant_blocker_slug: str = "",
        continue_iteration: bool | None = None,
        rewrite_mode: str = "",
        stop_gate_status: str = "inactive",
    ) -> tuple[dict, dict[str, Path]]:
        self.set_revision(package_dir, revision)
        self.run_init(package_key)
        packet, outputs = self.load_packet(package_dir, package_key, revision=revision)

        if schema_version is None:
            packet.pop("packet_schema_version", None)
        else:
            packet["packet_schema_version"] = schema_version
        self.write_packet_manifest(package_dir, package_key, revision, packet)

        outputs["blueprint"].write_text(
            "# Hardened Blueprint\n\n"
            "## Promise\n\nA bounded thesis.\n\n"
            "## Spine\n\nA section spine.\n\n"
            "## Paragraph burden\n\nEach section has a job.\n\n"
            "## Evidence burden\n\nBody work and references are separated.\n\n"
            "## Cut order\n\nTrim examples before the core argument.\n\n"
            "## Failure triggers\n\nPromotion is void if the evidence no longer supports the claim.\n\n"
            "## Opening Lab\n\nNot active.\n\n"
            "## Object Decision\n\nNot active.\n\n"
            "## Body / Support / Footnote Ledger\n\nNot active.\n\n"
            "## Second-Pass Bet\n\nNot active.\n"
        )
        outputs["candidate"].write_text(
            "# Candidate Draft\n\n"
            "A concrete opening paragraph.\n\n"
            "## Limits\n\nThis essay does not claim complete institutional coverage.\n\n"
            "## References\n\nOne annotated reference.\n"
        )

        write_frontmatter_markdown(
            outputs["replacement_review"],
            {
                "kind": "essay_iteration_replacement_review",
                "package": package_key,
                "revision": revision,
                "judgment_policy": "draft_only",
                "live_draft_path": packet["live_draft_path"],
                "candidate_path": packet["candidate_path"],
                "replacement_verdict": "revise_again",
                "north_star_verdict": north_star_verdict,
                "dominant_blocker_slug": dominant_blocker_slug,
                "continue_iteration": continue_iteration,
                "evidence_anchor_paths": [packet["live_draft_path"], packet["candidate_path"]],
            },
            (
                "# Cold Replacement Review\n\n"
                "## Findings\n\n- `P1`: Anchored finding.\n\n"
                "## Prioritized Issues\n\n- `P1`: Major issue.\n\n"
                "## Scorecard\n\n- Thesis strength: 8\n\n"
                "## Replacement Verdict\n\nRevise again.\n\n"
                "## North-Star Verdict\n\nBelow target.\n\n"
                "## Main Blockers\n\nUtility and limits still need sharpening.\n\n"
                "## Dominant Blocker\n\nNot active.\n\n"
                "## North-Star Delta\n\nNot active.\n\n"
                "## Continue Or Stop\n\nNot active.\n\n"
                "## If Continue, What Gets Cut\n\nNot active.\n"
            ),
        )

        write_frontmatter_markdown(
            outputs["atlas_scorecard"],
            {
                "kind": "essay_iteration_atlas_scorecard",
                "package": package_key,
                "revision": revision,
                "judgment_policy": "draft_only",
                "candidate_path": packet["candidate_path"],
                "opening_anchor": "candidate:1",
                "middle_anchor": "candidate:5",
                "ending_anchor": "candidate:9",
                "nearby_archive_anchor": "nearby-essay",
                "stronger_archive_anchor": "stronger-essay",
                "weaker_archive_anchor": "weaker-essay",
                "traction": 8,
                "craft": 7,
                "publication_power": 8,
                "next_score_blocker": "Practical utility is still thin.",
            },
            (
                "# Atlas Live-Draft Scorecard\n\n"
                "## Whole-Draft Rationale\n\nMeasured against archive standards.\n\n"
                "## Opening Anchor\n\ncandidate:1\n\n"
                "## Middle Anchor\n\ncandidate:5\n\n"
                "## Ending Anchor\n\ncandidate:9\n\n"
                "## Archive Anchors\n\n- Nearby: nearby-essay\n- Stronger: stronger-essay\n- Weaker: weaker-essay\n\n"
                "## Direct Dimensions\n\n- Debate: 7\n- Precision: 7\n- Synthesis: 7\n- Utility: 7\n\n"
                "## Traction\n\n8\n\n"
                "## Craft\n\n7\n\n"
                "## Publication Power\n\n8\n\n"
                "## Next-score Blocker\n\nPractical utility is still thin.\n"
            ),
        )

        write_frontmatter_markdown(
            outputs["decision"],
            {
                "kind": "essay_iteration_decision",
                "package": package_key,
                "revision": revision,
                "judgment_policy": "draft_only",
                "live_draft_path": packet["live_draft_path"],
                "candidate_path": packet["candidate_path"],
                "recommendation": recommendation,
                "promotion_allowed": False,
                "requires_human_approval": True,
                "rewrite_mode": rewrite_mode,
                "stop_gate_status": stop_gate_status,
            },
            (
                "# Promotion Decision\n\n"
                f"## Recommendation\n\n{recommendation}\n\n"
                "## Promotion Gate\n\nHuman review still required.\n\n"
                "## Required Follow-Through\n\nRevise the candidate and rerun validation.\n\n"
                "## Escalation Decision\n\nNot active.\n\n"
                "## Rewrite Mode\n\nNot active.\n\n"
                "## Stop Gate For Next Pass\n\nNot active.\n"
            ),
        )

        return packet, outputs

    def test_init_packet_reuses_existing_non_empty_files_without_force(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            self.run_init(package_key)

            candidate_path = package_dir / f"{package_key}-candidate-r1.md"
            candidate_path.write_text("# Candidate Draft\n\ncustom work\n")

            payload = self.run_init(package_key)
            self.assertEqual(payload["file_status"]["candidate"], "kept")
            self.assertEqual(candidate_path.read_text(), "# Candidate Draft\n\ncustom work\n")

    def test_validator_fails_when_candidate_path_matches_live_draft(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            packet, _ = self.populate_valid_packet(package_dir, package_key)
            packet["candidate_path"] = packet["live_draft_path"]
            (package_dir / f"{package_key}-essay-iteration-packet-r1.json").write_text(json.dumps(packet, indent=2))

            payload = self.run_validator(package_key, expect_success=False)
            self.assertTrue(any("Candidate path must differ" in error for error in payload["errors"]))

    def test_validator_fails_on_missing_blueprint_headings(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            _, outputs = self.populate_valid_packet(package_dir, package_key)
            outputs["blueprint"].write_text("# Hardened Blueprint\n\n## Promise\n\nOnly one heading.\n")

            payload = self.run_validator(package_key, expect_success=False)
            self.assertTrue(any("Blueprint is missing required heading" in error for error in payload["errors"]))

    def test_validator_fails_on_missing_archive_anchors(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            _, outputs = self.populate_valid_packet(package_dir, package_key)
            frontmatter, body = yaml.safe_load(outputs["atlas_scorecard"].read_text().split("---\n", 2)[1]), outputs["atlas_scorecard"].read_text().split("---\n", 2)[2]
            frontmatter["nearby_archive_anchor"] = ""
            write_frontmatter_markdown(outputs["atlas_scorecard"], frontmatter, body)

            payload = self.run_validator(package_key, expect_success=False)
            self.assertTrue(any("nearby_archive_anchor" in error for error in payload["errors"]))

    def test_validator_fails_on_missing_opening_middle_ending_anchors(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            _, outputs = self.populate_valid_packet(package_dir, package_key)
            frontmatter, body = yaml.safe_load(outputs["atlas_scorecard"].read_text().split("---\n", 2)[1]), outputs["atlas_scorecard"].read_text().split("---\n", 2)[2]
            frontmatter["opening_anchor"] = ""
            write_frontmatter_markdown(outputs["atlas_scorecard"], frontmatter, body)

            payload = self.run_validator(package_key, expect_success=False)
            self.assertTrue(any("opening_anchor" in error for error in payload["errors"]))

    def test_validator_fails_on_missing_limits_or_references_section(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            _, outputs = self.populate_valid_packet(package_dir, package_key)
            outputs["candidate"].write_text("# Candidate Draft\n\nNo section headings here.\n")

            payload = self.run_validator(package_key, expect_success=False)
            self.assertTrue(any("limits or borders section" in error for error in payload["errors"]))

    def test_validator_fails_on_em_dash(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            _, outputs = self.populate_valid_packet(package_dir, package_key)
            outputs["candidate"].write_text("# Candidate Draft\n\nThis sentence uses an em dash — which is banned.\n\n## Limits\n\nBounded.\n\n## References\n\nReference.\n")

            payload = self.run_validator(package_key, expect_success=False)
            self.assertTrue(any("literal '—'" in error for error in payload["errors"]))

    def test_validator_fails_when_decision_claims_promotion_under_draft_only(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            packet, outputs = self.populate_valid_packet(package_dir, package_key)
            write_frontmatter_markdown(
                outputs["decision"],
                {
                    "kind": "essay_iteration_decision",
                    "package": package_key,
                    "revision": 1,
                    "judgment_policy": "draft_only",
                    "live_draft_path": packet["live_draft_path"],
                    "candidate_path": packet["candidate_path"],
                    "recommendation": "promote_candidate",
                    "promotion_allowed": True,
                    "requires_human_approval": True,
                },
                "# Promotion Decision\n\n## Recommendation\n\npromote_candidate\n\n## Promotion Gate\n\nNo.\n\n## Required Follow-Through\n\nNone.\n",
            )

            payload = self.run_validator(package_key, expect_success=False)
            self.assertTrue(any("Draft-only packet may not allow promotion" in error for error in payload["errors"]))

    def test_validator_fails_when_publication_power_reaches_nine_under_draft_only(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            _, outputs = self.populate_valid_packet(package_dir, package_key)
            frontmatter, body = yaml.safe_load(outputs["atlas_scorecard"].read_text().split("---\n", 2)[1]), outputs["atlas_scorecard"].read_text().split("---\n", 2)[2]
            frontmatter["publication_power"] = 9
            write_frontmatter_markdown(outputs["atlas_scorecard"], frontmatter, body)

            payload = self.run_validator(package_key, expect_success=False)
            self.assertTrue(any("Publication Power 9 or above" in error for error in payload["errors"]))

    def test_validator_passes_on_known_good_packet(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            self.populate_valid_packet(package_dir, package_key)

            payload = self.run_validator(package_key, expect_success=True)
            self.assertTrue(payload["success"])

    def test_schema_v1_packet_still_valid(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            self.populate_valid_packet(package_dir, package_key, schema_version=None)

            payload = self.run_validator(package_key, expect_success=True)
            self.assertTrue(payload["success"])

    def test_schema_v2_non_escalation_packet_passes(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            packet, outputs = self.populate_valid_packet(
                package_dir,
                package_key,
                schema_version=2,
                north_star_verdict="below_target",
                recommendation="revise_candidate",
                stop_gate_status="inactive",
            )

            payload = self.run_validator(package_key, expect_success=True)
            self.assertTrue(payload["success"])
            self.assertEqual(packet["packet_schema_version"], 2)
            decision_frontmatter, _ = yaml.safe_load(outputs["decision"].read_text().split("---\n", 2)[1]), outputs["decision"].read_text().split("---\n", 2)[2]
            self.assertEqual(decision_frontmatter["stop_gate_status"], "inactive")

    def test_schema_v2_escalation_requires_new_fields(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            _, outputs = self.populate_valid_packet(
                package_dir,
                package_key,
                schema_version=2,
                north_star_verdict="below_north_star",
                recommendation="revise_candidate",
                dominant_blocker_slug="abstract-opening-and-evidence-distribution",
                continue_iteration=True,
                rewrite_mode="compression_with_ignition",
                stop_gate_status="armed",
            )

            review_frontmatter, review_body = yaml.safe_load(outputs["replacement_review"].read_text().split("---\n", 2)[1]), outputs["replacement_review"].read_text().split("---\n", 2)[2]
            review_frontmatter.pop("dominant_blocker_slug", None)
            review_body = review_body.replace("## Dominant Blocker\n\nNot active.\n\n", "")
            write_frontmatter_markdown(outputs["replacement_review"], review_frontmatter, review_body)

            payload = self.run_validator(package_key, expect_success=False)
            self.assertTrue(any("dominant_blocker_slug" in error for error in payload["errors"]))
            self.assertTrue(any("Dominant Blocker" in error for error in payload["errors"]))

    def test_first_escalation_pass_can_arm_stop_gate(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            self.populate_valid_packet(
                package_dir,
                package_key,
                schema_version=2,
                north_star_verdict="below_north_star",
                recommendation="revise_candidate",
                dominant_blocker_slug="abstract-opening-and-evidence-distribution",
                continue_iteration=True,
                rewrite_mode="compression_with_ignition",
                stop_gate_status="armed",
            )

            payload = self.run_validator(package_key, expect_success=True)
            self.assertTrue(payload["success"])

    def test_same_blocker_second_pass_must_fire_stop_gate(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            self.populate_valid_packet(
                package_dir,
                package_key,
                revision=2,
                schema_version=2,
                north_star_verdict="below_north_star",
                recommendation="revise_candidate",
                dominant_blocker_slug="late-compression-and-landing",
                continue_iteration=True,
                rewrite_mode="late_compression_and_landing",
                stop_gate_status="armed",
            )
            self.populate_valid_packet(
                package_dir,
                package_key,
                revision=3,
                schema_version=2,
                north_star_verdict="below_north_star",
                recommendation="revise_candidate",
                dominant_blocker_slug="late-compression-and-landing",
                continue_iteration=True,
                rewrite_mode="late_compression_and_landing",
                stop_gate_status="armed",
            )

            payload = self.run_validator(package_key, expect_success=False)
            self.assertTrue(any("same dominant_blocker_slug persists" in error for error in payload["errors"]))
            self.assertTrue(any("stop_flagship_iteration" in error for error in payload["errors"]))

    def test_changed_blocker_allows_one_more_pass(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            self.populate_valid_packet(
                package_dir,
                package_key,
                revision=2,
                schema_version=2,
                north_star_verdict="below_north_star",
                recommendation="revise_candidate",
                dominant_blocker_slug="abstract-opening-and-evidence-distribution",
                continue_iteration=True,
                rewrite_mode="compression_with_ignition",
                stop_gate_status="armed",
            )
            self.populate_valid_packet(
                package_dir,
                package_key,
                revision=3,
                schema_version=2,
                north_star_verdict="below_north_star",
                recommendation="revise_candidate",
                dominant_blocker_slug="late-compression-and-landing",
                continue_iteration=True,
                rewrite_mode="late_compression_and_landing",
                stop_gate_status="armed",
            )

            payload = self.run_validator(package_key, expect_success=True)
            self.assertTrue(payload["success"])

    def test_immediate_stop_after_first_escalation_is_valid(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            self.populate_valid_packet(
                package_dir,
                package_key,
                schema_version=2,
                north_star_verdict="below_north_star",
                recommendation="revise_candidate",
                dominant_blocker_slug="frame-ceiling",
                continue_iteration=False,
                rewrite_mode="stop_flagship_iteration",
                stop_gate_status="fired",
            )

            payload = self.run_validator(package_key, expect_success=True)
            self.assertTrue(payload["success"])

    def test_support_prefers_latest_revision_artifacts(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            status = yaml.safe_load((package_dir / "status.yaml").read_text())
            (package_dir / f"{package_key}-blueprint-r1.md").write_text("r1")
            (package_dir / f"{package_key}-blueprint-r2.md").write_text("r2")
            (package_dir / f"{package_key}-replacement-review-r1.md").write_text("r1")
            (package_dir / f"{package_key}-replacement-review-r3.md").write_text("r3")

            latest_blueprint = essay_iteration_support.resolve_nearest_blueprint_path(package_dir, status)
            review_artifacts = essay_iteration_support.resolve_review_artifact_paths(package_dir, status)

            self.assertEqual(latest_blueprint.name, f"{package_key}-blueprint-r2.md")
            self.assertEqual(review_artifacts[0].name, f"{package_key}-replacement-review-r3.md")


if __name__ == "__main__":
    unittest.main()
