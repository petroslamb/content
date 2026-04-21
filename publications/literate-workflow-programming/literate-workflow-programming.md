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

## Term Boundaries

The article now has enough evidence to separate its vocabulary instead of sliding between near-neighbor terms.

| Term | Safest Meaning Here | Strongest Anchors | Boundary |
| :--- | :--- | :--- | :--- |
| context engineering | governed construction, storage, retrieval, delivery, and evaluation of context artifacts | `2512.05470`, `2602.20478`, `2603.05344` | broader than workflow source |
| natural-language harness | runtime orchestration logic externalized into editable natural-language contracts and adapters | `2603.25723`, `2604.05278` | not a generic README or static policy file |
| agent specification language | explicit workflow, state, and control representation that can be adapted or executed across runtimes | `2510.04173`, `2512.19769`, `2604.13346` | not the whole of context engineering |
| prompt specification language | formal interaction procedures with trace-level conformance checks | `2512.18940` | narrower than a workflow language |
| skills-as-code | externalized procedural expertise that needs routing, verification, and capability binding | `2604.03088`, `2602.12670`, `2604.01687`, `2604.08224` | not raw portable markdown by default |
| literate programming for agents | the article's synthesis label for inspectable specs plus validators, traces, provenance, and human-readable context | ICM plus the spec/harness/trace stack | not a paper-native standard |

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

The 2026-04-21 claim-state gap pass added three drafting caveats without changing the lead. Context-file value is metric-dependent. Specification formality does not monotonically improve conformance. Skills can help, but production skill substrate requires capability binding, verification, routing, and namespace control. The pass is recorded in [`research-notes/2026-04-21-claim-state-gap-contradiction-pass.md`](research-notes/2026-04-21-claim-state-gap-contradiction-pass.md).

The 2026-04-21 article-surface pressure pass completed the missing surface work. Validation is now framed as lifecycle infrastructure, workflow-as-namespace is bounded as navigational synthesis, and static contradiction checking is now part of the validation stack. The surface-completion note is [`research-notes/2026-04-21-article-surface-pressure-pass.md`](research-notes/2026-04-21-article-surface-pressure-pass.md).

## P2a Local Intake Read

The 2026-04-21 P2a local intake converted the queued trace/provenance papers into package evidence. The note is [`research-notes/2026-04-21-p2a-local-intake-trace-provenance.md`](research-notes/2026-04-21-p2a-local-intake-trace-provenance.md).

The intake tightened the stack this way:

- AgentPex makes traces evaluatable against prompt-derived rules, which strengthens the claim that logs are debugging surfaces rather than the artifact of record.
- AgentFixer makes validation look like lifecycle infrastructure: prompt analysis, cross-stage checks, trace comparison, diagnosis, and refinement in one loop.
- Claim-Level Auditability makes contradiction transparency and claim-level provenance paper-backed requirements rather than only transferred workflow ideas.

The safe consequence is now explicit:

Reviewable Runs can cover trace checking and parts of failure localization. They do not yet satisfy claim-level provenance. That next layer requires contradiction transparency, provenance coverage, provenance soundness, and audit effort to be queryable at the claim level.

## Surface Completion

The article can now safely say this:

Workflow specifications are the visible surface. Context engineering is the broader substrate that feeds them. Validation is the hinge that keeps them attached to the environment. Policy enforcement and contradiction checks keep the control surface coherent. Reviewable traces and drift checks make the system debuggable. Claim-level auditability is the next provenance layer. Skills belong in the story as an externalized procedural layer, but only with explicit routing, verification, and capability binding. "Literate workflow programming" remains the article's synthesis label for that stack, not the name of an already-settled paper category.

## Next Research Tasks

1. Draft from the article-ready claim set only after each body claim has ledger status, contradiction status, and rubric status.
2. Use the term boundaries and the trace stack explicitly in the draft: trace checking, failure localization, then claim-level provenance.
3. Keep `imports`, package-as-object semantics, full Evidence Governance contradiction-ledger machinery beyond this curated register, and repo-wide validator promotion parked until there is stronger local proof.
4. Use P2b selectively only if the draft exposes a real gap in context-file evidence, skills evidence, or contradiction-check depth.
5. Decide whether a local claim-provenance experiment is warranted before touching `phased-strategy/`.
