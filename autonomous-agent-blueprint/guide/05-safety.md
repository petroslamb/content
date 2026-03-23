# Part 5: The Attack Surface You Built

## Agent Safety as Interface Architecture

*Part 5 of 6: A Practical Guide to Foundation Agents*

---

In 2024, a team of researchers published a paper called *Agent Smith* (Yu et al., 2024). The title was a deliberate reference to the character from *The Matrix*, and the comparison was apt in a precise, technical way. The researchers demonstrated that a single adversarial image, injected into a multimodal agent's environment, could propagate through agent-to-agent interactions and compromise a large population of agents , without the attacker needing to repeat the injection. The attack spread through the same interaction mechanisms the agents relied on for legitimate coordination. The capability that made the agents useful made them vulnerable to exactly this kind of propagation.

The result was striking not because it described a hypothetical future risk but because it described the present architecture of real systems. Any agent that reads external content and communicates with other agents has the surface this attack requires. No exotic capabilities are needed. No model vulnerabilities are exploited. The agents behave correctly according to their specification. The specification is the problem , because it does not treat the communication channels as potentially adversarial.

This is the central argument of safety as interface architecture: agent security failures are not primarily alignment failures or capability failures. They are design failures at the interfaces , the surfaces through which agents receive input, store state, and take action. Controlling those interfaces is what controls the risk. An agent system that has never been designed with adversarial inputs in mind is not "mostly safe." It is an unaudited system whose failure modes have not been found yet.

---

## The Capability-Vulnerability Identity

Every capability introduced in Parts 1 through 4 of this guide opens a corresponding safety surface. This is not an accident of implementation. It is a structural property of useful agent systems.

**Action and tool use** (Part 1) gives the agent the ability to change external state. That same ability gives it blast radius , the scope of damage a failure or a compromised action can produce. An agent that can write to a database can write incorrect data. An agent that can send email can send phishing email in your name. An agent that can call an external API without rate limiting can exhaust your API quota in minutes. The action surface that makes the agent effective is the surface that determines its failure radius.

**Memory** (Part 3) gives the agent persistence across sessions. That same persistence makes the agent's behavior dependent on what is stored , and a stored knowledge base is a static target. *PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models* (Zou et al., 2024) demonstrated that injecting a small percentage of adversarially crafted documents into a large RAG corpus can systematically shift retrieved content to bias agent behavior. The retrieval system works correctly , it retrieves the most similar content. The content it retrieves is no longer trustworthy. *AGENT POISON: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases* (Chen et al., 2024) extends this to agent-specific memory structures, showing that episodic memory and long-term knowledge stores have similar vulnerabilities.

**Multi-agent coordination** (Part 4) gives the system the ability to scale. That same inter-agent communication is a propagation path for adversarial content. Agent Smith uses it. If one agent in a multi-agent system processes an external document containing an adversarial instruction and then passes on a summary of that document to another agent, the adversarial instruction can survive the summarization step in attenuated form. The artifact handoffs that make multi-agent pipelines coherent are the same channels through which contamination moves.

**Retrieval and search** are the mechanism that makes memory practically useful. *Machine Against the RAG: Jamming Retrieval-Augmented Generation with Blocker Documents* (Shafran et al., 2024) demonstrates that retrieval can be disrupted not just through poisoning but through jamming: adversarially crafted documents that are retrieved instead of the intended content, degrading the agent's knowledge access without injecting false information. The result looks like a retrieval quality problem, but it is a denial-of-service attack.

This pattern , capability and vulnerability sharing the same underlying mechanism , means that building capabilities without simultaneously designing the safety architecture is not the first phase of a two-phase process. It is building the attack surface before deciding whether to defend it.

---

## The Six Attack Surfaces

The Chapter 17, 18, and 19 material synthesizes the threat landscape into six interface categories, each of which is a distinct attack surface requiring distinct controls.

**Untrusted content in the prompt** is the surface addressed by *Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection* (Greshake et al., 2023). An agent performing a task reads a document, a web page, an email, or a retrieved chunk , and that content contains an instruction that the agent treats as equivalent to a system instruction. The attacker does not need access to the agent's system prompt. They need access to any content the agent will read. If the agent browses the web as part of its task, every web page it visits is a potential injection vector. If the agent reads uploaded documents, every uploaded document is a potential injection vector.

*InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents* (Zhan et al., 2024) extends this to tool-integrated agents specifically and shows that injection attacks have higher success rates when the agent has access to more powerful tools , because the agent can be instructed to use those tools on behalf of the attacker. An agent with email access and injection vulnerability can be turned into a phishing sender. An agent with file system access and injection vulnerability can be turned into a data exfiltration path.

The control here is trust separation at the architecture level: system instructions and user intent occupy a different trust category than retrieved content and external documents. The agent's action policy governs from the former, not the latter. Retrieved content informs the agent's knowledge; it does not override its instruction set. This distinction needs to be enforced in the system design, not in the prompt.

**Unsafe tools** are tools whose scope of action is broader than the task requires. An agent given a tool that can delete any file, modify any database record, or query any API endpoint is operating with permissions calibrated for the broadest possible case rather than the narrowest necessary one. When the agent is compromised through injection, stale memory, or reasoning error, the damage is bounded by its permissions. Small permissions, small damage. Broad permissions, large damage.

Least-privilege design , each agent has access only to the tools it actively needs for its assigned task, with the narrowest possible scope within those tools , is the implementation of this principle. It is not a safety feature bolted onto an already-designed system. It should be in the initial design specification, before tools are assigned.

**Poisoned retrieval** affects every system with a RAG layer. Knowledge base ingestion pipelines are often given insufficient scrutiny: documents are processed, embedded, and indexed without validation of their source trustworthiness or their potential for adversarial content. A document that was legitimate when it was ingested may become a liability as the world changes and the document becomes stale. A document submitted through a user-facing upload path may have been crafted to bias retrieval in a specific direction.

The controls are concrete: source provenance tracking (where did this document come from, and what trust level does that source carry?), ingestion validation for content that looks like instruction templates rather than factual material, freshness policies that mark stale documents for review or retirement, and retrieval-time content checks that flag retrieved material whose structure resembles adversarial patterns.

**Memory poisoning** is the persistent variant of retrieval poisoning. If an agent's episodic memory is corrupted , through a genuine bad run that was stored uncritically, through an adversarial injection into an early session, or through a poisoned document that updated the agent's long-term factual store , that corruption persists across sessions and influences future behavior. Unlike retrieval poisoning, which affects what the agent knows, memory poisoning can affect how the agent reasons , if the corrupted memory contains prior "decisions" or "lessons learned" that now reflect adversarial intent.

The control is memoy hygiene: write policies that filter what gets stored, correctability of stored memories through human review and explicit correction, and segregation of high-trust memory (system-validated facts) from lower-trust memory (agent-derived conclusions from sessions that have not been audited).

**Uncontrolled inter-agent communication** is the Agent Smith surface. When agents share context through free-form conversation or pass artifacts that have not been validated for adversarial content, injections can propagate. The control is the same artifact handoff principle introduced in Part 4 , typed contracts between agents, validated at each boundary , with an additional security requirement: content arriving from another agent should be treated with appropriate skepticism, especially when it contains instructions that override or extend the receiving agent's task specification.

**High-impact actions without approval gates** are a class of risk rather than an attack surface , the category of failures where the agent does something consequential that it should not have been able to do unilaterally. For irreversible, financially significant, compliance-sensitive, or externally visible actions, the correct architecture is mandatory human approval before execution. This is not the concession that agents cannot be trusted. It is the recognition that accountability for consequential decisions belongs to humans, and architecturally, that accountability must be structurally enforced.

---

## Safety as a Design Layer

The most important reframe in Chapter 17 is positional: safety is not a suffix. It is not the chapter you read after building the system to find out what to add before deploying. It is a design layer specified at the same time as the capability architecture.

Practically, this means the safety specification precedes or accompanies the tool specification, the memory design, and the multi-agent topology. Before the action layer is designed, the permission scope and the approval gates are specified. Before the memory layer is designed, the write policies, source trustworthiness taxonomy, and forgetting rules are specified. Before the multi-agent topology is designed, the inter-agent trust levels and artifact validation rules are specified.

This sequencing matters because retrofitting safety into a complete system is expensive and typically incomplete. Permissions that were designed broadly for development convenience are difficult to narrow in production without breaking workflows that have come to depend on them. Memory that has been accumulating without write policies cannot be retroactively curated without significant engineering effort. Inter-agent communication that was designed as free-form chat cannot be retyped into artifact contracts without redesigning the coordination layer.

*Identifying the Risks of LM Agents with an LM-Emulated Sandbox* (Ruan et al., 2023) provides a pre-deployment evaluation methodology: ToolEmu emulates an agent's tool interactions in a sandbox that can simulate adversarial conditions, allowing safety tests before the agent interacts with real systems. The key insight is that sandboxed evaluation is a design phase activity. Evaluating safety properties before deployment , where the consequences of failures are limited to simulation outputs , is qualitatively different from discovering them in production.

---

## The Safety Blueprint for Deployed Systems

The six controls that the Chapter 17–19 material supports form a concrete safety architecture:

**Trust separation at the input boundary.** Every input the agent receives is classified by source: system instructions, user intent, retrieved context, external documents, tool results, inter-agent messages. The agent's action policy is governed by its system instructions. External content enriches its knowledge without overriding its behavior. This classification is enforced in the system design, not in the prompt.

**Least-privilege tool scopes.** Every agent has access to the minimum set of tools required for its task, with the minimum permission scope within each tool. Tools that modify external state require explicit authorization. Tools that are irreversible require audit logging and, where the stakes are high, human approval.

**Retrieval hygiene.** Knowledge base ingestion tracks source provenance. Documents are stratified by source trust level. High-trust sources (internal validated documents) are retrieved with different weight than low-trust sources (user uploads, external web). Fresh content is distinguished from stale content. Ingestion pipelines include checks for documents that look like instruction templates rather than factual material.

**Approval gates before irreversible actions.** Any action that is irreversible, financially significant, legally consequential, or externally visible sits behind an approval gate. The gate can be automated (a deterministic policy check that must pass) or human (a review step before execution). What it cannot be is optional, advisory, or bypassable by the agent itself.

**Inter-agent skepticism.** Artifacts arriving from other agents in a multi-agent system are validated against their expected schema before use. Instructions embedded in inter-agent messages that override the receiving agent's task specification are flagged rather than executed. The trust level of inter-agent content is explicitly lower than the trust level of system instructions.

**Red-teaming before widening autonomy.** Before any expansion of the agent's tool access, permission scope, or autonomy level, the current configuration is tested against the known injection and poisoning patterns documented in the literature. Testing is not a compliance activity performed once before launch. It is a scheduled review activity that precedes every autonomy expansion.

---

## What Cannot Be Fixed in the Prompt

The most common misapprehension about agent safety is that the primary defense is a well-crafted system prompt. Instructions not to follow adversarial content, instructions to only take explicitly authorized actions, instructions to report suspicious inputs before acting on them , these are real mitigations and worth including. They are not the architecture.

A system prompt instruction is read by the model once, at the beginning of each context. Adversarial content embedded in a retrieved document later in the same context can exploit the temporal distance. A retrieval query that returns adversarial content returns it with high similarity scores, meaning the agent's retrieval mechanisms treat it as especially relevant. An inter-agent message that arrives well into a long reasoning trace carries the accumulated context of the prior steps.

Prompt-level safety instructions also do not address permission scope , an instruction not to delete files does not remove the file deletion tool from the agent's action space. They do not address retrieval hygiene , an instruction to be skeptical of unusual requests does not prevent an adversarially crafted document from ranking highly in retrieval. They do not address memory poisoning , an instruction to act in good faith does not filter corrupted entries out of a poisoned episodic memory.

Safety as interface architecture means that the system enforces its safety properties structurally, not through the model's judgment. The model's judgment is a last line of defense, not a first line. The first lines are the input boundary classification, the permission scope, the retrieval trust stratification, the approval gates, and the inter-agent validation contracts. None of those are in the prompt.

---

## The Architecture Closes the Loop

The five essays before this one described what agents can do: act on tools, reason through tasks, remember knowledge, and communicate with each other. This essay describes what each of those capabilities looks like from the adversarial angle. The action surface is a blast-radius surface. The memory layer is a persistent-state corruption surface. The multi-agent communication channel is a contamination-propagation surface.

This is not a reason to avoid building capable agents. It is a reason to build them with their attack surfaces designed, not discovered. A system that is designed with trust separation, least privilege, retrieval hygiene, approval gates, inter-agent skepticism, and pre-deployment red-teaming is not a less capable system than one without those properties. It is a system whose capabilities are bounded by its safety architecture rather than by whatever the attacker decides to try first.

The Autonomy Tax analysis in prior work estimated that most enterprise agent failures trace to control-layer failures rather than model capability gaps. The safety pattern described here is the control layer. Closing the gap between what agents can do and what they are architecturally constrained to do is the single most important step in moving agents from production prototypes to production deployments that organizations can stand behind.

---

*Part 6, the final essay in this guide, addresses optimization: how to improve an agent system that already works, why the whole workflow is the object of improvement rather than any individual prompt or component, and what the correct optimization sequence looks like.*

---

**Source basis for this essay:** Chapters 17, 18, and 19 of *Advances and Challenges in Foundation Agents* (2025); *Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection* (Greshake et al., 2023) [arXiv:2302.12173](https://arxiv.org/abs/2302.12173); *InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents* (Zhan et al., 2024) [arXiv:2403.02691](https://arxiv.org/abs/2403.02691); *PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models* (Zou et al., 2024) [arXiv:2402.07867](https://arxiv.org/abs/2402.07867); *AGENT POISON: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases* (Chen et al., 2024) [arXiv:2407.12784](https://arxiv.org/abs/2407.12784); *Machine Against the RAG: Jamming Retrieval-Augmented Generation with Blocker Documents* (Shafran et al., 2024) [arXiv:2406.05870](https://arxiv.org/abs/2406.05870); *Agent Smith: A Single Image Can Jailbreak One Million Multimodal LLM Agents Exponentially Fast* (Yu et al., 2024) [arXiv:2402.08567](https://arxiv.org/abs/2402.08567); *Identifying the Risks of LM Agents with an LM-Emulated Sandbox* (Ruan et al., 2023) [arXiv:2309.15025](https://arxiv.org/abs/2309.15025); *BadRAG: Identifying Vulnerabilities in Retrieval Augmented Generation of Large Language Models* (2024) [arXiv:2406.00083](https://arxiv.org/abs/2406.00083); `practical-chapter-blueprints/06-safety-blueprint.md`.
