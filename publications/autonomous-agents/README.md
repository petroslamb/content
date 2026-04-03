# Autonomous Agent Blueprint

Umbrella package for two connected surfaces:

- the published builder-first architecture manual behind *Autonomous AI Agents: Core Foundations and Recent Breakthroughs*
- the active *Operating Agents* course essays and companions

This package is not one article folder. It is a shared source tree where essays, architecture blueprints, paper notes, and implementation examples stay separated so the package remains navigable.

## Package Status

- Archetype: Umbrella package
- Status: Published umbrella plus active course development
- Publication map: the published Rooted Layers essay *Autonomous AI Agents: Core Foundations and Recent Breakthroughs* maps here, and the active *Operating Agents* essay package also lives here
- Canonical workflow docs: [`../workflows/paper-intake/README.md`](../../workflows/paper-intake/README.md), [`../workflows/essay-iteration/README.md`](../../workflows/essay-iteration/README.md), [`../workflows/substack-publishing/README.md`](../../workflows/substack-publishing/README.md)

## Fastest Useful Path

If you are reading the builder-first architecture manual:

1. [`core/agentic-architectures-blueprint.md`](core/agentic-architectures-blueprint.md)
2. [`core/practical-chapter-blueprints/README.md`](core/practical-chapter-blueprints/README.md)
3. the chapter blueprint that matches the problem you are solving
4. the closest file in [`implementation/use-cases/`](implementation/use-cases/)

If you are reading the public course essays:

1. [`essays/README.md`](essays/README.md)
2. [`essays/launch-note/preface.md`](essays/launch-note/preface.md)
3. the relevant topic essay
4. the matching `companion.md`
5. the matching chapter blueprint in [`core/practical-chapter-blueprints/`](core/practical-chapter-blueprints/)

## Surface Map

- [`essays/`](essays/) is the public course-chapter layer.
- [`core/`](core/) is the architecture and method layer.
- [`reference/`](reference/) is the literature and source-audit layer.
- [`implementation/use-cases/`](implementation/use-cases/) is the reference-architecture layer.
- [`notes/`](notes/) is exploratory material that should not define the default reading path.

## Papers, Artifacts, And Archive

- The canonical paper library lives in [`reference/papers/`](reference/papers/).
- The literature map lives in [`reference/source-index.md`](reference/source-index.md).
- Course artifacts and local archives live inside topic folders under [`essays/`](essays/), usually as `artifacts/` and `archive/`.
- This umbrella package intentionally keeps a stronger source layout than the generic single-publication `papers/markdown/` pattern.

## Working Rules

- Update the package only when new evidence changes the builder guidance materially, not for every new paper.
- If research moves, start with a paper note in [`reference/papers/`](reference/papers/) and then update the relevant source index, blueprint, or essay surface.
- Keep notes and exploratory material in [`notes/`](notes/) unless they are strong enough to change the package’s public reading path.
