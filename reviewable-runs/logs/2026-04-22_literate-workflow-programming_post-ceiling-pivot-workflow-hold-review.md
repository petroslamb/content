# Post-Ceiling Pivot Workflow Hold Review

Date: 2026-04-22

Package: `literate-workflow-programming`
Branch: `codex/literate-workflow-pilot`
Workflow under test: `post_ceiling_pivot`

## Purpose

Record whether the new stop-to-pivot workflow held on a second real package and where it still behaved mediocrely enough to justify planned improvements.

## What Held

1. The stop boundary was real.
   The package produced a canonical donor report at the exact point where flagship iteration stopped.

2. The donor handoff was usable.
   The pivot workflow consumed the `ceiling report` without needing the legacy `post-ceiling reframe` plus `process capture` pair.

3. The overlay gates behaved correctly.
   `pivot_research_grounding` passed with `research_grounded_but_not_north_star_viable`.
   `pivot_north_star_viability` blocked rather than allowing a premature sibling flagship package.

4. The active pivot workspace held up after the filesystem split.
   The resolver found artifacts in `pivot/active/`, and legacy root-level compatibility remained intact.

5. The workflow enforced the right discipline.
   The package did not go straight from object ceiling to new draft writing. It had to produce:
   - a pivot slate
   - a grounded candidate
   - a research delta
   - a north-star viability judgment

## Where The Workflow Was Mediocre

### 1. Stage resolution is still misleading at this boundary

`stage:next` still reports `essay_iteration` as the next stage because the repo preserves compatibility stage ids. That is technically true and operationally muddy. Once the package is in live pivot work, the more useful answer is not "essay_iteration" but "active post-ceiling pivot overlay."

This is the biggest clarity weakness exposed by the pilot.

### 2. The overlay does not surface a crisp next bounded action

`workflow:resolve` for `post_ceiling_pivot` correctly reports gates and context, but it does not yet tell the operator:

- which exact submove comes next
- whether the next move is rerank, consequence pass, viability retest, or fresh search

The package had to infer that from the prose workflow doc.

### 3. Comparative rerank is a real workflow step without a canonical artifact

The workflow doc names reranking as a recurring move, but the contract does not provide a dedicated template or required artifact for it. That forced a package-local note instead of a canonical surface.

### 4. Consequence pressure is necessary but still ad hoc

The pilot showed that north-star viability can hinge on sharpening:

- the public enemy
- the consequence surface

That move is real and recurrent, but the workflow does not currently name it as an explicit substep or artifact.

### 5. Guided overlay execution is still awkward

`workflow:resolve` correctly says the overlay is guided and not directly executable in the Phase 1.5 sense. That is honest. It is also clumsy because the operator still ends up doing contract-following by hand rather than through a more structured guided packet.

## Verdict

The workflow held.

It is no longer theater. It controlled the package correctly, preserved the right boundary, and blocked a fake flagship pivot.

It is also still mediocre in operator clarity once the package enters live pivot work. The weak point is not gate semantics. The weak point is that the overlay lacks a more explicit substep model after grounding and before either clearance or abandonment.

## Improvement Targets

1. Teach `workflow:resolve` to return `next_overlay_action`.
2. Add a canonical comparative-rerank artifact or template.
3. Add a canonical consequence-pressure artifact or fold that logic into north-star viability.
4. Surface active overlay state more clearly from `stage:next` without breaking stage-id compatibility.

## Bottom Line

This pilot is strong enough to treat `post_ceiling_pivot` as a real tracked overlay.

It is not yet clean enough to call finished. The next improvement pass should target overlay clarity, not donor-report or gate semantics.
