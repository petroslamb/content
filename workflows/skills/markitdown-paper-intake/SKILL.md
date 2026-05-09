---
name: markitdown-paper-intake
description: Legacy fallback for repo-local paper intake when OpenDataLoader PDF cannot convert a source. Prefer opendataloader-paper-intake for PDF-to-Markdown conversion, and use markitdown only as the fallback or for non-PDF sources.
---

# Markitdown Paper Intake Fallback

Use this skill only as the fallback path for repo-local paper intake and conversion, not for generic OCR advice.

The primary paper-intake converter is now OpenDataLoader PDF through `../opendataloader-paper-intake/`.

## Working Rules

1. Start with the tracked workflow doc at `../../../workflows/paper-intake/README.md`.
2. Prefer the OpenDataLoader wrapper for PDFs:

   ```bash
   .venv/bin/python workflows/skills/opendataloader-paper-intake/scripts/convert_pdf_to_markdown.py input.pdf output.md
   ```

3. Use the repo-local markitdown binary only as fallback:

   ```bash
   .venv/bin/markitdown input.pdf -o output.md
   ```

4. Prefer placing source PDFs or HTML exports under the target package `papers/` directory.
5. For single-publication packages, prefer `papers/markdown/` for converted markdown and `papers/index.md` for the package paper index unless the package already has a stronger established variant.
6. Keep filenames descriptive and stable. Do not rename aggressively if the package already has a working convention.
7. When converting several papers, write outputs first, then summarize failures or partial conversions instead of stopping after the first bad file.
8. If the package already has a paper manifest or source index, update that instead of creating a duplicate second index.

## Reference Map

- `../../../workflows/paper-intake/README.md`: canonical tracked paper-intake workflow.
- `../../../README.md`: repo package model, vocabulary, and package-map context.
