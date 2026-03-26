# Failure Review: Enterprise Policy Memo

## Failure

The first draft of the memo used a superseded retention clause that still appeared in retrieval results because an archived policy copy was indexed alongside the current version.

## Why it is plausible

This is the exact kind of failure a retrieval-backed enterprise agent will face: the content is relevant enough to retrieve and polished enough to look trustworthy, but it is operationally stale.

## Taxonomy mapping

- [`../../../../implementation/evaluation/failure-mode-catalog.md`](../../../../implementation/evaluation/failure-mode-catalog.md): `Stale memory reuse`
- [`../../../../implementation/evaluation/failure-mode-catalog.md`](../../../../implementation/evaluation/failure-mode-catalog.md): `Retrieval poisoning`

## Checklist controls that should catch it

- [`../../../../implementation/evaluation/architecture-review-checklist.md`](../../../../implementation/evaluation/architecture-review-checklist.md): `Is there a write policy for memory rather than automatic logging?`
- [`../../../../implementation/evaluation/architecture-review-checklist.md`](../../../../implementation/evaluation/architecture-review-checklist.md): `Are retrieval and memory treated as attack surfaces?`
- [`../../../../implementation/evaluation/architecture-review-checklist.md`](../../../../implementation/evaluation/architecture-review-checklist.md): `Is verification stronger than a single first-pass answer?`

## What would reduce the failure

- require freshness metadata in every evidence row
- rank current revisions above archived copies at retrieval time
- make supersession checks mandatory in the verification stage

## Decision

Keep the enterprise default architecture. Tighten retrieval freshness controls rather than replacing the architecture.
