# Operating Agents V: Trust Boundaries and Agent Safety

*Part of the Operating Agents series, a builder-first run on how modern agent systems actually work once language leaves the prompt and starts acting inside software.*

#### Video TL;DR

[AI Agent Safety Blueprint](./artifacts/video/AI%20Agent%20Safety%20Blueprint.mp4)

Safety closes the core run because every capability above widens the attack surface. Once content, tools, and internal artifacts can move across the workflow, trust separation stops being a prompt preference and becomes a systems requirement.

![Slide 1: Agent Safety Is System Architecture](./artifacts/slides/Agent%20Safety%20Architecture/slide-001.png)

One support team arrived on a Monday to find twenty-three urgent review tasks created overnight by an internal operations agent. Several carried account excerpts that should never have left the billing system at triage. The agent had not failed in a cinematic way. It had followed an instruction embedded in a help article it retrieved while drafting the escalations.

The article looked routine. It contained copied troubleshooting text, a note that resembled an internal escalation hint, and one line telling the agent to attach account details for faster manual handling. The workflow read the ticket, retrieved the article, wrote an internal task, and handed that task to the next system as though it were trusted internal work. By the time analysts noticed, they were cleaning a queue full of artifacts that looked normal because they had been produced inside the workflow.

Nothing about the model had to break in an exotic way. The system simply trusted the wrong interfaces.

Agent safety is trust-boundary design, not refusal theater.

That framing is the safety distillation taken here from the broader [foundation-agents survey](https://arxiv.org/abs/2504.01990) and tightened in the local [safety blueprint](../../core/practical-chapter-blueprints/06-safety-blueprint.md). The transcript supplies the progression, but the chapter's narrower claim is architectural: once content, memory, artifacts, and tools can move across the workflow, the real safety question is what trust each channel carries and what it is allowed to reach.

![Slide 2: Where Control Can Be Taken](./artifacts/slides/Agent%20Safety%20Architecture/slide-002.png)

## One Hostile Input Can Become A Workflow

The important shift in modern agent safety is that untrusted content no longer stays on the page. It can move.

It can shape retrieval. It can land in memory. It can appear inside an internal artifact. It can influence a tool call. It can arrive at another agent as though it were already trusted because it was produced inside the system. That movement is what makes agent safety different from earlier chatbot safety talk. The issue is not only whether the model says something bad. The issue is what the workflow lets bad content reach.

The decision rule is dull and severe for a reason. Model every channel by what trust it carries and what it can reach.

![Slide 3: The Practical Attack Surface Map](./artifacts/slides/Agent%20Safety%20Architecture/slide-003.png)

That question is better than asking whether the content looked suspicious, whether the prompt sounded careful, or whether the output still felt internally coherent. Safety begins when a system stops inheriting trust by accident.

## Trust Class Beats Prompt Tone

[*Not What You've Signed Up For*](https://arxiv.org/abs/2302.12173) mattered because it attacked the old trust model directly. The paper was not mainly proving that prompt injection exists in principle. The field already suspected that. It showed that once language systems are integrated with outside content and tools, instructions and data can no longer be treated as though they deserve the same trust status.

That changed the operator question from "how do I make the prompt stronger" to "what happens if retrieved or external content can influence the planner at all." Retrieved passages are evidence, not privileged instruction. Help text is observation, not authority. Another component's output is not safe merely because it came from inside the workflow.

If a system cannot preserve those distinctions, it is not relying on safety controls. It is relying on tone and hope.

![Slide 4: The Poisoned Context Window](./artifacts/slides/Agent%20Safety%20Architecture/slide-004.png)

## Tool Scope Is Safety Architecture

Retrieval poisoning gets attention because it is vivid. Over-broad tool scope is just as operationally dangerous.

A tool that can search documentation does not deserve the same reach as a tool that can write to a customer record. A tool that drafts an internal note does not deserve the same reach as one that can send an external message. Read tools, write tools, and destructive tools are different safety categories because they create different consequence categories.

That is why least privilege belongs in the center of agent safety rather than at the edge of it. The workflow should not be asked to maintain moral discipline with the same prompt while holding wildly different forms of authority.

![Slide 5: From Text to Side Effects](./artifacts/slides/Agent%20Safety%20Architecture/slide-005.png)

The trust map has to say what a channel can read, what it can write, and what still requires a deterministic gate or human approval.

```yaml
channel: retrieved_support_article
trust_class: untrusted_content
allowed_tools: ["search_docs", "draft_internal_task"]
write_targets: []
approval_required: true
```

That object matters because it forces the workflow to declare what this channel is allowed to influence. Safety becomes practical when channels carry policy instead of inheriting reach by accident.

![Slide 10: Boundary One, Trust Separation](./artifacts/slides/Agent%20Safety%20Architecture/slide-010.png)

## Retrieval, Memory, And Handoffs Carry Influence Forward

Modern agent writing still treats retrieval and memory as quality layers first and security layers second. Once the system acts on what it retrieves, that order is backwards.

[*PoisonedRAG*](https://arxiv.org/abs/2402.07867) mattered because it showed that a knowledge store should not be treated as neutral substrate. A small amount of poisoned content can distort what the system sees, when it sees it, and how confidently it moves forward. The attack is interesting not because malicious documents exist, but because it collapses the old assumption that retrieval is merely a convenience layer beneath the real intelligence of the agent.

The same skepticism applies to memory writes and internal artifacts. A summary written by one agent can smuggle a poisoned instruction. A screenshot can carry hostile content across roles. A review packet can freeze stale evidence into a form the next stage mistakes for sanctioned state. Structured handoffs reduce ambiguity. They do not create trust.

![Slide 6: The Memory Liability](./artifacts/slides/Agent%20Safety%20Architecture/slide-006.png)

Trust has to reset at every handoff.

![Slide 8: Safety Failures Happen at Interfaces](./artifacts/slides/Agent%20Safety%20Architecture/slide-008.png)

## Rehearse Abuse Before You Widen Autonomy

The last major safety mistake is chronological. Teams wait until after deployment to discover what a tool-using workflow will do badly.

[*ToolEmu*](https://arxiv.org/abs/2309.15817) mattered because it turned that sequence around. The paper's important move was not only sandboxing. It was evaluation before consequence. If a workflow can read untrusted content, invoke tools, and generate side effects, then the architecture should be pressure-tested before autonomy is widened.

That is also where approval belongs. Human approval is not a confession that the system is weak. It is recognition that some actions are expensive enough that accountability has to sit in the architecture itself. Financial actions, destructive writes, external submissions, legal or policy-sensitive moves, and hard-to-reverse operations should not be protected by prompt style alone. They need scoped tools, deterministic checks, and explicit gates.

The escalation rule should stay hard. Widen autonomy only after trust separation, tool scope, handoff skepticism, deterministic checks, and approval are already explicit.

![Slide 9: The Default Safety Blueprint](./artifacts/slides/Agent%20Safety%20Architecture/slide-009.png)

## Narrow The Surface Before You Widen Freedom

The conservative lesson of the chapter is plain. Separate instructions from data. Treat retrieval and memory as integrity-sensitive infrastructure. Split read tools from write tools and low-impact tools from destructive ones. Reset trust at handoffs. Put deterministic checks and human approval in front of consequential action. Stress the workflow before expanding its freedom.

Every extra capability widens the attack surface. Broader tool access, larger corpora, looser handoffs, and more autonomy are not neutral upgrades. They are expansions of what the wrong content can do if the boundaries are weak.

Sometimes the most serious safety move is not a clever defense. It is a narrower default.

![Slide 14: Control Matrix](./artifacts/slides/Agent%20Safety%20Architecture/slide-014.png)

## References

[Advances and Challenges in Foundation Agents: From Brain-Inspired Intelligence to Evolutionary, Collaborative, and Safe Systems](../../advances-and-challenges-in-foundation-agents.md) ([arXiv](https://arxiv.org/abs/2504.01990)) is the source booklet from which this chapter was ultimately distilled. Its key contribution is breadth. It places safety in the larger operating stack of action, memory, reasoning, coordination, and optimization. This essay narrows that wider survey into one practical claim: safety in agent systems is mostly a problem of trust-boundary design.

[Chapter 11 Blueprint: Trust Boundaries and Agent Safety](../../core/practical-chapter-blueprints/06-safety-blueprint.md) is the builder-facing backbone for this chapter. Its key contribution is translating the safety literature into an interface map. It fixes the default controls around trust classes, tool scope, retrieval integrity, handoff skepticism, approval, and adversarial evaluation before autonomy is widened.

[The Architecture of AI Agent Safety transcript](./artifacts/transcript_The%20Architecture%20of%20AI%20Agent%20Safety_full.txt) is the direct narrative source behind this draft. Its key contribution is structural. It gives the essay its flow from the opening failure archetype through trust separation, tool scope, retrieval and memory as integrity-sensitive infrastructure, skeptical handoffs, and the need to rehearse abuse before the system is granted more freedom.

[*Not What You've Signed Up For*](https://arxiv.org/abs/2302.12173) matters because it redrew the trust model for integrated agents. Its key contribution is making the distinction between instructions and data impossible to ignore once external content can influence planning and action. This essay leans on that move to treat retrieved content as evidence rather than authority.

[*PoisonedRAG*](https://arxiv.org/abs/2402.07867) matters because it turns retrieval integrity into part of the attack surface instead of a background relevance concern. Its key contribution is showing that a knowledge store the workflow later trusts is already part of the safety model.

[*ToolEmu*](https://arxiv.org/abs/2309.15817) matters because it moved safety evaluation in front of deployment. Its key contribution is sequencing: pressure-test the actual contamination paths and tool surfaces before widening autonomy.

[*Agent Poison*](https://arxiv.org/abs/2407.12784) matters because it shows how durable memory and knowledge stores can become future influence channels. Its key contribution is reinforcing that memory policy is part of safety policy once poisoned state can survive into later runs.

[*Agent Smith*](https://arxiv.org/abs/2402.08567) matters because it makes cross-agent contamination feel concrete, especially once artifacts and multimodal inputs start moving between roles. Its key contribution is sharpening the rule that trust has to reset at every handoff rather than glide forward automatically.

![Slide 18: Safety Is Architecture](./artifacts/slides/Agent%20Safety%20Architecture/slide-018.png)
