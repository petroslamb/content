# YouTube Analytics

Recommendation-only analytics state for YouTube follow-through decisions.

The operational channel workflow lives in [`../../workflows/youtube-channel-ops/README.md`](../../workflows/youtube-channel-ops/README.md). The scripts are documented in [`../../scripts/README.md`](../../scripts/README.md).

## State Files

- `decision_rules.yaml`: local classification rules for recommendation reports
- `metrics_ledger.json`: generated read-only metrics ledger when analytics fetches run
- `weekly_reports/`: generated recommendation reports

## Boundary

This layer should recommend actions, not mutate the channel. Uploads, playlist edits, related-video fixes, and privacy/scheduling changes still require the YouTube workflow approval boundaries and live API or Studio readback where relevant.
