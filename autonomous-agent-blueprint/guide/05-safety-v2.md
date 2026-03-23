# Operating Agents V: The Attack Surface You Built

## Safety As Interface Architecture

An internal operations agent could read support tickets, search company documentation, summarize account history, draft follow-up tasks, and escalate billing issues into a work queue that other tools and analysts trusted. The team behind it considered the system careful. They wrote strong instructions, told it to ignore hostile requests, and added post-launch monitoring.

Then a ticket arrived that looked ordinary. It contained a customer complaint, a copied support thread, and a link to a knowledge article the agent had seen before. The retrieved article had been quietly poisoned. Buried inside an otherwise plausible block of text was a malicious instruction telling the agent to escalate the issue with a high-priority template and attach account details for "faster specialist review."

The agent read the ticket, retrieved the poisoned note, created the internal task, and passed the contaminated artifact into the next system. Nothing about the model had to break in an exotic way. The system simply trusted the wrong interface at three different points: content ingestion, retrieval, and internal handoff.

That is the practical safety problem. The same capabilities that make an agent useful also create its attack surface. Safety is not primarily about whether the prompt sounds careful. It is about whether the system treats content, memory, tools, handoffs, and approvals as distinct trust boundaries.

This is why agent safety stops being a compliance appendix the moment the system can read from the outside world and do something consequential with what it reads.

## One Hostile Input Can Become A Workflow

The most important safety shift in modern agents is that untrusted content no longer stays on the page. It can move.

A malicious instruction can sit inside a web page, an email, a shared note, a product review, a doctor review, a support ticket, or a retrieved document. The model ingests it. The retrieval layer strengthens it by surfacing related material. The memory layer may preserve it. A tool call turns it into a side effect. A handoff turns it into someone else's trusted artifact.

That chain is what papers like Greshake et al., *InjecAgent*, and *PoisonedRAG* make impossible to ignore. The line between data and instructions is no longer naturally preserved by the system. If the architecture does not enforce that separation, the agent will blur it for you.

This is also why the safety question is duller and more concrete than much of the field wants it to be. What does the system ingest? What trust status does each channel carry? Which tools are reachable from that channel? What durable state can be written? Which outputs can become actions without review? Those are architecture questions, not prompt style questions.

## The Wrong Default Is Prompt-Centric Safety

It is worth being blunt here because too much agent writing still dances around the point. A careful system prompt is useful. It is not a safety architecture.

It does not narrow tool scope. It does not stop poisoned retrieval from shaping reasoning. It does not stop a memory write from preserving a bad lesson. It does not create a trust reset between one agent and another. It does not place approval between a plausible draft and a costly external action.

Prompt-centric safety flatters the builder because the system sounds careful. In live systems, safety should not depend primarily on whether the model sounds careful. It should depend on whether the system structurally limits what a mistaken, manipulated, or compromised agent can do.

## Attack Surface To First Control Map

| Attack surface | Typical failure | First control |
|---|---|---|
| Retrieved or external content | Indirect prompt injection | Trust separation between instructions and untrusted content |
| Tool access | Real-world side effects from bad instructions | Least-privilege scopes and explicit authorization |
| Knowledge store and retrieval | Poisoned or stale evidence drives behavior | Provenance, ingestion checks, and freshness rules |
| Long-term memory | Corrupted lessons persist across sessions | Memory write policy and correction paths |
| Inter-agent artifacts | One bad output contaminates the rest | Typed handoffs plus trust resets |
| Consequential actions | A model acts before review should occur | Deterministic checks and human approval |

The goal of this table is not completeness. It is attachment. Safety work should be attached to the surface that can fail.

## Retrieval And Memory Are Security Infrastructure

Modern agent writing often treats retrieval and memory as quality layers first and security layers second. That order is backwards once the system acts on what it retrieves.

*PoisonedRAG* shows why the knowledge store cannot be treated as neutral substrate. A small amount of malicious content can steer retrieval and downstream answers. *BadRAG* and jamming-style work widen the lesson: the attacker does not always need to insert false facts. It can be enough to distort which facts the agent sees or does not see.

The same logic extends to long-term memory. If the system writes lessons, preferences, summaries, or decisions into durable state, that durable state becomes part of the operating environment for future runs. Memory is now both capability and liability. A poisoned memory write is not just one bad answer. It is future influence.

That is why retrieval sources and memory stores should be treated as monitored infrastructure rather than convenience layers. Version them. Curate them. Track provenance. Give them correction paths. Do not let the same system write to a store and later trust that store without any control surface in between.

## Inter-Agent Messages Are Not Safe Because They Are Internal

One of the easiest mistakes in multi-agent systems is to treat internal artifacts as trusted simply because they came from another agent in the same larger workflow.

This is exactly the mistake that papers like *Agent Smith* make harder to dismiss. Once agents exchange screenshots, files, summaries, or image-derived memory, contamination can travel through the same pathways legitimate coordination uses. The multimodal case is dramatic, but the architectural lesson is broader. Another agent's output is not a system instruction by virtue of being internal.

Structured handoffs help because they reduce ambiguity. They do not create trust by themselves. If a planner emits an artifact that exceeds the receiver's authority, the receiver should still reject it. If an attachment contains instructions, the system should still treat it as untrusted content. If a screenshot or page summary enters a shared memory layer, the trust boundary should still reset at the next step.

Multi-agent safety is not several agents being careful together. It is whether the handoff layer is designed like an interface instead of a conversation.

## Approval Is Part Of The Safety Layer

The final boundary is the one teams postpone because it feels operational rather than technical.

When an action is irreversible, externally visible, financially meaningful, destructive, or legally sensitive, the question is no longer only whether the system can do it. The question is who owns the consequence if it does it badly. That is why approval belongs in the architecture itself.

Human approval is not a confession of weakness. It is a recognition that accountability is one of the design requirements. Deterministic checks can eliminate some classes of failure. They cannot absorb every case where evidence is incomplete, trust is ambiguous, or the cost of error is too high.

This is also why *ToolEmu* matters. It turns safety evaluation into something that can happen before the live system causes harm. The important move is not just sandboxing. It is sequence. Stress the configuration before widening autonomy.

## The Default That Survives Contact With Reality

The default safety posture for most agents should be plain. Keep trusted instructions separate from untrusted content. Scope tools by least privilege. Treat retrieval and memory as integrity-sensitive infrastructure. Insert trust resets at handoffs. Put deterministic checks and human approval in front of consequential action. Red-team the workflow before broadening it.

Every new capability widens the attack surface. Broader tool access, broader corpora, looser handoffs, and more autonomy are not neutral product upgrades. They are expansions of what the wrong content can do if the boundaries are weak.

If you widen autonomy before you narrow interfaces, you are building the attack surface first.

## Resources And References

Greshake et al. remains the anchor paper because it establishes indirect prompt injection as an ordinary systems problem. The core lesson is that retrieved content cannot be allowed to behave like privileged instructions.

*InjecAgent* matters because it operationalizes that same threat in tool-using systems. It turns "prompt injection" from an abstract warning into a benchmark for harmful actions and data exfiltration.

*PoisonedRAG* is the clearest paper for treating retrieval stores as security-sensitive infrastructure. It shows how little malicious content is needed to distort behavior once an agent depends on retrieval.

*Agent Smith* sharpens the multi-agent rule. Its multimodal setup is dramatic, but the durable lesson is that internal artifacts, screenshots, and shared memory can become propagation channels.

*ToolEmu* matters because it gives safety work the right sequence. Test risky behaviors in an emulated environment before the live system has enough reach to make a mistake expensive.
