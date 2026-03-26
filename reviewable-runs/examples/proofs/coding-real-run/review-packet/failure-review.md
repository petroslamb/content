# Governance Record: Failure Review

## Failure

The plausible near miss is that the patch fixes the explicit `0%` label regression while still leaving some nearby invoice serialization edge case under-tested.

## Why It Is Plausible

The run is intentionally narrow. It inspected only one module and one test file, then relied on a small test suite for verification. That is appropriate for a bounded fix, but it still creates a risk that an adjacent formatting path is untested.

## Taxonomy Mapping

- `First-pass overconfidence`
- `Irreversible action without enough evidence`

## Checklist Controls

- use the targeted regression rerun plus the full suite, not only the target test
- surface residual risk explicitly before merge
- require merge review rather than auto-merge

## What Would Reduce The Failure

- add one more regression test if invoice discount formatting has adjacent contract variants
- keep the merge gate human-reviewed for this class of billing changes

## Decision

keep
