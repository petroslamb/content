# Bounded Blueprint: Your AI Is Confidently Wrong

Live draft: `publications/evidence-governance/your-ai-is-confidently-wrong-and/your-ai-is-confidently-wrong-and.md`
Candidate target: `publications/evidence-governance/your-ai-is-confidently-wrong-and/your-ai-is-confidently-wrong-and-candidate-r4.md`

## Goal

Write the strongest essay the current evidence can support without pretending that one project has already established a general cross-domain doctrine.

## Promise

This essay proves a bounded claim: one Ethereum verification project exposed a recurring trust problem in AI-generated analysis. When polished summaries and lower-level artifacts disagree, trust becomes a workflow problem, not a model-personality problem.

## Spine

1. **The Moment of Contradiction**: one run produces a confident summary and contradictory lower-level evidence.
2. **What Counted as Evidence**: explain the evidence hierarchy inside this case and separate the 47 direct-adjudication rows from the broader 81-row scored pack.
3. **What the Runs Actually Showed**: error-profile differences across Haiku, Sonnet, and Opus; obligation ID instability; disputed obligations.
4. **What the Negative Control Taught**: EIP-7702 shows that environment metadata can flip the narrative.
5. **The Rules the Project Forced**: evidence hierarchy, contradiction register, row-level scoring, claim ledger, and phase boundaries as pragmatic controls, not universal law.
6. **What Changed Operationally**: contradictions surfaced, claims downgraded, model selection became a governance decision.
7. **Borders**: state exactly what this case does not prove.
8. **Landing**: the real cost is adjudication discipline.

## Paragraph burden

- **Opening**: show that the contradiction happened inside one system, not in abstract debate.
- **Evidence section**: make the admissibility rules visible before making the case.
- **Runs section**: keep the empirical center on direct-adjudication evidence.
- **Negative control**: use environment-sensitive outcomes to show why metadata matters.
- **Rules section**: present the controls as rules earned from project failure, with literature as supporting context only.
- **Borders**: explicitly deny portability, correctness gains, and doctrine status beyond the current proof boundary.
- **Ending**: land on the human cost of downgrading preferred narratives when the artifacts do not support them.

## Evidence burden

- **Body work**:
  - `companion.md`
  - `docs/evaluations/sample_scored_run.csv` in the external repo
  - `docs/evaluations/contradictions.csv` in the external repo
  - `docs/evaluations/evidence_ledger.md` in the external repo
  - `docs/QUALITATIVE_EVALUATION.md` in the external repo
  - `examples/qualitative_validation_transcript.md` in the external repo
  - the two EIP-7702 workflow summaries in the external repo
- **Support and borders only**:
  - Simhi et al. on confidence divorced from correctness
  - Ji et al. on claim-level verification
  - evidence-based medicine / hierarchy references

## Cut order

1. General doctrine language.
2. Broad cross-domain extrapolation.
3. Most of the historical medicine section if it starts carrying proof burden instead of interpretive burden.
4. Any metric that depends on compare-derived rows unless its caveat is carried inline.

## Failure triggers

- The essay treats the full 81-row pack as if it were all equal-strength evidence.
- The essay uses literature to certify portability instead of using it to explain why the case matters.
- The essay sounds like a product pitch for `eip-verify`.
- The essay hides the difference between direct-adjudication rows and compare-derived proxy rows.
- The essay claims improved correctness instead of improved inspectability, contradiction handling, or adjudication discipline.
