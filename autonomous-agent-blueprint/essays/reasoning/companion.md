# Reasoning Companion

The public reasoning essay was built around one discipline: do not pick a reasoning method by prestige. Pick it by failure shape. That gave the main piece its force. It also meant leaving some of the chapter's breadth off the page. The wider chapter is not only a case for `decompose -> ReAct -> verify`. It is a map of how reasoning, planning, critique, verification, and search sit in relation to each other, and of how easily builders over-escalate when they misread the problem in front of them.

That broader map matters because reasoning failures are still routinely diagnosed in the wrong place. People say the model is weak when the workflow is understructured. They add search when the task needed decomposition. They add critique when the real problem is lack of evidence. The useful thing about the chapter is not that it names many methods. It is that it gives you a way to stop choosing them theatrically.

## Start By Asking What Kind Of Failure You Have

The chapter becomes practical once you stop reading it as a menu of clever prompts and start reading it as a diagnostic tree.

If the task is multi-step but largely deterministic, decomposition is usually the right first move. Least-to-Most matters here because it makes ordered subproblem solving explicit and reusable. It is a way of imposing structure before you spend money on heavier reasoning.

If the task interacts with tools, external state, code execution, or search, the center of gravity shifts. Pure verbal reasoning is no longer enough. ReAct matters because it alternates reasoning with action and observation. That makes the workflow responsive to the actual environment rather than to the model's guess about it.

If the first answer is close but brittle, then refinement may be worth adding. If the failure is factual and the output matters, verification becomes the right escalation. If one reasoning path keeps collapsing and multiple plausible paths exist, then search methods can make sense. The chapter is best understood as a progression of these choices.

## Why Decomposition Is More Important Than It Sounds

Decomposition often looks almost too simple compared with the more famous methods in the chapter. That is precisely why it gets underrated. A surprising amount of reasoning work is lost not because the model cannot think, but because the task was presented as one monolithic jump.

Least-to-Most prompting matters because it formalizes a very practical move: separate the hard task into ordered, easier subproblems whose outputs support the next step. That keeps the agent from spending its whole budget improvising the structure of the problem while also trying to solve it. In many workflows, that is the first real gain in reliability.

Step-Back Prompting belongs near this tier as well, but for a different reason. Sometimes the issue is not missing steps. It is premature commitment to the wrong conceptual frame. Asking the model to recover the governing abstraction before it attacks the details can be a surprisingly effective reset.

## Where Reasoning Turns Into Planning

One subtle strength of the chapter is that it separates reasoning about an answer from planning through actions. Those two are related, but they are not identical.

Reasoning can stay purely verbal. Planning has to shape a sequence of actions, tool uses, or state transitions. This is why ReAct sits so centrally in the practical interpretation of the chapter. It is the hinge between the reasoning stack and the action stack. The model is no longer only explaining a solution. It is deciding what to do next, observing the result, and adjusting course.

That distinction matters because a lot of systems are called planners when they are really narrators. A real planning layer changes control flow. It does not merely produce a persuasive paragraph about what ought to happen.

## Critique, Verification, And Consensus Are Not The Same Thing

The chapter also helps disentangle three methods that often get lumped together because they all look like "extra reasoning."

Self-Refine is a draft-critique-revise loop. It is best when the first answer is directionally correct but underspecified, messy, or incomplete.

Chain-of-Verification is a different move. It does not merely improve prose quality. It creates a separate checking phase that can challenge the first answer on factual grounds. That makes it one of the most practically important overlays in the chapter, especially once outputs can trigger downstream action.

Self-Consistency is different again. It addresses a single-trace brittleness problem by sampling multiple reasoning traces and selecting a consensus answer. That can work well, but only when the task actually benefits from multiple independent traces. If the problem is weak structure or bad evidence, consensus will not rescue it.

The broader chapter matters because it keeps those methods separate. They are solving different problems and should not be chosen as if they were interchangeable badges of sophistication.

## When Search Is Actually Justified

Tree of Thoughts and LATS are valuable because some tasks really do have branching difficulty. There are dead ends. There are multiple plausible routes. A single linear chain is not enough. That is the honest case for search.

But the chapter is just as useful for telling builders when not to use search. Search is expensive, slower to evaluate, harder to instrument, and easy to romanticize. If decomposition, ReAct, and verification solve the task, then branching search is usually unnecessary complexity. LLM+P makes a similar point from another direction. Some problems need stronger formal structure, but that does not mean every problem does.

This is why the practical reading of the chapter stays conservative. The impressive methods are real. They are also escalation paths, not defaults.

## Resources And References

### [Reasoning Essay: Operating Agents III: The Lightest Correct Scaffold](../reasoning/02-reasoning-planning-v5.md)

Read the essay first for the sharp operational claim. It compresses the chapter into a diagnosis rule and a sensible default stack.

Use this companion when you want the wider method map and the fuller chapter logic around decomposition, planning, critique, verification, and search.

### [Builder Blueprint: Reasoning and Planning](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md)

The blueprint is the builder-facing translation of the chapter. It turns the method landscape into decision rules about what to add when the task is deterministic, tool-dependent, fact-sensitive, or search-heavy.

It is also the clearest place to see the intended escalation ladder: decomposition first, ReAct as the default live-state loop, verification early, and heavier search only when justified.

### [Foundation Agents: Practical Chapters Guide](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/reference/chapters-guide.md)

The guide is the broader booklet interpretation. It turns the chapter from a taxonomy into a practical menu and keeps the focus on task fit rather than method prestige.

It is also where the already-practical versus promising-but-not-default distinction is stated most clearly, which matters for reading this chapter sanely.

### [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) (2022)

ReAct is the control-loop paper of this cluster. Its lasting contribution is not only benchmark improvement. It joins reasoning, action, and observation into one topology, which makes it the natural bridge between the reasoning chapter and the action chapter.

The paper matters most whenever the agent has to interact with live tools or state. It should be read less as a prompt pattern and more as a default execution loop for grounded work.

### [Least-to-Most Prompting Enables Complex Reasoning in Large Language Models](https://arxiv.org/abs/2205.10625) (2022)

Least-to-Most matters because it makes decomposition itself a first-class technique. It is one of the strongest arguments in the chapter for solving structured multi-step tasks with ordered subproblems before escalating to heavier methods.

Its practical importance is that it often fixes the right problem first. Many failures that look like reasoning weakness are really failures of task packaging.

### [SELF-REFINE: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651) (2023)

Self-Refine is the cleanest draft-critique-revise loop in the chapter. It matters because it is easy to add and often useful when an answer is close but not good enough.

Its limitation is equally important. It can polish a weak or ungrounded answer into a cleaner weak or ungrounded answer. That is why refinement belongs beside verification, not in place of it.

### [Chain-of-Verification Reduces Hallucination in Large Language Models](https://arxiv.org/abs/2309.11495) (2023)

CoVe is one of the most practically important papers in the stack because it turns checking into its own phase. That separation is what makes it more than a polite "double-check yourself" instruction.

It matters wherever factual error can trigger downstream decisions or actions. In those settings, reliability improves when verification has its own questions, evidence path, and revision step.

### [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171) (2022)

Self-Consistency addresses a narrow but real failure mode: too much dependence on one reasoning trace. By sampling multiple traces and taking the consensus, it can improve reliability when the task actually supports that kind of variation.

That narrowness is why it remains useful. It is powerful for brittle traces. It is not a substitute for good decomposition, grounding, or evidence selection.

### [Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models](https://arxiv.org/abs/2310.06117) (2023)

Step-Back Prompting matters because some failures begin before the steps are even chosen. The model commits too early to a local answer and misses the governing concept.

This makes it a strong mid-tier intervention. It is cheaper than search and often enough when the problem is conceptual framing rather than branching complexity.

### [LLM+P: Empowering Large Language Models with Optimal Planning Proficiency](https://arxiv.org/abs/2304.11477) (2023)

LLM+P is the clearest bridge from natural-language reasoning to formal planning. It matters because it shows that some tasks should hand structure off to planning machinery instead of staying entirely inside prose.

Its practical importance in this package is disciplinary. It reminds readers that not every hard task should be solved by asking the model to think harder in text.

### [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601) (2023)

Tree of Thoughts matters because it treats reasoning as branching search over alternatives rather than as one linear trace. That is useful when the problem genuinely contains dead ends and multiple viable routes.

It belongs in the companion rather than the main essay because it is real and important, but still too heavy for the default stack of most workflows.

### [Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models](https://arxiv.org/abs/2310.04406) (2023)

LATS pushes the same logic further by combining reasoning, action, and tree search in one heavier planning loop. It is a strong reference for difficult planning problems where simpler scaffolds no longer hold up.

It also serves as a warning about escalation cost. Once you add search, you add latency, orchestration complexity, and a harder evaluation problem. That is why the chapter keeps it in the escalation tier.
