---
workflow_id: essay_iteration
runner_mode: guided
default_skill: null
launch_templates: []
required_context:
  - canonical live draft
  - package README or leaf README
  - blueprint, companion, or review artifacts when present
expected_outputs:
  - updated live draft or bounded rewrite candidate
  - review artifact or rubric pass when the revision is substantive
done_when:
  - the live draft is ready for the next lifecycle stage and any active review artifacts reflect the current direction
approval_gate: required_for_major_rewrite
---

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
- package evidence surface when the rewrite is evidence-sensitive and the blueprint makes source-backed claims

## Evidence-Backed Defaults

- Brutal reviews in this repo are expected to be explicit, scored, and rubric-driven. Casual “looks good” feedback is not enough when a draft is near publication.
- If the user asks for version comparison, keep the rubric stable across versions so the comparison stays apples-to-apples.
- When the package is clearly aiming at public publication, include importance, distinctiveness, or virality as separate axes instead of collapsing everything into one prose-quality score.
- When a draft is already close, prefer surgical fixes that clear the remaining blockers over a broad rewrite that destabilizes the whole piece.
- The stable-live-draft-plus-archive model is the default. The main exception is when a package explicitly manages parallel bundle baselines, in which case versioned siblings can temporarily stay live until one becomes canonical.
- For refinement passes on an existing essay, harden the blueprint before a major rewrite when the blueprint is derived from the draft and still contains fuzzy claims, unresolved citation drift, or under-specified revision goals.
- When a major rewrite is needed, prefer a clearly named bounded candidate such as `-v2.md` or `-revision-2.md` before promoting it into the stable live path. Do not overwrite the live draft first and decide later what changed.
- If the blueprint already exists, use it as the preparation surface instead of creating a separate memo by default. Add a new memo only when the blueprint cannot absorb the needed evidence validation cleanly.

## Canonical Iteration Loop

1. maintain one stable live draft path
2. run a brutal review with explicit scoring or rubric criteria when the draft is mature enough
3. if the package already has a blueprint or plan, harden it before a major rewrite when the next direction is still fuzzy or under-evidenced
4. use the review and any hardened blueprint to shape the next iteration plan
5. get user approval before a major rewrite pass when the next direction materially changes the essay
6. if the draft is close, apply bounded fixes first; otherwise produce a clearly bounded candidate and compare it against the live draft before promotion
7. archive superseded versions, local review files, and retired companions once they are no longer the active surface

## Refinement Defaults

For a published or older essay under refinement, the recurring strong pattern is:

1. keep the current live draft intact
2. harden the blueprint until it can actually govern the rewrite
3. run targeted validation against the package evidence surface when principle-level claims need pressure-testing
4. write a bounded `v2` candidate beside the live draft
5. compare, choose, and only then promote one draft back into the canonical live path

This is the default refinement loop unless the package has a stronger established editorial process.

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
