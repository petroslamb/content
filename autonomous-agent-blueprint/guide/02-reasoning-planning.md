# Part 2: The Lightest Correct Scaffold

## How Agents Structure Their Thinking Through Work

*Part 2 of 6: A Practical Guide to Foundation Agents*

---

A large insurance company built a document review agent to process incoming claims. The model was strong , one of the best available at the time. The task was well-defined: read an insurance claim document, identify whether it met the criteria for fast-track processing, and produce a structured recommendation. The team spent weeks on prompt craft. They fine-tuned on domain vocabulary. They added more context.

The agent kept failing. Not catastrophically , it rarely said something obviously wrong. But it missed logical dependencies between claim fields. It would classify a claim as fast-track eligible when one of its own stated criteria was not met, having reasoned its way into the answer without checking whether the reasoning path held together. Humans caught these on review and the rejection rate was high enough to eliminate the efficiency gain.

The team's hypothesis was that the model needed to be smarter, or trained on more claims data, or given a longer context window. None of that was the problem. The problem was the workflow was asking the model to answer a complex multi-step judgment question in a single generation pass. The moment someone added an intermediate step , decompose the claim into its logical components, verify each component against the criteria, then make the classification , the failure rate dropped by roughly two-thirds without changing the model.

The scaffold was the problem. The scaffold was also the fix.

---

## Reasoning Failures Are Scaffold Mismatches

The most common misdirection in agent development is attributing reasoning failures to the model. A model reasoning trace that looks wrong , incomplete reasoning, gaps in logic, hallucinated intermediate facts , often indicates that the workflow gave the model the wrong structure for the task rather than that the model is incapable of the task.

This distinction matters because the responses are completely different. If the model is the problem, you upgrade the model. If the scaffold is the problem, you redesign the workflow. Upgrading the model when the scaffold is the problem wastes money and produces marginal gains. Redesigning the scaffold often produces large gains with no model change at all.

*Advances and Challenges in Foundation Agents* (2025) makes this explicit in Chapter 2: the chapter separates reasoning structures from planning structures and classifies the main scaffolding patterns that have emerged around LLMs. Its practical contribution is not the taxonomy for its own sake. It is the selection logic: different task failure modes map to different scaffold choices, and the right scaffold for a task is usually simpler than what practitioners reach for.

The insurance claim case required nothing exotic. Decomposition , breaking a complex judgment into bounded subproblems with typed intermediate outputs , was enough. No search. No debate. No tree search. A structured sequence of simpler questions whose outputs constrained the final classification.

That is the most important practical insight from the reasoning literature: find the cheapest scaffold that makes the task reliable. Not the most sophisticated one. The cheapest correct one.

---

## Four Reasoning Failures and Their Scaffolds

Production reasoning failures cluster around four patterns. Each has a specific scaffold that addresses it. Knowing which failure you face is more useful than knowing the full taxonomy of available methods.

### Failure: Too Shallow

The agent produces an answer that is technically responsive but does not work through the necessary steps. On multi-part questions, it answers the first or easiest part and glosses the rest. On tasks with logical dependencies, it jumps to a conclusion without verifying that the dependencies hold.

The scaffold is **decomposition**. Break the task into a bounded sequence of subproblems. Require the model to produce an intermediate output for each step before moving to the next. Least-to-Most prompting, introduced formally in *Least-to-Most Prompting Enables Complex Reasoning in Large Language Models* (Zho et al., 2022), formalizes this by progressively solving simpler subproblems whose solutions feed into the next. The key mechanism is that decomposition makes logical gaps visible , if step 3 requires an output that step 2 never produced, the gap is explicit rather than implicit. That makes debugging tractable.

Decomposition is particularly strong for enterprise workflows with clear structure: a policy check has components A, B, and C; all three must pass independently before the overall check can pass. Asking the model to assess all three simultaneously in one generation is asking it to hold multiple reasoning threads at once and not drop any of them. Decomposing it into three consecutive checks is cheaper, more reliable, and easier to audit.

### Failure: Brittle Across Attempts

The agent gets the right answer on some runs and the wrong answer on others, on the same input. No prompt change fixes this because the issue is stochastic single-path reasoning.

The scaffold is **self-consistency**. Instead of trusting the output of one reasoning trace, sample several and choose the most common answer. *Self-Consistency Improves Chain of Thought Reasoning in Language Models* (Wang et al., 2022) is the clean formalization of this idea: for tasks where the answer can be verified by agreement rather than by external check, majority voting over multiple traces is often surprisingly effective. The cost is obvious , multiple inference calls per input , but the reliability gain is real, and for tasks where the cost of a wrong answer is high, it is often a rational tradeoff.

The practical use case is narrower than it might appear. Self-consistency works best when multiple reasoning paths are plausible and the correct answer is one that most of them arrive at if they do not go wrong in idiosyncratic ways. It does not work well when the reasoning task requires specific external grounding that a single path would need anyway.

### Failure: Ungrounded from Environment

The agent reasons fluently but ignores what is actually happening in the environment it is supposed to be acting on. It produces a plan that describes what should happen without checking current tool outputs, live data, or intermediate state. Then it acts on its own plan rather than on observed reality.

The scaffold is **ReAct: Synergizing Reasoning and Acting in Language Models** (Yao et al., 2022). ReAct is the most practically important paper in this section of the survey , the one that connected reasoning to external state in permanent and generalizable form. Its structure is a control loop: the model reasons about what to do next, takes an action (queries a tool, retrieves a document, calls an API), observes the result, and continues reasoning from what was actually observed rather than from what was expected.

The grounding that ReAct provides is what prevents the class of failures where an agent reasons correctly given its internal model of the world but incorrectly given the actual world. If the tool returns a different result than the model expected, ReAct allows the next reasoning step to respond to that difference. Without the loop, the model is a good reasoner operating on a stale premise.

For most tool-using agents, ReAct is the default reasoning structure. Not because it is sophisticated, but because it is the minimum necessary structure for a system that acts on live state. Reasoning without grounding, in a system that takes actions, produces confident mistakes.

### Failure: Hallucination-Prone on Factual Claims

The agent makes factual claims that are not derivable from the context it has been given. These claims look like reasoning because they are syntactically consistent with the rest of the output, but they introduce incorrect information that downstream steps inherit and act on.

The scaffold is **Chain-of-Verification** (CoVe, Dhuliawala et al., 2023). CoVe is a structured verification pattern: the model generates an answer, then generates a set of questions that the answer implies should be true, then answers those questions independently (without reference to the original answer), then revises the original answer based on any discrepancies revealed. This multi-step structure prevents the most common hallucination mechanism, in which the model produces a fluent completion that is self-consistent but not consistent with external reality.

CoVe matters specifically for agents because agent outputs become actions. A factual error in a report is unfortunate. A factual error in a structured output that an agent then uses to fill a form, trigger a workflow, or call an API is a failure with real consequences. Verification should sit between reasoning and action wherever the claim is consequential.

---

## The Practical Reasoning Stack

The four scaffolds above combine into a default reasoning stack applicable to most agent workflows:

Start with **decomposition**. If the task has multiple components with dependencies, decompose it into subproblems with typed intermediate outputs before doing anything else. This is not fancy. It is the most reliable first move for most structured, multi-part reasoning tasks.

Run a **ReAct loop** for any task that requires tools, live state, or external information. The reason-act-observe cycle is the backbone of tool-using agents. Without it, reasoning floats free of the environment the agent is supposed to be acting in.

Add **verification** before any high-value factual claim becomes an action or a structured output. The lightweight version is a self-check pass; the stronger version is CoVe-style independent question answering. This is not a polish step , it is the step that closes the hallucination circuit.

Add **self-consistency** for tasks where you can afford the latency and where the model's reasoning is stochastically unreliable in ways that multiple traces would resolve. This is the narrowest application , appropriate for high-stakes, well-defined tasks where answer agreement is a meaningful signal.

This is the complete practical stack for most agents. Two things are deliberately absent from it: Tree of Thoughts and LATS.

---

## When to Escalate , and What Escalation Costs

*Tree of Thoughts: Deliberate Problem Solving with Large Language Models* (Yao et al., 2023) and *Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models* (LATS, Zhou et al., 2023) are both real contributions. Tree of Thoughts turns reasoning into a branching search problem over alternative thought paths, allowing the system to explore multiple directions and backtrack when a path fails. LATS adds a more formal Monte Carlo Tree Search layer over a combined reasoning-acting system, giving it structured evaluation of branches before committing.

Both methods are genuinely powerful on tasks that have real branching difficulty , tasks where the first plausible path often fails and the correct answer requires exploring alternatives. Mathematical reasoning, complex planning with hard constraints, and adversarial problem-solving are the domains where these methods produce clear gains.

They are also expensive, operationally complex, and prone to being applied to the wrong tasks. A team that reaches for ToT when the problem was actually a decomposition failure will build a slower, more expensive system that still fails , just in more elaborate ways. Tree search is not an upgrade to ReAct-plus-verification. It is a different tool for a different class of problem.

The signal that justifies escalation to tree search is specific: the task has multiple plausible approaches, the first approach reliably fails in ways that a different approach would not, and the cost of exploring alternatives is worth the reliability gain. If the reasoning failures in a system are caused by insufficient decomposition or insufficient grounding, tree search will not fix them.

This selection logic , use the cheapest scaffold that solves the task reliably , is the most useful practical principle in the Chapter 2 material. The taxonomy of available methods is interesting. The decision rule for which one to use is what matters for building.

---

## Planning as a Distinct Problem

The chapter makes one distinction that deserves separate treatment: the difference between reasoning and planning.

Reasoning, in the framework established so far, is about deriving conclusions , whether factual (what does this claim document say?) or inferential (what does the answer to step 2 imply for step 3?). Planning is about deriving sequences of actions: what should the agent do next, in what order, to achieve a goal that requires multiple steps in the world?

The distinction matters because planning has additional constraints that reasoning alone does not. A reasoning error can be corrected by revising the argument. A planning error can propagate into actions that change external state. A plan that includes an irreversible step in position 3 cannot be safely retried from the beginning if step 3 already executed.

*LLM+P: Empowering Large Language Models with Optimal Planning Proficiency* (Liu et al., 2023) is useful as a boundary case. It shows that for tasks with strong formal structure , logistics optimization, scheduling problems with hard constraints , it can be better to have the LLM generate a problem specification in a formal planning language and hand that to a classical planner rather than ask the LLM to plan directly. This is not the default for most agent tasks, but it is a signal: when planning quality dominates and the task has well-defined structure, a formal planner can be a better tool than prompting alone.

For most enterprise agent tasks, the practical planning architecture is simpler: decompose the task into ordered subgoals, use a ReAct loop to execute each one, and require human approval before any subgoal whose action is irreversible. That is planning without a formal planner , and for document processing, data workflows, API-driven tasks, and supervised automation, it is usually enough.

---

## What Goes Wrong in Practice

**First-pass overconfidence** is the failure mode where the model commits too early to a weak reasoning path. The agent generates an answer that sounds plausible, does not critique it, and moves to action. The fix is verification , not as a moral obligation but as a structural step before any high-value output becomes an action. If first-pass overconfidence is a recurring pattern in your system, the verification layer is missing or too weak.

**Planning without grounding** is the failure mode where the agent produces a plan , sometimes an elaborate, coherent, well-structured plan , that does not reflect the actual state of the environment. It plans to use a vendor API that is currently down. It plans to retrieve a document from memory that was never stored. It plans to submit a form whose required fields it has not yet collected. These failures are often attributed to "hallucination," but the mechanism is not generation of false facts , it is reasoning disconnected from observation. The fix is ReAct, not prompt engineering.

**Search overkill** is the failure mode where the team adds tree search or LATS to a system that was failing because of decomposition or grounding errors. The result is a system that expands its search space over a reasoning structure that was already broken. More search over broken reasoning produces more elaborate wrong answers, often with longer traces that are harder to diagnose. The fix is to identify the failure mode before selecting the scaffold.

**Critique without signal** is the failure mode where self-refinement loops are added but the critique has no real signal to act on. The model produces an output, critiques it, produces a revised output that is structurally different but not actually better, and the loop adds latency without improving quality. Self-refinement works when the critique captures something meaningful , a logical gap, a factual inconsistency, a schema violation. It does not work when the critique is vague ("this answer could be more complete") because the revision responds to the same vague direction.

---

## The Scaffold Is the Architecture

The practical conclusion from this essay is that the reasoning layer of an agent system is an architectural decision, not a prompting decision. Choosing a scaffold is choosing the structure of the reasoning loop: what order the model works through the problem, when it checks its own work, when it grounds itself in external state, and when it hands off to a different mechanism.

That choice should follow from a diagnosis of how the current system fails, not from a survey of available techniques. A system that fails because of logical gaps needs decomposition. A system that fails because it ignores tool output needs ReAct. A system that fails because its first answer is usually close but imprecise needs self-refinement. A system that fails because it states facts it cannot verify needs CoVe.

The insurance claim agent's problem was not that its model was too weak for the task. It was that the scaffold asked the model to do in one step what it needed to do in three. The fix was not a better model. It was a structured sequence of simpler questions , the kind of change that takes an afternoon to implement and weeks to realize was the answer.

That is the anatomy of a scaffold mismatch. And diagnosing it correctly is what separates an agent system that improves from one that keeps getting more expensive without getting more reliable.

---

*Part 3 addresses memory: how agents persist and retrieve knowledge across time, why memory failures are almost always retrieval policy failures rather than storage failures, and what a complete memory architecture looks like for real deployed systems.*

---

**Source basis for this essay:** Chapter 2 of *Advances and Challenges in Foundation Agents* (2025); *ReAct: Synergizing Reasoning and Acting in Language Models* (Yao et al., 2022) [arXiv:2210.03629](https://arxiv.org/abs/2210.03629); *Least-to-Most Prompting Enables Complex Reasoning in Large Language Models* (Zhou et al., 2022) [arXiv:2205.10625](https://arxiv.org/abs/2205.10625); *Self-Consistency Improves Chain of Thought Reasoning in Language Models* (Wang et al., 2022) [arXiv:2203.11171](https://arxiv.org/abs/2203.11171); *SELF-REFINE: Iterative Refinement with Self-Feedback* (Madaan et al., 2023) [arXiv:2303.17651](https://arxiv.org/abs/2303.17651); *Chain-of-Verification Reduces Hallucination in Large Language Models* (Dhuliawala et al., 2023) [arXiv:2309.11495](https://arxiv.org/abs/2309.11495); *Tree of Thoughts: Deliberate Problem Solving with Large Language Models* (Yao et al., 2023) [arXiv:2305.10601](https://arxiv.org/abs/2305.10601); *Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models* (Zhou et al., 2023) [arXiv:2310.04406](https://arxiv.org/abs/2310.04406); *LLM+P: Empowering Large Language Models with Optimal Planning Proficiency* (Liu et al., 2023) [arXiv:2304.11477](https://arxiv.org/abs/2304.11477); `practical-chapter-blueprints/02-reasoning-planning-blueprint.md`.
