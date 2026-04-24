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
