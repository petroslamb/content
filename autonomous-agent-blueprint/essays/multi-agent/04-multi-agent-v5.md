# Operating Agents IV: One Agent Is Not Enough

A team built a seven-role committee to handle customer escalation workflow: a planner, a researcher, a writer, a reviewer, an editor, a compliance checker, and a human approver. Each role had an elaborate description. The system produced slow, meandering conversations across roles. Six months in, no one could localize failures. Handoffs were free-form chat. Authority was unclear. Artifacts were not typed. The multi-agent upgrade made the system harder to govern, not more capable.

That is the multi-agent trap. The public story about multi-agent systems is still badly distorted by the way the term is used. It is often presented as a raw capability upgrade, as though several agents naturally imply more intelligence, more creativity, or more autonomy than one. The practical literature says something stricter. A multi-agent system is not one idea. It is an architectural decision to buy a boundary that a single-agent workflow could not provide cleanly.

If you do not know which boundary the extra agent buys you, you are probably building theater.

## Exactly Three Reasons To Split

A second agent does not create free intelligence. It creates another handoff, another state boundary, another evaluation point, and another place where ambiguity can either be reduced or multiplied. That means every extra agent imposes coordination debt. If the handoff is typed and the authority boundary is real, the debt may be worth paying. If the handoff is conversational and the roles are mostly decorative, the system becomes slower, harder to audit, and harder to fix.

The three legitimate reasons to add agents are fundamentally different architectures.

The first is role separation. An executor should not necessarily hold the same permissions as a reviewer. A planner may need broad read access but no write authority. A compliance or approval role may need independence precisely because accountability is the point. In those cases the extra role is not there to sound different. It is there to make the authority structure explicit.

The second is reliability through critique. Debate systems and reviewer overlays can help when the first pass suffers from predictable blind spots, when the cost of a bad output is high enough to justify another view, or when disagreement itself surfaces useful error signals. *MAD* and *RECONCILE* matter here because they show that multiple agents can improve reasoning quality when the task truly benefits from structured disagreement and reconciliation (Liang et al.; Chen et al.).

The third is task decomposition through artifacts. Some workflows really do have stages that deserve different local contexts and different deliverables. A planner writes a spec. A retriever assembles an evidence packet. An executor produces an artifact against that evidence. A reviewer checks the result against explicit criteria. The value is not several personalities talking. The value is several stages exchanging typed objects.

## Handoffs Are The Architecture

The most important choice in a multi-agent system is not the role names. It is the form of the handoff.

A research team learned this after turning one reporting agent into five roles. Searcher, summarizer, synthesizer, critic, and writer all had thoughtful prompts. Median runtime more than doubled. More damaging, postmortems that used to take minutes began consuming half an afternoon because drift could enter at several conversational handoffs before anyone could localize it. The critic often noticed something real, but too late to show where the error had actually entered.

The split had not bought a meaningful boundary. It had bought more narration.

Free-form conversation is seductive because it is natural to prototype. It is also the fastest route to ambiguity. One role passes along a message with mixed state, assumptions, and conclusions. The next role has to infer what matters, what is binding, and what is mere context. By the time the workflow fails, the team can no longer say which boundary actually failed because no boundary was explicit enough to inspect.

Typed artifact handoffs are the stricter alternative. A planner emits a spec. A retriever emits an evidence packet. A reviewer emits a pass-fail record. The receiving role does not have to reconstruct intent from prose. It receives a contract.

That is the architecture. The roles are secondary.

## The AutoGen Warning

*AutoGen* made multi-agent conversation much easier to program, which is a real contribution. It lowered the barrier to experimenting with agent interaction patterns, human-in-the-loop turns, and tool-augmented roles (Wu et al.).

It is also a useful warning. When conversation becomes the primary fabric of coordination, it becomes easy to let free-form exchange substitute for interface design. One role passes a long message that mixes instructions, evidence, assumptions, and tentative conclusions. The next role has to infer what is binding, what is noise, and what counts as task state. By the time the system fails, nobody can localize where the failure entered because the boundary between stages was never explicit enough to inspect.

The teams that succeed with multi-agent systems are usually the ones that treat conversation as a means to an end rather than the architecture itself.

## Multi-Agent Decision Matrix

| Which problem are you solving? | Architecture pattern | Signals you chose wrong |
|---|---|---|
| Role separation | Distinct agents with bounded authority and auditable execution | Roles share the same permissions and the split changes nothing important |
| Reliability through critique | Reviewer, debate, or consensus overlay with explicit disagreement | The reviewer paraphrases, latency rises, and quality barely moves |
| Task decomposition through artifacts | Typed pipeline with specs, evidence packets, drafts, patches, or reports | Handoffs are long free-form messages and failure localization is impossible |

If you cannot map your multi-agent system to one of these patterns, you probably have not bought a boundary. You have bought coordination debt without architectural benefit.

## The Human Role Usually Matters More Than The Fifth Agent

The most important multi-agent design decision is often where the human sits, not how many models are involved.

Approval, policy judgment, exception handling, and accountability do not disappear because the workflow has become more elaborate. In many serious systems the human is the real boundary that keeps critique honest, exceptions reviewable, and irreversible steps accountable. A human approver is not an embarrassing leftover from a less autonomous era. In many workflows that role is part of the architecture's point.

This is one reason typed artifact handoffs matter so much. A human can review a spec, a patch, an evidence packet, or a pass-fail report far more reliably than a drifting conversation between synthetic roles.

## The Boundary Test

The deepest practical contribution of the multi-agent literature is not that many roles can talk to each other. It is that boundaries can be made visible. *MetaGPT* and *ChatDev* matter most where they push multi-agent design toward structured outputs and legible stages rather than toward role-play with better branding (Hong et al.; Qian et al.).

That is why the default should stay strict. Start with one agent, bounded tools, and a clear control loop. Add a second role only when it buys a permission boundary, an independent check, or a typed handoff that a single-agent workflow cannot provide cleanly.

The escalation rule is just as strict. If the single-agent workflow is failing, diagnose the failure before you split it. Teams often compensate for weak decomposition, poor retrieval, or vague artifacts by adding more agents. That move usually makes the diagnosis harder.

If the split does not buy a real boundary, keep the system single.

## Resources And References

### [Builder Blueprint: Multi-Agent Design](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/05-multi-agent-design-blueprint.md)

This blueprint turns the essay's three-way split into concrete guidance for when to separate roles, when to add critique, and when typed handoffs justify another agent.

### [Multi-Agent Companion](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/multi-agent/companion.md)

The companion restores the broader multi-agent chapter: topology choices, protocol layers, evaluation framing, and the wider research terrain that sits around the essay's three-problems thesis.

### [MetaGPT: Software Engineers as Multi-Agent Society with LLM-based Agents](https://arxiv.org/abs/2308.00352) (2024)

MetaGPT matters because it gives the strongest practical case for multi-agent systems organized around artifacts rather than conversational improvisation.

### [ChatDev: Communicative Agents for Software Development](https://arxiv.org/abs/2307.07924) (2023)

ChatDev matters because it shows how role-based collaboration becomes legible when the domain naturally produces staged outputs.

### [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation](https://arxiv.org/abs/2308.08155) (2023)

AutoGen matters because it normalized programmable multi-agent conversation and thereby made the coordination problem easier to see.

### [Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate](https://arxiv.org/abs/2305.19118) (2024) and [RECONCILE: Round-Table Conference Improves Reasoning via Consensus among Diverse LLMs](https://arxiv.org/abs/2309.13007) (2023)

These papers matter because they show the narrow but real class of tasks where structured disagreement improves reliability.
