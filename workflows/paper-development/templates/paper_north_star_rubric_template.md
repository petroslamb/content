---
kind: paper_north_star_rubric
package: "<package>"
workflow: paper_development
status: draft
north_star_bar: fast_feedback_ladder_with_peer_review_quality_floor
approval_model: two_reviewer_docs_only_gate
---

# <Paper Title> North-Star Rubric

## North Star

The paper should become a peer-reviewable `cs.SE` short paper with enough concrete contribution to survive NIER or workshop review as a framework, systematization, and illustrative artifact-analysis paper.

AIware is an optional fast-feedback route only if the audit clears it. arXiv posting waits until a complete manuscript exists.

## Scoring

Score each dimension from 0 to 2.

| Dimension | 0 | 1 | 2 |
| :--- | :--- | :--- | :--- |
| Scholarly contribution | Essay-shaped argument, unclear research contribution. | Plausible contribution but still under-specified or too dependent on prose force. | Crisp contribution with definition, model, taxonomy, method, or artifact analysis. |
| Evidence and literature fit | Literature is thematic or missing. | Literature partially supports the frame but has thin mapping or weak section burden. | Literature map directly supports the contribution, limits, and section burden. |
| Case-study/method spine | No concrete unit of analysis or corpus. | Illustrative case exists but method, corpus, or observations need hardening. | Unit, corpus, coding scheme, observations, and non-claims are explicit. |
| Claim discipline and forbidden-frame avoidance | Uses forbidden framing or overclaims evidence. | Mostly disciplined, with caveats or claim boundaries needing tightening. | Forbidden claims are absent, limits are visible, and claim boundaries govern the draft. |
| Venue/feedback readiness | No realistic route or route treats arXiv as review. | Route is plausible but timing, anonymity, or checklist work remains. | Fast-feedback ladder is explicit and venue constraints are respected. |
| Reviewability and artifact traceability | Reviewers cannot trace claims to surfaces. | Main artifacts exist but links, roles, or authority boundaries need cleanup. | Claims, evidence, case artifacts, and approval decisions are trace-linked and reviewable. |

Maximum score: 12.

## Caps

- Any forbidden framing violation blocks approval.
- No case-study unit or corpus caps the score at 7.
- No literature or evidence map caps the score at 7.
- Treating arXiv as peer review blocks approval.
- ArXiv route approval is blocked without manuscript, references, method, artifact statement, and checklist.

## Gate Decisions

- `approve_aiware_sprint`: score is at least 9; scholarly contribution is 2; claim discipline is 2; case-study/method spine is at least 1; both reviewers approve the same route.
- `approve_peer_review_short_paper`: score is at least 10; scholarly contribution, evidence, method, and claim discipline are all 2; both reviewers approve the same route.
- `hold_for_method_hardening`: route is promising but method or evidence is not strong enough for drafting.
- `park_paper_route`: contribution remains essay-shaped, the paper violates hard caps, or the route no longer justifies continued work.

## Reviewer Roles

- Reviewer A: scholarship, evidence, and method.
- Reviewer B: venue fit, paper shape, and reviewability.

Both reviewers must independently approve the same drafting route before manuscript drafting starts. A split verdict blocks drafting until the audit or method is revised and the approval gate is rerun.
