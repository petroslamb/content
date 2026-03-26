# Multi-Agent Companion

Three systems can all be called multi-agent and almost nothing is clarified by the label. One is a single orchestrator with bounded tools and a human approval gate. One adds an independent reviewer who challenges the first pass. One turns the workflow into a staged artifact pipeline with different local contexts and different deliverables. All three might use several models. They are not variations of one idea. They are different economic claims about where reliability comes from.

That is the useful second-pass way to read multi-agent design. The question is not how many roles appear in the diagram. The question is what boundary the split is buying, what coordination debt it introduces, and whether that debt is worth paying.

The public essay keeps the law narrow and adversarial. This companion owns the surrounding terrain: topology contrast, handoff economics, human placement, and protocol discussion that would have weakened the public chapter if it stayed inside it.

## Three Topologies, Three Different Bets

Start with the simplest contrast.

First, a single-agent orchestrator with bounded tools. It owns the state, produces one reviewable artifact, and hands off to a human only for high-cost decisions. This system bets that simplicity, good tool boundaries, and a clear control loop will beat specialization.

Second, a reviewer overlay. One agent does the work. Another checks the output, challenges claims, or flags risk. This system bets that independent critique will catch enough important error to justify the extra pass.

Third, an artifact pipeline. One role produces a spec or plan, another assembles evidence, another executes against that evidence, another reviews the result. This system bets that typed handoffs and local contexts are worth the coordination cost because the work naturally decomposes.

Those are not stylistic variations. They are different economic claims about where reliability comes from. The field gets this wrong whenever it treats multi-agent as one axis of more capability.

## A Worked Contrast: Orchestrator, Reviewer, Pipeline

Take an internal incident-remediation workflow.

In the single-agent orchestrator version, one agent gathers logs, checks current deployment state, drafts the remediation plan, and produces a structured review packet for a human approver. This is the right baseline when one role can own the state and when the main risk is tool misuse or missing evidence rather than division of labor.

In the reviewer-overlay version, the first agent still does the work, but a second role checks whether the evidence packet is complete, whether live state was actually queried, and whether the proposed fix overreaches. This becomes justified when the first pass has predictable blind spots and the review criteria are explicit.

In the artifact-pipeline version, the planner writes the decision frame, the retriever assembles the evidence packet, the executor drafts the fix against that packet, and the reviewer signs off or rejects with typed reasons. This version earns its keep only when each artifact genuinely narrows ambiguity for the next stage.

The wrong escalation becomes easier to spot once the contrast is explicit. If the baseline system is failing because it never queries live state, adding a reviewer is usually weaker than fixing the control loop. If the baseline system is failing because one stage keeps handing mixed assumptions and evidence to another, an artifact pipeline may help. If the split does not change authority, local context, or artifact quality, it is usually narration with extra cost.

## Handoffs Need Types, Budgets, And Exit Conditions

The practical win in multi-agent design is usually the handoff, not the existence of several thinkers.

A good handoff says what artifact is being transferred, what status it carries, what evidence is attached, what the receiver is allowed to do with it, and what counts as done. A weak handoff is just a long message that mixes instructions, assumptions, context, and provisional conclusions. That is where many role-heavy systems quietly become unreviewable.

Typed handoffs matter more than role names. A spec, evidence packet, patch, exception note, risk flag, or pass-fail record is stronger than a conversational blob because it lets the next stage know what is binding. It also lets a human reconstruct failure later.

There is an economic side to this too. Every handoff needs a budget. If a reviewer role never catches anything important, remove it. If a specialist uses the same tools and emits the same artifact as the orchestrator, collapse it. If a debate loop adds time and no meaningful lift on hard cases, stop calling it architecture.

## Collapse Roles When The Boundary Is Not Real

Multi-agent systems get harder to simplify once the role names start to feel like identity. That is exactly when simplification matters most. A role should survive only if it creates a boundary that shows up in authority, evidence flow, or reviewability. If the planner and orchestrator use the same state, emit the same object, and differ only in narrative posture, the split is decorative. If a reviewer cannot point to a distinct check it performs, the split is decorative. If a specialist exists because the workflow might need more perspectives, the split is decorative until proven otherwise.

This is not a stylistic preference. Collapse discipline is what keeps topology from drifting away from the work. Every unnecessary role adds more transcript, more latency, and more state transfer that someone later has to untangle after a miss. Builders should get comfortable removing agents with the same seriousness they use when adding them. In most production settings, simplification is the most reliable multi-agent optimization available.

The strongest signal here is not role count. It is whether failure review gets shorter after the split. If the answer is still no after several runs, the topology is telling you to collapse, not to elaborate.

## The Human Role Usually Determines Whether The Split Is Real

One of the best conservative instincts in this terrain is to treat the human as part of the topology when judgment, approval, or accountability still matter.

In serious workflows, the human is not outside the system tidying up after the interesting work is over. The human often defines the confidence envelope, resolves ambiguity, approves irreversible action, and decides when a recommendation is allowed to become a decision. If that is true, model it directly. Do not pretend the topology is autonomous and then hide the governing labor in an inbox.

This is another place where the field likes spectacle more than clarity. A five-agent committee that quietly relies on one human to interpret the whole trace is often worse than a simple orchestrator that hands over one clean artifact at the right moment.

## The Field Still Overvalues Conversation

Conversation is useful. It is also one of the weakest coordination substrates in the space.

*AutoGen* mattered because it made programmable multi-agent interaction easy to build. That was a real contribution. It also made it easy to confuse communication fabric with architecture. Once every role can pass long, flexible messages, teams stop feeling the pressure to type artifacts, harden interfaces, or specify what a handoff actually means.

Protocol work matters only after topology discipline. MCP, A2A, and related infrastructure are heading in the right direction because coordination improves when interfaces harden. But a bad split with a cleaner protocol is still a bad split. The anti-pattern is overbuilding the transport layer before the workflow has earned the roles it is trying to connect.

First earn the split. Then harden the wire.

## Analytical References

**[MetaGPT note](../../reference/papers/metagpt.md).** This note is about artifact-driven role collaboration. It is the clearest source for why typed deliverables matter more than conversational theater.

**[ChatDev note](../../reference/papers/chatdev.md).** This note is about staged software-team simulation. It matters less for the theatrical role names than for the artifact-pipeline lesson underneath them.

**[AutoGen note](../../reference/papers/autogen.md).** This note is about programmable multi-agent conversation as a coordination fabric. It is useful as both a capability reference and a warning about transport becoming a substitute for interface design.

**[MAD note](../../reference/papers/mad.md).** This note is about disagreement as a reliability intervention. It belongs in cases where a second role is justified by what gets challenged rather than by broader topology.

**[RECONCILE note](../../reference/papers/reconcile.md).** This note is about structured consensus and confidence-aware reconciliation. It matters when the question is whether disagreement carries real signal or only overhead.

## Sources Behind This Chapter

The core sources behind this chapter are [*MAD*](https://arxiv.org/abs/2305.19118), [*MetaGPT*](https://arxiv.org/abs/2308.00352), [*ChatDev*](https://arxiv.org/abs/2307.07924), and [*AutoGen*](https://arxiv.org/abs/2308.08155). They matter together because they do not defend one thing called multi-agent design. MAD sharpens the critique-overlay case, MetaGPT and ChatDev make artifact pipelines visible, and AutoGen exposes both the power and danger of flexible role conversation.

The adjacent terrain matters because the chapter is really about topology economics rather than role count. *RECONCILE* and related critique-style work widen the question of when disagreement carries real signal. Protocol layers matter because transport eventually affects reliability once the topology is already justified. These sources belong in the companion because they broaden the decision surface without weakening the public law.

The broader picture of the chapter is boundary purchase under coordination debt. The [public essay](./04-multi-agent-v7.md) states the law in its hardest form. The [multi-agent blueprint](../../core/practical-chapter-blueprints/05-multi-agent-design-blueprint.md) turns it into build order and collapse discipline. The paper notes let the interested reader move back into the literature and see how critique, artifact exchange, and transport layers became one conservative doctrine about when a second agent has actually earned its keep.
