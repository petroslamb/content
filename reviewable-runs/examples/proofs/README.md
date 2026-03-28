# Proofs

This folder contains the package's strongest evidence layer.

Unlike the canonical dossiers, these artifacts are meant to prove that reviewable runs can improve real review quality rather than merely teach the framework shape.

## Proof Types

- `real-run-index.md`: the registry of real Codex traces considered by the framework
- `march-07-origin-refactor/`: the original dossier-first refactor that introduced reviewable runs as the active model
- `march-12-alphaxiv-auth-refactor/`: an external coding-package run that moved `alphaxiv-py` to API-key-first auth and landed as pushed commit `24bdff1`
- `march-27-manual-mirror-import/`: a publish-style fallback run that manually imported seven posts into the mirror and verified the deployed Pages state
- `march-27-youtube-playlist-order-fix/`: an external-action run that corrected live YouTube playlist state through a mixed Studio-and-API path
- `march-26-standalone-extraction/`: the committed extraction run that decoupled the framework from the blueprint package
- `march-26-compact-public-package/`: the committed package/usability refactor that produced the current compact public shape
- `coding-real-run/`: a smaller real captured coding run reconstructed into the six-record surface
- `failure-contrast/`: a negative contrast showing what ordinary logs fail to make reviewable

## How To Use This Folder

Read in this order:

1. `../../README.md`
2. `real-run-index.md`
3. `march-27-manual-mirror-import/README.md`
4. `march-27-youtube-playlist-order-fix/README.md`
5. `march-12-alphaxiv-auth-refactor/README.md`
6. `march-26-compact-public-package/README.md`
7. `march-26-standalone-extraction/README.md`
8. `march-07-origin-refactor/README.md`
9. `../../PLAYBOOK.md`
10. `coding-real-run/README.md`
11. `failure-contrast/README.md`

This folder should stay small. Add proof artifacts only when they materially strengthen the framework's operational case.

Real-trace proofs in this folder rely on both:

- the six canonical review records
- the optional raw-artifact support layer used to preserve source manifests, excerpts, changed-surface summaries, verification outputs, and boundary records

If you want the current proof set interpreted and critiqued, use `../../investigation/README.md`.

If you want the real proof set compared systematically across run class, boundary type, verification mode, and packet weight, use `../../calibration/REAL_RUN_MATRIX.md`.
