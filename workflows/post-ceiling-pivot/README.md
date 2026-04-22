---
workflow_id: post_ceiling_pivot
workflow_kind: overlay
stability: experimental
workflow_group: editorial
runner_mode: guided
default_skill: alphaxiv
launch_templates: []
packet_templates:
  - "workflows/post-ceiling-pivot/templates/post_ceiling_reframe_template.md"
  - "workflows/post-ceiling-pivot/templates/pivot_grounding_review_template.md"
  - "workflows/post-ceiling-pivot/templates/pivot_north_star_viability_template.md"
  - "workflows/post-ceiling-pivot/templates/pivot_decision_template.md"
required_context:
  - leaf package README
  - latest stop-gate or replacement-review finding from the capped essay
  - latest ceiling report or legacy donor-report pair from the capped essay
  - current pivot artifacts when they already exist
  - package evidence surface when local papers already anchor the failed object
expected_outputs:
  - pivot slate with ranked candidate families
  - grounding review and blocker record
  - one active next-pivot candidate surface
  - candidate-specific research delta
  - north-star viability gate for any candidate being considered for clearance
  - explicit pivot decision: blocked, provisional, clear lead, or pivot cleared
done_when:
  - one candidate clears both research grounding and north-star viability, or the package explicitly blocks the whole pivot search and records why
approval_gate: required_for_pivot_clearance
---

# Post-Ceiling Pivot

This is the tracked experimental workflow for what to do **after** a flagship essay hits a frame ceiling inside `essay_iteration`.

It is not ordinary draft iteration. It is the repo process for:

- freezing the donor object
- searching for a better flagship object without drafting prematurely
- separating candidate discovery from candidate clearance
- deciding whether a new pivot is real enough to open a new flagship package or sibling object

This workflow was extracted from the April 15, 2026 `clean-interface-illusion` rollout and should be treated as **experimental** until it succeeds cleanly on at least one more package.

## Trigger

Use this workflow only when all of these are true:

1. an essay has already gone through a serious bounded iteration cycle
2. the stop gate has fired or the package has an explicit frame-ceiling finding
3. another local rewrite from the same object would likely produce diminishing returns
4. the package still appears to contain reusable assets for a better object

If the current essay is merely underdeveloped, stay in [`../essay-iteration/README.md`](../essay-iteration/README.md).

## What This Workflow Is For

Use it to answer:

- what should survive from the capped object
- what new candidate objects are actually worth testing
- which candidate is only attractive versus genuinely grounded
- whether any candidate is strong enough to become the next flagship object

Do **not** use it for:

- polishing the old essay
- broad literature browsing with no active decision surface
- opening a new package because a candidate “sounds stronger”

## Core Rule

A pivot is not real because it sounds larger.

A pivot becomes real only when it clears both a research-grounding gate and a north-star viability gate.

That means:

1. search first
2. paper-level inspection second
3. assistant comparison and pressure-testing third
4. north-star viability check before clearance
5. new flagship drafting only after explicit clearance

This workflow treats **candidate discovery** and **candidate clearance** as separate stages.
It also treats **research-grounded** and **north-star viable** as different claims.

## Filesystem Shape

Keep the donor artifact split explicit:

- the `ceiling report` stays at package root because it is the terminal artifact of `essay_iteration`
- the active pivot-search workspace should live under `pivot/active/`
- superseded pivot-search attempts should move to `pivot/archive/<pivot-id>/`

This keeps the flagship iteration packet visible while preventing root-level mixing between:

- terminal essay-iteration artifacts
- live pivot-search artifacts

For legacy packages, root-level pivot artifacts remain valid. For new packages, prefer `pivot/active/`.

## Status Vocabulary

Use these states explicitly in the package artifacts:

- `blocked_hypothesis`
  A candidate that sounded promising but failed the research-grounding gate.
- `provisional_candidate`
  A candidate that is still alive but not yet clearly ahead.
- `clear_lead_candidate`
  The strongest current candidate in the package, still not yet cleared.
- `research_grounded_but_not_north_star_viable`
  A candidate whose evidence seam is real and essay-capable, but whose field-reordering move, evidence aperture, or doctrine is not strong enough for a top-cluster attempt.
- `pivot_cleared_for_north_star_attempt`
  Strong enough to initialize a new flagship object or sibling package because it has cleared both research grounding and north-star viability.

Do not skip from “interesting idea” to `pivot_cleared_for_north_star_attempt` without a grounding review.
Do not skip from `research_grounded` to `pivot_cleared_for_north_star_attempt` without the north-star viability gate.

## Required Artifact Set

The recurring strong artifact set is:

1. `ceiling report`
   Canonical donor report for new packages. This replaces separate reframe and process-capture requirements.
2. `pivot slate`
   Rank several materially different candidate families before deep research.
3. `pivot grounding review`
   Record what the research actually supports.
4. `pivot blocker`
   Preserve why an attractive candidate was rejected.
5. `next pivot candidate`
   Keep one active candidate surface without pretending it is cleared.
6. `candidate-specific research delta`
   Define the exact gaps the next research pass must close.
7. `north-star viability gate`
   Decide whether the candidate has enough field-reordering force, scale-matched evidence, and doctrine to plausibly beat the top archive cluster.
8. `pivot decision`
   Record whether the package should keep searching, clear a pivot, or stop.

Legacy compatibility:

- older packages may still satisfy the donor-report requirement with the pair:
  - `post-ceiling reframe`
  - `process capture`

For new packages, do not generate that pair as a second canonical layer. Use the single `ceiling report`.

These do not need to be identical filenames across packages, but the functions should all exist.

## Working Sequence

### 1. Ceiling Report Or Legacy Donor Report

Start by freezing the donor object.

State:

- why the old object capped out
- what assets survive
- what should not be tried again

For new packages, that happens inside the `ceiling report`.
For legacy packages, use the old `post-ceiling reframe` plus `process capture` pair.

Typical surviving assets:

- opener or anomaly
- comparative turn
- doctrine consequence
- evidence seam that remains strong

### 2. Pivot Slate

Generate a small slate of candidates before deepening research.

For each candidate, record:

- object type
- one-sentence promise
- what it reuses
- what evidence delta it needs
- why it could break the ceiling
- kill criteria
- a compact score

The recurring useful axes are:

- debate gain
- aperture gain
- doctrine utility
- opening power
- synthesis headroom

Do not let the first attractive candidate monopolize the search.

### 3. Grounding Rule

For each serious candidate, use alphaXiv in this order:

1. `search`
2. `paper`
3. `assistant`

Keep assistant sessions short. Start fresh sessions rather than dragging one long chat forward.

Use:

- broad discovery when the seam is still unclear
- narrow validation when the package already has a candidate and the question is “does this framing survive?”

The assistant is for:

- comparing candidates
- pressure-testing the framing
- judging what the papers license

The assistant is **not** the retrieval layer.

## Grounding Pass Patterns

### Search-First Candidate Discovery

This should be the default mode.

1. search for a candidate family
2. inspect abstracts and summaries
3. ask the assistant to compare candidate objects inside the retrieved seam

This is stronger than brainstorm-first discovery because it reduces attractive but unsupported pivots.

### Candidate-Specific Research Delta

Once one candidate is ahead, stop broad discovery and write a research delta for that candidate.

The delta should name:

- what is already closed
- what still needs closing
- immediate search targets
- immediate reading priority
- next assistant questions
- exit criteria

This is the main control surface for the next pass.

### Comparative Rerank

When new evidence changes the seam materially, rerank the live candidates.

Use reranking when:

- a top candidate hits a new blocker
- a supporting seam becomes strong enough to compete
- a negative search result materially changes the evidence shape

Important rule:

- a single negative search can justify demotion
- but final ranking should be governed by **comparative candidate quality**, not by one failed rescue move in isolation

### Supporting Seam Versus Main Candidate

Sometimes a research pass discovers a stronger adjacent seam without actually displacing the main candidate.

Record that distinction explicitly:

- main candidate
- strongest adjacent workflow seam
- strongest narrower writeable synthesis

Do not force every useful seam to become the headline object.

### Full-Package Clearance Pass

When one candidate is clearly ahead, run one final full-package synthesis pass against:

- the candidate’s core seam
- the strongest adjacent seam
- the strongest rival frame
- the most relevant intervention papers

Ask one strict question:

- is this now a real flagship pivot, or only the best remaining candidate?

This is the point where a candidate can move from `clear_lead_candidate` to either:

- `research_grounded_but_not_north_star_viable`
- `pivot_cleared_for_north_star_attempt`

The full-package clearance pass must include the north-star viability gate below before the final status is assigned.

### North-Star Viability Gate

Use this gate after the candidate is research-grounded and before opening a successor flagship package.

The goal is to prevent a recurring failure mode:

- the candidate is real
- the papers support it
- the essay can be strong
- but the resulting draft caps below north star because the idea lacks field-reordering force or the evidence cannot support the largest intended landing

Answer these questions explicitly:

1. **Field-reordering move**
   What does the essay make newly visible about the field? A summary of papers is not enough.
2. **False proxy or public enemy**
   What mistaken substitute does the essay kill or demote? Examples: benchmark score, raw capability, trust calibration, clean-interface success, or another widely overread proxy.
3. **Portable governing term**
   What phrase can carry the essay after reading? It must be precise enough to survive critique and broad enough to travel.
4. **Scale-matched evidence**
   Does the evidence support the essay's largest intended landing? If the ending wants high-stakes governance, the evidence cannot be mostly short lab tasks, toy settings, or theory.
5. **Doctrine with consequence**
   What does the essay force builders, operators, or readers to do differently tomorrow? If the ending is only "be careful," the candidate is not north-star viable.
6. **Largest-claim evidence check**
   Name the essay's biggest intended claim and the exact evidence that licenses it. If that evidence is missing, block or narrow.

Pass this gate only when the candidate is not merely research-supported, but structurally likely to produce a top-cluster essay.

Fail this gate with `research_grounded_but_not_north_star_viable` when the candidate is promising and evidence-backed but likely to cap below the archive's north-star bar unless it is narrowed or receives materially stronger evidence.

## Negative Evidence Rules

Negative results count.

In this workflow, all of these can materially change ranking:

- empty or near-empty search on the decisive missing layer
- intervention papers that fail to close the gap they were supposed to solve
- institutional or workflow evidence showing that a concept works only decoratively

Do not treat failed searches as nothing. Treat them as evidence about what the current frame still lacks.

## Decision Rules

### Block a candidate when:

- the seam stays correlational and under-specified
- the decisive missing layer never materializes
- the candidate remains more slogan than research object
- a better-supported candidate overtakes it

### Mark `clear_lead_candidate` when:

- the candidate is clearly ahead of the remaining live alternatives
- the package can state why it leads
- the candidate still has unresolved research risks that matter for flagship drafting

### Mark `pivot_cleared_for_north_star_attempt` when:

- the candidate survives a full-package clearance pass
- the strongest rival frame no longer looks stronger
- the remaining issues are blueprint risks, not candidate-selection blockers
- the north-star viability gate passes
- the largest intended landing has scale-matched evidence

### Mark `research_grounded_but_not_north_star_viable` when:

- the candidate is supported by the literature and can likely produce a strong essay
- the field-reordering move is not large or surprising enough
- the false proxy or public enemy is weak or diffuse
- the governing term is useful but not yet archive-top-cluster strong
- the largest intended landing outruns the evidence
- the doctrine is correct but not consequential enough to change behavior

## Interaction With Existing Workflows

Use this workflow **after** [`../essay-iteration/README.md`](../essay-iteration/README.md) when a flagship attempt has clearly capped out.

Use [`../alphaxiv-research/README.md`](../alphaxiv-research/README.md) as the execution layer inside this workflow, especially for:

- search-first discovery
- paper inspection
- short assistant pressure-testing

Use [`../paper-intake/README.md`](../paper-intake/README.md) only after a selected paper becomes part of the package’s real evidence base.

## What This Workflow Produced In Practice

The extracted rollout showed a repeatable pattern:

1. capped donor essay
2. donor report freeze
3. pivot slate
4. blocked early candidates
5. stronger winner candidate
6. adjacent workflow seam that improved the picture but did not replace the winner
7. behavioral-proxy pass that stabilized the ranking
8. full-package clearance pass that finally cleared the pivot
9. a later successor package showed that this clearance was still too permissive because research-grounded did not guarantee north-star viability

That is exactly why this workflow exists separately from ordinary draft iteration.
It is also why the north-star viability gate is now required before future pivot clearance.

For the original rollout, donor report freeze meant the legacy pair:

- `post-ceiling reframe`
- `process capture`

For new packages, use the single `ceiling report` instead.

## Current Promotion Read

Treat this as:

- tracked
- usable
- experimental

Do not yet treat it as the canonical repo default for all packages.

Promote the stable pieces into the core iteration system only after at least one more package runs it end-to-end successfully.
