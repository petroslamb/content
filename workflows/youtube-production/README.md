# YouTube Production

This is the tracked canonical workflow for the local production stage that turns narrated audio, slide images, transcripts, and captions into a verified MP4 before any YouTube upload or replacement step.

Use this workflow before mutating the channel. It is the local production layer behind the YouTube upload skills.

## Evidence-Backed Defaults

- Caption timestamps are the timing anchor. OCR is only for drafting aid.
- `quotaExceeded` should not stop local production work. Keep moving on subtitle recovery, cue generation, and rendering.
- Prefer a real timed `.srt` file over watch-page transcript text whenever possible.
- Keep render inputs and outputs close to the chapter's `artifacts/video/` surface.
- Do not render from unreviewed OCR output when the deck is dense, reordered, or diagram-heavy.
- **5 fps for slide-only videos** — dramatically smaller file with zero quality loss for static images.
- **Render uses `-preset medium` / `crf 23`** (script defaults). Don't adjust these for slideshows.
- The script encodes at 1920×1080 with 192kbps AAC audio. Audio typically dominates output size on long narrations.

## Canonical Flow

### Phase 1 — Recover timing inputs

Download auto-captions from YouTube Data API (preferred) or fall back to `yt-dlp` / watch-page scraping. Zero-byte files are not valid; recover a real SRT before proceeding.

### Phase 2 — Build the cue sheet

Three paths exist, chosen by how well the slides match the spoken narration:

**Path A — OCR-first alignment.** When slide text contains named terms that appear in the transcript, run `align_slides_to_captions.py` for a draft map, review match scores, and convert the verified markdown map into cues with `line_map_markdown_to_cues.py`. If match scores are consistently below 0.30, switch to Path B.

**Path B — Manual cue curation.** When OCR alignment fails (low scores, reordered slides, different deck from the audio's source):

1. **Read the SRT** — scan for topic keywords, named papers, numeric values, and section transitions. Use `grep -i "keyword"` to find where specific concepts appear.
2. **Visually read every slide** — use multimodal image read to extract text and diagram content. Don't rely on OCR for dense diagrams.
3. **Map each slide to its audio moment** — align slide content to the approximate timestamp where that topic is discussed. Prefer slightly early placement over perfectly synced.
4. **Interleave multiple decks** — if you have light/dark variants, alternate them for visual variety. Aim for a slide change every 1–3 minutes.
5. **Write a hand-crafted cue sheet JSON** with the structure below.

**Path C — Template draft.** `scripts/render_audio_slides_video.py template` gives evenly-spaced slides. Useful as a scaffold but rarely publish-ready.

### Phase 3 — Render the MP4

```bash
.venv/bin/python scripts/render_audio_slides_video.py render \
  --cues <cues.json> \
  --output <output.mp4> \
  --fps 5
```

If rendering is interrupted or crashes mid-write, the output is truncated (missing the `moov atom` header) and unplayable. Delete and re-run. A 5ps render of a 55-minute narration takes roughly 5–7 minutes.

### Phase 4 — Hand off

Once the MP4 is verified, switch to the channel workflows for auth checks, playlist updates, and upload.

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
