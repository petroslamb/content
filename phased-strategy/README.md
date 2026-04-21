# Phased Strategy

This folder owns the long-range strategy, phase gates, and closure ledgers for turning this repo from a personal content operating environment into a harness-native and eventually productizable system.

Use this layer differently from the workflow layer:

- `phased-strategy/` decides what phase the repo is in and what must be true before advancing.
- `workflows/` defines repeatable content and operations playbooks.
- `scripts/` and `workflows/skills/` execute or assist those playbooks.
- `reviewable-runs/` records bounded operational runs and retained proof examples.

## Documents

| Document | Role |
| :--- | :--- |
| [`strategic_plan.md`](strategic_plan.md) | The canonical phase roadmap from clean internal automation through harness-native autonomy, operator shell, platform, and SaaS product. |
| [`phase-1-1-5-closure-checklist.md`](phase-1-1-5-closure-checklist.md) | Current closure checklist for Phase 1 and Phase 1.5, including what is done, what is partial, and what remains open. |

## Research Dependencies

Workflow-system research that might later affect this strategy now lives in [`../publications/literate-workflow-programming/`](../publications/literate-workflow-programming/).

Use that publication package for:

- paper intake and alphaXiv literature work
- research notes on markdown workflow languages, imports, skills, and compiler analogies
- draft claims about whether the repo should adopt those ideas

Extract findings back into this folder only when they change a phase gate, proof-run requirement, or product-readiness read.

## Current Read

As of 2026-04-17:

- Phase 1 is closed as the Clean Machine phase: repo normalization, one-command lifecycle visibility, package orientation, root-script hygiene, generic stage dispatch, and v2 reviewable run logs are in place.
- The original "start-to-finish by an agent" ambition is now treated as Phase 1.5/1.6 autonomy proof work, not as a remaining Phase 1 blocker.
- Phase 1.5 is substantially built as a harness-facing surface.
- Phase 1.5 is not gate-cleared until proof runs show that a harness can operate with minimal prompt glue across real work.
- Phase 1.6 should remain the operator-shell layer that follows the Phase 1.5 proof-run gap.

## When To Update This Folder

Update this folder when:

- a phase gate changes status
- a proof run closes or reopens a milestone
- a new phase is introduced
- workflow refactors change the honest strategic read
- the repo gains or loses a capability that affects product-readiness

Do not update the strategy documents just because one package advances. Package progress belongs in package `status.yaml`, package READMEs, review artifacts, or run logs.
