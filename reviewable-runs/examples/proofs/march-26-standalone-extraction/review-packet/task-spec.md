# Runtime Record: Task Spec

## Task

Finalize the extraction of `reviewable-runs` into a standalone package by removing remaining bridge routing from the blueprint package, consolidating blueprint root docs, and landing the combined restructuring as one commit.

## Objective

- make `reviewable-runs` the derivative package that points upstream, not the reverse
- reduce root clutter in `publications/autonomous-agents`
- tighten maintenance and contributing guidance around post-publication research updates
- commit the extraction as one coherent repo change

## Inputs

- the user's decoupling and cleanup requests
- the current bridge references in blueprint docs
- the package docs in both `publications/autonomous-agents` and `reviewable-runs`

## Constraints

- keep the blueprint package self-contained
- preserve `reviewable-runs` as the derivative work with origin links back to AAB
- avoid stale links to deleted root docs
- stop only after the repo-level commit boundary is reached

## Stop Condition

The packages are decoupled in the intended direction, the blueprint root is consolidated, and the restructuring is committed with a clean worktree.

