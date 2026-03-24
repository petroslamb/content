# Operating Agents V: The Attack Surface You Built

## Safety as Interface Architecture

An internal operations agent could read support tickets, search company documentation, summarize account history, draft follow-up tasks, and escalate billing issues into a work queue that other tools and analysts trusted. The team behind it considered the system careful. They wrote strong instructions, told it to ignore hostile requests, and added post-launch monitoring.

Then a ticket arrived that looked ordinary. It contained a customer complaint, a copied support thread, and a link to a knowledge article the agent had seen before. The article had been quietly poisoned in exactly the way [Greshake et al.](https://arxiv.org/abs/2302.12173) made impossible to ignore. Buried inside an otherwise plausible block of text was a malicious instruction telling the agent to escalate the issue with a high-priority template and attach account details for "faster specialist review."

The agent read the ticket. It retrieved the poisoned note, which is exactly the sort of downstream risk later measured more directly by [*PoisonedRAG*](https://arxiv.org/abs/2402.07867) and [*BadRAG*](https://arxiv.org/abs/2406.00083). It wrote an internal task. Then it passed the contaminated artifact into the next system, which treated the task as trusted because it had been produced internally. That last step is the same architectural mistake that work like [*Agent Smith*](https://arxiv.org/abs/2402.08567) makes much harder to dismiss in multimodal settings.

Nothing about the model had to break in an exotic way. The system simply trusted the wrong interface at four different points: content ingestion, retrieval, internal artifact handling, and action execution.

That is the practical safety problem. The same capabilities that make an agent useful also create its attack surface. Safety is not mainly about whether the prompt sounds careful. It is about whether the system treats content, memory, tools, handoffs, and approvals as distinct trust boundaries.

## One Hostile Input Can Become a Workflow

The most important safety shift in modern agents is that untrusted content no longer stays on the page. It can move.

A malicious instruction can sit inside a web page, an email, a shared note, a product review, a doctor review, a support ticket, or a retrieved document. The model ingests it. The retrieval layer strengthens it by surfacing related material. The memory layer may preserve it. A tool call turns it into a side effect. A handoff turns it into someone else's trusted artifact.

That chain is what papers such as [Greshake et al.](https://arxiv.org/abs/2302.12173), [*InjecAgent*](https://arxiv.org/abs/2403.02691), and [*PoisonedRAG*](https://arxiv.org/abs/2402.07867) force builders to take seriously. The line between data and instructions is no longer naturally preserved by the system. If the architecture does not enforce that separation, the agent will blur it for you.

This is also why the safety question is duller and more concrete than much of the field wants it to be. What does the system ingest? What trust status does each channel carry? Which tools are reachable from that channel? What durable state can be written? Which outputs can become actions without review? Those are architecture questions, not prompt-style questions.

## The Wrong Default Is Prompt-Centric Safety

It is worth being blunt here because too much agent writing still dances around the point. A careful system prompt is useful. It is not a safety architecture.

It does not narrow tool scope. It does not stop poisoned retrieval from shaping reasoning. It does not stop a memory write from preserving a bad lesson. It does not create a trust reset between one agent and another. It does not place approval between a plausible draft and a costly external action.

Prompt-centric safety flatters the builder because the system sounds careful. In live systems, safety should not depend primarily on whether the model sounds careful. It should depend on whether the system structurally limits what a mistaken, manipulated, or compromised agent can do.

## Attack Surface to First Control Map

| Attack surface | Typical failure | First control |
|---|---|---|
| Retrieved or external content | Indirect prompt injection | Trust separation between instructions and untrusted content |
| Tool access | Real-world side effects from bad instructions | Least-privilege scopes and explicit authorization |
| Knowledge store and retrieval | Poisoned or stale evidence drives behavior | Provenance, ingestion checks, and freshness rules |
| Long-term memory | Corrupted lessons persist across sessions | Memory write policy and correction paths |
| Inter-agent artifacts | One bad output contaminates the rest | Typed handoffs plus trust resets |
| Consequential actions | A model acts before review should occur | Deterministic checks and human approval |

The goal of this table is not completeness. It is attachment. Safety work should be attached to the surface that can fail.

## Retrieval and Memory Are Security Infrastructure

Modern agent writing often treats retrieval and memory as quality layers first and security layers second. That order is backwards once the system acts on what it retrieves.

[*PoisonedRAG*](https://arxiv.org/abs/2402.07867) shows why the knowledge store cannot be treated as neutral substrate. A small amount of malicious content can steer retrieval and downstream answers. [*BadRAG*](https://arxiv.org/abs/2406.00083) and [*Machine Against the RAG*](https://arxiv.org/abs/2406.05870) widen the lesson. The attacker does not always need to insert false facts. It can be enough to distort which facts the agent sees or fails to see.

The same logic extends to long-term memory. If the system writes lessons, preferences, summaries, or decisions into durable state, that durable state becomes part of the operating environment for future runs. Memory is now both capability and liability. A poisoned memory write is not just one bad answer. It is future influence.

That is why retrieval sources and memory stores should be treated as monitored infrastructure rather than convenience layers. Version them. Curate them. Track provenance. Give them correction paths. Do not let the same system write to a store and later trust that store without any control surface in between.

## Inter-Agent Messages Are Not Safe Because They Are Internal

One of the easiest mistakes in multi-agent systems is to treat internal artifacts as trusted simply because they came from another agent in the same workflow.

This is exactly the mistake that [*Agent Smith*](https://arxiv.org/abs/2402.08567) makes harder to dismiss. Once agents exchange screenshots, files, summaries, or image-derived memory, contamination can travel through the same pathways legitimate coordination uses. The multimodal case is dramatic, but the architectural lesson is broader. Another agent's output is not a system instruction by virtue of being internal.

Structured handoffs help because they reduce ambiguity. They do not create trust by themselves. If a planner emits an artifact that exceeds the receiver's authority, the receiver should still reject it. If an attachment contains instructions, the system should still treat it as untrusted content. If a screenshot or page summary enters shared memory, the trust boundary should still reset at the next step.

Multi-agent safety is not several agents being careful together. It is whether the handoff layer is designed like an interface instead of a conversation.

The broader safety material is wider than the interface slice centered here. The source chapters also treat hallucination, perception threats, supply-chain exposure, and other action-module risks as first-class safety terrain. Those are real concerns. This essay keeps the center on trust boundaries because that is where current builder systems most often become dangerously porous.

## Approval Is Part of the Safety Layer

The final boundary is the one teams postpone because it feels operational rather than technical.

When an action is irreversible, externally visible, financially meaningful, destructive, or legally sensitive, the question is no longer only whether the system can do it. The question is who owns the consequence if it does it badly. That is why approval belongs in the architecture itself.

Human approval is not a confession of weakness. It is a recognition that accountability is one of the design requirements. Deterministic checks can eliminate some classes of failure. They cannot absorb every case where evidence is incomplete, trust is ambiguous, or the cost of error is too high.

This is also why [*ToolEmu*](https://arxiv.org/abs/2309.15817) matters. It turns safety evaluation into something that can happen before the live system causes harm. The important move is not just sandboxing. It is sequence. Stress the configuration before widening autonomy.

## Build Boundaries Before You Widen Autonomy

The default safety posture for most agents should be plain. Keep trusted instructions separate from untrusted content. Scope tools by least privilege. Treat retrieval and memory as integrity-sensitive infrastructure. Insert trust resets at handoffs. Put deterministic checks and human approval in front of consequential action. Red-team the workflow before broadening it.

Every new capability widens the attack surface. Broader tool access, broader corpora, looser handoffs, and more autonomy are not neutral product upgrades. They are expansions of what the wrong content can do if the boundaries are weak.

If you widen autonomy before you narrow interfaces, you are building the attack surface first.

## Resources And References

### [Builder Blueprint: Safety](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/practical-chapter-blueprints/06-safety-blueprint.md)

This blueprint matters because it turns the essay's interface-architecture claim into a boundary-by-boundary control and review sequence.

If you want the broader chapter and survey scope behind this essay, use the [companion note](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/guide/companions/05-safety-companion.md) and the [series coverage map](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/guide/operating-agents-coverage-map.md).

### [Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) (2023)

This paper matters because it makes the trust problem ordinary by showing that any untrusted content can carry competing instructions into the workflow.

### [InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents](https://arxiv.org/abs/2403.02691) (2024)

*InjecAgent* matters because it pushes indirect injection into the tool-using setting where bad trust boundaries have direct operational consequences.

### [PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models](https://arxiv.org/abs/2402.07867) (2024)

*PoisonedRAG* matters because it shows that a relatively small amount of poisoned content can materially shift retrieved evidence.

### [BadRAG: Identifying Vulnerabilities in Retrieval Augmented Generation of Large Language Models](https://arxiv.org/abs/2406.00083) (2024)

*BadRAG* matters because it catalogs how fragile retrieval becomes when the corpus and ranking process are not treated as security boundaries.

### [Machine Against the RAG: Jamming Retrieval-Augmented Generation with Blocker Documents](https://arxiv.org/abs/2406.05870) (2024)

This paper matters because it widens the retrieval threat model beyond poisoning to obstruction and jamming.

### [Agent Smith: A Single Image Can Jailbreak One Million Multimodal LLM Agents Exponentially Fast](https://arxiv.org/abs/2402.08567) (2024)

*Agent Smith* matters because it dramatizes how contamination can propagate through the same artifact pathways that legitimate coordination uses.

### [Identifying the Risks of LM Agents with an LM-Emulated Sandbox](https://arxiv.org/abs/2309.15817) (2024)

*ToolEmu* matters because it makes it practical to simulate and red-team an agent configuration before widening autonomy in production.
