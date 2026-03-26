# Implementer Lens

## Thesis

The framework concept is ahead of its implementation support. The record model is coherent, but the package still lacks the practical tooling and capture rules that would make repeated use cheap.

## What Worked

- `Q1:` The framework handles runs best when the underlying system already emits usable artifacts: diffs, tests, grep output, status checks, or browser state evidence. The coding and package-refactor proofs are strong precisely because the underlying data surface is concrete. Evidence: [`../../examples/proofs/coding-real-run/README.md`](../../examples/proofs/coding-real-run/README.md), [`../../examples/proofs/march-26-compact-public-package/README.md`](../../examples/proofs/march-26-compact-public-package/README.md).
- `Q3:` The template/evaluation core is already aligned enough to build on. The six direct templates map cleanly to the run-review checklist, and the proofs reuse that shape well. Evidence: [`../../templates/README.md`](../../templates/README.md), [`../../evaluation/README.md`](../../evaluation/README.md).
- `Q5:` The emitted-versus-reconstructed distinction in `USE_IT.md` is one of the framework's most implementation-useful ideas. It prevents the framework from requiring live prose generation for everything. Evidence: [`../../USE_IT.md`](../../USE_IT.md).

## What Failed

- `Q2:` The framework becomes hard to implement on runs where provenance, handoffs, or long horizons are weakly instrumented. The synthetic memory-heavy, long-horizon, and multi-agent cases all expose this. Evidence: [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md).
- `Q4:` The current proof process is too manual. It requires human slicing, source-manifest creation, curated excerpts, changed-file summaries, and hand-authored records. That is workable for proof packets, not yet for routine deployment.
- `Q6:` The template layer still stops short of the real raw-artifact shape now used in the proof packets. The framework has six direct templates, but not standardized templates for `source-manifest.md`, `session-excerpt.md`, or the other raw-artifact support files that real trace use clearly needs. Evidence: [`../../examples/proofs/march-26-standalone-extraction/raw-artifacts/source-manifest.md`](../../examples/proofs/march-26-standalone-extraction/raw-artifacts/source-manifest.md), [`../../templates/README.md`](../../templates/README.md).

## What Is Missing

- `Q8:` The highest-value missing support is a minimal extraction workflow:
  - run slicer
  - source manifest generator
  - curated excerpt generator
  - changed-files collector
  - verification artifact collector
- `Q9:` Real proof supports the claim that the six-record model can be applied to real traces. It does not yet support the claim that this can be done cheaply or consistently at scale without tooling. Evidence: [`../../examples/proofs/README.md`](../../examples/proofs/README.md), [`../../examples/proofs/real-run-index.md`](../../examples/proofs/real-run-index.md).

## Tuning Needed

- `Q7:` Add implementation guidance that distinguishes:
  - machine-captured raw artifacts
  - human-curated review packet fields
  - optional automation layers
- `Q10:` The highest-value next implementation experiments are:
  - add raw-artifact support templates
  - define minimum machine-captured fields for each record
  - prototype a JSONL-to-proof extraction helper for the current Codex trace shape

## Strongest Evidence

- [`../../USE_IT.md`](../../USE_IT.md)
- [`../../templates/README.md`](../../templates/README.md)
- [`../../examples/proofs/march-26-standalone-extraction/raw-artifacts/source-manifest.md`](../../examples/proofs/march-26-standalone-extraction/raw-artifacts/source-manifest.md)
- [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md)

## Confidence

Overall confidence: `high`

Reason: the gap between conceptual clarity and implementation support is visible across every real proof and reinforced by the synthetic edge cases.

