---
kind: paper_draft_approval_gate
package: "literate-workflow-programming/specification-surface-source-of-truth"
revision: 1
status: approved_for_drafting
created: "2026-04-30"
workflow: paper_development
source_audit: "specification-surface-source-of-truth-draftability-audit-r1.md"
approval_model: two_reviewer_docs_only_gate
decision: approve_aiware_sprint
manuscript_drafting_allowed: true
external_submission_allowed: false
---

# Specification Surface Paper Draft Approval Gate R1

## Gate Purpose

This docs-only gate decides whether manuscript drafting may start. It does not submit to arXiv, OpenReview, a workshop, a conference, or a journal.

Verdict: manuscript drafting may start for the AIware fast-feedback sprint.

## North-Star Bar

Fast-feedback ladder with peer-review quality floor:

1. AIware sprint only if the audit clears a coherent fast-feedback short paper.
2. ICSE NIER/workshop remains the main peer-review route.
3. arXiv waits until the manuscript packet is complete and compatible with target venue policy.

## Required Inputs

- Paper roadmap: [`specification-surface-source-of-truth-paper-roadmap-r1.md`](specification-surface-source-of-truth-paper-roadmap-r1.md)
- Paper north-star rubric: [`specification-surface-source-of-truth-paper-north-star-rubric-r1.md`](specification-surface-source-of-truth-paper-north-star-rubric-r1.md)
- Draftability audit: [`specification-surface-source-of-truth-draftability-audit-r1.md`](specification-surface-source-of-truth-draftability-audit-r1.md)
- Literature mapping: [`specification-surface-source-of-truth-literature-mapping-r1.md`](specification-surface-source-of-truth-literature-mapping-r1.md)
- Case-study trace: [`specification-surface-source-of-truth-case-study-trace-r1.md`](specification-surface-source-of-truth-case-study-trace-r1.md)
- Publication route note: [`specification-surface-source-of-truth-publication-route-r1.md`](specification-surface-source-of-truth-publication-route-r1.md)

## Reviewer A Decision

Reviewer A owns scholarship, evidence, and method.

Reviewer A verdict: `approve_aiware_sprint`

Reviewer A blockers: no drafting blocker. Method hardening is required before external submission.

## Reviewer B Decision

Reviewer B owns venue fit, paper shape, and reviewability.

Reviewer B verdict: `approve_aiware_sprint`

Reviewer B blockers: no drafting blocker. Submission remains blocked until the manuscript, references, artifact statement, figure/table choices, and route checklist exist.

## Gate Decision

Decision: `approve_aiware_sprint`

Manuscript drafting allowed: `true`

External submission allowed: `false`

## Required Follow-Through

Draft target:

- `specification-surface-source-of-truth-paper-draft-r1.md`

Draft route:

- AIware fast-feedback short paper first if the draft is coherent by the checkpoint.
- Keep ICSE NIER/workshop as the quality floor and next review path.
- Do not post to arXiv until the manuscript packet is complete and preprint policy has been checked.

Required draft contents:

- introduction with clear research gap;
- definition of `specification surface`;
- taxonomy table;
- lifecycle model;
- literature mapping section;
- concise method paragraph for illustrative artifact analysis;
- case-study artifact table;
- limitations and threats to validity;
- references placeholder strategy;
- artifact availability placeholder.
