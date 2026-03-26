# Operating Agents IV: One Agent Is Not Enough

## When to Split, How to Coordinate, and What to Keep Single

Multi-agent systems solve three different problems, and most disappointing multi-agent systems are built by confusing them. A second agent might buy you a permission boundary. It might buy you an independent review. It might buy you a typed handoff between two genuinely different stages of work. Those are different architectures with different costs, controls, and failure modes.

That distinction matters because teams talk about multi-agent systems as though they were one upgrade. They are not. A reviewer overlay is not a staged pipeline. A staged pipeline is not a permission split. When those designs get blurred, the system acquires more roles without acquiring a reason.

If you do not know which boundary the extra agent buys you, you are probably building theater.

## Problem One: Role Separation

Sometimes the second agent exists because one role should not hold the same tools, permissions, or blast radius as another.

A reviewer should not automatically share the same write permissions as an executor. A planner may need broad read access but no external action. A compliance or approval role may need structural separation because accountability is part of the architecture, not because the system enjoys role-play.

This is the cleanest justification for orchestrator-plus-specialist patterns. The split buys a boundary. It narrows authority and makes it easier to reason about who was allowed to do what.

When teams miss this point, they create several agents with identical permissions and call the resulting sprawl sophistication. Nothing important was separated, so nothing important became safer or easier to review.

## Problem Two: Reliability Through Critique

Sometimes the second agent exists because the first pass needs an independent check.

This is where debate and reviewer patterns can make sense. The right use case is not "the task feels hard." The right use case is that the first judgment is predictably biased, incomplete, or brittle enough that an independent view reduces meaningful error. Work like [*MAD*](https://arxiv.org/abs/2305.19118) and [*RECONCILE*](https://arxiv.org/abs/2309.13007) belongs here, not as proof that many voices are always better, but as evidence that disagreement can sometimes add signal when the task actually justifies it.

This architecture is easy to overuse because critique feels serious. Yet many supposed critic layers are compensating for something cheaper. If a structured self-check or a deterministic verification pass would solve the problem, a full reviewer agent is mostly latency and noise.

Critique is a real pattern. It is just narrower than the marketing around multi-agent systems suggests.

## Problem Three: Task Decomposition Through Artifacts

The third reason to split is the one the field should talk about more. Some workflows really do have stages that deserve different local contexts and different outputs. A planner emits a spec. A retriever emits an evidence packet. An executor works against the spec. A reviewer checks the result against explicit criteria.

The value here is not several personalities. It is that the handoffs can be typed and auditable.

This is why [*MetaGPT*](https://arxiv.org/abs/2308.00352) is more useful than a great deal of multi-agent rhetoric. Its practical contribution is not that it names many roles. It is that the roles exchange structured artifacts rather than drifting through one sprawling conversation. The same is true of the best reading of [*ChatDev*](https://arxiv.org/abs/2307.07924). These systems matter when the workflow has real stages and the outputs of those stages can be judged.

When artifact flow is real, multi-agent structure can be load-bearing. When it is not, the added roles simply create more places for ambiguity to hide.

## Multi-Agent Pattern Map

| Problem you actually have | Good pattern | What the split buys you | Bad substitute |
|---|---|---|---|
| Roles need different tools or permissions | Orchestrator plus specialists | Real blast-radius boundaries | Several agents with identical authority |
| The first pass needs independent review | Critic or reviewer overlay | A second view on a costly failure mode | Debate where verification would do |
| The work moves through distinct artifacts | Typed pipeline | Inspectable stages and clearer failure localization | Free-form handoffs dressed up as roles |
| The task has parallel subproblems with clean separation | Coordinated specialists | Parallelism with bounded interfaces | Committees because the task feels hard |

This table is intentionally narrow. It is meant to make addition harder, not easier.

## Handoffs Are the Architecture

The most important choice in a multi-agent system is not the role names. It is the form of the handoff.

A research team learned this after turning one reporting agent into five roles. Searcher, summarizer, synthesizer, critic, and writer all had thoughtful prompts. Median runtime more than doubled. More damaging, postmortems that used to take minutes began consuming half an afternoon because drift could enter at several conversational handoffs before anyone could localize it. The critic often noticed something real, but too late to show where the error had actually entered.

The split had not bought a meaningful boundary. It had bought more narration.

Free-form conversation is seductive because it is natural to prototype. It is also the fastest route to ambiguity. One role passes along a message with mixed state, assumptions, and conclusions. The next role has to infer what matters, what is binding, and what is mere context. By the time the workflow fails, the team can no longer say which boundary actually failed because no boundary was explicit enough to inspect.

Typed artifact handoffs are the stricter alternative. A planner emits a spec. A retriever emits an evidence packet. A reviewer emits a pass-fail record. The receiving role does not have to reconstruct intent from prose. It receives a contract.

That is the architecture. The roles are secondary.

This is also why [*AutoGen*](https://arxiv.org/abs/2308.08155) is both useful and dangerous in the same breath. It made programmable agent conversation much easier. That lowered the cost of experimentation. It also lowered the cost of overbuilding. Once conversational coordination becomes cheap, it becomes easy to substitute chatter for interface design.

If agents are only passing conversational state, the system is much closer to one large conversation than to a well-decomposed workflow.

## The Human Role Usually Matters More Than the Fifth Agent

Many important multi-agent decisions are really decisions about where the human sits.

Where is approval required? Where is escalation required? Which outputs can move forward without review, and which ones should never do so? In enterprise and policy-sensitive work, these questions often matter more than whether the system has two model roles or five.

A planner-reviewer pair with a human approval gate is often a stronger design than a seven-agent committee because it has a reason to exist. It creates explicit preparation, explicit review, and explicit accountability. Removing the human is not maturity if the risk surface quietly expands and no one owns the consequence.

The architecture checklist in this repo matters here for exactly that reason. A multi-agent workflow should still be able to reconstruct what happened, show what artifact supported the next step, explain who approved a consequential action, and localize where the failure entered the system. If the topology makes those questions harder to answer, the split has probably made the system worse.

The broader multi-agent chapter is wider than the argument made here. It also covers topologies, message types, decision mechanisms, protocol layers, and a fuller human-collaboration frame. Those layers matter once a split is justified. The essay keeps the center on why a split should exist at all, because that is the decision teams most often get wrong.

## The Split Has to Buy a Boundary

The default should still be one agent with a clear control loop, clear tools, and clear approval boundaries.

Add a second agent only when you can name the exact boundary it buys you. Different permissions. A real artifact contract. An independent review signal that a self-check cannot supply. If you cannot name the boundary, you are probably adding role theater instead of architecture.

The escalation rule is equally strict. If the single-agent system is failing, do not split it before you know why it is failing. Teams often compensate for weak decomposition, poor retrieval, or vague artifacts by adding more agents. That move usually makes the diagnosis harder.

If the boundary is not clear enough to name, it is not clear enough to justify.

## Resources And References

### [Builder Blueprint: Multi-Agent Design](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/05-multi-agent-design-blueprint.md)

This blueprint matters because it turns the essay's three-problem split into concrete topology, handoff, and review decisions.

If you want the broader chapter and survey scope behind this essay, use the [companion note](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/multi-agent/companion.md) and the [series coverage map](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/operating-agents-coverage-map.md).

### [MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352) (2023)

*MetaGPT* matters because it makes artifact-driven coordination more important than the mere existence of multiple roles.

### [ChatDev: Communicative Agents for Software Development](https://arxiv.org/abs/2307.07924) (2023)

*ChatDev* matters because it makes staged collaboration legible and shows when artifact-bearing stages can justify a split.

### [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation](https://arxiv.org/abs/2308.08155) (2023)

*AutoGen* matters because it made multi-agent conversation easy to build and therefore made overbuilding easy too.

### [Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate](https://arxiv.org/abs/2305.19118) (2023)

*MAD* matters because it is a clean reference for disagreement as a reliability mechanism rather than as theater.

### [RECONCILE: Round-Table Conference Improves Reasoning via Consensus among Diverse LLMs](https://arxiv.org/abs/2309.13007) (2023)

*RECONCILE* matters because it makes consensus formation explicit and helps distinguish review-oriented multi-agent systems from decorative debate.

### [Architecture Review Checklist](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/implementation/evaluation/architecture-review-checklist.md)

This checklist matters because it provides the practical test for whether a multi-agent split improved clarity, reconstruction, and failure analysis.
