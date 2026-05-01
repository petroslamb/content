---
kind: submission_checklist
package: "literate-workflow-programming/specification-surface-source-of-truth"
workflow: paper_development
status: blocked_until_human_approval
created: "2026-04-30"
target: aiware_2026_arxiv_track_round_2
source_draft: "specification-surface-source-of-truth-paper-draft-r2.md"
source_pdf: "specification-surface-source-of-truth-paper-draft-r2.pdf"
external_submission_allowed: false
verified_online: "2026-04-30"
---

# AIware 2026 ArXiv Track Checklist

## Route Facts

Official source: <https://conf.researchr.org/track/aiware-2026/aiware-2026-arxiv-track>

- Conference: AIware 2026, co-located with FSE 2026, July 6-7, 2026.
- Round 2 submission deadline: May 15, 2026 AoE.
- Round 2 notification: June 1, 2026.
- Accepted submissions do not appear in proceedings.
- Manuscripts do not need to be on arXiv at submission time, but accepted works should be made available on arXiv before the conference date.
- Anonymization is not required.
- Supplemental materials, datasets, and artifacts are encouraged.
- There is no enforced page or word limit, but the track suggests keeping manuscript length commensurate with contribution. It points to main-track guidance: 8 pages for full-length papers, 2-4 pages for short papers, and 14-20 pages for surveys or literature reviews.

## Current Local Status

| Item | Status | Notes |
| :--- | :--- | :--- |
| Paper draft | done | `specification-surface-source-of-truth-paper-draft-r2.md` exists. |
| References | done | `references.bib` exists. |
| Method paragraph | done for local review | R2 names the unit, corpus, coding protocol, observation boundary, and non-claims. |
| Artifact availability statement | done for AIware draft | R2 includes route-aware artifact language; revisit if route shifts to double-anonymous review. |
| AI/tool-use disclosure | done for AIware draft | R2 includes a disclosure statement; revisit if venue wording is stricter. |
| Figure/table decisions | partial | Draft has tables and a text lifecycle figure; decide whether to render figures. |
| Post-draft readiness review | done | `specification-surface-source-of-truth-submission-readiness-review-r1.md` holds submission for method and packet tightening. |
| R2 readiness review | done | `specification-surface-source-of-truth-submission-readiness-review-r2.md` marks the packet ready for human approval. |
| PDF | done for local review | `specification-surface-source-of-truth-paper-draft-r2.pdf` exists; final venue-format polish may still be requested. |
| Human approval for external submission | pending | `specification-surface-source-of-truth-external-submission-approval-r1.md` exists but does not approve submission. |
| arXiv posting | blocked | Do not post until manuscript packet and policy review are complete. |

## Submission Blockers

- Human external-submission approval is pending and not granted.
- Venue-format polish may still be needed because the local PDF has wide-table overfull-box warnings.
- The manuscript has not yet passed a human AIware external-submission approval review.

## Local Pre-Submission Checks

- [x] Review `specification-surface-source-of-truth-paper-draft-r1.md` for coherence, length, and venue fit.
- [x] Create `specification-surface-source-of-truth-paper-draft-r2.md`.
- [x] Confirm the draft stays within the forbidden-frame boundaries.
- [x] Tighten the illustrative artifact-analysis method paragraph.
- [ ] Decide whether the lifecycle model and taxonomy should remain tables/text or become figures.
- [x] Finalize artifact availability language for the AIware draft route.
- [x] Generate a PDF.
- [x] Create or update `arxiv-checklist.md`.
- [ ] Record human approval before any external submission.
- [ ] Rerun `./content-agent validate --workflow paper_development --package literate-workflow-programming/specification-surface-source-of-truth`.
- [ ] Rerun `npm run check:repo-links`.

## Decision

Current decision: `blocked_until_human_approval`

The draft may be reviewed and revised locally. It may not be submitted to AIware, uploaded to arXiv, or posted through OpenReview without a separate human approval surface.
