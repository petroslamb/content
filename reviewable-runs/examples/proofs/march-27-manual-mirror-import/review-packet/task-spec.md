# Task Spec

## Run Type

Manual mirror-import fallback for a publication archive.

## Objective

Import seven `Operating Agents` posts and their slide assets into the tracked Substack mirror so the GitHub Pages mirror can publish them even while automated sync remains blocked by Substack `403` responses on GitHub Actions.

## Run Boundary

- Start: user request to manually import the seven `v7-with-slides` essay files and copy the relative image assets
- Stop: imported posts are deployed and verified live on GitHub Pages

## Success Criteria

- archive snapshots exist for all seven posts
- image assets are copied into the tracked archive
- `metadata.json` registers the imported posts
- local mirror validation passes
- deploy succeeds and the mirrored posts resolve publicly
