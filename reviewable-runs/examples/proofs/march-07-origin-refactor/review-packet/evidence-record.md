# Runtime Record: Evidence Record

## Key Evidence

- the implementation prompt explicitly required replacing `artifact bundles` with `reviewable runs`
- `git status --short` showed the archive move plus the new dossier layer in the active path
- file listings confirmed the new three-case dossier structure with `runtime-records/` and `governance-records/`
- grep output and the final summary confirmed `reviewable-runs.md` became the live routing surface

## What Actually Mattered

The decisive evidence was not one diff. It was the combination of:

- new dossier folders in the active path
- archive preservation under `archive/case-studies-v1/`
- routing changes in README/evaluation/use-case surfaces
- explicit validation that broken archive-relative links were patched

## What Was Omitted

The raw session contains earlier planning context and a prior submodule commit unrelated to this exact refactor. Those were omitted from the proof packet to keep the run boundary clean.

