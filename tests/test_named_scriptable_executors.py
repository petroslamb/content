from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import check_workflow_yaml_contracts  # noqa: E402
from lifecycle import WORKFLOWS_DIR, load_gate_contracts  # noqa: E402


class NamedScriptableExecutorTests(unittest.TestCase):
    maxDiff = None

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

    def run_content_agent(self, args: list[str], run_id: str) -> dict:
        self.cleanup_run_artifacts(run_id)
        result = subprocess.run(
            ["./content-agent", "run", *args, "--run-id", run_id, "--format", "json"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_full_reddit_run_passes_context_admission_then_emits_subagent_request(self) -> None:
        run_id = "test-named-executor-reddit-discussion"
        try:
            payload = self.run_content_agent(
                [
                    "--workflow",
                    "reddit_discussion_lab",
                    "--package",
                    "evidence-governance/your-ai-is-confidently-wrong-and",
                    "--codex-session-handoff",
                    "defer_to_subagent",
                ],
                run_id,
            )

            self.assertEqual(payload["terminal_status"], "deferred")
            self.assertIn("emitted generic codex_session subagent request", payload["stop_reason"])
            self.assertIsNotNone(payload["subagent_request_path"])
            self.assertEqual(payload["scriptable_steps_executed"], 1)
            self.assertEqual(payload["command_results"][0]["status"], "passed")
            self.assertEqual(payload["command_results"][0]["executor_name"], "content-agent context-admission")
        finally:
            self.cleanup_run_artifacts(run_id)

    def test_run_record_named_executor_completes_without_shell_command(self) -> None:
        run_id = "test-named-executor-run-record"
        try:
            payload = self.run_content_agent(
                [
                    "--workflow",
                    "reddit_discussion_lab",
                    "--package",
                    "evidence-governance/your-ai-is-confidently-wrong-and",
                    "--start-at",
                    "record_handoff",
                ],
                run_id,
            )

            self.assertEqual(payload["terminal_status"], "completed")
            self.assertEqual(payload["scriptable_steps_executed"], 1)
            self.assertEqual(payload["command_results"][0]["status"], "passed")
            self.assertEqual(payload["command_results"][0]["executor_name"], "content-agent run-record")
        finally:
            self.cleanup_run_artifacts(run_id)

    def test_archive_sync_route_named_executor_defers_without_running_sync(self) -> None:
        run_id = "test-named-executor-route-archive-sync"
        try:
            payload = self.run_content_agent(
                [
                    "--workflow",
                    "substack_publishing",
                    "--package",
                    "neural-architectures/neural-architecture-design-as-a-compositional-32e",
                    "--start-at",
                    "archive_follow_through",
                    "--input",
                    "release_gate_verdict=test-approved-for-route-regression",
                    "--input",
                    "existing_substack_draft=test-draft-readback-for-route-regression",
                ],
                run_id,
            )

            self.assertEqual(payload["terminal_status"], "deferred")
            self.assertIn("Archive sync is a separate governed workflow", payload["stop_reason"])
            self.assertEqual(payload["scriptable_steps_executed"], 1)
            self.assertEqual(payload["command_results"][0]["status"], "deferred")
            self.assertEqual(payload["command_results"][0]["executor_name"], "content-agent route archive_sync")
        finally:
            self.cleanup_run_artifacts(run_id)

    def test_unsupported_named_executor_fails_workflow_yaml_validation(self) -> None:
        with tempfile.TemporaryDirectory(dir=WORKFLOWS_DIR, prefix="tmp-named-executor-") as tmpdir:
            temp_workflow_dir = Path(tmpdir)
            shutil.copy2(WORKFLOWS_DIR / "reddit-discussion-lab" / "README.md", temp_workflow_dir / "README.md")
            contract_path = temp_workflow_dir / "workflow.yaml"
            contract = yaml.safe_load((WORKFLOWS_DIR / "reddit-discussion-lab" / "workflow.yaml").read_text())
            contract["steps"][0]["executor"]["named"] = "content-agent unsupported-sentinel"
            contract_path.write_text(yaml.safe_dump(contract, sort_keys=False))

            errors = check_workflow_yaml_contracts.validate_contract(
                contract_path,
                set(load_gate_contracts().keys()),
            )

        self.assertTrue(any("executor.named 'content-agent unsupported-sentinel'" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
