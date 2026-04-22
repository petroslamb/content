# YouTube Cinematic Pilot Notes

## Purpose

This workspace coordinates the shared cinematic-video experiment lane. It does not own generated media. Package artifact folders remain the canonical home for cinematic MP4s, caption files, Shorts manifests, portrait renders, and upload reports.

## Current Decisions

- Pilot set:
  - `neural_architecture`
  - `illusion_of_swarm`
  - `autonomy_tax`
- Shared cinematic playlist title: `Rooted Layers Cinematic Briefs`
- Shared Shorts playlist ID: `PL8lPx5mgRhhbMQQ70d-C4dAKKKPzCd5Hd`
- Metric checkpoints:
  - `+24h`
  - `+72h`
  - `+7d`

## Pending Operator Work

- Generate and download the three cinematic MP4s into the package-local artifact paths named in `pilot_manifest.yaml`.
- Make `The Autonomy Tax` baseline longform `1laAYOsrTLg` public before the pilot starts.
- After each cinematic upload, recover the SRT before locking the final Shorts clips.
- For `illusion_of_swarm` and `autonomy_tax`, create the package-local `artifacts/video/shorts/shorts_manifest.json` only after clip boundaries are confirmed.

## Keep Rules

- At least 2 of 3 cinematic uploads must beat their benchmarks by day 7.
- At least 3 of 6 pilot Shorts must exceed `100` views by day 7.
- If neither condition lands, stop the cinematic lane after this pilot.
