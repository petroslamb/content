# Maintenance

This repo should change only when newer research materially updates the guidance published in the original booklet on March 25, 2025.

The maintenance job is not "keep adding papers." The maintenance job is "track whether the last year of research changes the current defaults, alternatives, escalation rules, or confidence levels."

## Source Intake Rules

A new source qualifies for inclusion only if it does at least one of the following:

- improves a default method already in the repo
- adds a credible alternative where the repo currently has a real gap
- materially changes a chapter-level decision rule
- sharpens evaluation or safety practice for an existing architecture

Do not add a source only because it is popular, recent, or adjacent.

## Post-Publication Update Standard

When reviewing work published after March 25, 2025, ask four questions:

1. Does it change a default recommendation?
2. Does it upgrade or downgrade an existing alternative?
3. Does it expose a real gap in one of the six chapter blueprints?
4. Does it materially change how one of the reference architectures should be composed?

If the answer to all four is no, do not update the package.

## Named Method Rule

If a core or supporting doc names a method or paper explicitly, it must also have:

- a `reference/papers/*.md` note
- a `reference/source-index.md` entry

If both do not exist yet, remove the named method from the core doc until the source map is updated.

## Core Vs Frontier

- `Core`: widely useful, practical, and strong enough to shape default guidance
- `Frontier`: interesting or promising, but not strong enough to become a baseline
- `Questionable`: mismatched, weak, or unreliable local material that must not anchor the main narrative

Only `Core` sources should drive default recommendations.

## Note Quality Tiers

- `indexed-only`: metadata plus raw local extraction; acceptable for source mapping and machine recall
- `readable summary`: metadata plus human summary plus raw local extraction; preferred for anchor papers that drive repo guidance
- `questionable`: mismatched or unreliable local material that must not anchor guidance

## Required Update Surfaces

If a new source is added because it actually changes the package, the update must also modify:

- `reference/source-index.md`
- the relevant note in `reference/papers/`
- `reference/literature-quality.md` if confidence, status, or category changes
- one comparison section or equivalent matrix in a chapter blueprint when the source affects method comparison
- one relevant chapter blueprint or use-case document if the source materially changes guidance
- `CHANGELOG.md`

## Update Workflow

Use this order:

1. screen the source for actual decision impact
2. add or improve the paper note
3. update source index and quality tracking
4. update the blueprint or use case only if the guidance changes
5. record the package-level change in `CHANGELOG.md`

## Update Rules For Chapter Blueprints

- Keep one obvious default method.
- Keep alternatives explicit but secondary.
- Keep escalation rules tied to concrete task conditions.
- Remove repeated doctrine when it adds no new decision value.

## Update Rules For Use-Case Docs

- Keep the use-case document compositional rather than theoretical.
- Name which chapter defaults are adopted.
- Name where the use case intentionally diverges from the generic default.
- Keep evaluation criteria and approval boundaries explicit.

## Confidence Policy

- Any ambiguous or mismatched local file must be recorded in `reference/literature-quality.md`.
- If confidence drops below `Medium`, pair the source with stronger neighboring sources or demote it from core guidance.
- `Questionable` sources must remain visible but clearly quarantined.
- If a note is only `indexed-only`, do not treat it as the sole support for a central recommendation when a stronger neighboring source exists.

## Review Rhythm

Run this review whenever the repo changes materially:

- confirm every `reference/papers/*.md` file appears in `reference/source-index.md`
- confirm every core doc still routes cleanly from `README.md`
- confirm new sources updated a comparison asset and not only the corpus
- confirm exploratory notes remain outside the default reading path
