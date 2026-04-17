# Templates

This folder contains the record shapes that support Reviewable Runs.

## Direct Record Templates

- `task-spec-template.md`
- `execution-trace-template.md`
- `evidence-record-template.md`
- `verification-report-template.md`
- `approval-decision-template.md`
- `failure-review-template.md`

These remain the framework's canonical record surface.

## Raw-Artifact Support Templates

- `source-manifest-template.md`
- `session-excerpt-template.md`
- `changed-files-summary-template.md`
- `verification-output-summary-template.md`
- `boundary-record-template.md`

These support real-trace reconstruction and proof work. They are optional support surfaces, not a new framework layer.

## Adjacent Support Patterns

- `memory-record-template.md`
- `tool-contract-template.md`
- `artifact-handoff-template.md`
- `harness-proof-run-template.md`

These support implementation, but they are not the framework itself.

## How To Use This Folder

Read `../PLAYBOOK.md` first.

Then:

- use the six direct templates when a run actually needs an explicit review packet
- use the raw-artifact support templates when you are reconstructing a run from real traces or assembling proof material
- use the adjacent patterns only when a system needs extra contracts for memory, tools, or handoffs
- use `harness-proof-run-template.md` when the repo itself is testing whether Codex or a similar harness can operate from the tracked contract and workflow surface

If a run is low-risk and reconstructable from ordinary logs, you do not need to force these templates onto it.
