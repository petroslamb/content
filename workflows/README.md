# Workflows

This directory is the tracked canonical playbook layer for `/Users/petros/Projects/content`.

Use it when you need to understand how the repo’s article-development lifecycle and adjacent publishing automation are supposed to work. Package README files explain local structure. Tracked skill bundles under [`skills/`](./skills/README.md) help execute the workflows, and `.agents/skills/` mirrors them locally for Codex discovery.

The current defaults in this directory were checked against recurring March-April 2026 rollout patterns for alphaXiv research, NotebookLM artifact work, Substack archive operations, YouTube production and channel ops, and the repo’s brutal-review essay loops. When rollout evidence and the idealized process diverged, the workflow docs were tightened toward the observed pattern.

## Current Workflow Map

| Workflow | Use When | Related Skill Bundle |
| :--- | :--- | :--- |
| [`paper-intake/README.md`](./paper-intake/README.md) | collecting papers, converting PDFs to markdown, and maintaining the package paper index | [`skills/markitdown-paper-intake/`](./skills/markitdown-paper-intake/) |
| [`alphaxiv-research/README.md`](./alphaxiv-research/README.md) | discovering papers, inspecting them, and using the alphaXiv assistant after retrieval | [`skills/alphaxiv/`](./skills/alphaxiv/) |
| [`essay-iteration/README.md`](./essay-iteration/README.md) | moving from live draft to review, rewrite, scoring, and archive discipline | package-local docs plus review artifacts |
| [`notebooklm-artifacts/README.md`](./notebooklm-artifacts/README.md) | generating audio, slide, and video artifacts and recovering transcripts | [`skills/notebooklm-artifact-bundle/`](./skills/notebooklm-artifact-bundle/), [`skills/pdf-slides-to-substack-images/`](./skills/pdf-slides-to-substack-images/) |
| [`substack-publishing/README.md`](./substack-publishing/README.md) | preparing and publishing essays to Substack and syncing their public presentation | package-local docs plus Substack helpers |
| [`substack-archive-sync/README.md`](./substack-archive-sync/README.md) | refreshing the tracked public archive, validating the mirror, and using the manual-import fallback | [`skills/substack-archive-sync/`](./skills/substack-archive-sync/) |
| [`youtube-production/README.md`](./youtube-production/README.md) | turning slide decks, transcripts, captions, and audio into a verified MP4 before upload | [`skills/youtube-slide-video-pipeline/`](./skills/youtube-slide-video-pipeline/) |
| [`youtube-channel-ops/README.md`](./youtube-channel-ops/README.md) | authenticated YouTube channel work such as OAuth checks, caption recovery, playlist diagnostics, and Shorts maintenance | [`skills/youtube-data-api/`](./skills/youtube-data-api/), [`skills/youtube-shorts-maintenance/`](./skills/youtube-shorts-maintenance/) |
| [`youtube-series-operating-agents/README.md`](./youtube-series-operating-agents/README.md) | the Operating Agents YouTube series layer: TL;DR uploads, cross-links, playlist order, and replacement uploads | [`skills/youtube-operating-agents/`](./skills/youtube-operating-agents/), [`skills/youtube-data-api/`](./skills/youtube-data-api/) |

## How To Use This Layer

1. Start with the relevant package `README.md`.
2. Open the matching workflow doc here.
3. Use the tracked skill bundle in [`skills/`](./skills/README.md) only after the tracked workflow is clear.
4. Use [`../scripts/README.md`](../scripts/README.md) when a workflow depends on tracked repo scripts.

## Skill Bundles

Tracked repo-local skills live in [`skills/`](./skills/README.md). Their `.agents/skills/` mirrors exist only so Codex can discover them locally.

Skill bundles should stay thinner than these workflow docs. They can:

- carry execution-specific commands
- point at tracked scripts
- store local-only helper logic

They should not become the only place where a shared repo process is documented.
