# Act II: The Conditional Execution Revolution
*How learned routing became a first-class primitive*

The defining shift of 2023–2025 was not a new layer type. It was a change in the fundamental contract of computation. In the previous era, neural networks were static graphs: every input token triggered the exact same sequence of floating-point operations. In the current era, computation is **conditional**.

This isn't just about Mixture-of-Experts (MoE). It is a convergence across attention, routing, and adaptation. The architecture no longer specifies *what* to compute; it specifies *how to choose* what to compute.

### 1. The Conditional Execution Convergence

If we look closely at the successful techniques of the last two years, a unifying pattern emerges. They are all forms of learned routing:

*   **MoE:** "Which expert processes this token?"
*   **Attention:** "Which previous tokens influence this output?"
*   **Sparse Patterns:** "Which positions matter?"
*   **LoRA:** "Which low-rank subspace adapts for this task?"

These are not distinct techniques; they are manifestations of the same composition operator: **conditional execution**.

Why did this happen now? Because GPU infrastructure finally matured to support it. For years, "sparsity" was a dirty word in high-performance computing because it meant irregular memory access and thread divergence—two things GPUs hate. But with the arrival of specialized kernels (like those in Triton and CUTLASS) and hardware support for block-sparse operations, the penalty for conditional execution dropped below the gain from increased capacity.

The thesis of Act II is simple: **Conditional execution is to the 2020s what residual connections were to the 2010s—the composition operator that enables the next order of magnitude in scaling.**

### 2. MoE: The Production Validation

For years, Mixture-of-Experts was the "technology of the future"—always promising, but difficult to train and impossible to serve. In 2024, that future arrived. MoE is no longer experimental; it is the standard for frontier scaling.

**The Honest Numbers:**
Let's strip away the marketing claims. Vendors often promise "5–7× speedups" with MoE. The reality, based on a meta-analysis of production deployments, is more grounded but still transformative:
*   **Realistic Inference Speedup:** **≈2–3×** throughput compared to dense models of similar quality, with a median around **2.1–2.5×** at 128K context.
*   **The Mechanism:** A model like DeepSeek-V3 (671B parameters) activates only 37B parameters per token. It delivers the intelligence of a massive model with the latency of a small one.

**The Evidence:**
The list of successes is exhaustive:
*   **DeepSeek-V3 (Dec 2024):** 671B total, 37B active. A masterclass in load balancing.
*   **Mixtral-8×7B:** The model that proved open-weights MoE could match GPT-3.5.
*   **Grok-1:** 314B parameters, proving MoE works at massive scale without fine-tuning.

**The Narrative Climax: The Meta Pivot**
The definitive proof of the MoE victory came in April 2025. For years, Meta was the staunchest defender of dense scaling. Llama 3 (405B) was a dense monolith, pushing the limits of what could be trained on a single cluster.

But physics wins. With **Llama 4**, Meta capitulated.
*   **Llama 4 Scout:** 109B total, 17B active (16 experts).
*   **Llama 4 Maverick:** 400B total, 17B active (128 experts).

When the strongest critic of an architecture adopts it for their flagship product, the debate is over. The Dense Era has ended.

### 3. The Context-Length Trap

However, A+++ analysis requires nuance. MoE is not a magic bullet. While it solves the compute bottleneck, it introduces a new, often overlooked vulnerability: **The Context-Length Trap**.

Our analysis of inference performance reveals a quadratic degradation in MoE throughput as context length increases.
*   **At 128 tokens:** MoE shines, delivering 30% higher throughput than baseline.
*   **At 2,048 tokens:** Performance drops by 30%.
*   **At 32K+ tokens:** Standard MoE implementations struggle significantly.

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

While elegant, hybrids remain niche. The complexity cost of maintaining three different inference kernels usually outweighs the benefits for general-purpose models. They are the solution for extreme requirements (256K+ contexts), not the default for general reasoning.

### 5. What Didn't Work: The Failure Mechanism

To understand why conditional execution won, we must look at what failed.

**Neural ODEs (2018):** Promised continuous depth and infinite adaptability.
*   **Why it failed:** ODE solvers are iterative and sequential. They fight the GPU's need for massive, predictable parallelism. Won Best Paper at NeurIPS; dead in production by 2021.

**Capsule Networks:** Proposed "routing-by-agreement" to solve spatial hierarchies.
*   **Why it failed:** The routing logic was **prescriptive**. It tried to enforce a specific structure (capsules) rather than creating a permissive space for the model to learn its own structure.

**The Lesson:** Compositionality that survives is **permissive**, not **prescriptive**. MoE provides a pool of experts and a router, but it doesn't tell the model *what* the experts should be. It lets gradient descent discover the structure. Capsule Networks tried to design the structure, and they failed.

**Act II Synthesis:**
Conditional execution won because it is the most general way to scale capacity without worsening the compute constraint. It maps to the GPU's ability to handle block-sparse operations. Llama 4's pivot confirms it is the standard. But the Context-Length Trap reminds us that every architectural choice is a trade-off.

In Act III, we will explore the final piece of the puzzle: why these transitions take so long, and where the field goes next.
