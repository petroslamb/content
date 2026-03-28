# Calibration Notes

These notes answer the current calibration questions against `REAL_RUN_MATRIX.md`.

## 1. Which run classes already calibrate the framework well?

`code-package`, `repo-refactor`, `external-action`, and `publish-deploy` are already calibrated well enough to support stable operator guidance. The corpus has multiple strong examples with clear boundaries and credible verification in those classes.

## 2. Which boundary types are now credibly handled?

`handoff`, `commit`, `submit`, `publish`, and `explicit non-approval reason` are now credibly represented in the real corpus. `merge` and `release` are still conceptually supported but underrepresented in the real proof set.

## 3. Which verification modes are now clearly understood?

`tests-and-checks`, `live platform state`, and `deployed public state` are now clear and well grounded. `local artifact validation` is stronger than the first pass implied when it is paired with a bounded internal run and explicit non-approval logic. `mixed` is real and important, but needs crisper internal handling.

## 4. Where does the framework still overfit code/commit-shaped runs?

The framework is less at risk than before, but it still inherits some code-centric instincts:

- commit boundaries still feel “cleaner” than operational submit/publish boundaries
- local verification still reads more naturally than external-state verification
- repo-refactor proofs are still the densest part of the corpus

## 5. Which runs are strong proofs of framework value beyond raw traces?

The strongest proofs beyond raw trace are:

- March 12 alphaXiv auth refactor
- March 27 YouTube playlist-order fix
- March 27 manual mirror import
- March 26 standalone extraction
- March 26 compact public package refactor

These runs show clear gains in boundary clarity, verification meaning, and reviewability beyond what the raw session alone would provide.

## 6. Which runs are useful only as edge, failure, or cautionary cases?

The most useful cautionary or edge cases are:

- March 27 sync workflow diagnosis and fallback decision
- March 26 opinion-only review

The transcript-alignment run now looks less like a cautionary case and more like a strong limit-finding run.

## 7. Where does the `Strong / Partial / Weak` thinking still feel too coarse?

It is too coarse in at least four places:

- runs with strong reconstruction but softer governance
- runs that validly discover a limit instead of producing a conventional success
- mixed-control runs where API inspection, UI workaround, and external final state are all part of one bounded run
- runs that are strong framework fits but should still stay secondary because they add little new public proof value

## 8. What kinds of judgment are still too manual or too subjective?

The most manual judgments are:

- deciding the exact run slice in long sessions
- deciding when lightweight reconstruction is enough versus when a full packet is worth it
- deciding whether a real but incomplete run is “usable with caveats” or too weak to retain
- deciding how strongly to separate framework fit from proof-retention priority

## 9. Which missing real-run categories now matter most?

The highest-priority missing categories are:

- retrieval-heavy governed-output run
- stronger browser held-submit or pre-submit run
- real degraded or partial-reconstruction run
- real near-miss or failure-review run with operational consequence

These would extend the framework meaningfully beyond the current coding, repo, platform, and publishing emphasis.

## 10. What should the next tuning wave target first?

The next tuning wave should target:

1. sharper internal thresholds for `framework fit: strong` versus `usable with caveats`
2. crisper handling of external-action and publish boundaries
3. clearer distinction between local validation, live-state verification, and deployed-state verification
4. explicit treatment of limit-finding and workflow-ops runs as valid categories
5. cleaner separation between framework fit and public proof-promotion status

## Net Judgment

The framework is now calibrated enough to say where it works well and where it still feels interpretive. The next gains will come from sharper thresholds and broader empirical coverage, not from inventing new core concepts.
