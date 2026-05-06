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

## Remaining Boundary

The proof stops where it should. A human still has to approve, reject, or defer the `topic_viability` gate before `proof-runs-as-source-surface` can become a package.
