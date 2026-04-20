# alphaXiv Discussion: Markdown Workflow Compiler

Date: 2026-04-20

Session id: `019dac64-2079-70cb-98cd-07677f1310e5`

Title: `Markdown Workflow Compiler`

Full history:

```bash
.venv/bin/alphaxiv assistant history 019dac64-2079-70cb-98cd-07677f1310e5
```

## Question Asked

Does the idea already exist that markdown workflow docs, skills, indexes, imports, package state, and reviewable logs behave like a programming language in English or compiler substrate for agent workflows?

The prompt explicitly tested:

- markdown files as source code
- indexes as symbol tables
- imports as dependency declarations
- workflow docs as function signatures
- packages as objects/state
- skills as functions/capabilities
- validators as tests/type checks
- reviewable runs as debug traces
- OOP vs functional organization for markdown/workflow/skills

## Papers In Scope

- `2603.16021` Interpretable Context Methodology
- `2603.25723` Natural-Language Agent Harnesses
- `2604.03088` SkVM
- `2603.17399` Bootstrapping Coding Agents
- `2603.08806` Test-Driven AI Agent Definition
- `2604.13346` AgentSPEX
- `2512.19769` Declarative Language for LLM Agent Workflows
- `2510.04173` Open Agent Specification
- `2512.18940` FASTRIC
- `2603.00822` ContextCov
- `2601.04748` When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail

## Extracted Takeaways

The discussion did not find a settled name for the full package idea. It treated the repo's frame as a synthesis of existing strands:

- context engineering
- filesystem-based agentic architecture
- natural-language harnesses
- declarative agent specifications
- skills-as-code
- prompt/specification testing
- literate-programming analogies

The closest local phrase remains `literate workflow programming`, but the assistant treated it as a novel synthesis rather than an established field label.

## Design Guidance Adopted

- Prefer scoped transclusion or declared dependencies over blind markdown concatenation.
- Treat skills as closer to pure functions: bounded inputs, bounded outputs, minimal durable state.
- Treat packages as stateful objects only at the package lifecycle level, not inside every skill.
- Keep validators as the closest analogue to tests/type checks.
- Treat reviewable-run logs as debugger/source-map material, not just receipts.
- Avoid deep import nesting because context indirection becomes a model-facing readability cost.

## Design Guidance Rejected Or Parked

- Do not claim the idea already exists as a mature compiler discipline.
- Do not claim ordinary markdown is a programming language without enforcement, validation, and traceability.
- Do not implement imports as simple concatenation before testing scoping and provenance.
- Do not promote OOP as the dominant model; it is useful for package state, while functional style is cleaner for skills and workflow stages.

## Where It Entered The Package

- [`../2026-04-20-markdown-workflow-language.md`](../2026-04-20-markdown-workflow-language.md)
- [`../../literate-workflow-programming.md`](../../literate-workflow-programming.md)
- [`../../claim-ledger.md`](../../claim-ledger.md)

## Current Status

Distilled. Keep as conceptual-vocabulary provenance. Use the paper texts, not this assistant session, as evidence for publication claims.
