---
name: opendataloader-paper-intake
description: Use when Codex needs to place papers into a package's canonical source tree, convert PDFs to single-file markdown with OpenDataLoader PDF as the primary converter, omit images, fall back to markitdown on failure, and update the package paper index using the tracked paper-intake workflow.
---

# OpenDataLoader Paper Intake

Use this skill for repo-local paper intake and PDF-to-Markdown conversion, not for generic OCR advice.

## Working Rules

1. Start with the tracked workflow doc at `../../../workflows/paper-intake/README.md`.
2. Use the repo wrapper rather than calling the converter directly:

   ```bash
   .venv/bin/python workflows/skills/opendataloader-paper-intake/scripts/convert_pdf_to_markdown.py input.pdf output.md
   ```

3. OpenDataLoader PDF requires Java 11+. Check `java -version` when bootstrapping a new machine.
4. For PDF sources, the wrapper uses OpenDataLoader PDF first with Markdown-only output, one Markdown file per PDF, page separators, and images disabled.
5. Keep `markitdown` installed as the fallback converter. The wrapper falls back to it when OpenDataLoader fails or when the source is not a PDF.
6. Prefer placing source PDFs or HTML exports under the target package `papers/` directory.
7. For single-publication packages, prefer `papers/markdown/` for converted markdown and `papers/index.md` for the package paper index unless the package already has a stronger established variant.
8. Keep filenames descriptive and stable. Do not rename aggressively if the package already has a working convention.
9. When converting several papers, write outputs first, then summarize failures or partial conversions instead of stopping after the first bad file.
10. If the package already has a paper manifest or source index, update that instead of creating a duplicate second index.

## Direct OpenDataLoader Equivalent

Use this only when debugging the wrapper:

```bash
.venv/bin/opendataloader-pdf input.pdf \
  --format markdown \
  --image-output off \
  --markdown-page-separator "<!-- page %page-number% -->" \
  --output-dir output/
```

The canonical conversion should still go through the wrapper so fallback behavior stays consistent.

## Reference Map

- `../../../workflows/paper-intake/README.md`: canonical tracked paper-intake workflow.
- `../../../README.md`: repo package model, vocabulary, and package-map context.
- `scripts/convert_pdf_to_markdown.py`: primary OpenDataLoader conversion wrapper with markitdown fallback.
