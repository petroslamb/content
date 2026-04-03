---
name: youtube-operating-agents
description: "Use when Codex needs to manage the Operating Agents YouTube pipeline specifically: TL;DR uploads, description cross-links, playlist ordering, caption recovery, or full-course replacement uploads tied to the local Operating Agents metadata."
---

# YouTube Operating Agents

Use this skill for the series-specific Operating Agents workflow. Prefer it over the broader `$youtube-data-api` skill when the task is clearly about the Operating Agents course or TL;DR playlists.

## Core Path

1. Treat `workflows/skills/youtube-data-api/references/operating_agents_tldr_metadata.json` as the source of truth.
2. Use `workflows/skills/youtube-data-api/scripts/sync_operating_agents_crosslinks.py` to plan or apply navigation blocks.
3. Use `workflows/skills/youtube-data-api/scripts/sync_operating_agents_playlist_order.py` to compare metadata order with live playlist order.
4. Use `youtube-slide-video-pipeline` to produce or verify the rendered MP4s, cue sheets, and caption timing before any replacement upload.
5. Use `workflows/skills/youtube-data-api/scripts/replace_course_video.py` or `replace_remaining_course_videos.py` only after the rendered MP4s and metadata inputs are confirmed.
6. If quota is exhausted, continue local subtitle recovery, cue generation, and rendering before resuming API writes.

## Working Rules

- Prefer dry-run output first, then add `--apply` only when the user explicitly wants the write.
- If playlist order updates fail, check for manual sort mode in YouTube Studio before changing code.
- Do not attempt end-screen automation. Use description blocks and playlist order instead.
- After any replacement that changes a full-course video ID, update metadata and rerun cross-link sync.

## Reference Map

- `../../../workflows/youtube-series-operating-agents/README.md`: tracked canonical series workflow for metadata, cross-links, order sync, and replacements.
- `../../../workflows/youtube-production/README.md`: tracked local production workflow that should be completed before uploads or replacements.
- `../youtube-data-api/references/operating-agents-workflows.md`: end-to-end workflow, quota fallback, and replacement sequencing.
- `../youtube-slide-video-pipeline/references/workflow.md`: local slide, transcript, cue, and render workflow before upload.
- `../youtube-data-api/references/rollout-lessons.md`: constraints recovered from prior Operating Agents YouTube runs.
