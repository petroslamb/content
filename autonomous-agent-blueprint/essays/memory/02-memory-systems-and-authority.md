# Operating Agents II: Memory Systems and Authority

*Part of the Operating Agents series, a builder-first run on how modern agent systems actually work once language leaves the prompt and starts acting inside software.*

#### Video TL;DR

[AI Agent Memory Blueprint](./artifacts/video/AI%20Agent%20Memory%20Blueprint.mp4)

## When The Past Becomes Part Of The System

A support agent can answer a refund question correctly on Monday and still make the wrong decision on Thursday if it keeps trusting stale policy, old customer state, or a summary written for a different case. That is the practical memory problem in agent systems. The issue is rarely that the model has too little text available. The issue is that the workflow has not decided what kind of past information deserves authority in the present, how that information should be stored, and when it should stop being trusted.

That is why memory should not be introduced as "long context" with better branding. A larger context window can postpone one failure mode, but it does not solve the design problem. A usable memory architecture has to separate what belongs in active context right now from what should live in a durable store, what should be retrieved only under the right conditions, what should be turned into a lesson, and what should be retired before it starts quietly steering later work in the wrong direction. That is the memory distillation taken here from the broader [foundation-agents survey](https://arxiv.org/abs/2504.01990) and organized in the local [memory blueprint](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/01-memory-blueprint.md). The central question is not how much the system can keep. It is how much of the past the present workflow should obey.

![Slide 2: The two bad defaults](./artifacts/slides/AI%20Memory%20Architecture/slide-002.png)

Two design habits make this problem worse. The first is prompt packing: tool outputs, prior messages, excerpts, and notes remain in active context long after they have stopped helping the current step. The second is indiscriminate storage: everything gets embedded, indexed, and left available for later retrieval whether or not it was worth preserving. The first habit overloads the model's working area. The second creates a durable store full of mixed authority, mixed relevance, and weak retrieval signals. Both habits feel like continuity. In practice they create interference.

The simplest way to regain clarity is to ask four questions. What does the model need in front of it right now in order to complete the next step well. What facts or documents should remain available for later retrieval. What experiences from earlier runs should influence later behavior. What repeated successful procedures should stop being rediscovered from scratch. These are not four names for the same storage bucket. They are four different memory jobs, and each one needs a different admission rule, retrieval rule, and expiration rule.

![Slide 3: The four memory questions](./artifacts/slides/AI%20Memory%20Architecture/slide-003.png)

Once the problem is framed that way, memory becomes easier to teach and easier to build. Instead of one large, vague promise about persistence, we get four concrete design responsibilities: keep the active context small, make durable retrieval trustworthy, turn experience into reusable lessons, and promote repeated procedures into explicit skills only when repetition justifies it. Everything else in the architecture follows from that separation.

## Four Kinds Of Memory, Four Different Jobs

Working memory is the narrowest layer and the one most teams misuse first. Its purpose is not to hold everything the system might possibly need. Its purpose is to hold the smallest set of state needed for the next operation: the current task, the immediate subgoal, the most relevant recent tool output, and perhaps a compact scratch area. The right mental model is not a warehouse. It is a workbench. If the bench is covered with every tool, note, and receipt from the last month, nothing on it is easy to use. Agent context behaves the same way.

![Slide 5: Active state versus durable knowledge](./artifacts/slides/AI%20Memory%20Architecture/slide-005.png)

Semantic memory begins where the workbench ends. This is the durable reference layer: policies, product documentation, structured records, inventories, logs, and other facts that may matter later but do not deserve to live in active context by default. The usual mistake is to treat all of that material as one searchable mass. Good systems do the opposite. They type it by domain, preserve provenance, and retrieve it through paths that match its trust level. A policy document, a customer profile, and an operations runbook may all be relevant to the same ticket, but they should not compete as if they were interchangeable evidence.

This is where the retrieval design starts to matter as much as the store itself. Imagine a question such as whether a customer received a refund last month. A weak store may return a policy excerpt about refund conditions, a vague prior case summary, and a user record whose name only partially matches the query. None of those objects is wrong in isolation. The failure appears when the model is asked to compose them into one answer without a clear authority ranking. If the system cannot tell which source is authoritative for the question at hand, retrieval becomes a generator of plausible confusion.

Episodic memory serves a different purpose. It stores what happened in earlier runs in a form that later work can use. This is not the same as keeping raw histories forever. Most long chat logs are a poor memory object because they mix signal and noise, and they force later retrieval to reconstruct the lesson from scratch. A more useful episodic layer stores interpreted experience: a failure pattern, a successful workaround, a correction that prevented recurrence, or a note that a particular environment behaves differently than the documentation suggests. Work such as [*Generative Agents*](https://arxiv.org/abs/2304.03442) and [*Reflexion*](https://arxiv.org/abs/2303.11366) matters here because it shows that reflection and abstraction often create more usable memory than raw preservation.

![Slide 6: Traces and reusable know-how](./artifacts/slides/AI%20Memory%20Architecture/slide-006.png)

Procedural memory is the most selective layer of the four. It asks whether the system should still reason through a procedure from first principles every time, or whether repeated success has earned promotion into a reusable routine. This can take the form of a stored tool sequence, a durable workflow template, a tested script, or a callable skill. The point is not to automate everything. The point is to stop paying repeated reasoning cost for a path that has already been validated enough times to be treated as a stable capability. [*Voyager*](https://arxiv.org/abs/2305.16291) remains useful here because it makes that promotion concrete: repeated success can be compiled into reusable behavior.

Teaching the four-way split matters because it prevents category error. Working memory should be small and fast. Semantic memory should be typed and retrievable. Episodic memory should store interpreted experience rather than endless history. Procedural memory should be rare, explicit, and earned through repetition. When those jobs are merged into one undifferentiated "memory layer," the workflow stops knowing what any stored object is for, and later retrieval inherits that ambiguity.

## Memory Is A Lifecycle, Not A Database

The four-way split is only the beginning. A serious memory design also has to define the lifecycle of a memory object from write to retirement. A useful way to think about the lifecycle is: acquire, encode, derive, retrieve, use, and forget. Something enters the system. The workflow decides how to represent it. It may derive a more compact object from it, such as a lesson or summary. Later, the object may be retrieved under a specific trigger. It influences current work. Eventually it should decay, be versioned out, or be deleted.

That lifecycle perspective changes the write step immediately. Before durable storage happens, the system should be able to answer four basic questions. Why is this worth saving. Which memory type does it belong to. Under what future condition should it be retrieved. When should it stop being trusted. If those questions cannot be answered, the safest default is often not to write the object at all. Cheap storage makes indiscriminate retention easy, but authority is much scarcer and should be granted more carefully.

![Slide 9: The unified memory system](./artifacts/slides/AI%20Memory%20Architecture/slide-009.png)

Several papers become easier to interpret once memory is viewed through that lifecycle. [*MemGPT*](https://arxiv.org/abs/2310.08560) is useful because it frames active context as scarce fast memory and external storage as slower tiers that need deliberate paging. Read that paper not as a claim that paging alone solves memory, but as a reminder that context should be managed rather than inflated. [*MemoryBank*](https://arxiv.org/abs/2305.10250) matters because it puts forgetting back into the system. It shows why retention without decay turns old state into silent interference. [*Mem0*](https://arxiv.org/abs/2504.19413) matters because it emphasizes salience and consolidation. Production systems do not need every observation. They need the small subset that will genuinely improve later runs. [*HippoRAG*](https://arxiv.org/abs/2405.14831) matters because some questions depend on relationships among facts, not just the nearest chunk in embedding space. It is best read as an escalation path, not as a default.

This is also the right place to teach forgetting explicitly. Teams often hesitate to delete, compress, or retire memory because it feels as if they are throwing information away. In practice they are protecting the future workflow from stale authority. Old policy, outdated personal preferences, transient operational notes, and obsolete lessons are all dangerous if they remain retrievable without versioning or expiry. The failure is rarely dramatic. More often the system grows less trustworthy by degrees because outdated state keeps surfacing with the same confidence as current state.

![Slide 13: Failure modes and anti-patterns](./artifacts/slides/AI%20Memory%20Architecture/slide-013.png)

Several failure patterns follow directly from poor lifecycle design. If instructions and reference material live in the same channel, retrieval can blur evidence with control. If every interaction is written durably, the system mistakes exhaust for learning. If stale state is never versioned out, several incompatible truths can coexist in the same store. If retrieval is treated as verification, old similarity can masquerade as current authority. The common thread is simple: memory becomes dangerous when the architecture cannot explain why a stored object should still matter now.

## A Practical Build Order

A useful memory methodology begins with restraint. Start with a small working set and a typed semantic retrieval layer. That combination solves a large share of practical problems because it separates active state from durable reference without overengineering the stack. Once the workflow is running, inspect real failures. If the same kind of mistake keeps recurring across runs, add an episodic layer that stores compact lessons or corrections. If a procedure succeeds often enough that repeated reasoning is wasteful, promote it into procedural memory. If retrieval failures persist because the answer depends on relations among entities, then and only then consider graph-shaped retrieval or richer memory indexing.

![Slide 14: The memory evaluation stack](./artifacts/slides/AI%20Memory%20Architecture/slide-014.png)

That build order is worth teaching because it gives each layer a reason to exist. Semantic retrieval is justified by missing facts. Episodic memory is justified by repeated mistakes the system should stop relearning. Procedural memory is justified by repeated successful routines that deserve compilation. Richer relational stores are justified by retrieval failures that are specifically relational. Without that discipline, teams often add layers in reverse order, ending with a beautiful memory diagram that no observed failure ever required.

Evaluation should be equally concrete. Ask whether retrieval returns the right object for the right question. Measure how often stale or superseded memory is retrieved. Compare token load and latency against a naive full-history baseline. Track whether known corrections actually reduce recurrence. Measure write precision by asking how often stored objects are later used in a way that improves a run. These are not academic extras. They are how a team learns whether the memory layer is creating trustworthy continuity or only additional infrastructure.

The most important lesson is that continuity should be selective. A good memory system does not preserve the past indiscriminately. It protects the present from the wrong parts of the past while making the right parts available at the right time. That is what "memory systems and authority" really means in practice. The design problem is not storage capacity. It is governance over what remains eligible to shape the next decision.

![Slide 15: Memory is governable state](./artifacts/slides/AI%20Memory%20Architecture/slide-015.png)

For the wider memory taxonomy, lifecycle models, retrieval escalations, and a deeper reading guide to the literature, continue with the [Memory Companion](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/memory/companion.md).

## References

[Advances and Challenges in Foundation Agents: From Brain-Inspired Intelligence to Evolutionary, Collaborative, and Safe Systems](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/advances-and-challenges-in-foundation-agents.md) ([arXiv](https://arxiv.org/abs/2504.01990)) is the broad survey behind this series. Read it to place memory alongside action, reasoning, optimization, coordination, and safety. In the memory chapter, its main value is scope: it shows that persistence is not an isolated feature but one layer in a larger operating system for agents.

[Chapter 3 Blueprint: Memory](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/01-memory-blueprint.md) is the most practical follow-on reference for builders. It turns the topic into a usable design aid by separating working, semantic, episodic, and procedural memory, then tying each one to lifecycle and evaluation questions. If you want the operational checklist behind this essay, start there.

[*MemGPT: Towards LLMs as Operating Systems*](https://arxiv.org/abs/2310.08560) is helpful for the paging mental model. It teaches why active context should be treated as scarce fast memory and why external stores need explicit management. Read it when a team is trying to use context expansion as a substitute for memory design.

[*Generative Agents: Interactive Simulacra of Human Behavior*](https://arxiv.org/abs/2304.03442) is worth reading for its treatment of reflection and synthesis. The practical lesson is that useful memory often comes from derived summaries and inferences rather than from storing every observed detail.

[*MemoryBank: Enhancing Large Language Models with Long-Term Memory*](https://arxiv.org/abs/2305.10250) matters because it foregrounds forgetting and refresh. It is a good reference when explaining why retention alone does not create reliable continuity.

[*Reflexion: Language Agents with Verbal Reinforcement Learning*](https://arxiv.org/abs/2303.11366) is useful for episodic memory that actually changes later behavior. Read it as a lesson in converting failure into a durable improvement signal rather than as a reason to preserve raw interaction history.

[*Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory*](https://arxiv.org/abs/2504.19413) is one of the most relevant production references in the set. Its value is not that it makes memory larger, but that it treats salience, consolidation, and selective retention as first-class design concerns.

[*HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models*](https://arxiv.org/abs/2405.14831) is the right escalation reference when flat similarity retrieval stops being enough. Read it when the problem is not recall in general but missing relationships among entities, events, or facts.

[*Voyager: An Open-Ended Embodied Agent with Large Language Models*](https://arxiv.org/abs/2305.16291) is the cleanest reference in this chapter for procedural promotion. It shows how repeated success can become an explicit skill library rather than remaining an expensive reasoning loop repeated from scratch.
