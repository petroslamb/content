# Post-Block Route Review

Date: 2026-04-22

Package: `literate-workflow-programming`
Branch: `codex/literate-workflow-pilot`
Workflow under test: `post_ceiling_pivot`

## Purpose

Record whether the workflow held at the exact boundary after a grounded candidate failed north-star viability and the package had to choose between:

- keeping the object as a narrower doctrine piece
- or restarting the pivot search

## Package Decision

The package made the decision explicitly in [`publications/literate-workflow-programming/pivot/active/literate-workflow-programming-pivot-decision.md`](../../publications/literate-workflow-programming/pivot/active/literate-workflow-programming-pivot-decision.md):

- keep `Validation Is Lifecycle Infrastructure` as a strong narrower doctrine object
- do not open a sibling flagship package
- do not restart broad successor hunting now
- reopen pivot search only if a materially larger successor seam appears later

This is the right substantive decision from the tracked evidence.

## What Held

1. The workflow did not force fake motion.
   The package was allowed to stop escalating the active candidate instead of pretending one more rescue pass would clear the flagship bar.

2. The gate layer stayed honest.
   `pivot_research_grounding` still passes and `pivot_north_star_viability` still blocks after the route decision.

3. The package now has an inspectable route decision.
   The decision is no longer implicit in scattered notes.

## Where The Workflow Is Still Mediocre

### 1. The resolver does not consume the decision it asked for

After the package made the route decision, both:

- `stage:next -- --package literate-workflow-programming`
- `workflow:resolve -- --workflow post_ceiling_pivot --package literate-workflow-programming`

still report:

- `overlay_phase: decide_post_block_route`
- `next_overlay_action: decide_narrow_or_restart_pivot_search`

That means the workflow can name the right question, but it cannot tell that the package already answered it.

### 2. The pivot decision artifact is too human-readable for the current harness

The package truth is now in prose:

- keep as narrower doctrine object
- postpone fresh pivot search

But the current harness only understands the older verdicts like:

- `research_grounded_but_not_north_star_viable`
- `pivot_cleared_for_north_star_attempt`

So the decision note is load-bearing for humans and mostly invisible to automation.

### 3. The overlay lacks a terminal blocked state

There is no canonical overlay phase like:

- `keep_as_narrower_doctrine_object`
- `park_pivot_search`
- `await_new_successor_seam`

So the package stays in a live decision phase even after the decision is made.

## Verdict

The workflow held at the editorial level and did a mediocre job at the state-machine level.

It helped the package make the right decision.
It did not yet know how to recognize that the decision was complete.

## Improvement Targets

1. Extend the pivot decision contract with an explicit post-block route field.
2. Teach the harness to resolve completed routes such as:
   - `keep_as_narrower_doctrine_object`
   - `restart_pivot_search_later`
3. Stop reporting `decide_post_block_route` once the package already contains an explicit completed route.

## Bottom Line

The package is now in a settled post-block state.

The workflow is strong enough to prevent fake flagship escalation.
It is still weak at recognizing a completed blocked-route decision after north-star failure.
