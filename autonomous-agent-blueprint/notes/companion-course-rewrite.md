# Companion Course Rewrite

This note governs the live companion layer for the course version of *Operating Agents*. It exists to keep the companions useful after the earlier doctrine-heavy drafting stack was removed.

## Purpose

Each companion is a second-pass public chapter. It should widen the field around the matching core essay without drifting into internal bundle commentary, source dumping, or rhetorical posture. The companion is where the reader gets the broader map, the omitted taxonomies, the edge cases, and the literature-reading guidance that would overload the main chapter.

The companion should answer four questions for the reader:

1. what important terrain did the main chapter intentionally leave out
2. how is the subfield organized when you look beyond the deployable center
3. which escalation paths are real and which are mostly overhead
4. which papers are worth reading next, and what design choice does each one clarify

## Fixed Shell

Every live companion uses this shell:

- `# <Topic> Companion`
- short opening that states what this second-pass chapter adds beyond the main essay
- 5 thematic `##` sections
- `## Analytical References`

Companions do not use `#### Video TL;DR`, and they do not end with `## Sources Behind This Chapter`.

## Section Contract

The five thematic sections should do distinct work:

- expand the field map with the booklet taxonomy and the practical blueprint
- explain adjacent methods or topologies that were too broad for the main chapter
- clarify the main escalation points and comparison logic
- show where failure analysis changes the architecture choice
- teach the reader how to reason about the literature, not just memorize paper names

The companion should read as prose-first course writing. Small tables are acceptable only when the comparison cannot be taught cleanly in paragraphs. Lists should remain rare.

## Analytical Reference Standard

The ending section is always `## Analytical References`.

Inside it:

- use one `###` subsection per paper or reference family
- give each entry at least two paragraphs
- the first paragraph explains what problem the work addresses, what it added, and how it differs from nearby methods
- the second paragraph explains how a builder should use the work after reading the chapter: when to read it, what design choice it sharpens, and what not to overclaim from it

The references should feel like guided study, not like badges.

## Figure Policy

Companions should use 5 to 7 figures. Figures are explanatory anchors, not decoration.

Preferred source order:

1. chapter-scoped booklet figures and tables under `core/practical-chapter-blueprints/extracted-figures/`
2. renamed page renders from the booklet when a chapter needs one more taxonomy or lifecycle visual
3. named course-slide derivatives only when the booklet does not provide enough chapter-relevant visuals

Use the figure filenames directly in prose decisions. Writers should be able to understand placement from the filename alone.

## Topic Coverage Defaults

Action companions should cover action-system taxonomy, tool-system taxonomy, action surfaces, discovery and selection, browser and GUI escalation, approval, recovery, and observation contracts.

Memory companions should cover cognitive memory models, typed memory, lifecycle policy, derivation and admission, retirement, procedural promotion, and retrieval escalation.

Reasoning companions should cover reasoning paradigms, decomposition, abstraction, grounding loops, verification, critique, consensus, planner handoff, and search stop rules.

Multi-agent companions should cover MAS taxonomy, collaboration goals, collaboration types, human-agent collaboration, decision-making structures, communication protocols, and evaluation frameworks.

Safety companions should cover trust classes, prompt injection, hallucination as an operational risk, tool and memory threats, retrieval contamination, cross-agent contamination, and replayable incident review.

Optimization companions should cover optimization layers, prompt cycles, workflow topology, tool optimization, evaluation support, judge systems, multi-objective tradeoffs, and bounded online self-improvement.

## Explicit Bans

Do not use doctrine framing.

Do not open with bundle-meta commentary such as “the public essay keeps the law.”

Do not link to removed `-v7` public essay filenames.

Do not end with `## Sources Behind This Chapter`.

Do not collapse the analytical reference section into one-line summaries.
