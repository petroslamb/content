# Operating Agents VI: The Workflow Is the Object

## How To Improve An Agent System That Already Works

*Operating Agents VI of VI*

*The opening case in this essay is a composite of common production failures, not a report of one named company.*

---

A document-classification agent had been in production for three months. It was not perfect, but it was useful. A human corrected the tail of the work, and the overall economics still made sense. Then the team decided to improve it.

Over the next six weeks they edited the system prompt repeatedly. Some edits seemed to help the recent failures they were staring at. Later edits quietly regressed other cases. The prompt grew longer. Tool descriptions changed. Nothing about the underlying evidence improved because there was no stable evaluation set, no clean record of which failure types mattered most, and no agreement about whether latency and correction rate were part of the objective or merely unfortunate side effects.

This is the flattering mistake that makes optimization feel productive when it is not. Teams call prompt churn optimization because the prompt is the surface they can see and edit quickly.

The stricter default is more disciplined. Optimization begins with measurement, not edits. The unit of improvement is the workflow, not the prompt. The first question is not "what wording should we try next?" It is "which layer is failing often enough to deserve intervention?"

---

## Prompt Tuning Is Usually A Late Move, Not The First Move

Once a system exists, the instinct to optimize locally becomes very strong. A bad output appears, and the fastest action is to change the prompt. Sometimes that works. Just as often it misdiagnoses the layer.

An agent workflow usually has several improvement surfaces: output schemas, tool descriptions, retrieval configuration, workflow decomposition, prompts, and feedback loops. Any one of them can be the true source of visible failure. A malformed output can look like a reasoning issue when it is actually a schema issue. A weak answer can look like a prompt issue when retrieval brought in the wrong evidence. A brittle workflow can look like a model issue when the steps are in the wrong order.

This is why *OPRO* matters conceptually. It treats prompt optimization as a measured search problem over examples rather than as artisanal tinkering. The important word there is examples. Without a fixed evaluation set, there is no stable signal against which a candidate change can be judged. *TextGrad* pushes the point further by treating the whole textual workflow as an object that can receive feedback, not just the final prompt.

Those papers are valuable because they point away from the comforting fantasy that good optimization is mainly a matter of clever phrasing. The workflow is the object.

---

## The Right Optimization Order Is More Conservative Than People Want

The field tends to discuss optimization at the exciting end: automatic prompt search, topology search, self-improving graphs, systems that rewrite themselves. Production teams usually need a much stricter order.

First, lock an evaluation set. If you do not have a fixed set of representative cases with known good outcomes, you do not yet have optimization. You have taste and anecdotes.

Second, fix schemas and contracts. A surprising amount of system pain comes from outputs that are hard for downstream components to consume reliably. Clean schemas are often the cheapest high-impact improvement.

Third, fix retrieval. If the workflow keeps reasoning over weak or partial evidence, prompt edits are often compensating for missing context rather than correcting the real problem.

Fourth, improve prompts and tool descriptions against the fixed evaluation set. At this point the signal is stronger because the upstream layers are less noisy.

Fifth, revisit workflow topology. Only once the local surfaces are reasonably clean does it make sense to ask whether the steps themselves are in the wrong order or whether the decomposition is wrong.

Last, and only last, consider self-improvement loops or topology search. Those methods may be real contributions, but they are the most expensive place to hide a bad diagnosis.

## Optimization Sequence Map

| Signal you see | First intervention | Why it comes first | Do not jump to |
|---|---|---|---|
| Results feel inconsistent but no one can prove regression | Build evaluation set and baseline metrics | Without a stable objective, every change is guesswork | Prompt rewrites driven by recent anecdotes |
| Downstream failures on otherwise decent answers | Tighten output schema and contracts | Schema fixes are cheap and remove whole classes of failure | Model upgrades |
| The system reasons over weak or irrelevant evidence | Improve retrieval configuration and source weighting | Better evidence beats better wording | Complex prompt layering |
| The answers are close but consistently misframed | Tune prompts and tool descriptions against the eval set | Now the prompt layer has a clean signal | Workflow topology search |
| The workflow still fails in patterned ways across layers | Rework task decomposition or topology | Structural failure finally justifies structural change | Blind self-improvement loops |
| The system is stable and well measured | Add bounded feedback loops | Now there is a trustworthy objective | Unbounded autonomous mutation |

This map is intentionally conservative because most systems fail from premature complexity, not from insufficient ambition.

---

## Measurement Is Not Overhead

The easiest way to see optimization clearly is to stop treating evaluation as a phase and start treating it as part of the system.

A real evaluation layer has defined inputs, defined outputs, and owners. It records accuracy, latency, cost, retries, approval rates, and human correction rates against a representative set of tasks. It catches regression before a change is mistaken for progress. It tells the team whether the system is improving in the dimensions that matter rather than in the dimensions that happen to be visible on a given afternoon.

This is where LLM-as-judge work becomes useful, though only with discipline. *MT-Bench* and related work show why model-based evaluation can scale coverage for complex outputs. They also show why calibration is not optional. A judge that has not been compared against human labels on a relevant sample is not a measurement instrument yet. It is a guess generator in evaluation clothing.

The important point is not that every team must adopt LLM judges. The important point is that optimization without measurement architecture is just editing with better branding.

---

## Self-Improvement Is Late And Bounded

This part would be incomplete if it ignored the more ambitious optimization literature. *AFLOW* and *GPTSwarm* matter because they treat workflow structure itself as searchable. *Reflexion* and *Voyager* matter because they show lighter ways systems can improve from failure and success traces over time.

What builders should take from that literature is not excitement first. It is sequence and scope.

Feedback loops are useful when the system is already stable enough to trust the signal that feeds them. A reviewed correction can become a better prompt, a reusable skill, or a tighter procedure. A system that is still unstable at the schema, retrieval, or topology level should not be given permission to rewrite itself in broad ways. It will optimize around noise, bypass guardrails, or entrench the wrong local behavior because the objective itself is still muddy.

That is the real lesson of bounded self-improvement. Improve only the surfaces you can validate. Promote only the routines that have earned promotion. Search topology only after the simpler explanations for failure have been ruled out.

In a mature system, self-improvement should feel less like science fiction and more like controlled maintenance.

---

## What The Live System Already Knows

A system that has been in production for months has something a prototype does not have: operational evidence. It has real latency distributions, not guesses. It has correction logs, not memories of the worst recent incident. It has evidence about which task classes break most often, which tools are rarely useful, which approval gates fire constantly, and which retrieval patterns return noise.

That evidence is where the optimization signal lives. The prompt-churn team from the opening example already had it. They simply were not using it. If they had built an evaluation set from human corrections, separated the failures by type, and inspected the distribution before editing, they likely would have discovered that one document class with underspecified metadata accounted for most of the pain. A schema and retrieval fix would have helped far more than a week of prompt rewrites.

That is why optimization belongs at the end of this series. It depends on the earlier layers being real enough to observe. Before that point, "optimization" is often just a smarter word for experimentation.

Optimization starts when the system can tell you where it hurts.

---

## Resources And References

### [Builder Blueprint: Optimization and Self-Improvement](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/practical-chapter-blueprints/04-optimization-self-improvement-blueprint.md)

For the companion technical note, use this public blueprint. It keeps the optimization order, comparison matrix, anti-patterns, and evaluation checklist in a more operational format than the essay. That makes it useful once a system is live enough that the question is no longer what to build, but where to push for improvement first.

### [Large Language Models as Optimizers](https://arxiv.org/abs/2309.03409) (2024)

*OPRO* matters because it takes prompt improvement out of the realm of artisanal tweaking and turns it into a measured search problem over a fixed evaluation set. That is why it is one of the core papers behind this essay. Its deepest contribution is not that prompts can improve. It is that improvement is meaningless without a stable objective.

### [TextGrad: Automatic "Differentiation" via Text](https://arxiv.org/abs/2406.07496) (2024)

*TextGrad* extends the same logic beyond one prompt. Its contribution is a way to think about multi-component textual workflows as things that can receive structured feedback across the system, not just at the final answer. In the essay it supports the claim that the workflow, not the node, is the true object of optimization.

### [AFLOW: Automating Agentic Workflow Generation](https://arxiv.org/abs/2410.10762) (2025)

*AFLOW* matters because it makes workflow structure itself a search space. That is a real advance, but it appears in this essay with a warning attached. Its value is clearest once simpler layers such as schemas, retrieval, and prompts have already stabilized. That makes it an escalation reference rather than a starting recommendation.

### [GPTSwarm: Language Agents as Optimizable Graphs](https://arxiv.org/abs/2402.16823) (2024)

*GPTSwarm* pushes the workflow-optimization story into graph form. It matters in this essay because it makes explicit how ambitious the search-for-structure move can become. That is helpful precisely because it sharpens the conservative rule: do not jump to graph optimization while still misdiagnosing local component failures.

### [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) (2023)

*Reflexion* is one of the most useful lighter-weight references here because it shows how reviewed failure can become a reusable signal for future improvement. In the essay it stands for bounded self-improvement done correctly: narrow scope, concrete lessons, and feedback grounded in actual outcomes rather than self-congratulating drift.

### [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) (2023)

*Voyager* matters in this part because it frames self-improvement through skill accumulation rather than unrestricted self-mutation. The paper's skill library is a strong example of how a system can build up reusable competence while preserving the asymmetry the essay cares about: adding validated routines is safer than letting the system freely tear down its own architecture.

### [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) (2023)

This paper is useful because it makes evaluation scale practical while also clarifying the calibration burden that comes with it. In the essay it supports the point that model-based judges can be part of a serious evaluation layer, but only if they are checked against human labels and treated as instruments that require validation rather than as automatic truth machines.
