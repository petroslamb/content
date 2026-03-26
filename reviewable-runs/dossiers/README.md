# Reviewable Run Dossiers

This folder is the package's primary concrete proof layer.

Status note:

- the dossiers in this folder are currently labeled `synthetic teaching dossier`
- real proof artifacts live under `../proofs/`
- status labels are defined in `../DOSSIER_STATUS.md`

The upstream abstract architectures still live in `../../autonomous-agent-blueprint/implementation/use-cases/`. The dossiers here show what those defaults look like when one concrete run is made reviewable from end to end.

These dossiers align most directly to `../reviewable-runs.md`. They are not meant to be a strict mechanical output of `../templates/` or `../evaluation/`.

That means two things:

1. the runtime and governance files here correspond clearly to the six review questions
2. the supporting templates and evaluation docs remain looser implementation and review aids rather than a one-to-one dossier schema

## How To Use This Folder

Read in this order:

1. the matching abstract use case in `../../autonomous-agent-blueprint/implementation/use-cases/`
2. `../reviewable-runs.md`
3. the matching dossier in this folder
4. the supporting `runtime-records/` only if you want to inspect how the run is grounded
5. the supporting `governance-records/` only if you want to inspect approval or failure handling
6. `../evaluation/run-review-checklist.md`
7. `../evaluation/failure-mode-catalog.md`

If you are trying to understand how the package is organized, the practical rule is simple:

- `../../autonomous-agent-blueprint/implementation/use-cases/` tells you what the system should be
- `../reviewable-runs.md` tells you what a serious run should surface
- this folder shows one run shaped into that review surface
- `../evaluation/` and `../templates/` support implementation and review, but do not define the dossier format by themselves

## Canonical Dossiers

- `enterprise-policy-memo/README.md`
- `coding-bugfix-agent/README.md`
- `web-form-agent/README.md`

## Historical Reference

The original packet-oriented worked-example layer is preserved under `../history/artifact-bundles-v1/README.md`. It is archival only and is no longer part of the default reading path.
