<!-- AGENT BLUEPRINT METADATA START -->
# LLM+P: Empowering Large Language Models with Optimal Planning Proficiency

- Year: 2023
- Primary chapter: Reasoning and Planning
- Method category: planner-augmented reasoning
- Practical role: bridge from language reasoning to formal planning when the task needs stronger structure
- Key contribution: Connects natural-language task understanding to formal planning machinery instead of relying on verbal reasoning alone.
- Major limitation: Most useful when the task can be formalized cleanly enough for a planner; heavier than practical defaults.
- Confidence: High
- Canonical link: https://arxiv.org/abs/2304.11477

<!-- AGENT BLUEPRINT METADATA END -->

## Thesis

LLM+P argues that some planning problems are better solved by handing structure to a classical planner than by relying on verbal reasoning alone. The model interprets natural-language goals and constraints, then delegates the actual planning to formal planning machinery.

## What It Contributes

The paper provides a clean bridge between language understanding and symbolic planning. That matters because it gives builders a concrete answer for tasks where structure, constraints, and search quality outrun what prompting alone can deliver.

## Why It Matters In This Repo

This repo uses LLM+P as the clearest example of planner augmentation in the reasoning chapter. It supports the rule that formal planning is an escalation path for strongly structured tasks, not the default for everyday agent workflows.

## Limitations

The approach depends on being able to translate the task into a formal planning representation. When the environment is noisy, underspecified, or poorly formalized, the handoff becomes harder and the benefit drops.

## Design Takeaways

- Use it when the task has strong symbolic structure, constraints, or long-horizon planning requirements.
- Treat planner handoff as an escalation from ReAct and decomposition, not as the baseline architecture.
- Make the language-to-formalization boundary explicit, because that translation is where many failures will sit.

## Raw Local Extraction

No raw local extraction is tracked in this repo for this note. Use the canonical arXiv link above for the primary paper text.
