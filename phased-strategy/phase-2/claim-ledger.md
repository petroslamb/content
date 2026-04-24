# Phase 2 Claim Ledger

This ledger turns the current Phase 2 conclusions into explicit claims that can be revised, strengthened, or downgraded before implementation starts.

Use it when a Phase 2 planning conclusion feels directionally right but still needs pressure:

- before promoting a planning conclusion into `workflow.yaml`
- before adding new runtime or gate behavior
- before treating a Phase 2 conclusion as implementation-ready
- before deciding that an open question is only an implementation detail

The literature and package-level extraction work still live primarily in [`../../publications/literate-workflow-programming/`](../../publications/literate-workflow-programming/README.md). This ledger is the Phase 2 decision surface that consumes those findings.

## Ledger

| Claim | Current Status | Evidence Surface | Caveat / Test |
| :--- | :--- | :--- | :--- |
| `workflow.yaml` should be the primary machine contract, while the adjacent README remains the human explanation surface. | Stable planning claim | [`workflow-yaml-schema.md`](workflow-yaml-schema.md), [`architecture.md`](architecture.md), `2604.13346`, `2512.19769`, `2510.04173`, `2603.25723` | Keep the machine contract small and explicit. Do not duplicate long prose into YAML or regenerate YAML from prose. |
| Phase 2 should consume tracked repo truth rather than invent a second system of record. | Stable planning claim | [`architecture.md`](architecture.md), [`README.md`](README.md), [`../../harness_contract.yaml`](../../harness_contract.yaml), manifest-first proof run, `2603.17399`, `2602.20478`, `2604.14228` | Rebuildable caches and indexes are allowed. Authority stays with tracked manifests, workflow contracts, package files, run records, and gate artifacts. |
| Validation and bounded enforcement are the hinge that make workflow contracts operational rather than advisory. | Stable planning claim | [`2.2-enforcement-and-validation-layer.md`](2.2-enforcement-and-validation-layer.md), [`architecture.md`](architecture.md), `2604.05278`, `2603.00822`, `2603.29848`, `2603.20380`, `2504.11703` | Do not overclaim perfect confinement. The first requirement is bounded denial and bounded checking. |
| Traces should support source-linked debugging but remain derivative from contracts, manifests, and governed source artifacts. | Stable planning claim | [`2.3-trace-and-provenance-minimums.md`](2.3-trace-and-provenance-minimums.md), [`architecture.md`](architecture.md), `2603.23806`, `2512.18940`, `2602.13855`, `2603.17399` | Trace quality still depends on recording context hashes, workflow version, validation results, parent artifacts, and gate ids. |
| Review stops should be explicit, file-backed, inspectable, and resumable through gate artifacts rather than terminal babysitting. | Stable local design claim | [`review-gate-protocol.md`](review-gate-protocol.md), [`architecture.md`](architecture.md), Reviewable Runs model, manifest-first proof run, `2604.13346`, `2603.25723` | This is strongly supported by the repo model, but still needs proof through real resumed runs rather than only planning consensus. |
| `content-agent` should stay thin first and wrap stable lifecycle machinery rather than becoming a second orchestration language. | Stable planning claim | [`architecture.md`](architecture.md), [`milestones.md`](milestones.md), [`../strategic_plan.md`](../strategic_plan.md), `2604.14228`, `2603.05344`, `2603.25723` | Thin does not mean trivial. It still must resolve package state, contracts, validations, traces, and gates correctly. |
| Skills should enter Phase 2 as bound capabilities under contract and policy rather than as raw portable markdown assumptions. | Stable planning claim | [`README.md`](README.md), [`architecture.md`](architecture.md), `2604.03088`, `2602.12670`, `2604.08224`, `2603.25723` | The claim is about binding, routing, and verification. It does not require Phase 2 to solve universal skill portability. |
| Phase 2 only needs a small contradiction/provenance state for promoted outputs, not full semantic provenance graphs. | Stable planning claim | [`2.3-trace-and-provenance-minimums.md`](2.3-trace-and-provenance-minimums.md), [`open-questions.md`](open-questions.md), `2602.13855`, package claim-state work in `literate-workflow-programming` | The vocabulary is mostly settled. The storage surface is not. |
| The current package model is a consumed platform input, not a Phase 2 redesign target. | Stable local proof-backed claim | [`README.md`](README.md), [`architecture.md`](architecture.md), [`milestones.md`](milestones.md), [`../../publications/literate-workflow-programming/status.yaml`](../../publications/literate-workflow-programming/status.yaml), manifest-first proof run | This is stable for publication packages. It does not settle whether non-publication system surfaces need a lighter manifest type. |
| Phase 2 closure should be proven through real file-backed runs on real packages, not through planning completeness, synthetic demos, or dashboard polish. | Stable planning claim | [`milestones.md`](milestones.md), [`open-questions.md`](open-questions.md), [`../strategic_plan.md`](../strategic_plan.md), Reviewable Runs evidence | The exact definition of a “full lifecycle” is still open and needs to be fixed before proof design. |

## Current Phase-2-Safe Conclusions

Use these as the strongest current conclusions before implementation:

1. The platform needs an explicit machine contract, and that contract should be authored as `workflow.yaml`, not inferred from prose.
2. Validation and enforcement belong in the execution path, not as advisory prose or a trailing test pass.
3. Traces are for debugging and audit support, not for replacing specs, manifests, or governed source artifacts.
4. Review boundaries should be represented as resumable gate artifacts that both the CLI and cockpit can inspect.
5. The runtime should stay thin and consume file-backed truth rather than becoming a second orchestration language or hidden database.
6. Package manifests and umbrella routing should be treated as baseline fixture inputs for the platform.
7. A small contradiction/provenance vocabulary is necessary for promoted outputs even before full provenance graphs exist.

## Claims That Still Need Pressure

- What the runtime can actually deny versus only surface as a violation.
- How much formality is useful before contracts become brittle or misleading.
- Where the small contradiction/provenance state should live.
- What counts as a full lifecycle for Phase 2 closure.
- How much persistent browser support is actually a Phase 2 dependency.
- Whether non-publication system surfaces need a lighter manifest type.

## Transfer Rule

Research should still be extracted in this order:

1. paper or local proof finding
2. package-level claim extraction in `literate-workflow-programming` when needed
3. Phase 2 claim update here only if the finding changes:
   - a Phase 2 conclusion
   - a Phase 2 open question
   - a contract boundary
   - a proof-run requirement
