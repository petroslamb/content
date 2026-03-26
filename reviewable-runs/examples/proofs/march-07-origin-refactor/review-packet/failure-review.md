# Governance Record: Failure Review

## Plausible Failure

The active path could look coherent while the archive quietly rots through stale relative links or old terminology that still shapes reader behavior.

## Failure Class

Migration drift and documentation split-brain.

## Control Gap

The refactor changed both structure and routing. Without explicit archive checks and active-path terminology sweeps, the repo could preserve history badly or keep teaching two conflicting models.

## Corrective Direction

- keep archive checks explicit whenever historical material moves
- treat review-surface terminology as a routed concept, not just local wording
- require a commit-time review that checks both active-path clarity and archive readability
