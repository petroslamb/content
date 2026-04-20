# Neural Architectures

Umbrella package for the neural-architecture essay line of the publication. It is the canonical publication home for the published essay *Neural Architecture Design as a Compositional Language*, the promoted scaffold rewrite *Neural Architecture Design as a Reusable Scaffold*, and *The Transformer Attractor*, while also holding adjacent working material on multimodal and component-level architecture trends.

## Package Status

- Archetype: Umbrella package
- Status: Published umbrella
- Publication map: published *Neural Architecture Design as a Compositional Language*, promoted scaffold essay *Neural Architecture Design as a Reusable Scaffold*, and *The Transformer Attractor*
- Canonical workflow docs: [`../../workflows/paper-intake/README.md`](../../workflows/paper-intake/README.md), [`../../workflows/essay-iteration/README.md`](../../workflows/essay-iteration/README.md)

## Orientation

- Published legacy essay surface: [`Neural Architecture Design as a Compositional Language.md`](<Neural Architecture Design as a Compositional Language.md>)
- Runnable leaf package for the promoted scaffold essay: [`neural-architecture-design-as-a-compositional-32e/README.md`](neural-architecture-design-as-a-compositional-32e/README.md)
- Adjacent live working files: [`The Next Frontier in AI PART 1.md`](<The Next Frontier in AI PART 1.md>), [`The Next Frontier in AI PART 2.md`](<The Next Frontier in AI PART 2.md>), [`Multimodal Reasoning with Integrated Transformers.md`](<Multimodal Reasoning with Integrated Transformers.md>)

## Shared Sources And Artifacts

- The shared paper library for this umbrella lives under [`papers/`](papers/), with the tracked index at [`papers/index.md`](papers/index.md).
- The `neural-architecture-design-as-a-compositional-32e` leaf package keeps its own blueprint and run state locally, while reusing that shared paper library through its manifest rather than duplicating it.
- This umbrella package does not keep one umbrella-level `archive/` manifest or run state. Runnable lifecycle state should live in the relevant leaf package.
- The multimodal note’s local media artifacts currently sit beside the essay as [`Multimodal Reasoning with Integrated Transformers.mp3`](<Multimodal Reasoning with Integrated Transformers.mp3>) and [`Multimodal Reasoning with Integrated Transformers.srt`](<Multimodal Reasoning with Integrated Transformers.srt>).
- Some upstream source material for *The Transformer Attractor* still lives in the sibling umbrella package [`../hardware-friction/README.md`](../hardware-friction/README.md).
- NotebookLM notebook mappings live in the umbrella and leaf `status.yaml` files and are indexed in [`../notebooklm-notebooks.md`](../notebooklm-notebooks.md).
