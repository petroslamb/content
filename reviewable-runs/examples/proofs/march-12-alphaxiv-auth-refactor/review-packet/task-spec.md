# Runtime Record: Task Spec

## Task

Refactor `alphaxiv-py` to API-key-first runtime auth, keep browser login only as an explicit optional path, align docs and packaging with that behavior, and land the result as one pushed commit.

## Objective

- remove automatic browser-token refresh from steady-state SDK and CLI usage
- make API-key auth a first-class saved/runtime path
- clarify that a headless browser is not required for normal use
- add missing publishability surfaces that were needed to ship the repo cleanly
- stop only after the refactor is committed and pushed

## Inputs

- the user's direct request to fix the auth path
- the question about whether a headless browser was required
- the current `alphaxiv-py` auth, CLI, docs, and packaging surfaces

## Constraints

- keep the public client usable without a browser dependency in normal operation
- preserve an explicit browser-login path instead of breaking that capability entirely
- keep the CLI surface broadly stable while clarifying auth semantics
- leave the repo publishable at the end of the run

## Stop Condition

The runtime auth path is API-key-first, browser support is clearly optional, verification passes, and the refactor lands as a pushed commit with a clean worktree.
