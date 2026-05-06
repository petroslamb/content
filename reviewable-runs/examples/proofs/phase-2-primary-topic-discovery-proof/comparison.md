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

The continuation now stops at `research_exit`. A human still has to approve, reject, or defer `research_exit-2026-05-06T19-59-47Z` before research can be marked done or essay iteration can begin.
