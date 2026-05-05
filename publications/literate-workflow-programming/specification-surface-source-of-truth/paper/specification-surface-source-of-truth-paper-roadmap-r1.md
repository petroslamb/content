---
kind: paper_roadmap
package: "literate-workflow-programming/specification-surface-source-of-truth"
revision: 1
status: active_experiment
created: "2026-04-30"
updated: "2026-05-05"
workflow: paper_development
current_phase: aiware_form_submission
next_artifact: "submitted_confirmation_in_specification-surface-source-of-truth-aiware-submission-record-r1.md"
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
- post-draft readiness reviews exist;
- R2 draft exists;
- local review PDF exists;
- external submission approval surface exists and approves AIware submission;
- AIware submission record exists in `pending_submission` state.

The workflow has crossed the human approval gate for AIware submission. The next substantive step is actual submission through the AIware form, followed by a local submission record. arXiv posting remains blocked unless separately approved.

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
| AIware submission record | Pending | `specification-surface-source-of-truth-aiware-submission-record-r1.md` | Record submission timestamp, form route, submitted packet, and any confirmation details. |

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
- [`specification-surface-source-of-truth-aiware-submission-record-r1.md`](specification-surface-source-of-truth-aiware-submission-record-r1.md)

## Remaining Surfaces

- submitted confirmation recorded in `specification-surface-source-of-truth-aiware-submission-record-r1.md`
- `figures/`, only if a lifecycle or taxonomy figure is needed for the chosen venue shape
- `submission-checklist-icse-nier-2027.md`, only if AIware is skipped or rejected

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

Current gate result: `approve_aiware_submission`. The reviewed R2 packet is authorized for AIware submission. arXiv posting remains blocked.

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
