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

## Canonical Flow

1. confirm the live draft is the polishing target
2. extract slide images from the generated PDF if that has not already happened
3. review the images, name them sensibly when the package uses named assets, and keep them in the package artifact surface
4. insert the images into the essay where they clarify the text rather than decorate it
5. if the podcast artifact is useful as a teaching surface, upload it back into NotebookLM as a source
6. wait for the source to finish processing and export the transcript from the source, not from the audio artifact
7. use the transcript to do a “rehumanization” pass when the current essay is correct but dry
8. finalize references, short orientation blurbs, appendices, and any repo companion links

## Image Placement Rules

The point is not to maximize image count. The point is to improve comprehension.

Use images when they:

- make a conceptual transition easier to follow
- compress a list of distinctions into one visual surface
- reduce repetition in the prose
- help the reader carry a taxonomy or pipeline forward

Do not place images only because they exist.

When naming extracted images:

- prefer short descriptive filenames over page-number-only names
- keep zero-padded sequencing if the package depends on ordered slides
- store them under the package artifact surface or the package’s stronger established equivalent

## Transcript Round-Trip

The recovered podcast transcript is not just another artifact. It is an editorial tool.

Use it to find:

- cleaner teaching phrasing
- more reader-friendly transitions
- places where the spoken version makes a dry paragraph easier to understand
- explanation moves that preserve precision while improving warmth and legibility

Do not blindly merge the transcript into the essay. Treat it as source material for a controlled editorial pass.

## Final Reference Pass

Before publishing:

- make the reference section precise and complete
- add short orientation text for references when it materially helps the reader
- keep appendices only when they genuinely help understanding
- link back to the repo when companions, datasets, or overflow material live here and do not belong in the main body

If the package points to a GitHub companion or dataset, make sure the link reflects the current canonical repo path before publication.

## Related Docs

- [`../notebooklm-artifacts/README.md`](../notebooklm-artifacts/README.md)
- [`../substack-publishing/README.md`](../substack-publishing/README.md)
- [`../../scripts/README.md`](../../scripts/README.md)
