# Post-Block Route Recognition Review

Date: 2026-04-22

Package: `literate-workflow-programming`
Branch: `codex/literate-workflow-pilot`
Workflow under test: `post_ceiling_pivot`

## Purpose

Record whether the workflow now recognizes a completed post-block route after the package settles on a non-flagship outcome for the active pivot candidate.

## What Improved

The workflow now consumes the explicit route from [`publications/literate-workflow-programming/pivot/active/literate-workflow-programming-pivot-decision.md`](../../publications/literate-workflow-programming/pivot/active/literate-workflow-programming-pivot-decision.md).

Both:

- `stage:next -- --package literate-workflow-programming`
- `workflow:resolve -- --workflow post_ceiling_pivot --package literate-workflow-programming`

now resolve:

- `overlay_phase: post_block_route_settled`
- `overlay_route: keep_as_strong_narrower_doctrine_object`
- `next_overlay_action: hold_for_narrower_doctrine_write_or_later_larger_successor`

That is materially better than the prior state, which kept repeating `decide_post_block_route` after the package had already made the decision.

## Why This Matters

The overlay is no longer merely naming the right question.

It can now distinguish:

- a north-star-blocked candidate that still needs a route decision
- a north-star-blocked candidate whose route has already been settled

That makes the workflow state machine meaningfully more honest.

## What Is Still Mediocre

The top compatibility surface still says:

- `next_stage: essay_iteration`

That is technically consistent with the repo’s stage-id model, but it remains less useful than the overlay state for an operator trying to understand the real next move.

So the workflow is now good at the overlay-substep level and still somewhat muddy at the top stage label.

## Verdict

This improvement closes the biggest exposed weakness from the pilot’s post-block boundary.

The overlay now recognizes a settled blocked route instead of leaving the package in fake indecision.

The remaining weakness is mostly presentation and compatibility shape, not route correctness.
