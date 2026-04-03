# Scripts

This directory holds the tracked repo-level automation code. These scripts are the implementation layer behind several content workflows, mirrors, and publication tasks. Start with the tracked workflow docs in [`../workflows/README.md`](../workflows/README.md), then use the tracked skill bundles under [`../workflows/skills/`](../workflows/skills/README.md) when you need execution help. This file explains what each script in this folder does.

## How To Read This Folder

- Start here when you need to understand a root-level automation workflow.
- Use `npm run ...` entry points when they exist instead of calling lower-level scripts by habit.
- Treat `archive_utils.py` as a support module, not a user-facing entrypoint.
- Treat `stitch_binding_gap_slides.py` as a package-specific utility, not a general repo workflow.

## Primary Workflows

### Substack Archive And Mirror

These scripts maintain the tracked Substack archive in `publication_strategy_and_archive/` and validate the Eleventy mirror.

Tracked workflow:

- [`../workflows/substack-archive-sync/README.md`](../workflows/substack-archive-sync/README.md)

| Script | Role | Normal Entry Point | Related Skill |
| :--- | :--- | :--- | :--- |
| `sync_substack_archive.py` | Canonical archive refresh: discovers public posts, localizes assets, writes markdown and HTML snapshots, updates `metadata.json`, and regenerates the root README publication table. | `npm run sync:substack` | [`substack-archive-sync`](../workflows/skills/substack-archive-sync/SKILL.md) |
| `archive_utils.py` | Shared paths and helpers for the archive manifest, `post_map.yaml`, and README table generation. | imported by other scripts | [`substack-archive-sync`](../workflows/skills/substack-archive-sync/SKILL.md) |
| `check_mirror.py` | Structural validation for the archive and built mirror output. Checks metadata keys, archive files, asset references, generated README section, and built internal links. | `npm run check:mirror` | [`substack-archive-sync`](../workflows/skills/substack-archive-sync/SKILL.md) |
| `e2e_mirror_smoke.py` | Runtime smoke test for the built mirror at both root and prefixed path layouts. | `npm run check:mirror` | [`substack-archive-sync`](../workflows/skills/substack-archive-sync/SKILL.md) |

### Operating Agents Substack Publishing

This workflow republishes the Operating Agents essay set from repo markdown to live Substack posts.

Tracked workflow:

- [`../workflows/substack-publishing/README.md`](../workflows/substack-publishing/README.md)

| Script | Role | Normal Entry Point | Related Skill |
| :--- | :--- | :--- | :--- |
| `sync_operating_agents_substack.py` | Republishes the preface and six essay posts, preserves the embedded video block, rewrites published essay links to Substack URLs, and retries on Substack rate limits. | `.venv/bin/python scripts/sync_operating_agents_substack.py` | [`operating-agents-substack-sync`](../workflows/skills/operating-agents-substack-sync/SKILL.md) |

### YouTube Slide-To-Video Production

These scripts handle the local production stage for narrated slide videos before any YouTube upload or replacement step.

Tracked workflows:

- [`../workflows/youtube-production/README.md`](../workflows/youtube-production/README.md)
- [`../workflows/youtube-channel-ops/README.md`](../workflows/youtube-channel-ops/README.md)
- [`../workflows/youtube-series-operating-agents/README.md`](../workflows/youtube-series-operating-agents/README.md)

| Script | Role | Typical Use | Related Skill |
| :--- | :--- | :--- | :--- |
| `align_slides_to_transcript.py` | Drafts slide timing from OCR plus an untimestamped transcript and audio duration. | first-pass alignment | [`youtube-slide-video-pipeline`](../workflows/skills/youtube-slide-video-pipeline/SKILL.md) |
| `align_slides_to_captions.py` | Drafts slide timing from OCR plus timed SRT captions. | first-pass alignment with captions | [`youtube-slide-video-pipeline`](../workflows/skills/youtube-slide-video-pipeline/SKILL.md) |
| `map_slides_to_transcript_lines.py` | Drafts transcript line ranges from OCR text files and a numbered transcript. | line-range drafting | [`youtube-slide-video-pipeline`](../workflows/skills/youtube-slide-video-pipeline/SKILL.md) |
| `line_map_markdown_to_cues.py` | Converts a reviewed markdown line map plus timed captions into the final cue-sheet JSON used for rendering. | verified cue generation | [`youtube-slide-video-pipeline`](../workflows/skills/youtube-slide-video-pipeline/SKILL.md) |
| `render_audio_slides_video.py` | Generates a rough evenly spaced template or renders the final MP4 from a cue sheet. | template or final render | [`youtube-slide-video-pipeline`](../workflows/skills/youtube-slide-video-pipeline/SKILL.md) |
| `scrape_youtube_watch_transcript.py` | Scrapes the visible watch-page transcript panel into JSON when you need a browser fallback for transcript inspection. | transcript fallback or debugging | [`youtube-slide-video-pipeline`](../workflows/skills/youtube-slide-video-pipeline/SKILL.md) |

## Package-Specific Utility

| Script | Role | Notes |
| :--- | :--- | :--- |
| `stitch_binding_gap_slides.py` | Stitches paired presenter and detailed binding-gap slides into comparison images. | This is tied to `binding-and-recoverability/` assets and is not a general repo automation entrypoint. |

## Related Skill Split

Some adjacent automation lives outside this folder:

- YouTube channel-management, caption download, Shorts maintenance, playlist updates, and replacement uploads live under [`../workflows/skills/youtube-data-api/scripts/`](../workflows/skills/youtube-data-api/scripts/) and are documented canonically in [`../workflows/youtube-channel-ops/README.md`](../workflows/youtube-channel-ops/README.md) and [`../workflows/youtube-series-operating-agents/README.md`](../workflows/youtube-series-operating-agents/README.md).
- PDF slide export lives under [`../workflows/skills/pdf-slides-to-substack-images/scripts/`](../workflows/skills/pdf-slides-to-substack-images/scripts/).
- NotebookLM and alphaXiv workflows are documented canonically under [`../workflows/`](../workflows/README.md) and do not use this root `scripts/` folder as their main implementation surface.

## Safe Starting Points

If you only need the normal repo entrypoints, start with:

```bash
npm run sync:substack
npm run check:mirror
PYTHONUNBUFFERED=1 .venv/bin/python scripts/sync_operating_agents_substack.py
```

For YouTube production work, start with [`../workflows/youtube-production/README.md`](../workflows/youtube-production/README.md) before calling the lower-level scripts directly.
