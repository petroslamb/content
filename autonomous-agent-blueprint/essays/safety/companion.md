# Safety Companion

Agent safety gets described too often as though the main danger were a model saying the wrong thing. That is rarely the operational center once a system becomes useful. The more serious failures begin when a workflow can ingest outside material, store durable state, invoke tools, pull dependencies, call remote services, or hand artifacts to other agents. At that point the question is no longer whether the model can be coaxed into bad text. The question is which boundary will let bad influence travel farthest.

That is why safety work becomes architectural so quickly. Each useful surface also creates a route by which compromised input, stale state, overbroad authority, or runtime drift can turn into consequential behavior. The system does not need to become evil. It only needs to trust the wrong thing at the wrong layer.

## Interfaces Fail First, But Environments Fail Too

The cleanest lesson in this terrain is still that safety failures happen at interfaces. They happen between instructions and untrusted content, between models and tools, between outputs and actions, and between one role and the next. That is the right center of gravity because most meaningful mitigations still come from trust separation, least privilege, controlled ingestion, and reviewable approvals.

But a second-pass reading has to widen the frame. Environments fail too.

A browser tool can inherit a compromised extension, a changed site policy, or a poisoned remote script. A code-execution environment can pull the wrong package version, run against the wrong secret scope, or behave differently after a runtime change the model never sees directly. A retrieval system can degrade because a corpus was poisoned, jammed, or allowed to drift. A memory store can become an attack surface simply by accepting writes that later come back wearing the authority of prior state.

The field still underestimates this because prompt injection remains the most vivid story. It is only one route through the same broader problem: unsafe influence moving across a boundary with more authority than it deserves.

## The Supply Chain Is Inside The Safety Model

One reason current safety discussions stay too narrow is that they still talk as though the model were the system and the environment were merely context.

That is not how useful agents work. The environment is part of the control loop. If the workflow browses the web, executes code, installs dependencies, trusts retrieved documents, or calls remote services, then the supply chain and runtime become part of the safety model. A tainted package, stale container, altered browser context, or shifted permission scope can change what the system is actually doing even if the prompt remains unchanged.

This is where the conservative posture matters. Safe agent design is not only about stopping hostile content. It is about bounding execution surfaces, pinning trust where you can, logging enough state to replay what happened, and refusing to treat surrounding infrastructure as neutral.

The anti-pattern is to build a sophisticated prompt-defense story on top of a runtime the team cannot reconstruct after failure.

## Retrieval, Memory, And Artifacts Carry Authority Forward

The essay kept the attention on prompt injection, retrieval poisoning, and inter-agent contamination for good reason. The second-pass lesson is that all three are really the same family of error: untrusted or weakly trusted material gets carried forward as though it were sanctioned state.

That can happen through a retrieved help article. It can happen through a durable memory write. It can happen through a screenshot one agent hands to another. It can happen through a summary that quietly smuggles instructions, overclaims evidence, or freezes stale state into a reusable artifact.

This is why retrieval and memory belong inside the default safety stack. Once the workflow acts on stored knowledge, the store is no longer just a relevance layer. It is a future influence layer. A system that writes to memory and later trusts it without friction has created a persistence mechanism for risk.

The same logic applies to artifacts. Typed handoffs help because they reduce ambiguity. They do not make an artifact trustworthy. Trust has to reset at every transfer.

## Reliability Controls Become Safety Controls

A second-pass reading also clarifies why reasoning controls show up in a safety discussion. Verification is not a substitute for containment. It is still essential because wrong output becomes a safety problem the moment it triggers action, contaminates state, or enters another workflow with borrowed authority.

Chain-of-Verification matters in this package for that reason. The paper was trying to create a distinct checking phase so the first answer no longer certifies itself. That is a reliability move first. It becomes a safety move whenever the unchecked answer can cause external effects.

This overlap is easy to miss. Builders separate "quality" and "safety" in design discussions, then discover in production that a false answer, a stale recommendation, or a fabricated justification can be just as damaging as overtly hostile input if it reaches the action layer.

## What A Serious Safety Posture Looks Like

The posture is conservative because the current gains are still mostly coming from discipline rather than cleverness.

Label trust classes. Keep instructions separate from observations. Split read tools from write tools and low-impact tools from irreversible ones. Pin and inspect execution environments that matter. Treat retrieval inputs and memory writes as integrity-sensitive operations. Reset trust at handoffs. Put deterministic checks and human approval in front of consequential action. Preserve enough logs, versions, and event traces to replay failure after the fact.

That is not glamorous, and it is exactly why it works. Most agent systems are still getting hurt by preventable boundary failures, runtime ambiguity, and misplaced trust long before they need speculative self-healing architectures.

Replayability deserves emphasis because it is where prevention and accountability meet. If a team cannot reconstruct the retrieved document set, tool state, runtime version, permission scope, and approval trail that produced an incident, the system is not merely hard to debug. It is harder to contain. Safety architecture has to assume that some failures will escape. What matters then is whether the workflow leaves behind enough typed evidence to narrow blast radius and stop the same failure from propagating quietly.

## Resources And References

### [Safety Essay: Operating Agents V: The Attack Surface You Built](../safety/05-safety-v5.md)

Read the essay first for the hard public claim that safety is interface architecture. It keeps the focus on boundary design where most current deployments still fail first.

### [Builder Blueprint: Safety](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/06-safety-blueprint.md)

The blueprint is the build-facing control stack for this terrain: trust separation, tool containment, approval, memory hygiene, inter-agent skepticism, and evaluation. Use it when you need safety design choices rather than a wider conceptual map.

### [Foundation Agents: Practical Chapters Guide](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/reference/chapters-guide.md)

The guide is the quickest route to the larger threat map behind the essay. It keeps the focus on production risks that appear once systems can read, remember, and act through real interfaces.

### [Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) (2023)

This paper matters because it changed the trust model for integrated language systems. It was solving a problem many builders had not named clearly enough yet: outside content can behave like instructions without ever entering the privileged prompt. Its architectural move is severe and durable. External text must stay data, not policy.

That should influence every workflow that mixes browsing, retrieval, or external documents with later action. It should not be reduced to a warning that can be solved with stronger wording in the system prompt.

### [InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents](https://arxiv.org/abs/2403.02691) (2024)

InjecAgent matters because it moves injection from conceptual alarm into tool-using environments. The paper was trying to measure how indirect prompt attacks behave once the system can browse, invoke tools, and affect external state. Its move is evaluative rather than defensive.

That matters because builders need attack surfaces they can test, not just anecdotes they can fear.

### [Identifying the Risks of LM Agents with an LM-Emulated Sandbox](https://arxiv.org/abs/2309.15817) (2024)

ToolEmu matters because it treats testing as part of the safety architecture. The paper was solving the problem of learning about unsafe tool behavior before the live system causes harm. Its key move is to put risky behavior inside an emulated environment where the workflow can be stressed without production fallout.

That should influence sandboxing, pre-deployment evaluation, and runtime discipline. It should not be treated as a replacement for strong boundaries in the live system.

### [AGENT POISON: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases](https://arxiv.org/abs/2407.12784) (2024) and [PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models](https://arxiv.org/abs/2402.07867) (2024)

These papers matter together because they show that stored knowledge is part of the attack surface. They were solving variants of the same problem: future behavior can be steered by contaminating the state the workflow later treats as evidence. Their architectural move is to force retrieval and memory into the security perimeter rather than leaving them in a separate relevance bucket.

That should influence ingestion policy, versioning, curation, and write control. It should not be read as a reason to distrust retrieval in general. The point is to govern it like infrastructure.

### [Agent Smith: A Single Image Can Jailbreak One Million Multimodal LLM Agents Exponentially Fast](https://arxiv.org/abs/2402.08567) (2024)

Agent Smith matters because it widens the contamination story beyond text. The paper was trying to show how one visual artifact can propagate across agents through memory and message exchange. Its deeper lesson is broader than multimodality: artifacts can carry influence across boundaries with more authority than teams expect.

That should influence screenshot handling, inter-agent artifact policy, and trust reset at transfer. It should not be treated as a niche visual-security curiosity.
