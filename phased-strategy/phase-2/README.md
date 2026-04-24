# Phase 2 Planning

Phase 2 owns the first real local execution platform for this repo.

Phase 1.5 proved the repo is harness-operable.
Phase 1.6 remains the operator-shell phase.
Phase 2 is where workflow specifications become a stable machine contract with validation, traces, gates, and a thin runtime on top.

The Phase 2 goal remains:

> The agent runs the lifecycle. You review outcomes, not steps.

Use this folder for Phase 2 planning only. Promote decisions into implementation surfaces only after the contract is stable.

## Status

- Phase 2 is planned, not started.
- Phase 1.6 still exists as a separate roadmap phase, but Phase 2 should depend only on the minimal stable contract surfaces it actually needs.
- This folder now treats Phase 2 as contract-first, validation-first, and trace-first rather than CLI-first.
- Umbrella and leaf package normalization is now mostly done. Phase 2 should treat the current package model as a consumed contract surface, not as new migration work.

## What Phase 2 Promotes From `literate-workflow-programming`

Promote these as roadmap inputs:

- manifest-first routing
- workflow specs as source-like surfaces only when attached to runtime, validation, and policy
- validation as lifecycle infrastructure
- source/trace separation
- bounded drift detection and trace evaluation
- lightweight contradiction/provenance state for promoted outputs
- workflow-as-namespace as a routing idea
- skills as bound, verified capabilities rather than raw portable markdown

Keep these parked:

- markdown import semantics as compiler behavior
- package-as-object semantics
- full semantic provenance graphs
- repo-wide validator promotion as doctrine
- any claim that logs are the source of truth

## Current Fixture Baseline

Phase 2 should use the normalized package classes already present in the repo as real fixtures:

- active umbrella with active flagship leaf: [`../../publications/evidence-governance/`](../../publications/evidence-governance/README.md)
- umbrella with stopped successor-search overlay: [`../../publications/literate-workflow-programming/`](../../publications/literate-workflow-programming/README.md)
- settled published umbrellas: [`../../publications/autonomous-agents/`](../../publications/autonomous-agents/README.md), [`../../publications/hardware-friction/`](../../publications/hardware-friction/README.md), [`../../publications/orchestration-paradigm/`](../../publications/orchestration-paradigm/README.md), and [`../../publications/neural-architectures/`](../../publications/neural-architectures/README.md)

Treat these as existing platform inputs. Do not spend Phase 2 re-litigating whether umbrella roots and leaves need separate manifests or whether umbrella roots may resolve through `umbrella_route`; those semantics are already part of the repo contract.

## Subphase Map

- **2.1 Executable Workflow Contract**: make `workflow.yaml` the primary machine surface.
- **2.2 Enforcement and Validation Layer**: make undeclared context, tools, and paths denyable and verifiable.
- **2.3 Trace and Provenance Minimums**: add the minimum trace and promoted-output state needed for semantic debugging.
- **2.4 Gate Runtime and `content-agent`**: make review stops resumable through stable artifacts and a thin CLI.
- **2.5 Local Cockpit**: expose package state, gates, and recent runs from file-backed truth.
- **2.6 Editorial Automation**: add structured style/compliance reporting and source-improvement suggestions without autonomous promotion.

## Documents

| Document | Role |
| :--- | :--- |
| [`milestones.md`](milestones.md) | Phase 2.1-2.6 sequence, dependencies, and closure read. |
| [`architecture.md`](architecture.md) | Core boundary and platform decisions: machine truth, thin runtime, gate store, traces, and source-of-truth rules. |
| [`workflow-yaml-schema.md`](workflow-yaml-schema.md) | The target machine contract for executable workflows. |
| [`review-gate-protocol.md`](review-gate-protocol.md) | Review-gate classes, artifact contract, gate store, and resume model. |
| [`dashboard-v0.md`](dashboard-v0.md) | The first local cockpit scope built on gate and trace artifacts. |
| [`open-questions.md`](open-questions.md) | The remaining Phase 2 decisions that are still genuinely open. |
| [`idea-bank.md`](idea-bank.md) | Candidate ideas that may justify rewriting Phase 2 before implementation. |
| [`claim-ledger.md`](claim-ledger.md) | Phase 2 planning claims that should be pressure-tested before implementation. |
| [`contradiction-register.md`](contradiction-register.md) | The tensions, authority rules, and design instructions that constrain Phase 2 conclusions. |

## Foundation Specs

The first implementation packets for the Phase 2 foundation are:

- [`2.1-executable-workflow-contract.md`](2.1-executable-workflow-contract.md)
- [`2.2-enforcement-and-validation-layer.md`](2.2-enforcement-and-validation-layer.md)
- [`2.3-trace-and-provenance-minimums.md`](2.3-trace-and-provenance-minimums.md)

## Input Sources

Keep this folder aligned with:

- [`../strategic_plan.md`](../strategic_plan.md)
- [`../README.md`](../README.md)
- [`../../publications/literate-workflow-programming/`](../../publications/literate-workflow-programming/)

## Planning Rule

Keep this folder strategy-facing.

When a planning decision becomes implementation work, promote it into:

- `workflows/` for lifecycle contracts
- `scripts/` or a future `content-agent` package for execution
- package manifests and READMEs for package-local state
- `reviewable-runs/` for run, gate, and proof artifacts
