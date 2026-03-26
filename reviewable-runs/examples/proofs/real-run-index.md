# Real Run Index

This file is the registry for real Codex traces considered by Reviewable Runs.

Only three statuses are allowed here:

- `flagship proof`
- `secondary candidate`
- `rejected`

## Current Inventory

| Run title | Source session | Status | Task boundary | Evidence | Verification | Approval | Public-facing now | Why it qualifies or fails |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| March 7 origin refactor | `019cc91f-24bb-73c3-a4c0-f20aa5a844a8` | `flagship proof` | Strong | Strong | Partial | Partial | Yes | Clear shift from artifact bundles to reviewable runs, strong dossier/evaluation/archive evidence, but stopped at handoff rather than commit. |
| March 26 standalone extraction | `019d2949-bad3-7000-82af-238c4a07affa` | `flagship proof` | Strong | Strong | Strong | Strong | Yes | Bounded restructuring run with explicit decoupling, cleanup, validation sweeps, and commit boundary `f3c1241`. |
| March 26 compact public package refactor | `019d2949-bad3-7000-82af-238c4a07affa` | `flagship proof` | Strong | Strong | Strong | Strong | Yes | Focused packaging/usability refactor with explicit deletion of old front doors, path cleanup, and commit boundary `e581b07`. |
| March 26 proof/operator docs expansion | `019d2949-bad3-7000-82af-238c4a07affa` | `secondary candidate` | Strong | Strong | Partial | Strong | No | Good real build run ending at `8210956`, but it overlaps heavily with later proof and package work. |
| March 26 validation-lab creation | `019d2949-bad3-7000-82af-238c4a07affa` | `secondary candidate` | Strong | Strong | Partial | Strong | No | Useful for framework growth, but less representative as a first public proof than extraction or package refactor. |
| March 26 validation results pass | `019d2949-bad3-7000-82af-238c4a07affa` | `secondary candidate` | Strong | Strong | Strong | Strong | No | Good run-level evaluation example ending at `c0ce338`, but best treated as support for the validation harness rather than a flagship proof. |
| March 26 essay bundle rewrite | `019d2add-b2f3-7ad0-a3f9-745c231ddf7e` | `secondary candidate` | Strong | Partial | Partial | Strong | No | Real editorial run with commits and checks, but evidence and verification are thinner than the framework package runs. |
| March 26 companion essay rewrite | `019d2b22-6f81-7180-8ce8-563421ee1de4` | `secondary candidate` | Strong | Partial | Partial | Strong | No | Real bounded content-editing run with commit boundary, but weaker on evidence provenance and explicit review surface. |
| March 26 opinion-only review | `019d2b40-b5a8-7751-9611-1a84e3368280` | `rejected` | Partial | Weak | Weak | Weak | No | Mostly evaluative discussion with no meaningful action, verification, or governance handoff. |

## Promotion Rule

Promote a secondary candidate only if it adds a new kind of real evidence that the current flagship proofs do not already show.

For now, the public proof set is:

1. `march-07-origin-refactor/`
2. `march-26-standalone-extraction/`
3. `march-26-compact-public-package/`

