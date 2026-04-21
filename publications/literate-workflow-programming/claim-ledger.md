# Claim Ledger

This ledger keeps the research package honest before any claim is promoted into an essay, workflow refactor, or phased-strategy update.

| Claim | Current Status | Evidence Surface | Caveat / Test |
| :--- | :--- | :--- | :--- |
| Markdown workflow docs, skills, indexes, imports, and logs may form a literate programming substrate for agent workflows. | Narrowed hypothesis | ICM, Natural-Language Agent Harnesses, AgentSPEX, TDAD, SkVM, ContextCov | The defensible claim is structured workflow specifications as source artifacts. "Literate programming" remains a stretch unless prose-heavy markdown can be compiled, checked, and traced. |
| The repo should treat packages as objects, workflows and skills as functions, policies/imports as declarative contracts, and reviewable runs as traces. | Working design frame | Local repo architecture, ICM, AgentSPEX, SkVM, P0 synthesis note | Useful as architecture vocabulary, but "package as object" is not directly established by the P0 literature. |
| Imports should start as declared dependencies, not automatic markdown concatenation. | Provisional design rule | ICM context layers, AgentSPEX workflow calls, SkVM capability binding | The P0 literature does not give a markdown import model. Treat imports as a repo experiment, not a paper-backed claim. |
| Reviewable Runs could evolve from execution receipts into source-map-like semantic debugging records. | Strong candidate experiment | ICM, Natural-Language Agent Harnesses, AgentSPEX, TDAD, ContextCov, AgentPex, AgentFixer, Claim-Level Auditability, P0 synthesis note | Logs should remain derived traces and execution records. The spec/stage contract should be the source of truth, and current logs still fall short of full claim-level provenance. Test with a `spec-diff` experiment. |
| Context files are useful only when scoped, minimal, and enforceable. | Strong candidate claim | `2602.11988`, `2601.20404`, `2511.12884`, ALARA, ContextCov, `2604.13108` | Evidence is mixed by task type, metric, and information architecture; do not claim AGENTS.md-style files are universally good or bad. |
| "A workflow is a namespace" is the bridge from `illusion-of-swarm` to this package. | Narrowed synthesis | `2601.04748`, `2604.13108`, `2512.05470`, `2602.20478`, `2604.08224`, local workflow system | The safe claim is navigational and routing-oriented: workflow-structured context bundles can act as namespaces. This does not yet prove package-as-object semantics or import semantics. |
| The specification is primary and the run log is secondary. | Strong candidate claim | `2603.17399`, AgentSPEX, TDAD, ContextCov | Avoid letting reviewable-run enthusiasm invert the hierarchy. Logs should prove, debug, and map execution back to source. |
| Skills need compilation or capability binding before they are production substrate. | Strong candidate claim | SkVM, AgentSPEX, Natural-Language Agent Harnesses | This pressures the current raw-markdown skill model. The repo can still use markdown skills, but should not claim portability without a binding/validation layer. |
| Contradiction state should be first-class in workflow-source systems. | Strong candidate claim | `2602.13855`, Confidence Debt artifact gate, `eth-llm` contradiction register, governance-core pilot protocol, local contradiction register, local `spec-diff` results | Use as a semantic-debugging and provenance requirement, not as the essay's public frame. The current package has contradiction state, but not yet claim-level provenance graphs or automated contradiction resolution. |
| Validation should be treated as lifecycle infrastructure, not as a one-time gate. | Strong candidate claim | `2604.05278`, `2603.29848`, `2411.13768`, TDAD, ContextCov, local `spec-diff` experiments | Supports a stronger account of validation as the hinge in the article. It does not prove every repo needs full multi-agent SDD or a full DevOps evaluation stack. |
| Workflow-source systems need static contradiction checks over their control surfaces. | Strong candidate claim | `2603.08993`, `2603.29848`, FASTRIC, ContextCov, local contradiction register | Static contradiction findings are validation signals, not automatic proof of runtime-visible harm. |

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

## P2a Local Intake Claim Extracts

The P2a local intake converted the queued trace/provenance papers into package evidence. See [`research-notes/2026-04-21-p2a-local-intake-trace-provenance.md`](research-notes/2026-04-21-p2a-local-intake-trace-provenance.md).

| Paper | Claim It Supports | Boundary For This Package |
| :--- | :--- | :--- |
| `2603.23806` AgentPex | Agent traces can be normalized into prompt/tool/message artifacts, checked against prompt-derived rules, and scored for procedural compliance beyond outcome-only evaluation. | Strong support for traces as evaluatable debugging surfaces. It does not make traces the source of truth, and it does not provide repair or claim-level provenance. |
| `2603.29848` AgentFixer | Validation can span prompt analysis, input/output checks, cross-stage consistency, root-cause analysis, trace comparison, and iterative refinement as a continuous engineering loop. | Strong support for validation as lifecycle infrastructure. It does not justify fully autonomous validation or remove the need for human prioritization and design judgment. |
| `2602.13855` Claim-Level Auditability | Claim-level provenance requires semantic graphs that measure provenance coverage, provenance soundness, contradiction transparency, and audit effort, with protocolized validation running during synthesis. | Strong support for contradiction transparency and claim-level provenance as the next provenance layer. It does not prove the current repo already implements that layer or that contradiction resolution can be automated away. |

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
4. Skills are closer to source code than documentation, and curated or verified skills can help materially, but raw skill markdown is not portable until the runtime can bind capabilities, govern selection, and adapt execution.
5. The local `spec-diff` experiment is a repo-native test of the source/trace claim: it compares declared package state against actual evidence and reports source-linked drift.
6. The next semantic-debugging step is claim-level provenance with contradiction transparency: a promoted workflow claim should preserve whether its evidence supports, conflicts, or leaves a gap.
7. Validation should be treated as lifecycle infrastructure: incident detection, diagnosis, intermediate checks, and design refinement keep workflow specifications connected to the environment they are supposed to govern.

## P2a Gap And Contradiction Pass

The 2026-04-21 targeted alphaXiv pass did not reopen the article lead. It added caveats and intake priorities. See [`research-notes/2026-04-21-claim-state-gap-contradiction-pass.md`](research-notes/2026-04-21-claim-state-gap-contradiction-pass.md).

| Finding | Claim Effect | Draft Boundary |
| :--- | :--- | :--- |
| AGENTS.md-style context evidence splits by task risk and metric: context files may improve runtime/token efficiency in some PR workflows while hurting correctness or cost in other settings. | Tightens the context-file claim. Scoped/minimal/enforceable remains the standard for correctness-critical or policy-sensitive work, not a universal condition for any efficiency gain. | Do not say context files are globally good or bad. Say their value depends on task risk, metric, instruction quality, and enforcement. |
| FASTRIC shows model-specific formality ranges and a highest-formality conformance collapse for at least one model. | Tightens the `spec-diff` claim. More formal specs do not automatically produce better behavior. | Keep `spec-diff` as a bounded source/evidence drift proof candidate, not a broad conformance proof. |
| Agent observability, AgentSight, AgentPex, and AgentFixer strengthen the trace/debugging direction. | Strengthens Reviewable Runs as traces, but exposes the missing semantic-provenance layer. | Do not claim current Reviewable Runs are full source maps. Say they are a substrate that needs source context, contract versions, validation results, and provenance links. |
| SkillsBench and CoEvoSkills complicate the raw-skill caveat. Skills can help, and verified self-evolved skills may help more. | Keeps CSA-C4 caveated rather than downgraded. The problem is not skills; it is portability, capability binding, verification, and semantic selection. | Do not imply raw markdown skills categorically fail. Say production substrate requires curation or verification plus harness binding and routing. |
| Claim-Level Auditability is a strong candidate for the contradiction-state upgrade. | Strengthens CSA-C6 as a next semantic-debugging requirement. | Do not treat contradiction state as implemented local capability until claim-evidence provenance exists. |

## P2a Local Intake

The 2026-04-21 P2a local intake converted the queued trace/provenance papers into package evidence. See [`research-notes/2026-04-21-p2a-local-intake-trace-provenance.md`](research-notes/2026-04-21-p2a-local-intake-trace-provenance.md).

| Finding | Claim Effect | Draft Boundary |
| :--- | :--- | :--- |
| AgentPex turns prompt-derived rules into trace-level compliance checks over normalized prompt/tool/message artifacts. | Strengthens CSA-C2 and CSA-C5 by making traces evaluatable against source-derived rules. | Do not call traces the source of truth or full provenance. They remain execution records and debugging surfaces. |
| AgentFixer treats validation as an engineering loop spanning prompt analysis, cross-stage checks, root-cause analysis, trace comparison, and iterative refinement. | Strengthens CSA-C7 and the article's hinge claim about validation. | Do not present validation as a fully autonomous black box. Human prioritization and design judgment remain part of the loop. |
| Claim-Level Auditability defines provenance coverage, provenance soundness, contradiction transparency, and audit effort over semantic provenance graphs. | Strengthens CSA-C6 and moves contradiction state from imported mechanism toward paper-backed provenance requirement. | Do not claim the repo already has claim-level provenance graphs or automated contradiction resolution. |

## Surface Completion

The 2026-04-21 article-surface pressure pass separated the article vocabulary and tightened the remaining design boundaries. See [`research-notes/2026-04-21-article-surface-pressure-pass.md`](research-notes/2026-04-21-article-surface-pressure-pass.md).

| Finding | Claim Effect | Draft Boundary |
| :--- | :--- | :--- |
| Context engineering is the broader substrate, not the same thing as workflow source. | Keeps the article honest about what is being claimed. | Use context engineering as surrounding architecture, not as a synonym for source code. |
| Validation is lifecycle infrastructure. | Strengthens the lead's hinge claim. | Say validation spans grounding hooks, intermediate checks, and evaluation loops. Do not reduce it to a final test pass. |
| Workflow-as-namespace is now safe as navigational synthesis. | Strengthens the bridge to `illusion-of-swarm`. | Keep package-as-object semantics and import semantics parked. |
| Static contradiction checking belongs in the validation stack. | Expands the contradiction-state story beyond missing-paper gaps. | Do not claim every structural contradiction creates visible runtime harm. |
| Skills can help before portability is solved. | Sharpens the skills section without removing the caveat. | Attack the stronger claim that raw markdown skills are already portable production substrate. |

## Claims To Keep Parked

- Markdown imports as a compiler feature. P0 supports context layers and reusable submodules, but not a general markdown import system.
- Package folders as objects. This remains a useful repo metaphor, but the P0 papers support runtime state more directly than package-as-object semantics.
- Repo-wide validator promotion. Keep `spec-diff` package-local until it has passed at least one proof candidate outside `literate-workflow-programming`.
- Full Evidence Governance contradiction-ledger machinery beyond this curated claim-state register. The mechanism is relevant, but the current article should not require every publication package to adopt governance-core style contradiction registers.
- Literate programming as a settled category. The phrase is usable as the essay frame only if the argument keeps the narrower source/runtime/debugging stack visible.
