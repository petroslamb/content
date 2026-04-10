# Editorial Atlas

Editorial instrumentation for the published essay corpus in
[`publication_strategy_and_archive/substack_archive/`](../publication_strategy_and_archive/substack_archive/).

This package is intentionally independent of the tracked workflow docs. It is
not a publishing workflow, intake workflow, or review workflow. It is an
editorial control layer: a place to map what kinds of essay objects already
exist, what strengths they carry, and what a new draft might want to borrow or
resist.

## Corpus

- Scope: the 20 published markdown essays in `substack_archive/`
- Status: first-pass qualitative scoring, manually judged from the published
  surfaces
- Excluded for now: live drafts outside the archive, including promoted rewrites
  that are not yet part of the stable published corpus

## What This Package Contains

- [`process.md`](process.md): scoring method, section slots, and usage notes
- [`rubric.md`](rubric.md): reusable scoring rubric for future essay passes
- [`rubric_assessments.yaml`](rubric_assessments.yaml): canonical rubric-input source for the scored corpus
- [`corpus_inventory.md`](corpus_inventory.md): inventory of all archive essays
- [`essay_atlas.md`](essay_atlas.md): whole-essay scoring pass across the corpus
- [`attractor_cards.md`](attractor_cards.md): short reusable profile cards for
  every archive essay
- [`section_atlas.md`](section_atlas.md): section-level scoring pass
- [`move_library.md`](move_library.md): reverse-engineered editorial moves from
  the archive
- [`draft_pull_sheet_template.md`](draft_pull_sheet_template.md): reusable
  design sheet for future drafts
- [`atlas_data.json`](atlas_data.json): machine-readable essay atlas data
- [`visualizations.md`](visualizations.md): visual layer notes for the atlas
- [`archive/`](archive/): legacy evaluative markdown and qualitative notes;
  not safe to read before a zero-knowledge scoring pass

## Data Contract

`rubric_assessments.yaml` is now the editable scoring source. It stores the
rubric inputs needed to derive:

- direct whole-essay dimensions
- traction subdimensions
- craft subdimensions
- section-slot scores
- explicit corpus exclusions
- draft routing objects

`atlas_data.json` is the generated mirror-facing artifact. Regenerate it with:

```bash
npm run sync:editorial-atlas
```

Validate that the checked-in atlas still matches the rubric source with:

```bash
.venv/bin/python scripts/generate_editorial_atlas.py --check
```

Current note:

- entries marked `rubric_status: migrated` were backfilled from the earlier
  atlas output so the system becomes reproducible and testable
- they still need manual rationale and passage-anchor audit before they should
  be treated as fully rubric-audited records

## Viewer Tabs

The public mirror viewer currently exposes five tabs:

- `Overview`: traction x craft constellation, essay detail card, section
  heatmap, and draft pull vector
- `Debate × Precision`: public-argument energy versus concept-border control
- `Synthesis × Utility`: archive-anchor surveys versus operator-facing essays
- `Openings × Endings`: section-level ignition versus landing strength
- `Move Matrix`: reverse-engineered editorial moves across the whole corpus

The mirror route also does three things the first pass did not:

- uses a shared selected-essay state across the axis views and tables
- encodes confidence directly in the scatterplots
- drives the pull vector from a real draft object in
  [`atlas_data.json`](atlas_data.json) instead of a hard-coded example

## Working Rule

Use the atlas to route and diagnose drafts, not to crown one permanent winner.
The useful question is not "which essay is best?" but "what kind of object is
this new essay trying to become, and which existing objects should pull it?"

## Zero-Knowledge Model Scoring

If an LLM or AI agent is tasked with running the editorial atlas scoring pass
for a new model identity, it **must** perform a zero-knowledge evaluation.

Use this explicit protocol.

### Safe Inputs Before Scoring

These files are safe to read before the model assigns scores:

1. this [`README.md`](README.md), which must remain non-evaluative
2. [`process.md`](process.md)
3. [`rubric.md`](rubric.md)
4. [`rubric_assessments_template.yaml`](rubric_assessments_template.yaml)
5. the published markdown essays in `substack_archive/`

### Unsafe Inputs Before Scoring

These files create a baseline leak and may **not** be read before scoring:

1. any `rubric_assessments_*.yaml` file other than
   `rubric_assessments_template.yaml`
2. [`atlas_data.json`](atlas_data.json)
3. any evaluative markdown in [`archive/`](archive/), including prior atlas
   runs, attractor summaries, or qualitative readouts
4. any future note that ranks essays, names current anchors, or summarizes
   corpus winners

### Repository Hygiene For Zero-Knowledge Scoring

To keep zero-knowledge scoring possible:

1. keep this `README.md` free of rankings, anchor winners, or comparative
   judgments about individual essays
2. put evaluative summaries in [`archive/`](archive/) or model-specific rubric
   files instead
3. treat any future evaluative prose added to `README.md` as a protocol break
