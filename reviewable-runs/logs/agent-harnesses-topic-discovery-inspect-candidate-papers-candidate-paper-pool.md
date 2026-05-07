# Ranked Candidate Paper Pool: agent harnesses

## Scope And Inputs

- Workflow step: `topic_discovery.inspect_candidate_papers`
- Runtime discovery trigger: `agent harnesses`
- Declared input used: `reviewable-runs/logs/agent-harnesses-topic-discovery-inspect-candidate-papers-topic-vocabulary-map.md`
- Declared input sha256: `9fa3dfa052a8d2b60c2acf267483b78e2cfadc58d70723269e0f9627ba81dfe7`
- Observed input sha256: `9fa3dfa052a8d2b60c2acf267483b78e2cfadc58d70723269e0f9627ba81dfe7`
- Retrieval mode: deterministic public alphaXiv search and `paper abstract` inspection only.

## Public alphaXiv Inspection Commands

- `.venv/bin/alphaxiv search papers "natural language agent harness"`
- `.venv/bin/alphaxiv search papers "agentic harness engineering"`
- `.venv/bin/alphaxiv search papers "agent evaluation harness"`
- `.venv/bin/alphaxiv search papers "coding agent terminal harness"`
- `.venv/bin/alphaxiv search papers "multi-agent harness synthesis"`
- `.venv/bin/alphaxiv search papers "agent harness vulnerability discovery"`
- `.venv/bin/alphaxiv search papers "fuzz harness generation LLM agents"`
- `.venv/bin/alphaxiv search papers "tool mediation context management agent systems"`
- `.venv/bin/alphaxiv paper abstract 2603.25723`
- `.venv/bin/alphaxiv paper abstract 2604.18071`
- `.venv/bin/alphaxiv paper abstract 2604.25850`
- `.venv/bin/alphaxiv paper abstract 2603.05344`
- `.venv/bin/alphaxiv paper abstract 2604.20801`
- `.venv/bin/alphaxiv paper abstract 2603.08616`
- `.venv/bin/alphaxiv paper abstract 2603.03329`
- `.venv/bin/alphaxiv paper abstract 2602.22480`
- `.venv/bin/alphaxiv paper abstract 2510.11977`
- `.venv/bin/alphaxiv paper abstract 2603.28052`
- `.venv/bin/alphaxiv paper abstract 2604.01527`
- `.venv/bin/alphaxiv paper abstract 2601.11868`
- `.venv/bin/alphaxiv paper abstract 2602.18029`
- `.venv/bin/alphaxiv paper abstract 2507.11633`
- `.venv/bin/alphaxiv paper abstract 2604.10352`
- `.venv/bin/alphaxiv paper abstract 2603.20075`
- `.venv/bin/alphaxiv paper abstract 2604.17288`
- `.venv/bin/alphaxiv paper abstract 2604.13630`
- `.venv/bin/alphaxiv paper abstract 2512.03420`
- `.venv/bin/alphaxiv paper abstract 2604.17562`

## Ranking Criteria

- Directness to the essay object: treats the agent harness itself as the controllable, inspectable, transferable system layer.
- Coverage of the admitted vocabulary map: context management, tool mediation, safety, orchestration, evaluation, optimization, traces, and durable artifacts.
- Usefulness for a north-star flagship essay: supports a broad thesis about non-model infrastructure becoming a first-class research object.
- Boundary control: keeps control harnesses, evaluation harnesses, fuzz harnesses, and adjacent benchmarks distinct.

## Tier 1: Core Candidate Pool

1. `2603.25723` — `Natural-Language Agent Harnesses`
   - Role: thesis anchor.
   - Why it ranks here: it names harness engineering directly, argues that harness design is buried in controller code and runtime conventions, and proposes portable natural-language harness artifacts executed by a shared runtime with explicit contracts, durable artifacts, adapters, ablations, and code-to-text migration.
   - Use in essay: define the central object and the strongest version of "harness as editable scientific artifact."

2. `2604.18071` — `Architectural Design Decisions in AI Agent Harnesses`
   - Role: architecture-survey anchor.
   - Why it ranks here: it gives a source-grounded taxonomy of recurring agent-system infrastructure decisions: subagents, context management, tool systems, safety mechanisms, orchestration, execution environments, governance, MCP/plugin extensions, and audit gaps.
   - Use in essay: show that harness design is not just prompt style but an architecture surface with repeated patterns and governance consequences.

3. `2604.25850` — `Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses`
   - Role: optimization anchor.
   - Why it ranks here: it treats harnesses as editable components, uses component/experience/decision observability, binds edits to falsifiable predictions, and reports Terminal-Bench 2, SWE-bench-verified, and cross-model-family transfer gains.
   - Use in essay: establish that harnesses can be optimized as systems, not only hand-designed as wrappers.

4. `2603.05344` — `Building Effective AI Coding Agents for the Terminal`
   - Role: product/system anchor.
   - Why it ranks here: it connects harness engineering to terminal-native coding agents, safety controls, context management, model routing, planning/execution separation, lazy tool discovery, adaptive context compaction, memory, and reminders.
   - Use in essay: translate the research object into the concrete operator surface readers recognize from CLI coding agents.

5. `2604.20801` — `Synthesizing Multi-Agent Harnesses for Vulnerability Discovery`
   - Role: multi-agent/security anchor.
   - Why it ranks here: it defines the harness as the program fixing agent roles, information flow, tools, retries, communication topology, and coordination protocol, then uses runtime diagnostic feedback to rewrite the harness.
   - Use in essay: show the harness as an active search space whose structure can move outcomes even with the model held fixed.

6. `2603.08616` — `Coverage-Guided Multi-Agent Harness Generation for Java Library Fuzzing`
   - Role: fuzz/security implementation anchor.
   - Why it ranks here: it decomposes harness generation into research, synthesis, compilation repair, coverage analysis, and refinement agents, uses MCP for on-demand documentation/source queries, and closes the loop with coverage-guided refinement.
   - Use in essay: keep the fuzz-harness meaning distinct while showing the same infrastructure logic in a mature software-testing setting.

7. `2603.03329` — `AutoHarness`
   - Role: code-harness synthesis anchor.
   - Why it ranks here: it shows a smaller model synthesizing a code harness from environment feedback to prevent illegal actions across TextArena games and, in some settings, replacing decision-time LLM calls with a generated code policy.
   - Use in essay: support the claim that harnesses can encode behavioral constraints and outperform larger-model substitution.

8. `2602.22480` — `VeRO: An Evaluation Harness for Agents to Optimize Agents`
   - Role: agent-optimization evaluation anchor.
   - Why it ranks here: it provides versioned agent snapshots, budget-controlled evaluation, structured execution traces, rewards, observations, and reference procedures for edit-execute-evaluate loops.
   - Use in essay: connect harness design to the measurement substrate required for agents that improve other agents.

9. `2510.11977` — `Holistic Agent Leaderboard`
   - Role: evaluation-infrastructure anchor.
   - Why it ranks here: it provides a standardized evaluation harness across hundreds of VMs, analyzes model/scaffold/benchmark axes, uses rollout logs and LLM-aided log inspection, and frames reliability beyond benchmark scores.
   - Use in essay: make the benchmark side legible without conflating evaluation harnesses with runtime/control harnesses.

10. `2603.28052` — `Meta-Harness`
    - Role: meta-optimization anchor.
    - Why it ranks here: it searches harness code using source, scores, and execution traces from prior candidates, improving context management, retrieval-augmented reasoning, and agentic coding baselines.
    - Use in essay: connect automated harness engineering to richer prior experience and trace-access design.

## Tier 2: Strong Supporting Candidates

11. `2604.10352` — `ClawVM: Harness-Managed Virtual Memory for Stateful Tool-Using LLM Agents`
    - Why it matters: it treats the harness as the enforcement point for state residency, durability, lifecycle boundaries, token-budget representations, and auditable writeback.
    - Best use: a context-management sidebar or section on harnesses as memory systems.

12. `2603.20075` — `Agentic Harness for Real-World Compilers`
    - Why it matters: it argues that compiler repair needs specialized agent-friendly tools, reproducible compiler bugs, and a tailored minimal agent harness.
    - Best use: a domain-specific example where harness engineering closes the loop between LLMs and complex systems.

13. `2604.13630` — `SafeHarness`
    - Why it matters: it frames the execution harness as a high-value attack surface and places filtering, causal verification, privilege-separated tool control, rollback, and adaptive degradation inside the lifecycle.
    - Best use: a safety/security section on why the harness is also a governance boundary.

14. `2604.01527` — `ProdCodeBench`
    - Why it matters: it shows how production-derived benchmark construction, multi-run stability checks, and offline evaluation signals drive model selection and harness design decisions.
    - Best use: practical evaluation context for coding-agent deployment teams.

15. `2601.11868` — `Terminal-Bench`
    - Why it matters: it provides hard terminal-environment tasks, comprehensive tests, error analysis, and an evaluation harness that several harness papers use as a proving ground.
    - Best use: benchmark context, not a main harness-design source.

16. `2602.18029` — `Towards More Standardized AI Evaluation`
    - Why it matters: it argues that agent evaluation is a control function for trust, iteration, governance, and non-deterministic systems.
    - Best use: conceptual framing for why harnesses need measurement discipline.

17. `2507.11633` — `General Modular Harness for LLM Agents in Multi-Turn Gaming Environments`
    - Why it matters: it decomposes agent harnessing into perception, memory, and reasoning modules and studies module contribution patterns across interactive settings.
    - Best use: comparative modular-harness example outside coding/security.

18. `2604.17288` — `Clover`
    - Why it matters: it describes a neural-symbolic agentic harness for RTL repair with specialized LLM agents, symbolic solvers, a toolbox, and stochastic tree-of-thoughts.
    - Best use: domain-specific near-core example of orchestration and structured search.

19. `2512.03420` — `HarnessAgent`
    - Why it matters: it scales automatic fuzzing harness construction with tool-augmented pipelines, compilation repair, symbol retrieval, and fake-definition validation.
    - Best use: fuzzing-specific support if the essay needs more evidence beyond Java library fuzzing.

20. `2604.17562` — `SafeAgent`
    - Why it matters: it separates runtime execution governance from semantic risk reasoning over persistent session state.
    - Best use: security architecture adjacency; include only if the argument broadens from harness-specific safety to runtime protection.

## Near-Misses And Exclusions

- `2509.06216` — `Agentic Software Engineering`: appears in search for harness engineering, but the retrieved title suggests a broader research-agenda paper rather than a harness-specific object.
- `2604.25727` — `Toward Scalable Terminal Task Synthesis via Skill Graphs`: useful for benchmark/task generation, but less direct than Terminal-Bench or HAL for harness-centered argument.
- `2506.12508` — `AgentOrchestra`: relevant to hierarchical multi-agent orchestration, but search evidence makes it adjacent to tool mediation rather than directly about harnesses.
- `2504.21030` — `Advancing Multi-Agent Systems Through Model Context Protocol`: useful MCP background, but better handled as supporting infrastructure vocabulary than as a candidate paper anchor.
- `2604.16762` — `Capability-Sealed Secret Mediation for Secure Agent Execution`: relevant to secure mediation, but the candidate pool already has stronger harness-specific safety anchors.
- `2509.15195` — `Orion`: fuzzing workflow automation adjacency; weaker than `2603.08616` and `2512.03420` for harness construction.
- `2512.04611` — `PBFuzz`: fuzzing adjacency; keep out unless the final paper needs more PoV-generation evidence.
- `2411.11532` — `CKGFuzzer`: older fuzz-driver generation adjacency; not central enough for this topic pool.
- `2603.04915` — `EVMbench`: smart-contract security evaluation adjacency; keep out unless the essay turns toward security benchmarks.
- `2510.02389` — `From Trace to Line`: vulnerability-analysis agent adjacency; not harness-centered from the search evidence.
- `2601.15630` — `Agentic AI Governance and Lifecycle Management in Healthcare`: governance adjacency; domain-specific and weaker than architecture/safety anchors.

## Recommended Initial Reading Order

1. Read `2603.25723`, `2604.18071`, and `2604.25850` together to establish the object: harness as artifact, architecture, and optimization surface.
2. Read `2603.05344` to ground the abstract harness vocabulary in terminal-native coding-agent product mechanics.
3. Read `2604.20801`, `2603.08616`, and `2603.03329` to compare multi-agent, fuzzing, and code-policy harness synthesis.
4. Read `2602.22480`, `2510.11977`, and `2603.28052` to separate evaluation infrastructure from harness optimization.
5. Pull Tier 2 papers only when drafting sections need concrete memory, safety, domain-specific, benchmark, or modularity examples.

## Boundary Notes For Downstream Use

- Do not collapse `agent-control harness`, `evaluation harness`, `fuzz harness`, and `model/context-management harness`; the vocabulary map explicitly warns that these are nearby but distinct meanings.
- For a north-star flagship essay, the strongest claim supported by this pool is: agent progress increasingly depends on non-model infrastructure that can be externalized, inspected, evaluated, and optimized.
- The best exclusion discipline is to drop papers that discuss agents, orchestration, MCP, governance, or security without making the harness itself an explicit control surface.
