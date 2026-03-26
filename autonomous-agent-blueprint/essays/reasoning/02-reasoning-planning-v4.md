# Operating Agents II: The Lightest Correct Scaffold

A claims-processing agent built with a strong base model and a careful prompt had a task that looked contained: read the claim, check the criteria, return a structured recommendation. In production, the system rarely said anything absurd. It simply skipped one dependency, collapsed several checks into one fluent answer, or treated one missing fact as though it were present. The output looked polished enough to pass a casual read and brittle enough to fail the moment a reviewer checked the file.

The team reacted the way many teams react. They added prompt detail. They tried more context. They discussed a stronger model. None of that touched the real problem because the real problem was not mainly the model's intelligence. The workflow was asking one generation to do the work of several.

A decomposition pass and a verification step cut the obvious misses quickly. What remained was narrower and more useful. Claims tied to live payer status still failed because the workflow was reasoning from stale state rather than forcing a fresh check against the external ledger. The first fix helped. It also exposed the next failure shape. The system had never had one reasoning problem. It had several scaffold problems sitting on top of each other.

That is why most agent writing still explains the wrong thing. It begins with capability talk, model comparisons, context-window size, benchmark rankings. The practical literature says something colder and more useful. Once an agent has to work across time, use tools, recover from partial failure, preserve trust boundaries, or survive review, the decisive questions move outward from the model and into the operating layers around it. The field's serious work on memory, reasoning scaffolds, action surfaces, coordination, and safety has been saying this for some time, but the public conversation still prefers the easier story that better models naturally become better systems.

The practical core is not mainly about model taste. It is about memory, reasoning scaffolds, action surfaces, workflow design, and safety boundaries. The message behind this series is simple: the deployable substance lives in the operating layers.

## Companion Note

This essay presents a focused narrative for a broad audience. For the full technical scope—including what this essay intentionally leaves out, how it maps to the chapter blueprint, and recommended deeper reading—see the [companion note](companion.md).

## Reasoning Failures Are Scaffold Mismatches

When an agent fails, the easiest story to tell is that the model was not smart enough. It is also very often the wrong story. Many production failures that get attributed to capability are really failures of reasoning structure. The task was presented as one step when it was really four. The workflow let the model reason in the abstract when the environment needed to be checked after every move. A plausible first answer was allowed to become an action without a verification stage. A task with one fragile branch was treated as if it required expensive search, while a task with real branching difficulty was forced through a single path and then blamed on the model when that path dead-ended. What fails in those situations is not only the answer. What fails is the scaffold.

That distinction is the single most useful thing the reasoning chapter offers. It turns reasoning from an adjective people attach to model behavior into a design problem with several different answers. Decomposition, ReAct, self-refinement, self-consistency, verification, tree search, and planner handoff are not interchangeable badges of sophistication. They are interventions for different failure shapes. A builder who cannot name the failure shape is usually not ready to choose the method. This is why the blueprint's central rule is so severe and so practical: use the lightest reasoning structure that makes the task reliable. That rule is less exciting than the public mythology around agent cognition, but it is much closer to how dependable systems actually get built.

The first broad distinction is between reasoning that stays inside language and reasoning that is coupled to the world. Plain decomposition, least-to-most prompting, and abstraction-first prompting help when the model is compressing too many dependencies into one answer or latching onto the wrong conceptual frame too early. These methods are often underrated because they do not look glamorous. Yet they frequently solve the most common failure in applied systems: the workflow asked one generation to do the work of several. Ordered subproblems make the hidden structure of the task explicit, and that alone can be enough to raise reliability sharply (Zhou et al.)

The moment the task depends on tools, live state, or environment feedback, however, reasoning has to become a control loop rather than a monologue. [*ReAct*](https://arxiv.org/abs/2210.03629) still matters for exactly this reason. It binds thought to action and observation, which means the model cannot remain trapped inside a narrated plan after the world has already contradicted it. That is the practical boundary between pleasing internal coherence and grounded reasoning. A workflow that keeps reasoning as though the environment obediently matches the model's expectations will often sound sophisticated right up to the point where a real external state change makes the whole chain worthless. ReAct is not merely one reasoning technique among many. In tool-using systems it is often the default architecture until failure analysis proves otherwise (Yao et al.)

This is also where the distinction between reasoning and planning becomes more than philosophical. Reasoning can remain a matter of producing better internal structure. Planning has to propose a sequence of actions that will touch the world, consume resources, and create state. That is why some tasks need more than prompt-level decomposition. They need either a ReAct-style loop that grounds every step, or in rarer cases a formal handoff to a planner when the constraint structure is strong enough to justify it. The practical message is conservative. Most tasks do not need a symbolic planner. Some do. The skill is not in loving formalism or distrusting it. The skill is in knowing when verbal scaffolds have reached their limit and the task's structure demands something stricter.

A second major distinction in the chapter is between generating an answer and deciding whether that answer deserves trust. [*Self-Refine*](https://arxiv.org/abs/2303.17651) matters because it captures a very common class of problems: the first answer is close, but not quite good enough. Maybe it is structurally weak, maybe it omitted a step, maybe the argument is directionally right but underspecified. In those settings a critique-and-revise loop can improve quality cheaply. [*Reflexion*](https://arxiv.org/abs/2303.11366) stretches that same idea across attempts by storing lessons from failure. Those are real techniques and often useful ones. But the chapter is strongest when it refuses to stop there. Many important tasks do not merely need refinement. They need verification. If an answer makes factual claims that will influence downstream decisions or actions, then the workflow should not rely on the same generative act that produced the claim to certify it silently (Madaan et al.; Shinn et al.)

That is why [*Chain-of-Verification*](https://arxiv.org/abs/2309.11495) is such an important paper in practical agent work. It makes verification explicit. Draft the answer. Generate questions that would challenge its claims. Answer those separately. Revise the result after the checking stage. What matters here is not only the method. What matters is the architectural move. The workflow stops pretending that a coherent first answer is entitled to trust. Instead it creates a dedicated place where trust has to be earned. This is one of the clearest ways to keep reasoning and reliability from being collapsed into the same unexamined performance (Dhuliawala et al.)

[*Self-Consistency*](https://arxiv.org/abs/2203.11171) sits slightly to the side of that argument. It does not verify against the world or against evidence. It samples several traces and looks for convergence. That is useful when the underlying task is stable enough that multiple correct paths tend to agree, and when the cost of additional traces is acceptable. It is much less useful when the main issue is stale evidence, missing observation, or weak task structure.

[*Tree of Thoughts*](https://arxiv.org/abs/2305.10601) and [*LATS*](https://arxiv.org/abs/2310.04406) matter because they make a case for treating some tasks as genuine search problems rather than as single-trace reasoning tasks. That is a real contribution. Some workflows do contain branching structure, multiple plausible paths, and dead ends that cannot be handled by simple decomposition or one-pass deliberation. These methods deserve their place in the chapter because they answer that class of problem directly (Yao et al.; Zhou et al.)

Their practical danger is overapplication. Search-heavy methods are expensive, operationally heavy, and easy to admire for the wrong reasons. Teams often invoke them as a sign of sophistication before proving that the task actually contains the kind of branching difficulty that would justify the cost. The right lesson is not that search is hype. The right lesson is that search belongs late.

The explanatory gap the blueprint leaves mostly implicit is that every reasoning method also creates a governance pattern. Decomposition produces intermediate artifacts that can be inspected. ReAct makes the world legible after every move. Verification creates a formal challenge stage. Self-refinement creates a controlled internal critic. Search creates many alternative paths whose selection criteria must be justified. Formal planning creates a translation boundary between language and structured state. Each method therefore changes not only quality but also the shape of review. This is why reasoning architecture belongs in a practical discussion of agents rather than in an abstract discussion of cognition. The moment a reasoning scaffold changes what evidence exists, what intermediate state is visible, and where a human or another system could intervene, it has become part of system design.

## Practically Speaking: Scaffold Chooser

| Failure shape | First scaffold | Why it comes first | Escalate only if |
|---------------|----------------|--------------------|------------------|
| Several checks get compressed into one answer | Decomposition | Hidden dependencies become explicit intermediate work | The task still fails after subproblems are legible |
| The plan ignores live state, tool results, or current context | ReAct loop | Reasoning proceeds from observation instead of expectation | The environment has real branching difficulty |
| The system states claims confidently and then acts on them | Verification before action | Expensive errors are caught at the edge where they matter | Verification still leaves several plausible paths |
| One input yields unstable answers across attempts | Self-consistency | Variance itself becomes measurable and reducible | External grounding is the real bottleneck |
| One plausible path often dead-ends | Tree search or LATS | Search explores alternatives only when alternatives matter | The search cost outweighs the improvement |

**The discipline:** Name the failure shape before choosing the method. The cheapest correct scaffold is almost always simpler than you expect.

## Escalation Spine

**Start with decomposition.** If the system is compressing multiple dependencies into one answer, break the task into ordered subproblems. Use [*Least-to-Most Prompting*](https://arxiv.org/abs/2205.10625) to make hidden structure explicit. This is the most common fix and the most underrated.

**Add a ReAct loop next.** Once tools or live state matter, reasoning must be grounded. Use [*ReAct*](https://arxiv.org/abs/2210.03629) as the default control loop: reason, act, observe, continue from what actually came back. Without this, the system remains inside a narrated plan while the world contradicts it.

**Add verification before action.** If claims become actions or high-confidence artifacts, install [*Chain-of-Verification*](https://arxiv.org/abs/2309.11495): draft → generate challenging questions → answer separately → revise. Verification is not polish; it is the part of the reasoning loop that closes the trust circuit.

**Optionally add self-consistency.** If the same input yields unstable answers across attempts, use [*Self-Consistency*](https://arxiv.org/abs/2203.11171) to sample multiple traces and look for convergence. Only when variance itself is the bottleneck.

**Late and rare: add search.** Use [*Tree of Thoughts*](https://arxiv.org/abs/2305.10601) or [*LATS*](https://arxiv.org/abs/2310.04406) only after decomposition, grounding, and verification are already in place, and only when failure analysis still points to genuine branching difficulty. Search does not fix shallow task breakdown, missing environmental grounding, or absent verification.

**Even rarer: formal planners.** Methods like [*LLM+P*](https://arxiv.org/abs/2304.11477) become worthwhile only when the task has strong constraint structure that language scaffolds cannot capture.

The default reasoning stack for most production agents is therefore: **decompose → ReAct → verify**. Add self-consistency or search only when the failure analysis demands them.

## What to Skip (For Now)

**Out of scope for the deployable center:**

- **Heavy search as default.** Tree search is expensive and operationally heavy. Reach for it only after cheaper scaffolds fail to solve a genuine branching problem.
- **Abstraction-first methods** like [*Step-Back Prompting*](https://arxiv.org/abs/2310.06117) unless the model is reasoning at the wrong conceptual level. These are useful escalations, not starting points.
- **Formal planners** ([*LLM+P*](https://arxiv.org/abs/2304.11477)) unless your task has strong symbolic constraints that justify a translation to formal planning language.
- **Self-refinement as substitute for verification.** You can refine a weak answer into a cleaner weak answer if the system lacks evidence or grounding. Verification is the boundary where trust gets earned, not just expressed.
- **Reasoning as an independent performance metric.** The goal is not to produce elaborate thoughts. The goal is to produce reliable outcomes. Elaborate reasoning that does not change failure shape is theater.

**If you find yourself adding complexity, ask:** What failure shape is this addressing? Have I already exhausted decomposition, grounding, and verification? Or am I reaching for sophistication before diagnosing the problem?

## Resources And References

### [Builder Blueprint: Reasoning and Planning](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md)

This blueprint matters because it turns the essay's diagnosis-first argument into a concrete chooser for decomposition, tool-grounded loops, verification overlays, and late-stage search.

### [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) (2022)

ReAct remains the control-loop paper because it solves a problem that many newer methods still inherit. Language models are dangerously good at narrating plans that have not survived contact with the world. ReAct breaks that pattern by interleaving reasoning, action, and observation so that the next step must answer to what actually happened rather than to what the model expected to happen (Yao et al.)

Its strength is architectural rather than merely benchmark-based. It gives builders a disciplined loop they can attach to tools, web state, code execution, and external documents. That is why it is hard to replace as the practical default. Its limitation is that it does not verify truth claims by itself and does not solve weak tool boundaries. But those are reasons to complement it, not reasons to demote it.

### [Least-to-Most Prompting Enables Complex Reasoning in Large Language Models](https://arxiv.org/abs/2205.10625) (2022)

Least-to-Most matters because it turns decomposition from advice into a method. The paper is valuable not because it proves that breaking work into steps can help. Everyone vaguely knows that. It matters because it shows how ordered subproblems can change performance on tasks that were previously too difficult when posed as one monolithic jump (Zhou et al.)

That contribution is more durable than the specific benchmark context. In practical systems, ordered decomposition often does more work than another round of model shopping because it prevents hidden dependencies from being silently compressed into one answer. Its limitation is equally clear. It does not ground reasoning in live state. It is therefore strongest before or alongside ReAct, not in place of it.

### [Chain-of-Verification Reduces Hallucination in Large Language Models](https://arxiv.org/abs/2309.11495) (2023)

Chain-of-Verification matters because it takes a vague norm that everyone endorses in principle and turns it into a concrete workflow. Of course we should verify important claims. The useful question is where verification sits, what it asks, and how it influences the final answer. The paper's real contribution is therefore topological. It gives verification its own stage instead of allowing it to remain an implicit hope embedded inside the original generation (Dhuliawala et al.)

That matters far beyond hallucination reduction. It creates a reusable control pattern for any workflow where a plausible answer is not good enough. The method is not a full safety architecture and does not protect against poisoned evidence on its own. But it is one of the cleanest ways to keep the system from confusing first-pass coherence with justified trust.

### [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171) (2022)

Self-Consistency matters because it addresses brittle single-pass reasoning without requiring a completely different scaffold. It samples multiple reasoning traces and selects the answer that appears most frequently. That is useful when the underlying task is stable enough that multiple correct paths tend to converge, and when added latency is acceptable. It is much less useful when the main failure modes are stale evidence, missing observation, or weak task decomposition.

### [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601) (2023) and [Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models](https://arxiv.org/abs/2310.04406) (2023)

Tree of Thoughts and LATS matter because they make a case for treating some tasks as genuine search problems rather than as single-trace reasoning tasks. That is a real contribution. Some workflows do contain branching structure, multiple plausible paths, and dead ends that cannot be handled by simple decomposition or one-pass deliberation. These methods deserve their place because they answer that class of problem directly (Yao et al.; Zhou et al.)

Their practical danger is overapplication. Search-heavy methods are expensive, operationally heavy, and easy to admire for the wrong reasons. Teams often invoke them as a sign of sophistication before proving that the task actually contains the kind of branching difficulty that would justify the cost. The right lesson is not that search is hype. The right lesson is that search belongs late—after decomposition, grounding, and verification are already working.

### [Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models](https://arxiv.org/abs/2310.06117) (2023) and [LLM+P: Empowering Large Language Models with Optimal Planning Proficiency](https://arxiv.org/abs/2304.11477) (2023)

Step-Back Prompting and LLM+P are useful because they show two different escalation directions once the default scaffold is no longer enough. Step-Back Prompting is a cheap abstraction reset. It helps when the model is reasoning at the wrong conceptual level. LLM+P goes the other way and hands structure to a formal planner when the task is strong enough in constraints and symbolic organization that language alone becomes the wrong substrate (Zhou et al.; Liu et al.)

Taken together, they show that "better reasoning" is not one direction of travel. Sometimes the task needs more abstraction. Sometimes it needs more formal structure. The practical virtue of the blueprint is that it keeps both moves available without pretending either one is the default.
