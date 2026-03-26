# Chapter 2 Blueprint: Reasoning and Planning

## Why This Chapter Matters

Reasoning is the chapter that tells you how the agent should think through work. It matters because agent failures are often blamed on "the model," when the real problem is that the workflow lacks the right reasoning scaffold. A base model can be capable and still fail because the task needs decomposition, tool interaction, critique, or search.

This chapter is practical because it shows that reasoning is not one thing. There are lightweight defaults, reliability overlays, and expensive search-heavy escalations. The job of a builder is not to admire the taxonomy. It is to choose the cheapest reasoning structure that reliably solves the task.

## Survey Subsections To Prioritize

- `2.2.2 Dynamic Reasoning Structures`
- `2.2.2.2 Static Reasoning Structures`
- `2.2.3 Unstructured Reasoning`
- `2.2.4 Planning`

The unified formalism can be skimmed. The named reasoning patterns are what matter for implementation.

## The Practical Question

The chapter is answering two questions:

1. How should the agent structure reasoning for this task?
2. When should reasoning become planning over actions rather than just verbal problem solving?

Those are related but not identical. A reasoning method can improve answers without ever touching the world. A planning method has to decide what sequence of actions should happen next.

## Core Literature And What Each Paper Adds

### `ReAct: Synergizing Reasoning and Acting in Language Models`

ReAct is the control-loop paper. It matters more than almost anything else in the practical stack because it joins thought to action. The agent reasons, acts, observes, and continues. That is the backbone for tool-using agents.

Use this paper as the default reasoning pattern whenever external state, tools, or long tasks are involved.

### `Self-Consistency Improves Chain of Thought Reasoning in Language Models`

Self-Consistency is the canonical reliability-through-sampling paper. It does not change the workflow topology much, but it gives a strong answer to one common failure mode: brittle single-pass reasoning.

Use it when reliability matters more than latency and the cost of multiple traces is acceptable.

### `SELF-REFINE: Iterative Refinement with Self-Feedback`

Self-Refine is one of the cleanest draft-critique-revise loops. Its practical value is that it is cheap to add and often effective on structured outputs, explanations, and multi-step reasoning.

Use it when the first answer is often improvable by one or two focused critique passes.

### `Reflexion: Language Agents with Verbal Reinforcement Learning`

Reflexion matters because it stretches critique across attempts. Instead of only fixing the current answer, it stores lessons from failure and uses them later.

Use it when the environment provides clear success or failure signals and repeated attempts are part of the task.

### `Chain-of-Verification Reduces Hallucination in Large Language Models`

CoVe is the most practically important factual-safety reasoning pattern in the chapter. It decomposes verification into a separate step rather than hoping the original answer is self-consistent.

Use it for high-stakes factual outputs, synthesis, and anything that will later trigger actions.

### `Tree of Thoughts: Deliberate Problem Solving with Large Language Models`

Tree of Thoughts turns reasoning into a branching search process. It matters because some tasks truly have dead ends and alternative paths that a single chain cannot handle well.

Use it only when the task profile justifies branching search.

### `Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models`

LATS adds a more formal search layer over agent action and reasoning. It is powerful, but it is not a default production method because it adds cost, latency, and orchestration complexity.

Use it when planning quality is worth a much heavier control loop.

### Additional Patterns The Chapter Makes Practical

`Least-to-Most Prompting Enables Complex Reasoning in Large Language Models` matters because decomposition is often more valuable than cleverness. `Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models` matters because some failures are conceptual, not local. `LLM+P: Empowering Large Language Models with Optimal Planning Proficiency` matters because some planning problems need a formal planner, not just better language.

## If Your Problem Looks Like X, Choose Y

- If the task is multi-step but mostly deterministic, choose decomposition first.
- If the task interacts with tools or live state, choose ReAct.
- If the first answer is close but weak, choose Self-Refine.
- If factual mistakes are the real risk, choose Chain-of-Verification.
- If one trace is too brittle but consensus is cheap enough, choose Self-Consistency.
- If the task has real dead ends and alternative paths, escalate toward Tree of Thoughts or LATS.

## Method Comparison Matrix

| Method | Best use | Main strength | Main risk | Escalate when |
| --- | --- | --- | --- | --- |
| Decomposition | structured multi-step tasks | cheap and legible | no grounding in external state | live tools or environment feedback matter |
| ReAct | tool-using tasks | reasoning tied to observation and action | still needs verification and bounded tools | first-pass outputs stay brittle |
| Self-Refine | near-miss outputs | cheap iterative improvement | can polish ungrounded work | repeated factual errors remain |
| Chain-of-Verification | high-stakes factual work | explicit verification path | extra latency and cost | branching difficulty dominates |
| Self-Consistency | brittle single traces | reliability through sampled consensus | expensive for routine tasks | task genuinely benefits from multiple traces |
| Tree of Thoughts or LATS | branching planning problems | search over alternatives | heavy orchestration and latency | simpler scaffolds no longer solve the task |

## The Chapter's Main Architectural Insight

The best insight in the chapter is not any single method. It is the selection logic:

- use decomposition for structured multi-step problems
- use ReAct when tools or environment state matter
- use self-refinement or verification when first-pass answers are brittle
- use self-consistency when correctness matters more than latency
- use search only when the task has real branching difficulty

This turns reasoning from a bag of prompts into an architectural menu.

## The Default Reasoning Blueprint

### Stage 1: Decompose

Turn the task into a bounded set of subgoals or steps. If the problem is long or ambiguous, define intermediate artifacts or checkpoints instead of asking the model to improvise the whole path.

### Stage 2: Run a ReAct Loop

Use a thought-action-observation cycle as the default execution-time reasoning pattern. This grounds reasoning in the current state of the world.

### Stage 3: Verify

Run a lightweight self-check or explicit verification pass before finalizing high-value outputs. Verification is a core step, not a polish step.

### Stage 4: Learn If The Task Repeats

If the same task class recurs, store lessons, critiques, or better subplans so that later attempts improve.

## Decision Rules

### Use plain decomposition when

The task is multi-step but mostly deterministic, and tool interaction is limited.

### Use ReAct when

The system needs tools, search, code execution, browsing, or live state inspection.

### Add self-refinement when

Outputs are close but often weak in clarity, structure, or consistency.

### Add CoVe when

The output makes factual claims that could trigger wrong decisions or wrong actions.

### Add self-consistency when

Different reasoning traces often converge on the right answer and the latency budget allows sampling.

### Add search methods when

There are many plausible reasoning paths, many dead ends, or planning quality dominates cost concerns.

## Failure Modes

- overusing chain-of-thought without environment grounding
- adding search where decomposition would be enough
- confusing verbal fluency with validated reasoning
- using critique loops without measurable improvement
- letting the model plan actions it cannot actually execute

## Evaluation

The reasoning stack should be judged by:

- first-pass success rate
- post-verification success rate
- tool-grounded plan coherence
- hallucination reduction
- latency and token cost per solved task
- failure recurrence after reflection or critique

The right metric is not "how impressive the reasoning trace looks." It is whether the reasoning structure improves task completion.

## Recommended Build Order

1. Start with decomposition plus ReAct.
2. Add a small verification step.
3. Introduce self-refinement where outputs are near-miss rather than wildly wrong.
4. Add self-consistency only for tasks where it clearly buys accuracy.
5. Escalate to search methods only for high-value, branching-heavy tasks.

## Anti-Patterns

- Do not make tree search the default.
- Do not confuse more reasoning tokens with better plans.
- Do not use debate or critique when the task lacks a real evaluation signal.
- Do not let the reasoning layer stay disconnected from tools or state when the task depends on them.

## Reading Sequence For This Chapter

1. `papers/react.md`
2. `papers/least_to_most_prompting.md`
3. `papers/step_back_prompting.md`
4. `papers/llm_plus_p.md`
5. `papers/self_refine.md`
6. `papers/chain_of_verification.md`
7. `papers/self_consistency.md`
8. `papers/reflexion.md`
9. `papers/tree_of_thoughts.md`
10. `papers/lats.md`

## Bottom Line

The practical chapter blueprint is not "use the smartest reasoning method." It is "use the lightest reasoning structure that makes the task reliable." For most real systems, that means decomposition, ReAct, and verification before anything more exotic.
