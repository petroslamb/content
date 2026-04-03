# Memory Companion

The hard part of memory is not recall. It is deciding what deserves to survive. Teams often think they are adding continuity when they are really manufacturing future interference. Every transcript gets saved. Every correction gets written somewhere. Every artifact feels as though it might matter later. Months pass, the store grows, and the workflow starts surfacing stale policy, reviving dead conventions, and retrieving the wrong thing with total confidence. The archive is full. The system still does not feel as though it has learned.

The useful second-pass view is harsher. Memory is not a single feature and not a single store. It is a set of decisions about which parts of the past deserve to stay live, which deserve to harden, which deserve to decay, and which never should have been written in the first place. That is what makes memory architecture so practical. It turns retained state from a quantity problem into a truth-management problem.

The public essay keeps the law severe and narrow. This companion owns the surrounding terrain: derivation, admission thresholds, retirement policy, procedural promotion, and the retrieval escalations that belong outside the deployable center.

## The Missing Middle Is Derivation

A lot of memory systems implement only two verbs. Write and retrieve. That is not enough.

Raw history is rarely the right memory object. A long conversation may contain one durable fact, one correction worth reusing later, and a lot of local noise that should never survive the task. A terminal transcript may contain a convention, a failed approach, and an irrelevant detour. If the system stores all of that in one undifferentiated way, later retrieval has to sift meaning from debris.

Derivation belongs at the center of a serious memory design. An observation becomes a fact summary, a failure lesson, a promotion candidate for a routine, or nothing at all. Without that middle step, memory becomes storage plus wishful retrieval.

This is why *Generative Agents*, *Reflexion*, and *Mem0* matter even though they do not all sit in the public essay. They do not treat experience as valuable simply because it happened. They try to turn history into a more useful object. That is the part most teams still skip.

## Four Memory Types Mean Four Different Truth Problems

The typed split remains the best baseline in the package because it solves a real operational confusion.

Working memory is the live task surface. If it gets too large, attention fragments and the current step loses shape.

Semantic memory is durable knowledge. If it lacks provenance, freshness rules, or retirement policy, the system starts treating yesterday's truth as today's authority.

Episodic memory is prior experience. If it is missing, the workflow keeps paying to relearn old failures. If it is noisy, the workflow starts treating random history as policy.

Procedural memory is reusable know-how. If it is absent, the system rediscovers the same routine repeatedly. If it is sloppy, the library becomes a junk drawer full of one-off wins that never deserved promotion.

This is where the field still gets memory wrong. It asks whether the agent can remember when the real question is what kind of past the system is trying to preserve. Facts, episodes, and routines should not be written, retrieved, or retired under the same rules. The four-layer split matters because it prevents one storage surface from pretending to solve four different truth problems.

## Read And Write Should Not Share The Same Threshold

One of the most common memory design mistakes is to make writing easier than later trust can justify. The system writes a note because it might be useful, stores a correction because it sounds plausible, or saves a summary because the run felt important. Months later that same object comes back through retrieval as though it had earned durable status.

Read policy and write policy should therefore be asymmetric. A workflow can often afford generous read access to well-governed memory classes while staying much stricter about what gets written, promoted, refreshed, or allowed to persist. That asymmetry is one of the simplest ways to keep memory from becoming a landfill of future interference.

It also clarifies the role of humans and verification. Some facts should only become durable after a checked extraction step. Some routines should only become procedural memory after repeated success across similar tasks. Some episodic traces should stay local to case review instead of entering a shared store at all. Teams that skip this distinction usually end up debugging retrieval quality when the real mistake was admission policy.

## Retirement Is Part Of Accuracy

Forgetting still sounds to many teams like a concession. It should sound more like hygiene in defense of truth.

A reimbursement policy from six months ago is not just old information. In the wrong retrieval path it becomes active misinformation. A deprecated routine is not neutral procedural history. In the wrong context it becomes a bad suggestion with the borrowed authority of prior success. A long-term memory layer that never demotes stale state is not more intelligent. It is less selective about what counts as current.

*MemoryBank* remains useful because it keeps forcing this point back into the conversation. The paper was not merely solving longer retention. It was trying to solve retention quality through decay and refresh logic. That should influence builders far more than the surface metaphor. Retention policy is part of correctness.

The operator rule is simple. Introduce retirement before scale makes it painful. A team that waits until retrieval quality is already collapsing will have to unpick a polluted store rather than govern a clean one.

Working memory deserves the same severity. Teams often think of it as free space because it lives close to generation. It is not free. Every irrelevant trace, old thought, or redundant observation entering active context competes with what the current step actually needs. Scarcity at the working layer is not a flaw. It is part of how the workflow keeps the present task sharper than the rest of its history.

## Procedural Memory Should Feel Earned

Procedural memory is where a lot of systems either become more useful or quietly start hoarding artifacts.

The seductive mistake is to treat every successful tactic as though it had earned promotion. One prompt worked once. One shell sequence solved a bug. One escalation template happened to pass. None of that guarantees reusable know-how. A routine deserves promotion only when the task class repeats, the success conditions are legible, and the stored object will still be interpretable later.

That is why *Voyager* matters to the broader memory discussion even though it is not centered in the public essay. The paper made procedural promotion visible in a setting where routines had to become reusable to matter. The lesson is broader than the environment. Promote repeated competence, not lucky improvisation.

The same severity should govern deletion. If the team cannot say when a fact, routine, or case summary should be retired, the memory layer is still incomplete. Durable state without a clear path to demotion is not a knowledge system. It is a queue for future contradiction.

## Richer Retrieval Comes After Governance

Graph-heavy retrieval, relational memories, and more elaborate memory topologies are real advances. They matter when the task depends on linked entities, dependency chains, or multi-hop factual structure that flat similarity search keeps losing.

They should not be where a team hides from the harder governance question. If freshness, provenance, admission policy, derivation, and forgetting are still weak, richer retrieval mostly makes clutter easier to traverse. It does not make the memory layer more trustworthy.

That is the second-pass discipline the package cares about most. Governance before sophistication. Typed memory before warehouse thinking. Promotion before hoarding. Retirement before regret.

## Analytical References

**[MemGPT note](../../reference/papers/memgpt.md).** This note explains the tiered-memory framing that turns context pressure into an explicit management problem. It is the best reference when the memory argument starts with movement between active state and external stores.

**[MemoryBank note](../../reference/papers/memorybank.md).** This note is about forgetting, decay, and refresh logic. It matters when the discussion needs a source for why retention policy is part of correctness rather than a secondary cleanup concern.

**[Mem0 note](../../reference/papers/mem0.md).** This note is about derived memory objects and production-style consolidation. It is useful when the workflow should store extracted facts or promoted routines instead of hoarding transcripts.

**[Generative Agents note](../../reference/papers/generative_agents.md).** This note is about turning raw observations into higher-level reflections. It matters when episodic memory needs to become a better object than a chronological log.

**[HippoRAG note](../../reference/papers/hipporag.md).** This note is about graph-aware retrieval for linked knowledge. It is the right reference when simple similarity search fails because the real problem is relational structure rather than topical recall.

## Sources Behind This Chapter

The core sources behind this chapter are [*MemGPT*](https://arxiv.org/abs/2310.08560), [*MemoryBank*](https://arxiv.org/abs/2305.10250), and [*Mem0*](https://arxiv.org/abs/2504.19413). They matter together because they define the chapter's practical center of gravity: explicit tiering, forgetting as part of correctness, and derived memory objects that deserve durable status. Read together, they move memory away from storage enthusiasm and toward governance over time.

The adjacent terrain expands the same question in different directions. *Generative Agents* and *Reflexion* matter because they show how experience can become a better object than raw history. *Voyager* matters because it makes procedural promotion concrete. Graph-aware retrieval work matters because some tasks really do need richer relational structure. These sources belong in the companion because they widen the taxonomy without weakening the public law.

The broader picture of the chapter is authority over the past. The [public essay](03-memory-v7.md) keeps the doctrine hard enough to carry into design review. The [memory blueprint](../../core/practical-chapter-blueprints/01-memory-blueprint.md) turns that law into layer choices, lifecycle policy, and anti-patterns. The paper notes let the interested reader move back into the literature and inspect how tiering, derivation, forgetting, and procedural promotion each contribute to one builder doctrine about trustworthy memory.
