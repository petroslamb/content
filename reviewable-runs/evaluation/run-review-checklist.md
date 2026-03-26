# Run Review Checklist

Use this file to review one meaningful run against the six review questions.

The standard here is not whether a system emitted six markdown files. The standard is whether a reviewer can reconstruct the necessary records credibly enough to inspect the run.

## The Six Questions

- [ ] What was the task?
- [ ] What happened?
- [ ] What did it rely on?
- [ ] How was it checked?
- [ ] Who approved impact, or why was approval not required?
- [ ] What failed or could fail?

## Record Checks

### Task Spec

- [ ] Is the task boundary explicit?
- [ ] Are constraints visible?
- [ ] Is the stop condition visible?

### Execution Trace

- [ ] Is the control loop reconstructable?
- [ ] Are notable actions and observations visible?
- [ ] Is it clear where the run stopped?

### Evidence Record

- [ ] Are the key sources, files, or state elements visible?
- [ ] Is provenance or freshness visible when it matters?
- [ ] Is it clear what evidence actually mattered to the run?

### Verification Report

- [ ] Are the checks named explicitly?
- [ ] Is the result of each important check visible?
- [ ] Is residual risk stated honestly?

### Approval Decision

- [ ] Is the approval boundary explicit?
- [ ] Is the pending action visible?
- [ ] Are the review packet and any conditions visible?

### Failure Review

- [ ] Is the plausible or actual failure stated concretely?
- [ ] Is the failure mapped to a recurring class or control gap?
- [ ] Is the corrective direction clear?

## Outcomes

### Strong

The run is reconstructable without guesswork and the records support real review.

### Partial

The run can be understood, but one or two key records are thin or implied rather than explicit.

### Weak

The run depends on scattered logs, memory, or inference, and cannot be reviewed credibly.
