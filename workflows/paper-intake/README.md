---
workflow_id: paper_intake
workflow_kind: stage
stage_binding: paper_intake
stability: canonical
workflow_group: evidence
runner_mode: guided
default_skill: opendataloader-paper-intake
launch_templates: []
required_context:
  - package README or leaf README
  - target evidence surface or source index
  - paper files or source URLs to intake
expected_outputs:
  - original paper files placed in the package evidence surface
  - converted markdown in the evidence markdown directory when needed
  - updated paper or source index
done_when:
  - selected papers are stored locally and the package evidence index is current
approval_gate: none
---

# Paper Intake

This is the canonical tracked workflow for bringing papers into a content package.

## Purpose

The goal is to keep papers discoverable, convertible, and reusable across essay work. For most single-publication packages, that means:

- keep original PDFs under `papers/`
- keep converted markdown under `papers/markdown/`
- keep a short tracked index in `papers/index.md`

If a package already has a stronger established source layer, preserve it. Examples:

- `publications/autonomous-agents/reference/papers/`
- `publications/autonomous-agents/reference/source-index.md`
- dataset-specific paper trees inside `publications/hardware-friction/`

## Canonical Layout For Single-Publication Packages

Default target:

```text
papers/
papers/markdown/
papers/index.md
```

If a PDF download, conversion, or file move fails with `Operation not permitted` or a sandbox denial, stop and hand the user the exact command and target path. Do not write a paper-index entry for a source that has not actually landed in the package evidence surface.

Recommended meanings:

- `papers/`: original PDFs and other paper-source files
- `papers/markdown/`: OpenDataLoader PDF conversions, fallback `markitdown` conversions, or closely related derived text
- `papers/index.md`: package-local inventory with title, source link or identifier, local filenames, and a short relevance note

## Evidence-Backed Defaults

- When a package already tracks a paper manifest or source index, update that existing structure instead of creating a second parallel inventory just because `papers/index.md` is the generic default.
- Move vetted papers out of temporary holding folders or scratch notes into the canonical package paper tree as soon as they become part of the live source library.
- If a new paper only sharpens an existing claim, prefer adding it as an annotated reference or source note instead of forcing a body rewrite.
- For evidence-sensitive article rewrites, finish paper intake before hardening the blueprint or drafting the next article candidate. Temporary alphaXiv-only context is not a stable source surface.

## Conversion Flow

Use the repo-local toolchain:

```bash
.venv/bin/python workflows/skills/opendataloader-paper-intake/scripts/convert_pdf_to_markdown.py \
  path/to/paper.pdf path/to/papers/markdown/paper-name.md
```

The wrapper uses OpenDataLoader PDF as the primary converter. It writes one Markdown file per PDF, keeps page boundaries with Markdown page separators, omits images with `--image-output off`, and falls back to markitdown if the OpenDataLoader path fails. OpenDataLoader PDF requires Java 11+ in the operator environment.

Recommended flow:

1. save the original PDF into `papers/`
2. convert it into `papers/markdown/`
3. inspect the conversion for obvious extraction failures
4. update `papers/index.md`, `manifest.json`, or the package’s existing source index
5. use the converted markdown when drafting notes, companions, claims files, or source summaries

## When To Keep Both PDF And Markdown

Default: keep both.

Reasons:

- the PDF is the closest local source artifact
- the markdown is easier to quote, inspect, and feed into local writing workflows

If a conversion is poor, still keep the PDF and either:

- keep the markdown with a note in `papers/index.md` that it is noisy, or
- defer conversion until the paper is actually needed

## Index Expectations

`papers/index.md` should stay lightweight. It should make the local paper library navigable, not become another essay.

Minimum useful fields:

- title
- local PDF path
- local markdown path if present
- citation key, arXiv id, DOI, or URL
- short relevance note

If the package already keeps annotated references inside the essay or companion, the local index can stay short and point outward rather than repeating the same notes twice.

The package paper index and the article reference section do different jobs:

- `papers/index.md` is the local library surface and should stay lightweight
- the article reference section can carry longer relevance paragraphs when the essay itself needs annotated references

## Related Skill Bundle

- [`../skills/opendataloader-paper-intake/`](../skills/opendataloader-paper-intake/)
- [`../skills/markitdown-paper-intake/`](../skills/markitdown-paper-intake/) fallback

Use the tracked skill bundle for execution. The local `.agents/skills/opendataloader-paper-intake/` path is just its discovery mirror.
