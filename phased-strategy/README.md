# Phased Strategy

This folder owns the long-range strategy, phase gates, and closure ledgers for turning this repo from a personal content operating environment into a harness-native and eventually productizable system.

Current status: Phase 1, Phase 1.5, and Phase 1.6 are archived historical strategy. They explain how the repo reached the current governed runtime, but they are no longer active operator guidance. The active baseline is Phase 2: file-backed workflow contracts, validation, evidence, gates, `content-agent`, cockpit, and bounded editorial automation.

Use this layer differently from the workflow layer:

- `phased-strategy/` decides what phase the repo is in and what must be true before advancing.
- `workflows/` defines repeatable content and operations playbooks.
- `scripts/` and `workflows/skills/` execute or assist those playbooks.
- `reviewable-runs/` records bounded operational runs and retained proof examples.

## Documents

| Document | Role |
| :--- | :--- |
| [`phase-2/README.md`](phase-2/README.md) | Current baseline for the local governed execution platform: executable workflow contracts, validation, traces, gates, CLI, cockpit, and bounded editorial automation. |
| [`strategic_plan.md`](strategic_plan.md) | Archived roadmap narrative from clean internal automation through productizable system. Keep for product/strategy context, not active command guidance. |
| [`archive/phase-1/README.md`](archive/phase-1/README.md) | Archived Phase 1, Phase 1.5, and Phase 1.6 strategy index. |
| [`archive/phase-1/phase-1-1-5-closure-checklist.md`](archive/phase-1/phase-1-1-5-closure-checklist.md) | Archived closure checklist for Phase 1 and Phase 1.5. |
| [`archive/phase-1/phase-1-1-5-proof-set-verdict-2026-04-22.md`](archive/phase-1/phase-1-1-5-proof-set-verdict-2026-04-22.md) | Archived proof-set verdict for the Phase 1.5 closure bar. |
| [`archive/phase-1/phase-1-6-operator-shell-brainstorm-2026-04-23.md`](archive/phase-1/phase-1-6-operator-shell-brainstorm-2026-04-23.md) | Archived operator-shell brainstorm superseded by Phase 2 `content-agent`. |
| [`archive/phase-1/publication-package-orientation-audit-2026-04-17.md`](archive/phase-1/publication-package-orientation-audit-2026-04-17.md) | Archived package-orientation audit used during Phase 1 closure. |
| [`archive/phase-1/repo-organization-audit-2026-04-28.md`](archive/phase-1/repo-organization-audit-2026-04-28.md) | Archived organization/authority audit that helped drive Phase 2 cleanup. |

## Research Dependencies

Workflow-system research that might later affect this strategy now lives in [`../publications/literate-workflow-programming/`](../publications/literate-workflow-programming/).

Use that publication package for:

- paper intake and alphaXiv literature work
- research notes on markdown workflow languages, imports, skills, and compiler analogies
- draft claims about whether the repo should adopt those ideas

Extract findings back into this folder only when they change a phase gate, proof-run requirement, or product-readiness read.

## Current Read

As of 2026-05-06:

- Phase 1 and Phase 1.5 are archived as closure history.
- Phase 1.6 is archived as a pre-`content-agent` operator-shell design thread.
- Phase 2.1 through Phase 2.6 are implemented as the current local platform baseline.
- The active source-of-truth map is [`../AUTHORITY.md`](../AUTHORITY.md).
- The active governed operator surface is `./content-agent`, backed by `workflow.yaml`, package `status.yaml`, root policy/profile/gate YAMLs, and reviewable-run evidence.
- The old `harness_contract.yaml`, `stage:*`, `workflow:*`, `gate:check`, `check:harness`, and generic `npm run run` compatibility layer is retired.

The next strategic step is not more compatibility migration. It is a proof campaign or Phase 3 definition that tests the Phase 2 platform across multiple real package paths and identifies reliability gaps.

## Archived Phase 1 Material

The Phase 1 files are retained because old strategy notes and proof records need historical context. Treat old command names inside them as period evidence, not current instructions.

Current replacements:

| Historical surface | Current surface |
| :--- | :--- |
| `harness_contract.yaml` | No generated compatibility rollup. Validate primary Phase 2 files directly. |
| `npm run stage:next` | `./content-agent next --package <package>` |
| `npm run stage:resolve` / `npm run workflow:resolve` | `./content-agent validate --workflow <workflow_id> --package <package>` |
| `npm run stage:run` / `npm run workflow:run` | `./content-agent run --workflow <workflow_id> --package <package>` |
| `npm run gate:check` | `./content-agent gate check --gate <gate_id> --package <package>` |
| `scripts/next_action.py` | `./content-agent next`, backed by shared `scripts/harness.py` resolution logic. |
| `scripts/run_stage.py` / `scripts/run_workflow.py` | `./content-agent run`. |

## When To Update This Folder

Update this folder when:

- a phase gate changes status
- a proof run closes or reopens a milestone
- a new phase is introduced
- workflow refactors change the honest strategic read
- the repo gains or loses a capability that affects product-readiness

Do not update the strategy documents just because one package advances. Package progress belongs in package `status.yaml`, package READMEs, review artifacts, or run logs.
