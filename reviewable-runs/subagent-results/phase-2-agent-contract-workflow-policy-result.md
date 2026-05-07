---
kind: subagent_result
schema_version: 1
request_id: phase-2-agent-contract-workflow-policy
agent_type: worker
fork_context: false
reasoning_effort: high
completed_at: '2026-05-07'
request_path: reviewable-runs/subagent-requests/phase-2-agent-contract-workflow-policy-request.yaml
---
# Phase 2 Agent-Contract Workflow Policy Result

## Summary

Implemented the workflow and policy declaration layer for the narrow Phase 2 agent-contract prototype on `essay_iteration.run_cold_replacement_review`. This patch does not implement model spawning or convert any other step to an agent task.

## Changed Files

- `workflows/essay-iteration/workflow.yaml`
- `harness_policy.yaml`
- `reviewable-runs/README.md`
- `reviewable-runs/subagent-results/phase-2-agent-contract-workflow-policy-result.md`

## Declaration Shape

- Added reviewable-runs write surfaces for subagent requests, subagent results, and integration decisions.
- Added a package-local `plot_contract` artifact declaration and top-level `plot_contract` carry-forward contract with required content: public object, thesis, forbidden frames, evidence anchors, and stop conditions.
- Declared `cold_replacement_review_agent_request`, `cold_replacement_review_agent_result`, and `cold_replacement_review_integration_decision` outputs with exact path templates under `reviewable-runs/`.
- Added an `agent_contract` to `run_cold_replacement_review` requiring clean-context independence: `fork_context: false`, `inherits_parent_context: false`, declared files only, and no parent conversation.
- Required request/result/integration schemas, source-hash echo and stale-on-mismatch behavior, allowed verdicts (`pass`, `fail`, `defer`, `stale`), and a `pass` result plus accepted integration decision before `replacement_north_star` can clear.
- Added blocking failure triggers for scaffold residue, evidence drift, plot drift, ungrounded north-star pass, and stale sources.

## Commands Run

- `npm run check:workflow-yaml`
- `npm run check:workflow-model`
- `.venv/bin/python - <<'PY' ... yaml.safe_load(...) ... PY`
- `./content-agent validate --workflow essay_iteration`
- `git diff --stat`
- `git status --short`

## Assumptions And Follow-Up

- The `plot_contract` artifact is declared as produced by blueprint hardening, not by the current packet initializer. Runtime/script workers may choose whether to materialize a template now or keep it as an operator-filled artifact during the prototype.
- The contract assumes another worker will teach `content-agent` and packet/gate validators to emit and mechanically validate the request/result/integration artifacts. This patch only declares the workflow and policy surfaces.
- A concurrent modification exists in `scripts/content_agent.py`; this worker did not touch it.
