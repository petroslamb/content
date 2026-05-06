# Real Run Index

This file is the registry for real Codex traces considered by Reviewable Runs.

Only three statuses are allowed here:

- `flagship proof`
- `secondary candidate`
- `rejected`

These statuses are proof-retention statuses, not framework-fit scores. A run can be a strong fit for Reviewable Runs and still remain a secondary candidate if it adds little new public proof value.

## Current Inventory

| Run title | Source session | Status | Task boundary | Evidence | Verification | Approval | Public-facing now | Why it qualifies or fails |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| March 7 origin refactor | `019cc91f-24bb-73c3-a4c0-f20aa5a844a8` | `flagship proof` | Strong | Strong | Partial | Partial | Yes | Clear shift from artifact bundles to reviewable runs, strong dossier/evaluation/archive evidence, but stopped at handoff rather than commit. |
| March 12 alphaXiv auth refactor | `019ce138-a4aa-7b22-ba6c-7964fe7b5261` | `flagship proof` | Strong | Strong | Strong | Strong | Yes | External coding-package run with API-key-first auth refactor, real local verification loop, and pushed commit boundary `24bdff1`. |
| March 27 manual mirror import | `019d3034-c6d4-7ab3-a4e5-ca26cdf6fc0d` | `flagship proof` | Strong | Strong | Strong | Strong | Yes | Publish-style fallback run that imported seven posts, validated the mirror locally, pushed commit `1e31aa9`, and confirmed the deployed GitHub Pages state live. |
| March 27 YouTube playlist-order fix | `019d3075-745a-7a51-a9de-57e05701e8fe` | `flagship proof` | Strong | Strong | Strong | Strong | Yes | External-action run with mixed API and Studio control, live playlist reorder, and final state verified directly on YouTube. |
| March 26 standalone extraction | `019d2949-bad3-7000-82af-238c4a07affa` | `flagship proof` | Strong | Strong | Strong | Strong | Yes | Bounded restructuring run with explicit decoupling, cleanup, validation sweeps, and commit boundary `f3c1241`. |
| March 26 compact public package refactor | `019d2949-bad3-7000-82af-238c4a07affa` | `flagship proof` | Strong | Strong | Strong | Strong | Yes | Focused packaging/usability refactor with explicit deletion of old front doors, path cleanup, and commit boundary `e581b07`. |
| March 27 YouTube cross-link fallback | `019d3075-745a-7a51-a9de-57e05701e8fe` | `secondary candidate` | Strong | Strong | Strong | Partial | No | Useful external-action run with live description updates, but weaker than the playlist fix because the approval boundary is more implicit and the effect is less structurally testable. |
| March 27 audio slideshow renderer | `019d3075-745a-7a51-a9de-57e05701e8fe` | `secondary candidate` | Strong | Strong | Partial | Partial | No | Good artifact-generation run with script and cue output, but weaker on external approval and downstream verification than the YouTube platform run. |
| March 27 transcript alignment limit | `019d3075-745a-7a51-a9de-57e05701e8fe` | `secondary candidate` | Strong | Strong | Partial | Partial | No | Valuable real limit-finding run: the alignment helper worked as a draft mechanism, but the transcript/slide mismatch exposed a real automation boundary rather than a strong public proof. |
| March 26 proof/operator docs expansion | `019d2949-bad3-7000-82af-238c4a07affa` | `secondary candidate` | Strong | Strong | Partial | Strong | No | Good real build run ending at `8210956`, but it overlaps heavily with later proof and package work. |
| March 26 validation-lab creation | `019d2949-bad3-7000-82af-238c4a07affa` | `secondary candidate` | Strong | Strong | Partial | Strong | No | Useful for framework growth, but less representative as a first public proof than extraction or package refactor. |
| March 26 validation results pass | `019d2949-bad3-7000-82af-238c4a07affa` | `secondary candidate` | Strong | Strong | Strong | Strong | No | Good run-level evaluation example ending at `c0ce338`, but best treated as support for the validation harness rather than a flagship proof. |
| March 26 essay bundle rewrite | `019d2add-b2f3-7ad0-a3f9-745c231ddf7e` | `secondary candidate` | Strong | Partial | Partial | Strong | No | Real editorial run with commits and checks, but evidence and verification are thinner than the framework package runs. |
| March 26 companion essay rewrite | `019d2b22-6f81-7180-8ce8-563421ee1de4` | `secondary candidate` | Strong | Partial | Partial | Strong | No | Real bounded content-editing run with commit boundary, but weaker on evidence provenance and explicit review surface. |
| March 26 opinion-only review | `019d2b40-b5a8-7751-9611-1a84e3368280` | `rejected` | Partial | Weak | Weak | Weak | No | Mostly evaluative discussion with no meaningful action, verification, or governance handoff. |
| March 27 sync workflow diagnosis and fallback decision | `019d3034-c6d4-7ab3-a4e5-ca26cdf6fc0d` | `secondary candidate` | Strong | Strong | Strong | Partial | No | Good operational run showing parser-fix diagnosis, branch/PR isolation, and an honest stop when Substack `403` kept the workflow from succeeding end to end. |
| March 27 pdf-slides skill creation | `019d2c65-5dfd-7f81-b0cb-514c856472de` | `secondary candidate` | Strong | Strong | Strong | Partial | No | Clean skill-construction run with real validation and export test, but the approval boundary is installation and local verification rather than a stronger commit, release, or external deployed state. |
| Specification surface full lifecycle | tracked repo evidence; local session dumps not imported | `secondary candidate` | Strong | Strong | Strong | Strong | No | Real leaf-publication lifecycle completed through research, draft, polish, Substack publication, archive sync, YouTube/media, and distribution. Kept secondary because the proof is retrospective/hybrid rather than one strict autonomous `content-agent` lifecycle run. |

## Promotion Rule

Promote a secondary candidate only if it adds a new kind of real evidence that the current flagship proofs do not already show.

For now, the public proof set is:

1. `march-07-origin-refactor/`
2. `march-12-alphaxiv-auth-refactor/`
3. `march-27-manual-mirror-import/`
4. `march-27-youtube-playlist-order-fix/`
5. `march-26-standalone-extraction/`
6. `march-26-compact-public-package/`
