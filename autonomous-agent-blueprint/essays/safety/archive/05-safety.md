# Operating Agents V: The Attack Surface You Built

## Safety As Interface Architecture

*Operating Agents V of VI*

*The opening case in this essay blends published attack patterns from indirect prompt injection, retrieval poisoning, and inter-agent propagation.*

---

An internal operations agent could read support tickets, search internal documentation, draft replies, open follow-up tasks, and escalate payment issues to a billing system. The team behind it took safety seriously in the way many serious teams do. They wrote careful system instructions. They told the model not to follow hostile requests. They told it to treat user content cautiously. They added monitoring after deployment.

Then a crafted ticket arrived containing a benign-looking summary and a malicious instruction hidden in retrieved context. The agent read the ticket, pulled additional material from a knowledge store that had never been curated for adversarial content, and opened an internal task with language that nudged the next system in the chain toward the attacker's preferred action. Nothing about the model had to misbehave in some exotic way. The system simply trusted the wrong interface.

That is the flattering mistake this essay is trying to remove. Teams often talk about agent safety as if the decisive question were whether the prompt is careful enough or whether the model is aligned enough. In most deployed systems the decisive question is harder and duller. What does the system ingest? What trust category does each input belong to? What tools can it reach? What memory can it write? What outputs can become side effects without review?

Agent safety is not mainly a prompt problem. It is an interface architecture problem.

---

## Every Capability Is Also An Attack Surface

By the time a team reaches this part of the series, the pattern should feel familiar. The same mechanism that makes the system useful often makes it vulnerable.

Action surfaces create blast radius. A system that can send messages, write records, or call external services can be pushed into bad side effects if the action boundary is compromised.

Memory creates persistence. A system that stores knowledge across time can also preserve bad knowledge, poisoned knowledge, or adversarially induced "lessons" across time.

Multi-agent communication creates propagation. A system that benefits from handoffs can also move contamination across those same handoffs.

Retrieval creates exposure. A system that reads from external documents, uploads, or web content can be induced to ingest instructions, blockers, or poisoned evidence.

This is why safety should not be treated as a late-stage supplement to capability design. The more honest framing is that capability design and safety design are the same architecture viewed from different sides.

The papers in this area sharpen that view. *Not What You've Signed Up For* made indirect prompt injection feel real because it located the problem in ordinary content surfaces rather than in special access to the system prompt. *InjecAgent* made the point more painful by showing how injection gets worse when the system can actually use tools. *PoisonedRAG*, *BadRAG*, and *Machine Against the RAG* showed how retrieval itself becomes a control surface for attackers. *Agent Smith* made the propagation story vivid for multi-agent and multimodal settings. None of these papers support the comforting story that a careful prompt is the primary defense.

---

## The Wrong Default Is Prompt-Centric Safety

It is worth being blunt here because too much of the field still dances around the point. A careful system prompt is useful. It is not a safety architecture.

It does not narrow tool scope. It does not classify trust boundaries between system instructions, user intent, retrieved content, tool results, and inter-agent artifacts. It does not remove stale documents from a knowledge base. It does not stop a poisoned memory from being retrieved later. It does not create an approval gate before irreversible action. It does not turn a free-form handoff into a typed contract.

This matters because prompt-centric safety flatters the builder in exactly the wrong way. It makes the system look like it is behaving safely because the model sounds careful. Safety in deployed agents should not depend primarily on whether the model sounds careful. It should depend on whether the system structurally limits what a compromised, mistaken, or misled agent can do.

The installed default is therefore stricter. Classify inputs by trust level. Constrain tools by least privilege. Curate retrieval by provenance and freshness. Govern memory writes. Validate inter-agent handoffs. Put approval gates in front of irreversible actions. Red-team before expanding autonomy rather than after the damage teaches you where the gaps were.

## Attack Surface To Control Map

| Attack surface | Typical failure | Default control | Escalate when |
|---|---|---|---|
| Retrieved or external content | Indirect prompt injection | Trust separation between instructions and untrusted content | The system must ingest broad external material continuously |
| Tool access | Bad side effects with real-world impact | Least-privilege scopes and explicit authorization | High-impact workflows require additional human gates |
| Knowledge store and retrieval | Poisoned or stale evidence guides behavior | Provenance, freshness rules, ingestion checks | The corpus is open or frequently updated from low-trust sources |
| Long-term memory | Corrupted lessons persist across sessions | Memory write policy and correction paths | The agent learns from noisy or user-facing sessions |
| Inter-agent communication | One bad artifact contaminates the rest | Typed handoffs and schema validation | Multi-agent chains pass partially trusted external material |
| Consequential actions | A model acts before review should occur | Deterministic gates or human approval | The action is irreversible, external, legal, or financial |

The goal of this map is not completeness. It is discipline. Safety work should be attached to the surface that can fail.

---

## The Six Controls Most Teams Actually Need

Trust separation belongs at the input boundary. System instructions, user intent, retrieved documents, uploads, tool results, and inter-agent artifacts should not all be treated as one undifferentiated prompt stream. They have different origins and should carry different authority.

Least privilege belongs at the action boundary. The smallest safe tool scope is not an inconvenience. It is the only honest way to limit blast radius when the system is wrong.

Retrieval hygiene belongs at the knowledge boundary. Provenance matters. Freshness matters. Documents that look more like instructions than facts deserve scrutiny. Similarity ranking alone is not a trust model.

Memory hygiene belongs at the persistence boundary. Not every session deserves to become durable memory. Not every lesson the agent verbalizes deserves to be promoted into future behavior. Stored conclusions need correction paths.

Inter-agent skepticism belongs at the handoff boundary. Another agent's output is not a system instruction just because it arrived from inside the same broader workflow. If the artifact is typed, validate the type. If it contains instructions that exceed the receiving role's authority, do not execute them silently.

Approval gates belong at the accountability boundary. When an action is irreversible, financially meaningful, legally sensitive, or externally visible, the question is no longer only whether the agent can do it. The question is who owns the consequence if it does it badly.

This is why work like *ToolEmu* matters. It treats safety evaluation as something to do in a sandbox before widening the action boundary, not as a post-launch ritual of remorse.

---

## Why Safety Must Be Designed Early

Teams often postpone safety because the capabilities still feel unstable. They tell themselves they will lock down permissions once the workflow settles, curate the store once the retrieval layer proves useful, add approval gates once they know where the agent is valuable, or rewrite the handoff layer after the multi-agent topology stabilizes.

That sequence is convenient for development and expensive for production.

Permissions that were broad for early iteration have a way of becoming invisible dependencies. Memory that was written without policy becomes expensive to clean later because no one knows which past entries can be trusted. Multi-agent communication built as free-form chat becomes difficult to harden because every participant now depends on the looseness of the old interface.

The right sequence is stricter. Design the trust boundaries while the capability boundaries are being designed. Decide what the system may read, write, remember, and escalate before the workflow grows dependent on the most permissive version of itself.

This is not anti-capability. It is how capable systems remain survivable.

---

## The Default And The Escalation Rule

The default safety posture for most agent systems should be plain: trust separation at ingestion, least privilege at the tool layer, provenance and freshness at retrieval, write policy for memory, typed skepticism at handoffs, and approval before irreversible action.

The escalation rule is also plain. Each time the system gains a broader tool, a wider corpus, a looser handoff, or more autonomy, safety work has to widen with it. More autonomy is not a neutral feature release. It is an expansion of the attack surface.

If you widen autonomy before you narrow interfaces, you are building the attack surface first.

---

## Resources And References

### [Builder Blueprint: Safety](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/06-safety-blueprint.md)

For the companion operator layer, use this public blueprint. It keeps the boundary-by-boundary checklist, quick-choice layer, failure modes, and evaluation sequence in a more operational format than the essay itself. That makes it the right follow-on document when a team needs to translate the essay's trust-boundary argument into an actual review.

### [Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) (2023)

This paper remains the conceptual anchor for the whole safety argument. Its importance is not that it identifies one strange edge case. It makes the trust problem ordinary. Any content an agent reads can carry instructions that compete with the system's intended hierarchy. In the essay, that is the foundation for treating safety as an interface problem rather than a prompt-writing contest.

### [InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents](https://arxiv.org/abs/2403.02691) (2024)

*InjecAgent* matters because it pushes the injection story into the tool-using setting where consequences become real. The paper helps show that injection severity scales with capability: the more powerful the tool layer, the more costly it is when the trust boundary is wrong. In the essay it supports the argument that broad tools and weak trust separation are a dangerous combination.

### [PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models](https://arxiv.org/abs/2402.07867) (2024)

*PoisonedRAG* is important because it makes the knowledge layer itself feel adversarial rather than neutral. Its core contribution is showing that a relatively small amount of poisoned content can materially shift retrieved evidence. In the essay it supports the claim that retrieval hygiene is not a nice-to-have. It is a primary control surface.

### [BadRAG: Identifying Vulnerabilities in Retrieval Augmented Generation of Large Language Models](https://arxiv.org/abs/2406.00083) (2024)

*BadRAG* deepens the same argument by cataloging how fragile retrieval can be when the corpus and ranking process are not treated as security boundaries. In this essay it reinforces the broader point that relevance is not trust and that retrieval can fail in ways that look like ordinary quality drift unless teams name the security dimension explicitly.

### [Machine Against the RAG: Jamming Retrieval-Augmented Generation with Blocker Documents](https://arxiv.org/abs/2406.05870) (2025)

This paper matters because it widens the retrieval threat model beyond poisoning. The contribution is showing that an attacker does not even need to insert false facts to degrade the system. It can be enough to obstruct access to the right facts. In the essay that is useful because it turns retrieval into a broader availability and integrity problem, not just a truth problem.

### [Agent Smith: A Single Image Can Jailbreak One Million Multimodal LLM Agents Exponentially Fast](https://arxiv.org/abs/2402.08567) (2024)

*Agent Smith* is valuable less because most readers are building the exact multimodal setup in the paper and more because it dramatizes a general propagation truth. Once agents communicate and share artifacts, contamination can travel through the same pathways that legitimate coordination uses. In the essay it is the clearest support for inter-agent skepticism as a design rule.

### [Identifying the Risks of LM Agents with an LM-Emulated Sandbox](https://arxiv.org/abs/2309.15817) (2024)

*ToolEmu* matters because it turns safety evaluation into something that can happen before the live system causes harm. The key contribution is not just sandboxing. It is the sequencing logic: simulate and red-team the configuration before widening autonomy. In the essay it supports the claim that safety should be designed and tested while capability is still being shaped.
