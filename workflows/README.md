# Workflows

This directory is the tracked canonical playbook layer for `/Users/petros/Projects/content`.

Use package READMEs to understand local structure. Use the workflow docs here to understand the repeatable process. Use tracked skill bundles under [`skills/`](skills/README.md) only after the workflow is clear.

The current defaults in this directory were tightened against recurring March-April 2026 rollout patterns. When the idealized process diverged from what actually worked in the rollouts, the workflow docs were rewritten toward the observed practice.

## Current Workflow Map

| Workflow | Use When | Related Skill Bundle |
| :--- | :--- | :--- |
| [`paper-intake/README.md`](paper-intake/README.md) | promoting already-selected papers into the package evidence surface, converting PDFs to markdown, and maintaining the paper index | [`skills/markitdown-paper-intake/`](skills/markitdown-paper-intake/) |
| [`alphaxiv-research/README.md`](alphaxiv-research/README.md) | discovering papers, refining a shortlist, and pressure-testing active claims against anchor papers before intake | [`skills/alphaxiv/`](skills/alphaxiv/) |
| [`essay-iteration/README.md`](essay-iteration/README.md) | hardening blueprints, running review and rewrite cycles, and maintaining live-draft/archive discipline | package-local docs plus review artifacts |
| [`notebooklm-artifacts/README.md`](notebooklm-artifacts/README.md) | generating audio, slide, and video artifacts and downloading them into package artifacts | [`skills/notebooklm-artifact-bundle/`](skills/notebooklm-artifact-bundle/), [`skills/pdf-slides-to-substack-images/`](skills/pdf-slides-to-substack-images/) |
| [`article-polish/README.md`](article-polish/README.md) | naming and placing images, transcript round-trips, rehumanizing the draft, and final reference cleanup before publication | package-local docs plus NotebookLM/PDF helpers |
| [`substack-publishing/README.md`](substack-publishing/README.md) | preparing and publishing essays to Substack and syncing their public presentation | package-local docs plus Substack helpers |
| [`substack-archive-sync/README.md`](substack-archive-sync/README.md) | refreshing the tracked public archive, validating the mirror, and using the manual-import fallback | [`skills/substack-archive-sync/`](skills/substack-archive-sync/) |
| [`youtube-production/README.md`](youtube-production/README.md) | turning slide decks, transcripts, captions, and audio into a verified MP4 before upload | [`skills/youtube-slide-video-pipeline/`](skills/youtube-slide-video-pipeline/) |
| [`distribution/README.md`](distribution/README.md) | handling post-publication distribution work for the channels that matter to a package | package-local `distribution/` or `socials/` surfaces |
| [`youtube-channel-ops/README.md`](youtube-channel-ops/README.md) | authenticated YouTube channel work such as OAuth checks, caption recovery, playlist diagnostics, and Shorts maintenance | [`skills/youtube-data-api/`](skills/youtube-data-api/), [`skills/youtube-shorts-maintenance/`](skills/youtube-shorts-maintenance/) |
| [`youtube-series-operating-agents/README.md`](youtube-series-operating-agents/README.md) | the Operating Agents YouTube series layer: TL;DR uploads, cross-links, playlist order, and replacement uploads | [`skills/youtube-operating-agents/`](skills/youtube-operating-agents/), [`skills/youtube-data-api/`](skills/youtube-data-api/) |

## Canonical Article Lifecycle

The lifecycle stage ids remain unchanged for runner compatibility. The working taxonomy for article development is:

1. **discovery**: use [`alphaxiv-research/README.md`](alphaxiv-research/README.md) to find and inspect candidate papers before they are admitted into a package
2. **validation**: use [`alphaxiv-research/README.md`](alphaxiv-research/README.md) in narrow claim-testing mode against the active anchor papers and package evidence surface
3. **blueprint hardening**: use [`essay-iteration/README.md`](essay-iteration/README.md) as the governing process surface, with targeted help from [`alphaxiv-research/README.md`](alphaxiv-research/README.md) and [`paper-intake/README.md`](paper-intake/README.md) when evidence needs to be tightened. After a blocking high-bar review, this is the mandatory next step and must either set an outstanding-governing rewrite direction or record an explicit impossibility finding
4. **external blueprint review**: optionally use [`essay-iteration/README.md`](essay-iteration/README.md) for an advisory outside review of the hardened blueprint before the prewrite gate. The writer adjudicates the findings and integrates only what materially improves the governing surface
5. **essay prewrite gate**: use [`essay-iteration/README.md`](essay-iteration/README.md) to decide whether an outstanding essay is actually writable before prose drafting begins. This step must either produce an essay-governing prewrite surface or an explicit blocker
6. **draft iteration**: use [`essay-iteration/README.md`](essay-iteration/README.md) to produce bounded rewrite candidates beside the live draft and compare before promotion
7. **production and publishing**: use NotebookLM, polish, publishing, archive-sync, distribution, and video workflows once the live draft is ready for outward-facing work

Optional post-publication follow-through can continue with:

1. distribution
2. YouTube production or channel operations when the package includes video work

The runner still uses the stage sequence:

1. `paper_intake`
2. `research`
3. `essay_iteration`
4. `notebooklm_artifacts`
5. `article_polish`
6. `substack_publishing`
7. `archive_sync`
8. `distribution`
9. `youtube_production`

For refinement cycles on an existing essay, the recurring April 2026 pattern is:

1. intake missing papers into the package evidence surface if the active claims still rely on temporary or alphaXiv-only context
2. harden the package blueprint if it is still fuzzy, under-evidenced, or outrunning the current anchor set
3. optionally run an external blueprint review, but keep it advisory and adjudicate the fixes as the writer
4. run the essay prewrite gate before drafting: either produce an essay-governing prewrite surface or conclude explicitly that the essay is not yet writable at the target bar
5. use alphaXiv in targeted validation mode against the active anchor papers when needed
6. produce a bounded candidate beside the stable live draft
7. run a cold replacement review against both the live draft and the outstanding-essay bar
8. if that review does not clear promotion, return immediately to blueprint hardening at the same top bar: either produce an outstanding-governing blueprint or conclude explicitly that the current frame cannot reach that bar from the available evidence
9. compare before promotion instead of overwriting first

That lifecycle is the cross-package default. Package READMEs can add local surfaces or exceptions, but they should not redefine the shared process when a tracked workflow already exists here.

## When To Use Which Surface

Use these surfaces differently:

| Surface | Use It For | Do Not Use It For |
| :--- | :--- | :--- |
| [`paper-intake/README.md`](paper-intake/README.md) | local evidence storage, PDF download destination, markdown conversion, and `papers/index.md` maintenance once a paper is clearly in scope | broad discovery, loose literature browsing, or framing debates before the paper is selected |
| [`alphaxiv-research/README.md`](alphaxiv-research/README.md) | broad discovery, shortlist refinement, and narrow claim pressure-testing against exact anchor papers | acting as the package’s long-term evidence store or replacing the package blueprint |
| [`essay-iteration/README.md`](essay-iteration/README.md) | rewrite-governing blueprints, bounded draft cycles, brutal review artifacts, cold replacement reviews, and the compare-before-promotion loop | paper retrieval or package evidence storage |

Blueprint hardening is therefore a named cross-cutting mode rather than a separate top-level workflow. It spans essay iteration, targeted alphaXiv validation, and selective paper intake when the claim set actually changes.

For evidence-sensitive rewrites, the default order is therefore:

1. paper intake
2. blueprint hardening
3. optional external blueprint review with writer adjudication
4. essay prewrite gate
5. bounded article rewrite

After a blocking high-bar review, return to step 2 rather than generating another loose rewrite candidate.

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
