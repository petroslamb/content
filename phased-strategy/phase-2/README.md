# Phase 2 Planning

Phase 2 owns the first real local execution platform for this repo.

Phase 1.5 proved the repo is harness-operable.
Phase 1.6 remains the operator-shell phase.
Phase 2 is where workflow specifications become a stable machine contract with validation, traces, gates, and a thin runtime on top.

The Phase 2 goal remains:

> The agent runs the lifecycle. You review outcomes, not steps.

Use this folder for Phase 2 planning only. Promote decisions into implementation surfaces only after the contract is stable.

## Status

- Phase 2.1 through 2.6 are implemented and committed as the Phase 2 local platform baseline.
- Phase 2.6 has a retained real-package proof run: `phase-2-6-editorial-report-proof`.
- Phase 2.7 is the documented post-baseline handoff-discipline subphase; it does not add runtime autonomy or change `content-agent` into a model runner.
- Phase 2.7a is a planned implementation subphase for request exit protocol hardening after 2.7; it is not implemented by this strategy packet.
- Phase 2.8 is the strategy-only experimental workflow lifecycle spec: experiments may run explicitly and produce evidence, but they cannot silently replace canonical lifecycle paths until they pass the promotion bar.
- The 2026-05-09 operationalization pass migrated all seven current experimental workflow docs into governed `workflow.yaml` contracts with `stability: experimental`; this is contract migration, not canonical promotion.
- Phase 1.6 still exists as a separate roadmap phase, but Phase 2 should depend only on the minimal stable contract surfaces it actually needs.
- This folder now treats Phase 2 as contract-first, validation-first, and trace-first rather than CLI-first.
- Umbrella and leaf package normalization is now mostly done. Phase 2 should treat the current package model as a consumed contract surface, not as new migration work.

The 2.1-2.6 baseline closes the local governed-runtime implementation: workflow contracts, validation, evidence, gates, `content-agent`, cockpit, and bounded editorial-report automation. It does not claim autonomous end-to-end publication, browser-backed external mutation, hidden multi-agent orchestration, or full lifecycle reliability across multiple fresh packages.

Phase 2.7 formalizes the post-baseline operator discipline for clean-context subagent handoffs: parent sessions orchestrate, subagents do model-mediated work, and deterministic artifacts prove what happened. Phase 2.7a plans the next implementation step: generated requests should carry exit protocol, skill recommendations, and verification requirements, with result validation requiring verification evidence for new 2.7a handoffs. Hook enforcement remains later work unless promoted into the appropriate authority surfaces.

Phase 2.8 formalizes experimental workflow lifecycle discipline using existing Phase 2 surfaces. It does not add runtime interfaces, schema fields, validators, cockpit behavior, or automatic route/canonical promotion.

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
- **2.7 Agent Handoff Discipline**: formalize clean-context subagent handoffs while keeping `content-agent` deterministic.
- **2.7a Request Exit Protocol Implementation**: planned hardening for generated request exit protocol, skill recommendations, and result verification requirements.
- **2.8 Experimental Workflow Lifecycle**: define how experiments are created, governed, proven, promoted, or retired without replacing canonical routes silently.

## Documents

| Document | Role |
| :--- | :--- |
| [`milestones.md`](milestones.md) | Phase 2.1-2.8 sequence, dependencies, and closure read. |
| [`architecture.md`](architecture.md) | Core boundary and platform decisions: machine truth, thin runtime, gate store, traces, and source-of-truth rules. |
| [`workflow-yaml-schema.md`](workflow-yaml-schema.md) | The target machine contract for executable workflows. |
| [`review-gate-protocol.md`](review-gate-protocol.md) | Review-gate classes, artifact contract, gate store, and resume model. |
| [`dashboard-v0.md`](dashboard-v0.md) | The first local cockpit scope built on gate and trace artifacts. |
| [`2.4-gate-runtime-and-content-agent.md`](2.4-gate-runtime-and-content-agent.md) | The deterministic CLI/runtime implementation plan after contracts, validation, and evidence. |
| [`2.5-local-cockpit.md`](2.5-local-cockpit.md) | The numbered cockpit phase wrapper and dependency boundary. |
| [`2.6-editorial-automation.md`](2.6-editorial-automation.md) | The bounded editorial automation plan after governed gates and article-polish boundaries stabilize. |
| [`2.7-agent-handoff-discipline.md`](2.7-agent-handoff-discipline.md) | The post-baseline parent/subagent handoff discipline, exit protocol, skill plan, and hook posture. |
| [`2.7a-request-exit-protocol.md`](2.7a-request-exit-protocol.md) | Planned implementation subphase for request exit protocol fields, result verification evidence, handoff skill creation, and regression proofs. |
| [`2.8-experimental-workflow-lifecycle.md`](2.8-experimental-workflow-lifecycle.md) | Strategy-only lifecycle discipline for experimental workflows, governed proofs, promotion, and retirement. |
| [`open-questions.md`](open-questions.md) | The remaining Phase 2 decisions that are still genuinely open. |
| [`idea-bank.md`](idea-bank.md) | Candidate ideas that may justify rewriting Phase 2 before implementation. |
| [`claim-ledger.md`](claim-ledger.md) | Phase 2 planning claims that should be pressure-tested before implementation. |
| [`contradiction-register.md`](contradiction-register.md) | The tensions, authority rules, and design instructions that constrain Phase 2 conclusions. |

## Foundation Specs

The numbered implementation and strategy packets for the Phase 2 foundation are:

- [`2.1-executable-workflow-contract.md`](2.1-executable-workflow-contract.md)
- [`2.2-enforcement-and-validation-layer.md`](2.2-enforcement-and-validation-layer.md)
- [`2.3-trace-and-provenance-minimums.md`](2.3-trace-and-provenance-minimums.md)
- [`2.4-gate-runtime-and-content-agent.md`](2.4-gate-runtime-and-content-agent.md)
- [`2.5-local-cockpit.md`](2.5-local-cockpit.md)
- [`2.6-editorial-automation.md`](2.6-editorial-automation.md)
- [`2.7-agent-handoff-discipline.md`](2.7-agent-handoff-discipline.md)
- [`2.7a-request-exit-protocol.md`](2.7a-request-exit-protocol.md) (planned)
- [`2.8-experimental-workflow-lifecycle.md`](2.8-experimental-workflow-lifecycle.md) (strategy-only)

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
