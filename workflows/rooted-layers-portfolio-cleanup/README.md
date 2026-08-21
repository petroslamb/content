---
workflow_id: rooted_layers_portfolio_cleanup
workflow_kind: module
stability: canonical
workflow_group: portfolio
runner_mode: guided
default_skill: null
launch_templates:
  - ".venv/bin/python scripts/rooted_layers_portfolio.py snapshot"
  - ".venv/bin/python scripts/rooted_layers_portfolio.py validate --manifest publication_strategy_and_archive/portfolio/portfolio_manifest.yaml"
  - ".venv/bin/python scripts/rooted_layers_portfolio.py report --manifest publication_strategy_and_archive/portfolio/portfolio_manifest.yaml"
  - ".venv/bin/python scripts/rooted_layers_portfolio.py digest --manifest publication_strategy_and_archive/portfolio/portfolio_manifest.yaml"
  - ".venv/bin/python scripts/apply_youtube_portfolio.py visibility --manifest publication_strategy_and_archive/portfolio/portfolio_manifest.yaml --report publication_strategy_and_archive/portfolio/dry-runs/youtube-visibility.json"
  - ".venv/bin/python scripts/apply_youtube_portfolio.py playlist --manifest publication_strategy_and_archive/portfolio/portfolio_manifest.yaml --report publication_strategy_and_archive/portfolio/dry-runs/youtube-playlist.json"
validator_commands:
  - ".venv/bin/python scripts/rooted_layers_portfolio.py validate --manifest publication_strategy_and_archive/portfolio/portfolio_manifest.yaml"
  - ".venv/bin/python scripts/rooted_layers_portfolio.py validate --mode apply-ready --manifest publication_strategy_and_archive/portfolio/portfolio_manifest.yaml --approval publication_strategy_and_archive/portfolio/approval.yaml --release-readiness reviewable-runs/gates/{run_id}-rooted-layers-portfolio-release-readiness.yaml"
  - "npm run check:mirror"
  - "npm run check:workflow-yaml"
  - "npm run check:workflow-model"
packet_templates: []
required_context:
  - complete public Substack discovery report and archive snapshot
  - authenticated all-channel YouTube ledger with channel identity and snapshot timestamp
  - two independent blind essay reviews
  - editorial atlas loaded only after blind review completion
  - reconciled source lineage for every proposed flagship
  - versioned portfolio manifest, decision report, and YouTube dry-runs
expected_outputs:
  - source snapshot and completeness report
  - independent blind review A and blind review B
  - review reconciliation and versioned portfolio manifest
  - concise decision report with exact manifest digest
  - mirror and professional-site change plans
  - YouTube visibility and playlist dry-run reports
  - digest-bound approval sidecar before rollout
  - immutable application and live-state reconciliation reports after rollout
done_when:
  - local evidence and decisions validate against the portfolio contract
  - the approved manifest digest still matches every applied public change
  - rollout completes in order with verified readbacks, or stops with an exact partial-state report
approval_gate: required_before_external_mutation
---

# Rooted Layers Portfolio Cleanup

This workflow turns the existing Rooted Layers archive into a selective technical portfolio without rewriting its publication history. It governs source refresh, evidence review, the versioned decision manifest, local website preparation, dry-run YouTube plans, one exact approval, ordered rollout, and final reconciliation.

The workflow is repo-wide. It does not create a second cleanup repository and it does not treat a publication package as the authority for portfolio-wide decisions. All decision artifacts live under [`../../publication_strategy_and_archive/portfolio/`](../../publication_strategy_and_archive/portfolio/).

## Non-Negotiable Boundary

Local, reversible preparation may proceed before approval:

- refresh and validate the public archive
- refresh the read-only YouTube ledger
- review essays and videos
- write evidence, manifests, reports, patches, and dry-runs
- build and test the local mirror

Rollout may not proceed before approval:

- deploy the mirror
- modify or deploy the sibling professional site
- create, update, populate, or feature a YouTube playlist
- change any YouTube video's visibility

Those actions require one `release_readiness` approval bound to the SHA-256 digest of the exact portfolio manifest reviewed by the user. The approval must cover the mirror change set, the professional-site link change, the playlist plan, and the complete YouTube unlisting set.

If one byte of the manifest changes after approval, the approval is invalid. Regenerate the decision report and dry-runs, obtain a new digest-bound approval, and only then resume. Application results belong in immutable reports keyed to the approved digest; never edit the approved manifest in place to record progress.

## Authority And Scope

The sources of truth are:

1. the refreshed public Substack archive and its completeness report
2. the authenticated all-channel YouTube ledger and caption rubric
3. the two blind reviews and their later reconciliation with the editorial atlas
4. `portfolio_manifest.yaml` for proposed public changes
5. `approval.yaml` plus the durable `release_readiness` review decision for authorization
6. immutable application and reconciliation reports for what actually happened

Substack remains the canonical historical publication. This workflow may read and mirror public Substack posts, but it must not change a Substack post, draft, subscriber record, paid item, or account setting.

The sibling repository at `/Users/petros/Projects/peterlamb` is a separately authorized external rollout surface, not an allowed path inside the `content` workflow sandbox and not part of this workflow's evidence store. Before approval, inspect it read-only outside governed execution and prepare an exact change plan under the portfolio directory. After approval, operate it under its own repository authority; only the declared Rooted Layers publication-link copy may be changed, followed by its own build and deployment verification.

## Phase 1: Establish Trustworthy Source Data

Run the archive synchronization first. Discovery must union:

- RSS results
- every page of the public archive API
- every published entry in `post_map.yaml`

The completeness report must identify source success or failure, pagination evidence, union membership, missing snapshots, and whether destructive cleanup was eligible. Any failed or incomplete discovery makes cleanup ineligible. Preserve existing archived files and stop before using the refresh as selection evidence.

Inventory public Substack posts only. Drafts, paid content, subscriber data, and account data are out of scope.

Refresh the authenticated all-channel YouTube ledger through the existing YouTube channel-operations authority, then admit its read-only result into this portfolio workflow with:

- verified channel id and title
- snapshot timestamp
- current visibility
- title and description
- thumbnails and playlists
- available metrics
- caption availability and locally available caption evidence

Private and unlisted videos are inventory-only. They may never be selected for a public visibility transition.

The canonical analytics ledger lives under `experiments/youtube-analytics/`, which is not a normal `content-agent` local-write path. This workflow therefore verifies and consumes that ledger; its refresh runs through the existing channel-operations surface before portfolio context admission rather than weakening the harness path policy.

For every essay that could become a flagship, reconcile the published snapshot, `post_map.yaml`, package `status.yaml`, package README, and working draft. A mismatch may be documented for archive or supporting work, but it blocks flagship selection until resolved.

## Phase 2: Build The Evidence And Decision Layer

Run two genuinely independent blind reviews across all public essays. Reviewers must not see the plan's named candidates, desired narrative, prior rankings, or the editorial atlas before submitting their initial judgments.

Only after both reviews are frozen may the workflow load the editorial atlas. Use it as prior evidence and a disagreement detector, not as a vote that overrides the blind reviews.

YouTube triage begins deterministically across every upload. Group duplicates, derivatives, series, format variants, broken/test artifacts, and likely family representatives before deep review. Deep-review only likely representatives, uncertain cases, and factual-risk candidates. A video needs captions, a transcript, or equivalent source evidence before it can enter selected work.

Do not calculate or rank by an aggregate numerical score. Each decision must cite concrete anchors, rationale, risk, and confidence. The result may contain fewer than four flagships or no flagships.

A flagship requires all of the following:

- clear value for technical evaluators
- a unique contribution inside its content family
- resolved source lineage
- documented personal contribution or an explicit honest-synthesis designation
- no unresolved high-risk factual claim
- sufficient standalone clarity and presentation quality

The versioned manifest keeps independent fields for identifiers, platform state, typed relationships, selection tier, editorial action, target visibility, homepage placement and order, provenance, contribution, factual risk, evidence anchors, rationale, confidence, approval status, and application status.

Normal proposal validation uses `--mode preapproval` (the default), so mutation candidates may remain `PENDING` while the user reviews them. `--mode apply-ready` is the fail-closed rollout validator: every homepage entry, selected-playlist video, and video targeted for unlisting must be `approval_status: APPROVED` and `application_status: NOT_APPLIED`. Application progress remains in immutable reports and never changes the approved manifest.

The manifest also binds its evidence bytes: `source_snapshot_sha256` must match the exact corpus snapshot, while `youtube.source_ledger_sha256`, `youtube.snapshot_timestamp`, `expected_channel_id`, `expected_channel_title`, and `expected_uploads_playlist_id` must match both that snapshot and the exact ledger bytes.

The manifest validator must reject:

- duplicate stable ids
- invalid relationship or action combinations
- more than four flagship or four supporting homepage entries
- selected work without evidence or rationale
- unresolved flagship lineage or contribution
- unresolved high-risk factual claims in a flagship
- unapproved homepage entries
- any YouTube transition other than `public` to `unlisted`
- any attempt to delete, publish, or expose private/unlisted inventory
- an approval whose digest does not match the exact manifest bytes

Editorial rewrite ideas may be labeled `REWRITE_CANDIDATE` or `MERGE_CANDIDATE`, but this workflow does not draft or publish rewrites.

## Phase 3: Prepare The Exact Proposal

Prepare, validate, and locally test:

1. the proposed mirror homepage and navigation
2. the professional-site link and bilingual copy change plan
3. the selected playlist membership, when at least two videos independently clear the bar
4. the exact video-by-video visibility dry-run
5. the concise decision report

The decision report must show:

- the proposed homepage in order
- the proposed selected playlist in order
- every YouTube before-state and requested after-state
- unresolved evidence and explicit blockers
- no more than ten genuine questions
- the SHA-256 digest of the exact manifest

The mirror may be prepared locally before approval. Its homepage has a maximum of four flagship and four supporting pieces, a link to the complete archive, the exact global AI-assistance disclosure, and a primary `Professional profile` CTA. It removes homepage archive statistics, recent additions, and editorial-atlas promotion while preserving the atlas route and every public mirrored essay in the archive.

Substack stays canonical for individual essays. The professional site's publication-level Rooted Layers links point to the curated mirror; direct essay links stay on Substack; the structured Substack profile link remains present; English and Greek copy must agree.

## Phase 4: Record One Exact Approval

Present the full decision report, local website verification, and both YouTube dry-runs together. The approval is all-or-nothing for the exact manifest digest.

Record authorization in both places:

- a durable `release_readiness` review decision under `reviewable-runs/gates/`
- `publication_strategy_and_archive/portfolio/approval.yaml`, containing the approved manifest SHA-256 and approval metadata

Validation of `approval.yaml` is necessary but not sufficient: the durable release gate must also be approved. A missing, rejected, deferred, stale, or digest-mismatched approval stops before the first rollout mutation.

`approval.yaml` has this exact schema:

```yaml
schema_version: 1
status: APPROVED
manifest_sha256: <64 lowercase hex characters for the exact manifest bytes>
approved_at: <ISO-8601 timestamp>
approved_by: <non-empty reviewer identity>
```

The durable gate remains a normal `kind: review_gate`, `schema_version: 1` artifact under `reviewable-runs/gates/`. It must be `status: resolved`, use `gate_contract: release_readiness` and `gate_type: external_mutation`, identify `workflow.workflow_id: rooted_layers_portfolio_cleanup`, contain an `approve` decision with all four contract dimensions required and approved, and add this portfolio-specific binding:

```yaml
portfolio_authorization:
  schema_version: 1
  manifest_path: publication_strategy_and_archive/portfolio/portfolio_manifest.yaml
  manifest_sha256: <exact manifest SHA-256>
  approval_path: publication_strategy_and_archive/portfolio/approval.yaml
  approval_manifest_sha256: <same exact manifest SHA-256>
  source_snapshot_path: publication_strategy_and_archive/portfolio/corpus_snapshot.json
  source_snapshot_sha256: <exact corpus snapshot SHA-256>
  expected_channel_id: <approved channel id>
  expected_channel_title: <approved exact channel title>
  expected_uploads_playlist_id: <approved uploads playlist id>
  snapshot_timestamp: <approved ledger snapshot timestamp>
  source_ledger_sha256: <exact ledger SHA-256>
```

## Phase 5: Roll Out In Fixed Order

Rollout order is mandatory:

1. deploy and verify the curated mirror
2. apply, build, deploy, and verify the sibling professional-site link
3. create or update the selected YouTube playlist, only when at least two videos are approved
4. apply the visibility operator with a canary batch of at most 25
5. continue only when every canary readback matches
6. capture final screenshots and reconcile all live state

The YouTube operator is dry-run by default. Apply mode must:

- verify the authenticated channel against the approved snapshot
- require live status to equal the manifest's expected before-state
- permit only `public` to `unlisted`
- batch no more than 25 videos
- read back every mutation
- preserve each previous state for explicit rollback
- durably checkpoint a separate in-progress journal before and after each
  remote mutation and after mutation readback
- write before/after results to an immutable report
- stop on channel mismatch, state drift, quota failure, or readback mismatch

It must not delete videos, make any video public, or edit titles or descriptions. Uncertainty defaults to `KEEP_PUBLIC`.

## Stop Rules And Partial State

Stop remaining work immediately when:

- source discovery is incomplete or a source fails
- a proposed flagship has unresolved lineage, contribution, or high factual risk
- the manifest fails validation
- approval is missing or its digest drifts
- a website build, deployment, link, accessibility, path-prefix, mobile, light-theme, or dark-theme check fails
- the authenticated YouTube channel differs from the approved snapshot
- a live video or playlist state differs from its approved before-state
- a YouTube mutation, quota request, or readback fails

Do not improvise a different public mutation to recover. Record the exact partial state, preserve successful verified work, and return for review.

The in-progress journal defaults to `<report>.in-progress.json` and may be
placed explicitly with `--journal`. It is an atomic snapshot, flushed to disk
and replaced after each operation checkpoint; it is not the immutable final
report. The final report is created once, and the retained journal records when
that write completed. A journal without a final report is a recovery signal:
do not rerun or resume automatically. Reconcile every `SUCCEEDED` and `UNKNOWN`
operation with live state before deciding on a separately authorized rollback.
Catchable interruption, including `KeyboardInterrupt`, is finalized as
`STOPPED` when possible. `SIGKILL` cannot be intercepted; if it lands during a
remote request, that request remains `UNKNOWN`, while every earlier completed
request was checkpointed before the next request started.

Rollback is explicit, not automatic:

- use git reversion for the two website repositories
- use the recorded YouTube before-state only after a separately authorized rollback decision
- never delete remote artifacts as a rollback shortcut

## Command Surface

Create or refresh the evidence snapshot:

```bash
.venv/bin/python scripts/rooted_layers_portfolio.py snapshot
```

Validate and render the proposal:

```bash
.venv/bin/python scripts/rooted_layers_portfolio.py validate --manifest publication_strategy_and_archive/portfolio/portfolio_manifest.yaml
.venv/bin/python scripts/rooted_layers_portfolio.py report --manifest publication_strategy_and_archive/portfolio/portfolio_manifest.yaml
.venv/bin/python scripts/rooted_layers_portfolio.py digest --manifest publication_strategy_and_archive/portfolio/portfolio_manifest.yaml
```

Generate YouTube dry-runs:

```bash
.venv/bin/python scripts/apply_youtube_portfolio.py visibility --manifest publication_strategy_and_archive/portfolio/portfolio_manifest.yaml --report publication_strategy_and_archive/portfolio/dry-runs/youtube-visibility.json
.venv/bin/python scripts/apply_youtube_portfolio.py playlist --manifest publication_strategy_and_archive/portfolio/portfolio_manifest.yaml --report publication_strategy_and_archive/portfolio/dry-runs/youtube-playlist.json
```

Verify the exact approval before rollout:

```bash
.venv/bin/python scripts/rooted_layers_portfolio.py validate --mode apply-ready --manifest publication_strategy_and_archive/portfolio/portfolio_manifest.yaml --approval publication_strategy_and_archive/portfolio/approval.yaml --release-readiness reviewable-runs/gates/<run-id>-rooted-layers-portfolio-release-readiness.yaml
```

The authenticated apply commands are deliberately absent from the quick launch surface. After `release_readiness` approval, the governed rollout uses:

```bash
.venv/bin/python scripts/apply_youtube_portfolio.py playlist --manifest publication_strategy_and_archive/portfolio/portfolio_manifest.yaml --approval publication_strategy_and_archive/portfolio/approval.yaml --release-readiness reviewable-runs/gates/<run-id>-rooted-layers-portfolio-release-readiness.yaml --report publication_strategy_and_archive/portfolio/applications/youtube-playlist.json --journal publication_strategy_and_archive/portfolio/applications/youtube-playlist.in-progress.json --apply
.venv/bin/python scripts/apply_youtube_portfolio.py visibility --manifest publication_strategy_and_archive/portfolio/portfolio_manifest.yaml --approval publication_strategy_and_archive/portfolio/approval.yaml --release-readiness reviewable-runs/gates/<run-id>-rooted-layers-portfolio-release-readiness.yaml --report publication_strategy_and_archive/portfolio/applications/youtube-visibility.json --journal publication_strategy_and_archive/portfolio/applications/youtube-visibility.in-progress.json --canary-size 25 --apply
```

Run the local validation surface before handoff:

```bash
npm run check:mirror
npm run check:workflow-yaml
npm run check:workflow-model
```

## Acceptance Boundary

Completion requires either a fully reconciled rollout or an exact stopped-state report. A successful rollout proves:

- selected work is reachable from the mirror homepage
- the full public archive remains accessible
- no Substack publication changed
- no video was deleted
- no private or unlisted video became public
- every YouTube mutation matches the approved manifest
- the professional site's primary Rooted Layers link reaches the curated mirror

Passing local tests without the digest-bound approval is preparation, not rollout completion.
