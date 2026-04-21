# Literate Workflow Programming

Status: live research brief, not an essay draft.

## Working Thesis

Markdown workflow docs, skill files, indexes, imports, package state, validators, and reviewable-run logs are becoming a literate programming substrate for agent workflows. The open question is whether that is a real architecture with its own software-engineering discipline, or only a useful metaphor for context engineering.

After the first P0 intake, the more defensible version is narrower:

Structured natural-language workflow specifications can act as source artifacts for agent systems when they are paired with explicit context loading, validators, runtime execution, and reviewable traces that map behavior back to the specification.

## Research Problem

The current agent tooling literature is converging from several directions:

- filesystem-based context architecture
- natural-language harnesses
- declarative agent specifications
- executable constraints from instruction files
- skills treated as portable code
- test-driven prompt or agent definitions
- observability and source-map-like traces

This package asks whether those threads compose into a practical programming model for agent-operated content and workflow systems.

## Provisional Architecture Vocabulary

| Software Concept | Workflow-System Analogue |
| :--- | :--- |
| Source code | Markdown workflow docs, skill files, package READMEs |
| Module | Workflow, skill, package surface, or reference bundle |
| Import | Declared dependency on another context file or artifact |
| Symbol table | Index files and package maps |
| Function | A workflow stage or skill that transforms inputs into outputs |
| Object | A package folder with state, evidence, artifacts, and lifecycle |
| Type check | Validator, schema check, policy check, or stage completion check |
| Compiler/linker | Harness code that resolves imports and assembles context packets |
| Runtime | Codex, local scripts, tools, and external services |
| Debug trace | Reviewable-run log |
| Source map | Future provenance layer connecting output back to source context |

## Initial Design Hunch

Use different programming styles at different layers:

- object-oriented for durable package state
- functional for workflow stages and skills
- declarative for policies, imports, and stage contracts
- event-sourced for reviewable-run logs

The first operational danger is passive-context sprawl. Markdown becomes a programming substrate only when it has explicit dependencies, scoped context layers, inputs and outputs, validators, provenance logs, and policy enforcement.

The first conceptual danger is confusing source with trace. Specifications and stage contracts should remain the source of truth. Reviewable-run logs should become source-map-like debugging surfaces that show what happened relative to that source.

## P0 Intake Read

The initial paper batch points toward a source/runtime/debugging stack:

- ICM supplies folder-structured context loading and markdown stage contracts.
- Natural-Language Agent Harnesses supplies externalized harness logic and durable artifacts.
- AgentSPEX supplies typed workflow definitions, submodules, explicit state, logging, checkpointing, replay, and a harness runtime.
- Bootstrapping Coding Agents insists that the specification, not the generated implementation or log, is the artifact of record.
- TDAD supplies tests, hidden checks, mutation testing, and regression vocabulary for agent specifications.
- ContextCov supplies executable guardrails derived from agent instruction files.
- SkVM supplies the skills-as-code pressure: raw markdown skills need capability binding or compilation to travel across models and harnesses.

The package should therefore prototype `spec-diff`: compare expected workflow state from a stage contract against actual run artifacts, then report semantic drift as source-linked findings. The first design note is [`research-notes/2026-04-20-spec-diff-experiment.md`](research-notes/2026-04-20-spec-diff-experiment.md).

## P1 Lead Decision

The P1 batch decides the lead frame:

Agent workflow specs become meaningful source only when coupled to validation gates, policy enforcement, and semantic debugging traces.

Agent Spec and the declarative workflow DSL strengthen the visible specification layer. FASTRIC adds prompt-protocol conformance and trace analysis. ALARA and Progent add the enforcement layer, showing why context and tool policy must be parsed and enforced rather than merely described. Single-Agent With Skills connects this package back to `illusion-of-swarm` by treating skills as internalized behaviors while exposing semantic-selection limits.

The article should therefore treat specification languages as the visible surface, validation as the hinge, and `spec-diff` as the repo-native proof that source-linked drift can be detected in a publication package. The P1 synthesis note is [`research-notes/2026-04-21-p1-synthesis-validation-gates.md`](research-notes/2026-04-21-p1-synthesis-validation-gates.md).

## Second-Package Proof Threshold

The first external `spec-diff` proof candidate ran against `publications/illusion-of-swarm/` on 2026-04-21. It found evidence-orientation drift in a package with different storage conventions, repaired only `papers/index.md`, and passed after repair.

This meets the second-package threshold as a candidate, not as a retained repo-wide proof. The next promotion decision should ask whether package-local validators should become a proof-run requirement. It should not assume a shared root command or update `phased-strategy/` until that decision is made explicitly.

## Adjacent Package Transfer

`publications/confidence-debt/` and the external `eth-llm` contradiction-ledger artifacts add a useful mechanism without changing this essay's subject. Confidence Debt is about trust outrunning evidence. This package is about workflow specs becoming source. The shared mechanism is claim state: promoted claims need evidence state, contradiction state, validation state, and trace state.

The cross-read note is [`research-notes/2026-04-21-confidence-debt-contradiction-ledger-transfer.md`](research-notes/2026-04-21-confidence-debt-contradiction-ledger-transfer.md).

## Claim-State Draft Gate

The next drafting pass should admit claims only after they have three statuses: ledger status in [`claim-ledger.md`](claim-ledger.md), contradiction status in [`contradiction-register.md`](contradiction-register.md), and rubric status in [`claim-scorecard.md`](claim-scorecard.md).

This keeps the article focused on the chosen lead while still importing the useful mechanism from Confidence Debt. The claim ledger owns evidence state. The contradiction register owns tension state. The scorecard owns article-readiness state.

## Next Research Tasks

1. Draft from the chosen lead frame only after each body claim has ledger status, contradiction status, and rubric status.
2. Separate existing terms: context engineering, natural-language harness, agent specification language, prompt specification language, skills-as-code, and literate programming for agents.
3. Keep `imports`, package-as-object semantics, full Evidence Governance contradiction-ledger machinery beyond this curated register, and repo-wide validator promotion parked until there is stronger local proof.
4. Decide whether the `illusion-of-swarm` result and contradiction-ledger transfer justify a promotion memo for package-local validators before touching `phased-strategy/`.
5. Use P2 papers for context-file limits, terminal-native harnesses, and observability rather than reopening the lead frame unless they directly break it.
