---
workflow_id: youtube_cinematic_pilot
workflow_kind: module
stability: experimental
workflow_group: operations
runner_mode: guided
default_skill: youtube-data-api
launch_templates: []
required_context:
  - experiment manifest entry for the target publication
  - package-local cinematic video and caption artifact targets
  - authenticated NotebookLM and YouTube access
expected_outputs:
  - settled cinematic pilot manifest state for the selected publication
  - verified local cinematic assets or an exact upload/mutation plan
  - recorded pilot metrics or blocked-state note for the publication run
done_when:
  - the requested cinematic pilot step is complete for the selected publication, or the exact blocker is recorded without hidden channel mutation
approval_gate: required_before_channel_mutation
---

# YouTube Cinematic Pilot

This is the tracked canonical workflow for the reusable cinematic-video experiment lane. It exists to test whether NotebookLM cinematic companions create a better acquisition path than the current longform and TL;DR stack.

Use this workflow when the task is a multi-publication cinematic pilot with one shared manifest, one release calendar, one cinematic playlist, and one measurement rubric.

## Ownership Split

- The experiment workflow owns:
  - `experiments/youtube-cinematic-pilot/pilot_manifest.yaml`
  - `experiments/youtube-cinematic-pilot/release_calendar.yaml`
  - prompt text, description templates, notes, and metric checkpoints
- Publication packages own:
  - cinematic MP4s
  - caption files
  - package-local Shorts manifests
  - portrait renders
  - upload reports under `artifacts/video/`

Do not move generated media into the experiment workspace. The experiment layer coordinates the run; the package artifact surfaces remain canonical for media.

## Evidence-Backed Defaults

- Treat this as an additive lane. Do not replace the current longform or TL;DR catalog during the pilot.
- Keep the cinematic prompt text outside the shared NotebookLM default prompt bundle. This experiment should be reusable without redefining the repo-wide standard `explainer` bundle.
- Prefer broad discovery titles over essay-faithful titles for the cinematic uploads. Do not publish titles containing `TL;DR` or `Cinematic`.
- Use one shared public cinematic playlist and one existing public Shorts playlist for the pilot rather than creating publication-specific playlist sprawl.
- Dry-run every upload step first. Channel mutation starts only after the manifest, playlist target, titles, descriptions, and schedule are settled.
- Recover the cinematic captions before choosing Shorts. Do not guess clip boundaries from untimed transcripts.

## Canonical Workspace

The reusable experiment workspace lives at:

- `experiments/youtube-cinematic-pilot/`

Tracked files in that workspace:

- `pilot_manifest.yaml`: publication-by-publication contract
- `release_calendar.yaml`: chronological rollout schedule
- `copy/cinematic_prompt.txt`: NotebookLM cinematic prompt
- `copy/cinematic_description_template.md`: upload description template
- `metrics/README.md`: checkpoint contract and report expectations
- `notes.md`: pilot assumptions, unresolved items, and operating notes

## Manifest Contract

Each publication entry in `pilot_manifest.yaml` must define:

- notebook ID
- package path under `publications/`
- essay URL
- baseline longform video ID and URL
- cinematic title
- cinematic hook
- cinematic summary
- cinematic target video file, caption file, and upload report path
- cinematic publish time
- cinematic playlist target
- Shorts manifest path in the package
- two selected Shorts with `slug`, title, and `publish_at`
- one reserve Short
- metric checkpoints

If the cinematic playlist does not yet have an ID, the uploader may create it on first apply. If a package-level Shorts manifest does not exist yet, the experiment manifest remains the planning source of truth until the package manifest is materialized.

## Canonical Flow

### 1. Verify Auth And Inputs

Check NotebookLM and YouTube auth before mutating anything:

```bash
.venv/bin/notebooklm auth check --test
.venv/bin/python workflows/skills/youtube-data-api/scripts/auth_and_channel_check.py
```

Also verify that the target package artifact paths are writable and that there are no zero-byte media traces:

```bash
find publications/<package>/artifacts -type f -size 0 2>/dev/null
```

### 2. Generate The Cinematic Video

Use NotebookLM directly. The cinematic prompt lives in the experiment workspace, not in the shared prompt bundle:

```bash
.venv/bin/notebooklm generate video \
  -n NOTEBOOK_ID \
  --retry 3 \
  --json \
  --format cinematic \
  "$(cat experiments/youtube-cinematic-pilot/copy/cinematic_prompt.txt)"
```

Poll the notebook artifacts until the cinematic video completes:

```bash
.venv/bin/notebooklm artifact list -n NOTEBOOK_ID --json
```

Download the cinematic MP4 into the package artifact surface named in `pilot_manifest.yaml`.

### 3. Dry-Run The Cinematic Upload

Use the dedicated uploader. It reads one publication entry from the experiment manifest and defaults to dry-run:

```bash
.venv/bin/python scripts/upload_publication_cinematic.py \
  --manifest experiments/youtube-cinematic-pilot/pilot_manifest.yaml \
  --publication neural_architecture
```

Dry-run must show:

- the target cinematic title
- the package-local source MP4
- the resolved or planned playlist target
- the final description preview
- the scheduled publish time when present

### 4. Upload The Cinematic Video

Apply only after the dry-run looks correct:

```bash
.venv/bin/python scripts/upload_publication_cinematic.py \
  --manifest experiments/youtube-cinematic-pilot/pilot_manifest.yaml \
  --publication neural_architecture \
  --apply
```

This uploader may create `Rooted Layers Cinematic Briefs` if the playlist is still missing, then uploads the package-local cinematic video and writes the upload report into the package artifact surface.

### 5. Recover Captions

After upload, recover the caption file into the publication’s `artifacts/video/` folder:

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/download_video_captions.py \
  --video-id <CINEMATIC_VIDEO_ID> \
  --output publications/<package>/artifacts/video/<cinematic>.srt
```

Do not choose the Shorts clips until the `.srt` exists and is non-empty.

### 6. Materialize The Package Shorts Manifest

The experiment manifest owns the selected clips and schedule. Before upload, materialize or update the package-local `shorts_manifest.json` so it contains the two selected clips for that run and their final `publish_at` values.

Use the experiment manifest as the scheduling source of truth. Use the package manifest as the execution surface that the Shorts uploader reads.

### 7. Dry-Run And Upload The Shorts

Use the cinematic upload as the related video and prioritize the cinematic link over the baseline longform link:

```bash
.venv/bin/python scripts/upload_publication_shorts.py \
  --package neural-architectures/neural-architecture-design-as-a-compositional-32e \
  --main-video-id <CINEMATIC_VIDEO_ID> \
  --playlist-id PL8lPx5mgRhhbMQQ70d-C4dAKKKPzCd5Hd \
  --essay-url https://lambpetros.substack.com/p/neural-architecture-design-as-a-compositional-32e \
  --full-video-url https://www.youtube.com/watch?v=<CINEMATIC_VIDEO_ID> \
  --primary-video-label "Full cinematic video" \
  --secondary-video-url https://www.youtube.com/watch?v=-2CM4JYfQAs \
  --secondary-video-label "Full research breakdown" \
  --manifest publications/neural-architectures/neural-architecture-design-as-a-compositional-32e/artifacts/video/shorts/shorts_manifest.json \
  --selection-manifest experiments/youtube-cinematic-pilot/pilot_manifest.yaml \
  --selection-publication neural_architecture
```

Apply only after the dry-run matches the pilot schedule.

## Measurement Contract

For every upload, record:

- `+24h`
- `+72h`
- `+7d`

Manual Studio metrics:

- impressions
- click-through rate
- average view duration
- 30-second retention
- traffic source mix
- subscribers gained

Repo/API metrics:

- video ID
- public URL
- publish time
- playlist placement
- caption readiness time
- related-video write status
- likes
- comments

Write the consolidated experiment report under `experiments/youtube-cinematic-pilot/metrics/`.

## Acceptance Rules

- Keep the cinematic lane only if at least 2 of 3 cinematic uploads beat their benchmarks by day 7.
- Also require at least 3 of 6 pilot Shorts to exceed `100` views by day 7.
- If no cinematic beats its benchmark and fewer than 2 Shorts exceed `100` views, stop the lane after the pilot.

## Related Surfaces

- `../../../workflows/notebooklm-artifacts/README.md`: standard NotebookLM artifact workflow that the pilot branches from for non-standard cinematic generation
- `../../../workflows/youtube-channel-ops/README.md`: caption recovery, playlist inspection, and other channel-state operations
- `../../../scripts/README.md`: tracked script map, including the cinematic uploader and Shorts uploader
