# Literate Workflow Programming Paper Index

This index tracks papers for the `literate-workflow-programming/` research package.

## Locally Intaken

### Natural-Language Agent Harnesses

- arXiv: [`2603.25723v1`](https://arxiv.org/abs/2603.25723)
- Authors: Linyue Pan, Lexiao Zou, Shuo Guo, Jingchen Ni, Hai-Tao Zheng
- Local PDF: [`2603.25723.pdf`](2603.25723.pdf)
- Local markdown: [`markdown/2603.25723.md`](markdown/2603.25723.md)
- Metadata: [`metadata/2603.25723.json`](metadata/2603.25723.json)
- Relevance: Strong support for externalized harness logic as a portable natural-language artifact executed by a runtime with explicit contracts, durable artifacts, and adapters.

### AgentSPEX: An Agent SPecification and EXecution Language

- arXiv: [`2604.13346v1`](https://arxiv.org/abs/2604.13346)
- Authors: Pengcheng Wang, Jerry Huang, Jiarui Yao, Rui Pan, Peizhi Niu, Yaowenqi Liu, Ruida Wang, Renhao Lu, Yuwei Guo, Tong Zhang
- Local PDF: [`2604.13346.pdf`](2604.13346.pdf)
- Local markdown: [`markdown/2604.13346.md`](markdown/2604.13346.md)
- Metadata: [`metadata/2604.13346.json`](metadata/2604.13346.json)
- Relevance: Direct evidence for explicit workflow source languages: typed steps, branching, loops, reusable submodules, explicit state/context management, checkpointing, logging, replay, and a harness runtime.

### Bootstrapping Coding Agents: The Specification Is the Program

- arXiv: [`2603.17399v1`](https://arxiv.org/abs/2603.17399)
- Authors: Martin Monperrus
- Local PDF: [`2603.17399.pdf`](2603.17399.pdf)
- Local markdown: [`markdown/2603.17399.md`](markdown/2603.17399.md)
- Metadata: [`metadata/2603.17399.json`](metadata/2603.17399.json)
- Relevance: Key pressure paper. It supports specification-as-source, but narrows reviewable logs into derived traces rather than the artifact of record.

### Test-Driven AI Agent Definition

- arXiv: [`2603.08806v1`](https://arxiv.org/abs/2603.08806)
- Authors: Tzafrir Rehan
- Local PDF: [`2603.08806.pdf`](2603.08806.pdf)
- Local markdown: [`markdown/2603.08806.md`](markdown/2603.08806.md)
- Metadata: [`metadata/2603.08806.json`](metadata/2603.08806.json)
- Relevance: Treats behavioral specifications as inputs that compile into tests and refined prompt artifacts, giving this package its strongest testing and regression vocabulary.

### ContextCov: Deriving and Enforcing Executable Constraints from Agent Instruction Files

- arXiv: [`2603.00822v1`](https://arxiv.org/abs/2603.00822)
- Authors: Reshabh K Sharma
- Local PDF: [`2603.00822.pdf`](2603.00822.pdf)
- Local markdown: [`markdown/2603.00822.md`](markdown/2603.00822.md)
- Metadata: [`metadata/2603.00822.json`](metadata/2603.00822.json)
- Relevance: Direct evidence that agent instruction files should become executable specifications with generated guardrails, runtime shims, and architectural validators.

### Interpretable Context Methodology: Folder Structure as Agentic Architecture

- arXiv: [`2603.16021v2`](https://arxiv.org/abs/2603.16021)
- Authors: Jake Van Clief, David McDermott
- Local PDF: [`2603.16021v2.pdf`](2603.16021v2.pdf)
- Local markdown: [`markdown/2603.16021v2.md`](markdown/2603.16021v2.md)
- Relevance: Anchor paper for filesystem structure, markdown stage contracts, layered context loading, human review gates, and compiler/source-map analogies for agent workflows.
- Intake note: The local v2 PDF and converted markdown use the title and abbreviation `Interpretable Context Methodology` / `ICM`. The alphaXiv abstract text still refers to `Model Workspace Protocol` / `MWP`, so use the local PDF text as the canonical version for this intake.

### SkVM: Revisiting Language VM for Skills across Heterogenous LLMs and Harnesses

- arXiv: [`2604.03088v3`](https://arxiv.org/abs/2604.03088)
- Authors: Le Chen, Erhu Feng, Yubin Xia, Haibo Chen
- Local PDF: [`2604.03088.pdf`](2604.03088.pdf)
- Local markdown: [`markdown/2604.03088.md`](markdown/2604.03088.md)
- Metadata: [`metadata/2604.03088.json`](metadata/2604.03088.json)
- Relevance: Strong support for treating skills as code with compilation/runtime concerns across heterogeneous models and harnesses; also a pressure paper against leaving skills as raw markdown context at runtime.

## Conversion Notes

- The P0 batch was downloaded through alphaXiv PDF resolution on 2026-04-20 and converted with the repo-local `markitdown` binary.
- `2603.25723`, `2603.08806`, and `2603.00822` contain table-like first-page extraction noise, but their body text is usable.
- `2604.13346` and `2603.17399` contain vertical arXiv-header noise at the top, but section text is usable.
- `2604.03088` converted cleanly enough for research use, with minor font warnings during conversion.

## Intake Queue

These papers are indexed for deliberate download and conversion later. They are not yet stored locally in this package.

| Priority | arXiv ID | Title | Why It Matters Here |
| :--- | :--- | :--- | :--- |
| P1 | [`2510.04173`](https://arxiv.org/abs/2510.04173) | Open Agent Specification | Agent and workflow representation across runtimes, with standardized evaluation. |
| P1 | [`2512.19769`](https://arxiv.org/abs/2512.19769) | A Declarative Language for Building and Orchestrating LLM-Powered Agent Workflows | Declarative workflow DSL separating agent specification from implementation and deployment. |
| P1 | [`2512.18940`](https://arxiv.org/abs/2512.18940) | FASTRIC: Prompt Specification Language for Verifiable LLM Interactions | Prompt specification language, finite-state framing, and procedural conformance checks. |
| P1 | [`2603.20380`](https://arxiv.org/abs/2603.20380) | ALARA for Agents | Least-privilege context/tool scoping through structured context-agent-tool definitions. |
| P1 | [`2504.11703`](https://arxiv.org/abs/2504.11703) | Progent | Deterministic tool privilege control and policy enforcement around agent actions. |
| P1 | [`2601.04748`](https://arxiv.org/abs/2601.04748) | When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail | Anchor for the `illusion-of-swarm` contradiction: single-agent-plus-skills works until routing/selection becomes semantically overloaded. |
| P2 | [`2603.05344`](https://arxiv.org/abs/2603.05344) | Building Effective AI Coding Agents for the Terminal | Terminal-native harnesses, context management, safety controls, lazy tool discovery, and instruction fade-out. |
| P2 | [`2512.05470`](https://arxiv.org/abs/2512.05470) | Everything is Context | Filesystem abstraction for persistent, governed context artifacts. |
| P2 | [`2602.20478`](https://arxiv.org/abs/2602.20478) | Codified Context | Hot/cold memory, persistent project conventions, and multi-session agent coherence. |
| P2 | [`2604.08224`](https://arxiv.org/abs/2604.08224) | Externalization in LLM Agents | Systems-level framing for memory, skills, protocols, and harnesses as external cognitive infrastructure. |
| P2 | [`2604.05278`](https://arxiv.org/abs/2604.05278) | Spec Kit Agents | Phase-level context-grounding and validation hooks for agentic workflows. |
| P2 | [`2505.20127`](https://arxiv.org/abs/2505.20127) | Agentic AI Process Observability | Process and causal discovery for behavioral variability in agent trajectories. |
| P2 | [`2508.02736`](https://arxiv.org/abs/2508.02736) | AgentSight | Observability that links high-level agent intent to low-level system effects. |
| P2 | [`2602.11988`](https://arxiv.org/abs/2602.11988) | Evaluating AGENTS.md | Contradictory pressure against bloated repository-level context files. |
| P2 | [`2601.20404`](https://arxiv.org/abs/2601.20404) | On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents | Counterpoint to `2602.11988`: context files can improve runtime and token use in some PR workflows. |
| P2 | [`2511.12884`](https://arxiv.org/abs/2511.12884) | Agent READMEs | Empirical view of agent context files as evolving configuration code. |
| P3 | [`2508.11126`](https://arxiv.org/abs/2508.11126) | AI Agentic Programming | Survey context for planning, context management, tool integration, monitoring, and benchmarks in agentic programming. |

## Current Reading Order

1. `2603.16021` for ICM and the filesystem/context-layer anchor.
2. `2603.17399`, `2603.08806`, and `2604.13346` for specification-as-program and language/runtime framing.
3. `2603.00822`, `2603.20380`, and `2504.11703` for the enforcement layer.
4. `2604.03088` and `2601.04748` for skills-as-code and the semantic-overload limit.
5. `2602.11988`, `2601.20404`, and `2511.12884` for context-file evidence and failure modes.
6. `2505.20127` and `2508.02736` for observability and source-map directions.
