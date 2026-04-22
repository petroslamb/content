# Review Gate Protocol

## Purpose

Phase 2 needs review stops that are explicit, inspectable, and resumable.

The runtime should not block on a terminal prompt waiting for a human. It should write a gate artifact, stop, and make the pending decision visible to both the CLI and the cockpit.

## Gate Store

This decision is closed for Phase 2 planning:

- pending and resolved review-gate artifacts live under `reviewable-runs/gates/`

That store should remain:

- file-backed
- easy to diff and inspect
- readable by both `content-agent` and the cockpit
- rebuildable enough that it does not become a hidden second system of record

## Gate Classes

### Auto-Run

Use when:

- the step is scriptable
- verification is local and objective
- no meaningful editorial or external-side-effect approval is needed

Behavior:

- run
- verify
- write run record
- update lifecycle state

### Human Review

Use when:

- a human must inspect a draft, asset, or preview
- judgment is qualitative, not only mechanical
- approval or rejection determines the next step

Behavior:

- run bounded work
- write preview and evidence
- write pending gate artifact
- stop

### External Approval

Use when the next mutation targets an external system such as:

- Substack
- YouTube
- NotebookLM

This is still a human-review gate, but it should be marked separately because "approved for quality" and "approved for external mutation" are not the same decision.

## Gate Artifact Contract

Each gate artifact should contain at least:

```yaml
gate_id: essay_iteration-major-rewrite-2026-04-22T18-10-00Z
package: publications/literate-workflow-programming
workflow_id: essay_iteration
step_id: write_bounded_candidate
gate_class: human_review
approval_gate: major_rewrite
status: pending
summary: Review the first bounded candidate before promotion.
preview_paths:
  - publications/literate-workflow-programming/literate-workflow-programming-candidate-r1.md
evidence_paths:
  - reviewable-runs/logs/2026-04-22_literate-workflow-programming_bounded-candidate-step.md
resume_command: content-agent review --gate essay_iteration-major-rewrite-2026-04-22T18-10-00Z --approve
reject_command: content-agent review --gate essay_iteration-major-rewrite-2026-04-22T18-10-00Z --reject
```

The runtime should also be able to attach:

- created time
- parent run id
- validation results relevant to the gate
- related artifact ids

## Decision Outcomes

Supported decisions:

- `approve`
- `reject`
- `defer`

Meaning:

- `approve`: resume from the next valid step
- `reject`: record the rejection reason and route back to the correction step
- `defer`: keep the gate pending without inventing a new run

## Runtime Rules

1. gate creation should happen automatically from workflow execution
2. the gate artifact must point at the exact preview surface
3. the gate artifact must identify the exact resume path
4. rejection must leave a durable reason, not just a boolean
5. external-side-effect approval must be visibly distinct
6. `content-agent review` should operate over this gate store rather than inventing an alternate approval path

## Relationship To Traces

Gate artifacts are not the same as run records.

- run records explain what happened
- gate artifacts explain why execution stopped and how it can resume

Both should remain derivative from the workflow contract rather than becoming the authority surface themselves.

## Non-Goals

The review-gate protocol is not:

- a chat transcript
- a generic issue tracker
- a hidden database queue

It should stay close to the repo’s inspectable, file-backed model.
