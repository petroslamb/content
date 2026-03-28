# Operating Agents IV: When a Second Agent Earns Its Keep

Multi-agent systems solve three different problems, and most disappointing multi-agent systems are built by confusing them. A second agent might buy you a permission boundary. It might buy you an independent review. It might buy you a typed handoff between genuinely different stages of work. Those are different architectures with different costs, controls, and failure modes.

That distinction matters because teams still talk about multi-agent systems as though they were one upgrade. They are not. A reviewer overlay is not a staged pipeline. A staged pipeline is not a permission split. When those designs get blurred, the system acquires more roles without acquiring a reason.

Once a single-agent workflow has explicit decomposition, grounded reasoning, and verification, the next question is narrower than the field usually admits. What real boundary would a second role buy?

If you do not know the answer, you are probably building theater.

## Architecture One: A Permission Boundary

A second agent does not create free intelligence. It creates another handoff, another state boundary, another evaluation point, and another place where ambiguity can either be reduced or multiplied. That means every extra agent imposes coordination debt. The split only earns its keep if it changes authority in a way that matters.

This is the cleanest reason to separate roles. An executor should not necessarily hold the same permissions as a reviewer. A planner may need broad read access but no write authority. A compliance or approval role may need independence precisely because accountability is the point. In those cases the extra role is not there to sound different. It is there to make the authority structure explicit.

This is also where the human role often matters more than the fifth synthetic specialist. Approval, policy judgment, exception handling, and accountability do not disappear because the workflow has become more elaborate. In many serious systems the human is the boundary the rest of the architecture is trying to protect. A human approver is not an embarrassing leftover from a less autonomous era. In many workflows that role is part of the design's purpose.

If the split does not change who is allowed to do what, it probably is not a permission architecture at all.

## Architecture Two: Independent Critique

Sometimes the first pass is not unsafe because it had the wrong permissions. It is unsafe because it has predictable blind spots.

That is where critique earns its keep. Debate systems and reviewer overlays can help when the first pass regularly misses one class of issue, when the cost of a bad output is high enough to justify another view, or when disagreement itself surfaces a useful error signal. *MAD* and *RECONCILE* matter here because they show that multiple agents can improve reasoning quality when the task truly benefits from structured disagreement and reconciliation (Liang et al.; Chen et al.).

This architecture is narrower than multi-agent marketing suggests. Many teams deploy reviewer agents where a deterministic verification pass would have been cheaper, faster, and easier to govern. Critique is not fake. It is just not the answer to every weak workflow. If the reviewer mostly paraphrases, if latency rises while quality barely moves, or if the disagreement never changes the decision, the system is paying coordination debt for ceremony.

Independent critique is real when the second view changes what evidence gets challenged, what standard gets applied, or what failure becomes visible.

## Architecture Three: Typed Artifact Handoffs

Some workflows really do have stages that deserve different local contexts and different deliverables. A planner writes a spec. A retriever assembles an evidence packet. An executor produces an artifact against that evidence. A reviewer checks the result against explicit criteria.

The value is not that several personalities are talking. The value is that several stages are exchanging typed objects.

That is why handoffs are the architecture. A spec, evidence packet, patch, draft, or pass-fail record can be reviewed, versioned, audited, and rejected. A free-form message that mixes instructions, evidence, assumptions, and tentative conclusions forces the receiving role to reconstruct intent from prose. Once the workflow fails, the team can no longer say where the failure entered because no boundary was explicit enough to inspect.

*MetaGPT* and *ChatDev* matter most where they push multi-agent design toward structured outputs and legible stages rather than toward role-play with better branding (Hong et al.; Qian et al.). The deeper lesson is not about software-team theater. It is about typed artifacts as control surfaces.

## The AutoGen Warning

*AutoGen* made multi-agent conversation much easier to program, which is a real contribution. It lowered the barrier to experimenting with agent interaction patterns, human-in-the-loop turns, and tool-augmented roles (Wu et al.).

It is also a warning. When conversation becomes the primary fabric of coordination, it becomes easy to let free-form exchange substitute for interface design. One role passes a long message that mixes instructions, evidence, assumptions, and tentative conclusions. The next role has to infer what is binding, what is noise, and what counts as task state. By the time the system fails, nobody can localize where the failure entered because the boundary between stages was never explicit enough to inspect.

The teams that succeed with multi-agent systems are usually the ones that treat conversation as a means to an end rather than the architecture itself.

## Keep The Default Single

The deepest practical contribution of the multi-agent literature is not that many roles can talk to each other. It is that boundaries can be made visible.

That is why the default should stay strict. Start with one agent, bounded tools, and a clear control loop. Add a second role only when it buys a permission boundary, an independent check, or a typed handoff that a single-agent workflow cannot provide cleanly.

The escalation rule is strict for the same reason. If the single-agent workflow is failing, diagnose the failure before you split it. Teams often compensate for weak decomposition, poor retrieval, or vague artifacts by adding more agents. That move usually makes the diagnosis harder.

If the split does not buy a real boundary, keep the system single.

The next essay closes the loop on that judgment. Once roles, handoffs, memory, and tools all exist, the question stops being how to coordinate them and becomes how to keep the wrong content from moving through them.

## Resources And References

### [Builder Blueprint: Multi-Agent Design](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/05-multi-agent-design-blueprint.md)

This blueprint turns the essay's three-way split into concrete guidance for when to separate roles, when to add critique, and when typed handoffs justify another agent.

### [Multi-Agent Companion](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/multi-agent/companion.md)

The companion restores the broader multi-agent chapter: topology choices, protocol layers, evaluation framing, and the wider research terrain that sits around the essay's three-problems thesis.

### [MetaGPT: Software Engineers as Multi-Agent Society with LLM-based Agents](https://arxiv.org/abs/2308.00352)

MetaGPT matters because it gives the strongest practical case for multi-agent systems organized around artifacts rather than conversational improvisation.

### [ChatDev: Communicative Agents for Software Development](https://arxiv.org/abs/2307.07924)

ChatDev matters because it shows how role-based collaboration becomes legible when the domain naturally produces staged outputs.

### [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation](https://arxiv.org/abs/2308.08155)

AutoGen matters because it normalized programmable multi-agent conversation and thereby made the coordination problem easier to see.

### [Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate](https://arxiv.org/abs/2305.19118) and [RECONCILE: Round-Table Conference Improves Reasoning via Consensus among Diverse LLMs](https://arxiv.org/abs/2309.13007)

These papers matter because they show the narrow but real class of tasks where structured disagreement improves reliability.
