# Substack Publishing

This is the canonical tracked workflow for taking a finished essay package to Substack.

## Purpose

Use this when an article is ready enough to become a public post and the package already contains:

- the live essay
- its final or near-final references
- any relevant artifact links or media placements

## Canonical Publishing Expectations

When appropriate, the published essay should include:

- a `#### Video TL;DR` heading near the top if a relevant video artifact exists
- a precise reference section at the end
- short orientation text for references when useful
- appendices when they genuinely help
- links back to the upstream repo for companions, datasets, or supporting material that do not fit inside the main essay

If a draft still reads like repo documentation rather than a public essay, simplify the publication surface before publishing. In practice that often means trimming documentation furniture, overly mechanical endings, or long reference machinery that belongs in the repo more than in email or Substack.

## Evidence-Backed Defaults

- Keep already-published links Substack-first when republishing or cross-linking a live series.
- If the post belongs in the tracked public archive, the publishing task is not done until the archive refresh and mirror validation pass.
- If archive sync is blocked and a manual import is required, use the canonical slug and replacement path so the future sync can overwrite cleanly instead of creating duplicate pages.

## Standard Flow

1. confirm the live draft is the canonical publish target
2. confirm references and appendices are publication-ready
3. insert the `Video TL;DR` block if a video artifact exists and the post format supports it
4. publish with `python-substack` or a package-specific publishing helper
5. refresh the tracked public archive if the post is part of the Substack archive system

## Package-Specific Exceptions

- Some series or packages have specialized publishing helpers, such as the Operating Agents Substack sync path.
- Use those only when the task is explicitly about that series. Do not generalize series-specific automation into the generic publishing path.

## Archive Follow-Through

If the published post belongs in the repo’s tracked public archive:

1. refresh the archive
2. validate the mirror
3. confirm the publication maps back to the correct package or umbrella package

## Related Docs

- [`../essay-iteration/README.md`](../essay-iteration/README.md)
- [`../notebooklm-artifacts/README.md`](../notebooklm-artifacts/README.md)
- [`../../publication_strategy_and_archive/README.md`](../../publication_strategy_and_archive/README.md)
