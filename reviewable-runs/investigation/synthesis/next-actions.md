# Next Actions

This file ranks the next framework actions by value and dependency.

## Priority Actions

### 1. Add slicing and boundary policy to the doctrine

`Evidence base: mixed`  
`Confidence: high`

Why first: almost every other improvement assumes the run unit is already clean.

Deliverable:
- update operator guidance so slicing is explicit
- define accepted stop-boundary types
- add “do not review whole sessions by default” as a clear anti-pattern

Evidence:
- [`../../examples/proofs/real-run-index.md`](../../examples/proofs/real-run-index.md)
- [`usage-findings.md`](usage-findings.md)

### 2. Add raw-artifact support templates

`Evidence base: real proof`  
`Confidence: high`

Why second: the proof packets already rely on a repeatable raw-artifact layer that the template surface does not yet acknowledge.

Deliverable:
- template for source manifest
- template for curated session excerpt
- template for changed-files summary
- template for verification-output summary
- template for commit or handoff record

Evidence:
- [`../../examples/proofs/march-26-standalone-extraction/raw-artifacts/source-manifest.md`](../../examples/proofs/march-26-standalone-extraction/raw-artifacts/source-manifest.md)
- [`framework-gaps-and-tuning.md`](framework-gaps-and-tuning.md)

### 3. Prototype a lightweight real-trace extraction helper

`Evidence base: real proof`  
`Confidence: medium-high`

Why third: it attacks the biggest manual-cost problem directly.

Deliverable:
- one helper that takes a raw Codex JSONL slice and produces a starter artifact bundle for proof work
- no scoring, only structured extraction support

Evidence:
- [`../../examples/proofs/march-26-compact-public-package/raw-artifacts/session-excerpt.md`](../../examples/proofs/march-26-compact-public-package/raw-artifacts/session-excerpt.md)
- [`../../examples/proofs/march-26-standalone-extraction/raw-artifacts/source-manifest.md`](../../examples/proofs/march-26-standalone-extraction/raw-artifacts/source-manifest.md)

### 4. Tune evaluation for degraded and contested cases

`Evidence base: synthetic`  
`Confidence: high`

Why fourth: the validation harness already tells us where the scoring is soft.

Deliverable:
- degraded-trace threshold notes
- multi-agent responsibility notes
- governance-failure override notes for otherwise reconstructable runs

Evidence:
- [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md)
- [`framework-gaps-and-tuning.md`](framework-gaps-and-tuning.md)

### 5. Add one real browser proof and one real retrieval-heavy proof

`Evidence base: mixed`  
`Confidence: medium-high`

Why fifth: this is the highest-value empirical broadening step after tooling and calibration basics.

Deliverable:
- one browser pre-submit or held-submit proof packet
- one memo or retrieval-heavy governed-output proof packet

Evidence:
- [`../../examples/proofs/real-run-index.md`](../../examples/proofs/real-run-index.md)
- [`results-and-judgment.md`](results-and-judgment.md)

### 6. Update package maturity and usage language after the tuning lands

`Evidence base: inference`  
`Confidence: medium`

Why last: doctrine should move after evidence and tooling, not before.

Deliverable:
- revise `README.md`
- revise `PLAYBOOK.md`
- revise `evaluation/README.md`

Evidence:
- [`results-and-judgment.md`](results-and-judgment.md)
- [`framework-gaps-and-tuning.md`](framework-gaps-and-tuning.md)
