# Claim Scoring Rubric

This rubric applies the Claim-State Authorization variant to this package.

It scores article and proof readiness for claims in [`claim-ledger.md`](claim-ledger.md). It does not score prose quality, and it should not promote a speculative claim merely because the idea is interesting.

## Dimensions

Score each dimension from 0 to 2.

| Dimension | 0 | 1 | 2 |
| :--- | :--- | :--- | :--- |
| Paper support | No direct paper support, or only thematic adjacency. | Partial, analogical, or synthesis support from identified sources. | Direct or strong hinge support from identified sources. |
| Local proof support | No local proof, validator, trace, or package example. | Partial local proof, one package example, or unretained proof candidate. | Repeated or retained local proof with clear artifact paths. |
| Validation/enforcement hook | No visible validation, policy, runtime, or enforcement mechanism. | Proposed or partial hook, but not yet exercised. | Exercised validator, policy check, runtime gate, or enforcement artifact. |
| Contradiction handling | Known contradiction is unresolved, ignored, or likely to mislead. | Tension is named but still open or caveated. | Tension is resolved, parked outside scope, or governed by a clear authority rule. |
| Article role | No clear article job, or the claim distracts from the thesis. | Useful supporting role, but not load-bearing. | Clear load-bearing role in the article frame, section spine, or proof argument. |

## Labels

| Total | Label | Draft Permission |
| :--- | :--- | :--- |
| `8-10` | article-ready | May carry body or section burden with caveat visible when needed. |
| `5-7` | use with caveat | May appear only with scope limits, proof limits, or contradiction state visible. |
| `3-4` | parked | Keep out of the article body until evidence, proof, or framing improves. |
| `0-2` | blocked or disputed | Do not use except as an explicit open question or rejected path. |

## Caps

- An unresolved blocking contradiction caps the total at 4.
- A claim with no identified paper support caps the total at 4 unless it is explicitly labeled as local practice rather than research claim.
- A proof-dependent claim with no local proof support caps the total at 7.
- A validation-dependent claim with no validation or enforcement hook caps the total at 7.
- A parked article role caps the total at 4 even when the evidence is interesting.

## Package-Specific Reading

- `article-ready` means the claim can enter the essay body with its caveat visible.
- `use with caveat` means the claim may appear only when its proof limit, scope limit, or unresolved tension is explicit.
- `parked` means the claim may stay in research notes, implementation plans, or future proof memos, but not in the article body.
- `blocked or disputed` means the claim should appear only as a known rejected path or open question.
