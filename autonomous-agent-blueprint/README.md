# Autonomous Agent Blueprint

This repo is a builder-first architecture manual for modern agent systems. It starts from a local research corpus, but its main job is no longer to summarize papers. Its job is to help you choose architectures, justify those choices with named sources, and review those designs before implementation.

## Start Here

- `START_HERE.md`
- `agentic-architectures-blueprint.md`
- `reviewable-runs.md`
- `source-index.md`
- `practical-chapter-blueprints/README.md`
- `use-cases/`
- `case-studies/`
- `evaluation/`

## Choose Your Path

### If you are following the Operating Agents series

Read in this order:

1. `guide/README.md`
2. `guide/00-launch-note-v3.md`
3. `guide/operating-agents-coverage-map.md`
4. the matching file in `guide/companions/`
5. the matching file in `practical-chapter-blueprints/`
6. the matching file in `papers/`

### If you are building an agent

Read in this order:

1. `START_HERE.md`
2. `agentic-architectures-blueprint.md`
3. `practical-chapter-blueprints/README.md`
4. the chapter blueprint that matches your bottleneck
5. the closest file in `use-cases/`
6. `reviewable-runs.md`
7. the closest dossier in `case-studies/`
8. `evaluation/architecture-review-checklist.md`
9. `evaluation/failure-mode-catalog.md`

### If you are writing about agent architectures

Read in this order:

1. `START_HERE.md`
2. `agentic-architectures-blueprint.md`
3. `foundation-agents-practical-chapters-guide.md`
4. `source-index.md`
5. `literature-quality.md`

### If you are surveying the literature

Read in this order:

1. `START_HERE.md`
2. `source-index.md`
3. `literature-quality.md`
4. `papers/`
5. `notes/`

## Stable Entry Surfaces

- `README.md`: front door and role-based routing.
- `START_HERE.md`: guided onboarding path.
- `guide/README.md`: public essay package and reading order.
- `guide/operating-agents-coverage-map.md`: series-to-source map for readers who want breadth behind the essays.
- `guide/companions/`: essay-specific breadth notes linking public posts back to the chapter guide, survey, blueprints, and paper notes.
- `reviewable-runs.md`: explanation of what a serious system must surface to make a run reviewable.
- `source-index.md`: literature map with confidence and practical role.
- `practical-chapter-blueprints/`: chapter-level decision layer.
- `use-cases/`: end-to-end reference architectures.
- `case-studies/`: linear worked dossiers backed by runtime records and governance records.
- `evaluation/`: architecture review and failure analysis.

## Repository Map

### Core

- `START_HERE.md`
- `agentic-architectures-blueprint.md`
- `reviewable-runs.md`
- `practical-chapter-blueprints/README.md`
- `practical-chapter-blueprints/*.md`
- `use-cases/`
- `case-studies/`
- `evaluation/`
- `templates/`

### Supporting

- `source-index.md`
- `literature-quality.md`
- `guide/README.md`
- `guide/*-v3.md`
- `guide/operating-agents-coverage-map.md`
- `guide/companions/*.md`
- `foundation-agents-practical-chapters-guide.md`
- `foundation-agents-practical-distillation.md`
- `papers/*.md`
- `MAINTENANCE.md`
- `BUILD_HISTORY.md`
- `archive/`

### Exploratory

- `notes/`

Exploratory material is worth keeping, but it should never be the default path for first-time readers.

## Publication Layering

- `guide/*-v3.md`: the public narrative layer.
- `guide/companions/*.md`: the breadth layer for readers who want the fuller chapter and survey picture.
- `practical-chapter-blueprints/*.md`: the operator layer for decisions, defaults, evaluation, and anti-patterns.
- `papers/*.md`: the source-note layer for named methods and individual literature artifacts.

## What This Repo Optimizes For

- practical defaults over exhaustive coverage
- named methods over vague clusters
- bounded workflows over theatrical autonomy
- decision rules over paper accumulation
- reviewable runs over decorative traces
- evaluation and failure analysis over hype

## Document Contracts

- Core docs must contain defaults, alternatives, escalation rules, evaluation criteria, and anti-patterns.
- Supporting docs must strengthen traceability, source quality, or chapter-level detail.
- Exploratory docs may contain useful ideas, but they are not allowed to anchor the main narrative without promotion into the core layer.

## Local Corpus Policy

Raw PDFs are kept locally for reference but ignored by git in this package. The tracked source of truth is the markdown material.

## Maintenance

See `MAINTENANCE.md` for source intake rules, confidence policy, and update requirements for future additions.
