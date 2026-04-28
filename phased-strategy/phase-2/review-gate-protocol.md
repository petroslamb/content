# Review Gate Protocol

## Purpose

Phase 2 review gates are explicit, inspectable, file-backed stop/resume objects.

The runtime should not wait on a terminal prompt or bury a decision in chat. When a workflow reaches a review, external mutation, or policy-sensitive boundary, `content-agent` writes a gate artifact, records the stop in the run record, and exits cleanly. The CLI and cockpit then expose the pending decision.

Review gates are derivative execution evidence. They do not replace `workflow.yaml`, package `status.yaml`, root policy/profile/gate YAMLs, or package content artifacts as source authority.

## Authority Position

Gate authority is split across three surfaces:

- `gate_contracts.yaml` defines reusable gate classes and required evidence.
- `workflow.yaml` declares where a workflow step can instantiate a gate.
- `reviewable-runs/gates/` contains concrete gate artifacts created by `content-agent`.

`pipeline_profiles.yaml` may require gates for a route. `harness_policy.yaml` may require approval before external mutation or lifecycle movement. Neither file should cause a gate to be hidden in terminal state.

## Gate Store

Pending and resolved review gate artifacts live under:

```text
reviewable-runs/gates/
```

The store should remain:

- YAML-backed
- easy to diff and inspect
- readable by `content-agent` and the cockpit
- linked to a run record and, when present, a `resolved_run`
- derivative from workflow and root policy contracts

Gate artifacts are maintained by `content-agent`. Humans inspect and decide on them through `content-agent review` or the cockpit rather than hand-authoring gate YAML.

## Gate Types

### Content Quality

Use when a human must inspect a draft, asset, preview, or decision packet.

Typical boundaries:

- major rewrite review
- essay prewrite review
- replacement/north-star review
- research exit review

The decision is qualitative. Approval means the content or artifact can proceed to the next valid workflow step. It does not automatically approve external mutation.

### External Mutation

Use when the next action mutates an external system, such as:

- Substack
- YouTube
- NotebookLM
- archive sync targets
- playlists, descriptions, captions, or published posts

External mutation approval is distinct from quality approval. A draft can be approved for quality and still not be approved for external publication, upload, sync, or distribution.

### Lifecycle Movement

Use when a gate decision changes package lifecycle state, route, or promotion status.

Typical boundaries:

- promote a draft to live/canonical
- move from research into essay iteration
- mark a package stage complete
- initialize a successor or pivot route

Lifecycle movement should be denied outside the governed path unless explicitly approved through the gate.

### Validation Stop

Use when runtime validation prevents completion and a human decision is needed.

Examples:

- required evidence missing
- bounded drift check failed
- context admission violation
- trace/run-record completeness failure
- policy requires manual triage before retry

Validation stops may resolve through retry, defer, reject, or route correction. They should not be silently converted into success.

## Non-Gate Scriptable Steps

Not every step is a review gate.

A scriptable step can run without a gate when:

- the step is declared in `workflow.yaml`
- inputs, context, tools, paths, budgets, and outputs pass validation
- no qualitative, lifecycle, promotion, or external mutation decision is required

Such steps still write run-record evidence. They do not need a pending gate artifact unless the workflow, route, validation layer, or root policy requires one.

## Gate Artifact Contract

Each concrete gate artifact should be YAML.

Suggested shape:

```yaml
gate_id: essay_iteration-major-rewrite-2026-04-22T18-10-00Z
status: pending
gate_type: content_quality
gate_contract: replacement_north_star

package:
  path: publications/literate-workflow-programming
  status_path: publications/literate-workflow-programming/status.yaml

workflow:
  workflow_id: essay_iteration
  workflow_version: 1
  workflow_hash: sha256:...
  step_id: write_bounded_candidate

run:
  run_id: run-2026-04-22T18-10-00Z
  resolved_run_path: reviewable-runs/resolved-runs/run-2026-04-22T18-10-00Z.yaml
  run_record_path: reviewable-runs/logs/run-2026-04-22T18-10-00Z.yaml

stop:
  reason: Review the bounded candidate before promotion.
  created_at: 2026-04-22T18:10:00Z
  created_by: content-agent

evidence:
  preview_paths:
    - publications/literate-workflow-programming/literate-workflow-programming-candidate-r1.md
  evidence_paths:
    - reviewable-runs/logs/run-2026-04-22T18-10-00Z.yaml
  validation_results:
    - id: candidate_matches_governing_brief
      status: passed
  enforcement_outcomes:
    - surface: external_mutation
      posture: deny
      status: not_attempted

approval:
  quality_required: true
  external_mutation_required: false
  lifecycle_movement_required: true
  allowed_decisions:
    - approve
    - reject
    - defer

resume:
  on_approve: next_step
  on_reject: correction_step
  on_defer: keep_pending
  command_hint: content-agent review --gate essay_iteration-major-rewrite-2026-04-22T18-10-00Z --approve

promoted_output_state:
  authority_order: workflow_contract_first
  claim_state: unchanged
  contradiction_state: none_known
  validation_state: passed
  trace_state: complete

decision: null
```

When resolved, `decision` should become a structured record:

```yaml
decision:
  decided_at: 2026-04-22T19:02:00Z
  decided_by: human
  outcome: approve
  quality_approved: true
  external_mutation_approved: false
  lifecycle_movement_approved: true
  reason: Candidate clears bounded rewrite review.
  resumed_by: content-agent
  resumed_run_record_path: reviewable-runs/logs/run-2026-04-22T19-02-00Z.yaml
```

## Required Fields

A pending gate must identify:

- gate id
- status
- gate type
- gate contract from `gate_contracts.yaml`
- package path and package status path
- workflow id, workflow version, workflow hash, and step id
- run id
- run record path
- resolved-run path when the run is governed, gated, resumable, continuous, or audit-relevant
- stop reason and creation time
- preview paths and evidence paths
- relevant validation results
- relevant deny/detect/record outcomes
- required approval dimensions
- allowed decisions
- resume or recovery behavior

If a gate concerns an external mutation, it must mark that explicitly. If a gate concerns lifecycle movement or promotion, it must mark that explicitly.

## Decision Outcomes

Supported decisions:

- `approve`
- `reject`
- `defer`

Meanings:

- `approve`: record approval and resume from the declared next step or resume target
- `reject`: record rejection reason and route to the declared correction or recovery step
- `defer`: keep the gate pending without inventing a new run or marking success

Rejection must leave a durable reason. Deferral must not mutate lifecycle state. Approval must only approve the dimensions named in the gate artifact.

## Runtime Rules

1. Gate creation happens automatically from governed workflow execution.
2. `content-agent` writes gate artifacts; humans do not hand-author them.
3. Gate artifacts must point at exact preview and evidence paths.
4. Gate artifacts must identify the exact run record and, when applicable, the `resolved_run`.
5. Gate artifacts must identify the exact resume or recovery path.
6. External mutation approval must be visibly distinct from content quality approval.
7. Lifecycle movement and promotion approval must be visibly distinct from quality approval.
8. `content-agent review` operates over `reviewable-runs/gates/` rather than inventing an alternate approval path.
9. Resuming from a gate must write follow-up run-record evidence.
10. A resolved gate should remain inspectable; do not replace it with an unlinked log line.

## Relationship To Traces

Gate artifacts are not run records.

- `run_record` explains what happened.
- `review_gate` explains why execution stopped and how it can resume.
- `resolved_run` explains the workflow contract applied to a package/run request.

The run record should include gate ids reached or resolved. The gate artifact should link back to the run record and resolved run. Both remain derivative execution evidence.

## Relationship To `content-agent`

The gate protocol depends on the v1 command surface:

- `content-agent status` lists pending gates and recent gate decisions.
- `content-agent next` treats pending gates as blockers for governed progress.
- `content-agent run` creates gates when workflow execution reaches a declared gate boundary.
- `content-agent resume` continues from an approved gate or durable `resolved_run`.
- `content-agent review` lists, inspects, approves, rejects, or defers gates.
- `content-agent validate` checks gate shape, required evidence, and trace completeness without approving anything.

`content-agent` is deterministic infrastructure. The gate protocol should not assume a separate LLM persona, hidden queue, or long-running chat state.

## Acceptance Read

The review-gate protocol is stable when:

1. gate classes resolve through `gate_contracts.yaml`
2. workflow steps can declare gate references without embedding full gate artifacts
3. governed runs write pending gates under `reviewable-runs/gates/`
4. gate artifacts link to run records and durable resolved runs when required
5. quality, external mutation, lifecycle movement, and promotion approvals are distinguishable
6. approve, reject, and defer decisions leave durable YAML evidence
7. `content-agent review` can operate over the gate store
8. the cockpit can read gate state without becoming a separate system of record

## Non-Goals

The review-gate protocol is not:

- a chat transcript
- a generic issue tracker
- a hidden database queue
- a standalone approval service
- a full provenance graph
- an autonomous publication permission
- a replacement for `workflow.yaml`, `gate_contracts.yaml`, `harness_policy.yaml`, or package `status.yaml`

It should stay close to the repo's inspectable, file-backed model.
