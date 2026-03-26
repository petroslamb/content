# Operating Agents IV Companion: Multi-Agent Design Beyond the Three-Problems Thesis

This note is the breadth layer behind [Operating Agents IV](../multi-agent/04-multi-agent-v4.md). The essay deliberately centers one claim: multi-agent systems solve three different problems, and most bad multi-agent systems are built by confusing them. That is a strong public thesis. This note restores the broader topology, protocol, and evaluation terrain around it.

## What This Essay Argues

The essay argues that serious multi-agent systems should be read through three lenses: role separation, reliability through critique, and task decomposition through artifact handoffs. It uses that split to make the default much stricter: one agent first, then split only when the second agent buys a real boundary.

That is the chapter's strongest practical move, but it is not the whole chapter.

## What The Distilled Chapter Also Covers

The relevant distilled layer is [Chapter 14 in the practical chapters guide](../../reference/chapters-guide.md) and the matching [multi-agent blueprint](../../core/practical-chapter-blueprints/05-multi-agent-design-blueprint.md).

| Distilled guide anchor | What it adds beyond the essay |
|---|---|
| `14.1.2 Heterogeneous Agents` | A broader role-splitting frame than the essay's anti-theater lens. |
| `14.2.1 Static Topologies` | Topology shape as a design choice, not just a byproduct of the three-problems thesis. |
| `14.3.4 Task-oriented Interaction` | The part of the guide most aligned with the essay's artifact-handoff argument. |
| `14.4 Human-Agent Collaboration` | Human supervision as a first-class workflow component. |
| `14.5 Decision-Making in Multi-Agent Systems` | Consensus and aggregation logic beyond simple critique. |
| `14.6.1` and `14.6.3` | Message types and protocol layers that the essay only gestures toward. |

The guide is wider than the essay on topologies, messages, and decision processes. The essay is tighter on why the split should exist at all.

## What The Full Survey Covers Beyond That

The fuller survey frame lives in [*Advances and Challenges in Foundation Agents*](../../advances-and-challenges-in-foundation-agents.md), especially across Chapters `13` to `16`.

| Survey section | Why it matters |
|---|---|
| `13 The Framework and Categories of Multi-Agent Systems` | The larger conceptual frame the essay intentionally avoids. |
| `13.1.2 From Single Agent to Multi-Agent Systems` | The transition logic before Chapter `14` gets concrete. |
| `14.2 Multi-Agent System Topologies` | Broader topology choices than the essay explicitly names. |
| `14.5 Decision-Making in Multi-Agent Systems` | More formal decision and consensus material. |
| `14.6 Communication Protocols in Multi-Agent Systems` | The protocol surface most underrepresented in the essay. |
| `15 Collective Intelligence and Adaptation` | Emergent or society-style material the essay deliberately deprioritizes. |
| `16 Evaluating Multi-Agent Systems` | Evaluation breadth the essay leaves mostly to the repo's review checklist. |

If you want the full source picture, the missing terrain is not the core split itself. It is the larger topology, protocol, collective-intelligence, and evaluation framing around that split.

## What This Essay Leaves Out On Purpose

The essay does not try to be a balanced treatment of multi-agent topologies, common protocol layers, or collective-intelligence theory. It also does not let "agent society" material onto the main stage. Instead it privileges task-oriented interaction, artifact contracts, and human accountability because those are the parts most likely to matter in current real systems.

That cut is deliberate. It is what keeps the public essay from turning into a vague celebration of many-agent complexity.

## How To Read The Broader Material Without Losing The Plot

Start with the essay's three-problems thesis and keep it. Then widen outward in this order: human collaboration, topology choices, message and protocol design, and only then the broader conceptual and collective-intelligence chapters.

That sequence matters. If you start from the society-scale framing, the essay will look too narrow. If you start from the workflow-decomposition problem, the broader material becomes legible without taking over the center.

## Recommended Reading Path In This Repo

1. Re-read [Operating Agents IV](../multi-agent/04-multi-agent-v4.md).
2. Read the multi-agent section in [foundation-agents-practical-chapters-guide.md](../../reference/chapters-guide.md), especially the material around `14.3.4`, `14.4`, `14.5`, and `14.6`.
3. Read [Chapter 14 Blueprint: Multi-Agent Design](../../core/practical-chapter-blueprints/05-multi-agent-design-blueprint.md).
4. Read the relevant survey sections in [advances-and-challenges-in-foundation-agents.md](../../advances-and-challenges-in-foundation-agents.md): `13.1.2`, `14.2`, `14.5`, `14.6`, and then `15` and `16` if you want the fuller surrounding picture.
5. Then go to the paper notes:
   [metagpt.md](../../reference/papers/metagpt.md),
   [chatdev.md](../../reference/papers/chatdev.md),
   [autogen.md](../../reference/papers/autogen.md),
   [mad.md](../../reference/papers/mad.md),
   and [reconcile.md](../../reference/papers/reconcile.md).
