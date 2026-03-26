# Proof: March 12 alphaXiv Auth Refactor

**Status:** `real captured run`

This folder reconstructs the bounded `alphaxiv-py` run that shifted the package to API-key-first auth, kept browser login optional, added publishability surfaces, and landed the result as a pushed commit.

## Scenario

The run starts from a direct user request to fix the auth path and clarify whether a headless browser is required. It ends when the refactor is committed and pushed as `24bdff1`.

## Why This Proof Matters

This is the first flagship proof outside the `reviewable-runs` package itself. It shows the framework on a real library-and-CLI engineering run with:

- a clear coding objective
- local verification with tests, lint, and type checking
- a publish-oriented cleanup pass
- a concrete commit-and-push approval boundary

## Folder Map

- `raw-artifacts/`: curated session evidence, changed-surface summary, verification outputs, commit record, and boundary record
- `review-packet/`: the reconstructed six-record surface
- `comparison.md`: what the packet makes clearer than the raw trace

## Run Outcome

- runtime auth became API-key-first
- browser login stayed explicit and optional instead of sitting on the steady-state path
- docs and package metadata were updated to match the runtime behavior
- `LICENSE`, CI, and the observational API inventory landed with the refactor
- the run ended at pushed commit `24bdff1`

## What This Proves

This proof shows that Reviewable Runs works on a real external coding package with stronger verification than the documentation-heavy package proofs and with a clearer publish/governance boundary than an uncommitted handoff run.
