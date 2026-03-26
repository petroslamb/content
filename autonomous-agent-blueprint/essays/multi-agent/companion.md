# Multi-Agent Companion

The fastest way to make an agent system look more advanced is to multiply the number of roles. The fastest way to make it harder to govern is often the same move. That is why multi-agent design keeps attracting theater. A second model, a reviewer persona, a planner, a debate loop, a human approver, and suddenly the trace looks serious. What matters is not how many names appear in the workflow. It is whether the split buys a boundary the single-agent baseline could not provide cleanly.

That boundary can be worth a great deal. It can also cost more than it returns. The useful second-pass reading of multi-agent design is therefore economic before it is architectural. Every extra role adds latency, state transfer, evaluation burden, and another place where ambiguity can accumulate. A split should only survive if it pays for its own coordination debt.

## Three Topologies, Three Very Different Bets

It helps to compare three systems that are often discussed as though they were variants of one idea.

First, a single-agent orchestrator with bounded tools. It owns the state, produces one reviewable artifact, and hands off to a human only for high-cost decisions. This system bets that simplicity, good tool boundaries, and a clear control loop will beat specialization.

Second, a reviewer overlay. One agent does the work. Another checks the output, challenges claims, or flags risk. This system bets that independent critique will catch enough important error to justify the extra pass.

Third, an artifact pipeline. One role produces a plan or spec, another assembles evidence, another executes against that evidence, another reviews the result. This system bets that typed handoffs and local contexts are worth the coordination cost because the work naturally decomposes.

Those are not stylistic variations. They are different economic claims about where reliability comes from. The field gets this wrong whenever it treats "multi-agent" as one axis of more capability.

## A Worked Contrast: Orchestrator, Reviewer, Pipeline

Take an internal policy-exception workflow.

In the single-agent orchestrator version, one agent gathers policy, checks account state, drafts the recommendation, and produces a structured review packet for a human approver. This is the right baseline when one role can own the state and when the main risk is tool misuse or missing evidence rather than division of labor.

In the reviewer-overlay version, the first agent still does the work, but a second role checks whether the policy basis is current, whether the live account state was actually queried, and whether the recommendation overreaches. This becomes justified when the first pass has predictable blind spots and the review criteria are explicit.

In the artifact-pipeline version, the planner writes the decision frame, the retriever assembles the evidence packet, the executor drafts the recommendation against that packet, and the reviewer signs off or rejects with typed reasons. This version earns its keep only when each artifact genuinely narrows ambiguity for the next stage.

The wrong escalation is easy to spot once the contrast is explicit. If the baseline system is failing because it never queries live state, adding a reviewer is usually weaker than fixing the control loop. If the baseline system is failing because one stage keeps handing mixed assumptions and evidence to another, an artifact pipeline may help. If the split does not change authority, local context, or artifact quality, it is usually narration with extra cost.

## Handoffs Need Types, Budgets, And Exit Conditions

The practical win in multi-agent design is usually the handoff, not the existence of several thinkers.

A good handoff says what artifact is being transferred, what status it carries, what evidence is attached, what the receiver is allowed to do with it, and what counts as done. A weak handoff is just a long message that mixes instructions, assumptions, context, and provisional conclusions. That is where many role-heavy systems quietly become unreviewable.

This is why typed handoffs matter more than role names. A spec, evidence packet, patch, exception note, risk flag, or pass-fail record is stronger than a conversational blob because it lets the next stage know what is binding. It also lets a human reconstruct failure later.

There is an economic side to this too. Every handoff needs a budget. If a reviewer role never catches anything important, remove it. If a specialist uses the same tools and emits the same artifact as the orchestrator, collapse it. If a debate loop adds two minutes and no meaningful lift on hard cases, stop calling it architecture.

## The Human Role Usually Determines Whether The Split Is Real

One of the best conservative instincts in this terrain is to treat the human as part of the topology when judgment, approval, or accountability still matter.

In serious workflows, the human is not outside the system tidying up after the interesting work is over. The human often defines the confidence envelope, resolves ambiguity, approves irreversible action, and decides when a recommendation is allowed to become a decision. If that is true, model it directly. Do not pretend the topology is autonomous and then hide the governing labor in an inbox.

This is another place where the field likes spectacle more than clarity. A five-agent committee that quietly relies on one human to interpret the whole trace is often worse than a simple orchestrator that hands over one clean artifact at the right moment.

## The Field Still Overvalues Conversation

Conversation is useful. It is also one of the weakest coordination substrates in the space.

AutoGen mattered because it made programmable multi-agent interaction easy to build. That was a real contribution. It also made it easy to confuse communication fabric with architecture. Once every role can pass long, flexible messages, teams stop feeling the pressure to type artifacts, harden interfaces, or specify what a handoff actually means.

That is why protocol talk only matters after topology discipline. MCP, A2A, and related infrastructure are heading in the right direction because coordination improves when interfaces harden. But a bad split with a cleaner protocol is still a bad split. The anti-pattern is overbuilding the transport layer before the workflow has earned the roles it is trying to connect.

## Resources And References

### [Multi-Agent Essay: Operating Agents IV: One Agent Is Not Enough](../multi-agent/04-multi-agent-v5.md)

Read the essay first for the hard public claim: extra agents only earn their keep when they buy a real boundary.

### [Builder Blueprint: Multi-Agent Design](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/05-multi-agent-design-blueprint.md)

The blueprint is the build-facing guide for topology choice, handoff design, and evaluation. Use it when you need to decide whether to keep one orchestrator, add a reviewer, or move to an artifact pipeline.

### [Foundation Agents: Practical Chapters Guide](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/reference/chapters-guide.md)

The guide is the quickest route to the larger landscape behind the essay. It keeps the focus on task-oriented interaction, explicit deliverables, and human participation rather than agent-society spectacle.

### [MetaGPT: Software Engineers as Multi-Agent Society with LLM-based Agents](https://arxiv.org/abs/2308.00352) (2024)

MetaGPT matters because it gives the clearest artifact-pipeline story in this cluster. The paper was trying to solve software work through staged deliverables rather than unstructured chat. Its architectural move is to make documents and outputs, not conversation volume, carry the workflow.

That should influence builders who are deciding whether a split truly buys decomposition. It should not tempt them to copy visible role names without copying the artifact discipline that made the paper useful.

### [ChatDev: Communicative Agents for Software Development](https://arxiv.org/abs/2307.07924) (2023)

ChatDev matters because it shows another version of staged multi-role collaboration where deliverables remain visible enough to inspect. The paper was solving coordinated software production, but its broader move is to make specialization legible through outputs.

Builders should borrow the emphasis on inspectable deliverables. They should not borrow the topology wholesale when their domain does not naturally produce the same artifacts.

### [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation](https://arxiv.org/abs/2308.08155) (2023)

AutoGen matters because it made conversation-based orchestration programmable. The paper was solving flexibility and reuse in multi-agent interaction. Its important move is infrastructural rather than doctrinal.

That is why it is both useful and dangerous. Builders should let it influence coordination tooling. They should not let its flexibility excuse vague handoffs or decorative role proliferation.

### [Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate](https://arxiv.org/abs/2305.19118) (2024) and [RECONCILE: Round-Table Conference Improves Reasoning via Consensus among Diverse LLMs](https://arxiv.org/abs/2309.13007) (2023)

These papers matter because they isolate one narrow reason to add another role: structured disagreement can improve reliability when disagreement itself carries signal. They were not solving general topology design. They were solving critique under uncertainty.

That should influence teams considering reviewer overlays or debate loops. It should not be generalized into a claim that more voices are usually better.
