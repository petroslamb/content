---
kind: paper_north_star_rubric
package: proof-runs-as-source-surface
workflow: paper_development
status: active_experiment
north_star_bar: fast_feedback_ladder_with_peer_review_quality_floor
approval_model: two_reviewer_docs_only_gate
promotion_claim: false
---

# Proof Runs As Source Surface North-Star Rubric

## North Star

The paper should become a peer-reviewable `cs.SE` short paper with a concrete
framework and systematization contribution: proof runs as source surfaces for
governed content-agent work.

AIware can be used as a fast-feedback route only if the draftability audit clears
it. ICSE NIER or a software-engineering workshop is the peer-review target.
arXiv posting waits until a complete manuscript, references, method note,
artifact statement, and venue checklist exist.

## Scoring

Score each dimension from 0 to 2.

| Dimension | 0 | 1 | 2 |
| :--- | :--- | :--- | :--- |
| Scholarly contribution | Essay-shaped argument about trust in agents. | Plausible framework but definitions, model, or evaluation burden remain thin. | Crisp definition, lifecycle model, systematization, or artifact-analysis method. |
| Evidence and literature fit | Sources are thematic or only justify motivation. | Evidence partially maps to runtime trust, benchmarks, specs, and context surfaces. | Literature map directly supports contribution, limits, and section burden. |
| Case-study/method spine | No concrete unit of analysis or corpus. | Reviewable Runs artifacts are named but coding scheme or observations need hardening. | Unit, corpus, coding scheme, observations, and non-claims are explicit. |
| Claim discipline and forbidden-frame avoidance | Claims agents can safely publish themselves or benchmark scores prove autonomy. | Claims are mostly bounded but need tighter non-claims. | Forbidden claims are absent and paper claims stay tied to governed evidence. |
| Venue/feedback readiness | No realistic route or route treats arXiv as review. | Fast-feedback and peer-review routes are plausible but checklist work remains. | Route respects feedback ladder, anonymity, preprint timing, and artifact expectations. |
| Reviewability and artifact traceability | Reviewers cannot trace claims to run artifacts or package surfaces. | Main artifacts exist but links, roles, or authority boundaries need cleanup. | Claims, evidence, case artifacts, and approval decisions are trace-linked. |

Maximum score: 12.

## Caps

- Any forbidden framing violation blocks approval.
- No case-study unit or artifact corpus caps the score at 7.
- No literature or evidence map caps the score at 7.
- Treating arXiv as peer review blocks approval.
- arXiv route approval is blocked without manuscript, references, method,
  artifact statement, and checklist.

## Gate Decisions

- `approve_aiware_sprint`: score is at least 9; scholarly contribution is 2;
  claim discipline is 2; case-study/method spine is at least 1; both reviewers
  approve the same route.
- `approve_peer_review_short_paper`: score is at least 10; scholarly
  contribution, evidence, method, and claim discipline are all 2; both reviewers
  approve the same route.
- `hold_for_method_hardening`: route is promising but method or evidence is not
  strong enough for manuscript drafting.
- `park_paper_route`: contribution remains essay-shaped, the paper violates hard
  caps, or the route no longer justifies continued work.

## Reviewer Roles

- Reviewer A: scholarship, evidence, and method.
- Reviewer B: venue fit, paper shape, and reviewability.

Both reviewers must independently approve the same drafting route before
manuscript drafting starts. A split verdict blocks drafting until the audit or
method is revised and the approval gate is rerun.

## Forbidden Claims

- Do not claim benchmark scores prove autonomous publication trust.
- Do not claim agents can publish themselves safely.
- Do not collapse the academic paper route into the live essay route.
- Do not treat retained proof evidence as workflow promotion.
