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

## Current Read

As of 2026-04-17:

- Phase 1 is mostly closed as repo normalization.
- Phase 1 is not strictly closed under its original "zero package-specific scripts" wording.
- Phase 1.5 is substantially built as a harness-facing surface.
- Phase 1.5 is not gate-cleared until proof runs show that a harness can operate with minimal prompt glue across real work.
- Phase 1.6 should remain a next layer, not a substitute for closing the proof-run gap.

## When To Update This Folder

Update this folder when:

- a phase gate changes status
- a proof run closes or reopens a milestone
- a new phase is introduced
- workflow refactors change the honest strategic read
- the repo gains or loses a capability that affects product-readiness

Do not update the strategy documents just because one package advances. Package progress belongs in package `status.yaml`, package READMEs, review artifacts, or run logs.
