# Operating Agents IV: One Agent Is Not Enough

A team built a seven-agent committee to handle customer escalation workflow: a planner, a researcher, a writer, a reviewer, an editor, a compliance checker, and a human approver. Each role had an elaborate description. The system produced slow, meandering conversations across roles. Six months in, no one could localize failures—handoffs were free-form chat, authority was unclear, artifacts were not typed. The "multi-agent upgrade" made the system harder to govern, not more capable. The extra roles added narration, not architecture.

That is the multi-agent trap. The public story about multi-agent systems is still badly distorted by the way the term is used. It is often presented as a raw capability upgrade, as though several agents naturally imply more intelligence, more creativity, or more autonomy than one. The practical literature says something stricter. A multi-agent system is not one idea. It is an architectural decision to buy a boundary that a single-agent workflow could not provide cleanly. Sometimes that boundary is about permissions. Sometimes it is about critique. Sometimes it is about moving work through typed artifacts and distinct local contexts. Those are different problems, and they lead to different systems. Most disappointing multi-agent workflows are built by confusing them.

This is why the blueprint's three-way split is so important. Role separation is one problem. Reliability through critique is another. Task decomposition through artifact handoffs is a third. If a team says it is building a multi-agent system but cannot say which of those problems the second agent is solving, it is usually building theater. The system may still be elaborate. It may still produce long transcripts full of specialized roles. But added narration is not added architecture. The extra role only matters if it changes authority, evidence flow, or review.

## Companion Note

This essay presents a focused narrative for a broad audience. For the full technical scope—including what this essay intentionally leaves out, how it maps to the chapter blueprint, and recommended deeper reading—see the [companion note](companion.md).

## Exactly Three Reasons to Add an Agent

A second agent does not create free intelligence. It creates another handoff, another state boundary, another evaluation point, and another place where ambiguity can either be reduced or multiplied. That means every extra agent imposes **coordination debt**. If the handoff is typed and the authority boundary is real, the debt may be worth paying. If the handoff is conversational and the roles are mostly decorative, the system becomes slower, harder to audit, and harder to fix.

The three legitimate reasons to add agents are fundamentally different architectures.

### 1. Role Separation (Different Permissions)

An executor should not necessarily hold the same permissions as a reviewer. A planner may need broad read access but no write authority. A compliance or approval role may need independence precisely because accountability is the point.

In those cases the second agent is not there to sound different. It is there to make the system's authority structure explicit. That is a genuine engineering reason to split. The split narrows blast radius, clarifies who was allowed to do what, and can make audits much easier to run after a failure.

### 2. Reliability Through Critique

Debate systems and reviewer overlays can help when the first pass suffers from predictable blind spots, when the cost of a bad output is high enough to justify another view, or when disagreement itself surfaces useful error signals. Papers like [*MAD*](https://arxiv.org/abs/2305.19118) and [*RECONCILE*](https://arxiv.org/abs/2309.13007) matter because they show that multiple agents can improve reasoning quality when the task truly benefits from structured disagreement and reconciliation.

But the fact that critique can help does not mean it should become the default answer to weak performance. Many teams deploy reviewer agents where a deterministic verification pass would have been cheaper, faster, and easier to govern. Critique is real. It is just narrower than the field's marketing around multi-agent systems suggests.

### 3. Task Decomposition Through Artifacts

Some tasks really do have stages that deserve different local contexts and different deliverables. A planner writes a spec. A retriever assembles an evidence packet. An executor produces an artifact against that evidence. A reviewer checks the result against explicit criteria.

The key point is not that different agents are talking. The key point is that different stages are exchanging **typed objects**. [*MetaGPT*](https://arxiv.org/abs/2308.00352) and [*ChatDev*](https://arxiv.org/abs/2307.07924) matter because they push multi-agent design toward that artifact-bearing model rather than toward one sprawling conversation. The moment the workflow is organized around plans, drafts, patches, evidence packets, or pass-fail reports, handoffs become legible and failure localization improves sharply.

## The AutoGen Cautionary Tale

[*AutoGen*](https://arxiv.org/abs/2308.08155) made multi-agent conversation much easier to program, which is a real contribution. It lowered the barrier to experimenting with agent interaction patterns, human-in-the-loop turns, and tool-augmented roles.

But that flexibility is also why AutoGen is such a useful cautionary reference. When conversation becomes the primary fabric of coordination, it becomes easy to let free-form exchange substitute for interface design. One role passes a long message that mixes instructions, evidence, assumptions, and tentative conclusions. The next role has to infer what is binding, what is noise, and what counts as the task state. By the time the system fails, nobody can localize where the failure entered because the boundary between stages was never explicit enough to inspect.

Conversation-centric frameworks lower the barrier to experiment at the cost of clarity. The teams that succeed with multi-agent systems are the ones that treat conversation as a means to an end, not as the architecture itself.

## Practically Speaking: Multi-Agent Decision Matrix

| Which problem are you solving? | Architecture pattern | Signals you've chosen wrong |
|-------------------------------|---------------------|-----------------------------|
| Role separation (different permissions/authorities) | Distinct agents with bounded authority sets, auditable execution logs | Roles have same permissions; handoffs are informal; cannot tell who was allowed to do what |
| Reliability through critique (independent review) | Debate (MAD) or consensus (RECONCILE) with structured disagreement and reconciliation | Reviewer just paraphrases; disagreement is noise not signal; latency increases without quality gain |
| Task decomposition through artifacts (staged handoffs) | Typed artifact pipeline (spec → evidence → draft → review) with schemas | Handoffs are long free-form messages; no clear artifact types; failure localization impossible |

**Rule:** If you cannot map your multi-agent system to one of these three patterns, you have probably not bought a boundary. You have bought coordination debt without architectural benefit.

## Escalation Spine

**Default:** One agent with bounded tools and a clear control loop. The vast majority of workflows should start here. If the task can be owned by a single agent with a well-defined action surface, memory policy, and verification stage, that is simpler, more debuggable, and more auditable than any multi-agent alternative.

**Add a second agent only when** one of the three boundary problems is real:
- **Role separation:** different agents need different permissions or accountability chains
- **Reliability through critique:** the task has predictable blind spots and the cost of error justifies a second view with structured disagreement
- **Artifact decomposition:** the work naturally moves through stages that produce distinct deliverables requiring separate contexts

**Prefer typed artifact handoffs over free-form chat.** Every handoff should have a schema. Every agent should produce outputs that are machine-readable, reviewable, and versionable. Free-form conversation between agents dramatically increases coordination debt.

**Keep the human in the architecture** wherever approval, policy judgment, or accountability require it. The most important multi-agent design decision is often where the human sits, not how many models are involved.

## What to Skip (For Now)

**Out of scope for the practical center:**

- **Agent societies and open-ended multi-agent ecosystems.** These are research curiosities or toy demonstrations. They do not solve a concrete boundary problem.
- **Free-form debate as a default capability upgrade.** Debate is expensive. Use it only when disagreement itself carries signal and the task justifies the latency.
- **Inter-agent communication protocols before topology.** A bad split with a cleaner protocol is still a bad split. Architecture comes first, infrastructure second.
- **Multi-agent as a general intelligence multiplier.** Adding agents does not add intelligence. It adds boundaries, handoffs, and coordination cost. If your justification is "more agents = more capability," you are likely building theater.
- **Complex role hierarchies without clear artifact flows.** If your seven-agent system cannot explain what typed object each role produces and consumes, you have overcomplicated the simplest solution.

**If you find yourself adding agents, ask:** What boundary does this split buy? Can I point to the specific problem a single-agent workflow cannot solve cleanly? What typed artifact crosses the handoff? Could a verification stage or a better tool specification solve this without adding a role?

## Resources And References

### [Builder Blueprint: Multi-Agent Design](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/05-multi-agent-design-blueprint.md)

This blueprint matters because it turns the essay's three-way split into concrete guidance for when to separate roles, when to add critique, and when typed artifact handoffs justify another agent.

### [MetaGPT: Software Engineers as Multi-Agent Society with LLM-based Agents](https://arxiv.org/abs/2308.00352) (2024)

MetaGPT matters because it gives the strongest practical argument for multi-agent systems that are organized around artifacts rather than around conversational improvisation. Its core contribution is not merely that it names multiple roles. It is that those roles exchange structured outputs within a workflow that resembles an engineered production process. That makes the system much more useful as an architecture reference than looser "agent society" examples (Hong et al.)

It is also a useful warning. MetaGPT is easy to imitate superficially. A team can copy role names and still miss the actual point, which is that the roles should exist because they carry different responsibilities, contexts, and deliverables. The paper matters precisely because it makes that distinction harder to ignore.

### [ChatDev: Communicative Agents for Software Development](https://arxiv.org/abs/2307.07924) (2023)

ChatDev matters because it shows how role-based collaboration can be made legible within a domain that naturally produces artifacts. Software work, like some research and documentation work, already has stages that generate drafts, code, tests, and revisions. The paper is therefore valuable not because every team should simulate a software company, but because it demonstrates how staged outputs can constrain coordination in a useful way (Qian et al.)

Its limitation is domain shape. A workflow that copies the visible form of ChatDev without sharing the same artifact-bearing structure will likely drift into role theater. That is why the paper is most useful when treated as a model for explicit deliverables and less useful when treated as a license to multiply personas.

### [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation](https://arxiv.org/abs/2308.08155) (2023)

AutoGen matters because it normalized programmable multi-agent conversation as a practical design surface. It made it easier to combine agents, humans, and tools in flexible message loops. That contribution is real. It opened a path for rapid experimentation and helped demonstrate how many coordination patterns can be built once the conversation layer becomes configurable (Wu et al.)

At the same time, it is one of the best cautionary papers in the chapter because its strength is also its danger. Flexible conversation is not the same thing as sound decomposition. When stopping conditions, artifact expectations, and authority boundaries are vague, the conversation fabric becomes a place where ambiguity compounds rather than a place where work is clarified.

### [Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate](https://arxiv.org/abs/2305.19118) (2024)

MAD matters because it makes disagreement concrete enough to evaluate. It is valuable not as a general proof that many voices are always better, but as a demonstration that reliability can improve when alternative views are structured, challenged, and reconciled deliberately (Liang et al.)

Its lesson is narrower than the broader multi-agent hype suggests. Debate is an expensive overlay. It belongs where error reduction is worth the cost and where disagreement actually carries signal. Used casually, it becomes latency with good branding. Used carefully, it shows when a second view genuinely improves judgment.

### [RECONCILE: Round-Table Conference Improves Reasoning via Consensus among Diverse LLMs](https://arxiv.org/abs/2309.13007) (2023)

RECONCILE matters because it shows how consensus can be structured and evaluated. It treats multi-agent reasoning as a process of converging on an answer through explicit discussion and revision, rather than as an aggregation of independent votes. That approach can reduce error when the task benefits from multiple perspectives that must be synthesized (Chen et al.)

Like MAD, its value is conditional. It is a technique for specific failure shapes, not a default architecture for all multi-agent systems.
