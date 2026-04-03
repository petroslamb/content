# Hardware Compatibility Architecture (2023-2025)

Umbrella package for the hardware-friction line of work. It combines the long quantitative essay, the shorter friction-map publication, the scorecard methodology, and the research dataset that supports them.

## Package Status

- Archetype: Umbrella package
- Status: Published umbrella
- Publication map: *What Actually Works: The Hardware Compatibility Filter in Neural Architecture (2023–2025)* and *The Hardware Friction Map*
- Related cross-package publication: *The Transformer Attractor* is published through [`../neural-architectures/README.md`](../neural-architectures/README.md), even though some shared upstream material lives here
- Canonical workflow docs: [`../workflows/paper-intake/README.md`](../../workflows/paper-intake/README.md), [`../workflows/essay-iteration/README.md`](../../workflows/essay-iteration/README.md), [`../workflows/substack-publishing/README.md`](../../workflows/substack-publishing/README.md)

## Orientation

- Canonical long-form article: [`long_article_sections/What_Actually_Works_2023_2025.md`](long_article_sections/What_Actually_Works_2023_2025.md)
- Canonical shorter publication draft: [`essay_sections/The_Hardware_Friction_Map_Essay_substack.md`](essay_sections/The_Hardware_Friction_Map_Essay_substack.md)
- Scorecard methodology: [`hardware_friction_scorecard/Hardware_Friction_Scorecard_v2.md`](hardware_friction_scorecard/Hardware_Friction_Scorecard_v2.md)
- Public dataset and local working copy: [`research_artifacts/scorecard_dataset/`](research_artifacts/scorecard_dataset/)

## Source Layers

- [`research_artifacts/`](research_artifacts/) is the main evidence layer, including the scorecard dataset, source compilation, timelines, and supplementary analyses.
- [`refs/research_references.md`](refs/research_references.md) is the local reference surface.
- [`essay_sections/`](essay_sections/) and [`substack_drafts/`](substack_drafts/) hold shorter publication-oriented markdown.
- [`long_article_sections/`](long_article_sections/) holds the longer article build.

## Artifacts, Distribution, And History

- Distribution assets for the essay line live in [`essay_sections/distribution/`](essay_sections/distribution/).
- Critiques and stress-test material live under both [`essay_sections/critiques/`](essay_sections/critiques/) and [`hardware_friction_scorecard/critiques/`](hardware_friction_scorecard/critiques/).
- This package uses domain-specific history layers rather than one top-level `archive/`.

## Working Guidance

- Treat the scorecard dataset as a first-class output, not just background evidence for the essay.
- Keep the shared hardware-friction source layer here even when a downstream publication maps to another umbrella package.
- When adding new evidence, update the relevant research artifact first and then propagate only the material changes into the publication surfaces.
