---
workflow_id: article_polish
runner_mode: guided
default_skill: null
launch_templates: []
required_context:
  - canonical live draft
  - package artifact surface with NotebookLM or local media outputs
  - current references and supporting links
expected_outputs:
  - polished live draft with intentional media placement
  - semantically named kept images in the artifact surface
  - publication-ready references and repo links
done_when:
  - the draft is publication-ready and ready to hand off to Substack publishing
approval_gate: required_before_publish
---

# Article Polish

This is the canonical tracked workflow for the editorial stage between NotebookLM artifact generation and final Substack publication.

Use it when the essay is already structurally sound and the remaining work is about presentation quality, media placement, pedagogical clarity, and final reference discipline.

## Purpose

This workflow exists to close the gap between:

- a precise draft with downloaded artifacts
- a publication-ready essay that reads well on Substack

In practice, this is where the repo turns artifact generation into editorial improvement.

## Inputs

Before starting this workflow, the package should already have:

- a canonical live draft
- a downloaded NotebookLM artifact bundle or equivalent local media outputs
- the slide deck PDF in the package artifact surface
- the package’s current references and supporting links

Before changing image paths, also inspect the current markdown and git diff. This catches the common failure where a raw artifact refresh accidentally deletes publishable images or removes embeds from the essay:

```bash
rg -n '!\[[^]]*\]\(' publications/<package>/<draft>.md
git diff --name-status -- publications/<package>/
```

## Outputs

When this workflow is done, the package should have:

- a polished live draft that still preserves the reviewed argument
- a named image set stored under the package artifact surface or its declared equivalent
- intentional image placements in the essay markdown
- a transcript-informed editorial pass where useful
- publication-ready references, appendices, and repo links

## Canonical Flow

1. confirm the live draft is the polishing target
2. extract slide images from the generated PDF if that has not already happened
3. review the images, shortlist the ones that actually help the reader, and name them intentionally
4. insert the images into the essay where they clarify the text rather than decorate it
5. if the podcast artifact is useful as a teaching surface, upload it back into NotebookLM as a source
6. wait for the source to finish processing and export the transcript from the source with the CLI `-o` flag, not by redirecting terminal preview text
7. use the transcript to do a “rehumanization” pass when the current essay is correct but dry
8. finalize references, short orientation blurbs, appendices, and any repo companion links

## Stage 1: Image Selection And Naming

Do not treat every extracted slide as a publishable image. Reduce the deck to the visuals that materially improve comprehension.

Raw slide exports are not the same thing as article assets. A folder such as `artifacts/latest/slides/` or `artifacts/previous/slides/` is a generated source surface. The article image set should use stable, semantically named files under the package's declared publishable asset surface.

Before deleting or renaming any existing image file:

- check whether a markdown draft references it
- check whether it is part of a prior reviewed article-image set
- preserve it unless the current polish pass intentionally removes that visual from the essay

Never remove image embeds from the draft just to make a raw artifact refresh look clean. Removing an image is an editorial decision. It should happen because the visual no longer helps the essay, not because a new deck produced different filenames.

Prefer images that:

- introduce a taxonomy the reader will reuse across several sections
- compress a long distinction set into one stable reference surface
- make a pipeline or causal chain easier to hold in working memory
- clarify a conceptual jump that would otherwise require dense prose

Skip images that:

- merely restate the paragraph directly above or below them
- depend too much on speaker context to stand alone
- only feel useful because they came from the deck

When naming extracted images:

- prefer semantic names over page-number-only names
- keep ordered numeric prefixes when sequence matters
- use short slug-style names with hyphens
- preserve zero padding if the package depends on ordered slide assets

Good patterns:

- `01-agent-loop-overview.png`
- `02-memory-authority-layers.png`
- `05-evaluation-failure-modes.png`

Weak patterns:

- `slide1.png`
- `image-final-v2.png`
- `page-7.png`

The goal is that a future editor can tell why the image exists without reopening the full slide deck.

## Stage 2: Intentional Image Placement

The point is not to minimize image count either. The point is to improve comprehension.

Use images when they:

- make a conceptual transition easier to follow
- compress a list of distinctions into one visual surface
- reduce repetition in the prose
- help the reader carry a taxonomy or pipeline forward
- give the reader a stable diagram they can reuse across several later sections

Do not place images only because they exist.
Do not cap images artificially if several visuals each do real explanatory work.

The practical sequence that has worked best in the repo is:

1. start with the obvious load-bearing visuals only
2. reread the essay as a reader, looking for long dry stretches where a diagram would materially reduce cognitive load
3. add one image at a time into those gaps, then reread the local section before adding the next
4. stop when the remaining unused visuals feel repetitive rather than clarifying

That sequence matters because the right visual density is rarely obvious from the deck alone. It emerges from alternating between essay reading and selective placement.

Placement rules:

- place the image near the paragraph where the reader first needs it
- add a short lead-in sentence if the image needs framing
- avoid stacking several visuals without enough prose between them
- if one visual supports several later sections, place it once at the earliest decisive point and refer back to it in prose
- keep the markdown readable even if the image does not load
- treat the opening and conclusion as distinct visual slots rather than as overflow zones for leftover slides

The normal editorial move is:

1. identify the paragraph where the visual earns its keep
2. insert it immediately before or after that paragraph
3. reread the surrounding prose so the image and text cooperate rather than compete

Two additional moves are now canonical:

1. if the essay opens with a title visual, consider a second early "thesis bridge" image before the first major section when it helps the reader grasp the argument's governing shift
2. if a late-body image and a summary image compete for the same conceptual space, move the summary image under the conclusion so it resolves the essay instead of crowding the final section

If an image feels decorative after insertion, remove it.
If several images remain genuinely load-bearing after insertion, keep them.

## Stage 3: Transcript Round-Trip And Rehumanization

The recovered podcast transcript is not just another artifact. It is an editorial tool.

Use it to find:

- cleaner teaching phrasing
- more reader-friendly transitions
- places where the spoken version makes a dry paragraph easier to understand
- explanation moves that preserve precision while improving warmth and legibility

Do not blindly merge the transcript into the essay. Treat it as source material for a controlled editorial pass.

The safest sequence is:

1. read the current essay section that feels precise but flat
2. read the corresponding transcript section
3. extract the useful teaching move, not the spoken wording wholesale
4. rewrite the essay paragraph so it keeps the reviewed claim but improves rhythm, accessibility, or explanation
5. stop if the prose starts sounding improvised, repetitive, or less defensible

Before using a recovered transcript, verify it is complete. A partial NotebookLM preview often contains a header with a large character count and then a line telling the caller to use `-o` to save full content. That file is not an editorial source; re-export it with `source fulltext -o`.

Good transcript-derived improvements:

- a cleaner transition between dense sections
- a concrete restatement after a technical claim
- a warmer explanation of why the distinction matters
- sentence rhythm that is easier to read without weakening the argument

Bad transcript-derived changes:

- importing filler, hedging, or spoken repetition
- replacing a precise claim with a looser but friendlier one
- turning a thesis-driven section into chatty narration
- copying transcript language mechanically across the whole essay

The transcript is a corrective when the review loop has made the essay too dry, not a new canonical draft source.

## Stage 4: Final Editorial Pass

Before handing off to Substack publishing, reread the essay as one package rather than as isolated sections.

Check for:

- image names and placements that still make sense after the last rewrite
- no accidental deletion of previously placed images; removed embeds should have an editorial reason
- visual spacing that still gives the prose room to breathe between diagrams
- references that are complete, precise, and consistently formatted
- short orientation blurbs only where they genuinely help
- appendix material that belongs at the end rather than in the main flow
- repo links that point at the current canonical path
- a reading experience that still feels like an essay rather than internal repo documentation

## Final Reference Pass

Before publishing:

- make the reference section precise and complete
- for newly added sources doing body work, add a short contribution note either in the reference entry or the surrounding prose so a future editor can tell why the citation is present
- add short orientation text for references when it materially helps the reader
- keep appendices only when they genuinely help understanding
- link back to the repo when companions, datasets, or overflow material live here and do not belong in the main body

If the package points to a GitHub companion or dataset, make sure the link reflects the current canonical repo path before publication.

## Acceptance Criteria

This workflow is complete when:

- the live draft reads better, not just longer
- every kept image has a defensible editorial reason to be there
- the essay is not visually starved when additional diagrams would clearly help readers hold the argument
- image filenames are understandable out of context
- the transcript round-trip improved clarity or warmth without weakening claims
- references and repo links are publication-ready
- the draft is ready to hand off into [`../substack-publishing/README.md`](../substack-publishing/README.md)

## Worked Examples

### Binding Gap Package

The cleanest repo-local example of this workflow is the binding-gap package:

- live essay: [`../../publications/binding-gap/The_Binding_Gap.md`](../../publications/binding-gap/The_Binding_Gap.md)
- named slide assets: [`../../publications/binding-gap/artifacts/slides/The_Binding_Gap_detailed/`](../../publications/binding-gap/artifacts/slides/The_Binding_Gap_detailed/)
- recovered transcript: [`../../publications/binding-gap/artifacts/audio/The_Binding_Gap_podcast_transcript.txt`](../../publications/binding-gap/artifacts/audio/The_Binding_Gap_podcast_transcript.txt)

Why it matters:

- the images are semantically named rather than left as raw page numbers
- the essay places them directly at the points where the argument changes shape
- the transcript round-trip exists as a real package artifact rather than as an abstract possibility
- the final artifact home is package-level `artifacts/`, not a duplicate essay-local media tree

This is the best canonical example for image naming, image placement, and transcript round-trip discipline.

### Operating Agents Transcript-Led Rewrites

The clearest repo-local examples of the rehumanization logic are the Operating Agents action and safety essays:

- action essay: [`../../publications/autonomous-agents/essays/action/01-action-tool-use.md`](../../publications/autonomous-agents/essays/action/01-action-tool-use.md)
- safety essay: [`../../publications/autonomous-agents/essays/safety/05-trust-boundaries-and-agent-safety.md`](../../publications/autonomous-agents/essays/safety/05-trust-boundaries-and-agent-safety.md)

Why they matter:

- they use the transcript’s teaching order rather than an older essay hook structure
- they show how a transcript can improve pedagogy without being copied wholesale
- they keep the reviewed doctrinal spine while making the prose more teachable and less dry

The lesson from those rewrites is that the transcript should often supply sequence and explanation rhythm, while the final essay still supplies precision, compression, and publication discipline.

## Related Docs

- [`../notebooklm-artifacts/README.md`](../notebooklm-artifacts/README.md)
- [`../substack-publishing/README.md`](../substack-publishing/README.md)
- [`../../scripts/README.md`](../../scripts/README.md)
