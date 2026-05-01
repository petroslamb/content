---
kind: paper_publication_route
package: "literate-workflow-programming/specification-surface-source-of-truth"
status: researched_route
created: "2026-04-30"
updated: "2026-04-30"
workflow: paper_development
source_blueprint: "specification-surface-source-of-truth-paper-blueprint.md"
recommended_primary_category: "cs.SE"
---

# Publication Route For The Specification Surface Paper

## Recommendation

Do not submit the current blueprint, essay, or a lightly academicized essay to arXiv.

The best route is:

1. Build a real paper manuscript from the blueprint: framework + systematization + illustrative artifact analysis.
2. Use the AIware 2026 ArXiv Track only if a credible 6-8 page manuscript can be ready by May 15, 2026. Treat this as fast community exposure, not archival proceedings publication.
3. Use ICSE 2027 NIER as the strongest peer-reviewed route if the paper remains a new framework with initial case-study evidence. Deadline: October 23, 2026.
4. Use ICSE 2027 Research Track only if the case study and method mature quickly enough to support a full research paper. Mandatory abstract: June 23, 2026. Paper: June 30, 2026.
5. Use ICSE 2027 workshops as the fallback peer-review route once accepted workshop topics are known. Workshop paper deadline: November 27, 2026.

The practical default should be:

paper draft -> optional AIware ArXiv Track -> ICSE NIER or workshop -> arXiv preprint once the manuscript is a complete research article.

## Route Ranking

| Rank | Route | Best Use | Deadline | Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| 1 | AIware 2026 ArXiv Track | Fast discussion of AI-powered software work; no proceedings; accepts arXiv/public-style manuscripts. | May 15, 2026 for Round 2. | Use only if the manuscript can become coherent immediately. Good for visibility and feedback, not archival review. |
| 2 | ICSE 2027 NIER | Peer-reviewed new idea with initial evidence and future-work path. | October 23, 2026. | Best peer-reviewed target for the current maturity if the case study is small but concrete. |
| 3 | ICSE 2027 Workshops | Workshop review after the accepted workshop list is known. | Workshop proposal acceptance expected August 17, 2026; paper deadline November 27, 2026. | Strong fallback; pick the workshop whose CFP best matches AI-assisted software engineering, requirements, agents, or SE governance. |
| 4 | ICSE 2027 Research Track | Full SE research paper. | Abstract June 23, 2026; paper June 30, 2026. | High bar and soon. Target only if the case study becomes a defensible method and evaluation quickly. |
| 5 | Journal route | Full expanded article after workshop/NIER feedback. | Rolling. | Too slow and too heavy as the first review route unless the paper grows into a larger empirical/framework article. |

## What The Paper Needs Before arXiv

Minimum viable arXiv manuscript:

- title and abstract;
- introduction with clear research gap;
- crisp definition of `specification surface`;
- taxonomy table;
- lifecycle model;
- related-work/systematization section;
- method section explaining paper selection and case-study method;
- evidence mapping table;
- concrete case-study or artifact-analysis section;
- discussion of code-review implications;
- limitations and threats to validity;
- references;
- artifact/data availability note;
- AI/tool-use disclosure if required by the target venue.

Do not post to arXiv until the case-study or artifact-analysis section exists. Without it, the manuscript will read like a position essay or survey.

## arXiv Plan

Recommended category:

- Primary: `cs.SE`
- Cross-list: `cs.AI` only if the final paper foregrounds AI agents and agent systems enough to justify it.

Do not use `cs.PL` unless the paper formalizes a language or semantics. Do not use `cs.SY` or `eess.SY` unless the paper genuinely develops a control/feedback-system model.

Submission sequence:

1. Create an arXiv account and verify author identity.
2. Confirm whether the author needs Computer Science endorsement. New submitters or submitters entering a new category may need it.
3. Prepare LaTeX source, figures, and bibliography. If the manuscript is TeX-derived, submit the TeX source rather than a generated PDF.
4. Choose license deliberately. The default safest choice for later venue compatibility is usually the arXiv non-exclusive distribution license unless a target venue or funder requires a Creative Commons license.
5. Submit under `cs.SE` with optional `cs.AI` cross-list.
6. Expect moderation for category fit and scholarly content. Do not describe arXiv posting as peer review.
7. If a venue review is in progress, follow that venue's anonymity and preprint rules. Do not mention the submission venue in the arXiv version during double-anonymous review.

Important arXiv policy facts:

- arXiv is a moderated repository, not a peer-review venue.
- arXiv accepts scholarly article-like submissions, but not every PDF or essay-like text is suitable.
- arXiv CS review/survey/position papers are riskier unless peer-reviewed first or clearly original enough to stand as a research article.
- The paper should therefore emphasize the definition, taxonomy, lifecycle model, explicit method, and artifact analysis.

Official sources:

- arXiv category taxonomy: https://arxiv.org/category_taxonomy
- arXiv submission overview: https://info.arxiv.org/help/submit/index.html
- arXiv endorsement: https://info.arxiv.org/help/endorsement.html
- arXiv moderation: https://info.arxiv.org/help/moderation/index.html
- arXiv content types: https://info.arxiv.org/help/policies/content-types.html
- arXiv license options: https://info.arxiv.org/help/license/index.html
- arXiv CS review/position update: https://blog.arxiv.org/2025/10/31/attention-authors-updated-practice-for-review-articles-and-position-papers-in-arxiv-cs-category/

## Review Route Details

### AIware 2026 ArXiv Track

Fit:

The track is about AI-powered software and software engineering. The paper's `specification surface` argument fits if framed around AI-assisted software engineering governance, agent harnesses, validation, and workflow authority.

Why it helps:

- The Round 2 deadline is close but reachable: May 15, 2026.
- Submissions can be accepted from PDF as well as arXiv links, but accepted submissions should be on arXiv before the conference date.
- Accepted papers are not in proceedings, so this is a visibility/discussion route rather than archival peer review.
- Reviews are lightweight relative to a full ICSE/ASE/FSE research track.

What it needs:

- 6-8 page credible manuscript.
- A concrete case-study or artifact-analysis section.
- Clear statement that the paper is a framework/systematization/case-study paper, not a position essay.

Official source:

- AIware 2026 ArXiv Track: https://conf.researchr.org/track/aiware-2026/aiware-2026-arxiv-track

### ICSE 2027 NIER

Fit:

This is the strongest peer-reviewed route if the contribution remains a new conceptual framework with initial evidence. NIER is for new ideas, emerging results, and early-stage research directions. The current paper can fit if it presents a concrete model and illustrative artifact analysis, while being honest that broader validation remains future work.

Why it helps:

- The October 23, 2026 deadline gives enough time to build the case-study trace and produce a tight 4-page paper.
- It is peer reviewed.
- It allows the paper to be framed as an emerging SE research direction rather than overclaiming full empirical maturity.

What it needs:

- 4 pages plus references in the official ICSE format.
- A concise problem statement.
- A novel framework contribution.
- Initial evidence: taxonomy + literature map + local artifact analysis.
- Explicit future-work plan.
- Double-anonymous compliance.

Official source:

- ICSE 2027 NIER: https://conf.researchr.org/track/icse-2027/icse-2027-new-ideas-and-emerging-results--nier-

### ICSE 2027 Research Track

Fit:

Possible but ambitious. The paper would need to look like a full SE research contribution, not only a well-argued framework.

Why it is hard:

- Abstract deadline is June 23, 2026 and full paper deadline is June 30, 2026.
- The research track expects mature contribution and a strong method.
- A single illustrative case study may be too thin unless the artifact analysis becomes systematic and the framework is positioned as a research method.

What it needs:

- Full paper in IEEE format.
- Research questions and method.
- Systematic selection/coding of literature.
- Case-study protocol.
- Threats to validity.
- Artifact availability.

Official source:

- ICSE 2027 Research Track: https://conf.researchr.org/track/icse-2027/icse-2027-research-track

### ICSE 2027 Workshops

Fit:

Likely strong once the workshop list is known. This paper could fit a workshop on AI-assisted software engineering, agents, requirements engineering, or software-engineering governance.

Why it helps:

- Workshop papers can be shorter and discussion-oriented while still peer reviewed.
- Accepted workshop list is expected before paper deadlines.
- Paper deadline is November 27, 2026.

Official source:

- ICSE 2027 Workshops: https://conf.researchr.org/track/icse-2027/icse-2027-workshops

## Not Recommended As First Route

| Route | Why Not First |
| :--- | :--- |
| Pure arXiv now | The current artifact is a blueprint, not a paper. A premature arXiv post risks looking like a position essay. |
| ASE 2026 Research | Deadline has passed for the current date. Future ASE can be reconsidered. |
| FSE 2026 Research | Deadline has passed for the current date. Future FSE can be reconsidered. |
| Requirements Engineering 2026 Research | Deadline has passed for the current date. Future RE can be reconsidered if the framing shifts toward requirements/specification governance. |
| Journal-first | Too slow and too heavy before the framework has community feedback. Better after NIER/workshop feedback. |

## Manuscript Workplan

### Phase 1: Paperization Sprint

Target: May 10, 2026.

Outputs:

- extended abstract;
- case-study trace note;
- literature mapping appendix;
- first paper draft in ACM or IEEE style.

Decision:

- If strong by May 10, submit AIware ArXiv Track by May 15.
- If not strong, skip AIware and keep building for ICSE NIER.

### Phase 2: Review-Ready Short Paper

Target: September 15, 2026.

Outputs:

- 4-page ICSE NIER version;
- anonymous artifact appendix if allowed;
- cleaned references and limitations;
- arXiv decision note.

Decision:

- Submit ICSE NIER by October 23.
- If NIER fit is poor, wait for ICSE workshop list and submit to a matching workshop by November 27.

### Phase 3: arXiv Posting

Best timing:

- If AIware route is used: arXiv before the AIware conference date.
- If ICSE NIER/workshop route is used: either post before submission if anonymity rules allow and there is a strategic reason, or wait until after submission/acceptance for the cleanest review posture.

The arXiv version should be a complete paper, not a venue proposal.

## Required Paper Assets

Create these under `paper/`:

- `specification-surface-source-of-truth-extended-abstract-r1.md`
- `specification-surface-source-of-truth-literature-mapping-r1.md`
- `specification-surface-source-of-truth-case-study-trace-r1.md`
- `specification-surface-source-of-truth-paper-draft-r1.tex` or `.md`
- `references.bib`
- `figures/`

Optional but useful:

- `submission-checklist-aiware-2026.md`
- `submission-checklist-icse-nier-2027.md`
- `arxiv-checklist.md`

## arXiv Readiness Checklist

- The paper is not just the essay.
- The contribution is named in the abstract and introduction.
- The paper contains one definition, taxonomy, lifecycle model, evidence map, and case study.
- Limitations explicitly forbid the natural-language-is-code, passive-docs, generated-code-does-not-matter, and more-formality-is-always-better claims.
- `cs.SE` is primary category.
- Cross-list decision is recorded.
- Author account and endorsement status are resolved.
- LaTeX source compiles locally.
- Figures are source-tracked or reproducible.
- Bibliography is complete.
- Artifact availability statement is included.
- Target venue preprint/anonymity policy is checked before posting.

## Current State And Next Decision

The first paperization sprint artifacts now exist:

1. `specification-surface-source-of-truth-case-study-trace-r1.md`
2. `specification-surface-source-of-truth-extended-abstract-r1.md`
3. `specification-surface-source-of-truth-literature-mapping-r1.md`
4. `specification-surface-source-of-truth-paper-north-star-rubric-r1.md`
5. `specification-surface-source-of-truth-draftability-audit-r1.md`
6. `specification-surface-source-of-truth-paper-draft-approval-gate-r1.md`
7. `specification-surface-source-of-truth-paper-draft-r1.md`
8. `references.bib`
9. `submission-checklist-aiware-2026.md`
10. `arxiv-checklist.md`
11. `specification-surface-source-of-truth-submission-readiness-review-r1.md`
12. `specification-surface-source-of-truth-paper-draft-r2.md`
13. `specification-surface-source-of-truth-paper-draft-r2.pdf`
14. `specification-surface-source-of-truth-submission-readiness-review-r2.md`
15. `specification-surface-source-of-truth-external-submission-approval-r1.md`

The draftability audit and docs-only approval gate authorized starting `specification-surface-source-of-truth-paper-draft-r1.md` for the AIware fast-feedback sprint. The R1 draft and route checklists now exist.

The R2 readiness review does not authorize external submission or arXiv posting. It marks the local packet ready for human external-submission approval. The approval surface now exists in `pending_human_decision` state. Before any external action, that surface must be updated by a human. arXiv posting separately needs license, endorsement/account, and venue-policy decisions.
