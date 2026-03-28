# Findings

This file merges the useful conclusions from the former investigation and calibration layers.

## Where The Framework Works Well

The framework now works well on:

- bounded code/package runs
- bounded repo/refactor runs
- external-action runs with real platform-state verification
- publish/deploy runs with real deployed-state verification

Across these classes, the framework adds real value over raw traces by making the task, boundary, evidence, verification, and residual risk much easier to review.

## Where It Still Feels Soft

The framework still feels softer on:

- workflow-ops runs that mix diagnosis, attempted repair, and stop-short-of-merge behavior
- editorial runs with thinner evidence and weaker verification
- degraded or partial-reconstruction cases
- multi-agent or contaminated handoff cases, which are still mostly supported synthetically

The issue is not conceptual incoherence. The issue is calibration and implementation support.

## What The Second Pass Changed

The second pass tightened three important judgments:

1. `framework fit` is not the same thing as `flagship proof` status  
   A run can be a strong use of the framework and still remain a secondary candidate if it adds little new public proof value.

2. Strong internal runs do not need commit or publish boundaries  
   A bounded internal run with an explicit non-approval reason and strong local verification can still count as a strong framework fit.

3. Limit-finding can be a strong outcome  
   A run that discovers a real boundary can still be strong if the discovered limit is concrete, evidence-backed, and review-useful.

## What This Means For Usage

The best-fit usage model remains:

1. preserve the raw trace
2. identify one bounded run
3. identify the real stop boundary
4. choose the minimum evidence set
5. reconstruct only the review surface the run needs
6. verify the correct final state for that run type
7. answer the six questions

The framework is strongest when used selectively on meaningful runs, not as blanket paperwork.

## What This Means For Judgment

The framework is now calibrated enough to say:

- strong code/package, repo/refactor, external-action, and publish/deploy runs are genuinely well supported
- strong local internal runs and strong limit-finding runs should not be underrated just because they are not flagship proofs
- workflow-ops and degraded runs still need narrower slicing and sharper scoring rules

The framework should be kept and refined. It should not yet be overclaimed as broadly settled across all run types.

## Bottom Line

Reviewable Runs is now a serious practical framework with a stable question model, stable usage guide, multiple real proofs, and a clearer sense of its operating range.

Its main remaining gaps are:

- broader real-world proof in missing categories
- sharper handling of degraded and mixed-control cases
- lighter implementation support for reconstructing real traces
