---
workflow_id: release_gate
workflow_kind: module
stability: canonical
workflow_group: release
runner_mode: guided
default_skill: null
launch_templates: []
packet_templates:
  - "workflows/release-gate/templates/release_gate_checklist_template.md"
required_context:
  - canonical live draft
  - latest promotion decision or publication approval note
  - package artifact surface and final media paths
  - current references, links, and Substack target when present
expected_outputs:
  - package-local release gate checklist or decision note
  - explicit release verdict: release ready, minor fixes, or blocked
  - list of required fixes before Substack publishing or external posting
done_when:
  - the package has an explicit publish-readiness verdict and no unresolved release blockers
approval_gate: required_before_live_publish
---

# Release Gate

This is the tracked pre-publication gate between [`../article-polish/README.md`](../article-polish/README.md) and [`../substack-publishing/README.md`](../substack-publishing/README.md).

Use it when an essay appears ready to publish, but before any external mutation such as Substack draft sync, live publication, archive sync, YouTube channel mutation, or distribution posting.

## Purpose

Article polish makes the essay better. Release gate decides whether the package is safe to ship.

The distinction matters because a polished essay can still fail release readiness:

- the wrong file is about to be published
- image paths point at unstable generated artifacts
- a video marker is present but the target draft has no uploaded video block
- a reference was added inline but not added to the endmatter
- a forbidden claim from an evidence ledger reappeared during polish
- a Substack draft target or archive follow-through path is stale

This workflow is deliberately practical. It does not replace editorial judgment. It stops avoidable release errors.

## Where It Sits

Use the release stack like this:

| Layer | Question | Canonical Surface |
| :--- | :--- | :--- |
| article polish | does the essay read and present well? | [`../article-polish/README.md`](../article-polish/README.md) |
| release gate | is this package safe to publish or sync? | this workflow |
| Substack publishing | how is the approved public post created or updated? | [`../substack-publishing/README.md`](../substack-publishing/README.md) |
| archive sync | does the tracked archive mirror the public state? | [`../substack-archive-sync/README.md`](../substack-archive-sync/README.md) |
| distribution | what external follow-through should happen? | [`../distribution/README.md`](../distribution/README.md) |

## When To Use It

Use it when:

- a final or near-final draft is about to be synced to Substack
- media has been regenerated or image paths changed
- a release includes video, slides, transcript-derived edits, or repo companions
- a weaker model handled artifact creation or publication prep
- a high-bar essay has evidence ledgers, warrant ledgers, or forbidden-claim constraints that must survive polish
- the publishing step would mutate an external service

Do not use it when:

- the essay is still in blueprint or candidate iteration
- the issue is ordinary prose quality; stay in article polish
- the package has not identified a publish target
- the task is archive refresh after an already-published post; use archive sync directly

## Canonical Output

Use the template:

- [`templates/release_gate_checklist_template.md`](templates/release_gate_checklist_template.md)

Good package-local names:

```text
release-gate.md
<package-slug>-release-gate.md
publication-readiness-checklist.md
```

The release gate verdict must be one of:

- `release_ready`
- `release_ready_after_minor_fixes`
- `blocked`

## Gate 1: Draft Integrity

Check:

1. the canonical live draft is the file being released
2. no unreviewed candidate draft is being published by accident
3. title, subtitle, opening, and ending match the latest promotion decision
4. no visible internal workflow notes remain in the public essay
5. limits and caveats match the latest approved blueprint, review, or evidence ledger

If the wrong file is being released, stop. Do not patch around it inside Substack.

## Gate 2: Evidence And References

Check:

1. body citations are present where the argument needs them
2. body citations use author-year parentheticals for cited papers rather than raw IDs, bare links, or title-only mentions
3. reference entries are formatted consistently enough for publication
4. cited paper entries use linked h4 headings to the arXiv paper or canonical source where available
5. newly added citations have a visible reason to exist
6. sources doing substantive argumentative work have contribution paragraphs, not only bibliographic entries
7. claims forbidden by an evidence ledger, hinge warrant ledger, or review artifact did not reappear during polish

If the essay contains a serious evidence overclaim, send it back to evidence authorization or blueprint hardening. Do not treat that as release polish.

## Gate 3: Media And Artifacts

Check:

1. every markdown image path resolves locally
2. every kept image has an editorial reason to be there
3. image names are stable and semantic enough for future maintenance
4. generated source assets are not confused with publishable article assets
5. transcript-derived edits came from a complete transcript, not a preview
6. video markers are present only when the publication path supports them

Useful local checks:

```bash
rg -n '!\[[^]]*\]\(' publications/<package>/<draft>.md
git diff --name-status -- publications/<package>/
```

If media extraction or transcript recovery failed because of sandbox permissions, stop that subtask and use the sandbox handoff protocol in [`../README.md`](../README.md). Do not invent or remove assets to make the checklist pass.

## Gate 4: Substack And External Mutation Readiness

Check:

1. the Substack draft or post target is known
2. `config.substack_url` and `config.substack_post_id` are current when the package uses them
3. local video markers match the expected `#### Video TL;DR` pattern when the sync script will preserve or inject a video block
4. external publication, archive sync, channel mutation, or distribution posting has explicit approval

This gate should fail closed. A release-ready local markdown file is not the same thing as approval to mutate Substack or another external service.

## Gate 5: Link And Archive Readiness

Check:

1. internal repo links point at the current canonical package paths
2. public links are Substack-first for already published posts
3. archive sync path is known for after publication
4. any known repo-link migration follow-up is recorded

The release does not need to run archive sync before publication, but it should know whether archive sync is the next follow-through step.

## Decision Rules

Mark `release_ready` only when:

- all gates pass
- no external mutation approval is missing for the requested action
- remaining notes are informational, not blocking

Mark `release_ready_after_minor_fixes` when:

- the essay is publishable after small mechanical fixes
- fixes are listed explicitly
- no evidence, file-target, or media-path blocker remains

Mark `blocked` when:

- the wrong file is targeted
- a major citation, evidence, image, or video path is unresolved
- a forbidden claim or major review blocker reappeared
- the package lacks the approval needed for an external side effect
- the publish target is unknown or stale

## Interaction With Existing Workflows

If the gate fails:

- evidence problem -> [`../evidence-authorization/README.md`](../evidence-authorization/README.md) or [`../essay-iteration/README.md`](../essay-iteration/README.md)
- prose or references problem -> [`../article-polish/README.md`](../article-polish/README.md)
- media problem -> [`../notebooklm-artifacts/README.md`](../notebooklm-artifacts/README.md), [`../article-polish/README.md`](../article-polish/README.md), or [`../youtube-production/README.md`](../youtube-production/README.md)
- Substack target problem -> [`../substack-publishing/README.md`](../substack-publishing/README.md)
- archive problem -> [`../substack-archive-sync/README.md`](../substack-archive-sync/README.md)

Do not mark the release gate complete by making an external edit directly in Substack and leaving the repo stale. The repo remains the canonical working tree.
