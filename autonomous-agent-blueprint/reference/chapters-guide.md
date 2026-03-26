# Foundation Agents: Practical Chapters Guide

**Note:** This repository provides two complementary practical guides:

- **Practical Chapters Guide** (this document): Navigates the paper itself. Explains which chapters and subsections to read, which anchor papers to focus on, and how to use each chapter when making design decisions. Use this for depth and source context.
- **Practical Distillation** (`foundation-agents-practical-distillation.md`): Condensed operator takeaways. Quick, actionable recommendations and bottom-line advice. Use this for fast reference.

Start with the distillation for orientation, then use this guide to explore specific topics in depth.

---

This note follows the spirit of the exploratory note in `notes/alphaxiv_chat.md`, but makes it more usable as a reading guide to the paper itself.

The goal is not to summarize the whole survey. It is to isolate the chapters that are most useful if you care about building agents, especially digital and enterprise agents, and to explain:
- what each practical chapter is trying to do
- which subsections are worth your time
- which papers are the anchors inside that chapter
- what each anchor paper is actually about
- how to use that chapter when making design decisions

## How to Read the Paper Practically

If you read the paper linearly, it feels much bigger than it is. The practical path is not the same as the paper order.

The most useful reading order is:

1. Chapter 3: Memory
2. Chapter 2: Reasoning and Planning
3. Chapter 8: Action Systems and Tool Use
4. Chapter 9 and Chapter 11: Optimization and Self-Improvement
5. Chapter 14: Multi-Agent Design
6. Chapters 17, 18, and 19: Safety

That reading order gives you a builder's view:
- how the agent remembers
- how it thinks
- how it acts
- how you improve it
- when to split it into multiple agents
- how it fails in production

## Quick Map of the Practical Chapters

### Chapter 3: Memory
This chapter answers: how does the agent carry useful information across time?

### Chapter 2: Reasoning and Planning
This chapter answers: how does the agent break down and work through problems?

### Chapter 8: Action Systems
This chapter answers: what can the agent do in the world, and how does it use tools?

### Chapters 9 and 11: Optimization and Self-Improvement
These chapters answer: how do you improve the system without replacing the base model?

### Chapter 14: Multi-Agent Design
This chapter answers: when should one agent become several, and how should they coordinate?

### Chapters 17, 18, and 19: Safety
These chapters answer: what breaks when agents read, remember, and act on real systems?

## Chapter 3: Memory

### What this chapter is doing

The memory chapter is one of the best parts of the paper because it turns "memory" from a vague buzzword into a design problem. The chapter does not just say agents need memory. It breaks memory into types, shows how information moves through the system, and ties different memory designs to real agent papers.

This is practical because almost every useful agent eventually runs into the same problem: the context window is not enough. Once the agent has to remember project state, user preferences, prior tasks, tool results, or reusable skills, you need an explicit memory system.

### Subsections worth reading

- `3.3.2 Short-Term Memory`
- `3.3.3 Long-Term Memory`
- `3.4 The Memory Lifecycle`
- `3.4.3 Memory Derivation`
- `3.4.4 Memory Retrieval and Matching`
- `3.4.6 Memory Utilization`

You can mostly skip `3.4.5 Neural Memory Networks` on a first practical pass unless you care about memory in model weights.

### The practical picture

The chapter's most useful move is the split between short-term and long-term memory, and then inside long-term memory, the split between semantic, episodic, and procedural memory.

That gives you a real architecture:

- Short-term memory is the active workspace. In practice, this is the prompt, temporary context, scratch state, or current task history.
- Semantic memory is durable factual knowledge: documents, structured facts, product information, policies, account state.
- Episodic memory is what happened before: prior conversations, steps taken, failures, successful task traces.
- Procedural memory is how to do things: reusable routines, code snippets, plans, or skills.

The chapter is also strong on the memory lifecycle. It argues that useful memory is not just stored, it is managed:
- acquire the right information
- encode it into usable form
- summarize or derive higher-level knowledge
- retrieve it based on the current task
- use it in generation or planning
- forget or compress what no longer matters

That lifecycle is the part many "memory agent" demos skip.

### Anchor papers and what they are about

- [MemGPT](https://arxiv.org/abs/2310.08560)
  MemGPT treats the context window like RAM and external storage like disk. The key idea is not just "more memory"; it is explicit memory management. Use it as a reference when you need an agent to move information in and out of active context rather than stuffing everything into one prompt.

- [Generative Agents](https://arxiv.org/abs/2304.03442)
  This is one of the clearest models of episodic memory plus reflection. Agents store many observations, score them by recency, relevance, and importance, and periodically synthesize higher-level reflections. Use this paper when you want to understand how raw experience becomes behavior.

- [MemoryBank](https://arxiv.org/abs/2305.10250)
  MemoryBank applies an Ebbinghaus-style forgetting curve to conversation memory. The practical lesson is simple: memory should decay or be refreshed; otherwise it bloats and becomes noisy.

- [Reflexion](https://arxiv.org/abs/2303.11366)
  Reflexion is not just a reasoning paper; it is also a memory paper. It stores verbal self-feedback from previous attempts and uses it in later tries. Use it when you want agents to learn from failure without model retraining.

- [Mem0](https://arxiv.org/abs/2504.19413)
  Mem0 is a production-oriented long-term memory layer. It extracts and consolidates salient facts from conversations rather than saving everything. It is useful as a practical reference for what a deployable memory service looks like.

- [HippoRAG](https://arxiv.org/abs/2405.14831)
  HippoRAG is a retrieval system that mixes knowledge-graph structure with Personalized PageRank. It matters because it shows when plain vector retrieval is too shallow, especially for multi-hop questions and linked knowledge.

- [Voyager](https://arxiv.org/abs/2305.16291)
  Voyager is important because it treats successful code behaviors as memory. Instead of only storing facts or chat history, it builds a skill library. This is the clearest procedural-memory pattern in the chapter.

### How to use this chapter in practice

Use this chapter when you need to answer questions like:

- What exactly should my agent remember?
- What should live in the prompt versus in an external store?
- Should I store facts, histories, or executable skills?
- How do I stop memory from becoming noisy or stale?
- How should retrieval work when the agent is in the middle of a task?

If you are building an enterprise agent, the most realistic design that comes out of this chapter is:
- short-term context for the current task
- RAG or structured retrieval for semantic memory
- session and task history for episodic memory
- a small skill or routine library for procedural memory
- summarization and forgetting so the system stays usable over time

### What is already practical vs what is promising

Already practical:
- RAG-backed semantic memory
- episodic task logs and session history
- reflection summaries after a task
- memory decay or pruning
- skill libraries for repeated routines

Promising but not default:
- graph-heavy retrieval for complex knowledge bases
- neural memory inside model weights
- lifelong test-time memory systems

## Chapter 2: Reasoning and Planning

### What this chapter is doing

This chapter is the paper's map of how an agent should think through a task. It separates reasoning structures from planning structures and tries to classify the main prompting and search strategies that have emerged around LLMs.

For builders, the most useful idea is that reasoning is not one thing. There are simple single-path methods, branching search methods, iterative self-correction methods, and planning methods that combine decomposition with action.

That matters because different failures need different scaffolds. Sometimes the agent needs clearer decomposition. Sometimes it needs tool interaction. Sometimes it needs a verification loop. Sometimes it needs branching search.

### Subsections worth reading

- `2.2.2 Dynamic Reasoning Structures`
- `2.2.2.2 Static Reasoning Structures`
- `2.2.3 Unstructured Reasoning`
- `2.2.4 Planning`

You can safely spend far less time on the unified mathematical formalism than on the named reasoning patterns.

### The practical picture

The chapter's practical value is not the taxonomy for its own sake. It is that it tells you which scaffolds help on which kinds of tasks.

The mental model is:

- If the problem is straightforward but multi-step, use chain-of-thought and decomposition.
- If the agent has to act in the world or use tools, use a reasoning-action loop.
- If the first answer is often wrong, add self-consistency or self-refinement.
- If hallucination matters, add explicit verification.
- If the task has many possible paths and dead ends, use a search-style method.

The planning section is especially useful because it makes the shift from "reasoning about the answer" to "building a sequence of actions."

### Anchor papers and what they are about

- [ReAct](https://arxiv.org/abs/2210.03629)
  ReAct alternates between reasoning and acting: think, call a tool or take a step, observe the result, then continue. This is the most important bridge between reasoning chapters and action chapters. Use it whenever the agent interacts with tools or external state.

- [Self-Consistency](https://arxiv.org/abs/2203.11171)
  Instead of trusting one reasoning trace, Self-Consistency samples several and chooses the consensus answer. It is simple, expensive, and often very effective. Use it when reliability matters more than latency.

- [Self-Refine](https://arxiv.org/abs/2303.17651)
  Self-Refine gives the model a draft, then asks it to critique and improve it. This is one of the cleanest "cheap improvement loop" patterns in the chapter.

- [Reflexion](https://arxiv.org/abs/2303.11366)
  Reflexion extends self-correction across attempts by storing verbal feedback about previous failures. It is especially useful on tasks where you can tell whether the previous attempt succeeded.

- [Chain-of-Verification (CoVe)](https://arxiv.org/abs/2309.11495)
  CoVe is a structured way to reduce hallucination: draft an answer, generate verification questions, answer those separately, then produce a revised answer. It is a practical pattern for high-stakes factual outputs.

- [Tree of Thoughts](https://arxiv.org/abs/2305.10601)
  Tree of Thoughts turns reasoning into a search problem over branches of thought. It is useful when there are many plausible paths and the first one often fails.

- [LATS](https://arxiv.org/abs/2310.04406)
  LATS combines LLM reasoning with Monte Carlo Tree Search. It is more powerful than simple prompting, but also slower and more complex. Use it as a reference for difficult planning tasks, not as the default.

- Least-to-Most Prompting Enables Complex Reasoning in Large Language Models
  This breaks a hard problem into easier ordered subproblems. It is one of the most practical planning methods because it maps cleanly to task decomposition.

- Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models
  This asks the model to identify the higher-level concepts first, then solve the specific problem. It is useful when the model jumps too quickly into a brittle local answer.

- LLM+P: Empowering Large Language Models with Optimal Planning Proficiency
  LLM+P connects LLM reasoning to classical planning. It matters because it shows how natural-language systems can hand off structure to a more formal planner when the task needs it.

### How to use this chapter in practice

Use this chapter when the agent gives answers that are:
- too shallow
- inconsistent across attempts
- bad at multi-step tasks
- poor at using tools coherently
- prone to hallucinating intermediate reasoning

The default practical stack from this chapter is:
- decomposition
- ReAct
- a lightweight self-check or verification pass

Then add heavier methods only if the task really needs them:
- Self-Consistency for higher reliability
- ToT or LATS for difficult search-heavy planning
- formal planners when the task has strong structure

### What is already practical vs what is promising

Already practical:
- chain-of-thought style prompting
- Least-to-Most decomposition
- ReAct
- self-refinement
- verification loops

Promising but not default:
- tree search as a standard layer
- world-model-heavy planning
- latent or implicit reasoning methods

## Chapter 8: Action Systems and Tool Use

### What this chapter is doing

This chapter is where the paper becomes most obviously agentic. It stops talking about thought alone and starts talking about action spaces, environments, and tools.

The practical contribution of the chapter is that it makes a simple but important distinction: an agent is not defined by better text generation, but by what actions it can actually take and how well it can use tools.

The chapter is also good because it separates language environments, digital environments, and physical environments. That helps you see that the real near-term action is in digital systems.

### Subsections worth reading

- `8.3.1 Action Space Paradigm`
- `8.3.2 Action Learning Paradigm`
- `8.3.3 Tool-Based Action Paradigm`

If you only care about software and enterprise agents, you should prioritize the language and digital parts of these sections and skim the physical section.

### The practical picture

The chapter argues that there are three increasingly powerful ways to define agent actions:

- plain-text actions
- code as action
- tool invocations in digital or physical systems

The most practical shift is from plain text to structured actions. Once the agent emits code, API calls, browser actions, database queries, or GUI operations, it becomes much more testable and useful.

This chapter also makes clear that "tool use" is not just one feature. It has several distinct problems:
- deciding whether to use a tool
- selecting the right tool
- filling the tool arguments correctly
- executing the tool safely
- integrating the result back into reasoning

### Anchor papers and what they are about

- [ToolFormer](https://arxiv.org/abs/2302.04761)
  ToolFormer shows that language models can learn when and how to call tools from examples. In the survey, it serves as one of the foundational papers for language-based tool use.

- [Gorilla](https://arxiv.org/abs/2305.15334)
  Gorilla focuses on accurate API call generation. It matters because it shows that tool use is partly a retrieval and API-spec understanding problem, not just general reasoning.

- [HuggingGPT](https://arxiv.org/abs/2303.17580)
  HuggingGPT uses an LLM as a controller over many specialist models. This is a strong reference for multimodal orchestration rather than a single monolithic agent.

- [WebAgent](https://arxiv.org/abs/2307.12856)
  WebAgent is a strong example of a web-based digital action agent. It matters because it shows the move from question-answering into task execution over websites.

- Mind2Web
  Mind2Web is a benchmark and reference point for general web action. It is useful if you care about browser agents and general web workflows.

- [Mobile-Agent](https://arxiv.org/abs/2401.16158) and [AppAgent](https://arxiv.org/abs/2312.13771)
  These are mobile and app interaction agents. They matter because they show how the action-space idea extends into GUI-heavy digital environments, not just text or APIs.

- [OmniParser](https://arxiv.org/abs/2408.00203)
  OmniParser is important because it turns screenshots and UI layout into machine-usable structure. This is one of the bottlenecks in computer-use systems.

- [MetaGPT](https://arxiv.org/abs/2308.00352), [SWE-Agent](https://arxiv.org/abs/2405.15793), and [OpenDevin](https://arxiv.org/abs/2407.16741)
  These matter because they use code as action. Instead of saying what should happen, the agent writes or executes something that can be checked.

- BIRD and Spider 2.0
  These are important because they pull agent action into structured data systems. They are a reminder that enterprise action is often SQL and business data, not just browsers and chat.

### How to use this chapter in practice

Use this chapter when you are making decisions like:

- Should my agent act through text, code, APIs, web, GUI, or database queries?
- Do I need one generic tool layer or many specialized tools?
- How should I represent actions so they are testable and replayable?
- How do I evaluate whether the agent used tools well?

The chapter pushes toward a practical default:
- use structured tool calls where possible
- use code as action when reproducibility matters
- treat digital environments as the main near-term action surface
- instrument tool invocation and selection as explicit system metrics

### What is already practical vs what is promising

Already practical:
- function-calling tool layers
- search, web, database, and code tools
- browser and GUI agents in constrained environments
- code-based agents for software tasks

Promising but not default:
- agents that create new tools on demand
- robust general computer-use across arbitrary apps
- physical-world action outside specialized verticals

## Chapters 9 and 11: Optimization and Self-Improvement

### What these chapters are doing

These chapters are about improving the agent after you have the basic architecture. Chapter 9 is mostly about prompt, workflow, and tool optimization. Chapter 11 expands this into online and offline self-improvement loops.

This is practical because real agent work usually stops being about "what architecture exists?" and becomes "how do I make this thing better without rebuilding it from scratch?"

The paper's best contribution here is that it moves the optimization target from prompts alone to whole workflows.

### Subsections worth reading

- `9.2 Prompt Optimization`
- `9.2.3 Evaluation Metrics`
- `9.3 Workflow Optimization`
- `9.4 Tool Optimization`
- `9.4.3 Evaluation of Tool Effectiveness`
- `11.1 Online Agent Self-Improvement`

### The practical picture

The chapter says that once you have a working agent, there are four main levers:

- improve the prompt
- improve the workflow topology
- improve tool use
- improve the system by feedback loops during or between runs

The most useful practical insight is that optimization needs metrics. The paper is good on this point. It frames tool use as something you can evaluate by invocation accuracy, selection quality, retrieval efficiency, and planning quality, not just vibes.

It also treats workflows as programmable objects. That matters because many current agents are really small multi-step systems, even when people describe them as "one agent."

### Anchor papers and what they are about

- [OPRO](https://arxiv.org/abs/2309.03409)
  OPRO uses the model itself to propose improved prompts based on earlier results. It is useful as a clean example of iterative prompt optimization without new model training.

- [TextGrad](https://arxiv.org/abs/2406.07496)
  TextGrad turns feedback into "textual gradients" that can improve prompts or multi-stage systems. It matters because it pushes optimization from a single prompt into a workflow.

- [AFLOW](https://arxiv.org/abs/2410.10762)
  AFLOW treats workflow search as an optimization problem and uses search over workflow structures. This is useful when you want to think about the workflow itself as the object you are tuning.

- GPTSwarm
  GPTSwarm matters because it treats workflow topology as something that can be optimized, not fixed. It is a good reference for graph-shaped agent workflows.

- [MT-Bench / Chatbot Arena](https://arxiv.org/abs/2306.05685)
  In this context, these matter less as chat benchmarks and more as evidence that LLM-as-Judge became a practical evaluation pattern.

- [Self-Refine](https://arxiv.org/abs/2303.17651) and [Reflexion](https://arxiv.org/abs/2303.11366)
  These are the chapter's most usable feedback-loop papers. They show how to improve a system by critique and memory rather than by retraining the base model.

- [Voyager](https://arxiv.org/abs/2305.16291)
  Voyager appears again because it is also a self-improvement system: attempt, reflect, store successful skills, repeat.

### How to use these chapters in practice

Use them when you have a system that works, but:
- costs too much
- takes too long
- uses tools badly
- fails repeatedly on the same kind of task
- has prompt changes that help one step but break another

The practical workflow coming out of these chapters is:

1. define evaluation cases
2. score the system by quality, cost, and latency
3. improve prompts and output schemas
4. improve routing and tool use
5. add self-refinement or reflection where it clearly helps
6. only then try more ambitious self-improvement loops

### What is already practical vs what is promising

Already practical:
- prompt optimization
- LLM-as-Judge evaluation
- workflow tuning by node and schema
- tool-use metrics
- reflection loops

Promising but not default:
- automatic generation of whole workflows
- self-supervised online redesign of agent architectures
- autonomous tool creation as a routine production feature

## Chapter 14: Multi-Agent Design

### What this chapter is doing

This chapter is about turning a single agent into a coordinated system. It covers roles, topologies, interaction styles, decision-making, communication, and human-agent collaboration.

This chapter is practical when it stays grounded in workflows and handoffs. It becomes less useful when it drifts into large-scale "agent society" ideas. The most useful parts are the ones that help you decide whether you actually need multiple agents and, if you do, how they should exchange work.

### Subsections worth reading

- `14.1.2 Heterogeneous Agents`
- `14.2.1 Static Topologies`
- `14.3.4 Task-oriented Interaction`
- `14.4 Human-Agent Collaboration`
- `14.5 Decision-Making in Multi-Agent Systems`
- `14.6.1 Types of Agent Messages`
- `14.6.3 Next-Generation Communication Protocols`

### The practical picture

The most useful claim in this chapter is that not all multi-agent systems are the same. There are at least three very different reasons to use multiple agents:

- role separation
- reliability through critique or debate
- task decomposition through structured handoffs

For most practical systems, the task-oriented interaction subsection is the strongest. It describes systems where agents pass artifacts, not endless conversation. That is much closer to how useful software pipelines work.

The human-agent collaboration subsection is also important. The paper is better than many agent papers here because it explicitly treats human supervision and multi-turn instruction as first-class collaboration modes.

### Anchor papers and what they are about

- [MetaGPT](https://arxiv.org/abs/2308.00352)
  MetaGPT is one of the clearest role-based pipeline systems: product manager, architect, developer, QA. It matters because it uses documents and handoffs, not just agent chatter.

- [ChatDev](https://arxiv.org/abs/2307.07924)
  ChatDev is another software-team style multi-agent system. It is useful as a reference for role-based collaboration and staged production pipelines.

- [AutoGen](https://arxiv.org/abs/2308.08155)
  AutoGen is the flexible conversation-oriented framework in this set. It matters because it became a practical starting point for many multi-agent experiments and products.

- [Multi-Agent Debate (MAD)](https://arxiv.org/abs/2305.19118)
  MAD uses multiple agents to argue and critique before selecting an answer. It matters when the goal is better reliability, not just division of labor.

- [RECONCILE](https://arxiv.org/abs/2309.13007)
  RECONCILE is important because it turns debate into a more structured decision process, including confidence-weighted mechanisms.

- MCP and A2A
  These are not task-solving papers so much as coordination infrastructure. In the paper they matter because they show that agent systems are moving toward common protocol layers for tools and inter-agent communication.

### How to use this chapter in practice

Use this chapter when you are asking:

- Is one agent enough?
- Do I need specialists or just better workflow structure?
- Should agents talk freely, or pass structured outputs?
- Where should human approval sit?
- What message format should the system use?

The practical lesson is conservative:

- start with one orchestrator if possible
- add specialists only when role separation is real
- prefer structured handoffs over free-form discussion
- use debate only where reliability is worth the extra cost
- keep humans in the loop for review and approval

### What is already practical vs what is promising

Already practical:
- role-based pipelines
- orchestrator-plus-specialist systems
- structured inter-agent messages
- human approval checkpoints

Promising but not default:
- very large agent teams
- dynamic emergent topologies as a core production feature
- broad interoperability layers for all applications

## Chapters 17, 18, and 19: Safety

### What these chapters are doing

These chapters turn the survey from "how to build capable agents" into "how capable agents break." The safety chapters matter because most of the practical agent stack becomes risky as soon as the system reads outside content, stores long-term knowledge, or executes tools.

Chapter 17 is about threats to the LLM core, including prompt injection and hallucination. Chapter 18 is about threats in perception and action, especially tool and supply-chain risk. Chapter 19 is about extrinsic interaction risk, especially RAG poisoning and inter-agent contamination.

### Subsections worth reading

- `17.1.2 Prompt Injection Attacks`
- `17.1.3 Hallucination Risks`
- `18.2.1 Supply Chain Attacks`
- `18.2.2 Risks in Tool Usage`
- `19.1 Agent-Memory Interaction Threats`
- `19.2 Agent-Environment Interaction Threats`
- `19.3 Agent-Agent Interaction Threats`

### The practical picture

The paper is strongest here when it focuses on three real production risks:

- indirect prompt injection through external content
- unsafe tool use and excessive permissions
- poisoned retrieval or memory systems

That is the part of the safety story most teams underestimate. A chat model that looks safe in a demo becomes much less safe when it:
- reads documents from unknown sources
- browses the web
- stores long-term memory
- sends emails, edits files, or triggers transactions
- exchanges messages with other agents

### Anchor papers and what they are about

- Greshake et al. on indirect prompt injection
  This is the key reference for the idea that malicious instructions can hide inside retrieved content and take over the agent's behavior. It is the conceptual foundation for treating outside content as untrusted.

- [InjecAgent](https://arxiv.org/abs/2403.02691)
  InjecAgent is important because it benchmarks real agents against prompt injection and shows how vulnerable many of them are.

- [ToolEmu](https://arxiv.org/abs/2309.15817)
  ToolEmu is a strong practical paper because it emulates tool use in sandboxed environments to expose risky behaviors before deployment.

- AgentPoison
  AgentPoison matters because it shows how poisoned knowledge bases can create backdoor behavior in retrieval-based agents.

- [PoisonedRAG](https://arxiv.org/abs/2402.07867)
  PoisonedRAG is one of the clearest demonstrations that a small number of adversarial documents can distort retrieval behavior in a large database.

- [BadRAG](https://arxiv.org/abs/2406.00083)
  BadRAG shows that tiny fractions of poisoned corpus content can heavily skew retrieval and answers. It is one of the strongest reasons not to treat the knowledge base as inherently trusted.

- [Jamming](https://arxiv.org/abs/2406.05870)
  Jamming matters because it shows denial-of-service style attacks against retrieval, not just misinformation.

- [Agent Smith](https://arxiv.org/abs/2402.08567)
  Agent Smith matters because it makes inter-agent contamination concrete: a single adversarial image can propagate through multimodal agent interactions and infect large populations of agents. Treat inter-agent messages, screenshots, and attachments as untrusted inputs.

- [Chain-of-Verification (CoVe)](https://arxiv.org/abs/2309.11495)
  CoVe appears again here because verification is one of the simplest ways to reduce factual failure in outputs.

### How to use these chapters in practice

Use them when designing:
- content boundaries
- tool permissions
- approval flows
- retrieval pipelines
- inter-agent communication

The practical safety stack implied by the paper is:

- label and isolate untrusted content
- separate instructions from retrieved data
- sandbox tool execution
- enforce least privilege
- require approval for irreversible actions
- monitor retrieval sources and anomalies
- treat inter-agent messages as another untrusted input channel

### What is already practical vs what is promising

Already practical:
- least privilege
- user approval gates
- sandboxing
- content/source separation
- retrieval curation and monitoring
- verification steps for critical outputs

Promising but not default:
- very strong automated detection of every indirect injection
- fully autonomous self-healing safety layers
- debate as a general-purpose safety substitute for access control

## What to Skip on a First Practical Pass

These are not worthless, but they are not where I would spend early reading time if your goal is to build:

- most of the brain-region analogy material
- most of the world model chapter
- most of the reward chapter unless you are doing RL-heavy agent training
- most of the emotion chapter
- the KL-divergence intelligence framing for scientific discovery
- large parts of the "agent society" framing beyond structured multi-agent workflows

## The Practical Core of the Paper

If you compress the whole survey into one builder's model, it looks like this:

- Memory is how the agent persists useful state across time.
- Reasoning is how the agent structures problem-solving.
- Action is how the agent interfaces with software and tools.
- Optimization is how the system gets better after the first version.
- Multi-agent design is about workflow decomposition, not magic intelligence.
- Safety is about boundaries around memory, tools, and untrusted inputs.

That is the practical spine of the paper.

## Suggested Next Step

If you want to turn this paper into a blueprint rather than just a reading guide, the next document should be:

`foundation-agent-enterprise-blueprint.md`

That file would not summarize the paper. It would translate these practical chapters into a concrete architecture:
- components
- memory layout
- reasoning loop
- tool layer
- evaluation loop
- safety boundaries
- where human approval sits
