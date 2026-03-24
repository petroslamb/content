# Operating Agents III: The Agent That Forgets

## Memory as Governance Over Time

An internal policy assistant worked well in its first months. It answered benefits questions, surfaced current rules, and drafted quick compliance summaries with enough confidence that teams started treating it like background infrastructure.

Then the failures changed shape. The answers were not obviously invented. They were outdated in operationally dangerous ways. A policy revision from three months ago failed to outrank the older version. A retired vendor relationship still appeared as active. A restructuring note from last quarter kept leaking into current org questions. The system was not forgetting facts. It was remembering them without governance.

The team blamed retrieval first. They adjusted embeddings, chunking, and re-ranking. The problem persisted because the failure had started earlier in the chain. Every update had been added to the store. Nothing had been retired, consolidated, versioned, or downgraded. Old and new states now competed in the same memory space, and retrieval was faithfully returning semantically close text from an unmanaged pile.

That is the practical memory problem. Memory is not storage. It is governance over what the agent is allowed to keep, retrieve, reuse, and forget across time.

That framing matters because "memory" is still discussed as if it were mostly about quantity. Longer context windows, larger stores, more recall, richer histories. In live systems the hard questions are different. What deserves to be written at all? In what form? For how long? Under what retrieval rule? At what trust level? When should it be compressed into a summary, promoted into a reusable routine, or removed before it corrupts later work?

If a design cannot answer those questions, it does not really have a memory architecture.

## The Context Window Is A Desk, Not A Filing Cabinet

Teams get memory wrong in part because they use the same word for two very different things. The context window feels like memory because it contains what the model is using right now. But it behaves nothing like durable memory. It is fast, scarce, and volatile. It is a working desk.

This is where *MemGPT* still provides the cleanest mental model. Its enduring contribution is not "more memory." It is explicit memory movement. The active context behaves like scarce fast memory. Durable facts, past episodes, and reusable routines live elsewhere and must be brought back deliberately when the current task needs them.

Once that separation is explicit, the design problem changes. The question stops being "how large a context window do I need?" and becomes "what belongs in active context now, and what should only be retrieved on demand?"

This sounds obvious after the fact. In practice it cuts against a common reflex. When the agent appears to forget, teams stuff more into the prompt. When that stops working, they dump more into a vector store. Neither move answers the real question of what information deserves durable status and what form that status should take.

An agent is not helped by being seated at a desk buried under every note it has ever seen.

## Four Memory Layers, Four Different Jobs

The strongest practical contribution of the memory literature is not a storage mechanism. It is the separation of memory into layers with different jobs.

Working memory holds the current task state: the active question, the current plan, the recent tool outputs, the evidence packet under review, and whatever scratch state the immediate step requires. Its failure mode is overload. If everything enters by default, nothing important dominates attention.

Semantic memory holds durable facts: policies, docs, product knowledge, structured records, approved reference data. Its failure mode is staleness and contamination. If it accumulates without provenance, freshness rules, or retirement paths, it becomes an elegant way to retrieve outdated answers.

Episodic memory holds what happened before: prior runs, corrections, mistakes, approvals, escalations, notable decisions. Its failure mode is amnesia of experience. The agent keeps paying to relearn what the organization already learned the hard way.

Procedural memory holds reusable know-how: templates, routines, playbooks, code snippets, repeatable tactics. Its failure mode is rediscovery. A mature system should not have to solve the same small class of problems from zero every week.

## Memory Layer Map

| Layer | What belongs there | What breaks when it is neglected | Control rule |
|---|---|---|---|
| Working | Current task state and recent evidence | Reasoning noise and lost focus | Keep it small and task-bound |
| Semantic | Durable facts, policies, documents, approved records | Stale or poisoned retrieval | Track provenance, freshness, and versioning |
| Episodic | Prior runs, corrections, failures, approvals | Repeated mistakes with no historical learning | Store events with outcome and context |
| Procedural | Reusable routines, templates, code, playbooks | Endless rediscovery of solved work | Promote only after repeated validated success |

This is not taxonomy for its own sake. It is what lets each memory type live under a different policy. You do not manage policy documents the way you manage correction logs. You do not manage correction logs the way you manage reusable tactics.

## A Coding Agent Fails Differently, But For The Same Reason

The same architecture problem appears in repository work, just with different symptoms.

A coding agent may not need a large personal history, but it does need to remember which repo conventions mattered, which tests repeatedly exposed the same class of mistake, and which patch patterns kept succeeding. If every failed command, every diff, and every terminal trace is dumped into one undifferentiated store, retrieval becomes cluttered and procedural improvement never arrives. The agent sees too much history and learns too little from it.

That is why the coding-agent architecture in this repo keeps working memory tight, uses episodic memory for prior failures and successful fixes, and keeps procedural memory narrow and earned. Repo conventions and previous mistakes are not the same object, and the system gets worse when it stores them as though they were.

Different domain, same rule: memory quality depends less on how much the system kept than on whether it kept the right thing in the right layer.

## Memory Improves Through A Lifecycle, Not Through Accumulation

The next correction matters just as much. Useful memory is not a write-once archive. It is a lifecycle.

*Generative Agents* made this vivid by showing how observations can later be reflected into higher-order summaries. *Mem0* pushed the same idea toward production by emphasizing extraction and consolidation rather than transcript hoarding. *Reflexion* showed how a failed attempt can become a reusable lesson. *MemoryBank* made the neglected point explicit: forgetting is not a defect. It is hygiene.

The lifecycle is straightforward to name and easy to neglect. Information is acquired, encoded, sometimes transformed into a better representation, retrieved when relevant, used inside the current task, and eventually forgotten, compressed, or retired. Each verb hides a design decision.

Acquisition is a gate. Not everything the system sees deserves durable storage.

Encoding is a gate. Raw text, extracted facts, summaries, and structured records behave differently later.

Derivation is a gate. Sometimes the valuable object is not the event itself but the lesson pulled from it.

Retrieval is a gate. Similarity alone is not enough when freshness and provenance matter.

Use is a gate. Retrieved memory has to fit back into working context without crowding out the task.

Forgetting is a gate. If nothing decays, nothing stays trustworthy.

This is the part many memory demos skip because deletion sounds less glamorous than recall. In live systems, the memory that never forgets does not become wiser. It becomes noisier, staler, and easier to manipulate.

## The Default That Holds Up

Most teams do not need an exotic memory stack. They need a governed one.

Keep working memory small and current. Retrieval should compete for scarce attention instead of entering by habit.

Treat semantic memory as a curated knowledge layer with provenance, versioning, and retirement rules. If the underlying source changes, the old answer path should not remain equally eligible forever.

Treat episodic memory as operational history. Preserve prior runs, corrections, reviewer notes, and failure patterns with enough context to matter later.

Treat procedural memory as promoted competence. Do not let it fill with unreviewed improvisations. Promote a routine only after it has repeatedly earned reuse.

When plain similarity retrieval stops being enough because the knowledge is relational, papers like *HippoRAG* become relevant. That is an escalation rule, not the default. The default is simpler: typed memory layers, explicit write policy, explicit retrieval policy, and deliberate forgetting.

A system that never forgets is not more intelligent. It is less trustworthy.

## Resources And References

*MemGPT* is the frame-setting paper here because it cleanly separates active context from managed external memory. Its real value is architectural: it shifts the conversation from prompt packing to memory movement.

*Generative Agents* matters because it turns memory into a lifecycle. The paper's lasting contribution is showing how raw observations can become higher-order summaries that shape later behavior.

*MemoryBank* is the clearest support for forgetting as hygiene. The decay framing matters less than the practical rule that stale or low-value memory should weaken over time unless something refreshes it.

*Mem0* is the most deployment-shaped paper in this cluster. It is useful because it focuses on extracting and consolidating salient facts instead of saving everything the system ever saw.

*Voyager* earns its place because it treats successful behavior as reusable memory. The embodied setting is secondary. The important move is procedural promotion: once a routine proves itself, the system should stop rediscovering it from scratch.
