---
kind: essay_iteration_decision
package: "$package_key"
revision: $revision
judgment_policy: "$judgment_policy"
live_draft_path: "$live_draft_path"
candidate_path: "$candidate_path"
recommendation: revise_candidate
promotion_allowed: false
requires_human_approval: true
rewrite_mode: ""
stop_gate_status: inactive
---
# Promotion Decision

## Recommendation

Choose one of: `promote_candidate`, `revise_candidate`, `keep_live`.

## Promotion Gate

State why promotion is still blocked or why the packet is ready for human review.

## Required Follow-Through

List the next concrete actions required before the stage can be marked done.

## Escalation Decision

Required only when north-star escalation mode is active; otherwise write `Not active.`

## Rewrite Mode

Required only when north-star escalation mode is active; otherwise write `Not active.`

## Stop Gate For Next Pass

Required only when north-star escalation mode is active; otherwise write `Not active.`
