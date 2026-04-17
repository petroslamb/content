---
workflow_id: youtube_production
workflow_group: artifacts
runner_mode: guided
default_skill: youtube-slide-video-pipeline
launch_templates: []
required_context:
  - canonical audio narration
  - slide images or PDFs
  - timed captions or transcript inputs
expected_outputs:
  - reviewed cue sheet
  - verified MP4 in the package video artifact surface
done_when:
  - the local MP4 render is verified and ready for channel-side upload or replacement work
approval_gate: required_before_channel_mutation
---

# YouTube Production

This is the tracked canonical workflow for the local production stage that turns narrated audio, slide images, transcripts, and captions into a verified MP4 before any YouTube upload or replacement step.

Use this workflow before mutating the channel. It is the local production layer behind the YouTube upload skills.

## Evidence-Backed Defaults

- Caption timestamps are the timing anchor. OCR is only for drafting aid.
- `quotaExceeded` should not stop local production work. Keep moving on subtitle recovery, cue generation, and rendering.
- Prefer a real timed `.srt` file over watch-page transcript text whenever possible.
- If only local audio exists, recover the `.srt` by temporary unlisted upload rather than inventing timings from an untimed transcript.
- Keep render inputs and outputs close to the chapter's `artifacts/video/` surface.
- Do not render from unreviewed OCR output when the deck is dense, reordered, or diagram-heavy.
- **5 fps for slide-only videos** — dramatically smaller file with zero quality loss for static images.
- **Render uses `-preset medium` / `crf 23`** (script defaults). Don't adjust these for slideshows.
- The script encodes at 1920×1080 with 192kbps AAC audio. Audio typically dominates output size on long narrations.
- If caption recovery, temporary upload, local render, or Shorts slicing fails because of sandbox or filesystem permissions, stop that operation and ask for the narrow permission or user execution of the exact command. Do not proceed from missing captions, zero-byte media, or guessed timings.

## Canonical Flow

### Phase 1 — Recover timing inputs

Download auto-captions from YouTube Data API (preferred) or fall back to `yt-dlp` / watch-page scraping. Zero-byte files are not valid; recover a real SRT before proceeding.

If you only have local audio and no managed YouTube video yet, use the temporary-upload path from [`../youtube-channel-ops/README.md`](../youtube-channel-ops/README.md): upload an unlisted still-image video, wait for automatic captions, download the `.srt`, then delete the temporary upload.

If the temporary-upload path is blocked by OAuth, browser, or sandbox permissions, hand the user the exact recovery command and the expected `.srt` path. Continue only after the `.srt` exists and is non-empty.

### Phase 2 — Build the cue sheet

Three paths exist, chosen by how well the slides match the spoken narration:

**Path A — OCR-first alignment.** When slide text contains named terms that appear in the transcript, run `align_slides_to_captions.py` for a draft map, review match scores, and convert the verified markdown map into cues with `line_map_markdown_to_cues.py`. If match scores are consistently below 0.30, switch to Path B.

**Path B — Manual cue curation.** When OCR alignment fails (low scores, reordered slides, different deck from the audio's source):

1. **Read the SRT** — scan for topic keywords, named papers, numeric values, and section transitions. Use `grep -i "keyword"` to find where specific concepts appear.
2. **Visually read every slide** — use multimodal image read to extract text and diagram content. Don't rely on OCR for dense diagrams.
3. **If the raw numbered deck already follows the spoken order, keep all numbered slides** — don't drop slides just because OCR under-matched. Preserve the full deck and place it by section timing.
4. **Map each slide to its real audio moment** — align slide content to the timestamp where that topic is discussed. Correct timing matters more than uniform spacing. Use even spacing only as a temporary scaffold, not as the reviewed final cue plan.
5. **Add branded opener/closer cards only if they improve the package** — they are optional wrappers around the deck, not replacements for content slides.
6. **Interleave multiple decks only when they genuinely help** — if you have light/dark variants, alternate them for visual variety. Aim for a slide change every 1–3 minutes.
7. **Write a hand-crafted cue sheet JSON** with the structure below.

**Path C — Template draft.** `scripts/render_audio_slides_video.py template` gives evenly-spaced slides. Useful as a scaffold but not a reviewed final cue sheet.

### Phase 3 — Render the MP4

```bash
.venv/bin/python scripts/render_audio_slides_video.py render \
  --cues <cues.json> \
  --output <output.mp4> \
  --fps 5
```

If rendering is interrupted or crashes mid-write, the output is truncated (missing the `moov atom` header) and unplayable. Delete and re-run. A 5ps render of a 55-minute narration takes roughly 5–7 minutes.

After rendering, verify that the output duration matches the narration closely. If the video stream overruns the audio despite `-shortest`, trim the container back to the audio duration before treating the MP4 as publishable.

Also check for failed byproducts before handoff:

```bash
find publications/<package>/artifacts/video -type f -size 0
```

Zero-byte audio slices, SRTs, or MP4s are failed generation traces. Do not keep them in the reviewed video bundle.

### Phase 4 — Hand off

Once the MP4 is verified, switch to the channel workflows for auth checks, playlist updates, and upload.

### Optional Phase 5 — Derive Shorts From The Verified Long-Form

If the finished video has insight-dense segments that can stand alone in roughly `45` to `120` seconds, derive Shorts from the verified long-form rather than rebuilding them from scratch.

Use this path when:

- the long-form already has a trusted timed `.srt`
- the rendered master is the source of truth for visuals
- the goal is to publish multiple Shorts that point back to the long-form upload

Canonical sequence:

1. Read the timed `.srt` and pick segments that contain one clear idea with a clean beginning and payoff.
2. Write a `shorts_manifest.json` next to `artifacts/video/shorts/` with:
   - `slug`
   - `title`
   - `summary`
   - `start`
   - `end`
   - optional `publish_at`
3. Render the Shorts from the long-form master:

```bash
.venv/bin/python scripts/create_publication_shorts_from_longform.py \
  --video-file <longform.mp4> \
  --manifest <shorts_manifest.json>
```

This produces:

- `artifacts/video/shorts/landscape/*.mp4`
- `artifacts/video/shorts/portrait/*_portrait.mp4`

4. Verify that no zero-byte intermediate or output files remain in `artifacts/video/shorts/`.
5. Hand the finished portrait clips to the channel workflow for upload, playlist placement, related-video linkage, and optional scheduled release.

## Cue Sheet Structure

The render script expects a JSON cue sheet with these fields:

```json
{
  "audio": "path/to/audio.m4a",
  "slides_dir": "path/to/primary/slides",
  "segments": [
    {
      "image": "slide-01.png",
      "image_path": "path/to/deck/slide-01.png",
      "start": "00:01:18.960",
      "note": "What audio topic this slide covers",
      "render_variant": "DeckName"
    }
  ]
}
```

Each `image_path` is the repo-relative or absolute path to that slide image. The `render_variant` field tracks which deck each segment comes from. The last segment extends to the end of the audio.

## Multi-Deck Strategy

When a package has multiple slide decks covering the same content with different visual styles:

1. Visually read all slides from all decks.
2. Map each slide to the audio topic it best represents.
3. Use the primary deck as anchors, insert secondary deck slides at points where visual refresh improves engagement and the topic still matches.
4. The `--render-slides-dir` interleaving in `build_slideshow_from_captions.py` only works when all decks share identical filenames, which they usually don't — so manual cue curation is required.

## Command Reference

For exact bash commands for each phase, see [`../skills/youtube-slide-video-pipeline/references/workflow.md`](../skills/youtube-slide-video-pipeline/references/workflow.md).

## Related Surfaces

- [`../../scripts/README.md`](../../scripts/README.md): tracked script map for the local render pipeline.
- [`../skills/youtube-slide-video-pipeline/`](../skills/youtube-slide-video-pipeline/): execution-focused skill bundle.
- [`../skills/youtube-data-api/`](../skills/youtube-data-api/): managed caption download and channel-side follow-up.

## Rollout Lessons

See [`../skills/youtube-slide-video-pipeline/references/rollout-lessons.md`](../skills/youtube-slide-video-pipeline/references/rollout-lessons.md) for constraints recovered from the Operating Agents YouTube production rollout.
