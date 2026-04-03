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
4. If the Data API quota is exhausted, recover subtitles with `yt-dlp` or inspect the watch-page transcript instead of blocking the pipeline.
5. Do not trust unreviewed OCR output on dense diagrams, reordered slides, or small labels. Verify the final mapping before rendering.

## Core Path

### Recover Timing Inputs

Use the managed caption downloader when auth and quota are available:

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/download_video_captions.py \
  --video-id <VIDEO_ID> \
  --output <chapter>/artifacts/video/<slug>_auto_captions.srt
```

If that path is blocked, switch to `yt-dlp` or inspect the watch-page transcript with `scripts/scrape_youtube_watch_transcript.py`.

### Draft The Slide Mapping

Use the draft aligners for first-pass timing:

```bash
.venv/bin/python scripts/align_slides_to_transcript.py --audio ... --slides-dir ... --transcript ... --output ...
.venv/bin/python scripts/align_slides_to_captions.py --slides-dir ... --captions ... --output ...
```

If you already have slide OCR text files and a numbered transcript, `scripts/map_slides_to_transcript_lines.py` can draft line ranges before manual verification.

### Convert A Verified Map Into Cues

Once the markdown slide-to-transcript map is reviewed, build the renderable cue sheet:

```bash
.venv/bin/python scripts/line_map_markdown_to_cues.py \
  --map <verified-map.md> \
  --captions <captions.srt> \
  --transcript <numbered-transcript.txt> \
  --chapter-dir <chapter-dir> \
  --output <cues.json>
```

### Render The MP4

Generate a rough evenly spaced template if needed:

```bash
.venv/bin/python scripts/render_audio_slides_video.py template \
  --audio <audio.mp3> \
  --slides-dir <slides-dir> \
  --output <draft-cues.json>
```

Render the final video from the verified cue sheet:

```bash
.venv/bin/python scripts/render_audio_slides_video.py render \
  --cues <cues.json> \
  --output <output.mp4>
```

### Hand Off To Upload Skills

Once the MP4 and metadata are ready, switch to `youtube-operating-agents` or `youtube-data-api` for replacement uploads, playlist updates, and description sync.

## Reference Map

- `../../../workflows/youtube-production/README.md`: tracked canonical local production workflow for captions, mapping, cue generation, and rendering.
- `references/workflow.md`: input layout, script map, example commands, and output naming.
- `references/rollout-lessons.md`: quota fallback, subtitle recovery, and the constraints recovered from the Operating Agents YouTube rollout.
