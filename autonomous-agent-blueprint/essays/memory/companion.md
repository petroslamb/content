# Memory Companion

Memory usually disappoints for a simple reason. Teams think they are adding recall when they are really creating future interference. A workflow stores every transcript, every correction, every artifact, every note, and calls the result long-term intelligence. Months later the system answers with stale policy, revives dead conventions, repeats an old mistake in a new setting, and retrieves the wrong thing with total confidence. The store is full. The agent still does not feel as though it has learned.

The useful second-pass view is harsher. Memory is not a single feature and not a single store. It is a set of decisions about which parts of the past deserve to stay live, which deserve to harden, which deserve to decay, and which should never have been written in the first place. That is what makes memory architecture so practical. It turns retained state from a quantity problem into a truth-management problem.

The public essay keeps the law severe and narrow. This companion owns the surrounding terrain: derivation, retirement, procedural promotion, and the retrieval escalations that belong outside the deployable center.

## The Missing Middle Is Derivation

A lot of memory systems implement only two verbs: write and retrieve. That is not enough.

Raw history is rarely the right memory object. A long conversation may contain one durable fact, one correction worth reusing later, and a lot of local noise that should never survive the task. A terminal transcript may contain a convention, a failed approach, and an irrelevant detour. If the system stores all of that in one undifferentiated way, later retrieval has to sift meaning from debris.

Derivation belongs at the center of a serious memory design. An observation becomes a fact summary, a failure lesson, a promotion candidate for a routine, or nothing at all. Without that middle step, "memory" becomes storage plus wishful retrieval.

Generative Agents and Reflexion both matter here for the same deeper reason. They do not treat experience as valuable simply because it happened. They try to turn history into a more useful object. That is the part most teams still skip.

## Four Memory Types Mean Four Different Truth Problems

The typed split remains the best baseline in the package because it solves a real operational confusion.

Working memory is the live task surface. If it gets too large, attention fragments and the current step loses shape.

Semantic memory is durable knowledge. If it lacks provenance, freshness rules, or retirement, the system starts treating yesterday's truth as today's authority.

Episodic memory is prior experience. If it is missing, the workflow keeps paying to relearn old failures. If it is noisy, the workflow starts treating random history as policy.

Procedural memory is reusable know-how. If it is absent, the system rediscovers the same routine repeatedly. If it is sloppy, the library becomes a junk drawer full of one-off wins that never deserved promotion.

This is where the field still gets memory wrong. It asks whether the agent can remember when the real question is what kind of past the system is trying to preserve. Facts, episodes, and routines should not be written, retrieved, or retired under the same rules.

## Read And Write Should Not Share The Same Threshold

One of the most common memory design mistakes is to make writing easier than later trust can justify. The system writes a note because it might be useful, stores a correction because it sounds plausible, or saves a summary because the run felt important. Months later that same object comes back through retrieval as though it had earned durable status.

Read policy and write policy should therefore be asymmetric. A workflow can often afford generous read access to well-governed memory classes while staying much stricter about what gets written, promoted, refreshed, or allowed to persist. That asymmetry is one of the simplest ways to keep memory from becoming a landfill of future interference.

It also clarifies the role of humans and verification. Some facts should only become durable after a checked extraction step. Some routines should only become procedural memory after repeated success across similar tasks. Some episodic traces should stay local to case review instead of entering a shared store at all. Teams that skip this distinction usually end up debugging retrieval quality when the real mistake was admission policy.

The asymmetry also gives builders a saner rollback path. When writes are selective, a bad memory policy can be corrected without excavating an entire polluted archive. When writes are loose and trust is generous, every cleanup becomes forensic work against history that never should have hardened.

## Retirement Is Part Of Accuracy

Forgetting still sounds to many teams like a concession. It should sound more like hygiene in defense of truth.

A reimbursement policy from six months ago is not just old information. In the wrong retrieval path it becomes active misinformation. A deprecated routine is not neutral procedural history. In the wrong context it becomes a bad suggestion with the authority of prior success. A long-term memory layer that never demotes stale state is not more intelligent. It is less selective about what counts as current.

MemoryBank remains useful because it keeps forcing this point back into the conversation. The paper was not merely solving longer retention. It was trying to solve retention quality through decay and refresh logic. That should influence builders far more than the surface metaphor. Retention policy is part of correctness.

The operator rule is simple: introduce retirement before scale makes it painful. A team that waits until retrieval quality is already collapsing will have to unpick a polluted store rather than govern a clean one.

Working memory deserves the same severity. Teams often think of it as free space because it lives close to generation. It is not free. Every irrelevant trace, old thought, or redundant observation entering active context competes with what the current step actually needs. Scarcity at the working layer is not a flaw in the system. It is part of how the system keeps the present task sharper than the rest of its history.

Deletion belongs in the same doctrine. If the team cannot say how a fact, routine, or case summary should be retired when it stops being trustworthy, the memory layer is still incomplete. Durable state without a clear path to demotion is not a knowledge system. It is a queue for future contradiction. Good memory systems stay useful partly because they know how to forget on purpose.

## Procedural Memory Should Feel Earned

Procedural memory is where a lot of systems either become more useful or quietly start hoarding artifacts.

The right promotion standard is strict. A routine should move into procedural memory only after repeated success, stable inputs, and clear boundaries on when it applies. That is what makes Voyager more important than its surface setting suggests. The paper was solving compounding competence by storing successful behaviors as callable assets instead of leaving them trapped in isolated runs.

That idea transfers well outside embodied environments. If a workflow keeps solving the same patch pattern, report pattern, or retrieval tactic, some part of that success should become explicit and reusable. But promotion has to stay selective. A single success is usually not a skill. It is an anecdote.

This is the anti-pattern to avoid: transcript hoarding disguised as learning. A procedural layer should look like promoted competence, not accumulated souvenirs.

## Escalate Retrieval Only When The Object Is Relational

Flat retrieval is not obsolete. Most teams underuse it well before they outgrow it.

Graph-aware and richer relational memory approaches matter once the memory object itself stops being mostly topical. If the system needs to reason over linked entities, dependencies, or multi-hop structure, then better ranking on flat chunks may not solve the problem because the representation is wrong. HippoRAG matters exactly at that boundary. It signals a shift from "retrieve the right text" to "retrieve the right knowledge structure."

That is the correct escalation rule. Do not reach for graph-heavy memory because retrieval feels vaguely disappointing. Reach for it when failure analysis says the missing thing is relational structure rather than policy, freshness, or derivation quality.

## Next Layer

Use the [public essay](../memory/03-memory-v6.md) for the doctrinal center, the [memory blueprint](../../core/practical-chapter-blueprints/01-memory-blueprint.md) for lifecycle policy and retrieval choice, and the paper notes for MemGPT, Generative Agents, MemoryBank, Reflexion, Mem0, Voyager, and HippoRAG when you need source-level detail rather than the broader companion cut.
