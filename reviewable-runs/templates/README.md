# Templates

This folder contains the record shapes that support Reviewable Runs.

## Direct Record Templates

- `task-spec-template.md`
- `execution-trace-template.md`
- `evidence-record-template.md`
- `verification-report-template.md`
- `approval-decision-template.md`
- `failure-review-template.md`

## Adjacent Support Patterns

- `memory-record-template.md`
- `tool-contract-template.md`
- `artifact-handoff-template.md`

These support implementation, but they are not the framework itself.

## How To Use This Folder

Read `../USE_IT.md` first.

Then:

- use the six direct templates when a run actually needs an explicit review packet
- use the adjacent patterns only when a system needs extra contracts for memory, tools, or handoffs

If a run is low-risk and reconstructable from ordinary logs, you do not need to force these templates onto it.
