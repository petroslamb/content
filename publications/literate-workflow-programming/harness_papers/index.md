# Harness Papers

Curated sub-index for harness-adjacent papers around `literate-workflow-programming/`.

Use this folder to track:

- alphaXiv overview value as a fast editorial read
- implementation or companion-resource links exposed by `alphaxiv paper resources`
- alphaXiv social signal
- whether the paper is a direct donor to the current literate-workflow-programming package, a strong adjacent donor, or better treated as a separate harness/self-improvement line

This is not the canonical intake index. The canonical evidence surface remains [`../papers/index.md`](../papers/index.md).

## Local Harness Library

The papers in this shortlist now have a dedicated local library alongside this index:

- PDFs: [`pdfs/`](pdfs/)
- Markdown: [`markdown/`](markdown/)
- Metadata: [`metadata/`](metadata/)

Intake notes:

- 24 unique papers from this shortlist or its immediate literate-programming follow-up were stored locally on 2026-04-23.
- Markdown was generated from alphaXiv full-text extraction where available.
- `2604.18071v1` used repo-local PDF conversion as a fallback because alphaXiv full text was unavailable.
- `2408.04820v4`, `2502.17441v1`, `2510.09073v1`, and `2405.06907v2` were added after an assistant-confirmed missing-paper pass.

## Scope And Method

- Ranking is sorted by alphaXiv `upvotes_count` pulled on `2026-04-23`.
- Social signal is shown as `upvotes / last-30-day visits`.
- `Implementation / resource` comes from `alphaxiv paper resources --json` and may be a runnable artifact, a companion repo, or only a survey/listing repo.
- `Overview value` is an editorial judgment for this package:
  - `very high`: overview is immediately useful as a synthesis/blog read for the package
  - `high`: useful overview with clear transfer value
  - `medium`: useful but secondary or narrower
  - `low`: mostly separate from the current package object

## Likes-Sorted Index

| Social | Paper | Overview Value | Implementation / Resource | Fit For Literate | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `617 / 108` | [A Self-Improving Coding Agent](https://www.alphaxiv.org/overview/2504.15228) | medium | [SelfImprovingAgent](https://github.com/NullLabTests/SelfImprovingAgent) | mostly separate | useful pressure on self-modifying agents, weak support for workflow-spec-as-source |
| `416 / 10.7k` | [Meta-Harness](https://www.alphaxiv.org/overview/2603.28052) | high | [meta-harness-tbench2-artifact](https://github.com/stanford-iris-lab/meta-harness-tbench2-artifact) | strong adjacent; separate harness line candidate | strong proof that harness engineering matters, but optimizes code harnesses rather than human-readable source surfaces |
| `400 / 241` | [Toward Efficient Agents](https://www.alphaxiv.org/overview/2601.14192) | medium | [Awesome-Efficient-Agents](https://github.com/yxf203/Awesome-Efficient-Agents) | peripheral | efficiency background on memory, tool learning, and planning rather than a direct harness/source paper |
| `280 / 310` | [Agent0](https://www.alphaxiv.org/overview/2511.16043) | low | [Agent0](https://github.com/aiming-lab/Agent0) | mostly separate | self-evolving agent line, not a strong donor to the contract-layer thesis |
| `224 / 4.3k` | [Natural-Language Agent Harnesses](https://www.alphaxiv.org/overview/2603.25723) | very high | [natural-language-agent-harnesses](https://github.com/curated-skills/natural-language-agent-harnesses) | direct donor | clearest paper for externalized natural-language harness logic, contracts, roles, stage structure, and durable artifacts |
| `217 / 1.2k` | [SkillsBench](https://www.alphaxiv.org/overview/2602.12670) | medium | [skillsbench](https://github.com/benchflow-ai/skillsbench) | secondary donor | good for the skills layer, especially where the package discusses whether curated skills actually help |
| `210 / 3.1k` | [SKILL0](https://www.alphaxiv.org/overview/2604.02268) | medium | [SkillZero](https://github.com/ZJU-REAL/SkillZero) | mostly separate; skills-internalization pressure | good pressure against assuming runtime skill files are the endpoint |
| `153 / 284` | [SWE-agent](https://www.alphaxiv.org/overview/2405.15793) | high | none in resources | strong adjacent | important ancestor for agent-computer interfaces and harness/interface design, even if not framed as literate workflow source |
| `114 / 270` | [Meta Context Engineering via Agentic Skill Evolution](https://www.alphaxiv.org/overview/2601.21557) | medium | [meta-context-engineering](https://github.com/metaevo-ai/meta-context-engineering) | strong adjacent | useful for context-engineering evolution and skill/history-driven harness refinement |
| `90 / 2.4k` | [Dive into Claude Code](https://www.alphaxiv.org/overview/2604.14228) | very high | [Dive-into-Claude-Code](https://github.com/VILA-Lab/Dive-into-Claude-Code) | strong adjacent to direct donor | one of the best applied reads for the package's "the real system lives in the harness" seam |
| `76 / 129` | [AOrchestra](https://www.alphaxiv.org/overview/2602.03786) | medium | [AOrchestra](https://github.com/FoundationAgents/AOrchestra) | strong adjacent | useful for sub-agent creation, orchestration, and dynamic capability assembly |
| `59 / 432` | [Building Effective AI Coding Agents for the Terminal](https://www.alphaxiv.org/overview/2603.05344) | high | [opendev](https://github.com/opendev-to/opendev) | strong direct donor | strong terminal-native harness/context-engineering paper with explicit scaffolding, compaction, memory, and safety lessons |
| `54 / 1.9k` | [Externalization in LLM Agents](https://www.alphaxiv.org/overview/2604.08224) | high | none in resources | strong synthesis donor | very useful umbrella paper for memory, skills, protocols, and harnesses as one externalized systems story |
| `47 / 864` | [AutoHarness](https://www.alphaxiv.org/overview/2603.03329) | medium | none in resources | strong adjacent; separate harness line candidate | good evidence that synthesized harnesses can dominate larger models, but it points more toward code-policy/harness automation than literate workflow source |
| `39 / 80` | [Codified Context](https://www.alphaxiv.org/overview/2602.20478) | high | none in resources | strong adjacent to direct donor | strong support for persistent, codified context infrastructure in real codebases |
| `34 / 271` | [From Static Templates to Dynamic Runtime Graphs](https://www.alphaxiv.org/overview/2603.22386) | high | [awesome-agentic-workflow-optimization](https://github.com/IBM/awesome-agentic-workflow-optimization) | strong taxonomy donor | very useful vocabulary paper for separating templates, realized graphs, and traces |
| `29 / 222` | [SkVM](https://www.alphaxiv.org/overview/2604.03088) | medium | none in resources | secondary donor | important pressure paper that says skills need capability binding/runtime adaptation across harnesses |
| `18 / 2` | [AIOS Compiler](https://www.alphaxiv.org/overview/2405.06907) | high | none in resources | strong adjacent | strongest missing "natural language as programming language" pressure paper, but broader than the package's markdown and harness-file object |
| `13 / 110` | [AgentSPEX](https://www.alphaxiv.org/overview/2604.13346) | very high | [AgentSPEX](https://github.com/ScaleML/AgentSPEX) | direct donor | one of the strongest direct papers for workflow specification as governed source with explicit control flow, state, verification, and runtime support |
| `8 / 4` | [Natural Language Outlines for Code](https://www.alphaxiv.org/overview/2408.04820) | very high | none in resources | direct donor | strongest literal literate-programming paper in the missing pass: natural-language outlines act as a bidirectionally synchronized high-level source surface for code |
| `4 / 2` | [Literate Tracing](https://www.alphaxiv.org/overview/2510.09073) | high | none in resources | strong adjacent | moves the "literate" idea from authoring into execution-trace explanation and gives the package a credible literate-observability seam |
| `3 / 7` | [Architectural Design Decisions in AI Agent Harnesses](https://www.alphaxiv.org/overview/2604.18071) | high | [arch-compiler-ai-harness-in-action](https://github.com/inetgas/arch-compiler-ai-harness-in-action) | strong adjacent to direct donor | empirically important for the harness layer; current resource link looks more like a related demo than a reproducibility artifact |
| `1 / 1` | [Renaissance of Literate Programming in the Era of LLMs](https://www.alphaxiv.org/overview/2502.17441) | high | none in resources | direct donor | useful literal donor for literate-programming framing in large projects, especially where the package wants stronger project-scale coherence arguments |
| `0 / 3` | [Spec Kit Agents](https://www.alphaxiv.org/overview/2604.05278) | high | none in resources | strong direct donor | strong paper for context-grounded workflow phases, validation hooks, and spec-driven agent work despite low current alphaXiv signal |

## Reading Priority For This Package

If the goal is specifically to strengthen `literate-workflow-programming`, the best next reads are not the same as the like-sorted order.

### P0 Direct Donors

1. [Natural Language Outlines for Code](https://www.alphaxiv.org/overview/2408.04820)
2. [Natural-Language Agent Harnesses](https://www.alphaxiv.org/overview/2603.25723)
3. [AgentSPEX](https://www.alphaxiv.org/overview/2604.13346)
4. [Building Effective AI Coding Agents for the Terminal](https://www.alphaxiv.org/overview/2603.05344)
5. [Spec Kit Agents](https://www.alphaxiv.org/overview/2604.05278)
6. [Renaissance of Literate Programming in the Era of LLMs](https://www.alphaxiv.org/overview/2502.17441)

### P1 Strong Adjacent Donors

1. [Dive into Claude Code](https://www.alphaxiv.org/overview/2604.14228)
2. [Architectural Design Decisions in AI Agent Harnesses](https://www.alphaxiv.org/overview/2604.18071)
3. [Literate Tracing](https://www.alphaxiv.org/overview/2510.09073)
4. [AIOS Compiler](https://www.alphaxiv.org/overview/2405.06907)
5. [From Static Templates to Dynamic Runtime Graphs](https://www.alphaxiv.org/overview/2603.22386)
6. [Externalization in LLM Agents](https://www.alphaxiv.org/overview/2604.08224)
7. [Codified Context](https://www.alphaxiv.org/overview/2602.20478)
8. [SWE-agent](https://www.alphaxiv.org/overview/2405.15793)

### Skills Layer Only

1. [SkillsBench](https://www.alphaxiv.org/overview/2602.12670)
2. [SkVM](https://www.alphaxiv.org/overview/2604.03088)
3. [Meta Context Engineering](https://www.alphaxiv.org/overview/2601.21557)

### Better For A Separate Harnesses Or Self-Improvement Publication

1. [Meta-Harness](https://www.alphaxiv.org/overview/2603.28052)
2. [AutoHarness](https://www.alphaxiv.org/overview/2603.03329)
3. [A Self-Improving Coding Agent](https://www.alphaxiv.org/overview/2504.15228)
4. [Agent0](https://www.alphaxiv.org/overview/2511.16043)
5. [SKILL0](https://www.alphaxiv.org/overview/2604.02268)

## Current Take

The package's strongest `literate-workflow-programming` seam still comes from the intersection of:

- externalized natural-language harnesses
- explicit workflow/spec languages
- context-grounded validation hooks
- contract-layer architecture around a thin model loop

The best separate `harnesses` seam is different:

- harness optimization itself
- code harness synthesis
- self-evolving harnesses
- sub-agent orchestration as a controllable runtime design space

That distinction is why the folder keeps both direct donors and separate-line candidates in one place without collapsing them into one thesis.

## Recent Literate-Programming Discovery Pass

The missing-paper pass produced four papers that were strong enough to intake locally and one that stayed out.

### Intaken From This Pass

1. [Natural Language Outlines for Code](https://www.alphaxiv.org/overview/2408.04820)
   Local files: [`pdfs/2408.04820v4.pdf`](pdfs/2408.04820v4.pdf), [`markdown/2408.04820v4.md`](markdown/2408.04820v4.md), [`metadata/2408.04820.json`](metadata/2408.04820.json)
2. [Renaissance of Literate Programming in the Era of LLMs](https://www.alphaxiv.org/overview/2502.17441)
   Local files: [`pdfs/2502.17441v1.pdf`](pdfs/2502.17441v1.pdf), [`markdown/2502.17441v1.md`](markdown/2502.17441v1.md), [`metadata/2502.17441.json`](metadata/2502.17441.json)
3. [Literate Tracing](https://www.alphaxiv.org/overview/2510.09073)
   Local files: [`pdfs/2510.09073v1.pdf`](pdfs/2510.09073v1.pdf), [`markdown/2510.09073v1.md`](markdown/2510.09073v1.md), [`metadata/2510.09073.json`](metadata/2510.09073.json)
4. [AIOS Compiler](https://www.alphaxiv.org/overview/2405.06907)
   Local files: [`pdfs/2405.06907v2.pdf`](pdfs/2405.06907v2.pdf), [`markdown/2405.06907v2.md`](markdown/2405.06907v2.md), [`metadata/2405.06907.json`](metadata/2405.06907.json)

### Excluded For Now

1. [Prompt Orchestration Markup Language](https://www.alphaxiv.org/overview/2508.13948)
   Strong prompt-structure paper, but the current package still treats it as scope creep relative to literate workflow source surfaces.
2. [SWE-AGI](https://www.alphaxiv.org/overview/2602.09447)
   Useful for specification-driven coding benchmarks, but still off-center for the package's human-readable source-language thesis.

The compact reasoning and assistant verification notes for this pass live in [`../research-notes/alphaxiv-discussions/019dbbe2-literate-workflow-papers.md`](../research-notes/alphaxiv-discussions/019dbbe2-literate-workflow-papers.md) and [`../research-notes/alphaxiv-discussions/019dbbe5-intake-confirmation.md`](../research-notes/alphaxiv-discussions/019dbbe5-intake-confirmation.md).
