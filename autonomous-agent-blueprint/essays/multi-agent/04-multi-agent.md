# Operating Agents IV: One Agent Is Not Enough

## When To Split, How To Coordinate, What To Keep Single

*Operating Agents IV of VI*

*The opening case in this essay is a composite of common production failures, not a report of one named company.*

---

A research team built a solid single-agent pipeline that could search, read, synthesize, and draft internal reports. The system had one obvious weakness: it slowed down on long inputs and occasionally muddied the boundary between extraction and synthesis. The team diagnosed this as a sign that the system needed multiple agents.

They split it into five. Searcher, summarizer, synthesizer, critic, and writer. Each role had a thoughtful description. Each felt specialized. The pipeline soon became slower, harder to observe, and more difficult to correct. The summarizer's errors flowed into the synthesizer. The critic often complained about defects created two steps earlier, without making it obvious where they had entered. When outputs degraded, the team had to inspect a chain of agent conversations just to understand which handoff had gone soft.

The original bottleneck had not been intelligence. It had been decomposition and state management. The new architecture added coordination cost to a system that had not yet earned it.

This is the flattering mistake that keeps multi-agent design fashionable: more agents look like more intelligence. In many production systems they are not more intelligence. They are workflow decomposition, sometimes justified and often not.

The stricter default is simple. Stay single-agent until a split solves a named problem of trust, routing, or handoff.

---

## Multi-Agent Is Not A Higher Form Of Mind

This point matters because the language around multi-agent systems is often more romantic than the engineering warrants. Teams talk about societies of minds, specialized roles, collaboration, critique, and internal debate. Some of those descriptions are accurate. Many are prettier versions of a more ordinary fact: the system needed clearer boundaries than one overloaded context window could provide.

That does not make multi-agent design fake. It makes it conditional.

The useful question is not "how many agents should this task have?" The useful question is "what exact problem does the second agent solve that the first one should not solve itself?" If the answer is vague, the split is probably cosmetic. If the answer is precise, the split may be load-bearing.

This is why *MetaGPT* remains a useful paper. Its real contribution is not that it named several roles. It is that the roles exchange typed artifacts instead of improvising around a shared chat. That is workflow engineering, not theatrical emergence. It is also why *AutoGen* is both influential and dangerous. It made multi-agent conversation programmable, which is real progress, and it lowered the cost of building coordination webs that teams cannot later reason about.

---

## There Are Only A Few Good Reasons To Split

Once the glamour is stripped away, the durable reasons to use multiple agents become surprisingly few.

The first is trust or permission separation. One part of the system should not hold the same tools, authority, or blast radius as another. A reviewer should not automatically share the same write permissions as an executor. A safety or compliance step may need genuine structural separation. In this case the split protects the system by narrowing what each participant can do.

The second is typed task decomposition. Some workflows really do have stages that deserve different local contexts and different outputs. A planner can emit a specification, an executor can act against it, and a reviewer can test the result against the specification. The value is not multiple personalities. The value is an auditable boundary between stages.

The third is independent critique. Sometimes a second judgment reduces error because the first pass is consistently biased or incomplete. This is where debate and consensus papers matter. The word sometimes matters even more. If the same result could have been achieved with a structured self-check, a full critic layer is overhead pretending to be sophistication.

Those reasons point to different architectures. Permission separation asks for narrow tool scopes and strong boundaries. Task decomposition asks for typed artifacts. Independent critique asks for a review signal strong enough to justify the cost of a second pass. When teams mix these motives without naming them, they often build systems that are confused about why they are multi-agent in the first place.

## Multi-Agent Topology Chooser

| Problem you actually have | Good multi-agent pattern | Why the split is justified | Bad substitute |
|---|---|---|---|
| One role should not hold another role's tools or permissions | Orchestrator plus specialists with narrow scopes | The split enforces blast-radius boundaries | Several agents with identical permissions |
| The work has real staged artifacts with clear boundaries | Typed pipeline | Each stage receives and emits a contract | Free-form handoffs dressed up as roles |
| The first pass needs an independent check | Critic or reviewer overlay | A second view catches errors the first pass misses | Debate for tasks that only need verification |
| The task has parallel subproblems with real separation | Coordinated specialists | The subtasks are separable and observable | Committees created because the task "feels hard" |

This table is deliberately narrow. It is meant to make addition harder, not easier.

---

## Handoffs Are The Architecture

The most important design choice in a multi-agent system is not the names of the roles. It is the form of the handoff.

Free-form conversation between agents is seductive because it feels natural and easy to prototype. It is also the fastest route to ambiguity. One agent produces a message with mixed state, assumptions, and conclusions. The next agent has to infer what matters, what is binding, and what is merely context. Small ambiguities accumulate until the system can no longer be diagnosed without replaying the entire conversation history.

Typed artifact handoffs are the stricter alternative. A planner emits a spec. A retriever emits an evidence packet. A reviewer emits a pass-fail record against explicit criteria. The receiving agent does not have to reconstruct intent from prose. It receives a contract. When something goes wrong, the system can point to the artifact boundary where it went wrong.

This is the heart of the case for papers like *ChatDev* and *MetaGPT*. The insight is not that multiple roles are inherently powerful. The insight is that typed handoffs let decomposition survive contact with real work.

If agents are only passing free-form text, the system is much closer to one sprawling conversation than to a cleanly decomposed workflow.

---

## The Human Boundary Still Matters Most

Many of the most important multi-agent decisions are really human-placement decisions.

Where does approval sit? Where does escalation sit? Which outputs are allowed to move forward without human review, and which ones are not? Those questions often matter more than whether the system has two model roles or five.

For irreversible actions, legal exposure, financial consequences, or external commitments, the correct boundary is often a human gate. That is not a confession of weakness. It is an admission that accountability requirements are part of architecture. A system that cleanly prepares a decision for human approval is often more mature than a system that theatrically removes the human and quietly expands risk.

That is also why a planner-reviewer pair with a human approval step can be a stronger multi-agent design than a seven-agent committee. It has a reason to exist.

---

## The Default And The Escalation Rule

The default should be one agent with a clear control loop, clear tools, and clear approval boundaries.

Add a second agent only when you can name the specific boundary it buys you. Different permissions. A staged artifact contract. An independent review signal that a self-check cannot deliver. If you cannot name the boundary, you are probably adding role theater rather than architecture.

The escalation rule is equally strict. If the single-agent system is failing, do not split it before you know why it is failing. Many teams compensate for weak decomposition, poor retrieval, or unclear artifacts by adding more agents. That move often makes the diagnosis harder. Solve the single-agent ambiguity first. Split only when the remaining bottleneck is genuinely about trust, routing, or handoff.

The second agent should buy you a boundary, not a vibe.

---

## Resources And References

### [Builder Blueprint: Multi-Agent Design](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/05-multi-agent-design-blueprint.md)

For the companion design note, use this public blueprint. It keeps the topology chooser, failure-mode list, build order, and design-pattern summary in a format better suited to implementation review. The essay is there to install the stricter default. The blueprint is there to help a team decide whether a split is justified at all.

### [MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352) (2024)

*MetaGPT* matters because it demonstrates the most important claim in this essay: the value of multi-agent structure often lives in typed artifacts and staged contracts, not in the mere presence of several model roles. In the essay it is the strongest support for the idea that handoff design is the real architecture.

### [ChatDev: Communicative Agents for Software Development](https://arxiv.org/abs/2307.07924) (2023)

*ChatDev* is useful because it shows a role-based pipeline with outputs that are at least more structured than free-form conversational drift. The paper helps make staged decomposition legible in a workflow that builders immediately recognize. In the essay it supports the narrower case for splitting systems when the stages are genuinely distinct and auditable.

### [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation](https://arxiv.org/abs/2308.08155) (2023)

*AutoGen* belongs here because it changed practice by making multi-agent conversation easy to program. That is both its contribution and its warning. In the essay it appears as the paper that lowered the barrier to building coordination webs, which is exactly why it supports the argument that ease of construction can hide serious operating cost.

### [Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate](https://arxiv.org/abs/2305.19118) (2024)

Multi-agent debate matters because it is the clearest example of critique as a specific reliability pattern rather than a default architecture. In the essay it helps separate the case where a second pass adds signal from the much more common case where debate simply adds latency and complexity to a task that needed a better verification step.

### [RECONCILE: Round-Table Conference Improves Reasoning via Consensus among Diverse LLMs](https://arxiv.org/abs/2309.13007) (2023)

*RECONCILE* matters as a refinement of the same critique theme. Its contribution is showing how structured consensus can improve some reasoning tasks, which makes it useful as an escalation reference. In the essay it helps draw the line between genuine disagreement worth paying for and faux collaboration that exists mostly because the system wants to look sophisticated.
