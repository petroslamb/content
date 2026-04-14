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

    def load_packet(self, package_dir: Path, package_key: str) -> tuple[dict, dict[str, Path]]:
        manifest_path = package_dir / f"{package_key}-essay-iteration-packet-r1.json"
        packet = json.loads(manifest_path.read_text())
        outputs = {
            name: (REPO_ROOT / relpath).resolve()
            for name, relpath in packet["output_paths"].items()
        }
        return packet, outputs

    def populate_valid_packet(self, package_dir: Path, package_key: str) -> tuple[dict, dict[str, Path]]:
        self.run_init(package_key)
        packet, outputs = self.load_packet(package_dir, package_key)

        outputs["blueprint"].write_text(
            "# Hardened Blueprint\n\n"
            "## Promise\n\nA bounded thesis.\n\n"
            "## Spine\n\nA section spine.\n\n"
            "## Paragraph burden\n\nEach section has a job.\n\n"
            "## Evidence burden\n\nBody work and references are separated.\n\n"
            "## Cut order\n\nTrim examples before the core argument.\n\n"
            "## Failure triggers\n\nPromotion is void if the evidence no longer supports the claim.\n"
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
                "revision": 1,
                "judgment_policy": "draft_only",
                "live_draft_path": packet["live_draft_path"],
                "candidate_path": packet["candidate_path"],
                "replacement_verdict": "revise_again",
                "north_star_verdict": "below_target",
                "evidence_anchor_paths": [packet["live_draft_path"], packet["candidate_path"]],
            },
            (
                "# Cold Replacement Review\n\n"
                "## Findings\n\n- `P1`: Anchored finding.\n\n"
                "## Prioritized Issues\n\n- `P1`: Major issue.\n\n"
                "## Scorecard\n\n- Thesis strength: 8\n\n"
                "## Replacement Verdict\n\nRevise again.\n\n"
                "## North-Star Verdict\n\nBelow target.\n\n"
                "## Main Blockers\n\nUtility and limits still need sharpening.\n"
            ),
        )

        write_frontmatter_markdown(
            outputs["atlas_scorecard"],
            {
                "kind": "essay_iteration_atlas_scorecard",
                "package": package_key,
                "revision": 1,
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
                "revision": 1,
                "judgment_policy": "draft_only",
                "live_draft_path": packet["live_draft_path"],
                "candidate_path": packet["candidate_path"],
                "recommendation": "revise_candidate",
                "promotion_allowed": False,
                "requires_human_approval": True,
            },
            (
                "# Promotion Decision\n\n"
                "## Recommendation\n\nrevise_candidate\n\n"
                "## Promotion Gate\n\nHuman review still required.\n\n"
                "## Required Follow-Through\n\nRevise the candidate and rerun validation.\n"
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
