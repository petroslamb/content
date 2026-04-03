# Essay Iteration

This is the canonical tracked workflow for taking an essay from live draft to review, rewrite, and archive.

## Core Model

The repo standard is:

- one stable **live draft** path
- supporting review artifacts beside it when useful
- older versions and superseded support files moved into local `archive/`

The default is not “versioned files forever” and not “rewrite in place with no history.”

## Recommended Supporting Files

Use these only when they help:

- `companion.md`
- blueprint or plan file
- claims ledger
- review file
- scoring or rubric file

These are working surfaces, not mandatory ceremony.

## Review Inputs

Before a serious review pass, pull the package context that actually defines the bar:

- package `README.md`
- root [`voice_consistency_guide.md`](../../voice_consistency_guide.md) when the package targets publication prose
- blueprint or plan file if one exists
- companion if the package uses one
- prior live drafts or comparison baselines when the task is version-to-version review

## Evidence-Backed Defaults

- Brutal reviews in this repo are expected to be explicit, scored, and rubric-driven. Casual “looks good” feedback is not enough when a draft is near publication.
- If the user asks for version comparison, keep the rubric stable across versions so the comparison stays apples-to-apples.
- When the package is clearly aiming at public publication, include importance, distinctiveness, or virality as separate axes instead of collapsing everything into one prose-quality score.
- When a draft is already close, prefer surgical fixes that clear the remaining blockers over a broad rewrite that destabilizes the whole piece.
- The stable-live-draft-plus-archive model is the default. The main exception is when a package explicitly manages parallel bundle baselines, in which case versioned siblings can temporarily stay live until one becomes canonical.

## Canonical Iteration Loop

1. maintain one stable live draft path
2. run a brutal review with explicit scoring or rubric criteria when the draft is mature enough
3. use the review to shape the next iteration plan
4. get user approval before a major rewrite pass when the next direction materially changes the essay
5. if the draft is close, apply bounded fixes first; otherwise rewrite the live draft or produce a clearly bounded candidate
6. archive superseded versions, local review files, and retired companions once they are no longer the active surface

## Archive Discipline

What should usually move into local `archive/`:

- older versioned drafts
- superseded companions
- retired local README files
- prior review matrices or scoring passes that no longer define the active direction

Keep the live surface readable. Archive depth should preserve history without overwhelming the default reading path.

## Package Expectations

For single-publication packages, the live surface should usually make it obvious where to find:

- the live essay
- optional companion
- papers
- artifacts
- archive

For umbrella packages, preserve the stronger established package structure. The archive discipline still applies inside the local topic or essay folder.
