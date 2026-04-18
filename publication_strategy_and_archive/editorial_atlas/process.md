# Process

## Purpose

This package turns the published archive into a reusable editorial reference
set. The goal is not literary judgment in the abstract. The goal is to support
three practical tasks:

1. Position a new draft against real prior essay objects
2. Diagnose why a draft feels weak or mis-shaped
3. Borrow strengths from earlier essays without flattening them into generic
   writing advice

## Corpus Source

The source corpus is the published markdown layer under
[`../publication_strategy_and_archive/substack_archive/`](../publication_strategy_and_archive/substack_archive/).

The canonical GPT-5.4 xhigh pass currently covers all 22 archive essays. Older
model-specific passes can explicitly exclude newly published essays until they
receive their own scoring pass.

## Method

Each essay gets four layers of analysis:

1. **Whole-essay atlas**
   - `Traction`: how naturally the piece works as a public object
   - `Craft`: how strong the piece is as prose and essay structure
   - `Publication Power`: coarse combined judgment, weighted toward traction
2. **Attractor card**
   - short reusable profile for editorial borrowing
3. **Section atlas**
   - `Opening`
   - `Thesis Lock`
   - `Development`
   - `Borders / Counterpressure`
   - `Ending`
   - `Reference Handling`
4. **Move library**
   - Named editorial moves drawn from concrete archive examples
5. **Draft objects**
   - data-backed pull sheets that route a new draft toward specific archive essays

This is a manual first pass. It is meant to be useful, not falsely precise.

## Score Semantics

`10` exceptional  
`8-9` strong  
`6-7` solid but uneven or narrower  
`5` or below noticeable weakness or non-flagship behavior

For reusable scoring rules, dimension anchors, and worksheet format, use
[`rubric.md`](rubric.md). This file stays shorter and describes the atlas
method at a package level.

## Composite Definitions

### Traction

A synthesis of:

- hook strength
- thesis compression
- frame portability
- audience breadth
- debate energy
- usable public packaging

### Craft

A synthesis of:

- sentence rhythm
- paragraph control
- structural pacing
- evidence integration
- ending strength

### Publication Power

A coarse combined judgment intended for editorial routing, not leaderboard use.
This pass leans slightly toward traction because the object of interest is the
published essay as a public artifact.

## Section Slots

To make unlike essays comparable, the section pass normalizes them into six
editorial slots:

- `Opening`: how the piece earns attention and establishes stakes
- `Thesis Lock`: where the claim becomes stable and memorable
- `Development`: the main middle architecture of the argument
- `Borders / Counterpressure`: where the piece narrows scope, adds limits, or
  handles objections
- `Ending`: how the piece lands and closes
- `Reference Handling`: how sources are integrated into the essay object

Not every essay has each slot equally. Some pieces are powered by opening and
ending, some by the middle, some by series scaffolding.

## Confidence Scale

- `High`: directly read and compared in detail during this pass
- `Medium`: enough direct reading to score with confidence, but not exhaustively
- `Low`: scored from lighter sampling, structure, and archive context

## How To Use This Package

### For a New Draft

1. Read the relevant model-specific `rubric_assessments_*.yaml` file to identify likely pull essays
2. Use [`atlas_data.json`](atlas_data.json) when you need the generated mirror-facing view of those scores
3. Use [`draft_pull_sheet_template.md`](draft_pull_sheet_template.md) before or
   during revision
4. Borrow one or two strengths intentionally rather than imitating a whole essay

### For a Live-Draft Scoring Pass

Use this mode when you want to place an unpublished draft against the archive
without pretending it is already part of the stable corpus.

Minimum procedure:

1. read the full draft once without scoring
2. choose three anchor essays: one nearby, one stronger, and one weaker
3. write a 2-4 sentence whole-draft rationale
4. capture one opening anchor, one middle anchor, and one ending anchor
5. score direct dimensions, traction, craft, publication power, and section
   slots
6. state the main blocker to the next score up
7. if the draft is being considered for promotion, say explicitly whether the
   score is against corpus standards or only against the package's previous
   version

Do not report a high draft score from cleanup or consolidation alone. A draft
gets atlas credit only for the essay object it has become on the page.

### For Retrospectives

Use the atlas to compare:

- what kind of object the draft intended to be
- what kind of object it actually became
- which sections created the gap

## Known Limits

- The archive includes series entries and chapter-like pieces alongside flagship
  essays. The atlas keeps that heterogeneity visible rather than pretending all
  items are the same kind of object.
- Scores are qualitative judgments, not measurements.
- The viewer now exposes a richer section model than the earliest markdown table
  pass. Prefer [`atlas_data.json`](atlas_data.json) and the generated viewer
  when those diverge from older prose summaries.
- This package should remain essay-anchored. If it drifts into abstract traits
  without concrete archive examples, it will become generic quickly.
