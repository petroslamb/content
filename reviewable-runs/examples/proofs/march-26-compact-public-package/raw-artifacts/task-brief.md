# Raw Artifact: Task Brief

Refactor `reviewable-runs` into a compact public package:

- keep only one narrative front door and one operator guide at top level
- group teaching examples and real proofs under `examples/`
- keep `validation-lab/` visible but clearly advanced
- move lineage material under `archive/`
- reduce the package so it reads like one product rather than a pile of adjacent notes

Acceptance target:

- a first-time reader understands the framework in ten minutes
- proof, teaching, validation, and archive are separated cleanly
- package-local links still resolve after the move

