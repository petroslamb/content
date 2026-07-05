# Experiments

This directory holds cross-package experiment state that is too operational for `publications/` and too run-specific for `workflows/`.

Use this layer for manifests, ledgers, metric rules, and temporary state that coordinate several packages or channels. Durable process belongs in [`../workflows/`](../workflows/README.md). Package-local outputs belong in the relevant package. Execution evidence belongs in [`../reviewable-runs/`](../reviewable-runs/README.md).

## Current Experiment Map

| Experiment | Owner Workflow | State Files | Posture |
| :--- | :--- | :--- | :--- |
| [`youtube-cinematic-pilot/`](youtube-cinematic-pilot/README.md) | [`../workflows/youtube-cinematic-pilot/README.md`](../workflows/youtube-cinematic-pilot/README.md) | public `copy/`; private `.private/youtube/cinematic-pilot/` state | Bounded pilot orientation and private historical metric surface |
| [`youtube-cinematic-rollout/`](youtube-cinematic-rollout/README.md) | [`../workflows/youtube-cinematic-rollout/README.md`](../workflows/youtube-cinematic-rollout/README.md) | public orientation only; active state in `.private/youtube/` | Evergreen active rollout state |
| [`youtube-reference-comments/`](youtube-reference-comments/README.md) | draft-only experiment, no stable owner workflow yet | `pilot_manifest.yaml`, `drafts/`, `notes.md` | Small-cohort backfill pilot for curated references comments |
| [`youtube-explainer-shorts/`](youtube-explainer-shorts/README.md) | [`../workflows/youtube-channel-ops/README.md`](../workflows/youtube-channel-ops/README.md) | `metrics/` | Historical experiment metric surface |
| [`youtube-insight-authority/`](youtube-insight-authority/SPEC.md) | [`../workflows/youtube-channel-ops/README.md`](../workflows/youtube-channel-ops/README.md) | public spec/rubric only; cohort and readback state in `.private/youtube/` | Active read-only cohort for cinematic authority claims |
| [`youtube-analytics/`](youtube-analytics/README.md) | [`../workflows/youtube-channel-ops/README.md`](../workflows/youtube-channel-ops/README.md) | `decision_rules.yaml`; generated jobs, ledgers, snapshots, and reports in `.private/youtube/` | Active recommendation-only analytics layer |

## Rules

- Keep experiment state indexed here before adding new root scripts or manifests.
- Do not treat experiment manifests as package source authority unless a workflow or package README explicitly names them.
- Keep external channel mutations behind the YouTube workflow approval boundaries.
- Move stable package-specific outputs back into package `artifacts/`, `distribution/`, or `socials/` folders when an experiment becomes normal publication work.
