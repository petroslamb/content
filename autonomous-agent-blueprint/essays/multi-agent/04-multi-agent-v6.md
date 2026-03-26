# Operating Agents IV: When a Second Agent Earns Its Keep

A team built a seven-role escalation workflow for customer exceptions: a planner, a researcher, a writer, a reviewer, an editor, a compliance checker, and a human approver. Each role had a careful description. Each handoff was a long conversational message. One role pasted policy excerpts, another rephrased them, another softened the recommendation, another announced that the result looked compliant. Six months in, an escalation went out on superseded policy and no one could localize where the stale clause had entered. The planner and researcher had the same permissions. The reviewer had no typed evidence packet to check. The human approver had to reconstruct the whole run from chat.

The system looked sophisticated. The split bought narration, not architecture.

That is the multi-agent trap. A second agent is not free intelligence. It is a boundary purchase, and the bill arrives as coordination debt.

## Multi-Agent Design Is About Boundary Economics

The public story about multi-agent systems is still badly distorted. "Multi-agent" is often treated as though it were one axis of more capability. More roles, more perspectives, more intelligence. The practical literature says something stricter. A multi-agent system is not one upgrade. It is a choice to buy a boundary that a single-agent workflow could not provide cleanly.

That boundary can be worth a great deal. It can also cost more than it returns. Every extra role adds another handoff, another local context, another evaluation burden, another place where ambiguity can either be reduced or multiplied. If the split does not change authority, evidence flow, or review structure, the system gets more expensive without becoming more legible.

The default should stay severe. Start with one agent, bounded tools, and a clear control loop. Add another role only when the split buys something a single-agent workflow cannot buy as cheaply.

In practice, there are only three reasons that count.

## Boundary One: Permission

Sometimes a second role exists because the system should not let one component both decide and act with the same authority. An executor should not necessarily hold the same permissions as a reviewer. A planner may need broad read access but no write authority. A compliance or approval role may need independence precisely because accountability is the point.

This is the cleanest reason to split roles because it changes what each role is allowed to do. The second agent is not there to sound different. It is there to make the authority structure explicit and narrower. The human role often matters most here. A human approver is not a leftover from a less advanced system. In many serious workflows that role is the boundary the rest of the design is trying to protect.

If the split does not change who is allowed to do what, it probably is not a permission architecture at all.

## Boundary Two: Independent Critique

Other workflows do not fail because one role had too much authority. They fail because the first pass has predictable blind spots and the cost of a miss is high enough to justify another view.

This is where critique earns its keep. Debate and reviewer papers such as [*MAD*](https://arxiv.org/abs/2305.19118) matter because they treat disagreement as a controlled reliability intervention rather than as background noise. The valuable move is not "many voices are better." It is narrower. A second role can challenge an evidence gap, a reasoning shortcut, or a weak recommendation when the task truly benefits from an independent pass.

That architecture is often overused. Many teams add reviewer agents where a deterministic verification stage would have been cheaper, faster, and easier to govern. Critique is real. It is just not the answer to every weak workflow. If the reviewer mostly paraphrases, if latency rises while quality barely moves, or if disagreement never changes the decision, the system is paying coordination debt for ceremony.

Independent critique is justified when the second role changes what gets challenged.

## Boundary Three: Typed Artifact Handoffs

Some tasks really do have stages that deserve different local contexts and different deliverables. A planner writes a spec. A retriever assembles an evidence packet. An executor produces an artifact against that packet. A reviewer checks the result against explicit criteria.

The key point is not that several personalities are talking. The key point is that the stages exchange typed objects.

[*MetaGPT*](https://arxiv.org/abs/2308.00352) mattered for a simple reason. It arrived when multi-agent rhetoric was drifting toward role-play, and its durable contribution was to push the design back toward artifacts, documents, and staged outputs. The same is true of artifact-heavy pipeline work such as [*ChatDev*](https://arxiv.org/abs/2307.07924), though the lesson is narrower than the visible role names suggest. The useful part is not pretending to be a software company. The useful part is that a spec, an evidence packet, a patch, or a pass-fail record gives the next stage something inspectable to receive.

A long conversational message that mixes instructions, evidence, assumptions, and tentative conclusions does the opposite. It forces the receiving role to reconstruct what is binding. Once the workflow fails, no one can say where the error entered because the handoff never became explicit enough to inspect.

Typed handoffs are the architecture. Conversation is only the transport.

## Failure Localization Is The Metric

One of the easiest ways to tell whether a split was justified is to ask what happens after a miss. In a good topology, failure becomes easier to localize. The team can say which role had authority, which artifact carried the error, which review stage missed it, and whether the next role received the right object. In a bad topology, every extra role expands the search space for blame without improving the evidence.

That makes the best single-agent baseline the right control case. If a multi-agent workflow cannot clearly beat one bounded agent with stronger tools, cleaner artifacts, and a sharper verification path, the extra topology is complexity without justification. The wrong score is transcript sophistication. The right score is whether the split bought a boundary and made failure review easier.

## AutoGen Made The Temptation Easier

[*AutoGen*](https://arxiv.org/abs/2308.08155) mattered because it made programmable multi-agent conversation practical. That contribution is real. It lowered the barrier to trying different agent roles, human-in-the-loop turns, and coordination patterns.

It is also one of the best cautionary papers in the space because its strength is also its danger. Once conversation becomes the default coordination fabric, it becomes easy to let flexible messaging substitute for interface design. Stopping conditions blur. Authority boundaries blur. Artifact expectations blur. The transcript grows more interesting while the workflow grows harder to govern.

Protocol cleanliness alone will not save a bad split. A cleaner transport layer over decorative roles is still decorative. Topology discipline has to come first.

## Collapse Decorative Roles Quickly

The conservative rule after deployment should be just as strict as the rule before deployment. If a reviewer never changes the decision, collapse it. If a specialist has the same permissions, the same tools, and the same output contract as the orchestrator, collapse it. If a planning role produces prose that no downstream stage can check against a typed artifact, collapse it. Multi-agent systems become governable partly by being willing to get smaller.

Role count is sticky once teams grow attached to the theater of specialization. A named role starts to feel like a capability even when it is only extra latency. Builders should instead treat every role as guilty until it proves one thing: that removing it would blur authority, weaken critique, or erase a typed handoff the workflow genuinely needs.

The doctrine sentence is plain enough to sound obvious. Extra agents multiply ambiguity unless they create a real boundary. Builders should act as though that sentence is expensive to violate, because it is.

The next chapter closes the loop on that point. Once roles, tools, memory, and handoffs exist, the question is no longer only how to coordinate them. It is how to keep the wrong content from moving through them.
