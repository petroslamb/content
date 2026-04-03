# Safety Companion

Prompt injection is the loudest story in agent safety because it fits on a slide. It is not the only one. A workflow can inherit risk from a poisoned retrieval path, a permissive tool boundary, a stale internal artifact, a memory write that later returns wearing authority, a runtime that changed under the model, or a handoff that quietly converted observation into instruction. The system does not need to become malicious. It only needs to trust the wrong thing at the wrong layer.

That is why safety becomes architectural so quickly once an agent becomes useful. Each new surface is also a new route by which compromised input, stale state, or over-broad authority can turn into consequential behavior.

The public essay keeps the law focused on trust boundaries. This companion owns the broader terrain: environment risk, supply-chain exposure, artifact contamination, and the reliability controls that become safety controls once consequence enters the loop.

## Interfaces Fail First, But Environments Fail Too

The cleanest lesson in this terrain is still that safety failures happen at interfaces. They happen between instructions and untrusted content, between models and tools, between outputs and actions, and between one role and the next. That is the right center of gravity because most meaningful mitigations still come from trust separation, least privilege, controlled ingestion, and reviewable approvals.

But a second-pass reading has to widen the frame. Environments fail too.

A browser tool can inherit a compromised extension, a changed site policy, or a poisoned remote script. A code-execution environment can pull the wrong package version, run against the wrong secret scope, or behave differently after a runtime change the model never sees directly. A retrieval system can degrade because a corpus was poisoned, jammed, or allowed to drift. A memory store can become an attack surface simply by accepting writes that later come back wearing the authority of prior state.

The field still underestimates this because prompt injection remains the most vivid story. It is only one route through the broader problem of unsafe influence moving across a boundary with more authority than it deserves.

## The Supply Chain Is Inside The Safety Model

One reason current safety discussions stay too narrow is that they still talk as though the model were the system and the environment were merely context.

That is not how useful agents work. The environment is part of the control loop. If the workflow browses the web, executes code, installs dependencies, trusts retrieved documents, or calls remote services, then the supply chain and runtime become part of the safety model. A tainted package, stale container, altered browser context, or shifted permission scope can change what the system is actually doing even if the prompt remains unchanged.

This is where the conservative posture matters. Safe agent design is not only about stopping hostile content. It is about bounding execution surfaces, pinning trust where you can, logging enough state to replay what happened, and refusing to treat surrounding infrastructure as neutral.

The anti-pattern is to build a sophisticated prompt-defense story on top of a runtime the team cannot reconstruct after failure.

## Retrieval, Memory, And Artifacts Carry Authority Forward

The essay kept attention on prompt injection, retrieval poisoning, and inter-agent contamination for good reason. The second-pass lesson is that all three are really the same family of error. Untrusted or weakly trusted material gets carried forward as though it were sanctioned state.

That can happen through a retrieved help article. It can happen through a durable memory write. It can happen through a screenshot one agent hands to another. It can happen through a summary that quietly smuggles instructions, overclaims evidence, or freezes stale state into a reusable artifact.

Retrieval and memory belong inside the default safety stack for the same reason. Once the workflow acts on stored knowledge, the store is no longer just a relevance layer. It is a future influence layer. A system that writes to memory and later trusts it without friction has created a persistence mechanism for risk.

The same logic applies to artifacts. Typed handoffs help because they reduce ambiguity. They do not make an artifact trustworthy. Trust has to reset at every transfer.

## Reliability Controls Become Safety Controls

A second-pass reading also clarifies why reasoning controls show up in a safety discussion. Verification is not a substitute for containment. It is still essential because wrong output becomes a safety problem the moment it triggers action, contaminates state, or enters another workflow with borrowed authority.

*Chain-of-Verification* matters in this package for that reason. The paper created a distinct checking phase so the first answer no longer certifies itself. That is a reliability move first. It becomes a safety move whenever the unchecked answer can cause external effects.

This overlap is easy to miss. Builders separate quality and safety in design discussions, then discover in production that a false answer, a stale recommendation, or a fabricated justification can be just as damaging as overtly hostile input if it reaches the action layer.

## What A Serious Safety Posture Looks Like

The posture is conservative because the current gains are still mostly coming from discipline rather than cleverness.

Label trust classes. Keep instructions separate from observations. Split read tools from write tools and low-impact tools from irreversible ones. Pin and inspect execution environments that matter. Treat retrieval inputs and memory writes as integrity-sensitive operations. Reset trust at handoffs. Put deterministic checks and human approval in front of consequential action. Preserve enough logs, versions, and event traces to replay failure after the fact.

That is not glamorous, and it is exactly why it works. Most agent systems are still getting hurt by preventable boundary failures, runtime ambiguity, and misplaced trust long before they need speculative self-healing architecture.

Replayability deserves emphasis because it is where prevention and accountability meet. If a team cannot reconstruct the retrieved document set, tool state, runtime version, permission scope, and approval trail that produced an incident, the system is not merely hard to debug. It is harder to contain.

## Abuse Cases Belong In Predeployment Review

One reason safety work stays abstract is that teams treat red-team style cases as optional stress rather than as design input. They launch the workflow, wait for the first ugly surprise, and then retrofit policy around the incident they happened to see.

A stronger posture is to rehearse abuse before widening autonomy. Seed the retriever with misleading but plausible content. Pass a stale internal artifact through a trusted-looking handoff. Force the tool layer to encounter partial completion, suspicious instructions, or changed execution conditions. Then review the run as though it were real. What channel carried influence. What boundary failed to narrow it. What write path stayed too open. What evidence would have been available to a human responder.

This kind of rehearsal turns safety from principle into architecture. It reveals whether trust classes are specific enough, whether approval actually protects the expensive actions, and whether the system leaves a typed trail strong enough for containment after the fact. A workflow that has never been tested against its own realistic contamination paths is still depending on luck.

It also reveals a harder truth. Some workflows should stay narrow. If abuse rehearsal keeps showing that one retrieval path, browser surface, or inter-agent handoff cannot be contained cleanly, the right answer may be to reduce autonomy rather than add another clever defense. Serious safety doctrine has to leave room for that verdict.

## Analytical References

**[Greshake note](../../reference/papers/greshake_indirect_prompt_injection.md).** This note is about indirect prompt injection through external content. It is the foundational reference when the argument starts with trust separation between instructions and observations.

**[PoisonedRAG note](../../reference/papers/poisonedrag.md).** This note is about retrieval poisoning and knowledge corruption. It matters when the workflow acts on retrieved material and the store itself becomes part of the attack surface.

**[ToolEmu note](../../reference/papers/toolemu.md).** This note is about sandboxed safety evaluation before consequence. It is the right source when the builder needs a reference for abuse rehearsal and predeployment stress testing.

**[Agent Poison note](../../reference/papers/agentpoison.md).** This note is about poisoning durable memory or knowledge bases so later behavior is redirected. It matters when memory policy and safety policy have started to collapse into the same problem.

**[Agent Smith note](../../reference/papers/agentsmith.md).** This note is about cross-agent contamination through multimodal artifacts. It is useful when the handoff itself becomes the propagation surface.

## Sources Behind This Chapter

The core sources behind this chapter are [*Not What You've Signed Up For*](https://arxiv.org/abs/2302.12173), [*PoisonedRAG*](https://arxiv.org/abs/2402.07867), and [*ToolEmu*](https://arxiv.org/abs/2309.15817). They matter together because they redraw safety around movement and consequence. Greshake and colleagues break the old instruction-data trust model, PoisonedRAG makes retrieval integrity part of the attack surface, and ToolEmu moves evaluation in front of deployment.

The wider cluster expands the same theme across different routes of contamination. *InjecAgent*, *Agent Poison*, *BadRAG*, and *Agent Smith* matter because they show how hostile or degraded material can enter through different retrieval, memory, and agent pathways. These sources belong in the companion because they fill out the family resemblance between prompt injection, retrieval poisoning, runtime ambiguity, and artifact contamination that the public essay states in compressed form.

The broader picture of the chapter is that trust boundaries, runtime discipline, and replayability all belong to the same safety argument. The [public essay](05-safety-v7.md) carries the doctrine. The [safety blueprint](../../core/practical-chapter-blueprints/06-safety-blueprint.md) turns it into control design. The paper notes give the interested reader the attack shapes, evaluation details, and boundary logic that sit underneath the chapter's conservative posture.
