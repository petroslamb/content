---
workflow_id: notebooklm_artifacts
workflow_kind: stage
stage_binding: notebooklm_artifacts
stability: canonical
workflow_group: artifacts
runner_mode: guided
default_skill: notebooklm-artifact-bundle
launch_templates: []
required_context:
  - canonical live draft
  - target NotebookLM notebook id or exact title
  - destination artifacts directory
expected_outputs:
  - downloaded artifact bundle in the package artifact surface
  - task or transcript references needed for later polish
done_when:
  - the required NotebookLM artifacts are downloaded into the canonical artifact home
approval_gate: none
---

# NotebookLM Artifacts

This is the canonical tracked workflow for generating and downloading NotebookLM media artifacts during essay development.

## Purpose

Use NotebookLM when an essay is strong enough to justify supporting artifacts such as:

- podcast audio
- slide deck PDF
- video

The normal destination is the package or topic `artifacts/` folder.

The public notebook mapping belongs in the package or leaf `status.yaml` and
stores titles only:

```yaml
config:
  notebooklm_notebook_title: <primary notebook title>
  notebooklm_related_notebooks:
    - title: <related notebook title>
```

Restricted NotebookLM UUIDs and owner URLs live in the private overlay at
`CONTENT_PRIVATE_DIR/notebooklm_registry.yaml`, defaulting to
`.private/notebooklm_registry.yaml`. Do not commit NotebookLM UUIDs or
`https://notebooklm.google.com/notebook/...` owner URLs to the public repo.

For umbrella packages where several posts share one manifest, use `config.notebooklm_posts.<post-slug>` with `primary` and `related` entries. The human-readable corpus index lives at [`../../publications/notebooklm-notebooks.md`](../../publications/notebooklm-notebooks.md).

## Evidence-Backed Defaults

- Reuse the standard prompt bundle and generation settings across comparable notebooks unless the user explicitly wants a different artifact voice.
- Resolve the public notebook title from `status.yaml` first, then resolve the private ID from `CONTENT_PRIVATE_DIR/notebooklm_registry.yaml`; use [`../../publications/notebooklm-notebooks.md`](../../publications/notebooklm-notebooks.md) when orienting manually across the corpus.
- Wait for notebook sources to become ready before generating artifacts.
- Artifact generation is asynchronous. Expect task IDs, poll status, and do not assume audio, slides, or video are immediately done just because smaller artifacts finished first.
- Keep one canonical artifact home. If NotebookLM first writes into an essay-scoped subfolder but the package expects package-level `artifacts/`, consolidate into the expected home and remove duplicates.
- Treat NotebookLM outputs as raw artifacts until the article-polish workflow selects, names, and places them. Do not delete semantically named article images or remove markdown image embeds during artifact generation.
- Moving labels such as `artifacts/latest/` and `artifacts/previous/` are acceptable for raw downloaded bundles, but they are not stable publication targets. Article embeds should point to semantically named assets chosen during polish.
- If NotebookLM auth, browser state, source upload, or transcript export fails with a sandbox or permission error, stop the operation and hand the user the exact command plus expected output path. Do not replace the missing audio, slide deck, video, or transcript with a partial terminal capture.
- Do not commit `.notebooklm/` browser state, storage files, restricted notebook IDs, owner URLs, or other hidden auth state as provenance. Reconstruct notebook provenance from the live CLI and the private registry when needed.

## Canonical Flow

1. resolve the target notebook
2. make sure the sources are ready
3. generate the standard artifact bundle
4. poll the artifact tasks until the required outputs are ready
5. download the artifacts into the essay or topic `artifacts/` folder
6. hand off to [`../article-polish/README.md`](../article-polish/README.md) for:
   - semantic image naming
   - intentional image placement in the live essay
   - podcast transcript round-trip
   - the final “rehumanization” editorial pass

## Artifact Placement

Default placement:

- single-publication package: package-level `artifacts/`
- topic-based umbrella package: topic-level `artifacts/`

If a package already uses a stronger established artifact convention, preserve it. Avoid duplicate artifact trees unless there is a strong reason to keep both.

## Raw Artifact Boundary

Artifact generation ends when the raw bundle is present and inspectable. It does not authorize editorial cleanup.

Keep these surfaces distinct:

| Surface | Owns | Do Not Use For |
| :--- | :--- | :--- |
| raw bundle | downloaded NotebookLM audio, slide PDF, video, extracted page PNGs | deciding which images belong in the essay |
| publishable image set | semantically named images selected for the article | storing every extracted slide by default |
| live draft | image placements and editorial prose | proving artifact generation completed |

The confidence-debt artifact pass exposed the failure mode this boundary prevents: a raw artifact refresh deleted the semantically named `assets/r3-slides/` images and removed the markdown embeds. That may be acceptable only as an explicit editorial decision inside article polish. It is not a normal NotebookLM artifact-generation move.

Before committing an artifact-generation pass, inspect the diff for accidental editorial changes:

```bash
git diff --name-status -- publications/<package>/
git diff -- publications/<package>/<draft>.md | rg '^-!\['
find publications/<package>/artifacts publications/<package>/archive -type f -size 0 2>/dev/null
git status --ignored --short publications/<package>/ | rg 'Library/|__pycache__|\.pyc' || true
.venv/bin/python scripts/check_notebooklm_registry.py
```

If the second command prints removed image embeds, stop and hand off to article polish or ask for review. If the size or ignored-cache checks print anything, inspect before committing; zero-byte media and stray cache trees are almost always failed generation traces, not useful artifacts. Do not hide these changes inside an artifact commit.

The binding-gap package is the clearest repo-local example of this rule:

- NotebookLM outputs were initially produced under an essay-scoped artifact tree
- the canonical home was later restored to package-level [`../../publications/binding-gap/artifacts/`](../../publications/binding-gap/artifacts/)
- duplicate copies were removed because they made later editorial work and publication prep harder

## Transcript Round-Trip Boundary

NotebookLM artifact generation includes the possibility of re-uploading the generated podcast audio as a source and exporting the resulting transcript. That round-trip is still part of the broader process, but the canonical editorial use of that transcript now lives in [`../article-polish/README.md`](../article-polish/README.md), alongside image naming and placement.

Operationally, the recurring successful path has been:

- `source add --type file --mime-type audio/mpeg`
- `source wait`
- `source fulltext -o <transcript.txt>`

Use the CLI output flag for full transcripts. Redirecting terminal output can capture only the preview text plus a message such as `use -o to save full content`, leaving a file that looks like a transcript but contains only the first page.

If transcript recovery is blocked by `Operation not permitted`, browser auth, or inaccessible `.notebooklm` state, hand off the exact command:

```bash
cd /Users/petros/Projects/content
.venv/bin/notebooklm source fulltext -n <NOTEBOOK_ID> <SOURCE_ID> -o publications/<package>/artifacts/<transcript>.txt
wc -c publications/<package>/artifacts/<transcript>.txt
```

Continue only after the output file is present and its size is consistent with the source character count reported by NotebookLM.

## Related Skill Bundles

- [`../skills/notebooklm-artifact-bundle/`](../skills/notebooklm-artifact-bundle/)
- [`../skills/pdf-slides-to-substack-images/`](../skills/pdf-slides-to-substack-images/)
