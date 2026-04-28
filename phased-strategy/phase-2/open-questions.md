# Phase 2 Open Questions

These are the decisions that still remain open after the distilled-findings, claim-ledger, and contradiction-register pass.

Use this file as the unresolved sidecar. Do not treat a question here as settled until the answer has moved through [`claim-ledger.md`](claim-ledger.md) and [`contradiction-register.md`](contradiction-register.md).

## 1. Do Non-Publication System Surfaces Need A Lighter Manifest Type?

`publications/` already have `status.yaml`.

It is still open whether Phase 2 later needs a lighter manifest type for system surfaces such as:

- `phased-strategy/`
- `workflows/`
- `reviewable-runs/`

The question is not whether to force them into the publication lifecycle. The question is whether the platform needs a parallel manifest for first-class non-publication operating surfaces.

Current rule: do not invent a second manifest family until Phase 2 hits a concrete failure mode that current publication routing plus workflow contracts cannot handle.

## 2. What Counts As A Full Lifecycle For Phase 2 Closure?

The Phase 2 gate requires three full essay lifecycles through the platform path.

It is still open whether that means:

- fully new idea-to-publication runs, or
- continuation of existing packages through all remaining stages using the platform path

This needs a strict answer before proof design starts. Synthetic demos may help development, but they do not close Phase 2.

Related contradiction: `P2-011`.

## 3. Where Should Promoted-Output State Live?

Phase 2 now commits to a small state vocabulary:

- `authority_order`
- `claim_state`
- `contradiction_state`
- `validation_state`
- `trace_state`

What remains open is the storage surface:

- inside run records
- inside gate artifacts
- inside a separate small manifest

The vocabulary should stay stable even if the storage surface changes. Full semantic provenance graphs remain out of scope.

Related contradiction: `P2-007`.

## 4. How Much Context Lifecycle Governance Belongs To Phase 2?

Phase 2 now treats context admission as promotable:

- required context should be explicit
- loaded context should be visible
- context paths and hashes should be recorded
- undeclared context should be denied or surfaced as a violation according to the enforcement surface

What remains open is lifecycle governance after context persists, resumes, compacts, or branches:

- decay
- pruning
- contradiction handling
- privacy policy
- versioned reuse

Current rule: promote admission now. Do not turn Phase 2 into a repo-wide memory system. Add lifecycle policy only where real runs expose stale-authority, privacy, or resumption failures.

Related contradiction: `P2-014`.

## 5. How Much Persistent Browser Support Belongs To Phase 2?

Phase 1.6 still owns operator-shell browser ergonomics in the roadmap.

What remains open is the dependency boundary:

- which auth-heavy browser behaviors are required before Phase 2 implementation can start
- which ones can remain Phase 1.6 or later hardening

The main cases are still:

- Substack
- NotebookLM
- YouTube Studio

Current rule: decide browser dependency per workflow and stage, not by blanket intuition.

Related contradiction: `P2-012`.
