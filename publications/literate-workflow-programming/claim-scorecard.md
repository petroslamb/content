# Claim Scorecard

This scorecard applies [`claim-scoring-rubric.md`](claim-scoring-rubric.md) to the current top claims from [`claim-ledger.md`](claim-ledger.md).

It is a draft gate, not a replacement for the ledger. The ledger owns evidence state. [`contradiction-register.md`](contradiction-register.md) owns tension state. This scorecard owns article-readiness state.

## Scorecard

| Claim ID | Short Claim | Paper Support | Local Proof Support | Validation / Enforcement Hook | Contradiction Handling | Article Role | Total | Label | Contradiction IDs | Next Action |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | :--- | :--- | :--- |
| CSA-C1 | Workflow specs become meaningful source only when coupled to validation gates, policy enforcement, and semantic debugging traces. | 2 | 2 | 2 | 2 | 2 | 10 | article-ready | CSA-001, CSA-002, CSA-003 | Use as the lead frame. Keep validation as the hinge, not a side feature. |
| CSA-C2 | Reviewable-run logs should be traces and semantic debugging surfaces, not the source of truth. | 2 | 2 | 2 | 2 | 2 | 10 | article-ready | CSA-003 | Use in the proof section to separate specification, execution record, trace evaluation, and provenance. |
| CSA-C3 | Markdown workflow files become programming substrate only when paired with runtime binding, validation, policy enforcement, and provenance. | 2 | 2 | 2 | 1 | 2 | 9 | article-ready | CSA-001, CSA-002, CSA-007 | Use as the narrowed version of the opening metaphor. Add the task-risk and metric caveat for context files. |
| CSA-C4 | Skills are code-like workflow units, but raw markdown skills are not portable production substrate. | 2 | 1 | 1 | 1 | 2 | 7 | use with caveat | CSA-004, CSA-009 | Use as a bounded supporting claim. Keep capability binding, verification, routing, and selection limits visible. |
| CSA-C5 | The local `spec-diff` experiments are repo-native proof candidates for source-linked drift detection. | 2 | 2 | 2 | 1 | 2 | 9 | article-ready | CSA-005, CSA-008 | Use as the local proof example for source/evidence drift only. Do not generalize to broad conformance proof. |
| CSA-C6 | Claim-level provenance and contradiction state should be part of the semantic-debugging surface for promoted workflow claims. | 2 | 1 | 1 | 2 | 2 | 8 | article-ready | CSA-006, CSA-008 | Use as the next-provenance-layer claim. Say the package has contradiction state, but not yet full claim-evidence graphs. |
| CSA-C7 | Validation should be treated as lifecycle infrastructure, not as a one-time gate. | 2 | 1 | 2 | 2 | 2 | 9 | article-ready | CSA-008 | Use to explain why validation is the hinge of the article rather than a trailing implementation detail. |

## Draft Gate

- Claims entering the next draft: CSA-C1, CSA-C2, CSA-C3, CSA-C5, CSA-C6, CSA-C7.
- Claims entering only with caveat: CSA-C4.
- Claims parked: imports as compiler feature, package-as-object semantics, repo-wide validator promotion.
- Claims blocked or disputed: none in the current top-claim set.
