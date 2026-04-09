# Revision 2 Research Blueprint: Neural Architecture Design

This document defines the evidence-backed research model for the neural architecture design package. Its subject is not one named model family and not one metaphor. Its subject is how the design target moved from bespoke model instances toward reusable blocks, trainable paths, parameterized design spaces, scalable recipes, and controlled non-uniformity.

The synthesis in this blueprint is provisional. Every major claim is either licensed by the local paper set or marked as a multi-source inference. Attractive framings that exceed the evidence are treated as risks, not as premises.

## 1. Subject Model

Neural architecture design is treated here as the design of computational constraints that make certain families of models trainable, scalable, and reusable under a given optimization regime. The evidence base supports five recurring objects of design:

- repeated blocks
- identity-preserving paths
- reusable block recipes
- parameterized design spaces
- controlled non-uniformity inside a stable scaffold

The strongest organizing frame in the current evidence base is **from design spaces to emergent phenomenology**, with **path-gradient trainability** as the main mechanistic thread. Three alternative frames remain useful but secondary:

- **Trainability-first design**: captures the residual and loss-landscape story, but underweights the design-space shift.
- **Conditional computation as unifying principle**: sharp for late sparse and gated systems, too narrow for the earlier eras.
- **Path-gradient hypothesis**: strong as mechanism, weaker as a full historical account.

The current evidence does **not** establish architecture as a literal grammar. At most it supports a weaker synthesis label: modern architectures increasingly look like reusable operator regimes and scalable recipes rather than bespoke diagrams.

## 2. Historical Findings

### Era 1: Bespoke Stacks to Repeated Blocks

**Problem**
Early deep learning systems could scale benchmark performance, but the architecture itself still lived in bespoke layer-by-layer judgment about receptive fields, module order, and local hierarchy.

**Change in the object of design**
The field began shifting from the custom stack toward the repeated block as the reusable unit of thought.

**Anchor findings**
- `2012_AlexNet.md`: deep convolutional vision models can win at scale with enough compute and data, but the architecture remains highly specific to the designer's local choices.
- `2014_VGGNet.md`: repeated small convolutions can compete with and simplify more ornate local design, making uniform repetition a serious design advantage before residual methods.
- `2014_Inception.md`: parallel composition keeps handcrafted operator variety alive as a competing answer to the same problem.

**What this era demonstrates**
Uniform repetition became a viable design strategy before the field had a clean answer to deep trainability.

**What this era does not justify**
It does not prove that uniformity alone solves depth, nor that early CNN history already implies a general compositional language.

### Era 2: Residual and Identity Structure Make Depth Trainable

**Problem**
Increasing depth raised training error instead of simply improving representation power. The issue was not just expressivity. It was optimization.

**Change in the object of design**
Depth stopped being treated mainly as a serial hierarchy and became an identity-preserving path structure in which layers refine rather than replace.

**Anchor findings**
- `2015_ResNet.md`: residual formulation eases optimization and turns depth into additive refinement.
- `2016_Identity_Mappings.md`: identity skip paths and pre-activation units materially improve signal propagation and optimization; deviations from identity shortcuts impede training.
- `2016_ResNet_Ensembles.md`: effective training relies heavily on short paths inside the residual network rather than on one monolithic full-depth chain.
- `2018_Loss_Landscapes.md`: skip connections promote flatter, less chaotic optimization regions and help explain why very deep residual systems remain trainable.

**What this era demonstrates**
Residual and identity structure make depth trainable by preserving direct forward and backward routes and by shortening effective paths through the network.

**What this era does not justify**
It does not prove that every successful architecture reduces to a residual ensemble, nor that semantic hierarchy itself is explained by the shallow-path story.

### Era 3: The Reusable Transformer Block and Emergent Internal Stratification

**Problem**
Sequence modeling still relied on architecture-specific bottlenecks such as recurrence and convolution, while the field lacked a block that could scale broadly across tasks.

**Change in the object of design**
The design target moved toward a reusable block recipe whose external interface stayed stable while training differentiated its internal use.

**Anchor findings**
- `2017_Transformers.md`: self-attention plus feed-forward sublayers inside residual structure creates a reusable block that removes sequence-aligned recurrence.
- `2019_GPT-2.md`: repeating the same transformer block at larger scales becomes a viable way to improve capability without redesigning the core architecture each time.
- `2019_BERT_Attention.md`: attention heads specialize in recognizable linguistic behaviors, but the evidence is head-level and partial rather than a complete pipeline theory.
- `2019_BERT_Rediscovers_Pipeline.md`: probing results show a layerwise ordering from lower-level to higher-level linguistic abstractions within BERT.
- `2020_ViT.md`: the transformer block transfers to vision when pretraining scale is high enough, showing that the block is reusable outside language even without convolutional inductive bias.

**What this era demonstrates**
One good block can become a reusable scaling unit, and repeated uniform scaffolds can develop differentiated internal roles after training.

**What this era does not justify**
It does not prove a neat universal NLP pipeline inside transformers, and it does not prove transformers dominate every regime regardless of data scale or inductive bias.

### Era 4: From Architecture Instances to Design Spaces and Scalable Recipes

**Problem**
Manual architecture design did not scale cleanly as the number of design choices increased, and the field needed better ways to reason about model families rather than single winning instances.

**Change in the object of design**
The object of design moved upward from one architecture instance to the search space, the design space, and the compute-aware recipe that governs a whole family of models.

**Anchor findings**
- `2017_NAS.md`: architecture search can be posed as an automated search over compositional choices, but the result remains a fixed discovered instance.
- `2019_DARTS.md`: architecture itself can be relaxed into a differentiable optimization object.
- `2020_RegNet.md`: the design target can be a parameterized population of models governed by simple regularities rather than one hand-tuned network.
- `2020_Scaling_Laws.md`: performance follows predictable scaling regularities, and many architectural shape choices matter less than scale within broad ranges.
- `2022_Chinchilla.md`: compute-optimal recipes require balancing model size and training tokens more carefully than Kaplan-style scaling implied, making recipe quality a first-class design concern.

**What this era demonstrates**
Architecture increasingly means the design of a family, a search space, or a compute-aware recipe rather than only the naming of one network diagram.

**What this era does not justify**
It does not prove that NAS or RegNet became the dominant frontier workflow, and it does not imply that architecture has become irrelevant once scaling enters the story.

### Era 5: Operator Refinement and Controlled Non-Uniformity

**Problem**
Once a stable scaffold exists, progress often depends less on inventing a wholly new backbone and more on improving the operators, control mechanisms, and specialization patterns inside that scaffold.

**Change in the object of design**
The design target becomes a stable repeated scaffold plus selective operator refinement and conditional specialization.

**Anchor findings**
- `2019_RMSNorm.md`: lightweight rescaling can preserve the useful stabilization properties of normalization without requiring full recentering in every setting.
- `2020_GLU_Variants.md`: multiplicative feed-forward variants such as GEGLU and SwiGLU improve transformer blocks under matched parameter and compute budgets.
- `2017_Sparsely_Gated_MoE.md`: sparse gating makes conditional computation operational at large scale and shows that specialization can be reintroduced without dense all-expert computation.
- `2021_Switch_Transformers.md`: simplified top-1 routing makes sparse expert models easier to train and scale, turning MoE from a promising mechanism into a more adoptable large-model recipe.
- `2024_Mixtral.md`: sparse routing remains compatible with a stable transformer scaffold and serves as a late exemplar rather than the origin of the MoE line.

**What this era demonstrates**
Recent innovation often elaborates a stable scaffold through operator refinement and conditional computation rather than through a return to bespoke monolithic architecture.

**What this era does not justify**
It does not prove that gating or RMSNorm are universal doctrines, and it does not prove that surrounding training procedure has already superseded architecture as the main design surface.

## 3. Derived Synthesis

The following findings are the strongest multi-source inferences this evidence base supports.

### 1. Repeated blocks win when scale and reuse dominate

VGG, ResNet, transformers, ViT, and RegNet all point in the same direction: once scale, maintenance cost, and family-level predictability matter, repeated blocks tend to beat bespoke heterogeneity. This is not a claim that uniformity always wins. It is a claim that the repeated block became the default unit of scalable architectural reasoning.

### 2. Residual and identity structure make depth trainable by preserving short effective paths

The ResNet cluster, the identity-mapping refinement, the Veit path analysis, and the loss-landscape work all converge on one mechanism: successful deep architectures preserve direct routes for information and gradient. This is the strongest mechanistic story in the package.

### 3. Uniform scaffolds can produce differentiated internal roles without hand-designed module hierarchy

The transformer/BERT cluster supports a narrower but important conclusion: repeated uniform stacks need not remain functionally uniform after training. The strongest safe formulation is emergent stratification, not a rigid rediscovered pipeline.

### 4. Design increasingly targets spaces, recipes, and reusable operator constraints

DARTS, RegNet, Kaplan, and Chinchilla show that the design problem now includes the search surface and the scaling recipe, not just the named architecture. The model family and its training allocation are part of the object being designed.

### 5. Controlled non-uniformity returns inside a stable scaffold

The later literature does not reverse the uniform-block story. It qualifies it. Routing, gating, and lightweight normalization show how selective non-uniformity can be reintroduced without abandoning the stable scaffold that made large-scale training feasible in the first place. The strongest version of this claim now runs through the Shazeer-to-Switch line, with Mixtral as a recent illustration rather than as the historical anchor.

## 4. Explicit Guardrails

The following moves are not licensed by the current evidence set and should be treated as errors if they reappear downstream.

- Do not treat architecture as a literal grammar or language unless new evidence is added that directly justifies that framing.
- Do not present DARTS or RegNet as the dominant frontier workflow for modern large language models.
- Do not use `2019_BERT_Attention.md` alone to claim a neat pipeline from syntax to semantics across layers.
- Do not use `2020_Scaling_Laws.md` alone for scaling doctrine after `2022_Chinchilla.md` revised the compute-optimal picture.
- Do not present `2025_DR_Tulu.md` as proof that architecture has already been displaced by training scaffolds.
- Do not promote `2019_RMSNorm.md` or `2020_GLU_Variants.md` into universal principles for all successful models.
- Do not use ViT to claim that inductive bias no longer matters in general; its results are explicitly scale-contingent.
- Do not convert the residual-path story into a total explanation of representation quality or semantic organization.
- Do not treat `2024_Mixtral.md` as the origin point of sparse conditional computation; it is a late exemplar in a longer MoE line.

## 5. Claim-to-Evidence Ledger

### Primary anchors

| Source | Result | Licenses | Does not license |
|:---|:---|:---|:---|
| `2012_AlexNet.md` | Bespoke deep CNN wins at ImageNet scale with the right compute and data regime. | Early large-scale success still depended on local architectural judgment. | A general reusable block story. |
| `2014_VGGNet.md` | Repeated small convolutions scale competitively against more ornate alternatives. | Uniform repetition became a serious design strategy before residuals. | A full explanation of trainability or a universal rule of architectural simplicity. |
| `2015_ResNet.md` | Residual addition eases optimization and enables much deeper networks. | Depth can be reframed as additive refinement. | Why identity-preserving detail matters most. |
| `2016_Identity_Mappings.md` | Identity skips and pre-activation materially improve signal propagation and optimization. | The strongest version of the trainability story depends on identity paths, not just residual form in the abstract. | That normalization or skip variants are interchangeable. |
| `2016_ResNet_Ensembles.md` | Residual networks behave like collections of short effective paths during training. | Pathwise trainability and shallow effective depth are central to residual success. | A complete semantic interpretation of deep residual systems. |
| `2017_Transformers.md` | Self-attention plus residual structure yields a highly parallel reusable block. | The transformer block is a reusable scaling unit, not merely an NLP curiosity. | That transformers are automatically universal without further evidence. |
| `2019_GPT-2.md` | Scaling a repeated transformer block yields broader zero-shot behavior. | Capability can increase through repeated use of a stable block rather than core redesign. | Compute-optimal scaling doctrine. |
| `2019_BERT_Attention.md` | Attention heads display partial syntactic and coreference-related specializations. | Functional specialization can emerge inside repeated transformer stacks. | A clean layerwise pipeline or a full theory of internal hierarchy. |
| `2019_BERT_Rediscovers_Pipeline.md` | Probing reveals ordered layerwise stratification across linguistic tasks. | Some pretrained transformers exhibit stage-like representational ordering. | That every transformer or every task follows the same pipeline. |
| `2020_ViT.md` | A pure transformer can work for vision at large pretraining scale. | The transformer block transfers beyond language under the right data regime. | That vision inductive biases no longer matter in smaller-scale or all-data regimes. |
| `2017_NAS.md` | Architecture search can be automated over a space of compositional choices. | Search spaces are legitimate objects of architectural design. | That searched architectures are themselves simple or generalizable principles. |
| `2019_DARTS.md` | Architecture choice can be relaxed into a differentiable optimization problem. | Architecture can be treated as an optimization object. | That this became the dominant design path for frontier systems. |
| `2020_RegNet.md` | Network design spaces can be simplified into regular, interpretable families. | The design target can be the family rather than the instance. | That one vision design-space result governs all modern architecture work. |
| `2018_Loss_Landscapes.md` | Skip connections correlate with flatter, less chaotic optimization regions. | Architectural form affects optimization geometry. | A complete theory of generalization or a universal geometry law. |
| `2020_Scaling_Laws.md` | Performance follows strong power-law regularities under scale. | Scaling behavior is a first-class design filter. | The final compute-optimal model/data recipe. |
| `2022_Chinchilla.md` | Compute-optimal training requires much more data than Kaplan-style practice implied. | Recipe quality includes model/data balance, not just model size. | That architecture shape is irrelevant once scaling is optimized. |
| `2019_RMSNorm.md` | Rescaling-only normalization can match LayerNorm in some settings with efficiency gains. | Lightweight normalization can be part of an efficient stable block recipe. | That full recentering is never needed or that RMSNorm is universally best. |
| `2020_GLU_Variants.md` | Gated FFN variants improve transformer quality under matched budgets. | Multiplicative control operators matter inside the transformer block. | A universal theory of gating across all architectures. |
| `2017_Sparsely_Gated_MoE.md` | Sparse gating makes extremely large conditional-computation models practical and introduces the load-balancing machinery that makes MoE usable. | The modern sparse-specialization line has a real pre-transformer historical anchor. | That sparse MoE immediately became the dominant default architecture across the field. |
| `2021_Switch_Transformers.md` | Top-1 expert routing simplifies sparse MoE training and makes very large sparse transformers much easier to scale. | Controlled non-uniformity can be made operational inside a stable large-model recipe. | That sparse routing is automatically the best choice in every scale regime or workload. |
| `2024_Mixtral.md` | Sparse expert routing improves capability-efficiency tradeoffs inside a transformer scaffold. | The MoE line remains live in recent frontier-adjacent practice. | The origin of sparse routing or a claim that sparse routing is always superior. |

### Secondary and demoted sources

| Source | Safe role | Why it is demoted |
|:---|:---|:---|
| `2018_BERT.md` | General BERT background and pretraining context. | The stronger layerwise hierarchy claims come from the later probing papers, not from the base model paper itself. |
| `2019_Lottery_Ticket.md` | Optional support for the idea that large networks contain trainable substructures. | It does not directly explain the historical shift in architecture design and can easily be overstretched into a generic scaffold theory. |
| `2021_Transformer_Circuits.md` | Optional evidence that reusable primitives can compose into interpretable behaviors. | It studies simplified attention-only models and does not directly license the package's larger historical claims. |
| `2023_MoE.md` and `2023_MoE_Instruction.md` | Adjacent context for sparse specialization. | The stronger historical line now runs through `2017_Sparsely_Gated_MoE.md` and `2021_Switch_Transformers.md`; these 2023 papers are no longer load-bearing. |
| `2023_Mamba.md` | Alternative primitive example. | It is useful only if the blueprint later broadens toward alternative sequence mixers. The current frame does not require it. |
| `2025_DR_Tulu.md` | Horizon evidence for outward pressure on training procedure. | It is not a historical anchor for neural architecture design and should not carry the late-era conclusion. |

## 6. Conditional Evidence Triggers

The following papers are not currently required because the present claim set has been narrowed. They become mandatory only if the blueprint broadens again.

- **Highway Networks or equivalent early trainability paper**: required if the trainability story is generalized beyond residual and identity structure.
- **BatchNorm and original LayerNorm**: required if normalization is treated as a historically central line rather than a local refinement inside modern blocks.
- **GShard or equivalent distributed sparse-model paper**: required if the MoE line is reframed around infrastructure and sharding rather than architectural simplification and adoptability.
- **NAS survey or explicit architecture-grammar paper**: required if the blueprint reintroduces strong “language,” “grammar,” or “cell syntax” claims.
- **RL or training-scaffold paper cluster**: required if the blueprint again tries to claim that surrounding procedure has become the main post-architecture locus of progress.
