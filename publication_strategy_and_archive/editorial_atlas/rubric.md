# Scoring Rubric

This rubric makes the atlas scoring pass reusable. It is designed for manual
editorial judgment, but it should be run in a controlled way so scores do not
drift from essay to essay or from one pass to the next.

Use this file together with:

- [`process.md`](process.md) for the package model
- `rubric_assessments_*.yaml` for existing model-specific whole-essay and section-slot scores
- [`atlas_data.json`](atlas_data.json) for the canonical machine-readable schema consumed by the mirror

## Core Rule

Do not score from vibe alone.

Every recorded score should be supported by:

- one short written rationale
- one concrete passage or section anchor
- one confidence label

If you cannot justify a score with a passage, lower confidence or defer the
score.

## Scope

This rubric applies to:

- whole-essay scores
- section-slot scores
- confidence assignment

It does not replace the move library. Moves are explanatory. Scores are
comparative.

## Scoring Scale

Use integer scores only.

- `10`: exceptional, archive-defining, unusually hard to improve
- `9`: excellent, clearly stronger than most essays in the corpus
- `8`: strong, reliably above corpus baseline
- `7`: solid, clearly functional, but not dominant
- `6`: mixed or narrower, works but with visible limits
- `5`: noticeably weak, partial, or underpowered
- `4`: weak enough that the function is not really being carried
- `3` and below: broken, missing, or not meaningfully present

Default discipline:

- Start from `7`, then move up or down based on evidence.
- Do not use `9` or `10` unless the essay is clearly among the best archive
  examples for that trait.
- Do not use `3` or below unless the function is truly absent or badly failed.

## Required Evidence Per Essay

Before finalizing an essay record, capture:

1. `Whole-essay note`
   A 2-4 sentence justification for the overall profile.
2. `Opening anchor`
   One passage or paragraph reference for how the essay starts.
3. `Middle anchor`
   One passage or section reference for the main argument architecture.
4. `Ending anchor`
   One passage or section reference for how the piece lands.
5. `Confidence`
   `High`, `Medium`, or `Low` using the rules below.

For live-draft scoring, also capture:

6. `Anchor comparison`
   Name one nearby archive essay, one stronger archive essay, and one weaker
   archive essay used for calibration.
7. `Next-score blocker`
   One sentence on the main reason the draft does not yet deserve the next score
   up.

## Scoring Procedure

Run the scoring pass in this order.

1. Read the full essay once without scoring.
2. Identify the six section slots:
   `Opening`, `Thesis Lock`, `Development`, `Borders`, `Ending`,
   `Reference Handling`.
3. Score the four direct auxiliary dimensions:
   `Debate`, `Precision`, `Synthesis`, `Utility`.
4. Score the six traction subdimensions.
5. Score the five craft subdimensions.
6. Derive `Traction`, `Craft`, and `Publication Power`.
7. Score the six section slots.
8. Write the rationale and assign confidence.

Do not start from existing atlas scores when rescoring a piece. Score from the
essay itself first, then compare against the atlas for consistency.

For unpublished drafts, do not start from the package's previous score or from
the author's target bar. Score the draft against the archive first, then note
whether it improved relative to the prior draft.

Do not award `9` or `10` to a live draft unless the worksheet evidence would
still support that score when compared directly against the strongest archive
anchors. "Better than before" is not enough.

## Whole-Essay Dimensions

### Direct Auxiliary Dimensions

These should be scored directly before the composites.

#### Debate

Question:
How naturally does this essay generate public argument, reposting, challenge,
or “you need to read this” energy?

Use:

- `9-10`: sharp public claim, clear adversarial surface, highly discussable
- `7-8`: arguable and portable, but not naturally explosive
- `5-6`: interesting but mostly absorptive rather than provocative
- `4` or below: low public-argument energy

Score high when:

- the core claim creates disagreement quickly
- the title/thesis is easy to argue with
- readers can summarize the conflict in one line

Score low when:

- the essay is mostly explanatory or accumulative
- disagreement requires too much setup
- the piece is respected more than debated

#### Precision

Question:
How well does the essay define borders, control scope, and avoid hand-waving?

Use:

- `9-10`: unusually disciplined concept control, clear borders, low fuzz
- `7-8`: generally careful, with manageable overreach
- `5-6`: partly clear, but with soft borders or compressed leaps
- `4` or below: fuzzy, overclaimed, or poorly bounded

Score high when:

- terms are defined cleanly
- objections or limits are handled inside the essay
- the claim narrows rather than sprawls

Score low when:

- key terms remain metaphorical or unstable
- the frame outruns what the essay actually proves
- the piece depends on reader charity

#### Synthesis

Question:
How well does the essay compress a broad literature, history, or design space
into one coherent argument?

Use:

- `9-10`: unusually strong integration across sources or traditions
- `7-8`: effective synthesis with clear through-line
- `5-6`: some integration, but still additive or survey-like
- `4` or below: little real synthesis beyond juxtaposition

Score high when:

- multiple source lines are turned into one argument
- the essay reduces complexity without flattening it
- literature serves the thesis instead of interrupting it

Score low when:

- sources remain stacked rather than integrated
- historical or research material feels bolted on
- the essay reads like notes more than synthesis

#### Utility

Question:
How directly can a reader use this essay for action, design, evaluation, or
decision-making?

Use:

- `9-10`: highly reusable for real choices and operating decisions
- `7-8`: provides usable filters, checklists, or design guidance
- `5-6`: some practical relevance, but mostly conceptual
- `4` or below: low immediate operational use

Score high when:

- the essay yields a scorecard, filter, doctrine, or design rule
- a reader could apply it Monday morning
- the piece changes what a builder or operator should do

Score low when:

- usefulness depends on heavy translation by the reader
- the essay is mostly interpretive
- action implications are implied but not made explicit

### Traction Composite

Score these six subdimensions first, then derive `Traction`.

#### Hook Strength

Question:
How quickly does the essay create curiosity, tension, or stakes?

- `9-10`: immediate tension; the opening earns attention in the first move
- `7-8`: clear hook, though not unusually sharp
- `5-6`: interesting but slower or more technical
- `4` or below: diffuse or delayed opening

#### Thesis Compression

Question:
How compressible is the core claim into one memorable line or phrase?

- `9-10`: strongly nameable, quoteable, or slogan-ready without distortion
- `7-8`: clear core claim, but less memorable or portable
- `5-6`: real thesis present, but diffuse or multi-claim
- `4` or below: thesis remains unstable or hard to restate

#### Frame Portability

Question:
How reusable is the essay’s framework outside this specific piece?

- `9-10`: portable across conversations, products, decisions, or future essays
- `7-8`: reusable in nearby contexts
- `5-6`: mostly useful inside the essay itself
- `4` or below: low portability

#### Audience Breadth

Question:
How many adjacent audiences can care without special preparation?

- `9-10`: crosses several strong reader groups naturally
- `7-8`: clear primary audience and at least one adjacent audience
- `5-6`: mainly one audience or one niche
- `4` or below: narrow specialist object

#### Debate Energy

Question:
Does the piece naturally create reaction, disagreement, or discussion?

This is narrower than `Debate`. Use it here as part of public-object shape.

- `9-10`: very likely to spark argument or reposting
- `7-8`: clearly discussable
- `5-6`: interesting but lower-energy
- `4` or below: not debate-shaped

#### Public Packaging

Question:
How well is the essay shaped for title, post, quote, or recommendation-based
spread?

- `9-10`: title, concept, and framing are unusually easy to package publicly
- `7-8`: good publication object, even if not inherently viral
- `5-6`: packageable with effort, but not naturally
- `4` or below: hard to package cleanly

### Traction Calculation

Calculate:

`Traction = rounded average of Hook Strength, Thesis Compression, Frame Portability, Audience Breadth, Debate Energy, Public Packaging`

Adjustment rule:

- Allow a single `+1` or `-1` editorial override if the essay’s actual public
  object behavior is clearly misrepresented by the average.
- Record the override reason in the rationale.

### Craft Composite

Score these five subdimensions first, then derive `Craft`.

#### Sentence Rhythm

Question:
How strong is the line-level cadence, compression, and variation?

- `9-10`: unusually controlled, memorable sentence-level writing
- `7-8`: strong and readable prose with good variation
- `5-6`: serviceable but plain, repetitive, or uneven
- `4` or below: clumsy, flat, or noticeably noisy

#### Paragraph Control

Question:
Do paragraphs hold one move cleanly and end at the right moment?

- `9-10`: very high paragraph discipline
- `7-8`: mostly controlled, with occasional drift
- `5-6`: mixed paragraph focus or length control
- `4` or below: paragraphs routinely sprawl or blur moves

#### Structural Pacing

Question:
How well does the essay manage movement, momentum, and reader fatigue?

- `9-10`: strong momentum with no major drag sections
- `7-8`: solid pacing, even if one section is slower
- `5-6`: readable but uneven or top-heavy
- `4` or below: visibly dragging or awkwardly structured

#### Evidence Integration

Question:
How well do examples, papers, citations, and references support the argument
without taking it over?

- `9-10`: evidence is deeply integrated into the essay’s motion
- `7-8`: evidence supports the case cleanly
- `5-6`: evidence is present but stacked, dumped, or interruptive
- `4` or below: either unsupported or citation-heavy in a way that breaks flow

#### Ending Strength

Question:
Does the essay land with clarity, force, and memorability?

- `9-10`: strong closing that sharpens the whole essay
- `7-8`: satisfying ending with clear landing
- `5-6`: adequate close, but tapering or merely summary-like
- `4` or below: weak, abrupt, or dissolving ending

### Craft Calculation

Calculate:

`Craft = rounded average of Sentence Rhythm, Paragraph Control, Structural Pacing, Evidence Integration, Ending Strength`

Adjustment rule:

- Allow a single `+1` or `-1` editorial override only when the essay is
  distinctly better or worse as a finished prose object than the mean implies.
- Record the override reason in the rationale.

### Publication Power

Calculate:

`Publication Power = round((0.6 * Traction) + (0.4 * Craft))`

Use `Publication Power` as a routing aid, not as a quality verdict.

Adjustment rule:

- Do not override by more than `1`.
- Override only if the piece’s real publication identity is clearly being
  flattened by the formula.

## Section-Slot Rubric

Score each slot for how well that slot performs its editorial function, not for
how much of the essay is devoted to it.

### Opening

Question:
How well does the opening establish curiosity, stakes, and directional trust?

Score high when:

- the reader quickly knows why the essay matters
- the first move creates tension or orientation
- the opening matches the eventual essay contract

Score low when:

- the opening delays the actual reason to care
- it overpromises relative to the essay
- it starts with setup that could have been compressed

### Thesis Lock

Question:
How clearly does the essay stabilize its main claim into a memorable form?

Score high when:

- the claim becomes legible early enough
- the reader can restate the thesis after reading this section
- the thesis is sharper after this section than before it

Score low when:

- the essay wanders before locking its claim
- the thesis remains multi-headed or soft
- the essay never really earns a stable line

### Development

Question:
How well does the middle architecture build, test, and deepen the argument?

Score high when:

- sections build rather than repeat
- the middle carries the essay without sagging
- the logic accumulates in a controlled sequence

Score low when:

- the middle becomes additive, list-like, or repetitive
- examples substitute for architecture
- the reader loses the thread of advancement

### Borders / Counterpressure

Question:
How well does the essay narrow scope, address tension, and handle objections or
limits?

Score high when:

- the essay becomes more credible by narrowing
- objections are metabolized rather than ignored
- the claim gains shape under pressure

Score low when:

- objections are missing where they are clearly needed
- limits are vague or deferred
- the frame expands instead of tightening

### Ending

Question:
How well does the ending land, sharpen, and close the essay?

Score high when:

- it creates a memorable final posture
- it clarifies stakes without merely repeating
- it makes the earlier argument feel more coherent

Score low when:

- the essay just stops
- the close is summary-only
- the ending narrows the essay’s force unintentionally

### Reference Handling

Question:
How well does the essay integrate sources, citations, examples, or references
into the argument object?

Score high when:

- references support motion rather than interrupt it
- source selection feels purposeful
- evidence is legible without overwhelming the prose

Score low when:

- citations feel bolted on
- examples clutter rather than clarify
- evidence appears either too thin or too dumped

## Confidence Rubric

### High

Use `High` only when:

- you read the full essay carefully
- you compared it directly against at least two nearby atlas essays
- you can cite concrete passage evidence for the major score claims

### Medium

Use `Medium` when:

- you read the full essay or nearly all of it
- you can support the main judgment, but not every edge case
- the score is stable enough for atlas use, but not deeply audited

### Low

Use `Low` when:

- you scored from lighter reading, structural sampling, or prior familiarity
- one or more important dimensions are inferred rather than directly evidenced
- the score should be treated as provisional

## Calibration Rules

To keep scores comparable across passes:

1. Always compare a new essay against at least three existing atlas anchors:
   one nearby, one stronger, and one weaker.
2. Do not score in isolation.
3. When uncertain between two adjacent scores, choose the lower one unless you
   can name the evidence for the higher score.
4. Use `10` sparingly. It should feel corpus-defining, not merely very good.
5. If an essay is highly unusual, explain the exception rather than hiding it in
   a rounded score.
6. For live drafts, separate "better than the previous package draft" from
   "actually at this corpus tier."

## Minimal Scoring Worksheet

Use this template when adding or rescoring an essay:

```md
## [Essay Title]

- Whole-essay rationale:
- Opening anchor:
- Middle anchor:
- Ending anchor:

### Direct dimensions
- Debate:
- Precision:
- Synthesis:
- Utility:

### Traction subdimensions
- Hook Strength:
- Thesis Compression:
- Frame Portability:
- Audience Breadth:
- Debate Energy:
- Public Packaging:
- Traction:

### Craft subdimensions
- Sentence Rhythm:
- Paragraph Control:
- Structural Pacing:
- Evidence Integration:
- Ending Strength:
- Craft:

### Section slots
- Opening:
- Thesis Lock:
- Development:
- Borders:
- Ending:
- Reference Handling:

### Composite
- Publication Power:
- Confidence:
```

## Known Limits

- This rubric improves consistency, but it is still a qualitative editorial
  instrument.
- The atlas contains heterogeneous objects: flagship essays, series entries,
  chapter-like pieces, and topical interventions. Comparability is useful, not
  perfect.
- Scores should stay anchored to passages and examples. If the scoring process
  becomes detached from the actual essays, the rubric will become generic again.
