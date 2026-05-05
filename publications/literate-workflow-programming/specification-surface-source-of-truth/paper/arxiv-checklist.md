---
kind: arxiv_checklist
package: "literate-workflow-programming/specification-surface-source-of-truth"
workflow: paper_development
status: blocked_by_endorsement
created: "2026-04-30"
recommended_primary_category: cs.SE
source_draft: "specification-surface-source-of-truth-paper-draft-r4.md"
source_pdf: "specification-surface-source-of-truth-paper-draft-r4.pdf"
source_arxiv_readiness_review: "specification-surface-source-of-truth-arxiv-readiness-review-r1.md"
source_arxiv_tex: "arxiv-source-r4/spec_surface_r4_arxiv.tex"
source_venue_matrix: "specification-surface-source-of-truth-venue-conflict-matrix-r1.md"
source_submission_attempt: "specification-surface-source-of-truth-arxiv-submission-attempt-r1.md"
external_posting_allowed: false
verified_online: "2026-05-05"
---

# arXiv Checklist

## Official Sources

- Submission guidelines: <https://info.arxiv.org/help/submit/index.html>
- Content type policy: <https://info.arxiv.org/help/policies/content-types.html>
- License policy: <https://info.arxiv.org/help/license/index.html>
- Moderation policy: <https://info.arxiv.org/help/moderation/index.html>
- Category taxonomy: <https://arxiv.org/category_taxonomy>

## Policy Facts

- arXiv is a moderated repository, not peer review.
- arXiv submissions should be topical and refereeable scientific contributions.
- Research articles should be complete final drafts.
- TeX/LaTeX source is preferred for TeX-derived work; PDF is accepted when appropriate.
- New users or new-category submitters may need endorsement.
- Authors must grant arXiv a distribution license and agree to submission policies.
- Do not post a venue-submitted version in a way that violates anonymity or concurrent-submission rules.

## Category Recommendation

- Primary: `cs.SE`
- Cross-list: `cs.AI` only if the final manuscript foregrounds AI agents and agent systems enough to justify it.

Do not choose `cs.PL`, `cs.SY`, or `eess.SY` unless the manuscript actually develops a programming-language, formal-semantics, or control-systems contribution.

## Current Local Status

| Requirement | Status | Notes |
| :--- | :--- | :--- |
| Complete manuscript | ready | R4 Markdown draft and local PDF exist, with arXiv-specific framing and no AIware acceptance claim. |
| References | present | `references.bib` exists and was used in the local PDF render. |
| Figures/tables | ready | Tables and text diagram render in the R4 PDF; table-heavy pages were visually checked. |
| Artifact statement | adequate but weak | R4 truthfully states that no separate public supplemental bundle exists yet. |
| AI/tool-use disclosure | present | R4 includes an AI/tool-use disclosure. |
| Post-draft readiness review | done | `specification-surface-source-of-truth-arxiv-readiness-review-r1.md` marks the packet ready for a human posting decision. |
| Venue conflict matrix | present | `specification-surface-source-of-truth-venue-conflict-matrix-r1.md` separates arXiv compatibility from future peer-review risk. |
| PDF | present | `specification-surface-source-of-truth-paper-draft-r4.pdf` exists as a local preview PDF. |
| TeX source | present | `arxiv-source-r4/spec_surface_r4_arxiv.tex` exists and is the preferred arXiv upload source. |
| License choice | selected for attempt | arXiv.org perpetual, non-exclusive license was selected during the blocked attempt. |
| Endorsement/account status | blocked | arXiv reports the account is not endorsed for `cs.SE`; endorsement email/code was sent to the registered address. |
| Venue preprint policy | checked for known routes | AIware compatibility is low risk; future ICSE/NIER-like strategy still carries double-anonymous risk. |
| Human posting approval | granted for attempt | The user instructed the browser flow to continue all the way; arXiv blocked before upload. |

## Posting Blockers

- `cs.SE` endorsement is missing.
- Posting without a public artifact snapshot is strategically acceptable only if the author accepts the credibility tradeoff.
- Future double-anonymous venue strategy remains weaker after public posting.

## Decision

Current decision: `blocked_by_endorsement`

R4 is the prepared preprint packet. arXiv posting cannot continue until the author gets `cs.SE` endorsement.
