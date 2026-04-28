# Reopened Pivot Grounding Review

## Candidate

`The Specification Surface Is the New Source of Truth`

## Grounding Verdict

`pivot_cleared_for_north_star_attempt`

## What Changed Since The Closure

The stopped `contract layer` candidate was blocked because it remained too architecture-internal. The reopened evidence pass found a more portable object:

controlled, typed, verifiable specification surfaces that often use natural-language syntax but function as source-of-truth artifacts.

This is not the claim that ordinary prose is executable. The evidence points the other way: loose context can hurt agent performance, while constrained specifications, contracts, outlines, and state interfaces are the pieces that become operational.

## Positive Evidence

| Evidence | What It Licenses |
| :--- | :--- |
| `2408.04820` Natural Language Outlines for Code | Natural-language outlines can become living, synchronized program-comprehension and code-review surfaces, not just stale comments. |
| `2603.17399` Bootstrapping Coding Agents | The strongest source-of-truth anchor: a coding agent can regenerate implementation from a natural-language specification, making the spec the stable artifact. |
| `2603.25723` Natural-Language Agent Harnesses | Harness control logic can be externalized into executable natural-language artifacts with contracts, roles, stage structure, adapters, state semantics, and failure taxonomies. |
| `2604.13346` AgentSPEX | Declarative workflow specifications can carry explicit control flow, state, context management, checkpointing, observability, and replay. |
| `2604.08224` Externalization in LLM Agents | The larger systems frame: reliability improves when memory, skills, protocols, and harnesses move cognitive burden into inspectable external infrastructure. |
| `2510.21413` Context Engineering for AI Agents in Open-Source Software | AI context files are emerging in real repositories as persistent machine-facing project artifacts, with active refinement in maintained projects. |
| `2511.12884` Agent READMEs | Agent context files behave more like living configuration artifacts than static documentation, but also create context debt and under-specify non-functional requirements. |
| `2602.00180` Spec-Driven Development | Specifications can become authoritative contracts for AI-assisted development through spec-first, spec-anchored, and spec-as-source workflows. |
| `2603.24284` The Specification Gap | Incomplete specifications cause measurable coordination failure in multi-agent code generation; rich specifications matter more than conflict reports alone. |
| `2512.14012` Professional Software Developers Don't Vibe, They Control | The professional practice counterweight: skilled developers use agents through supervision, explicit prompting, design control, and manual verification. |
| `2512.14805` Sharing State Between Prompts and Programs | Natural-language code can interact with formal program state through defined interfaces, effects, and handlers. |
| `2508.06942` CNL-P | Controlled natural language can be linted and statically checked, turning prompt surfaces toward software-engineering discipline. |
| `2603.15691` VibeContract | Task-level contracts can make AI-native coding more traceable, testable, and auditable. |

## Negative Evidence

`2602.11988` blocks the loose version of the thesis. Repository-level context files can reduce success and raise cost, and human-provided context gives only marginal gains at higher expense.

That negative result is useful. It prevents the reopened candidate from saying "more natural language context is better." The candidate must say something narrower:

operational specification surfaces matter only when they are scoped, structured, maintained, validated, and trace-linked.

## Why This Beats The Contract-Layer Candidate

`contract layer` named an architecture location. `specification surface` names a public object people can inspect, write, version, test, and argue about.

The candidate now crosses more than governed agent-workflow doctrine:

- code comprehension and review
- professional AI-assisted software practice
- natural/formal program interoperability
- context files in open-source repositories
- QA and verification for vibe-coded systems
- agent harness specification and execution

## What It Does Not Yet License

- It does not license a broad claim that loose prose is code.
- It does not prove every context file is beneficial.
- It does not prove natural language replaces formal specification.
- It does not yet clear the north-star viability gate.

## Immediate Consequence

The umbrella route should reopen around this candidate and run the north-star viability gate next. This verdict clears the candidate for a north-star attempt, not for successor-leaf initialization.
