# What Actually Works: The Hardware Compatibility Filter in Neural Architecture (2023–2025)

*How GPU primitives shape adoption, why MoE spread, and why architecture innovation is slowing down*

**TL;DR**
- Hardware compatibility—not just benchmarks—explains which architectures actually make it into 2023–2025 production LLMs.
- FlashAttention, GQA/MLA, and MoE win because they map cleanly onto GPU primitives and memory hierarchies; KANs and pure SSMs don’t.
- There is a predictable 12/24/36‑month “infrastructure lag” from paper to standard practice, driven by integration cost (weights → kernels → serving).
- Architecture has become a relatively stable container; the biggest gains now come from training innovation (RL-style post-training, optimization, data curation) on top of that container.

# Introduction

In "Neural Architecture Design as a Compositional Language," we established that architecture evolved from hand-crafted hierarchies to modular component libraries. The Transformer validated this: uniform blocks, structured composition rules, and emergent specialization through training.

We ended with three open questions. What primitives belong in the toolkit beyond attention and MLPs? What composition operators enable scaling? How do we train compositional systems effectively?

Two years of production deployments provide answers, but not through the lens most researchers expected. The organizing principle of the last 24 months isn't expressiveness or theoretical elegance. It is **hardware compatibility**.

By "hardware compatibility," we mean a concrete set of properties: operations that can be expressed as dense matrix multiplications on tensor cores, memory access patterns that respect the SRAM/HBM hierarchy, and enough regular parallelism to saturate modern GPUs. GPU architectures—optimized for these dense, parallel primitives—create a filter. Techniques that map naturally to them tend to win; techniques that fight them rarely survive contact with production, regardless of benchmark results on small models.

Hardware is not the only determinant of adoption—data availability, optimization effort, and product fit all matter—but when we compare architectures across labs in 2023–2025, hardware alignment is the strongest common constraint that shows up repeatedly in both open-weight releases and closed-model behavior.

This post examines the 2023–2025 era through three perspectives:

*   **Act I: The Compatibility Filter** — How Flash Attention, MoE, and attention variants succeeded by exploiting GPU architecture, while KANs and pure SSMs failed by fighting it.
*   **Act II: The Conditional Execution Revolution** — How learned routing (attention, MoE, sparse patterns) became the defining composition operator, replacing designed computation graphs.
*   **Act III: The Infrastructure Lag Pattern** — Why Flash Attention took 24 months to become standard, why MoE took 36, and how to predict adoption timelines.

We argue for three claims, using production-style evidence and public model documentation:

1.  **Hardware compatibility is a better early predictor of adoption** than small-scale benchmarks.
2.  **Architecture innovation is slowing relative to training innovation**; for the foreseeable future on today's GPU-centric stacks, the leverage is likely in optimization and data, not entirely new primitives.
3.  **Pure SSMs have not yet scaled to frontier models**; in practice, hybrids appear to be the effective ceiling today (see Appendix, Table 3).

All three are falsifiable. For example, a technique that is clearly misaligned with GPU primitives but still becomes standard at frontier scale would directly challenge the hardware compatibility thesis; a pure SSM frontier model would falsify our current ceiling claim. As of December 2025, we have not seen such counterexamples in the public record.

What doesn't work: Speculation without production validation, marketing claims without aggregate data, and techniques that ignore deployment constraints.

What does work: Hardware-compatible primitives, permissive compositional operators, and training methods that exploit—not fight—modular structure.

---

## Act I: The Compatibility Filter
*How hardware constraints shaped what survived*

**Scope & Limitations**  
This act (and the broader analysis) focuses on large language models trained and deployed between 2023–2025 on GPU-centric infrastructure, using public papers, model cards, and system documentation as primary evidence. Closed-source models are included only to the extent that their internals can be inferred from public disclosures and third-party analyses; we do not claim completeness over proprietary experiments. All heuristics here (e.g., hardware compatibility as a filter, 12/24/36-month adoption lags) are empirical patterns observed in this window, not guarantees, and may not generalize to future hardware or domains outside production-scale LLMs. For definitions of key terms, see the **Glossary and Key Concepts** section; for a deeper look at how hardware and kernels interact with these ideas, see the **Hardware and Kernel Primer** section.

### 1. The Attention Bottleneck

By early 2023, the Transformer architecture faced a crisis, but it wasn't about intelligence. It was about memory. The quadratic cost of attention ($O(n^2)$) is often cited as a computational problem, but in practice, it is a memory movement problem.

At 128K context length, the Key-Value (KV) cache for a 70B model grows to hundreds of gigabytes, exceeding the HBM (High Bandwidth Memory) capacity of even an H100 GPU. The bottleneck wasn't doing the math; it was moving the matrices from HBM to the compute units (SRAM) and back.

Naive solutions failed because they tried to approximate the math (sparse attention patterns, low-rank approximations) rather than solve the memory movement. They broke the one thing researchers wouldn't compromise: the exactness of the attention mechanism. The solution that won didn't change the math at all. It changed the memory access pattern.

### 2. Flash Attention: Hardware as Design Constraint

Flash Attention (Dao et al., 2022; 2023) is one of the cleanest case studies for the Hardware Compatibility Thesis. Published in May 2022, it did not propose a new neural primitive. Instead, it proposed a **tiling algorithm** that respects the GPU's memory hierarchy.

Standard attention materializes the massive $N \times N$ attention matrix in HBM, reading and writing gigabytes of data for every token generation. Flash Attention tiles the computation so that blocks of the matrix are loaded into SRAM (fast, on-chip memory), computed, and discarded without ever writing the full matrix to HBM.

**The Mechanism:** By keeping the computation in SRAM, Flash Attention reduces memory reads/writes by roughly an order of magnitude and delivers 2–4× speedups on attention while cutting memory usage by ~10–20× at long sequences (see Appendix, Table 4). It turns a memory-bound operation into a compute-bound one, which is exactly what GPUs are designed to handle.

**The Adoption Timeline (The ≈24-Month Lag):**
The adoption of Flash Attention reveals a predictable infrastructure lag pattern that governs the entire field:

*   **May 2022:** Paper published. Benchmarks show 2–4× speedup and near-linear memory scaling.
*   **2022–2023 (Stage 2):** Early adopters and startups integrate it manually. Custom CUDA kernels are required.
*   **January 2024 (Stage 3):** PyTorch 2.2 officially integrates FlashAttention-2. It becomes a standard library call.
*   **May 2024 (Stage 4):** Standard practice. Major 2024 releases (Llama 3, Gemma 2, Phi-3 and peers) rely on FlashAttention-style kernels by default (Appendix, Table 4).

It took roughly 24 months for a technique that required kernel-level changes to move from "proven research" to "standard practice." This lag is not accidental; it is the cost of infrastructure integration. We will see this pattern repeat with MoE.

### 3. The Compatibility Winners

The winners of 2023–2025 all share one trait: they reduce memory bandwidth pressure without requiring new, exotic compute kernels.

**Grouped Query Attention (GQA):**
GQA is the dominant attention variant of 2024 in our audit, appearing in a large majority of open-weight and documented models, including Llama 3, Mistral 7B, and Qwen2.5 (see Appendix, Table 5). Its mechanism is simple: share Key and Value heads across multiple Query heads.
*   **Why it won:** It reduces the size of the KV cache by 8× (for 8 groups), directly lowering memory bandwidth requirements. It uses standard matrix multiplication. It requires no new hardware support.
*   **The result:** For 2024–2025 releases, it is effectively the default in most large model families we examined.

**Multi-Head Latent Attention (MLA):**
Pioneered by DeepSeek (V2/V3), MLA takes compression further. It projects the KV cache into a low-rank latent vector.
*   **Why it won:** It compresses the KV cache significantly (crucial for DeepSeek's 128K context) while maintaining the expressiveness of full attention (Appendix, Table 5). Like GQA, it relies on dense matrix projections—the GPU's native language.

MoE sits in the same compatibility bucket: when well-engineered, large MoE deployments deliver approximately **2–3×** higher throughput than dense models of similar quality, not the **5–7×** often claimed in marketing, and their advantage shrinks toward **≈1.3–1.5×** at very long contexts as routing and KV/cache bandwidth dominate (Appendix, Table 2). The techniques that stick are those that respect the hardware, even when their real-world gains are less dramatic than the launch slides.

**Contrast: The Failure of KANs**
Kolmogorov-Arnold Networks (KANs) generated immense hype in early 2024 by proposing learnable activation functions on edges (splines) rather than fixed weights.
*   **Why they struggle:** Spline evaluation does not map cleanly to dense matrix multiplication. It requires disparate memory access patterns and custom kernels that are harder to implement in a way that saturates GPU tensor cores.
*   **The verdict (as of 2025):** Despite theoretical elegance and promising small-scale results, we find no public evidence of large-scale production deployments. In practice, KANs remain a research curiosity for frontier-scale workloads, primarily because their current implementations are poorly aligned with GPU primitives.

### 4. SSMs: The Compatibility Boundary

State Space Models (SSMs) like Mamba (Gu et al., 2021; Gu & Dao et al., 2023) represent the most significant architectural challenge to the Transformer. They promise linear scaling ($O(n)$) by replacing the attention mechanism with a recurrent state update.

**The Mechanism:** Mamba compresses context into a fixed-size state, updating it sequentially as it processes tokens. This eliminates the KV cache entirely, theoretically solving the memory bottleneck for infinite contexts.

**The Friction:** Pure SSMs push against the GPU's greatest strength: **parallelism**.
Transformers process all tokens in a sequence simultaneously during training (parallel prefix scan). SSMs, by definition, have a sequential dependency: state $t$ depends on state $t-1$. While Mamba introduces a "parallel scan" algorithm to mitigate this, the fundamental operation is still less straightforward to parallelize than the brute-force matmuls of a Transformer.

**The Evidence (The Ceiling):**
*   **Proven Scale:** Pure Mamba models exist and work at 130M, 1.4B, 2.8B, and 7B (Falcon Mamba; Appendix, Table 3).
*   **The Gap:** We find no public evidence of a pure SSM scaling to 13B, 70B, or frontier levels (100B+); all large SSM-style deployments above 7B are hybrids (Appendix, Table 3).
*   **Major Lab Adoption:** As of late 2025, OpenAI, Google, Meta, and Anthropic have not publicly documented pure SSMs in their frontier models. Adoption is 0/5 in our audit.

**The Nuance:** Hybrids exist. Jamba (AI21) and Qwen3-Next use SSM layers mixed with Attention layers.
*   **Why hybrids work:** They route local, sequential dependencies to the SSM (efficient) and global, complex dependencies to Attention (expressive).
*   **The Prediction:** Absent new evidence or hardware, pure SSMs look unlikely to become the dominant frontier architecture. The main bottleneck appears architectural (parallelism and in-context learning), not just a missing training trick. Hybrids are where we see real adoption today, and even they remain niche due to implementation complexity.

### 5. External Memory (RAG): The Compatibility Shortcut

While researchers fought over $O(n^2)$ vs $O(n)$ architectures, the industry solved the context problem with a database. Retrieval-Augmented Generation (RAG) is the ultimate compatibility hack.

*   **Mechanism:** Offload memory to a vector database (highly optimized for search). Retrieve only relevant chunks. Feed them to the GPU context window.
*   **Why it won:** It requires **zero changes** to the neural architecture. It treats the GPU as a reasoning engine, not a storage engine.
*   **Adoption:** Effectively universal among major commercial assistants as of 2025. ChatGPT, Claude, Gemini and similar products all expose some form of retrieval or tool-based long-context access.

**Act I Synthesis:**
Across 2023–2025, the pattern is consistent. Flash Attention (maps to the memory hierarchy) took about 24 months to become standard (Appendix, Table 4). GQA (maps to bandwidth constraints) diffused in roughly 12 months as a weight-only change (Appendix, Tables 4 and 5). Pure SSMs (which push against parallelism) currently top out at 7B with no public frontier-scale models (Appendix, Table 3). KANs (incompatible compute paths) have no documented large-scale production deployments.

We are not designing neural networks in a vacuum. We are discovering which computations GPUs can efficiently express. Hardware acts as a ruthless filter on which ideas survive into production today.

In Act II, we will see how this filter shaped the most important composition operator of the decade: the shift from static graphs to learned, conditional execution.
