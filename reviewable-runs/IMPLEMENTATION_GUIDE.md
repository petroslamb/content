# Implementation Guide

This doc explains how teams would build reviewable runs in practice.

The framework does not require markdown files in production. It requires a review surface that can be emitted live or reconstructed later.

## First Deployment Target

A good enough first deployment should support:

- explicit task spec capture
- reconstructable execution trace
- evidence selection or provenance capture
- explicit verification result
- explicit approval capture for meaningful gates
- a standard failure-review path after incidents

Do not try to automate every record on day one. Start with one run class and make that class reviewable end to end.

## What To Capture Live

These are best captured automatically during the run:

- task identifier
- task inputs
- tool calls
- notable observations
- files touched or sources retrieved
- checks run and their result
- gate events

These are the machine-captured spine. Without them, reconstruction quickly becomes guesswork.

## What Can Be Reconstructed Later

These can often be assembled after the run if the raw spine exists:

- cleaned task spec
- reviewer-facing execution trace summary
- curated evidence record
- reviewer summary in the verification report
- structured failure review

This is why the framework emphasizes reconstructability rather than document theater.

## Record-by-Record Build Guidance

### Task Spec

Typical source:

- user request
- workflow config
- job manifest
- ticket or issue

Must be visible:

- plain-language task
- constraints
- stop condition

Good enough first version:

- one structured task object or markdown record created at run start

### Execution Trace

Typical source:

- logs
- event stream
- tool-call history
- shell history

Must be visible:

- control loop steps
- notable observations
- actions taken
- where the run stopped

Good enough first version:

- a reconstructed step list derived from tool events and command outputs

### Evidence Record

Typical source:

- retrieval outputs
- files inspected
- state snapshots
- screenshots
- selected source rows

Must be visible:

- what evidence mattered
- where it came from
- why it mattered
- freshness or state when relevant

Good enough first version:

- one curated table of files, sources, or states used to justify the result

### Verification Report

Typical source:

- tests
- validators
- checks
- policy rules
- reviewer signoff

Must be visible:

- which checks ran
- pass, fail, or partial result
- residual risk

Good enough first version:

- one short report listing checks and remaining uncertainty

### Approval Decision

Typical source:

- approval UI
- policy engine
- reviewer comment
- merge or release gate

Must be visible:

- pending action
- approver or responsible role
- status
- conditions

Good enough first version:

- one explicit gate record when a run stops before a meaningful side effect

### Failure Review

Typical source:

- incident postmortem
- near-miss review
- red-team exercise
- retrospective after a rejected run

Must be visible:

- concrete failure or near miss
- why it was plausible
- taxonomy mapping
- control gap
- corrective direction

Good enough first version:

- one short structured postmortem using the existing failure-review template

## Machine-Captured Vs Human-Authored

Machine-captured by default:

- task metadata
- tool and action history
- raw checks and outputs
- source identifiers
- gate events

Human-authored or reviewer-authored by default:

- reviewer-facing summaries
- evidence curation
- residual risk statement
- approval rationale
- failure-review narrative

Hybrid is normal. The framework does not require every record to be authored by the runtime itself.

## When To Emit Live Vs Reconstruct Later

Emit live when:

- the information is cheap to capture
- the system may lose it later
- the action is high risk
- exact timing matters

Reconstruct later when:

- the raw spine is already available
- the reviewer needs a cleaner summary than raw logs
- the record mainly exists to support review rather than execution

## Adjacent Support Templates

Use the adjacent templates only when they solve a real implementation problem.

- `memory-record-template.md`: use when durable memory policy matters across runs
- `tool-contract-template.md`: use when tool interfaces need explicit control and auditability
- `artifact-handoff-template.md`: use when work passes between stages, agents, or humans

Do not treat these as part of the mandatory six-record surface.

## First Pilot Recommendation

Start with one coding workflow:

- issue or ticket as task source
- shell and test output as trace source
- inspected files as evidence source
- pytest results as verification source
- merge gate as approval source
- near-miss review as failure source

That is the cheapest path to a real reviewable-runs implementation.
