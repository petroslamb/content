# Autonomous Agent Blueprint

This repo is a builder-first architecture manual for modern agent systems. It keeps the public essay layer, the architecture layer, the literature layer, and the reference-architecture layer separate so the package stays usable instead of sprawling.

The package now stops at architecture and reference design. Worked examples, review frameworks, and other derivative material live elsewhere.

## Fastest Useful Path

If you are building, read in this order:

1. `core/agentic-architectures-blueprint.md`
2. `core/practical-chapter-blueprints/README.md`
3. the chapter blueprint that matches your bottleneck
4. the closest file in `implementation/use-cases/`
5. the matching blueprint sections on verification, approval, and failure handling

If you are following the *Operating Agents* course essays, read:

1. `essays/README.md`
2. `essays/launch-note/preface.md`
3. the relevant topic essay
4. the matching topic `companion.md`
5. the matching file in `core/practical-chapter-blueprints/`
6. the matching file in `reference/papers/`

The essay package is being developed as a structured course for builders rather than as a loose set of public essays. The chapter standard lives in `essays/README.md`, and the companion layer now serves as the second-pass breadth layer for each topic.

## Repository Map

- `README.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `MAINTENANCE.md`
- `BUILD_HISTORY.md`
- `essays/`
- `core/`
- `reference/`
- `implementation/`
- `notes/`

## Surface Roles

- `essays/` is the public course-chapter layer for builders, including core chapters and second-pass companions.
- `core/` is the architecture decision layer.
- `reference/` is the literature and source-audit layer.
- `implementation/use-cases/` is the reference-architecture layer.
- `notes/` holds exploratory and working material that should not drive the default reading path.

## What To Update When Research Moves

This package is not meant to absorb every new paper. It should only change when newer research materially updates the guidance published in the original booklet on March 25, 2025.

If a new source changes the package, the usual flow is:

1. add or improve the paper note in `reference/papers/`
2. update `reference/source-index.md`
3. update `reference/literature-quality.md` if confidence or status changes
4. update the relevant chapter blueprint if a decision rule shifts
5. update the relevant use case if the architecture default shifts
6. record the change in `CHANGELOG.md`

## What This Repo Optimizes For

- practical defaults over exhaustive coverage
- named methods over vague clusters
- bounded workflows over theatrical autonomy
- decision rules over paper accumulation
- verification and failure analysis over decorative traces
- evaluation and failure analysis over hype

## Working Rules

- `MAINTENANCE.md` explains the source-intake and update discipline.
- `CONTRIBUTING.md` explains how to propose new notes, blueprint changes, and use cases.
- `BUILD_HISTORY.md` records how the package was originally assembled.
