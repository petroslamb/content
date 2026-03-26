# Operating Agents III: The Lightest Correct Scaffold

A claims-processing agent built with a strong base model and a careful prompt had a task that looked contained: read the claim, check the criteria, return a structured recommendation. In production, the system rarely said anything absurd. It simply skipped one dependency, collapsed several checks into one fluent answer, or treated one missing fact as though it were present. The output looked polished enough to pass a casual read and brittle enough to fail the moment a reviewer checked the file.

The team reacted the way many teams react. They added prompt detail. They tried more context. They discussed a stronger model. None of that touched the real problem because the real problem was not mainly the model's intelligence. The workflow was asking one generation to do the work of several.

A decomposition pass and a verification step cut the obvious misses quickly. What remained was narrower and more useful. Claims tied to live payer status still failed because the workflow was reasoning from stale state rather than forcing a fresh check against the external ledger. The first fix helped. It also exposed the next failure shape. The system had never had one reasoning problem. It had several scaffold problems sitting on top of each other.

Most production reasoning failures are scaffold failures. Teams keep shopping for a smarter mind when the real problem is the wrong structure.

## Start With Failure Shape, Not Method Shopping

Reasoning literature becomes useful the moment it stops looking like a catalog of techniques and starts looking like a diagnosis framework.

If the system keeps skipping dependencies, the likely fix is decomposition. If it keeps reasoning as though the environment will obediently match its expectations, the likely fix is a reason-act-observe loop. If it states claims confidently and then turns them into side effects, the likely fix is verification before action. If the main difficulty is that the workflow must choose and order real steps under real constraints, the missing piece may be planning rather than more fluent reasoning. If one plausible path regularly dead-ends while another would have worked, then and only then do heavier search methods start to earn their keep.

That distinction matters because the response changes with the diagnosis. If the bottleneck is capability, a stronger model may help. If the bottleneck is scaffold, a stronger model often hides the problem longer by making the flawed workflow sound plausible more often.

The central rule has to stay severe: use the lightest reasoning structure that makes the task reliable.

## Decomposition Comes Before Brilliance

Builders underrate decomposition because it looks unsophisticated. It is often the most valuable change they can make.

If the system keeps skipping dependencies, compressing several checks into one answer, or hiding assumptions inside a fluent paragraph, the first fix is usually to make the hidden structure visible. *Least-to-Most Prompting* matters because it turns that move from vague advice into a concrete method. Ordered subproblems often do more work than another round of model shopping because they prevent the workflow from silently collapsing multiple dependencies into one pass (Zhou et al.).

A task that feels like one judgment usually contains several smaller judgments with dependencies between them. A case review may require an eligibility check, an exception check, and a supporting-evidence check. A research synthesis may require retrieval, extraction, contradiction handling, and final prose. A policy memo may need evidence collection, policy grounding, and approval logic before it is safe to draft a recommendation.

If the system is allowed to compress those steps into one generation, it can skip one dependency and still sound intelligent. Decomposition fixes that by turning hidden logic into visible workflow. The system has not become more generally intelligent. It has simply stopped pretending that a multi-stage task is a one-stage task.

## ReAct Is The Default When The World Matters

The moment the task depends on tools, live state, or environment feedback, reasoning has to become a control loop rather than a monologue. *ReAct* still matters for exactly this reason. It binds thought to action and observation, which means the model cannot remain trapped inside a narrated plan after the world has already contradicted it (Yao et al.).

A workflow that keeps reasoning as though the environment obediently matches the model's expectations will often sound sophisticated right up to the point where a real state change makes the whole chain worthless. ReAct is not merely one technique among many. In tool-using systems it is often the practical default until failure analysis proves otherwise.

## Planning Begins When Sequencing Itself Becomes The Risk

Reasoning and planning are related, but they are not the same engineering job. Reasoning can stay inside language and still help. Planning has to propose a sequence of steps that will consume resources, touch state, obey constraints, and create consequences.

That distinction matters because some failures are not really about local thought quality at all. The system may know what a good step looks like in isolation and still fail because the order is wrong, the prerequisites are hidden, the commitment point comes too early, or a constraint that should have been explicit stayed buried in prose. In that class of task, better decomposition is necessary but not sufficient. The workflow needs a clearer sequencing layer.

Most teams should still stay conservative here. They do not need a formal planner by default. They need a staged workflow where the plan exists as an inspectable object before the system starts spending resources or changing state. When the task has strong symbolic or operational constraints, methods such as *LLM+P* become relevant because they create a handoff from language into a stricter planning substrate. The important move is not formalism for its own sake. It is knowing when verbal scaffolds have reached their limit and the sequence itself has become the main source of risk (Liu et al.).

## Verification Belongs Before Action

Many important tasks do not simply need refinement. They need trust.

*Self-Refine* and *Reflexion* matter because they capture a real class of problems: the first answer is close but not quite good enough, or the system can learn from prior failure if it stores the lesson in a reusable form (Madaan et al.; Shinn et al.). Those are useful methods. They are not substitutes for verification.

If an answer makes factual claims that will influence downstream decisions or actions, then the workflow should not rely on the same generative act that produced the claim to certify it silently. *Chain-of-Verification* matters so much in practical agent work because it gives trust its own stage. Draft the answer. Generate the questions that would challenge it. Answer those separately. Revise after the checking stage. The deeper contribution is architectural. Verification gets its own place in the workflow instead of remaining an implicit hope inside the first draft (Dhuliawala et al.).

That move changes more than answer quality. It changes where trust is earned.

## Search Is Late And Conditional

*Self-Consistency* is useful when one input yields unstable answers across attempts and the task is stable enough that multiple correct paths tend to converge. It is much less useful when the bottleneck is stale evidence, missing observation, or weak task structure (Wang et al.).

*Tree of Thoughts* and *LATS* matter because some workflows really are search problems. They contain branching paths, plausible dead ends, and choices that simple decomposition cannot resolve cleanly (Yao et al.; Zhou et al.). Their practical danger is overapplication. Teams often invoke search as a sign of sophistication before proving that the task actually contains the kind of branching difficulty that would justify the cost.

Search is not hype. It is just late in the escalation order.

## A Conservative Escalation Spine

Start with decomposition so hidden dependencies become visible. Add a ReAct loop when the world can contradict the model. Insert verification before any claim becomes a consequential step. If the real problem is that the workflow must manage explicit sequencing or hard constraints, promote the plan itself into a first-class object and hand off to a stricter planner only when that structure is genuinely present. Reach for search only after the simpler scaffolds are already working and failure analysis still points to branching difficulty.

That order matters because each stage earns a different kind of trust. Decomposition makes intermediate work inspectable. ReAct makes the world legible after every move. Verification creates a formal challenge stage. Planner handoff creates an explicit boundary between language and constrained state. Search creates alternative paths whose selection criteria have to be justified.

That is why reasoning architecture belongs in a practical discussion of agents rather than an abstract discussion of cognition. The moment a scaffold changes what evidence exists, what intermediate state is visible, and where a human or another system could intervene, it becomes part of system design.

For most production agents the conservative stack is still the right one: decompose, ground, verify, then escalate to planner handoff or search only when the failure analysis earns it.

If your agent reasons badly, fix the structure before you go shopping for a smarter mind.

That is also the boundary into the next essay. Once the scaffold is explicit, the next question is no longer how one agent should think. It is whether a second role buys a real boundary that the single-agent workflow still lacks.

## Resources And References

### [Builder Blueprint: Reasoning and Planning](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md)

This blueprint turns the essay's diagnosis-first argument into concrete rules for decomposition, tool-grounded loops, verification overlays, planner handoff, and late-stage search.

### [Reasoning Companion](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/reasoning/companion.md)

The companion restores the wider reasoning and planning chapter: self-refinement, abstraction-reset methods, formal planner handoff, and the broader taxonomy that sits around the essay's conservative default stack.

### [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)

ReAct matters because it remains the cleanest practical control loop for tasks where the world can contradict the model.

### [Least-to-Most Prompting Enables Complex Reasoning in Large Language Models](https://arxiv.org/abs/2205.10625)

Least-to-Most matters because it turns decomposition from vague advice into an explicit method for exposing hidden dependencies.

### [Chain-of-Verification Reduces Hallucination in Large Language Models](https://arxiv.org/abs/2309.11495)

Chain-of-Verification matters because it gives verification its own stage instead of leaving trust inside the first draft.

### [LLM+P: Empowering Large Language Models with Optimal Planning Proficiency](https://arxiv.org/abs/2304.11477)

LLM+P matters because it makes planner handoff concrete when the task has enough explicit constraint structure to justify a more formal sequencing layer.

### [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171)

Self-Consistency matters because it gives teams a disciplined response to unstable answers when variance itself is the problem.

### [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601) and [Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models](https://arxiv.org/abs/2310.04406)

These papers matter because they show when reasoning should be treated as genuine search rather than as a single-path generation problem.
