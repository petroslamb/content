# Operating Agents VI: The Workflow Is the Object

## How To Improve An Agent System That Already Works

A document-classification agent had been in production for three months. It was not perfect, but it was useful. Humans still corrected the tail of the work, yet the economics made sense and the workflow was stable enough that the team decided it was time to improve it.

Over the next six weeks they edited the system prompt repeatedly. One revision seemed to help the recent failures everyone still remembered. A later revision quietly regressed another slice of traffic. Tool descriptions changed. Instructions got longer. The team debated phrasing with the urgency people reserve for work that feels productive.

Nothing important improved because the team was tuning the easiest visible surface before it had stabilized the objective. There was no fixed evaluation set, no clean failure taxonomy, no agreement about whether latency and correction rate were part of the goal, and no serious view of whether the underlying issue lived in schema design, retrieval quality, or prompt wording at all.

That is the practical anti-pattern of agent optimization: prompt churn without measurement. If you cannot say which layer is failing and measure it against a stable objective, you are not optimizing a workflow. You are editing it.

This is why the title of this chapter matters more than it first appears to. The workflow is the object. Not the prompt in isolation. Not the node that happens to be easiest to change. The workflow.

That means inputs, schemas, retrieval, tool behavior, routing, approval burden, latency, cost, retries, regressions, and human correction load all belong inside the improvement loop.

## Optimization Starts When The Objective Stops Moving

The field likes to discuss optimization at the exciting end: prompt search, topology search, self-improving graphs, systems that rewrite themselves. Production teams usually need a much duller first move.

They need to freeze an evaluation set.

Without a stable task set and known-good outcomes, there is no durable signal against which a change can be judged. There is only recency bias, taste, and anecdote. The last ugly incident gets more influence than the other fifty tasks that quietly improved or degraded.

This is why papers like *OPRO* matter conceptually even if many teams will never run that exact method. The important lesson is not that prompts can be optimized by search. The important lesson is that optimization presupposes an objective and a repeated evaluation loop.

Once that is clear, many supposed optimization debates become easier to settle. The prompt might not be the problem. The workflow might be reasoning over weak evidence. The output schema might be turning a decent answer into downstream failure. The routing might be pushing the wrong cases through a brittle path. The approval boundary might be firing constantly because the system is poorly scoped, not because the reviewer is conservative.

## Signal To First Intervention Map

| Signal you see | First intervention | Why it comes first |
|---|---|---|
| Results feel inconsistent but no one can prove regression | Build an evaluation set and baseline metrics | Without a stable objective, every change is guesswork |
| Downstream systems reject otherwise decent answers | Tighten schemas and contracts | A cleaner interface removes whole classes of failure cheaply |
| The system reasons over weak or irrelevant evidence | Improve retrieval and tool configuration | Better evidence beats better wording |
| The answers are close but consistently misframed | Tune prompts and tool descriptions | The prompt layer finally has a clean signal |
| The workflow fails in patterned ways across layers | Rework decomposition or topology | Structural change is now justified by evidence |
| The system is stable and well measured | Add bounded feedback loops | Only now does self-improvement have a trustworthy target |

The order is conservative because most systems do not fail from insufficient ambition. They fail from premature complexity.

## Cheap Fixes Come Before Clever Ones

A surprising amount of agent pain comes from cheap surfaces that teams skip because they are not glamorous enough.

Schemas are one of them. If an enterprise agent keeps forcing manual corrections because its artifacts are hard to consume, that is often not a prompt problem. It is an interface problem. The same is true in coding systems where diff shape and verification handoff are poor, or in browser agents where the state summary is too loose for safe action.

Retrieval and tool descriptions are another. A weak answer can look like weak reasoning when the real issue is that the system never saw the right evidence or kept reaching for the wrong tool.

These are precisely the surfaces the use-case architectures in this repo emphasize. The enterprise architecture tracks reviewer correction frequency, approval-hit rate, and retrieval relevance quality. The coding architecture cares about regression rate, scope adherence, and reviewer acceptance. The web architecture tracks navigation recovery, submission error rate, and extraction accuracy. Those are not auxiliary metrics. They are where the system tells you what hurts.

This is the operational version of the chapter's main claim. Optimize the workflow the way you would optimize any production system. Start where failure is cheapest to localize and cheapest to correct.

## Measurement Is Part Of The System

Teams still talk about evaluation as though it were a separate phase that begins after the system exists. That is a category error.

A real evaluation layer is part of the architecture. It has defined inputs, defined outputs, owners, and stored comparisons over time. It tracks quality, latency, cost, retries, approval burden, tool-use quality, and human correction load against representative cases. It catches regression before a change is mistaken for progress.

This is where model-based judging becomes useful, with discipline. *MT-Bench* and related work helped normalize LLM-as-judge because human review does not scale to every experiment. The right lesson is not that model judges are magically reliable. It is that they can become useful instruments if they are calibrated against human judgment on relevant samples and used inside a larger evaluation design.

Optimization without measurement architecture is just editing with better branding.

## Self-Improvement Is Late And Bounded

The more ambitious optimization literature belongs in the story, but it belongs near the end.

*TextGrad* matters because it broadens the unit of optimization beyond one prompt. Feedback can flow across a compound textual system. *Reflexion* matters because reviewed failure can become reusable signal instead of a dead log entry. *AFLOW* matters because workflow structure itself can become searchable.

All three ideas are useful. All three are dangerous when the baseline is still unstable.

If schemas are still sloppy, retrieval is still weak, or the failure taxonomy is still muddy, a self-improving system will optimize around noise. It will make local changes that look persuasive against an unstable target, and the team will call the drift intelligence because the system was the author of its own edits.

Bounded self-improvement is a stricter and more believable idea. Improve only the surfaces you can validate. Promote only the routines that have earned promotion. Search workflow structure only after simpler explanations for failure have already been ruled out.

In a mature system, self-improvement should feel less like science fiction and more like controlled maintenance.

## What The Live System Already Knows

A system that has been in production for months has something a prototype never has: operational evidence.

It has real latency distributions rather than guesses. It has correction logs rather than memories of the last painful incident. It has evidence about which task classes fail most often, which tools are rarely useful, which approval gates fire constantly, and which retrieval patterns return noise.

That evidence is where the optimization signal lives. The prompt-churn team from the opening example already had it. If they had built an evaluation set from their correction stream and separated failures by type, they likely would have discovered that one document class with underspecified metadata caused most of the pain. A schema and retrieval repair would have helped more than another week of prompt edits.

That is why optimization belongs at the end of this series. It depends on the earlier layers being real enough to observe.

Optimization starts when the workflow can tell you where it hurts.

## Resources And References

*OPRO* matters because it turns prompt improvement into a measured search problem over a fixed objective. Its lasting contribution is not that prompts can improve. It is that improvement is meaningless without stable evaluation.

*TextGrad* extends that logic across larger textual systems. It is useful because it treats compound workflows, not just one prompt, as optimization targets that can receive structured feedback.

*Reflexion* belongs here because it is the clearest lighter-weight example of learning from reviewed failure without pretending the whole system should freely rewrite itself.

*AFLOW* matters as the escalation reference for workflow search. It helps make the search-for-structure move concrete, which also makes it easier to see why that move should come late.

*MT-Bench* and *Chatbot Arena* matter because they helped normalize scalable model-based judging while also making its limitations legible. They are useful as evaluation pattern references, not as substitutes for task-specific measurement.
