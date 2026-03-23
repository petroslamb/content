# Part 6: The Workflow Is the Object

## How to Improve an Agent System That Already Works

*Part 6 of 6: A Practical Guide to Foundation Agents*

---

A team running a document classification agent had been in production for three months. The system was functional , it correctly categorized about 82% of incoming documents on the first pass and required human correction on the rest. That was acceptable. Then the team started trying to improve it.

Over six weeks, they edited the system prompt eleven times. They tried different framing, different instruction sequences, different levels of detail. Some changes improved accuracy on the cases they were watching. A week later, accuracy on other cases had regressed. They had no evaluation set , they were watching specific failure examples and tuning toward them. They had no baseline metrics , latency and cost were tracked in a dashboard they had not looked at in a month.

After six weeks of edits, the system's overall accuracy was approximately the same as it had been before they started. The prompt had grown by 40%. The team did not know which changes had helped and which had hurt, because they had never instrumented the system well enough to find out.

This is the most common form of agent optimization, and it is not optimization. It is prompt drift. The signal is weak, the feedback loop is slow, and the changes accumulate without any systematic understanding of whether the system is improving.

Optimization that works looks different. It starts with measurement. Then it identifies which component is failing. Then it improves that component by the smallest intervention that addresses the failure. Then it measures again. That sequence , which sounds obvious and is systematically ignored , is what separates agent systems that improve from agent systems that change.

---

## The Whole Workflow Is the Object

The most important conceptual shift in Chapter 9 and 11 of the *Foundation Agents* survey is positional: the unit of optimization is the workflow, not the prompt.

This matters because most optimization instinct is local. When an agent produces a bad output, the intuitive response is to look at what the agent was told to do , the system prompt, the user message, the retrieval instruction , and change something. This is prompt tuning, and it is sometimes the right intervention. But it is rarely the right first intervention, because the prompt is only one component in a system with multiple components, and the failure may not be in the prompt.

An agent workflow has at least four improvable surfaces: the prompt and schema (how the agent is instructed), the tool set and tool descriptions (what the agent has access to and how it understands those tools), the retrieval configuration (what gets pulled into context and how it is weighted), and the workflow topology itself (the sequence in which tasks are decomposed and executed). A failure in the output can originate at any of these layers. Tuning the prompt when the failure is in retrieval quality produces marginal gains at best and prompt sprawl at worst.

*Large Language Models as Optimizers* (OPRO, Yang et al., 2023) is the conceptual anchor for prompt optimization treated as a formal problem: given examples of successes and failures, generate candidate prompt improvements, evaluate them against those examples, and iterate. The key word is "examples": OPRO works because there is a fixed evaluation set against which candidate prompts can be measured. Without that evaluation set, the optimization loop has no signal. The prompt changes. The developer watches an anecdote or two. The prompt changes again. Nothing improves systematically because nothing is measured systematically.

*TextGrad: Automatic "Differentiation" via Text* (Yuksekgonul et al., 2024) generalizes this from single prompts to multi-component textual systems. TextGrad propagates feedback signals backward through the system graph from a loss signal , an error, a quality failure, a constraint violation , identifying which textual components (prompts, schemas, instructions) contributed to the outcome and how. This is the formal version of the observation that optimization targets the workflow rather than the node: the loss signal can be attributed to any component, and the gradient analogue is the natural-language feedback about what that component should have said or done differently.

*AFLOW: Automating Agentic Workflow Generation* (Liu et al., 2024) and *GPTSwarm: Language Agents as Optimizable Graphs* (Zhugue et al., 2024) push the optimization target to the next level: not individual prompts or schemas but the workflow graph itself. AFLOW uses code-based workflow representation and Monte Carlo Tree Search to evaluate candidate workflow modifications. GPTSwarm treats an agent system as a computational graph whose edge weights and node configurations can both be optimized. These are powerful methods and genuinely research-frontier contributions. They are also not where most teams should start, because they presuppose that the local component failures have been resolved and the workflow structure is the actual bottleneck.

---

## The Correct Optimization Sequence

The practical lesson from this literature is a specific ordering that most teams invert. From most to least impactful as a starting point, and from least to most risk of creating new problems:

**Evaluate first.** Before changing anything, build an evaluation set: a fixed collection of representative inputs with known good outputs, annotated by domain experts or reconstructed from human corrections. Run the current system against this set. Record the accuracy, latency, and cost. This is not optional preparation for optimization , it is optimization's first output. Without a fixed set, there is no baseline, no regression protection, and no signal that improvement has occurred.

**Fix the output schema.** The most impactful low-risk change in almost every agent system is schema clarity: ensuring that the model's output is structured in a way that downstream components can reliably use. Schema failures are the most common source of integration errors between agent components, and they are the cheapest to fix. A well-specified JSON schema with required fields, typed values, and explicit formatting constraints eliminates an entire class of downstream failures without affecting the model's reasoning.

**Fix the retrieval configuration.** When the evaluation results show that the agent is working with incomplete or irrelevant context, retrieval quality is the bottleneck. The interventions at this layer are concrete: chunk size, overlap, similarity threshold, re-ranking, metadata filtering, and query reformulation. Each of these can be evaluated against the fixed evaluation set. Each of these is cheaper to improve than the prompt.

**Improve the prompt and tool descriptions.** After schema and retrieval are clean, prompt improvements are more tractable because the input-output relationship is less noisy. At this stage, OPRO-style systematic optimization , generate candidates, evaluate against the fixed set, iterate , is appropriate. What is not appropriate is prompt editing without evaluation, because the signal is too weak.

**Improve the workflow topology.** If the evaluation results show that the failures are distributed across multiple components in a pattern that suggests the task decomposition is wrong , that some steps need to be added, reordered, or parallelized , this is when workflow structure changes are warranted. Not before. Changing the workflow structure when local component failures are still present adds complexity to an already-failing system.

**Consider self-improvement loops.** Once the system is stable and measurable, feedback loops from human corrections, evaluation failures, and runtime signals can be used to improve the system automatically. *Reflexion: Language Agents with Verbal Reinforcement Learning* (Shinn et al., 2023) demonstrates the lightest form of this: storing verbal self-critique from failure events and using that critique to improve subsequent reasoning on similar tasks. *Voyager: An Open-Ended Embodied Agent with Large Language Models* (Wang et al., 2023) demonstrates a more ambitious form: building a skill library from successful runs, continuously adding proven behaviors, and using past experience to avoid repeating solved problems. Both approaches share a property that should be non-negotiable: the feedback loop is bounded by human-reviewed success signals. Reflexion stores reviewed corrections. Voyager promotes skills that have been validated by environment feedback. Neither allows the system to modify itself based on unvalidated self-assessment.

---

## Measurement Is the Architecture

The most important structural claim of this essay is that the evaluation layer is a component of the agent system, not a phase of its development.

A component of the system has a specification, inputs, outputs, and owners. Evaluation has all four. Its specification is the set of quality dimensions that matter for the task: accuracy, latency, cost, retry rate, approval gate hit rate, and correction rate. Its inputs are the agent's outputs on a representative set of tasks. Its outputs are structured measurements of those quality dimensions over time. Its owners are whoever is responsible for system quality.

When evaluation is treated as a phase , a thing done at the beginning (testing) and at the end (review) , the signal it provides is coarse. The system either works or it does not, and the feedback loop is too slow to support iterative improvement. When evaluation is a continuous component, the signal is fine-grained. Failures are surfaced before they accumulate. Regressions are caught before they become user-facing. Optimization has a responsive objective function rather than an occasional report.

*Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* (Zheng et al., 2023) matters here as practical calibration: using a language model as an evaluator for complex outputs , quality, coherence, correctness , scales the evaluation process beyond what human annotation can cover. LLM-as-judge has real limitations: it can share the biases of the model it evaluates, it can be fooled by confident but incorrect outputs, and it requires calibration against human judgments on a subset of cases to remain trustworthy. Used with those constraints acknowledged, it is a practical way to maintain evaluation coverage as systems grow.

The calibration requirement is not a footnote. An uncalibrated LLM judge is a measurement instrument with unknown accuracy , which is to say, not a measurement instrument at all. Calibration against human labels on a random sample of evaluated outputs, with explicit checks for the failure modes LLM judges are known to exhibit (length bias, instruction-following bias over correctness), is part of what makes the evaluation layer worth building.

---

## The Limits of Self-Improvement

The self-improvement methods in the literature span an enormous range, from *Reflexion*'s simple failure-critique loop to *GPTSwarm*'s full topology optimization. The temptation to reach for the ambitious end of this range before the simpler end is validated is one of the most reliable paths to systems that are harder to understand and no more reliable.

The safety argument for bounded self-improvement is simple. A self-improvement system that can modify its own reasoning prompts can, in principle, modify prompts that govern safety-relevant behavior. A self-improvement system that can restructure its own workflow can, in principle, remove or bypass approval gates. These are not hypothetical risks , they are predictable failure modes of systems whose self-modification actions are not explicitly bounded.

The practical constraint is that every self-improvement loop should have explicit scope boundaries: which components can be modified, through what mechanism, subject to what validation before the change becomes active. Prompt improvement that passes evaluation set validation before deployment is self-improvement with appropriate validation. Workflow topology search that rewrites the graph without human review is self-improvement on trust that has not been earned.

*Voyager*'s skill library is instructive here precisely because its scope is bounded in a specific way: the agent can add to the skill library when the environment validates the skill (the behavior succeeded), and it can use skills from the library on future tasks, but it cannot remove or modify previously validated skills without external intervention. That asymmetry , build up, do not tear down without review , is a design principle for safe self-improvement that generalizes beyond embodied agents.

---

## What the Three-Month Production System Knows

An agent deployed for three months has accumulated something that a prototype does not have: operational evidence. It has latency curves, not just latency estimates. It has failure distributions, not just synthetic test cases. It has correction logs, not just anecdotal error examples. It has approval gate hit rates under real workloads, not just design-time assumptions about how often human review would be needed.

That operational evidence is the most valuable input to optimization. It reveals which failure modes are common versus rare, which task types are reliably handled versus consistently problematic, which tools are used frequently and which are never invoked, which retrieval queries are returning high-quality results and which are returning noise.

The document classification team had three months of this evidence. They were not using it. They were watching a selected set of recent failures and editing the prompt in response to whichever failure was most visible. If they had built the evaluation set from their correction log, run baseline metrics, and identified which task type had the highest error rate, they would have found that most corrections were concentrated in one category of document , the kind that had ambiguous metadata , and that the schema for that category was underspecified. A schema fix would have addressed two-thirds of the corrections without touching the prompt.

Optimization begins not when you want the system to be better but when you understand what "better" means for the specific failure modes the system is actually exhibiting. That understanding requires measurement. Measurement requires a fixed evaluation set. The evaluation set is built from the operational evidence the system has been generating since its first day in production.

That is why optimization is the final part of this guide and not the second. It requires the system to exist, to be running, and to have generated the operational evidence that gives optimization its signal. Before that, you are editing in the dark.

---

## The Guide as a Whole

The six essays in this guide follow the building order deliberately: action first because it defines what an agent is, reasoning because it determines how the agent structures its work, memory because it gives the agent persistence and learning, multi-agent design because it is the escalation path when one agent is genuinely insufficient, safety because it is the architectural consequence of everything the first four essays built, and optimization because it is the continuous improvement process for a system that now exists and is measurable.

The guide's underlying argument is also one: building useful agents is a sequence of concrete architectural decisions, each of which has specific implications for reliability, debuggability, and safety. The worst outcome in agent development is not that the system fails , it is that the system fails in ways that cannot be localized, understood, or systematically improved. Every recommendation in this guide is a recommendation for clarity about what the system is doing and why, so that when it fails, the failure is diagnosable and the fix is tractable.

That is the difference between an agent system and a capable-seeming prototype. The prototype works until it doesn't, and no one is sure why. The system has action contracts, reasoning scaffolds, memory lifecycle rules, multi-agent coordination architecture, safety boundaries, and measurement infrastructure , and when it fails, someone can point to the layer.

---

**Source basis for this essay:** Chapters 9 and 11 of *Advances and Challenges in Foundation Agents* (2025); *Large Language Models as Optimizers* (OPRO, Yang et al., 2023) [arXiv:2309.03409](https://arxiv.org/abs/2309.03409); *TextGrad: Automatic "Differentiation" via Text* (Yuksekgonul et al., 2024) [arXiv:2406.07496](https://arxiv.org/abs/2406.07496); *AFLOW: Automating Agentic Workflow Generation* (Liu et al., 2024) [arXiv:2410.10762](https://arxiv.org/abs/2410.10762); *GPTSwarm: Language Agents as Optimizable Graphs* (Zhugue et al., 2024) [arXiv:2402.16823](https://arxiv.org/abs/2402.16823); *Reflexion: Language Agents with Verbal Reinforcement Learning* (Shinn et al., 2023) [arXiv:2303.11366](https://arxiv.org/abs/2303.11366); *Voyager: An Open-Ended Embodied Agent with Large Language Models* (Wang et al., 2023) [arXiv:2305.16291](https://arxiv.org/abs/2305.16291); *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* (Zheng et al., 2023) [arXiv:2306.05685](https://arxiv.org/abs/2306.05685); *SELF-REFINE: Iterative Refinement with Self-Feedback* (Madaan et al., 2023) [arXiv:2303.17651](https://arxiv.org/abs/2303.17651); `practical-chapter-blueprints/04-optimization-self-improvement-blueprint.md`.
