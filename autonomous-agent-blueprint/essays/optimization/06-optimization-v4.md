# Operating Agents Bonus: The Workflow Is the Object

A team spent three weeks optimizing their research agent. They lengthened the system prompt, added more examples, tweaked temperature, refined the role description. Each change felt like improvement for one task, but another task quietly regressed. Latency grew from 4 seconds to 12. Cost doubled. They had no evaluation set, no stable metrics, no regression detection. They were editing by taste, not by engineering. The output looked cleaner for a day, then a different failure mode resurfaced in a form they could no longer explain.

What they were doing was not optimization. It was prompt churn without measurement. The workflow itself was the object, but they kept polishing the most visible surface.

That is where most agent teams start lying to themselves. They say they are improving the system, but what they are really doing is editing visible surfaces until the latest run *feels* better. A prompt becomes longer. An example is added. A role is split. A tool description is rewritten. A retrieval threshold moves. The output looks cleaner for a day, then a different task regresses, latency grows, cost drifts upward, or a hidden failure mode resurfaces in a form the team can no longer explain. None of this is unusual. It is what optimization looks like when the workflow is not yet being treated as an object with stable evaluation, measurable components, and explicit regression discipline.

## Optimization Is Not Prompt Engineering

Once a system exists, improvement pressure can land on several surfaces:

1. **Prompts and schemas** (the most visible)
2. **Workflow topology** (role arrangement, node order, handoff structure)
3. **Tool descriptions and routing** (function specs, parameter validation, error handling)
4. **Memory-backed feedback loops** (Reflexion-style lessons, Voyager-style skill accumulation)
5. **Broader workflow search or self-improvement** (topology optimization, unconstrained mutation)

The practical question is not which of these methods sounds most advanced. The practical question is where the failure actually lives and whether the evaluation layer is stable enough to tell improvement from drift.

[*OPRO*](https://arxiv.org/abs/2309.03409) and [*TextGrad*](https://arxiv.org/abs/2406.07496) capture the appeal of optimization in its cleanest form. They treat prompts and textual systems as optimization targets rather than as artisanal drafts that improve only through intuition. That shift is useful because it disciplines a part of the workflow many teams otherwise edit by taste. If a node's outputs can be evaluated reliably, then prompt and schema changes can be explored with something closer to a real search process (Yang et al.; Yuksekgonul et al.)

But both papers have a hard precondition: **the outputs must be measurable**. Without a fixed evaluation set, a stable objective function, and a regression discipline, optimization becomes theater. OPRO-style iteration quickly becomes structured overfitting. TextGrad's "gradients" are only as meaningful as the judge that produces them.

The blueprint is especially right to insist that **workflow structure often matters more than prompt phrasing** once a system has grown beyond a trivial baseline. If the wrong tool is being called, if the wrong role is making the decision, if the order of stages is wrong, or if the output schema is creating downstream brittleness, then another round of prompt polishing will not fix the actual problem. It may hide it temporarily. [*AFLOW*](https://arxiv.org/abs/2410.10762) and [*GPTSwarm*](https://arxiv.org/abs/2402.16823) push this idea to its logical conclusion: they treat the workflow itself as the searchable structure. But that move only becomes defensible after the cheaper surfaces are stable and instrumented. Otherwise search merely explores a confused design space faster.

This is why the optimization chapter belongs after safety, not before it. Optimization changes the system. If trust boundaries are weak, approvals are vague, or the evaluation layer is thin, then optimization simply accelerates instability. A workflow that cannot explain its own current behavior is not ready to search over alternative topologies. The right order is humbler.

## Companion Note

This essay presents a focused narrative for a broad audience. For the full technical scope—including what this essay intentionally leaves out, how it maps to the chapter blueprint, and recommended deeper reading—see the [companion note](companion.md).

## The Four Levers, in Order

The practical doctrine is deliberately plain. Improve in this order:

### 1. Schema, Retrieval, Tools (Cheapest, Highest Impact)

Before touching prompts, ensure:
- Output schemas are clear and match downstream consumers
- Retrieval configuration is sensible (chunk size, embedding model, reranking, filters)
- Tool descriptions are accurate, parameters well-typed, error handling explicit
- Routing logic is correct (which tool for which task)
- Retry policies are appropriate

These are often the actual bottlenecks. A vague tool description or a brittle schema creates more degradation than a suboptimal prompt ever did.

### 2. Prompt Refinement (After Above Are Stable)

Once schemas, tools, and retrieval are correct, then—and only then—does prompt optimization begin to matter. [*OPRO*](https://arxiv.org/abs/2309.03409) shows that prompts can be optimized through search when the evaluation signal is stable. The contribution is real. The precondition is everything. Without stable eval, you are just overfitting to the latest few examples.

### 3. Feedback Loops (Bounded Self-Improvement)

[*Reflexion*](https://arxiv.org/abs/2303.11366) and [*Voyager*](https://arxiv.org/abs/2305.16291) show that not all improvement requires global redesign. A system can improve through:
- **Critique loops** (Reflexion: store failure as reusable verbal lesson)
- **Skill accumulation** (Voyager: build a library of successful code-like behaviors)

These are valuable precisely because they are narrower and easier to govern than unconstrained self-modification. They improve future behavior by enriching the workflow's local competence rather than by pretending the whole architecture should mutate itself freely (Shinn et al.; Wang et al.)

### 4. Topology Search (Last, Measured, Constrained)

[*AFLOW*](https://arxiv.org/abs/2410.10762) and [*GPTSwarm*](https://arxiv.org/abs/2402.16823) treat the workflow topology itself as an optimization target. That is an important step for the field because many practical failures do live in role arrangement, node order, and interaction structure rather than in any single prompt.

But topology search is **dangerous** if attempted earlier. It does not fix a poorly specified evaluation. It does not fix incorrect schemas or tool descriptions. It simply explores a confused design space faster. Use it only when:
- The baseline is already stable, reviewed, and instrumented
- You know which component you are trying to optimize (latency? quality? cost?)
- You have a frozen, representative evaluation set
- You have regression detection in place

## Measurement Is Not Overhead. It Is the Product.

The defining characteristic of real optimization is a stable evaluation layer. Before you edit anything, you must have:

1. **A frozen set of test cases** that represent the workload you care about
2. **A fixed set of metrics**: task quality (grounded in correct answers), latency, cost, tool accuracy, retry behavior, failure categories
3. **Regression detection**: every change must be checked against the frozen set; if quality drops on any case, the change is rejected or investigated

Without these, improvement is just drift with intentionality.

This is not a process argument—it is an architecture argument. The evaluation layer is a component of the system. If you do not have it, you do not have an optimization problem. You have a guess.

[*MT-Bench*](https://arxiv.org/abs/2306.05685) and [*Chatbot Arena*](https://arxiv.org/abs/2306.05685) matter because they helped normalize a practical fact: if human evaluation is too expensive to run at every iteration, then some proxy judgment system may be necessary. That move is useful and dangerous. It enables scale, but it also creates a new calibration problem. A judge that is misaligned with the actual business or engineering objective will give the team a false sense of progress. Optimization then becomes more systematic and no less misleading (Zheng et al.)

Use LLM-as-judge only with calibration (spot-check against human labels) and only inside a larger evaluation stack. Never as the sole source of truth.

## Every Optimization Strategy Implies a Theory of Intelligence

The explanatory step is that every optimization method assumes a different answer to "where does intelligence live in the workflow?"

- **Prompt optimization** assumes the node already has the right role and the right information, but is under-specified in how it should use them.
- **Tool optimization** assumes the workflow knows what it wants, but is weak at choosing or parameterizing its instruments.
- **Topology optimization** assumes the architecture itself may be wrong—that the arrangement of roles and handoffs is the bottleneck.
- **Reflection and skill accumulation** assume the system repeats enough work that experience can change future attempts.
- **Judge-based evaluation** assumes the objective is stable enough that comparative scoring is meaningful.

Once those assumptions are visible, many misplaced optimization efforts become easier to diagnose. Teams reaching for topology search often have a prompt or schema problem. Teams reaching for self-improvement often lack a stable evaluation layer. Teams doing endless prompt churn often have the wrong tool or the wrong role making the decision.

## Practically Speaking: Optimization Decision Tree

```
Where is failure?

├─ Wrong tool or wrong parameters?
│   └─ Fix tool descriptions, routing, and schema validation first
│
├─ Output format unusable?
│   └─ Fix schemas and prompts to match downstream consumers
│
├─ Retrieval giving bad evidence?
│   └─ Tune retrieval config, embeddings, chunking, filtering
│
├─ Task genuinely ambiguous or needs multi-step thinking?
│   └─ Add verification or decomposition scaffold (see Reasoning chapter)
│
├─ System repeats same mistakes across attempts?
│   └─ Add feedback loop (Reflexion for lessons, Voyager for skills)
│
└─ Architecture itself may be wrong (role arrangement, handoff order)?
    └─ Only after all above are stable: consider topology search (AFLOW, GPTSwarm)
```

**The cardinal rule:** Optimization is not a creative writing exercise. It is engineering with measurable components.

## Escalation Spine

**Step 1: Define the objective and freeze evaluation.**
Before you change anything, write down what "better" means, and lock a representative set of test cases with ground truth. No edits happen without this.

**Step 2: Measure current performance with granularity.**
Run the baseline. Collect: quality per task, latency, cost, tool call accuracy, retry counts, failure categories. Know where you stand.

**Step 3: Improve the cheapest and safest surfaces first.**
Schemas, retrieval configuration, tool descriptions, obvious routing mistakes, retry policies. These often yield the biggest gains with the lowest risk.

**Step 4: Refine prompts, but only after Step 3 is complete and with evaluation fixed.**
OPRO-style methods are real, but they are conditional. Without stable eval, you are just guessing.

**Step 5: Add bounded feedback loops where justified.**
Reflexion (failure → lesson) or Voyager (success → skill) where the system repeats similar tasks and near-misses are costly. These improve by enriching memory, not by mutating architecture.

**Step 6: Escalate to topology search only after the baseline is stable, reviewed, and instrumented.**
AFLOW and GPTSwarm are legitimate tools, but they are late-stage. They explore a design space that is already well-understood. They do not fix an unstable baseline.

**Step 7: Use LLM-as-judge only with calibration and spot checks.**
Never let the judge be the only evaluation layer. Always have human sanity checks on a subset.

** Throughout: Treat the workflow as an object to be measured, debugged, and changed carefully—not as a creative-writing project with a leaderboard.**

## What to Skip (For Now)

**Out of scope for disciplined optimization:**

- **Prompt churn without measurement.** Editing prompts because "it feels better" is not optimization. It is noise.
- **Unconstrained self-improvement.** Systems that mutate prompts, roles, tools, and approval logic without containment are eroding reviewability, not gaining maturity.
- **Leaderboard-driven tuning.** Optimizing for a benchmark that does not match your actual business or engineering objective is systematic drift.
- **Optimization before evaluation exists.** You cannot improve what you cannot measure. Freeze your test set first.
- **Treating latency or cost alone as the target.** Efficiency without guardrails degrades quality. Optimize within quality constraints.

**If your optimization work feels vague, ask:** Do we have a frozen evaluation set? Do we know which component is failing? Are we changing the cheapest surface first? Or are we reaching for the most sophisticated method before diagnosing the problem?

## Resources And References

### [Builder Blueprint: Optimization and Self-Improvement](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/04-optimization-self-improvement-blueprint.md)

This blueprint matters because it translates the essay's workflow-first argument into a concrete order of operations: evaluation first, cheap surface fixes second, feedback loops third, and architecture search last.

### [Large Language Models as Optimizers](https://arxiv.org/abs/2309.03409) (2024)

OPRO matters because it takes prompt improvement out of the realm of taste and puts it into the realm of search. The paper's contribution is not simply that prompts can be varied and scored. Everyone already does that informally. Its contribution is to formalize the idea that the model can participate in proposing better instructions when evaluation cases provide a stable signal about what "better" means (Yang et al.)

That contribution is powerful and easy to misuse. Without stable evaluation, OPRO-style iteration quickly becomes structured overfitting or simple noise. The right lesson is therefore conditional. Prompt optimization is real, but it becomes serious only when the objective is fixed enough to resist wishful interpretation.

### [TextGrad: Automatic "Differentiation" via Text](https://arxiv.org/abs/2406.07496) (2024)

TextGrad matters because it generalizes the same instinct to broader textual systems. Instead of treating only prompts as optimization targets, it treats textual feedback as a kind of gradient over a larger computational object. That makes it one of the most conceptually useful papers in the chapter because it pushes the field away from single-node prompt tweaking and toward multi-step textual optimization (Yuksekgonul et al.)

Its practical limitation is the same as its appeal. Once the system becomes the object, the demand for good evaluation becomes much stronger. TextGrad is useful precisely because it reminds builders that richer optimization objects require richer objective discipline.

### [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) (2023)

Reflexion matters because it shows how a system can improve through verbal reinforcement learning—storing lessons from failure and applying them to future attempts. The approach is narrower than full self-modification and therefore easier to govern. It demonstrates that bounded improvement loops can be effective without surrendering architectural control (Shinn et al.)

That makes Reflexion a key reference for teams that want adaptive behavior without the risks of unconstrained optimization.

### [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) (2023)

Voyager matters because it makes procedural improvement concrete through a skill library. When a system stores successful behaviors as reusable code-like skills, it stops paying repeatedly for discoveries it has already made. That is the clearest practical image of bounded self-improvement in the literature (Wang et al.)

Its embodied setting is not the main point. The transferable lesson is that improvement can come from accumulating and reusing successful patterns, rather than from continuously re-optimizing the entire architecture.

### [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) (2023)

The MT-Bench and Chatbot Arena paper matters because it helped make comparative judgment scalable enough to be operational. In optimization work, that is a significant contribution. Human review is expensive, inconsistent, and difficult to run at every iteration. Some form of automated judgment is often necessary if a workflow is going to be tuned seriously over time (Zheng et al.)

Its danger is equally important. A judgment model does not remove the objective problem. It only makes the proxy cheaper to run. If the proxy is badly calibrated, then the team can optimize faster in the wrong direction. This is why judge-based evaluation belongs inside a larger evaluation stack rather than serving as the only source of truth.

### [AFLOW: Automating Agentic Workflow Generation](https://arxiv.org/abs/2410.10762) (2025)

AFLOW matters because it asks the bold question directly: what if the workflow topology itself is the optimization target? That is an important step for the field because many practical failures do live in role arrangement, node order, and interaction structure rather than in any single prompt. The paper makes it possible to talk about workflow search as a legitimate engineering agenda rather than as speculative hype (Zhang et al.)

But AFLOW also makes the chapter's central warning easier to defend. Topology search is powerful only after the baseline is stable enough to deserve search. Otherwise it becomes a way to automate confusion. The right use of this paper is therefore late, measured, and highly constrained.

### [GPTSwarm: Language Agents as Optimizable Graphs](https://arxiv.org/abs/2402.16823) (2024)

GPTSwarm matters for the same reason as AFLOW. It treats agent workflows as graphs that can be optimized. It shows how language agents can be constructed with explicit nodes, edges, and state, and how that structure opens the door to optimization methods that were previously only applicable to traditional software (Dudziak et al.)

Together, AFLOW and GPTSwarm represent the frontier of workflow-level optimization. They are valuable papers, and they are also the clearest demonstrations of why the optimization chapter belongs at the end of the series: these methods are only safe and sensible when the entire architecture underneath is already stable, measurable, and reviewable.
