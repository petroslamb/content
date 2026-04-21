# Claim Scorecard

This scorecard applies [`claim-scoring-rubric.md`](claim-scoring-rubric.md) to the current top claims from [`claim-ledger.md`](claim-ledger.md).

It is a draft gate, not a replacement for the ledger. The ledger owns evidence state. [`contradiction-register.md`](contradiction-register.md) owns tension state. This scorecard owns article-readiness state.

## Scorecard

| Claim ID | Short Claim | Paper Support | Local Proof Support | Validation / Enforcement Hook | Contradiction Handling | Article Role | Total | Label | Contradiction IDs | Next Action |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | :--- | :--- | :--- |
| CSA-C1 | Workflow specs become meaningful source only when coupled to validation gates, policy enforcement, and semantic debugging traces. | 2 | 2 | 2 | 2 | 2 | 10 | article-ready | CSA-001, CSA-002, CSA-003 | Use as the lead frame. Keep validation as the hinge, not a side feature. |
| CSA-C2 | Reviewable-run logs should be traces and semantic debugging surfaces, not the source of truth. | 2 | 2 | 2 | 2 | 2 | 10 | article-ready | CSA-003 | Use in the proof section to separate specification, execution, and trace. |
| CSA-C3 | Markdown workflow files become programming substrate only when paired with runtime binding, validation, policy enforcement, and provenance. | 2 | 2 | 2 | 2 | 2 | 10 | article-ready | CSA-001, CSA-002 | Use as the narrowed version of the opening metaphor. Do not claim passive markdown is executable. |
| CSA-C4 | Skills are code-like workflow units, but raw markdown skills are not portable production substrate. | 2 | 1 | 1 | 1 | 2 | 7 | use with caveat | CSA-004 | Use as a bounded supporting claim. Keep capability binding and selection limits visible. |
| CSA-C5 | The local `spec-diff` experiments are repo-native proof candidates for source-linked drift detection. | 2 | 2 | 2 | 2 | 2 | 10 | article-ready | CSA-005 | Use as the local proof example. Do not promote to a shared root command in this article pass. |
| CSA-C6 | Contradiction state should be part of the semantic-debugging surface for promoted workflow claims. | 1 | 1 | 1 | 2 | 2 | 7 | use with caveat | CSA-006 | Use as the next-step claim, not as the article's public frame or proof centerpiece. |

## Draft Gate

- Claims entering the next draft: CSA-C1, CSA-C2, CSA-C3, CSA-C5.
- Claims entering only with caveat: CSA-C4, CSA-C6.
- Claims parked: imports as compiler feature, package-as-object semantics, repo-wide validator promotion.
- Claims blocked or disputed: none in the current top-claim set.
