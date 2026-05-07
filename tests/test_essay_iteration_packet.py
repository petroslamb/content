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
    (package_dir / "blueprint.md").write_text("# Blueprint\n\n## Promise\n\nA bounded promise.\n")
    draft_path.write_text(f"# {package_key}\n\n## Limits\n\n## References\n")

    status = {
        "kind": "leaf",
        "publication": package_key,
        "revision": 1,
        "config": {
            "markdown_path": f"publications/{package_key}/{package_key}.md",
            "blueprint_path": "blueprint.md",
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

    def run_content_agent(
        self,
        package_key: str,
        run_id: str,
        start_at: str,
        *,
        extra_args: list[str] | None = None,
    ) -> dict:
        command = [
            "./content-agent",
            "run",
            "--workflow",
            "essay_iteration",
            "--package",
            package_key,
            "--start-at",
            start_at,
            "--run-id",
            run_id,
            "--format",
            "json",
        ]
        command.extend(extra_args or [])
        result = subprocess.run(
            command,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        return json.loads(result.stdout)

    def codex_handoff_mode_arg(self) -> str | None:
        result = subprocess.run(
            ["./content-agent", "run", "--help"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        for arg in (
            "--codex-session-handoff-mode",
            "--codex-session-handoff",
            "--codex-session-mode",
            "--handoff-mode",
        ):
            if arg in result.stdout:
                return arg
        return None

    def cleanup_run_artifacts(self, run_id: str) -> None:
        for dirname in (
            "resolved-runs",
            "logs",
            "gates",
            "subagent-requests",
            "subagent-results",
            "integration-decisions",
        ):
            directory = REPO_ROOT / "reviewable-runs" / dirname
            if not directory.exists():
                continue
            for path in directory.iterdir():
                if path.is_file() and run_id in path.name:
                    path.unlink(missing_ok=True)

    def replacement_source_hashes(self, packet: dict) -> dict[str, dict[str, str]]:
        return {
            relpath: {
                "type": "file_sha256",
                "sha256": essay_iteration_support.file_sha256(REPO_ROOT / relpath),
            }
            for relpath in (
                packet["packet_manifest_path"],
                packet["live_draft_path"],
                packet["candidate_path"],
            )
        }

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
        manifest_path = package_dir / "iterations" / f"r{revision}" / f"{package_key}-essay-iteration-packet-r{revision}.json"
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
        manifest_path = package_dir / "iterations" / f"r{revision}" / f"{package_key}-essay-iteration-packet-r{revision}.json"
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
            outputs["prewrite_gate"],
            {
                "kind": "essay_iteration_prewrite_gate",
                "package": package_key,
                "revision": revision,
                "judgment_policy": "draft_only",
                "live_draft_path": packet["live_draft_path"],
                "candidate_path": packet["candidate_path"],
                "writability_verdict": "writable",
                "candidate_authorized": True,
                "dominant_blocker_slug": "",
                "supporting_artifact_paths": [packet["input_paths"]["governing_brief_path"]],
            },
            (
                "# Essay Prewrite Gate\n\n"
                "## Promise\n\nA bounded thesis.\n\n"
                "## Spine\n\nA section spine.\n\n"
                "## Paragraph burden\n\nEach section has a job.\n\n"
                "## Evidence burden\n\nBody work and references are separated.\n\n"
                "## Cut order\n\nTrim examples before the core argument.\n\n"
                "## Failure triggers\n\nPromotion is void if the evidence no longer supports the claim.\n\n"
                "## Claim-State Gate\n\nThe governing brief and blueprint authorize the candidate.\n\n"
                "## Writability Verdict\n\nWritable; the candidate is authorized.\n\n"
                "## Required Follow-Through\n\nComplete the candidate review packet.\n"
            ),
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

        write_frontmatter_markdown(
            outputs["ceiling_report"],
            {
                "kind": "object_ceiling_report",
                "package": package_key,
                "revision": revision,
                "live_draft_path": packet["live_draft_path"],
                "terminal_candidate_path": packet["candidate_path"],
                "terminal_replacement_review_path": packet["output_paths"]["replacement_review"],
                "terminal_decision_path": packet["output_paths"]["decision"],
                "dominant_blocker_slug": dominant_blocker_slug,
                "ceiling_verdict": "object_ceiling",
                "effort_verdict": "hard_enough",
                "next_route": "post_ceiling_pivot",
            },
            (
                "# Ceiling Report\n\n"
                "## Verdict\n\nThe object hit a real ceiling.\n\n"
                "## Iteration Chronology\n\nThe candidate was tested through the active packet.\n\n"
                "## Blocker Timeline\n\nThe dominant blocker persisted through the stop decision.\n\n"
                "## Effort Audit\n\nThe pass did enough work to justify stopping.\n\n"
                "## What Survived\n\n- The reusable thesis pressure.\n\n"
                "## What Did Not Survive\n\n- The flagship object.\n\n"
                "## Lessons Learned\n\n- Route successor work through a new package.\n\n"
                "## Next Route\n\nPost-ceiling pivot.\n"
            ),
        )

        return packet, outputs

    def test_init_packet_reuses_existing_non_empty_files_without_force(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            self.run_init(package_key)

            candidate_path = package_dir / "iterations" / "r1" / f"{package_key}-candidate-r1.md"
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
            self.write_packet_manifest(package_dir, package_key, 1, packet)

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

    def test_validator_fails_on_duplicate_template_tail_scaffold_residue(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            _, outputs = self.populate_valid_packet(package_dir, package_key)
            outputs["candidate"].write_text(
                "# Candidate Draft\n\n"
                "A concrete opening paragraph.\n\n"
                "## Limits\n\nThis essay stays bounded.\n\n"
                "## References\n\nOne real reference.\n\n"
                "## Limits\n\nState the boundaries, counterpressure, or what the essay will not claim.\n\n"
                "## References\n\nInclude real endmatter or references, not just a companion pointer.\n"
            )

            payload = self.run_validator(package_key, expect_success=False)
            self.assertTrue(any("scaffold residue" in error for error in payload["errors"]))
            self.assertTrue(any("repeats limits" in error for error in payload["errors"]))

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

    def test_replacement_agent_contract_accepts_generated_artifact_shape(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            packet, _ = self.populate_valid_packet(package_dir, package_key)
            packet["output_paths"]["manifest"] = packet["packet_manifest_path"]

            with tempfile.TemporaryDirectory() as artifact_dir:
                artifact_root = Path(artifact_dir)
                result_path = artifact_root / "cold-result.md"
                integration_path = artifact_root / "integration.yaml"
                packet["output_paths"]["cold_replacement_review_agent_result"] = str(result_path)
                packet["output_paths"]["cold_replacement_review_integration_decision"] = str(integration_path)

                source_hashes = {
                    packet["packet_manifest_path"]: {
                        "type": "file_sha256",
                        "sha256": essay_iteration_support.file_sha256(REPO_ROOT / packet["packet_manifest_path"]),
                    },
                    packet["live_draft_path"]: {
                        "type": "file_sha256",
                        "sha256": essay_iteration_support.file_sha256(REPO_ROOT / packet["live_draft_path"]),
                    },
                    packet["candidate_path"]: {
                        "type": "file_sha256",
                        "sha256": essay_iteration_support.file_sha256(REPO_ROOT / packet["candidate_path"]),
                    },
                }
                result_frontmatter = {
                    "kind": "subagent_result",
                    "schema_version": 1,
                    "request_id": "request-1",
                    "result_id": "result-1",
                    "package": {
                        "path": f"publications/{package_key}",
                        "status_path": f"publications/{package_key}/status.yaml",
                    },
                    "workflow": {
                        "workflow_id": "essay_iteration",
                        "step_id": "run_cold_replacement_review",
                    },
                    "run": {"run_id": "run-1"},
                    "verdict": "pass",
                    "source_hashes": source_hashes,
                }
                write_frontmatter_markdown(
                    result_path,
                    result_frontmatter,
                    "# Result\n\n## Findings\n\n- line-grounded check.\n",
                )
                integration_path.write_text(
                    yaml.safe_dump(
                        {
                            "kind": "integration_decision",
                            "schema_version": 1,
                            "request_id": "request-1",
                            "package": {
                                "path": f"publications/{package_key}",
                                "status_path": f"publications/{package_key}/status.yaml",
                            },
                            "workflow": {
                                "workflow_id": "essay_iteration",
                                "step_id": "run_cold_replacement_review",
                            },
                            "run": {"run_id": "run-1"},
                            "decision": "accept_pass",
                            "accepted_result_ids": ["result-1"],
                            "rejected_result_ids": [],
                            "source_hashes": source_hashes,
                        },
                        sort_keys=False,
                    )
                )

                errors, details = essay_iteration_support.validate_replacement_agent_contract(
                    packet,
                    require_present=True,
                    require_allowed=True,
                )

            self.assertEqual(errors, [])
            self.assertEqual(details["cold_review_verdict"], "pass")
            self.assertEqual(details["integration_decision"], "accept_pass")

    def test_replacement_agent_contract_blocks_stale_source_hashes(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            packet, _ = self.populate_valid_packet(package_dir, package_key)
            packet["output_paths"]["manifest"] = packet["packet_manifest_path"]

            with tempfile.TemporaryDirectory() as artifact_dir:
                artifact_root = Path(artifact_dir)
                result_path = artifact_root / "stale-cold-result.md"
                integration_path = artifact_root / "stale-integration.yaml"
                packet["output_paths"]["cold_replacement_review_agent_result"] = str(result_path)
                packet["output_paths"]["cold_replacement_review_integration_decision"] = str(integration_path)

                current_hashes = self.replacement_source_hashes(packet)
                stale_result_hashes = {key: dict(value) for key, value in current_hashes.items()}
                stale_result_hashes[packet["candidate_path"]] = {
                    "type": "file_sha256",
                    "sha256": "0" * 64,
                }
                write_frontmatter_markdown(
                    result_path,
                    {
                        "kind": "subagent_result",
                        "schema_version": 1,
                        "request_id": "request-1",
                        "result_id": "result-1",
                        "package": {"path": f"publications/{package_key}"},
                        "workflow": {
                            "workflow_id": "essay_iteration",
                            "step_id": "run_cold_replacement_review",
                        },
                        "run": {"run_id": "run-1"},
                        "verdict": "pass",
                        "source_hashes": stale_result_hashes,
                    },
                    "# Result\n\n## Findings\n\n- stale candidate hash fixture.\n",
                )
                integration_path.write_text(
                    yaml.safe_dump(
                        {
                            "kind": "integration_decision",
                            "schema_version": 1,
                            "request_id": "request-1",
                            "package": {"path": f"publications/{package_key}"},
                            "workflow": {
                                "workflow_id": "essay_iteration",
                                "step_id": "run_cold_replacement_review",
                            },
                            "run": {"run_id": "run-1"},
                            "decision": "accept_pass",
                            "accepted_result_ids": ["result-1"],
                            "rejected_result_ids": [],
                            "source_hashes": current_hashes,
                        },
                        sort_keys=False,
                    )
                )

                errors, _ = essay_iteration_support.validate_replacement_agent_contract(
                    packet,
                    require_present=True,
                    require_allowed=True,
                )

            self.assertTrue(
                any("Cold-review result candidate sha256 is stale" in error for error in errors),
                errors,
            )

    def test_replacement_agent_contract_blocks_malformed_result_artifact(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            packet, _ = self.populate_valid_packet(package_dir, package_key)
            packet["output_paths"]["manifest"] = packet["packet_manifest_path"]

            with tempfile.TemporaryDirectory() as artifact_dir:
                artifact_root = Path(artifact_dir)
                result_path = artifact_root / "malformed-cold-result.md"
                integration_path = artifact_root / "malformed-integration.yaml"
                packet["output_paths"]["cold_replacement_review_agent_result"] = str(result_path)
                packet["output_paths"]["cold_replacement_review_integration_decision"] = str(integration_path)

                source_hashes = self.replacement_source_hashes(packet)
                result_path.write_text("---\nkind: [unterminated\n---\n# Result\n")
                integration_path.write_text(
                    yaml.safe_dump(
                        {
                            "kind": "integration_decision",
                            "schema_version": 1,
                            "request_id": "request-1",
                            "package": {"path": f"publications/{package_key}"},
                            "workflow": {
                                "workflow_id": "essay_iteration",
                                "step_id": "run_cold_replacement_review",
                            },
                            "run": {"run_id": "run-1"},
                            "decision": "accept_pass",
                            "accepted_result_ids": ["result-1"],
                            "rejected_result_ids": [],
                            "source_hashes": source_hashes,
                        },
                        sort_keys=False,
                    )
                )

                errors, _ = essay_iteration_support.validate_replacement_agent_contract(
                    packet,
                    require_present=True,
                    require_allowed=True,
                )

            self.assertTrue(
                any("Invalid replacement agent contract artifact" in error for error in errors),
                errors,
            )

    def test_content_agent_emits_subagent_request_without_model_spawn(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            self.populate_valid_packet(package_dir, package_key)
            run_id = f"test-agent-contract-{package_key}"
            cleanup_paths = [
                REPO_ROOT / "reviewable-runs" / "resolved-runs" / f"{run_id}.yaml",
                REPO_ROOT / "reviewable-runs" / "logs" / f"{run_id}.yaml",
                REPO_ROOT / "reviewable-runs" / "subagent-requests" / f"{run_id}-run-cold-replacement-review.yaml",
            ]
            for path in cleanup_paths:
                path.unlink(missing_ok=True)

            try:
                result = subprocess.run(
                    [
                        "./content-agent",
                        "run",
                        "--workflow",
                        "essay_iteration",
                        "--package",
                        package_key,
                        "--start-at",
                        "run_cold_replacement_review",
                        "--run-id",
                        run_id,
                        "--format",
                        "json",
                    ],
                    cwd=REPO_ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
                payload = json.loads(result.stdout)
                self.assertEqual(payload["terminal_status"], "deferred")
                request_path = REPO_ROOT / payload["subagent_request_path"]
                request = yaml.safe_load(request_path.read_text())

                self.assertFalse(request["runtime_behavior"]["content_agent_spawns_model"])
                self.assertEqual(request["workflow"]["step_id"], "run_cold_replacement_review")
                self.assertTrue(
                    request["expected_artifacts"]["result_path"].startswith("reviewable-runs/subagent-results/")
                )
                self.assertTrue(
                    request["expected_artifacts"]["integration_decision_path"].startswith(
                        "reviewable-runs/integration-decisions/"
                    )
                )
                self.assertIn("public_object", request["plot_contract_requirements"]["required_content"])
            finally:
                for path in cleanup_paths:
                    path.unlink(missing_ok=True)

    def test_content_agent_emits_generic_codex_session_request_for_non_review_step(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        mode_arg = self.codex_handoff_mode_arg()
        extra_args = [mode_arg, "defer_to_subagent"] if mode_arg else []
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            packet, _ = self.populate_valid_packet(package_dir, package_key)
            run_id = f"test-generic-codex-handoff-{package_key}"
            self.cleanup_run_artifacts(run_id)

            try:
                payload = self.run_content_agent(
                    package_key,
                    run_id,
                    "harden_blueprint",
                    extra_args=extra_args,
                )
                request_relpath = payload.get("subagent_request_path")
                if request_relpath is None:
                    self.skipTest("content-agent runtime does not yet emit generic codex_session requests")

                self.assertEqual(payload["terminal_status"], "deferred")
                request_path = REPO_ROOT / request_relpath
                request = yaml.safe_load(request_path.read_text())
                self.assertEqual(request["kind"], "subagent_request")
                self.assertEqual(request["workflow"]["workflow_id"], "essay_iteration")
                self.assertEqual(request["workflow"]["step_id"], "harden_blueprint")
                self.assertEqual(request["step"]["mode"], "codex_session")
                self.assertFalse(request["runtime_behavior"]["content_agent_spawns_model"])
                self.assertTrue(request["runtime_behavior"]["defer_after_request"])
                self.assertIsInstance(request["agent_contract"], dict)
                self.assertNotEqual(
                    request["agent_contract"].get("contract_id"),
                    "essay_iteration.cold_replacement_review.v1",
                )
                self.assertTrue(
                    request["expected_artifacts"]["result_path"].startswith("reviewable-runs/subagent-results/")
                )
                self.assertTrue(
                    request["expected_artifacts"]["integration_decision_path"].startswith(
                        "reviewable-runs/integration-decisions/"
                    )
                )
                self.assertIn(packet["packet_manifest_path"], request["source_hashes"])
                output_ids = {item["id"] for item in request["output_targets"]}
                self.assertIn("hardened_blueprint", output_ids)
            finally:
                self.cleanup_run_artifacts(run_id)

    def test_content_agent_same_session_handoff_mode_defers_without_request_if_supported(self) -> None:
        mode_arg = self.codex_handoff_mode_arg()
        if mode_arg is None:
            self.skipTest("content-agent does not expose a codex_session handoff-mode override")

        publications_dir = REPO_ROOT / "publications"
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            self.populate_valid_packet(package_dir, package_key)
            run_id = f"test-same-session-handoff-{package_key}"
            self.cleanup_run_artifacts(run_id)

            try:
                payload = self.run_content_agent(
                    package_key,
                    run_id,
                    "harden_blueprint",
                    extra_args=[mode_arg, "same_session"],
                )
                self.assertEqual(payload["terminal_status"], "deferred")
                self.assertIsNone(payload["subagent_request_path"])
                requests_dir = REPO_ROOT / "reviewable-runs" / "subagent-requests"
                matching_requests = [
                    path
                    for path in requests_dir.iterdir()
                    if path.is_file() and run_id in path.name
                ] if requests_dir.exists() else []
                self.assertEqual(matching_requests, [])
            finally:
                self.cleanup_run_artifacts(run_id)

    def test_replacement_agent_contract_discovers_paths_from_generated_request(self) -> None:
        publications_dir = REPO_ROOT / "publications"
        requests_dir = REPO_ROOT / "reviewable-runs" / "subagent-requests"
        requests_dir.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=publications_dir, prefix="tmp-essay-packet-") as tmpdir:
            package_dir = Path(tmpdir)
            package_key = create_temp_leaf_package(package_dir)
            packet, _ = self.populate_valid_packet(package_dir, package_key)
            packet["output_paths"]["manifest"] = packet["packet_manifest_path"]
            request_path = requests_dir / f"test-agent-contract-request-{package_key}.yaml"

            with tempfile.TemporaryDirectory() as artifact_dir:
                artifact_root = Path(artifact_dir)
                result_path = artifact_root / "cold-result.md"
                integration_path = artifact_root / "integration.yaml"
                source_hashes = {
                    packet["packet_manifest_path"]: {
                        "type": "file_sha256",
                        "sha256": essay_iteration_support.file_sha256(REPO_ROOT / packet["packet_manifest_path"]),
                    },
                    packet["live_draft_path"]: {
                        "type": "file_sha256",
                        "sha256": essay_iteration_support.file_sha256(REPO_ROOT / packet["live_draft_path"]),
                    },
                    packet["candidate_path"]: {
                        "type": "file_sha256",
                        "sha256": essay_iteration_support.file_sha256(REPO_ROOT / packet["candidate_path"]),
                    },
                }
                write_frontmatter_markdown(
                    result_path,
                    {
                        "kind": "subagent_result",
                        "schema_version": 1,
                        "request_id": "request-1",
                        "result_id": "result-1",
                        "package": {"path": f"publications/{package_key}"},
                        "workflow": {
                            "workflow_id": "essay_iteration",
                            "step_id": "run_cold_replacement_review",
                        },
                        "run": {"run_id": "run-1"},
                        "verdict": "pass",
                        "source_hashes": source_hashes,
                    },
                    "# Result\n",
                )
                integration_path.write_text(
                    yaml.safe_dump(
                        {
                            "kind": "integration_decision",
                            "schema_version": 1,
                            "request_id": "request-1",
                            "package": {"path": f"publications/{package_key}"},
                            "workflow": {
                                "workflow_id": "essay_iteration",
                                "step_id": "run_cold_replacement_review",
                            },
                            "run": {"run_id": "run-1"},
                            "decision": "accept_pass",
                            "accepted_result_ids": ["result-1"],
                            "rejected_result_ids": [],
                            "source_hashes": source_hashes,
                        },
                        sort_keys=False,
                    )
                )
                request_path.write_text(
                    yaml.safe_dump(
                        {
                            "kind": "subagent_request",
                            "schema_version": 1,
                            "request_id": "request-1",
                            "agent_contract": {"contract_id": "essay_iteration.cold_replacement_review.v1"},
                            "package": {"path": f"publications/{package_key}"},
                            "workflow": {
                                "workflow_id": "essay_iteration",
                                "step_id": "run_cold_replacement_review",
                            },
                            "run": {"run_id": "run-1"},
                            "allowed_input_paths": [
                                {"id": "packet_manifest", "paths": [packet["packet_manifest_path"]]},
                            ],
                            "source_hashes": source_hashes,
                            "expected_artifacts": {
                                "result_path": str(result_path),
                                "integration_decision_path": str(integration_path),
                            },
                        },
                        sort_keys=False,
                    )
                )

                try:
                    errors, details = essay_iteration_support.validate_replacement_agent_contract(
                        packet,
                        require_present=True,
                        require_allowed=True,
                    )
                finally:
                    request_path.unlink(missing_ok=True)

            self.assertEqual(errors, [])
            self.assertEqual(details["agent_request_path"], f"reviewable-runs/subagent-requests/{request_path.name}")

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
            (package_dir / "iterations" / "r1").mkdir(parents=True)
            (package_dir / "iterations" / "r2").mkdir(parents=True)
            (package_dir / "iterations" / "r3").mkdir(parents=True)
            (package_dir / "iterations" / "r1" / f"{package_key}-blueprint-r1.md").write_text("r1")
            (package_dir / "iterations" / "r2" / f"{package_key}-blueprint-r2.md").write_text("r2")
            (package_dir / "iterations" / "r1" / f"{package_key}-replacement-review-r1.md").write_text("r1")
            (package_dir / "iterations" / "r3" / f"{package_key}-replacement-review-r3.md").write_text("r3")

            latest_blueprint = essay_iteration_support.resolve_nearest_blueprint_path(package_dir, status)
            review_artifacts = essay_iteration_support.resolve_review_artifact_paths(package_dir, status)

            self.assertEqual(latest_blueprint.name, f"{package_key}-blueprint-r2.md")
            self.assertEqual(review_artifacts[0].name, f"{package_key}-replacement-review-r3.md")


if __name__ == "__main__":
    unittest.main()
