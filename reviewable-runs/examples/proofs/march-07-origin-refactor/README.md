# Proof: March 7 Origin Refactor

**Status:** `real captured run`

This folder reconstructs the first explicit refactor that changed the upstream blueprint package from packet-style worked examples to the reviewable-runs model.

## Scenario

The run takes an existing `autonomous-agent-blueprint` worked-example layer organized around artifact bundles and rewrites it around one clearer standard: one dossier per case, backed by runtime and governance records, with the old packet-oriented layer preserved as archive.

## Why This Proof Matters

This is the framework's origin case. It shows that the idea did not begin as an abstract essay. It came out of a real documentation and architecture refactor with migration risk, archive concerns, and review-surface design decisions.

## Folder Map

- `raw-artifacts/`: curated extracts from the original Codex session
- `review-packet/`: the reconstructed six-record review surface
- `comparison.md`: what the packet makes clearer than the raw trace alone

## Run Outcome

- `reviewable-runs.md` became the conceptual source of truth
- dossier-first case folders replaced the flat packet-oriented examples
- the older artifact-bundle model was archived under `archive/case-studies-v1/`
- front-door docs, evaluation docs, and use cases were rerouted
- the run stopped at handoff and did not self-approve a merge

## What This Proves

This proof shows that Reviewable Runs can describe a real origin refactor even when the run ends before commit. That matters because many serious review boundaries are handoffs, not auto-merge events.

