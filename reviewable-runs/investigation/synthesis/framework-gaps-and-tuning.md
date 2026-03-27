# Framework Gaps And Tuning

This file answers the practical question: what must change in the framework itself after the first real-proof and synthetic pass.

## Findings

### 1. Run slicing needs to become first-class doctrine

`Evidence base: mixed`  
`Confidence: high`

The framework currently implies slicing, but the real proofs show it is foundational. A run must be bounded before risk tiering, packet assembly, or review can work cleanly.

Evidence:
- [`../../examples/proofs/real-run-index.md`](../../examples/proofs/real-run-index.md)
- [`../../examples/proofs/march-26-standalone-extraction/README.md`](../../examples/proofs/march-26-standalone-extraction/README.md)
- [`../../USE_IT.md`](../../USE_IT.md)

Tuning:
- add explicit slicing rules to operator guidance
- define acceptable stop-boundary types
- treat “whole session” as a default anti-pattern

### 2. Partial reconstruction thresholds are too soft

`Evidence base: synthetic`  
`Confidence: high`

The synthetic harness shows that the framework knows when degraded traces are risky, but it still lacks a crisp line between “partial but usable” and “effectively weak.”

Evidence:
- [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md)

Tuning:
- define when missing early trace, evidence loss, or missing checks should force a weak judgment
- separate reconstruction quality from governance quality when necessary

### 3. Multi-agent attribution is underdeveloped

`Evidence base: synthetic`  
`Confidence: medium`

The framework can expose contaminated handoffs, but it cannot yet say enough about who owns the failure and where the control should live.

Evidence:
- [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md)
- [`../../evaluation/failure-mode-catalog.md`](../../evaluation/failure-mode-catalog.md)

Tuning:
- add a handoff responsibility rubric
- define upstream/downstream blame language
- consider whether multi-agent runs need one extra supporting record without changing the six-question core

### 4. The raw-artifact layer is now real, but not yet templated

`Evidence base: real proof`  
`Confidence: high`

The proof packets rely on `source-manifest.md`, `session-excerpt.md`, `changed-files.txt`, `verification-output.txt`, and `commit-record.txt`, but the template layer still stops at the six canonical records.

Evidence:
- [`../../examples/proofs/march-26-standalone-extraction/raw-artifacts/source-manifest.md`](../../examples/proofs/march-26-standalone-extraction/raw-artifacts/source-manifest.md)
- [`../../examples/proofs/march-26-compact-public-package/raw-artifacts/session-excerpt.md`](../../examples/proofs/march-26-compact-public-package/raw-artifacts/session-excerpt.md)
- [`../../templates/README.md`](../../templates/README.md)

Tuning:
- add a small raw-artifact template set
- define minimum machine-captured fields for real-trace proofs

### 5. Governance timing is stronger than governance taxonomy

`Evidence base: mixed`  
`Confidence: medium-high`

The framework already catches late or implied approval well, but it still needs a sharper taxonomy for handoff, commit, merge, release, publish, submit, and external action boundaries.

Evidence:
- [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md)
- [`../../examples/proofs/march-07-origin-refactor/review-packet/approval-decision.md`](../../examples/proofs/march-07-origin-refactor/review-packet/approval-decision.md)
- [`../../examples/proofs/coding-real-run/review-packet/approval-decision.md`](../../examples/proofs/coding-real-run/review-packet/approval-decision.md)

Tuning:
- make control-boundary type explicit in governance records
- distinguish “approved to stop” from “approved to act externally”

### 6. The scoring model is a little too coarse

`Evidence base: synthetic`  
`Confidence: medium`

`Strong` / `Partial` / `Weak` works for first-pass separation, but some cases are reconstructable yet governance-failing, or evidence-rich yet attribution-thin. The framework likely needs a sharper internal rubric before it needs a bigger public taxonomy.

Evidence:
- [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md)

Tuning:
- keep the public labels for now
- add internal calibration notes for contested, degraded, and governance-failing cases

### 7. The framework is more proven than the README says, but still not broadly proven

`Evidence base: mixed`  
`Confidence: medium`

The current package now has multiple real proofs, not just one. But they still cluster around coding and documentation-heavy work, so the framework should become more accurate, not more grand.

Evidence:
- [`../../README.md`](../../README.md)
- [`../../examples/proofs/README.md`](../../examples/proofs/README.md)
- [`../../examples/proofs/real-run-index.md`](../../examples/proofs/real-run-index.md)

Tuning:
- update maturity language after this investigation
- keep the package honest about domain spread and manual overhead

### 8. External-action boundary taxonomy needs to be sharper than commit-centric governance

`Evidence base: mixed`  
`Confidence: high`

The YouTube playlist-order fix shows that some of the strongest real runs do not end at commits, merges, or releases. They end at a third-party platform state change that must be treated as an operational approval boundary in its own right.

Evidence:
- [`../../examples/proofs/march-27-youtube-playlist-order-fix/README.md`](../../examples/proofs/march-27-youtube-playlist-order-fix/README.md)
- [`../../examples/proofs/march-27-youtube-playlist-order-fix/raw-artifacts/boundary-record.md`](../../examples/proofs/march-27-youtube-playlist-order-fix/raw-artifacts/boundary-record.md)
- [`../../examples/proofs/real-run-index.md`](../../examples/proofs/real-run-index.md)

Tuning:
- sharpen the boundary taxonomy for external platform actions
- distinguish local artifact creation from the real operational stop boundary
- make live third-party verification a first-class expectation for these runs

### 9. API-insufficiency plus UI workaround is a real run type

`Evidence base: real proof`  
`Confidence: medium-high`

The framework now has evidence for a meaningful run shape where API inspection identifies the problem, a UI step unlocks control, and the API then performs the durable state update. That mixed-control pattern should be handled explicitly rather than treated as an awkward exception.

Evidence:
- [`../../examples/proofs/march-27-youtube-playlist-order-fix/review-packet/execution-trace.md`](../../examples/proofs/march-27-youtube-playlist-order-fix/review-packet/execution-trace.md)
- [`../../examples/proofs/march-27-youtube-playlist-order-fix/review-packet/failure-review.md`](../../examples/proofs/march-27-youtube-playlist-order-fix/review-packet/failure-review.md)

Tuning:
- note mixed API/UI control as a supported run shape
- require the packet to record why the API-only path was insufficient
- avoid collapsing browser intervention and API action into one vague “automation” label
