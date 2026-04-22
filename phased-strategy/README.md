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
| [`phase-1-6-operator-shell-brainstorm-2026-04-23.md`](phase-1-6-operator-shell-brainstorm-2026-04-23.md) | Brainstorm-first execution plan for the Phase 1.6 operator shell, including option space, convergence choices, and a recommended thin-slice build order. |
| [`phase-2/README.md`](phase-2/README.md) | Phase 2 planning index for the local execution platform: executable workflow contracts, validation, traces, gates, CLI, cockpit, and open questions. |

## Research Dependencies

Workflow-system research that might later affect this strategy now lives in [`../publications/literate-workflow-programming/`](../publications/literate-workflow-programming/).

Use that publication package for:

- paper intake and alphaXiv literature work
- research notes on markdown workflow languages, imports, skills, and compiler analogies
- draft claims about whether the repo should adopt those ideas

Extract findings back into this folder only when they change a phase gate, proof-run requirement, or product-readiness read.

## Current Read

As of 2026-04-23:

- Phase 1 is closed as the Clean Machine phase: repo normalization, one-command lifecycle visibility, package orientation, root-script hygiene, generic stage dispatch, and v2 reviewable run logs are in place.
- The original "start-to-finish by an agent" ambition is now treated as Phase 1.5/1.6 autonomy proof work, not as a remaining Phase 1 blocker.
- Phase 1.5 is now pragmatically gate-cleared: the retained proof set covers `research-heavy`, `publish-adjacent`, and `media/distribution`, even though the lanes remain asymmetric in cleanliness.
- Phase 1.6 should remain the operator-shell layer that follows Phase 1.5 closure and hardens the remaining caveats.
- Phase 2 now has its own planning folder under [`phase-2/`](phase-2/README.md), and that plan is now organized around executable contracts, validation, traces, gates, and a thin runtime rather than a CLI-first platform story.
- Umbrella and leaf package normalization is now mostly complete in the repo baseline. Phase 1.6 and Phase 2 should treat the package-shape migration as largely done and use the real package classes as fixtures:
  - settled published umbrella roots such as [`../publications/autonomous-agents/`](../publications/autonomous-agents/README.md), [`../publications/hardware-friction/`](../publications/hardware-friction/README.md), [`../publications/orchestration-paradigm/`](../publications/orchestration-paradigm/README.md), and [`../publications/neural-architectures/`](../publications/neural-architectures/README.md)
  - an active umbrella with an active flagship leaf at [`../publications/evidence-governance/`](../publications/evidence-governance/README.md)
  - an umbrella with a stopped successor-search overlay at [`../publications/literate-workflow-programming/`](../publications/literate-workflow-programming/README.md)

## When To Update This Folder

Update this folder when:

- a phase gate changes status
- a proof run closes or reopens a milestone
- a new phase is introduced
- workflow refactors change the honest strategic read
- the repo gains or loses a capability that affects product-readiness

Do not update the strategy documents just because one package advances. Package progress belongs in package `status.yaml`, package READMEs, review artifacts, or run logs.
