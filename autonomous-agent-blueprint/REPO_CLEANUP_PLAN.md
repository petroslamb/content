# Repository Cleanup Plan

**Last revised**: 2026-03-26  
**Status**: Proposed  
**Goal**: reduce top-level clutter, make the public essay package easier to navigate, and separate active reference material from leftovers and build-era debris.

## What This Plan Optimizes For

- Keep the repo usable for builders, writers, and readers without making the root feel like a dump of every document class.
- Put companion notes next to the essays they belong to.
- Make the public essay package read like a coherent package, not a side effect of the blueprint workspace.
- Defer archival and speculative expansion work until the active structure is clean.

## Decisions Already Made

- Archiving `v1` to `v3` essay drafts makes sense, but it is **not the priority right now**.
- Companions should live near the essays, not in a separate central folder.
- The current `guide/` name is too generic. The best rename is `essays/`.
- The root should keep only true entry docs and a small number of major folders.
- Existing polish ideas from the old Phase 4 still make sense, but only after the structural cleanup.
- The old Phase 5 is too speculative for the current state of the repo and should be removed from the active plan.

## Current Problems

### 1. The essay package is split awkwardly

Right now the public package is half topic-based (`guide/action/`, `guide/memory/`, and so on) and half centralized (`guide/companions/`). That makes the reading surface harder to understand than it should be.

### 2. The root mixes too many roles

The top level currently mixes:

- onboarding docs
- architecture docs
- writing support docs
- research reference material
- implementation examples
- evaluation assets
- templates

That creates friction even when the individual documents are good.

### 3. There is still visible build residue

The repo still exposes build-era material, exploratory notes, archived patterns, and multiple near-duplicate documents too close to the main path.

## Target Shape

The exact names can still be adjusted, but the structure should move toward this:

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
│   ├── README.md
│   ├── launch-note/
│   ├── action/
│   ├── reasoning/
│   ├── memory/
│   ├── multi-agent/
│   ├── safety/
│   └── optimization/
├── core/
│   ├── agentic-architectures-blueprint.md
│   ├── reviewable-runs.md
│   └── practical-chapter-blueprints/
├── reference/
│   ├── source-index.md
│   ├── literature-quality.md
│   ├── chapters-guide.md
│   ├── practical-distillation.md
│   └── papers/
├── implementation/
│   ├── use-cases/
│   ├── case-studies/
│   ├── evaluation/
│   └── templates/
├── notes/
└── archive/
```

## Naming Recommendations

### `guide/` -> `essays/`

Recommendation: rename `guide/` to `essays/`.

Reason:

- `guide/` is vague and competes conceptually with `foundation-agents-practical-chapters-guide.md`.
- `essays/` tells the truth about what the folder is.
- It makes companion placement obvious: the companion belongs inside the topic folder beside the essay.

### Companion naming

Recommendation: each essay folder should own its companion file directly.

Example:

```text
essays/action/
├── 01-action-tool-use-v4.md
├── companion.md
├── README.md
└── artifacts/
```

If you want stronger filename symmetry, use `01-action-tool-use-companion.md`. Either is fine. The important part is locality, not the exact filename.

## Phase 1: Clean The Public Essay Surface First

This is the highest-value cleanup because it fixes the most visible confusion with the least conceptual risk.

### 1.1 Rename `guide/` to `essays/`

- Move the full essay package under `essays/`.
- Keep topic subfolders as they are.
- Rename `guide/operating-agents-coverage-map.md` to live under `essays/`.

### 1.2 Move companions into the topic folders

- Move each file from `guide/companions/` into its matching topic folder.
- Update essay links, `README.md`, `START_HERE.md`, and the package README to point to the new local paths.
- Remove the centralized `companions/` folder once links are updated.

### 1.3 Remove non-package working material from the essay package root

Move these out of the future `essays/` root:

- `analysis_and_brainstorm.md` -> `notes/essay-evolution/` or `notes/working/`

The essay package root should contain the package README, the coverage map, and topic folders. Nothing else.

### 1.4 Sharpen the role of each topic folder

Each topic folder should contain only:

- current essay
- companion
- topic README
- artifacts
- optionally an `archive/` subfolder later

Do not leave old drafts mixed with the live essay once the archive pass happens.

**Acceptance for Phase 1**

- A new reader can enter `essays/` and understand the package without opening unrelated files.
- Every companion is adjacent to its essay.
- No centralized companion hub remains.

## Phase 2: Declutter The Root By Grouping Document Classes

This is the main structural cleanup for the whole package.

### 2.1 Keep only real entry docs at the root

Keep these at root:

- `README.md`
- `START_HERE.md`
- `REPOSITORY_ANALYSIS.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `MAINTENANCE.md`
- `BUILD_HISTORY.md`
- the major top-level folders

Everything else should justify its root placement or move.

### 2.2 Create a `core/` area for builder-facing architecture docs

Move:

- `agentic-architectures-blueprint.md`
- `reviewable-runs.md`
- `practical-chapter-blueprints/`

into a single builder-facing cluster.

This reduces the "three important docs floating at root" problem and makes the builder path more legible.

### 2.3 Create a `reference/` area for survey and literature support

Move:

- `source-index.md`
- `literature-quality.md`
- `foundation-agents-practical-chapters-guide.md`
- `foundation-agents-practical-distillation.md`
- `papers/`

into a single reference cluster.

This is also the right moment to clarify the difference between:

- `chapters-guide.md`: how to navigate the survey/book material
- `practical-distillation.md`: the shorter synthesis or operator take

### 2.4 Create an `implementation/` area for applied assets

Move:

- `use-cases/`
- `case-studies/`
- `evaluation/`
- `templates/`

into a single applied/builder cluster.

These folders belong together more than they belong at root.

**Acceptance for Phase 2**

- The root reads as a map, not as a warehouse.
- Builder, reference, essay, implementation, notes, and archive surfaces are visibly separated.

## Phase 3: Reduce Duplication In Entry Docs

Once the moves are done, simplify how people enter the repo.

### 3.1 Keep both `README.md` and `START_HERE.md`, but stop duplicating their jobs

Recommended split:

- `README.md`: one-screen overview and routing table
- `START_HERE.md`: task-based reading paths only

Do not let both files carry full repo maps, long explanations, and repeated reading sequences.

### 3.2 Update all navigation after the move

Specifically update:

- root `README.md`
- `START_HERE.md`
- `essays/README.md`
- topic `README.md` files
- any cross-links from blueprints, case studies, or evaluation docs

### 3.3 Add one clear "you are here" map

`REPOSITORY_ANALYSIS.md` should remain the deeper explanation, but the root `README.md` should include one short map explaining the six stable surfaces:

- root entry docs
- `essays/`
- `core/`
- `reference/`
- `implementation/`
- `notes/` and `archive/`

**Acceptance for Phase 3**

- A first-time reader can tell where to go without reading both root docs end to end.
- Cross-links no longer point to pre-cleanup paths.

## Phase 4: Archive And Residue Cleanup

This phase still makes sense, but it should happen after the structure is stable.

### 4.1 Archive old essay drafts

- Move `v1` to `v3` essay drafts out of the live topic folders.
- Preferred target: an archive area grouped by topic.
- Add one short archive README explaining historical status.

### 4.2 Move or quarantine leftovers

Review and relocate anything that is:

- build-era working material
- abandoned improvement ideas
- one-off planning notes
- outdated path references

If it is worth keeping, move it to `notes/` or `archive/`. If it is not worth keeping, delete it.

### 4.3 Validate all links after the archive pass

Run one repo-wide path validation pass after the structural and archive moves.

**Acceptance for Phase 4**

- Live folders no longer contain draft noise.
- Notes and archive material remain available without crowding the main path.

## Explicit Deprioritizations

These were in the older cleanup plan, but they should not be active cleanup priorities right now:

- new speculative docs such as deprioritized-territories manifests
- implementation cookbook expansion
- validation evidence tracking expansions
- blueprint decision-log expansions
- confidence tables added everywhere
- issue-template work

These may still be good ideas later, but they are not the current cleanup problem.

## Order Of Execution

1. Finalize the target naming and destination map.
2. Clean the public essay package.
3. Group root document classes into `core/`, `reference/`, and `implementation/`.
4. Simplify navigation docs.
5. Archive draft material and remove leftovers.

## Success Criteria

This cleanup is successful if:

- the repo root feels intentionally small
- essay companions sit beside the essays they support
- the public essay package is clearly separate from blueprint/reference machinery
- working notes and leftovers are not on the main path
- the main entry docs route users cleanly without duplication
