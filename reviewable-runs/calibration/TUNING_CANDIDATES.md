# Tuning Candidates

This file lists the bounded framework changes that calibration now justifies.

## 1. Sharper Thresholds For `Strong` Versus `Usable With Caveats`

- Title: Sharpen outcome thresholds
- Problem: Some runs are clearly reviewable but still soft on governance, verification, or slice breadth. The current outcome language flattens those differences.
- Evidence: `REAL_RUN_MATRIX.md` rows for March 7 origin refactor, March 27 transcript alignment limit, and March 27 sync workflow diagnosis and fallback decision.
- Proposed framework change: Add internal calibration notes that define what must stay true for a run to count as fully strong versus merely usable with caveats.
- Confidence: high
- Blocked by more evidence? no

## 2. External-Action Boundary Calibration Notes

- Title: Clarify external-action boundaries
- Problem: External runs now have strong proof support, but they still require extra operator judgment because `submit` and `publish` boundaries do not behave like commits.
- Evidence: March 27 YouTube playlist-order fix and March 27 manual mirror import.
- Proposed framework change: Add a short calibration note set for external platform runs that distinguishes local artifact changes from the real operational boundary.
- Confidence: high
- Blocked by more evidence? no

## 3. Local Validation vs Live/Deployed-State Verification

- Title: Separate verification modes more explicitly
- Problem: The framework currently describes verification well in prose, but the corpus now shows three different verification families that deserve firmer separation.
- Evidence: March 12 alphaXiv auth refactor, March 27 YouTube playlist-order fix, March 27 manual mirror import.
- Proposed framework change: Add explicit internal definitions for `tests-and-checks`, `live platform state`, and `deployed public state`, and use them consistently in future calibration and proof work.
- Confidence: high
- Blocked by more evidence? no

## 4. Treat Limit-Finding Runs As Valid Outcomes

- Title: Legitimize limit-finding runs
- Problem: Some real runs produce a useful limit or failure boundary rather than a clean success artifact. The framework currently recognizes this, but not crisply enough.
- Evidence: March 27 transcript alignment limit.
- Proposed framework change: Add a calibration note that a run can be successful as a limit-finding run if the boundary learned is explicit, evidence-backed, and review-useful.
- Confidence: medium-high
- Blocked by more evidence? no

## 5. Retention Policy For `Flagship Proof` vs `Secondary Candidate`

- Title: Tighten promotion policy
- Problem: The corpus is getting large enough that proof retention needs a more explicit empirical rule, and the second pass shows that framework fit is not the same thing as proof-promotion priority.
- Evidence: `REAL_RUN_MATRIX.md` across flagship proofs versus secondary candidates.
- Proposed framework change: Add a promotion rubric that prefers new verification modes, new boundary types, or new run classes over more examples of already-covered proof shapes, and explicitly decouples `framework fit` from `flagship proof` status.
- Confidence: high
- Blocked by more evidence? no

## 6. Workflow-Ops And Publication-Ops As First-Class Categories

- Title: Recognize ops-style runs explicitly
- Problem: Workflow-ops and publish-deploy runs are now real parts of the corpus, but the framework still reads slightly code-first.
- Evidence: March 27 sync workflow diagnosis and fallback decision, March 27 manual mirror import.
- Proposed framework change: Treat workflow-ops and publication-style runs as first-class operational categories in future proof selection and calibration work.
- Confidence: medium-high
- Blocked by more evidence? no

## 7. Strong Internal Runs With Explicit Non-Approval Reasons

- Title: Legitimize strong local internal runs
- Problem: The first pass underrated bounded internal runs that had no commit or publish boundary but did have explicit non-approval logic and strong local validation.
- Evidence: March 27 pdf-slides skill creation after second-pass review.
- Proposed framework change: Add a calibration note that explicit non-approval reason plus strong local verification can still support `framework fit: strong` for bounded internal runs.
- Confidence: medium-high
- Blocked by more evidence? no
