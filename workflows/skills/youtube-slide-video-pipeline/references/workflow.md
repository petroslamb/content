# YouTube Slide Video Workflow

Use this file for the local slide, transcript, cue-sheet, and render path that feeds the YouTube upload skills.

## Expected Chapter Inputs

Typical chapter layout:

- `artifacts/audio/*.mp3`
- `artifacts/slides/<deck-name>/slide-*.png`
- `artifacts/transcript_*_full.txt` or numbered transcript
- `artifacts/video/` for captions, mappings, cues, and renders

## Script Map

- `scripts/align_slides_to_transcript.py`: OCR-first draft alignment against an untimestamped transcript plus the audio duration.
- `scripts/align_slides_to_captions.py`: OCR-first draft alignment against timed SRT captions.
- `scripts/build_slideshow_from_captions.py`: caption-first shortcut that drafts a cue-sheet JSON and can render a first-pass MP4, optionally using a separate render slide directory with matching filenames.
- `scripts/map_slides_to_transcript_lines.py`: optional drafting aid when you already have OCR text files and a numbered transcript.
- `scripts/line_map_markdown_to_cues.py`: converts a reviewed markdown line-map plus timed captions into a renderable cue-sheet JSON.
- `scripts/render_audio_slides_video.py`: generates a rough evenly spaced template or renders the final MP4 from a cue sheet.
- `scripts/scrape_youtube_watch_transcript.py`: captures the visible watch-page transcript into JSON for inspection or fallback analysis.
- `workflows/skills/youtube-data-api/scripts/download_video_captions.py`: preferred managed caption downloader when auth and quota are available.

## Core Sequence

### 1. Recover Captions Or Transcript Timing

Preferred managed caption path:

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/download_video_captions.py \
  --video-id <VIDEO_ID> \
  --output "publications/autonomous-agents/essays/<slug>/artifacts/video/<slug>_auto_captions.srt"
```

Watch-page transcript fallback:

```bash
.venv/bin/python scripts/scrape_youtube_watch_transcript.py \
  --video-id <VIDEO_ID> \
  --output "publications/autonomous-agents/essays/<slug>/artifacts/video/<slug>_watch_transcript.json"
```

### 2. Draft An OCR-First Mapping

Against the full transcript:

```bash
.venv/bin/python scripts/align_slides_to_transcript.py \
  --audio <audio.mp3> \
  --slides-dir <slides-dir> \
  --transcript <transcript.txt> \
  --output <ocr-first.json>
```

Against timed captions:

```bash
.venv/bin/python scripts/align_slides_to_captions.py \
  --slides-dir <slides-dir> \
  --captions <captions.srt> \
  --output <ocr-first.json>
```

Caption-first cue-sheet plus draft render shortcut:

```bash
.venv/bin/python scripts/build_slideshow_from_captions.py \
  --audio <audio.mp3> \
  --captions <captions.srt> \
  --slides-dir <ocr-slides-dir> \
  --support-slides-dir <optional-second-ocr-slides-dir> \
  --render-slides-dir <optional-render-slides-dir> \
  --render-slides-dir <optional-second-render-slides-dir> \
  --output-cues <draft-cues.json> \
  --output-video <draft-video.mp4>
```

Use `--support-slides-dir` when a second slide deck adds complementary text that improves OCR-first boundary drafting.
Use the `--slides-dir` / repeated `--render-slides-dir` split when OCR works better on one deck but the final review or rendered video should use one or more richer stitched or alternate decks that keep the same filenames.

Optional line-range drafting when OCR text files already exist:

```bash
.venv/bin/python scripts/map_slides_to_transcript_lines.py \
  --numbered-transcript <numbered-transcript.txt> \
  --ocr-dir <ocr-dir> \
  --output <line-map-draft.json>
```

### 3. Verify The Markdown Line Map

The render path expects a reviewed markdown table mapping `slide-XXX.png` to transcript line ranges. Do not render directly from unreviewed OCR output when the deck is dense or slide order diverges from transcript order.

### 4. Convert The Verified Map Into Final Cues

```bash
.venv/bin/python scripts/line_map_markdown_to_cues.py \
  --map "publications/autonomous-agents/essays/<slug>/artifacts/video/<slug>_slide_transcript_map_ocr_verified.md" \
  --captions "publications/autonomous-agents/essays/<slug>/artifacts/video/<slug>_auto_captions.srt" \
  --transcript "publications/autonomous-agents/essays/<slug>/artifacts/transcript_<Chapter Title>_numbered.txt" \
  --chapter-dir "publications/autonomous-agents/essays/<slug>" \
  --output "publications/autonomous-agents/essays/<slug>/artifacts/video/<slug>_cues_from_srt.json"
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

## Output Naming

The working convention is:

- `<slug>_auto_captions.srt`
- `<slug>_slide_transcript_map_ocr_first.*`
- `<slug>_slide_transcript_map_ocr_verified.md`
- `<slug>_cues_from_srt.json`
- `<Course Title>.mp4`

Keep these files in `artifacts/video/` next to the chapter assets.
