# Chapters 17, 18, and 19 Blueprint: Safety

## Why These Chapters Matter

The safety chapters matter because they explain when the practical stack becomes dangerous. A model that looks safe in a chat demo becomes a very different system once it reads untrusted content, stores memory, calls tools, writes files, or communicates with other agents.

This is why safety belongs at the end of the reading order but at the center of deployment design. You need the earlier chapters to understand what the agent can do, and then these chapters tell you how those abilities fail in production.

## Survey Subsections To Prioritize

- `17.1.2 Prompt Injection Attacks`
- `17.1.3 Hallucination Risks`
- `18.2.1 Supply Chain Attacks`
- `18.2.2 Risks in Tool Usage`
- `19.1 Agent-Memory Interaction Threats`
- `19.2 Agent-Environment Interaction Threats`
- `19.3 Agent-Agent Interaction Threats`

These sections map directly to the practical attack surface of modern agents.

## The Practical Question

The safety chapters are answering one simple question: once the agent can read, remember, and act, where can an attacker or failure chain take control?

The answer is sharper than generic "alignment" talk. The practical attack surfaces are:

- untrusted content
- unsafe tools
- poisoned retrieval and memory
- broad permissions
- weak approval boundaries
- inter-agent communication channels and artifact handoffs

## Core Literature And What Each Paper Adds

### `Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection`

This is the conceptual foundation for treating retrieved or external content as untrusted. The paper matters because it shows how instructions can hide inside data and override system intent indirectly.

Use it as the starting point for all content-boundary design.

### `InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents`

InjecAgent matters because it operationalizes the prompt-injection problem against real tool-using agents rather than abstract prompting setups.

Use it when designing evaluations or red-team tests for tool-integrated systems.

### `Identifying the Risks of LM Agents with an LM-Emulated Sandbox`

ToolEmu matters because it creates a practical safety evaluation pattern. Instead of waiting for failures in production, it emulates tool environments to expose risky behaviors.

Use it when you need a sandbox-first safety evaluation loop.

### `AGENT POISON: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases`

Agent Poison matters because it shows how memory and knowledge stores can become attack vectors. A memory system is not only a capability layer. It is also a liability surface.

Use it when the agent writes or retrieves from durable stores that later influence action.

### `PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models`

PoisonedRAG is one of the clearest demonstrations that a small number of malicious documents can bias retrieval and downstream behavior.

Use it when designing corpus ingestion, retrieval curation, and anomaly detection.

### `BadRAG: Identifying Vulnerabilities in Retrieval Augmented Generation of Large Language Models`

BadRAG reinforces the lesson that retrieval corpora cannot be assumed trustworthy simply because they are large.

Use it when retrieval is central enough that poisoning would materially change system behavior.

### `Machine Against the RAG: Jamming Retrieval-Augmented Generation with Blocker Documents`

Jamming matters because it expands the threat model beyond misinformation. Retrieval can be degraded or blocked even without injecting false facts.

Use it when retrieval availability and coverage matter as much as factual integrity.

### `Chain-of-Verification Reduces Hallucination in Large Language Models`

CoVe belongs here as a reliability control. It does not solve adversarial input problems, but it is one of the cleanest ways to reduce unchecked factual error in outputs.

Use it when factual mistakes would become actions or would contaminate downstream decisions.

### `Agent Smith: A Single Image Can Jailbreak One Million Multimodal LLM Agents Exponentially Fast`

Agent Smith matters because it turns agent-to-agent contamination from a vague concern into a concrete multimodal propagation model. It shows that one adversarial image can move through agent interactions and memory-sharing workflows without repeated attacker intervention.

Use it when agents exchange screenshots, files, image observations, or other multimodal artifacts.

## If Your Problem Looks Like X, Choose Y

- If the agent reads external text and later acts, choose strong trust separation first.
- If the agent calls tools with side effects, choose tool containment and approval gates first.
- If retrieval is central to the workflow, choose retrieval curation, provenance, and poisoning checks.
- If the agent writes durable memory, choose memory hygiene and audit controls.
- If several agents exchange work, treat inter-agent messages, files, and screenshots as untrusted until proven otherwise.

## Method Comparison Matrix

| Control | Best use | Main strength | Main risk if missing | Escalate when |
| --- | --- | --- | --- | --- |
| Trust separation | untrusted content and retrieval | prevents data from behaving like instructions | indirect prompt injection | actions or writes become possible |
| Tool containment | tool-using workflows | narrows blast radius with least privilege | unsafe or over-broad side effects | irreversible actions exist |
| Approval gates | high-impact actions | creates accountable human oversight | irreversible mistakes | deterministic checks alone are not enough |
| Retrieval and memory hygiene | RAG or durable memory | reduces poisoning and stale-state risk | corrupted or jammed grounding | ingestion becomes broader or multi-tenant |
| Inter-agent skepticism | multi-agent systems and artifact handoffs | blocks silent contamination between roles and attachments | unsafe cross-agent message or file trust | agent count, multimodal inputs, or role separation grows |
| Verification | factual or high-stakes outputs | reduces unchecked error propagation | brittle outputs trigger actions | task value justifies heavier review |

## The Chapter's Main Architectural Insight

The strongest practical insight is that safety failures happen at interfaces:

- between instructions and data
- between model and tool
- between retrieval and memory
- between one agent and another
- between agent output and irreversible action

This means the safety layer is not a single classifier or a safety prompt. It is an interface architecture.

## The Default Safety Blueprint

### Boundary 1: Trust Separation

Separate trusted instructions from untrusted content. Retrieved text, web pages, emails, uploaded files, inter-agent messages, and inter-agent attachments should never share the same trust status as system instructions.

### Boundary 2: Tool Containment

Run tools with least privilege. Separate read tools from write tools. Separate low-impact tools from financial, legal, or destructive tools.

### Boundary 3: Action Approval

Require deterministic checks and human approval for irreversible or high-impact actions.

### Boundary 4: Memory Hygiene

Treat memory and knowledge stores as monitored infrastructure. Version, curate, audit, and watch for poisoning or drift.

### Boundary 5: Inter-Agent Skepticism

Treat inter-agent messages and artifacts as another untrusted input channel. Structured handoffs reduce ambiguity, but they do not create trust by themselves.

### Boundary 6: Verification

For important outputs, run explicit verification before action or publication. Verification is not a full security layer, but it is a critical reliability layer.

## Design Decisions That Matter Most

### When prompt injection becomes a core risk

Prompt injection becomes a core risk as soon as the agent reads externally authored content and can later take actions with side effects.

### When retrieval becomes a safety issue

Retrieval becomes a safety issue once the knowledge base is open enough to be poisoned or stale enough to drive incorrect behavior.

### When human approval is mandatory

Human approval is mandatory whenever the downstream action is irreversible, financially meaningful, legally sensitive, or reputationally expensive.

### When sandboxing is non-negotiable

Sandboxing is non-negotiable when the agent executes code, writes files, changes system state, or touches external accounts.

## Evaluation

The safety stack should be evaluated through:

- injection resistance tests
- red-team tool scenarios
- retrieval poisoning simulations
- cross-agent contamination drills with shared files, screenshots, or image memory
- excessive-permission reviews
- approval-bypass tests
- incident replay and root-cause drills

A system that has never been stressed at these interfaces is not safe enough to deploy confidently.

## Failure Modes

- mixing instructions and retrieved content in one undifferentiated prompt
- giving an agent broad tool permissions without hard gates
- assuming internal corpora are automatically trustworthy
- letting one agent's output, attachment, or screenshot become another agent's instruction without control
- treating post hoc monitoring as a substitute for containment

## Recommended Build Order

1. Define trust classes for every input channel.
2. Separate read, write, and destructive tools by policy.
3. Add deterministic approval gates for high-impact actions.
4. Curate and monitor retrieval sources.
5. Add verification for critical outputs.
6. Red-team the whole workflow before widening autonomy.

## Anti-Patterns

- Do not treat safety as a suffix prompt.
- Do not let the agent write to the same knowledge base it later trusts without controls.
- Do not assume multi-agent systems are safer because they have more voices.
- Do not rely on debate as a substitute for access control.

## Reading Sequence For These Chapters

1. `../../essays/safety/05-safety-v6.md`
2. `../../essays/safety/companion.md`
3. `papers/greshake_indirect_prompt_injection.md`
4. `papers/injecagent.md`
5. `papers/toolemu.md`
6. `papers/agentpoison.md`
7. `papers/poisonedrag.md`
8. `papers/badrag.md`
9. `papers/jamming.md`
10. `papers/agentsmith.md`
11. `papers/chain_of_verification.md`

## Bottom Line

The practical message of the safety chapters is that agent safety is architecture. The moment the system reads untrusted content, stores durable state, or takes external action, boundaries, permissions, approval gates, and retrieval hygiene become first-class design components.
