# PDF export rollout lessons

Use this file when the export approach needs justification or when a shell-only attempt starts failing on macOS.

## Why The Exporter Exists

- Earlier repo work used manual `pdftoppm` loops and rename passes.
- The stable skill path now uses `pdfinfo`, `pdftocairo`, and `sips` through `scripts/export_pdf_slides.py` because it is deterministic and avoids GNU-only shell features.

## macOS Constraints

- Do not rely on `mapfile` or other GNU bash helpers.
- Export per page with `pdftocairo -singlefile` and write the final zero-padded filename directly.
- Verify page counts and sample dimensions immediately after export instead of assuming the raster pass succeeded.

## Output Expectations

- Filenames should be `slide-001.png`, `slide-002.png`, and so on.
- Padding should be at least three digits.
- The output directory should sit next to the source PDF unless the caller chooses a shared `--output-root`.
