# alphaXiv Discussion: Literate Workflow Thesis Test

Date: 2026-04-20

Session id: `019dac7e-9593-70a6-bb54-167db4667d47`

Title: `Literate Workflow Thesis Test`

Full history:

```bash
.venv/bin/alphaxiv assistant history 019dac7e-9593-70a6-bb54-167db4667d47
```

## Question Asked

Pressure-test the package thesis:

> Markdown workflow docs, skills, indexes, imports, package state, validators, and reviewable-run logs may be becoming a literate programming substrate for agent workflows, not just context-engineering prose.

The session asked which P0 papers support the thesis, which narrow or contradict it, what vocabulary is defensible, and what one implementation experiment should come next.

## Papers In Scope

- `2603.16021` Interpretable Context Methodology
- `2603.25723` Natural-Language Agent Harnesses
- `2604.13346` AgentSPEX
- `2603.17399` Bootstrapping Coding Agents
- `2603.08806` Test-Driven AI Agent Definition
- `2603.00822` ContextCov
- `2604.03088` SkVM

## Extracted Takeaways

The session sharpened the package thesis:

- the strongest support is for structured workflow specifications as source artifacts
- the weakest term is `literate programming`, unless the repo proves prose-heavy specs can be compiled, checked, and traced
- `imports` and `package state` are under-supported by the P0 papers
- validators are strongly supported through ContextCov and TDAD
- reviewable logs are useful, but only as traces and source maps
- Bootstrapping Coding Agents is the main correction: the specification is primary
- SkVM is the main pressure on raw markdown skills: production portability needs compilation or capability binding

## Design Guidance Adopted

- Use `workflow specification`, `stage contract`, `context layer`, `validator`, `runtime trace`, `source map`, and `spec drift` as safer vocabulary.
- Keep `markdown programming language`, `imports`, `package object`, and `compiler` as experimental or metaphorical until implemented.
- Treat `spec-diff` as the next repo experiment.
- Keep research inside this package until it changes a proof-run requirement or workflow policy.

## Where It Entered The Package

- [`../2026-04-20-p0-intake-synthesis.md`](../2026-04-20-p0-intake-synthesis.md)
- [`../2026-04-20-spec-diff-experiment.md`](../2026-04-20-spec-diff-experiment.md)
- [`../../claim-ledger.md`](../../claim-ledger.md)
- [`../../literate-workflow-programming.md`](../../literate-workflow-programming.md)

## Current Status

Distilled. The extraction note is the tracked package artifact. The full remote transcript remains recoverable through the session id.
