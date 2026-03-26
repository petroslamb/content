# Runtime Record: Task Spec

## Task

Refactor `reviewable-runs` into a compact public package with one front door, one operator guide, grouped examples, a single evaluation surface, an advanced validation surface, and a non-default archive surface.

## Objective

- collapse top-level doc sprawl
- group real proof and teaching examples under `examples/`
- push history into `archive/`
- keep validation visible but clearly advanced
- preserve package clarity while reducing surface count

## Inputs

- the user implementation plan
- the existing top-level docs and folders in `reviewable-runs`
- the current proof, teaching, evaluation, validation, and archive surfaces

## Constraints

- keep the framework readable within ten minutes
- keep proof, teaching, validation, and archive conceptually separate
- avoid stale links to deleted entrypoints
- land the refactor as one coherent package change

## Stop Condition

The package reflects the intended compact surface model, links are intact, and the refactor is committed cleanly.

