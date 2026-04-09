# Workflows

This directory is the tracked canonical playbook layer for `/Users/petros/Projects/content`.

Use package READMEs to understand local structure. Use the workflow docs here to understand the repeatable process. Use tracked skill bundles under [`skills/`](skills/README.md) only after the workflow is clear.

The current defaults in this directory were tightened against recurring March-April 2026 rollout patterns. When the idealized process diverged from what actually worked in the rollouts, the workflow docs were rewritten toward the observed practice.

## Current Workflow Map

| Workflow | Use When | Related Skill Bundle |
| :--- | :--- | :--- |
| [`paper-intake/README.md`](paper-intake/README.md) | collecting papers, converting PDFs to markdown, and maintaining the package paper index | [`skills/markitdown-paper-intake/`](skills/markitdown-paper-intake/) |
| [`alphaxiv-research/README.md`](alphaxiv-research/README.md) | discovering papers, inspecting them, and using the alphaXiv assistant after retrieval | [`skills/alphaxiv/`](skills/alphaxiv/) |
| [`essay-iteration/README.md`](essay-iteration/README.md) | moving from live draft to review, rewrite, scoring, and archive discipline | package-local docs plus review artifacts |
| [`notebooklm-artifacts/README.md`](notebooklm-artifacts/README.md) | generating audio, slide, and video artifacts and downloading them into package artifacts | [`skills/notebooklm-artifact-bundle/`](skills/notebooklm-artifact-bundle/), [`skills/pdf-slides-to-substack-images/`](skills/pdf-slides-to-substack-images/) |
| [`article-polish/README.md`](article-polish/README.md) | naming and placing images, transcript round-trips, rehumanizing the draft, and final reference cleanup before publication | package-local docs plus NotebookLM/PDF helpers |
| [`substack-publishing/README.md`](substack-publishing/README.md) | preparing and publishing essays to Substack and syncing their public presentation | package-local docs plus Substack helpers |
| [`substack-archive-sync/README.md`](substack-archive-sync/README.md) | refreshing the tracked public archive, validating the mirror, and using the manual-import fallback | [`skills/substack-archive-sync/`](skills/substack-archive-sync/) |
| [`youtube-production/README.md`](youtube-production/README.md) | turning slide decks, transcripts, captions, and audio into a verified MP4 before upload | [`skills/youtube-slide-video-pipeline/`](skills/youtube-slide-video-pipeline/) |
| [`distribution/README.md`](distribution/README.md) | handling post-publication distribution work for the channels that matter to a package | package-local `distribution/` or `socials/` surfaces |
| [`youtube-channel-ops/README.md`](youtube-channel-ops/README.md) | authenticated YouTube channel work such as OAuth checks, caption recovery, playlist diagnostics, and Shorts maintenance | [`skills/youtube-data-api/`](skills/youtube-data-api/), [`skills/youtube-shorts-maintenance/`](skills/youtube-shorts-maintenance/) |
| [`youtube-series-operating-agents/README.md`](youtube-series-operating-agents/README.md) | the Operating Agents YouTube series layer: TL;DR uploads, cross-links, playlist order, and replacement uploads | [`skills/youtube-operating-agents/`](skills/youtube-operating-agents/), [`skills/youtube-data-api/`](skills/youtube-data-api/) |

## Canonical Article Lifecycle

The tracked article-development sequence is:

1. paper intake
2. alphaXiv research
3. essay iteration
4. NotebookLM artifacts
5. article polish
6. Substack publishing
7. archive sync

Optional post-publication follow-through can continue with:

8. distribution
9. YouTube production or channel operations when the package includes video work

For refinement cycles on an existing essay, the recurring April 2026 pattern is:

1. harden the package blueprint if it is still fuzzy or under-evidenced
2. use alphaXiv in targeted validation mode against the active anchor papers when needed
3. produce a bounded `v2` candidate beside the stable live draft
4. compare before promotion instead of overwriting first

That lifecycle is the cross-package default. Package READMEs can add local surfaces or exceptions, but they should not redefine the shared process when a tracked workflow already exists here.

## How To Use This Layer

1. Start with the relevant package `README.md`.
2. Open the matching workflow doc here.
3. Use the tracked skill bundle in [`skills/`](skills/README.md) only after the tracked workflow is clear.
4. Use [`../scripts/README.md`](../scripts/README.md) when a workflow depends on tracked repo scripts.

## Skill Bundles

Tracked repo-local skills live in [`skills/`](skills/README.md). Their `.agents/skills/` mirrors exist only so Codex can discover them locally.

Skill bundles should stay thinner than these workflow docs. They can:

- carry execution-specific commands
- point at tracked scripts
- store local-only helper logic

They should not become the only place where a shared repo process is documented.
