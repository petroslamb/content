# Reasoning Companion

The easiest way to waste time in agent design is to respond to the wrong failure with a more impressive method. A workflow skips one dependency, so the team adds search. It hallucinates on live state, so they add critique. It produces unstable answers, so they stretch the prompt and call it planning. The result is usually not more intelligence. It is more machinery wrapped around a diagnosis error.

The useful second-pass view of reasoning is not a taxonomy of clever techniques. It is a discipline for matching intervention to failure shape. That is what makes this topic practical. It turns reasoning from a prestige contest into workflow triage.

## One Failure, Three Possible Misreads

Consider a policy-review agent that must decide whether an exception request can be approved. It reads the request, checks the policy, verifies current account status, and returns a recommendation. The workflow keeps failing on difficult cases. One team says the model needs tree search because the task is complex. Another says the model needs critique because the answers are brittle. A third says the model needs stronger planning because the output feels too shallow.

All three can be wrong at once.

If the system keeps skipping one required check, the problem is often decomposition. If it keeps speaking confidently about account state without querying the live system, the problem is usually grounding through a reason act observe loop. If it keeps making factual claims that later trigger action, the missing piece is verification before consequence. Search only becomes justified if several grounded, verified paths still remain live and the task genuinely branches.

That is the operator lesson the main essay intentionally compressed. A reasoning stack earns its cost only when it corrects the failure that actually exists.

## Decomposition Is Not The Baby Version

Builders underrate decomposition because it does not look glamorous. It should be taken more seriously than most frontier method talk.

Many tasks arrive wrapped as one judgment but are structurally several judgments with dependencies. Eligibility before exception. Evidence before synthesis. Current state before recommendation. If the workflow is allowed to improvise those stages inside one generation, it can sound coherent while silently skipping the task's actual structure.

Least-to-Most matters because it solved exactly that problem. The paper was trying to force multi-step tasks into ordered subproblems whose outputs support later steps. Its lasting move is architectural, not cosmetic. It separates "solve the task" from "discover the task structure while solving it." Builders should apply that move whenever the task is multi-step and mostly deterministic.

Step-Back Prompting sits near the same tier, but for a different reason. Sometimes the issue is not missing steps. It is early commitment to the wrong frame. In those cases, the right repair is not more branching. It is recovering the governing abstraction before descending into details.

## Planning Starts When The World Can Say No

Reasoning and planning are adjacent but not interchangeable. A system can reason entirely inside language. Planning becomes real when the next step changes control flow, touches tools, or consumes resources in an environment that can contradict the model.

That is why ReAct remains the control-loop paper of this cluster. It was trying to solve the mismatch between narrated reasoning and grounded interaction. Its important move is not that it produces longer traces. It binds thought to action and observation so the world can force course correction.

This is where teams often choose the wrong escalation. They see a workflow fail against live state and reach for a heavier reasoning method when what they really need is a better loop. If the environment matters, ReAct or something close to it usually belongs before critique overlays and well before search.

LLM+P belongs later because it solves a stricter problem. Some tasks do need a formal planning handoff, especially when the constraint structure is too rigid to leave in prose. That should influence builders who are hitting the limit of verbal scaffolds. It should not tempt them to treat every hard task as a symbolic-planning problem in disguise.

## Critique, Verification, And Consensus Buy Different Things

This is where the literature gets flattened most often. Several methods look like "extra reasoning," but they are buying different corrections.

Self-Refine buys local improvement. The answer is roughly right, but too thin, messy, or incomplete. A draft critique revise loop can help.

Chain-of-Verification buys trust separation. The first answer no longer gets to certify itself. A checking phase asks different questions, follows a different evidence path, and can force revision before consequence.

Self-Consistency buys protection against single-trace brittleness. It helps when several traces over the same task tend to converge on a stable answer.

Consensus and debate methods belong elsewhere again. They are reliability overlays only when disagreement itself carries signal. If the workflow lacks evidence or structure, more voices will not rescue it.

The anti-pattern is to treat these as interchangeable sophistication upgrades. They are different levers. Use the one that closes the actual gap.

## Search Should Arrive Late And Defend Its Cost

Tree of Thoughts and LATS matter because some problems really do branch. The papers were trying to solve tasks where one linear chain keeps missing viable alternatives or walking into dead ends. Their key move is to treat reasoning as search over a space of candidate paths rather than as one narrated attempt.

That is real progress. It is also easy to romanticize.

Search adds latency, orchestration complexity, harder evaluation, and a greater temptation to confuse activity with progress. Builders should only pay that cost after decomposition is doing real work, grounding is in place when the world matters, and verification sits in front of consequential outputs. If those layers are still weak, search usually magnifies confusion instead of correcting it.

This is the field's common misread. Search looks like the advanced answer because it is the most visible escalation. In practice, it is often the expensive answer to a problem that should have been solved one tier earlier.

## Resources And References

### [Reasoning Essay: Operating Agents III: The Lightest Correct Scaffold](../reasoning/02-reasoning-planning-v5.md)

Read the essay first for the hard public claim: choose the lightest scaffold that makes the task reliable. It keeps the center of gravity on diagnosis rather than method-shopping.

### [Builder Blueprint: Reasoning and Planning](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md)

The blueprint is the build-facing chooser for this terrain: decomposition, ReAct, verification, variance handling, and late search. Use it when you need to decide what to add next to a live workflow.

### [Foundation Agents: Practical Chapters Guide](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/reference/chapters-guide.md)

The guide is the quickest way to see the full reasoning landscape without losing the practical hierarchy. It keeps the already-useful methods separate from the promising but expensive ones.

### [Least-to-Most Prompting Enables Complex Reasoning in Large Language Models](https://arxiv.org/abs/2205.10625) (2022)

Least-to-Most matters because it treats decomposition as a first-class intervention. The paper was solving structured multi-step tasks by forcing ordered subproblem solving instead of one monolithic leap. Its architectural move is to externalize structure before the model spends compute improvising it.

Builders should let it influence task packaging, not just prompting style. It is the right default whenever the workflow hides dependencies inside one fluent answer.

### [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) (2022)

ReAct matters because it joins reasoning, action, and observation into one loop. The paper was solving grounded tasks where the world can invalidate the model's current belief. Its move is to make observation a first-class correction mechanism rather than a late afterthought.

That should influence any tool-using workflow. It should not be reduced to a trace format or treated as decorative chain-of-thought with actions sprinkled in.

### [Chain-of-Verification Reduces Hallucination in Large Language Models](https://arxiv.org/abs/2309.11495) (2023)

CoVe matters because it separates answer generation from answer checking. The paper was trying to solve factual fragility by giving verification its own stage and questions. That move matters far beyond hallucination benchmarks because it changes where trust is earned.

Builders should apply it when outputs can trigger decisions or actions. They should not mistake it for a generic polishing loop.

### [LLM+P: Empowering Large Language Models with Optimal Planning Proficiency](https://arxiv.org/abs/2304.11477) (2023)

LLM+P matters because it marks the point where verbal reasoning yields to formal planning structure. The paper was solving tasks whose constraint logic deserved a stricter handoff than prose alone could provide.

Its influence should be disciplinary. Not every hard task needs it, but it is an important reminder that "think harder in text" is not the only escalation path.

### [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601) (2023) and [Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models](https://arxiv.org/abs/2310.04406) (2023)

These papers matter because they treat reasoning as branching search rather than one trace. They were solving genuinely multi-path problems where alternatives and dead ends matter. Their architectural move is to make exploration itself part of the workflow.

That should influence builders only after cheaper scaffolds have already done their work. Search is real. It is not the first repair.
