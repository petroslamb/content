# Tuning Candidates

This file lists the bounded framework changes that the current evidence justifies.

## 1. Sharper Thresholds For `Strong` Versus `Usable With Caveats`

- Problem: Some runs are clearly reviewable but still soft on governance, verification, or slice breadth.
- Evidence: `REAL_RUN_MATRIX.md` rows for March 7 origin refactor, March 27 transcript alignment limit, and March 27 sync workflow diagnosis and fallback decision.
- Proposed framework change: Add internal notes that define what must remain true for a run to count as fully strong versus merely usable with caveats.
- Confidence: high
- Blocked by more evidence? no

## 2. External-Action Boundary Notes

- Problem: External runs now have strong proof support, but `submit` and `publish` boundaries still require more operator judgment than commits.
- Evidence: March 27 YouTube playlist-order fix and March 27 manual mirror import.
- Proposed framework change: Add short operator and evaluation notes that distinguish local artifact changes from the real operational boundary in external runs.
- Confidence: high
- Blocked by more evidence? no

## 3. Verification Mode Separation

- Problem: The corpus now supports three distinct verification families, but the framework still describes them too loosely in some places.
- Evidence: March 12 alphaXiv auth refactor, March 27 YouTube playlist-order fix, March 27 manual mirror import.
- Proposed framework change: Define `tests-and-checks`, `live platform state`, and `deployed public state` more explicitly and use them consistently.
- Confidence: high
- Blocked by more evidence? no

## 4. Limit-Finding Runs As Valid Strong Outcomes

- Problem: Some real runs discover a useful limit rather than producing a conventional success artifact.
- Evidence: March 27 transcript alignment limit.
- Proposed framework change: Add explicit language that a limit-finding run can be strong if the learned boundary is concrete, evidence-backed, and review-useful.
- Confidence: medium-high
- Blocked by more evidence? no

## 5. Promotion Policy For `Flagship Proof` Versus `Secondary Candidate`

- Problem: The corpus is now large enough that proof retention needs a clearer empirical rule, and strong framework fit is not the same thing as flagship status.
- Evidence: `REAL_RUN_MATRIX.md` across flagship proofs and strong secondary runs.
- Proposed framework change: Add a promotion rubric that prefers new run classes, boundary types, or verification modes over more examples of already-covered proof shapes.
- Confidence: high
- Blocked by more evidence? no

## 6. Workflow-Ops And Publication-Ops As First-Class Categories

- Problem: Workflow-ops and publication-style runs are now real parts of the corpus, but the package still reads slightly code-first.
- Evidence: March 27 sync workflow diagnosis and fallback decision, March 27 manual mirror import.
- Proposed framework change: Treat workflow-ops and publication-style runs as first-class categories in future proof selection and calibration work.
- Confidence: medium-high
- Blocked by more evidence? no

## 7. Strong Internal Runs With Explicit Non-Approval Reasons

- Problem: Strong bounded internal runs can still be underrated if they do not end in a commit, release, or deployed external state.
- Evidence: March 27 pdf-slides skill creation after the second pass.
- Proposed framework change: Keep explicit non-approval reasons as a first-class strong boundary for bounded internal runs when verification is strong.
- Confidence: medium-high
- Blocked by more evidence? no

## 8. Lighter Real-Trace Reconstruction Support

- Problem: The framework is conceptually stable, but assembling proof-quality packets from real traces is still too manual.
- Evidence: proof packets across `examples/proofs/` and the retained support templates.
- Proposed framework change: prioritize lightweight extraction support before adding more conceptual framework layers.
- Confidence: medium-high
- Blocked by more evidence? no
