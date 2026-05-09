# Scripts

This directory holds the tracked repo-level automation code. These scripts are the implementation layer behind several content workflows, mirrors, and publication tasks. Start with the tracked workflow docs in [`../workflows/README.md`](../workflows/README.md), then use the tracked skill bundles under [`../workflows/skills/`](../workflows/skills/README.md) when you need execution help. This file explains what each script in this folder does.

## How To Read This Folder

- Start here when you need to understand a root-level automation workflow.
- Treat blueprint hardening and alphaXiv validation as workflow-and-skill processes, not root-script entrypoints. They currently have no dedicated root script by design because they depend on judgment and evidence review rather than fixed automation.
- Use `npm run ...` entry points when they exist instead of calling lower-level scripts by habit.
- Treat `archive_utils.py` as a support module, not a user-facing entrypoint.

## Script Scope Policy

The default rule is: root-level scripts should be generic repo automation. A script may show a package name in CLI help text as an example when it still accepts `--package` or another generic selector. A script becomes a Phase 1 exception when it hardcodes one package, one series, or one migration context into its behavior.

Current root-script status: no accepted package-specific root-script exceptions. Temporary cross-package experiment toolchains are allowed only when they are indexed in [`../experiments/README.md`](../experiments/README.md) and tied back to a workflow.

Retired or moved exceptions:

| Script | Decision | Current Location |
| :--- | :--- | :--- |
| `stitch_binding_gap_slides.py` | Removed. The one-off Binding Gap slide utility was not a root workflow. | Retired. |
| `sync_operating_agents_substack.py` | Moved to the Operating Agents umbrella package because it is a series adapter, not root automation. | [`../publications/autonomous-agents/scripts/sync_operating_agents_substack.py`](../publications/autonomous-agents/scripts/sync_operating_agents_substack.py) |
| `update_initial_status.py` | Removed. Historical lifecycle bootstrap is no longer a day-to-day command. | Retired. |

Non-exceptions:

- `check_repo_links.py` can name legacy paths because its job is to detect migration residue.
- Generic package scripts such as `render_publication_video.py`, `upload_publication_tldrs.py`, and `upload_publication_shorts.py` can mention example package names if the actual package remains a CLI argument.

## Lifecycle / Status Automation

These scripts keep the publication lifecycle contracts, manifests, and refinement cycles coherent. They are the automation layer behind `content-agent`, workflow validation, and package-local support tools, but they do not replace the workflow docs that define how the work should actually be done.

For source-of-truth and operator-surface questions, read [`../AUTHORITY.md`](../AUTHORITY.md) first. Governed execution should use `./content-agent` over `workflow.yaml`, root policy/profile/gate YAMLs, and package `status.yaml`. The older `stage:*`, `workflow:*`, `gate:check`, and generic `npm run run` compatibility commands are retired from the active package script surface.

Routine lifecycle records from this layer belong in [`../reviewable-runs/logs/`](../reviewable-runs/logs/README.md), not in the retained proof surface under `reviewable-runs/examples/proofs/`. For scaffolded `essay_iteration`, the log records the scaffold event while the canonical working packet lives under the leaf's `iterations/r<revision>/` directory.

Use `npm run check` as the lightweight pre-review validation bundle. It runs workflow YAML validation, workflow-model validation, content-agent validation readiness, Reviewable Runs log validation, repo-link validation, and alphaXiv discussion tracking. It intentionally excludes mirror builds, publication sync, and other external or heavier checks.

When a workflow declares runtime inputs, `content-agent.py` expects them as repeatable `--input key=value` arguments on both `validate` and `run`; the resolved-run evidence records the admitted values.

Tracked docs:

- [`../workflows/README.md`](../workflows/README.md)
- [`../workflows/essay-iteration/README.md`](../workflows/essay-iteration/README.md)

| Script | Role | Normal Entry Point | Notes |
| :--- | :--- | :--- | :--- |
| `lifecycle.py` | Shared lifecycle constants plus the generic workflow/gate/profile contract loader used by the other lifecycle scripts. | imported by other scripts | This is the contract layer, not a direct user command. |
| `harness.py` | Shared helpers for policy loading, context resolution, stage composition, workflow resolution, gate evaluation, package initialization, and legacy log readers still consumed by `content-agent` and validators. | imported by other scripts | Shared library only; it is not a user-facing compatibility command surface. |
| `essay_iteration_support.py` | Shared helpers for essay-iteration packet discovery, scaffold detection, path resolution, and packet validation constants. | imported by essay-iteration scripts | Support module, not a user-facing entrypoint. |
| `research_exit_support.py` | Shared helpers for canonical research-exit gate path construction and frontmatter/body validation constants. | imported by research-exit checks | Support module, not a user-facing entrypoint. |
| `init_status.py` | Initializes `status.yaml` manifests for publication packages. | `.venv/bin/python scripts/init_status.py --package <package>` | Use `--recursive` when bootstrapping many README-backed packages. |
| `sync_status_schema.py` | Adds missing lifecycle stages and leaf defaults to existing manifests after schema changes. | `.venv/bin/python scripts/sync_status_schema.py` | Maintenance helper when the tracked stage list changes. |
| `check_status.py` | Prints the leaf-package lifecycle matrix across `publications/`. | `.venv/bin/python scripts/check_status.py` | Fast visibility into current package state. |
| `check_package_lifecycle.py` | Checks one package for stage/README drift, governing-brief resolution, and packet-scaffold consistency. | `npm run check:package-lifecycle -- --package <leaf-package>` | Advisory lifecycle guardrail surface and the machine-readable input used by the local Stop hook. |
| `check_notebooklm_registry.py` | Validates NotebookLM notebook mappings from `post_map.yaml` to package `status.yaml`, checks restricted URL/ID consistency, and can resolve IDs through the NotebookLM CLI with `--live`. | `.venv/bin/python scripts/check_notebooklm_registry.py` | Use after adding or changing publication NotebookLM mappings. |
| `check_alphaxiv_discussions.py` | Validates that package notes mentioning alphaXiv assistant session ids are indexed in package-local `research-notes/alphaxiv-discussions/index.md` files. | `npm run check:alphaxiv-discussions` | Use after alphaXiv assistant sessions materially shape package claims, vocabulary, or paper queues. |
| `content_agent.py` | Implements the Phase 2 `content-agent` facade over `workflow.yaml`, root policy/profile/gate YAMLs, package `status.yaml`, context admission, tool/path posture, gate readiness, trace readiness, gate checks, and Phase 2 YAML execution evidence. | `./content-agent status`, `./content-agent next`, `./content-agent validate`, `./content-agent run`, `./content-agent gate check`, or `./content-agent review list` | Validation, status, next, and gate checks are read-only except for evidence logs. Review decisions are the explicit file-backed gate mutation path and do not move lifecycle state, publish, or promote outputs. |
| `content_cockpit.py` | Serves the Phase 2.5/2.6 local cockpit over `content-agent` status, next-action, review-gate, run-record, validation, review-decision, and report-only editorial commands. | `npm run cockpit -- --package <package>` or `./content-cockpit --package <package>` | Cockpit actions call existing repo commands. It does not run arbitrary jobs, edit packages, move lifecycle state, publish, or promote outputs. |
| `generate_editorial_report.py` | Generates the Phase 2.6 structured article-polish editorial report from the package `status.yaml` live draft and `voice_consistency_guide.md`. | `npm run editorial:report -- --package <package>` or `.venv/bin/python scripts/generate_editorial_report.py --package <package> --stdout` | Report-only automation. It records findings and source-improvement suggestions without rewriting drafts, approving gates, moving lifecycle state, publishing, or promoting outputs. |
| `init_package.py` | Bootstraps a minimal leaf package from an idea or a canonical topic-discovery packet and seeds a runnable `status.yaml`. | `npm run package:init -- --idea "..."` or `npm run package:init -- --from-topic-packet <packet>` | Creates the harness-first idea-to-package scaffold. |
| `init_essay_iteration_packet.py` | Seeds the package-local essay packet under `iterations/r<revision>/` beside the live draft's directory using the tracked essay-iteration templates. | `.venv/bin/python scripts/init_essay_iteration_packet.py --package <leaf-package>` | Called by the `essay_iteration` workflow's scriptable scaffold step under `./content-agent run`. |
| `check_essay_iteration_packet.py` | Validates the package-local essay packet for required headings, prewrite-gate state, anchors, policy limits, and machine-checkable voice violations. | `npm run check:essay-prewrite -- --package <leaf-package>` or `npm run check:essay-iteration -- --package <leaf-package>` | Use the prewrite command before opening a bounded candidate; use the full packet command before claiming the packet is ready for review. |
| `check_research_exit_gate.py` | Validates the canonical package-local research-exit gate artifact. | `.venv/bin/python scripts/check_research_exit_gate.py --package <leaf-package>` | Use before clearing `research` into `essay_iteration`. |
| `check_workflow_model.py` | Validates workflow/gate/profile contracts, content-agent validation readiness, plus the lightweight workflow-model fixtures. | `npm run check:workflow-model` | Use this after changing modular routing, gates, validation posture, or reusable workflow behavior. |
| `check_workflow_yaml_contracts.py` | Validates authored Phase 2 `workflow.yaml` contracts for v1 shape, README drift, gate references, hook references, output references, and allowed-path coverage. | `npm run check:workflow-yaml` | Also runs as part of `npm run check:workflow-model`; use the narrow command while authoring new workflow contracts. |
| `check_reviewable_run_logs.py` | Validates the current lightweight Reviewable Runs log schema for lifecycle logs, workflow logs, gate checks, and launch packs. | `npm run check:reviewable-runs` | Use this after changing run logging, launch packs, gate checks, or Reviewable Runs log policy. |
| `install_codex_stop_hook.py` | Creates or refreshes the repo-local `.codex/` Stop-hook mirror from the tracked hook assets under `scripts/codex_hooks/`. | `.venv/bin/python scripts/install_codex_stop_hook.py` | Keeps `.codex/` local-only while preserving the hook logic as tracked repo documentation and code. |
| `start_refinement.py` | Starts a new refinement cycle by bumping revision, optionally syncing from archive, and resetting selected stages. | `.venv/bin/python scripts/start_refinement.py --package <package> --reset <stage,...>` | The main automation entrypoint for a new bounded rewrite cycle. |
| `sync_from_archive.py` | Copies a published archive snapshot back into a package, updates `status.yaml` with the resolved markdown path and slug, and backfills referenced archive assets into the package-local `assets/` folder. | `.venv/bin/python scripts/sync_from_archive.py --package <package>` | Used directly and by `start_refinement.py`. |
| `import_substack_draft_to_archive.py` | Manual-import helper for unpublished Substack drafts: fetches draft metadata, writes a tracked markdown and HTML snapshot into `publication_strategy_and_archive/substack_archive/`, localizes any referenced local assets, and updates `metadata.json`. | `.venv/bin/python scripts/import_substack_draft_to_archive.py --post-id <id> --markdown <path>` | Use when a draft exists on Substack but is intentionally not yet in the public archive. |
| `audit_package.py` | Runs an advisory structural and evidence-drift audit for one package. | `.venv/bin/python scripts/audit_package.py --package <package>` | Used directly and by shared lifecycle resolution helpers. |

## Local Codex Hook Mirror

Tracked repo-supported Codex hook assets live under [`codex_hooks/`](codex_hooks/README.md). The live activation path remains the local `.codex/` folder, which stays gitignored.

Use the installer when you want the repo-local `Stop` hook backstop:

```bash
.venv/bin/python scripts/install_codex_stop_hook.py
```

Keep the same source/mirror split used for repo skills:

- tracked docs and scripts here are canonical
- `.codex/` is only the local activation mirror
- the hook is advisory infrastructure, not the source of truth for lifecycle policy

## Publication / Archive Automation

These scripts maintain the tracked Substack archive in `publication_strategy_and_archive/` and validate the Eleventy mirror.

Tracked workflow:

- [`../workflows/substack-archive-sync/README.md`](../workflows/substack-archive-sync/README.md)

| Script | Role | Normal Entry Point | Related Skill |
| :--- | :--- | :--- | :--- |
| `sync_substack_archive.py` | Canonical archive refresh: discovers public posts, localizes assets, writes markdown and HTML snapshots, updates `metadata.json`, and regenerates the root README publication table. | `npm run sync:substack` | [`substack-archive-sync`](../workflows/skills/substack-archive-sync/SKILL.md) |
| `generate_editorial_atlas.py` | Generates `publication_strategy_and_archive/editorial_atlas/atlas_data.json` from complete model-specific `publication_strategy_and_archive/editorial_atlas/rubric_assessments_*.yaml` files and can verify that the checked-in atlas still matches the rubric sources. | `npm run sync:editorial-atlas` | none |
| `editorial_atlas_utils.py` | Shared rubric-source validation and atlas derivation helpers used by the generator and mirror checks. | imported by other scripts | none |
| `archive_utils.py` | Shared paths and helpers for the archive manifest, `post_map.yaml`, and README table generation. | imported by other scripts | [`substack-archive-sync`](../workflows/skills/substack-archive-sync/SKILL.md) |
| `check_mirror.py` | Structural validation for the archive, editorial atlas, and built mirror output. Checks metadata keys, rubric-derived atlas generation, archive files, asset references, generated README section, and built internal links. | `npm run check:mirror` | [`substack-archive-sync`](../workflows/skills/substack-archive-sync/SKILL.md) |
| `check_repo_links.py` | Validation pass for stale old-package paths, broken relative links, and outdated internal GitHub repo links after the `publications/` migration. | `npm run check:repo-links` | none |
| `e2e_mirror_smoke.py` | Runtime smoke test for the built mirror at both root and prefixed path layouts. | `npm run check:mirror` | [`substack-archive-sync`](../workflows/skills/substack-archive-sync/SKILL.md) |

### Operating Agents Substack Publishing

This workflow republishes the Operating Agents essay set from repo markdown to live Substack posts.

Tracked workflow:

- [`../workflows/substack-publishing/README.md`](../workflows/substack-publishing/README.md)

| Script | Role | Normal Entry Point | Related Skill |
| :--- | :--- | :--- | :--- |
| `../publications/autonomous-agents/scripts/sync_operating_agents_substack.py` | Republishes the preface and six essay posts, preserves the embedded video block, rewrites published essay links to Substack URLs, and retries on Substack rate limits. | `.venv/bin/python publications/autonomous-agents/scripts/sync_operating_agents_substack.py` | [`operating-agents-substack-sync`](../workflows/skills/operating-agents-substack-sync/SKILL.md) |

### Generic Substack Draft Sync

This workflow updates one existing Substack draft from a canonical local markdown file without driving the browser UI.

Tracked workflow:

- [`../workflows/substack-publishing/README.md`](../workflows/substack-publishing/README.md)

| Script | Role | Normal Entry Point | Related Skill |
| :--- | :--- | :--- | :--- |
| `sync_markdown_post_to_substack.py` | Syncs one markdown file into one existing Substack draft, uploads local images, preserves or injects the draft's uploaded video block when the markdown uses a `#### Video TL;DR` section, and can reuse a logged-in Chrome session over CDP to mint the auth cookie string. | `.venv/bin/python scripts/sync_markdown_post_to_substack.py --publication-url https://<subdomain>.substack.com --post-id <id> --markdown <file> --chrome-debug-url http://127.0.0.1:9222` | none |

## Media / Render Automation

These scripts handle the local production stage for narrated slide videos before any YouTube upload or replacement step.

Tracked workflows:

- [`../workflows/youtube-production/README.md`](../workflows/youtube-production/README.md)
- [`../workflows/youtube-channel-ops/README.md`](../workflows/youtube-channel-ops/README.md)
- [`../workflows/youtube-series-operating-agents/README.md`](../workflows/youtube-series-operating-agents/README.md)

| Script | Role | Typical Use | Related Skill |
| :--- | :--- | :--- | :--- |
| `align_slides_to_transcript.py` | Drafts slide timing from OCR plus an untimestamped transcript and audio duration. | first-pass alignment | [`youtube-slide-video-pipeline`](../workflows/skills/youtube-slide-video-pipeline/SKILL.md) |
| `align_slides_to_captions.py` | Drafts slide timing from OCR plus timed SRT captions and can blend OCR from complementary slide directories that share the same filenames. | first-pass alignment with captions | [`youtube-slide-video-pipeline`](../workflows/skills/youtube-slide-video-pipeline/SKILL.md) |
| `build_slideshow_from_captions.py` | Drafts a cue sheet from timed SRT captions plus slide OCR, can blend complementary OCR slide decks, and can render a first-pass MP4 while interleaving multiple render slide directories that share the same filenames. | caption-first draft render | [`youtube-slide-video-pipeline`](../workflows/skills/youtube-slide-video-pipeline/SKILL.md) |
| `map_slides_to_transcript_lines.py` | Drafts transcript line ranges from OCR text files and a numbered transcript. | line-range drafting | [`youtube-slide-video-pipeline`](../workflows/skills/youtube-slide-video-pipeline/SKILL.md) |
| `line_map_markdown_to_cues.py` | Converts a reviewed markdown line map plus timed captions into the final cue-sheet JSON used for rendering. | verified cue generation | [`youtube-slide-video-pipeline`](../workflows/skills/youtube-slide-video-pipeline/SKILL.md) |
| `render_audio_slides_video.py` | Generates a rough evenly spaced template or renders the final MP4 from a cue sheet. | template or final render | [`youtube-slide-video-pipeline`](../workflows/skills/youtube-slide-video-pipeline/SKILL.md) |
| `render_publication_video.py` | Thin convenience wrapper that renders one package's final publication video from its prepared cues. | package-level final render | [`youtube-slide-video-pipeline`](../workflows/skills/youtube-slide-video-pipeline/SKILL.md) |
| `create_publication_shorts_from_longform.py` | Slices a verified long-form MP4 into named short clips from a manifest and renders portrait Shorts variants. | package-level Shorts derivation from one long-form video | [`youtube-slide-video-pipeline`](../workflows/skills/youtube-slide-video-pipeline/SKILL.md) |
| `convert_landscape_videos_to_portrait.py` | Converts landscape MP4 clips into portrait `9:16` versions by centering the original frame over a blurred vertical background, keeping output in a standard `H.264`/`AAC` web-delivery envelope. | prep horizontal clips for Shorts-style upload | [`youtube-slide-video-pipeline`](../workflows/skills/youtube-slide-video-pipeline/SKILL.md) |
| `probe_shorts_media.py` | Probes portrait Shorts masters for dimensions, audio, duration, and JSON-reportable preflight status. | verify Shorts media before upload | [`youtube-data-api`](../workflows/skills/youtube-data-api/SKILL.md) |
| `scrape_youtube_watch_transcript.py` | Scrapes the visible watch-page transcript panel into JSON when you need a browser fallback for transcript inspection. | transcript fallback or debugging | [`youtube-slide-video-pipeline`](../workflows/skills/youtube-slide-video-pipeline/SKILL.md) |

## YouTube Analytics And Experiment Tooling

These scripts support cross-package YouTube experiments tracked under [`../experiments/`](../experiments/README.md). They are not package lifecycle runners.

| Script | Role | Typical Use | Related Workflow |
| :--- | :--- | :--- | :--- |
| `refresh_youtube_analytics_dashboard.py` | Runs the full read-only YouTube analytics refresh in dependency order and writes a compact dashboard snapshot. | one-command refresh for `../experiments/youtube-analytics/` before review | [`youtube-channel-ops`](../workflows/youtube-channel-ops/README.md) |
| `fetch_youtube_analytics.py` | Fetches read-only YouTube Analytics and video metadata into the local analytics ledger. | update `../experiments/youtube-analytics/metrics_ledger.json` before a recommendation pass | [`youtube-channel-ops`](../workflows/youtube-channel-ops/README.md) |
| `sync_youtube_reporting_reports.py` | Downloads delayed YouTube Reporting API CSV exports and merges reach/card data into the analytics ledger. | refresh thumbnail impressions, CTR, card, and reach fields after fetch | [`youtube-channel-ops`](../workflows/youtube-channel-ops/README.md) |
| `analyze_youtube_srt_content.py` | Builds a caption-derived content rubric from videos in the analytics ledger. | generate `../experiments/youtube-analytics/content_rubric.json` for dashboard review | [`youtube-channel-ops`](../workflows/youtube-channel-ops/README.md) |
| `build_youtube_decision_report.py` | Builds recommendation-only weekly YouTube decision reports from the analytics ledger and decision rules. | generate `../experiments/youtube-analytics/weekly_reports/` without mutating the channel | [`youtube-channel-ops`](../workflows/youtube-channel-ops/README.md) |
| `build_youtube_analytics_dashboard.py` | Builds a static local dashboard from the analytics ledger and latest recommendation report. | generate `../experiments/youtube-analytics/dashboard/index.html` for weekly review | [`youtube-channel-ops`](../workflows/youtube-channel-ops/README.md) |
| `build_youtube_reference_comment_draft.py` | Extracts a local essay bibliography or references section into a short YouTube comment draft with a curated source list and essay back-link. | seed `../experiments/youtube-reference-comments/` draft comments before any manual posting decision | draft-only experiment, no stable owner workflow yet |
| `insight_authority_experiment.py` | Validates Insight Authority packets, renders plain-language YouTube metadata, strips AI wrapper suffixes, enforces release cadence, creates minimalist PNG thumbnails, and writes local emit/publish plan files. | dry-run packet review or `--apply` for local plan and thumbnail artifacts; never mutates YouTube state | local experiment helper, no stable owner workflow yet |
| `prepare_overlay_remaster_backfill.py` | Prepares overlay-remaster Shorts manifests and a crosswalk report for a multi-package backfill. | create or refresh rollout remaster planning state under `../experiments/youtube-cinematic-rollout/` | [`youtube-cinematic-rollout`](../workflows/youtube-cinematic-rollout/README.md) |
| `sync_overlay_remaster_uploads.py` | Syncs overlay-remaster crosswalk items from generated upload reports. | update remaster crosswalk state after upload reports exist | [`youtube-cinematic-rollout`](../workflows/youtube-cinematic-rollout/README.md) |
| `mark_overlay_remaster_studio_verified.py` | Marks overlay-remaster items as Studio related-video verified. | record manual Studio verification in the remaster crosswalk | [`youtube-cinematic-rollout`](../workflows/youtube-cinematic-rollout/README.md) |
| `unlist_overlay_remaster_old_shorts.py` | Unlists old Shorts after verified overlay remaster uploads. | guarded cleanup after remasters are uploaded and related-video verification is recorded | [`youtube-channel-ops`](../workflows/youtube-channel-ops/README.md) |

## Thin Operational Wrappers

These scripts are thin wrappers around workflow or skill behavior. They remain generic enough for the root script surface.

| Script | Role | Notes |
| :--- | :--- | :--- |
| `list_youtube_videos.py` | Lists videos from the authenticated YouTube channel. | Thin wrapper around the YouTube skill script layer. Use [`../workflows/youtube-channel-ops/README.md`](../workflows/youtube-channel-ops/README.md) for the canonical process. |
| `upload_publication_tldrs.py` | Uploads TL;DR video variants from one package into a playlist. | Thin publication wrapper around the YouTube API helper stack; package selection is an argument. |
| `upload_publication_cinematic.py` | Uploads one manifest-driven cinematic companion, creates or reuses the shared cinematic playlist, cross-links back to the configured research-breakdown surface in the description, and writes a publication-local upload report. | Works with both the bounded pilot manifest and the evergreen rollout backlog manifest. Defaults to dry-run. |
| `wait_for_youtube_captions.py` | Polls YouTube caption availability and downloads the first matching caption track once it appears. | Use for cinematic rollout caption recovery after upload. Defaults to 10-minute polling for up to 2 hours, matching the rollout manifest defaults. |
| `upload_publication_shorts.py` | Uploads portrait Shorts variants for one package, adds them to a Shorts playlist, links them back to the main long-form video, can schedule release times from a manifest, and writes an upload/readback report. | Supports both the canonical `artifacts/video/shorts/portrait` folder and run-specific `--shorts-dir` overrides such as daily rollout batches. Defaults to dry-run and preflights local media. After upload, verify the related-video card in YouTube Studio and reload the edit page before treating the batch as complete. |
| `run_daily_cinematic_rollout.py` | Syncs the evergreen cinematic backlog, performs the NotebookLM auth preflight, schedules approved Shorts, materializes package-local rollout manifests, and appends the daily release ledger. | Use with [`../workflows/youtube-cinematic-rollout/README.md`](../workflows/youtube-cinematic-rollout/README.md). Defaults to dry-run. This helper only reconciles and schedules state; the active automation run should still keep polling every 10 minutes until in-flight uploads, captions, Shorts, and Studio verification are complete. |
| `extract_cinematic_short_candidates.py` | Extracts transcript-aligned cinematic Shorts candidates from a timed SRT, scores them heuristically against the rollout rubric, and writes a shortlist report beside the package artifacts. | Use as the first pass before manually promoting `approved_clips` into the rollout backlog manifest. |
| `upload_ad_hoc_shorts.py` | Uploads arbitrary local portrait clips, or converts landscape clips first, then links them to a long-form video and writes an upload/readback report. | Use for downloaded or manually edited clips outside a package's canonical Shorts folder. Defaults to dry-run and preflights local media. |

## Related Skill Split

Some adjacent automation lives outside this folder:

- YouTube channel-management, caption download, temporary upload transcript recovery, playlist diagnostics, generic publication bundle uploads, Shorts maintenance, and replacement uploads live under [`../workflows/skills/youtube-data-api/scripts/`](../workflows/skills/youtube-data-api/scripts/) and are documented canonically in [`../workflows/youtube-channel-ops/README.md`](../workflows/youtube-channel-ops/README.md) and [`../workflows/youtube-series-operating-agents/README.md`](../workflows/youtube-series-operating-agents/README.md).
- PDF slide export lives under [`../workflows/skills/pdf-slides-to-substack-images/scripts/`](../workflows/skills/pdf-slides-to-substack-images/scripts/).
- NotebookLM, blueprint hardening, and alphaXiv validation are documented canonically under [`../workflows/`](../workflows/README.md) and do not use this root `scripts/` folder as their main implementation surface.

## Safe Starting Points

If you only need the normal repo entrypoints, start with:

```bash
npm run sync:substack
npm run sync:editorial-atlas
npm run check:mirror
npm run check:repo-links
PYTHONUNBUFFERED=1 .venv/bin/python publications/autonomous-agents/scripts/sync_operating_agents_substack.py
```

For YouTube production work, start with [`../workflows/youtube-production/README.md`](../workflows/youtube-production/README.md) before calling the lower-level scripts directly.
