---
kind: paper_work_surface
package: "literate-workflow-programming/specification-surface-source-of-truth"
status: experimental
workflow: paper_development
---

# Paper Work

This folder holds the experimental paper route for the `specification-surface-source-of-truth` leaf.

It is separate from the Substack essay route. Do not promote files from this folder into the live essay without an explicit essay-iteration decision.

Start with [`specification-surface-source-of-truth-paper-roadmap-r1.md`](specification-surface-source-of-truth-paper-roadmap-r1.md). That roadmap is the package-local status surface for what is done, what remains, and whether the route is drafting, hardening, submitting, or parked.

## Current Artifacts

- [`specification-surface-source-of-truth-paper-roadmap-r1.md`](specification-surface-source-of-truth-paper-roadmap-r1.md): package-local operating surface for completed artifacts, remaining artifacts, current phase, next decision, and rejection/parking policy.
- [`specification-surface-source-of-truth-paper-north-star-rubric-r1.md`](specification-surface-source-of-truth-paper-north-star-rubric-r1.md): governing rubric for the draftability audit and docs-only two-reviewer approval gate.
- [`specification-surface-source-of-truth-paper-blueprint.md`](specification-surface-source-of-truth-paper-blueprint.md): framework/systematization/case-study blueprint for turning the essay argument into a viable paper.
- [`specification-surface-source-of-truth-publication-route-r1.md`](specification-surface-source-of-truth-publication-route-r1.md): researched arXiv and peer-review route, including venue priorities, deadlines, manuscript requirements, and readiness checklist.
- [`specification-surface-source-of-truth-case-study-trace-r1.md`](specification-surface-source-of-truth-case-study-trace-r1.md): local artifact-analysis trace that keeps the paper route concrete rather than purely positional.
- [`specification-surface-source-of-truth-literature-mapping-r1.md`](specification-surface-source-of-truth-literature-mapping-r1.md): appendix-ready mapping from sources to taxonomy roles, lifecycle stages, paper sections, and claim boundaries.
- [`specification-surface-source-of-truth-extended-abstract-r1.md`](specification-surface-source-of-truth-extended-abstract-r1.md): short-paper skeleton for AIware/ICSE NIER go/no-go work.
- [`specification-surface-source-of-truth-draftability-audit-r1.md`](specification-surface-source-of-truth-draftability-audit-r1.md): two-role scoring audit that approves starting an AIware fast-feedback manuscript draft while blocking submission.
- [`specification-surface-source-of-truth-paper-draft-approval-gate-r1.md`](specification-surface-source-of-truth-paper-draft-approval-gate-r1.md): docs-only two-reviewer gate authorizing manuscript drafting but not external submission.
- [`specification-surface-source-of-truth-paper-draft-r1.md`](specification-surface-source-of-truth-paper-draft-r1.md): first full Markdown manuscript draft for internal review.
- [`references.bib`](references.bib): working bibliography for the manuscript draft.
- [`submission-checklist-aiware-2026.md`](submission-checklist-aiware-2026.md): AIware 2026 route checklist and current submission blockers.
- [`arxiv-checklist.md`](arxiv-checklist.md): arXiv posting checklist and current posting blockers.
- [`specification-surface-source-of-truth-submission-readiness-review-r1.md`](specification-surface-source-of-truth-submission-readiness-review-r1.md): post-draft review that keeps external submission blocked pending revision, PDF, and human approval.
- [`specification-surface-source-of-truth-paper-draft-r2.md`](specification-surface-source-of-truth-paper-draft-r2.md): revised manuscript draft with tightened artifact-analysis method and artifact/disclosure language.
- `specification-surface-source-of-truth-paper-draft-r2.pdf`: local review PDF generated from the R2 Markdown draft; not tracked because repository policy ignores generated PDFs.
- [`specification-surface-source-of-truth-submission-readiness-review-r2.md`](specification-surface-source-of-truth-submission-readiness-review-r2.md): post-R2 review that marks the packet ready for human external-submission approval, while keeping submission blocked.
- [`specification-surface-source-of-truth-external-submission-approval-r1.md`](specification-surface-source-of-truth-external-submission-approval-r1.md): human approval gate authorizing AIware submission of the reviewed R2 packet, while keeping arXiv blocked.
- [`specification-surface-source-of-truth-paper-draft-r3.md`](specification-surface-source-of-truth-paper-draft-r3.md): pre-submit polish manuscript with author block, rendered bibliography metadata, tightened venue framing, and revised claim/artifact language.
- `specification-surface-source-of-truth-paper-draft-r3.pdf`: current local submission-candidate PDF generated from R3; not tracked because repository policy ignores generated PDFs.
- [`specification-surface-source-of-truth-submission-readiness-review-r3.md`](specification-surface-source-of-truth-submission-readiness-review-r3.md): post-R3 review that recommends R3 for final human confirmation before form submission.
- [`specification-surface-source-of-truth-aiware-submission-record-r1.md`](specification-surface-source-of-truth-aiware-submission-record-r1.md): pending record for the actual AIware form submission and confirmation details.

## Current Status

The blueprint, publication route, case-study trace, literature map, extended abstract, north-star rubric, draftability audit, docs-only approval gate, manuscript drafts, working references, AIware checklist, arXiv checklist, local PDFs, readiness reviews, human approval gate, and submitted AIware record are complete. The current phase is waiting for the AIware Round 2 notification on June 1, 2026.

The north-star bar is a fast-feedback ladder with a peer-review quality floor: try AIware only if the manuscript remains coherent by the checkpoint, mature toward ICSE NIER or workshop review as the main peer-review route, and wait on arXiv until a complete manuscript packet exists. The draft approval gate authorized manuscript drafting only; the later external-submission approval gate now authorizes AIware submission while keeping arXiv posting blocked.

The reviewed R2 packet was approved for AIware submission. R3 superseded R2 after the pre-submit polish pass and was submitted through the AIware Google Form on 2026-05-05. arXiv remains blocked until a separate posting decision resolves license, endorsement/account, and venue-policy questions.

## Workflow

Use the experimental root workflow:

```bash
./content-agent validate --workflow paper_development --package literate-workflow-programming/specification-surface-source-of-truth
```

The workflow goal is not to publish a paper directly. It should produce and harden paper-facing artifacts in this folder:

- paper roadmap/status surface
- paper north-star rubric
- paper blueprint
- literature mapping table
- case-study trace plan
- draftability audit
- docs-only two-reviewer approval gate
- method note when the case-study trace is too thin
- manuscript draft
- references and venue checklist surfaces

## Boundary

The allowed paper route is:

- framework
- systematization
- illustrative case study

The forbidden route is:

- lightly academicized essay
- pure position paper
- pure literature review
- arXiv submission before the paper has a concrete contribution

If the experiment is rejected, park it rather than deleting it. Keep useful paper artifacts, mark the route as parked, and remove the shared workflow from active maps only if it should no longer be advertised.
