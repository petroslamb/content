---
kind: subagent_result
schema_version: 1
request_id: phase-3-codex-session-handoff:policy
agent_type: worker
completed_at: '2026-05-07'
request_path: reviewable-runs/subagent-requests/phase-3-codex-session-handoff-policy-request.yaml
---
# Phase 3 Codex Session Handoff Policy Result

## Summary

Defined the narrow Phase 3 policy surface for codex-session handoff behavior. The policy keeps `content-agent` deterministic: it can resolve handoff mode, emit request artifacts, validate returned artifacts, and defer, but it does not spawn models or perform model-mediated work.

The existing cold replacement review remains the first gate-critical explicit `agent_contract`.

## Changed Files

- `harness_policy.yaml`
- `reviewable-runs/README.md`
- `workflows/essay-iteration/workflow.yaml`
- `reviewable-runs/subagent-results/phase-3-codex-session-handoff-policy-result.md`

## Policy Keys Added Or Changed

- `harness_policy.yaml:codex_session_handoff`
  - `default_mode: defer_to_subagent`
  - `compatibility_mode: same_session`
  - `allowed_modes: policy_default, defer_to_subagent, same_session`
  - `resolution_order`: step override, workflow default, root policy default
  - `runtime_contract`: denies model spawning and direct Codex execution from `content-agent`; allows deterministic request emission and result validation
  - `artifact_paths`: points to `reviewable-runs/subagent-requests/`, `reviewable-runs/subagent-results/`, and `reviewable-runs/integration-decisions/`
  - `mode_semantics`: defines `policy_default`, `defer_to_subagent`, and `same_session`
  - `generic_contract`: enables generic codex-session contracts for uncontracted steps and requires explicit contracts for gate-critical steps
- `workflows/essay-iteration/workflow.yaml:codex_session_handoff`
  - Sets the workflow default to `policy_default`.
  - Declares generic request, result, and integration-decision path templates.
  - Adds a local step override for `run_cold_replacement_review` using `defer_to_subagent` plus `essay_iteration.cold_replacement_review.v1`.
- `workflows/essay-iteration/workflow.yaml:steps[].codex_session_handoff`
  - Adds the explicit local override on `run_cold_replacement_review`.
- `reviewable-runs/README.md`
  - Documents where subagent requests, results, and integration decisions live.
  - Documents that `same_session` preserves no-request defer behavior.
  - Documents that `content-agent` must not spawn models.

Existing Phase 2 reviewable-run paths under `local_write_allowed` and `review_gate_store` were preserved and remain the artifact stores for this policy.

## Runtime Assumptions

- Runtime mode resolution should follow `step.codex_session_handoff.mode`, then `workflow.codex_session_handoff.default_mode`, then `harness_policy.yaml:codex_session_handoff.default_mode`.
- `policy_default` is a resolver value, not a terminal execution behavior.
- `defer_to_subagent` should write a deterministic request artifact and then stop the `content-agent` run.
- `same_session` should preserve compatibility behavior by stopping at the codex-session step without writing a request artifact.
- For codex-session steps without explicit `agent_contract`, the runtime worker may synthesize a generic request from workflow id, step id, package, run id, `consumes`, `produces`, resolved output targets, and available input source hashes.
- Gate-critical handoffs should not rely only on generic synthesis. `essay_iteration.run_cold_replacement_review` keeps its explicit contract and remains blocked on a passing result plus accepted integration decision before `replacement_north_star`.

## Verification Performed

- Parsed `harness_policy.yaml` and `workflows/essay-iteration/workflow.yaml` with `yaml.safe_load`.
- Ran `npm run check:workflow-yaml`: passed.
- Ran `./content-agent validate --workflow essay_iteration --format json`: passed with `success: true` and no findings, including after this result artifact was written.
- Ran `git diff --check -- harness_policy.yaml reviewable-runs/README.md workflows/essay-iteration/workflow.yaml reviewable-runs/subagent-results/phase-3-codex-session-handoff-policy-result.md`: passed.

## Scope Notes

- Did not edit `scripts/` or `tests/`.
- Did not broaden the policy across other workflow YAML files.
