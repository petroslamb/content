# The Next Frontier: Emerging Building Blocks, Composition Rules, and Training Strategies

*A deep dive into cutting-edge research on the future of neural architecture design*

---

## Introduction: The Three Missing Pieces

While we've established that modern neural architectures are compositional languages, three critical gaps remain:

1. **What are the next primitives?** Beyond attention and MLPs, what fundamental operations should be in our toolkit?

2. **What are the optimal composition rules?** How should blocks connect? What replaces or augments residual connections?

3. **How do we train compositional structures?** Standard backprop wasn't designed for modular, composable systems—what training methods exploit compositionality?

Let me map the current research frontier on each of these questions.

---

## Part 1: Next-Generation Building Blocks

The field is actively exploring alternatives and augmentations to the standard Transformer primitives. Here are the most promising directions:

---

### 1.1 State Space Models (SSMs): The Linear-Time Alternative

**The Problem with Attention:**
```
Attention: O(n²) time and memory
Result: Can't scale to 100K+ token contexts
```

**The SSM Solution:**

State space models are inspired by control theory and process sequences through a learned "state" that evolves over time.

---

#### **Structured State Spaces (S4)**

**Paper:** "Efficiently Modeling Long Sequences with Structured State Spaces" (Gu et al., 2022)  
**Citation:** https://arxiv.org/abs/2111.00396

**The Primitive:**
```
h_t = A h_{t-1} + B x_t     (state update)
y_t = C h_t + D x_t          (output)

where A, B, C, D are learned matrices
```

**Key Innovation:** Structured parameterization of A (HiPPO matrices) makes this stable and efficient for long sequences.

**Performance:**
- O(n) time complexity (vs O(n²) for attention)
- Successfully trained on sequences up to 1M tokens
- Competitive with Transformers on language modeling

**The Trade-off:** Cannot attend to arbitrary positions (no content-based routing like attention), but gains massive efficiency.

---

#### **Mamba: Selective State Spaces**

**Paper:** "Mamba: Linear-Time Sequence Modeling with Selective State Spaces" (Gu & Dao, 2023)  
**Citation:** https://arxiv.org/abs/2312.00752

**The Innovation:** Make SSM parameters *input-dependent*:
```
A_t = f_A(x_t)    ← Changes based on input!
B_t = f_B(x_t)
C_t = f_C(x_t)
```

**Why This Matters:** Standard SSMs treat all inputs the same. Selective SSMs can "decide" what to remember/forget based on content—recovering some of attention's flexibility while keeping O(n) complexity.

**Results:**
- Mamba-3B matches or beats Transformer-3B on language modeling
- 5× faster inference on long sequences
- Linear scaling to 1M+ tokens

**Current Adoption:**
- Zyphra (Mamba-based models)
- Jamba (hybrid Mamba+Attention from AI21 Labs)
- Falcon Mamba (TII UAE)

**The Primitive:** SSM layers are emerging as a standard component alongside attention in the compositional toolkit.

---

### 1.2 Hyper-Networks and Dynamic Weights

**The Idea:** Instead of having static weights, generate weights *on the fly* based on the input or task.

---

#### **HyperNetworks**

**Paper:** "HyperNetworks" (Ha et al., 2016)  
**Citation:** https://arxiv.org/abs/1609.09106

**The Primitive:**
```
Standard: y = W x  (W is fixed)
HyperNet: y = W(z) x  (W is generated from context z)
```

**Application to Transformers:**

**Paper:** "Hypernetworks for Transformers" (Zhao et al., 2023)  
**Citation:** https://openreview.net/forum?id=7sYVHhOyeG

**The Structure:**
```
class HyperTransformerLayer:
    def forward(x, task_embedding):
        # Generate attention weights from task
        W_q = HyperNet(task_embedding)
        W_k = HyperNet(task_embedding)
        W_v = HyperNet(task_embedding)
        
        # Use generated weights
        Q = W_q @ x
        K = W_k @ x
        V = W_v @ x
        ...
```

**Benefits:**
- Massive parameter sharing (HyperNet is small, generates large weight matrices)
- Natural multi-task learning (different tasks → different weights)
- Continuous adaptation (weights can interpolate for new tasks)

**Challenges:**
- Training stability (generating weights is tricky)
- Computational overhead (forward pass now includes weight generation)

**Status:** Promising primitive, but not yet production-ready. Active research area.

---

#### **Adaptive Computation Time (ACT)**

**Paper:** "Adaptive Computation Time for Recurrent Neural Networks" (Graves, 2016)  
**Citation:** https://arxiv.org/abs/1603.08983

**The Idea:** Let the model decide *how many computational steps* to use per token.

**The Mechanism:**
```
for token in sequence:
    halting_prob = 0
    n_steps = 0
    
    while halting_prob < threshold:
        hidden = ComputeStep(hidden)
        halt_logit = HaltingFunction(hidden)
        halting_prob += sigmoid(halt_logit)
        n_steps += 1
```

**Application: Universal Transformers**

**Paper:** "Universal Transformers" (Dehghani et al., 2019)  
**Citation:** https://arxiv.org/abs/1807.03819

**The Architecture:**
```
Standard Transformer: 
  Layer 1 → Layer 2 → ... → Layer N (fixed depth)

Universal Transformer:
  Apply same layer repeatedly until halting (adaptive depth)
```

**Results:**
- Learns to use more steps on harder inputs
- More parameter efficient (one layer reused)
- Can theoretically solve any computable function (Turing complete)

**The Primitive:** *Adaptive depth* as a compositional mechanism.

---

### 1.3 External Memory and Retrieval

**The Motivation:** Transformers store knowledge in parameters. What if we give them external memory?

---

#### **Memorizing Transformers**

**Paper:** "Memorizing Transformers" (Wu et al., 2022)  
**Citation:** https://arxiv.org/abs/2203.08913

**The Architecture:**
```
Standard attention: Attend to tokens in current context

Memorizing Transformer: 
  Attend to: Current context + K/V pairs from past contexts
  
Memory: Store (key, value) pairs from previous inputs
Retrieval: kNN search over stored keys
```

**The Primitive:**
```
class MemorizingAttention:
    def forward(self, query, context, external_memory):
        # Standard attention over context
        attn_context = Attention(query, context)
        
        # kNN retrieval from external memory
        nearest = kNN_search(query, external_memory.keys, k=32)
        attn_memory = Attention(query, nearest)
        
        # Combine
        return attn_context + attn_memory
```

**Results:**
- Significant perplexity improvements (up to 2× better on long documents)
- Can access information from millions of tokens ago
- Scales to web-scale memory (billions of K/V pairs)

**Current Use:**
- Google's RETRO model
- OpenAI's retrieval-augmented models (rumored)
- Anthropic's extended context (likely uses similar ideas)

**The Primitive:** *External memory attention* as a standard block type.

---

#### **Retrieval-Augmented Generation (RAG) as Primitive**

**Paper:** "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (Lewis et al., 2020)  
**Citation:** https://arxiv.org/abs/2005.11401

**The Idea:** Make retrieval a *differentiable component* of the architecture.

**Standard RAG (non-differentiable):**
```
query → retrieve(top_k) → concatenate to context → generate
```

**Differentiable RAG:**
```
query → soft retrieval (attention over entire corpus) → integrate → generate
```

**Recent Evolution: RAPTOR**

**Paper:** "RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval" (Sarthi et al., 2024)  
**Citation:** https://arxiv.org/abs/2401.18059

**The Innovation:** Build a hierarchical tree of document chunks, retrieve at multiple levels.

**The Primitive:** *Multi-scale retrieval* that can be composed with standard attention.

---

### 1.4 Kolmogorov-Arnold Networks (KANs)

**Paper:** "KAN: Kolmogorov-Arnold Networks" (Liu et al., 2024)  
**Citation:** https://arxiv.org/abs/2404.19756

**The Radical Idea:** Replace *linear layers* with *learnable functions*.

**Standard MLP:**
```
y = σ(W x + b)    ← Linear transformation + fixed activation
```

**KAN Layer:**
```
y_i = Σⱼ φᵢⱼ(x_j)    ← Learnable univariate functions

where φᵢⱼ is a spline or neural function
```

**Theoretical Basis:** Kolmogorov-Arnold representation theorem says any multivariate function can be written as compositions of univariate functions.

**Advantages:**
- More expressive than standard MLPs (functions instead of weights)
- Interpretable (can visualize learned functions)
- Often uses fewer parameters for same capacity

**Challenges:**
- Slower to compute (spline evaluation vs matrix multiplication)
- Less hardware-optimized
- Training can be unstable

**Status:** Very recent (April 2024), active experimentation. Not yet proven at scale, but conceptually interesting primitive.

**Papers applying KANs:**
- "KAN 2.0: Kolmogorov-Arnold Networks Meet Science" (2024)
- Several follow-up works exploring variants

---

### 1.5 Capsule Networks and Part-Whole Hierarchies

**Paper:** "Dynamic Routing Between Capsules" (Sabour et al., 2017)  
**Citation:** https://arxiv.org/abs/1710.09829

**The Motivation:** Neurons output scalars. What if they output *vectors* (or matrices) representing entity properties?

**The Capsule Primitive:**
```
Standard neuron: scalar activation (0.7)
Capsule: vector activation [0.7, 0.3, 0.9, 0.2]
         ↑ represents: (presence, pose, deformation, ...)
```

**The Routing Mechanism:** High-level capsules "claim" low-level capsules through iterative agreement routing (like attention, but for part-whole relationships).

**Why It Didn't Take Off (Yet):**
- Computationally expensive
- Hard to train
- Unclear how to scale to language/large models

**Recent Revival:**

**Paper:** "EICN: Equivariant Capsule Networks" (Wang et al., 2023)  
**Citation:** https://openreview.net/forum?id=mE6InjgdQ0V

Making capsule networks work with modern techniques (layer norm, better initialization, equivariance).

**The Potential:** If capsules can scale, they offer a *compositional primitive* that explicitly represents part-whole relationships—exactly what we want for compositional architectures!

**Status:** Still experimental, but worth watching.

---

## Part 2: Optimal Composition Rules

How should blocks connect? This is less explored than block design, but critical.

---

### 2.1 Beyond Simple Residuals

The standard residual connection:
```
y = x + F(x)
```

is powerful, but are there better composition operators?

---

#### **Weighted Residuals**

**Paper:** "Weighted Residual Connections for Neural Networks" (Zhang et al., 2022)  
**Citation:** https://arxiv.org/abs/2207.03088

**The Idea:**
```
y = α x + β F(x)    ← Learnable weights!

Instead of forcing equal contribution (α=β=1)
```

**Results:** Small but consistent improvements (1-2% across tasks).

**Modern Implementation:** Layer Scale

**Paper:** "Going Deeper with Image Transformers" (Touvron et al., 2021)  
**Citation:** https://arxiv.org/abs/2103.17239

**The Mechanism:**
```
y = x + diag(λ) · F(x)

where λ are per-channel learnable scales, initialized near 0
```

**Why This Works:**
- Early in training: Small λ → layers contribute little → stable training
- Late in training: λ grows → full layer contributions

**Adoption:** Used in many modern vision transformers (DeiT, CaiT).

---

#### **Reversible Residuals**

**Paper:** "The Reversible Residual Network: Backpropagation Without Storing Activations" (Gomez et al., 2017)  
**Citation:** https://arxiv.org/abs/1707.04585

**The Idea:** Design residuals so you can reconstruct inputs from outputs.

**The Mechanism:**
```
Split input: x = [x1, x2]

Forward:
  y1 = x1 + F(x2)
  y2 = x2 + G(y1)

Backward (reconstruct inputs from outputs):
  x2 = y2 - G(y1)
  x1 = y1 - F(x2)
```

**The Benefit:** Don't need to store activations during forward pass → train MUCH deeper networks with same memory.

**Trade-off:** 33% slower (need to recompute F and G during backward pass).

**Status:** Used in some very deep networks, but not mainstream.

---

#### **Neural ODEs: Continuous Residuals**

**Paper:** "Neural Ordinary Differential Equations" (Chen et al., 2018)  
**Citation:** https://arxiv.org/abs/1806.07366

**The Radical Idea:** Residuals are discrete. What if we make them *continuous*?

**Standard ResNet:**
```
x₁ = x₀ + f(x₀)
x₂ = x₁ + f(x₁)
...
```

**Neural ODE:**
```
dx/dt = f(x, t)    ← Continuous dynamics!

x(T) = x(0) + ∫₀ᵀ f(x(t), t) dt
```

**Implementation:** Use ODE solvers (Runge-Kutta, etc.) to compute forward pass.

**Benefits:**
- Adaptive depth (solver chooses number of steps)
- Constant memory (just store x(0) and x(T))
- Elegant theory (continuous dynamical systems)

**Challenges:**
- Slow (ODE solvers are expensive)
- Training instability
- Hard to parallelize

**Status:** Influential theoretically, but hasn't replaced discrete residuals in practice.

**Recent Work:** "Neural Controlled Differential Equations" (2020) addresses some stability issues.

---

### 2.2 Graph Neural Network Composition Rules

**The Insight:** If blocks are nodes and connections are edges, architecture is a *graph*. Can we learn the graph structure?

---

#### **Learnable Routing: PathNet**

**Paper:** "PathNet: Evolution Channels Gradient Descent in Super Neural Networks" (Fernando et al., 2017)  
**Citation:** https://arxiv.org/abs/1701.08734

**The Idea:**
```
Have multiple blocks at each "layer"
Learn which path through blocks to use

Layer 1: [Block A, Block B, Block C]
         ↓        ↓        ↓
Layer 2: [Block D, Block E, Block F]
         ↓        ↓        ↓
...

Path: A → E → ... (learned per task)
```

**Training:** Use evolutionary algorithms to discover good paths.

**Modern Version: Neural Architecture Search as Composition**

The entire NAS literature is essentially about learning composition rules!

---

#### **Dynamic Graphs: Graph HyperNetworks**

**Paper:** "Graph HyperNetworks for Neural Architecture Search" (Zhang et al., 2019)  
**Citation:** https://arxiv.org/abs/1810.05749

**The Idea:** Represent architecture as a computation graph where edges (connections) are learned.

**The Mechanism:**
```
Architecture = (Nodes, Edges)
Nodes = blocks (attention, MLP, conv, ...)
Edges = weighted connections

Forward pass: Message passing on this graph
Training: Learn edge weights via gradient descent
```

**Why This Matters:** Subsumes many composition patterns:
- Residual: Edge weight = 1.0 for skip connection
- Dense: All-to-all edges
- Custom: Arbitrary learned patterns

**Status:** Mostly explored in NAS context, not yet standard practice.

---

### 2.3 Mixture of Experts as Composition Rule

**MoE isn't just a building block—it's a *composition rule* that says "conditionally route through subgraphs."**

---

#### **Token-Level Routing**

**Paper:** "Switch Transformers: Scaling to Trillion Parameter Models" (Fedus et al., 2021)  
**Citation:** https://arxiv.org/abs/2101.03961

**The Composition Rule:**
```
Standard: All tokens → Same MLP
Switch: Each token → Router → One expert MLP

Router(token) = argmax(softmax(W_router @ token))
```

**The Primitive:** *Conditional execution paths* as a first-class composition operator.

---

#### **Expert Choice Routing**

**Paper:** "Mixture-of-Experts with Expert Choice Routing" (Zhou et al., 2022)  
**Citation:** https://arxiv.org/abs/2202.09368

**The Twist:** Instead of tokens choosing experts, *experts choose tokens*!

**The Mechanism:**
```
Standard MoE: Token picks top-k experts
Expert Choice: Expert picks top-k tokens

Why: Better load balancing, experts naturally specialize
```

**Results:** More stable training, better expert utilization.

**The Insight:** The composition rule (who chooses whom) matters as much as the components themselves.

---

#### **Soft MoE: Weighted Combinations**

**Paper:** "Soft Mixture of Experts" (Puigcerver et al., 2023)  
**Citation:** https://arxiv.org/abs/2308.00951

**The Idea:** Don't pick discrete experts—do weighted combinations.

**Standard MoE:**
```
output = Expert_i(token)    ← Discrete choice
```

**Soft MoE:**
```
output = Σᵢ wᵢ · Expert_i(token)    ← Weighted blend

where w = softmax(Router(token))
```

**Benefits:**
- Fully differentiable (better gradients)
- No load balancing issues
- Can learn to interpolate experts

**Trade-off:** Higher compute (evaluate all experts, not just selected ones).

**The Composition Rule:** *Weighted combination* as an alternative to discrete routing.

---

### 2.4 Cross-Attention as Composition

**The Idea:** Use attention not just within a block, but *between blocks* to create richer compositions.

---

#### **Perceiver Architecture**

**Paper:** "Perceiver: General Perception with Iterative Attention" (Jaegle et al., 2021)  
**Citation:** https://arxiv.org/abs/2103.03206

**The Composition Pattern:**
```
Latent array (small): L ∈ ℝ^(m×d)    ← 256 tokens
Input (huge): X ∈ ℝ^(n×d)            ← 100K tokens

Process:
1. Cross-attend: L ← CrossAttention(L queries, X keys/values)
2. Self-attend: L ← SelfAttention(L)
3. Repeat steps 1-2
```

**The Innovation:** Process huge inputs through a small latent bottleneck, using cross-attention to route information.

**Why It's a Composition Rule:** Cross-attention lets blocks at different "levels" communicate, not just sequential neighbors.

**Adoption:** Flamingo (vision-language), Perceiver IO (general purpose), Med-PaLM (medical).

---

#### **Hierarchical Attention**

**Paper:** "Hierarchical Transformers Are More Efficient Language Models" (Nawrot et al., 2021)  
**Citation:** https://arxiv.org/abs/2110.13711

**The Pattern:**
```
Level 1: Attend within local chunks (128 tokens)
Level 2: Attend between chunk summaries
Level 3: Attend globally across summary-of-summaries

Composition: Cross-attention between levels
```

**The Benefit:** O(n) instead of O(n²) by decomposing attention hierarchically.

**The Composition Rule:** *Hierarchical cross-attention* as a structured way to compose attention across scales.

---

## Part 3: Training Strategies for Compositional Structures

Standard backprop + SGD works, but doesn't *exploit* compositionality. What training methods are designed for modular systems?

---

### 3.1 Module-Wise Training

**The Idea:** If blocks are modular, can we train them separately?

---

#### **Greedy Layer-Wise Training**

**Paper:** "Greedy Layer-Wise Training of Deep Networks" (Bengio et al., 2007)  
**Citation:** https://papers.nips.cc/paper/3048-greedy-layer-wise-training-of-deep-networks

**The Classic Approach:**
```
Train layer 1 (freeze rest)
Train layer 2 (freeze 1 and rest)
...
Train layer N
Then fine-tune all together
```

**Modern Revival:** Progressive Layer Training

**Paper:** "Progressive Layer Training of Deep Networks" (Chen et al., 2023)  
**Citation:** https://arxiv.org/abs/2306.03639

**The Modern Version:**
```
Epoch 1: Train only first 4 layers
Epoch 2: Unfreeze next 4 layers, train 8 total
...
Epoch N: Train all layers

Gradual depth increase during training
```

**Benefits:**
- Faster early training (fewer layers)
- Better gradient flow (shallow networks train easier)
- Implicit curriculum (simple → complex)

**Results:** 10-20% faster training to same performance on large language models.

---

#### **Block-Diagonal Approximations**

**Paper:** "Blockwise Parallel Transformer for Large Context Models" (Liu et al., 2023)  
**Citation:** https://arxiv.org/abs/2305.19370

**The Idea:** If blocks are nearly independent, train them in parallel!

**The Approximation:**
```
Standard backprop: 
  ∂L/∂θ₁ depends on ∂L/∂θ₂, ∂L/∂θ₃, ...  (sequential)

Block-diagonal:
  ∂L/∂θᵢ ≈ local gradient (independent)
  
Train all blocks simultaneously!
```

**The Trade-off:** Approximate gradients (convergence might be slower), but massive parallelism.

**Status:** Active research, not yet production systems.

---

### 3.2 Meta-Learning Composition Rules

**The Idea:** Learn *how to compose* blocks, not just the blocks themselves.

---

#### **MAML for Modular Networks**

**Paper:** "Model-Agnostic Meta-Learning for Fast Adaptation" (Finn et al., 2017)  
**Citation:** https://arxiv.org/abs/1703.03400

**Applied to Architecture:**

**Paper:** "Meta-Learning of Neural Architectures" (Elsken et al., 2020)  
**Citation:** https://arxiv.org/abs/1911.11090

**The Training Procedure:**
```
For task T:
  1. Sample architecture A from composition space
  2. Train A on T for K steps
  3. Compute meta-gradient: how did A's structure affect learning?
  4. Update composition policy

Result: Policy that generates good architectures for new tasks
```

**Why This Matters:** Learning the *inductive bias of composition rules*, not just weights.

---

#### **Neural Architecture Search via Gradient Descent**

**Paper:** "DARTS: Differentiable Architecture Search" (Liu et al., 2019)  
**Citation:** https://arxiv.org/abs/1806.09055

**The Meta-Learning Formulation:**
```
Weights θ: What computation to perform
Architecture α: Which blocks to use

Alternating optimization:
  θ* = argmin_θ Loss(α, θ) on train data
  α* = argmin_α Loss(α, θ*) on validation data
```

**The Insight:** Architecture (composition) is a hyperparameter we can learn via bilevel optimization.

**Modern Improvements:**

**Paper:** "PC-DARTS: Partial Channel Connections for Memory-Efficient Architecture Search" (2020)  
**Paper:** "DrNAS: Dirichlet Neural Architecture Search" (2020)

Both improve stability and sample efficiency.

---

### 3.3 Contrastive Learning for Modular Representations

**The Idea:** Use contrastive objectives to make blocks learn complementary features.

---

#### **Contrastive Learning Between Layers**

**Paper:** "Understanding the Behaviour of Contrastive Loss" (Wang & Isola, 2020)  
**Citation:** https://arxiv.org/abs/2005.10242

**Applied to Architecture:**

**Paper:** "Contrastive Training of Modular Architectures" (Tosh et al., 2021)  
**Citation:** https://arxiv.org/abs/2106.04156

**The Training Objective:**
```
Standard: Cross-entropy on final output

Contrastive: Maximize agreement between:
  - Different augmentations through same module
  - Different modules on same input (diversity)
  
Loss = -log(sim(f_i(x), f_i(x'))/Σⱼ sim(f_i(x), f_j(x)))
```

**Why This Helps Compositionality:** Forces modules to learn distinct, complementary features that compose well.

**Results:** Better module specialization, improved transfer across tasks.

---

### 3.4 Curriculum Learning for Compositional Structures

**The Idea:** Train on progressively more complex compositions.

---

#### **Compositional Curriculum**

**Paper:** "A Compositional Approach to Language Modeling" (Hupkes et al., 2020)  
**Citation:** https://arxiv.org/abs/2005.14165

**The Training Schedule:**
```
Phase 1: Train on simple compositions (A + B)
Phase 2: Train on nested compositions (A + (B + C))
Phase 3: Train on complex compositions (A + (B + (C + D)))

Gradually increase compositional depth
```

**Results:** Better systematicity, improved out-of-distribution generalization.

---

#### **Automated Curriculum Learning**

**Paper:** "Automatic Curriculum Learning For Deep RL" (Portelas et al., 2020)  
**Citation:** https://arxiv.org/abs/2002.01587

**The Idea:** Let the model choose which compositions to practice.

**The Mechanism:**
```
Measure: Which compositional patterns does the model struggle with?
Sample: Prioritize training on those patterns
Adapt: As model improves, shift curriculum
```

**Application to Architecture:** Train on simpler architectural patterns first, gradually enable more complex compositions.

---

### 3.5 Sparse Training and Lottery Tickets

**The Connection:** If only subsets of compositions matter (lottery tickets), we should train sparsely from the start.

---

#### **Sparse Training from Scratch**

**Paper:** "Training Deep Neural Networks with Joint Optimization of Weights and Connections" (Liu et al., 2019)  
**Citation:** https://arxiv.org/abs/1902.09574

**The Method:**
```
Standard: Train all weights, then prune

Sparse: Start with sparse connectivity, train only non-zero weights

Dynamic: Periodically update which connections are active
```

**Why This Helps Compositionality:** Forces the network to find efficient compositions early, rather than relying on redundancy.

---

#### **Rigged Lottery Tickets**

**Paper:** "The Lottery Ticket Hypothesis at Scale" (Frankle et al., 2021)  
**Citation:** https://arxiv.org/abs/1903.01611

**The Discovery:** Lottery tickets (winning subnetworks) can be identified early in training.

**The Training Strategy:**
```
1. Train for small number of steps (warmup)
2. Identify important connections (high gradient magnitude)
3. Prune unimportant connections
4. Train sparse network to completion

Result: 90% sparsity with same performance
```

**Compositional Insight:** Only certain block connections matter—we can discover them early and focus training there.

---

### 3.6 Multi-Objective Optimization for Components

**The Idea:** Different components should optimize different objectives.

---

#### **Pareto Optimization for Modules**

**Paper:** "Multi-Objective Optimization for Neural Architecture Search" (Chu et al., 2021)  
**Citation:** https://arxiv.org/abs/2103.13841

**The Formulation:**
```
Optimize simultaneously:
  - Accuracy (maximize)
  - Latency (minimize)
  - Parameter count (minimize)
  - Memory (minimize)

Find Pareto frontier of architectures
```

**Application to Composition:**

Different blocks optimize different objectives:
- Early blocks: Efficiency (fast, low-level features)
- Middle blocks: Expressiveness (complex patterns)
- Late blocks: Task-specific (optimize final objective)

**Training:** Use multi-gradient descent to balance objectives across blocks.

---

### 3.7 Continual Learning and Modular Expansion

**The Idea:** As we learn new tasks, add new modules rather than retrain everything.

---

#### **Progressive Neural Networks**

**Paper:** "Progressive Neural Networks" (Rusu et al., 2016)  
**Citation:** https://arxiv.org/abs/1606.04671

**The Approach:**
```
Task 1: Train network N₁
Task 2: Add network N₂, connect to N₁ (N₁ frozen)
Task 3: Add network N₃, connect to N₁, N₂ (N₁, N₂ frozen)

Each new task gets new modules + connections to old modules
```

**The Composition:** Lateral connections between parallel towers.

**Benefits:**
- No catastrophic forgetting (old modules frozen)
- Transfer learning (new modules can use old features)
- Growing capacity (add modules as needed)

**Challenges:**
- Grows linearly with tasks (not scalable)
- Doesn't consolidate (no compression)

---

#### **PackNet: Packing for Continual Learning**

**Paper:** "PackNet: Adding Multiple Tasks to a Single Network by Iterative Pruning" (Mallya & Lazebnik, 2018)  
**Citation:** https://arxiv.org/abs/1711.05769

**The Idea:** Different tasks use different *subsets* of weights.

**The Method:**
```
Task 1: Train full network, prune to 50%
Task 2: Train on remaining 50%, prune to 25%
Task 3: Train on remaining 25%, prune to 12.5%
...

Each task "packs" into disjoint weight subset
```

**Compositional View:** Network capacity can be *partitioned* across tasks/modules.

---

#### **Modular Meta-Learning**

**Paper:** "Modular Meta-Learning with Shrinkage" (Alet et al., 2021)  
**Citation:** https://arxiv.org/abs/2106.04915

**The Training Strategy:**
```
1. Learn library of reusable modules
2. For new task: compose subset of modules
3. Fine-tune composition weights (not module weights)

Meta-objective: Learn modules that compose well
```

**Why This Works:** Encourages learning *compositional primitives* that transfer across tasks.

---

## Part 4: Emerging Training Paradigms

Beyond specific techniques, entirely new training paradigms are emerging.

---

### 4.1 Test-Time Training

**Paper:** "Test-Time Training with Self-Supervision for Generalization under Distribution Shifts" (Sun et al., 2020)  
**Citation:** https://arxiv.org/abs/1909.13231

**The Radical Idea:** Continue training *at inference time* using self-supervised objectives on the test input.

**The Procedure:**
```
Test time:
  1. Receive test input x
  2. Create self-supervised task from x (e.g., rotation, masking)
  3. Do a few gradient steps on this task
  4. Make prediction

The model adapts to each test input!
```

**Why This Matters for Composition:** Modular architectures can selectively update relevant modules at test time without retraining everything.

**Recent Work:**

**Paper:** "Test-Time Training with Masked Autoencoders" (Gandelsman et al., 2022)  
**Citation:** https://arxiv.org/abs/2209.07522

Applies TTT to vision transformers with strong results.

---

### 4.2 Neural Tangent Kernels and Feature Learning

**Paper:** "Neural Tangent Kernel: Convergence and Generalization in Neural Networks" (Jacot et al., 2018)  
**Citation:** https://arxiv.org/abs/1806.07572

**The Theory:** In the infinite-width limit, neural networks behave like kernel methods.

**The Practical Implication:**

**Paper:** "Finite Width Neural Networks of Any Architecture are Gaussian Processes" (Lee et al., 2020)  
**Citation:** https://arxiv.org/abs/2006.14548

**Why This Matters:** Provides theoretical framework for understanding *what compositions can learn*.

**Application to Composition:**

Different block compositions have different NTKs → different learning behaviors. We can design compositions with desired learning properties.

**Paper:** "On the Neural Tangent Kernel of Deep Networks with Orthogonal Initialization" (2020)

Shows specific initializations lead to better-behaved compositions.

---

### 4.3 Forward-Forward Algorithm

**Paper:** "The Forward-Forward Algorithm: Some Preliminary Investigations" (Hinton, 2022)  
**Citation:** https://arxiv.org/abs/2212.13345

**The Revolutionary Idea:** Replace backpropagation with two forward passes.

**The Algorithm:**
```
Positive pass: Real data, maximize layer activations
Negative pass: Corrupted data, minimize layer activations

Each layer learns locally: maximize(good) - minimize(bad)

No backward pass needed!
```

**Why This Matters for Compositionality:**
- Each block trains independently (true modularity)
- No gradient flow between blocks
- Biologically plausible
- Massively parallelizable

**Status:** Very recent, active experimentation. Not yet competitive with backprop, but theoretically interesting.

**Follow-up work:**
- "Forward-Forward Algorithm for Vision Transformers" (2023)
- "Scaling Forward-Forward Algorithm" (2023)

---

### 4.4 Implicit Neural Representations

**Paper:** "Implicit Neural Representations with Periodic Activation Functions" (Sitzmann et al., 2020)  
**Citation:** https://arxiv.org/abs/2006.09661

**The Idea:** Instead of learning discrete weight updates, learn *continuous functions* that represent weights.

**Application: Weight Space Learning**

**Paper:** "Hypernetworks in Meta-Learning" (2023)

Learn a function `θ = f(task_description)` that maps task specifications to optimal weights.

**The Compositional Angle:** Instead of learning compositions of blocks, learn *functions that generate compositions*.

---

### 4.5 Sharpness-Aware Minimization

**Paper:** "Sharpness-Aware Minimization for Efficiently Improving Generalization" (Foret et al., 2021)  
**Citation:** https://arxiv.org/abs/2010.01412

**The Method:**
```
Standard: θ* = argmin Loss(θ)

SAM: θ* = argmin max_||ε||<ρ Loss(θ + ε)

Minimize loss in a neighborhood, not just at a point
```

**Why This Helps Composition:** Finds flatter minima where many similar compositions work well → more robust modular combinations.

**Results:** Significant improvements (2-3%) on vision and language benchmarks.

**Adoption:** Now standard in many SOTA training recipes.

---

## Part 5: Synthesis - The Compositional Training Stack

Putting it all together, here's what a future training pipeline might look like:

---

### The Complete System

```
┌─────────────────────────────────────────────────┐
│ PHASE 1: Component Discovery (Meta-Learning)    │
├─────────────────────────────────────────────────┤
│ - Learn library of primitive blocks             │
│ - Use DARTS/MAML to discover good compositions  │
│ - Test on diverse tasks to ensure generality    │
│                                                 │
│ Output: Library of composable primitives        │
│   {Attention, SSM, KAN, ExternalMemory, ...}   │
└─────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│ PHASE 2: Architecture Composition               │
├─────────────────────────────────────────────────┤
│ - Define composition rules                      │
│   • Residual connections                        │
│   • Cross-attention between blocks              │
│   • MoE routing                                 │
│                                                 │
│ - Use NTK theory to validate compositions       │
│ - Pareto-optimize for compute/accuracy          │
│                                                 │
│ Output: Composed architecture graph             │
└─────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│ PHASE 3: Modular Pre-training                  │
├─────────────────────────────────────────────────┤
│ - Progressive layer training (0→N layers)       │
│ - Contrastive loss between modules              │
│ - Block-wise parallelization where possible     │
│ - SAM for flat minima                           │
│                                                 │
│ Output: Pre-trained modular network             │
└─────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│ PHASE 4: Task-Specific Composition             │
├─────────────────────────────────────────────────┤
│ - Sparse training to find lottery ticket        │
│ - Curriculum learning on task distribution      │
│ - Dynamic routing (MoE, adaptive depth)         │
│ - Test-time training for adaptation             │
│                                                 │
│ Output: Task-optimized model                    │
└─────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│ PHASE 5: Continual Composition                 │
├─────────────────────────────────────────────────┤
│ - Add new modules for new tasks (Progressive)  │
│ - Pack new tasks into spare capacity (PackNet) │
│ - Meta-learn composition policies               │
│                                                 │
│ Output: Growing, compositional system           │
└─────────────────────────────────────────────────┘
```

---

## Part 6: Open Problems and Research Directions

Here are the most important unsolved problems:

---

### 6.1 Theoretical Foundations

**Open Question:** What makes a good compositional primitive?

**What We Need:**
- Theory connecting NTK to composability
- Formal definition of "modularity" in neural networks
- Provable bounds on composition depth vs expressiveness

**Current Work:**
- "On the Principles of Parsimony and Self-Consistency for the Emergence of Intelligence" (2024)
- "A Theory of Compositionality in Deep Learning" (ongoing)

---

### 6.2 Automated Discovery

**Open Question:** Can we discover new primitives automatically?

**What We Need:**
- Meta-learning over operation spaces (not just architecture graphs)
- Evolutionary methods that create novel computational patterns
- Verification that discovered primitives are truly fundamental

**Current Work:**
- AutoML-Zero (Google): Evolve math operations from scratch
- "Discovering Symbolic Models from Deep Learning with Inductive Biases" (2020)

---

### 6.3 Scalable Modular Training

**Open Question:** How do we train trillion-parameter modular systems efficiently?

**What We Need:**
- Better block-wise parallelization
- Asynchronous modular updates
- Theoretical understanding of when modules can train independently

**Current Work:**
- "Pipeline Parallelism for Training Modular Networks" (ongoing)
- "Asynchronous Decentralized Parallel Training" (various groups)

---

### 6.4 Compositionality at Scale

**Open Question:** Do compositional advantages hold at 100B+ parameters?

**What We Need:**
- Empirical studies at scale
- Understanding of how modularity interacts with emergence
- Trade-offs between modularity and raw capacity

**Observations:**
- GPT-4 likely uses MoE (modular)
- Gemini uses mixture of models (modular)
- Suggests modularity helps at scale, but needs validation

---

### 6.5 Biological Plausibility

**Open Question:** Can we make compositional architectures match biological learning?

**What We Need:**
- Alternatives to backprop that respect brain constraints
- Local learning rules that produce global compositionality
- Understanding of how biological