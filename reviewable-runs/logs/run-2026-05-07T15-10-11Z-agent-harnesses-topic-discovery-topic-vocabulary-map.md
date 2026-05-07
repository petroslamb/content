# Topic Vocabulary Map: agent harnesses

## Scope

- Workflow step: `topic_discovery.map_topic_vocabulary`
- Runtime discovery trigger: `agent harnesses`
- Retrieval mode: deterministic public alphaXiv topic and paper search only.
- Admitted guidance source: `workflows/skills/alphaxiv/SKILL.md`

## Source Hash Awareness

- `workflows/skills/alphaxiv/SKILL.md`
  - declared sha256: `15dc7b3bfbe601198cc29cd67d6e7e2f5c8372651a006d391970c506cc95e2e7`
  - observed sha256: `15dc7b3bfbe601198cc29cd67d6e7e2f5c8372651a006d391970c506cc95e2e7`
  - status: reconciled

## Deterministic Retrieval Performed

- `.venv/bin/alphaxiv search topics "agent harnesses"`
- `.venv/bin/alphaxiv search papers "agent harnesses"`
- `.venv/bin/alphaxiv search all "agent harnesses"`
- `.venv/bin/alphaxiv search topics "coding agent harness evaluation"`
- `.venv/bin/alphaxiv search papers "coding agent harness evaluation"`
- `.venv/bin/alphaxiv paper abstract 2603.25723`
- `.venv/bin/alphaxiv paper abstract 2604.20801`
- `.venv/bin/alphaxiv paper abstract 2604.25850`
- `.venv/bin/alphaxiv paper abstract 2604.18071`
- `.venv/bin/alphaxiv paper abstract 2603.08616`
- `.venv/bin/alphaxiv paper abstract 2603.03329`
- `.venv/bin/alphaxiv paper abstract 2602.22480`
- `.venv/bin/alphaxiv paper abstract 2510.11977`
- `.venv/bin/alphaxiv paper abstract 2603.05344`
- `.venv/bin/alphaxiv paper abstract 2603.28052`

## alphaXiv Topic Slugs To Try

- Direct trigger query returned: `agent-based-systems`, `reinforcement-learning`, `multi-agent-learning`, `cs.RO`.
- Harness evaluation query returned: `agentic-frameworks`, `reinforcement-learning`, `cs.LG`, `cs.AI`.
- Practical next search vocabulary should begin with `agent harnesses`, then branch to `coding agent harness`, `agent evaluation harness`, `agentic frameworks`, `agent optimization`, and `harness engineering`.

## Paper-Search Vocabulary

### Core Harness Terms

- `agent harness`
- `AI agent harness`
- `LLM agent harness`
- `coding-agent harness`
- `model harness`
- `code harness`
- `natural-language harness`
- `portable executable artifact`
- `shared runtime`
- `controller code`
- `runtime-specific conventions`

### Harness Design And Architecture

- `harness engineering`
- `architectural design decisions`
- `agent-system infrastructure`
- `tool mediation`
- `context handling`
- `delegation`
- `safety control`
- `orchestration`
- `subagent architecture`
- `context management`
- `tool systems`
- `safety mechanisms`
- `registry-oriented tool systems`
- `MCP-oriented extensions`
- `plugin-oriented extensions`
- `execution environments`
- `structured governance`
- `audit`

### Optimization And Evolution

- `automatic harness evolution`
- `automated harness engineering`
- `outer-loop optimization`
- `agent optimization`
- `edit-execute-evaluate cycles`
- `harness code search`
- `agentic proposer`
- `source code, scores, and execution traces`
- `experience observability`
- `decision observability`
- `component observability`
- `falsifiable contract`
- `module ablation`
- `code-to-text harness migration`
- `revertible components`

### Evaluation And Benchmarking

- `standardized evaluation harness`
- `reproducible evaluation harness`
- `agent evaluation infrastructure`
- `versioned agent snapshots`
- `budget-controlled evaluation`
- `structured execution traces`
- `parallel evaluations`
- `agent rollouts`
- `scaffolds`
- `benchmarks`
- `LLM-aided log inspection`
- `Terminal-Bench`
- `TerminalBench-2`
- `SWE-bench-verified`
- `TextArena`
- `GameArena`
- `Holistic Agent Leaderboard`

### Multi-Agent And Security Harnesses

- `multi-agent harness`
- `typed graph DSL`
- `agent roles`
- `communication topology`
- `coordination protocol`
- `feedback-driven outer loop`
- `runtime signals`
- `vulnerability discovery`
- `security vulnerabilities`
- `fuzz harness`
- `coverage-guided fuzzing`
- `method-targeted coverage`
- `agent-guided termination`
- `compilation repair`
- `coverage analysis`
- `refinement agent`

### Coding-Agent Product Vocabulary

- `terminal-native agents`
- `CLI-based agents`
- `compound AI system`
- `scaffolding`
- `context engineering`
- `workload-specialized model routing`
- `dual-agent architecture`
- `planning and execution separation`
- `lazy tool discovery`
- `adaptive context compaction`
- `automated memory`
- `instruction fade-out`
- `event-driven system reminders`

## Retrieved Anchor Candidates

- `2603.25723` — `Natural-Language Agent Harnesses`: strongest direct seed anchor; frames harnesses as externalized, editable natural-language artifacts executed by a shared runtime with explicit contracts, durable artifacts, and adapters.
- `2604.18071` — `Architectural Design Decisions in AI Agent Harnesses`: architecture-survey anchor; useful for vocabulary around context management, tool systems, safety mechanisms, orchestration, subagents, MCP/plugins, isolation, and governance.
- `2604.25850` — `Agentic Harness Engineering`: optimization/evolution anchor; useful for observability, autonomous harness evolution, component-level editability, trajectory evidence, falsifiable edits, transfer, and ablation language.
- `2604.20801` — `Synthesizing Multi-Agent Harnesses for Vulnerability Discovery`: multi-agent/security anchor; useful for roles, prompts, tools, communication topology, coordination protocol, runtime diagnostic feedback, and vulnerability-discovery harness synthesis.
- `2603.08616` — `Coverage-Guided Multi-Agent Harness Generation for Java Library Fuzzing`: fuzzing anchor; useful for fuzz harness generation, Java library API invocation, ReAct agents, MCP documentation/source-code queries, coverage feedback, and refinement loops.
- `2603.03329` — `AutoHarness`: code-harness anchor; useful for environment constraints, illegal-action prevention, iterative refinement from environment feedback, TextArena/GameArena, and synthesized policies.
- `2602.22480` — `VeRO`: evaluation-harness anchor; useful for agent optimization, versioned snapshots, rewards, observations, execution traces, and target-agent improvement.
- `2510.11977` — `Holistic Agent Leaderboard`: evaluation-infrastructure anchor; useful for standardized harnesses, parallel VM evaluation, scaffold/model/benchmark axes, rollout logs, and real-world reliability framing.
- `2603.05344` — `OPENDEV terminal coding agent`: product/system anchor; useful for terminal-native coding agents, safety controls, context management, planning/execution separation, lazy tool discovery, context compaction, memory, and system reminders.
- `2603.28052` — `Meta-Harness`: meta-optimization anchor; useful for harness code search, richer prior experience, execution traces, context management, retrieval-augmented reasoning, and agentic coding harness baselines.

## Vocabulary Clusters For Candidate Search

- Scientific object framing: `harness as scientific object`, `transferable harness design`, `compare agent harnesses`, `portable harness artifacts`, `natural-language agent harness`.
- Infrastructure framing: `agent-system infrastructure`, `agent scaffolding`, `tool mediation`, `runtime contracts`, `durable artifacts`, `adapters`, `context services`.
- Evaluation framing: `standardized evaluation harness`, `agent evaluation infrastructure`, `rollout logs`, `execution traces`, `model scaffold benchmark analysis`, `budget-controlled evaluation`.
- Optimization framing: `automated harness engineering`, `outer-loop harness search`, `agent optimization`, `observability-driven evolution`, `harness code optimization`.
- Safety/security framing: `safety mechanisms`, `execution isolation`, `audit`, `vulnerability discovery agents`, `fuzz harness generation`, `illegal action prevention`.
- Product/operations framing: `terminal-native coding agents`, `CLI agent harness`, `context compaction`, `memory systems`, `instruction fade-out`, `event-driven reminders`.

## Search Expansions For Next Step

- `natural language agent harness`
- `agentic harness engineering`
- `automated harness engineering`
- `agent evaluation harness`
- `AI agent evaluation infrastructure`
- `agent scaffold benchmark`
- `model scaffold benchmark agent`
- `agent optimization harness`
- `meta harness model harness`
- `coding agent terminal harness`
- `multi-agent harness synthesis`
- `agent harness vulnerability discovery`
- `fuzz harness generation LLM agents`
- `tool mediation context management agent systems`
- `MCP plugin agent harness`

## Boundary Notes

- The term `harness` splits into at least four nearby meanings: agent-control harness, evaluation harness, fuzz harness, and model/context-management harness. Future candidate ranking should avoid collapsing these meanings unless the essay wants the ambiguity itself.
- `agent harnesses` appears to be a live 2026 vocabulary cluster in alphaXiv search results, so downstream discovery should treat it as a current research term, not only as an internal operator metaphor.
- The strongest north-star angle is likely not "agents are useful"; it is that non-model infrastructure around agents is becoming a first-class, testable, optimizable research object.
- No assistant synthesis, package inspection, or workflow execution beyond `map_topic_vocabulary` was performed.
