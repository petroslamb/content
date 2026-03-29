# Chapter 3 Blueprint: Memory

## Use This Blueprint When

Memory becomes architecture the moment a workflow has to carry trustworthy state across steps, sessions, or repeated tasks. The real question is not how to keep more text around. It is what kind of past state deserves authority in the present, how that state should be retrieved, and when it should stop being trusted.

## The Decision

Every serious memory design has to answer four questions cleanly:

1. What belongs in active context right now?
2. What durable facts should be retrieved on demand?
3. What prior experiences should shape later behavior?
4. What repeated successful routines should stop being rediscovered from scratch?

If those four questions collapse into one storage bucket, the system does not have a memory architecture yet. It has retention.

## Default Position

The default memory stack should stay conservative.

- Keep working memory small and legible.
- Use typed semantic retrieval for durable knowledge.
- Add episodic summaries only when repeated failures justify them.
- Promote repeated successful routines into procedural memory only after repetition is visible.
- Escalate to graph or relational retrieval only when flat retrieval fails for specifically relational reasons.

This is the practical lesson from the memory chapter. Good memory is selective, typed, and governed. It is not a longer prompt with better branding.

## Default Build

### Layer 1: Working Memory

Working memory should hold only the current task state, current plan, recent observations, and temporary scratch state. Treat it like a workbench rather than a warehouse. If active context starts carrying long-lived reference state, memory design has already slipped.

### Layer 2: Semantic Memory

Semantic memory should hold durable facts, documents, policies, structured records, and other reference knowledge that may matter later but does not belong in active context by default. Keep this layer typed by domain and preserve provenance. Policy, user state, product knowledge, and operational records should not compete as if they carried the same authority.

### Layer 3: Episodic Memory

Episodic memory should store interpreted experience from prior runs: failures, corrections, successful workarounds, and notable decisions. Raw transcripts are usually a weak memory object. Compact lessons, summaries, and post-task reflections are usually stronger.

### Layer 4: Procedural Memory

Procedural memory should hold reusable routines: skills, templates, scripts, playbooks, or validated action sequences. If the same successful path keeps recurring, the workflow should stop paying full reasoning cost for it every time.

### Lifecycle Policy

Every durable write should answer four questions before it lands:

1. Why is this worth storing?
2. What memory type does it belong to?
3. Under what trigger will it be retrieved later?
4. When should it be refreshed, summarized, versioned, or deleted?

That lifecycle matters as much as the store itself. A memory layer that writes aggressively and retires nothing will slowly turn relevance into noise.

## Escalate When

- The context window is doing storage work instead of step work.
- The same avoidable mistake survives across runs.
- The same successful routine keeps being rediscovered.
- Retrieval misses linked facts rather than merely similar facts.
- Stale state keeps surfacing with the same confidence as current state.

## Alternatives And When They Win

| Approach | Best use | Why it wins | Main risk |
| --- | --- | --- | --- |
| Working memory only | short bounded tasks | cheapest possible stack | collapses on long or repeated work |
| Typed semantic retrieval | durable factual knowledge | strong default for most builders | stale or weakly ranked retrieval |
| Episodic summaries and reflection | repeated workflows | turns history into reusable lessons | memory sprawl if write discipline is weak |
| Procedural memory | repeated successful routines | converts success into callable capability | brittle routines if promotion is careless |
| Graph or relational retrieval | linked knowledge and multi-hop facts | preserves relationships flat chunks lose | higher complexity before the baseline is stable |

## What To Measure

- Retrieval relevance on real tasks
- Stale retrieval rate
- Token savings against a naive full-history baseline
- Recurrence of corrected failures
- Procedural reuse rate
- Memory write precision, meaning how often stored objects matter later

If memory increases infrastructure cost without improving continuity, retrieval quality, or reuse, it is not helping.

## Failure Review

- Storing everything and retrieving noise
- Mixing instructions, evidence, and facts in one memory channel
- Letting stale policy or stale user state survive without versioning
- Treating raw transcripts as the default durable object
- Confusing retrieval score with authority
- Treating retrieval as a substitute for verification

## Reading Sequence

Start with the live chapter, then widen only as needed.

1. `../../essays/memory/02-memory-systems-and-authority.md`
2. `../../essays/memory/companion.md`
3. `../../reference/papers/memgpt.md`
4. `../../reference/papers/generative_agents.md`
5. `../../reference/papers/memorybank.md`
6. `../../reference/papers/reflexion.md`
7. `../../reference/papers/mem0.md`
8. `../../reference/papers/hipporag.md`
9. `../../reference/papers/voyager.md`

Return to survey sections `3.3.2`, `3.3.3`, `3.4`, `3.4.3`, `3.4.4`, and `3.4.6` when the local design question is clear enough to warrant the full taxonomy.

## Bottom Line

Memory should be governed state, not accumulated residue. Start with a small working set and typed retrieval. Add episodic and procedural layers only when failure analysis earns them. Forgetting, versioning, and promotion rules are part of the architecture, not cleanup after the fact.
