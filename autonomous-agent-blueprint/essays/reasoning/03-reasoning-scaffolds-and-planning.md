# Operating Agents III: Reasoning Scaffolds and Planning

*Part of the Operating Agents series, a builder-first run on how modern agent systems actually work once language leaves the prompt and starts acting inside software.*

#### Video TL;DR

[AI Reasoning Builder's Guide](./artifacts/video/AI%20Reasoning%20Builder%27s%20Guide.mp4)

Reasoning comes after action and memory because a workflow with tools and durable state can still fail under a bad scaffold. The hard question is not whether the model can think at length. It is whether the loop knows when to think, what evidence to inspect, and when to stop.

![Slide 1: Reasoning and Planning Architectures](./artifacts/slides/Reasoning%20Architectures/slide-001.png)

The recommendation looked careful. It quoted the exception clause, summarized the claim, named the likely payer outcome, and returned a clean structured decision. The reviewer rejected it in less than a minute. One required check was missing, and the workflow had never queried live payer status before drafting the answer.

Nothing in the output looked absurd. That was the problem. It was polished enough to pass a casual read and brittle enough to fail the moment somebody asked whether the workflow had earned its confidence.

The team reacted the way many teams react. They added prompt detail. They tried more context. They discussed a stronger model. None of that touched the real problem because the real problem was not mainly the model's intelligence. The workflow was asking one generation to do the work of several.

Most production reasoning failures are control failures before they are intelligence failures.

That is the reasoning distillation taken here from the broader [foundation-agents survey](https://arxiv.org/abs/2504.01990) and sharpened in the local [reasoning blueprint](../../core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md). The transcript gives the prose its order, but the core claim is operational: many reasoning failures are really workflow failures in disguise.

![Slide 2: The Model Is Not Always the Problem](./artifacts/slides/Reasoning%20Architectures/slide-002.png)

## Start With The Failure Shape

The easiest way to waste time in agent design is to answer the wrong failure with a more impressive method. A workflow skips a dependency, so the team reaches for search. It hallucinates on live state, so they add critique. It produces unstable answers, so they stretch the prompt and call it planning. The result is usually not more intelligence. It is more machinery wrapped around a diagnosis error.

The decision rule is colder than that. Diagnose the failure shape first, then install the lightest scaffold that corrects it.

![Slide 3: The Escalation](./artifacts/slides/Reasoning%20Architectures/slide-003.png)

If the system keeps compressing dependent checks into one answer, the first fix is decomposition. If it keeps reasoning as though the environment will obediently match its expectations, the first fix is a reason-act-observe loop. If a plausible answer is becoming consequence before it has earned trust, the first fix is verification. If the workflow keeps failing because order itself is the risk, the plan has to become a first-class object. Only when those simpler layers are already working and the task still contains real branching difficulty does search begin to earn its cost.

That selection logic is the argument of the chapter. Not the prestige order of methods. The choice discipline.

## Decomposition Before Brilliance

[*Least-to-Most Prompting*](https://arxiv.org/abs/2205.10625) mattered because it solved a problem builders still underrate. Many tasks arrive wrapped as one judgment even though they are structurally several judgments with dependencies. Eligibility before exception. Evidence before synthesis. Current state before recommendation. If the workflow is allowed to improvise those stages inside one generation, it can sound coherent while silently skipping the task's actual structure.

The paper's durable move was to externalize the sequence of subproblems before the model tried to solve the whole thing at once. That is more than a prompting trick. It is an architectural intervention. It separates "discover the task structure" from "execute the task." The workflow stops pretending that a multi-stage problem is a one-stage act of eloquence.

![Slide 4: The Default Reasoning Blueprint](./artifacts/slides/Reasoning%20Architectures/slide-004.png)

Decomposition is often the most undervalued repair in the stack because it does not look glamorous. It does something better. It makes hidden dependencies visible enough to inspect.

![Slide 5: Structural Decomposition](./artifacts/slides/Reasoning%20Architectures/slide-005.png)

## ReAct When The World Can Contradict You

The moment the task depends on tools, live records, code, or environment state, reasoning has to stop being a monologue and become a control loop.

[*ReAct*](https://arxiv.org/abs/2210.03629) remains the control-loop paper because it attacked exactly that boundary. Chain-of-thought prompting had shown that models could narrate reasoning. What it could not do was keep that reasoning answerable to a world that could contradict it. ReAct bound thought to action and observation so the next step had to proceed from what actually happened rather than from what the model expected to happen.

![Slide 6: Grounding with ReAct](./artifacts/slides/Reasoning%20Architectures/slide-006.png)

That distinction still explains a large share of production failure. A workflow that keeps reasoning in prose while the real state lives in a ledger, browser, database, or tool result is not mainly suffering from weak intelligence. It is suffering from a broken loop. The model is being asked to reason from fiction.

ReAct belongs before heavier overlays in most practical stacks. If the environment matters, the world gets a vote.

## Verification Before Consequence

Many workflows do not merely need better answers. They need answers that deserve consequence.

[*Chain-of-Verification*](https://arxiv.org/abs/2309.11495) mattered because it gave that requirement a real place in the workflow. Draft the answer. Generate the questions that would challenge it. Answer those separately. Revise only after the checking stage. The contribution was topological before it was stylistic.

![Slide 8: Chain-of-Verification](./artifacts/slides/Reasoning%20Architectures/slide-008.png)

That move stops the first generation from silently certifying itself. A coherent answer may still be wrong. A polished recommendation may still be unsupported. Verification creates a stage where trust has to be earned rather than merely implied.

This is the failure shape many teams misread as reasoning weakness. The problem is often not that the draft was too stupid. The problem is that the draft was allowed to become consequential before anybody asked it hard questions.

## Planning Begins At Commitment Points

Reasoning and planning are adjacent but not interchangeable. A system can reason entirely inside language. Planning becomes a different engineering job when commitment points inside the workflow start carrying the risk.

A claim can be routed before eligibility is confirmed. An appeal can be drafted before the denial code is verified. A field visit can be scheduled before the account state is refreshed. In those cases the problem is not only that the answer is weak. The problem is that the order of operations is smuggling risk into the workflow.

That is where planner handoff belongs. Most teams should stay conservative and keep the plan in inspectable language for as long as possible. Some tasks stop being about better local reasoning and start being about whether the sequence itself respects prerequisites, scarce resources, and irreversible steps. [*LLM+P*](https://arxiv.org/abs/2304.11477) marks that escalation boundary. The lesson is not that every hard task wants a formal planner. It is that verbal scaffolds have a limit, and builders need a rule for noticing when they have reached it.

Planning begins when sequence itself becomes the risk.

![Slide 11: Reasoning Is an Architectural Menu](./artifacts/slides/Reasoning%20Architectures/slide-011.png)

## Search Owes A Specific Debt

Search-heavy methods matter because some tasks really do branch. They have several plausible paths, real dead ends, and choices that simpler scaffolds cannot resolve cleanly. That is the genuine contribution of work such as [*Tree of Thoughts*](https://arxiv.org/abs/2305.10601).

They also attract one of the field's most persistent diagnosis errors. Teams often invoke search as a sign that they are taking reasoning seriously before they have proved that the task contains the kind of branching difficulty that would justify the cost.

Search does not fix weak decomposition. It does not fix missing observation. It does not fix absent verification. If those layers are still weak, search mostly magnifies confusion and latency at the same time.

![Slide 10: Search and Escalation](./artifacts/slides/Reasoning%20Architectures/slide-010.png)

The escalation rule should stay severe. Decompose first. Then ground the workflow in live state. Then verify before consequence. Then promote the plan when commitment points are the problem. Only after that should search enter the picture, and only if branching difficulty still remains.

If one generation is doing the work of several, a better model only buys a more polished mistake.

![Slide 15: Evaluating the Reasoning Stack](./artifacts/slides/Reasoning%20Architectures/slide-015.png)

![Slide 16: Architectural Anti-Patterns](./artifacts/slides/Reasoning%20Architectures/slide-016.png)

## References

[Advances and Challenges in Foundation Agents: From Brain-Inspired Intelligence to Evolutionary, Collaborative, and Safe Systems](../../advances-and-challenges-in-foundation-agents.md) ([arXiv](https://arxiv.org/abs/2504.01990)) is the source booklet from which this chapter was ultimately distilled. Its key contribution is breadth. It places reasoning inside the larger operating stack of action, memory, coordination, safety, and optimization. This essay narrows that broader survey into one practical argument: the hardest part of reasoning in production is often not intelligence itself but the scaffold that decides when evidence is gathered, when checks happen, and when sequence becomes binding.

[Chapter 7 Blueprint: Reasoning Scaffolds and Planning](../../core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md) is the builder-facing backbone for this chapter. Its key contribution is diagnostic discipline. It turns the literature into an escalation rule: decompose first, then ground the loop in live state, then verify before consequence, then promote the plan when sequence becomes risky, and only then pay for search.

[Reasoning scaffolds for reliable AI agents transcript](./artifacts/transcript_Reasoning%20scaffolds%20for%20reliable%20AI%20agents_full.txt) is the direct narrative source behind this draft. Its key contribution is the sequence the essay follows: failure-shape diagnosis, decomposition, ReAct-style control loops, explicit verification, planner escalation, and the late entry of search once simpler fixes have already been exhausted.

[*Least-to-Most Prompting*](https://arxiv.org/abs/2205.10625) matters because it shows why decomposition is not the baby version of reasoning. Its key contribution is exposing dependent subproblems before asking one generation to improvise the whole structure. This essay leans on that move to treat decomposition as an architectural repair rather than as a prompting trick.

[*ReAct*](https://arxiv.org/abs/2210.03629) matters because it binds reasoning to action and observation. Its key contribution is making the world part of the loop instead of leaving the model alone with its expectations. That is why this essay treats grounding as a control requirement whenever the workflow depends on live state.

[*Chain-of-Verification*](https://arxiv.org/abs/2309.11495) matters because it gives verification an explicit place in the workflow rather than leaving it as a vague norm. Its key contribution is staging trust. A draft answer should not certify itself merely by sounding coherent. This essay uses that idea to separate answer production from consequence.

[*LLM+P*](https://arxiv.org/abs/2304.11477) matters because it marks the point where sequence itself becomes the risk. Its key contribution is showing when a plan has to become a first-class object rather than a soft implication inside prose. That is the escalation boundary this essay cares about.

[*Tree of Thoughts*](https://arxiv.org/abs/2305.10601) matters here mostly as a boundary marker. Its key contribution is clarifying what real branching search is for and, by contrast, what it cannot repair. Search belongs late, after decomposition, grounding, and verification are already doing their jobs.

![Slide 17: Use the Lightest Structure That Works](./artifacts/slides/Reasoning%20Architectures/slide-017.png)
