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

## Current Read

This first pass suggests four distinct anchor roles inside the archive:

- `The Transformer Attractor`: strongest flagship public object
- `The Binding Gap`: strongest prose precision and concept control
- `The Autonomy Tax`: strongest practical/public framework
- `The Illusion of the Swarm`: strongest balanced research-to-builder synthesis

Two secondary anchors also matter:

- `What Actually Works`: strongest long-form evidence-heavy survey object
- `The Moltbook Phenomenon`: strongest topical narrative hijack

## Working Rule

Use the atlas to route and diagnose drafts, not to crown one permanent winner.
The useful question is not "which essay is best?" but "what kind of object is
this new essay trying to become, and which existing objects should pull it?"
