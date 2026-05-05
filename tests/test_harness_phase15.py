from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import harness  # noqa: E402
import essay_iteration_support  # noqa: E402
import sync_from_archive  # noqa: E402


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
            "blueprint_path": f"publications/{package_key}/{package_key}-blueprint.md",
        },
        "stages": {
            stage: {"done": False, "last_updated": None}
            for stage in harness.STAGES
        },
    }
    (package_dir / "status.yaml").write_text(yaml.safe_dump(status, sort_keys=False))
    (package_dir / f"{package_key}-blueprint.md").write_text(f"# {package_key} Blueprint\n")
    return package_key


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

    def test_guided_stage_resolution_resolves_routed_live_draft(self) -> None:
        resolution = harness.build_stage_resolution("evidence-governance", "article_polish")
        context = {item["name"]: item for item in resolution["required_context"]}

        self.assertEqual(resolution["runner_mode"], "guided")
        self.assertFalse(resolution["can_execute"])
        self.assertEqual(context["canonical live draft"]["status"], "resolved")
        self.assertEqual(
            context["package artifact surface with NotebookLM or local media outputs"]["status"],
            "resolved",
        )

    def test_stage_resolution_for_essay_iteration_returns_packet_metadata(self) -> None:
        resolution = harness.build_stage_resolution(
            "evidence-governance/your-ai-is-confidently-wrong-and",
            "essay_iteration",
        )

        self.assertEqual(resolution["runner_mode"], "hybrid")
        self.assertEqual(resolution["launch_mode"], "scaffold_only")
        self.assertTrue(resolution["requires_approval"])
        self.assertTrue(resolution["can_execute"])
        self.assertEqual(resolution["judgment_policy"], "draft_only")
        self.assertTrue(
            any(template.endswith("hardened_blueprint_template.md") for template in resolution["packet_templates"])
        )
        self.assertEqual(
            resolution["package_context_paths"]["live_draft_path"],
            "publications/evidence-governance/your-ai-is-confidently-wrong-and/your-ai-is-confidently-wrong-and.md",
        )
        self.assertEqual(
            resolution["package_context_paths"]["parent_package_readme_path"],
            "publications/evidence-governance/README.md",
        )
        self.assertTrue(
            resolution["packet_paths"]["manifest"].endswith(
                "your-ai-is-confidently-wrong-and-essay-iteration-packet-r4.json"
            )
        )
        self.assertTrue(
            any(command.startswith(
                "npm run check:essay-iteration -- --package evidence-governance/your-ai-is-confidently-wrong-and"
            ) for command in resolution["validator_commands"])
        )

    def test_next_action_returns_distribution_for_illusion_of_swarm(self) -> None:
        payload = harness.build_next_action("illusion-of-swarm")

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
            ), mock.patch.object(
                essay_iteration_support, "REPO_ROOT", tmp_root
            ), mock.patch.object(
                essay_iteration_support, "PUBLICATIONS_DIR", publications_dir
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
        resolution = harness.build_stage_resolution(
            "evidence-governance/your-ai-is-confidently-wrong-and",
            "essay_iteration",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch.object(harness, "LOGS_DIR", Path(tmpdir)):
                launch_pack_path = harness.emit_launch_pack(resolution)
                payload = json.loads(launch_pack_path.read_text())

        self.assertTrue(launch_pack_path.name.endswith("_launch-pack.json"))
        self.assertEqual(payload["kind"], "harness_launch_pack")
        self.assertEqual(payload["stage"], "essay_iteration")
        self.assertEqual(payload["package"], "evidence-governance/your-ai-is-confidently-wrong-and")
        self.assertEqual(payload["judgment_policy"], "draft_only")
        self.assertTrue(payload["packet_paths"]["manifest"].endswith("-essay-iteration-packet-r4.json"))
        self.assertTrue(payload["prohibited_moves"])

    def test_content_agent_validate_rejects_missing_package(self) -> None:
        result = subprocess.run(
            [
                "./content-agent",
                "validate",
                "--workflow",
                "substack_publishing",
                "--package",
                "does-not-exist",
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
        self.assertFalse(payload["success"])
        self.assertIn("does-not-exist", payload["error"])

    def test_essay_iteration_resolution_suggests_content_agent_scaffold(self) -> None:
        resolution = harness.build_stage_resolution(
            "evidence-governance/your-ai-is-confidently-wrong-and",
            "essay_iteration",
        )

        self.assertTrue(
            any(
                command.startswith("./content-agent run --workflow essay_iteration")
                for command in resolution["suggested_commands"]
            )
        )
        self.assertFalse(any("stage:run" in command for command in resolution["suggested_commands"]))

    def test_archive_sync_copies_referenced_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            package_dir = tmp_root / "publications" / "demo"
            package_dir.mkdir(parents=True)
            archive_dir = tmp_root / "publication_strategy_and_archive" / "substack_archive"
            archive_assets_dir = archive_dir / "assets"
            archive_assets_dir.mkdir(parents=True)

            archive_markdown = archive_dir / "demo.md"
            archive_markdown.write_text(
                "# Demo\n\n![](assets/asset-one.png)\n\n![](assets/asset-two.jpeg)\n\n![](assets/asset-one.png)\n"
            )
            (archive_assets_dir / "asset-one.png").write_text("one")
            (archive_assets_dir / "asset-two.jpeg").write_text("two")

            destination = package_dir / "demo.md"

            with mock.patch.object(sync_from_archive, "REPO_ROOT", tmp_root), mock.patch.object(
                sync_from_archive, "ARCHIVE_ASSETS_DIR", archive_assets_dir
            ):
                sync_from_archive.shutil.copy2(archive_markdown, destination)
                copied_assets = sync_from_archive.sync_assets_for_markdown(destination)

                copied_names = sorted(path.name for path in copied_assets)
                self.assertEqual(copied_names, ["asset-one.png", "asset-two.jpeg"])
                self.assertTrue((destination.parent / "assets" / "asset-one.png").exists())
                self.assertTrue((destination.parent / "assets" / "asset-two.jpeg").exists())


if __name__ == "__main__":
    unittest.main()
