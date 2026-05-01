---
kind: paper_draft_approval_gate
package: "<package>"
workflow: paper_development
status: pending
source_audit: "<draftability-audit>"
approval_model: two_reviewer_docs_only_gate
decision: pending
manuscript_drafting_allowed: false
---

# <Paper Title> Draft Approval Gate

## Gate Purpose

This docs-only gate decides whether manuscript drafting may start. It does not submit to arXiv, OpenReview, a workshop, a conference, or a journal.

## North-Star Bar

Fast-feedback ladder with peer-review quality floor:

1. AIware sprint only if the audit clears a coherent fast-feedback short paper.
2. ICSE NIER/workshop remains the main peer-review route.
3. arXiv waits until the manuscript packet is complete and compatible with target venue policy.

## Required Inputs

- Paper roadmap:
- Paper north-star rubric:
- Draftability audit:
- Literature mapping:
- Case-study trace or method note:
- Publication route note:

## Reviewer A Decision

Reviewer A owns scholarship, evidence, and method.

Reviewer A verdict:

Reviewer A blockers:

## Reviewer B Decision

Reviewer B owns venue fit, paper shape, and reviewability.

Reviewer B verdict:

Reviewer B blockers:

## Gate Decision

Choose one:

- `approve_aiware_sprint`
- `approve_peer_review_short_paper`
- `hold_for_method_hardening`
- `park_paper_route`

Decision:

Manuscript drafting allowed: `false`

## Required Follow-Through

If approved, name the exact draft target and route. If not approved, name the method, evidence, or route work required before rerunning this gate.
