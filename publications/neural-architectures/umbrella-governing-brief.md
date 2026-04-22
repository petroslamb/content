# Neural Architectures Umbrella Governing Brief

This file is the package-level governing brief for `publications/neural-architectures/`.

It is not a single-essay blueprint. It exists to make the umbrella package routable and to keep stage decisions honest.

## Governing Object

This umbrella governs the **neural-architecture publication line**, not one draft.

The package currently contains three distinct object types:

- the published legacy essay [`Neural Architecture Design as a Compositional Language.md`](<Neural Architecture Design as a Compositional Language.md>)
- the promoted scaffold leaf [`neural-architecture-design-as-a-compositional-32e/`](neural-architecture-design-as-a-compositional-32e/README.md)
- the published *Transformer Attractor* line, whose upstream source material still partly lives in [`../hardware-friction/`](../hardware-friction/README.md)

The shared evidence surface for the line remains [`papers/`](papers/).

## Routing Rule

When work targets a **single runnable essay object**, route to the default leaf package:

- [`neural-architecture-design-as-a-compositional-32e/`](neural-architecture-design-as-a-compositional-32e/README.md)

Use the umbrella package directly only when the task is genuinely umbrella-level:

- shared paper-library maintenance
- package-level publication mapping
- NotebookLM or media routing that belongs to the architecture line rather than one leaf
- published *Transformer Attractor* lineage where the publication home is this umbrella, even if some source material still lives in `hardware-friction`

## Current Lifecycle Interpretation

The umbrella manifest is allowed to retain lifecycle state, but that state should be read narrowly.

- Do not infer that `essay_iteration` or other draft-making work should happen directly in the umbrella unless the task is explicitly umbrella-level.
- Do not use adjacent working files such as `The Next Frontier...` or `Multimodal Reasoning...` as governing surfaces unless they are explicitly promoted.
- Treat the default leaf as the first destination for runnable editorial work unless the task clearly targets the umbrella's shared publication line.

## Guardrails

- Do not overwrite leaf-package drafts or artifacts from the umbrella by default.
- Do not treat upstream `hardware-friction` source files as if they already migrated into this package.
- Do not let shared-paper maintenance silently change the governing object of the default leaf.
- Do not use this brief to justify promotion or publication moves on its own; it is a routing surface, not a publication approval artifact.
