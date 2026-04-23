---
workflow_id: youtube_cinematic_rollout
workflow_kind: module
stability: experimental
workflow_group: operations
runner_mode: guided
default_skill: youtube-data-api
launch_templates: []
required_context:
  - experiments/youtube-cinematic-rollout/backlog_manifest.yaml
  - authenticated NotebookLM and YouTube access
  - package-local artifact surfaces for the target publications
expected_outputs:
  - updated evergreen backlog state
  - package-local cinematic and Shorts artifacts or an exact blocked-state note
  - appended release-ledger entry for the run
done_when:
  - all in-flight package work for the run is reconciled, up to two new cinematics are started or completed when possible, and blockers are recorded without hidden state
approval_gate: required_before_channel_mutation
---

# YouTube Cinematic Rollout

This is the tracked canonical workflow for the evergreen cinematic lane. It takes over after the bounded pilot and treats cinematic briefs as a standing daily distribution workflow rather than a one-off experiment batch.

Use this workflow when the task is:

- continuing the cinematic backlog across all eligible published essays
- reconciling in-flight cinematic packages before starting new ones
- recovering captions, selecting high-bar Shorts, rendering them, and scheduling them into the shared daily queue
- handling hard NotebookLM auth and quota gates without faking progress

## Ownership Split

- The evergreen rollout workspace owns:
  - `experiments/youtube-cinematic-rollout/backlog_manifest.yaml`
  - `experiments/youtube-cinematic-rollout/release_ledger.md`
- Publication packages own:
  - cinematic MP4s
  - cinematic SRTs
  - candidate reports
  - package-local Shorts manifests
  - portrait renders
  - upload reports under `artifacts/video/`

Do not move generated media into the experiment workspace.

## Hard Rules

- Run the NotebookLM auth preflight first. Expired NotebookLM auth is a hard gate for new cinematic generation.
- When auth is expired, do not start new cinematics. Record `blocked_auth_expired`, notify with `.venv/bin/notebooklm login`, and continue only with downstream YouTube-only reconciliation that does not require NotebookLM.
- Recover the cinematic `.srt` before choosing Shorts. Do not guess clip boundaries from untimed transcripts.
- Apply the high-bar Shorts rubric and schedule only clips that score `22` or higher.
- Publish cinematics immediately after upload.
- Publish Shorts starting the following day, at most one Short per source video per day.

## Canonical Files

- Backlog manifest:
  - `experiments/youtube-cinematic-rollout/backlog_manifest.yaml`
- Release ledger:
  - `experiments/youtube-cinematic-rollout/release_ledger.md`
- Existing mapped-video exclusion source:
  - `experiments/youtube-cinematic-pilot/metrics/video_asset_youtube_map.yaml`
- Shared cinematic prompt and description template:
  - `experiments/youtube-cinematic-pilot/copy/cinematic_prompt.txt`
  - `experiments/youtube-cinematic-pilot/copy/cinematic_description_template.md`

## Helper Scripts

- Backlog and scheduling:
  - `.venv/bin/python scripts/run_daily_cinematic_rollout.py --manifest experiments/youtube-cinematic-rollout/backlog_manifest.yaml`
- Candidate extraction from timed captions:
  - `.venv/bin/python scripts/extract_cinematic_short_candidates.py --package <package> --srt-file <cinematic.srt> --output <candidate_report.json>`
- Cinematic upload:
  - `.venv/bin/python scripts/upload_publication_cinematic.py --manifest experiments/youtube-cinematic-rollout/backlog_manifest.yaml --publication <key>`
- Shorts render:
  - `.venv/bin/python scripts/create_publication_shorts_from_longform.py --video-file <cinematic.mp4> --manifest <package-local-shorts-manifest.json>`
- Shorts upload:
  - `.venv/bin/python scripts/upload_publication_shorts.py --package <package> --shorts-dir <run-folder>/portrait --manifest <package-local-shorts-manifest.json> --main-video-id <cinematic-video-id> ...`

## Canonical Daily Run

### 1. Sync backlog and preflight auth

Run the evergreen rollout helper:

```bash
.venv/bin/python scripts/run_daily_cinematic_rollout.py \
  --manifest experiments/youtube-cinematic-rollout/backlog_manifest.yaml
```

The script must:

- discover newly eligible published packages
- dedupe umbrella roots into their canonical leaf when required
- print in-flight items first
- list up to two new generation candidates
- verify `.venv/bin/notebooklm auth check --test`
- record a blocked auth state in the ledger when auth fails

### 2. Finish in-flight packages first

Before starting any new cinematic generation, reconcile entries whose state is already beyond `queued`:

- caption recovery
- candidate extraction
- rubric scoring
- approved-clip scheduling
- package-local shorts-manifest materialization
- portrait render
- Shorts upload and readback

### 3. Start up to two new cinematics

When auth is valid and no higher-priority in-flight work blocks progress:

```bash
.venv/bin/notebooklm generate video \
  -n NOTEBOOK_ID \
  --retry 3 \
  --json \
  --format cinematic \
  --wait \
  "$(cat experiments/youtube-cinematic-pilot/copy/cinematic_prompt.txt)"
```

If NotebookLM returns a global quota or rate-limit error, stop new generation for that run, record `blocked_rate_limited`, and retry on the next scheduled day.

### 4. Upload the cinematic immediately

Use the shared upload wrapper:

```bash
.venv/bin/python scripts/upload_publication_cinematic.py \
  --manifest experiments/youtube-cinematic-rollout/backlog_manifest.yaml \
  --publication <key> \
  --apply
```

The cinematic should be public immediately unless a specific `publish_at` override is present.

### 5. Recover captions and extract candidates

Download the timed captions:

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/download_video_captions.py \
  --video-id <CINEMATIC_VIDEO_ID> \
  --output publications/<package>/artifacts/video/<cinematic>.srt
```

Then extract candidate windows:

```bash
.venv/bin/python scripts/extract_cinematic_short_candidates.py \
  --package <package> \
  --srt-file publications/<package>/artifacts/video/<cinematic>.srt \
  --output publications/<package>/artifacts/video/daily-cinematic-rollout/candidate_report.json
```

The helper produces candidate windows, excerpts, duration metadata, and heuristic novelty hints. The operator still applies the final rubric judgment.

### 6. Score and approve clips

Use the fixed rubric:

- hook strength
- standalone clarity
- novelty versus existing channel Shorts for that publication
- clip arc and compression
- rewatch/shareability

Scoring contract:

- `22-25`: approve and schedule
- `20-21`: reserve only
- `19 or below`: reject

Write approved, reserve, and rejected clips back into the backlog manifest entry, then rerun the rollout helper with `--apply` so it recomputes publish times and materializes the package-local Shorts manifest.

### 7. Render and upload Shorts

Render from the cinematic MP4 using the package-local manifest generated by the rollout helper, then upload with:

```bash
.venv/bin/python scripts/upload_publication_shorts.py \
  --package <package> \
  --shorts-dir publications/<package>/artifacts/video/daily-cinematic-rollout/portrait \
  --main-video-id <CINEMATIC_VIDEO_ID> \
  --playlist-id PL8lPx5mgRhhbMQQ70d-C4dAKKKPzCd5Hd \
  --essay-url <essay-url> \
  --full-video-url https://www.youtube.com/watch?v=<CINEMATIC_VIDEO_ID> \
  --primary-video-label "Full cinematic video" \
  --secondary-video-url <secondary-link-url> \
  --secondary-video-label "Full research breakdown" \
  --manifest publications/<package>/artifacts/video/daily-cinematic-rollout/shorts_manifest.json \
  --apply
```

## Shorts Scheduling Contract

- Each source video starts releasing Shorts on the calendar day after its cinematic publishes.
- Each source contributes at most one Short per day.
- Shared Athens-time slot ladder:
  - `09:00`, `10:30`, `12:00`, `13:30`, `15:00`, `16:30`, `18:00`, `19:30`, `21:00`, `22:30`
- On a given day, assign one slot per active source in rollout order.
- If a source runs out of approved clips, it drops out of the next day’s slot allocation automatically.

## Related Surfaces

- `../youtube-cinematic-pilot/README.md`: bounded pilot history and legacy contracts
- `../youtube-channel-ops/README.md`: auth, caption recovery, and playlist/channel operations
- `../youtube-series-operating-agents/README.md`: Operating Agents series-specific YouTube context
- `../../scripts/README.md`: root script map including the evergreen rollout helper and candidate extraction script
