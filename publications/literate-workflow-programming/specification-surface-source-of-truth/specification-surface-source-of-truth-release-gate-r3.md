# Release Gate Checklist

## Package

- Package: `literate-workflow-programming/specification-surface-source-of-truth`
- Live draft: `publications/literate-workflow-programming/specification-surface-source-of-truth/specification-surface-source-of-truth.md`
- Canonical publish target: `https://lambpetros.substack.com/p/the-specification-surface-is-the`
- Substack draft or target URL: `https://lambpetros.substack.com/publish/post/196091276`
- Release gate owner: Codex, with explicit user approval
- Date: 2026-05-04

## Verdict

Verdict: release_ready

Blocking reason if any: none.

## Draft Integrity

- [x] Canonical live draft is the file being released.
- [x] No unreviewed candidate draft is being published by accident.
- [x] Title, subtitle, opening, and ending match the latest promotion decision.
- [x] No visible internal workflow notes remain in the public essay.
- [x] Limits, caveats, and reference claims match the approved blueprint or final review.

## Evidence And References

- [x] Body citations are present where the argument needs them.
- [x] Body citations use author-year parentheticals where cited papers carry claims.
- [x] Reference entries use consistent author/year/title/link formatting where available.
- [x] Cited paper entries use linked h4 headings to the arXiv paper or canonical source where available.
- [x] Newly added citations have a visible reason to exist.
- [x] Sources doing substantive argumentative work have contribution paragraphs, not only bibliographic entries.
- [x] Repo-only evidence, companions, or datasets are linked intentionally.
- [x] Claims that were forbidden by the evidence ledger or review artifacts are not present.

## Media And Artifacts

- [x] Every markdown image path resolves locally.
- [x] Every kept image has an editorial reason to be in the essay.
- [x] Image filenames are stable and semantic enough for future maintenance.
- [x] Video TL;DR marker is present only if a video artifact exists and the post should include it.
- [x] Transcript-derived edits came from a complete transcript, not a preview.
- [x] Generated artifacts are not confused with publishable article assets.

## Substack Readiness

- [x] Target draft or post ID is known when syncing to an existing draft.
- [x] `config.substack_url` and `config.substack_post_id` are current if the package uses them.
- [x] Local video markers match the publishing script's expected `#### Video TL;DR` format if used.
- [x] Existing uploaded video block should be preserved or intentionally replaced.
- [x] External publication, archive sync, and distribution side effects have approval.

## Link And Archive Readiness

- [x] Internal repo links point at current canonical package paths.
- [x] Public links are Substack-first for already published posts.
- [x] Archive sync path is known for after publication.
- [x] Any known repo-link migration follow-up is recorded.

## Rhythm Remediation

The public page was found to contain a short-question cadence introduced by the publication-sharpness pass. The canonical draft has been repaired to restore the publication voice rhythm, and `scripts/generate_editorial_report.py` now includes a `sentence_rhythm` advisory so future article-polish and essay-iteration passes flag repeated staccato edits before release.

## Final Commands

```bash
git diff --name-status -- publications/literate-workflow-programming/specification-surface-source-of-truth/ workflows/essay-iteration workflows/article-polish scripts/generate_editorial_report.py
rg -n '!\\[[^]]*\\]\\(' publications/literate-workflow-programming/specification-surface-source-of-truth/specification-surface-source-of-truth.md
.venv/bin/python scripts/generate_editorial_report.py --package literate-workflow-programming/specification-surface-source-of-truth --stdout
npm run check:repo-links
```

## Required Fixes

- None. The live Substack post has been repaired from the canonical markdown, the reference-format pass is synced, and the tracked public archive has been refreshed.

## Approval Boundary

External side effects approved?

- [ ] No external side effect requested.
- [x] Draft sync approved.
- [x] Live publish approved.
- [x] Archive sync approved.
- [x] Distribution posting approved.
