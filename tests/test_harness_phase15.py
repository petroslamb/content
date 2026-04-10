from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import harness  # noqa: E402
import next_action  # noqa: E402


class HarnessPhase15Tests(unittest.TestCase):
    maxDiff = None

    def test_stage_resolution_uses_status_config_for_hybrid_stage(self) -> None:
        resolution = harness.build_stage_resolution(
            "neural-architectures/neural-architecture-design-as-a-compositional-32e",
            "substack_publishing",
        )
        context = {item["name"]: item for item in resolution["required_context"]}

        self.assertEqual(resolution["runner_mode"], "hybrid")
        self.assertFalse(resolution["can_execute"])
        self.assertTrue(resolution["requires_approval"])
        self.assertEqual(
            context["config.markdown_path"]["value"],
            "publications/neural-architectures/neural-architecture-design-as-a-compositional-32e/neural-architecture-design-as-a-compositional-32e.md",
        )
        self.assertEqual(context["config.substack_url"]["value"], "https://lambpetros.substack.com")
        self.assertEqual(context["config.substack_post_id"]["value"], 180114871)

    def test_guided_stage_resolution_reports_missing_live_draft(self) -> None:
        resolution = harness.build_stage_resolution("evidence-governance", "article_polish")
        context = {item["name"]: item for item in resolution["required_context"]}

        self.assertEqual(resolution["runner_mode"], "guided")
        self.assertFalse(resolution["can_execute"])
        self.assertEqual(context["canonical live draft"]["status"], "missing")
        self.assertEqual(
            context["package artifact surface with NotebookLM or local media outputs"]["status"],
            "missing",
        )

    def test_next_action_returns_distribution_for_illusion_of_swarm(self) -> None:
        payload = next_action.build_next_action("illusion-of-swarm")

        self.assertEqual(payload["next_stage"], "distribution")
        self.assertEqual(payload["runner_mode"], "guided")
        self.assertFalse(payload["can_execute"])

    def test_initialize_package_prefers_research_for_idea_only_package(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            publications_dir = tmp_root / "publications"
            publications_dir.mkdir()

            with mock.patch.object(harness, "REPO_ROOT", tmp_root), mock.patch.object(
                harness, "PUBLICATIONS_DIR", publications_dir
            ):
                payload = harness.initialize_package("A compositional essay about tool memory")
                status_path = publications_dir / payload["package"] / "status.yaml"
                status = harness.load_yaml_file(status_path)
                next_stage = harness.next_stage_for_package(publications_dir / payload["package"], status)

        self.assertEqual(payload["next_stage"], "research")
        self.assertEqual(next_stage, "research")
        self.assertEqual(
            status["config"]["markdown_path"],
            f"publications/{payload['package']}/{payload['package']}.md",
        )

    def test_emit_launch_pack_writes_json_packet(self) -> None:
        resolution = harness.build_stage_resolution("illusion-of-swarm", "article_polish")

        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch.object(harness, "LOGS_DIR", Path(tmpdir)):
                launch_pack_path = harness.emit_launch_pack(resolution)
                payload = json.loads(launch_pack_path.read_text())

        self.assertTrue(launch_pack_path.name.endswith("_launch-pack.json"))
        self.assertEqual(payload["kind"], "harness_launch_pack")
        self.assertEqual(payload["stage"], "article_polish")
        self.assertEqual(payload["package"], "illusion-of-swarm")

    def test_stage_run_refuses_hybrid_execution(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/run_stage.py",
                "--package",
                "neural-architectures/neural-architecture-design-as-a-compositional-32e",
                "--stage",
                "substack_publishing",
                "--execute",
                "--format",
                "json",
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertIn("not executable", payload["error"])
        self.assertTrue(any("hybrid" in issue for issue in payload["blocking_issues"]))


if __name__ == "__main__":
    unittest.main()
