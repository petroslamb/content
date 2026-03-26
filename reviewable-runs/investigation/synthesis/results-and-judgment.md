# Results And Judgment

This file gives the blunt overall judgment from the first investigation pass.

## Findings

### 1. The framework's core claim is supported

`Evidence base: mixed`  
`Confidence: high`

The current evidence supports the claim that raw traces are often too thin for serious review, and that a structured review surface makes important runs easier to inspect, defend, and critique.

Evidence:
- [`../../examples/proofs/coding-real-run/comparison.md`](../../examples/proofs/coding-real-run/comparison.md)
- [`../../examples/proofs/march-07-origin-refactor/comparison.md`](../../examples/proofs/march-07-origin-refactor/comparison.md)
- [`../../examples/proofs/march-26-standalone-extraction/comparison.md`](../../examples/proofs/march-26-standalone-extraction/comparison.md)

### 2. The framework is already coherent as a practical operating model

`Evidence base: mixed`  
`Confidence: high`

Between the operator guide, checklist, real proofs, and synthetic harness, Reviewable Runs is no longer just an intuition. It is a working framework with a stable review unit, a stable question model, and visible best-fit domains.

Evidence:
- [`../../USE_IT.md`](../../USE_IT.md)
- [`../../evaluation/run-review-checklist.md`](../../evaluation/run-review-checklist.md)
- [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md)

### 3. The main weakness is calibration and implementation support, not conceptual incoherence

`Evidence base: mixed`  
`Confidence: high`

The framework does not currently fail because the ideas clash. It fails because the current doctrine is still too soft around slicing, degraded traces, multi-agent attribution, and the amount of manual work needed to assemble a packet.

Evidence:
- [`../../examples/proofs/real-run-index.md`](../../examples/proofs/real-run-index.md)
- [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md)
- [`../../templates/README.md`](../../templates/README.md)

### 4. What is real-proofed is still narrower than what is synthetically supported

`Evidence base: mixed`  
`Confidence: high`

The real-proof layer now supports the framework on coding and documentation-heavy runs with clear artifact surfaces. The hardest questions, especially multi-agent responsibility and degraded reconstruction, are still mostly backed by synthetic evidence.

Evidence:
- [`../../examples/proofs/real-run-index.md`](../../examples/proofs/real-run-index.md)
- [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md)

### 5. The framework is good enough to keep and refine, not yet broad enough to overclaim

`Evidence base: inference`  
`Confidence: medium-high`

The right current judgment is:

- keep it
- use it selectively
- refine it with sharper tuning and lighter tooling
- avoid presenting it as broadly settled or low-friction across all run types

Evidence:
- [`../../examples/proofs/README.md`](../../examples/proofs/README.md)
- [`../../examples/proofs/real-run-index.md`](../../examples/proofs/real-run-index.md)
- [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md)

## Bottom Line

Reviewable Runs is now strong enough to stand as a serious framework and weak enough in the right places to need another refinement cycle. That is a good place to be.

It is no longer missing a concept.

It is missing:

- sharper calibration
- lighter implementation support
- broader real-world proof

