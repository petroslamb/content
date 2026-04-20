# Markdown Workflow Language Research Note

Date: 2026-04-20

Status: early framing note.

alphaXiv discussion: [`alphaxiv-discussions/019dac64-markdown-workflow-compiler.md`](alphaxiv-discussions/019dac64-markdown-workflow-compiler.md)

## Prompt

The working question was whether this package's emerging frame already exists in the literature:

> Can markdown workflow docs, skills, indexes, imports, package state, validators, and reviewable logs behave like a programming language in English or a compiler architecture for agent workflows?

The alphaXiv pass searched for natural-language harnesses, specification languages, prompt specification languages, skills-as-code, and "the specification is the program" style work.

## Initial Finding

The idea exists in fragments, but not yet as one settled category.

Closest terms:

- filesystem-based agent architecture
- natural-language agent harnesses
- declarative agent workflow language
- agent specification and execution language
- prompt specification language
- test-driven agent definition
- skills-as-code
- context engineering
- literate programming for agents

The package's synthesis is probably best described as:

> literate workflow programming for agents

This is stronger than "prompt engineering" and broader than ICM. It treats markdown and adjacent files as a source layer for agent-operated workflows.

## Literature Anchors

| Paper | Contribution To This Frame |
| :--- | :--- |
| [`2603.16021`](https://arxiv.org/abs/2603.16021) | ICM: folder structure, markdown contracts, layered context, and source-map future work. |
| [`2603.25723`](https://arxiv.org/abs/2603.25723) | Natural-language harnesses: executable harness behavior externalized into editable natural language plus runtime contracts. |
| [`2604.13346`](https://arxiv.org/abs/2604.13346) | AgentSPEX: explicit agent workflow language with typed steps, state, verification, logging, and reusable modules. |
| [`2510.04173`](https://arxiv.org/abs/2510.04173) | Open Agent Specification: portable agent/workflow representation across runtimes. |
| [`2512.19769`](https://arxiv.org/abs/2512.19769) | Declarative language for LLM agent workflows. |
| [`2603.17399`](https://arxiv.org/abs/2603.17399) | Specification is the program: the stable artifact is the spec, not the generated implementation. |
| [`2603.08806`](https://arxiv.org/abs/2603.08806) | TDAD: prompts as compiled artifacts, tested against behavioral specifications. |
| [`2512.18940`](https://arxiv.org/abs/2512.18940) | FASTRIC: prompt specification language and procedural conformance. |
| [`2603.00822`](https://arxiv.org/abs/2603.00822) | ContextCov: instruction files converted into executable constraints. |
| [`2604.03088`](https://arxiv.org/abs/2604.03088) | SkVM: skills treated as executable units across heterogeneous models and harnesses. |

## Compiler Analogy

The analogy appears productive if kept precise:

| Programming Concept | Markdown Workflow Equivalent |
| :--- | :--- |
| Source code | Markdown workflow docs, skill files, package READMEs |
| Module | Workflow doc, skill bundle, package surface, or reference bundle |
| Import | Declared context dependency |
| Symbol table | Index files and package maps |
| Function signature | Stage contract with inputs, process, outputs, validators, and stop condition |
| Object instance | Package folder with local state and artifacts |
| Type check | Validator, schema check, policy check, or link check |
| Linker | Import resolver that assembles a bounded context packet |
| Runtime | Harness, model, local tools, and external services |
| Debug trace | Reviewable-run log |
| Source map | Future provenance layer from output back to source context |

## Imports

Imports should start as declared dependencies, not automatic concatenation.

Possible first shape:

```yaml
imports:
  required:
    - path: workflows/skills/alphaxiv/SKILL.md
      role: execution_skill
    - path: publications/literate-workflow-programming/papers/index.md
      role: source_index
  optional:
    - path: publications/illusion-of-swarm/the-illusion-of-the-swarm.md
      role: prior_argument
```

This gives the repo a dependency graph before it creates a context compiler. Later, a script could assemble imports into a context packet and preserve provenance comments, but that should wait until the import graph is useful.

## Modularity And DRY

Use DRY for contracts, commands, stage ids, schemas, policy, and canonical paths.

Do not over-DRY local judgment. Some short reminders should stay near the stage where they matter, because moving all judgment into one global file recreates context bloat.

The principle is:

> DRY the mechanics; keep judgment close to the work.

## OOP vs Functional Style

Use both, at different layers:

- packages are object-like: identity, state, papers, artifacts, lifecycle, archive
- workflows are function-like: inputs plus references produce outputs plus logs
- skills are reusable functions or capabilities
- policies and imports are declarative
- reviewable runs are event traces

This prevents the repo from forcing every concept into one programming style.

## Open Problems

1. Conflict resolution: what happens when imported markdown files disagree?
2. Dead imports: how do we detect context files that are indexed but never used?
3. Source maps: how do we trace a flawed output back to the exact source instruction or artifact?
4. Type system: what counts as a valid workflow output?
5. Executability boundary: when is a markdown file documentation, and when is it an instruction the harness must obey?

## Working Claim

Markdown becomes a programming substrate only when it has declared imports, scoped context layers, explicit inputs and outputs, validators, provenance logs, and policy enforcement.

Plain markdown is not enough. Structured markdown plus a harness begins to look like a language.
