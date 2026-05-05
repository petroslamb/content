---
kind: venue_conflict_matrix
package: "literate-workflow-programming/specification-surface-source-of-truth"
revision: 1
status: active_decision_support
created: "2026-05-05"
workflow: paper_development
source_submission_record: "specification-surface-source-of-truth-aiware-submission-record-r1.md"
source_draft: "specification-surface-source-of-truth-paper-draft-r4.md"
current_packet: aiware_submitted_r3_plus_arxiv_ready_r4
arxiv_posting_allowed: false
recommended_preprint_decision: ready_for_human_posting_decision
---

# Venue Conflict Matrix R1

## Current State

R3 was submitted to the AIware 2026 ArXiv Track on 2026-05-05. R4 is now prepared as an arXiv-facing preprint packet. The strategic question is whether to post it publicly now for timestamping and fast feedback.

The answer is not a simple no. AIware's ArXiv Track explicitly accepts manuscripts that are not yet on arXiv and says accepted works should be made available on arXiv before the conference date. It is also non-proceedings. The main risk is arXiv CS moderation, not AIware conflict.

Current recommendation: `ready_for_human_posting_decision`.

That means: do not post R3. Use R4 if posting. Before clicking submit, choose license, confirm account/endorsement status, and explicitly approve public posting.

## Official Source Notes

- AIware 2026 ArXiv Track: <https://conf.researchr.org/track/aiware-2026/aiware-2026-arxiv-track>
- arXiv moderation policy: <https://info.arxiv.org/help/moderation/index.html>
- arXiv content types: <https://info.arxiv.org/help/policies/content-types.html>
- arXiv CS review/position practice update: <https://blog.arxiv.org/2025/10/31/attention-authors-updated-practice-for-review-articles-and-position-papers-in-arxiv-cs-category/>
- arXiv category taxonomy: <https://arxiv.org/category_taxonomy>
- ICSE 2027 Research Track: <https://conf.researchr.org/track/icse-2027/icse-2027-research-track>
- ICSE 2026 NIER reference page: <https://conf.researchr.org/track/icse-2026/icse-2026-nier>

## Conflict Matrix

| Route | Archival / proceedings? | Preprint allowed? | Concurrent-review risk | Anonymity risk | Artifact expectation | Current verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| AIware 2026 ArXiv Track | Non-proceedings. Accepted submissions do not appear in proceedings. | Yes. Track says work need not be on arXiv at submission time, but should be on arXiv before the conference date if accepted. | Low with arXiv. The track is built around arXiv papers. | Low. AIware ArXiv Track says submissions need not be anonymized. | Supplemental materials are encouraged and treated as positive, but no explicit policy requires them. | Already submitted with R3 PDF. No conflict with later arXiv posting appears from AIware policy. |
| arXiv `cs.SE` preprint | Moderated repository, not peer review. Permanent public scholarly record after announcement. | Applicable route if the paper is a complete research article. | Not a peer-review venue, but public posting can affect later venue strategy. | Medium for later double-anonymous review; some venues allow preprints but recommend postponing. | Public artifact bundle not required by arXiv, but stronger for credibility. | R4 is ready for human posting decision; still blocked on license/account/public-posting approval. |
| arXiv `cs.AI` cross-list | Same as arXiv. | Possible only if AI-agent substance is strong enough. | Same as arXiv. | Same as arXiv. | Same as arXiv. | Optional cross-list only if final arXiv version foregrounds agent systems enough. Primary should remain `cs.SE`. |
| ICSE 2027 Research Track | Archival peer-reviewed conference track. | Authors have the right to upload preprints, but the track recommends postponing arXiv or similar posting until after notification for double-anonymous reviewing. | High during ICSE review: paper must not be under review elsewhere while under ICSE consideration. | Medium-high. Double-anonymous; do not state the work is submitted to ICSE on arXiv. | Open science expected by default; artifacts should be available to reviewers or non-sharing justified. | Do not submit concurrently. A public arXiv version is allowed but strategically weaker for double-anonymous ICSE review. |
| Future ICSE NIER / NIER-like route | Usually archival or proceedings-bearing when accepted; exact 2027 policy not yet used here. | Must check the specific CFP. ICSE 2026 NIER used double-anonymous review and accepted public preprint links in the program after acceptance, but that does not by itself authorize a future submission plan. | Must check when CFP opens. Do not assume concurrent submission is allowed. | Likely medium-high because NIER commonly uses double-anonymous review. | Likely expects a credible future-work plan and may expect artifacts or explanation. | Candidate route only after AIware notification or withdrawal/decision. |
| Journal route | Depends on journal. | Many journals allow preprints, but policy must be checked per journal. | Usually cannot be simultaneously under peer review elsewhere. | Usually low unless the journal uses double-anonymous review. | Depends on journal; artifact statement increasingly expected. | Possible later, but not a spray-submit target. |
| Another workshop / OpenReview-hosted venue | Depends entirely on the venue. OpenReview is infrastructure, not acceptance. | Must check venue CFP. | Unknown until CFP says whether simultaneous or prior submissions are allowed. | Unknown. | Unknown. | Do not submit without a venue-specific policy check. |

## Reasons To Post The Preprint Now

1. Public timestamp. arXiv establishes a visible version and date for the idea.
2. Fast feedback. The paper can be read, criticized, and improved before a slower peer-review cycle.
3. AIware alignment. The AIware ArXiv Track is explicitly built around high-quality arXiv papers and says accepted works should be available on arXiv before the conference date.
4. Distribution. A public arXiv link is more legible to researchers than a Substack essay or local PDF.
5. Versioning. Later revisions can be posted as arXiv versions if the paper improves.

## Reasons Against Posting Now

1. arXiv CS moderation risk. arXiv CS now treats review/survey articles and position papers much more strictly unless they have completed peer review. R4 reduces this risk by emphasizing definition, taxonomy, lifecycle, literature systematization, and artifact analysis, but the risk is not zero.
2. Permanent public record. Once announced, arXiv generally treats the paper as part of the permanent scholarly record. A weak version can be revised but not quietly erased.
3. Future double-anonymous pressure. ICSE 2027 says authors have the right to upload preprints, but recommends postponing arXiv or similar posting until after notification to support double-anonymous review.
4. Artifact weakness. R4 truthfully says there is no separate public supplemental bundle. That is acceptable for fail-fast distribution, but a public arXiv version would look stronger with a public or anonymized artifact snapshot.
5. Version maturity. R4 has a rendered PDF and generated TeX source, but it has not benefited from post-AIware reviewer feedback.
6. No post-AIware feedback yet. Waiting until June 1, 2026 may produce useful acceptance/rejection signal before the version becomes public.

## Decision Rule

Post now only if the strategic value of public timestamp and fast feedback is worth the arXiv moderation and future-review risks.

Minimum `go_now` packet:

- arXiv-ready R4 draft, not raw R3;
- title and abstract frame the contribution as research/framework + artifact analysis, not opinion or survey;
- full rendered references;
- explicit AI/tool-use disclosure;
- category recommendation: primary `cs.SE`; optional `cs.AI` only if justified;
- license choice;
- arXiv account and endorsement status checked;
- no claim of AIware acceptance;
- optional but strongly preferred: public or anonymized artifact snapshot.

Default `wait` packet:

- keep AIware submission as the current fast-feedback route;
- wait for June 1, 2026 notification;
- if accepted, prepare arXiv with AIware context and artifact snapshot;
- if rejected, revise before public posting.

## Current Recommendation

Do not post R3. If the strategic goal is "get it out there and fail fast," use R4 and post only after the author selects a license, confirms account/endorsement status, and accepts the future-review tradeoff.
