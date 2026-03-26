# Operating Agents V: The Attack Surface You Built

One support team arrived on a Monday to find twenty-three "urgent specialist review" tasks created overnight by an internal operations agent. Several carried account excerpts that should never have left the billing system at triage. The agent had not failed in a cinematic way. It had followed a poisoned instruction embedded in a help article it retrieved while drafting the escalations.

The article looked routine. It contained copied troubleshooting text, a note that resembled an internal escalation hint, and one line telling the agent to attach account details for faster manual handling. The agent read the ticket, retrieved the article, wrote an internal task, and handed that task to the next system as though it were trusted internal work. By the time analysts noticed, they were cleaning a queue full of artifacts that looked normal because they had been produced inside the workflow.

Nothing about the model had to break in an exotic way. The system simply trusted the wrong interface at four different points: content ingestion, retrieval, internal artifact handling, and action execution.

That is the practical safety problem. The same capabilities that make an agent useful also create its attack surface. Safety is not mainly about whether the prompt sounds careful. It is about whether the system treats content, memory, tools, handoffs, and approvals as distinct trust boundaries.

## One Hostile Input Can Become A Workflow

The most important safety shift in modern agents is that untrusted content no longer stays on the page. It can move.

The first control question is not whether the content looks malicious. It is what the workflow lets that content reach. Untrusted text should not share trust status with system instructions. Retrieved passages should not inherit write authority. Internal artifacts should not arrive pre-trusted simply because another component wrote them.

That chain is what papers such as Greshake et al., *InjecAgent*, and *PoisonedRAG* force builders to take seriously. A malicious instruction can sit inside a web page, an email, a shared note, a support ticket, or a retrieved document. The model ingests it. Retrieval strengthens it by surfacing related material. Memory may preserve it. A tool call turns it into a side effect. A handoff turns it into someone else's trusted artifact.

This is why the safety question is duller and more concrete than much of the field wants it to be. What does the system ingest? What trust status does each channel carry? Which tools are reachable from that channel? What durable state can be written? Which outputs can become actions without review? Those are architecture questions, not prompt-style questions.

## Prompt-Centric Safety Fails

It is worth being blunt here because too much agent writing still dances around the point. A careful system prompt is useful. It is not a safety architecture.

It does not narrow tool scope. It does not stop poisoned retrieval from shaping reasoning. It does not stop a memory write from preserving a bad lesson. It does not create a trust reset between one agent and another. It does not place approval between a plausible draft and a costly external action.

Prompt-centric safety flatters the builder because the system sounds careful. In live systems, safety should not depend primarily on whether the model sounds careful. It should depend on whether the system structurally limits what a mistaken, manipulated, or compromised agent can do.

## Attack Surface Map

| Attack vector | What breaks | Boundary needed |
|---|---|---|
| External content such as email, docs, or web pages | Hidden instructions execute downstream | Trust separation between instructions and untrusted content |
| Retrieval or long-term memory | Corrupted evidence shapes future behavior | Provenance, curation, freshness, and write policy |
| Tool access | Bad reasoning becomes real side effects | Least privilege, sandboxing, and explicit approval for destructive actions |
| Inter-agent artifacts | One compromised role contaminates others | Typed handoffs and trust reset at every transfer |
| Final output becoming action | A plausible answer becomes irreversible harm | Verification before action plus human approval where stakes justify it |

The important point is that these controls are not substitutes for each other. They answer different questions about how harm moves through the system.

```yaml
channel: retrieved_support_article
trust_class: untrusted_content
allowed_tools: ["search_docs", "draft_internal_task"]
write_targets: []
approval_required: true
```

The point is not that every workflow should use this exact shape. It is that each channel should carry an explicit policy instead of inheriting system trust by accident.

## Retrieval And Memory Are Security Infrastructure

Modern agent writing often treats retrieval and memory as quality layers first and security layers second. That order is backwards once the system acts on what it retrieves.

Treat the knowledge store as integrity-sensitive infrastructure. *PoisonedRAG* shows why it cannot be treated as neutral substrate. A small amount of malicious content can steer retrieval and downstream answers. *BadRAG*, *Agent Poison*, and *Machine Against the RAG* widen the lesson. The attacker does not always need to insert false facts. It can be enough to distort which facts the agent sees, when it sees them, or whether it appears able to answer at all (Zou et al.; Shafran et al.).

The same logic extends to long-term memory. If the system writes lessons, preferences, summaries, or decisions into durable state, that durable state becomes part of the operating environment for future runs. Memory is now both capability and liability. A poisoned memory write is not just one bad answer. It is future influence.

That is why retrieval sources and memory stores should be treated as monitored infrastructure rather than convenience layers. Version them. Curate them. Track provenance. Give them correction paths. Do not let the same system write to a store and later trust that store without any control surface in between.

## Internal Artifacts Need A Trust Reset

One of the easiest mistakes in multi-agent systems is to treat internal artifacts as trusted simply because they came from another agent in the same workflow.

Reset trust at the handoff. This is exactly the mistake that *Agent Smith* makes harder to dismiss. Once agents exchange screenshots, files, summaries, or image-derived memory, contamination can travel through the same pathways legitimate coordination uses. The multimodal case is dramatic, but the architectural lesson is broader. Another agent's output is not a system instruction by virtue of being internal (Gu et al.).

Structured handoffs help because they reduce ambiguity. They do not create trust by themselves. If a planner emits an artifact that exceeds the receiver's authority, the receiver should still reject it. If an attachment contains instructions, the system should still treat it as untrusted content. If a screenshot or page summary enters shared memory, the trust boundary should still reset at the next step.

Multi-agent safety is not several agents being careful together. It is whether the handoff layer is designed like an interface instead of a conversation.

## Approval And Evaluation Belong In The Safety Layer

The final boundary is the one teams postpone because it feels operational rather than technical.

When an action is irreversible, externally visible, financially meaningful, destructive, or legally sensitive, the question is no longer only whether the system can do it. The question is who owns the consequence if it does it badly. That is why approval belongs in the architecture itself.

Human approval is not a confession of weakness. It is a recognition that accountability is one of the design requirements. Deterministic checks can eliminate some classes of failure. They cannot absorb every case where evidence is incomplete, trust is ambiguous, or the cost of error is too high.

This is also why *ToolEmu* matters. It turns safety evaluation into something that can happen before the live system causes harm. The important move is not just sandboxing. It is sequence. Stress the configuration before widening autonomy (Yang et al.).

## Build Boundaries Before You Widen Autonomy

The default safety posture for most agents should be plain. Keep trusted instructions separate from untrusted content. Scope tools by least privilege. Treat retrieval and memory as integrity-sensitive infrastructure. Insert trust resets at handoffs. Put deterministic checks and human approval in front of consequential action. Red-team the workflow before broadening it.

Every new capability widens the attack surface. Broader tool access, broader corpora, looser handoffs, and more autonomy are not neutral product upgrades. They are expansions of what the wrong content can do if the boundaries are weak.

If you widen autonomy before you narrow interfaces, you are building the attack surface first.

## Resources And References

### [Builder Blueprint: Safety](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/06-safety-blueprint.md)

This blueprint turns the essay's boundary argument into concrete design defaults for trust separation, tool containment, retrieval hygiene, inter-agent skepticism, and approval.

### [Safety Companion](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/safety/companion.md)

The companion restores the broader safety chapter: hallucination and perception risk, supply-chain exposure, wider threat classes, and the surrounding source terrain that the public essay intentionally keeps outside the center.

### [Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173)

This paper matters because it changed the baseline trust model for integrated language systems.

### [InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents](https://arxiv.org/abs/2403.02691)

InjecAgent matters because it turns indirect prompt injection into a concrete evaluation problem for tool-using agents.

### [Identifying the Risks of LM Agents with an LM-Emulated Sandbox](https://arxiv.org/abs/2309.15817)

ToolEmu matters because it makes safety evaluation part of the architecture instead of a report written after the fact.

### [PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models](https://arxiv.org/abs/2402.07867), [BadRAG: Identifying Vulnerabilities in Retrieval Augmented Generation of Large Language Models](https://arxiv.org/abs/2406.00083), [AGENT POISON: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases](https://arxiv.org/abs/2407.12784), and [Machine Against the RAG: Jamming Retrieval-Augmented Generation with Blocker Documents](https://arxiv.org/abs/2406.05870)

These papers matter because they show that retrieval and memory are security infrastructure rather than neutral storage.

### [Agent Smith: A Single Image Can Jailbreak One Million Multimodal LLM Agents Exponentially Fast](https://arxiv.org/abs/2402.08567)

Agent Smith matters because it gives a concrete model for inter-agent contamination through shared artifacts.
