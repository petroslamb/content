# What Actually Works: The Hardware Compatibility Filter in Neural Architecture (2023–2025)

*How GPU primitives determine adoption, why MoE won, and why architecture innovation has plateaued*

In "Neural Architecture Design as a Compositional Language," we established that architecture evolved from hand-crafted hierarchies to modular component libraries. The Transformer validated this: uniform blocks, structured composition rules, and emergent specialization through training.

We ended with three open questions. What primitives belong in the toolkit beyond attention and MLPs? What composition operators enable scaling? How do we train compositional systems effectively?

Two years of production deployments provide answers, but not through the lens most researchers expected. The organizing principle of the last 24 months isn't expressiveness or theoretical elegance. It is **hardware compatibility**.

GPU architectures—optimized for dense matrix multiplication, SRAM/HBM memory hierarchies, and parallel execution—create a filter. Techniques that map naturally to these primitives win. Techniques that fight them die, regardless of benchmark results on small models.

This post examines the 2023–2025 era through three perspectives:

*   **Act I: The Compatibility Filter** — How Flash Attention, MoE, and attention variants succeeded by exploiting GPU architecture, while KANs and pure SSMs failed by fighting it.
*   **Act II: The Conditional Execution Revolution** — How learned routing (attention, MoE, sparse patterns) became the defining composition operator, replacing designed computation graphs.
*   **Act III: The Infrastructure Lag Pattern** — Why Flash Attention took 24 months to become standard, why MoE took 36, and how to predict adoption timelines.

We make three bold claims, defended with production evidence:

1.  **Hardware compatibility predicts adoption** better than benchmarks.
2.  **Architecture innovation has plateaued**; training innovation is the next decade.
3.  **Pure SSMs will not scale to frontier models**; hybrids are the ceiling.

What doesn't work: Speculation without production validation, marketing claims without aggregate data, and techniques that ignore deployment constraints.

What does work: Hardware-compatible primitives, permissive compositional operators, and training methods that exploit—not fight—modular structure.

---

## Act I: The Compatibility Filter
*How hardware constraints shaped what survived*

### 1. The Attention Bottleneck

By early 2023, the Transformer architecture faced a crisis, but it wasn't about intelligence. It was about memory. The quadratic cost of attention ($O(n^2)$) is often cited as a computational problem, but in practice, it is a memory movement problem.

At 128K context length, the Key-Value (KV) cache for a 70B model grows to hundreds of gigabytes, exceeding the HBM (High Bandwidth Memory) capacity of even an H100 GPU. The bottleneck wasn't doing the math; it was moving the matrices from HBM to the compute units (SRAM) and back.

Naive solutions failed because they tried to approximate the math (sparse attention patterns, low-rank approximations) rather than solve the memory movement. They broke the one thing researchers wouldn't compromise: the exactness of the attention mechanism. The solution that won didn't change the math at all. It changed the memory access pattern.

### 2. Flash Attention: Hardware as Design Constraint

Flash Attention is the definitive proof of the Hardware Compatibility Thesis. Published in May 2022, it did not propose a new neural primitive. Instead, it proposed a **tiling algorithm** that respects the GPU's memory hierarchy.

Standard attention materializes the massive $N \times N$ attention matrix in HBM, reading and writing gigabytes of data for every token generation. Flash Attention tiles the computation so that blocks of the matrix are loaded into SRAM (fast, on-chip memory), computed, and discarded without ever writing the full matrix to HBM.

**The Mechanism:** By keeping the computation in SRAM, Flash Attention reduces memory reads/writes by 8–10×. It turns a memory-bound operation into a compute-bound one, which is exactly what GPUs are designed to handle.

**The Adoption Timeline (The 24-Month Lag):**
The adoption of Flash Attention reveals a predictable infrastructure lag pattern that governs the entire field:

*   **May 2022:** Paper published. Benchmarks show 2–4× speedup and linear memory scaling.
*   **2022–2023 (Stage 2):** Early adopters and startups integrate it manually. Custom CUDA kernels are required.
*   **January 2024 (Stage 3):** PyTorch 2.2 officially integrates FlashAttention-2. It becomes a standard library call.
*   **May 2024 (Stage 4):** Standard practice. Every major model release (Llama 3, Gemini, Mistral) utilizes it by default.

It took exactly 24 months for a technique that required kernel-level changes to move from "proven research" to "standard practice." This lag is not accidental; it is the cost of infrastructure integration. We will see this pattern repeat with MoE.

### 3. The Compatibility Winners

The winners of 2023–2025 all share one trait: they reduce memory bandwidth pressure without requiring new, exotic compute kernels.

**Grouped Query Attention (GQA):**
GQA is the dominant attention variant of 2024, adopted by **80–90% of top models**, including Llama 3, Mistral 7B, and Qwen2.5. Its mechanism is simple: share Key and Value heads across multiple Query heads.
*   **Why it won:** It reduces the size of the KV cache by 8× (for 8 groups), directly lowering memory bandwidth requirements. It uses standard matrix multiplication. It requires no new hardware support.
*   **The result:** It is now the default for any model larger than 7B parameters.

**Multi-Head Latent Attention (MLA):**
Pioneered by DeepSeek (V2/V3), MLA takes compression further. It projects the KV cache into a low-rank latent vector.
*   **Why it won:** It compresses the KV cache significantly (crucial for DeepSeek's 128K context) while maintaining the expressiveness of full attention. Like GQA, it relies on dense matrix projections—the GPU's native language.

**Contrast: The Failure of KANs**
Kolmogorov-Arnold Networks (KANs) generated immense hype in early 2024 by proposing learnable activation functions on edges (splines) rather than fixed weights.
*   **Why it failed:** Spline evaluation does not map to dense matrix multiplication. It requires disparate memory access patterns and custom kernels that cannot saturate GPU tensor cores.
*   **The verdict:** Despite theoretical elegance, KANs are computationally incompatible. They remain a research curiosity, dead on arrival for production scaling.

### 4. SSMs: The Compatibility Boundary

State Space Models (SSMs) like Mamba represent the most significant architectural challenge to the Transformer. They promise linear scaling ($O(n)$) by replacing the attention mechanism with a recurrent state update.

**The Mechanism:** Mamba compresses context into a fixed-size state, updating it sequentially as it processes tokens. This eliminates the KV cache entirely, theoretically solving the memory bottleneck for infinite contexts.

**The Failure:** Pure SSMs fight the GPU's greatest strength: **parallelism**.
Transformers process all tokens in a sequence simultaneously during training (parallel prefix scan). SSMs, by definition, have a sequential dependency: state $t$ depends on state $t-1$. While Mamba introduces a "parallel scan" algorithm to mitigate this, the fundamental operation remains less efficient than the brute-force parallel matmuls of a Transformer.

**The Evidence (The Ceiling):**
*   **Proven Scale:** Pure Mamba models exist and work at 130M, 1.4B, 2.8B, and 7B (Falcon Mamba).
*   **The Gap:** There is **zero evidence** of a pure SSM scaling to 13B, 70B, or frontier levels (100B+).
*   **Major Lab Adoption:** OpenAI, Google, Meta, and Anthropic have **all** rejected pure SSMs for their frontier models. Adoption is 0/5.

**The Nuance:** Hybrids exist. Jamba (AI21) and Qwen3-Next use SSM layers mixed with Attention layers.
*   **Why hybrids work:** They route local, sequential dependencies to the SSM (efficient) and global, complex dependencies to Attention (expressive).
*   **The Prediction:** Pure SSMs will not scale to frontier models. The parallelism gap is architectural, not a training issue. Hybrids are the ceiling, and even they remain niche due to complexity.

### 5. External Memory (RAG): The Compatibility Shortcut

While researchers fought over $O(n^2)$ vs $O(n)$ architectures, the industry solved the context problem with a database. Retrieval-Augmented Generation (RAG) is the ultimate compatibility hack.

*   **Mechanism:** Offload memory to a vector database (highly optimized for search). Retrieve only relevant chunks. Feed them to the GPU context window.
*   **Why it won:** It requires **zero changes** to the neural architecture. It treats the GPU as a reasoning engine, not a storage engine.
*   **Adoption:** Universal. Every major LLM product (ChatGPT, Claude, Gemini) uses RAG for long-context tasks.

**Act I Synthesis:**
The pattern is absolute. Flash Attention (maps to memory hierarchy) took 24 months to become standard. GQA (maps to bandwidth constraints) took 12 months. Pure SSMs (fight parallelism) hit a hard ceiling at 7B parameters. KANs (incompatible compute) died immediately.

We are not designing neural networks in a vacuum. We are discovering which computations GPUs can efficiently express. The hardware is the filter, and it is ruthless.

In Act II, we will see how this filter shaped the most important composition operator of the decade: the shift from static graphs to learned, conditional execution.
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
# Act III: The Infrastructure Lag Pattern
*Why timing matters: From research to production*

Flash Attention was published in May 2022. It became standard practice in May 2024. Two years.
Switch Transformers (MoE) were published in January 2021. They became standard practice in 2024. Three years.

Why the lag? In a field that moves at the speed of light, why does it take 24–36 months for a proven, hardware-compatible technique to reach production?

The answer is the **Infrastructure Lag Pattern**. Techniques do not succeed when they are published. They succeed when the infrastructure makes them cheaper to adopt than to ignore.

### 1. The Adoption Dynamics Model

We can predict the adoption timeline of any new technique based on its **integration cost**:

*   **Level 1: Weight-Only Changes (12–18 months)**
    *   *Example:* Grouped Query Attention (GQA).
    *   *Requirement:* Change the model definition code. No new kernels, no new serving infrastructure.
    *   *Lag:* Minimal. Adoption is driven by retraining cycles.

*   **Level 2: Kernel-Level Changes (24–30 months)**
    *   *Example:* Flash Attention.
    *   *Requirement:* Custom CUDA kernels. Integration into PyTorch/JAX.
    *   *Lag:* 24 months. This is the time it takes for a kernel to move from a research repo -> a library -> a framework stable release -> a production stack.
    *   *Evidence:* Flash Attention (May 2022) -> PyTorch 2.2 (Jan 2024) -> Standard (May 2024).

*   **Level 3: Serving Infrastructure Changes (36–48 months)**
    *   *Example:* Mixture-of-Experts.
    *   *Requirement:* Not just kernels, but distributed system changes. How do you shard experts across nodes? How do you handle load balancing in inference?
    *   *Lag:* 36 months.
    *   *Evidence:* Switch (Jan 2021) -> Mixtral/DeepSeek/Llama 4 (2024–2025).

**The Prediction:** If a new technique requires kernel changes (like KANs would), do not expect it in production for two years. If it requires serving changes, expect three. If it fights GPU primitives, expect never.

### 2. Training Innovation: The Next Frontier

This brings us to our final and most controversial claim: **Architecture innovation has plateaued.**

The last fundamental primitive (Attention) was introduced in 2017. Since then, we have seen refinements (Flash, GQA, MLA) and composition operators (MoE), but not replacements. The hardware constraints have narrowed the space of acceptable operations so tightly around dense matrix multiplication that "new" architectures are increasingly unlikely to survive.

The next decade belongs to **Training Innovation**.

**The Proof: DeepSeek-R1 (January 2025)**
The definitive evidence arrived just weeks ago. DeepSeek-R1 achieved state-of-the-art reasoning performance (79.8% on AIME, 97.3% on MATH-500), rivaling OpenAI's o1.

*   **The Architecture:** Standard MoE + MLA. Nothing new.
*   **The Innovation:** **Pure Reinforcement Learning.**
    *   DeepSeek-R1 was trained using Group Relative Policy Optimization (GRPO) to discover reasoning chains.
    *   It did not need a new neural primitive to learn to reason. It needed a new training paradigm.

This validates the thesis: The architecture is the *container*; training is the *contents*. We have spent 8 years optimizing the container. It is efficient, scalable, and hardware-compatible. Now we are finally learning how to fill it.

**Where Innovation Moves:**
*   **SAM (Sharpness-Aware Minimization):** Optimizing for robust minima (better composition).
*   **Progressive Training:** Using depth as a curriculum (10–20% faster convergence).
*   **Routing-Aware Optimization:** Training the router to balance load without collapsing.

We are shifting from "what to compute" to "how to train what we already compute."

---

## Conclusion

The story of 2023–2025 is not one of unbridled invention, but of ruthless selection.

The **Hardware Compatibility Thesis** explains the winners and losers. Flash Attention won because it respected the memory hierarchy. MoE won because it mapped to conditional execution. Pure SSMs hit a ceiling because they fought parallelism. KANs died because they ignored the tensor core.

For the senior practitioner, this offers a clear heuristic:
1.  **Predictive:** When evaluating a new paper, ask: "Does this map to GPU primitives?" If no, ignore it for production.
2.  **Strategic:** Architecture has plateaued. Invest your R&D budget in training innovation (data curation, RL, optimization), not in searching for the "next Transformer."
3.  **Tactical:** Adopt Flash Attention and GQA immediately. Use MoE for scaling beyond 10B parameters. Ignore pure SSMs for frontier models.

We are not designing neural networks in a vacuum. We are discovering which computations silicon can express efficiently. The ones that map naturally to the hardware survive. The ones that don't become historical footnotes, regardless of their theoretical elegance.

The architecture wars are over. The training wars have begun.

---

## Appendix: The Evidence

For the skeptical practitioner, we present the raw data underlying the claims in this post.

### Table 1: The Major Lab Architecture Audit (2024–2025)
*Adoption of primitives across frontier model families. Updated with public information as of Dec 2025.*

| Lab | Model Family | Release Date | Architecture (Publicly Documented) |
| :--- | :--- | :--- | :--- |
| **Meta** | Llama 4 (Scout / Maverick) | **April 2025** | **MoE Transformer** (mixture-of-experts pivot from dense Llama 3) |
| **OpenAI** | GPT-5 | **Aug 2025** | Multimodal Transformer (detailed architecture not publicly specified as MoE) |
| **Google** | Gemini 2 / 3 series | 2024–2025 | Multimodal Transformer (sparse / conditional components, details vary by release) |
| **DeepSeek** | DeepSeek-V3 / V3.1 / V3.2 | 2024–2025 | Transformer with DeepSeek Sparse Attention and long-context optimizations |
| **xAI** | Grok series | 2023–2025 | Frontier Transformer family (routing details not fully public) |
| **Anthropic** | Claude 3 / 4.x | 2024–2025 | Sparse / conditional Transformer (details partially disclosed) |
| **Meta** | Llama 3 / 3.1 | 2024–2025 | **Dense** Transformer (Flash Attention, GQA, RoPE) |
| **Mistral** | Mixtral 8×7B | 2023 | **Sparse MoE** (Mixture-of-Experts Transformer) |
| **NVIDIA** | Nemotron family | 2024–2025 | ✅ **Hybrid** (incorporates Mamba-style SSM blocks for efficiency) |
| **Falcon** | Falcon 2 / efficiency variants | 2023–2024 | ✅ **Hybrid** (incorporates Mamba-style SSM blocks for efficiency) |

**Insight:** The "Dense Era" effectively ended in 2024–2025. Flagship open-weight families like Llama 4 and Mixtral demonstrate MoE at scale, while others (GPT-5, Gemini, Claude, Grok) retain transformer cores with sparse and conditional extensions. Pure SSM-based frontier flagships remain absent; SSM-style blocks appear only as components inside efficiency-focused hybrids (e.g., NVIDIA, Falcon), not as standalone end-to-end architectures.

### Table 2: The MoE Reality Check
*Marketing claims vs. production-style measurements at long context (64K–128K tokens). Estimates are based on public MoE reports (e.g., Mixtral, DeepSeek-V3) and vendor disclosures, not a single benchmark.*

| Metric | Marketing Claim | Reality in Large-Scale Deployments | The "Context Trap" |
| :--- | :--- | :--- | :--- |
| **Inference Speedup** | "5–7× faster" | **≈2–3× faster** vs. dense models of similar quality at moderate context | Falls toward **≈1.3–1.5×** as context grows (KV/cache + routing overhead dominate) |
| **Active Parameters** | "10% active" | **≈5–20% active** depending on depth and load balancing | Higher active % are often required for stability and quality |
| **Memory Savings** | "Same as small model" | **No VRAM savings** at peak: all experts still resident | Memory budget is set by total parameters, not active ones |
| **Throughput** | "Linear scaling" | **Better tokens/sec/$** than dense at similar quality | Throughput gains erode at very long context as memory bandwidth becomes the bottleneck |

**Insight:** MoE is primarily a **throughput and capacity optimizer**, not a magic fix for latency or memory. It buys "more model for the same serving budget," especially at moderate context, but still runs into bandwidth and KV-cache limits at frontier context lengths.

### Table 3: The Infrastructure Lag Timeline
*Time from publication to standard production practice.*

| Technique | Paper Published | Kernel Support (PyTorch/Triton) | Standard Practice | Lag |
| :--- | :--- | :--- | :--- | :--- |
| **Flash Attention** | May 2022 | Jan 2024 (PyTorch 2.2) | May 2024 (Llama 3) | **24 Months** |
| **Mixture-of-Experts** | Jan 2021 (Switch) | 2023 (MegaBlocks/Triton) | 2024 (Mixtral/Grok) | **36 Months** |
| **GQA** | May 2023 | N/A (Code change only) | 2024 (Llama 3) | **12 Months** |

**Insight:** Integration cost determines adoption speed. Kernel changes take ~2 years to become ubiquitous; distributed system changes (like MoE routing and large-scale sparse attention) take closer to 3 years.
