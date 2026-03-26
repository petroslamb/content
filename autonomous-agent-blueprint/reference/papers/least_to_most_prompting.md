<!-- AGENT BLUEPRINT METADATA START -->
# Least-to-Most Prompting Enables Complex Reasoning in Large Language Models

- Year: 2022
- Primary chapter: Reasoning and Planning
- Method category: progressive decomposition prompting
- Practical role: ordered decomposition default for difficult multi-step reasoning
- Key contribution: Shows that solving ordered easier subproblems can unlock harder reasoning tasks without changing the base model.
- Major limitation: Best when tasks can be decomposed cleanly; weaker when the main challenge is external state or verification.
- Confidence: High
- Canonical link: https://arxiv.org/abs/2205.10625

<!-- AGENT BLUEPRINT METADATA END -->

## Thesis

Least-to-Most Prompting argues that many hard reasoning failures come from asking the model to solve the whole problem in one jump. The paper breaks a difficult task into an ordered sequence of easier subproblems and solves them progressively.

## What It Contributes

Its main contribution is to make decomposition itself a first-class prompting method rather than a vague instruction. That matters because ordered subproblems are often more valuable than longer raw reasoning traces.

## Why It Matters In This Repo

This repo uses the paper as a practical default for multi-step reasoning that does not yet need search. It supports the chapter-level doctrine that decomposition should usually come before heavier planning methods.

## Limitations

The method assumes the task can be decomposed sensibly and that early subproblem answers are useful rather than misleading. It does not help much when the task needs live environment feedback or formal planning.

## Design Takeaways

- Use it for structured reasoning tasks where the solution can be built progressively.
- Prefer ordered subgoals over long monolithic prompts when the model struggles with hard multi-step tasks.
- Escalate beyond it only when decomposition alone no longer resolves the task.

## Raw Local Extraction

No raw local extraction is tracked in this repo for this note. Use the canonical arXiv link above for the primary paper text.
