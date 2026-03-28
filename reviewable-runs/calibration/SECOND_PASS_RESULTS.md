# Second-Pass Results

This file records what changed when the calibrated framework was applied to the current real-run corpus a second time.

The point of this pass is not to add more runs. It is to see whether the calibration layer actually changes judgments and reveals tighter framework rules.

## What Changed

### 1. `framework fit` is not the same thing as `public proof priority`

Second-pass review showed that some runs are strong fits for the framework even if they should remain secondary candidates for public proof selection.

Most important examples:

- March 27 pdf-slides skill creation
- March 27 transcript alignment limit

These runs are still secondary for retention purposes because they add less public proof value than the flagship set, but they are stronger framework fits than the first-pass matrix suggested.

### 2. Strong local internal runs do not need commit or publish boundaries

The second pass shows that a bounded internal run with:

- explicit non-approval reason
- strong local validation
- clear changed surface

can still count as `framework fit: strong`.

That matters for the skill-creation run. The previous matrix slightly underweighted local installation plus verification because it read weaker than a commit or publish boundary.

### 3. Limit-finding can be a strong outcome

The second pass also shows that a run whose main value is discovering a real operational limit can still be strong if:

- the task was genuinely to test a possibility
- the evidence is explicit
- the limit discovered is concrete and review-useful

That matters for the transcript-alignment run. It should be read less like a weak success and more like a strong limit-finding case.

### 4. Workflow diagnosis still needs stricter slicing

The sync workflow diagnosis and fallback decision run remains `usable with caveats`.

Why it did not upgrade:

- the session slice still mixes diagnosis, attempted repair, PR cleanup, and stop-short-of-merge behavior
- the boundary is honest, but the run shape is less clean than the stronger proofs

This is still useful evidence, but it remains a caution that workflow-ops runs need strict slicing if they are going to become strong proofs.

## Outcome Adjustments

The second pass supports these recalibrated readings:

- March 27 pdf-slides skill creation: `framework fit: strong`
- March 27 transcript alignment limit: `framework fit: strong`
- March 27 sync workflow diagnosis and fallback decision: stays `framework fit: usable with caveats`
- March 7 origin refactor: stays `framework fit: usable with caveats`

## What Tightened

The framework is tighter after this pass in four ways:

1. it now better separates framework fit from proof-promotion status
2. it no longer implicitly treats commit/publish boundaries as the only strong shapes
3. it has a cleaner path for strong limit-finding runs
4. it has a clearer caution that workflow-ops runs need narrower slices

## Net Result

The calibrated framework now reads less code-biased than before. It still needs broader evidence, but the second pass reduces one important distortion: the tendency to underrate strong local or limit-finding runs just because they are not flagship proof material.
