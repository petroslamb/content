# Stress Tester Lens

## Thesis

The framework holds up well under controlled stress, but the stress cases reveal three real soft spots: partial reconstruction thresholds, multi-agent attribution, and how to score contested but still reviewable runs.

## What Worked

- `Q1:` The framework handles bounded, explicit, and well-instrumented runs best, even under stress. The conflicting-evidence case is a good example: the framework does not collapse just because the evidence and verification disagree. Evidence: [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md).
- `Q3:` It adds value beyond raw traces by making ambiguity inspectable instead of mysterious. That is visible in both the conflicting-evidence case and the long March 26 real proofs, where the packet makes the run boundary and risk legible. Evidence: [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md), [`../../examples/proofs/march-26-compact-public-package/comparison.md`](../../examples/proofs/march-26-compact-public-package/comparison.md).
- `Q5:` The failure taxonomy and six-question model are already coherent enough to expose the right kinds of weakness. The framework is not missing the categories; it is missing calibration inside some categories. Evidence: [`../../evaluation/failure-mode-catalog.md`](../../evaluation/failure-mode-catalog.md), [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md).

## What Failed

- `Q2:` Long-horizon partial reconstruction and multi-agent contamination remain the hardest cases. The framework can surface the problem but not yet give crisp thresholds or responsibility splits. Evidence: [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md).
- `Q4:` The current `Strong` / `Partial` / `Weak` outcomes are too coarse for some edge cases. A run can be reconstructable but still governance-failing, or evidence-rich but responsibility-thin.
- `Q6:` The current docs are a little too smooth about contested cases. The framework is directionally right here, but its scoring vocabulary is thinner than its actual reasoning needs.

## What Is Missing

- `Q8:` Missing support includes:
  - a degraded-trace threshold policy
  - a multi-agent responsibility rubric
  - a way to distinguish contested-but-reviewable from simply thin
- `Q9:` The hardest current criticisms are still mostly supported by synthetic evidence, not real proof. That is acceptable for now, but it should be said plainly. Evidence: [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md), [`../../examples/proofs/real-run-index.md`](../../examples/proofs/real-run-index.md).

## Tuning Needed

- `Q7:` Add sharper evaluation policy for:
  - when partial reconstruction should collapse to weak
  - when governance failure should override otherwise good reconstruction
  - how multi-agent runs should localize responsibility
- `Q10:` The highest-value next experiments are a real multi-agent or handoff-heavy run, and a deliberately degraded real trace where reconstruction loss is measurable rather than synthetic.

## Strongest Evidence

- [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md)
- [`../../evaluation/failure-mode-catalog.md`](../../evaluation/failure-mode-catalog.md)
- [`../../examples/proofs/real-run-index.md`](../../examples/proofs/real-run-index.md)

## Confidence

Overall confidence: `medium-high`

Reason: the main stress findings are highly consistent across the synthetic harness, but they still need more real-run confirmation.

