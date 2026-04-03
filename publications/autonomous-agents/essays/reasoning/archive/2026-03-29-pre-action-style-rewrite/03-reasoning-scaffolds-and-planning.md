# Operating Agents III: Reasoning Scaffolds and Planning

*Part of the Operating Agents series, a builder-first run on how modern agent systems actually work once language leaves the prompt and starts acting inside software.*

#### Video TL;DR

[AI Reasoning Builder's Guide](artifacts/video/AI%20Reasoning%20Builder%27s%20Guide.mp4)

The easiest way to misread an agent failure is to blame the model first. The workflow loops, skips a dependency, hallucinates a parameter, or writes a polished answer that collapses the moment live state pushes back, and the reflex is to say the base model was not smart enough. The transcript for this chapter starts by attacking that reflex directly. In a large share of production failures, the model is not the primary defect. The workflow is missing the scaffold that would have decomposed the task, queried the world, checked the draft, or escalated only when the task truly required heavier search. That is the reasoning claim carried here from the broader [foundation-agents survey](https://arxiv.org/abs/2504.01990), tightened in the local [reasoning blueprint](../../core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md), and recast through the transcript's sequence.

![Slide 2: The model is not always the problem](artifacts/slides/Reasoning%20Architectures/slide-002.png)

## The Failure Builders Misdiagnose

The transcript opens with a useful inversion. Teams do not usually under-engineer these systems because they lack methods. They under-engineer them because they misdiagnose the problem. A workflow fails on a live task and the response is usually more prompt detail, more context, or a stronger model. Those can help at the margin, but they do not answer the deeper question of what kind of reasoning failure actually happened. Did the workflow compress several dependent checks into one draft. Did it reason inside language when the relevant state lived in a tool. Did it let the first generation certify itself. Did it face real branching complexity or merely a missing sequence of bounded steps. Once those questions are asked, the topic stops looking like "reasoning" in the abstract and starts looking like control design.

That is why the transcript keeps returning to cost and latency. The point is not to admire the full taxonomy of reasoning methods. It is to choose the lightest structure that reliably solves the task. A builder who defaults to the most elaborate scaffold is making the same mistake as the builder who defaults to one giant prompt. Both are refusing diagnosis. One under-builds. The other burns money to hide that it never named the failure shape correctly.

## Reasoning Ends Where Planning Begins

The first hard split in the transcript is the one between reasoning and planning. Reasoning is verbal problem solving that stays inside the model's own processing loop. Planning begins when the system has to sequence operations against a world that can refuse, drift, or surprise it. That distinction matters because static context windows and dynamic environments obey different laws. A model can produce an elegant proof, a plausible migration plan, or a clean recommendation entirely inside language. The minute the server returns a dependency clash or the database answers with a null the architecture changes shape. Now the system has to act, observe, compare expected state with actual state, and choose again.

![Slide 3: Reasoning versus planning](artifacts/slides/Reasoning%20Architectures/slide-003.png)

The transcript phrases this as a move away from treating the model like a bag of prompts and toward treating it like an engineering menu. That is the right frame. Builders do not need one giant reasoning trick. They need a small set of methods with clear selection rules. Some tasks are solved by bounded decomposition. Some need a thought-action-observation loop. Some need a separate checking stage. Some need search or a formal planner. The mistake is not only choosing the wrong method. It is failing to notice when verbal reasoning has already reached its boundary and sequence under uncertainty has begun.

## The Default Loop

Once the reasoning/planning split is clear, the transcript becomes very concrete. The default baseline is two-part: decomposition first, then a reason-act-observe loop. Decomposition matters because many hard tasks are not one judgment at all. They are several dependent judgments that teams keep asking one generation to improvise in a single pass. That is why papers like [*Least-to-Most Prompting*](https://arxiv.org/abs/2205.10625) still matter. Their contribution is not rhetorical. They externalize the order of subproblems before the model is allowed to synthesize an answer. The task stops pretending to be one act of eloquence.

![Slide 4: The default reasoning blueprint](artifacts/slides/Reasoning%20Architectures/slide-004.png)

The transcript also pulls in [*Take a Step Back*](https://arxiv.org/abs/2310.06117), and that is a good reminder that some failures are conceptual before they are local. A model can fail not because it lacks the machinery to compute the answer, but because it jumped too quickly into local detail without first recovering the governing principle. That is why decomposition in this chapter is broader than task splitting. Sometimes the repair is to restore abstraction before execution. A workflow that cannot tell whether it needs subgoals or a conceptual reset will keep paying for heavier methods it never needed.

![Slide 5: Decomposition and abstraction](artifacts/slides/Reasoning%20Architectures/slide-005.png)

The second stage is the [*ReAct*](https://arxiv.org/abs/2210.03629) loop. This is the point where reasoning stops being a monologue. Thought leads to action. Action produces observation. Observation constrains the next thought. The force of ReAct is not that it made models more articulate. It made them answerable to the environment. If the task depends on tools, live records, code execution, browsers, or APIs, the loop has to proceed from what actually happened rather than from what the model expected to happen. That is why the transcript treats ReAct as the operational bridge between reasoning and planning. It is the first place where the world gets a vote.

![Slide 6: ReAct as the operational backbone](artifacts/slides/Reasoning%20Architectures/slide-006.png)

## Overlays For Weak First Passes

The baseline loop still leaves a hard problem in place. Even when the environment is wired in correctly, first-pass reasoning can be weak. A parameter gets hallucinated. A draft is almost right but malformed. A failure recurs across attempts. A factual synthesis sounds confident and is still wrong. The transcript's next move is useful because it separates these failure modes instead of treating them as one generic need for "more reasoning."

[*Self-Refine*](https://arxiv.org/abs/2303.17651) belongs first because it is the cheapest overlay in the stack. It assumes the output is structurally close and that localized critique will fix the miss. That is a different job from rebuilding the workflow. It is a near-miss repair loop, not a replacement for grounding. The transcript is careful on this point. Self-refine is appropriate when the draft needs a correction in syntax, structure, or clarity, not when the whole answer was born unmoored from the task.

[*Reflexion*](https://arxiv.org/abs/2303.11366) changes the temporal scope. The critique does not die with the current attempt. It becomes a stored lesson that can shape the next run. That matters whenever the environment provides clear success or failure signals and the task repeats often enough for lessons to compound. In that sense the chapter is already leaning toward memory. A reasoning scaffold can become smarter over time, but only if failure is turned into an explicit, inspectable object rather than disappearing into the log.

![Slide 7: Self-Refine and Reflexion](artifacts/slides/Reasoning%20Architectures/slide-007.png)

The transcript treats [*Chain-of-Verification*](https://arxiv.org/abs/2309.11495) as the most important factual-safety overlay, and that emphasis is deserved. The reason is mechanical. A model that has just spent hundreds of tokens defending a mistaken claim is statistically pulled toward agreement with its own draft. Asking it to "double check" inside the same context does not create independence. It creates a polite restatement of the same error. CoVe matters because it isolates the check. Claims are extracted, turned into separate questions, and sent into fresh contexts that do not inherit the draft's momentum. Verification becomes a different stage with a different topology.

![Slide 8: Chain-of-Verification](artifacts/slides/Reasoning%20Architectures/slide-008.png)

That separation is the real lesson. Verification before consequence is not a stylistic preference. It is a way of preventing the first answer from quietly certifying itself. Once the transcript reaches financial disclosures, medical summaries, or any other pipeline that can trigger irreversible downstream action, the argument sharpens. Generation and verification should not share one undifferentiated context and pretend that is enough. They need a boundary between them.

## When Search Finally Earns Its Cost

Only after the baseline and the overlays are in place does the transcript move into the expensive escalations. That order matters. Search methods are not the serious version of reasoning. They are a costly answer to specific failure shapes that simpler scaffolds cannot resolve. [*Self-Consistency*](https://arxiv.org/abs/2203.11171) is the first escalation because it attacks brittleness statistically. If one reasoning trace is too fragile, sample several, let them diverge, and take the consensus. That works well when the task has a definite answer but small variances early in the trace can derail the whole solution.

![Slide 9: Self-Consistency](artifacts/slides/Reasoning%20Architectures/slide-009.png)

The price is obvious and the transcript does not soften it. Parallel traces multiply cost and latency directly. That means self-consistency belongs in places where correctness dominates responsiveness, not in every user-facing flow. The value of the method is not that it is clever. It is that it gives builders a way to spend extra compute only when variance, rather than structure, is the thing actually breaking the task.

The heavier turn arrives with [*Tree of Thoughts*](https://arxiv.org/abs/2305.10601), [*LATS*](https://arxiv.org/abs/2310.04406), and [*LLM+P*](https://arxiv.org/abs/2304.11477). These methods matter because some tasks really do branch. They have dead ends, alternative routes, constraints, and order effects that a single linear trace cannot manage. Tree of Thoughts explores the branches explicitly. LATS pushes further by combining search with environmental feedback. LLM+P makes a different move and hands the formal planning burden to a classical solver after the language model translates the task into a planning representation. The transcript's point is not that these methods are excessive in the abstract. It is that they are excessive by default.

![Slide 10: Search-heavy escalation](artifacts/slides/Reasoning%20Architectures/slide-010.png)

That is one of the strongest parts of the chapter. The model is not the only thing teams overestimate. They also overestimate the dignity of heavyweight search. If the task is a mostly deterministic pipeline and bounded decomposition already maps the route, adding tree search is not sophistication. It is orchestration overhead disguised as ambition.

## The Discipline Is Selection

The transcript resolves into a build order rather than a taxonomy. Start with decomposition and ReAct. Add verification before irreversible actions. Use self-refine where outputs are near misses. Add self-consistency only when accuracy needs justify the multiple traces. Escalate to search only when the task still contains real branching difficulty after the simpler layers are working. That progression is less glamorous than the frontier literature makes the field look, but it is much closer to how robust systems are actually assembled.

![Slide 14: The recommended build order](artifacts/slides/Reasoning%20Architectures/slide-014.png)

```text
decompose -> observe the world -> verify -> refine near misses -> sample only if brittleness remains -> search only if branching remains
```

The anti-pattern section lands because it describes evaluation errors, not merely implementation errors. Builders overuse chains of thought without environmental grounding. They let the model plan actions it cannot actually execute. They confuse a graceful reasoning trace with a valid one. The transcript is especially sharp on that last point. Large language models are built to sound good. If an engineer reads a confident multi-paragraph plan and mistakes fluency for validity, the system has already won the wrong kind of trust.

![Slide 16: Architectural anti-patterns](artifacts/slides/Reasoning%20Architectures/slide-016.png)

That is why the evaluation block belongs at the end. The stack should be judged by post-verification success rate, by whether the plan actually matches the tool and state constraints of the environment, and by latency and token cost per solved task. Not by how intelligent the internal monologue appears. Not by how elaborate the scaffold sounds in a design review. The right architecture is the one that crosses the reliability threshold with the least extra machinery.

![Slide 15: Evaluating the reasoning stack](artifacts/slides/Reasoning%20Architectures/slide-015.png)

The closing claim follows naturally from all of this. Reasoning is not a prestige contest between methods. It is a discipline of restraint. The good builder is not the one who deploys the most advanced paper in the stack. It is the one who can tell when decomposition is enough, when the world needs a vote, when verification must be separate, and when branching search has finally earned the right to exist.

![Slide 17: Use the lightest structure that works](artifacts/slides/Reasoning%20Architectures/slide-017.png)

## References

[Advances and Challenges in Foundation Agents: From Brain-Inspired Intelligence to Evolutionary, Collaborative, and Safe Systems](../../advances-and-challenges-in-foundation-agents.md) ([arXiv](https://arxiv.org/abs/2504.01990)) is the source booklet from which this chapter was ultimately distilled. Its key contribution is scope. It places reasoning inside a larger operating stack that also includes action, memory, coordination, safety, and optimization. This essay narrows that broader survey to one practical claim: many reasoning failures in production are really scaffold failures that were misread as model failures.

[Reasoning and Planning blueprint](../../core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md) is the builder-facing backbone for this chapter. Its key contribution is selection logic. It translates the research into a cheap-first escalation discipline: decompose, ground in the world, verify before consequence, add targeted repair loops, and only then consider consensus sampling or search-heavy planners.

[Reasoning scaffolds for reliable AI agents transcript](artifacts/transcript_Reasoning%20scaffolds%20for%20reliable%20AI%20agents_full.txt) is the direct structural source behind this draft. Its key contribution is order. It begins with the industry's habit of blaming the base model, draws the line between reasoning and planning, installs decomposition and ReAct as the baseline, then adds overlays and expensive escalations only after the simpler scaffold has been made explicit.

[*Least-to-Most Prompting*](https://arxiv.org/abs/2205.10625) matters because it shows that many "reasoning" failures are hidden sequencing failures. Its key contribution is progressive decomposition. Instead of asking one generation to improvise the entire path, it externalizes the subproblems and lets the workflow move through them in order.

[*Take a Step Back*](https://arxiv.org/abs/2310.06117) matters because it identifies a different kind of failure. Sometimes the model has not lost the computation. It has lost the governing abstraction. Its key contribution is the abstraction-first reset, which helps the system recover the right conceptual frame before it dives back into local detail.

[*ReAct*](https://arxiv.org/abs/2210.03629) matters because it forced reasoning back into contact with the environment. Its key contribution is the thought-action-observation loop that keeps the next step answerable to what actually happened rather than to what the model merely expected.

[*Self-Refine*](https://arxiv.org/abs/2303.17651) matters because it gives builders a cheap near-miss repair loop. Its key contribution is not deeper reasoning in the grand sense. It is a practical way to improve outputs that are already close without redesigning the whole controller.

[*Reflexion*](https://arxiv.org/abs/2303.11366) matters because it extends critique across attempts. Its key contribution is turning failure into stored verbal guidance that can shape future runs. That makes it a bridge between reasoning repair and memory policy.

[*Chain-of-Verification*](https://arxiv.org/abs/2309.11495) matters because it turns checking into a separate stage rather than a polite request appended to the original draft. Its key contribution is mechanical separation. The model that generated the claim should not automatically be the only context allowed to validate it.

[*Self-Consistency*](https://arxiv.org/abs/2203.11171) matters because it addresses brittle reasoning traces statistically rather than structurally. Its key contribution is consensus through multiple samples, which can buy real reliability when the task has a correct answer but the path to it is unstable.

[*Tree of Thoughts*](https://arxiv.org/abs/2305.10601) matters because it treats reasoning as a search problem when the task truly contains dead ends and alternative routes. Its key contribution is making branching explicit instead of hiding it inside one linear trace.

[*LATS*](https://arxiv.org/abs/2310.04406) matters because it combines branching search with environmental feedback. Its key contribution is showing what a much heavier reasoning-and-planning controller looks like when search is guided by actual outcomes in the world rather than by language alone.

[*LLM+P*](https://arxiv.org/abs/2304.11477) matters because it makes the handoff to formal planning explicit. Its key contribution is separation of labor. The language model handles semantic translation, while the classical planner handles the constrained search problem the language model was never especially good at solving on its own.
