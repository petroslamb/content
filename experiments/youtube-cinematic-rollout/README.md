# YouTube Cinematic Rollout

Public orientation for the daily cinematic rollout lane.

Canonical process lives in [`../../workflows/youtube-cinematic-rollout/README.md`](../../workflows/youtube-cinematic-rollout/README.md). Active queue, release, remaster, upload, readback, and Studio verification state is private operational material and lives under `CONTENT_PRIVATE_DIR/youtube/`, defaulting to `.private/youtube/`.

## State Files

- `.private/youtube/cinematic-rollout/backlog_manifest.yaml`: active cross-package cinematic backlog and scheduling state
- `.private/youtube/cinematic-rollout/release_ledger.md`: daily release and follow-through ledger
- `.private/youtube/`: generated upload reports, candidate reports, Shorts manifests, remaster crosswalks, and Studio readbacks

## Boundary

Do not move private rollout state back into the public repository. Update operational state through the rollout workflow or the relevant YouTube scripts, then verify live channel state when publishing or scheduling matters.
