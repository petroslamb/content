# Operating Agents II: The Lightest Correct Scaffold

## How Agents Should Think Through Work

Most production reasoning failures are scaffold failures. Teams keep shopping for a smarter mind when the real problem is the wrong structure.

The mistake begins with a category blur. Several very different failures get dumped into the bucket called reasoning: hidden dependencies compressed into one answer, plans that never check the world, claims that become actions before verification, and tasks that really do need search. Those failures do not ask for the same fix.

The useful question is stricter. What exact failure shape are you seeing, and what is the lightest scaffold that corrects it?

## Start with Failure Shape, Not Method Shopping

Reasoning literature becomes useful the moment it stops looking like a catalog of techniques and starts looking like a diagnosis framework.

If the system keeps skipping dependencies, the likely fix is decomposition. That is why [*Least-to-Most Prompting*](https://arxiv.org/abs/2205.10625) still matters. It gives a clean language for turning one fluent answer into ordered subproblems. If the system keeps reasoning as though the environment will obediently match its expectations, the likely fix is a reason act observe loop, which is why [*ReAct*](https://arxiv.org/abs/2210.03629) remains the practical control-loop paper in this whole cluster. If the system states claims confidently and then turns them into side effects, the likely fix is verification before action, where [*Chain-of-Verification*](https://arxiv.org/abs/2309.11495) is still the clearest reference. If one plausible path regularly dead-ends while another would have worked, then and only then do heavier search methods such as [*Tree of Thoughts*](https://arxiv.org/abs/2305.10601) or [*LATS*](https://arxiv.org/abs/2310.04406) start to earn their keep.

That distinction matters because the response changes with the diagnosis. If the bottleneck is capability, a stronger model may help. If the bottleneck is scaffold, a stronger model often hides the problem longer by making the flawed workflow sound plausible more often.

The right bias is conservative. Do not buy more sophistication until you know what kind of failure you are paying to correct.

## Failure Shape to Scaffold Map

| Failure shape | First scaffold | Why it comes first | Escalate only if |
|---|---|---|---|
| Several checks get compressed into one answer | Decomposition | Hidden dependencies become explicit intermediate work | The task still fails after the subproblems are made legible |
| The plan ignores live state, tool results, or current context | ReAct loop | Reasoning proceeds from observation instead of expectation | The environment has real branching difficulty |
| The system states claims confidently and then acts on them | Verification before action | Expensive errors are caught at the edge where they matter | Verification still leaves several plausible paths |
| One input yields unstable answers across attempts | Self-consistency | Variance itself becomes measurable and reducible | External grounding is the real bottleneck |
| One plausible path often dead-ends | Tree search or LATS | Search explores alternatives only when alternatives matter | The search cost outweighs the improvement |

The point of this table is not the names. It is the discipline. It forces the builder to explain what went wrong before reaching for a heavier method.

## Decomposition Comes Before Brilliance

Builders underrate decomposition because it looks unsophisticated. It is often the most valuable change they can make.

A claims-processing team learned this the expensive way. Their document-review agent used a strong base model and a careful prompt. The task looked contained: read the claim, check the criteria, return a structured recommendation. In production the system rarely said anything absurd. It simply skipped one dependency, collapsed several checks into one fluent answer, or treated one missing fact as though it were present. The output looked polished enough to pass a casual read and brittle enough to fail the moment a reviewer checked the file.

The team reacted the way many teams react. They added prompt detail. They tried more context. They discussed a stronger model. None of that touched the real problem because the real problem was not mainly the model's intelligence. The workflow was asking one generation to do the work of several.

A decomposition pass and a verification step cut the obvious misses quickly. What remained was narrower and more useful. Claims tied to live payer status still failed because the workflow was reasoning from stale state rather than forcing a fresh check against the external ledger. The first fix helped. It also exposed the next failure shape. The system had never had one reasoning problem. It had several scaffold problems sitting on top of each other.

A task that feels like one judgment usually contains several smaller judgments with dependencies between them. A case review may require an eligibility check, an exception check, and a supporting-evidence check. A research synthesis may require retrieval, extraction, contradiction handling, and final prose. A policy memo may need evidence collection, policy grounding, and approval logic before it is safe to draft a recommendation.

If the system is allowed to compress those steps into one generation, it can skip one dependency and still sound intelligent. Decomposition fixes that by turning hidden logic into visible workflow. The system has not become more generally intelligent. It has simply stopped pretending that a multi-stage task is a one-stage task.

This is also why reasoning and planning should not be collapsed casually into one concept. Reasoning draws conclusions. Planning sequences actions. In a live system, a planning error can escape into the world and create irreversible state. That is a stricter standard than getting an answer paragraph wrong.

## ReAct Is the Default When the World Matters

Reasoning that floats free of observation is one of the most expensive forms of fluency. It produces plans that sound coherent because they are coherent inside the model's imagined world.

This is why [*ReAct*](https://arxiv.org/abs/2210.03629) remains the default paper for tool-using systems. Its lasting contribution is not that it makes the model look busier. It keeps the control loop corrigible. The system acts, observes, and continues from what actually came back. If the tool returns partial completion instead of final completion, the loop can absorb that. If retrieval contradicts the current assumption, the next step can revise. If the page state changed, the plan can change with it.

Prompting alone does not fix the gap between narrated reasoning and grounded reasoning. The problem is structural. The workflow never forced the model to check.

If your agent uses tools, external documents, or live state, ReAct is not one interesting option among many. It is the working default until failure analysis proves you need something heavier.

## Verification Belongs Before Action

Teams often treat verification as polish. They build the main reasoning loop first and add checks later if the errors become embarrassing enough.

That order is backwards. Verification is part of the reasoning architecture because it decides when a plausible answer is trustworthy enough to become a downstream action, a classification, or a high-confidence artifact.

This is where [*Chain-of-Verification*](https://arxiv.org/abs/2309.11495) matters, and it is also where lighter self-checks and even [*Self-Consistency*](https://arxiv.org/abs/2203.11171) can still earn their keep. The goal is not ritualized caution. The goal is to close the gap between "the answer sounds coherent" and "the answer survived the checks this workflow requires."

The distinction between useful and useless critique is sharper than teams admit. "Be more complete" is not a real signal. "You never verified criterion C" is a signal. The first creates latency. The second creates information.

## Search Is Late, Expensive, and Often Premature

Search-heavy methods such as [*Tree of Thoughts*](https://arxiv.org/abs/2305.10601) and [*LATS*](https://arxiv.org/abs/2310.04406) are real contributions. They are also widely overapplied.

They earn their keep when a task has genuine branching difficulty. One plausible path regularly fails. Another would have worked. The value of the method lies in exploring alternatives that matter.

What search does not fix is shallow task breakdown, missing environmental grounding, or absent verification. If the system currently fails because it compressed several dependencies into one pass, tree search only explores more elaborate versions of the same flawed setup. If it fails because it never checked the world, search over internal reasoning simply makes the wrong answer slower and more expensive.

The escalation rule is therefore blunt: search belongs after decomposition, grounding, and verification are already in place, and only when failure analysis still shows a branching problem.

The broader reasoning chapter is wider than the chooser used here. It also covers self-refinement, abstraction-first methods such as step-back prompting, and formal planning handoff methods such as LLM+P. Those techniques belong in the architecture menu. This essay keeps them outside the center because the first practical mistake is usually not picking the wrong advanced method. It is failing to install the light scaffold the task already needed.

## Structure Before More Intelligence

The default reasoning stack for most production agents should be plain to state. Decompose multi-part work into explicit subproblems. Use a reason act observe loop whenever tools or live state matter. Verify consequential claims before they become actions. Add self-consistency only when variance itself is the problem. Add search only when branching difficulty is proved rather than imagined.

That stack will look underpowered to teams trained to admire sophistication first. In practice it is often the scaffold that turns a plausible demo into a system that can survive ordinary work.

If your agent reasons badly, fix the structure before you go shopping for a smarter mind.

## Resources And References

### [Builder Blueprint: Reasoning and Planning](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md)

This blueprint matters because it turns the essay's scaffold-selection argument into a concrete chooser for design, debugging, and review.

If you want the broader chapter and survey scope behind this essay, use the [companion note](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/reasoning/companion.md) and the [series coverage map](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/operating-agents-coverage-map.md).

### [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) (2022)

*ReAct* matters because it joins reasoning, action, and observation inside one loop that updates from what the environment actually returns.

### [Least-to-Most Prompting Enables Complex Reasoning in Large Language Models](https://arxiv.org/abs/2205.10625) (2022)

*Least-to-Most* matters because it makes decomposition explicit and supports the claim that many reasoning failures are really failures to respect task structure.

### [Chain-of-Verification Reduces Hallucination in Large Language Models](https://arxiv.org/abs/2309.11495) (2023)

*Chain-of-Verification* matters because it makes verification part of the reasoning architecture rather than an afterthought.

### [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171) (2022)

*Self-Consistency* matters because it addresses brittle single-pass reasoning without requiring a completely different scaffold.

### [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601) (2023)

*Tree of Thoughts* matters because it marks the point where branching search becomes real enough to justify its added cost and complexity.

### [Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models](https://arxiv.org/abs/2310.04406) (2023)

*LATS* matters because it shows what a genuinely search-heavy reasoning scaffold looks like once planning, action, and feedback are all inside the loop.
