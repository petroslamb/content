# Effective Route Cleanup Review

Date: 2026-04-22

Package: `literate-workflow-programming`
Branch: `codex/literate-workflow-pilot`
Workflow under test: `stage:next` with active `post_ceiling_pivot`

## Purpose

Record whether the stage surface now communicates the real live route clearly enough after the pilot exposed the compatibility-stage mismatch.

## What Improved

`stage:next` still preserves:

- `next_stage: essay_iteration`

for compatibility.

But it now also exposes the operational truth directly:

- `effective_workflow: post_ceiling_pivot`
- `effective_workflow_kind: overlay`
- `effective_next_action: hold_for_narrower_doctrine_write_or_later_larger_successor`
- `effective_route: keep_as_strong_narrower_doctrine_object`
- `effective_can_execute: false`

That is the right separation.

The stage id remains stable for existing callers.
The real route is no longer hidden inside lower-priority overlay fields.

## Why This Is Better

Before this cleanup, the top of `stage:next` suggested:

- stage: `essay_iteration`
- can execute: `true`

which was technically compatible and operationally misleading, because the live route was really a guided overlay that should not be executed like a normal stage run.

After the cleanup, the operator can read the response in two layers:

1. compatibility stage
2. effective live workflow

That makes the output much harder to misread.

## Remaining Weakness

The compatibility stage still appears first in the JSON shape because that field is preserved.

So the surface is now honest enough, but it is still not as elegant as a future route-first interface could be.

## Verdict

This cleanup is good enough.

The route layer now communicates the real package state without breaking compatibility, and the biggest remaining issue is presentation preference rather than workflow correctness.
