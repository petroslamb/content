# Operating Agents I Companion: Action, Tool Use, and the Broader Action Chapter

This note is the breadth layer behind [Operating Agents I](../action/01-action-tool-use-v4.md). The essay deliberately takes the digital practical cut of the action chapter. That is the right public emphasis. This note restores the wider chapter and survey terrain for the reader who wants the whole picture.

## What This Essay Argues

The essay's controlling claim is that the step from assistant to agent is not a model upgrade. It is the moment language becomes accountable state change. From there it narrows quickly to the action surfaces most relevant to real software systems: typed APIs, code execution, SQL, browser automation, and GUI fallback. It also treats tool use as a seam problem rather than one blurry capability.

That is a good cut. It already captures most of the practical core.

## What The Distilled Chapter Also Covers

The relevant distilled layer is [Chapter 8 in the practical chapters guide](../../reference/chapters-guide.md) and the matching [action blueprint](../../core/practical-chapter-blueprints/03-action-tool-use-blueprint.md).

| Distilled guide anchor | What it adds beyond the essay |
|---|---|
| `8.3.1 Action Space Paradigm` | Puts plain text, code, and tool use inside a broader action-representation ladder. |
| `8.3.2 Action Learning Paradigm` | Adds the question of how agents acquire or improve action policies, not just which surface they use. |
| `8.3.3 Tool-Based Action Paradigm` | Covers tool use more broadly than the essay's enterprise-digital cut. |
| language, digital, and physical framing | Reminds the reader that the chapter is about action generally, even if the practical near-term value sits in digital systems. |

The essay already captures the strongest deployable part of this material. What it does not try to do is survey action learning as a research area or treat physical action as a serious near-term default for builders.

## What The Full Survey Covers Beyond That

The fuller survey frame sits in [*Advances and Challenges in Foundation Agents*](../../advances-and-challenges-in-foundation-agents.md), primarily in Chapter `8`.

| Survey section | Why it matters |
|---|---|
| `8.1 The Human Action System` | Biological framing the essay intentionally skips. |
| `8.2 From Human Action to Agentic Action` | A broader transition story than the essay's production-interface framing. |
| `8.3.1 Action Space Paradigm` | The complete action-space taxonomy across language, digital, and physical action. |
| `8.3.2 Action Learning Paradigm` | The part of the chapter most underrepresented in the essay. |
| `8.3.3 Tool-Based Action Paradigm` | A broader tool-use landscape including orchestration and multimodal control. |
| `8.4 Action and Perception: Outside-In or Inside-Out` | Perception-action coupling that the public essay mostly leaves implicit. |

If you want the full source picture, the missing terrain is not mainly "better examples." It is action learning, multimodal orchestration, and the broader relation between action and perception.

## What This Essay Leaves Out On Purpose

The essay does not try to cover physical-world action, robotics-style control, or a balanced review of action-learning methods. It also treats multimodal orchestration and general computer-use work as secondary to the cleaner software surfaces that actually dominate current enterprise value.

That is not an accident. The point of the essay is to install a stronger default: structured digital action first, broader and weaker surfaces only when the environment forces them.

## How To Read The Broader Material Without Losing The Plot

Do not use the broader chapter to weaken the essay's main point. Use it to locate where the essay chose to stop.

The best reading sequence is:

1. Keep the essay's production definition of agency.
2. Widen outward to the action-space paradigm in the guide.
3. Widen further to action learning and perception-action coupling in the survey.
4. Return to the blueprint if your real question is implementation, not literature breadth.

That keeps the practical center intact while letting the broader research picture sit around it.

## Recommended Reading Path In This Repo

1. Re-read [Operating Agents I](../action/01-action-tool-use-v4.md).
2. Read the action section in [foundation-agents-practical-chapters-guide.md](../../reference/chapters-guide.md), especially the material around `8.3.1`, `8.3.2`, and `8.3.3`.
3. Read [Chapter 8 Blueprint: Action Systems and Tool Use](../../core/practical-chapter-blueprints/03-action-tool-use-blueprint.md).
4. Read the relevant survey sections in [advances-and-challenges-in-foundation-agents.md](../../advances-and-challenges-in-foundation-agents.md): `8.1`, `8.2`, `8.3.1`, `8.3.2`, `8.3.3`, and `8.4`.
5. Then go to the paper notes that match the missing breadth:
   [toolformer.md](../../reference/papers/toolformer.md),
   [gorilla.md](../../reference/papers/gorilla.md),
   [hugginggpt.md](../../reference/papers/hugginggpt.md),
   [webagent.md](../../reference/papers/webagent.md),
   [mind2web.md](../../reference/papers/mind2web.md),
   [mobile_agent.md](../../reference/papers/mobile_agent.md),
   [appagent.md](../../reference/papers/appagent.md),
   [omniparser.md](../../reference/papers/omniparser.md),
   [swe_agent.md](../../reference/papers/swe_agent.md),
   [bird.md](../../reference/papers/bird.md),
   and [spider_2_0.md](../../reference/papers/spider_2_0.md).
