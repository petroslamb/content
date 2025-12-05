# Act II: The Conditional Execution Revolution
*How learned routing became a first-class primitive*

The defining shift of 2023–2025 was not a new layer type. It was a change in the fundamental contract of computation. In the previous era, neural networks were static graphs: every input token triggered the exact same sequence of floating-point operations. In the current era, computation is **conditional**—the model learns *where* to spend compute, not just *what* layers exist.

This isn't just about Mixture-of-Experts (MoE). It is a convergence across attention, routing, and adaptation. The architecture increasingly specifies *how to choose* what to compute for a given token, task, or context.

### 1. The Conditional Execution Convergence

If we look closely at the successful techniques of the last two years, a unifying pattern emerges: they all introduce some form of *learned selectivity* over compute or parameters:

*   **MoE:** "Which expert processes this token?" (hard routing of tokens to expert FFNs).
*   **Attention:** "Which previous tokens influence this output?" (soft routing of influence over a dense attention kernel).
*   **Sparse Patterns:** "Which positions matter?" (structured masking that skips compute for parts of the sequence).
*   **LoRA / adapters:** "Which low-rank subspace adapts for this task?" (task-conditional parameter additions, not token-time routing).

These are not identical mechanisms, but they share a common composition operator: **conditional execution**. Some (like MoE and sparse attention) route tokens or positions to different compute paths at runtime; others (like LoRA) condition *which parameters* are active for a given task or domain.

Why did this happen now? Because GPU infrastructure finally matured to support it at scale. For years, "sparsity" was a dirty word in high-performance computing because it meant irregular memory access and thread divergence—two things GPUs hate. But with the arrival of specialized kernels and serving stacks for block-sparse operations (e.g., Triton/MegaBlocks-style MoE kernels, FasterMoE, Aurora, FlashInfer, and MoE-aware DeepSpeed/Megatron/FasterTransformer), the penalty for conditional execution dropped below the capacity and throughput gains it unlocks (Appendix, Table 2).

The thesis of Act II is simple: **Conditional execution is to the 2020s what residual connections were to the 2010s—the composition operator that enables the next order of magnitude in scaling.**

### 2. MoE: The Production Validation

For years, Mixture-of-Experts was the "technology of the future"—from Shazeer et al.'s sparsely-gated MoE (2017) through Switch Transformers (Fedus et al., 2021) and GLaM (Du et al., 2021)—always promising, but difficult to train and painful to serve. In 2024–2025, that future finally arrived. MoE is no longer an exotic research trick; it has become one of the primary strategies for scaling frontier models, especially when total parameter counts exceed what dense training and serving can economically support (Appendix, Table 1).

**The Honest Numbers:**
Let's strip away the marketing claims. Vendors often promise "5–7× speedups" with MoE. The reality, based on a meta-analysis of production-style deployments and system papers, is more grounded but still transformative (Appendix, Table 2):
*   **Realistic Inference Speedup:** **≈2–3×** throughput compared to dense models of similar quality at moderate context, with a median around **2.1–2.5×** in our aggregated studies.
*   **The Mechanism:** A model like DeepSeek-V3 (671B parameters) activates only 37B parameters per token. It delivers the intelligence of a massive model with the latency of a small one.

**The Evidence:**
The list of successes is now long and growing. A few representative examples:
*   **DeepSeek-V3 (Dec 2024):** 671B total, 37B active (DeepSeek-AI, 2024). A masterclass in load balancing and MoE + MLA design.
*   **DeepSeek-R1 (Jan 2025):** 671B/37B MoE + MLA reasoning model with state-of-the-art math scores (DeepSeek-AI, 2025).
*   **Mixtral-8×7B:** The model from Mistral AI (2023) that proved open-weights MoE could match or beat GPT-3.5-class systems on many benchmarks.
*   **Grok-1:** 314B parameters, confirming MoE works at massive scale without fine-tuning, in an open checkpoint (xAI, 2023–2024).

**The Narrative Climax: The Meta Pivot**
The clearest public signal of MoE's arrival came in April 2025. Until then, Meta had pushed dense scaling hard—Llama 3.1's 405B dense model was a monument to that strategy. With **Llama 4**, Meta introduced its first MoE family:
*   **Llama 4 Scout:** 109B total, 17B active (16 experts).
*   **Llama 4 Maverick:** 400B total, 17B active (128 experts).

Meta's pivot does not mean dense models are obsolete—dense Llama variants and many closed models still exist—but it is a strong signal that at frontier scale, MoE is now considered a first-class option rather than a risky experiment (Appendix, Table 1). The Dense Era has not ended, but it now shares the stage with sparse, conditionally-executed capacity.

### 3. The Context-Length Trap

However, A+++ analysis requires nuance. MoE is not a magic bullet. While it addresses the compute bottleneck, it introduces a new, often overlooked vulnerability: **The Context-Length Trap**.

Our analysis of inference performance across 18 MoE sources reveals a consistent degradation in effective throughput as context length increases (Extended Dataset 1; qualitatively summarized in Appendix, Table 2).
*   **At short context (≈128 tokens):** Well-engineered MoE often delivers its best-case speedups, with throughput peaks around our "≈2–3×" range versus dense baselines.
*   **At medium context (1–2K tokens):** Throughput erodes; in our aggregated context-length study, performance at 2,048 tokens is roughly **30% lower** than at 128 tokens.
*   **At long context (32K+ tokens):** Standard MoE implementations can struggle significantly; the effective advantage shrinks toward **≈1.3–1.5×** vs dense as KV/cache traffic and routing overhead dominate (Appendix, Table 2).

**The Mechanism:** MoE routing requires loading expert weights from HBM to SRAM. As context length grows, the batch size of tokens assigned to each expert fluctuates, leading to memory fragmentation and inefficient memory bandwidth usage. The "sparse" advantage evaporates when the system spends more time moving weights than computing attentions.

This explains why MoE wins on *throughput* (tokens per second) but fights on *context* (memory bandwidth). It is a trade-off, not a pure upgrade.

### 4. Hybrid Architectures: Principled Heterogeneity

To solve the Context-Length Trap, we are seeing the emergence of **Hybrid Architectures**.

**Qwen3-Next** is the prime example. It doesn't use just one primitive. It uses a three-dimensional hybrid approach:
1.  **Linear Attention** for the infinite context backbone.
2.  **Gated Attention** for high-fidelity retrieval.
3.  **MoE** for feed-forward capacity.

**The Principle:** Route computation to the primitive that handles it best.
*   **SSM/Linear:** Handles local, sequential dependencies (efficient).
*   **Attention:** Handles global, arbitrary dependencies (expressive).
*   **MoE:** Handles knowledge storage and reasoning (capacity).

While elegant, hybrids remain niche. The complexity cost of maintaining three different inference kernels usually outweighs the benefits for general-purpose models. Today, they are the solution for extreme requirements (256K+ contexts and ultra-long workflows), not yet the default for general reasoning.

### 5. What Didn't Work: The Failure Mechanism

To understand why conditional execution won, we must look at what failed.

**Neural ODEs (2018):** Promised continuous depth and infinite adaptability.
*   **Why they struggled:** ODE solvers are iterative and sequential. They fight the GPU's need for massive, predictable parallelism. They won Best Paper at NeurIPS, influenced theory, and saw use in niche domains—but in our survey we find no evidence of large-scale production adoption for LLM-style workloads.

**Capsule Networks:** Proposed "routing-by-agreement" to solve spatial hierarchies.
*   **Why they struggled:** The routing logic was **prescriptive**. It tried to enforce a specific structure (capsules) rather than creating a permissive space for the model to learn its own structure. Despite a burst of research interest, we again find no evidence that capsule-style routing became a pattern in large-scale production models.

**The Lesson:** Compositionality that survives is **permissive**, not **prescriptive**. MoE provides a pool of experts and a router, but it doesn't tell the model *what* the experts should be. It lets gradient descent discover the structure. Capsule Networks and Neural ODEs tried to design the structure explicitly, and they did not cross the production chasm.

**Act II Synthesis:**
Conditional execution won because it is the most general way to scale capacity without worsening the compute constraint. It maps to the GPU's ability to handle block-sparse operations and conditional parameter usage. Llama 4's pivot confirms MoE as a standard frontier tool, not just a research prototype. But the Context-Length Trap reminds us that every architectural choice is a trade-off.

In Act III, we will explore the final piece of the puzzle: why these transitions take so long, and where the field goes next.
