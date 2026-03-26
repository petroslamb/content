# Operating Agents V Companion: Safety Beyond the Interface-Architecture Spine

This note is the breadth layer behind [Operating Agents V](../safety/05-safety-v4.md). The essay takes one hard line: agent safety is interface architecture. That is a strong and useful public thesis. This note restores the broader safety terrain in the distilled guide and the original survey.

## What This Essay Argues

The essay argues that the same interfaces that make agents useful also define their attack surface. It therefore centers indirect prompt injection, poisoned retrieval and memory, unsafe tools, inter-agent contamination, and approval boundaries. That is the right practical center for a public builder essay.

It is also narrower than the full safety material behind it.

## What The Distilled Chapter Also Covers

The relevant distilled layer is the safety section in [foundation-agents-practical-chapters-guide.md](../../reference/chapters-guide.md) and the matching [safety blueprint](../../core/practical-chapter-blueprints/06-safety-blueprint.md).

| Distilled guide anchor | What it adds beyond the essay |
|---|---|
| `17.1.2 Prompt Injection Attacks` | The conceptual core the essay foregrounds. |
| `17.1.3 Hallucination Risks` | Factual brittleness as a safety issue, not just a quality issue. |
| `18.2.1 Supply Chain Attacks` | Broader non-brain-module risk than the essay spells out. |
| `18.2.2 Risks in Tool Usage` | A wider tool-risk frame than the essay's least-privilege emphasis alone. |
| `19.1 Agent-Memory Interaction Threats` | Memory as an attack surface, not only a capability layer. |
| `19.2 Agent-Environment Interaction Threats` | Environment-facing risk beyond the essay's chosen examples. |
| `19.3 Agent-Agent Interaction Threats` | The broader inter-agent threat surface. |

The guide is broader on hallucination, supply-chain risk, and the full split across brain, non-brain, and extrinsic interaction threats. The essay is tighter on the boundary-centered parts most relevant to current deployment practice.

## What The Full Survey Covers Beyond That

The fuller survey frame lives in [*Advances and Challenges in Foundation Agents*](../../advances-and-challenges-in-foundation-agents.md), primarily in Chapters `17`, `18`, and `19`, with Chapter `20` as adjacent context.

| Survey section | Why it matters |
|---|---|
| `17.1.2 Prompt Injection Attacks` | The strongest conceptual source for the essay's trust-separation argument. |
| `17.1.3 Hallucination Risks` | A safety concern the essay acknowledges but does not dwell on. |
| `18.1 Perception Safety Threats` | Broader non-language input risk the essay mostly leaves outside the frame. |
| `18.2.1 Supply Chain Attacks` | Dependency and tooling-chain risk beyond direct tool misuse. |
| `18.2.2 Risks in Tool Usage` | Wider action-module threat surface. |
| `19.1`, `19.2`, `19.3` | Memory, environment, and agent-agent interaction threats. |
| `20 Superalignment and Safety Scaling Law in AI Agents` | Adjacent context the essay intentionally does not center. |

The essay is strongest on injection, retrieval, handoffs, and approval. The broader survey also wants you to think about hallucination, perception, supply-chain exposure, and the larger safety-scaling conversation.

## What This Essay Leaves Out On Purpose

The essay does not try to cover the full alignment and superalignment discourse, safety-scaling-law work, or a balanced review of every class of intrinsic and extrinsic safety risk. It also does not let hallucination or perception safety dominate the piece, because that would weaken its central claim about interfaces and trust boundaries.

That cut is deliberate. The point of the essay is to make current builders stop treating safety as a suffix prompt.

## How To Read The Broader Material Without Losing The Plot

Keep the essay's interface-architecture frame first. Then widen outward in layers.

First add hallucination and tool-module risk. Then add perception and supply-chain material. Then widen to the full agent-memory, agent-environment, and agent-agent split. Only after that should you read the Chapter `20` safety-scaling context, because it is more useful once the concrete surfaces are already clear.

That sequence keeps the practical center intact while restoring the fuller survey picture.

## Recommended Reading Path In This Repo

1. Re-read [Operating Agents V](../safety/05-safety-v4.md).
2. Read the safety section in [foundation-agents-practical-chapters-guide.md](../../reference/chapters-guide.md), especially the material around `17.1.2`, `17.1.3`, `18.2.1`, `18.2.2`, `19.1`, `19.2`, and `19.3`.
3. Read [Chapters 17, 18, and 19 Blueprint: Safety](../../core/practical-chapter-blueprints/06-safety-blueprint.md).
4. Read the relevant survey sections in [advances-and-challenges-in-foundation-agents.md](../../advances-and-challenges-in-foundation-agents.md): `17.1.2`, `17.1.3`, `18.1`, `18.2.1`, `18.2.2`, `19.1`, `19.2`, and `19.3`. Then read `20` only if you want the larger alignment and safety-scaling context.
5. Then go to the paper notes:
   [greshake_indirect_prompt_injection.md](../../reference/papers/greshake_indirect_prompt_injection.md),
   [injecagent.md](../../reference/papers/injecagent.md),
   [toolemu.md](../../reference/papers/toolemu.md),
   [agentpoison.md](../../reference/papers/agentpoison.md),
   [poisonedrag.md](../../reference/papers/poisonedrag.md),
   [badrag.md](../../reference/papers/badrag.md),
   [jamming.md](../../reference/papers/jamming.md),
   [agentsmith.md](../../reference/papers/agentsmith.md),
   and [chain_of_verification.md](../../reference/papers/chain_of_verification.md).
