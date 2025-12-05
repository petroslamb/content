# Hardware Compatibility Design Review Kit v1.0

*A framework for evaluating whether a neural architecture primitive will reach production on GPU-centric stacks.*

---

## Scope & Limitations

**Calibrated for:** 2023–2025 NVIDIA GPU stacks (A100/H100 class, CUDA 12.x, PyTorch 2.x / JAX+XLA).

**What this measures:** Hardware compatibility of *architecture primitives* (attention variants, MoE, SSMs, etc.) using their best-known optimized implementations on this stack.

**What this does NOT measure:** Model quality, benchmark performance, or research novelty. A low score means "hard to productionize," not "bad idea."

---

## The 5-Axis Rubric

Each axis is scored 0–2. Higher = easier to make production-grade on NVIDIA GPU stacks.

---

### Axis 1: GEMM-Alignment (GA)

**What it measures:** How much compute lands in big, batched dense matmuls that saturate tensor cores.

| Score | Criteria |
|:-----:|:---------|
| **2** | ≥90% of FLOPs in batched dense matmuls/conv backed by cuBLAS/cuDNN-class libraries. Control flow and elementwise ops never dominate wall-clock at scale. |
| **1** | 50–90% of FLOPs in GEMMs, but a non-trivial fraction in scatter/gather, state updates, or irregular kernels that can bottleneck at scale. |
| **0** | <50% in GEMMs, or key algorithmic steps cannot be decomposed into large batched matmuls without changing the algorithm. |

**Anchor examples:**
- **2:** Vanilla Transformer (MHA + MLP), GQA, MLA, FlashAttention
- **1:** SSM/linear-attention with per-position state updates; block-sparse attention
- **0:** KAN spline evaluations, Neural ODE adaptive solvers

**Non-example (does NOT qualify as 2):** An attention variant relying on per-token Python/CPU logic between matmuls. Even if the math is GEMM-heavy, if the implementation is dominated by non-GEMM overhead, GA ≠ 2.

---

### Axis 2: Memory Access Locality (MAL)

**What it measures:** How well the algorithm respects GPU memory hierarchy—minimizing HBM↔SRAM traffic via tiling and fusion.

| Score | Criteria |
|:-----:|:---------|
| **2** | Critical paths explicitly tiled/fused so key tensors load once into SRAM, are reused multiple times, and avoid materializing O(n²) intermediates. |
| **1** | Some tiling/fusion exists, but large intermediates or repeated HBM traffic become visible bottlenecks at long sequences or large batches. |
| **0** | Routinely materializes large intermediates and re-reads from HBM. Kernel is clearly memory-bound. |

**Anchor examples:**
- **2:** FlashAttention (tiles QKV, never writes full attention matrix), fused MLPs
- **1:** SSM blocks with per-layer state materialization; MoE without aggressive KV optimization
- **0:** Naive O(n²) attention without Flash-style tricks

**Non-example (does NOT qualify as 2):** Naive attention that computes QKᵀ, writes the full matrix to HBM, then applies softmax in a separate pass—even though it uses matmuls.

---

### Axis 3: Kernel Maturity (KM)

**What it measures:** How much new GPU kernel surface area you must own and maintain.

| Score | Criteria |
|:-----:|:---------|
| **2** | Implementable using only upstream kernels from a major framework (PyTorch/JAX/TF) or vendor libraries (cuBLAS/cuDNN). No custom CUDA/Triton required. |
| **1** | Requires additional kernels, but from known classes with at least one actively maintained, production-used open-source implementation. You integrate, not invent. |
| **0** | Requires novel kernel semantics with no widely-used, production-grade implementation. You own kernel design, optimization, and maintenance. |

**Anchor examples:**
- **2:** Standard attention, GQA/MLA (post-PyTorch 2.2), fused MLPs
- **1:** FlashAttention before upstreaming; MoE expert kernels (MegaBlocks, Triton)
- **0:** First KAN GPU kernels, custom ODE solvers

**Non-example (does NOT qualify as 1):** A research repo with a Triton kernel, last committed 18 months ago, no production users, unaddressed issues → that's KM = 0.

---

### Axis 4: Serving Topology Impact (STI)

**What it measures:** How much the serving system changes compared to a standard dense Transformer LLM stack.

| Score | Criteria |
|:-----:|:---------|
| **2** | Works with same parallelization/topology as dense Transformers. No new routing, sharding, or load-balancing abstractions required. |
| **1** | Requires additional serving logic, but within existing LLM framework concepts—e.g., static expert placement, known routing patterns, predictable resources. |
| **0** | Requires qualitatively new topologies: dynamic expert movement, non-standard consistency protocols, or complex scheduling that current infra doesn't support. |

**Anchor examples:**
- **2:** FlashAttention (kernel swap), GQA/MLA (weight change only)
- **1:** Mixtral/DeepSeek-style MoE with static expert sharding and router load balancing
- **0:** Highly dynamic MoE with elastic experts migrating across GPUs at runtime

**Non-example (does NOT qualify as 2):** A design requiring layer-wise heterogeneous sharding—even if "in principle" mappable to standard layouts.

---

### Axis 5: Framework Support Maturity (FSM)

**What it measures:** How mature and stable the framework-level integration is—APIs, docs, CI, compatibility.

| Score | Criteria |
|:-----:|:---------|
| **2** | Exposed through stable, documented APIs in a major framework's standard release, covered by CI, compatible with current CUDA/driver stacks. |
| **1** | Available via actively maintained third-party libraries that integrate with major frameworks but are not upstream. May lag framework/CUDA releases. |
| **0** | Only research/prototype code. No maintained library. Frequent breakage with new framework versions. |

**Anchor examples:**
- **2:** FlashAttention in PyTorch 2.2+, standard SDPA with docs
- **1:** MoE libraries (MegaBlocks), mamba-ssm package
- **0:** Early KAN implementations, capsule network research code

**Non-example (does NOT qualify as 1):** A pip package with one release years ago and no tests. Packaging alone doesn't lift FSM above 0.

---

## Composite Interpretation

**Total = GA + MAL + KM + STI + FSM** (range 0–10)

| Score | Zone | Interpretation |
|:-----:|:----:|:---------------|
| **8–10** | 🟢 Green | **Drop-in or near drop-in.** Adoption gated by retraining cycles and product priorities, not infra risk. ~12–24 month band, often faster for weight-only changes. |
| **5–7** | 🟡 Yellow | **Viable with serious engineering.** Infra and kernel work are non-trivial but not research-grade. ~12–36 month lag depending on which axes are at 1 vs. 0. Frontier labs may adopt early; others wait for tooling. |
| **3–4** | 🟠 Orange | **Clear research-to-production gap.** Multiple axes at 0. Realistically 24–36+ months unless you're a frontier lab willing to own kernels and serving changes. Candidates for targeted pilots, not broad adoption. |
| **0–2** | 🔴 Red | **Research-only.** Incompatible or very poorly aligned with GPU-centric stacks as they exist. Do not plan production without hardware shifts or major algorithmic redesign. |

---

## Calibration: Scored Anchor Cases

These scores demonstrate how the rubric applies to known architectures.

| Architecture | GA | MAL | KM | STI | FSM | Total | Zone | Known Adoption Lag |
|:-------------|:--:|:---:|:--:|:---:|:---:|:-----:|:----:|:-------------------|
| Transformer + FlashAttention | 2 | 2 | 2 | 2 | 2 | **10** | 🟢 | ~24 months (paper → standard) |
| GQA | 2 | 2 | 2 | 2 | 2 | **10** | 🟢 | ~12 months (weight-only) |
| MLA (DeepSeek) | 2 | 2 | 2 | 2 | 1 | **9** | 🟢 | ~12–18 months |
| Mixtral-style MoE | 2 | 1 | 1 | 1 | 1 | **6** | 🟡 | ~36 months (Switch → production) |
| DeepSeek V3 (MoE+MLA) | 2 | 1 | 1 | 1 | 1 | **6** | 🟡 | DeepSeek leads by 12–24 mo |
| Pure Mamba 7B | 1 | 1 | 1 | 2 | 1 | **6** | 🟡 | Ceiling at 7B; no frontier proof |
| Hybrid SSM+Attention | 1 | 1 | 1 | 1 | 1 | **5** | 🟠 | Limited production adoption |
| KANs | 0 | 0 | 0 | 2 | 0 | **2** | 🔴 | None (research-only) |
| Neural ODEs | 0 | 0 | 0 | 1 | 0 | **1** | 🔴 | None (never crossed for LLMs) |
| Capsule Networks | 1 | 0 | 0 | 2 | 0 | **3** | 🟠 | None (historical example) |

**Validation:** Composite predictions align with observed adoption timelines across all anchor cases.

---

## How to Use This Scorecard

### For evaluating a new architecture/primitive:

1. **Score each axis (0–2)** using the criteria above.
2. **Sum the scores** (range 0–10).
3. **Check the zone** and set expectations accordingly.
4. **Compare to anchors** to sanity-check your scoring.

### For design review:

Ask: *"Which axes are at 0 or 1? What would it take to raise them?"*

- Low GA → Redesign for GEMM-friendly compute paths
- Low MAL → Investigate tiling/fusion strategies
- Low KM → Find or fund kernel development
- Low STI → Simplify serving requirements or wait for infra
- Low FSM → Contribute upstream or wait for adoption

### For roadmap planning:

- **Green (8–10):** Safe to adopt now. Plan for 1 retraining cycle.
- **Yellow (5–7):** Allocate engineering resources. Plan for 2–3 cycles.
- **Orange (3–4):** Pilot only. Don't bet product timelines on this.
- **Red (0–2):** Track as research. Don't plan production.

---

## Calibration Notes

**Scoring date:** December 2025

**Methodology:** Scores based on published papers, technical reports, model cards, framework changelogs, and observed production deployment timelines.

**Limitations:**
- Calibrated for NVIDIA GPU stacks. Adjustments may be needed for TPU, AMD, or custom ASICs.
- KM and FSM axes often correlate; architectures rarely score high on one and low on the other.
- Pure Mamba's score (6) doesn't capture its *scaling ceiling*—the lack of evidence above 7B is a separate risk factor.

**Inter-rater validation:** Recommended before finalizing. Have 2–3 independent ML infra engineers score the anchor cases. If agreement is <80% on any axis, tighten definitions.

---

## Version History

- **v1.0 (December 2025):** Initial release. 5 axes, 10 anchor cases, composite interpretation.
