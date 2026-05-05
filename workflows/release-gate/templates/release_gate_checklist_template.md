# Release Gate Checklist

## Package

- Package:
- Live draft:
- Canonical publish target:
- Substack draft or target URL:
- Release gate owner:
- Date:

## Verdict

Choose one:

- `release_ready`
- `release_ready_after_minor_fixes`
- `blocked`

Verdict:

Blocking reason if any:

## Draft Integrity

- [ ] Canonical live draft is the file being released.
- [ ] No unreviewed candidate draft is being published by accident.
- [ ] Title, subtitle, opening, and ending match the latest promotion decision.
- [ ] No visible internal workflow notes remain in the public essay.
- [ ] Limits, caveats, and reference claims match the approved blueprint or final review.

## Evidence And References

- [ ] Body citations are present where the argument needs them.
- [ ] Body citations use author-year parentheticals where cited papers carry claims.
- [ ] Reference entries use consistent author/year/title/link formatting where available.
- [ ] Cited paper entries use linked h4 headings to the arXiv paper or canonical source where available.
- [ ] Newly added citations have a visible reason to exist.
- [ ] Sources doing substantive argumentative work have contribution paragraphs, not only bibliographic entries.
- [ ] Repo-only evidence, companions, or datasets are linked intentionally.
- [ ] Claims that were forbidden by the evidence ledger or review artifacts are not present.

## Media And Artifacts

- [ ] Every markdown image path resolves locally.
- [ ] Every kept image has an editorial reason to be in the essay.
- [ ] Image filenames are stable and semantic enough for future maintenance.
- [ ] Video TL;DR marker is present only if a video artifact exists and the post should include it.
- [ ] Transcript-derived edits came from a complete transcript, not a preview.
- [ ] Generated artifacts are not confused with publishable article assets.

## Substack Readiness

- [ ] Target draft or post ID is known when syncing to an existing draft.
- [ ] `config.substack_url` and `config.substack_post_id` are current if the package uses them.
- [ ] Local video markers match the publishing script's expected `#### Video TL;DR` format if used.
- [ ] Existing uploaded video block should be preserved or intentionally replaced.
- [ ] External publication, archive sync, and distribution side effects have approval.

## Link And Archive Readiness

- [ ] Internal repo links point at current canonical package paths.
- [ ] Public links are Substack-first for already published posts.
- [ ] Archive sync path is known for after publication.
- [ ] Any known repo-link migration follow-up is recorded.

## Final Commands

Record commands run and result.

```bash
# examples
git diff --name-status -- publications/<package>/
rg -n '!\\[[^]]*\\]\\(' publications/<package>/<draft>.md
npm run check:workflow-yaml
npm run check:workflow-model
```

## Required Fixes

- 

## Approval Boundary

External side effects approved?

- [ ] No external side effect requested.
- [ ] Draft sync approved.
- [ ] Live publish approved.
- [ ] Archive sync approved.
- [ ] Distribution posting approved.
