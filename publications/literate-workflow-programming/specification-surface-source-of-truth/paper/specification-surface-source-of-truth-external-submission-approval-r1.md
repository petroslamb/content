---
kind: paper_external_submission_approval
package: "literate-workflow-programming/specification-surface-source-of-truth"
revision: 1
status: pending_human_decision
created: "2026-04-30"
workflow: paper_development
source_draft: "specification-surface-source-of-truth-paper-draft-r2.md"
source_pdf: "specification-surface-source-of-truth-paper-draft-r2.pdf"
source_readiness_review: "specification-surface-source-of-truth-submission-readiness-review-r2.md"
target_route: aiware_2026_arxiv_track_round_2
decision: pending
external_submission_allowed: false
arxiv_posting_allowed: false
deciding_human: null
decided_at: null
---

# External Submission Approval R1

## Current Decision

Decision: `pending`.

No external submission, arXiv posting, OpenReview action, or public essay-route mutation is authorized by this file in its current state.

## Packet Under Review

- Draft: [`specification-surface-source-of-truth-paper-draft-r2.md`](specification-surface-source-of-truth-paper-draft-r2.md)
- PDF: `specification-surface-source-of-truth-paper-draft-r2.pdf` local generated PDF, not tracked because repository policy ignores generated PDFs.
- References: [`references.bib`](references.bib)
- AIware checklist: [`submission-checklist-aiware-2026.md`](submission-checklist-aiware-2026.md)
- arXiv checklist: [`arxiv-checklist.md`](arxiv-checklist.md)
- Readiness review: [`specification-surface-source-of-truth-submission-readiness-review-r2.md`](specification-surface-source-of-truth-submission-readiness-review-r2.md)

## Decision Options

Select exactly one by updating the frontmatter `decision`, `status`, and permission fields.

- `approve_aiware_submission`: Authorizes AIware submission of the reviewed packet only. Does not automatically authorize arXiv posting unless `arxiv_posting_allowed: true` is also explicitly set.
- `skip_aiware_continue_nier_or_workshop`: Blocks AIware submission and routes the paper toward ICSE NIER or a matching workshop.
- `hold_for_revision`: Blocks external action until another draft/review cycle.
- `park_paper_route`: Parks the paper route while preserving local artifacts.

## Approval Criteria

Before changing the decision to `approve_aiware_submission`, the deciding human should confirm:

- the R2 draft is acceptable for the AIware fast-feedback route;
- the generated PDF is acceptable or has been replaced by a better submission PDF;
- the artifact availability language is acceptable for a non-anonymous fast-feedback route;
- the AI/tool-use disclosure is acceptable;
- the paper does not claim that natural language is code;
- the paper does not claim passive docs, prompts, or context files are automatically governed specification surfaces;
- the paper does not claim generated code stops mattering;
- the paper does not claim richer or more formal specification always improves model behavior;
- arXiv posting remains blocked unless separately approved.

## Pending State

Current state: `pending_human_decision`.

The workflow has produced the packet and stopped at the approval boundary. Any external action requires a human update to this file.
