# Changelog

This file records package-level changes that materially affect the architecture guidance, the literature base, or the reference architectures.

## [Unreleased]

### Changed
- Consolidated root orientation into `README.md` and removed `START_HERE.md`, `REPOSITORY_ANALYSIS.md`, and the old cleanup plan.
- Reduced the package back to architecture, literature, essays, use cases, and notes.
- Removed the old internal worked-example, evaluation, template, and artifact-bundle layers after their extraction into a separate derivative package.
- Tightened `MAINTENANCE.md` around post-March 25, 2025 research updates that actually change guidance.
- Tightened `CONTRIBUTING.md` so contributions update the package only when they materially affect defaults, alternatives, or architecture composition.

### Removed
- `START_HERE.md`
- `REPOSITORY_ANALYSIS.md`
- `REPO_CLEANUP_PLAN.md`
- the former internal `implementation/case-studies/`, `implementation/evaluation/`, `implementation/templates/`, and `archive/case-studies-v1/` surfaces

## [2026-03-26] - Architecture Package Cleanup

### Changed
- Reorganized the package around four live surfaces: `essays/`, `core/`, `reference/`, and `implementation/use-cases/`.
- Moved companions beside essays and cleaned the public essay layer.
- Removed internal derivative-framework material so the package now stops at architecture and reference design.

## [2025-03-25] - Initial Public Release

### Added
- Core architecture blueprint
- Six practical chapter blueprints
- Literature and source-index layer
- Public essay package
- Three reference use cases
- Maintenance and build-history docs
