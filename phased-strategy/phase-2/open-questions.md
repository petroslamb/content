# Phase 2 Open Questions

These are the decisions that still remain open after the Phase 2 rewrite.

## 1. Do Non-Publication System Surfaces Need A Lighter Manifest Type?

`publications/` already have `status.yaml`.

It is still open whether Phase 2 later needs a lighter manifest type for system surfaces such as:

- `phased-strategy/`
- `workflows/`
- `reviewable-runs/`

The question is not whether to force them into the publication lifecycle. The question is whether the platform needs a parallel manifest for first-class non-publication operating surfaces.

## 2. What Counts As A Full Lifecycle For Phase 2 Closure?

The Phase 2 gate requires three full essay lifecycles through the platform path.

It is still open whether that means:

- fully new idea-to-publication runs, or
- continuation of existing packages through all remaining stages using the platform path

This needs a strict answer before proof design starts.

## 3. Where Should Contradiction/Provenance State Live?

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

The vocabulary should stay stable even if the storage surface changes.

## 4. How Much Persistent Browser Support Belongs To Phase 2?

Phase 1.6 still owns operator-shell browser ergonomics in the roadmap.

What remains open is the dependency boundary:

- which auth-heavy browser behaviors are required before Phase 2 implementation can start
- which ones can remain Phase 1.6 or later hardening

The main cases are still:

- Substack
- NotebookLM
- YouTube Studio
