# alphaXiv Discussion: Literate workflow papers

Date: 2026-04-23

Session id: `019dbbe2-9392-7560-a573-eb1ba25c6e40`

Title: `Literate Workflow Papers`

Full history:

```bash
.venv/bin/alphaxiv assistant history 019dbbe2-9392-7560-a573-eb1ba25c6e40
```

## Question Asked

Rank the best missing 2024-2026 papers for the `literate-workflow-programming` package after grounding the assistant in the current harness shortlist, with a strict split between direct donors, strong-adjacent papers, and tempting but off-thesis candidates.

## Papers Or Claims In Scope

- `2408.04820` / `Natural Language Outlines for Code: Literate Programming in the LLM Era`
- `2502.17441` / `Renaissance of Literate Programming in the Era of LLMs: Enhancing LLM-Based Code Generation in Large-Scale Projects`
- `2510.09073` / `Literate Tracing`
- `2602.09447` / `SWE-AGI: Benchmarking Specification-Driven Software Construction with MoonBit in the Era of Autonomous Agents`
- `2405.06907` / `AIOS Compiler: LLM as Interpreter for Natural Language Programming and Flow Programming of AI Agents`
- `2508.13948` / `Prompt Orchestration Markup Language`
- Current harness shortlist in `../../harness_papers/index.md`
- Package claim boundary: markdown, natural-language specs, harness files, and adjacent contract surfaces as source languages for agent workflows

## Extracted Takeaways

- `2408.04820` is the strongest direct missing donor from a literal literate-programming angle. Its bidirectional sync between natural-language outlines and code strengthens the package's "natural language as source surface" seam rather than merely adding more prompt-engineering evidence.
- `2502.17441` is a real direct donor, but weaker than `2408.04820`. It helps justify literate-programming framing for LLM-era code generation, especially for large-project coherence, without changing the package as much as the outlines paper.
- `2510.09073` is worth treating as a strong adjacent donor, not a direct one. It moves "literate" from authoring/spec surfaces into execution-trace explanation and therefore sharpens the observability/log side of the package rather than the source-language claim itself.
- `2405.06907` and `2508.13948` are credible adjacent candidates beyond the originally retrieved four. They matter because they pressure the package toward "natural language / markup as executable language" and "markup as prompt contract surface," respectively.
- `2602.09447` should stay out of the direct queue. It is useful as a specification-driven benchmark but its object is agent capability under spec pressure, not literate workflow surfaces as human-readable source.
- The assistant surfaced `Agent READMEs` as relevant context-file evidence, but the cited id was wrong in the chat. Deterministic follow-up confirmed the correct paper is `2511.12884`, which was already in the package queue, so it does not count as a new missing paper from this session.

## Adopted

- Promote `2408.04820` to the top of the "missing direct donor" queue for this package.
- Promote `2502.17441` as the next direct literate-programming donor after `2408.04820`.
- Treat `2510.09073` as a likely P1 adjacent paper for the trace/observability seam rather than as a core source-language anchor.
- Add `2405.06907` and `2508.13948` to the "adjacent but worth pressure-testing" shortlist when the package needs stronger language/compiler/markup framing.
- Keep `2602.09447` out of the direct donor shortlist.

## Rejected Or Parked

- Do not let a generic "specification-driven coding" frame absorb the package. `2602.09447` stays parked unless the package explicitly shifts toward benchmarked spec-to-code performance.
- Do not treat assistant-provided ids as authoritative without deterministic retrieval. The `Agent READMEs` citation in the chat was incorrect and needed verification.
- Do not promote `2510.09073` into the direct donor tier without first deciding that the package needs a stronger literate-trace or observability section.

## Where It Entered The Package

- `../../harness_papers/index.md`
- `./index.md`

## Current Status

- Distilled
