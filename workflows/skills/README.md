# Skill Bundles

This directory is the tracked source for the repo-local Codex skill family.

The live discovery path remains `.agents/skills/`, but that tree is now a symlink mirror of the folders here. Keep the tracked copies here as the source of truth. Keep the `.agents/skills/` mirror only for local skill discovery.

## Current Skill Map

### Intake / discovery

- [`markitdown-paper-intake/`](markitdown-paper-intake/) for package paper intake, PDF-to-markdown conversion, and paper-index maintenance
- [`alphaxiv/`](alphaxiv/) for topic-discovery execution, broad paper discovery, exact-paper inspection, and shortlist refinement before a paper enters the package evidence surface

### Validation / hardening

- [`alphaxiv/`](alphaxiv/) is also the repo's execution skill for narrow claim validation against an existing blueprint, draft, or anchor-paper set. In article-development work, that validation mode is often more valuable than broad discovery.

### Production / publishing

- [`notebooklm-artifact-bundle/`](notebooklm-artifact-bundle/) for the standard NotebookLM artifact bundle and transcript round-trip
- [`pdf-slides-to-substack-images/`](pdf-slides-to-substack-images/) for slide-PDF export into article-ready PNG folders
- [`substack-archive-sync/`](substack-archive-sync/) for the tracked public archive and mirror pipeline
- [`operating-agents-substack-sync/`](operating-agents-substack-sync/) for the Operating Agents series-specific publishing flow
- [`youtube-data-api/`](youtube-data-api/) for authenticated YouTube channel automation, captions, playlists, and upload workflows
- [`youtube-operating-agents/`](youtube-operating-agents/) for the Operating Agents YouTube series layer
- [`youtube-shorts-maintenance/`](youtube-shorts-maintenance/) for Shorts draft and playlist maintenance
- [`youtube-slide-video-pipeline/`](youtube-slide-video-pipeline/) for narrated slide-video production before upload

## Workflow Pairing

Use the workflow docs under [`../`](../) as the canonical process layer:

- paper intake and local evidence storage -> [`../paper-intake/README.md`](../paper-intake/README.md)
- pre-package topic discovery and essay-object selection -> [`../topic-discovery/README.md`](../topic-discovery/README.md)
- alphaXiv discovery and claim pressure-testing -> [`../alphaxiv-research/README.md`](../alphaxiv-research/README.md)
- blueprint hardening and bounded rewrite cycles -> [`../essay-iteration/README.md`](../essay-iteration/README.md)
- release readiness before external mutation -> [`../release-gate/README.md`](../release-gate/README.md)
- archive and mirror work -> [`../substack-archive-sync/README.md`](../substack-archive-sync/README.md)
- local slide/audio/transcript render work -> [`../youtube-production/README.md`](../youtube-production/README.md)
- general authenticated YouTube channel work -> [`../youtube-channel-ops/README.md`](../youtube-channel-ops/README.md)
- Operating Agents YouTube series work -> [`../youtube-series-operating-agents/README.md`](../youtube-series-operating-agents/README.md)

## Working Rule

When a workflow is shared across the repo, explain it first in the tracked workflow docs under [`../`](../). Use the skill bundles here for execution-specific guidance, references, and scripts.
