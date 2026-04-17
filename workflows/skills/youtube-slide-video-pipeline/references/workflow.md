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
- `scripts/create_publication_shorts_from_longform.py`: slices a verified long-form MP4 into named short clips from a manifest, then renders portrait variants for Shorts upload.
- `workflows/skills/youtube-data-api/scripts/download_video_captions.py`: preferred managed caption downloader when auth and quota are available.

## Core Sequence

### 1. Recover Captions Or Transcript Timing

Preferred managed caption path:

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/download_video_captions.py \
  --video-id <VIDEO_ID> \
  --output "publications/autonomous-agents/essays/<slug>/artifacts/video/<slug>_auto_captions.srt"
```

If you only have local audio, recover timings by temporary upload:

```bash
.venv/bin/python workflows/skills/youtube-data-api/scripts/recover_transcript_via_temporary_upload.py \
  --audio-path <audio.mp3> \
  --image-path <still-image.png> \
  --title "<temporary caption recovery title>" \
  --output "publications/autonomous-agents/essays/<slug>/artifacts/video/<slug>_auto_captions.srt"
```

Watch-page transcript fallback:

```bash
.venv/bin/python scripts/scrape_youtube_watch_transcript.py \
  --video-id <VIDEO_ID> \
  --output "publications/autonomous-agents/essays/<slug>/artifacts/video/<slug>_watch_transcript.json"
```

### 2. Draft An OCR-First Mapping Or Switch Early To Manual Review

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

If the deck is already a raw numbered sequence that follows the narration, preserve all numbered slides and use OCR only to recover likely section boundaries. Do not let weak OCR matches collapse the deck into a few late slides.

Optional line-range drafting when OCR text files already exist:

```bash
.venv/bin/python scripts/map_slides_to_transcript_lines.py \
  --numbered-transcript <numbered-transcript.txt> \
  --ocr-dir <ocr-dir> \
  --output <line-map-draft.json>
```

### 3. Verify The Reviewed Cue Plan

Correct slide timing matters more than even spacing. If OCR under-matches a dense deck, replace it with a hand-built cue sheet from the SRT plus a visual slide read. The even-spacing template is a scaffold, not a final timing plan.
The render path expects a reviewed timing plan. Do not render directly from unreviewed OCR output when the deck is dense or slide order diverges from transcript order.

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
  --output <output.mp4> \
  --fps 5
```

Render uses the script defaults for slide videos: `libx264`, `-preset medium`, `crf 23`, `1920x1080`, and `192kbps AAC`.

Before promotion, check for failed byproducts in the video artifact folder:

```bash
find <chapter-or-package>/artifacts/video -type f -size 0
```

Zero-byte files should be deleted or regenerated before handoff.

### 6. Optional Shorts Derivation From The Long-Form

When the rendered long-form has strong stand-alone segments, derive Shorts from the verified MP4 plus its timed `.srt`:

1. pick segments that each make one idea land cleanly
2. write `artifacts/video/shorts/shorts_manifest.json`
3. render them with:

```bash
.venv/bin/python scripts/create_publication_shorts_from_longform.py \
  --video-file <longform.mp4> \
  --manifest <shorts_manifest.json>
```

This writes both `landscape/` and `portrait/` outputs under `artifacts/video/shorts/`.

After Shorts rendering, run the same zero-byte check on `artifacts/video/shorts/` before treating the clips as upload-ready.

## Output Naming

The working convention is:

- `<slug>_auto_captions.srt`
- `<slug>_slide_transcript_map_ocr_first.*`
- `<slug>_slide_transcript_map_ocr_verified.md`
- `<slug>_cues_from_srt.json`
- `<Course Title>.mp4`

Keep these files in `artifacts/video/` next to the chapter assets.

If Shorts are derived from the long-form, keep the adjacent convention:

- `artifacts/video/shorts/shorts_manifest.json`
- `artifacts/video/shorts/landscape/*.mp4`
- `artifacts/video/shorts/portrait/*_portrait.mp4`

Verify the output duration against the narration after render. If the video stream overruns the audio, trim the final MP4 back to the audio duration before promotion.

## Render Compatibility Note

When the output MP4 is intended for Substack, prefer a standard web-delivery envelope even for static-slide videos:

- resolution at `1080p` or `1440p`
- `H.264` video
- bitrate at or below roughly `8 Mbps`
- frame rate between `5` and `120` fps
- `AAC` audio

This reduces the chance of slow-processing warnings on upload.
