# Operating Agents III: The Lightest Correct Scaffold

A claims-processing agent built with a strong base model and a careful prompt had a task that looked contained: read the claim, check the criteria, return a structured recommendation. In production, the system rarely said anything absurd. It simply skipped one dependency, collapsed several checks into one fluent answer, or treated one missing fact as though it were present. The output looked polished enough to pass a casual read and brittle enough to fail the moment a reviewer checked the file.

The team reacted the way many teams react. They added prompt detail. They tried more context. They discussed a stronger model. None of that touched the real problem because the real problem was not mainly the model's intelligence. The workflow was asking one generation to do the work of several.

A decomposition pass and a verification step cut the obvious misses quickly. What remained was narrower and more useful. Claims tied to live payer status still failed because the workflow was reasoning from stale state rather than forcing a fresh check against the external ledger. The first fix helped. It also exposed the next failure shape. The system had never had one reasoning problem. It had several scaffold problems sitting on top of each other.

Most production reasoning failures are control failures before they are intelligence failures.

## Start With Failure Shape, Not Method Prestige

The easiest way to waste time in agent design is to answer the wrong failure with a more impressive method. A workflow skips a dependency, so the team reaches for search. It hallucinates on live state, so they add critique. It produces unstable answers, so they stretch the prompt and call it planning. The result is usually not more intelligence. It is more machinery wrapped around a diagnosis error.

The practical question is colder. What failure shape exists here, and what is the lightest scaffold that corrects it.

If the system keeps compressing dependent checks into one answer, the first fix is decomposition. If it keeps reasoning as though the environment will obediently match its expectations, the first fix is a reason-act-observe loop. If a plausible answer is becoming an action before it has earned trust, the first fix is verification. If the task must sequence constrained actions under explicit rules, the plan itself may need to become a first-class object. Only when the simpler layers are already working and the task still contains genuine branching difficulty does search begin to earn its cost.

That selection logic is the argument of the chapter. Not the taxonomy. Not the prestige order of methods. The choice discipline.

## Decomposition Comes Before Brilliance

[*Least-to-Most Prompting*](https://arxiv.org/abs/2205.10625) mattered because it solved a problem that builders still underrate. Many tasks arrive wrapped as one judgment even though they are structurally several judgments with dependencies. Eligibility before exception. Evidence before synthesis. Current state before recommendation. If the workflow is allowed to improvise those stages inside one generation, it can sound coherent while silently skipping the task's actual structure.

The paper's durable move was to externalize the sequence of subproblems before the model tried to solve the whole thing at once. That is more than a prompting trick. It is an architectural intervention. It separates "discover the task structure" from "execute the task." The workflow stops pretending that a multi-stage problem is a one-stage act of eloquence.

Decomposition is often the most undervalued repair in the stack. It does not look glamorous. It does something better. It makes hidden dependencies visible enough to inspect.

## ReAct Begins When The World Can Say No

The moment the task depends on tools, live records, code, or environment state, reasoning has to stop being a monologue and become a control loop.

[*ReAct*](https://arxiv.org/abs/2210.03629) remains the control-loop paper because it attacked exactly that boundary. Chain-of-thought prompting had shown that models could narrate reasoning. What it could not do was keep that reasoning answerable to a world that could contradict it. ReAct bound thought to action and observation so the next step had to proceed from what actually happened rather than from what the model expected to happen.

That distinction still explains a large share of production failure. A workflow that keeps reasoning in prose while the real state lives in a ledger, a browser, a database, or a tool result is not mainly suffering from weak intelligence. It is suffering from a broken loop. The model is being asked to reason from fiction.

ReAct belongs before heavier overlays in most practical stacks. If the environment matters, the world gets a vote.

## Verification Changes Where Trust Is Earned

Many workflows do not merely need better answers. They need answers that deserve consequence.

[*Chain-of-Verification*](https://arxiv.org/abs/2309.11495) mattered because it took a vague norm and gave it a place in the workflow. Of course important claims should be checked. The useful question is where the checking happens and whether it is meaningfully different from the act that produced the original answer. The paper's real contribution was topological. Draft the answer. Generate the questions that would challenge it. Answer those separately. Revise only after the checking stage.

That move stops the first generation from silently certifying itself. A coherent answer may still be wrong. A polished recommendation may still be unsupported. Verification creates a stage where trust has to be earned rather than merely implied.

This is the failure shape many teams misread as "reasoning weakness." The problem is often not that the draft was too stupid. The problem is that the draft was allowed to become consequential before anybody asked it hard questions.

## Planning Begins When Sequence Itself Is The Risk

Reasoning and planning are adjacent but not interchangeable. A system can reason entirely inside language. Planning becomes a different engineering job when the order of operations, the use of resources, and the commitment points in the workflow become part of the risk.

That is where planner handoff belongs. Most teams should stay conservative and keep the plan in inspectable language for as long as possible. Some tasks, however, stop being about better local reasoning and start being about whether the sequence itself respects hard constraints.

[*LLM+P*](https://arxiv.org/abs/2304.11477) marks that escalation boundary. The paper was trying to solve tasks whose constraint structure was strong enough that prose alone had become the wrong substrate. Its lesson is not that every hard task wants a formal planner. Its lesson is that verbal scaffolds have a limit, and builders need a rule for noticing when they have reached it.

The rule is practical. If the workflow keeps failing because prerequisites stay implicit, commitment points arrive too early, or constraints remain buried in prose, the sequence itself has become the risk. That is the moment planning begins.

## Search Belongs Late

Search-heavy methods matter because some tasks really do branch. They have several plausible paths, real dead ends, and choices that simpler scaffolds cannot resolve cleanly.

That is the contribution of work such as [*Tree of Thoughts*](https://arxiv.org/abs/2305.10601) and the later search-heavy planner family. They defend a real class of task. They also attract one of the field's most persistent diagnosis errors. Teams often invoke search as a sign that they are taking reasoning seriously before they have proved that the task actually contains the kind of branching difficulty that would justify the cost.

Search does not fix weak decomposition. It does not fix missing observation. It does not fix absent verification. If those layers are still weak, search mostly magnifies confusion and latency at the same time.

The escalation rule stays severe: decompose, ground, verify, promote the plan when sequence itself becomes the risk, and only then escalate toward search if branching difficulty still remains.

If the workflow asks one generation to do the work of several, a better model only hides the mistake longer.

The next chapter starts after that discipline is in place. Once one agent can reason, act, and verify through an explicit scaffold, the next question is whether a second role buys a real boundary or just more narration.
