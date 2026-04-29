---
kind: essay_iteration_decision
package: "literate-workflow-programming/specification-surface-source-of-truth"
revision: 3
judgment_policy: "draft_only"
live_draft_path: "publications/literate-workflow-programming/specification-surface-source-of-truth/specification-surface-source-of-truth.md"
candidate_path: "publications/literate-workflow-programming/specification-surface-source-of-truth/specification-surface-source-of-truth-candidate-r3.md"
recommendation: keep_live
promotion_allowed: false
requires_human_approval: true
rewrite_mode: human_publication_review
stop_gate_status: inactive
---
# Promotion Decision

## Recommendation

`keep_live`

Keep the live draft unchanged under `draft_only` policy and send `specification-surface-source-of-truth-candidate-r3.md` to human replacement review. R3 is the strongest candidate so far, but this packet cannot promote it automatically.

## Promotion Gate

Promotion remains blocked by policy, not by the old bridge-evidence gap or by the r2 publication-sharpness blocker. The r3 review finds that the candidate clears the named north-star blocker, but `promotion_allowed` remains `false` and `requires_human_approval` remains `true`.

## Required Follow-Through

Run the packet validators and keep `essay_iteration.done` false. Do not overwrite `specification-surface-source-of-truth.md`. A human reviewer may later approve promotion, request publication polish against r3, or decide to keep the live anchor.

## Escalation Decision

North-star escalation is no longer active because the r3 replacement review is not `below_north_star` and this decision does not recommend another autonomous candidate revision.

## Rewrite Mode

`human_publication_review`

Further changes should be human-directed publication edits against r3, not a new research pass or broad r4 rewrite.

## Stop Gate For Next Pass

`inactive`

The stop gate does not need to fire because r3 clears the prior north-star blocker. The workflow should pause for human review rather than continue automatic same-object iteration.
