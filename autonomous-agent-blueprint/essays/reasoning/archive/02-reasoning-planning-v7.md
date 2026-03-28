# Operating Agents III: Diagnose the Scaffold Before You Shop the Model

Read with: [Reasoning Companion](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/reasoning/companion-v7.md) and [Reasoning Blueprint](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md).

The recommendation looked careful. It quoted the exception clause, summarized the claim, named the likely payer outcome, and returned a clean structured decision. The reviewer rejected it in less than a minute. One required check was missing, and the workflow had never queried live payer status before drafting the answer.

Nothing in the output looked absurd. That was the problem. It was polished enough to pass a casual read and brittle enough to fail the moment somebody asked whether the workflow had earned its confidence.

The team reacted the way many teams react. They added prompt detail. They tried more context. They discussed a stronger model. None of that touched the real problem because the real problem was not mainly the model's intelligence. The workflow was asking one generation to do the work of several.

Most production reasoning failures are control failures before they are intelligence failures.

## Start With The Failure Shape

The easiest way to waste time in agent design is to answer the wrong failure with a more impressive method. A workflow skips a dependency, so the team reaches for search. It hallucinates on live state, so they add critique. It produces unstable answers, so they stretch the prompt and call it planning. The result is usually not more intelligence. It is more machinery wrapped around a diagnosis error.

The decision rule is colder than that. Diagnose the failure shape first, then install the lightest scaffold that corrects it.

If the system keeps compressing dependent checks into one answer, the first fix is decomposition. If it keeps reasoning as though the environment will obediently match its expectations, the first fix is a reason-act-observe loop. If a plausible answer is becoming consequence before it has earned trust, the first fix is verification. If the workflow keeps failing because order itself is the risk, the plan has to become a first-class object. Only when those simpler layers are already working and the task still contains real branching difficulty does search begin to earn its cost.

That selection logic is the argument of the chapter. Not the prestige order of methods. The choice discipline.

## Decomposition Before Brilliance

*Least-to-Most Prompting* mattered because it solved a problem builders still underrate. Many tasks arrive wrapped as one judgment even though they are structurally several judgments with dependencies. Eligibility before exception. Evidence before synthesis. Current state before recommendation. If the workflow is allowed to improvise those stages inside one generation, it can sound coherent while silently skipping the task's actual structure.

The paper's durable move was to externalize the sequence of subproblems before the model tried to solve the whole thing at once. That is more than a prompting trick. It is an architectural intervention. It separates "discover the task structure" from "execute the task." The workflow stops pretending that a multi-stage problem is a one-stage act of eloquence.

Decomposition is often the most undervalued repair in the stack because it does not look glamorous. It does something better. It makes hidden dependencies visible enough to inspect.

## ReAct When The World Can Contradict You

The moment the task depends on tools, live records, code, or environment state, reasoning has to stop being a monologue and become a control loop.

*ReAct* remains the control-loop paper because it attacked exactly that boundary. Chain-of-thought prompting had shown that models could narrate reasoning. What it could not do was keep that reasoning answerable to a world that could contradict it. ReAct bound thought to action and observation so the next step had to proceed from what actually happened rather than from what the model expected to happen.

That distinction still explains a large share of production failure. A workflow that keeps reasoning in prose while the real state lives in a ledger, browser, database, or tool result is not mainly suffering from weak intelligence. It is suffering from a broken loop. The model is being asked to reason from fiction.

ReAct belongs before heavier overlays in most practical stacks. If the environment matters, the world gets a vote.

## Verification Before Consequence

Many workflows do not merely need better answers. They need answers that deserve consequence.

*Chain-of-Verification* mattered because it gave that requirement a real place in the workflow. Draft the answer. Generate the questions that would challenge it. Answer those separately. Revise only after the checking stage. The contribution was topological before it was stylistic.

That move stops the first generation from silently certifying itself. A coherent answer may still be wrong. A polished recommendation may still be unsupported. Verification creates a stage where trust has to be earned rather than merely implied.

This is the failure shape many teams misread as reasoning weakness. The problem is often not that the draft was too stupid. The problem is that the draft was allowed to become consequential before anybody asked it hard questions.

## Planning Begins At Commitment Points

Reasoning and planning are adjacent but not interchangeable. A system can reason entirely inside language. Planning becomes a different engineering job when commitment points inside the workflow start carrying the risk.

A claim can be routed before eligibility is confirmed. An appeal can be drafted before the denial code is verified. A field visit can be scheduled before the account state is refreshed. In those cases the problem is not only that the answer is weak. The problem is that the order of operations is smuggling risk into the workflow.

That is where planner handoff belongs. Most teams should stay conservative and keep the plan in inspectable language for as long as possible. Some tasks stop being about better local reasoning and start being about whether the sequence itself respects prerequisites, scarce resources, and irreversible steps. *LLM+P* marks that escalation boundary. The lesson is not that every hard task wants a formal planner. It is that verbal scaffolds have a limit, and builders need a rule for noticing when they have reached it.

Planning begins when sequence itself becomes the risk.

## Search Owes A Specific Debt

Search-heavy methods matter because some tasks really do branch. They have several plausible paths, real dead ends, and choices that simpler scaffolds cannot resolve cleanly. That is the genuine contribution of work such as *Tree of Thoughts*.

They also attract one of the field's most persistent diagnosis errors. Teams often invoke search as a sign that they are taking reasoning seriously before they have proved that the task contains the kind of branching difficulty that would justify the cost.

Search does not fix weak decomposition. It does not fix missing observation. It does not fix absent verification. If those layers are still weak, search mostly magnifies confusion and latency at the same time.

The escalation rule should stay severe. Decompose first. Then ground the workflow in live state. Then verify before consequence. Then promote the plan when commitment points are the problem. Only after that should search enter the picture, and only if branching difficulty still remains.

If one generation is doing the work of several, a better model only buys a more polished mistake.

## Selected Sources

[Least-to-Most Prompting](https://arxiv.org/abs/2205.10625). Least-to-Most matters because it shows why decomposition is not the baby version of reasoning. It is the paper behind the doctrine's first move: expose dependent subproblems before asking one generation to improvise the whole structure.

[ReAct](https://arxiv.org/abs/2210.03629). ReAct matters because it binds reasoning to action and observation. The chapter's control-first view of reasoning owes a great deal to that move. A workflow that depends on live state but still reasons in prose is disconnected from reality.

[Chain-of-Verification](https://arxiv.org/abs/2309.11495). CoVe matters because it gives verification a real place in the workflow instead of leaving it as a vague norm. Trust should be earned in a distinct stage, not implied by the fluency of the first answer.

[LLM+P](https://arxiv.org/abs/2304.11477). LLM+P matters because it marks the point where sequence itself becomes the risk. The paper's importance here is not frontier breadth. It is the escalation rule it implies: promote the plan into a first-class object only when prose can no longer carry the constraints safely.

[Tree of Thoughts](https://arxiv.org/abs/2305.10601). Tree of Thoughts matters in this doctrine mostly as a boundary marker. It clarifies what true branching search is for and, by contrast, what it is not for. Search belongs late, after decomposition, grounding, and verification are already doing their jobs.

For the broader terrain this essay leaves out on purpose, read the [Reasoning Companion](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/reasoning/companion-v7.md). For the operator layer, chooser logic, and escalation defaults, read the [Reasoning Blueprint](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md).
