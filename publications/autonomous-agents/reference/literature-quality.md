# Literature Quality

This file records where the local corpus is strong, where it is merely usable, and where it should not be trusted without correction. The goal is to keep weak or ambiguous local files from silently anchoring the repo's core guidance.

## Confidence Levels

- `High`: the local file matches a well-known paper cleanly enough to support core claims.
- `Medium`: the source is useful, but the local extraction, aliasing, or scope requires some caution.
- `Low`: the source may still be useful as supporting material, but it should not carry core claims by itself.
- `Questionable`: the local file is mismatched, misnamed, or otherwise unreliable enough that it must not anchor the main narrative.

## High-Confidence Core Sources

These are the main sources the repo can safely lean on for core architecture guidance:

- ReAct
- Least-to-Most Prompting Enables Complex Reasoning in Large Language Models
- Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models
- Self-Consistency
- LLM+P: Empowering Large Language Models with Optimal Planning Proficiency
- Self-Refine
- Reflexion
- Chain-of-Verification
- Toolformer
- Gorilla
- MemGPT
- MemoryBank
- Mem0
- HippoRAG
- MetaGPT
- AutoGen
- ChatDev
- ToolEmu
- InjecAgent
- Agent Smith
- PoisonedRAG
- BadRAG
- Jamming Retrieval-Augmented Generation
- SWE-agent
- WebAgent
- Mind2Web

## Medium-Confidence Sources

These files are still useful, but the repo should lean on them with more care:

- `papers/opendevin.md`
  The local alias says `opendevin`, but the actual paper in the file is `OpenHands: An Open Platform for AI Software Developers as Generalist Agents`. The core docs should use the paper's actual name and only mention the local alias when necessary for navigation.

- `papers/appagent.md`, `papers/mobile_agent.md`, and `papers/omniparser.md`
  These are valuable action-surface references, but they are highly specific to GUI and device interaction. They are strong supporting sources, not universal defaults.

- `papers/mt_bench_chatbot_arena.md`
  Useful as an evaluation-pattern paper, but not an architecture blueprint by itself.

- `papers/aflow.md` and `papers/gptswarm.md`
  Important for optimization and workflow search, but they belong to an escalation layer rather than the default baseline.

## Quarantine Policy

There are no currently quarantined tracked paper notes. If a future note is found mismatched or mislabeled, record it here immediately and remove it from core guidance until corrected.

## Corpus-Wide Limitations

- Many `papers/*.md` files are raw PDF-to-text extractions rather than polished notes. They are good enough for source mapping and local recall, but weak for precise section-level quotation.
- Only the wave-1 anchor notes rewritten for this repo upgrade are guaranteed to have human-readable summary sections above the raw extraction. The rest of the corpus remains source-mapped local notes first.
- Some top-level interpretation files are stronger as syntheses than as direct evidence. The repo should continue to privilege primary paper notes for source tracing.
- Several papers are cross-chapter by nature. The source index assigns one primary chapter for navigational clarity, but many of these sources should still be cited across memory, reasoning, optimization, and safety when the argument warrants it.

## How To Use This File

- Use `source-index.md` to find papers.
- Use this file to decide how much trust to place in a local file.
- If a source is marked `Questionable`, do not use it as a core authority.
- If a source is marked `Medium`, pair it with a stronger neighboring source when making a central argument.

## Future Update Rule

If a new paper is added and changes the repo's guidance, the update must modify:

- `source-index.md`
- one comparison matrix or equivalent chapter comparison section
- one relevant chapter or use-case document

If a new local file is ambiguous or mismatched, it must be documented here before it is allowed into the main narrative.
