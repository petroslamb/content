---
name: pdf-slides-to-substack-images
description: Convert slide PDFs into high-DPI, zero-padded PNG folders for Substack or article publishing. Use when Codex needs to turn a single deck PDF or a directory of PDFs into per-slide images, verify page counts and sample dimensions, and report the output folders. Prefer this skill for macOS workflows that rely on pdfinfo, pdftocairo, and sips.
---

# PDF Slides to Substack Images

Use `workflows/skills/pdf-slides-to-substack-images/scripts/export_pdf_slides.py` for the normal path. It handles PDF discovery, per-page export, zero-padded filenames, and verification without GNU-specific shell features.

## Gather Context

- Resolve the input as either one PDF or a directory of PDFs.
- Confirm `pdfinfo`, `pdftocairo`, and `sips` are available before starting work.
- Default to creating one output folder per PDF next to the source file unless the user asks for a different root.

## Run The Exporter

Export one PDF:

```bash
.venv/bin/python workflows/skills/pdf-slides-to-substack-images/scripts/export_pdf_slides.py /path/to/deck.pdf
```

Export every PDF in a directory:

```bash
.venv/bin/python workflows/skills/pdf-slides-to-substack-images/scripts/export_pdf_slides.py /path/to/decks/
```

Change DPI or centralize outputs:

```bash
.venv/bin/python workflows/skills/pdf-slides-to-substack-images/scripts/export_pdf_slides.py /path/to/decks --dpi 300 --output-root /path/to/output
```

## Expected Output

- Create one folder per PDF, named from the PDF basename.
- Name slides as `slide-001.png`, `slide-002.png`, and so on.
- Keep numbering zero-padded with a minimum width of 3 digits.
- Report, for each PDF, the source path, page count, PNG count, output folder, sample dimensions, and any failed pages.
- Treat the exported slide folder as a raw source surface. Do not replace semantically named article images or edit markdown embeds from this skill.

## Verification

- Compare PNG count with the PDF page count for each folder.
- Inspect the first slide dimensions with `sips`.
- Treat missing binaries, page-count mismatches, or failed page exports as errors and report them explicitly.

## Troubleshoot

- If page counts do not match, rerun only the missing pages or rerun the script after clearing the affected output folder.
- If output images look soft, increase or enforce DPI instead of resizing the PNGs later.
- Do not use this skill for slide redesign, OCR, or content editing. Its job is export and verification.

## Reference Map

- `../../../workflows/notebooklm-artifacts/README.md`: tracked context for the slide-PDF export step inside the article artifact workflow.
- `references/rollout-lessons.md`: macOS-specific export constraints and the reason this skill uses a Python exporter instead of ad hoc shell loops.
