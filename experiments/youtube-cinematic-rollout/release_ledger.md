# Daily Cinematic Rollout Ledger

Created: 2026-04-23
Timezone: Europe/Athens
Automation target: daily at 10:00 local time

## Purpose

This ledger is the evergreen run record for the daily cinematic rollout lane.
It replaces the bounded pilot-follow-through ledger as the canonical record for:

- backlog discovery
- hard blockers such as NotebookLM auth expiry or global cinematic quota
- per-package cinematic and Shorts state transitions
- daily release scheduling decisions

The historical pilot remains in `experiments/youtube-cinematic-pilot/`.

## Current Backlog

Initial rollout order from `backlog_manifest.yaml`:

1. `illusion_of_swarm`
2. `the_agent_revolution`
3. `operating_agents_action`
4. `operating_agents_memory`
5. `operating_agents_reasoning`
6. `operating_agents_multi_agent`
7. `operating_agents_safety`
8. `operating_agents_optimization`
9. `moltbook_phenomenon`
10. `programmable_thinking`

## Existing Mapped Cinematics Excluded From Backlog

- `neural_architecture`
- `autonomy_tax`
- `confidence_debt`
- `binding_gap`

## Carried Blockers

- `illusion_of_swarm` is already the front-of-queue item.
- Last known cinematic-create failure on 2026-04-23: `API rate limit or quota exceeded. Please wait before retrying.`
- NotebookLM auth is a hard gate for new cinematic generation and must be refreshed manually with `.venv/bin/notebooklm login` whenever it expires.

## Run Entries

### 2026-04-23 bootstrap

- Created the evergreen backlog manifest and rollout workflow surface.
- Preserved the existing pilot map as the exclusion source for already-mapped cinematic uploads.
- Fixed the initial secondary-link policy:
  - use YouTube long-form links when known
  - use the essay URL fallback for `programmable_thinking`

### 2026-04-23T13:27:27.576994+00:00

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- Next generation candidates: `illusion_of_swarm`, `the_agent_revolution`

### 2026-04-23T13:49:22Z

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- Generation attempts:
  - `illusion_of_swarm`: `.venv/bin/notebooklm generate video -n 8bdbaa61-25f3-4c6c-bc4f-cdcb29b174ee --retry 3 --json --format cinematic --wait ...`
  - `the_agent_revolution`: `.venv/bin/notebooklm generate video -n cc1c6170-b7d5-426a-bee4-a4acc2f5a60c --retry 3 --json --format cinematic --wait ...`
- Result: both returned immediate `RPC CREATE_ARTIFACT failed` errors before any new artifact task was created.
- Interpretation: treat this as a global NotebookLM cinematic quota or rate-limit block for the day, not a notebook-specific failure.
- Queue action: keep the backlog pinned at `illusion_of_swarm`; do not advance the generation pointer.
- Follow-through: retry on the next scheduled daily run.

### 2026-04-23T13:48:13.410940+00:00

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- Next generation candidates: `illusion_of_swarm`, `the_agent_revolution`

### 2026-04-24T07:00:43.828308+00:00

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- Next generation candidates: `illusion_of_swarm`, `the_agent_revolution`

### 2026-04-24T07:03:53.913605+00:00

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- In-flight first: `illusion_of_swarm`, `the_agent_revolution`

### 2026-04-24T07:01:11Z

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- New cinematic task accepted for `illusion_of_swarm`.
- NotebookLM task/artifact id: `52fd6b52-6720-4381-b4e1-6d590a1b95a8`
- Current artifact status: `in_progress`
- Queue action: mark `illusion_of_swarm` as `generation_pending` and keep it ahead of any new queue work until the cinematic artifact completes.

### 2026-04-24T07:01:31Z

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- New cinematic task accepted for `the_agent_revolution`.
- NotebookLM task/artifact id: `89e6395b-7101-496d-8ab6-c4584cd96743`
- Current artifact status: `in_progress`
- Queue action: mark `the_agent_revolution` as `generation_pending`; do not start additional new cinematics while these two jobs are active.

### 2026-04-24T08:09:54Z

- Both NotebookLM cinematic renders completed and were downloaded into the package artifact paths.
- `illusion_of_swarm` uploaded to YouTube: `q3_gPM4E8yw`
- `the_agent_revolution` uploaded to YouTube: `N7FKycVsIUw`
- Playlist action: both were added to `Rooted Layers Cinematic Briefs`.
- Queue action: move both entries from `generation_pending` to `captions_pending`.
- Caption recovery status:
  - `q3_gPM4E8yw`: no caption tracks found yet
  - `N7FKycVsIUw`: no caption tracks found yet
- Follow-through: retry caption download on the next watcher run, then continue into Shorts extraction and scheduling.

### 2026-04-24T08:12:20.675239+00:00

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- In-flight first: `illusion_of_swarm`, `the_agent_revolution`

### 2026-04-24T08:43:20.474883+00:00

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- In-flight first: `illusion_of_swarm`, `the_agent_revolution`

### 2026-04-24T08:46:44.078296+00:00

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- In-flight first: `illusion_of_swarm`, `the_agent_revolution`
- Materialized Shorts manifests: `publications/illusion-of-swarm/artifacts/video/daily-cinematic-rollout/shorts_manifest.json`, `publications/autonomous-agents/the-agent-revolution/artifacts/video/daily-cinematic-rollout/shorts_manifest.json`
- Newly scheduled approved clips: `7`

### 2026-04-24T08:47:45.880128+00:00

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- In-flight first: `illusion_of_swarm`, `the_agent_revolution`
- Materialized Shorts manifests: `publications/illusion-of-swarm/artifacts/video/daily-cinematic-rollout/shorts_manifest.json`, `publications/autonomous-agents/the-agent-revolution/artifacts/video/daily-cinematic-rollout/shorts_manifest.json`

### 2026-04-24T08:49:00Z

- Public caption fallback succeeded through `yt-dlp` after the managed YouTube caption downloader failed on an expired OAuth token.
- Approved and scheduled Shorts queue:
  - `illusion_of_swarm`: 3 approved clips scheduled for 2026-04-25 through 2026-04-27
  - `the_agent_revolution`: 4 approved clips scheduled for 2026-04-25 through 2026-04-28
- Render blocker: local Shorts rendering failed because `ffmpeg` is not installed or not on PATH.
- Channel blocker: the managed YouTube API token at `.youtube/token.json` could not refresh, so future Shorts uploads will also require auth refresh before the API path can continue.
- Queue action: keep both publications in `shorts_render_pending` until `ffmpeg` exists; after that, continue into local render and then Shorts upload once YouTube auth is refreshed.

### 2026-04-24T08:51:25.773232+00:00

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- In-flight first: `illusion_of_swarm`, `the_agent_revolution`

### 2026-04-24T09:00:00Z

- Local render toolchain recovered: Shorts scripts now resolve `ffmpeg` and `ffprobe` automatically from standard Homebrew paths when they are missing from `PATH`.
- Portrait render jobs were restarted for both in-flight publications:
  - `publications/illusion-of-swarm/artifacts/video/daily-cinematic-rollout/`
  - `publications/autonomous-agents/the-agent-revolution/artifacts/video/daily-cinematic-rollout/`
- YouTube follow-through blocker remains: the managed OAuth flow now asks for a fresh authorization visit through `workflows/skills/youtube-data-api/scripts/auth_and_channel_check.py` before API uploads can continue reliably.
- Queue action: keep both publications in-flight; finish local portrait rendering, then upload the queued Shorts immediately after YouTube auth is refreshed.

### 2026-04-24T11:03:30Z

- YouTube OAuth was refreshed successfully and both in-flight Shorts batches were uploaded.
- `illusion_of_swarm` Shorts scheduled:
  - `bGS_PcK4-oE` at `2026-04-25T06:00:00Z`
  - `8oawVSdt9vM` at `2026-04-26T06:00:00Z`
  - `SNbhI6ceIRc` at `2026-04-27T06:00:00Z`
- `the_agent_revolution` Shorts scheduled:
  - `bQQYzmHmAoo` at `2026-04-25T07:30:00Z`
  - `kFEns6A8tZk` at `2026-04-26T07:30:00Z`
  - `TeU3k4i6X_8` at `2026-04-27T07:30:00Z`
  - `opdhk_sizGY` at `2026-04-28T06:00:00Z`
- Verification:
  - all seven Shorts read back as `private` with the expected `publishAt`
  - all seven were added to the Shorts playlist
  - all seven were linked back to their corresponding cinematic uploads as the related video
- Queue action: `illusion_of_swarm` and `the_agent_revolution` are now fully `completed`; the in-flight watcher can be removed.

### 2026-04-24T11:00:06.495265+00:00

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- In-flight first: `illusion_of_swarm`, `the_agent_revolution`

### 2026-04-24T11:02:38.240566+00:00

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- Next generation candidates: `operating_agents_action`, `operating_agents_memory`

### 2026-04-25T07:02:19.029189+00:00

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- Next generation candidates: `operating_agents_action`, `operating_agents_memory`

### 2026-04-25T07:11:07Z

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- New cinematic task accepted for `operating_agents_action`.
- NotebookLM task/artifact id: `31498c5c-8d0c-4222-ab96-7e0113ac0900`
- Current artifact status: `in_progress`
- New cinematic task accepted for `operating_agents_memory`.
- NotebookLM task/artifact id: `b31dcd80-4c6e-4091-941e-8f2839ef656e`
- Current artifact status: `in_progress`
- Queue action: mark both entries as `generation_pending`; do not start additional new cinematics while these jobs are active.
- Watcher note: this Codex runtime does not expose an automation-management tool, so `experiment.automation.watcher_automation_id` remains `null` and no 30-minute heartbeat watcher could be created from this run.

### 2026-04-26T07:01:16.533387+00:00

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- In-flight first: `operating_agents_action`, `operating_agents_memory`

### 2026-04-26T07:04:23Z

- Downloaded both completed NotebookLM cinematic renders into their package artifact paths.
- `operating_agents_action` uploaded to YouTube: `NIJ92a65SxM`
- `operating_agents_memory` uploaded to YouTube: `J9dz9_9YPQw`
- Playlist action: both were added to `Rooted Layers Cinematic Briefs`.
- Queue action: move both entries from `generation_pending` to `captions_pending`.
- Caption recovery status:
  - `NIJ92a65SxM`: no caption tracks exposed yet through the managed downloader or the `yt-dlp` fallback
  - `J9dz9_9YPQw`: no caption tracks exposed yet through the managed downloader or the `yt-dlp` fallback
- Follow-through: retry caption recovery on the next watcher or daily run, then continue into Shorts extraction and scheduling.
- Watcher note: `experiment.automation.watcher_automation_id` remains `null` because this Codex runtime still does not expose an automation-management tool, so the required 30-minute heartbeat watcher could not be created or refreshed from this run.

### 2026-04-27T10:44:09Z

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- YouTube OAuth/channel check: `ok`
- Caption recovery succeeded for both in-flight cinematics:
  - `operating_agents_action`: `publications/autonomous-agents/essays/action/artifacts/video/operating_agents_action_cinematic.srt`
  - `operating_agents_memory`: `publications/autonomous-agents/essays/memory/artifacts/video/operating_agents_memory_cinematic.srt`
- Candidate extraction completed:
  - `operating_agents_action`: `8` candidates, top score `20`
  - `operating_agents_memory`: `7` candidates, top score `19`
- Shorts decision:
  - no clips cleared the `22/25` approval bar, so no `approved_clips` were promoted
  - `operating_agents_action` keeps one reserve candidate at score `20`
- Queue action:
  - `operating_agents_action` -> `no_shorts_approved`
  - `operating_agents_memory` -> `no_shorts_approved`
  - next daily generation can resume from `operating_agents_reasoning`
- Watcher state:
  - `experiment.automation.watcher_automation_id` remains `null`
  - no in-flight entries remain, so no watcher should exist after this run

### 2026-04-27T11:43:30Z

- Best-effort Shorts override: promoted two manual high-signal clips each for `operating_agents_action` and `operating_agents_memory` instead of leaving both videos in `no_shorts_approved`.
- Uploaded `operating_agents_action` Shorts:
  - `writing-the-script-isnt-agency` -> `Ue9gGySTVRI` scheduled `2026-04-29T06:00:00Z`
  - `css-tags-can-break-an-agent` -> `bsvMg8LUb1M` scheduled `2026-04-30T06:00:00Z`
- Uploaded `operating_agents_memory` Shorts:
  - `agents-dont-lose-iq-they-lose-attention` -> `QRD1FJiKTfU` scheduled `2026-04-29T07:30:00Z`
  - `flat-vector-memory-becomes-a-security-hole` -> `4UzuyKGNaKc` scheduled `2026-04-30T07:30:00Z`
- Verification:
  - all four Shorts read back as `private` with scheduled `publishAt`
  - all four were added to the shared Shorts playlist
  - all four were linked back to their source cinematic uploads as the related video
- Prompt update:
  - tightened `experiments/youtube-cinematic-pilot/copy/cinematic_prompt.txt` to force at least three self-contained 25-45 second claim blocks that can survive as Shorts without extra setup
- Title convention fix:
  - confirmed all four uploaded Shorts retain scheduled `publishAt` values on YouTube
  - renamed `NIJ92a65SxM` to `Why Reliable Agents Start with Action Boundaries | A Cinematic Research Brief`
  - renamed `J9dz9_9YPQw` to `Why Agent Memory Needs Authority | A Cinematic Research Brief`
  - patched `scripts/upload_publication_cinematic.py` so future cinematic uploads automatically keep the `| A Cinematic Research Brief` suffix

### 2026-04-27T10:42:49.380014+00:00

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- In-flight first: `operating_agents_action`, `operating_agents_memory`

### 2026-04-27T14:11:54.065746+00:00

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- Next generation candidates: `operating_agents_reasoning`, `operating_agents_multi_agent`

### 2026-04-27T14:12:28Z

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- New cinematic task accepted for `operating_agents_reasoning`.
- NotebookLM task/artifact id: `feccbf63-8d28-40fc-a43d-5b091406df98`
- Current artifact status: `in_progress`
- New cinematic task accepted for `operating_agents_multi_agent`.
- NotebookLM task/artifact id: `3113a471-43b4-4125-9ba2-993bb16e0bd8`
- Current artifact status: `in_progress`
- Queue action: mark both entries as `generation_pending`; do not start additional new cinematics while these two jobs are active.
- Watcher note: `experiment.automation.watcher_automation_id` remains `null` because this Codex runtime still does not expose an automation-management tool, so the required 30-minute heartbeat watcher could not be created or refreshed from this run.

### 2026-04-27T14:23:47Z

- Follow-up check for in-flight cinematic generation.
- `operating_agents_reasoning` artifact `feccbf63-8d28-40fc-a43d-5b091406df98`: still `in_progress`; no URL or error exposed yet.
- `operating_agents_multi_agent` artifact `3113a471-43b4-4125-9ba2-993bb16e0bd8`: still `in_progress`; no URL or error exposed yet.
- Queue action: keep both entries in `generation_pending`; no upload, caption recovery, Shorts extraction, or scheduling can continue until NotebookLM marks the artifacts completed.

### 2026-04-27T15:13:03Z

- Follow-through completed for `operating_agents_reasoning` and `operating_agents_multi_agent`.
- NotebookLM artifacts completed and were downloaded into the package artifact paths:
  - `operating_agents_reasoning`: `publications/autonomous-agents/essays/reasoning/artifacts/video/operating_agents_reasoning_cinematic.mp4`
  - `operating_agents_multi_agent`: `publications/autonomous-agents/essays/multi-agent/artifacts/video/operating_agents_multi_agent_cinematic.mp4`
- Cinematic uploads:
  - `operating_agents_reasoning`: `bto9FNWlahY`
  - `operating_agents_multi_agent`: `abBHq8lwCEE`
- Caption recovery succeeded after a 10-minute retry loop:
  - `publications/autonomous-agents/essays/reasoning/artifacts/video/operating_agents_reasoning_cinematic.srt`
  - `publications/autonomous-agents/essays/multi-agent/artifacts/video/operating_agents_multi_agent_cinematic.srt`
- Candidate extraction completed:
  - `operating_agents_reasoning`: `7` candidates
  - `operating_agents_multi_agent`: `8` candidates
- Approved and scheduled Shorts:
  - `the-ai-did-not-fail-the-scaffold-did` -> `T-XSEz2bQUk` scheduled `2026-04-28T06:00:00Z`
  - `ai-cannot-check-its-own-gravity` -> `QCK0hPc0dPM` scheduled `2026-04-29T06:00:00Z`
  - `agent-theater-is-not-intelligence` -> `PV-KfDYiLPo` scheduled `2026-04-28T07:30:00Z`
  - `the-coordination-tax-kills-agent-handoffs` -> `qTucAFn5g8Y` scheduled `2026-04-29T07:30:00Z`
- Verification:
  - all four Shorts read back as `private` with expected `publishAt`
  - all four Shorts read back as `processed`
  - all four Shorts are in the shared Shorts playlist
  - all four Shorts are linked back to their source cinematic upload
- Queue action:
  - `operating_agents_reasoning` -> `completed`
  - `operating_agents_multi_agent` -> `completed`
  - no in-flight entries remain; next daily generation can resume from `operating_agents_safety`

### 2026-04-27T15:08:39.807619+00:00

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- In-flight first: `operating_agents_reasoning`, `operating_agents_multi_agent`
- Materialized Shorts manifests: `publications/autonomous-agents/essays/reasoning/artifacts/video/daily-cinematic-rollout/shorts_manifest.json`, `publications/autonomous-agents/essays/multi-agent/artifacts/video/daily-cinematic-rollout/shorts_manifest.json`
- Newly scheduled approved clips: `4`

### 2026-04-27T15:12:49.188157+00:00

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- Next generation candidates: `operating_agents_safety`, `operating_agents_optimization`
- Follow-through note: no in-flight entries remain after the reasoning and multi-agent completions; these candidates are for the next daily starter run, not this watcher-style continuation.

### 2026-04-27T16:23:21Z

- Studio UI verification corrected the related-video cards for the four newly scheduled Shorts:
  - `T-XSEz2bQUk` -> `Diagnose the Scaffold Before You Shop the Model | A Cinematic Research Brief` (`bto9FNWlahY`)
  - `QCK0hPc0dPM` -> `Diagnose the Scaffold Before You Shop the Model | A Cinematic Research Brief` (`bto9FNWlahY`)
  - `PV-KfDYiLPo` -> `When the Second Agent Actually Buys a Boundary | A Cinematic Research Brief` (`abBHq8lwCEE`)
  - `qTucAFn5g8Y` -> `When the Second Agent Actually Buys a Boundary | A Cinematic Research Brief` (`abBHq8lwCEE`)
- Important workflow correction: API related-video readback was not sufficient; Studio initially showed `Related video: None` for the Shorts. Each Short was fixed in YouTube Studio, saved, reloaded, and verified as reload-persistent.
- Updated the cinematic rollout, channel ops, YouTube API skill, and scripts documentation so future Shorts batches require Studio related-video verification before a batch is marked complete.

### 2026-04-27T16:27:27Z

- Baked 10-minute async waits into the evergreen cinematic workflow:
  - NotebookLM artifact completion should use `.venv/bin/notebooklm artifact wait <ARTIFACT_ID> -n <NOTEBOOK_ID> --timeout 21600 --interval 600 --json` before yielding from the active run.
  - YouTube caption recovery should use `scripts/wait_for_youtube_captions.py --interval 600 --timeout 7200` before Shorts extraction.
- Added polling defaults to `experiments/youtube-cinematic-rollout/backlog_manifest.yaml` so future daily starters and watcher runs have canonical wait settings.
- Added the root caption wait helper and documented it in the workflow, script index, and YouTube Data API skill.
