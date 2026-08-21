# Rooted Layers Curated Portfolio

This directory is the governed decision layer for the selective Rooted Layers
portfolio. It does not replace the full Substack archive, rewrite published
articles, or authorize a public change by itself.

## Authority And Scope

- Substack remains the canonical historical publication.
- The GitHub Pages mirror is the curated entrance and still exposes the complete
  public archive.
- `portfolio_manifest.yaml` is the only selection and YouTube-action manifest.
- `approval.yaml` is deliberately absent until Petros approves the exact
  manifest SHA-256 shown in `ROOTED_LAYERS_DECISIONS.md`.
- Any byte-level manifest change invalidates an existing approval.
- Existing private and unlisted YouTube videos are inventory-only. They can
  never be made public by this workflow.
- Article rewrites are labels for future consideration only; this phase creates
  no rewrite drafts.

## Evidence Files

- `corpus_snapshot.json`: hashes and counts for the accepted Substack and
  YouTube source snapshots.
- `blind_review_a.yaml` and `blind_review_b.yaml`: independent blind passes over
  every public essay, completed before consulting prior atlas judgments.
- `review_reconciliation.yaml`: disagreements between the blind passes, source
  lineage, and the existing editorial atlas.
- `youtube_triage.json`: deterministic family/format/duplicate triage plus the
  evidence state for manually reviewed candidates.
- `portfolio_manifest.yaml`: proposed homepage, playlist, editorial labels, and
  exact visibility changes.
- `ROOTED_LAYERS_DECISIONS.md`: concise human review surface generated from the
  manifest.
- `applications/`: immutable dry-run/application reports and their separate
  recoverable in-progress journals.

## Commands

Build a source snapshot only after the Substack completeness report and the
authenticated all-channel YouTube ledger are current:

```bash
.venv/bin/python scripts/rooted_layers_portfolio.py snapshot
```

Validate and render the proposed decision surface:

```bash
.venv/bin/python scripts/rooted_layers_portfolio.py validate
.venv/bin/python scripts/rooted_layers_portfolio.py report
.venv/bin/python scripts/rooted_layers_portfolio.py digest
```

This default `preapproval` validation permits `PENDING` proposal entries. The
manifest pins the exact corpus-snapshot bytes and, through that snapshot, the
authenticated ledger bytes, timestamp, channel id, channel title, and uploads
playlist id.

Inspect the YouTube plan without mutating the channel:

```bash
.venv/bin/python scripts/apply_youtube_portfolio.py all
```

External YouTube application is possible only after `approval.yaml` matches the
current manifest digest and the resolved durable `release_readiness` gate binds
the same manifest, approval, snapshot, channel identity, timestamp, and ledger
digest:

```bash
.venv/bin/python scripts/rooted_layers_portfolio.py validate --mode apply-ready --approval publication_strategy_and_archive/portfolio/approval.yaml --release-readiness reviewable-runs/gates/<run-id>-rooted-layers-portfolio-release-readiness.yaml
.venv/bin/python scripts/apply_youtube_portfolio.py all --approval publication_strategy_and_archive/portfolio/approval.yaml --release-readiness reviewable-runs/gates/<run-id>-rooted-layers-portfolio-release-readiness.yaml --apply
```

That operator verifies the authenticated channel, rejects stale before-state,
requires every selected video to remain public and owned by the approved
channel, uses a canary followed by batches of at most 25, reads every mutation
back, and atomically checkpoints a separate in-progress journal before and
after each mutation and after mutation readback. The journal retains complete
playlist/video before-state and rollback data even when a request fails. It
does not delete videos or edit titles and descriptions. A matching playlist
rerun performs zero item updates.

By default the journal is `<report>.in-progress.json`; `--journal` may set an
explicit path. The operator flushes each snapshot and atomically replaces the
journal before it proceeds to another remote request. The final report is still
created exactly once and remains immutable; the retained journal records
whether that final report was written. If a journal exists without a final
report, do not rerun or resume the operator. Reconcile its successful and
`UNKNOWN` operations against live state, then obtain separate authorization for
any rollback. `KeyboardInterrupt` and other catchable failures are finalized as
`STOPPED` when possible. `SIGKILL` cannot be intercepted, so an in-flight
request at the instant of termination remains `UNKNOWN`; completed earlier
requests have already been checkpointed before the next request begins.

## Approval Gate

One approval must cover the same exact manifest for:

1. the mirror homepage change;
2. the publication-level link on the professional site;
3. the selected YouTube playlist;
4. every named `public → unlisted` transition.

Until that approval exists, all public rollout steps remain blocked even when
local builds and dry-runs pass.

The sidecar schema is `schema_version: 1`, `status: APPROVED`, the exact
`manifest_sha256`, `approved_at`, and `approved_by`. The gate is a standard
resolved `review_gate` for `gate_contract: release_readiness` with an approved
external-mutation decision and the `portfolio_authorization` mapping documented
in the canonical workflow README.
