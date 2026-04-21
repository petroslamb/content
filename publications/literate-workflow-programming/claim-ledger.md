# Claim Ledger

This ledger keeps the research package honest before any claim is promoted into an essay, workflow refactor, or phased-strategy update.

| Claim | Current Status | Evidence Surface | Caveat / Test |
| :--- | :--- | :--- | :--- |
| Markdown workflow docs, skills, indexes, imports, and logs may form a literate programming substrate for agent workflows. | Narrowed hypothesis | ICM, Natural-Language Agent Harnesses, AgentSPEX, TDAD, SkVM, ContextCov | The defensible claim is structured workflow specifications as source artifacts. "Literate programming" remains a stretch unless prose-heavy markdown can be compiled, checked, and traced. |
| The repo should treat packages as objects, workflows and skills as functions, policies/imports as declarative contracts, and reviewable runs as traces. | Working design frame | Local repo architecture, ICM, AgentSPEX, SkVM, P0 synthesis note | Useful as architecture vocabulary, but "package as object" is not directly established by the P0 literature. |
| Imports should start as declared dependencies, not automatic markdown concatenation. | Provisional design rule | ICM context layers, AgentSPEX workflow calls, SkVM capability binding | The P0 literature does not give a markdown import model. Treat imports as a repo experiment, not a paper-backed claim. |
| Reviewable Runs could evolve from execution receipts into source-map-like semantic debugging records. | Strong candidate experiment | ICM, Natural-Language Agent Harnesses, AgentSPEX, TDAD, ContextCov, P0 synthesis note | Logs should remain derived traces. The spec/stage contract should be the source of truth. Test with a `spec-diff` experiment. |
| Context files are useful only when scoped, minimal, and enforceable. | Strong candidate claim | `2602.11988`, `2601.20404`, `2511.12884`, ALARA, ContextCov | Evidence is mixed by task type; do not claim AGENTS.md-style files are universally good or bad. |
| "A workflow is a namespace" is the bridge from `illusion-of-swarm` to this package. | Author synthesis | `2601.04748`, ICM, local workflow system | Interpretation, not a direct paper claim. Needs careful wording. |
| The specification is primary and the run log is secondary. | Strong candidate claim | `2603.17399`, AgentSPEX, TDAD, ContextCov | Avoid letting reviewable-run enthusiasm invert the hierarchy. Logs should prove, debug, and map execution back to source. |
| Skills need compilation or capability binding before they are production substrate. | Strong candidate claim | SkVM, AgentSPEX, Natural-Language Agent Harnesses | This pressures the current raw-markdown skill model. The repo can still use markdown skills, but should not claim portability without a binding/validation layer. |
| Contradiction state should be first-class in workflow-source systems. | Cross-package mechanism import | Confidence Debt artifact gate, `eth-llm` contradiction register, governance-core pilot protocol, local `spec-diff` results | Use as a semantic-debugging requirement, not as the essay's public frame. The current `spec-diff` prototype classifies gaps but does not yet validate claim conflicts or authority order. |

## P0 Paper-Backed Claim Extracts

These extracts are the working source anchors for the first essay pass. They record what each P0 paper directly supports and what it does not license yet.

| Paper | Claim It Supports | Boundary For This Package |
| :--- | :--- | :--- |
| `2603.16021` Interpretable Context Methodology | Sequential, human-reviewed agent workflows can use folder structure, markdown stage contracts, layered context, local scripts, and editable intermediate outputs as an orchestration surface. The paper also names semantic debugging and source-level traceability as future work. | Supports the filesystem and stage-contract side of the argument. It does not by itself prove that passive markdown enforces behavior or that the folder is enough for harness-native autonomy. |
| `2603.25723` Natural-Language Agent Harnesses | Harness logic can be externalized into editable natural language with roles, contracts, adapters, state conventions, validation gates, and deterministic runtime hooks. | Supports the claim that natural-language workflow artifacts can be executable harness inputs. It still depends on a runtime that interprets the contracts and supplies adapters/tools. |
| `2604.13346` AgentSPEX | Agent workflows can be specified as an explicit language with typed steps, branching, loops, reusable submodules, explicit state/context management, checkpointing, verification, logging, replay, and visual authoring. | The strongest P0 anchor for source/runtime architecture. It supports workflow specs as source artifacts more directly than the broader literate-programming metaphor. |
| `2603.17399` Bootstrapping Coding Agents | A compact specification can be the stable artifact of record when implementations are regenerable from it; the specification, not the generated implementation, is primary. | Strongly supports "spec first, trace second." It warns against treating reviewable logs or generated artifacts as the source of truth. |
| `2603.08806` Test-Driven AI Agent Definition | Behavioral specifications can be transformed into visible and hidden tests, compiled prompt artifacts, mutation tests, and regression checks for agent behavior. | Supports validators and regression vocabulary. It does not imply every workflow doc is executable without a test-generation and execution harness. |
| `2603.00822` ContextCov | Agent instruction files can be treated as executable specifications by extracting process, source, and architectural constraints into runtime checks, prohibited commands, and validators. | Supports the enforcement layer and the claim that passive instruction files are insufficient. It pushes the package toward `spec-diff` and other drift checks. |
| `2604.03088` SkVM | Skills should be treated as code whose capability requirements must be compiled or adapted across heterogeneous models and harnesses. Raw skills-as-context are fragile and inconsistent. | Supports "skills need binding/compilation." It limits any claim that current markdown skills are already portable production substrate. |

## P1 Paper-Backed Claim Extracts

The P1 batch decides the article's lead frame. Specification languages are the visible surface, but validation, policy enforcement, and debugging traces are what make workflow specs behave like source.

| Paper | Claim It Supports | Boundary For This Package |
| :--- | :--- | :--- |
| `2510.04173` Open Agent Specification | Agent and workflow definitions can be represented in a framework-agnostic form, adapted across runtimes, and evaluated through common semantics and harnesses. | Supports portability and shared representation. It still assumes parsers, runtime adapters, schemas, and validation rather than passive documentation. |
| `2512.19769` Declarative workflow DSL | Agent workflows can be separated from implementation and deployment through a DSL that compiles to an intermediate representation, supports static validation, and runs across backend environments. | Strong evidence for workflow source as configuration. It does not license a claim that arbitrary markdown is executable without an engine. |
| `2512.18940` FASTRIC | Multi-turn prompt protocols can be represented as finite-state interaction specs and checked through procedural conformance over execution traces. | Supports trace-based semantic debugging at the prompt-protocol layer. It also shows that useful formality depends on model capacity. |
| `2603.20380` ALARA | Context, agent, and tool files can structurally enforce least-privilege context and tool access when parsed by a runtime. | Supports context-as-policy and file-backed enforcement. It narrows the claim from "context files help" to "scoped files matter when the runtime enforces them." |
| `2504.11703` Progent | Agent tool privileges can be governed by a deterministic policy DSL with runtime blocking, fallback behavior, and dynamic policy updates. | Supports policy-as-code at the execution boundary. It does not make model-level reliability claims by itself. |
| `2601.04748` Single-Agent With Skills | Some multi-agent systems can be compiled into single-agent skill libraries, but skill selection has capacity and semantic-confusability limits. | Supports skills-as-code, namespace pressure, and the bridge to `illusion-of-swarm`. It does not prove multi-agent systems are unnecessary. |

## Article Lead Decision

Lead with this claim:

Agent workflow specs become meaningful source only when coupled to validation gates, policy enforcement, and semantic debugging traces.

This keeps the article on the strongest paper-backed ground. The specification language is the surface readers can inspect. Validation is the hinge that turns that surface into engineering. `spec-diff` is the repo-native proof that a declared package state can be checked against the evidence surface and reported as source-linked drift.

Adjacent transfer: Confidence Debt and the `eth-llm` contradiction register add one mechanism to this frame. A source-linked trace is more useful when it preserves contradiction state, not only file presence or stage status. See [`research-notes/2026-04-21-confidence-debt-contradiction-ledger-transfer.md`](research-notes/2026-04-21-confidence-debt-contradiction-ledger-transfer.md).

## Claim-State Authorization

This package uses the optional Claim-State Authorization variant of the evidence authorization workflow.

The ledger remains the evidence-state surface. The other claim-state surfaces are:

- [`contradiction-register.md`](contradiction-register.md): curated tensions, authority rules, and draft instructions.
- [`claim-scoring-rubric.md`](claim-scoring-rubric.md): scoring rule for article and proof readiness.
- [`claim-scorecard.md`](claim-scorecard.md): current top-claim draft gate.

Before a claim enters the article body, it should have ledger status, contradiction status, and rubric status. The scorecard can downgrade a researched claim when the contradiction state or proof state is still too weak.

## Current Essay-Safe Claims

Use these as the highest-confidence claims in the next draft:

1. Structured natural-language and declarative workflow specifications can become source artifacts when a harness interprets them and validators check their effects.
2. Reviewable-run logs should be treated as traces and semantic debugging surfaces, not as the primary source of truth.
3. Markdown workflow files become programming substrate only when paired with declared context, runtime binding, validation gates, policy enforcement, and provenance.
4. Skills are closer to source code than documentation, but raw skill markdown is not portable until the runtime can bind capabilities, govern selection, and adapt execution.
5. The local `spec-diff` experiment is a repo-native test of the source/trace claim: it compares declared package state against actual evidence and reports source-linked drift.
6. The next semantic-debugging step is contradiction state: a promoted workflow claim should preserve whether its evidence is supported, contested, classified as a gap, or blocked.

## Claims To Keep Parked

- Markdown imports as a compiler feature. P0 supports context layers and reusable submodules, but not a general markdown import system.
- Package folders as objects. This remains a useful repo metaphor, but the P0 papers support runtime state more directly than package-as-object semantics.
- Repo-wide validator promotion. Keep `spec-diff` package-local until it has passed at least one proof candidate outside `literate-workflow-programming`.
- Full Evidence Governance contradiction-ledger machinery beyond this curated claim-state register. The mechanism is relevant, but the current article should not require every publication package to adopt governance-core style contradiction registers.
- Literate programming as a settled category. The phrase is usable as the essay frame only if the argument keeps the narrower source/runtime/debugging stack visible.
