# Orchestration Paradigm

Umbrella package for the published *Orchestration Paradigm* series and the broader ToolOrchestra research line that feeds it.

This package is not one essay folder. It combines the published series surface, supporting deep-dive research material, and local media outputs around orchestration, routing, and compound AI systems.

## Package Status

- Archetype: Umbrella package
- Status: Published umbrella
- Publication map: *The Orchestration Paradigm Series* and Issues 2–4 map here
- Canonical workflow docs: [`../../workflows/paper-intake/README.md`](../../workflows/paper-intake/README.md), [`../../workflows/essay-iteration/README.md`](../../workflows/essay-iteration/README.md), [`../../workflows/article-polish/README.md`](../../workflows/article-polish/README.md)

## Orientation

- Published series subpackage: [`ToolOrchestra_Parts/README.md`](ToolOrchestra_Parts/README.md)
- Standalone research essay surface: [`The Agent Revolution.md`](<The Agent Revolution.md>)
- Framework notes and adjacent analysis: `Agent Stack - *.md`, [`ToolOrchestra.md`](ToolOrchestra.md), and the related deep-dive research files at the package root
- Media outputs: [`assets/`](assets/)

## Package Shape

- [`ToolOrchestra_Parts/`](ToolOrchestra_Parts/) is the canonical published-series layer.
- The package root holds broader orchestration and agent-stack analysis that feeds the series but is not identical to the published sequence.
- This package intentionally behaves like an umbrella rather than a single-publication package. Do not force it into one live draft plus one archive.

## Papers, Artifacts, And History

- The ToolOrchestra paper surface lives under [`ToolOrchestra_Parts/papers/`](ToolOrchestra_Parts/papers/).
- Package-level media artifacts live in [`assets/`](assets/).
- Promotional and publication-adjacent material lives under [`ToolOrchestra_Parts/promoting_ideas/`](ToolOrchestra_Parts/promoting_ideas/) and [`ToolOrchestra_Parts/substack_posts/`](ToolOrchestra_Parts/substack_posts/).
- NotebookLM notebook mappings for the series issues live in [`status.yaml`](status.yaml) and are indexed in [`../notebooklm-notebooks.md`](../notebooklm-notebooks.md).
- Historical and exploratory material stays distributed across the package rather than being forced into one top-level `archive/`.

## Working Guidance

- Start with the series subpackage if the task is about the published Orchestration Paradigm essays.
- Use the package root research files when the task is broader than the published series and needs the surrounding argument or technical context.
- Keep the series reading path stable, and place any new package-level orientation in subpackage READMEs rather than in ad hoc root notes.
