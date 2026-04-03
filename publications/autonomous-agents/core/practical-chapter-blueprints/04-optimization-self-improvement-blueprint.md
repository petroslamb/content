# Chapters 9 and 11 Blueprint: Optimization and Self-Improvement

## Use This Blueprint When

Use this blueprint when the workflow already exists and the problem is no longer invention but improvement. The important question is not how to make the agent look smarter. It is where improvement pressure should land first, what evidence should justify escalation, and which parts of the workflow should remain off-limits to automatic change.

## The Decision

Optimization becomes useful only after three things are true:

1. The workflow can be evaluated repeatedly on stable cases.
2. Failures can be localized to real surfaces rather than vague impressions.
3. The team can tell improvement from drift.

Once those conditions hold, the question becomes straightforward: which surface is actually failing, and what is the cheapest safe change that could improve it?

## Default Position

The optimization stack should remain deliberately conservative.

- Freeze an evaluation set before tuning anything.
- Measure the current workflow before changing it.
- Improve schemas, prompts, retrieval, and tool contracts before changing topology.
- Add critique or reflection loops only where repeated failures justify them.
- Use workflow search and broader self-improvement only after the baseline is stable, instrumented, and worth the added complexity.

Optimization should feel like production engineering, not like prompt folklore.

## Default Build

### Step 1: Lock The Evaluation Set

Build a representative set of repeatable tasks first. If the workflow cannot be measured consistently, optimization will mostly create motion without learning.

### Step 2: Measure The Current System

Track quality, latency, cost, tool-use quality, retry behavior, escalation rates, and failure categories. The workflow has to become legible before it becomes optimizable.

### Step 3: Improve The Cheapest Surfaces First

Start with the surfaces that usually carry the highest leverage and the lowest risk:

- output schemas
- prompt clarity
- retrieval configuration
- tool descriptions and argument contracts
- retry, stop, and fallback policy

### Step 4: Add Feedback Loops Where Repetition Exists

Use critique, reflection, or memory-backed improvement only where failures repeat and the signal is trustworthy. A feedback loop without a real signal is just a new source of drift.

### Step 5: Search Workflow Structure Only After Stability

Workflow generation, topology search, graph optimization, and more ambitious self-improvement belong late. They are not starting moves. They become useful only after the simpler surfaces are already measured and mostly under control.

## Escalate When

- One or two nodes are underperforming while the rest of the workflow is stable.
- Tool failures dominate end-task quality, which points to catalog, routing, or schema problems.
- The workflow shape itself seems wrong and local tuning is no longer enough.
- Human evaluation no longer scales and comparative scoring support is necessary.
- The environment is bounded enough that tightly constrained online adaptation becomes justifiable.

## Alternatives And When They Win

| Method | Best use | Why it wins | Main risk |
| --- | --- | --- | --- |
| Prompt and schema optimization | local node weakness | highest leverage for the lowest risk | overfitting to a narrow eval set |
| Retrieval and tool-contract tuning | wrong tool choice or weak grounding | improves end-task behavior directly | hidden regressions without instrumentation |
| Self-Refine or Reflexion loops | repeated near-miss failures | adds cheap feedback where repetition exists | noisy critique if the signal is weak |
| LLM-as-judge evaluation support | broader comparative review | scales assessment beyond full human review | calibration drift and blind spots |
| AFLOW or GPTSwarm style workflow search | mature multi-node workflows | searches structure instead of wording | premature complexity and noisy search |
| Online self-improvement | bounded environments with strong signals | adapts between or during runs | mutating the wrong surfaces under weak oversight |

## What To Measure

- Task quality and pass rate
- Tool invocation accuracy
- Retrieval quality
- Latency and cost
- Stability across repeated runs
- Regression rate after changes
- Operator burden, including review and debugging cost

An optimization loop without regression checks is a drift generator.

## Failure Review

- Tuning prompts before freezing an evaluation set
- Searching topology before fixing obvious local defects
- Treating benchmark movement as proof of production improvement
- Using LLM-as-judge without calibration spot checks
- Allowing self-improvement to alter safety-critical surfaces directly
- Optimizing quality without measuring operator or latency cost

## Reading Sequence

1. `../../essays/optimization/06-workflow-optimization-and-evaluation.md`
2. `../../essays/optimization/companion.md`
3. `../../reference/papers/opro.md`
4. `../../reference/papers/textgrad.md`
5. `../../reference/papers/self_refine.md`
6. `../../reference/papers/reflexion.md`
7. `../../reference/papers/voyager.md`
8. `../../reference/papers/mt_bench_chatbot_arena.md`
9. `../../reference/papers/aflow.md`
10. `../../reference/papers/gptswarm.md`

Return to survey sections `9.2`, `9.2.3`, `9.3`, `9.4`, `9.4.3`, and `11.1` when the local optimization question is clear enough to justify the broader map.

## Bottom Line

Optimize the workflow the way you would optimize any production system. Freeze the evaluation set, measure the baseline, improve the cheapest surfaces first, and treat self-improvement as a bounded engineering choice rather than a license for self-redesign.
