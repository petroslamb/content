---
kind: essay_iteration_decision
package: "proof-runs-as-source-surface"
revision: 1
judgment_policy: "draft_only"
live_draft_path: "publications/proof-runs-as-source-surface/proof-runs-as-source-surface.md"
candidate_path: "publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-candidate-r1.md"
recommendation: hold_for_human_review
promotion_allowed: false
requires_human_approval: true
rewrite_mode: ""
stop_gate_status: inactive
---
# Promotion Decision

## Recommendation

`hold_for_human_review`. Treat the candidate as the active bounded replacement candidate, but do not promote or overwrite the live draft under `judgment_policy: draft_only`.

## Promotion Gate

Promotion is blocked by policy. The candidate clears the local proof packet's replacement and north-star review, but the packet explicitly forbids promotion and Publication Power 9+ claims. A human can review the candidate, inspect the proof evidence, and decide whether to open a later non-draft promotion pass.

## Required Follow-Through

Run `npm run check:essay-iteration -- --package proof-runs-as-source-surface`, run `./content-agent gate check --gate replacement_north_star --package proof-runs-as-source-surface`, and stop at the `replacement_north_star` gate before lifecycle movement. If a later pass seeks publication, verify paper claims against PDFs and run release-stage proof separately.

## Escalation Decision

Not active.

## Rewrite Mode

Not active.

## Stop Gate For Next Pass

Not active.
