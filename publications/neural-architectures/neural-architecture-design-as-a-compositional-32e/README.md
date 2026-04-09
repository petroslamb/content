# Neural Architecture Design as a Reusable Scaffold

Leaf publication package for the legacy slug-based workflow surface behind the published Rooted Layers essay, now governed by the promoted live scaffold essay *Neural Architecture Design as a Reusable Scaffold*.

## Package Role

- Archetype: Leaf package inside the [`../README.md`](../README.md) umbrella
- Status: Published post plus completed leaf-first refinement pass
- Canonical live draft: [`neural-architecture-design-as-a-compositional-32e.md`](neural-architecture-design-as-a-compositional-32e.md)
- Active essay frame: *Neural Architecture Design as a Reusable Scaffold*
- Canonical workflows: [`../../../workflows/paper-intake/README.md`](../../../workflows/paper-intake/README.md), [`../../../workflows/alphaxiv-research/README.md`](../../../workflows/alphaxiv-research/README.md), [`../../../workflows/essay-iteration/README.md`](../../../workflows/essay-iteration/README.md), [`../../../workflows/notebooklm-artifacts/README.md`](../../../workflows/notebooklm-artifacts/README.md), [`../../../workflows/article-polish/README.md`](../../../workflows/article-polish/README.md), [`../../../workflows/substack-publishing/README.md`](../../../workflows/substack-publishing/README.md), [`../../../workflows/youtube-production/README.md`](../../../workflows/youtube-production/README.md), [`../../../workflows/youtube-channel-ops/README.md`](../../../workflows/youtube-channel-ops/README.md), [`../../../workflows/distribution/README.md`](../../../workflows/distribution/README.md)

## Evidence And Neighbor Surfaces

- Local blueprint: [`blueprint.md`](blueprint.md)
- Archive of superseded drafts and live predecessors: [`archive/`](archive/)
- Shared evidence library: [`../papers/`](../papers/)
- Shared paper index: [`../papers/index.md`](../papers/index.md)
- Published legacy reading surface kept at the umbrella root: [`../Neural Architecture Design as a Compositional Language.md`](<../Neural Architecture Design as a Compositional Language.md>)

This leaf package keeps its runnable blueprint local while reusing the umbrella paper library rather than maintaining a duplicate evidence tree. The manifest points to the shared papers through `config.evidence_path`.

## Completed Pass Coverage

The completed neural-architecture refinement pass on this leaf package covered more than the minimal article lifecycle:

- shared paper intake and validation against [`../papers/`](../papers/)
- blueprint hardening and live-draft replacement under this leaf package
- NotebookLM artifact generation into local `artifacts/`
- article polish with semantically named slide assets and transcript round-trip
- local long-form video production under `artifacts/video/`
- manifest-driven Shorts derivation under `artifacts/video/shorts/`
- Substack draft-sync preparation for the existing post target

That matters because the package now carries both the publication draft and the working artifact stack that the completed pass actually used.

The remaining outward-facing stages are still separate on purpose:

- `substack_publishing` is for the actual draft-sync or publish action
- `archive_sync` is for the public archive refresh after a live change
- `distribution` is for downstream channel follow-through after publication

Those should only be marked done when the external work actually happens.

## Local Working Surfaces

- `status.yaml`: leaf lifecycle manifest for the runner
- `artifacts/`: local assets tied specifically to this slug package
- `archive/`: prior snapshots or staged rewrite history for this leaf package
- Canonical local video artifact: [`artifacts/video/neural-architecture-design-as-a-compositional-32e_slides_video_final.mp4`](artifacts/video/neural-architecture-design-as-a-compositional-32e_slides_video_final.mp4)

## Boundary Map

Use this leaf package as the canonical runnable surface for:

- the local blueprint and live draft
- the local artifact bundle
- the local video and Shorts masters
- the lifecycle manifest in [`status.yaml`](status.yaml)

Do not use this leaf package as the only place to understand the wider workflow:

- shared paper storage stays in the umbrella package under [`../papers/`](../papers/)
- routine lifecycle guidance stays under [`../../../workflows/README.md`](../../../workflows/README.md)
- channel-side YouTube upload, playlist mutation, and Shorts release live under [`../../../workflows/youtube-channel-ops/README.md`](../../../workflows/youtube-channel-ops/README.md)
- not every downstream channel action is represented as a leaf `status.yaml` stage, even when the rollout produced the local assets needed for it

## Artifact Map

The local artifact surface is now split by function:

- [`artifacts/audio/`](artifacts/audio/) for narration exports and transcript recovery
- [`artifacts/slides/`](artifacts/slides/) for the exported slide deck, semantically named kept visuals, and the raw numbered slide tree
- [`artifacts/video/`](artifacts/video/) for cue sheets, captions, and long-form renders
- [`artifacts/video/shorts/`](artifacts/video/shorts/) for Shorts manifests plus derived landscape and portrait clips
- [`artifacts/flashcards/`](artifacts/flashcards/) and [`artifacts/quiz/`](artifacts/quiz/) for the rest of the NotebookLM bundle

## Working Rule

Read the umbrella README for the broader neural-architecture essay map. Use this leaf package when the task is specifically about running or iterating the `neural-architecture-design-as-a-compositional-32e` publication lifecycle.
