# Workflows

This directory is the tracked canonical playbook layer for `/Users/petros/Projects/content`.

Use package READMEs to understand local structure. Use the workflow docs here to understand the repeatable process. Use tracked skill bundles under [`skills/`](skills/README.md) only after the workflow is clear.

The current defaults in this directory were tightened against recurring March-April 2026 rollout patterns. When the idealized process diverged from what actually worked in the rollouts, the workflow docs were rewritten toward the observed practice.

## Current Workflow Map

Read the workflow layer by group first, then by individual doc. The `workflow_group` frontmatter uses this taxonomy.

| Group | Workflow | Use When | Related Skill Bundle |
| :--- | :--- | :--- | :--- |
| package | [`package-normalization/README.md`](package-normalization/README.md) | normalizing package shape, manifests, evidence paths, artifact homes, and scaffold expectations | none |
| portfolio | [`topic-discovery/README.md`](topic-discovery/README.md) | deciding whether a broad idea, archive gap, research seam, or capped-essay successor deserves a package, pivot pass, or no further work | [`skills/alphaxiv/`](skills/alphaxiv/) as the execution layer |
| evidence | [`paper-intake/README.md`](paper-intake/README.md) | promoting already-selected papers into the package evidence surface, converting PDFs to markdown, and maintaining the paper index | [`skills/markitdown-paper-intake/`](skills/markitdown-paper-intake/) |
| evidence | [`alphaxiv-research/README.md`](alphaxiv-research/README.md) | discovering papers, refining a shortlist, and pressure-testing active claims against anchor papers before intake | [`skills/alphaxiv/`](skills/alphaxiv/) |
| evidence | [`evidence-authorization/README.md`](evidence-authorization/README.md) | creating a claim-permission layer between a package source index and a blueprint when evidence-sensitive rewrites risk overclaiming | package-local source index plus blueprint/review artifacts |
| editorial | [`essay-iteration/README.md`](essay-iteration/README.md) | hardening blueprints, running review and rewrite cycles, and maintaining live-draft/archive discipline | package-local docs plus review artifacts |
| editorial | [`post-ceiling-pivot/README.md`](post-ceiling-pivot/README.md) | **experimental**: a flagship essay has clearly capped out and the package needs a research-grounded pivot before opening a new flagship object | package-local stop-gate findings plus [`alphaxiv-research/README.md`](alphaxiv-research/README.md) |
| artifacts | [`notebooklm-artifacts/README.md`](notebooklm-artifacts/README.md) | generating audio, slide, and video artifacts and downloading them into package artifacts | [`skills/notebooklm-artifact-bundle/`](skills/notebooklm-artifact-bundle/), [`skills/pdf-slides-to-substack-images/`](skills/pdf-slides-to-substack-images/) |
| artifacts | [`youtube-production/README.md`](youtube-production/README.md) | turning slide decks, transcripts, captions, and audio into a verified MP4 before upload | [`skills/youtube-slide-video-pipeline/`](skills/youtube-slide-video-pipeline/) |
| release | [`article-polish/README.md`](article-polish/README.md) | naming and placing images, transcript round-trips, rehumanizing the draft, and final reference cleanup before the release gate | package-local docs plus NotebookLM/PDF helpers |
| release | [`release-gate/README.md`](release-gate/README.md) | checking draft integrity, evidence, references, media paths, Substack targets, and approval boundaries before external mutation | package-local release checklist |
| release | [`substack-publishing/README.md`](substack-publishing/README.md) | preparing and publishing essays to Substack and syncing their public presentation after release approval | package-local docs plus Substack helpers |
| release | [`substack-archive-sync/README.md`](substack-archive-sync/README.md) | refreshing the tracked public archive, validating the mirror, and using the manual-import fallback | [`skills/substack-archive-sync/`](skills/substack-archive-sync/) |
| distribution | [`distribution/README.md`](distribution/README.md) | handling post-publication distribution work for the channels that matter to a package | package-local `distribution/` or `socials/` surfaces |
| operations | [`youtube-channel-ops/README.md`](youtube-channel-ops/README.md) | authenticated YouTube channel work such as OAuth checks, caption recovery, playlist diagnostics, and Shorts maintenance | [`skills/youtube-data-api/`](skills/youtube-data-api/), [`skills/youtube-shorts-maintenance/`](skills/youtube-shorts-maintenance/) |
| operations | [`youtube-series-operating-agents/README.md`](youtube-series-operating-agents/README.md) | the Operating Agents YouTube series layer: TL;DR uploads, cross-links, playlist order, and replacement uploads | [`skills/youtube-operating-agents/`](skills/youtube-operating-agents/), [`skills/youtube-data-api/`](skills/youtube-data-api/) |

## Working Hierarchy

The April 2026 neural-architecture pilot made one structural fact clearer: this repo needs a layered reading order, not just a flat stage list.

Use the layers like this:

| Layer | Main Question | Canonical Surface |
| :--- | :--- | :--- |
| package context | what publication object am I actually changing? | `status.yaml` first, then package `README.md` / leaf `README.md`, then the governing brief named by `config.blueprint_path` when present |
| lifecycle workflow | what kind of work am I doing right now? | the relevant tracked workflow doc in this directory |
| execution help | which commands, helper scripts, or repo-local skills actually perform it? | [`skills/`](skills/README.md) and [`../scripts/README.md`](../scripts/README.md) |
| routine run record | what happened in this bounded operational run? | [`../reviewable-runs/logs/README.md`](../reviewable-runs/logs/README.md) |
| retained proof | which runs are strong enough to preserve as reviewable-run examples? | [`../reviewable-runs/examples/proofs/README.md`](../reviewable-runs/examples/proofs/README.md) |

That separation matters. Workflow docs explain the process. Skills and scripts execute the process. Reviewable Runs records what happened. Those are different layers and should not collapse into one another.

## Sandbox And Permission Failures

Some agents run inside stricter filesystem, browser, or macOS permission boundaries than the terminal user. If a command fails with `Operation not permitted`, `permission denied`, sandbox denial, browser-auth failure, or an inaccessible hidden/cache directory, do not keep retrying the same command and do not invent the missing artifact.

Use this escalation pattern:

1. record the exact command, working directory, target path, and error
2. classify the blocked action as one of: repo file read/write, hidden auth state, browser/OAuth step, network download, media render, or channel mutation
3. ask for the narrow permission needed, or hand the user the exact command to run locally
4. state the expected output path and the verification command
5. continue only after the expected file or state exists and passes verification

For weaker agents, a sandbox failure is a stop condition for that operation, not a reason to produce a substitute. The correct fallback is a user-exec handoff such as:

```bash
cd /Users/petros/Projects/content
<exact command>
<verification command>
```

Auth-heavy and filesystem-sensitive steps should fail closed. This includes NotebookLM login and source export, alphaXiv browser auth, YouTube temporary uploads or caption downloads, writes into hidden folders such as `.youtube/` or `.notebooklm/`, and any operation that touches `~/Library`, `~/.gemini`, or other tool cache homes.

## Canonical Article Lifecycle

The lifecycle stage ids remain unchanged for runner compatibility. Before a package exists, or before a capped package earns a successor object, use [`topic-discovery/README.md`](topic-discovery/README.md) as the optional front door.

The working taxonomy for article development is:

1. **topic discovery**: use [`topic-discovery/README.md`](topic-discovery/README.md) when the repo is still deciding what essay object should exist, which research seam matters, or whether a capped donor package has a real successor
2. **research discovery**: use [`alphaxiv-research/README.md`](alphaxiv-research/README.md) to find and inspect candidate papers before they are admitted into a package
3. **validation**: use [`alphaxiv-research/README.md`](alphaxiv-research/README.md) in narrow claim-testing mode against the active anchor papers and package evidence surface
4. **blueprint hardening**: use [`essay-iteration/README.md`](essay-iteration/README.md) as the governing process surface, with targeted help from [`alphaxiv-research/README.md`](alphaxiv-research/README.md), [`paper-intake/README.md`](paper-intake/README.md), and [`evidence-authorization/README.md`](evidence-authorization/README.md) when evidence needs to be tightened. After a blocking high-bar review, this is the mandatory next step and must either set an outstanding-governing rewrite direction or record an explicit impossibility finding
5. **external blueprint review**: optionally use [`essay-iteration/README.md`](essay-iteration/README.md) for an advisory outside review of the hardened blueprint before the prewrite gate. The writer adjudicates the findings and integrates only what materially improves the governing surface
6. **essay prewrite gate**: use [`essay-iteration/README.md`](essay-iteration/README.md) to decide whether an outstanding essay is actually writable before prose drafting begins. This step must either produce an essay-governing prewrite surface or an explicit blocker. In the generic workflow it now lives inside the `essay_iteration` packet rather than as a new lifecycle stage
7. **draft iteration**: use [`essay-iteration/README.md`](essay-iteration/README.md) to seed the package-local essay packet, produce bounded rewrite candidates beside the live draft, and compare before promotion
8. **production and release**: use NotebookLM, polish, release-gate, publishing, archive-sync, distribution, and video workflows once the live draft is ready for outward-facing work

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

For real end-to-end work, treat those flat stage ids as a compatibility layer over a more useful hierarchy:

1. **Portfolio and topic selection**: topic discovery before package init, or post-ceiling pivot when a capped package needs a successor object
2. **Evidence shaping**: `paper_intake`, `research`, evidence authorization when a claim-permission layer is needed
3. **Draft governance and rewrite**: `essay_iteration`
4. **Package media production**: `notebooklm_artifacts`, `article_polish`, `youtube_production`
5. **Publication and outward release**: release gate, `substack_publishing`, `archive_sync`, `distribution`

Two adjacent operational surfaces often appear during a real rollout but are not default `status.yaml` stages:

- [`youtube-channel-ops/README.md`](youtube-channel-ops/README.md): channel-side upload, captions, playlist mutation, and Shorts release work
- [`youtube-series-operating-agents/README.md`](youtube-series-operating-agents/README.md): series-specific YouTube operations that do not belong in a generic article lifecycle

This distinction is intentional. `youtube_production` ends at a verified local MP4. Channel mutation is a separate operational boundary with different auth, quota, and approval risks.

For refinement cycles on an existing essay, the recurring April 2026 pattern is:

1. intake missing papers into the package evidence surface if the active claims still rely on temporary or alphaXiv-only context
2. harden the package blueprint if it is still fuzzy, under-evidenced, or outrunning the current anchor set
3. optionally run an external blueprint review, but keep it advisory and adjudicate the fixes as the writer
4. run the essay prewrite gate before drafting: either produce an essay-governing prewrite surface or conclude explicitly that the essay is not yet writable at the target bar
5. keep confidence-debt-style or package-local proof notes as optional support, but express the actual draft-authorization verdict through the packet's prewrite gate
6. use alphaXiv in targeted validation mode against the active anchor papers when needed
7. run `stage:run` for `essay_iteration` to seed or refresh the package-local packet beside the stable live draft
8. fill that packet with a bounded candidate, replacement review, scorecard, and decision artifact
9. run the packet validator before claiming the packet is ready for review
10. compare before promotion instead of overwriting first
11. if that review does not clear promotion, return immediately to blueprint hardening at the same top bar: either produce an outstanding-governing blueprint or conclude explicitly that the current frame cannot reach that bar from the available evidence

If that cycle ends in an explicit frame ceiling rather than a rewrite path, do not keep iterating locally by default. Use the experimental [`post-ceiling-pivot/README.md`](post-ceiling-pivot/README.md) workflow to decide whether a real new flagship object exists before drafting again.

The handoff between `research` and `essay_iteration` should be interpreted strictly:

- close `research` when the package has enough local evidence and claim governance to support a bounded draft candidate
- do not keep `research` open just because narrower conditional follow-on reading might still improve a later section
- carry those conditional triggers into `essay_iteration` instead of using them as a stage blocker

For package-stage decisions, read the package surfaces in this order:

1. `status.yaml`
2. package `README.md`
3. the workflow doc for the target stage
4. the governing brief named by `config.blueprint_path` when present
5. packet or review artifacts only when the stage actually needs them

That lifecycle is the cross-package default. Package READMEs can add local surfaces or exceptions, but they should not redefine the shared process when a tracked workflow already exists here.

For `essay_iteration`, `stage:run` now means “seed or refresh the package-local packet scaffold.” It does not mean “complete the rewrite stage automatically.” Promotion, stage completion, and top-tier score claims remain gated behind stronger review or human approval.

## When To Use Which Surface

Use these surfaces differently:

| Surface | Use It For | Do Not Use It For |
| :--- | :--- | :--- |
| [`topic-discovery/README.md`](topic-discovery/README.md) | deciding whether a broad idea, research seam, archive gap, or capped-essay successor should become a package, pivot pass, or parked idea | storing papers, replacing package-local research, or drafting before the handoff decision is explicit |
| [`package-normalization/README.md`](package-normalization/README.md) | checking or repairing package shape, status manifests, canonical draft pointers, evidence paths, artifact homes, and archive expectations | rewriting an essay or deciding whether an argument is publication-worthy |
| [`paper-intake/README.md`](paper-intake/README.md) | local evidence storage, PDF download destination, markdown conversion, and `papers/index.md` maintenance once a paper is clearly in scope | broad discovery, loose literature browsing, or framing debates before the paper is selected |
| [`alphaxiv-research/README.md`](alphaxiv-research/README.md) | broad discovery, shortlist refinement, and narrow claim pressure-testing against exact anchor papers | acting as the package’s long-term evidence store or replacing the package blueprint |
| [`evidence-authorization/README.md`](evidence-authorization/README.md) | mapping sources to the claims they are allowed to license, naming synthesis boundaries, forbidden claims, and source burdens | storing papers, discovering new papers, or replacing the blueprint |
| [`essay-iteration/README.md`](essay-iteration/README.md) | rewrite-governing blueprints, bounded draft cycles, brutal review artifacts, cold replacement reviews, and the compare-before-promotion loop | paper retrieval or package evidence storage |
| [`release-gate/README.md`](release-gate/README.md) | final publish-readiness checks for draft target, references, media paths, Substack targets, approval boundaries, and archive follow-through | improving prose, discovering sources, or bypassing required external-mutation approval |

Blueprint hardening is therefore a named cross-cutting mode rather than a separate top-level workflow. It spans essay iteration, targeted alphaXiv validation, and selective paper intake when the claim set actually changes.

For evidence-sensitive rewrites, the default order is therefore:

1. paper intake
2. evidence authorization when the claim set is large, synthetic, or contested
3. blueprint hardening
4. optional external blueprint review with writer adjudication
5. essay prewrite gate
6. bounded article rewrite

After a blocking high-bar review, return to step 2 rather than generating another loose rewrite candidate.

## How To Use This Layer

1. Start with the relevant package `README.md`.
2. Read that package's `status.yaml` before inferring the current stage from prose.
3. Open the matching workflow doc here.
4. Load the governing brief from `config.blueprint_path` when the manifest names one.
5. Use the tracked skill bundle in [`skills/`](skills/README.md) only after the tracked workflow is clear.
6. Use [`../scripts/README.md`](../scripts/README.md) when a workflow depends on tracked repo scripts.

## Skill Bundles

Tracked repo-local skills live in [`skills/`](skills/README.md). Their `.agents/skills/` mirrors exist only so Codex can discover them locally.

Skill bundles should stay thinner than these workflow docs. They can:

- carry execution-specific commands
- point at tracked scripts
- store local-only helper logic

They should not become the only place where a shared repo process is documented.

## Local Codex Hook Mirror

The repo also supports a local `.codex/` mirror for lightweight assistive hooks. Keep the same source/mirror rule used for skills:

- tracked docs and scripts remain canonical
- `.codex/` stays local-only and gitignored
- use [`../scripts/install_codex_stop_hook.py`](../scripts/install_codex_stop_hook.py) to mirror the tracked Stop-hook assets into `.codex/`

The hook is a backstop, not a source of truth. Lifecycle correctness still belongs to `status.yaml`, workflow docs, and tracked checkers.
