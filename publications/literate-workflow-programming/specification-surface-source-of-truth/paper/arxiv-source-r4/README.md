---
kind: arxiv_source_packet
package: "literate-workflow-programming/specification-surface-source-of-truth"
revision: 4
status: generated_local_packet
created: "2026-05-05"
workflow: paper_development
source_draft: "../specification-surface-source-of-truth-paper-draft-r4.md"
posting_allowed: false
---

# arXiv Source Packet R4

This folder holds the generated arXiv-facing source packet for R4.

## Files

- `spec_surface_r4_arxiv.tex`: standalone LaTeX source generated from the R4 Markdown draft with references rendered by Pandoc citeproc.
- `spec_surface_r4_arxiv_source.tar.gz`: local upload archive containing only `spec_surface_r4_arxiv.tex`; generated and not required for git history.

## Regeneration Command

Run from the package-local `paper/` folder:

```bash
pandoc specification-surface-source-of-truth-paper-draft-r4.md \
  --citeproc \
  --bibliography=references.bib \
  --shift-heading-level-by=-1 \
  -V geometry:margin=1in \
  -s \
  -o arxiv-source-r4/spec_surface_r4_arxiv.tex

tar -czf arxiv-source-r4/spec_surface_r4_arxiv_source.tar.gz \
  -C arxiv-source-r4 \
  spec_surface_r4_arxiv.tex
```

## Boundary

This packet is prepared for a human arXiv posting decision. It is not a submission record and does not authorize public posting.
