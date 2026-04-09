---
name: youtube-slide-video-pipeline
description: Use when Codex needs to turn repo slide decks plus narrated audio, transcripts, or captions into long-form YouTube-ready MP4s, draft or verify cue sheets, recover transcript timing, or prepare replacement-course assets before using the YouTube upload skills.
---

# YouTube Slide Video Pipeline

Use this skill for the local production stage before YouTube channel writes. Use `youtube-data-api` or `youtube-operating-agents` only after the MP4, captions, cue sheet, and metadata inputs are ready.

## Working Rules

1. Prefer local alignment and rendering work first. This stage does not require YouTube write quota.
2. Caption timestamps are the timing anchor. OCR is only a drafting aid.
3. Keep generated mapping, cue, caption, and render files near the chapter's `artifacts/video/` folder.
4. If you only have local audio, recover a real `.srt` via the temporary-upload path instead of inventing timings from an untimed transcript.
5. If the Data API quota is exhausted, recover subtitles with `yt-dlp` or inspect the watch-page transcript instead of blocking the pipeline.
6. Do not trust unreviewed OCR output on dense diagrams, reordered slides, or small labels. Verify the final mapping before rendering.
7. If the raw numbered deck already follows the narration, keep all numbered slides and place them by section timing. Do not let weak OCR matches drop large parts of the deck.
8. Correct slide timing matters more than uniform spacing. Even spacing is a scaffold, not a final cue plan.
9. If the MP4 is headed for Substack, prefer standard web-delivery: `1080p` or `1440p`, `H.264`, bitrate no higher than ~8 Mbps, **5 fps for slide-only videos**, and `AAC` audio.
10. Render uses script defaults: `-preset medium`, `crf 23`, 1920×1080, 192kbps AAC. Don't adjust these for slideshows.
9. Verify final MP4 duration against the narration. If the container overruns the audio, trim it back before promotion.

## Core Paths

All command sequences, full script usage, and output conventions are in [`references/workflow.md`](references/workflow.md).

### High-level sequence

1. **Recover timing** — download auto-captions (Data API), use the temporary-upload path for local audio, or fall back to `yt-dlp` / watch-page scrape
2. **Build cues** — OCR alignment if scores > 0.30, otherwise manual SRT + visual slide curation
3. **Render MP4** — `scripts/render_audio_slides_video.py render --fps 5` for slide-only videos
4. **Verify duration** — confirm the MP4 tracks the narration and trim if needed
5. **Hand off** — to `youtube-operating-agents` or `youtube-data-api` for channel writes

### Multi-deck interleaving

When a package has visually distinct variants of the same slides: read them all, manually map each slide to audio topics, and interleave for visual variety. Aim for a slide change every 1–3 minutes. The auto-interleaving in `build_slideshow_from_captions.py` only works when decks share identical filenames, so manual curation is usually required.

### Interrupted renders

If rendering crashes mid-write (background timeout, OOM, etc.) the output MP4 is truncated — missing the `moov atom` — and unplayable. Delete it and re-run.

## Reference Map

- [`references/workflow.md`](references/workflow.md): input layout, script map, exact bash commands, output naming.
- [`references/rollout-lessons.md`](references/rollout-lessons.md): quota fallback, subtitle recovery, and constraints recovered from the Operating Agents YouTube rollout.
- `../../../workflows/youtube-production/README.md`: tracked canonical local production workflow with decision logic and multi-deck strategy.
