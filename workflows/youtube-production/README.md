# YouTube Production

This is the tracked canonical workflow for the local production stage that turns narrated audio, slide images, transcripts, and captions into a verified MP4 before any YouTube upload or replacement step.

Use this workflow before mutating the channel. It is the local production layer behind the YouTube upload skills.

## Evidence-Backed Defaults

- Caption timestamps are the timing anchor. OCR is only a drafting aid.
- `quotaExceeded` should not stop local production work. Keep moving on subtitle recovery, cue generation, and rendering.
- Prefer a real timed `.srt` file over watch-page transcript text whenever possible.
- Keep render inputs and outputs close to the chapter’s `artifacts/video/` surface.
- Do not render from unreviewed OCR output when the deck is dense, reordered, or diagram-heavy.

## Canonical Flow

### 1. Recover Captions Or Transcript Timing

Preferred managed caption path:

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/download_video_captions.py \
  --video-id <VIDEO_ID> \
  --output <chapter>/artifacts/video/<slug>_auto_captions.srt
```

When that path is blocked, recover subtitles with `yt-dlp` or inspect the watch-page transcript with `scripts/scrape_youtube_watch_transcript.py`.

### 2. Draft A Slide Map

Against the untimestamped transcript:

```bash
.venv/bin/python scripts/align_slides_to_transcript.py --audio ... --slides-dir ... --transcript ... --output ...
```

Against timed captions:

```bash
.venv/bin/python scripts/align_slides_to_captions.py --slides-dir ... --captions ... --output ...
```

If OCR text files and a numbered transcript already exist, `scripts/map_slides_to_transcript_lines.py` can draft line ranges before manual review.

### 3. Review The Verified Markdown Map

The render path expects a reviewed markdown slide-to-transcript map. Low OCR match scores are review targets, not auto-accepted timings. If the spoken order diverges from the slide order, record that deliberately in the verified map.

### 4. Convert The Verified Map Into Final Cues

```bash
.venv/bin/python scripts/line_map_markdown_to_cues.py \
  --map <verified-map.md> \
  --captions <captions.srt> \
  --transcript <numbered-transcript.txt> \
  --chapter-dir <chapter-dir> \
  --output <cues.json>
```

### 5. Render The MP4

Template draft:

```bash
.venv/bin/python scripts/render_audio_slides_video.py template \
  --audio <audio.mp3> \
  --slides-dir <slides-dir> \
  --output <draft-cues.json>
```

Final render:

```bash
.venv/bin/python scripts/render_audio_slides_video.py render \
  --cues <cues.json> \
  --output <output.mp4>
```

### 6. Hand Off To Channel Workflows

Once the MP4, cue sheet, and metadata are ready:

- use [`../youtube-channel-ops/README.md`](../youtube-channel-ops/README.md) for auth checks, captions, general playlist state, or Shorts maintenance
- use [`../youtube-series-operating-agents/README.md`](../youtube-series-operating-agents/README.md) when the task is the Operating Agents course or TL;DR series

## Related Surfaces

- [`../../scripts/README.md`](../../scripts/README.md): tracked script map for the local render pipeline.
- [`../skills/youtube-slide-video-pipeline/`](../skills/youtube-slide-video-pipeline/): execution-focused skill bundle.
- [`../skills/youtube-data-api/`](../skills/youtube-data-api/): managed caption download and channel-side follow-up.
