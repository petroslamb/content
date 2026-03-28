# Calibration

This folder is the advanced empirical calibration layer for Reviewable Runs.

It treats the current real-run corpus as a structured dataset rather than a loose collection of proof packets.

## What This Surface Does

Use this layer to answer:

- which run classes the framework already handles well
- which boundary and verification modes are now calibrated
- where the framework still feels soft or overfit
- which tuning candidates are justified by real evidence
- which missing run categories matter most next

This is analysis first. It does not directly rewrite doctrine, checklists, or templates.

## Folder Map

- `REAL_RUN_MATRIX.md`: the source-of-truth calibration dataset across all indexed real runs
- `SECOND_PASS_RESULTS.md`: the recalibrated second-pass review of the current corpus
- `CALIBRATION_NOTES.md`: concise matrix-backed findings
- `TUNING_CANDIDATES.md`: bounded framework changes suggested by the evidence
- `COVERAGE_GAPS.md`: the next empirical categories to acquire

## How This Differs From Investigation

- `../investigation/` is the interpretation and critique layer
- `calibration/` is the dataset-backed cross-run analysis layer

Use `investigation/` when you want broader synthesis and critique.
Use `calibration/` when you want a more operational comparison of run classes, boundaries, verification modes, and packet weights.

## Reading Order

Read in this order:

1. `REAL_RUN_MATRIX.md`
2. `SECOND_PASS_RESULTS.md`
3. `CALIBRATION_NOTES.md`
4. `TUNING_CANDIDATES.md`
5. `COVERAGE_GAPS.md`

This is an advanced surface. It is not part of the default front-door reading path.
