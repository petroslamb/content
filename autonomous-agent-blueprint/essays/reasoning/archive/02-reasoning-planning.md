# Operating Agents II: The Lightest Correct Scaffold

## How Agents Should Think Through Work

*Operating Agents II of VI*

*The opening case in this essay is a composite of common production failures, not a report of one named company.*

---

A claims-processing team built a document-review agent to decide which incoming cases qualified for a fast path. The model was strong. The prompts were carefully tuned. The task seemed contained: read the claim, check the criteria, return a structured recommendation. In the demo environment the system looked competent. In production it kept making a more expensive kind of mistake. It rarely said something obviously absurd. It simply skipped one dependency, dropped one condition, or treated one missing fact as if it were present. The answers sounded orderly enough to survive a casual read and brittle enough to collapse under review.

The team reacted the way many teams react. They tried more prompt detail. They tried more context. They considered a stronger model. None of that touched the real problem because the real problem was not the model's intelligence. The real problem was that the workflow asked one generation to do the work of several. Once the team broke the task into smaller typed checks and required a verification pass before classification, the failure rate fell sharply without a model swap.

That is the flattering mistake this essay is trying to correct: when reasoning looks weak, builders assume the model is weak. In many cases the model is being asked to think inside the wrong structure.

The more useful default is stricter. Start with the lightest scaffold that makes the task reliable. Decompose before you escalate. Ground before you search. Verify before you act.

---

## Most Reasoning Failures Are Scaffold Failures

The phrase "reasoning failure" encourages the wrong diagnosis because it makes the model look like the natural culprit. Yet a large share of failures in live agent systems have a different shape. The model is not incapable of the task. It is being asked to do too much in one pass, or to act without checking the environment, or to commit before verification, or to search when the real need was structure.

That distinction matters because the responses are different. If the bottleneck is capability, then a stronger model may be the right answer. If the bottleneck is scaffold, a stronger model often buys less than builders hope. It can even hide the problem longer by making the flawed workflow look plausible more often.

The practical contribution of the reasoning literature is not that it produced an expanding catalog of techniques. It is that it made scaffold choice discussable. *Least-to-Most Prompting* clarifies when decomposition turns a brittle task into a series of bounded ones. *ReAct* clarifies what it means for reasoning to stay grounded in the world rather than drift into internal narration. *Chain-of-Verification* clarifies that factual confidence should be checked before it becomes action. *Tree of Thoughts* clarifies when branching search is genuinely warranted instead of theatrically expensive.

The most valuable sentence in this part is not a research sentence. It is a builder sentence: do not buy more sophistication until you know what kind of failure you are paying to correct.

---

## The Default Stack Is Simpler Than Most Teams Think

Most agents do not need a grand reasoning architecture. They need a disciplined one.

The first default is decomposition. If a task has multiple dependent conditions, make those conditions explicit. If the output is supposed to rest on three checks, force three checks. A model asked to answer the whole question at once can hide missing steps inside fluent prose. A model asked to emit intermediate outputs step by step has to show its work in a way the system can examine.

The second default is a reason-act-observe loop whenever the world matters. This is where *ReAct* changed the field in a durable way. It did not simply make reasoning longer. It put reasoning back in contact with evidence. An agent that uses tools, reads live state, or depends on external facts should not reason as though the world will obediently match its expectations. It should act, observe, and continue from what actually came back.

The third default is verification before consequential output becomes action. A report can survive an isolated factual mistake. A workflow trigger, a form fill, or a write operation often cannot. That is why *Chain-of-Verification* matters. It turns a polished answer into a provisional one and asks what would need to be true for that answer to hold.

Everything beyond those three defaults is an escalation, not a starting point.

## Reasoning Scaffold Chooser

| Failure shape | Default scaffold | Why it is the first move | Escalate only if |
|---|---|---|---|
| The answer skips dependencies or compresses several checks into one | Decomposition | It turns hidden gaps into explicit intermediate steps | The task still fails after the subproblems are made legible |
| The plan ignores live state, tool results, or changing context | ReAct loop | It forces reasoning to continue from observation, not expectation | The environment itself is too branching for one path |
| The system states facts confidently and then acts on them | Verification before action | It catches errors at the boundary where they become expensive | Verification still leaves multiple plausible solution paths |
| The same input yields different answers and agreement is meaningful | Self-consistency | It stabilizes brittle single-pass reasoning | External grounding is the real bottleneck |
| The task has real branching difficulty and early paths reliably dead-end | Tree search or LATS | Search explores alternatives when one path is not enough | The cost of search exceeds the value of the improvement |

The important thing about this table is not the names. It is the bias. The bias is conservative by design.

---

## Decomposition Comes Before Brilliance

Builders underrate decomposition because it looks unsophisticated. It is often the most valuable change they can make.

The reason is structural. A task that feels like one judgment often contains several smaller judgments with dependencies between them. A policy decision may require three criteria to be independently true. A claims decision may require a threshold check, an exception check, and a supporting-document check. A research workflow may require retrieval, extraction, and synthesis in sequence. If the system is allowed to compress those steps into one generation, it can return a plausible answer that quietly skipped one of the dependencies.

Decomposition fixes that by turning the hidden logic into a visible workflow. That is why the gain is often larger than the gain from a marginal model upgrade. The system has not become more generally intelligent. It has simply stopped pretending that a multi-stage task is a one-stage task.

This is also why reasoning and planning should not be casually collapsed into one concept. Reasoning draws conclusions. Planning sequences actions. In a real system, a planning error can escape into the world and create irreversible state. That is a stricter standard than getting an answer paragraph wrong.

Formal planning methods such as *LLM+P* matter at the edge, especially when the task has strong constraint structure. Most enterprise agent tasks do not live at that edge. They need ordered subgoals, live observation, and approval gates before irreversible steps. They do not need planners because planners are elegant. They need them only when task structure genuinely demands them.

---

## ReAct Is The Default When The World Matters

Reasoning that floats free of observation is one of the most expensive kinds of fluency. It produces plans that sound coherent because they are coherent inside the model's imagined world.

*ReAct* is still the central paper here because it solved a permanent problem. The value of the reason-act-observe loop is not that it makes agents look more active. It makes them corrigible. If the search result contradicts the current assumption, the next step can revise. If the tool returns partial completion instead of final completion, the loop can continue. If the environment changed, the system can absorb the change before it hardens into action.

This is why planning without grounding is not just a variety of hallucination. It is a structural disconnect between the control loop and the environment it is supposed to govern. Prompting alone will not fix that disconnect because the problem is not that the answer is insufficiently careful. The problem is that the workflow never forced the model to check.

If your agent uses tools, external documents, or live state, ReAct is not one interesting option among many. It is the working default until failure analysis proves you need something heavier.

---

## Verification Belongs Before Action, Not After Embarrassment

Teams often treat verification as polish. They ship the main reasoning loop first and add checks later if the failures become visible enough.

That order is backwards. Verification is part of the reasoning architecture because it decides when a plausible answer is trustworthy enough to become a side effect.

This is where *Chain-of-Verification* matters, and it is also where lighter-weight self-checks can still be useful. The goal is not ritualized caution. The goal is to close the gap between "the answer sounds coherent" and "the answer has survived the checks this workflow requires." If the system is going to fill a form, classify a case, escalate an incident, or trigger a downstream step, then verification belongs at the edge where the claim becomes consequential.

Self-refinement can help when the system is close and the critique signal is real. It becomes useless when the critique is vague. "Be more complete" is not a signal. "You never verified criterion C" is a signal. The distinction matters because builders often add refinement loops and call the extra latency progress.

---

## Search Is Late, Expensive, And Often Premature

Search-heavy methods such as *Tree of Thoughts* and *Language Agent Tree Search* are real contributions. They are also widely overapplied.

They earn their keep when a task has actual branching difficulty. Not apparent difficulty, not prompt-writing frustration, but a genuine pattern where one plausible path often dead-ends and another path would have succeeded. Mathematical search, hard-constrained planning, or adversarial tasks can look like this.

What search does not fix is a shallow task breakdown, missing environmental grounding, or absent verification. If the current system fails because it compressed several dependencies into one pass, tree search only explores more elaborate versions of the same bad setup. If the current system fails because it never checked the world, search over internal reasoning just makes the wrong answer take longer to arrive.

This is the escalation rule: search belongs after decomposition, grounding, and verification are already in place and failure analysis still shows that the task needs alternative paths.

That rule is less exciting than the frontier rhetoric around reasoning systems. It is also how teams avoid building expensive machinery around the wrong diagnosis.

---

## The Stricter Default

The default reasoning stack for most production agents should be plain to state. Decompose multi-part work into typed subproblems. Use a reason-act-observe loop whenever tools or live state matter. Verify consequential claims before they become actions. Add self-consistency only when variance itself is the problem. Add search only when branching difficulty is proved rather than imagined.

That stack will look underpowered to teams that have been taught to admire complexity first. In practice, it is usually the stack that turns a plausible demo into a system that can survive ordinary work.

If your agent reasons badly, fix the scaffold before you shop for a smarter mind.

---

## Resources And References

### [Builder Blueprint: Reasoning and Planning](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md)

For the companion design layer, use this public blueprint. It preserves the quick-choice logic, comparison matrix, anti-patterns, and build order that are useful in implementation meetings but too schematic for the main essay. The point of keeping it separate is that the essay can stay argumentative while the blueprint stays operational.

### [Least-to-Most Prompting Enables Complex Reasoning in Large Language Models](https://arxiv.org/abs/2205.10625) (2022)

This paper matters because it formalizes one of the least glamorous and most useful builder moves: decomposition. In the essay, it supports the claim that many reasoning failures come from asking one generation to do work that should be split into explicit intermediate steps. Its value is not that it makes reasoning longer. Its value is that it makes logical dependencies visible.

### [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) (2022)

*ReAct* is the most important default citation in this part because it puts reasoning back in contact with the world. The paper's lasting contribution is not simply "tools plus thoughts." It is the insistence that reasoning should proceed from observed results rather than from internal expectation alone. That is why the essay treats ReAct as a default for tool-using agents rather than as one optional trick among many.

### [Chain-of-Verification Reduces Hallucination in Large Language Models](https://arxiv.org/abs/2309.11495) (2023)

*Chain-of-Verification* matters here because it makes verification structural instead of decorative. The paper is valuable for any workflow where a plausible answer can become a costly side effect. In the essay it supports the stricter claim that verification belongs before action, not after an embarrassing failure teaches you why it was missing.

### [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171) (2022)

*Self-consistency* is useful because it shows there are tasks where variance itself is the bottleneck. Sampling several reasoning traces and aggregating them can stabilize outputs when one single path is too brittle. In this essay, though, the paper appears with a limit attached: it is an escalation method for a narrow failure shape, not a substitute for decomposition or grounding.

### [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601) (2023)

*Tree of Thoughts* matters because it is the clearest signal that some tasks genuinely need branching search. It belongs in the essay not as a default recommendation, but as the cleanest example of a method teams reach for too early. Its presence helps sharpen the escalation rule: search earns its cost only after simpler scaffold fixes have been tried.

### [Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models](https://arxiv.org/abs/2310.04406) (2024)

*LATS* extends the same escalation story in a more explicit action-planning direction. Its value in this essay is not that every builder should adopt it. Its value is that it clarifies what a real search-heavy scaffold looks like, which makes it easier to tell when teams are using heavy machinery to compensate for a simpler diagnosis they never made.
