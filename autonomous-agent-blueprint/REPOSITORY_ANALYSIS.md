# Repository Analysis

**Status**: current structure map  
**Last updated**: 2026-03-26

This repo started from a large academic survey and was turned into a builder-first package with separate layers for decision-making, public explanation, source auditability, and applied examples. The main cleanup goal was to make those layers visible in the folder structure instead of leaving them mixed together at the root.

## Structure At A Glance

```text
autonomous-agent-blueprint/
├── README.md
├── START_HERE.md
├── REPOSITORY_ANALYSIS.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── MAINTENANCE.md
├── BUILD_HISTORY.md
├── essays/
├── core/
├── reference/
├── implementation/
├── notes/
└── archive/
```

## What Each Surface Does

### `essays/`

The public *Operating Agents* package lives here.

- Topic folders keep the essay, its companion, its local README, and any presentation artifacts together.
- `essays/operating-agents-coverage-map.md` is the bridge from the public essays to the deeper repo layers.
- The active public path is the `v4` essays. Older drafts remain colocated for now and can be archived later.

### `core/`

This is the builder-facing decision layer.

- `core/agentic-architectures-blueprint.md`: overall architecture spine
- `core/reviewable-runs.md`: reviewability contract
- `core/practical-chapter-blueprints/`: the six stable decision guides

If someone asks "what should I build and why," this is the center of gravity.

### `reference/`

This is the literature and synthesis layer.

- `reference/chapters-guide.md`: reading guide into the source survey
- `reference/practical-distillation.md`: sharper operator summary
- `reference/source-index.md`: source catalog
- `reference/literature-quality.md`: confidence and quality notes
- `reference/papers/`: paper-level notes

If someone asks "where does this claim come from," this surface answers it.

### `implementation/`

This is the applied layer.

- `implementation/use-cases/`: abstract reference architectures
- `implementation/case-studies/`: concrete dossiers with runtime and governance records
- `implementation/evaluation/`: architecture review and failure-mode docs
- `implementation/templates/`: reusable structural patterns

If someone asks "what does this look like in practice," this is where they go.

### `notes/`

Exploratory and working material. Useful, but not part of the default path.

### `archive/`

Historical material preserved for reference. It should stay readable but should not compete with the live path.

## Transformation Pipeline

The repo still follows the same pipeline, but the surfaces are now grouped more clearly:

```text
Source survey
  -> reference/chapters-guide.md
  -> reference/practical-distillation.md
  -> core/practical-chapter-blueprints/
  -> essays/
  -> implementation/use-cases/
  -> implementation/case-studies/
  -> implementation/evaluation/
  -> implementation/templates/
  -> reference/papers/
```

## Essay And Blueprint Numbering

The numbering mismatch is intentional.

### Blueprint build order

1. Memory
2. Reasoning and Planning
3. Action and Tool Use
4. Optimization and Self-Improvement
5. Multi-Agent Design
6. Safety

### Essay publication order

1. Action
2. Reasoning
3. Memory
4. Multi-Agent
5. Safety
6. Optimization

The blueprints are ordered for construction logic. The essays are ordered for narrative clarity. Match by topic, not by number.

## Common Confusions

### Should I read the essay or the blueprint?

- If you are building, start in `core/practical-chapter-blueprints/`.
- If you are explaining or publishing, start in `essays/`.
- If you want the broader chapter and source terrain behind an essay, read the local `companion.md`.

### Why did companions move next to essays?

Because the old centralized companion folder hid the most useful scope-clarification material. Locality is better: each essay folder now owns its own companion.

### Why are `README.md` and `START_HERE.md` both still present?

They now have different jobs:

- `README.md`: front-door map
- `START_HERE.md`: task-based reading paths

### Why are there still old drafts in the essay folders?

Draft archiving was intentionally deferred so the repo could be reorganized first. The active path is still the `v4` set.

## Recommended Entry Paths

### Builder

1. `core/agentic-architectures-blueprint.md`
2. `core/practical-chapter-blueprints/README.md`
3. `implementation/use-cases/`
4. `core/reviewable-runs.md`
5. `implementation/case-studies/`
6. `implementation/evaluation/`

### Operating Agents reader

1. `essays/README.md`
2. `essays/launch-note/00-launch-note-v4.md`
3. the relevant `essays/*/*-v4.md`
4. the local `companion.md`
5. the matching blueprint and paper notes

### Writer or researcher

1. `reference/chapters-guide.md`
2. `reference/practical-distillation.md`
3. `reference/source-index.md`
4. `reference/literature-quality.md`
5. `reference/papers/`

## Maintenance Rule

The core rule is still the same: the builder-facing recommendations live in `core/`, the public argument lives in `essays/`, the source trail lives in `reference/`, and the applied proof lives in `implementation/`. New material should strengthen one of those surfaces without blurring their roles.
