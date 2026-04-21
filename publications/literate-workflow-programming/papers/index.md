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

### Open Agent Specification (Agent Spec): A Unified Representation for AI Agents

- arXiv: [`2510.04173v4`](https://arxiv.org/abs/2510.04173)
- Authors: Soufiane Amini, Yassine Benajiba, Cesare Bernardis, Paul Cayet, Hassan Chafi, Abderrahim Fathan, Louis Faucon, Damien Hilloulin, Sungpack Hong, Ingo Kossyk, Tran Minh Son Le, Rhicheek Patra, Sujith Ravi, Jonas Schweizer, Jyotika Singh, Shailender Singh, Weiyi Sun, Kartik Talamadupula, Jerry Xu
- Local PDF: [`2510.04173v4.pdf`](2510.04173v4.pdf)
- Local markdown: [`markdown/2510.04173v4.md`](markdown/2510.04173v4.md)
- Metadata: [`metadata/2510.04173.json`](metadata/2510.04173.json)
- Relevance: Strengthens the portability and standardization side of the claim: agent definitions and workflows can be represented once, adapted across runtimes, and evaluated through a common harness.

### A Declarative Language for Building And Orchestrating LLM-Powered Agent Workflows

- arXiv: [`2512.19769v1`](https://arxiv.org/abs/2512.19769)
- Authors: Ivan Daunis
- Local PDF: [`2512.19769.pdf`](2512.19769.pdf)
- Local markdown: [`markdown/2512.19769.md`](markdown/2512.19769.md)
- Metadata: [`metadata/2512.19769.json`](metadata/2512.19769.json)
- Relevance: Direct support for a workflow DSL that separates agent workflow specification from implementation and deployment, with runtime portability and variant evaluation.

### FASTRIC: Prompt Specification Language for Verifiable LLM Interactions

- arXiv: [`2512.18940v1`](https://arxiv.org/abs/2512.18940)
- Authors: Wen-Long Jin
- Local PDF: [`2512.18940.pdf`](2512.18940.pdf)
- Local markdown: [`markdown/2512.18940.md`](markdown/2512.18940.md)
- Metadata: [`metadata/2512.18940.json`](metadata/2512.18940.json)
- Relevance: Extends the specification-as-source frame to prompt-level interaction protocols, finite-state structure, and procedural conformance checks.

### ALARA for Agents: Least-Privilege Context Engineering Through Portable Composable Multi-Agent Teams

- arXiv: [`2603.20380v1`](https://arxiv.org/abs/2603.20380)
- Authors: Christopher J. Agostino, Nayan D'Souza
- Local PDF: [`2603.20380.pdf`](2603.20380.pdf)
- Local markdown: [`markdown/2603.20380.md`](markdown/2603.20380.md)
- Metadata: [`metadata/2603.20380.json`](metadata/2603.20380.json)
- Relevance: Supplies the least-privilege context and tool-scoping layer: context-agent-tool files become enforceable structure rather than advisory prompt context.

### Progent: Programmable Privilege Control for LLM Agents

- arXiv: [`2504.11703v2`](https://arxiv.org/abs/2504.11703)
- Authors: Tianneng Shi, Jingxuan He, Zhun Wang, Hongwei Li, Linyu Wu, Wenbo Guo, Dawn Song
- Local PDF: [`2504.11703v2.pdf`](2504.11703v2.pdf)
- Local markdown: [`markdown/2504.11703v2.md`](markdown/2504.11703v2.md)
- Metadata: [`metadata/2504.11703.json`](metadata/2504.11703.json)
- Relevance: Strong support for deterministic policy enforcement around tool privileges, giving the workflow-source idea a security and runtime-control pressure test.

### When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail

- arXiv: [`2601.04748v2`](https://arxiv.org/abs/2601.04748)
- Authors: Xiaoxiao Li
- Local PDF: [`2601.04748v2.pdf`](2601.04748v2.pdf)
- Local markdown: [`markdown/2601.04748v2.md`](markdown/2601.04748v2.md)
- Metadata: [`metadata/2601.04748.json`](metadata/2601.04748.json)
- Relevance: Bridges this package to the `illusion-of-swarm` frame by showing why skill libraries can replace multi-agent coordination until semantic routing and skill selection hit capacity limits.

## Conversion Notes

- The P0 batch was downloaded through alphaXiv PDF resolution on 2026-04-20 and converted with the repo-local `markitdown` binary.
- The P1 batch was downloaded through alphaXiv PDF resolution on 2026-04-21 and converted with the repo-local `markitdown` binary.
- Local PDFs are intentionally gitignored third-party evidence. Treat the `Local PDF` links above as local evidence pointers, not as expected tracked files.
- `2603.25723`, `2603.08806`, and `2603.00822` contain table-like first-page extraction noise, but their body text is usable.
- `2604.13346` and `2603.17399` contain vertical arXiv-header noise at the top, but section text is usable.
- `2604.03088` converted cleanly enough for research use, with minor font warnings during conversion.
- `2510.04173v4` and `2504.11703v2` contain compressed spacing in portions of the converted text, but section structure and body text remain usable.
- `2512.19769`, `2512.18940`, `2603.20380`, and `2601.04748v2` contain first-page arXiv/header extraction noise, but the main body text is usable.

## Intake Queue

These papers are indexed for deliberate download and conversion later. They are not yet stored locally in this package.

| Priority | arXiv ID | Title | Why It Matters Here |
| :--- | :--- | :--- | :--- |
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
