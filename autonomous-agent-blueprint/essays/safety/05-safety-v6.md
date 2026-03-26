# Operating Agents V: The Attack Surface You Built

One support team arrived on a Monday to find twenty-three "urgent specialist review" tasks created overnight by an internal operations agent. Several carried account excerpts that should never have left the billing system at triage. The agent had not failed in a cinematic way. It had followed a poisoned instruction embedded in a help article it retrieved while drafting the escalations.

The article looked routine. It contained copied troubleshooting text, a note that resembled an internal escalation hint, and one line telling the agent to attach account details for faster manual handling. The agent read the ticket, retrieved the article, wrote an internal task, and handed that task to the next system as though it were trusted internal work. By the time analysts noticed, they were cleaning a queue full of artifacts that looked normal because they had been produced inside the workflow.

Nothing about the model had to break in an exotic way. The system simply trusted the wrong interfaces.

That is where the safety problem starts. Once an agent can read, remember, hand off, and act, safety stops being a prompt-writing problem and becomes a trust-boundary problem.

## One Hostile Input Can Become A Workflow

The important shift in modern agent safety is that untrusted content no longer stays on the page. It can move.

It can shape retrieval. It can land in memory. It can appear inside an internal artifact. It can influence a tool call. It can arrive at another agent as though it were already trusted because it was produced "inside the system." That movement is what makes agent safety different from earlier chatbot safety talk. The issue is not only whether the model says something bad. The issue is what the workflow lets bad content reach.

The first useful safety question is therefore dull and severe. What does this channel reach. That question is better than asking whether the content looked suspicious, whether the model had a careful prompt, or whether the output still sounded internally coherent.

## Greshake Changed The Trust Model

[*Not What You've Signed Up For*](https://arxiv.org/abs/2302.12173) mattered because it attacked the old trust model directly. The paper was not mainly proving that prompt injection exists in principle. The field already suspected that. It showed that once language systems are integrated with outside content and tools, instructions and data can no longer be treated as though they deserve the same trust status.

That changed the operator question from "how do I make the prompt stronger" to "what happens if retrieved or external content can influence the planner at all." It is a simple shift, but it redraws the architecture. Retrieved passages are evidence, not privileged instruction. Help text is observation, not authority. Another component's output is not safe merely because it came from inside the workflow.

If a system cannot preserve those distinctions, it is not relying on safety controls. It is relying on hope.

## Retrieval Is Integrity Infrastructure

Modern agent writing often treats retrieval and memory as quality layers first and security layers second. Once the system acts on what it retrieves, that order is backwards.

[*PoisonedRAG*](https://arxiv.org/abs/2402.07867) mattered because it showed that a knowledge store should not be treated as neutral substrate. A small amount of poisoned content can distort what the system sees, when it sees it, and how confidently it moves forward. The attack is not interesting because it proves the existence of malicious documents. It is interesting because it collapses the old assumption that retrieval is merely a convenience layer beneath the "real" intelligence of the agent.

For that reason, retrieval and memory belong inside the integrity model. Provenance, curation, freshness, versioning, correction paths, anomaly review, and controlled write policy are not just quality improvements. They are part of the trust boundary. A system should not be able to write casually into a store and later trust that same store as though nothing happened in between.

The same skepticism applies to internal artifacts and inter-agent handoffs. Structured handoffs reduce ambiguity. They do not create trust.

## Handoffs Need Trust Reset

One of the quietest safety mistakes in agent systems is to let internal artifacts inherit authority simply because they were produced inside the workflow. A summary written by one agent can smuggle a poisoned instruction. A screenshot can carry hostile content across roles. A review packet can freeze stale evidence into a form the next stage mistakes for sanctioned state.

Trust therefore has to reset at every handoff. The question is not "did another component produce this." The question is "what evidence supports this object, what is this channel allowed to influence, and what should the receiver still distrust." Typed handoffs help because they expose structure. They do not remove the need for skepticism.

## ToolEmu Put Safety Before Deployment

The last safety mistake is chronological. Teams wait until after deployment to discover what a tool-using system will do badly.

[*ToolEmu*](https://arxiv.org/abs/2309.15817) mattered because it turned that sequence around. The paper's important move was not only sandboxing. It was evaluation before consequence. If a workflow can read untrusted content, invoke tools, and generate side effects, then the architecture should be pressure-tested before autonomy is widened.

This is also where approval belongs. Human approval is not a confession that the system is weak. It is a recognition that some actions are expensive enough that accountability has to sit in the architecture itself. Financial actions, destructive writes, external submissions, legal or policy-sensitive moves, and hard-to-reverse operations should not be protected by prompt tone alone. They need deterministic checks, scoped tools, and approval boundaries.

A safety posture that cannot say where approval sits is not finished.

## Predeployment Tests Should Be Adversarial

The right safety rehearsal is not a polite benchmark pass. It is an abuse-case pass against the actual channels the workflow exposes. Feed the retriever poisoned but plausible documents. Insert misleading instructions into help text. Simulate stale internal artifacts that look sanctioned. Test what happens when one role hands another a structured object with the wrong evidence attached. Then ask what the workflow allowed that content to reach.

That style of rehearsal does not replace containment. It sharpens it. A team learns which trust classes are too broad, which write paths are still too open, which approval points are missing, and which logs are too weak to reconstruct failure after the fact. If a workflow has never been tested against the kind of contamination chain it is architecturally capable of carrying, the deployment is still relying on optimism.

The point of those rehearsals is not to stage a dramatic demo. It is to prove that the workflow fails in bounded ways. A safe system still gets pressured. It just refuses to let pressure jump channels without leaving a trail or policy decision.

```yaml
channel: retrieved_support_article
trust_class: untrusted_content
allowed_tools: ["search_docs", "draft_internal_task"]
write_targets: []
approval_required: true
```

That object is useful because it forces the workflow to declare what this channel is allowed to influence. Safety becomes practical when channels carry policy instead of inheriting trust by accident.

## Build Boundaries Before You Widen Autonomy

The doctrine here is plain. Separate instructions from data. Treat retrieval and memory as integrity-sensitive infrastructure. Scope tools by least privilege. Reset trust at handoffs. Put deterministic checks and human approval in front of consequential action. Stress the workflow before expanding its freedom.

Every extra capability widens the attack surface. Broader tool access, larger corpora, looser handoffs, and more autonomy are not neutral upgrades. They are expansions of what the wrong content can do if the boundaries are weak.

If you widen autonomy before you narrow interfaces, you are building the attack surface first.

The bonus post that follows only becomes useful after these boundaries are legible. Optimization without trust architecture is just a faster way to drift.
