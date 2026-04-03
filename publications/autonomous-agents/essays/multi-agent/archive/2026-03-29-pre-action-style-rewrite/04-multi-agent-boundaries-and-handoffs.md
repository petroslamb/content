# Operating Agents IV: Multi-Agent Boundaries and Handoffs

*Part of the Operating Agents series, a builder-first run on how modern agent systems actually work once language leaves the prompt and starts acting inside software.*

#### Video TL;DR

[Blueprint Multi-Agent AI](artifacts/video/Blueprint%20Multi-Agent%20AI.mp4)

The easiest way to romanticize multi-agent systems is to treat them as extra intelligence. More roles, more voices, more perspective, more emergent capability. The transcript for this chapter begins by taking that story apart. Multi-agent design is not about magic emergence. It is about workflow decomposition. A second agent helps only when role separation, structured handoffs, or independent review measurably improve the work. That is the claim carried here from the broader [foundation-agents survey](https://arxiv.org/abs/2504.01990), tightened in the local [multi-agent blueprint](../../core/practical-chapter-blueprints/05-multi-agent-design-blueprint.md), and rebuilt from the transcript's escalation logic rather than from the older archived essay.

![Slide 2: Workflow decomposition over agent theater](artifacts/slides/Multi-Agent%20Design%20Blueprint/slide-002.png)

## The Mistake Is Agent Theater

The transcript names the central failure mode early because it explains most of the confusion in this area. Agent theater is what happens when a team instantiates several roles, gives them impressive names, and mistakes the dashboard for architecture. One model becomes the researcher, another the writer, another the editor. They share the same base capabilities, the same tools, the same permissions, and often the same effective context, but now they talk to each other in loops that look sophisticated in a demo. What changed is narration. What did not change is the actual structure of the work.

That is why the transcript keeps pulling the discussion back toward systems engineering. Every extra role adds a handoff. Every handoff compresses state, introduces ambiguity, consumes tokens, and creates another place where the workflow can fail. If the split does not change authority, evaluation, or artifact quality, the system has become more expensive without becoming more legible. Multi-agent design begins by asking what boundary the split is buying. Without that question, the whole topic collapses into theater.

## Four Questions Before The First Split

The transcript gets concrete very quickly. Before adding another role, the builder has to answer four practical questions. Is one agent enough. If not, what roles should actually be split. How should those roles exchange work. Where does human supervision remain mandatory. Those questions are better than any generic "should we go multi-agent" discussion because they force the architecture back toward permissions, interfaces, and review structure.

![Slide 3: The four workflow questions](artifacts/slides/Multi-Agent%20Design%20Blueprint/slide-003.png)

The first question is still the hardest because it is the least glamorous. One agent remains the correct default when the task can still be owned with bounded tools and a legible control loop. The transcript is severe on this point for good reason. If one agent can still own the task, extra roles are an optimization debt, not a capability win. A split has to be earned by a specific bottleneck.

## Role Separation Means Different Power

The clearest reason to split a role is not stylistic at all. Different parts of the workflow may need different tools, different permissions, or different evaluation logic. The transcript uses a clean example: one component can retrieve sensitive customer or financial data, while another should communicate outward with no access to the underlying records. That is a real boundary. It is not a conversation trick. It is least privilege expressed as workflow design.

![Slide 5: Orchestrator plus specialists](artifacts/slides/Multi-Agent%20Design%20Blueprint/slide-005.png)

This is why the chapter keeps returning to the word bounded. A genuine specialist has a narrower tool set, a narrower authority envelope, a narrower output contract, or a different success condition. A fake specialist is just another instance of the same model with a different costume. If the only distinction between the planner and the reviewer is narrative tone, the split is decorative. If one role can touch the payment gateway and another cannot, the split has finally become architectural.

The human role belongs in this same frame. The transcript does not treat the human as an afterthought standing outside the workflow. It treats the human as a routing node that remains mandatory wherever approval, policy judgment, or interpretation cannot be safely delegated. That is a sober and useful correction. In serious systems, the human is often the most important boundary in the whole topology.

## Handoffs Matter More Than Personalities

Once roles are split, the next question is what they exchange. The transcript is blunt here as well. Free-form chat is weak coordination. Typed artifacts are strong coordination. That is what makes [*MetaGPT*](https://arxiv.org/abs/2308.00352) so useful in this chapter. Its lasting contribution is not role-play. It is the fact that work advances through structured deliverables. A design document hands off to implementation. A requirements artifact permits the next stage to begin. The receiving role gets an object it can inspect, validate, or reject.

[*ChatDev*](https://arxiv.org/abs/2307.07924) reinforces the same lesson from a different angle. Even when the surface presentation looks conversational, the deeper architecture is a staged pipeline. Requirements become development work. Development becomes testing. The important part is not that a CEO role talks to a programmer role. It is that the workflow is sequenced and that the transitions between stages can be made explicit.

![Slide 6: Role-based pipelines](artifacts/slides/Multi-Agent%20Design%20Blueprint/slide-006.png)

The transcript keeps pushing on this because it is one of the few places where multi-agent design becomes more observable rather than less. A typed JSON handoff, a spec, a patch, a test report, an evidence packet, or a pass-fail record gives the next stage something binding to receive. A long natural-language summary does the opposite. It forces the next role to reconstruct what is authoritative and what was merely discussed.

![Slide 9: Typed artifact handoffs](artifacts/slides/Multi-Agent%20Design%20Blueprint/slide-009.png)

That is also where [*AutoGen*](https://arxiv.org/abs/2308.08155) becomes useful as both a capability reference and a warning. AutoGen made multi-agent conversation programmable and practical. It also made it much easier to confuse transport with interface design. Message passing is not the same thing as a good handoff. If the topology depends on endless chat without stop conditions or artifact contracts, the system gets more flexible at exactly the moment it needed to become easier to inspect.

## Reliability Is A Different Problem Than Decomposition

The transcript's literature section reaches its most important synthesis when it separates the reasons people add more than one agent. Some splits exist for role separation. Some exist for task decomposition through artifact handoffs. Others exist for reliability through critique. Those are not the same job, and confusing them is how teams build the wrong topology.

[*MAD*](https://arxiv.org/abs/2305.19118) matters because it turns disagreement into a reliability intervention. The point is not division of labor. It is to force alternative reasoning paths when one model might otherwise anchor on its own first answer. [*RECONCILE*](https://arxiv.org/abs/2309.13007) matters because it structures that disagreement further, making the system manage confidence and consensus rather than letting the participants argue forever.

![Slide 8: Debate and consensus are specialized overlays](artifacts/slides/Multi-Agent%20Design%20Blueprint/slide-008.png)

The transcript is careful not to inflate the importance of these systems beyond their proper scope. Debate belongs late. Consensus belongs later still. If the task really needs an artifact pipeline, a debate loop will not rescue it. If the task merely needs a deterministic verification stage, a critic swarm is overkill. Reliability overlays answer a different failure mode than role separation or staged decomposition, and the builder has to know which problem is actually on the table.

## Multi-Agent Design Is An Escalation Path

This is the section where the transcript becomes most operational. Multi-agent design is an escalation path, never the baseline. The levels are simple and severe. Start with one orchestrator. Escalate to orchestrator plus specialists only when roles truly need different tools or permissions. Escalate again when the work becomes artifact-heavy and sequential enough to justify a pipeline. Add a critic overlay only for high-value outputs where targeted review earns its cost. Reserve debate or consensus groups for hard judgment tasks where disagreement itself carries information.

![Slide 11: The escalation path](artifacts/slides/Multi-Agent%20Design%20Blueprint/slide-011.png)

That ordering matters because it turns multi-agent design into a discipline of constraint. Each new role has to be justified by a failure in the previous level. One agent overloaded with too many tools may justify a specialist. A specialist pattern that still cannot make staged work reviewable may justify a pipeline. A working pipeline that still produces brittle high-value outputs may justify a critic. The field often tells the story in the opposite direction, as if richer topologies were a mark of seriousness. The transcript tells the truer story. A richer topology is a tax that must be earned.

The build order that follows stays just as conservative. Build the single-agent baseline first. Identify failures that are actually role-separable. Split only the roles that need different tools, permissions, or deliverables. Add typed handoff contracts. Integrate humans explicitly where approval and judgment remain necessary. Only then consider overlays for critique or debate. This is less exciting than the industry's favorite diagrams. It is also far closer to what survives contact with production.

![Slide 10: Humans remain first-class nodes](artifacts/slides/Multi-Agent%20Design%20Blueprint/slide-010.png)

## Failure Localization Is The Real Test

The transcript ends in the right place. Multi-agent systems should not be judged by how smart the internal chat sounds. They should be judged by end-task quality, coordination overhead, latency and cost per handoff, and most of all by failure localization. When the output is wrong, how quickly can the team identify the broken node. If the answer is "read thousands of lines of agent conversation and hope," the topology is already telling you it was built on the wrong substrate.

![Slide 13: Evaluate against the single-agent baseline](artifacts/slides/Multi-Agent%20Design%20Blueprint/slide-013.png)

That is why typed handoffs matter so much. A bad JSON artifact localizes a failure. A bad patch localizes a failure. A long conversational drift does not. And that is why the single-agent baseline has to remain in view all the way through the design process. If the multi-agent topology does not clearly beat a strong, tool-bounded single workflow on quality, cost, latency, and debuggability, then it is complexity without justification.

The closing line of the transcript is the one worth keeping. Multi-agent design is not a messy artificial brain. It is conservative workflow decomposition. Start with one agent, add specialists only when the boundary is real, prefer artifacts over chatter, and reserve disagreement for the places where reliability truly demands it.

![Slide 14: Multi-agent is workflow decomposition](artifacts/slides/Multi-Agent%20Design%20Blueprint/slide-014.png)

## References

[Advances and Challenges in Foundation Agents: From Brain-Inspired Intelligence to Evolutionary, Collaborative, and Safe Systems](../../advances-and-challenges-in-foundation-agents.md) ([arXiv](https://arxiv.org/abs/2504.01990)) is the source booklet from which this chapter was ultimately distilled. Its key contribution is scope. It places multi-agent design inside the broader operating stack rather than treating it as an autonomous subfield. This essay narrows that wider survey to one practical question: when should one agent become several, and what must the split buy to justify itself.

[Multi-Agent Design blueprint](../../core/practical-chapter-blueprints/05-multi-agent-design-blueprint.md) is the builder-facing backbone for this chapter. Its key contribution is selection discipline. It separates role separation, reliability-through-critique, and task decomposition into different architectural jobs, then turns those jobs into a conservative escalation path.

[The escalation path for multi agent AI transcript](artifacts/transcript_The%20escalation%20path%20for%20multi%20agent%20AI_full.txt) is the direct structural source behind this draft. Its key contribution is order. It begins by rejecting agent theater, then moves through the four design questions, the literature on artifacts and critique, the five-level escalation matrix, and finally the harsh evaluation rule that every topology must beat a strong single-agent baseline.

[*MetaGPT*](https://arxiv.org/abs/2308.00352) matters because it makes artifact-driven collaboration concrete. Its key contribution is showing that multi-agent work becomes far more legible once roles exchange structured deliverables instead of relying on loose conversation as the default substrate.

[*ChatDev*](https://arxiv.org/abs/2307.07924) matters because it pushes the same lesson through staged workflow structure. Its key contribution is treating role-based collaboration as a sequenced pipeline rather than as an open-ended group chat, which makes it a useful reference for tasks that naturally decompose into stages.

[*AutoGen*](https://arxiv.org/abs/2308.08155) matters because it made multi-agent conversation programmable and widely accessible. Its key contribution is flexible coordination. The reason it matters in this chapter is that its flexibility also exposes the risk of overbuilding conversation loops where typed interfaces would have been stronger.

[*MAD*](https://arxiv.org/abs/2305.19118) matters because it frames disagreement as a reliability overlay rather than as a general system architecture. Its key contribution is surfacing alternative reasoning paths when a single model would otherwise anchor too hard on its own first answer.

[*RECONCILE*](https://arxiv.org/abs/2309.13007) matters because it pushes debate toward a more explicit decision process. Its key contribution is making disagreement structured and confidence-aware, which is useful when consensus itself needs to be governed rather than improvised.
