---
kind: case_study_trace_plan
package: proof-runs-as-source-surface
workflow: paper_development
status: planning
---

# Case-Study Trace Plan

## Unit Of Analysis

One governed proof-campaign run of `paper_development` on
`proof-runs-as-source-surface`.

## Artifact Corpus

- `reviewable-runs/resolved-runs/phase-2-8-proof-paper-development-proof-runs.yaml`
- `reviewable-runs/logs/phase-2-8-proof-paper-development-proof-runs*.json`
- `reviewable-runs/logs/phase-2-8-proof-paper-development-proof-runs*.yaml`
- `reviewable-runs/subagent-requests/*phase-2-8-proof-paper-development-proof-runs*.yaml`
- `reviewable-runs/subagent-results/*phase-2-8-proof-paper-development-proof-runs*.md`
- `publications/proof-runs-as-source-surface/paper/*.md`

## Coding Scheme

| Code | Question |
| :--- | :--- |
| workflow_identity | Does the artifact bind workflow id, version, package, and run id? |
| context_admission | Are admitted input paths and hashes visible? |
| path_boundary | Are read/write boundaries explicit and respected? |
| handoff_integrity | Are request/result artifacts linked and verified? |
| gate_or_blocker | Is the stopping condition explicit? |
| external_mutation | Is external mutation absent or approved? |
| lifecycle_movement | Is lifecycle movement absent or approved? |
| promotion_boundary | Is proof evidence separated from promotion claims? |

## Observations To Collect

- Which artifacts provide trust evidence before any output is read.
- Which artifacts make continuation or blocker diagnosis possible.
- Which artifacts are insufficient without human review.

## Non-Claims

This case study does not claim external validity, autonomous publication safety,
workflow promotion, or benchmark superiority.
