# Phase 2 Contradiction Register

This register records the tensions that matter before Phase 2 conclusions are promoted into implementation.

It is narrower than a general research notebook. Keep only contradictions that change:

- the honest Phase 2 conclusion
- the contract boundary
- the proof-run requirement
- the implementation sequence

## Status Labels

- `resolved`: the authority rule is clear enough to guide implementation.
- `open`: the tension is real and still needs proof, narrowing, or a sharper authority rule.
- `parked`: the tension is known but outside the current Phase 2 scope.
- `blocked`: the tension prevents honest implementation on the affected surface.

## Register

| ID | Tension | Claim A | Source A | Claim B | Source B | Authority / Resolution Rule | Status | Design Instruction |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| P2-001 | Human-readable workflow guidance vs machine-authoritative execution contract. | Workflow docs should stay readable and close to operator language. | [`README.md`](README.md), workflow docs, natural-language harness/spec papers | The runtime needs one explicit machine authority surface. | [`workflow-yaml-schema.md`](workflow-yaml-schema.md), `2604.13346`, `2512.19769` | `workflow.yaml` wins for machine authority. The README wins for human explanation. Drift checks police the seam. | resolved | Do not ask README prose to carry permissions, allowed paths, or gate semantics alone. |
| P2-002 | File-backed truth vs runtime convenience state. | The runtime and cockpit need indexes, summaries, and pending-work views. | [`architecture.md`](architecture.md), [`dashboard-v0.md`](dashboard-v0.md) | Hidden runtime state would violate the repo’s inspectable source-of-truth model. | [`architecture.md`](architecture.md), [`review-gate-protocol.md`](review-gate-protocol.md), root harness surfaces | File-backed tracked artifacts win. Caches are allowed only when rebuildable from tracked files. | resolved | Keep gate store, run records, manifests, and contracts inspectable. Treat caches as disposable. |
| P2-003 | Stronger formal contracts vs brittle or misleading conformance. | More explicit contracts make denial, verification, and debugging possible. | `2604.13346`, `2512.19769`, `2603.00822`, local contract planning | More formality does not automatically improve runtime conformance and can exceed a model’s useful operating range. | `2512.18940`, trace/compliance findings imported through `literate-workflow-programming` | Treat contract precision as a diagnostic tool, not monotonic proof. When strictness becomes brittle, route the failure into debugging rather than pretending the contract is therefore wrong or complete. | open | Keep the first contract vocabulary small. Prove useful strictness through real runs before expanding it. |
| P2-004 | Denyable boundaries vs merely visible violations. | Phase 2 should deny undeclared tools, undeclared paths, and undeclared context. | [`2.2-enforcement-and-validation-layer.md`](2.2-enforcement-and-validation-layer.md), [`../strategic_plan.md`](../strategic_plan.md) | The current harness/runtime may only be able to block some of these and may need to surface others as violations first. | current repo/tool reality, proof-run limits, local harness model | Start with a mixed rule: deny what the runtime can confidently mediate, and record visible contract violations for the rest. | open | Do not block Phase 2 on perfect confinement. Make the denial vs visibility boundary explicit per surface. |
| P2-005 | Traces as semantic debugging surfaces vs traces becoming fake authority. | Rich traces help explain what happened, why it stopped, and what drifted. | [`2.3-trace-and-provenance-minimums.md`](2.3-trace-and-provenance-minimums.md), `2603.23806`, `2603.29848` | Logs and traces should not become the source of truth. | [`architecture.md`](architecture.md), `2603.17399`, `2602.13855` | Contracts, manifests, and governed source artifacts remain primary. Traces explain execution against them. | resolved | Never let run logs silently replace contracts, package state, or provenance decisions. |
| P2-006 | Thin runtime wrapper vs second orchestration language. | `content-agent` should stay thin and wrap stable machinery. | [`architecture.md`](architecture.md), [`milestones.md`](milestones.md) | A useful runtime still needs enough semantics to resolve packages, contracts, validations, traces, and gates. | same docs plus local proof-run evidence | Keep orchestration semantics in tracked contracts and repo-native artifacts. Let `content-agent` own resolution and execution plumbing, not a rival planning language. | open | Reject convenience features that duplicate workflow semantics instead of reading them from contracts. |
| P2-007 | Small contradiction/provenance state vs full semantic provenance graphs. | Phase 2 only needs a minimal promoted-output vocabulary to support trustworthy promotion decisions. | [`2.3-trace-and-provenance-minimums.md`](2.3-trace-and-provenance-minimums.md), [`open-questions.md`](open-questions.md) | Claim-level provenance is richer and more correct, but not required to start the platform. | `2602.13855`, imported package claim-state work | The small stable vocabulary wins for Phase 2. Full graphs stay out of scope. | open | Fix the vocabulary now. Delay graph-heavy machinery until the platform path is proven. |
| P2-008 | Consuming the current package model vs redesigning package taxonomy inside the platform. | The repo already has stable enough umbrella/leaf semantics to serve as runtime input. | [`README.md`](README.md), [`architecture.md`](architecture.md), [`milestones.md`](milestones.md), manifest-first proof run | Some awkward cases still exist, especially outside publication packages. | [`open-questions.md`](open-questions.md), system-surface ambiguity | For publication packages, current manifests win. Do not reopen the package-model debate inside Phase 2 implementation. | resolved | Build against real package fixtures now. Handle non-publication surfaces as a separate explicit question. |
| P2-009 | Publication-package manifests vs lighter manifests for system surfaces. | Publication packages already provide the needed lifecycle contract. | [`open-questions.md`](open-questions.md), current `status.yaml` use | `phased-strategy/`, `workflows/`, and `reviewable-runs/` may also need first-class machine identity without pretending to be publication packages. | same open question | Keep this open until Phase 2 hits a real need that cannot be handled by current publication routing plus workflow contracts. | open | Do not invent a second manifest family prematurely. Record the exact failure mode first. |
| P2-010 | Explicit file-backed gates vs blocking terminal prompts or hidden approval queues. | Review decisions need previews, evidence, and resumable commands. | [`review-gate-protocol.md`](review-gate-protocol.md), Reviewable Runs model | Direct terminal prompting is simpler in the short term. | current harness behavior, legacy prompt loops | File-backed gates win because they are inspectable, resumable, and visible to both CLI and cockpit. | resolved | Treat blocking terminal prompts as an implementation smell once gate artifacts exist. |
| P2-011 | Real-package proof runs vs synthetic platform demonstrations. | Real package runs reveal routing ambiguity, artifact drift, and gate friction honestly. | manifest-first proof run, current package fixtures, [`milestones.md`](milestones.md) | Synthetic demos are easier to build and explain. | common platform temptation; no tracked contradiction yet | Proof on real package fixtures wins for phase closure. Synthetic demos may help development, but they do not close Phase 2. | open | Tie every major Phase 2 claim back to a real package-path proof requirement. |
| P2-012 | Phase 1.6 browser hardening vs Phase 2 browser dependency. | Browser ergonomics belong to the operator-shell layer. | [`README.md`](README.md), [`open-questions.md`](open-questions.md) | Some auth-heavy browser behaviors may be prerequisites for honest platform execution. | Substack, NotebookLM, YouTube workflow reality | Keep the dependency boundary open until the required browser-backed mutations are enumerated by workflow and stage. | open | Decide browser dependency per workflow, not by blanket intuition. |
| P2-013 | Skills as declared capabilities vs raw markdown guidance. | Skills should be bound, verified, and routable capabilities in the platform path. | [`README.md`](README.md), [`architecture.md`](architecture.md), `2604.03088`, `2604.08224` | The repo still contains many markdown skill surfaces that are useful as operator guidance. | current repo practice | Keep markdown skills as operator help, but do not let Phase 2 assume that guidance text alone is a stable executable capability surface. | open | Separate operator guidance from executable capability declarations. |

## Current Pressure Points

The highest-value unresolved tensions before implementation are:

1. `P2-003` contract precision vs brittleness
2. `P2-004` denyable boundaries vs surfaced violations
3. `P2-006` thin runtime vs semantic creep
4. `P2-007` where the promoted-output state actually lives
5. `P2-011` what a real closure proof run must look like
6. `P2-012` how much browser dependency belongs inside Phase 2

## Use Rule

Before promoting a Phase 2 conclusion into implementation:

1. check whether the claim exists in [`claim-ledger.md`](claim-ledger.md)
2. check whether a contradiction here limits or narrows it
3. update the authority rule if the contradiction is newly resolved
4. only then promote the conclusion into contracts, scripts, or runtime behavior
