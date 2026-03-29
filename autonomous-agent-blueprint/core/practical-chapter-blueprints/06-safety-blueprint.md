# Chapters 17, 18, and 19 Blueprint: Safety

## Use This Blueprint When

Use this blueprint the moment the workflow can read untrusted content, call tools, write files, store memory, or exchange artifacts with other agents. Safety becomes real when language acquires consequence. From that point on, the question is where control can be lost and what boundary has to hold for the workflow to remain deployable.

## The Decision

Safety design should answer one question clearly: once the agent can read, remember, and act, where can untrusted input or weak authority take control?

In practical agent systems that question appears at a small set of interfaces:

- between instructions and untrusted data
- between the model and a tool with side effects
- between retrieval, memory, and present authority
- between one agent and another
- between output and irreversible action

If those boundaries are not explicit, the workflow is already operating on borrowed trust.

## Default Position

The default safety posture should be architectural.

- Separate trusted instructions from untrusted content.
- Run tools with least privilege and clear containment.
- Add deterministic checks and human approval for high-impact actions.
- Treat memory and retrieval stores as monitored infrastructure.
- Treat inter-agent messages and artifacts as untrusted by default.
- Use verification as a reliability layer, not as a substitute for access control.

Safety is not a suffix prompt. It is the design of the interfaces where authority changes hands.

## Default Build

### Boundary 1: Trust Separation

Classify each input channel before the model uses it. Retrieved passages, emails, web pages, uploaded files, screenshots, and agent handoffs should never inherit the same trust status as system policy or privileged instructions.

### Boundary 2: Tool Containment

Separate read, write, and destructive tools by policy. Grant the least privilege the task can tolerate. The workflow should not discover at runtime that a soft boundary was really no boundary at all.

### Boundary 3: Approval And Irreversibility

Require deterministic checks and human approval wherever the action is financially meaningful, legally sensitive, destructive, or reputationally expensive. Approval is part of the action boundary, not an embarrassing fallback.

### Boundary 4: Retrieval And Memory Hygiene

Version, curate, audit, and monitor durable stores. Memory and retrieval are capability layers, but they are also attack surfaces. A store that the workflow can write and later trust without controls is already unsafe.

### Boundary 5: Inter-Agent Skepticism

Treat messages, files, screenshots, and other artifacts crossing agent boundaries as another untrusted input channel. Structured handoffs help, but structure does not create trust by itself.

### Boundary 6: Verification

Run explicit verification for outputs whose errors could become actions, durable memory, or downstream instruction. Verification reduces unsupported claims. It does not replace trust separation, containment, or approval design.

## Escalate When

- The agent reads external content and can later trigger side effects.
- Tool permissions widen from read-only toward write, execution, or account access.
- Retrieval becomes broader, more open, or more multi-tenant.
- The workflow writes durable memory or shared knowledge that later influences action.
- Several agents exchange files, screenshots, or multimodal observations.
- The system executes code, writes files, or changes external system state.

## Alternatives And When They Win

| Control | Best use | Why it wins | Main risk if missing |
| --- | --- | --- | --- |
| Trust separation | untrusted content and retrieval | stops data from silently becoming instruction | indirect prompt injection and authority collapse |
| Tool containment | tool-using workflows | reduces blast radius with least privilege | broad side effects and unsafe execution |
| Approval gates | high-impact actions | creates accountable review before consequence | irreversible mistakes by default |
| Retrieval and memory hygiene | RAG and durable memory | reduces poisoning, drift, and stale authority | corrupted or jammed grounding |
| Inter-agent skepticism | multi-agent handoffs | blocks silent contamination across roles | unsafe internal propagation |
| Verification | factual or high-value outputs | reduces unchecked error propagation | brittle claims turning into action |

## What To Measure

- Injection resistance under realistic content flows
- Tool-risk behavior in sandboxed or emulated scenarios
- Retrieval poisoning and jamming resilience
- Excessive-permission exposure
- Approval-bypass rate
- Cross-agent contamination under shared artifacts
- Incident replay quality and root-cause clarity

A workflow that has never been stressed at these interfaces is not ready for confident deployment.

## Failure Review

- Mixing retrieved content and instructions in one undifferentiated prompt
- Treating internal corpora as automatically trustworthy
- Letting the agent write to the same store it later trusts without controls
- Giving one node broad permissions without hard gates
- Assuming extra agents make the workflow safer by default
- Using debate or post hoc monitoring as a substitute for containment

## Reading Sequence

1. `../../essays/safety/05-trust-boundaries-and-agent-safety.md`
2. `../../essays/safety/companion.md`
3. `../../reference/papers/greshake_indirect_prompt_injection.md`
4. `../../reference/papers/injecagent.md`
5. `../../reference/papers/toolemu.md`
6. `../../reference/papers/agentpoison.md`
7. `../../reference/papers/poisonedrag.md`
8. `../../reference/papers/badrag.md`
9. `../../reference/papers/jamming.md`
10. `../../reference/papers/agentsmith.md`
11. `../../reference/papers/chain_of_verification.md`

Return to survey sections `17.1.2`, `17.1.3`, `18.2.1`, `18.2.2`, `19.1`, `19.2`, and `19.3` when the local boundary question expands into the broader threat map.

## Bottom Line

Agent safety is interface design under consequence. The moment the workflow can read untrusted content, preserve state, or act on the world, trust classes, permissions, approval seams, and monitored stores stop being optional. They become the architecture.
