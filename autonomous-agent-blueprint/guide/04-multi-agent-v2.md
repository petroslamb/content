# Operating Agents IV: One Agent Is Not Enough

## When To Split, How To Coordinate, What To Keep Single

A research team had a solid internal reporting workflow. One agent could search, read, extract, synthesize, and draft a memo. It was not perfect, but the bottlenecks were understandable: long inputs slowed it down, and it sometimes blurred the line between evidence extraction and synthesis.

The team decided this meant the system needed multiple agents.

They split it into five. Searcher, summarizer, synthesizer, critic, and writer. Every role had a thoughtful prompt. Every role sounded specialized. The pipeline soon became slower, harder to observe, and more difficult to fix. The summarizer's drift flowed into the synthesizer. The critic complained about defects that had entered two steps earlier without making it obvious where they had entered. When output quality fell, the team had to replay a chain of conversations just to understand which handoff had gone soft.

The failure was not that multi-agent systems never work. It was that the system had solved the wrong problem. Multi-agent design does not name one thing. It names at least three very different reasons to split a workflow, and confusing those reasons is how teams create coordination debt faster than they create value.

That is the controlling claim of this chapter: multi-agent systems solve three different problems. They can create role separation, reliability through critique, or task decomposition through artifact handoffs. Those are different architectures with different costs, different controls, and different failure modes.

If you do not know which one you are building, you are probably building theater.

## Problem One: Role Separation

Sometimes the second agent exists because one role should not hold the same tools, permissions, or blast radius as another.

A reviewer should not automatically share the same write permissions as an executor. A planner may need broad read access but no external action. A compliance or approval role may need structural separation because accountability is part of the architecture, not because the system enjoys role-play.

This is the cleanest justification for orchestrator-plus-specialist patterns. The split buys a boundary. It narrows authority and makes it easier to reason about who was allowed to do what.

When teams miss this point, they create several agents with identical permissions and call the resulting sprawl sophistication. Nothing important was separated, so nothing important became safer or easier to review.

## Problem Two: Reliability Through Critique

Sometimes the second agent exists because the first pass needs an independent check.

This is where debate and reviewer patterns can make sense. The right use case is not "the task feels hard." The right use case is that the first judgment is predictably biased, incomplete, or brittle enough that an independent view reduces meaningful error.

This architecture is easy to overuse because critique feels serious. Yet many supposed critic layers are compensating for something cheaper. If a structured self-check or a deterministic verification pass would solve the problem, a full reviewer agent is mostly latency and noise.

Critique is a real pattern. It is just narrower than the marketing around multi-agent systems suggests.

## Problem Three: Task Decomposition Through Artifacts

The third reason to split is the one the field should talk about more. Some workflows really do have stages that deserve different local contexts and different outputs. A planner emits a spec. A retriever emits an evidence packet. An executor works against the spec. A reviewer checks the result against explicit criteria.

The value here is not several personalities. It is that the handoffs can be typed and auditable.

This is why *MetaGPT* is more useful than a great deal of multi-agent rhetoric. Its practical contribution is not that it names many roles. It is that the roles exchange structured artifacts rather than drifting through one sprawling conversation. The same is true of the best reading of *ChatDev*. These systems matter when the workflow has real stages and the outputs of those stages can be judged.

When artifact flow is real, multi-agent structure can be load-bearing. When it is not, the added roles simply create more places for ambiguity to hide.

## Multi-Agent Pattern Map

| Problem you actually have | Good pattern | What the split buys you | Bad substitute |
|---|---|---|---|
| Roles need different tools or permissions | Orchestrator plus specialists | Real blast-radius boundaries | Several agents with identical authority |
| The first pass needs independent review | Critic or reviewer overlay | A second view on a costly failure mode | Debate where verification would do |
| The work moves through distinct artifacts | Typed pipeline | Inspectable stages and clearer failure localization | Free-form handoffs dressed up as roles |
| The task has parallel subproblems with clean separation | Coordinated specialists | Parallelism with bounded interfaces | Committees because the task feels hard |

This table is intentionally narrow. It is meant to make addition harder, not easier.

## Handoffs Are The Architecture

The most important choice in a multi-agent system is not the role names. It is the form of the handoff.

Free-form conversation is seductive because it is natural to prototype. It is also the fastest route to ambiguity. One role passes along a message with mixed state, assumptions, and conclusions. The next role has to infer what matters, what is binding, and what is mere context. By the time the workflow fails, the team can no longer say which boundary actually failed because no boundary was explicit enough to inspect.

Typed artifact handoffs are the stricter alternative. A planner emits a spec. A retriever emits an evidence packet. A reviewer emits a pass-fail record. The receiving role does not have to reconstruct intent from prose. It receives a contract.

That is the architecture. The roles are secondary.

If agents are only passing conversational state, the system is much closer to one large conversation than to a well-decomposed workflow.

## The Human Role Usually Matters More Than The Fifth Agent

Many important multi-agent decisions are really decisions about where the human sits.

Where is approval required? Where is escalation required? Which outputs can move forward without review, and which ones should never do so? In enterprise and policy-sensitive work, these questions often matter more than whether the system has two model roles or five.

A planner-reviewer pair with a human approval gate is often a stronger design than a seven-agent committee because it has a reason to exist. It creates explicit preparation, explicit review, and explicit accountability. Removing the human is not maturity if the risk surface quietly expands and no one owns the consequence.

## The Conservative Default

The default should still be one agent with a clear control loop, clear tools, and clear approval boundaries.

Add a second agent only when you can name the exact boundary it buys you. Different permissions. A real artifact contract. An independent review signal that a self-check cannot supply. If you cannot name the boundary, you are probably adding role theater instead of architecture.

The escalation rule is equally strict. If the single-agent system is failing, do not split it before you know why it is failing. Teams often compensate for weak decomposition, poor retrieval, or vague artifacts by adding more agents. That move usually makes the diagnosis harder.

The second agent should buy you a boundary, not a vibe.

## Resources And References

*MetaGPT* is the most important paper in this cluster because it makes artifact-driven coordination the center of the story. Its real contribution is not the number of roles. It is the insistence that roles exchange structured deliverables rather than drifting through chatter.

*ChatDev* matters because it makes staged collaboration legible in a workflow builders immediately recognize. It is useful as a pipeline example, not as proof that more roles are automatically better.

*AutoGen* belongs here because it made multi-agent conversation programmable and popular. That is both its contribution and its warning. Once coordination webs become cheap to build, overbuilding becomes cheap too.

*RECONCILE* is useful as the cleaner reference for critique and consensus when disagreement itself may add signal. It helps draw the line between real second-pass value and expensive faux collaboration.
