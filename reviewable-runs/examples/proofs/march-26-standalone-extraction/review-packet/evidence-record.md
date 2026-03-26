# Runtime Record: Evidence Record

## Key Evidence

- the user explicitly requested stronger decoupling and one-way dependency from `reviewable-runs` back to AAB
- assistant commentary records removal of bridge surfaces and consolidation of blueprint root docs
- grep sweeps targeted exactly the old bridge paths and deleted root-doc references
- commit `f3c1241` shows both package surfaces landing together

## What Actually Mattered

The run was justified by four visible facts:

- AAB lost the explicit routing into `reviewable-runs`
- blueprint root docs were collapsed and cleaned up
- `reviewable-runs` kept the origin context instead of the blueprint package
- the resulting repo change landed as one commit with a clean worktree

## What Was Omitted

The session contained later framework-building work that reused the same long trace. Those turns were omitted so this packet represents only the extraction run ending at `f3c1241`.

