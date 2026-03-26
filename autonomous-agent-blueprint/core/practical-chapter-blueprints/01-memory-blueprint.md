# Chapter 3 Blueprint: Memory

## Why This Chapter Matters

Memory is the first practical chapter because almost every serious agent breaks the moment the task is longer than a single prompt. The memory chapter is useful not because it proves that memory matters, but because it turns memory into an architectural decomposition. It distinguishes active working state from durable knowledge, and then distinguishes durable knowledge from experience traces and reusable skills.

That distinction is what makes the chapter deployable. Without it, "memory" collapses into one of two bad defaults: either everything stays in the prompt until the context window breaks, or everything gets dumped into a vector store and retrieval quality slowly decays.

## Survey Subsections To Prioritize

- `3.3.2 Short-Term Memory`
- `3.3.3 Long-Term Memory`
- `3.4 The Memory Lifecycle`
- `3.4.3 Memory Derivation`
- `3.4.4 Memory Retrieval and Matching`
- `3.4.6 Memory Utilization`

The practical guide is right to deprioritize `3.4.5 Neural Memory Networks` for first-pass builders. It is relevant for research, but it is not the default enterprise move.

## The Practical Question

The chapter is answering one question: what should the agent remember, in what form, for how long, and with what retrieval logic?

That question has to be split into four smaller ones:

1. What belongs in active context right now?
2. What durable facts should be retrieved on demand?
3. What prior experiences should shape later behavior?
4. What successful routines should become reusable skills?

If a design cannot answer all four, the agent does not really have a memory architecture.

## Core Literature And What Each Paper Adds

### `MemGPT: Towards LLMs as Operating Systems`

This is the best mental-model paper in the memory cluster. Its contribution is not "more context." Its contribution is explicit memory management. The paper reframes the context window as scarce fast memory and external storage as slower memory tiers. That is a builder's insight because it shifts design attention from prompt packing to memory movement.

Use this paper when the agent has to page information in and out of active context across long runs or long sessions.

### `Generative Agents: Interactive Simulacra of Human Behavior`

This paper is still one of the clearest demonstrations of episodic memory plus reflection. Its practical value is that it separates raw observations from synthesized higher-level inferences. That is the difference between storing a log and learning from one.

Use this paper when you want to understand how experience should become reusable state rather than remain unstructured history.

### `MemoryBank: Enhancing Large Language Models with Long-Term Memory`

MemoryBank is valuable because it treats forgetting as a feature. The Ebbinghaus-style decay framing is less important than the practical lesson: stale or low-value memories should weaken or disappear over time unless refreshed. This is the simplest antidote to memory sprawl.

Use this paper when you need a policy for memory decay, refresh, and pruning.

### `Reflexion: Language Agents with Verbal Reinforcement Learning`

Reflexion matters twice. It is a reasoning paper, but it is also a memory paper. It shows that verbal self-critique can become durable experience, which then changes later attempts without retraining the model.

Use this paper when you want the system to learn from failure by storing explicit lessons, not just more transcripts.

### `Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory`

Mem0 is the most deployment-oriented paper in the set. Its importance is that it optimizes for extracting and consolidating salient information rather than saving everything. That is exactly what practical memory systems need.

Use this paper when the design needs a production-style memory service rather than an academic taxonomy.

### `HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models`

HippoRAG matters when plain vector retrieval is too shallow. Its graph-aware retrieval logic is useful for multi-hop or relational knowledge where isolated chunks do not preserve enough structure.

Use this paper when semantic memory has linked entities, dependency chains, or factual relations that simple chunk retrieval loses.

### `Voyager: An Open-Ended Embodied Agent with Large Language Models`

Voyager is the clearest procedural-memory paper in the set. The skill library idea is more important than the embodied setting. The agent stores successful code behaviors and reuses them later instead of rediscovering them.

Use this paper when repeated task routines should become callable skills, templates, or code modules.

## If Your Problem Looks Like X, Choose Y

- If the agent mainly forgets facts, choose semantic memory with retrieval and freshness rules.
- If the agent repeats avoidable mistakes, choose episodic memory plus reflection.
- If the agent keeps rediscovering the same routines, choose procedural memory and a skill library.
- If plain similarity retrieval misses linked facts, escalate toward graph-aware retrieval such as HippoRAG.
- If memory is mostly long prompts, stop and redesign the write, retrieval, and pruning policy first.

## Method Comparison Matrix

| Method | Best use | Main strength | Main risk | Escalate when |
| --- | --- | --- | --- | --- |
| Working memory only | short bounded tasks | cheapest and simplest | collapses across long or repeated work | the context window becomes the bottleneck |
| Semantic memory with retrieval | factual knowledge | durable knowledge on demand | stale or weak retrieval | facts are linked or need stronger provenance |
| Episodic memory and reflection | repeated workflows | turns history into learnable experience | noisy histories and memory sprawl | repeated failures survive across runs |
| Procedural memory or skill library | reusable routines | turns success into callable behavior | brittle or outdated routines | the same task class keeps recurring |
| Graph-aware retrieval | multi-hop knowledge | preserves relations better than flat chunks | higher indexing and retrieval complexity | plain retrieval misses relational structure |

## The Chapter's Main Architectural Insight

The chapter's strongest contribution is the memory split:

- short-term memory as active workspace
- semantic memory as durable factual knowledge
- episodic memory as task history and traces
- procedural memory as reusable know-how

That split is more useful than any vendor-specific memory stack because it tells you what type of information each storage layer should hold. The real practical advance is that the chapter also describes memory as a lifecycle:

- acquire
- encode
- derive or summarize
- retrieve
- use
- forget

This means a memory system is not just a storage backend. It is a policy system governing write decisions, retrieval decisions, compression, and deletion.

## The Default Memory Blueprint

### Layer 1: Working Memory

Keep only the current task state, current plan, recent tool outputs, and temporary scratch state in active context. Working memory should stay small enough to remain legible and cheap.

### Layer 2: Semantic Memory

Store documents, facts, policies, structured records, and durable reference knowledge externally. Retrieval should be task-aware, source-aware, and ideally typed by domain so that policy text, product docs, and user records do not collapse into one undifferentiated corpus.

### Layer 3: Episodic Memory

Store prior runs, decisions, failures, corrections, and notable interaction outcomes. Episodic memory should support reflection and future debugging, not just personalization.

### Layer 4: Procedural Memory

Store successful routines as skills, templates, playbooks, or code. If a behavior repeats and matters, it should stop being rediscovered from scratch.

### Lifecycle Policy

Every memory write should answer four questions:

1. Why is this worth storing?
2. What memory type does it belong to?
3. How will it be retrieved later?
4. When should it decay, summarize, or be deleted?

## Design Decisions That Matter Most

### What belongs in the prompt versus the store

The prompt should hold active state. The store should hold durable or replayable state. If the information will matter after the current step, it probably belongs outside the prompt.

### When to use vector retrieval

Use vector retrieval for broad semantic lookup over documents and factual chunks. It is the default for general enterprise knowledge assistants.

### When to use graph or relational retrieval

Use graph-heavy retrieval when the task depends on linked knowledge, entities, or multi-hop reasoning. If the agent repeatedly fails because relevant facts are connected rather than merely similar, vector retrieval alone is too weak.

### When to introduce procedural memory

Introduce procedural memory when the agent repeatedly solves the same kind of problem with similar steps. The clearest sign is repeated successful tool sequences or code patterns.

### When forgetting becomes mandatory

Forgetting becomes mandatory as soon as memory quality starts degrading retrieval quality. A memory system that never deletes or compresses is not persistent intelligence; it is slow corruption.

## Failure Modes

- storing everything and retrieving noise
- mixing instructions and facts in the same memory channel
- letting stale policy or stale user state survive without versioning
- storing raw transcripts when summarized facts would be better
- never promoting repeated routines into procedural memory
- treating retrieval scores as trust scores

## Evaluation

The chapter implies a memory evaluation stack, even if it does not formalize it as a product rubric:

- retrieval relevance on real tasks
- stale-memory rate
- token savings versus full-history baselines
- correction recurrence rate
- procedural reuse rate
- memory write precision, meaning how often stored items matter later

If a memory layer adds cost but does not improve continuity, reuse, or retrieval quality, it is not working.

## Recommended Build Order

1. Start with semantic retrieval plus small working memory.
2. Add episodic traces and post-task summaries.
3. Introduce forgetting and pruning before memory volume explodes.
4. Add procedural memory once repeated routines are visible.
5. Escalate to graph or advanced retrieval only when failure analysis justifies it.

## Anti-Patterns

- Do not begin with neural memory in model weights.
- Do not begin with a giant undifferentiated "memory" collection.
- Do not write every interaction to durable storage.
- Do not treat memory retrieval as a substitute for verification.

## Reading Sequence For This Chapter

1. `../../essays/memory/03-memory-v5.md`
2. `../../essays/memory/companion.md`
3. `papers/memgpt.md`
4. `papers/generative_agents.md`
5. `papers/memorybank.md`
6. `papers/reflexion.md`
7. `papers/mem0.md`
8. `papers/hipporag.md`
9. `papers/voyager.md`

## Bottom Line

The chapter's practical message is simple: memory should be typed, managed, and selective. A good memory blueprint is not "longer context." It is a disciplined system for turning transient runs into durable, retrievable, and governable state.
