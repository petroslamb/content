# Neural Architecture Pilot Review

This note applies the current Reviewable Runs standard to the April 2026 neural-architecture leaf-package pilot around:

- [`publications/neural-architectures/neural-architecture-design-as-a-compositional-32e/neural-architecture-design-as-a-compositional-32e.md`](../../publications/neural-architectures/neural-architecture-design-as-a-compositional-32e/neural-architecture-design-as-a-compositional-32e.md)
- the commit sequence from `441f81c` through `f0510a5`
- the legacy stage packets now parked under [`../logs/legacy-stage-runs/`](../logs/legacy-stage-runs/README.md)

The goal is twofold:

1. recover which bounded runs in the pilot are actually reviewable
2. judge what this pilot says about the robustness and usefulness of the framework itself

## Scope And Method

This pass used:

- commit history and changed-surface inspection for the April 9 rollout sequence
- the retained package state under `publications/neural-architectures/neural-architecture-design-as-a-compositional-32e/`
- direct artifact checks on the long-form video, Shorts outputs, slide exports, manifest, and NotebookLM metadata
- the Reviewable Runs slicing rule from [`../PLAYBOOK.md`](../PLAYBOOK.md): one run = one objective + one stop boundary

Important: the whole modernization effort is not one run. The pilot only becomes reviewable when split into bounded sub-runs.

## What The Pilot Produced

The retained package state makes several outcomes directly checkable:

- NotebookLM bundle present, including:
  - `artifacts/notebooklm_metadata.json`
  - `artifacts/audio/from_bespoke_layers_to_scalable_ai_scaffolds_deep-dive_long.mp3`
  - `artifacts/slides/the_neural_scaffold_detailed.pdf`
  - `artifacts/video/neural_architecture_design_explainer.mp4`
- local long-form slide video present at:
  - `artifacts/video/neural-architecture-design-as-a-compositional-32e_slides_video_final.mp4`
- long-form video probe:
  - codec `h264` + `aac`
  - resolution `1920x1080`
  - duration `1586.4s`
- slide export surface present:
  - `17` numbered slide PNGs under `artifacts/slides/the_neural_scaffold_detailed/`
- caption and cue surface present:
  - `artifacts/video/neural-architecture-design-as-a-compositional-32e_auto_captions.srt`
  - `artifacts/video/neural-architecture-design-as-a-compositional-32e_all_slides_reviewed_cues.json`
- Shorts manifest present with `6` named clips and scheduled publish times
- generated Shorts outputs present:
  - `6` landscape files
  - `8` portrait files

That last point matters because the manifest only specifies `6` clips. Two portrait files remain outside the manifest surface:

- `Designing the World's Sensory System_portrait.mp4`
- `How Skip Connections Save Training_portrait.mp4`

This is a real robustness signal: the output directory contains stale or extra artifacts that the manifest does not govern.

## Recovered Candidate Runs

### 1. `3c73e99` Promote scaffold essay and harden iteration workflow

- Run class: `editorial`
- Boundary type: `commit`
- Verification mode: `local artifact validation`
- Framework fit: `usable with caveats`
- Retention recommendation: `secondary candidate`

Why it works:

- the run has a visible objective: promote the scaffold-framed live essay and preserve the superseded local states
- the stop boundary is clean because the promotion lands as a commit
- the archive surface is explicit: prior live and intermediate versions were preserved under `archive/`

Why it stays soft:

- evidence provenance is still mostly reconstructed from git state rather than captured at run time
- review quality depends on human reading of the old and new drafts; verification is honest but thin

### 2. `a75dd45` Generate scaffold essay NotebookLM artifact bundle

- Run class: `artifact-generation`
- Boundary type: `commit`
- Verification mode: `local artifact validation`
- Framework fit: `strong`
- Retention recommendation: `secondary candidate`

Why it works:

- one objective, one stop boundary
- the artifact family is visible and bounded
- the resulting state is concrete and inspectable after the fact
- `artifacts/notebooklm_metadata.json` anchors the bundle to one titled NotebookLM object created on `2026-04-09T15:23:26`

Why it is not yet flagship proof:

- the preserved evidence is mostly the resulting files rather than a richer raw run trace
- verification is strong enough for an internal artifact run, but lighter than code tests or live external-state checks

### 3. `0fc95de` Produce slide video and harden YouTube workflow

- Run class: `artifact-generation`
- Boundary type: `commit`
- Verification mode: `local artifact validation`
- Framework fit: `strong`
- Retention recommendation: `secondary candidate`, with the best claim to future promotion

Why it works:

- the objective is clean: produce the verified local MP4 and the supporting cue/caption surface
- the package now contains exactly the reviewable evidence this run needs
- local verification can be stated concretely:
  - final MP4 exists
  - final MP4 is `1920x1080`
  - final MP4 duration is `1586.4s`
  - caption and cue files exist
  - `17` slide exports exist

Why it matters for the framework:

- this is the clearest real artifact-generation candidate in the current repo corpus
- it strengthens a category that the framework currently treats as only partially covered

### 4. `2b60cbe` Add manifest-driven Shorts creation pipeline

- Run class: `code-package`
- Boundary type: `commit`
- Verification mode: `mixed`
- Framework fit: `usable with caveats`
- Retention recommendation: `secondary candidate`

Why it works:

- the run defines a reusable control surface rather than only shipping one asset set
- the manifest makes clip boundaries, titles, and publish times explicit

Why it stays softer:

- most decisive behavioral verification appears in the next asset-generation run rather than this commit alone
- the review surface spans code, docs, and one package manifest, which makes the slice slightly broader than ideal

### 5. `f0510a5` Add generated neural architecture Shorts assets

- Run class: `artifact-generation`
- Boundary type: `commit`
- Verification mode: `local artifact validation`
- Framework fit: `usable with caveats`
- Retention recommendation: `secondary candidate`

Why it works:

- the run has a bounded output family
- the manifest-to-output relationship is mostly reconstructable
- at least one checked pair validates the expected format change cleanly:
  - landscape clip `01-why-handcrafted-ai-breaks.mp4` is `1920x1080`, `86s`
  - portrait clip `01-why-handcrafted-ai-breaks_portrait.mp4` is `1080x1920`, `86s`

Why it stays caveated:

- the manifest declares `6` clips, but the portrait folder contains `8` files
- the extra portrait files weaken the governed-output story because the output directory is not fully explained by the retained control surface

## Weak Or Mis-Sliced Surfaces

### The April 7 legacy stage packets are not meaningful proof artifacts

The old runner packets under [`../logs/legacy-stage-runs/`](../logs/legacy-stage-runs/README.md) are useful as operational history, but weak as Reviewable Runs examples.

The main problems are structural:

- they use the umbrella package name `neural-architectures` instead of the later leaf package key
- `paper_intake` and `article_polish` reduce the entire run to `Manual gate approved by user`
- both `research` packets reduce the run to rejection without preserving the governing reason
- `archive_sync` captures real command output, but the run boundary is repo-wide mirror refresh behavior rather than a leaf-package outcome

These packets answer almost none of the six questions well enough for serious review. They are a good negative reminder that stage status is not the same thing as a bounded run.

### The early pilot commits are too broad to review as one run

These commits are important to the rollout, but weak reviewable-run slices:

- `441f81c` Refactor leaf package workflow and add neural architectures v2
- `75b4027` Harden article workflows and neural architecture draft

Both mix package restructuring, workflow changes, and content/evidence movement. They are better treated as broad rollout setup than as first-class reviewable runs.

### `9ea7728` Prepare neural architecture post for Substack sync is too thin by itself

This run has a clean commit boundary, but it stops before any real submit or publish boundary. Without a later external-state action, it is best treated as a support run rather than a retained example.

## What This Pilot Says About The Framework

### Useful

The pilot is a good result for the framework in one important sense:

- even with imperfect instrumentation, Reviewable Runs still helps recover a credible after-the-fact review surface from commit history plus retained artifacts

That means the framework is not only useful when a perfect packet is written during execution. It is also useful as a reconstruction discipline for real rollouts.

The strongest value here came from three ideas:

- slicing the long session into bounded runs
- insisting on the real stop boundary for each run
- matching verification to run type instead of pretending every stage can be checked the same way

### Soft

The pilot also exposes where the implementation support is still weak.

### 1. Generated stage records are too thin

The runner-generated stage packets behave more like status receipts than review surfaces.

They tell us:

- which stage label was touched
- whether the runner marked it done
- a tiny output snippet

They do not tell us well enough:

- the actual bounded objective
- the evidence that mattered
- the verification logic
- the approval rationale
- the real failure mode when a gate is rejected

### 2. Stage labels are a bad proxy for run boundaries

The neural-architecture pilot crossed research, draft iteration, artifact production, article polish, local video, and Shorts work. Those are lifecycle surfaces, not stable run boundaries.

The strongest reviewable units were commit-sliced sub-runs inside those stages, not the stages themselves.

### 3. Artifact-generation needs stronger default verification support

For media-heavy runs, a good review surface should preserve structured facts such as:

- file inventory
- duration
- resolution
- manifest-to-output consistency
- unexplained leftovers

This pilot made that need concrete. The long-form video could be verified quickly. The Shorts output also revealed a governance gap because the manifest and directory contents diverged.

## What This Pilot Adds To The Corpus

This pilot improves the framework evidence base in three ways.

### 1. Better real evidence for artifact-generation runs

The NotebookLM bundle and local slide-video production runs are better real artifact-generation cases than the framework currently emphasizes.

### 2. Better real evidence for end-to-end content rollouts

The pilot shows that Reviewable Runs can help on a content-production chain that is longer and more heterogeneous than a pure code run, as long as the chain is sliced into commit-bounded segments.

### 3. A concrete negative case for autogenerated stage packets

The legacy packets are not just “lighter.” They demonstrate a real failure mode: proof-shaped records that are not actually reviewable enough to support proof-level judgment.

## Recommended Framework Direction

The immediate lessons are practical rather than conceptual.

1. Keep the current framework model. The six questions and slicing rule still worked.
2. Do not treat lifecycle-stage automation as proof generation.
3. For artifact-generation runs, add lightweight structured verification helpers before adding more theory.
4. When reviewing long publication rollouts, prefer commit-sliced candidates over stage-labeled packets.
5. If this pilot is later promoted into the public proof set, reconstruct `0fc95de` first and `a75dd45` second.

## Bottom Line

The neural-architecture pilot is a good stress test for Reviewable Runs.

It shows:

- the framework is useful well beyond code-only runs
- commit history plus retained artifacts can be enough to recover real review surfaces
- autogenerated stage packets are still too thin to serve as proof artifacts
- artifact-generation verification is the next place where implementation support should get sharper

So the verdict is:

- framework concept: reinforced
- framework implementation support: still underpowered for content/media rollouts
- strongest recovered run from this pilot: `0fc95de`
