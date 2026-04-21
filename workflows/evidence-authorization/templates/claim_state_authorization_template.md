# <Package Or Essay> Claim-State Authorization

## Purpose

This packet applies the optional Claim-State Authorization mode of the `evidence_authorization` workflow.

The normal ledger asks what claims the evidence authorizes. This variant asks what each top claim's current state is across evidence, contradiction, validation, and draft readiness.

Use this only when the package already has researched claims plus real tensions between papers, local proof, repo practice, and article framing. It is an extension of evidence authorization, not a new workflow.

## Surfaces

| Surface | Path | Job |
| :--- | :--- | :--- |
| Claim ledger | `<claim-ledger path>` | Evidence-state surface. Records researched claims, source support, caveats, parked claims, and safe wording. |
| Contradiction register | `<contradiction-register path>` | Tension-state surface. Records curated contradictions or frame conflicts with an authority rule and draft instruction. |
| Scoring rubric | `<claim-scoring-rubric path>` | Readiness-state rule. Defines how claims are scored before entering the article body. |
| Claim scorecard | `<claim-scorecard path>` | Draft-gate surface. Applies the rubric to current top claims and names next actions. |

## Claim-State Map

| Claim ID | Ledger Status | Contradiction IDs | Contradiction Status | Rubric Label | Draft Permission |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `<supported / synthesis / parked / blocked>` | `<CSA-001>` | `<resolved / open / parked / blocked>` | `<article-ready / use with caveat / parked / blocked or disputed>` | `<body / caveated body / footnote / park / cut>` |

## Working Decision

State the package-level drafting gate in one paragraph.

Example:

Claims may enter the article body only when they have a ledger status, contradiction status, and rubric status. Article-ready claims can carry section burden. Use-with-caveat claims can appear only with their caveat visible. Parked and blocked claims stay out of the draft.

## Boundary

This variant scores article and proof readiness. It does not score prose quality. It does not promote local validators, lifecycle stages, or repo-wide policy unless a separate workflow decision authorizes that change.

## Next Draft Gate

- Claims entering the body: `<claim IDs>`
- Claims usable only with caveat: `<claim IDs>`
- Claims parked: `<claim IDs>`
- Claims blocked or disputed: `<claim IDs>`
