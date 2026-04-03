# NotebookLM Artifacts

This is the canonical tracked workflow for generating and downloading NotebookLM media artifacts during essay development.

## Purpose

Use NotebookLM when an essay is strong enough to justify supporting artifacts such as:

- podcast audio
- slide deck PDF
- video

The normal destination is the package or topic `artifacts/` folder.

## Evidence-Backed Defaults

- Reuse the standard prompt bundle and generation settings across comparable notebooks unless the user explicitly wants a different artifact voice.
- Wait for notebook sources to become ready before generating artifacts.
- Artifact generation is asynchronous. Expect task IDs, poll status, and do not assume audio, slides, or video are immediately done just because smaller artifacts finished first.
- Keep one canonical artifact home. If NotebookLM first writes into an essay-scoped subfolder but the package expects package-level `artifacts/`, consolidate into the expected home and remove duplicates.

## Canonical Flow

1. resolve the target notebook
2. make sure the sources are ready
3. generate the standard artifact bundle
4. poll the artifact tasks until the required outputs are ready
5. download the artifacts into the essay or topic `artifacts/` folder
6. hand off to [`../article-polish/README.md`](../article-polish/README.md) for image extraction, image placement, transcript round-trip, and final editorial use

## Artifact Placement

Default placement:

- single-publication package: package-level `artifacts/`
- topic-based umbrella package: topic-level `artifacts/`

If a package already uses a stronger established artifact convention, preserve it. Avoid duplicate artifact trees unless there is a strong reason to keep both.

## Transcript Round-Trip Boundary

NotebookLM artifact generation includes the possibility of re-uploading the generated podcast audio as a source and exporting the resulting transcript. That round-trip is still part of the broader process, but the canonical editorial use of that transcript now lives in [`../article-polish/README.md`](../article-polish/README.md).

Operationally, the recurring successful path has been:

- `source add --type file --mime-type audio/mpeg`
- `source wait`
- `source fulltext`

## Related Skill Bundles

- [`../skills/notebooklm-artifact-bundle/`](../skills/notebooklm-artifact-bundle/)
- [`../skills/pdf-slides-to-substack-images/`](../skills/pdf-slides-to-substack-images/)
