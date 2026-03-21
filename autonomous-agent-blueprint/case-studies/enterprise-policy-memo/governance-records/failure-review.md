# Governance Record: Failure Review

## Failure

The first draft absorbed a superseded retention clause because an archived policy copy was indexed alongside the current version.

## Why It Is Plausible

This is a standard enterprise retrieval miss: the text is relevant, polished, and operationally stale at the same time.

## Taxonomy Mapping

- [`../../../evaluation/failure-mode-catalog.md`](../../../evaluation/failure-mode-catalog.md): `Stale memory reuse`
- [`../../../evaluation/failure-mode-catalog.md`](../../../evaluation/failure-mode-catalog.md): `Retrieval poisoning`

## Checklist Controls

- [`../../../evaluation/architecture-review-checklist.md`](../../../evaluation/architecture-review-checklist.md): `Can the system show what evidence, provenance, or state supported the run?`
- [`../../../evaluation/architecture-review-checklist.md`](../../../evaluation/architecture-review-checklist.md): `Can the system show how the result or action was verified?`
- [`../../../evaluation/architecture-review-checklist.md`](../../../evaluation/architecture-review-checklist.md): `Are retrieval and memory treated as attack surfaces?`

## What Would Reduce The Failure

- require freshness metadata in every evidence row
- rank current revisions above archived copies at retrieval time
- make supersession checks mandatory in verification

## Decision

Keep the enterprise default architecture. Tighten retrieval freshness controls rather than widening the workflow.
