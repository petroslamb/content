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

## Next Research Tasks

1. Sketch the `spec-diff` experiment for one real workflow.
2. Extract exact P0 claims into the claim ledger as the papers are read in detail.
3. Separate existing terms: context engineering, natural-language harness, agent specification language, prompt specification language, skills-as-code, and literate programming for agents.
4. Decide whether `imports` should stay advisory links, become declared dependencies, or eventually compile into context packets.
5. Intake P1 only after the next literature question is sharpened by the experiment.
6. Identify what should be extracted back into `phased-strategy/` only after the evidence is strong.
