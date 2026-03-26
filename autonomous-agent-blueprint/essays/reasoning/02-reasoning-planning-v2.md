# Operating Agents II: The Lightest Correct Scaffold

## How Agents Should Think Through Work

A claims-processing team built a document-review agent to decide which incoming cases qualified for a fast path. The base model was strong. The prompts were careful. The task even looked contained: read the claim, check the criteria, return a structured recommendation.

In production the system kept making the expensive kind of mistake. It rarely said anything absurd. It simply skipped one dependency, collapsed several checks into one fluent answer, or treated one missing fact as though it were present. The output looked orderly enough to pass a casual read and brittle enough to fail the moment a reviewer checked the file.

The team reacted the way many teams react. They added prompt detail. They tried more context. They considered a stronger model. None of that touched the real problem because the real problem was not mainly the model's intelligence. The workflow was asking one generation to do the work of several.

That is the practical claim here: most reasoning failures in production are scaffold failures. Teams keep shopping for a smarter mind when the real problem is the wrong structure.

Once the team broke the task into explicit checks and required a verification pass before classification, the failure rate dropped without a model swap. That pattern repeats across domains. A policy workflow skips one criterion. A research agent compresses retrieval and synthesis into one confident paragraph. A tool-using agent makes a plan that never checks whether the world actually matched the plan. These are not the same failure. They only look the same if you call all of them reasoning.

The useful question is stricter. What exact failure shape are you seeing, and what is the lightest scaffold that corrects it?

## Start With Failure Shape, Not Method Shopping

Reasoning literature becomes useful the moment it stops looking like a list of techniques and starts looking like a diagnosis framework.

If the system keeps skipping dependencies, the likely fix is decomposition. If it keeps reasoning as though the environment will obediently match its expectations, the likely fix is a reason-act-observe loop. If it states facts confidently and then turns them into side effects, the likely fix is verification before action. If one path keeps dead-ending while another would have worked, the likely fix may finally be search.

That distinction matters because the response changes with the diagnosis. If the bottleneck is capability, a stronger model may help. If the bottleneck is scaffold, a stronger model often hides the problem longer by making the flawed workflow sound plausible more often.

The right bias is conservative. Do not buy more sophistication until you know what kind of failure you are paying to correct.

## Failure Shape To Scaffold Map

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

A task that feels like one judgment usually contains several smaller judgments with dependencies between them. A case review may require an eligibility check, an exception check, and a supporting-evidence check. A research synthesis may require retrieval, extraction, contradiction handling, and final prose. A policy memo may need evidence collection, policy grounding, and approval logic before it is safe to draft a recommendation.

If the system is allowed to compress those steps into one generation, it can skip one dependency and still sound intelligent. Decomposition fixes that by turning hidden logic into visible workflow. The system has not become more generally intelligent. It has simply stopped pretending that a multi-stage task is a one-stage task.

This is also why reasoning and planning should not be collapsed casually into one concept. Reasoning draws conclusions. Planning sequences actions. In a live system, a planning error can escape into the world and create irreversible state. That is a stricter standard than getting an answer paragraph wrong.

## ReAct Is The Default When The World Matters

Reasoning that floats free of observation is one of the most expensive forms of fluency. It produces plans that sound coherent because they are coherent inside the model's imagined world.

This is why *ReAct* remains the default paper for tool-using systems. Its lasting contribution is not that it makes the model look busier. It keeps the control loop corrigible. The system acts, observes, and continues from what actually came back. If the tool returns partial completion instead of final completion, the loop can absorb that. If the retrieval result contradicts the current assumption, the next step can revise. If the page state changed, the plan can change with it.

Prompting alone does not fix the gap between narrated reasoning and grounded reasoning. The problem is structural. The workflow never forced the model to check.

If your agent uses tools, external documents, or live state, ReAct is not one interesting option among many. It is the working default until failure analysis proves you need something heavier.

## Verification Belongs Before Action

Teams often treat verification as polish. They build the main reasoning loop first and add checks later if the errors become embarrassing enough.

That order is backwards. Verification is part of the reasoning architecture because it decides when a plausible answer is trustworthy enough to become a downstream action, a classification, or a high-confidence artifact.

This is where *Chain-of-Verification* matters, and it is also where lighter self-checks can still earn their keep. The goal is not ritualized caution. The goal is to close the gap between "the answer sounds coherent" and "the answer survived the checks this workflow requires."

The distinction between useful and useless critique is sharper than teams admit. "Be more complete" is not a real signal. "You never verified criterion C" is a signal. The first creates latency. The second creates information.

## Search Is Late, Expensive, And Often Premature

Search-heavy methods such as *Tree of Thoughts* and *Language Agent Tree Search* are real contributions. They are also widely overapplied.

They earn their keep when a task has genuine branching difficulty. One plausible path regularly fails. Another would have worked. The value of the method lies in exploring alternatives that matter.

What search does not fix is shallow task breakdown, missing environmental grounding, or absent verification. If the system currently fails because it compressed several dependencies into one pass, tree search only explores more elaborate versions of the same flawed setup. If it fails because it never checked the world, search over internal reasoning simply makes the wrong answer slower and more expensive.

The escalation rule is therefore blunt: search belongs after decomposition, grounding, and verification are already in place, and only when failure analysis still shows a branching problem.

## The Practical Default

The default reasoning stack for most production agents should be plain to state. Decompose multi-part work into explicit subproblems. Use a reason-act-observe loop whenever tools or live state matter. Verify consequential claims before they become actions. Add self-consistency only when variance itself is the problem. Add search only when branching difficulty is proved rather than imagined.

That stack will look underpowered to teams trained to admire sophistication first. In practice it is often the scaffold that turns a plausible demo into a system that can survive ordinary work.

If your agent reasons badly, fix the structure before you go shopping for a smarter mind.

## Resources And References

*ReAct* is the central paper here because it puts reasoning back in contact with the world. The lasting insight is not "tools plus thoughts." It is that control loops should proceed from observation rather than expectation.

*Least-to-Most Prompting* matters because it formalizes the least glamorous and most useful move in this cluster: decomposition. It gives a cleaner language for turning hidden dependencies into explicit intermediate work.

*Chain-of-Verification* matters because it makes verification structural rather than decorative. It is most useful wherever a plausible answer can become an expensive action.

*Tree of Thoughts* belongs here not as a default, but as the cleanest statement of when branching search is real enough to justify its cost.

*LATS* is useful as the heavier escalation reference. It clarifies what a true search-heavy scaffold looks like, which makes it easier to notice when teams are compensating for a simpler diagnosis they never made.
