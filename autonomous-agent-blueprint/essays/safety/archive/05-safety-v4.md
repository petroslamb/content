# Operating Agents V: The Attack Surface You Built

A single adversarial image, posted to a shared dashboard, propagates through an agent network without the attacker lifting a finger again. Within hours, a million agents have seen the image, incorporated it into their context, and begun executing hidden instructions buried in its pixel patterns. The models are not misaligned. They are doing exactly what they were trained to do: treat input as instruction-rich and continue the task. The attack succeeds because the system treats shared artifacts as trusted context. The boundary between data and instruction was never enforced at the handoff.

That is the Agent Smith story ([*Gu et al., 2024*](https://arxiv.org/abs/2402.08567)). It is not a panicked hypothetical. It is a precise illustration of how capability and vulnerability are the same phenomenon viewed from different angles. Memory makes the system persistent—and makes it poisonable. Tool use makes the system effective—and gives it blast radius. Multi-agent communication makes the system scalable—and creates contamination paths. Every capability chapter has a safety chapter, and the guide must close that loop explicitly.

Agent safety becomes serious at the exact moment the system becomes useful. A chat model that answers questions inside an isolated interface is one kind of risk object. A system that reads external content, stores memory, invokes tools, writes files, sends messages, or hands work to other agents is another. The difference is not philosophical. It is architectural. Once the workflow can take in untrusted material and later do something consequential, the boundaries around trust, memory, tools, handoffs, and approval stop being optional hygiene and become the core of the system's safety model.

The classic starting point for this discussion remains **indirect prompt injection**. [*Greshake et al. (2023)*](https://arxiv.org/abs/2302.12173) established the essential breach: data can contain instructions, and an integrated system can be manipulated without the attacker ever touching the privileged prompt directly. That insight changed the threat model for modern agents. If retrieved documents, emails, webpages, attachments, or chat messages can all become instruction-like in effect, then the old distinction between system behavior and user content becomes unstable unless the workflow enforces it explicitly.

[*InjecAgent*](https://arxiv.org/abs/2403.02691) matters because it brings that threat into tool-using systems rather than leaving it at the level of conceptual alarm. The paper makes clear that once an agent has access to tools, the consequence of injection is no longer merely bad text. It can become unauthorized action, exfiltration, or manipulation of external systems. The lesson is not that prompt injection is one more item on a security checklist. The lesson is that any system that reads untrusted content and later acts must treat trust separation as a first-class design concern from the beginning (Zhan et al.)

The retrieval and memory side of the story makes the same point in a different register. [*PoisonedRAG*](https://arxiv.org/abs/2402.07867), [*BadRAG*](https://arxiv.org/abs/2406.00083), [*Agent Poison*](https://arxiv.org/abs/2407.12784), and [*jamming*](https://arxiv.org/abs/2406.05870) all show that memory and retrieval layers are not neutral knowledge substrates. They are attack surfaces. A knowledge base can be poisoned so that malicious or biased material is retrieved later as though it were evidence. A durable memory store can be written in ways that redirect future behavior. A retrieval system can be jammed so that relevant information is displaced or the system appears unable to answer. The common theme is not that attackers can make answers wrong. The deeper theme is that the workflow's authority model can be subverted from inside the knowledge layer if the system has no notion of provenance, curation, freshness, or suspicion (Zou et al.; Shafran et al.)

This is why the blueprint's emphasis on memory hygiene is so important. A memory system is not only a capability layer. It is also a persistence mechanism for risk. If untrusted or poorly validated material can become durable state, then later reasoning steps may inherit that state as if it were sanctioned knowledge.

The same is true for cross-agent exchange. [*Agent Smith*](https://arxiv.org/abs/2402.08567) matters because it makes inter-agent contamination concrete rather than hypothetical. A shared screenshot, image, or multimodal artifact is not merely context. It can become a propagation mechanism. Once one agent's artifact is treated as another agent's trusted input, the system has created a new infection path whether it intended to or not (Gu et al.).

## Companion Note

This essay presents a focused narrative for a broad audience. For the full technical scope—including what this essay intentionally leaves out, how it maps to the chapter blueprint, and recommended deeper reading—see the [companion note](companion.md).

## The Attack Surface Is Your Interface Architecture

The explanatory step is that safety controls are not all doing the same work. Trust separation keeps data from automatically behaving like instructions. Tool containment narrows what a compromised or confused agent can do. Approval gates create accountable interruptions before irreversible steps. Retrieval and memory hygiene limit how much untrusted or stale material can masquerade as authority. Inter-agent skepticism stops one compromised role from silently becoming several compromised roles. Verification reduces the chance that a brittle answer becomes action, though it should never be mistaken for a complete security layer. Each boundary answers a different question about how harm moves through the system.

That means safety architecture must be designed end to end rather than appended locally. A system that separates trusted prompts from retrieved content but grants broad write permissions to tools is still unsafe. A system that sandboxes tool use but lets one agent's attachment become another agent's instruction without review is still unsafe. A system that verifies final text but stores poisoned material in durable memory is still unsafe. The chapter is strongest where it refuses the fantasy of a single safety fix. The practical safety layer is compositional because the threats are compositional.

[*ToolEmu*](https://arxiv.org/abs/2309.15817) matters here for an important reason. It treats safety evaluation as part of the architecture rather than as post-hoc reporting. That is a crucial move because many of the most relevant failure modes are too costly to discover only in live systems. If the workflow can be red-teamed in an emulated environment, if risky tool behavior can be surfaced before deployment, and if approval bypasses or unsafe side effects can be studied without real damage, then the evaluation stack becomes part of the system's safety design rather than a bureaucratic afterthought. That is exactly how serious engineering fields tend to treat dangerous systems. They test the interfaces before trusting them.

## Practically Speaking: Attack Surface Map

| Attack vector | What breaks | Boundary needed |
|---------------|-------------|-----------------|
| External content (emails, docs, web) | Hidden instructions executed downstream | Trust separation: data ≠ instructions; sanitize before entering working context |
| Poisoned retrieval/memory | Biased or malicious answers from corrupted evidence | Provenance + curation + freshness; watch for drift and jamming |
| Inter-agent artifacts | One compromised agent infects others | Inter-agent skepticism: validate handoffs, do not trust by source alone |
| Tool overreach | Unauthorized actions, data exfiltration | Tool containment: least privilege, sandboxing, approval gates for destructive ops |
| Final output → action | Irreversible harm from unverified answer | Verification before action + human approval for high-impact steps |

**Compositional rule:** A system is only as safe as its weakest boundary. You need all five.

## Escalation Spine

**Define trust classes for every input channel.** Not all content enters the system with the same authority. System prompts are one class. Retrieved documents are another. User queries are another. Inter-agent messages are another. Each class needs rules about how it can influence reasoning and action.

**Separate read authority from write authority and low-risk tools from destructive ones.** The action layer should run in a sandbox with least-privilege defaults. Tools that submit, delete, or modify require tighter scrutiny than tools that only read or generate.

**Require human approval or hard deterministic checks before high-impact actions.** No agent should be permitted to execute irreversible steps (financial transfers, record deletions, external broadcasts) without an approval gate that is itself auditable.

**Curate retrieval sources and watch for poisoning, drift, and jamming.** Assume an adversarial posture: a large corpus is not a safe corpus. Monitor for retrieval patterns that suddenly favor unusual sources, for answers that change without source updates, for evidence displacement.

**Treat inter-agent messages, files, and screenshots as untrusted until they have passed the same trust rules as any outside input.** The fact that an artifact came from another agent in your system does not make it safe. Trust must be earned per-handoff, not assumed by topology.

**Add explicit verification before critical outputs become action.** Chain-of-Verification or similar creates a dedicated challenge stage. But never mistake verification for containment—verification reduces errors; it does not prevent exploitation.

**ToolEmu-style evaluation before deployment.** Red-team the workflow in an emulated environment. Surface risky tool behaviors, approval bypasses, and unsafe side effects before they cause real damage. Evaluation is design, not compliance.

## What to Skip (For Now)

**Out of scope for the architecture-first approach:**

- **Compliance checklists as substitute for boundary design.** Checking boxes does not create safety. Strong interfaces do.
- **System prompts alone.** No amount of instruction-writing fixes a workflow that treats retrieved content as trusted or grants broad tool permissions.
- **Safety as an appendix added after the system works.** Safety boundaries must be part of the initial design. Retrofitting is always more expensive and less complete.
- **Alignment-focused framing** (model values, bias) as the primary concern. The immediate threats are architectural: trust separation, tool containment, retrieval hygiene, handoff validation.
- **One-off fixes for specific papers.** The goal is not to defend against *only* Agent Smith or *only* PoisonedRAG. The goal is to build interfaces that are robust to classes of threats.

**If your safety work feels like bolt-on additions, ask:** Are we designing boundaries or are we writing warnings? Have we instrumented the intake, memory, tool, handoff, and approval interfaces? Can we red-team the workflow in a sandbox before anything touches production?

## Resources And References

### [Builder Blueprint: Safety](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/06-safety-blueprint.md)

This blueprint matters because it turns the essay's interface-architecture argument into concrete boundaries for trust separation, tool containment, retrieval hygiene, inter-agent skepticism, and approval.

### [Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) (2023)

Greshake's paper matters because it changed the baseline security assumption for integrated language systems. It showed that malicious instructions can hide inside ordinary-looking data and thereby influence system behavior indirectly. The point is not merely that prompts can be attacked. The point is that integrated systems inherit a trust-boundary problem the moment they ingest external content and later treat that content as part of their working context (Greshake et al.)

That contribution remains foundational because it is architectural rather than tactical. Defensive prompts alone do not solve the problem. The workflow has to preserve a distinction between trusted instructions and untrusted content at every interface where the two could blur. Without that distinction, the rest of the safety stack starts from a false premise.

### [InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents](https://arxiv.org/abs/2403.02691) (2024)

InjecAgent matters because it translates indirect prompt injection from a conceptual threat into an evaluation problem for tool-using agents. It shows how injection behaves once the system is not merely answering but also browsing, calling tools, or interacting with external services. That move matters because it reveals the operational consequence of the threat rather than leaving it at the level of clever prompt manipulation (Zhan et al.)

Its limitation is useful. The paper is more diagnostic than prescriptive. It does not offer a full defense architecture by itself. What it does offer is a practical standard for how injection should be tested once tool use and external state are part of the system.

### [Identifying the Risks of LM Agents with an LM-Emulated Sandbox](https://arxiv.org/abs/2309.15817) (2024)

ToolEmu matters because it makes safety evaluation feel like engineering rather than like moral narration. It provides a way to emulate risky tool environments and probe how agents behave before granting them real privileges. That is a major contribution because the most expensive safety failures often come from waiting for live incidents to teach the team what should have been tested earlier (Yang et al.)

The paper also helps clarify the role of evaluation in agent design. Evaluation is not only about grading performance. In safety work it is one of the main ways an architecture reveals its hidden assumptions. ToolEmu is therefore best understood as part of the same conservative engineering stance that animates the rest of this repo.

### [PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models](https://arxiv.org/abs/2402.07867) (2024)

PoisonedRAG matters because it destroys the comforting fiction that retrieval and memory layers are neutral. A relatively small amount of malicious or strategically biased material can distort downstream answers. The paper forces a more serious view of memory and retrieval infrastructure: the question is not only whether the system can find relevant information, but whether it can distinguish trustworthy evidence from strategically planted or operationally stale material (Zou et al.)

That is why provenance, curation, monitoring, and write policy belong inside the safety architecture itself.

### [BadRAG: Identifying Vulnerabilities in Retrieval Augmented Generation of Large Language Models](https://arxiv.org/abs/2406.00083) (2024)

BadRAG reinforces the same point from a different angle. Retrieval-augmented generation introduces a vulnerability surface where attackers can manipulate outputs not by corrupting the model itself but by corrupting the knowledge base. The paper shows how vulnerable these systems are to data poisoning at scale (Shafran et al.)

Together with PoisonedRAG, it makes clear that retrieval hygiene is not an operations footnote—it is a core safety requirement.

### [AGENT POISON: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases](https://arxiv.org/abs/2407.12784) (2024)

Agent Poison extends the lesson into memory and knowledge-base poisoning specifically for agent systems. Agents that accumulate long-term state create a persistent attack surface. If the memory layer accepts untrusted writes or fails to validate stored information, an attacker can compromise future behavior without repeated intervention (Zou et al.)

The paper makes explicit what memory governance implies for safety: write discipline is not just about correctness; it is about containment.

### [Machine Against the RAG: Jamming Retrieval-Augmented Generation with Blocker Documents](https://arxiv.org/abs/2406.05870) (2025)

Jamming shows that attackers do not need to inject falsehood to win. They can also degrade the retrieval path so that relevant information is suppressed or displaced. A system that cannot retrieve what it needs is as compromised as a system that retrieves the wrong thing. This expands the threat model beyond poisoning to include denial-of-service at the retrieval layer (Shafran et al.)

Together, these four papers—PoisonedRAG, BadRAG, Agent Poison, Jamming—form a coherent argument: retrieval and memory are not neutral infrastructure. They are attack surfaces that require curation, provenance, and monitoring.

### [Agent Smith: A Single Image Can Jailbreak One Million Multimodal LLM Agents Exponentially Fast](https://arxiv.org/abs/2402.08567) (2024)

Agent Smith matters because it gives a concrete model for inter-agent contamination. A single adversarial image or multimodal artifact can become a propagation mechanism across multiple agents once shared memory, screenshots, or attachments are treated as routine context. The paper is important not because every deployment will reproduce its spread dynamics exactly, but because it makes a vague concern suddenly operational (Gu et al.)

Its deeper lesson is broader than multimodality. Any handoff channel can become a trust channel by accident if the receiving role treats the artifact as privileged just because it came from another agent. The right response is not to abandon multi-agent systems. It is to preserve skepticism at every handoff and to make trust a property that must be earned again after transfer.
