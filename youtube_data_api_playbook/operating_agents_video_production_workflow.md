# Operating Agents Video Production Workflow

This note captures the workflow used to turn the chapter slide decks and narrated audio into the long-form *Operating Agents* course videos now live on YouTube.

## Inputs Per Chapter

Each chapter folder is expected to provide:

- `artifacts/audio/*.mp3`
- `artifacts/slides/<deck-name>/slide-*.png`
- `artifacts/transcript_*_full.txt`
- `artifacts/video/`

The `video/` folder is the working area for:

- downloaded YouTube auto-captions
- OCR-first draft mappings
- verified cue sheets
- rendered replacement MP4s

## Local Tools

- [render_audio_slides_video.py](/Users/petros/Projects/content/scripts/render_audio_slides_video.py): renders an MP4 from narrated audio plus a cue sheet
- [align_slides_to_transcript.py](/Users/petros/Projects/content/scripts/align_slides_to_transcript.py): OCR-first transcript matching draft
- [align_slides_to_captions.py](/Users/petros/Projects/content/scripts/align_slides_to_captions.py): OCR-first draft cue-sheet generation against timed YouTube captions
- [line_map_markdown_to_cues.py](/Users/petros/Projects/content/scripts/line_map_markdown_to_cues.py): converts a verified slide-to-transcript markdown map plus timed captions into a renderable cue-sheet JSON
- [download_video_captions.py](/Users/petros/Projects/content/youtube_data_api_playbook/scripts/download_video_captions.py): downloads the managed caption track for the currently live YouTube video
- [replace_course_video.py](/Users/petros/Projects/content/youtube_data_api_playbook/scripts/replace_course_video.py): uploads a replacement full-course video with preserved metadata and swaps the playlist entry
- [sync_operating_agents_crosslinks.py](/Users/petros/Projects/content/youtube_data_api_playbook/scripts/sync_operating_agents_crosslinks.py): re-syncs description navigation after full-video IDs change

## Working Method

1. Download the automatic caption track from the live YouTube course video.
2. Run OCR-first alignment to get a draft sense of where slide topics appear in the transcript.
3. Inspect the actual slides and correct the draft. Do not trust OCR alone on dense diagrams, small labels, or structurally reordered slides.
4. Build a verified cue sheet that records only slide-change timestamps, not subtitle text.
5. Render the long-form slideshow cut from the verified cue sheet.
6. Upload the replacement as a new YouTube video and swap it into the course playlist.
7. Update local metadata and description cross-links so TL;DR videos point to the replacement full-course cut.

## No-Quota Subtitle Recovery

The Data API quota is not required for the local alignment stage once the chapter assets already exist.

Use this sequence:

1. Check whether `artifacts/video/<slug>_auto_captions.srt` is real or an empty placeholder.
2. If it is empty, recover YouTube's automatic English subtitles with `yt-dlp` instead of the Data API.
3. Convert the verified markdown line map into a cue-sheet JSON using the recovered `.srt`.

This was the working path for `reasoning`, `multi-agent`, `safety`, and `optimization` after the YouTube Data API quota was exhausted.

Install `yt-dlp` into the repo environment if needed:

```bash
.venv/bin/pip install yt-dlp
```

Recover a chapter subtitle track without using the Data API:

```bash
.venv/bin/yt-dlp \
  --skip-download \
  --write-auto-sub \
  --sub-lang en \
  --convert-subs srt \
  -o "autonomous-agent-blueprint/essays/<slug>/artifacts/video/<slug>_auto_captions.%(ext)s" \
  "https://www.youtube.com/watch?v=<FULL_VIDEO_ID>"
```

If `yt-dlp` writes `<slug>_auto_captions.en.srt`, rename it back to the chapter-standard filename:

```bash
mv \
  "autonomous-agent-blueprint/essays/<slug>/artifacts/video/<slug>_auto_captions.en.srt" \
  "autonomous-agent-blueprint/essays/<slug>/artifacts/video/<slug>_auto_captions.srt"
```

## Verified Cue-Sheet Conversion

Once the chapter has:

- a verified markdown line map
- a non-empty `*_auto_captions.srt`
- the numbered transcript

convert the slide swaps into actual timestamps:

```bash
.venv/bin/python scripts/line_map_markdown_to_cues.py \
  --map "autonomous-agent-blueprint/essays/<slug>/artifacts/video/<slug>_slide_transcript_map_ocr_verified.md" \
  --captions "autonomous-agent-blueprint/essays/<slug>/artifacts/video/<slug>_auto_captions.srt" \
  --transcript "autonomous-agent-blueprint/essays/<slug>/artifacts/transcript_<Chapter Title>_numbered.txt" \
  --chapter-dir "autonomous-agent-blueprint/essays/<slug>" \
  --output "autonomous-agent-blueprint/essays/<slug>/artifacts/video/<slug>_cues_from_srt.json"
```

Important details:

- The cue builder sorts slides by mapped transcript line start, not by filename.
- This matters because some decks are ordered differently from the spoken transcript.
- Summary slides can still overlap on the same transcript block. That is editorial, not a tooling bug.
- Low match scores should be treated as review targets before rendering.

## Output Naming

Keep the generated files near the chapter assets. The working convention is:

- `<slug>_auto_captions.srt`
- `<slug>_slide_transcript_map_ocr_first.md`
- `<slug>_slide_transcript_map_ocr_verified.md`
- `<slug>_cues_from_srt.json`
- `<slug>_cues_youtube_verified.json`
- `<Course Title>.mp4`

## Quality Bar

- Caption timestamps are the timing anchor.
- OCR is only a draft alignment layer.
- Final decisions should be checked against the slide images themselves.
- When transcript flow and slide-number order conflict, favor semantic order and record that in the cue sheet.
- If a local `*_auto_captions.srt` is zero bytes, do not trust it. Recover a real subtitle file before building cue sheets.
