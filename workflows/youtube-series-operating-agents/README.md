---
workflow_id: youtube_series_operating_agents
workflow_kind: module
stability: canonical
workflow_group: operations
runner_mode: guided
default_skill: youtube-operating-agents
launch_templates: []
required_context:
  - Operating Agents metadata file or exact chapter/video target
  - verified local production artifacts when the task touches a full-video upload or replacement
  - authenticated YouTube channel access
expected_outputs:
  - bounded Operating Agents channel mutation or verified no-op decision
  - local record of the exact chapter/video target, links, or playlist state changed
done_when:
  - the requested series-specific upload, cross-link, playlist, or replacement task is complete, or the exact blocker is recorded
approval_gate: required_before_channel_mutation
---

# YouTube Series: Operating Agents

This is the tracked canonical workflow for the Operating Agents YouTube series: TL;DR uploads, description cross-links, playlist order, and full-course replacement uploads tied to the local metadata file.

Use this workflow when the task is series-specific. It sits on top of the broader YouTube channel and local production workflows.

## Evidence-Backed Defaults

- Treat `workflows/skills/youtube-data-api/references/operating_agents_tldr_metadata.json` as the source of truth for order, links, and current video IDs.
- Prefer dry-run output first for cross-links, playlist order, TL;DR uploads, and replacements. Add `--apply` only when the intended write is confirmed.
- If playlist updates fail with `manualSortRequired`, switch the playlist to manual sort mode in YouTube Studio before retrying.
- Do not attempt API end-screen automation. Use managed description blocks and playlist order instead.
- If write quota is exhausted, continue local subtitle recovery, cue generation, and rendering work before retrying the channel writes.

## Canonical Flow

### 1. Confirm Local Production Inputs

If the task involves a new or replacement full video, complete the local production path first:

- [`../youtube-production/README.md`](../youtube-production/README.md)

That should leave you with a verified MP4, cue sheet, and caption inputs.

### 2. Treat Metadata As Authoritative

Use the metadata file for:

- chapter order
- full-video IDs and URLs
- TL;DR video IDs and URLs
- description navigation targets

After any replacement that changes a full-video ID, update the metadata before rerunning link or order sync.

### 3. Sync Description Navigation

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/sync_operating_agents_crosslinks.py \
  --course-playlist-id <COURSE_PLAYLIST_ID>
```

Add `--apply` only when the user wants the write.

### 4. Sync Playlist Order

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/sync_operating_agents_playlist_order.py
```

Default output is a plan. Add `--apply` to rewrite positions after the playlist is in manual sort mode.

### 5. Upload TL;DRs Or Replace Full Videos

TL;DR workflow:

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/upload_operating_agents_tldrs.py
```

Single replacement workflow:

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/replace_course_video.py \
  --old-video-id <CURRENT_FULL_VIDEO_ID> \
  --media-path <chapter>/artifacts/video/<TITLE>.mp4 \
  --playlist-id <OPERATING_AGENTS_COURSE_PLAYLIST_ID> \
  --position <chapter_position>
```

Batch replacement remains repo-specific:

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/replace_remaining_course_videos.py
```

All three print a plan by default and require `--apply` for writes.

## Related Surfaces

- [`../youtube-channel-ops/README.md`](../youtube-channel-ops/README.md): auth, captions, and general channel state.
- [`../youtube-production/README.md`](../youtube-production/README.md): local render and cue workflow.
- [`../skills/youtube-operating-agents/`](../skills/youtube-operating-agents/): series-specific execution bundle.
- [`../skills/youtube-data-api/`](../skills/youtube-data-api/): broader YouTube automation bundle.
