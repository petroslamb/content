# Operating Agents: Preface

![Operating Agents Preface Cover](./preface-cover-v3.png)

This course is a builder-first guide to how modern agent systems are designed, evaluated, and constrained in practice. It is not trying to explain every direction in agent research, and it is not trying to turn the field into a sequence of slogans. Its purpose is narrower and more useful. It aims to teach what a serious builder needs in order to inspect a real workflow, identify what layer is failing, and choose the right level of intervention.

The package was distilled from the broader survey [*Advances and Challenges in Foundation Agents*](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/advances-and-challenges-in-foundation-agents.md). That survey is wide by design. It covers memory, reasoning, action, optimization, collaboration, safety, and much more. This course takes the practical center of that larger landscape and turns it into a teaching sequence. The essays teach the operating problem. The companions widen the field. The blueprints turn the lesson into a builder-facing decision guide. The paper notes preserve the deeper source layer for readers who want to study the literature directly.

## Who This Course Is For

This course is for serious builders, technical operators, and researchers who want deployable understanding rather than hype. It is written for readers who expect to review or ship agent workflows in real systems, where the questions are about state, interfaces, authority, evaluation, failure handling, and cost. The target reader does not need to be a specialist in every part of the literature, but they do need to care about how the system behaves once language leaves the prompt and starts interacting with software, memory, people, and policy.

It is also useful for readers who already know the surface vocabulary of the field but want a cleaner map of how the pieces fit together. Many people have seen the names of the methods and the demo categories. Far fewer have a stable model of which layer each method belongs to, what failure it is meant to address, and when it should not be the first tool reached for.

This course is not a beginner overview of AI. It is not a framework tutorial. It is not a collection of demos dressed up as architecture. The package assumes the reader wants operational judgment: the ability to say what kind of system this is, what part of it deserves attention, and what standard should be used to decide whether a change actually improved it.

## What You Should Be Able To Do After Reading

By the end of the course, a reader should be able to inspect an agent workflow and locate the layer where the main problem lives. That means distinguishing a memory problem from a reasoning problem, a reasoning problem from an action-interface problem, a collaboration problem from a safety-boundary problem, and a workflow-quality problem from an evaluation problem. The outcome is not abstract familiarity with agent terminology. The outcome is the ability to read a system and judge what it needs next.

In practical terms, the reader should be able to:

1. review a live or proposed agent workflow and identify which architectural layer is carrying the failure
2. choose the right chapter and matching blueprint for the problem at hand
3. use the companion to widen the map when the main chapter is too narrow for the case
4. know which papers deserve escalation once the local design question is clear

That is the standard the package is trying to meet. If a reader finishes the course and still cannot review a workflow that they may need to inspect next week, the course is not doing its job.

## How The Course Is Organized

The public course has six sections, presented in this order.

- **[Action](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/action/01-action-tool-use.md)** explains what changes when language gains the ability to produce bounded state change through tools, code, data systems, browsers, and other software interfaces.
- **[Memory](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/memory/02-memory-systems-and-authority.md)** explains how an agent should carry information across time without turning the past into an ungoverned source of present authority.
- **[Reasoning](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/reasoning/03-reasoning-scaffolds-and-planning.md)** explains how tasks should be structured, grounded, checked, and escalated when a single fluent pass is not enough.
- **[Multi-Agent](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/multi-agent/04-multi-agent-boundaries-and-handoffs.md)** explains when one workflow should become several roles and what kind of handoff makes that split real rather than theatrical.
- **[Safety](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/safety/05-trust-boundaries-and-agent-safety.md)** explains where control can be lost once the system can read untrusted input, remember durable state, call tools, and exchange artifacts.
- **[Optimization](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/optimization/06-workflow-optimization-and-evaluation.md)** explains how to improve the workflow once it works at all, and why the workflow rather than the prompt becomes the true object of optimization.

Optimization is intentionally treated as a bonus module. It assumes the earlier layers already exist in recognizable form. A workflow cannot be optimized responsibly before its memory, reasoning, action, coordination, and safety surfaces are clear enough to evaluate.

## How To Use The Course Surfaces

The package separates teaching, architecture, and literature so that each surface can stay readable.

The core essays are the public teaching layer. Each one is meant to stand on its own as a course chapter, explain the operating problem in clear prose, and give the reader a practical method rather than a pile of citations.

The companions are second-pass breadth chapters. They exist because the main essays should stay tight. A good core chapter teaches the practical center. A good companion widens the field, explains adjacent taxonomies and edge cases, and shows the reader how to use the literature without overwhelming the main path.

The current companion layer is:

- Action: [Companion](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/action/companion.md)
- Memory: [Companion](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/memory/companion.md)
- Reasoning: [Companion](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/reasoning/companion.md)
- Multi-Agent: [Companion](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/multi-agent/companion.md)
- Safety: [Companion](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/safety/companion.md)
- Optimization: [Companion](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/optimization/companion.md)

The blueprints are the practical implementation and review layer. They take the topic out of chapter form and turn it into a builder-facing decision guide. A reader who knows the problem but needs defaults, escalation rules, failure modes, and evaluation criteria should move from the essay and companion into the matching blueprint.

The matching blueprint set is:

- Action: [Chapter 8 Blueprint: Action Systems and Tool Use](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/03-action-tool-use-blueprint.md)
- Memory: [Chapter 3 Blueprint: Memory Systems and Authority](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/01-memory-blueprint.md)
- Reasoning: [Chapter 2 Blueprint: Reasoning Scaffolds and Planning](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md)
- Multi-Agent: [Chapter 14 Blueprint: Multi-Agent Boundaries and Handoffs](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/05-multi-agent-design-blueprint.md)
- Safety: [Chapter 19 Blueprint: Trust Boundaries and Agent Safety](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/06-safety-blueprint.md)
- Optimization: [Chapter 9 Blueprint: Workflow Optimization and Evaluation](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/04-optimization-self-improvement-blueprint.md)

The original survey is the source landscape from which this course was distilled. It is where the larger taxonomy lives and where the full breadth of the field remains visible. The course uses that breadth selectively, keeping the parts that matter most for deployable systems while preserving the survey as the deeper map behind the public teaching layer.

The paper notes remain the source-audit layer. They are where a reader goes once the local design question is clear and the next step is no longer orientation but close study of the underlying work.

## Two Orders Matter

Two different orders organize this package, and they serve different purposes.

The public essay order is for teaching. It opens with action because action makes the boundary between assistant and agent visible at once. From there the course moves into memory, reasoning, multi-agent design, safety, and optimization. This sequence is meant to help the reader form a stable picture of the operating system they are studying.

The blueprint order is for architectural dependency. In `core/practical-chapter-blueprints/`, the sequence runs memory, reasoning, action, optimization, multi-agent, and safety. That order reflects the engineering dependency chain. A long-running system first needs persistence rules. Then it needs task structure. Then it needs action surfaces. Then it becomes worth improving. Only after that do coordination choices and full deployment boundaries come into view.

The public sequence is for teaching. The blueprint order is for architectural dependency. The course keeps both visible because hiding one of them would make the package harder to use. A reader should be able to learn the field in the public order while still understanding why the underlying builder stack is arranged differently.

## How To Read This Package Well

The cleanest study loop is simple.

1. Read the essay first to understand the operating problem and the practical center of the chapter.
2. Read the companion next if you need the wider field map, the omitted taxonomies, or a better guide to the surrounding literature.
3. Read the matching blueprint when the question becomes architectural or operational and you need defaults, escalation rules, or evaluation criteria.
4. Return to the survey or the paper notes only after the design question is specific enough that deeper reading will answer something concrete.

Readers do not need to move linearly through the whole package every time. If the immediate task is a workflow review, it is often better to start with the chapter that matches the bottleneck, then use the companion and blueprint as depth layers. The course is structured so that this kind of targeted reading is possible without losing the larger map.

The standard behind all of this is plain and demanding. The package favors bounded workflows over theatrical autonomy, explicit evaluation over decorative traces, typed memory over undifferentiated retention, strict action surfaces over vague intent, conservative multi-agent escalation over agent proliferation, and safety as architecture rather than as a soft suffix. If the course does its job, the reader should leave with something more durable than a list of methods. They should leave with a way to inspect agent systems soberly, name what matters in them, and improve them without confusing motion for progress.
