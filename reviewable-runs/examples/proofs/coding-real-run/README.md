# Proof: Coding Real Run

**Status:** `real captured run`

This folder contains a real bounded coding-agent run captured in a temporary proof repository and reconstructed into the reviewable-runs surface.

## Scenario

The run fixes a narrow regression in an invoice serializer: invoices with a `0%` discount lost the `"0%"` label because the serializer used truthiness instead of an explicit `None` check.

## Why This Is The First Proof

Coding is the cheapest place to prove the framework because:

- the task boundary is easy to state
- the evidence surface is concrete
- verification is cheap
- the merge gate is obvious

## Folder Map

- `raw-artifacts/`: the original task, terminal transcript, test output, and patch artifact
- `review-packet/`: the six-record reconstructed packet
- `comparison.md`: what the review packet makes legible that raw artifacts alone do not

## Run Outcome

- one targeted regression failed
- the agent inspected the serializer and test file
- one line changed
- the targeted regression passed
- the full suite passed
- the patch was held for merge approval instead of auto-merged

## What This Proves

This proof is not meant to prove universal superiority.

It is meant to show that:

- a real run can be reconstructed into the six-record surface
- the packet is more reviewable than raw artifacts alone
- the framework can support real operator use rather than only synthetic teaching dossiers
