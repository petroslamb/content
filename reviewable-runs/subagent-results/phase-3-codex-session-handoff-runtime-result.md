# Phase 3 Codex Session Handoff Runtime Result

## Changed files

- `scripts/content_agent.py`
- `reviewable-runs/subagent-results/phase-3-codex-session-handoff-runtime-result.md`

## CLI and policy knobs implemented

- Added `./content-agent run --codex-session-handoff {policy,default,defer_to_subagent,same_session}`.
- `policy` and `default` resolve through `harness_policy.yaml` when a `codex_session_handoff` policy mapping is present, with runtime fallback to `defer_to_subagent`.
- Supported policy keys are intentionally tolerant: global `default_mode`/`mode`/`handoff_mode`, workflow overrides under `workflows` or `workflow_overrides`, step overrides under `steps`, `step_overrides`, or an `overrides` list.
- `defer_to_subagent` emits a deterministic request artifact and defers.
- `same_session` preserves compatibility behavior for generic `codex_session` steps: defer without creating a subagent request.
- Explicit `agent_contract` steps still emit their declared request shape; this preserves `essay_iteration.run_cold_replacement_review`.
- Resolved runs and run records now surface `policy_resolution.codex_session_handoff`, selected-step handoff mode/source, and execution handoff evidence.

## Generic request shape

For a `codex_session` step without `agent_contract`, `content-agent` synthesizes:

- `agent_contract.contract_id`: `{workflow_id}.{step_id}.generic_codex_session.v1`
- `agent_contract.contract_kind`: `generic_codex_session`
- `agent_contract.generated_from`: `workflow_id`, `step_id`, `consumes`, `produces`, and `output_targets`
- `expected_artifacts.request_path`: `reviewable-runs/subagent-requests/request-{run_id}-{step_id}.yaml`
- `expected_artifacts.result_path`: `reviewable-runs/subagent-results/result-{run_id}-{step_id}.md`
- `expected_artifacts.integration_decision_path`: `reviewable-runs/integration-decisions/decision-{run_id}-{step_id}.yaml`
- `runtime_behavior.content_agent_spawns_model`: `false`
- `runtime_behavior.defer_after_request`: `true`

The request records package/workflow/run identity, allowed input paths, source hashes for existing inputs, step consumes/produces, output targets, success criteria, failure triggers, and result/integration requirements.

## Verification commands run

- `python3 -m py_compile scripts/content_agent.py`
- `python3 -m unittest tests.test_essay_iteration_packet.EssayIterationPacketTests.test_content_agent_emits_generic_codex_session_request_for_non_review_step tests.test_essay_iteration_packet.EssayIterationPacketTests.test_content_agent_same_session_handoff_mode_defers_without_request_if_supported tests.test_essay_iteration_packet.EssayIterationPacketTests.test_content_agent_emits_subagent_request_without_model_spawn`
- `./content-agent validate --workflow essay_iteration --format json`
- `python3 -m unittest tests.test_essay_iteration_packet`
- `./content-agent run --help`

All verification commands passed. Temporary test run artifacts were cleaned up.
