# Analysis

This folder is the single advanced analysis surface for Reviewable Runs.

It combines what used to be split across the old investigation and calibration layers.

## What This Surface Does

Use this layer to answer:

- what the current proof corpus actually covers
- where the framework works well
- where it still feels soft or overfit
- what tuning is justified by evidence
- which missing run categories matter most next

This is not part of the default front-door reading path.

## Folder Map

- `EVIDENCE_MAP.md`: the source-of-truth corpus for the analysis layer
- `REAL_RUN_MATRIX.md`: the structured cross-run comparison table
- `FINDINGS.md`: the merged findings and second-pass judgment
- `TUNING_CANDIDATES.md`: bounded framework changes justified by the evidence
- `COVERAGE_GAPS.md`: the acquisition plan for the next empirical categories
- `NEURAL_ARCHITECTURE_PILOT_REVIEW.md`: commit-sliced review of the April 2026 neural-architecture workflow pilot and what it reveals about framework fit

## How To Read This Folder

Read in this order:

1. `EVIDENCE_MAP.md`
2. `REAL_RUN_MATRIX.md`
3. `FINDINGS.md`
4. `TUNING_CANDIDATES.md`
5. `COVERAGE_GAPS.md`

## Role In The Package

- `examples/` shows the evidence
- `validation-lab/` pressure-tests the framework synthetically
- `analysis/` interprets the current evidence systematically
- `PLAYBOOK.md` is the operator guide that follows from that analysis
