# Hardware and Kernel Primer

*A mental model for how hardware, kernels, and frameworks shape what “actually works.”*

This primer gives a quick, practical view of how GPU hardware, kernels, and frameworks fit together, and why they create the Hardware Compatibility Filter and Infrastructure Lag Pattern described in the main article. For definitions of specific acronyms and components (HBM, SRAM, GEMM, tensor cores, etc.), see the **Glossary and Key Concepts** section.

---

## 1. The Three-Layer Stack

At a high level, modern LLM infrastructure looks like a three-layer stack:

1. **Hardware** – GPUs, tensor cores, HBM/SRAM, interconnects (PCIe, NVLink).
2. **Kernels and Libraries** – CUDA/Triton kernels, cuBLAS/cuDNN, FlashAttention, block-sparse matmuls.
3. **Frameworks and Models** – PyTorch/JAX operators, Transformer/MoE/SSM blocks, full model architectures.

The key idea: **models only run fast if their operations can be expressed as a small number of highly optimized kernels that fit the hardware well.** Every time you invent a new primitive that needs a new kernel, you pay an integration and validation tax across this stack.

---

## 2. What a Kernel Actually Is

In this context, a **kernel** is not just an algorithm on paper; it is the concrete, low-level implementation of that algorithm on GPUs:

- It specifies how work is divided over **threads, warps, and thread blocks**.
- It defines how data is laid out in **memory** (HBM vs on-chip SRAM/shared memory vs registers).
- It chooses **tiling strategies** (how matrices are sliced) to keep tensor cores fed and minimize memory traffic.
- It must be **numerically stable**, performant across different GPU generations, and integrated into libraries (e.g., PyTorch, JAX).

Writing a good kernel is hard. Making it production-grade is harder: you need tests, fallbacks, debugging hooks, and framework integration. This is why “kernel-level changes” show a ~24-month lag from paper → library → framework → production (see Appendix, Table 4).

---

## 3. How Hardware Shapes Compatibility

Modern GPUs (A100, H100, etc.) are built around three key properties:

1. **Dense matrix multiplications (GEMMs)** on tensor cores.
2. **Hierarchical memory** – small, fast SRAM on-chip + large, slower HBM off-chip.
3. **Massive parallelism** – thousands of threads executing similar instructions in lockstep.

A technique is **hardware-compatible** if:

- It can be expressed as regular, batched GEMMs or other well-optimized primitives.
- It keeps parallel threads doing similar work with minimal branching.
- It minimizes expensive HBM↔SRAM transfers by reusing data in on-chip memory.

Techniques that require irregular scatter/gather, heavy branching, or inherently sequential computation (e.g., iterative solvers) tend to underutilize the hardware and are much harder to push to frontier scale.

---

## 4. Concrete Examples

### 4.1 FlashAttention: Same Math, Better Kernel

- **Problem:** Standard attention materializes an n×n attention matrix in HBM and repeatedly reads/writes large Q/K/V tensors, making it **memory-bound** and limiting context length.
- **Kernel innovation:** FlashAttention reorganizes the computation into **tiles** that fit into SRAM. It loads small blocks of Q/K/V, computes attention for those blocks, and discards intermediate results without writing the full matrix to HBM.
- **Hardware match:**
  - Uses dense GEMMs on tensor cores.
  - Minimizes HBM traffic; reuses data in SRAM.
  - Preserves exact attention math (no approximation).

This is why FlashAttention could become a near-universal drop-in: it is a **kernel-level improvement** that respects GPU primitives while keeping the higher-level abstraction identical. The price was ~24 months of integration work across libraries and frameworks (Appendix, Table 4).

### 4.2 GQA and MLA: Weight-Only vs Compressed KV

- **GQA (Grouped-Query Attention):**
  - Changes the **weight shapes** so many Query heads share fewer Key/Value heads.
  - Uses the same underlying GEMM kernels as standard MHA.
  - Effect: smaller KV cache, less memory traffic; no new kernels required.
  - **Integration cost:** Weight-only change → adoption driven by retraining cycles (~12 months; Appendix, Table 4).

- **MLA (Multi-Head Latent Attention):**
  - Projects KV vectors into a low-rank latent space before caching.
  - Still uses dense GEMMs, but changes how KV is stored and retrieved.
  - Effect: much smaller KV cache and bandwidth at long contexts (DeepSeek V2/V3).
  - **Integration cost:** Mostly handled via existing linear-algebra kernels; complexity lives in model code and training, not low-level kernels.

In both cases, the operations remain “tensor-core friendly,” which is why they spread quickly once shown to work.

### 4.3 MoE: Conditional Compute Needs Kernel + System Help

Mixture-of-Experts introduces **block-sparse compute** and **conditional routing**:

- Multiple experts (FFNs) per layer, with a router choosing a subset per token.
- On paper, this saves compute: only a fraction of the experts are active per token.
- On hardware, naïve implementations can be **3–15× slower** than dense models because:
  - Tokens for a given expert may be scattered across batches.
  - Expert weights must be moved in and out of SRAM frequently.
  - Communication overhead across GPUs can dominate.

Efficient MoE requires:

- **Block-sparse kernels** that can pack token assignments into regular blocks and run them as GEMMs.
- **Expert sharding and load balancing** across GPUs (e.g., MegaBlocks, FasterMoE, Aurora).
- **Serving stacks** that know how to route tokens to experts, keep experts resident in memory, and handle dynamic loads.

This is why MoE falls into the **Level 3 (serving + distributed system) category** and shows a ~36-month lag from Switch → Mixtral/DeepSeek/Llama 4 (Appendix, Table 4).

### 4.4 SSMs vs Attention: Parallelism Gap

State Space Models (SSMs) like Mamba use **sequential state updates**:

- Each token updates a latent state based on the previous state and current input.
- Even with clever “parallel scan” algorithms, the structure is less naturally parallel than attention’s big batched matmuls.

On GPUs:

- Attention can compute many Q·Kᵀ matmuls in parallel across tokens, heads, and layers.
- SSMs must simulate a recurrence, which is more sequential and often requires custom kernels that are harder to optimize.

The result in 2023–2025:

- Pure Mamba/SSM models are very efficient up to 7B (Falcon Mamba 7B).
- Beyond that, all successful large deployments use SSMs as **components in hybrids** with attention, not as full replacements (Appendix, Table 3).

This illustrates how **parallelism and kernel complexity** can limit which architectures make it to frontier scale on today’s GPU stacks.

---

## 5. How This Creates Infrastructure Lag

Putting it together, the **Infrastructure Lag Pattern** emerges naturally from these layers:

- **Weight-only changes (e.g., GQA):**
  - Only model definition and training code change.
  - No new kernels or serving infra.
  - Adoption timeline: ≈12 months (one or two retraining cycles).

- **Kernel-level changes (e.g., FlashAttention):**
  - Require new CUDA/Triton kernels, library support, and framework integration.
  - Need extensive testing and validation across models and hardware.
  - Adoption timeline: ≈24 months from paper to “standard practice.”

- **Serving + distributed-system changes (e.g., MoE):**
  - Need kernels, framework ops, **and** new serving stacks (expert sharding, routing, load balancing).
  - Often require rewriting major parts of infra and monitoring.
  - Adoption timeline: ≈36 months from initial paper to widespread production use.

Architectural ideas that **align with existing kernels and hardware** (GQA, RoPE, RMSNorm) diffuse quickly. Those that require entirely new kernels or system designs (Flash, MoE, SSMs at scale) move more slowly. Those that **fight GPU primitives** (e.g., heavy spline evaluations in KANs, iterative solvers in Neural ODEs) face the steepest uphill battle and, so far, have not crossed into frontier-scale production.

This is the practical substrate of the Hardware Compatibility Filter: it is not just about mathematical elegance, but about how gracefully a technique flows through hardware, kernels, frameworks, and serving systems.
