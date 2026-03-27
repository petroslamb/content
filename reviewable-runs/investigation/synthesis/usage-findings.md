# Usage Findings

This file is the evidence-and-critique backing for `PLAYBOOK.md`, not the main operator guide. It records the practical usage findings that the canonical playbook now compresses into direct operating rules.

## Findings

### 1. Best-fit unit: one bounded run, not one whole session

`Evidence base: mixed`  
`Confidence: high`

Reviewable Runs should be applied to one bounded run with one meaningful stop or approval boundary. Long sessions must be sliced first. The March 26 mega-session only became strong evidence after it was split into `f3c1241` and `e581b07` sub-runs, and the synthetic long-horizon case confirms why this matters.

Evidence:
- [`../../examples/proofs/real-run-index.md`](../../examples/proofs/real-run-index.md)
- [`../../examples/proofs/march-26-standalone-extraction/README.md`](../../examples/proofs/march-26-standalone-extraction/README.md)
- [`../../examples/proofs/march-26-compact-public-package/README.md`](../../examples/proofs/march-26-compact-public-package/README.md)
- [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md)

### 2. Best-fit run types are bounded, artifact-rich, and review-sensitive

`Evidence base: real proof`  
`Confidence: high`

The framework is strongest on runs like coding fixes, repo/package refactors, browser pre-submit flows, and other tasks where task boundary, evidence, checks, and approval boundary are concrete.

Evidence:
- [`../../examples/proofs/coding-real-run/README.md`](../../examples/proofs/coding-real-run/README.md)
- [`../../examples/proofs/march-26-standalone-extraction/README.md`](../../examples/proofs/march-26-standalone-extraction/README.md)
- [`../../examples/proofs/march-26-compact-public-package/README.md`](../../examples/proofs/march-26-compact-public-package/README.md)

### 3. Raw traces should be preserved, but not reviewed directly as the final surface

`Evidence base: real proof`  
`Confidence: high`

The framework works best when it preserves raw trace and then adds a lighter review surface on top. Every current real proof shows that the packet is useful not because the trace lacks facts, but because it reduces reviewer guesswork around boundary, evidence, approval, and residual risk.

Evidence:
- [`../../examples/proofs/coding-real-run/comparison.md`](../../examples/proofs/coding-real-run/comparison.md)
- [`../../examples/proofs/march-07-origin-refactor/comparison.md`](../../examples/proofs/march-07-origin-refactor/comparison.md)
- [`../../examples/proofs/march-26-standalone-extraction/comparison.md`](../../examples/proofs/march-26-standalone-extraction/comparison.md)

### 4. Full packets are worth it only for medium- and high-signal runs

`Evidence base: mixed`  
`Confidence: high`

The framework should stay selective. The real-run index rejects or downgrades low-signal review-only traces, while the synthetic lab shows the strongest value where evidence, verification, or approval quality actually matters.

Evidence:
- [`../../examples/proofs/real-run-index.md`](../../examples/proofs/real-run-index.md)
- [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md)
- [`../../PLAYBOOK.md`](../../PLAYBOOK.md)

### 5. Commit, handoff, and explicit non-approval reasons are all valid stop boundaries

`Evidence base: mixed`  
`Confidence: medium-high`

The March 7 proof shows that a handoff can be a credible governance boundary. The coding proof shows a held-before-merge boundary. The synthetic support-triage case shows that explicit “approval not required” logic also works when risk stays internal.

Evidence:
- [`../../examples/proofs/march-07-origin-refactor/README.md`](../../examples/proofs/march-07-origin-refactor/README.md)
- [`../../examples/proofs/coding-real-run/review-packet/approval-decision.md`](../../examples/proofs/coding-real-run/review-packet/approval-decision.md)
- [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md)

### 6. External-action runs need live state verification, not just local success signals

`Evidence base: mixed`  
`Confidence: high`

The new YouTube evidence shows that verification changes meaning once the run acts on a third-party platform. In these cases, local script execution and repo artifacts are only supporting evidence. The decisive check is live state confirmation on the platform itself.

Evidence:
- [`../../examples/proofs/march-27-youtube-playlist-order-fix/README.md`](../../examples/proofs/march-27-youtube-playlist-order-fix/README.md)
- [`../../examples/proofs/march-27-youtube-playlist-order-fix/raw-artifacts/verification-output.txt`](../../examples/proofs/march-27-youtube-playlist-order-fix/raw-artifacts/verification-output.txt)
- [`../../examples/proofs/real-run-index.md`](../../examples/proofs/real-run-index.md)

### 7. Anti-patterns are already visible

`Evidence base: mixed`  
`Confidence: high`

Do not use the framework as a wrapper around whole conversations, opinion-only review threads, or runs with no preserved evidence basis. Those cases either become weak or force too much reconstruction guesswork.

Evidence:
- [`../../examples/proofs/real-run-index.md`](../../examples/proofs/real-run-index.md)
- [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md)

## Working Usage Model

The current best usage pattern is:

1. preserve the raw trace or raw artifacts
2. identify one bounded run
3. choose the risk tier
4. curate the minimum raw evidence set
5. reconstruct the packet only as far as the review task requires
6. for external-action runs, verify the live platform state explicitly
7. review with the six questions

That model is already supported by the evidence. What it lacks is lighter tooling, not conceptual clarity.
