# Phase 2 Idea Bank

This is the upstream pressure surface for revising Phase 2.

Use this file before claims, contradictions, or implementation. Its job is to collect the ideas that might justify rewriting the current Phase 2 plan rather than merely executing it.

Suggested order:

1. collect ideas here
2. decide which ideas actually change the plan
3. turn only the surviving ideas into claims in [`claim-ledger.md`](claim-ledger.md)
4. record the real tensions in [`contradiction-register.md`](contradiction-register.md)
5. then rewrite planning docs or implementation surfaces

## Idea Classes

- `rewrite candidate`: strong enough to change how Phase 2 is framed or ordered
- `enabling idea`: sharpens implementation shape without rewriting the whole phase
- `pressure idea`: mostly useful as a constraint or caveat
- `parked`: interesting, but not yet worth letting it rewrite the phase

## Idea Bank

| Idea | Class | Why It Matters | Strongest Sources | Consequence For Phase 2 |
| :--- | :--- | :--- | :--- | :--- |
| The real system is the harness and contract layer around a thin model loop. | rewrite candidate | It suggests Phase 2 should be framed less as a generic “agent platform” and more as a governed harness/runtime layer that reads repo truth, applies contracts, and stops at review gates. | `2604.14228`, `2603.25723`, `2603.05344`, `2604.18071`, local harness surfaces | Rewrite the public description of Phase 2 around contracts, adapters, gates, context admission, and traceable runtime behavior. |
| Human explanation, machine contract, and runtime adapter should be separate surfaces. | rewrite candidate | This sharpens the README vs `workflow.yaml` split and pressures the plan toward explicit runtime adapters rather than one blended workflow surface. | `2604.13346`, `2512.19769`, `2510.04173`, `2603.25723` | Strengthen the architecture from “README plus YAML” to a three-part model: explanation, contract, adapter/executor. |
| Workflow contracts should carry explicit preconditions, invariants, budgets, and recovery semantics. | rewrite candidate | This upgrades Phase 2 from “declared steps” into bounded behavioral contracts that can drift, recover, and fail in known ways. | `2602.22302`, `2601.08815`, `2508.02721`, `2503.18666` | Rewrite `workflow.yaml` and enforcement thinking around behavioral envelopes rather than only step schemas. |
| Context should be admitted like a governed dependency, not merely loaded as prompt material. | rewrite candidate | This reframes `required_context` as a policy and admission problem rather than only a documentation problem. | `2602.20478`, `2604.08224`, `2603.05344`, `2603.20380`, `2603.00822` | Rewrite `required_context` and enforcement thinking toward context admission, visibility, and violations. |
| Context needs lifecycle governance: decay, contradiction handling, privacy policy, pruning, and versioned reuse. | rewrite candidate | Admission alone is too shallow once context persists across runs, compacts, or resumes. | `2603.18330`, `2603.11768`, `2602.22402`, `2507.13334`, `2508.00031` | Rewrite context management from one-time intake into an explicit lifecycle model. |
| Validation should be a layered stack: static checks, bounded enforcement, trace checks, and gate review. | rewrite candidate | The current plan already says validation is lifecycle infrastructure, but this idea gives it a clearer internal architecture. | `2604.05278`, `2603.29848`, `2603.23806`, `2602.13855`, local `spec-diff` work | Rewrite 2.2 and 2.3 as a validation stack rather than as two adjacent subphases with loose boundaries. |
| Gates are durable runtime objects, not pauses in a chat loop. | rewrite candidate | This changes how approval is represented and makes the file-backed gate store feel like a primary Phase 2 object rather than a support detail. | `2604.13346`, `2603.25723`, local [`review-gate-protocol.md`](review-gate-protocol.md), Reviewable Runs model | Pull gate objects forward in the Phase 2 framing and treat resume/reject/defer semantics as core runtime behavior. |
| Execution state should be event-sourced and replayable, not merely logged. | rewrite candidate | This turns traces from passive records into re-runnable, checkable state history. | `2602.23193`, `2505.17716`, `2603.18096`, `2604.07988` | Rewrite 2.3 around append-only state, replay, and assurance rather than generic trace capture. |
| Source template, realized runtime graph, and trace record are different objects. | rewrite candidate | This gives a cleaner ontology for avoiding source/trace confusion and for relating workflow contracts to actual runs. | `2603.22386`, `2604.13346`, local architecture/traces work | Rewrite the object model in `architecture.md` to separate source contracts, realized execution structure, and derivative traces more explicitly. |
| Workflow execution may need explicit scheduler or graph objects rather than one opaque loop. | rewrite candidate | It gives the runtime a more inspectable execution object than an ever-growing conversational loop. | `2604.11378`, `2603.22386`, `2508.01186` | Push the runtime model toward schedulable graphs, dependencies, and recoverable structure. |
| Skills should be treated as capability bindings rather than reusable markdown by default. | enabling idea | This makes the current “skills need binding” conclusion more operational. | `2604.03088`, `2602.12670`, `2604.08224`, `2603.25723` | Push Phase 2 toward declared capability surfaces and away from treating skill documents as executable by default. |
| The first useful provenance layer is promoted-output state, not full semantic provenance graphs. | enabling idea | This supports a practical middle layer between naive logs and full provenance infrastructure. | `2602.13855`, local claim-state work, current Phase 2 trace docs | Keep the small vocabulary, but make it a first-class design object rather than a leftover note. |
| Real-package proof runs are more important than synthetic demos for closing the phase honestly. | enabling idea | The repo already has real package fixtures and proof-run evidence. This idea keeps the phase from drifting into elegant but unproven platform design. | manifest-first proof run, current package fixtures, [`milestones.md`](milestones.md) | Rewrite closure criteria and proof planning around retained runs on actual package paths. |
| External systems should be treated as approval-bound mutation surfaces, not just tool calls. | enabling idea | This sharpens the difference between “quality approved” and “approved to mutate Substack/NotebookLM/YouTube.” | local workflow reality, [`review-gate-protocol.md`](review-gate-protocol.md), publishing workflows | Keep external approval gates as distinct first-class objects and possibly elevate them earlier in the plan. |
| Path-dependent execution governance should be a first-class policy surface. | enabling idea | In real runs, the meaning of a tool call depends on how the system got there, not only on the final action. | `2603.16586`, `2604.05119`, `2604.18652`, `2603.14332` | Push Phase 2 toward path-aware policy and pre-action checks rather than only static allowlists. |
| Contracts should be able to degrade gracefully from deny to detect. | pressure idea | This is the practical answer to imperfect confinement. | current harness reality, enforcement planning, observability/debugging work | Clarify that some boundaries will begin as visible violations rather than hard runtime denial. |
| A lighter manifest type for non-publication operating surfaces may eventually be needed. | parked | This may matter later, but it is still too easy to let it derail the phase into taxonomy work. | [`open-questions.md`](open-questions.md), local repo structure | Keep it open, but do not let it rewrite the early Phase 2 implementation. |

## Highest-Value Rewrite Candidates

If Phase 2 is going to be rewritten before implementation, the strongest ideas to rewrite around are:

1. the harness/contract layer is the real system
2. workflows need explicit preconditions, invariants, budgets, and recovery semantics
3. human explanation, machine contract, runtime control plane, and derivative trace are separate surfaces
4. context needs both admission control and lifecycle governance
5. validation is a layered stack, not one bucket
6. workflow execution should realize explicit graphs, events, and gates rather than an opaque loop
7. source, runtime graph, gate objects, and traces are different objects
8. path-dependent governance belongs in runtime policy rather than only in prompts

## Ideas That Could Change The Current Documents Most

These ideas would most directly rewrite the current Phase 2 docs:

- [`README.md`](README.md): move from “platform” language toward “governed harness/runtime” language
- [`architecture.md`](architecture.md): sharpen the object model and separate source contracts from runtime graphs, control planes, and traces
- [`workflow-yaml-schema.md`](workflow-yaml-schema.md): add budgets, recovery hooks, capability policy, and context lifecycle semantics
- [`2.1-executable-workflow-contract.md`](2.1-executable-workflow-contract.md): move from step declaration toward bounded executable contracts
- [`2.2-enforcement-and-validation-layer.md`](2.2-enforcement-and-validation-layer.md): turn validation into an explicit layered stack with path-aware policy
- [`2.3-trace-and-provenance-minimums.md`](2.3-trace-and-provenance-minimums.md): make replayable state and promoted-output provenance more deliberate objects
- [`review-gate-protocol.md`](review-gate-protocol.md): elevate gates from supporting mechanism to core runtime object

## Current Use Rule

Do not treat an idea here as settled just because it feels better than the current wording.

Promote an idea only if it does one of these:

- simplifies the architecture while keeping the source-of-truth rules intact
- explains a Phase 2 boundary more honestly
- changes what must be proven before implementation
- improves the sequencing of 2.1 to 2.4

## Corpus Coverage

This pass now includes a paper-by-paper Phase 2 idea extraction from both current research corpora:

- the curated harness corpus in [`../../publications/literate-workflow-programming/harness_papers/index.md`](../../publications/literate-workflow-programming/harness_papers/index.md)
- the current `literate-workflow-programming` paper corpus in [`../../publications/literate-workflow-programming/papers/index.md`](../../publications/literate-workflow-programming/papers/index.md)

A second exhaustive alphaXiv expansion below goes beyond both corpora. It uses `feed list`, `search papers`, `paper similar`, `paper resources`, full-text and overview checks, plus one assistant pass that was validated back against deterministic `paper show` calls before inclusion.

Reading rule:

- `Source Set = both` means the paper currently appears in both corpora.
- Inclusion here does not mean adoption.
- Each row captures the strongest current Phase 2 idea to extract from that paper, not a full paper summary.

## Paper-By-Paper Extraction

### Rewrite-Candidate Papers

These are the papers most likely to justify rewriting the current Phase 2 framing or architecture before implementation.

| Paper | Source Set | Extracted Phase 2 Idea | Class | Why It Matters For Phase 2 | Rewrite Surface |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `2603.25723` Natural-Language Agent Harnesses | both | Natural-language contracts can be real runtime control surfaces when paired with adapters, state conventions, and validation gates. | rewrite candidate | Pushes Phase 2 toward governed harness execution rather than a generic agent platform story. | `README.md`, `architecture.md`, `workflow-yaml-schema.md`, `review-gate-protocol.md` |
| `2604.13346` AgentSPEX | both | Workflow specs need explicit state, control flow, verification, checkpointing, logging, replay, and reusable submodules. | rewrite candidate | Gives Phase 2 a more rigorous contract/runtime split and a clearer object model. | `architecture.md`, `workflow-yaml-schema.md`, `2.1-executable-workflow-contract.md` |
| `2603.16021` Interpretable Context Methodology | paper-index | Folder structure, stage contracts, intermediate artifacts, and human review gates can be treated as architecture, not just organization. | rewrite candidate | Supports a repo-native harness model instead of a black-box runtime model. | `README.md`, `architecture.md`, `review-gate-protocol.md` |
| `2603.05344` Building Effective AI Coding Agents for the Terminal | both | Compaction, tool discovery, safety, and context shaping are harness responsibilities around the loop. | rewrite candidate | Strengthens the idea that the runtime layer should own bounded context/tool mediation explicitly. | `README.md`, `architecture.md`, `2.2-enforcement-and-validation-layer.md` |
| `2604.14228` Dive into Claude Code | harness | The interesting system lives in permissions, hooks, context management, summaries, and tool mediation around a simple loop. | rewrite candidate | Strongest applied pressure to frame Phase 2 as a governed harness/runtime rather than a model-centric platform. | `README.md`, `architecture.md`, `milestones.md` |
| `2604.05278` Spec Kit Agents | both | Phase-structured context grounding and validation hooks are first-class workflow primitives. | rewrite candidate | Makes validation and grounding feel structural rather than secondary. | `2.2-enforcement-and-validation-layer.md`, `workflow-yaml-schema.md`, `milestones.md` |
| `2602.20478` Codified Context | both | Persistent project conventions and hot/cold context layers should be governed as first-class repo context. | rewrite candidate | Pushes `required_context` toward admission policy and context-state management. | `architecture.md`, `workflow-yaml-schema.md`, `open-questions.md` |
| `2604.08224` Externalization in LLM Agents | both | Memory, skills, protocols, and harnesses belong in one externalized systems stack around the model. | rewrite candidate | Helps Phase 2 unify contracts, skills, context, and traces instead of treating them as separate add-ons. | `README.md`, `architecture.md` |
| `2603.22386` From Static Templates to Dynamic Runtime Graphs | harness | Source templates, realized runtime graphs, and execution traces are different objects. | rewrite candidate | Cleans up the Phase 2 ontology and reduces source/trace confusion. | `architecture.md`, `2.3-trace-and-provenance-minimums.md` |
| `2408.04820` Natural Language Outlines for Code | harness | High-level natural-language source surfaces can stay synchronized with lower-level implementation artifacts. | rewrite candidate | Strengthens the case for keeping an inspectable human-readable source layer above execution details. | `README.md`, `workflow-yaml-schema.md`, `architecture.md` |
| `2510.09073` Literate Tracing | harness | Traces can become explanatory, inspectable artifacts rather than opaque logs. | rewrite candidate | Sharpens the trace layer into something deliberately readable and reviewable. | `2.3-trace-and-provenance-minimums.md`, `dashboard-v0.md` |
| `2405.06907` AIOS Compiler | harness | Natural language flow can be treated as an interpreted programming surface, but only with an explicit interpreter/runtime. | rewrite candidate | Pressures Phase 2 to think in terms of interpreters/adapters instead of static docs alone. | `README.md`, `architecture.md`, `2.1-executable-workflow-contract.md` |

#### Claim And Contradiction Hooks

| Paper | Claim Candidate | Main Contradiction |
| :--- | :--- | :--- |
| `2603.25723` Natural-Language Agent Harnesses | Natural-language harness files can be authoritative runtime inputs when adapters, state conventions, and gates are explicit. | Human-readable flexibility helps governance, but natural language alone becomes advisory prose without runtime binding. |
| `2604.13346` AgentSPEX | Phase 2 workflows should be represented as explicit stateful executable contracts rather than mostly implicit stage conventions. | Richer contract power improves control, but it risks doc/runtime divergence and unnecessary language complexity. |
| `2603.16021` Interpretable Context Methodology | Filesystem layout, stage folders, and review artifacts can be part of execution architecture. | Repo structure can guide execution, but by itself it does not enforce behavior. |
| `2603.05344` Building Effective AI Coding Agents for the Terminal | Context shaping, tool discovery, and safety scaffolding belong to the runtime layer around the model loop. | A thin runtime is desirable, but too-thin wrappers often hide or ignore essential harness responsibilities. |
| `2604.14228` Dive into Claude Code | Phase 2 should treat permissions, hooks, context management, and summaries as the real system around a simple loop. | Useful harness depth improves control, but the runtime can become a fat orchestration layer if it absorbs too much policy. |
| `2604.05278` Spec Kit Agents | Each workflow phase should declare its own grounding and validation hooks. | Phase discipline improves control, but rigid phases can ossify work that needs bounded flexibility. |
| `2602.20478` Codified Context | Context should be stored and admitted as governed persistent project state, not only assembled ad hoc per run. | Persistent context increases coherence, but it also creates context bloat and stale-authority risk. |
| `2604.08224` Externalization in LLM Agents | Memory, skills, protocols, and harnesses should be treated as one externalized infrastructure layer around the model. | An integrated externalized stack is coherent, but it also multiplies the number of surfaces that need governance. |
| `2603.22386` From Static Templates to Dynamic Runtime Graphs | Source contracts, realized runtime graphs, and traces should be distinct platform objects. | Clearer ontology helps debugging, but it also increases the number of objects the runtime must keep coherent. |
| `2408.04820` Natural Language Outlines for Code | Phase 2 should preserve a high-level human-readable source surface that can stay synchronized with lower-level execution artifacts. | High-level source coherence is valuable, but synchronization introduces drift and maintenance overhead. |
| `2510.09073` Literate Tracing | Traces should become readable explanatory artifacts rather than only opaque logs. | Readable traces are more useful, but they can be mistaken for authority or become expensive overhead. |
| `2405.06907` AIOS Compiler | Natural-language flow may be executable through interpreters and adapters, not only through rigid DSLs. | Natural-language programming is flexible, but it is also ambiguous and harder to constrain statically. |

### Enabling Papers

These papers sharpen implementation shape, sequencing, or object boundaries without necessarily rewriting the whole phase by themselves.

| Paper | Source Set | Extracted Phase 2 Idea | Class | Why It Matters For Phase 2 | Rewrite Surface |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `2603.17399` Bootstrapping Coding Agents: The Specification Is the Program | paper-index | The stable artifact of record can be the specification rather than the generated implementation or run log. | enabling idea | Reinforces spec-first authority and keeps traces secondary. | `architecture.md`, `2.3-trace-and-provenance-minimums.md` |
| `2603.08806` Test-Driven AI Agent Definition | paper-index | Behavioral specs can compile into tests, hidden checks, and regression surfaces. | enabling idea | Gives Phase 2 a clearer validation hook vocabulary. | `2.2-enforcement-and-validation-layer.md`, `workflow-yaml-schema.md` |
| `2603.00822` ContextCov | paper-index | Instruction files should be mined into executable constraints, prohibited moves, and runtime checks. | enabling idea | Tightens the path from human-readable contract to enforceable runtime behavior. | `2.2-enforcement-and-validation-layer.md`, `workflow-yaml-schema.md` |
| `2510.04173` Open Agent Specification | paper-index | Agent/workflow definitions can be represented once and adapted across runtimes. | enabling idea | Supports contract portability without forcing one runtime implementation style. | `2.1-executable-workflow-contract.md`, `workflow-yaml-schema.md` |
| `2512.19769` Declarative Workflow DSL | paper-index | Workflow specification, implementation, and deployment should be separable layers. | enabling idea | Reinforces the separation of human explanation, machine contract, and runtime execution. | `architecture.md`, `2.1-executable-workflow-contract.md` |
| `2512.18940` FASTRIC | paper-index | Prompt and protocol behavior can be represented as finite interaction structure and checked procedurally. | enabling idea | Adds a formal conformance-checking model for parts of the validation stack. | `2.2-enforcement-and-validation-layer.md`, `2.3-trace-and-provenance-minimums.md` |
| `2603.20380` ALARA | paper-index | Context and tool access should be least-privilege and structurally scoped. | enabling idea | Gives Phase 2 a stronger context-admission and tool-scope rule. | `workflow-yaml-schema.md`, `2.2-enforcement-and-validation-layer.md` |
| `2504.11703` Progent | paper-index | Tool privileges can be expressed as deterministic policy with runtime blocking and fallback behavior. | enabling idea | Sharpens the policy boundary between declared permissions and runtime action. | `2.2-enforcement-and-validation-layer.md`, `workflow-yaml-schema.md` |
| `2601.04748` Single-Agent With Skills | paper-index | Skill libraries can replace some orchestration until selection and semantic overload break down. | enabling idea | Helps Phase 2 place skills as bounded capabilities rather than automatic modularity. | `architecture.md`, `open-questions.md` |
| `2603.23806` AgentPex / Willful Disobedience | paper-index | Traces can be checked for rule compliance against prompt/spec-derived rules, not only scored by outcomes. | enabling idea | Strengthens the trace-validation layer. | `2.2-enforcement-and-validation-layer.md`, `2.3-trace-and-provenance-minimums.md` |
| `2603.29848` AgentFixer | paper-index | Validation is a loop spanning prompt analysis, cross-stage checks, failure localization, and iterative refinement. | enabling idea | Gives Phase 2 a more layered validation architecture. | `2.2-enforcement-and-validation-layer.md`, `milestones.md` |
| `2602.13855` Claim-Level Auditability | paper-index | The first serious provenance upgrade is claim/evidence state with contradiction transparency, not generic logs. | enabling idea | Directly informs the promoted-output state model. | `2.3-trace-and-provenance-minimums.md`, `open-questions.md` |
| `2602.12670` SkillsBench | both | Skill usefulness should be measured empirically across tasks instead of assumed from architecture alone. | enabling idea | Supports capability benchmarking and discourages doctrine-only skill design. | `architecture.md`, `milestones.md` |
| `2604.03088` SkVM | both | Skills need capability binding/runtime adaptation across models and harnesses. | enabling idea | Turns “skills need binding” into a Phase 2 capability-contract problem. | `architecture.md`, `workflow-yaml-schema.md` |
| `2601.21557` Meta Context Engineering | harness | Context and skill layers can be improved iteratively from execution history. | enabling idea | Suggests later refinement loops without making them Phase 2 prerequisites. | `open-questions.md`, `milestones.md` |
| `2405.15793` SWE-agent | harness | The agent-computer interface is part of the system boundary, not just a tool detail. | enabling idea | Useful pressure on executor design and repo/tool mediation. | `architecture.md`, `2.2-enforcement-and-validation-layer.md` |
| `2602.03786` AOrchestra | harness | Sub-agent creation and orchestration should be explicit runtime objects if they are allowed at all. | enabling idea | Helps keep orchestration explicit rather than implicit prompt behavior. | `architecture.md`, `open-questions.md` |
| `2604.18071` Architectural Design Decisions in AI Agent Harnesses | harness | Harness architecture choices have real empirical consequences and should be treated as design variables. | enabling idea | Validates taking harness design seriously at the strategy layer. | `README.md`, `architecture.md` |
| `2512.05470` Everything is Context | paper-index | Persistent context should be treated as governed filesystem abstraction, not just transient prompt stuffing. | enabling idea | Strengthens context admission and storage thinking. | `architecture.md`, `workflow-yaml-schema.md` |
| `2505.20127` Agentic AI Process Observability | paper-index | Process observability should explain why trajectories diverge, not only whether they succeeded. | enabling idea | Strengthens trace interpretation and debugging requirements. | `2.3-trace-and-provenance-minimums.md`, `dashboard-v0.md` |
| `2508.02736` AgentSight | paper-index | High-level intent should be connectable to low-level system effects. | enabling idea | Useful for designing traces and cockpit views that are not just command logs. | `2.3-trace-and-provenance-minimums.md`, `dashboard-v0.md` |
| `2604.13108` Formal Architecture Descriptors | paper-index | Explicit architecture descriptors can act as navigation primitives for agents. | enabling idea | Supports architecture/context descriptors as governed inputs rather than commentary. | `workflow-yaml-schema.md`, `architecture.md` |
| `2411.13768` Evaluation-Driven Development and Operations of LLM Agents | paper-index | Evaluation belongs across the lifecycle, not at the end of it. | enabling idea | Strong support for Phase 2’s validation-first sequencing. | `README.md`, `2.2-enforcement-and-validation-layer.md`, `milestones.md` |
| `2502.17441` Renaissance of Literate Programming in the Era of LLMs | harness | Large projects may need a persistent high-level explanatory source layer for coherence. | enabling idea | Reinforces the value of keeping a human-readable specification surface visible. | `README.md`, `workflow-yaml-schema.md` |
| `2604.01687` CoEvoSkills | paper-index | Verified self-evolving skills can outperform static curated skills, but verification is the important part. | enabling idea | Pressures Phase 2 to think in terms of verifiable capability evolution rather than static skill docs. | `architecture.md`, `open-questions.md` |

#### Claim And Contradiction Hooks

| Paper | Claim Candidate | Main Contradiction |
| :--- | :--- | :--- |
| `2603.17399` Bootstrapping Coding Agents | The specification should be treated as the stable artifact of record rather than the generated implementation or run log. | Spec primacy is clean in theory, but specs also drift when teams only maintain generated artifacts. |
| `2603.08806` Test-Driven AI Agent Definition | Behavioral specs should compile into tests and regression hooks wherever possible. | Strong test scaffolds help, but they can still create false confidence when the spec itself is thin or incomplete. |
| `2603.00822` ContextCov | Human-readable instruction files can be converted into executable constraints and prohibited moves. | Constraint extraction is powerful, but it can overfit visible text and miss latent intent or context. |
| `2510.04173` Open Agent Specification | Phase 2 should favor portable workflow representations over runtime-specific definitions when possible. | Portable schemas improve reuse, but they can flatten or hide local runtime nuance. |
| `2512.19769` Declarative Workflow DSL | Workflow specification, implementation, and deployment should remain separable layers. | Clean layering helps governance, but every extra abstraction adds maintenance and translation overhead. |
| `2512.18940` FASTRIC | Some prompt/protocol behavior can be formally checked against explicit interaction structure. | Formality helps checking, but too much formality can reduce conformance or usefulness for real models. |
| `2603.20380` ALARA | Context and tool scope should be least-privilege by default. | Tight scoping improves safety, but it can also starve the runtime of needed context or tools. |
| `2504.11703` Progent | Tool privileges should be deterministic and enforceable at runtime. | Hard policy control improves safety, but it reduces flexibility when tasks legitimately need exceptions or recovery paths. |
| `2601.04748` Single-Agent With Skills | Some orchestration should collapse into skill libraries rather than defaulting to multi-agent design. | Simpler single-agent skill systems help until the skill namespace becomes overloaded or semantically confusable. |
| `2603.23806` AgentPex / Willful Disobedience | Traces should be checked against prompt/spec-derived rules, not only scored by outcomes. | Procedural compliance is useful, but compliant traces are not sufficient proof of correct authority or provenance. |
| `2603.29848` AgentFixer | Validation should localize failures and feed redesign rather than only detect them. | Continuous validation loops are valuable, but they can also become endless repair machinery without stable stop rules. |
| `2602.13855` Claim-Level Auditability | Promoted outputs need claim/evidence state with contradiction transparency. | Rich provenance is desirable, but Phase 2 still needs a smaller practical layer before full provenance graphs. |
| `2602.12670` SkillsBench | Skill value should be measured empirically across tasks rather than assumed from architecture. | Benchmark gains matter, but they do not resolve production portability or capability-binding problems. |
| `2604.03088` SkVM | Skills need explicit capability binding across harness/model pairs. | External skill abstractions are useful, but they break down without harness-specific adaptation. |
| `2601.21557` Meta Context Engineering | Context and skill layers can evolve from execution history and feedback. | Adaptive evolution is attractive, but it can exceed Phase 2’s need for explicit, inspectable, stable surfaces. |
| `2405.15793` SWE-agent | The agent-computer interface is part of the system boundary, not a hidden tool detail. | Interface-specific pragmatism improves realism, but it can make the platform too tied to one executor style. |
| `2602.03786` AOrchestra | Sub-agents should be explicit runtime objects if they are allowed at all. | Orchestration flexibility is useful, but it quickly becomes complexity creep when contracts are weak. |
| `2604.18071` Architectural Design Decisions in AI Agent Harnesses | Harness architecture choices have measurable consequences and deserve first-class design attention. | Many harness options exist, but Phase 2 still needs a narrow opinionated baseline rather than an endless design space. |
| `2512.05470` Everything is Context | Persistent context should be treated as governed filesystem infrastructure, not transient prompt stuffing. | Context infrastructure increases coherence, but broad context surfaces can swamp specificity and control. |
| `2505.20127` Agentic AI Process Observability | Process observability should explain why trajectories diverge, not just whether they succeeded. | Rich observability helps diagnosis, but it can easily become trace overload or analytics creep. |
| `2508.02736` AgentSight | High-level intent should be connectable to low-level system effects. | Stronger linkage is useful, but it can overburden the trace model if every effect must be fully aligned. |
| `2604.13108` Formal Architecture Descriptors | Architecture descriptors can be first-class navigation inputs for the runtime. | Helpful descriptors improve navigation, but they also create authoring burden and descriptor drift risk. |
| `2411.13768` Evaluation-Driven Development and Operations of LLM Agents | Evaluation should operate across the lifecycle rather than after it. | Lifecycle evaluation improves governance, but it can also bloat the platform if every stage becomes heavy process. |
| `2502.17441` Renaissance of Literate Programming in the Era of LLMs | Large projects benefit from a persistent explanatory source layer above implementation detail. | Explanatory layers improve coherence, but they also risk duplicating information that must stay synchronized. |
| `2604.01687` CoEvoSkills | Capability evolution can be useful if verification remains explicit. | Dynamic skill evolution is promising, but Phase 2 still needs stable declarative capability surfaces first. |

### Pressure And Parked Papers

These papers matter because they constrain Phase 2, warn against easy mistakes, or suggest later lines that should not quietly rewrite the phase too early.

| Paper | Source Set | Extracted Phase 2 Idea | Class | Why It Matters For Phase 2 | Rewrite Surface |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `2504.15228` A Self-Improving Coding Agent | harness | Self-improvement loops are a real direction, but they should be treated as later pressure rather than a safe Phase 2 baseline. | parked | Prevents premature expansion from governed execution into autonomous self-modification. | `open-questions.md`, `milestones.md` |
| `2603.28052` Meta-Harness | harness | Harness optimization is a first-class engineering problem separate from model choice. | pressure idea | Strong pressure that the harness layer matters, but it points more toward later optimization than current Phase 2 structure. | `README.md`, `milestones.md` |
| `2601.14192` Toward Efficient Agents | harness | Runtime budget tradeoffs for memory, tools, and planning should stay visible. | pressure idea | Useful as cost/performance pressure without rewriting the contract-first shape. | `dashboard-v0.md`, `open-questions.md` |
| `2511.16043` Agent0 | harness | Self-evolving agent systems belong to a later, more autonomous line than the current local governed runtime. | parked | Helps hold the Phase 2 scope line. | `open-questions.md` |
| `2604.02268` SKILL0 | harness | Skill internalization pressures against assuming external skill files are the final abstraction. | pressure idea | Useful constraint on the skills layer, but not a reason to abandon external capability contracts yet. | `architecture.md`, `open-questions.md` |
| `2603.03329` AutoHarness | harness | Harness code itself can be synthesized and improved automatically. | pressure idea | Important later pressure, but too early to let it replace explicit contract design now. | `open-questions.md`, `milestones.md` |
| `2602.11988` Evaluating AGENTS.md | paper-index | Repository-level context files can reduce success and increase cost when they add the wrong kind of context. | pressure idea | Forces caution on context admission and against naive “more context files help” claims. | `2.2-enforcement-and-validation-layer.md`, `open-questions.md` |
| `2601.20404` On the Impact of AGENTS.md Files | paper-index | Repository-level context files can improve efficiency in some workflows. | pressure idea | Creates the metric split: context-file utility depends on task and metric. | `2.2-enforcement-and-validation-layer.md`, `open-questions.md` |
| `2511.12884` Agent READMEs | paper-index | Agent context files behave like evolving configuration rather than static prose. | pressure idea | Supports treating context files as governed artifacts, but warns that readability and governance matter. | `workflow-yaml-schema.md`, `open-questions.md` |
| `2603.08993` Arbiter | paper-index | Contradictions, redundancies, and ambiguities inside control surfaces are detectable and worth checking statically. | pressure idea | Pushes Phase 2 toward contradiction checks without overclaiming runtime harm. | `2.2-enforcement-and-validation-layer.md`, `2.3-trace-and-provenance-minimums.md` |
| `2508.11126` AI Agentic Programming | paper-index | The field is broad enough that Phase 2 must stay narrow and avoid becoming a survey-shaped architecture. | parked | Useful scope pressure, not a direct design donor. | `README.md` |

#### Claim And Contradiction Hooks

| Paper | Claim Candidate | Main Contradiction |
| :--- | :--- | :--- |
| `2504.15228` A Self-Improving Coding Agent | Self-improvement loops are real, but they should be treated as later pressure rather than a Phase 2 default. | Strong autonomy gains are tempting, but they cut against the current need for bounded, inspectable governance. |
| `2603.28052` Meta-Harness | Harness optimization should eventually be measured directly rather than inferred from model quality. | Harness optimization matters, but Phase 2 still needs stable contracts before it needs systematic harness tuning. |
| `2601.14192` Toward Efficient Agents | Runtime budget tradeoffs for memory, tools, and planning should stay visible. | Efficiency matters, but early optimization can distract from correctness and governance. |
| `2511.16043` Agent0 | Self-evolving agent systems are a later line than the current local governed runtime. | The autonomy frontier is real, but it exceeds current Phase 2 scope. |
| `2604.02268` SKILL0 | External skill files may be transitional rather than the final skill abstraction. | External skill surfaces are useful now, but later internalization or adaptation may change the abstraction boundary. |
| `2603.03329` AutoHarness | Harnesses themselves may eventually be synthesized and improved automatically. | Automated harness generation is promising, but it conflicts with the current need for explicit inspectable contracts. |
| `2602.11988` Evaluating AGENTS.md | More repository-level context documentation can hurt success and cost. | Context guidance can help some tasks, but it can also overload or distract the agent. |
| `2601.20404` On the Impact of AGENTS.md Files | Repository-level context files can improve efficiency in some workflows. | Efficiency gains do not prove correctness gains or good governance. |
| `2511.12884` Agent READMEs | Context files are closer to living configuration than static README prose. | Living configuration is useful, but it drifts without governance and clear authority rules. |
| `2603.08993` Arbiter | Static contradiction checks over prompts/control surfaces are worthwhile. | Detecting contradictions statically is useful, but static interference does not automatically prove runtime harm. |
| `2508.11126` AI Agentic Programming | Phase 2 should stay narrow and implementation-facing rather than absorbing the whole field vocabulary. | Broad surveys help orientation, but they can dissolve concrete design decisions into generic terminology. |

## Exhaustive alphaXiv Expansion Beyond Current Corpora

This pass is for ideas that were not already captured by the two active corpora but materially affect Phase 2.

Reading rule:

- `Social` is `upvotes / last-30-day visits`
- `Full Text` means alphaXiv returned a normal paper record and text-access path
- `Implementation` is the first surfaced resource repo when one exists
- `Status` is a rough `hot / new / survey / pressure` tag, not an adoption decision

### Rewrite-Candidate Additions

| Paper | Status | Social | Full Text | Implementation | Extracted Phase 2 Idea | Why It Matters For Phase 2 | Rewrite Surface |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `2602.22302` Agent Behavioral Contracts | new | `4 / 19` | yes | - | Executable workflows should declare preconditions, invariants, governance rules, and recovery semantics as runtime-enforceable objects. | Sharpens Phase 2 contracts from step schemas into bounded behavior envelopes with explicit drift and recovery logic. | `2.1-executable-workflow-contract.md`, `workflow-yaml-schema.md`, `2.2-enforcement-and-validation-layer.md` |
| `2601.08815` Agent Contracts | new | `2 / 11` | yes | - | Workflow contracts should carry resource budgets, temporal bounds, and delegation conservation rules. | Adds budget governance and hierarchical delegation semantics to workflow contracts. | `workflow-yaml-schema.md`, `architecture.md`, `2.1-executable-workflow-contract.md` |
| `2508.02721` Blueprint First, Model Second | new | `3 / 1` | yes | - | Deterministic blueprints should guide model execution rather than emerge from it. | Direct support for contract-first execution and cleaner separation between planning surface and model actuation. | `README.md`, `architecture.md`, `2.1-executable-workflow-contract.md` |
| `2601.17744` Faramesh | new | `5 / 6` | yes | - | A thin protocol-agnostic execution control plane can mediate side effects and workflow authority. | Helps define the runtime boundary more concretely than a generic agent shell. | `README.md`, `architecture.md`, `review-gate-protocol.md` |
| `2604.18652` From Craft to Kernel | new | `2 / 12` | yes | `ArbiterOS (112 stars)` | A governance-first kernel with semantic instructions may need to sit between model output and high-risk execution sinks. | Strong pressure on runtime policy, capability binding, and pre-action verification. | `architecture.md`, `2.2-enforcement-and-validation-layer.md`, `review-gate-protocol.md` |
| `2604.11378` From Agent Loops to Structured Graphs | new | `0 / 17` | yes | - | The agent loop should be reframed as an explicit schedulable graph with clearer dependencies and recovery structure. | Strengthens the runtime-graph idea and the shift away from opaque loop execution. | `architecture.md`, `2.1-executable-workflow-contract.md`, `2.3-trace-and-provenance-minimums.md` |
| `2507.13334` Survey of Context Engineering | survey, hot | `352 / 166` | yes | `Awesome-Context-Engineering (2332 stars)` | Context engineering is a formal system-design discipline spanning retrieval, processing, management, and system integration. | Reinforces that Phase 2 context design is architecture, not prompt advice. | `README.md`, `architecture.md`, `workflow-yaml-schema.md` |
| `2503.18666` AgentSpec | hot | `97 / 75` | yes | `AgentSpec (6 stars)` | Runtime constraint DSLs can be lightweight, interpretable, and adaptable across domains. | Pushes enforcement toward explicit rule surfaces rather than diffuse prompt constraints. | `2.2-enforcement-and-validation-layer.md`, `workflow-yaml-schema.md` |

#### Claim And Contradiction Hooks

| Paper | Claim Candidate | Main Contradiction |
| :--- | :--- | :--- |
| `2602.22302` Agent Behavioral Contracts | Workflows should expose preconditions, invariants, governance rules, and recovery semantics as executable contract surfaces. | Probabilistic recovery helps bounded drift, but some irreversible side effects still require hard gates rather than soft recovery. |
| `2601.08815` Agent Contracts | Workflow contracts should declare budgets, temporal limits, and delegation conservation rules. | Stronger budget semantics improve governance, but they can overconstrain exploratory work or create brittle delegation trees. |
| `2508.02721` Blueprint First, Model Second | Deterministic blueprints should precede model execution in structured workflows. | Blueprint-first control improves predictability, but it can underserve tasks that legitimately need bounded exploration. |
| `2601.17744` Faramesh | Phase 2 should treat the runtime as an execution control plane for side effects rather than a monolithic agent loop. | Protocol-agnostic control improves portability, but it can flatten local capability nuance or force lowest-common-denominator policy. |
| `2604.18652` From Craft to Kernel | High-risk execution may need a semantic instruction layer between model intent and tool dispatch. | A governance-first kernel improves control, but it risks turning Phase 2 into a fat runtime if imported too literally. |
| `2604.11378` Structured Graphs | Workflow execution should be modeled as explicit graphs rather than one mutable loop. | Graph structure improves debugging and recovery, but it can become too rigid for open-ended editorial work. |
| `2507.13334` Survey of Context Engineering | Context should be treated as a formal systems discipline spanning retrieval, processing, management, and integration. | The survey clarifies the field, but it is broad enough to sprawl Phase 2 beyond its local governed-runtime target. |
| `2503.18666` AgentSpec | Runtime rules can live in a lightweight constraint DSL rather than only in prompts or code. | DSL-based enforcement improves clarity, but every new rule surface creates translation and maintenance burden. |

### Enabling Additions

| Paper | Status | Social | Full Text | Implementation | Extracted Phase 2 Idea | Why It Matters For Phase 2 | Rewrite Surface |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `2602.23193` ESAA | new | `1 / 12` | yes | - | Run state can be append-only and event-sourced instead of inferred from ad hoc traces. | Gives 2.3 a more concrete state model than generic logs. | `2.3-trace-and-provenance-minimums.md`, `dashboard-v0.md` |
| `2505.17716` AgentRR | hot | `76 / 19` | yes | - | Recorded experiences and check functions can guide replayed workflows safely. | Supports proof artifacts, exemplar runs, and reuse of validated trajectories. | `2.3-trace-and-provenance-minimums.md`, `review-gate-protocol.md`, `milestones.md` |
| `2603.18096` Trace-Based Assurance | new | `2 / 1` | yes | - | Traces can carry contracts, testing, deterministic replay, and fault-injection surfaces. | Adds assurance vocabulary for trace evaluation and governance. | `2.2-enforcement-and-validation-layer.md`, `2.3-trace-and-provenance-minimums.md` |
| `2604.05119` Governance-Aware Agent Telemetry | new | `1 / 6` | yes | - | Telemetry can close the loop by feeding policy enforcement rather than remaining observability-only. | Bridges observability with bounded runtime enforcement. | `2.2-enforcement-and-validation-layer.md`, `dashboard-v0.md` |
| `2603.16586` Runtime Governance for AI Agents | new | `4 / 33` | yes | - | Governance should operate on execution paths and not only on final outputs or individual tool calls. | Sharpens path-dependent policy and runtime checkpoints. | `2.2-enforcement-and-validation-layer.md`, `review-gate-protocol.md` |
| `2603.18330` MemArchitect | new | `5 / 31` | yes | - | Memory needs explicit decay, conflict-resolution, and privacy policies. | Turns context governance into lifecycle management, not just admission. | `workflow-yaml-schema.md`, `architecture.md`, `open-questions.md` |
| `2603.11768` Governing Evolving Memory | new | `11 / 57` | yes | - | Long-term memory should be governed against semantic drift and safety regressions. | Useful pressure on any persistent context store or learned memory layer. | `architecture.md`, `open-questions.md` |
| `2602.22402` Contextual Memory Virtualisation | new | `2 / 10` | yes | - | Context and state can be versioned as snapshot, branch, and trim objects with structurally lossless compaction. | Suggests a repo-like model for context compaction and resumption. | `architecture.md`, `2.3-trace-and-provenance-minimums.md`, `dashboard-v0.md` |
| `2508.00031` Git Context Controller | new | `16 / 72` | yes | `GCC (11 stars)` | Context admission can be managed like explicit diffs, branches, and reverts instead of hidden prompt stuffing. | Strongly aligns with repo-native operator controls. | `workflow-yaml-schema.md`, `2.2-enforcement-and-validation-layer.md`, `dashboard-v0.md` |
| `2601.16746` SWE-Pruner | hot | `66 / 205` | yes | `swe-pruner (110 stars)` | Context pruning should be adaptive and task-conditioned rather than static compaction. | Gives a practical compaction and context-budget donor. | `2.2-enforcement-and-validation-layer.md`, `open-questions.md` |
| `2512.16970` PAACE | new | `7 / 4` | yes | - | Plans and context selection should co-evolve instead of being independent preprocessing steps. | Suggests plan-aware context assembly for workflows. | `2.1-executable-workflow-contract.md`, `workflow-yaml-schema.md` |
| `2603.14332` Governing Dynamic Capabilities | new | `1 / 8` | yes | - | Dynamic tool or capability acquisition needs cryptographic binding and reproducibility verification. | Helps define capability governance beyond static tool declarations. | `2.2-enforcement-and-validation-layer.md`, `workflow-yaml-schema.md` |
| `2603.13404` Schema First Tool APIs | new | `1 / 3` | yes | - | Tool interfaces should be schema-first and diagnostic-rich. | Supports tool-call schema enforcement and better recovery. | `2.2-enforcement-and-validation-layer.md`, `workflow-yaml-schema.md` |
| `2604.02375` KAIJU | new | `2 / 10` | yes | `kaiju (0 stars)` | Intent-gated execution kernels can separate semantic intent validation from raw tool dispatch. | Another concrete donor for a thin executive kernel. | `architecture.md`, `review-gate-protocol.md` |

#### Claim And Contradiction Hooks

| Paper | Claim Candidate | Main Contradiction |
| :--- | :--- | :--- |
| `2602.23193` ESAA | Run state should be append-only and replayable rather than reconstructed from loose logs. | Event sourcing clarifies provenance, but it may be too heavy if Phase 2 tries to record everything by default. |
| `2505.17716` AgentRR | Validated experiences and check functions should be reusable proof artifacts for later runs. | Replay improves reliability, but it can fossilize stale workflows or hide novel failure modes. |
| `2603.18096` Trace-Based Assurance | Traces should support contract checking, replay, and fault injection rather than only observability. | Assurance-rich traces are powerful, but they can exceed the minimum viable trace surface if adopted wholesale. |
| `2604.05119` Governance-Aware Telemetry | Telemetry should feed closed-loop enforcement rather than dashboards alone. | Closed-loop telemetry improves control, but it can blur the line between observing and governing. |
| `2603.16586` Policies on Paths | Runtime policy should reason over execution paths, not only isolated actions. | Path-aware governance is more faithful to real risk, but it is harder to explain and enforce incrementally. |
| `2603.18330` MemArchitect | Persistent memory should obey decay, conflict, and privacy policy. | Governance improves memory quality, but it can discard nuance or create a heavy policy burden. |
| `2603.11768` Governing Evolving Memory | Long-term memory needs drift governance and safety checks. | Strong memory governance improves stability, but it may also suppress useful adaptation. |
| `2602.22402` Contextual Memory Virtualisation | Context should be versioned with snapshot, branch, and trim semantics. | Versioned context helps replay and resumption, but it introduces storage and authoring complexity. |
| `2508.00031` Git Context Controller | Context admission should be explicit, inspectable, and reversible. | Git-like control improves governance, but it may add operator friction and slower iteration. |
| `2601.16746` SWE-Pruner | Context pruning should be adaptive and task-conditioned. | Adaptive pruning saves budget, but it can silently drop authority-critical context. |
| `2512.16970` PAACE | Plan generation and context assembly should be coupled. | Coupling improves relevance, but it risks circular planning and context dependence. |
| `2603.14332` Governing Dynamic Capabilities | Tool capabilities need externally verifiable binding rather than prompt-only attachment. | Verifiable capability binding strengthens governance, but it may be too heavy for the first local baseline. |
| `2603.13404` Schema First Tool APIs | Tool APIs should be schema-first and validation-driven. | Strict schemas improve reliability, but they can underfit messy real tools or slow iteration. |
| `2604.02375` KAIJU | Intent should be validated before raw tool execution. | Intent gating helps safety, but it can become another opaque classifier if it is not inspectable. |

### Pressure And Parked Additions

| Paper | Status | Social | Full Text | Implementation | Extracted Phase 2 Idea | Why It Matters For Phase 2 | Rewrite Surface |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `2508.01186` Survey on Agent Workflow | survey | `19 / 22` | yes | - | Agent workflows are now a broad field with their own orchestration vocabulary and design splits. | Useful field map, but too broad to rewrite Phase 2 on its own. | `README.md`, `open-questions.md` |
| `2511.20920` Securing MCP | pressure | `12 / 9` | yes | - | Protocol-level security and governance matter if Phase 2 leans on MCP ecosystems. | Strong pressure on connector and tool protocol boundaries. | `2.2-enforcement-and-validation-layer.md`, `open-questions.md` |
| `2604.13630` SafeHarness | pressure | `3 / 41` | yes | - | The harness itself is a high-value attack surface that deserves lifecycle security treatment. | Useful runtime-hardening constraint, not the main architecture donor. | `architecture.md`, `milestones.md` |
| `2604.07988` LogAct | pressure | `0 / 51` | yes | - | Shared logs can act as a coordination substrate and reliability primitive. | Interesting trace-runtime idea, but it may exceed a thin local file-backed baseline. | `2.3-trace-and-provenance-minimums.md`, `dashboard-v0.md` |
| `2602.10133` AgentTrace | pressure | `4 / 42` | yes | - | Logs need structured operational, cognitive, and contextual separation. | Good observability pressure, but not authority by itself. | `2.3-trace-and-provenance-minimums.md`, `dashboard-v0.md` |
| `2506.04133` TRiSM for Agentic AI | survey | `31 / 23` | yes | - | Trust, risk, and security management need lifecycle treatment across the whole agent stack. | Survey pressure that governance cannot be bolted on late. | `README.md`, `milestones.md` |
| `2603.17639` VeriGrey | pressure | `9 / 38` | yes | - | Greybox validation can probe agent failures between black-box evals and full verification. | Good testing pressure, but not a direct contract donor. | `2.2-enforcement-and-validation-layer.md`, `milestones.md` |
| `2509.14647` AgentCompass | pressure | `14 / 10` | yes | - | Production workflow evaluation needs reliability signals beyond raw task success. | Relevant for proof closure and ops, but later than foundational Phase 2. | `milestones.md`, `dashboard-v0.md` |
| `2510.25694` Process-Level Trajectory Evaluation | pressure | `5 / 9` | yes | `EnConda-Bench (44 stars)` | Process-level evaluation can reveal environment-setup failures invisible to final outcomes. | Useful proof pressure for real workflows, not core architecture. | `milestones.md`, `2.3-trace-and-provenance-minimums.md` |
| `2603.22868` Agent-Sentry | pressure | `9 / 32` | yes | - | Execution provenance can learn behavioral bounds and block out-of-bounds tool calls. | Pressure toward provenance-informed enforcement, but still heavier than the initial local baseline. | `2.2-enforcement-and-validation-layer.md`, `2.3-trace-and-provenance-minimums.md` |
| `2512.15892` VET Your Agent | parked | `5 / 3` | yes | - | Verifiable execution traces and agent identity documents matter for host-independent autonomy. | Valuable for high-trust deployments, but heavy for the first local Phase 2 baseline. | `open-questions.md`, `2.3-trace-and-provenance-minimums.md` |
| `2510.03495` AgentHub | parked | `0 / 6` | yes | - | Discoverable and verifiable agent registries matter later if workflows or agents become shareable artifacts. | Future distribution and governance line, not a current Phase 2 driver. | `open-questions.md` |

#### Claim And Contradiction Hooks

| Paper | Claim Candidate | Main Contradiction |
| :--- | :--- | :--- |
| `2508.01186` Survey on Agent Workflow | Phase 2 should stay legible against the broader workflow field. | Broad surveys help orientation, but they can dissolve specific architectural decisions into generic taxonomy. |
| `2511.20920` Securing MCP | Tool and context protocols need explicit governance boundaries. | Protocol governance matters, but Phase 2 should not overfit to one external ecosystem too early. |
| `2604.13630` SafeHarness | The harness itself should be treated as a security surface. | Harness hardening is important, but over-weighting security architecture can turn Phase 2 into an infrastructure program. |
| `2604.07988` LogAct | Shared logs can become execution primitives rather than passive records. | Shared-log execution is intriguing, but it may overshoot the desired thin runtime. |
| `2602.10133` AgentTrace | Traces should distinguish operational, cognitive, and context events. | Better structure improves debugging, but structured logging is still not authority. |
| `2506.04133` TRiSM | Governance should be lifecycle-wide rather than an afterthought. | TRiSM scope is valuable, but it is broad enough to pull Phase 2 into generic governance language. |
| `2603.17639` VeriGrey | Greybox validation is a useful middle layer between black-box eval and formal proof. | More validation helps, but too many validation modes can bloat the platform. |
| `2509.14647` AgentCompass | Reliability evaluation should consider workflow behavior in production conditions. | Production evaluation is useful, but it belongs later than contract stabilization. |
| `2510.25694` Process-Level Trajectory Evaluation | Process-level evaluation should accompany outcome evaluation in proof runs. | Process-level signals help diagnose failures, but they can create heavy proof requirements too early. |
| `2603.22868` Agent-Sentry | Provenance can be used to learn and enforce behavioral bounds. | Provenance-bounded execution is appealing, but learned bounds may be opaque or brittle. |
| `2512.15892` VET Your Agent | Verifiable execution traces may eventually matter for high-trust autonomy. | Host-independent proofs are powerful, but far beyond the first local governed-runtime baseline. |
| `2510.03495` AgentHub | Workflows or agents may later need registry-grade discovery and verification metadata. | Registry concerns are real, but Phase 2 still needs local execution discipline before sharing infrastructure. |

## Coverage Checklist

The current paper-by-paper extraction covers these papers from the two active corpora:

- Harness corpus: `2504.15228`, `2603.28052`, `2601.14192`, `2511.16043`, `2603.25723`, `2602.12670`, `2604.02268`, `2405.15793`, `2601.21557`, `2604.14228`, `2602.03786`, `2603.05344`, `2604.08224`, `2603.03329`, `2602.20478`, `2603.22386`, `2604.03088`, `2405.06907`, `2604.13346`, `2408.04820`, `2510.09073`, `2604.18071`, `2502.17441`, `2604.05278`
- `papers/index.md` corpus: `2603.25723`, `2604.13346`, `2603.17399`, `2603.08806`, `2603.00822`, `2603.16021`, `2604.03088`, `2510.04173`, `2512.19769`, `2512.18940`, `2603.20380`, `2504.11703`, `2601.04748`, `2603.23806`, `2603.29848`, `2602.13855`, `2603.05344`, `2512.05470`, `2602.20478`, `2604.08224`, `2604.05278`, `2505.20127`, `2508.02736`, `2602.11988`, `2601.20404`, `2511.12884`, `2603.08993`, `2604.13108`, `2602.12670`, `2604.01687`, `2411.13768`, `2508.11126`

## Current Rewrite Slate

If you want to rewrite Phase 2 from this extraction rather than from the earlier top-level synthesis, the strongest current rewrite slate is:

1. frame Phase 2 as a governed harness/runtime layer around a thin model loop
2. turn workflows into explicit contracts with preconditions, invariants, budgets, and recovery semantics
3. separate human explanation, machine contract, runtime control plane, and derivative trace more explicitly
4. treat context as admitted and lifecycle-governed state rather than passive prompt material
5. model execution as graphs, events, and gates rather than an opaque loop
6. recast validation as a layered stack spanning static checks, bounded enforcement, trace checks, replay, and review gates
7. elevate path-dependent capability governance, gate objects, and promoted-output state into first-class runtime objects
