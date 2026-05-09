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
  - approved video-specific prompt packet for each new cinematic before generation
  - package-local cinematic and Shorts artifacts or an exact blocked-state note
  - Shorts candidates with hook pattern, overlay copy, rubric score, and scheduling status
  - verified Studio card and end-screen links for uploaded cinematic briefs when a YouTube research-breakdown target exists
  - appended release-ledger entry for the run
done_when:
  - all in-flight package work for the run is reconciled, cold-open and Shorts quality gates are either satisfied or explicitly blocking, uploaded cinematic briefs have Studio card/end-screen wiring or an explicit blocker recorded, up to two new cinematics are started or completed when possible, and blockers are recorded without hidden state
approval_gate: required_before_channel_mutation
---

# YouTube Cinematic Rollout

This is a contracted experimental workflow for the evergreen cinematic lane. It follows the bounded pilot and treats cinematic briefs as a standing opt-in distribution workflow rather than a one-off experiment batch.

## Phase 2.8 Lifecycle State

State: `contracted`. This workflow has a governed `workflow.yaml` with `stability: experimental`, so it can be invoked explicitly through `content-agent`; it is not a canonical/default route and has no promotion proof from this pass.

Use this workflow when the task is:

- continuing the cinematic backlog across all eligible published essays
- reconciling in-flight cinematic packages before starting new ones
- recovering captions, selecting high-bar Shorts, rendering them, and scheduling them into the shared daily queue
- wiring full cinematic uploads in YouTube Studio so viewers can jump to the paired long research breakdown from an info card and end screen
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
- Do not start a new cinematic generation until `cinematic.cold_open.status: approved`, `cinematic.prompt_packet.status: approved`, and the packet has a concrete first line, viewer promise, conflict, payoff by 30 seconds, and failure chain.
- Generate NotebookLM from the package-local `cinematic.prompt_file`, not the shared fallback, whenever the rollout helper has materialized one.
- After timed captions are recovered, check `cinematic.generation_compliance`. A `failed_first_line` status means NotebookLM ignored the required cold open; the helper moves the entry to `generation_compliance_review_pending` and blocks Shorts scheduling/materialization unless `cinematic.generation_compliance_override: true` is set intentionally.
- Recover the cinematic `.srt` before choosing Shorts. Do not guess clip boundaries from untimed transcripts.
- Apply the high-bar Shorts rubric and schedule only clips that score `22` or higher.
- Do not schedule newly approved Shorts unless they also have a feed-native `hook`, `cta`, `summary`, and `pattern` with `type` and `topic_lane`.
- Render approved Shorts with the manifest-configured overlay treatment by default: top hook, spoken subtitles from the cinematic SRT, and bottom related-video CTA.
- Publish cinematics immediately after upload.
- For every full cinematic upload in `Rooted Layers Cinematic Briefs`, add one YouTube Studio info card pointing to the configured YouTube research-breakdown target in the first few minutes.
- Do not try to add a second info card pointing to the same research-breakdown video. YouTube Studio rejects duplicate video-card targets for the same upload with a "multiple cards cannot reference the same video" validation error.
- For every full cinematic upload with a configured YouTube research-breakdown target, make the end screen rich: keep one explicit video element pointing to that target, add one `best for viewer` video element, and add one subscribe element.
- Do not add cards or end screens to Shorts as part of this workflow.
- If the configured secondary link is an external essay URL rather than a YouTube video, record `studio_link_blocked_external_target` and skip the Studio card/end-screen step. Do not guess a target video.
- If YouTube Studio browser auth is missing, record `studio_link_pending`, notify the user to sign in to Studio, and keep the item in follow-through until the card/end-screen wiring is verified.
- Publish Shorts starting the following day, at most one Short per source video per day.
- The active daily run or watcher must wait through normal asynchronous generation delays instead of yielding early. Use the manifest polling defaults: `poll_interval_seconds: 600`, `notebooklm_generation_wait_timeout_seconds: 21600`, and `youtube_caption_wait_timeout_seconds: 7200`.

## Canonical Files

- Backlog manifest:
  - `experiments/youtube-cinematic-rollout/backlog_manifest.yaml`
  - includes `experiment.automation.watcher_automation_id` so the daily starter can avoid duplicating watcher heartbeats
- Release ledger:
  - `experiments/youtube-cinematic-rollout/release_ledger.md`
- Existing mapped-video exclusion source:
  - `experiments/youtube-cinematic-pilot/metrics/video_asset_youtube_map.yaml`
- Shared cinematic prompt fallback and description template:
  - `experiments/youtube-cinematic-pilot/copy/cinematic_prompt.txt`
  - `experiments/youtube-cinematic-pilot/copy/cinematic_description_template.md`
- Package-local prompt packet artifacts:
  - `publications/<package>/artifacts/video/daily-cinematic-rollout/prompt_packet.yaml`
  - `publications/<package>/artifacts/video/daily-cinematic-rollout/cinematic_prompt.txt`

## Automation Topology

- Daily starter:
  - runs once per day at `10:00` Athens time
  - reconciles state first, then starts up to two new cinematic generations when capacity allows
  - after starting NotebookLM work, blocks on 10-minute generation polling when the current runtime can safely remain active
  - when any cinematic rollout entry is in flight, the active run should stay alive and keep using 10-minute sleep-and-check polling until that batch is fully finished through Shorts scheduling, Shorts upload, Shorts related-video Studio verification, and full cinematic Studio card/end-screen verification
  - do not yield early just because the next required step is asynchronous; sleep for `poll_interval_seconds` and resume until the current batch is fully reconciled or a real auth/rate-limit blocker is recorded
  - if it creates or detects any in-flight cinematic rollout work and the runtime truly cannot stay alive, create or refresh a temporary watcher heartbeat for this thread as the fallback only
- Temporary watcher:
  - runs every `30` minutes
  - watches only in-flight entries already present in the backlog manifest
  - does not start new backlog generations
  - continues the pipeline through upload, Studio card/end-screen wiring, captions, Shorts selection, render, Shorts upload, and readback, using 10-minute waits for NotebookLM artifacts and YouTube captions before yielding
  - deletes itself when there are no in-flight cinematic rollout entries left

Do not rely on a single reconciliation pass. The active run should normally stay alive and wait through the full in-flight batch end to end, using repeated 10-minute polling windows. The watcher is the backup follow-through layer only when that active runtime cannot stay alive.

## Helper Scripts

- Backlog and scheduling:
  - `.venv/bin/python scripts/run_daily_cinematic_rollout.py --manifest experiments/youtube-cinematic-rollout/backlog_manifest.yaml`
- Candidate extraction from timed captions:
  - `.venv/bin/python scripts/extract_cinematic_short_candidates.py --package <package> --srt-file <cinematic.srt> --output <candidate_report.json>`
- Cinematic upload:
  - `.venv/bin/python scripts/upload_publication_cinematic.py --manifest experiments/youtube-cinematic-rollout/backlog_manifest.yaml --publication <key>`
- Caption wait/download:
  - `.venv/bin/python scripts/wait_for_youtube_captions.py --video-id <CINEMATIC_VIDEO_ID> --output <cinematic.srt> --interval 600 --timeout 7200`
- Studio card and end-screen wiring:
  - `https://studio.youtube.com/video/<CINEMATIC_VIDEO_ID>/editor`
- Shorts render:
  - `.venv/bin/python scripts/create_publication_shorts_from_longform.py --video-file <cinematic.mp4> --manifest <package-local-shorts-manifest.json>`
  - The package-local manifest carries `source_srt` and `overlay` settings, so the renderer should burn in hook/subtitle/CTA overlays without extra flags. Use `--no-burn-in-subtitles` only for a deliberate raw-render diagnostic.
- Shorts upload:
  - `.venv/bin/python scripts/upload_publication_shorts.py --package <package> --shorts-dir <run-folder>/portrait --manifest <package-local-shorts-manifest.json> --main-video-id <cinematic-video-id> ...`

## Tightening Gates

The rollout is experimental, but it should not treat polished output as progress by itself. The daily helper now reports quality-gate issues and uses those gates when scheduling future work.

### Prompt Packet Gate

Every new or queued cinematic must carry this operator-approved prompt packet before NotebookLM generation starts:

```yaml
cinematic:
  cold_open:
    status: approved
    first_line: "The first sentence viewers hear."
    viewer_promise: "What the viewer will understand if they stay."
    conflict: "The concrete tension or failure this brief resolves."
    payoff_by_30s: "What has been made clear by the first 30 seconds."
  prompt_packet:
    status: approved
    artifact_goal: hook_repair | scale_winner | concept_refresh | exploration
    source_signal: analytics | backlog | manual_pick | remaster
    failure_chain:
      - "The concrete setup or misdiagnosis."
      - "The specific operational break."
      - "The better scaffold, boundary, or action the viewer should take."
    clip_safe_claim_blocks:
      minimum: 3
    forbidden:
      - "TL;DR"
      - "top 5"
      - "in this video"
```

If either packet is missing or not approved, `scripts/run_daily_cinematic_rollout.py` moves the entry to `cold_open_review_pending` and does not consider it a generation candidate. When both packets pass, the helper materializes:

- `prompt_packet.yaml`: the structured source of truth for why this artifact exists
- `cinematic_prompt.txt`: the NotebookLM prompt rendered from that packet

This is intentional: the current analytics show that cinematic topics can earn clicks and subscribers while losing too much attention in the opening. The prompt packet makes the reason for the artifact explicit before generation starts.

### Generation Compliance Gate

NotebookLM can preserve the concept while rewriting the first line. After the cinematic `.srt` is recovered, rerun the rollout helper. If the entry has a materialized `cinematic.prompt_file`, the helper writes:

```yaml
generation_compliance:
  status: passed_first_line | failed_first_line
  match_mode: normalized_prefix_exact
  expected_first_line: "The requested first spoken line."
  observed_opening: "The first recovered caption text."
```

Treat `failed_first_line` as a repair signal. The result may still be usable after manual review, but the workflow should not treat it as evidence that the prompt contract worked. Set `cinematic.generation_compliance_override: true` only when the operator has reviewed the miss and deliberately wants downstream Shorts work to continue.

### Shorts Pattern Gate

Approved Shorts are not just clips; they are pattern tests. Each approved clip should include:

```yaml
pattern:
  type: contradiction | mechanism | consequence | concrete_failure | metric_shock
  topic_lane: memory | multi-agent | safety | reasoning | workflow | hardware | other
  source_signal: scale | hook_repair | remaster | exploration
```

The helper only schedules new unscheduled clips when the clip has:

- `total_score` at or above the manifest `approved_min`
- a top `hook` within the configured word limit
- a `cta`
- a `summary`
- `pattern.type`
- `pattern.topic_lane`

Existing scheduled clips are not silently rewritten. They are reported as quality-gate issues so the operator can repair or leave them intentionally.

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
- mark entries with missing or unapproved cold-open or prompt packets as `cold_open_review_pending`
- materialize package-local `prompt_packet.yaml` and `cinematic_prompt.txt` files for generation-ready entries
- print in-flight items first
- list up to two new generation candidates
- verify `.venv/bin/notebooklm auth check --test`
- print quality-gate issues for cold opens and approved Shorts
- record a blocked auth state in the ledger when auth fails

### 2. Finish in-flight packages first

Before starting any new cinematic generation, reconcile entries whose state is already beyond `queued`:

- cold-open review for `cold_open_review_pending` entries
- prompt-packet review for entries whose cold open is approved but whose artifact goal, source signal, or failure chain is missing
- caption recovery
- generation compliance review after captions are recovered
- Studio card/end-screen reconciliation for any uploaded cinematic brief with a YouTube research-breakdown target
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
  "$(cat publications/<package>/artifacts/video/daily-cinematic-rollout/cinematic_prompt.txt)"
```

If the generation command returns an artifact ID before the video is downloadable, wait inside the same active run:

```bash
.venv/bin/notebooklm artifact wait <ARTIFACT_ID> \
  -n NOTEBOOK_ID \
  --timeout 21600 \
  --interval 600 \
  --json
```

When the artifact completes, download or export the completed video immediately into the entry's `cinematic.video_file`, then continue to upload. If the wait times out but the task is still `in_progress`, keep the entry in `generation_pending`, write the current artifact ID into the manifest, and rely on the 30-minute watcher for the next 10-minute polling window. Do not start additional backlog entries while any entry remains `generation_pending`.

If NotebookLM returns a global quota or rate-limit error, stop new generation for that run, record `blocked_rate_limited`, and retry on the next scheduled day.

After new cinematic work is started, create or refresh the temporary 30-minute watcher so those jobs are polled to completion without waiting for the next daily run.

### 4. Upload the cinematic immediately

Use the shared upload wrapper:

```bash
.venv/bin/python scripts/upload_publication_cinematic.py \
  --manifest experiments/youtube-cinematic-rollout/backlog_manifest.yaml \
  --publication <key> \
  --apply
```

The cinematic should be public immediately unless a specific `publish_at` override is present.

### 5. Wire Studio card and end screen

This step applies only to the full cinematic upload in the `Rooted Layers Cinematic Briefs` playlist. It does not apply to Shorts, TL;DR uploads, visual deep dives, or other YouTube workflows.

Use the configured YouTube research-breakdown target:

- `secondary_link.video_id` when the manifest entry provides one
- the mapped baseline longform/explainer video ID for pilot or legacy entries
- no target when the secondary link is only an external essay URL

When there is no YouTube target, write `studio_link_blocked_external_target` to the release ledger and continue with captions and Shorts. Cards and end screens should point to YouTube videos only; do not invent a fallback.

Open the uploaded cinematic in YouTube Studio:

```text
https://studio.youtube.com/video/<CINEMATIC_VIDEO_ID>/editor
```

In Studio:

- Add or edit the end screen. The target end screen should contain:
  - one specific video element set to the configured research-breakdown video ID
  - one `best for viewer` video element
  - one subscribe element for the channel
- If an older end screen already has the explicit research-breakdown video, keep it and add the missing `best for viewer` and subscribe elements.
- Add or edit info cards. Use one video card pointing to the configured research-breakdown video ID.
- Prefer `00:01:00` for the card teaser time. If Studio rejects that timestamp for a very short upload, use the earliest valid first-minutes timestamp.
- If asked for a second identical card at the midpoint, record `studio_card_duplicate_target_not_allowed`; do not leave an invalid unsaved duplicate card in Studio.
- Reopen the editor after saving and verify the main editor shows the end screen and info cards as editable, the explicit research-breakdown target appears on the timeline, and both the `best for viewer` and subscribe elements are present where Studio exposes them. If any surface did not persist, reopen that editor and save again.

If Studio browser auth is missing, record `studio_link_pending` with the cinematic video ID and target video ID, notify the user to sign in to YouTube Studio in the in-app browser, and keep the item in the active follow-through loop until auth is restored or the run is explicitly blocked. Downstream YouTube-only work can continue only when it does not hide the unresolved Studio wiring.

### 6. Recover captions and extract candidates

Wait for timed captions and download them. YouTube automatic captions often appear after upload processing, so use the polling wrapper rather than a single caption attempt:

```bash
.venv/bin/python scripts/wait_for_youtube_captions.py \
  --video-id <CINEMATIC_VIDEO_ID> \
  --output publications/<package>/artifacts/video/<cinematic>.srt \
  --interval 600 \
  --timeout 7200
```

Then extract candidate windows:

```bash
.venv/bin/python scripts/extract_cinematic_short_candidates.py \
  --package <package> \
  --srt-file publications/<package>/artifacts/video/<cinematic>.srt \
  --output publications/<package>/artifacts/video/daily-cinematic-rollout/candidate_report.json
```

The helper produces candidate windows, excerpts, duration metadata, and heuristic novelty hints. The operator still applies the final rubric judgment.

### 7. Score and approve clips

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

For every approved clip, include:

- `hook`: a short, specific top overlay line. Prefer a concrete insight or tension over a label. Keep it under roughly nine words when possible.
- `cta`: normally `Full cinematic brief in Related Video`, unless there is a stronger source-specific related-video CTA.
- `summary`: the YouTube description seed, distinct from the hook. The hook is on-screen copy; the summary is metadata.
- `pattern`: the hook pattern and topic lane being tested, so analytics can later distinguish "this topic worked" from "this rhetorical shape worked."

Do not promote merely intelligent clips. Promote feed-ready clips:

- they make sense without the cinematic
- they expose one concrete tension immediately
- they pay off before the viewer has to infer the thesis
- they are different enough from existing channel Shorts to teach the next iteration
- they have a specific related-video CTA rather than a generic content label

### 8. Render and upload Shorts

Render from the cinematic MP4 using the package-local manifest generated by the rollout helper:

```bash
.venv/bin/python scripts/create_publication_shorts_from_longform.py \
  --video-file publications/<package>/artifacts/video/<cinematic>.mp4 \
  --manifest publications/<package>/artifacts/video/daily-cinematic-rollout/shorts_manifest.json
```

The default overlay contract is:

- top zone: approved clip `hook`, falling back to clip `title`
- middle/lower zone: spoken subtitle events recovered from the source cinematic SRT and normalized into non-overlapping caption segments
- bottom zone: approved clip `cta`, falling back to `experiment.defaults.shorts_overlay.default_cta`
- generated overlay assets: `<run-folder>/overlays/<clip-stem>/overlay.mov` plus segment PNGs
- final upload artifact: `<run-folder>/portrait/<clip-stem>_portrait.mp4`

Keep YouTube captions available on the upload; the burned-in subtitles are for feed readability, not a replacement for accessibility captions.

Before uploading, do a quick visual QA pass on at least three sampled frames per Short:

- hook is readable in the top matte space
- spoken caption is not covering the main subject
- bottom CTA sits above the normal YouTube Shorts control area
- no text overlaps another overlay or gets clipped on the 1080x1920 frame
- if the SRT is missing or badly timed, keep the item in `captions_pending` or `shorts_render_pending`; do not silently upload raw non-overlay Shorts

Then upload with:

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

After upload, verify the Shorts related-video setting in YouTube Studio, not only through the API report:

- Open each Short in Studio at `https://studio.youtube.com/video/<SHORT_ID>/edit`.
- In the right-side `Related video` card, set the related video to that Short's source cinematic brief from the `Rooted Layers Cinematic Briefs` playlist.
- Save the Studio metadata change.
- Stay on the page until the save state fully settles; do not navigate away immediately after clicking Save.
- Reload the same Studio edit page and verify the `Related video` card still shows the cinematic brief title.
- If the card returns to `None`, repeat the Studio selection and save; do not mark the entry completed until the reload check persists.
- Use the Codex in-app browser for this verification and persistence pass whenever browser automation is available for the run.

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
