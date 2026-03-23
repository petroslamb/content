# Neural Architecture Design as a Compositional Language

Date: 2025-11-27
URL: https://lambpetros.substack.com/p/neural-architecture-design-as-a-compositional-32e

### Introduction: The Architect’s Secret

It’s a common misconception to think of designing a neural network like writing a piece of traditional software. We imagine architects meticulously programming every logical step, crafting a perfect, intricate machine from the ground up. But the reality of modern AI is far more counter-intuitive and fascinating.

The most successful AI architectures aren’t rigid blueprints; they are flexible scaffolds. An architect’s job is not to design a flawless machine, but to create a rich environment—a framework of possibilities—where an algorithm can learn and discover solutions on its own. This post explores five of the most surprising and impactful ideas that have shaped this new philosophy, revealing how the field shifted from building models to writing the very language of computation.

--------------------------------------------------------------------------------

### 1. Architectures Aren’t Blueprints; They’re Scaffolds

The “Scaffold Hypothesis” is a simple but profound idea: an architect’s primary role is to create a *space of possible computations* where an optimization process like gradient descent can easily find effective solutions.

This stands in stark contrast to traditional programming, where a developer specifies exact instructions like `if x > 5, then do y`. In AI architecture, the goal is different. Take the Transformer model’s famous Query-Key-Value (QKV) attention mechanism. The designers didn’t explicitly program the network to “use Q for asking what information is needed, K for signaling what information is available, and V for providing that information.” Instead, they created a mathematical structure where that function was *easy to learn*. The network discovered this communication protocol on its own through training.

This principle reframes the entire design process. The architecture is no longer the final product but the starting point for discovery.

The architecture is the hypothesis; training is the proof.

This shift explains why simple, repeated structures are so effective. Instead of pre-ordaining a complex function, they provide a flexible, high-dimensional canvas and a simple set of rules, allowing the training process itself to paint the masterpiece.

--------------------------------------------------------------------------------

### 2. Simpler and Deeper Beats Clever and Custom

Early in deep learning’s history, models like AlexNet were built with custom-designed layers, each with a specific, hand-tuned purpose. The field has since learned a powerful lesson: uniformity and simplicity almost always win. The shift began with models like VGGNet and ResNet, which abandoned complex, varied layers in favor of stacking simple, identical blocks over and over again.

This wasn’t just a competition between models; it was a clash of design philosophies. The complex Inception model represented a “clever, parallel committee” approach, where designers offered the model multiple hand-tuned computational paths at once. In contrast, ResNet championed a “brute-force sequential” approach with a single, deep compositional rule. ResNet’s victory proved that a simple, repeatable formula was far more scalable and powerful.

...simpler, more uniform building blocks win over complex, hand-tuned modules.

The power of this principle is staggering. A massive model like GPT-3 is built by repeating the exact same architectural block 96 times. This principle of uniform, repeatable blocks became the bedrock of modern AI. But to truly scale it, researchers had to solve a fundamental problem: how do you make a network hundreds of layers deep without the signal getting lost? The answer came in a single, elegant formula.

--------------------------------------------------------------------------------

### 3. A Single, Simple Formula Unlocked Extreme Depth

A breakthrough paper from 2015 revealed a disarmingly simple formula that would shatter the perceived limits of network depth: the “residual connection.” The formula is just `x_out = x_in + F(x_in)`.

This small addition caused a massive paradigm shift. Before ResNet, architects asked, “What should each layer compute?” After ResNet, the question became, “What *refinement* should each layer add?” By making each layer learn a modification to the input (`F(x_in)`) rather than an entirely new representation, the model’s task became dramatically easier.

This changed the network’s job from replacing information at each layer to *accumulating refinements*. The final output is no longer the result of a complex transformation, but the sum of the original input plus a series of small, learned adjustments: `Output = Input + Block₁(Input) + Block₂(...) + ...`. This is the foundational compositional operator of modern deep learning. This simple change created “gradient highways” that allowed networks to be built with 100+ layers, enabling the extreme depth that powers today’s most capable models.

--------------------------------------------------------------------------------

### 4. Sophisticated Specialization Emerges From Identical Blocks

One of the most stunning validations of the “scaffold hypothesis” came from analyzing models like BERT. BERT is constructed from a stack of identical Transformer blocks; architecturally, layer 2 is the same as layer 10. Yet, after training, these identical layers learn to perform distinct and specialized roles.

Analysis revealed a clear functional hierarchy that emerged on its own:

- **Early layers:** Focus on syntax and surface-level features (e.g., making determiners attend to their nouns).
- **Middle layers:** Learn more abstract semantic relationships and entity recognition.
- **Late layers:** Handle complex, long-range tasks like coreference resolution (e.g., linking the pronoun “it” back to its subject paragraphs earlier).

This specialization was not designed by an architect; it was discovered by the training process as an efficient way to solve the problem. The uniform stack of blocks provided the capacity, and optimization found the structure.

The architecture didn’t specify this hierarchy—training discovered it!

This demonstrates that a well-designed architectural scaffold doesn’t need to encode complex behaviors itself. It only needs to create a space where those behaviors are easy for the model to learn.

--------------------------------------------------------------------------------

### 5. Today’s AI Is Built With Standardized “Lego” Blocks

The modern process of designing a new state-of-the-art AI model has evolved significantly. Instead of inventing novel architectures from scratch, designers now select high-performing components from a shared, validated library—much like building with a set of standardized Lego blocks.

This library includes proven solutions for every part of a model’s core block:

- **Position Encodings:** RoPE (Rotary Position Embeddings)
- **Normalizations:** RMSNorm
- **MLP Variants:** SwiGLU (Swish-Gated Linear Unit)

A model like Llama 3 is a perfect example of this philosophy. It is a stack of 80 identical blocks, where each block is a carefully chosen composition of these best-in-class, off-the-shelf components. This design can be elegantly captured in just a few lines of code:

```
class LlamaBlock:
    attention = GroupedQueryAttention(
        position_encoding=RoPE
    )
    norm1 = RMSNorm()
    mlp = SwiGLU()
    norm2 = RMSNorm()

# Stack 80 identical blocks
model = Stack([LlamaBlock() for _ in range(80)])
```

This modularity allows the entire field to advance more rapidly. Researchers can innovate on a single component and instantly plug it into a wide range of existing models. This shifts the focus from bespoke architecture design to engineering better training methods and scaling up proven formulas with confidence.

--------------------------------------------------------------------------------

### Conclusion: From Building Models to Writing Grammars

The journey from AlexNet to modern LLMs validates a powerful set of principles. We learned that architectures are scaffolds, not blueprints (1); that simple, deep repetition beats clever customization (2); that a single formula could unlock this depth by reframing computation as refinement (3); that specialization emerges from this uniformity rather than needing to be designed (4); and that this entire process has culminated in a modular, ‘Lego-like’ design philosophy that accelerates the entire field (5).

The story of neural architecture design is a journey away from crafting specific models and toward designing compositional languages. The most impactful breakthroughs have consistently been those that provided simpler, more general, and more scalable building blocks. This evolution has validated the core theme: the goal is not to build a machine, but to create a rich scaffold that allows intelligence to emerge.

We’re not building neural networks anymore. We’re building grammars of computation, and training is the process of writing programs in those grammars.

*Read the next post on this series:*

# Deep Dive

A good way to read this long post, is to play the podacast audio, while following the text under it. It outlines a new “grammar” emerged in the last 13 years of deep learning research progress. The post outlines several of the seminal papers and their incremental contributions to the field of AI. So you get a historical flashback as a treat :)

*How the deep learning field evolved from designing specific models to designing languages of reusable components*

---

## Introduction: The Scaffold Hypothesis

A profound shift is occurring in how we think about neural network architecture. Rather than viewing architecture design as “building the perfect model,” researchers increasingly recognize it as **creating computational scaffolds that training discovers how to exploit**.

This is a departure from traditional software engineering. When you write a program, you specify exactly what happens: `if x > 5, then do y`. But when you design a neural architecture, you’re doing something different: you’re creating a *space of possible computations* and letting gradient descent search through that space.

Consider the standard Transformer layer with its Query-Key-Value attention mechanism. The designers didn’t program the network to “use Q for asking what information is needed and K for signaling what information is available.” Instead, they created a mathematical structure where this pattern is *easy to learn*, and gradient descent discovered it. The architecture is the hypothesis; training is the proof.

This blog post traces how this understanding emerged, from early hand-crafted networks to today’s modular, compositional design philosophy. We’ll see how “designing architectures” evolved into “designing languages of components,” and why this shift matters for the future of AI.

---

## Era 1: The Hand-Crafted Hierarchy (2012-2015)

### AlexNet (2012): The Custom Stack

**Paper:** “ImageNet Classification with Deep Convolutional Neural Networks” (Krizhevsky, Sutskever, Hinton, 2012)

**Citation:** <https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks>

**The Architecture:**

```
Conv(11×11) → MaxPool → Conv(5×5) → MaxPool →
Conv(3×3) → Conv(3×3) → Conv(3×3) → MaxPool →
FC(4096) → FC(4096) → FC(1000)
```

**The Mindset:** Each layer was individually designed. The choice of 11×11 convolutions first, then 5×5, then 3×3 wasn’t based on a general principle—it was a specific hypothesis about how visual processing should work. The architecture encoded the designers’ beliefs about hierarchical feature extraction: large receptive fields first (for global structure), then smaller ones (for details).

**Key Contribution:** Proved that deep networks could work at scale. But the architecture itself was a monolithic, task-specific design.

**The Problem:** Every new domain required a new custom architecture. Transfer learning was limited because the architectural choices were entangled with the specific task.

---

### VGGNet (2014): The First Hint of Repetition

**Paper:** “Very Deep Convolutional Networks for Large-Scale Image Recognition” (Simonyan & Zisserman, 2014)

**Citation:** <https://arxiv.org/abs/1409.1556>

**The Insight:** What if we stopped varying everything and just used simple, repeated patterns?

**The Architecture:**

```
[Conv(3×3) → Conv(3×3) → MaxPool] × multiple times
```

**Key Contribution:** Introduced the idea of *architectural uniformity*. Instead of carefully varying kernel sizes (11×11, then 5×5, then 3×3), use the same simple 3×3 convolution throughout. Depth comes from repetition, not from custom hierarchies.

**Why It Mattered:** This was the first move toward *compositional design*. The basic block (two conv layers + pooling) became a reusable module. VGG-16 and VGG-19 differed only in how many times this block was repeated—the first example of “architecture as a parameterized family” rather than “a single design.”

**The Limitation:** Still no theoretical justification for why repetition works, and training very deep VGG networks was difficult (gradient flow issues).

---

## Era 2: The Modular Revolution (2015-2017)

### ResNet (2015): The Block as the Fundamental Unit

**Paper:** “Deep Residual Learning for Image Recognition” (He et al., 2015)

**Citation:** <https://arxiv.org/abs/1512.03385>

**The Breakthrough:** This paper fundamentally changed how we think about architecture design.

**The Residual Block:**

```
x_out = x_in + F(x_in)
```

Where F is typically:

```
Conv(1×1) → BatchNorm → ReLU →
Conv(3×3) → BatchNorm → ReLU →
Conv(1×1) → BatchNorm
```

**The Paradigm Shift:**

Before ResNet, the question was: “What should each layer compute?”

After ResNet, the question became: “What *refinement* should each layer add?”

**Key Contributions:**

1. **Residual connections enable training of 100+ layer networks** by providing gradient highways
2. **Proved uniformity works:** ResNet-50, ResNet-101, ResNet-152 differ only in how many times the same block repeats
3. **The block becomes the design unit:** Instead of designing networks layer-by-layer, design one good block and stack it

**The Compositional Insight:**

ResNet showed that you could view a deep network as:

```
Output = Input + Block₁(Input) + Block₂(...) + ... + Blockₙ(...)
```

Each block makes a “suggestion” for how to modify the representation. The network doesn’t *replace* information at each layer—it *accumulates refinements*. This is fundamentally compositional: the final result is a sum of contributions from independent modules.

**Evidence of Emergent Specialization:**

Later analysis (Veit et al., 2016, “Residual Networks Behave Like Ensembles of Relatively Shallow Networks”) showed that ResNet blocks naturally specialize:

- Early blocks: low-level features (edges, textures)
- Middle blocks: mid-level features (object parts)
- Late blocks: high-level features (complete objects)

This happened without any explicit supervision or architectural variation—the blocks were all identical, but training caused them to specialize!

---

### Inception/GoogLeNet (2014-2016): Exploring Parallel Composition

**Paper:** “Going Deeper with Convolutions” (Szegedy et al., 2014)

**Citation:** <https://arxiv.org/abs/1409.4842>

**The Alternative Composition:** While ResNet did sequential composition (stack blocks), Inception explored *parallel composition*.

**The Inception Module:**

```
Input → ├─ Conv(1×1) ──────────┐
        ├─ Conv(1×1) → Conv(3×3) ─┤
        ├─ Conv(1×1) → Conv(5×5) ─┤
        └─ MaxPool → Conv(1×1) ───┘
                                   ↓
                            [Concatenate]
```

**The Idea:** Instead of choosing one operation (3×3 or 5×5 conv), do *all* of them and let the network learn to weight them appropriately during training.

**Key Contribution:** Demonstrated that architectural choice could be *deferred to training time*. The architecture provides multiple computational paths, and gradient descent learns which to emphasize.

**The Limitation:** Inception modules were complex and had many hyperparameters. Unlike ResNet’s simple, uniform blocks, Inception was harder to reason about and modify.

**Historical Note:** While influential, the field largely converged on ResNet’s simpler compositional pattern. This suggests a principle: *simpler, more uniform building blocks win over complex, hand-tuned modules*.

---

## Era 3: The Compositional Explosion (2017-2019)

### Transformers (2017): A New Universal Block

**Paper:** “Attention Is All You Need” (Vaswani et al., 2017)

**Citation:** <https://arxiv.org/abs/1706.03762>

**The Revolutionary Building Block:**

```
TransformerLayer(x):
  # Sub-block 1: Attention
  x = x + MultiHeadAttention(LayerNorm(x))

  # Sub-block 2: Feed-Forward
  x = x + MLP(LayerNorm(x))

  return x
```

**Why This Mattered:**

1. **Modular sub-components:** The attention mechanism itself is compositional:

```
Q = W_Q × x  (what to search for)
K = W_K × x  (how to be found)
V = W_V × x  (what information to provide)
```

1. Each component (Q, K, V) is a learned projection, and their interaction is a fixed mathematical operation (scaled dot-product attention).
2. **Universal applicability:** Unlike CNNs (spatial bias) or RNNs (sequential bias), the Transformer block worked for:

   - Language (BERT, GPT)
   - Vision (ViT)
   - Audio (Whisper)
   - Multi-modal tasks (CLIP, Flamingo)
3. **Extreme uniformity:** GPT-2 (1.5B parameters) used the *exact same block* 48 times. GPT-3 (175B) used it 96 times. The only scaling dimension was repetition count and hidden size.

**The Compositional Language Emerges:**

The Transformer defined a **vocabulary of components**:

- **Mixing operations:** Attention, MLP
- **Connections:** Residual (+)
- **Normalizations:** LayerNorm
- **Position information:** Sinusoidal embeddings

These could be mixed and matched. Within a few years, researchers were systematically exploring this design space.

---

### BERT (2018): Emergent Specialization at Scale

**Paper:** “BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding” (Devlin et al., 2018)

**Citation:** <https://arxiv.org/abs/1810.04805>

**The Architecture:** Literally just 12-24 stacked Transformer blocks (identical to the original paper).

**The Surprise:** Analysis of what BERT learned (Clark et al., 2019, “What Does BERT Look At?”) revealed that despite identical architecture across all layers, the network developed a clear hierarchy:

**Layer 1-4 (Early):**

- Attention heads focus on syntactic relationships (e.g., determiners attending to their nouns)
- Learn part-of-speech patterns
- Capture local, surface-level features

**Layer 5-8 (Middle):**

- Semantic role labeling emerges
- Entity recognition patterns
- More abstract semantic relationships

**Layer 9-12 (Late):**

- Coreference resolution (pronouns to antecedents)
- Pragmatic inference
- Task-specific behaviors

**The Profound Implication:**

The architecture didn’t specify this hierarchy—training discovered it! The uniform stack of transformer blocks provided a *scaffold*, and the optimization process found that specialization by depth was an effective strategy.

This validated the “scaffold hypothesis”: good architectural design isn’t about encoding specific behaviors, but about creating a space where useful behaviors are easy to learn.

**Paper:** “What Does BERT Look At? An Analysis of BERT’s Attention” (Clark et al., 2019)

**Citation:** <https://arxiv.org/abs/1906.04341>

---

### GPT-2 (2019): Scaling the Block

**Paper:** “Language Models are Unsupervised Multitask Learners” (Radford et al., 2019)

**Citation:** <https://d4mucfpksywv.cloudfront.net/better-language-models/language_models_are_unsupervised_multitask_learners.pdf>

**The Experiment:** What happens if you take the Transformer block and just… scale it?

**The Results:**

```
GPT-2 Small:   12 layers  × identical blocks = 117M params
GPT-2 Medium:  24 layers  × identical blocks = 345M params
GPT-2 Large:   36 layers  × identical blocks = 762M params
GPT-2 XL:      48 layers  × identical blocks = 1.5B params
```

**Key Finding:** Smooth scaling laws. Performance improved predictably with depth and width, following power laws (later formalized by Kaplan et al., 2020).

**The Implication:** The Transformer block had become a **universal scaling unit**. The field moved from “designing architectures” to “scaling a fixed architecture.”

---

## Era 4: The Search Era (2017-2021)

### Neural Architecture Search (2017-2019): Automating Component Discovery

**Foundational Paper:** “Neural Architecture Search with Reinforcement Learning” (Zoph & Le, 2017)

**Citation:** <https://arxiv.org/abs/1611.01578>

**The Motivation:** If architectures are compositions of building blocks, can we automate the search over combinations?

**The NAS Approach:**

1. **Define a search space:**

```
Operations = {conv3x3, conv5x5, maxpool, avgpool, skip, ...}
Connections = {sequential, parallel, skip-connection, ...}
```

1. **Use RL/evolution/gradient methods to search for combinations**
2. **Evaluate thousands of candidate architectures**

**Key Contribution:** Made explicit that architecture design is about choosing from a **compositional language**. The search space IS the language—a grammar of components and composition rules.

**Example Search Space (from paper):**

```
Cell = Composition of:
  - 5-7 operations (chosen from operation set)
  - Connection patterns between operations
  - Reduction cells vs. normal cells
```

The final architecture is a repetition of discovered cells—again, the pattern of uniform blocks!

---

### DARTS (2019): Differentiable Architecture Search

**Paper:** “DARTS: Differentiable Architecture Search” (Liu et al., 2019)

**Citation:** <https://arxiv.org/abs/1806.09055>

**The Innovation:** Instead of discrete search, treat architecture as a *continuous mixture* of operations.

**The Formulation:**

```
Output = Σᵢ (αᵢ · Operation_i(input))

where α are learned weights (architecture parameters)
```

**The Insight:** Architecture search becomes *gradient descent on architecture parameters* alongside weight parameters. The network literally learns which components to use!

**Why This Matters:** Blurs the line between architecture design and training. The “language of components” becomes a differentiable space that can be optimized directly.

**The Discovered Pattern:** DARTS consistently discovered skip connections and 3×3 separable convolutions—the same patterns humans had manually designed (ResNet, Xception). This validated that certain compositional patterns are fundamentally effective.

---

### Designing Network Design Spaces (2020): Principles Over Architectures

**Paper:** “Designing Network Design Spaces” (Radosavovic et al., 2020)

**Citation:** <https://arxiv.org/abs/2003.13678>

**The Paradigm Shift:**

Instead of searching for *one best architecture*, this paper asked: **What principles make a** ***family*** **of architectures work?**

**The Methodology:**

1. Define design dimensions:

   - Depth (number of blocks)
   - Width (channels per layer)
   - Group width (grouped convolutions)
   - Bottleneck ratio (expansion in blocks)
2. Sample thousands of random architectures from this space
3. Identify empirical principles:

```
Good design space:
- Width increases gradually across stages (not drastically)
- Depth is similar across stages
- Bottleneck ratio around 1.0 performs best
- Group width of 8-16 is optimal
```

1. Create RegNet family following these principles

**The Revolutionary Idea:**

> “Rather than focusing on designing individual network instances, we design network design spaces that parametrize populations of networks.”

This is exactly the “compositional language” perspective! They defined:

- **Primitives:** Block structure (X block with group convolution)
- **Composition rules:** How blocks stack (stage structure)
- **Constraints:** Principles that make compositions effective

**The Result:** RegNet architectures, generated by simple rules, matched or beat hand-designed networks and NAS-discovered architectures.

**The Implication:** Good architecture design is about **defining the right constraints on the compositional space**, not finding one perfect instantiation.

---

## Era 5: The Understanding Era (2019-2023)

### Scaling Laws (2020): Why Depth Matters

**Paper:** “Scaling Laws for Neural Language Models” (Kaplan et al., 2020)

**Citation:** <https://arxiv.org/abs/2001.08361>

**The Empirical Discovery:**

Model performance follows predictable power laws:

```
Loss ∝ (1/N^α) × (1/D^β) × (1/C^γ)

where:
N = number of parameters
D = dataset size
C = compute budget
```

**The Architectural Implication:**

For fixed compute budget, optimal allocation is:

- Depth: ~40-80 layers for 7B-70B models
- Width: 4K-8K hidden dimensions

**Why This Matters:** Explains why ~32 layers emerged as the “standard” for 7B models—not because 32 is magic, but because it’s the optimal depth for that parameter budget given current optimization methods.

**The Deeper Insight:**

The paper showed that architecture scaling (depth, width) should be done *proportionally*. You can’t just make one dimension huge—there’s an optimal balance. This suggests that the “compositional structure” (how blocks combine) has mathematical constraints.

---

### Lottery Ticket Hypothesis (2019): Architectures as Search Spaces

**Paper:** “The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks” (Frankle & Carbin, 2019)

**Citation:** <https://arxiv.org/abs/1803.03635>

**The Finding:**

> “Dense, randomly-initialized networks contain sparse subnetworks that—when trained in isolation—reach test accuracy comparable to the original network”

**The Interpretation:** A large architecture isn’t just a single computational graph—it’s a *space of possible subnetworks*. Training searches through this space.

**Why Repetition Works:**

Having 32 identical transformer layers provides many possible “paths” through the network. Some paths might be more important than others, but having redundancy:

1. Makes optimization easier (more chances to find good solutions)
2. Provides fallback routes if some paths fail
3. Allows different paths to specialize

**The Compositional View:** The architecture is less like a designed circuit and more like a **fabric of possibilities** that training selectively activates.

---

### Visualizing Loss Landscapes (2018): Why Blocks Enable Training

**Paper:** “Visualizing the Loss Landscape of Neural Nets” (Li et al., 2018)

**Citation:** <https://arxiv.org/abs/1712.09913>

**The Discovery:** Networks with residual connections have dramatically smoother loss landscapes than networks without them.

**Visual Result:**

```
Without residuals: Chaotic, many local minima, sharp peaks
With residuals:    Smooth convex-like regions, gentle slopes
```

**The Implication:** The residual block structure doesn’t just make gradients flow—it fundamentally changes the *optimization geometry*. The compositional structure (x + F(x)) creates a more trainable space than a monolithic design.

**Why This Validates Compositionality:** Good architectural building blocks aren’t just about expressiveness—they’re about creating loss landscapes that optimization algorithms can navigate.

---

### Mechanistic Interpretability: Circuits Emerge from Blocks

**Paper/Project:** “A Mathematical Framework for Transformer Circuits” (Elhage et al., 2021)

**Citation:** <https://transformer-circuits.pub/2021/framework/index.html>

**The Discovery:** Within transformer blocks, specific **circuits** emerge—reusable patterns of computation that implement recognizable algorithms.

**Examples Found:**

- **Induction heads:** Blocks that detect “A…B…A” patterns and predict “B”
- **Previous token heads:** Heads that always attend to the previous token
- **Duplicate token heads:** Heads that find copies of the current token

**The Profound Insight:**

These circuits are **compositions of the primitive operations** (Q, K, V projections, attention, MLPs). They’re not explicitly programmed—they emerge during training because the block structure makes them easy to implement.

**The Analogy:**

```
Assembly language provides: MOV, ADD, JMP
Programmers discover:      Loops, function calls, recursion

Transformer blocks provide: Q, K, V, MLP
Training discovers:         Induction heads, copying, matching
```

The architecture defines a **computational primitive set**, and training discovers **algorithms** built from those primitives.

---

## Era 6: The Hybrid Era (2023-Present)

### Moving Beyond Pure Uniformity

By 2023, researchers had thoroughly validated uniform repetition. But they also began asking: **When should we break uniformity?**

---

### Mixture of Experts (2022-2024): Conditional Composition

**Paper:** “Mixture-of-Experts Meets Instruction Tuning” (Shen et al., 2023) and “Mixtral of Experts” (Jiang et al., 2024)

**Citations:**

- <https://arxiv.org/abs/2305.14705>
- <https://arxiv.org/abs/2401.04088>

**The Idea:** Replace uniform MLP blocks with *conditional selection* from multiple expert MLPs.

**The Architecture:**

```
Standard Transformer:
  All tokens → Same MLP → Output

MoE Transformer:
  Each token → Router → Select 2 of 8 expert MLPs → Output
```

**Why It Works:**

Different experts naturally specialize:

- Expert 1: Math/code
- Expert 2: Creative writing
- Expert 3: Factual knowledge
- Expert 4: Translation
- etc.

**The Compositional Insight:** This is **learned non-uniformity**. The architecture still uses identical blocks, but adds a routing mechanism that lets tokens take different computational paths. The specialization isn’t hand-coded—it emerges during training.

**Mixtral-8×7B Results:**

- 8 experts, each 7B parameters
- Total: 47B parameters, but only 13B active per token
- Matches 70B dense models at 5× lower inference cost

**The Pattern:** When breaking uniformity helps, let the *model* learn when to break it (via routers), rather than hard-coding architectural variation.

---

### Mamba (2023): Alternative Primitives

**Paper:** “Mamba: Linear-Time Sequence Modeling with Selective State Spaces” (Gu & Dao, 2023)

**Citation:** <https://arxiv.org/abs/2312.00752>

**The Question:** Does *attention* have to be the core primitive, or can we use different building blocks?

**The Mamba Block:**

```
Instead of: Attention + MLP
Use:        Selective State Space Layer + MLP
```

State space models (SSMs) are an alternative to attention for sequence mixing:

- **Attention:** O(n²) complexity, global context
- **SSM:** O(n) complexity, selective memory

**Why This Matters:** Shows that the Transformer block structure (mixing layer + pointwise layer + residuals) is more fundamental than any specific mixing mechanism. You can swap attention for SSMs and keep everything else.

**The Compositional Lesson:** A good architectural “language” should have **swappable components**. The residual + norm + mixing + MLP structure is the syntax; attention vs SSM is vocabulary choice.

---

### Hybrid Architectures: Compositional Mixing

**Recent Trend (2023-2024):** Combine different primitive types in one model.

**Example: Jamba (AI21 Labs, 2024)**

```
Layers 1-8:   Mamba blocks (efficient, local context)
Layers 9-16:  Attention blocks (global reasoning)
Layers 17-24: Mamba blocks (local refinement)
Layers 25-32: Attention blocks (output generation)
```

**Why It Works:**

- Mamba handles repetitive patterns efficiently
- Attention handles long-range dependencies
- Different layers need different capabilities

**The Design Philosophy:** Don’t force uniformity where non-uniformity helps, but make the non-uniformity **principled** (alternating pattern) rather than ad-hoc.

---

## Era 7: Modern Compositional Thinking (2024-Present)

### Current State: Component Libraries

Today, architecture design has evolved into **selecting from a library of validated components**:

**Attention Variants:**

- Multi-head attention (original)
- Multi-query attention (faster inference)
- Grouped-query attention (balance speed/quality)
- Flash Attention (optimized implementation)

**Position Encodings:**

- Sinusoidal (original)
- Learned absolute
- Rotary (RoPE) - current best for long context
- ALiBi - best for length generalization

**Normalizations:**

- LayerNorm (original)
- RMSNorm (simpler, just as good)
- Pre-norm vs post-norm (pre-norm won)

**Activations:**

- ReLU (original)
- GELU (better for transformers)
- SiLU/Swish (used in modern LLMs)

**MLP Variants:**

- Standard (Linear → Act → Linear)
- GLU (Gated Linear Unit)
- SwiGLU (current best) - Llama, Qwen, Mistral all use this

**The Design Process Today:**

1. Start with base Transformer block structure (proven)
2. Select components from validated options:

```
Attention: GQA
Position: RoPE
Norm: RMSNorm
MLP: SwiGLU
```

1. Determine scaling (depth, width) using scaling laws
2. Add specialized components if needed (MoE, hybrid layers)

**Example: Llama 3 (2024)**

```
class LlamaBlock:
    attention = GroupedQueryAttention(
        position_encoding=RoPE
    )
    norm1 = RMSNorm()
    mlp = SwiGLU()
    norm2 = RMSNorm()
# Stack 80 identical blocksmodel = Stack([LlamaBlock() for _ in range(80)])
```

Every component is a *choice from the library*, not a custom design.

---

### DR Tulu (2025): RL with Evolving Rubrics

**Paper:** “DR Tulu: Reinforcement Learning with Evolving Rubrics for Deep Research” (Shao, Asai, et al., 2025)

**Citation:** <https://arxiv.org/abs/2511.19399>

**Relevance to Compositional Design:**

DR Tulu demonstrates a new dimension of the “scaffold hypothesis”: not just architectural scaffolds, but **training scaffolds** that evolve with the model.

**The Method:**

- Base architecture: Standard Qwen3-8B (proven Transformer blocks)
- Innovation: Not in architecture, but in training methodology
- Evolving rubrics provide dynamic learning objectives

**The Insight:** Once we have good architectural building blocks (Transformer layers), the frontier shifts to **how we train** those blocks. The compositional language extends beyond static structure to dynamic training procedures.

**Why This Fits the Narrative:**

1. **Uses standard components:** Proves you don’t need novel architecture
2. **Focuses on training:** The next dimension of compositionality
3. **Achieves SOTA:** 8B model matches 175B+ proprietary systems

The field is moving from “what blocks should we use?” to “how should we train the blocks we have?”

---

## The Emerging Principles

From this 13-year journey, several principles have crystallized:

### Principle 1: Uniformity Enables Scale

**Evidence:**

- ResNet: 50-152 layers of identical blocks
- GPT-3: 96 identical transformer layers
- Llama 70B: 80 identical blocks

**Why:** Uniform blocks are easier to:

- Optimize (one set of hyperparameters)
- Scale (just add more)
- Analyze (compare across depths)
- Parallelize (same computation)

**Exception:** When introducing non-uniformity, make it *learned* (MoE routing) or *principled* (alternating patterns).

---

### Principle 2: Residual Structure is Fundamental

**Evidence:**

- Every modern architecture uses residuals (ResNet, Transformer, Mamba)
- Loss landscape analysis shows they enable training
- Theory: Residuals create implicit ensembles

**Why:** `x + F(x)` is more than a training trick—it’s a **compositional operator** that allows additive construction of representations.

---

### Principle 3: Specialization Emerges, Don’t Force It

**Evidence:**

- BERT layers specialize despite identical architecture
- MoE experts specialize without explicit supervision
- Early/mid/late layers learn different abstractions naturally

**Why:** The optimization landscape naturally encourages specialization when it’s useful. Pre-specifying it (e.g., “layer 1-10 for syntax, 11-20 for semantics”) often hurts because you might be wrong about what’s needed.

**Design Implication:** Provide uniform capacity and let training discover the specialization pattern.

---

### Principle 4: Components Should Be Swappable

**Evidence:**

- Can swap attention → SSM (Mamba)
- Can swap GELU → SiLU (minimal impact)
- Can swap LayerNorm → RMSNorm (often better)

**Why:** Good “compositional languages” have **interfaces** that allow substitution. The Transformer block structure:

```
x = x + Mixing(Norm(x))
x = x + Pointwise(Norm(x))
```

doesn’t care whether Mixing is attention, convolution, or SSM—the interface is the same.

---

### Principle 5: Depth Is Iterative Refinement

**Evidence:**

- Lottery ticket hypothesis: Many paths through the network
- Scaling laws: Depth and width must scale proportionally
- Interpretability: Later layers refine earlier representations

**Why:** Deep networks don’t work by hierarchical stages (layer 1 → 2 → 3 → …) but by **iterative refinement** where each layer adds a small update. The residual structure makes this explicit.

**Math:**

```
x_out = x_0 + Δx_1 + Δx_2 + ... + Δx_n

Each layer contributes a refinement Δx_i
```

---

### Principle 6: Optimization Geometry Determines Viability

**Evidence:**

- Loss landscape visualizations (Li et al., 2018)
- Why some architectures train better than others
- Batch normalization, layer normalization effects

**Why:** An architecture isn’t good because it’s “more expressive”—it’s good because gradient descent can find good solutions. The compositional structure creates a trainable loss surface.

---

## The Future: From Blocks to Ecosystems

Where is this heading?

### Trend 1: Learned Architecture Components

**Current:** Hand-design the component library

**Future:** Meta-learning to discover new primitives

**Example Research:**

- AutoML-Zero (Google): Evolve mathematical operations from scratch
- Neural Tangent Kernel theory: Understand what functions different architectures can learn
- Mechanistic design: Design blocks to implement specific circuits

---

### Trend 2: Dynamic Architectures

**Current:** Fixed depth/width at train time

**Future:** Adapt architecture during inference

**Examples:**

- Early exit (stop when confident)
- Adaptive depth (harder inputs get more layers)
- Conditional computation (activate only needed blocks)

**The Vision:** Architecture becomes a **menu of computational options**, and the model learns a policy for which options to use per input.

---

### Trend 3: Compositional Training Methods

DR Tulu represents this: keeping architecture simple while making training more sophisticated.

**Other Examples:**

- Curriculum learning (order training data compositionally)
- Multi-task learning (compose objectives)
- Evolving loss functions (like evolving rubrics)

**The Shift:** From “design better blocks” to “design better training procedures that teach existing blocks new tricks.”

---

### Trend 4: Cross-Modal Composability

**Current:** Different architectures for vision (CNNs/ViT), language (Transformers), audio (Conformers)

**Future:** Universal blocks that work across modalities

**Progress:**

- Vision Transformers (apply language blocks to vision)
- Perceiver architecture (unified for all inputs)
- Flamingo (mix image and text blocks)

**The Goal:** A single compositional language that works for any data type, with modality-specific adaptations happening via learned components (like MoE), not architectural redesign.

---

### Trend 5: Efficiency Through Compositionality

**The Realization:** The same compositional structure that makes architectures trainable also makes them compressible.

**Examples:**

- LoRA: Only a subset of weights need adaptation
- Quantization: Different blocks can use different precisions
- Pruning: Remove entire blocks with minimal impact
- Distillation: Compress 100-layer → 12-layer models

**Why Compositionality Helps:** If blocks are modular and somewhat redundant, you can remove/compress/approximate individual blocks without breaking the whole system.

---

## Conclusion: The Scaffold Hypothesis Validated

We’ve traced a 13-year journey from AlexNet’s hand-crafted hierarchy to today’s compositional design philosophy. The field discovered that:

1. **Uniformity scales better than specificity**

   ResNet’s repeated blocks beat carefully designed hierarchies
2. **Emergent specialization beats forced specialization**

   BERT’s layers learned syntax→semantics→pragmatics without being told to
3. **Simple primitives enable complex behaviors**

   Q, K, V attention supports everything from grammar to reasoning
4. **Composition rules matter as much as components**

   Residual connections fundamentally changed what’s learnable
5. **Architecture is a hypothesis space for training to explore**

   Lottery tickets, loss landscapes, and scaling laws all point to this

**The Modern Paradigm:**

Architecture design is no longer “build the perfect network.” It’s “design a compositional language of:

- **Primitives** (attention, MLPs, convolutions, SSMs)
- **Composition operators** (residuals, concatenation, gating)
- **Structural patterns** (repeated blocks, skip connections)

that create a space where gradient descent can discover useful algorithms.”

**Why This Matters:**

This shift has practical consequences:

- **Faster iteration:** Test new components without redesigning everything
- **Better transfer:** Components learned in one context work in another
- **Clearer debugging:** Understand what each block does
- **Principled scaling:** Apply scaling laws confidently
- **Open science:** Share component libraries, not monolithic models

**The Open Questions:**

1. **What are the fundamental primitives?** We have attention, convolution, SSMs—what else?
2. **What composition operators haven’t we discovered?** Residuals were a breakthrough—what’s the next one?
3. **How do we design for interpretability?** Can we build blocks that are compositionally interpretable (circuits)?
4. **What’s the optimal balance between uniformity and specialization?** MoE shows some heterogeneity helps—what’s the right amount?
5. **Can we automate principled design?** Not NAS (search), but discovering the principles (like RegNet did)?

**The Through-Line:**

From AlexNet to DR Tulu, the most successful architectures weren’t the most clever—they were the most **compositional**. They gave training a rich space to explore, with clear building blocks and combination rules.

As we move into the era of ever-larger models trained on ever-more compute, this compositional perspective becomes even more critical. We can’t manually design networks at trillion-parameter scale. We need to design **languages** that scale.

The scaffold hypothesis—that architecture creates a space for training to discover algorithms—has been thoroughly validated. The future isn’t designing better specific models; it’s designing better languages for describing computational structures, and better training methods for teaching those structures to do useful work.

**We’re not building neural networks anymore. We’re building grammars of computation, and training is the process of writing programs in those grammars.**

---

## References & Further Reading

### Foundational Papers (Chronological)

1. **Krizhevsky et al. (2012)** - AlexNet: ImageNet Classification with Deep CNNs

   <https://papers.nips.cc/paper/4824>
2. **Simonyan & Zisserman (2014)** - VGGNet: Very Deep Convolutional Networks

   <https://arxiv.org/abs/1409.1556>
3. **He et al. (2015)** - ResNet: Deep Residual Learning for Image Recognition

   <https://arxiv.org/abs/1512.03385>
4. **Vaswani et al. (2017)** - Attention Is All You Need

   <https://arxiv.org/abs/1706.03762>
5. **Devlin et al. (2018)** - BERT: Pre-training of Deep Bidirectional Transformers

   <https://arxiv.org/abs/1810.04805>

### Understanding Architectures

1. **Veit et al. (2016)** - Residual Networks Behave Like Ensembles

   <https://arxiv.org/abs/1605.06431>
2. **Li et al. (2018)** - Visualizing the Loss Landscape of Neural Nets

   <https://arxiv.org/abs/1712.09913>
3. **Clark et al. (2019)** - What Does BERT Look At?

   <https://arxiv.org/abs/1906.04341>
4. **Frankle & Carbin (2019)** - The Lottery Ticket Hypothesis

   <https://arxiv.org/abs/1803.03635>
5. **Kaplan et al. (2020)** - Scaling Laws for Neural Language Models

   <https://arxiv.org/abs/2001.08361>

### Architecture Search & Design

1. **Zoph & Le (2017)** - Neural Architecture Search with Reinforcement Learning

   <https://arxiv.org/abs/1611.01578>
2. **Liu et al. (2019)** - DARTS: Differentiable Architecture Search

   <https://arxiv.org/abs/1806.09055>
3. **Radosavovic et al. (2020)** - Designing Network Design Spaces

   <https://arxiv.org/abs/2003.13678>

### Modern Architectures & Surveys

1. **Lin et al. (2022)** - A Survey of Transformers

   <https://arxiv.org/abs/2106.04554>
2. **Gu & Dao (2023)** - Mamba: Linear-Time Sequence Modeling with SSMs

   <https://arxiv.org/abs/2312.00752>
3. **Jiang et al. (2024)** - Mixtral of Experts

   <https://arxiv.org/abs/2401.04088>
4. **Shao, Asai et al. (2025)** - DR Tulu: RL with Evolving Rubrics for Deep Research

   <https://arxiv.org/abs/2511.19399>

### Books

1. **Goodfellow, Bengio, Courville (2016)** - Deep Learning

https://www.deeplearningbook.org/

1. **Prince (2023)** - Understanding Deep Learning

   <https://udlbook.github.io/udlbook/>

### Online Resources

1. **Transformer Circuits (Anthropic)** - Mechanistic Interpretability

https://transformer-circuits.pub/

1. **Distill.pub** - Visual Explanations of ML Concepts

https://distill.pub/

---

*This blog post synthesizes insights from 13 years of research into neural architecture design. The field continues to evolve rapidly—the best way to stay current is to follow major ML conferences (NeurIPS, ICML, ICLR) and research blogs from leading labs.*
