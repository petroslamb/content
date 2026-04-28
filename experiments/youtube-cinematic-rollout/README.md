# YouTube Cinematic Rollout

Evergreen state for the daily cinematic rollout lane.

Canonical process lives in [`../../workflows/youtube-cinematic-rollout/README.md`](../../workflows/youtube-cinematic-rollout/README.md). This folder keeps shared queue, release, and remaster state that coordinates multiple publication packages.

## State Files

- `backlog_manifest.yaml`: active cross-package cinematic backlog and scheduling state
- `release_ledger.md`: daily release and follow-through ledger
- `overlay_remaster_backfill_pilot.json`: overlay remaster backfill crosswalk
- `related_video_studio_fix_2026-04-28.json`: local Studio related-video fix/readback state when present

## Boundary

This folder can contain active worktree state. Do not rewrite or normalize these files just to make the repo look tidy. Update them through the rollout workflow or the relevant YouTube scripts, then verify live channel state when publishing or scheduling matters.
