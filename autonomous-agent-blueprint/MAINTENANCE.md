# Maintenance

This repo is allowed to grow only if new material strengthens the decision system rather than just increasing the corpus size.

## Source Intake Rules

A new source qualifies for inclusion only if it does at least one of the following:

- improves a default method already in the repo
- adds a credible alternative where the repo currently has a real gap
- materially changes a chapter-level decision rule
- sharpens evaluation or safety practice for an existing architecture

Do not add a source only because it is popular, recent, or adjacent.

## Named Method Rule

If a core or supporting doc names a method or paper explicitly, it must also have:

- a `papers/*.md` note
- a `source-index.md` entry

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

If a new source is added, the update must also modify:

- `source-index.md`
- one comparison section or equivalent matrix in a chapter blueprint
- one relevant chapter blueprint or use-case document if the source materially changes guidance

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

- Any ambiguous or mismatched local file must be recorded in `literature-quality.md`.
- If confidence drops below `Medium`, pair the source with stronger neighboring sources or demote it from core guidance.
- `Questionable` sources must remain visible but clearly quarantined.
- If a note is only `indexed-only`, do not treat it as the sole support for a central recommendation when a stronger neighboring source exists.

## Review Rhythm

Run this review whenever the repo changes materially:

- confirm every `papers/*.md` file appears in `source-index.md`
- confirm every core doc still routes cleanly from `README.md` and `START_HERE.md`
- confirm new sources updated a comparison asset and not only the corpus
- confirm exploratory notes remain outside the default reading path
