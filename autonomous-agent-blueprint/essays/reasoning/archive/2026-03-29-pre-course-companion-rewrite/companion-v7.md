# Reasoning Companion

One workflow fails on a policy exception because it skipped a dependency. Another fails because it kept speaking confidently about live state it never checked. A third fails because the first answer became consequential before anyone challenged it. The field likes to call all three failures reasoning problems and then answer them with a more advanced-sounding method. That is how stacks get overbuilt.

The useful second-pass view of reasoning is not a catalog of clever techniques. It is a discipline for matching intervention to failure shape. That is what makes this topic practical. It turns reasoning from a prestige contest into workflow triage.

The public essay keeps the center of gravity on scaffold diagnosis. This companion owns the surrounding terrain: adjacent repair classes, broader planning logic, critique and consensus methods, and the search family that belongs outside the public spine.

## One Failure, Three Possible Misreads

Consider a policy-review workflow that must decide whether an exception request can be approved. It reads the request, checks the policy, verifies current account state, and returns a recommendation. The workflow keeps failing on difficult cases. One team says the model needs tree search because the task is complex. Another says the model needs critique because the answers are brittle. A third says the model needs stronger planning because the output feels too shallow.

All three can be wrong at once.

If the workflow keeps skipping one required check, the problem is often decomposition. If it keeps speaking confidently about account state without querying the live system, the problem is usually grounding through a reason-act-observe loop. If it keeps making factual claims that later trigger action, the missing piece is verification before consequence. Search only becomes justified if several grounded, verified paths still remain live and the task genuinely branches.

That is the operator lesson the public essay intentionally compressed. A reasoning stack earns its cost only when it corrects the failure that actually exists.

## Decomposition Is Not The Baby Version

Builders underrate decomposition because it does not look glamorous. It should be taken more seriously than most frontier method talk.

Many tasks arrive wrapped as one judgment but are structurally several judgments with dependencies. Eligibility before exception. Evidence before synthesis. Current state before recommendation. If the workflow is allowed to improvise those stages inside one generation, it can sound coherent while silently skipping the task's actual structure.

*Least-to-Most Prompting* belongs here because it solved exactly that problem. The paper forced multi-step tasks into ordered subproblems whose outputs support later steps. Its lasting move is architectural, not cosmetic. It separates solving the task from discovering the task structure while solving it.

*Step-Back Prompting* belongs near the same tier, but for a different reason. Sometimes the issue is not missing steps. It is early commitment to the wrong frame. In those cases the repair is not more branching. It is recovering the governing abstraction before descending into detail. That distinction matters because decomposition and abstraction reset solve different local failures.

## Grounding And Planning Buy Different Corrections

Reasoning and planning are adjacent but not interchangeable. A system can reason entirely inside language. Planning becomes real when the next step changes control flow, touches tools, or consumes resources in an environment that can contradict the model.

*ReAct* remains the control-loop paper of this cluster for a simple reason. It was trying to solve the mismatch between narrated reasoning and grounded interaction. Its important move is not that it produces longer traces. It binds thought to action and observation so the world can force course correction.

This is where teams often choose the wrong escalation. They see a workflow fail against live state and reach for a heavier reasoning method when what they really need is a better loop. If the environment matters, ReAct or something close to it usually belongs before critique overlays and well before search.

*LLM+P* belongs later because it solves a stricter problem. Some tasks do need a formal planning handoff, especially when the constraint structure is too rigid to leave in prose. That should influence builders who are hitting the limit of verbal scaffolds. It should not tempt them to treat every hard task as a symbolic-planning problem in disguise.

## Critique, Verification, And Consensus Are Not The Same Thing

Several methods get flattened into the category of extra reasoning even though they buy different corrections.

*Self-Refine* buys local improvement. The answer is roughly right, but too thin, messy, or incomplete. A draft-critique-revise loop can help.

*Chain-of-Verification* buys trust separation. The first answer no longer gets to certify itself. A checking phase asks different questions, follows a different evidence path, and can force revision before consequence.

*Self-Consistency* buys protection against single-trace brittleness. It helps when several traces over the same task tend to converge on a stable answer.

Consensus and debate methods belong elsewhere again. They are reliability overlays only when disagreement itself carries signal. If the workflow lacks evidence or structure, more voices will not rescue it.

The anti-pattern is to treat these as interchangeable sophistication upgrades. They are different levers. Use the one that closes the actual gap.

## Escalation Needs A Stop Rule

The practical failure in reasoning design is rarely that teams know too little about advanced methods. It is that they climb the ladder without a stop rule. A task fails once, so the workflow gains critique. It fails again, so search arrives. Then a planner is added because the trace still feels shaky. Before long the stack has become expensive enough that no one wants to ask whether the first intervention was misdiagnosed.

A stop rule keeps that from happening. If decomposition restores the missing dependency and the error disappears, stop there. If ReAct closes the grounding gap, stop there. If verification catches the unsupported claim before action, stop there. Builders should only add the next layer when the current one fails under review against a concrete failure class.

That sounds conservative because it is. Most reasoning stacks get overbuilt by prestige and under-audited by failure type.

## Search Should Arrive Late And Defend Its Cost

*Tree of Thoughts* and *LATS* matter because some problems really do branch. The papers were trying to solve tasks where one linear chain keeps missing viable alternatives or walking into dead ends. Their key move is to treat reasoning as search over a space of candidate paths rather than as one narrated attempt.

That is real progress. It is also easy to romanticize.

Search adds latency, orchestration complexity, harder evaluation, and a greater temptation to confuse activity with progress. Builders should only pay that cost after decomposition is doing real work, grounding is in place when the world matters, and verification sits in front of consequential outputs. If those layers are still weak, search usually magnifies confusion instead of correcting it.

This is the field's common misread. Search looks like the advanced answer because it is the most visible escalation. In practice, it is often the expensive answer to a problem that should have been solved one tier earlier.

Reasoning review should therefore stay hostile to beautiful traces. A long chain, a polished planner output, or an elegant search tree can still be evidence that the workflow is spending more tokens to hide the same diagnosis error. The right question remains whether the chosen scaffold removed the failure mode that justified its cost.

## Analytical References

**[Least-to-Most note](../../reference/papers/least_to_most_prompting.md).** This note is about ordered decomposition for tasks whose real difficulty is hidden dependency structure. It is the right source when the workflow keeps trying to solve several subproblems in one generation.

**[ReAct note](../../reference/papers/react.md).** This note is about the reason-act-observe loop. It matters when the builder needs a concrete reference for grounding reasoning in live tools and environment state.

**[Chain-of-Verification note](../../reference/papers/chain_of_verification.md).** This note is about separating answering from checking. It is useful when the workflow needs a distinct trust-earning stage before consequence.

**[LLM+P note](../../reference/papers/llm_plus_p.md).** This note is about planner handoff when prose can no longer carry hard constraints safely. It belongs in discussions where commitment points and ordering risk dominate.

**[Tree of Thoughts note](../../reference/papers/tree_of_thoughts.md).** This note is about true branching search over candidate paths. It matters when the team needs a source for what search is actually for, and for why it should arrive late.

## Sources Behind This Chapter

The core sources behind this chapter are [*Least-to-Most Prompting*](https://arxiv.org/abs/2205.10625), [*ReAct*](https://arxiv.org/abs/2210.03629), [*Chain-of-Verification*](https://arxiv.org/abs/2309.11495), and [*LLM+P*](https://arxiv.org/abs/2304.11477). They matter together because they map four different interventions: decomposition for hidden dependencies, control loops for live state, verification for earned trust, and planner handoff for sequence risk under hard constraints. That sequence is the real spine of the chapter.

The adjacent terrain widens the same logic without flattening it. *Step-Back Prompting* matters when the failure is premature framing rather than missing steps. *Self-Refine* and *Self-Consistency* matter because they solve different local problems than verification does. *Tree of Thoughts* and *LATS* matter because they defend true branching search rather than merely longer traces. They belong in the companion because they show how large the reasoning toolbox is once the public essay has installed the selection discipline.

The broader picture of the chapter is method triage under pressure. The [public essay](./02-reasoning-planning-v7.md) keeps only the doctrine line and the escalation spine. The [reasoning blueprint](../../core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md) turns that spine into a chooser. The paper notes are where the interested reader can inspect exactly what each method was trying to repair before the chapter compressed them into one control discipline.
