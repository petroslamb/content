# Proof: March 26 Standalone Extraction

**Status:** `real captured run`

This folder reconstructs the run that finalized `reviewable-runs` as a standalone package and pushed `publications/autonomous-agents` back into a cleaner upstream role.

## Scenario

The run removes remaining bridge surfaces from the blueprint package, consolidates the blueprint front door, tightens maintenance guidance, and commits the extraction as one coherent repo restructuring change.

## Why This Proof Matters

This is the first fully committed real trace that shows Reviewable Runs operating on its own package boundary. It has a clear repo-scoped task, explicit validation sweeps, and a visible commit approval boundary.

## Folder Map

- `raw-artifacts/`: curated session evidence, commit record, and validation outputs
- `review-packet/`: the reconstructed six-record surface
- `comparison.md`: what the packet makes clearer than the raw trace

## Run Outcome

- `reviewable-runs` remained the standalone package
- explicit routing from `publications/autonomous-agents` into `reviewable-runs` was removed
- redundant root orientation docs in the blueprint package were removed
- maintenance and contributing guidance were tightened
- the resulting extraction landed as commit `f3c1241`

## What This Proves

This proof shows the framework on a real documentation and repo-structure run with a concrete commit boundary, structural validation, and a meaningful approval surface.

