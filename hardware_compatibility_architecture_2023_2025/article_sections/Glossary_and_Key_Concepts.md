# Glossary and Key Concepts

This glossary collects the main acronyms and concepts used across the three Acts and the Appendix, with short but detailed explanations aimed at readers who know modern deep learning but may not live inside LLM infra day-to-day.

---

## Attention and Memory

**Attention (Self-Attention)**  
Mechanism that lets each token in a sequence attend to every other token, computing a weighted sum of their representations. In standard Transformer self-attention, each position produces Query (Q), Key (K), and Value (V) vectors; attention weights are computed as a softmax over Q·Kᵀ and used to mix the V vectors. This gives models flexible, content-based access to the entire context, at the cost of O(n²) memory and compute in the sequence length.

**Multi-Head Attention (MHA)**  
Original Transformer attention variant in which several independent attention “heads” run in parallel, each with its own Q/K/V projections and slightly different focus. Outputs from all heads are concatenated and linearly projected. MHA improves expressiveness but scales memory and compute linearly in the number of heads and quadratically in sequence length.

**Grouped-Query Attention (GQA)**  
An efficient attention variant where many Query heads share a smaller number of Key/Value heads. For example, 8 Query heads might share 1 Key and 1 Value head. This reduces the size of the KV cache (and memory bandwidth) without significantly degrading quality, especially for large models. GQA is a “weight-only” change—no new kernels are required—so it spreads quickly once integrated into a model family.

**Multi-Query Attention (MQA)**  
An earlier efficiency variant in which all Query heads share a single Key and Value head. This maximizes KV sharing but can be less flexible than GQA. Some early Gemini versions used MQA, with later models and other families converging more on GQA-like patterns that balance efficiency and expressiveness.

**Multi-Head Latent Attention (MLA)**  
An attention mechanism introduced by DeepSeek in which the KV cache is projected into a low-rank latent space before being stored. Instead of keeping full-resolution K/V vectors for every token, MLA maintains a compressed latent representation and attends over that; this significantly reduces memory footprint and bandwidth. MLA still uses dense matrix multiplications and fits well on GPUs, but changes the storage and retrieval pattern to support long contexts (e.g., 128K) and large MoE models.

**KV Cache (Key-Value Cache)**  
During autoregressive generation, models cache the Key and Value tensors from previous tokens so they don’t have to recompute them at each step. For long contexts and large models, this cache dominates memory usage—often hundreds of GB at 128K context for 70B+ models if stored naïvely. Techniques like GQA, MLA, and FlashAttention-style kernels largely exist to make the KV cache more manageable.

**FlashAttention**  
An IO-aware attention algorithm that reorders computation to respect GPU memory hierarchies. Instead of materializing the full n×n attention matrix in HBM (off-chip memory), FlashAttention tiles the computation into blocks that fit in SRAM (on-chip cache), computes attention over those blocks, and discards them without ever writing the full matrix to HBM. The result is 2–4× speedups and 10–20× memory savings at long sequences, turning attention from a memory-bound to a compute-bound operation and enabling much longer contexts.

**Sliding-Window Attention (SWA)**  
An attention pattern where each token attends only to a local window of nearby tokens, rather than the entire sequence. This reduces the effective complexity from O(n²) to roughly O(n·w), where w is the window size, and is useful for long contexts where many long-range interactions are unnecessary. Mistral 7B is a canonical example of GQA + SWA in production.

**Sparse Attention / DeepSeek Sparse Attention (DSA)**  
Sparse attention restricts which positions can attend to which others, either via fixed patterns (e.g., blocks, dilations) or learned structures, to reduce computation and memory. DeepSeek’s DSA is a specific form of sparse attention that reduces complexity from O(L²) to O(L·k) by attending only to selected key positions, enabling long contexts (e.g., 128K) in V3.2 with more predictable memory use.

**RoPE (Rotary Position Embeddings)**  
A positional encoding method that rotates query/key vectors in a way that encodes relative positions while preserving certain algebraic properties of the dot product. RoPE supports extrapolation to longer contexts and has become a de facto standard in modern LLMs (Llama, Mistral, Qwen, etc.).

---

## Mixture-of-Experts and Conditional Execution

**Mixture-of-Experts (MoE)**  
An architectural pattern in which certain layers (usually the feed-forward / MLP blocks) contain multiple “experts,” and a small router network selects a subset of experts (e.g., top-1 or top-2) for each token. This makes the layer’s parameters “sparse”: the total parameter count can be very large, but only a small fraction is active per token. MoE is a form of conditional execution—different tokens route to different compute paths—enabling large capacity at lower per-token compute cost, at the price of more complex training and serving.

**Experts and Router**  
In MoE, each expert is usually a feed-forward network (FFN) or similar module. A router (often a small linear layer per token) produces a distribution over experts, and a sparse selection (top-k or expert-choice) determines which experts process each token. Good routing is crucial for performance and load-balancing; poor routing leads to “collapsed experts” and low utilization.

**Conditional Execution**  
An umbrella term for mechanisms that allow the model to dynamically select which computations or parameters to use, conditioned on the input or context. This includes:
- Hard routing (MoE): token → expert selection.
- Soft routing (attention): token → weighted combination of other tokens.
- Structured sparsity (sparse attention, SWA): token → subset of positions computed.
- Task-conditional parameters (LoRA/adapters): task → which low-rank parameter additions are active.
Conditional execution is central to scaling capacity without uniformly increasing compute for every token.

**FasterMoE / Aurora / MoE System Stacks**  
System-level implementations and optimizations for serving MoE models efficiently. These frameworks design block-sparse kernels, expert sharding strategies, and communication patterns to keep GPUs well utilized. They are a key part of why MoE became practical in production: without efficient system support, MoE can be 3–15× slower than dense models despite fewer active parameters.

---

## State Space Models (SSMs) and Mamba

**State Space Models (SSMs)**  
Models that represent sequences via latent “state” variables evolving over time according to linear or nonlinear state-space equations. Instead of attending over the full sequence, SSMs update a recurrent hidden state as tokens come in, offering nominal O(n) complexity and fixed memory in sequence length. In practice, they can be very efficient for certain long-sequence tasks but have historically struggled with in-context learning and arbitrary long-range interactions compared to attention.

**Mamba**  
A specific SSM variant that introduces “selective state spaces”—mechanisms that allow the model to dynamically control which parts of the state get updated. Mamba and its variants have shown strong efficiency and competitive performance at small-to-medium scales (up to 7B), including Falcon Mamba 7B. However, as of late 2025, no pure Mamba model has been publicly demonstrated at 13B+ or frontier scale; above 7B, SSM-style blocks mainly appear inside hybrids with attention.

**Hybrid SSM+Attention Architectures (Jamba, Falcon-H1, Qwen3-Next)**  
Architectures that mix SSM-like blocks with attention layers to get the best of both worlds: SSMs for efficient local/sequential processing and attention for flexible global dependencies and in-context learning. Examples include:
- Jamba: Alternating Mamba and attention layers.
- Falcon-H1: Parallel mixtures of Mamba2-like and attention components.
- Qwen3-Next: Linear attention (e.g., Gated DeltaNet) + gated attention + MoE.  
These hybrids show how SSMs can be powerful components without replacing attention outright.

---

## Optimization, Training, and RL

**SAM (Sharpness-Aware Minimization)**  
An optimization technique that modifies the gradient update to favor flatter regions of the loss landscape. Instead of minimizing the loss at the current parameters, SAM approximately minimizes the worst-case loss within a small neighborhood in parameter space. This tends to produce models that generalize better and are more robust, at modest additional compute cost. In the LLM context, SAM has been used as a drop-in optimizer improvement in some large training runs.

**Progressive Depth / Curriculum Training**  
A training strategy in which models start training with shallower networks (fewer layers) and progressively increase depth as training progresses, or gradually “unfreeze” deeper layers. This can lead to faster convergence—often ≈10–20% wall-clock savings compared to training a full-deep network from scratch—while reaching similar or better final performance. It is a training-level innovation that leverages the same architecture more efficiently.

**Routing-Aware Optimization (for MoE)**  
Training methods that explicitly optimize the MoE router and expert usage: auxiliary losses to balance load, penalties for collapsed experts, and specialized temperature schedules or regularizers. These methods improve expert utilization and stability, which in turn improves effective throughput and quality. ST-MoE-style work and DeepSeek’s MoE stacks are examples of routing-aware optimization in action.

**GRPO (Group Relative Policy Optimization)**  
A reinforcement learning algorithm used in DeepSeek-R1, among others, to train reasoning behavior. GRPO is a variant of policy gradient methods that compares performance across groups of trajectories, focusing updates on relatively better reasoning chains. It allows the model to discover multi-step reasoning strategies by rewarding useful trajectories, even when supervised labels are sparse or noisy.

---

## Retrieval and Memory-Augmented Methods

**RAG (Retrieval-Augmented Generation)**  
A design pattern in which a language model is paired with an external retrieval system (often a vector database or search index). At query time, relevant documents or snippets are retrieved based on the input, and those retrieved chunks are fed into the model’s context. This effectively gives the model access to a much larger “memory” than its fixed context window, without changing its architecture: the GPU still runs the same Transformer-style computations, but over retrieved text instead of a monolithic long prompt.

---

## Infrastructure and Hardware

**GPU Primitives / Tensor Cores**  
Modern GPUs (e.g., NVIDIA A100/H100) are optimized around dense matrix multiplications (GEMMs) and tensor-core operations. A “hardware-compatible” neural primitive is one that can be implemented as regular, batched GEMMs that keep tensor cores busy. Operations that require irregular scatter/gather, small non-vectorized ops, or sequential dependencies tend to underutilize the hardware and are harder to scale.

**HBM and SRAM (Memory Hierarchy)**  
HBM (High Bandwidth Memory) is large but slower off-chip memory on GPUs, while SRAM (on-chip cache/registers) is small but extremely fast. Efficient kernels minimize data movement between HBM and SRAM by reusing data in SRAM as much as possible. Both FlashAttention and MLA are designed explicitly around this hierarchy.

**Block-Sparse Operations**  
Sparse computations where nonzero elements cluster in blocks rather than arbitrary positions, making them amenable to efficient GPU implementations. MoE and many sparse attention variants are implemented as block-sparse matmuls to preserve parallelism and compatibility with GPU primitives.

---

## Other Architectures and Research Directions

**KANs (Kolmogorov-Arnold Networks)**  
Architectures that replace standard linear layers and fixed activations with spline-based, learnable functions on edges, motivated by Kolmogorov-Arnold representation theorems. They offer a more flexible function class in principle but involve spline evaluations that do not map cleanly to dense GEMMs, making them less hardware-friendly. As of 2023–2025, KANs have generated research interest and hype but have not been demonstrated at frontier LLM scale.

**Neural ODEs (Neural Ordinary Differential Equations)**  
Models that interpret layer depth as a continuous variable and use ODE solvers to evolve hidden states. This offers theoretical elegance and continuous-depth flexibility, but ODE solvers are iterative and sequential, conflicting with GPUs’ need for large, regular batches of parallel work. Neural ODEs have influenced theory and some niche applications but have not become a mainstream architecture for large-scale LLMs.

**Capsule Networks**  
Architectures that group neurons into “capsules” and use routing-by-agreement mechanisms to decide how lower-level capsules contribute to higher-level ones. They aim to capture part-whole relationships and invariant representations. However, the routing logic is prescriptive and computationally heavy, and despite early excitement, capsule networks have not been adopted in large-scale production LLMs; they mostly remain a historical example of a compositional idea that did not cross the infra chasm.
