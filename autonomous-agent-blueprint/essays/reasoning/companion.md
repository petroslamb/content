# Operating Agents II Companion: Reasoning, Planning, and the Broader Scaffold Map

This note is the breadth layer behind [Operating Agents II](../reasoning/02-reasoning-planning-v4.md). The essay deliberately turns the chapter into a diagnosis framework: failure shape first, scaffold second. That is the right argumentative center for the series. This note restores the wider reasoning and planning terrain around it.

## What This Essay Argues

The essay's claim is that most production reasoning failures are scaffold failures. It narrows the chapter to the lightest practical chooser: decomposition, ReAct, verification, self-consistency where needed, and search only when branching difficulty is real.

That is a strong public cut. It is also narrower than the chapter.

## What The Distilled Chapter Also Covers

The relevant distilled layer is [Chapter 2 in the practical chapters guide](../../reference/chapters-guide.md) and the matching [reasoning and planning blueprint](../../core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md).

| Distilled guide anchor | What it adds beyond the essay |
|---|---|
| `2.2.2 Dynamic Reasoning Structures` | The broader family of iterative and reactive reasoning patterns. |
| `2.2.2.2 Static Reasoning Structures` | A wider taxonomy than the essay's diagnosis frame explicitly names. |
| `2.2.3 Unstructured Reasoning` | Acknowledges looser reasoning styles the essay mostly sidelines. |
| `2.2.4 Planning` | Formalizes the shift from answer reasoning to action sequencing. |
| `Self-Refine`, `Step Back`, `LLM+P` | Useful patterns the essay acknowledges only lightly or leaves to the companion layer. |

The guide is broader than the essay on purpose. The essay keeps the methods that most clearly support conservative scaffold choice. The guide keeps a wider menu.

## What The Full Survey Covers Beyond That

The fuller survey frame lives in [*Advances and Challenges in Foundation Agents*](../../advances-and-challenges-in-foundation-agents.md), primarily in Chapter `2`.

| Survey section | Why it matters |
|---|---|
| `2.2.1 A Unified Formulation of Reasoning` | The formal taxonomy the essay does not try to reproduce. |
| `2.2.2 Dynamic Reasoning Structures` | The wider iterative and search-heavy family beyond the essay's defaults. |
| `2.2.2.2 Static Reasoning Structures` | The fuller static-method picture. |
| `2.2.3 Unstructured Reasoning` | Broader reasoning styles not central to the essay. |
| `2.2.4 Planning` | The part of the chapter that matters most if your real problem is action sequencing rather than answer quality. |

The essay underplays three things the source material treats more broadly: self-refinement loops, abstraction-first methods such as step-back prompting, and formal planning handoff methods such as LLM+P.

## What This Essay Leaves Out On Purpose

The essay does not try to give a balanced survey of every reasoning method in the chapter. It intentionally deprioritizes taxonomy for its own sake, the unified formalism, and broader planning formalisms that matter more when the task is already structurally strong enough to justify them.

That cut is deliberate. The point of the essay is not to teach the whole chapter. It is to stop teams from misdiagnosing scaffold problems as intelligence problems.

## How To Read The Broader Material Without Losing The Plot

Use the broader chapter to widen the chooser, not to erase it.

The right sequence is:

1. Keep the essay's failure-shape diagnosis as the main decision rule.
2. Add the missing near-practical patterns from the guide: self-refine, step-back, formal-planning handoff.
3. Only then widen into the survey's fuller taxonomy and planning material.
4. Return to the blueprint when the real question becomes implementation order rather than conceptual coverage.

If you reverse that order, the chapter starts looking like a menu again, which is exactly what the essay was written to prevent.

## Recommended Reading Path In This Repo

1. Re-read [Operating Agents II](../reasoning/02-reasoning-planning-v4.md).
2. Read the reasoning and planning section in [foundation-agents-practical-chapters-guide.md](../../reference/chapters-guide.md), especially the material around `2.2.2`, `2.2.3`, and `2.2.4`.
3. Read [Chapter 2 Blueprint: Reasoning and Planning](../../core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md).
4. Read the relevant survey sections in [advances-and-challenges-in-foundation-agents.md](../../advances-and-challenges-in-foundation-agents.md): `2.2.1`, `2.2.2`, `2.2.3`, and `2.2.4`.
5. Then go to the paper notes that widen the essay's cut:
   [react.md](../../reference/papers/react.md),
   [least_to_most_prompting.md](../../reference/papers/least_to_most_prompting.md),
   [self_consistency.md](../../reference/papers/self_consistency.md),
   [self_refine.md](../../reference/papers/self_refine.md),
   [step_back_prompting.md](../../reference/papers/step_back_prompting.md),
   [chain_of_verification.md](../../reference/papers/chain_of_verification.md),
   [llm_plus_p.md](../../reference/papers/llm_plus_p.md),
   [tree_of_thoughts.md](../../reference/papers/tree_of_thoughts.md),
   and [lats.md](../../reference/papers/lats.md).
