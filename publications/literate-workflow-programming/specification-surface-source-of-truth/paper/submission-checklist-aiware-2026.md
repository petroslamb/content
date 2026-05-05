---
kind: submission_checklist
package: "literate-workflow-programming/specification-surface-source-of-truth"
workflow: paper_development
status: submitted_to_aiware
created: "2026-04-30"
updated: "2026-05-05"
target: aiware_2026_arxiv_track_round_2
source_draft: "specification-surface-source-of-truth-paper-draft-r3.md"
source_pdf: "specification-surface-source-of-truth-paper-draft-r3.pdf"
external_submission_allowed: false
arxiv_posting_allowed: false
submitted_at: "2026-05-05T17:35:57+03:00"
verified_online: "2026-05-05"
---

# AIware 2026 ArXiv Track Checklist

## Route Facts

Official source: <https://conf.researchr.org/track/aiware-2026/aiware-2026-arxiv-track>

- Conference: AIware 2026, co-located with FSE 2026, July 6-7, 2026.
- Venue location listed online: Montreal, Canada.
- Round 2 submission deadline: May 15, 2026 AoE.
- Round 2 notification: June 1, 2026.
- Submission form: <https://forms.gle/rYgz3NGVa3o9UrYK9>
- Accepted submissions do not appear in proceedings.
- Manuscripts do not need to be on arXiv at submission time, but accepted works should be made available on arXiv before the conference date.
- Anonymization is not required.
- Supplemental materials, datasets, and artifacts are encouraged.
- There is no enforced page or word limit, but the track suggests keeping manuscript length commensurate with contribution. It points to main-track guidance: 8 pages for full-length papers, 2-4 pages for short papers, and 14-20 pages for surveys or literature reviews.

## Current Local Status

| Item | Status | Notes |
| :--- | :--- | :--- |
| Paper draft | done | `specification-surface-source-of-truth-paper-draft-r3.md` is the current recommended packet after pre-submit polish. |
| References | done | `references.bib` exists. |
| Method paragraph | done for local review | R3 names the unit, corpus, coding protocol, observation boundary, and non-claims. |
| Artifact availability statement | done for AIware draft | R3 states that no separate public supplemental bundle is included and keeps the case illustrative. |
| AI/tool-use disclosure | done for AIware draft | R3 includes a disclosure statement; revisit if venue wording is stricter. |
| Figure/table decisions | partial | Draft has tables and a text lifecycle figure; decide whether to render figures. |
| Post-draft readiness review | done | `specification-surface-source-of-truth-submission-readiness-review-r1.md` holds submission for method and packet tightening. |
| R2 readiness review | done | `specification-surface-source-of-truth-submission-readiness-review-r2.md` marks the packet ready for human approval. |
| R3 readiness review | done | `specification-surface-source-of-truth-submission-readiness-review-r3.md` recommends R3 for final human confirmation. |
| PDF | done for local review | `specification-surface-source-of-truth-paper-draft-r3.pdf` exists, includes rendered references, and visually checks cleanly on table pages. |
| Human approval for external submission | done | `specification-surface-source-of-truth-external-submission-approval-r1.md` approved R2; the submitter then confirmed and submitted the R3 packet. |
| AIware form submission | done | Google Forms confirmation page displayed "Your response has been recorded" on 2026-05-05. |
| arXiv posting | blocked | Do not post until manuscript packet and policy review are complete. |

## Submission Blockers

- arXiv posting remains blocked.
- No resubmission or draft update should be attempted unless the chairs explicitly allow it.

## Local Pre-Submission Checks

- [x] Review `specification-surface-source-of-truth-paper-draft-r1.md` for coherence, length, and venue fit.
- [x] Create `specification-surface-source-of-truth-paper-draft-r2.md`.
- [x] Create `specification-surface-source-of-truth-paper-draft-r3.md` for pre-submit venue/claim polish.
- [x] Confirm the draft stays within the forbidden-frame boundaries.
- [x] Tighten the illustrative artifact-analysis method paragraph.
- [ ] Decide whether the lifecycle model and taxonomy should remain tables/text or become figures.
- [x] Finalize artifact availability language for the AIware draft route.
- [x] Generate a PDF.
- [x] Render full references from `references.bib` into the PDF.
- [x] Create or update `arxiv-checklist.md`.
- [x] Record human approval before any external submission.
- [x] Record final human confirmation to submit R3 rather than R2.
- [x] Rerun `./content-agent validate --workflow paper_development --package literate-workflow-programming/specification-surface-source-of-truth`.
- [x] Rerun `npm run check:repo-links`.
- [x] Submit through the AIware Google Form.
- [x] Record the submission in `specification-surface-source-of-truth-aiware-submission-record-r1.md`.

## Decision

Current decision: `submitted_to_aiware`

R3 was submitted to the AIware 2026 ArXiv Track. Do not upload to arXiv, resubmit, or post elsewhere without a separate approval surface.
