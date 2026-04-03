---
name: markitdown-paper-intake
description: Use when Codex needs to place papers into a package's canonical source tree, convert PDFs or HTML papers to markdown with the repo-local markitdown binary, and update the package's paper index using the tracked paper-intake workflow.
---

# Markitdown Paper Intake

Use this skill for repo-local paper intake and conversion, not for generic OCR advice.

## Working Rules

1. Start with the tracked workflow doc at `../../../workflows/paper-intake/README.md`.
2. Use the repo-local binary: `.venv/bin/markitdown`.
3. Prefer placing source PDFs or HTML exports under the target package `papers/` directory.
4. For single-publication packages, prefer `papers/markdown/` for converted markdown and `papers/index.md` for the package paper index unless the package already has a stronger established variant.
5. Keep filenames descriptive and stable. Do not rename aggressively if the package already has a working convention.
6. When converting several papers, write outputs first, then summarize failures or partial conversions instead of stopping after the first bad file.
7. If the package already has a paper manifest or source index, update that instead of creating a duplicate second index.

## Reference Map

- `../../../workflows/paper-intake/README.md`: canonical tracked paper-intake workflow.
- `../../../README.md`: repo package model, vocabulary, and package-map context.
