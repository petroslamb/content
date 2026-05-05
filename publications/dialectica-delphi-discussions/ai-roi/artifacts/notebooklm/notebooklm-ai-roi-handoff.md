# NotebookLM Handoff: AI ROI Delphi Prototype

Notebook title: `Dialectica Delphi - AI ROI Operator Prototype`

Notebook ID: `1b26a133-699a-4772-89a4-8150da8d900c`

Notebook URL: `https://notebooklm.google.com/notebook/1b26a133-699a-4772-89a4-8150da8d900c`

## Source Boundary

Uploaded only the constrained AI ROI work-sample packet:

- `00-read-me-first.md`
- `01-data-model-instance.md`
- `source-inventory-and-handling-notes.md`
- `artifact-map.md`
- `claim-map.md`
- `give-get-actions.md`
- `michael-pere-ai-roi-brief.md`
- `session-record.md`

Excluded from upload:

- raw transcript and raw chat
- Claude Mythos and Hormuz Fallout
- private decision brief and final role email
- support notes, career files, pricing, title, and compensation material

## Prompts Used

- Slide deck: `publications/dialectica-delphi-discussions/ai-roi/notebooklm-source/prompts/slide-deck-prompt.md`
- Podcast: `publications/dialectica-delphi-discussions/ai-roi/notebooklm-source/prompts/podcast-prompt.md`
- Explainer video: `publications/dialectica-delphi-discussions/ai-roi/notebooklm-source/prompts/video-prompt.md`

## Generated Artifacts

Sendable brief:

- Local PDF: `../sendable/ai-roi-delphi-operating-loop-brief.pdf`
- Local source markdown: `../sendable/ai-roi-delphi-operating-loop-brief.md`
- Local HTML render: `../sendable/ai-roi-delphi-operating-loop-brief.html`
- Status: one-page PDF generated from the sendable markdown source, with no local markdown links

Slide deck:

- Artifact ID: `ef1a1051-e6d6-42d0-9400-f96ea1032341`
- NotebookLM title: `The Delphi Operating Loop`
- Status: completed
- Local PDF: `ai-roi-delphi-operating-loop-deck.pdf`
- Local PPTX: `ai-roi-delphi-operating-loop-deck.pptx`
- Rendered page images: `deck-pages/page-1.png` through `deck-pages/page-8.png`

Audio:

- Artifact ID: `17a144ee-889e-434d-9227-ba16f440c066`
- NotebookLM title: `Fixing AI ROI bottlenecks with Delphi`
- Generation settings: `--format deep-dive --length short`
- Status at handoff: pending after two bounded waits

Explainer video:

- Artifact ID: `241f31ef-6220-431a-8485-9e193dbb79c4`
- NotebookLM title: `Delphi Prototype: AI ROI`
- Generation settings: `--format explainer --style classic`
- Prompt: `publications/dialectica-delphi-discussions/ai-roi/notebooklm-source/prompts/video-prompt.md`
- Status: completed
- Local MP4: `ai-roi-delphi-operating-loop-explainer.mp4`
- Duration: 6:10

## Initial Deck Read

The deck followed the requested 8-slide structure and stayed within the AI ROI example. It is useful as a first NotebookLM-generated draft, but it should be treated as raw material before sending.

Known review points:

- The deck uses NotebookLM's blueprint visual style and watermark.
- Text is readable, but several slides are visually dense.
- The story is on target: source material, AI ROI bottleneck, operating loop, concrete artifacts, Michael evaluation, Pere loop, final decision.
- Before sending to Pere and Michael, convert the useful structure into a cleaner local deck or manually polish the PPTX.

## Next Step

If the audio completes, download it to this folder:

```bash
.venv/bin/notebooklm download audio \
  -n 1b26a133-699a-4772-89a4-8150da8d900c \
  -a 17a144ee-889e-434d-9227-ba16f440c066 \
  publications/dialectica-delphi-discussions/ai-roi/artifacts/notebooklm/ai-roi-delphi-operating-loop-deep-dive.mp3
```

Then recover the transcript through the NotebookLM audio round-trip before building a timed slide video.

Explainer video was downloaded with:

```bash
.venv/bin/notebooklm download video \
  -n 1b26a133-699a-4772-89a4-8150da8d900c \
  -a 241f31ef-6220-431a-8485-9e193dbb79c4 \
  publications/dialectica-delphi-discussions/ai-roi/artifacts/notebooklm/ai-roi-delphi-operating-loop-explainer.mp4
```

The video should be reviewed before use. The prompt asked for a 4-6 minute private explainer with seven segments: intro, problem, five-step loop, source/claim, artifact/give-get, expert memory/Michael test, and a concluding matrix.
