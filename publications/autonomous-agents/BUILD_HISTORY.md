# Build History

This file records the completed build-out that moved the repo from synthesis to value. The checkmarks remain as a scope record, not as an active planning queue.

## Phase 0: Foundation Already In Place

- [x] Establish a core intellectual spine with the practical guide, architecture blueprint, and chapter blueprints.
- [x] Package the repo cleanly with a top-level README and a scoped PDF ignore policy.
- [x] Consolidate the practical chapter structure into six chapter blueprints.
- [x] Separate tracked authored markdown from local-only PDFs.

## Phase 1: Make the Repo Navigable

- [x] Rewrite the top-level README so it routes by user goal.
- [x] Add a dedicated first-time-reader entrypoint, later consolidated back into `README.md`.
- [x] Classify the major documents as core, supporting, or exploratory through the main navigation surface.
- [x] Move exploratory material into a dedicated `notes/` path.
- [x] Add recommended reading paths for builders, writers, and researchers.

## Phase 2: Make the Literature Auditable

- [x] Create `source-index.md`.
- [x] Record full titles, local files, chapter relevance, method categories, practical roles, canonical links, and confidence.
- [x] Create `literature-quality.md`.
- [x] Add a lightweight standard header to each `papers/*.md` note.
- [x] Mark known source issues so they cannot silently anchor core arguments.
- [x] Index every named method that appears in core or supporting docs.
- [x] Promote the wave-1 anchor papers to readable summary notes above raw extraction.

## Phase 3: Turn Each Chapter into a Decision Engine

- [x] Add a method comparison matrix to each chapter blueprint.
- [x] Add quick choice guidance to each chapter blueprint.
- [x] Standardize each chapter around defaults, alternatives, escalation logic, evaluation, and anti-patterns.
- [x] Keep the existing architecture prose while making the files more decision-oriented.

## Phase 4: Add End-to-End Reference Architectures

- [x] Create `use-cases/enterprise-agent.md`.
- [x] Create `use-cases/coding-agent.md`.
- [x] Create `use-cases/web-agent.md`.
- [x] Specify memory, reasoning, action, verification, human gates, safety boundaries, and evaluation in each use-case doc.
- [x] Name adopted defaults and intentional divergences.
- [x] Add chapter and paper backing to the major subsystem choices in each use-case doc.
- [x] Add explicit rejected alternatives to each use-case doc.

## Phase 5: Add Evaluation And Review Assets

- [x] Create the original architecture review and failure-mode assets.
- [x] Add a cross-cutting architecture scorecard.
- [x] Add chapter-linked review prompts.
- [x] Add a threat-model checklist.

## Phase 6: Add Implementation-Adjacent Templates

- [x] Create the original tool contract, memory record, run trace, approval gate, and artifact handoff templates.
- [x] Keep templates structural and framework-agnostic.
- [x] Link templates back to the relevant chapter and use-case docs.

## Phase 7: Add Maintenance Discipline

- [x] Create `MAINTENANCE.md`.
- [x] Define source intake rules and confidence policy.
- [x] Define update rules for chapter blueprints and use-case docs.
- [x] Require future source additions to update the source map and a comparison asset.

## Verification

- [x] Confirm every `papers/*.md` file appears in `source-index.md`.
- [x] Confirm terminology is consistent across README, chapter guides, use-case docs, and evaluation docs.
- [x] Confirm exploratory notes are demoted from the main path.
- [x] Confirm no questionable source appears as a core authority without warning.
- [x] Confirm no unindexed named method remains in core or supporting docs.
- [x] Confirm all wave-1 anchor notes have readable summary sections above raw extraction.
- [x] Confirm every use-case default names both its chapter basis and paper basis.
- [x] Confirm OpenHands naming is consistent across core and supporting docs while `papers/opendevin.md` remains the local file alias.

## Extension: Worked Example Layer

- [x] Add `case-studies/` as a stable repo surface.
- [x] Add three canonical worked examples for enterprise, coding, and web agents.
- [x] Add realistic artifact bundles and failure reviews for each case.
- [x] Add a cross-case comparison matrix and forward links from abstract use cases and evaluation docs.

Historical note: the worked-example layer that once lived here was later spun out into its own derivative package. This build history now records only the architecture package itself.
