---
kind: paper_roadmap
package: "literate-workflow-programming/specification-surface-source-of-truth"
revision: 1
status: submitted_to_aiware_arxiv_blocked_by_endorsement
created: "2026-04-30"
updated: "2026-05-05"
workflow: paper_development
current_phase: arxiv_endorsement_blocker
next_artifact: "arxiv_endorsement_result_or_aiware_notification"
runner_patch_required: false
rejection_policy: park
north_star_bar: fast_feedback_ladder_with_peer_review_quality_floor
approval_model: two_reviewer_docs_only_gate
---

# Specification Surface Paper Roadmap

This is the package-local operating surface for the experimental paper route. It records what already exists, what remains, and which decision comes next.

The route is intentionally separate from the public essay route. Paper artifacts in this folder do not promote, replace, or publish the live essay.

The north-star bar is a fast-feedback ladder with a peer-review quality floor: try AIware only if the audit clears it, mature toward ICSE NIER or workshop review as the main peer-review route, and wait on arXiv until a complete manuscript packet exists.

## Current State

The paper has cleared the first paperization sprint and produced a local manuscript packet:

- north-star rubric exists;
- blueprint exists;
- publication route exists;
- literature mapping exists;
- case-study trace exists;
- extended abstract exists;
- draftability audit exists;
- docs-only approval gate exists;
- first manuscript draft exists;
- working references exist;
- AIware and arXiv checklists exist;
- venue conflict matrix exists;
- post-draft readiness reviews exist;
- R2 draft, R3 pre-submit polish draft, and R4 arXiv-facing draft exist;
- local review PDFs exist;
- generated arXiv TeX source packet exists;
- arXiv readiness review exists;
- arXiv submission attempt record exists;
- external submission approval surface exists and approved AIware submission;
- AIware submission record exists in `submitted` state.

The workflow crossed the human approval gate for the R2 AIware packet. R3 superseded R2 after the pre-submit paper-shape and AI-written-tell pass, and the R3 PDF was submitted through the AIware Google Form on 2026-05-05. R4 now exists as an arXiv-facing fail-fast preprint packet with a generated TeX source archive. The arXiv browser flow was started, but arXiv blocked continuation because the account is not endorsed for `cs.SE`. arXiv posting remains blocked until endorsement is granted.

## Phase Ledger

| Phase | Status | Surface | Exit Criteria |
| :--- | :--- | :--- | :--- |
| Route setup | Done | `README.md`, blueprint, publication route | The paper route is separated from the essay route and has a viable framework/systematization/case-study shape. |
| Rubric setup | Done | `specification-surface-source-of-truth-paper-north-star-rubric-r1.md` | The draftability audit and approval gate share one scoring bar. |
| Draftability audit | Done | `specification-surface-source-of-truth-draftability-audit-r1.md` | Decision: `approve_aiware_sprint` for manuscript drafting only. |
| Approval gate | Done | `specification-surface-source-of-truth-paper-draft-approval-gate-r1.md` | Two reviewer roles approved the same drafting route. |
| Method hardening | Partial | `specification-surface-source-of-truth-paper-draft-r1.md`, readiness review | The draft includes a method section, but the readiness review requires tighter protocol and observation language before submission. |
| Manuscript draft | Done | `specification-surface-source-of-truth-paper-draft-r1.md` | First coherent short-paper draft exists in Markdown. |
| Venue packet | Done for local review | `references.bib`, AIware checklist, arXiv checklist, R2 PDF | References, route checklists, artifact/disclosure language, and a local PDF exist; final venue-format polish may still be requested. |
| Submission decision | Done for R2 | `specification-surface-source-of-truth-submission-readiness-review-r2.md` | Decision: ready for human approval gate; no external submission yet. |
| Human approval | Done | `specification-surface-source-of-truth-external-submission-approval-r1.md` | Decision: `approve_aiware_submission`; arXiv remains blocked. |
| Pre-submit R3 polish | Done | `specification-surface-source-of-truth-paper-draft-r3.md`, `specification-surface-source-of-truth-submission-readiness-review-r3.md` | R3 PDF exists with rendered references and tightened venue framing. |
| AIware submission record | Done | `specification-surface-source-of-truth-aiware-submission-record-r1.md` | Records submission timestamp, form route, submitted packet, and browser confirmation. |
| Venue conflict matrix | Done | `specification-surface-source-of-truth-venue-conflict-matrix-r1.md` | Separates AIware/arXiv compatibility from future venue and moderation risks. |
| arXiv R4 packet | Done | `specification-surface-source-of-truth-paper-draft-r4.md`, `arxiv-source-r4/` | R4 Markdown, local PDF, generated TeX source, and source archive exist for human posting decision. |
| arXiv readiness review | Done | `specification-surface-source-of-truth-arxiv-readiness-review-r1.md` | Decision: `ready_for_human_posting_decision`; public posting still blocked. |
| arXiv submission attempt | Blocked | `specification-surface-source-of-truth-arxiv-submission-attempt-r1.md` | Start page completed for `cs.SE`; arXiv requires endorsement before upload. |
| arXiv endorsement | Pending | Email/code held outside repository | A qualified `cs.SE` endorser must endorse the account before submission can continue. |
| AIware notification | Pending | To be created after June 1, 2026 notification | Record accept/reject outcome, reviewer/chair feedback if any, and next route decision. |

## Completed Surfaces

- [`specification-surface-source-of-truth-paper-north-star-rubric-r1.md`](specification-surface-source-of-truth-paper-north-star-rubric-r1.md)
- [`specification-surface-source-of-truth-paper-blueprint.md`](specification-surface-source-of-truth-paper-blueprint.md)
- [`specification-surface-source-of-truth-publication-route-r1.md`](specification-surface-source-of-truth-publication-route-r1.md)
- [`specification-surface-source-of-truth-case-study-trace-r1.md`](specification-surface-source-of-truth-case-study-trace-r1.md)
- [`specification-surface-source-of-truth-literature-mapping-r1.md`](specification-surface-source-of-truth-literature-mapping-r1.md)
- [`specification-surface-source-of-truth-extended-abstract-r1.md`](specification-surface-source-of-truth-extended-abstract-r1.md)
- [`specification-surface-source-of-truth-draftability-audit-r1.md`](specification-surface-source-of-truth-draftability-audit-r1.md)
- [`specification-surface-source-of-truth-paper-draft-approval-gate-r1.md`](specification-surface-source-of-truth-paper-draft-approval-gate-r1.md)
- [`specification-surface-source-of-truth-paper-draft-r1.md`](specification-surface-source-of-truth-paper-draft-r1.md)
- [`references.bib`](references.bib)
- [`submission-checklist-aiware-2026.md`](submission-checklist-aiware-2026.md)
- [`arxiv-checklist.md`](arxiv-checklist.md)
- [`specification-surface-source-of-truth-submission-readiness-review-r1.md`](specification-surface-source-of-truth-submission-readiness-review-r1.md)
- [`specification-surface-source-of-truth-paper-draft-r2.md`](specification-surface-source-of-truth-paper-draft-r2.md)
- `specification-surface-source-of-truth-paper-draft-r2.pdf` local generated PDF, not tracked because repository policy ignores generated PDFs
- [`specification-surface-source-of-truth-submission-readiness-review-r2.md`](specification-surface-source-of-truth-submission-readiness-review-r2.md)
- [`specification-surface-source-of-truth-external-submission-approval-r1.md`](specification-surface-source-of-truth-external-submission-approval-r1.md)
- [`specification-surface-source-of-truth-paper-draft-r3.md`](specification-surface-source-of-truth-paper-draft-r3.md)
- `specification-surface-source-of-truth-paper-draft-r3.pdf` local generated PDF, not tracked because repository policy ignores generated PDFs
- [`specification-surface-source-of-truth-submission-readiness-review-r3.md`](specification-surface-source-of-truth-submission-readiness-review-r3.md)
- [`specification-surface-source-of-truth-aiware-submission-record-r1.md`](specification-surface-source-of-truth-aiware-submission-record-r1.md)
- [`specification-surface-source-of-truth-venue-conflict-matrix-r1.md`](specification-surface-source-of-truth-venue-conflict-matrix-r1.md)
- [`specification-surface-source-of-truth-paper-draft-r4.md`](specification-surface-source-of-truth-paper-draft-r4.md)
- `specification-surface-source-of-truth-paper-draft-r4.pdf` local generated PDF, not tracked because repository policy ignores generated PDFs
- [`specification-surface-source-of-truth-arxiv-readiness-review-r1.md`](specification-surface-source-of-truth-arxiv-readiness-review-r1.md)
- [`specification-surface-source-of-truth-arxiv-submission-attempt-r1.md`](specification-surface-source-of-truth-arxiv-submission-attempt-r1.md)
- [`arxiv-source-r4/README.md`](arxiv-source-r4/README.md)
- [`arxiv-source-r4/spec_surface_r4_arxiv.tex`](arxiv-source-r4/spec_surface_r4_arxiv.tex)

## Remaining Surfaces

- `cs.SE` endorsement result
- AIware notification outcome after June 1, 2026
- public or anonymized artifact snapshot, optional before arXiv but recommended for credibility
- `figures/`, only if a lifecycle or taxonomy figure is needed for the chosen venue shape
- `submission-checklist-icse-nier-2027.md`, only if AIware is rejected or the paper route should continue toward peer-reviewed publication

## Draftability Audit Bar

Use [`specification-surface-source-of-truth-paper-north-star-rubric-r1.md`](specification-surface-source-of-truth-paper-north-star-rubric-r1.md) as the governing rubric.

The audit must answer:

- Is the contribution more than an essay claim?
- Is the case study concrete enough for a framework/systematization/case-study paper?
- Which claims are supported by literature?
- Which claims are supported only by local artifact analysis?
- Which claims must be weakened or removed?
- Is the May 10, 2026 AIware go/no-go plausible, or should the route move toward ICSE NIER/workshop review?

Valid audit decisions:

- `approve_aiware_sprint`: draft a 6-8 page short paper immediately only after the two-reviewer approval gate also clears this route.
- `approve_peer_review_short_paper`: draft toward a peer-reviewed short-paper route only after the two-reviewer approval gate also clears this route.
- `hold_for_method_hardening`: improve the case-study method before drafting.
- `park_paper_route`: park the route because the contribution is not paper-shaped enough or violates hard caps.

## Approval Gate

Manuscript drafting is blocked until `specification-surface-source-of-truth-paper-draft-approval-gate-r1.md` exists and records matching reviewer decisions.

- Reviewer A owns scholarship, evidence, and method.
- Reviewer B owns venue fit, paper shape, and reviewability.
- Both reviewers must independently approve the same route.
- A split verdict blocks drafting; revise the audit or method and rerun the gate.

Current gate result: `submitted_to_aiware_arxiv_blocked_by_endorsement`. R3 is the submitted AIware packet. R4 is the prepared arXiv packet. arXiv posting remains blocked on `cs.SE` endorsement.

## Rejection And Parking

Default rejection policy: park it.

If the experiment is rejected:

- keep package-local `paper/` artifacts as useful notes;
- mark this roadmap or the shared workflow README as parked;
- remove the workflow from active workflow maps if it should no longer be advertised;
- do not delete the blueprint, route research, literature map, case trace, or extended abstract unless a later artifact supersedes them;
- do not patch `content-agent` for the rejected experiment.

If the route succeeds across more than one paper package, consider promoting `paper_development` from an experimental workflow to a stable scholarship workflow.

## Runner Boundary

No `content-agent` patch is required for this experiment. The runner already discovers `workflows/*/workflow.yaml`; this route should remain data-driven unless a later generic validator is justified.

Validation commands:

```bash
./content-agent validate --workflow paper_development --package literate-workflow-programming/specification-surface-source-of-truth
npm run check:workflow-yaml -- --format json
npm run check:repo-links
```

Also run a targeted scan for absolute local paths, file URI strings, and placeholder-link markers in the package paper folder and shared workflow folder.
