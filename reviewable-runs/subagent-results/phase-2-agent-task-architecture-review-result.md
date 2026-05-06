---
kind: subagent_result
schema_version: 1
request_id: phase-2-agent-task-architecture-review
agent_id: 019dff52-1e36-7923-ade3-3012d7fa189e
agent_nickname: Volta
agent_type: default
fork_context: false
reasoning_effort: xhigh
completed_at: '2026-05-07'
request_path: reviewable-runs/subagent-requests/phase-2-agent-task-architecture-review-request.yaml
---
# Phase 2 Agent-Task Architecture Review

## Verdict

Prototype narrowly.

The proposal is directionally right, but implementing the full `agent_task` layer now would overfit the runtime before proving the judgment contract. The actual miss was not that `content-agent` lacked model access. It was that high-judgment drafting and review were underspecified: the deterministic runtime validated packet shape while the candidate lost plot and the review failed to catch obvious publication blockers.

The request itself states that split clearly at [phase-2-agent-task-architecture-review-request.yaml:17](../subagent-requests/phase-2-agent-task-architecture-review-request.yaml) and [phase-2-agent-task-architecture-review-request.yaml:24](../subagent-requests/phase-2-agent-task-architecture-review-request.yaml).

## Root Diagnosis

`essay_iteration` currently has open-ended `codex_session` steps for blueprint hardening, candidate drafting, and cold review at [workflow.yaml:490](../../workflows/essay-iteration/workflow.yaml), [workflow.yaml:529](../../workflows/essay-iteration/workflow.yaml), and [workflow.yaml:550](../../workflows/essay-iteration/workflow.yaml). The gates require artifacts, but the validator surface is still mostly packet completeness and declared gate flow at [workflow.yaml:365](../../workflows/essay-iteration/workflow.yaml).

The proof audit says topic discovery preserved the editorial object, while drafting drift and review failure caused the break: [phase-2-primary-proof-plot-audit-result.md:17](phase-2-primary-proof-plot-audit-result.md), [phase-2-primary-proof-plot-audit-result.md:27](phase-2-primary-proof-plot-audit-result.md), [phase-2-primary-proof-plot-audit-result.md:47](phase-2-primary-proof-plot-audit-result.md). So the fix is not "more agents"; it is explicit judgment contracts, clean critical context where warranted, and gate semantics that treat editorial failure as failure.

## Minimal Schema Additions

Add an `agent_contract` object to high-judgment steps before introducing a broad new mode:

- `contract_id`, `task_type`: `writer`, `critic`, `auditor`, `scout`
- `independence`: `clean_context_required`, `inherits_parent_context: false`, allowed files only
- `inputs`: artifact ids, exact paths, hashes, and required line-reference surfaces
- `success_criteria`: concrete pass conditions
- `failure_triggers`: e.g. scaffold residue, self-reference, evidence drift, public-object loss, ungrounded north-star pass
- `result`: path template, schema version, verdict enum: `pass`, `fail`, `defer`, `stale`
- `blocking_gates`: gate ids and required verdicts
- `integration_decision`: required path, allowed decisions, rationale, accepted/rejected result ids

The result artifact should include `request_id`, `workflow_id`, `step_id`, `package`, `run_id`, source hashes, allowed inputs, verdict, findings, line-grounded evidence, and unresolved blockers.

## Content-Agent Behavior

Keep `content-agent` deterministic. That matches the authority boundary: runtime executes declared contracts and must not invent workflow semantics at [AUTHORITY.md:14](../../AUTHORITY.md), with context admission defined in workflow YAML at [AUTHORITY.md:87](../../AUTHORITY.md).

For `agent_contract` steps, `content-agent` should emit a request artifact, stop/defer, and later validate only mechanical facts: schema, request/result match, source hashes, verdict enum, required sections, required line citations, integration decision presence, and whether blocking verdicts allow the gate to proceed. It should not spawn models and should not decide prose quality itself.

## Workflow Changes

For `essay_iteration`: prototype on `run_cold_replacement_review` first. Make the replacement gate require an independent result artifact and integration decision before `replacement_north_star` can pass. Add a deterministic scaffold-residue check, because the audit's duplicate/template-tail failure is machine-detectable. Add a small `plot_contract` carried from prewrite into candidate and review: public object, thesis, forbidden frames, required evidence anchors, and stop conditions.

Do not initially force `write_bounded_candidate` into a clean-context subagent. Drafting benefits from continuity. Give it an explicit contract first, then add a separate anti-self-reference/public-reader critic after the candidate only if the prototype proves useful.

For `topic_discovery`: do not blanket-convert. Its current workflow already separates retrieval, slate, handoff, and gate artifacts at [workflow.yaml:69](../../workflows/topic-discovery/workflow.yaml) and [workflow.yaml:222](../../workflows/topic-discovery/workflow.yaml). Add an optional public-object scout only for broad, high-ambition, or package-initializing decisions. More importantly, make the handoff emit the `plot_contract` consumed by essay iteration.

## Anti-Patterns

Avoid model spawning inside `content-agent`; arbitrary prompt blobs hidden inside YAML; treating a model "pass" as gate approval; subagents that inherit the parent conversation while claiming independence; subagents for deterministic validation, status reads, YAML checks, or run-record writing; integration decisions that rubber-stamp results; and a second workflow language embedded in markdown result bodies.

## Staged Migration

1. Add request/result/integration schemas for one step: `essay_iteration.run_cold_replacement_review`.
2. Add deterministic scaffold-residue and stale-hash checks.
3. Re-run the failed proof path and require the independent reviewer to fail the known scaffold/evidence-drift case.
4. Add `plot_contract` to topic handoff and essay prewrite.
5. Expand only to anti-self-reference critic and release proof auditor if the prototype catches real misses.
6. After two or three retained proof runs, decide whether `agent_task` deserves first-class mode status or whether `codex_session + agent_contract` is sufficient.
