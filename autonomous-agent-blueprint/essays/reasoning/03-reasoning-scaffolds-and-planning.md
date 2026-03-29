# Operating Agents III: Reasoning Scaffolds and Planning

*Part of the Operating Agents series, a builder-first run on how modern agent systems actually work once language leaves the prompt and starts acting inside software.*

#### Video TL;DR

[AI Reasoning Builder's Guide](./artifacts/video/AI%20Reasoning%20Builder%27s%20Guide.mp4)

## The Failure Builders Often Misread

An agent can produce a polished plan for a refund workflow and still fail as soon as it has to touch live state. It may query the wrong transaction, miss a missing field in the CRM response, misread the policy exception that applies to the case, or neglect to verify the final amount before issuing the action. When teams see that kind of failure, they often jump to the same conclusion: the model was not smart enough. In many cases that diagnosis is incomplete. The failure came from asking one generation to do the work of decomposition, tool interaction, verification, and planning without enough structure around it.

That distinction matters because it changes what the builder is trying to improve. If the problem is purely model capability, the remedy is mostly outside the workflow. If the problem is control, then the remedy lies in the reasoning scaffold: how the task is decomposed, how the environment is consulted, how intermediate steps are checked, and how the system decides whether a more expensive search procedure is warranted. That is the reasoning distillation taken here from the broader [foundation-agents survey](https://arxiv.org/abs/2504.01990) and organized in the local [reasoning blueprint](../../core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md). The practical lesson is simple: many production reasoning failures appear before the limit of intelligence has actually been reached.

![Slide 2: The model is not always the problem](./artifacts/slides/Reasoning%20Architectures/slide-002.png)

The design question, then, is not "which reasoning paper is best." It is "what is the lightest structure that makes this task reliable enough to operate." That question is deliberately conservative. Underbuild the scaffold and the model compresses too much work into one fluent guess. Overbuild it and the system pays unnecessary cost and latency for a task that simpler control would already solve. Mature reasoning design is therefore diagnostic. It starts by identifying the failure shape before selecting the method.

One useful way to teach the topic is to separate three levels of burden. Some tasks need only better decomposition. Some need decomposition plus interaction with a world that can surprise the plan. Some need explicit verification or search because the task remains brittle even after the baseline scaffold is in place. The rest of the chapter follows that escalation path.

## Reasoning, Planning, And The Baseline Scaffold

The first distinction the reader should hold clearly is the difference between reasoning and planning. Reasoning is problem solving that can stay largely inside the model's own context. Planning begins when the workflow has to sequence actions against an external environment that can refuse, drift, or return unexpected state. A model may reason elegantly about the steps of a cloud migration, for example, but once credentials have expired, services differ across environments, or a dependency behaves differently than expected, the problem is no longer a closed-form intellectual exercise. It is an interaction with a live system.

![Slide 3: Reasoning versus planning](./artifacts/slides/Reasoning%20Architectures/slide-003.png)

That is why decomposition is usually the first scaffold worth adding. Many tasks that look like one hard reasoning act are really a chain of smaller judgments that have been packed into a single prompt. Work such as [*Least-to-Most Prompting*](https://arxiv.org/abs/2205.10625) matters because it shows the value of solving subproblems in sequence rather than trusting one large synthesis step. [*Take a Step Back*](https://arxiv.org/abs/2310.06117) matters for a related reason: some failures happen because the model rushes into details before it has recovered the governing principle or frame of the problem. Both papers teach the same operational lesson. If the first pass is doing too much, better structure often helps more than a larger model.

![Slide 4: The default reasoning blueprint](./artifacts/slides/Reasoning%20Architectures/slide-004.png)

For agents that use tools, the baseline scaffold usually needs a second piece in addition to decomposition. It needs a loop that binds later reasoning to external feedback. [*ReAct*](https://arxiv.org/abs/2210.03629) remains so influential because it expresses this clearly: the model forms a thought, takes an action, observes the result, and then continues from the observed state rather than from its original assumption. The value of that structure is not stylistic. It reduces the chance that the workflow continues building on a mistaken internal picture after the environment has already contradicted it.

![Slide 6: ReAct as the operational backbone](./artifacts/slides/Reasoning%20Architectures/slide-006.png)

This gives a good default methodology for most production tasks. First, break the task into bounded subgoals or intermediate artifacts. Second, use a thought-action-observation loop whenever live tools, APIs, or external state are involved. Third, judge the baseline on whether the next step answers to the world rather than only to the model's prior prose. A large share of reasoning failures can be reduced at this stage, before any heavier method becomes necessary.

The practical value of this baseline is easiest to see in tasks that mix reasoning and operations. A refund workflow is a good example. The system has to identify the relevant transaction, retrieve the applicable policy, inspect the exception logic, and only then decide whether action is allowed. That is not one thought. It is a sequence of narrower judgments tied to external evidence. Decomposition and ReAct together create a simple discipline: break apart the logic, touch the world at the relevant seams, and let new observations govern the next step.

## How To Correct A Weak First Pass

Even a sound baseline still leaves several common failure shapes. Sometimes the output is close, but a local mistake remains in formatting, schema, or phrasing. Sometimes the workflow repeats a mistake it should have learned from on a prior attempt. Sometimes the real danger is factual hallucination or unsupported claims inside an otherwise coherent answer. These are different problems and they deserve different correction methods.

Local repair is where [*Self-Refine*](https://arxiv.org/abs/2303.17651) is most useful. The paper is worth reading not because every task needs iterative self-critique, but because it gives a clean pattern for near-miss outputs. If the draft is broadly right and only needs one bounded correction pass, a refinement loop is often cheaper than redesigning the entire workflow. In practice this is common when the system has selected the right tool or policy path but produced malformed code, missed a schema field, or worded a user-facing answer poorly.

Cross-run learning is where [*Reflexion*](https://arxiv.org/abs/2303.11366) becomes more interesting. Its contribution is not simply critique. It is the idea that failure can be written into a reusable lesson that changes later attempts. That matters for agent design because many repeated mistakes are not best solved by making the immediate draft longer or more reflective. They are better solved by preserving a compact lesson such as "this endpoint returns partial records unless expanded" or "this approval path requires finance signoff above a threshold." In that sense, Reflexion sits close to episodic memory. It is reasoning support that persists across runs.

Verification is a third category and it should be taught separately because it solves a different problem. [*Chain-of-Verification*](https://arxiv.org/abs/2309.11495) is important because it does not ask the model merely to "be more careful." It separates generation from checking. Claims are identified, reopened in a fresh context, and compared against source material before the output is allowed to stand. This is the right pattern whenever unsupported factual claims can create real downstream cost. In course terms, this is one of the most important distinctions in the chapter: refinement improves a draft, reflection improves later attempts, and verification checks whether the claims should survive at all.

![Slide 8: Chain-of-Verification](./artifacts/slides/Reasoning%20Architectures/slide-008.png)

This distinction also helps explain why fluent reasoning traces are such weak evidence of correctness. A trace can sound careful and still rely on a nonexistent endpoint, an invalid assumption about the environment, or a policy reading that was never checked against the authoritative source. What matters is not whether the chain of thought sounds like careful human analysis. What matters is whether the workflow forces important claims back through evidence and world state before consequence follows.

A useful methodology at this stage is therefore layered. Start by asking whether the baseline scaffold already separates subgoals and grounds the plan in observations. If it does, then inspect the remaining error. If the problem is a near miss, use local refinement. If the problem recurs across runs, preserve a lesson. If the problem is factual confidence without sufficient checking, isolate verification. This is the kind of structure that helps teams avoid randomly adding "reason harder" prompts to places where a different control is what the workflow actually needs.

## When To Pay For Heavier Search

Only after the baseline and the corrective overlays are working does it make sense to consider more expensive methods. [*Self-Consistency*](https://arxiv.org/abs/2203.11171) is the most accessible example. It samples multiple reasoning traces and selects the answer supported by the strongest agreement. The method is helpful when a single trace is too brittle and when the gain in reliability is worth the added cost. The paper is best read as an answer to variance, not as a default recipe for all difficult tasks.

The search-heavy family goes farther. [*Tree of Thoughts*](https://arxiv.org/abs/2305.10601), [*LATS*](https://arxiv.org/abs/2310.04406), and [*LLM+P*](https://arxiv.org/abs/2304.11477) all explore the idea that some tasks contain genuine branching structure, dead ends, and planning states that linear prompting cannot handle well. Their value is real, but it is easy to misuse them. These papers should be read as escalation references for tasks where branching difficulty has already been demonstrated, not as prestige upgrades for ordinary workflows.

![Slide 10: Search-heavy escalation](./artifacts/slides/Reasoning%20Architectures/slide-010.png)

[LLM+P](https://arxiv.org/abs/2304.11477) is especially useful in a course setting because it teaches an important systems lesson: not every planning burden should stay inside the language model. In some tasks the right move is to let the model formulate the problem, hand the formal part to a classical planner, and then translate the result back into workflow terms. That is a valuable corrective to the habit of treating the language model as the place where every difficulty must be solved.

The build order that follows from all this is straightforward. Begin with decomposition and a thought-action-observation loop. Add verification before high-stakes outputs or irreversible actions. Add local refinement when the workflow is mostly right but misses in a bounded way. Preserve lessons when failure repeats across runs. Use self-consistency when single-trace variance remains high and latency budgets allow it. Escalate to formal or tree-shaped search only when simpler scaffolds have clearly failed on a genuinely branching problem.

![Slide 14: The recommended build order](./artifacts/slides/Reasoning%20Architectures/slide-014.png)

Evaluation should match that build order. Measure solved-task quality after verification, not before it. Measure whether the plan remains coherent once tool feedback enters the loop. Measure latency and token cost per successful task, because a method that cannot live inside the production budget is not a practical win. And measure failure localization: can the team tell whether a miss came from poor decomposition, weak grounding, absent verification, or an overambitious search layer. These metrics make reasoning architecture inspectable rather than impressionistic.

The broader lesson is restrained but durable. Good reasoning design does not mean using the most sophisticated scaffold available. It means selecting the smallest scaffold that makes the task reliable, explainable, and affordable. That is why the topic belongs in a course on operating agents. The useful question for builders is how the workflow should structure thought so that it remains correct once the environment starts answering back.

![Slide 17: Use the lightest structure that works](./artifacts/slides/Reasoning%20Architectures/slide-017.png)

For the broader taxonomy of reasoning methods, planner handoff logic, search escalations, and paper-by-paper reading guidance, continue with the [Reasoning Companion](./companion.md).

## References

[Advances and Challenges in Foundation Agents: From Brain-Inspired Intelligence to Evolutionary, Collaborative, and Safe Systems](../../advances-and-challenges-in-foundation-agents.md) ([arXiv](https://arxiv.org/abs/2504.01990)) is the broad survey behind this series. It is useful here because it places reasoning next to action, memory, optimization, coordination, and safety, which helps the reader see that reasoning scaffolds are one layer of a larger operating system rather than a complete solution on their own.

[Chapter 2 Blueprint: Reasoning and Planning](../../core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md) is the most practical reference to keep nearby while building. It turns the research landscape into a usable escalation path: decompose first, ground with ReAct, verify where necessary, and pay for heavy search only when the task has earned it.

[*Least-to-Most Prompting Enables Complex Reasoning in Large Language Models*](https://arxiv.org/abs/2205.10625) is useful for teaching decomposition. It shows why breaking a problem into smaller sequential steps can outperform one-shot synthesis on multi-step tasks.

[*Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models*](https://arxiv.org/abs/2310.06117) is worth reading when a workflow keeps getting lost in local details. Its value is methodological: recover the governing abstraction before committing to the next narrow step.

[*ReAct: Synergizing Reasoning and Acting in Language Models*](https://arxiv.org/abs/2210.03629) remains the operational backbone for tool-using reasoning. Read it to understand why thought without observation is fragile once the workflow touches a live environment.

[*SELF-REFINE: Iterative Refinement with Self-Feedback*](https://arxiv.org/abs/2303.17651) is a strong reference for local repair. It is most useful when the draft is close and a bounded critique pass is cheaper than redesigning the whole system.

[*Reflexion: Language Agents with Verbal Reinforcement Learning*](https://arxiv.org/abs/2303.11366) matters because it turns failure into a persistent lesson. That makes it one of the better references for reasoning improvements that should survive across attempts.

[*Chain-of-Verification Reduces Hallucination in Large Language Models*](https://arxiv.org/abs/2309.11495) is essential reading for high-stakes factual workflows. Its main lesson is that checking should be separated from drafting, not appended as a vague request for caution.

[*Self-Consistency Improves Chain of Thought Reasoning in Language Models*](https://arxiv.org/abs/2203.11171) is the right reference when a single reasoning trace is too brittle. It teaches when multiple sampled traces are worth the added cost.

[*Tree of Thoughts: Deliberate Problem Solving with Large Language Models*](https://arxiv.org/abs/2305.10601), [*Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models*](https://arxiv.org/abs/2310.04406), and [*LLM+P: Empowering Large Language Models with Optimal Planning Proficiency*](https://arxiv.org/abs/2304.11477) are the heavy-search references in the chapter. Read them to understand when branching difficulty justifies more elaborate search and when it is better to hand part of the problem to a different planning substrate altogether.
