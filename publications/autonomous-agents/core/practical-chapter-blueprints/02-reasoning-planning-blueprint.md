# Chapter 2 Blueprint: Reasoning and Planning

## Use This Blueprint When

Use this blueprint when the workflow is failing because it does not know how to work through the task, not because it lacks data, tools, or permissions. The important question is not whether the model can sound intelligent. It is what control structure the task requires and what level of reasoning cost the task can justify.

## The Decision

Every reasoning design has to answer two questions:

1. What structure should the workflow use to work through this task?
2. When does reasoning need to become planning over actions rather than verbal problem solving alone?

The right answer is almost never the most elaborate method available. It is the cheapest structure that makes the task reliable.

## Default Position

The default reasoning stack should be simple and explicit.

- Decompose the task into bounded steps or artifacts.
- Use a ReAct-style loop whenever tools or live state matter.
- Add an explicit verification pass before trusting important outputs.
- Store lessons only when the same task class repeats.
- Escalate to heavier search only when the task has real branching difficulty.

Most reasoning failures in production are not frontier failures. They are control failures. The workflow is under-structured, under-grounded, or under-checked.

## Default Build

### Stage 1: Decompose

Break the job into bounded subgoals, checkpoints, or artifacts. If the task is long, ambiguous, or multi-stage, do not ask the model to improvise the whole path in one fluent pass.

### Stage 2: Run A Grounded Loop

Use a ReAct-style thought, action, and observation loop whenever the workflow interacts with tools, search, code, browsing, or other live state. Reasoning becomes more reliable when it is tied to observable state instead of remaining purely verbal.

### Stage 3: Verify

Run a separate self-check or verification pass before finalizing outputs that carry factual, operational, or policy weight. Verification is not polish. It is the point where the workflow decides whether the first pass deserves trust.

### Stage 4: Learn Only Where Repetition Exists

If the same task class recurs, store critiques, lessons, or better subplans so later attempts improve. If the task is mostly one-off, do not force a learning loop into it.

## Escalate When

- A multi-step task is still failing after clean decomposition.
- Tool-using work remains brittle because the reasoning loop is not grounded tightly enough in observations.
- First passes are close but weak, which justifies critique and revision.
- Factual errors remain the dominant failure mode, which justifies explicit verification.
- One reasoning trace is too brittle and the latency budget can afford multiple traces.
- The task genuinely contains dead ends, competing paths, or heavy planning pressure.

## Alternatives And When They Win

| Method | Best use | Why it wins | Main risk |
| --- | --- | --- | --- |
| Decomposition | structured multi-step tasks | cheapest strong default | no live grounding by itself |
| ReAct | tool-using or stateful work | ties reasoning to observation and action | still needs bounded tools and verification |
| Self-Refine | near-miss outputs | cheap critique and revision loop | can polish ungrounded errors |
| Chain-of-Verification | factual or high-stakes outputs | separates answer generation from checking | extra latency and cost |
| Self-Consistency | brittle single traces | improves reliability through sampled agreement | expensive for routine work |
| Tree of Thoughts or LATS | branching planning problems | searches alternate paths explicitly | heavy orchestration and poor default economics |
| Formal planning via LLM+P style handoff | strongly structured planning problems | uses a real planner where language alone is weak | too heavy for loosely structured work |

## What To Measure

- First-pass success rate
- Post-verification success rate
- Tool-grounded plan coherence
- Hallucination reduction
- Latency and token cost per solved task
- Recurrence of previously corrected failures

The right metric is task completion under control, not how impressive the reasoning trace looks.

## Failure Review

- Using longer chain-of-thought instead of better task structure
- Leaving reasoning disconnected from live state when tools matter
- Adding critique loops without a real signal of improvement
- Using search where decomposition would have been enough
- Letting the model plan actions it cannot actually execute
- Treating verbal fluency as evidence of reasoning quality

## Reading Sequence

1. `../../essays/reasoning/03-reasoning-scaffolds-and-planning.md`
2. `../../essays/reasoning/companion.md`
3. `../../reference/papers/react.md`
4. `../../reference/papers/least_to_most_prompting.md`
5. `../../reference/papers/step_back_prompting.md`
6. `../../reference/papers/self_refine.md`
7. `../../reference/papers/chain_of_verification.md`
8. `../../reference/papers/self_consistency.md`
9. `../../reference/papers/reflexion.md`
10. `../../reference/papers/tree_of_thoughts.md`
11. `../../reference/papers/lats.md`
12. `../../reference/papers/llm_plus_p.md`

Return to survey sections `2.2.2`, `2.2.2.2`, `2.2.3`, and `2.2.4` when you need the broader reasoning taxonomy rather than the operating default.

## Bottom Line

Reasoning should be treated as a control problem, not a theater problem. Start with decomposition, grounded loops, and verification. Add critique, sampling, or search only when failure analysis shows that the simpler structure is no longer enough.
