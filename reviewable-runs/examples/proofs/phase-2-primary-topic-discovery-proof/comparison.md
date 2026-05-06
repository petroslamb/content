# Comparison: Raw Activity vs Governed Proof

## What Raw Activity Would Show

A raw transcript could show alphaXiv searches, a few notes, and a claim that a new package idea is ready.

That would still leave a reviewer to infer:

- which workflow contract governed the work
- which package context was admitted
- which runtime inputs bounded the discovery pass
- which artifacts were expected
- whether package initialization was allowed
- whether lifecycle movement actually stopped at a gate

## What The Governed Proof Adds

The retained Phase 2 packet makes those boundaries explicit:

- `reviewable-runs/resolved-runs/phase-2-primary-topic-discovery-proof.yaml` records the workflow, package, admitted context, runtime inputs, policy resolution, selected steps, gates, and output targets.
- `reviewable-runs/logs/phase-2-primary-topic-discovery-proof.yaml` records the governed invocation and the gated terminal status.
- `reviewable-runs/gates/gate-phase-2-primary-topic-discovery-proof-topic-viability.yaml` records the pending lifecycle gate, evidence preview paths, approval requirements, and resume command.
- `reviewable-runs/logs/phase-2-primary-topic-discovery-proof-topic-discovery-handoff.md` records the handoff decision and carry-forward fields needed for package initialization.

## Continuation Boundary

The first proof stop worked: a human had to approve `topic_viability` before `proof-runs-as-source-surface` became a package.

The second stop worked: a human had to approve `research_exit` before research was marked done and paper intake moved the package toward essay iteration.

The third stop worked: the `essay_prewrite` gate had to be approved before a bounded candidate was written.

The current continuation stops at `replacement_north_star-2026-05-06T20-46-37Z`. That gate is intentionally pending because it carries quality, lifecycle movement, and promotion dimensions. The packet can pass validation and still refuse silent promotion; that is the boundary the proof is meant to preserve.
