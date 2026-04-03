# NotebookLM Artifacts

This is the canonical tracked workflow for generating and using NotebookLM media artifacts during essay development.

## Purpose

Use NotebookLM when an essay is strong enough to justify supporting artifacts such as:

- podcast audio
- slide deck PDF
- video

The normal destination is the package or topic `artifacts/` folder.

## Evidence-Backed Defaults

- Reuse the standard prompt bundle and generation settings across comparable notebooks unless the user explicitly wants a different artifact voice.
- Wait for notebook sources to become ready before generating artifacts.
- Artifact generation is asynchronous. Expect task IDs, poll status, and do not assume audio, slides, or video are immediately done just because flashcards or quiz finished first.
- Keep one canonical artifact home. If NotebookLM first writes into an essay-scoped subfolder but the package expects package-level `artifacts/`, consolidate into the expected home and remove duplicates.

## Canonical Flow

1. resolve the target notebook
2. make sure the sources are ready
3. generate the standard artifact bundle
4. poll the artifact tasks until the required outputs are ready
5. download the artifacts into the essay or topic `artifacts/` folder
6. extract slide images from the generated PDF
7. place the slide images into the essay where they actually help the text
8. optionally upload the generated podcast audio back into NotebookLM as a source and recover the transcript

## Artifact Placement

Default placement:

- single-publication package: package-level `artifacts/`
- topic-based umbrella package: topic-level `artifacts/`

If a package already uses a stronger established artifact convention, preserve it. Avoid duplicate artifact trees unless there is a strong reason to keep both.

## Slide PDF Extraction

After generating the slide deck PDF, extract slide images using the repo’s slide-export workflow or the local PDF slide-export skill.

The canonical next step is:

1. review the images
2. name them sensibly if the package uses named assets
3. place them into the essay markdown where they serve the text rather than decorate it

## Podcast Transcript Round-Trip

When the generated audio feels useful as a teaching surface:

1. upload the MP3 back into the notebook as a source
2. wait for it to become ready
3. export the transcript from the source, not from an audio artifact
4. place that transcript near the audio artifacts

Operationally, the recurring successful path has been:

- `source add --type file --mime-type audio/mpeg`
- `source wait`
- `source fulltext`

This transcript often helps make a precise but dry essay more lively, educational, and reader-friendly.

## Related Skill Bundles

- [`../skills/notebooklm-artifact-bundle/`](../skills/notebooklm-artifact-bundle/)
- [`../skills/pdf-slides-to-substack-images/`](../skills/pdf-slides-to-substack-images/)
