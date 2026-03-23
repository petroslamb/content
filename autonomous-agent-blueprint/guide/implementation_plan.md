# Implementation Plan: Practical Foundation Agents — A 6-Part Substack Guide

## What This Plan Is

This is the decision and implementation document for publishing the six-part guide derived from the `autonomous-agent-blueprint` corpus and the Google *Advances and Challenges in Foundation Agents* (2025) survey. It resolves every contested structural question before writing begins, then specifies each part in enough detail that writing can proceed from this plan without ambiguity.

---

## Resolved Decisions

### Decision 1: Target Reader

**Resolved: The skilled-practitioner-at-inflection-point.**

The target reader is a senior engineer or technical architect who has built at least one LLM-powered prototype but has not shipped a production agent system. They read research-adjacent content, not hallway blog posts. They are skeptical of hype and will abandon writing that lacks specificity. They are not beginners — no paragraph should explain what an LLM is. They are not researchers — no paragraph should spend paragraphs on mathematical notation.

The implicit offer of the series: *You already understand the pieces. This guide tells you what a complete system looks like and why the order of assembly matters.*

Everything that addresses someone who needs to be sold on the idea of agents is cut. Everything that addresses a working builder making a concrete choice stays.

---

### Decision 2: Part Order

**Resolved: Action-first order. Not the chapter-map order.**

The blueprint reading order (Memory → Reasoning → Action → Optimization → Multi-Agent → Safety) is an architectural dependency order designed for reference lookup. It is the wrong order for narrative reading.

The narrative order is:

| Part | Title (provisional) | Why Here |
|------|---------------------|----------|
| 1 | **Action and Tool Use** | Draws the clearest line between what an agent is versus a chat model. Anchors the reader in what distinguishes this whole conversation from prompt engineering. |
| 2 | **Reasoning and Planning** | Once action is established, the natural question is: how does the agent decide what to do next? The reasoning scaffold is the answer. |
| 3 | **Memory** | Now the reader understands what the agent does and how it thinks. The question becomes: how does it persist knowledge and learn across time? Memory is now motivated. |
| 4 | **Multi-Agent Design** | Once single-agent systems are real, the escalation question arrives naturally: when does one agent become several? |
| 5 | **Safety** | The threat model is now intelligible because the reader understands what agents read, do, remember, and communicate. |
| 6 | **Optimization and Self-Improvement** | Deliberately last. Optimization only has meaning once a complete, deployable system exists. The final part is for teams who have crossed that threshold. It is a coda, not a foundation. |

This order tells a building story: define what the system can do → structure how it thinks → give it persistence → scale it carefully → protect it → improve it.

---

### Decision 3: Citation Style

**Resolved: Named in prose, linked at first mention, treated as intellectual artifacts.**

Every anchor paper is named in prose — not as "(Smith et al., 2023)" but as its full name or a clear short form on first reference. Each is linked via footnote or inline markdown at first mention, pointing to the arxiv page. Papers are not cited as credentialing devices. They are included because the mechanism they describe matters for the argument. The treatment follows the voice guide's standard: what problem it solved, why the timing mattered, what the mechanism was, what failure it revealed in the prior approach.

Secondary papers (those not anchor papers but named in the blueprints) are mentioned in passing if they are germane, and omitted if they would interrupt the prose flow. The goal is not to be comprehensive — it is to be right.

The survey itself (*Advances and Challenges in Foundation Agents*, 2025) is cited in the series introduction, not in every part. Each part's theoretical grounding flows through the individual papers, not through the survey as a first-order citation.

---

### Decision 4: Theory-to-Practice Ratio Per Part

**Resolved: Per-part ratio, not uniform enforcement.**

| Part | Theory Weight | Practice Weight | Rationale |
|------|--------------|-----------------|-----------|
| Action (1) | 30% | 70% | The "what is an agent" argument is conceptual but brief. The mechanism question — how actions are represented, selected, and safely executed — is where the practical depth lives. |
| Reasoning (2) | 40% | 60% | The reasoning-scaffold taxonomy (the if-X-choose-Y logic) is the theoretical contribution; case application drives the rest. |
| Memory (3) | 45% | 55% | The four-layer model is a theoretical contribution with high practical density; both halves carry weight. |
| Multi-Agent (4) | 40% | 60% | The three-reason taxonomy is the key theory; the failure mode analysis dominates the practical side. |
| Safety (5) | 35% | 65% | Safety is described through attack papers (theory), but the bulk of the essay is interface architecture (practice). |
| Optimization (6) | 50% | 50% | The conceptual shift (whole-workflow as optimization object) needs full exposition; the four-lever framework is equally weighted. |

---

### Decision 5: Case Study Integration

**Resolved: Embedded scenario fiction, not dossier references.**

The existing case studies (`enterprise-policy-memo`, `coding-bugfix-agent`, `web-form-agent`) are structurally sound but read as reference material, not as narrative material. For Substack essays, they are used as scenario raw material, not as explicit references.

Each part uses at least one embedded scenario — a specific enough fictional team, agent, and failure situation that the reader recognizes their own context. These scenarios are drawn from the failure modes and dossier patterns in the case studies, but they are restructured as narrative (present tense, specific details, grounded failure) rather than as dossier records.

The evaluation files (`failure-mode-catalog.md`, `architecture-review-checklist.md`) contribute specific named failure modes to each part. These are named in the essays because named failures are memorable in a way that generic warnings are not. "Memory sprawl," "agent theater," "planning without grounding," "unstructured handoff drift" — these are the language the reader should leave with.

---

### Decision 6: Series Positioning

**Resolved: Provisional and explicit.**

The series positions itself as: *what the best current research and production patterns say about building agents that actually work* — not as the definitive permanent guide to agent architecture. This phrasing appears in a brief series preface (either a standalone Part 0 post or an intro section in Part 1). The survey's 2025 date is referenced. The fact that some papers are 2023–2024 is acknowledged. The reader is told that the principles are more durable than the specific papers, but the papers give the principles their evidence base.

This is not a hedge. It is the correct epistemic posture for writing about a rapidly-evolving technical field, and it is consistent with the voice guide's characteristic move of intellectual calm without hype.

---

## Part Specifications

### Part 1: Action Systems and Tool Use

**Working title:** *When the Model Starts Doing Things: Action, Tools, and the Architecture of Real Agents*

**Thesis:** The transition from assistant to agent does not happen when the model improves. It happens when the action representation changes. Moving from text output to code-as-action to typed tool invocations in real environments is what makes a system testable, replayable, and meaningfully different from a chatbot.

**Secondary thesis:** Tool use is not one problem. It is five — need detection, tool selection, argument filling, safe execution, result integration. Most production failures live at one of these seams.

**Opening move:** A team builds an LLM system that produces detailed plans in natural language. The plans are correct. Nothing happens. Add an email tool: the first action fails because the argument schema is wrong. Fix the schema: the agent sends to the wrong address because it misread a retrieved contact. Roll back: now there is no rollback because no log was kept. This scenario names the three seams (argument filling, result integration, safe execution) before the essay defines them.

**Theory section:** The action representation ladder — plain text → code → typed tool calls in real environments. Why each rung up makes the system more testable. The five-subproblem decomposition of tool use from Chapter 8.

**Practice section:** The action surface hierarchy (APIs → code → database → browser → GUI). Why the surface choice matters more than model choice for reliability. Tool selection as a retrieval and spec-understanding problem (Gorilla). Code as action and why testability is the payoff (SWE-agent). The database action surface for enterprise contexts (BIRD, Spider 2.0).

**Anchor papers:**
- *ToolFormer* — the conceptual bridge from language to tool use
- *Gorilla* — tool use as API selection and argument construction
- *SWE-agent* — code execution as the action surface for software tasks
- *BIRD* / *Spider 2.0* — the overlooked database surface
- *OmniParser* — GUI as last resort, and why

**Comparison matrix:** One table: action surface, best use, main strength, main risk, when to escalate. Small, earned by the preceding prose.

**Failure modes named:** wrong-tool selection, irreversible action without evidence, observation-action confusion, plain-text plans where typed actions are possible.

**Closing move:** The practical question is not "how autonomous is the agent?" It is: "given this environment, what is the narrowest action surface that still reaches the system?" That question has a specific answer, and it determines whether the system is debuggable.

**Source documents:** `03-action-tool-use-blueprint.md`, `use-cases/coding-agent.md`, `use-cases/web-agent.md`, `failure-mode-catalog.md` (action section), `agentic-architectures-blueprint.md` sections 3 and 5.

**Target word count:** 3,800–4,500 words.

---

### Part 2: Reasoning and Planning

**Working title:** *The Lightest Correct Scaffold: How Agents Think Through Work*

**Thesis:** Reasoning failures are almost never model failures. They are scaffold mismatches. The right reasoning structure makes a capable model reliable on a specific task. The cheapest correct scaffold for each task class exists and is usually simpler than practitioners expect.

**Secondary thesis:** Verification is not a polish step. It is part of the reasoning loop that closes the circuit.

**Opening move:** A capable model fails repeatedly on a multi-step document processing task. The team experiments with longer context, better prompts, a more powerful model. Nothing sticks. The fix turns out to be decomposition — breaking the task into bounded subgoals with typed outputs at each step. The model was never the problem. The scaffold was.

**Theory section:** The four reasoning failure modes (too shallow, brittle single-pass, ungrounded from environment, hallucination-prone) and the scaffold that addresses each. The shift from reasoning about an answer to planning a sequence of actions.

**Practice section:** Decomposition as the first default. ReAct as the backbone for tool-using agents. Self-Refine for near-miss outputs. Chain-of-Verification for high-stakes factual claims. Self-Consistency where reliability justifies the cost. ToT and LATS only for proven branching-heavy tasks.

**Anchor papers:**
- *ReAct* — reason, act, observe; the backbone for tool-using agents
- *Least-to-Most Prompting* — decomposition as the most underrated planning method
- *Chain-of-Verification* — closing the hallucination circuit
- *Self-Refine* — the cheap improvement loop
- *Tree of Thoughts* — when search is actually the answer (and why it usually isn't)

**Comparison matrix:** One table: method, best use, main strength, main risk, when to escalate. Readable as a rapid-reference decision aid.

**Failure modes named:** first-pass overconfidence, planning without grounding, search overkill, verbal fluency mistaken for validated reasoning.

**Closing move:** The practical heuristic: start with decomposition and ReAct. Add verification before anything else. Escalate to search-heavy methods only when failure analysis proves the task has real branching difficulty. The default reasoning stack is not glamorous. That is what makes it deploy.

**Source documents:** `02-reasoning-planning-blueprint.md`, `agentic-architectures-blueprint.md` sections 1 and 4, `failure-mode-catalog.md` (reasoning section).

**Target word count:** 3,500–4,200 words.

---

### Part 3: Memory Systems

**Working title:** *The Agent That Forgets: Memory as Architecture, Not as Prompt Size*

**Thesis:** Memory failures in production agents are almost always retrieval policy failures, not storage failures. Agents do not truly forget — they store the wrong things and retrieve irrelevantly. The solution is not a bigger vector store. It is a write policy, a typed memory architecture, and a forgetting rule.

**Secondary thesis:** The context window is not memory. It is a working desk. Treating it as a filing cabinet is the root cause of most early-stage agent memory problems.

**Opening move:** An enterprise agent that drafts policy memos works well for the first fifty interactions. Then it starts hallucinating citations. Then it starts applying policies from previous clients. Then it fails on simple cases it handled correctly in month one. The memory was never managed — just accumulated. Nothing was forgotten. Everything became noise.

**Theory section:** The MemGPT insight — context window as scarce fast memory, external storage as slower tiers. The four-layer model: working memory, semantic memory, episodic memory, procedural memory. The memory lifecycle: acquire, encode, derive, retrieve, use, forget.

**Practice section:** What each layer holds and how it fails without the others. RAG as semantic memory and its limits (MemoryBank's forgetting argument). Episode logs and reflection (Generative Agents). Procedural memory as skill libraries (Voyager). When plain vector retrieval fails and graph-aware retrieval steps in (HippoRAG). Mem0 as what production memory management actually looks like.

**Anchor papers:**
- *MemGPT* — memory management as a design frame, not prompt packing
- *Generative Agents* — episodic memory plus reflection as a working model
- *MemoryBank* — forgetting as a feature, not a failure
- *Reflexion* — verbal self-critique as durable experience
- *Mem0* — what production-ready memory extraction looks like
- *Voyager* — procedural memory as the skill library pattern

**Comparison matrix:** One table: memory method, best use, main strength, main risk, when to escalate.

**Failure modes named:** memory sprawl, stale memory reuse, wrong memory layer, storing raw transcripts instead of synthesized facts, never promoting routines into procedural memory.

**Closing move:** Memory is not storage. It is a governance policy. A system that stores everything and forgets nothing is not intelligent — it is slow corruption. The question every memory design must answer is not "how much can I keep?" but "what is worth keeping, in what form, for how long, and retrieved how?"

**Source documents:** `01-memory-blueprint.md`, `use-cases/enterprise-agent.md`, `agentic-architectures-blueprint.md` section 2, `failure-mode-catalog.md` (memory section).

**Target word count:** 4,000–4,800 words.

---

### Part 4: Multi-Agent Design

**Working title:** *One Agent Is Not Enough: When to Split, How to Coordinate, What Can Go Wrong*

**Thesis:** Adding agents does not add intelligence. It separates concerns, enables independent review, or structures artifact handoffs. These are workflow engineering decisions. Treating them as intelligence decisions produces agent theater: more agents, no real improvement, a larger failure surface.

**Secondary thesis:** There are exactly three reasons to build a multi-agent system. Confusing them produces three different failure architectures.

**Opening move:** A team is unhappy with the reliability of their single-agent pipeline. They split it into five agents. Each agent has a clever role name. The pipeline takes twice as long, fails in new ways they cannot localize, and produces outputs indistinguishable from the original. The problem was never agent count. The problem was that no version of the system had a verified output at the right stage.

**Theory section:** The three-reason taxonomy — role separation (different tools, permissions, deliverables), reliability through critique (independent review, debate), task decomposition through artifact handoffs (staged pipelines). Why each implies a completely different topology, communication style, and failure mode.

**Practice section:** Single orchestrator as the default. When specialists are real versus cosmetic. Typed artifact handoffs versus free-form conversation — the coordination debt argument. Critique and debate as reliability overlays, not default architecture. Human agents as explicit participants in approval chains.

**Anchor papers:**
- *MetaGPT* — role separation via structured artifact handoffs, not chatter
- *ChatDev* — staged pipeline with real role contracts
- *AutoGen* — the framework that made multi-agent programmable and where it goes wrong
- *MAD* — debate as a reliability pattern, not a general architecture
- *RECONCILE* — structured consensus for harder disagreements

**Comparison matrix:** One table: topology pattern, best use, main strength, main risk, when to escalate.

**Failure modes named:** agent theater, unstructured handoff drift, giving all agents the same permissions, using debate where simple verification would be cheaper, adding specialist roles without specialist evaluation criteria.

**Closing move:** The most important multi-agent design decision is often where the human sits, not how many models are involved. A planner-reviewer pair with a human approval gate is not less sophisticated than a seven-agent system. It is more deployable — and "deployable" is the measure that matters.

**Source documents:** `05-multi-agent-design-blueprint.md`, `agentic-architectures-blueprint.md` section 6, `failure-mode-catalog.md` (multi-agent section).

**Target word count:** 3,500–4,000 words.

---

### Part 5: Safety as Architecture

**Working title:** *The Attack Surface You Built: Agent Safety as Interface Design*

**Thesis:** Agent safety is not an alignment problem. It is an interface architecture problem. The failure modes in Chapters 17, 18, and 19 of the survey are not about model values. They are about the surfaces through which the model receives input, stores state, and takes action. Controlling those interfaces is what controls the risk.

**Secondary thesis:** Every capability chapter has a safety chapter. The same architecture that makes agents useful is the architecture that makes them vulnerable.

**Opening move:** Agent Smith (2024) — a single adversarial image propagates through multimodal agent interactions, infecting large populations of agents without the attacker lifting a finger after the first injection. This is not a distant speculation. This is what the memory and multi-agent capabilities from Parts 3 and 4 look like from an adversarial angle. The capabilities and the vulnerabilities are the same system.

**Theory section:** The six attack surfaces: untrusted content (indirect prompt injection), unsafe tools (excessive permissions, destructive scope), poisoned retrieval (PoisonedRAG, BadRAG), memory poisoning (AgentPoison), retrieval jamming (Jamming), inter-agent contamination (Agent Smith). Why safety happens at interfaces, not inside the model.

**Practice section:** The six-boundary safety blueprint — trust separation, tool containment, action approval gates, memory hygiene, inter-agent skepticism, verification. Red-teaming before widening autonomy. ToolEmu as the sandbox-first safety evaluation loop.

**Anchor papers:**
- *Greshake (indirect prompt injection)* — the conceptual foundation for treating retrieved content as untrusted
- *InjecAgent* — benchmarking injection against real tool-integrated agents
- *PoisonedRAG* / *BadRAG* — small corpus contamination with large behavioral impact
- *AgentPoison* — memory and knowledge stores as attack vectors
- *Jamming* — denial-of-service via retrieval interference
- *Agent Smith* — inter-agent multimodal contamination as propagation
- *ToolEmu* — sandbox-first evaluation for pre-deployment safety

**Comparison matrix:** One table: control, best use, main strength, main risk if missing, when to escalate.

**Failure modes named:** indirect prompt injection via retrieved content, retrieval poisoning from uncurated ingestion, tool overreach via broad permissions, inter-agent contamination through untrusted artifacts, treating post-hoc monitoring as a substitute for containment.

**Closing move:** A system that has never been stress-tested at its interfaces is not safe enough to deploy confidently. Sandboxing, trust separation, approval gates, and retrieval hygiene are not features added after the architecture is complete. They are the architecture. If you are planning to do a red team exercise after launch, you are planning it in the wrong order.

**Source documents:** `06-safety-blueprint.md`, `agentic-architectures-blueprint.md` section 5, `failure-mode-catalog.md` (safety section), `evaluation/architecture-review-checklist.md`.

**Target word count:** 4,000–4,800 words.

---

### Part 6: Optimization and Self-Improvement

**Working title:** *The Workflow Is the Object: How to Improve an Agent System That Already Works*

**Thesis:** Most agent tuning fails because the team optimizes the prompt before they understand the workflow. The correct optimization order exists, is not obvious, and is more conservative than most practitioners expect. The whole workflow is the object, not any single node.

**Secondary thesis:** Measurement is not overhead. It is the product. Without a fixed evaluation set and explicit metrics, agent improvement is drift with intention.

**Opening move:** A team's agent has been in production for four months. Quality is inconsistent. They edit the system prompt twelve times in three weeks. Sometimes it helps, sometimes it regresses something else. They have no evaluation set. Every improvement is a guess. The problem is not the prompts. The problem is the absence of a stable measurement framework before optimization begins.

**Theory section:** The four optimization levers — prompt and schema, workflow topology, tool-use quality, feedback loops. Why the target is the workflow, not the node. The shift from prompt-as-craft to optimization-as-discipline (OPRO, TextGrad). Workflow topology as a searchable object (AFLOW, GPTSwarm). Self-improvement as bounded feedback (Reflexion, Voyager) versus unbounded architectural mutation (the danger zone).

**Practice section:** The correct optimization sequence — lock an evaluation set, measure the current system, improve cheapest surfaces first (schemas, prompts, retrieval), add feedback loops with evidence, search topology only after stability. LLM-as-judge as a practical evaluation tool with calibration obligations. Regression checking as a non-negotiable discipline.

**Anchor papers:**
- *OPRO* — prompt improvement as iterative optimization with evaluation cases
- *TextGrad* — structured feedback as the input to multi-node optimization
- *Self-Refine* / *Reflexion* — the lightweight feedback path before topology search
- *Voyager* — self-improvement through a bounded skill library, not unrestricted self-modification
- *AFLOW* / *GPTSwarm* — when workflow topology itself becomes the optimization target (and why this is not the first move)
- *MT-Bench / Chatbot Arena* — LLM-as-judge as a practical scaling pattern for evaluation

**Comparison matrix:** One table: optimization method, best use, main strength, main risk, when to escalate.

**Failure modes named:** prompt churn without measurement, premature workflow search, LLM-as-judge without calibration checks, allowing self-improvement to touch safety-critical surfaces, optimizing for benchmark scores while production latency collapses.

**Closing move:** An agent deployed for three months is a different thing than a prototype. The three-month deployment has failure patterns, cost curves, latency data, correction logs, and approval hit rates. Those are the inputs to real optimization. Optimization without them is not engineering — it is editing for its own sake.

**Source documents:** `04-optimization-self-improvement-blueprint.md`, `agentic-architectures-blueprint.md` sections on verification and optimization, `failure-mode-catalog.md` (optimization section).

**Target word count:** 3,800–4,500 words.

---

## Series Mechanics

### Series Preface

A brief (~600 word) series introduction precedes Part 1 (either as a standalone post or as an opening section). It establishes:

- What the series is and is not (a practical guide grounded in current research, not a survey summary, not a tutorial)
- The target reader explicitly named
- The survey source (*Advances and Challenges in Foundation Agents*, 2025) acknowledged and linked
- The provisional positioning: this is what the best current evidence says, and the principles are more durable than any individual paper
- The reading sequence rationale (why Action comes first)

### Cross-Series Format Conventions

**Opening move:** Every part opens with a concrete scenario — a specific enough situation that the reader recognizes their own context. This is the narrative anchor. The scenario does not resolve immediately; it is returned to after the theoretical and practical material gives the reader the tools to diagnose it.

**Theory section:** Proposes one or two specific, falsifiable claims about how agents fail or behave in a specific domain. Grounds each claim in named paper mechanisms. Never more than one comparison matrix per part: small, precise, placed once, earned by the prose.

**Practice section:** Translates theory into concrete architecture decisions. Uses named failure modes from the catalog as anchors. Ends with the escalation logic — what the default is, what the signal is that says "go further," and what the next level of complexity costs.

**Closing move:** Returns to the opening scenario with the tools the reader now has. Closes with a single declarative statement — a thesis distilled to one sentence that the reader can carry away.

**Voice notes:** No bullet lists except the single comparison matrix. No em dashes. No "Furthermore," "Moreover," "In conclusion." No "delve," "leverage," "crucial," "tapestry." Decisions stated directly. Papers treated as intellectual artifacts unpacked through mechanism, not citation chain.

---

## Content Not to Write

The following are explicitly excluded from scope for the six-part guide:

- Brain-region analogies from the survey (not useful for builder arguments)
- Emotion and personality modeling chapters
- Physical-world robotics (treated as a different engineering regime)
- Reward modeling and RL-heavy agent training (not the reader's bottleneck)
- Agent society / emergent population dynamics beyond structured multi-agent workflows
- Latent or implicit reasoning methods that have no current production path
- Any framework comparison article ("AutoGen vs LangGraph vs CrewAI")
- Tutorial-style "how to install" or "code walkthrough" material

---

## Quality Gates Per Part

Before any part is considered complete:

1. **Thesis test.** Can the thesis be stated in one sentence? Is it falsifiable? Would a reasonable person disagree with it?
2. **Paper test.** Is every anchor paper cited with its mechanism, not just its name? Does the treatment match the voice guide standard?
3. **Scenario test.** Does the opening scenario feel specific enough to be real? Does the closing return to it with the reader's new tools?
4. **Voice test.** Read two paragraphs aloud. Does it sound like a decisive, technically grounded human who has read the research? Or does it sound like a structured document?
5. **Failure mode test.** Are the named failure modes sharp enough that a reader could recognize one in their own system?
6. **Escalation test.** Is the default clear? Is the escalation signal clear? Is the escalation cost named?

---

## File Destinations

Each essay, once written, is saved into the repo under a new folder to be created:

```
autonomous-agent-blueprint/guide/
  00-series-preface.md
  01-action-tool-use.md
  02-reasoning-planning.md
  03-memory.md
  04-multi-agent.md
  05-safety.md
  06-optimization.md
```

This folder is separate from the blueprint layer (which remains a builder reference system) and from eventual publication files.

---

## What to Do If a Part Is Not Working

If a part's draft does not pass the thesis test after two writing attempts, it means the thesis is wrong — not the prose. Return to the blueprint documents, identify what the most important and most contestable claim is, and restate it. The thesis precedes everything else.

If a part passes the thesis test but fails the voice test, the problem is usually that the theory section has become a paper summary and the practice section has become a checklist. The fix is to re-read one paragraph of existing published work (*The Autonomy Tax*, *The Illusion of the Swarm*) before re-drafting.

---

*Plan compiled March 2026 from analysis of all six `practical-chapter-blueprints/`, `agentic-architectures-blueprint.md`, `foundation-agents-practical-chapters-guide.md`, `evaluation/`, `use-cases/`, `case-studies/`, and `voice_consistency_guide.md`.*
