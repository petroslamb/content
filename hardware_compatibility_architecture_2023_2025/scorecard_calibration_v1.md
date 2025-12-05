# Hardware Compatibility Scorecard v1.1 — Worked Examples & Stress Tests (Single-Author Draft)

**Scope:** 2023–2025 NVIDIA GPU stacks (A100/H100, CUDA 12.x, PyTorch 2.x / JAX+XLA)  
**Scoring date:** December 2025  
**Status:** Single-author draft. Not externally validated.

---

## What This Document Is (And Isn't)

**This is a single-author worked example set, not a validated calibration.**

The scores below show how to apply the rubric to known architectures. They demonstrate the rubric's mechanics, not its predictive power.

**Explicit limitations:**
1. **Confirmation bias:** Scores were assigned after knowing adoption outcomes.
2. **No surprises:** All scored cases are archetypes with known outcomes.
3. **Speculative entries:** KAN's STI is N/A (no deployments to verify).

**What would make this a real calibration:**
- **External raters:** 2-3 independent scorers. If agreement <80%, revise rubric.
- **Prospective test:** Score a new technique before observing adoption; check back in 12-24 months.

---

## 4-Axis Rubric (v1.1)

*KM and FSM merged into IM — they rarely scored differently in practice.*

| Axis | Measures | 2 | 1 | 0 |
|:-----|:---------|:--|:--|:--|
| **GA** | GEMM-Alignment | ≥90% FLOPs in batched matmuls | 50-90% | <50% or non-GEMM core ops |
| **MAL** | Memory Locality | Tiled/fused, no O(n²) | Partial tiling | Materializes large intermediates |
| **STI** | Serving Topology | Drop-in | Localized changes | New topology class |
| **IM** | Infra Maturity | Upstream kernels + stable API | Maintained external libs | Research code only |

**STI for MoE (v1.1 refinement):** For MoE architectures, STI accounts for expert count and routing complexity:
- ≤16 experts with static routing → STI=2
- 17-64 experts or load-balanced routing → STI=1  
- 65+ experts or dynamic routing → STI=0

*This refinement evolved from stress-testing v1.0, which couldn't distinguish 8-expert from 256-expert designs.*

---

## Worked Examples

These scores demonstrate how the rubric applies. Justifications aim to be **property-based** (measuring the technique itself) rather than **adoption-based** (who uses it).

---

### 1. Vanilla Transformer + FlashAttention

| Axis | Score | Property-Based Justification |
|:-----|:-----:|:-------------|
| GA | **2** | QKV projections: batched matmul. Attention: QK^T matmul + softmax + V matmul. MLP: two dense matmuls. All dispatch to cuBLAS. |
| MAL | **2** | FlashAttention loads Q/K/V blocks into SRAM, computes softmax incrementally, writes output blocks. Full N×N attention matrix never exists in HBM. |
| STI | **2** | Same tensor/pipeline parallel sharding as pre-Flash Transformers. FlashAttention is a kernel swap; serving topology unchanged. |
| IM | **2** | `torch.nn.functional.scaled_dot_product_attention` in PyTorch 2.2+ dispatches to FlashAttention2 backend. Stable API, documented, CI-backed. |
| **Total** | **8** | |

---

### 2. Grouped-Query Attention (GQA)

| Axis | Score | Property-Based Justification |
|:-----|:-----:|:-------------|
| GA | **2** | Identical matmul structure to MHA. Q projection: `[batch, seq, heads, d] @ W_q`. K/V projections: fewer heads, same op type. |
| MAL | **2** | KV cache per token: `num_kv_heads × d` instead of `num_heads × d`. 8× reduction in KV cache size and bandwidth. |
| STI | **2** | KV cache is smaller but same structure. No sharding changes. No routing. |
| IM | **2** | Supported in HuggingFace `transformers`, PyTorch, JAX. Config change: `num_key_value_heads` parameter. |
| **Total** | **8** | |

---

### 3. Multi-Head Latent Attention (MLA)

| Axis | Score | Property-Based Justification |
|:-----|:-----:|:-------------|
| GA | **2** | Down-projection: `[batch, seq, d] @ W_down → [batch, seq, latent_d]`. Up-projection for attention. All dense matmuls. |
| MAL | **2** | KV cache stores latent vectors (smaller than full K/V). Cache size: `latent_d` per token instead of `heads × d_k`. |
| STI | **2** | Same sharding as dense attention. Latent dimension is a model config, not a topology change. |
| IM | **1** | Not in vanilla PyTorch. Requires DeepSeek's model code. HuggingFace has DeepSeek models but not a generic MLA module. |
| **Total** | **7** | |

---

### 4. Mixtral 8×7B MoE

| Axis | Score | Property-Based Justification |
|:-----|:-----:|:-------------|
| GA | **2** | Expert FFNs: standard dense matmuls. Router: small matmul + top-k. >95% FLOPs in cuBLAS ops. |
| MAL | **1** | Expert weights resident in HBM. Per-token routing means different experts activated → weight loading patterns less predictable. |
| STI | **2** | 8 experts with static top-2 routing. Fits v1.1 criteria for STI=2. |
| IM | **1** | HuggingFace supports Mixtral. vLLM has MoE backend. Requires MoE-aware serving stack. |
| **Total** | **6** | |

---

### 5. DeepSeek V3 (256 experts)

| Axis | Score | Property-Based Justification |
|:-----|:-----:|:-------------|
| GA | **2** | Same as Mixtral — expert FFNs are dense matmuls. |
| MAL | **1** | 256 experts means more weight sharding, less predictable activation patterns. |
| STI | **1** | 256 experts (>64) with load-balanced routing. Fits v1.1 criteria for STI=1. |
| IM | **1** | DeepSeek's implementation. External libraries required. |
| **Total** | **5** | |

---

### 6. Pure Mamba / SSM (Falcon Mamba 7B)

| Axis | Score | Property-Based Justification |
|:-----|:-----:|:-------------|
| GA | **1** | Input/output projections: dense matmuls. Core SSM operation: parallel scan over states (NOT a GEMM). Estimated: 60-70% FLOPs in matmuls. |
| MAL | **1** | No O(n²) attention matrix. But state is updated per position, written/read per layer. Not Flash-level fusion. |
| STI | **2** | No routing, no expert sharding. Dense tensor structure. Same parallelism patterns as dense Transformer. |
| IM | **1** | `mamba-ssm` package provides CUDA kernels. Maintained by Mamba authors. Not upstream in PyTorch/JAX. |
| **Total** | **5** | |

**⚠️ RUBRIC LIMITATION:** Mamba scores 5 ("viable with engineering") but no pure SSM above 7B exists. Compatibility ≠ scalability.

---

### 7. GLA/DeltaNet

| Axis | Score | Property-Based Justification |
|:-----|:-----:|:-------------|
| GA | **2** | Linear attention is more GEMM-friendly than selective scan. Avoids Mamba's parallel scan. |
| MAL | **1** | Linear-time complexity, but state updates per position. Similar to Mamba. Not Flash-level fusion. |
| STI | **2** | Standard dense topology. No routing. |
| IM | **1** | fla package provides Triton kernels. Actively maintained. HuggingFace supports Qwen3-Next. |
| **Total** | **6** | |

---

### 8. KANs (Kolmogorov-Arnold Networks)

| Axis | Score | Property-Based Justification |
|:-----|:-----:|:-------------|
| GA | **0** | Core operation: per-edge spline evaluation. Not expressible as batched dense matmuls. Tensor cores largely idle. |
| MAL | **0** | Many small, irregular ops. Spline coefficients accessed per edge, per token. No natural tiling structure. |
| STI | **N/A** | No production deployments exist to verify. |
| IM | **0** | Research code only. No maintained library. |
| **Total** | **—** | |

---

### 9. Neural ODEs

| Axis | Score | Property-Based Justification |
|:-----|:-----:|:-------------|
| GA | **0** | ODE solvers are iterative. Many small matmuls per forward pass. Tensor cores underutilized. |
| MAL | **0** | Repeated function evaluations. Hard to fuse across solver steps. |
| STI | **1** | Variable compute depth complicates batching but not completely incompatible. |
| IM | **0** | `torchdiffeq` exists but not optimized for LLM-scale. Research-focused. |
| **Total** | **1** | |

---

## Summary Table (Not a Benchmark)

| Architecture | GA | MAL | STI | IM | Total | Zone |
|:-------------|:--:|:---:|:---:|:--:|:-----:|:----:|
| Transformer + Flash | 2 | 2 | 2 | 2 | **8** | 🟢 |
| GQA | 2 | 2 | 2 | 2 | **8** | 🟢 |
| MLA | 2 | 2 | 2 | 1 | **7** | 🟢 |
| Mixtral 8×7B | 2 | 1 | 2 | 1 | **6** | 🟡 |
| DeepSeek V3 (256 exp) | 2 | 1 | 1 | 1 | **5** | 🟡 |
| Pure Mamba | 1 | 1 | 2 | 1 | **5** | 🟡 |
| GLA/DeltaNet | 2 | 1 | 2 | 1 | **6** | 🟡 |
| KANs | 0 | 0 | N/A | 0 | — | 🔴 |
| Neural ODEs | 0 | 0 | 1 | 0 | **1** | 🔴 |

---

## Zone Interpretation

| Score | Zone | Meaning |
|:-----:|:----:|:--------|
| 7–8 | 🟢 | Drop-in ready |
| 4–6 | 🟡 | Viable with engineering effort |
| 2–3 | 🟠 | Research-to-production gap |
| 0–1 | 🔴 | Research-only |

---

## Known Failure Modes

1. **Mamba ceiling:** Scores 5 but no SSM above 7B. Compatibility ≠ scalability.
2. **Competitive dynamics:** Sparse attention would score 6-7 but was replaced by Flash. Rubric ignores alternatives.
3. **Ecosystem investment:** Similar scores can have different adoption based on institutional backing (GLA vs Mamba).

---

## Prospective Predictions (Dec 2025 → Dec 2027)

| Technique | Score | Prediction | Pushes prior? |
|:----------|:-----:|:-----------|:-------------:|
| Differential Transformer | 6 | Should spread with kernel work | No |
| Titans | 2 | Research-only | Slightly |
| xLSTM | 5 | May hit Mamba ceiling | No |
| Mixture of Depths | 5 | Serving complexity limits adoption | No |
| GLA/DeltaNet | 6 | Continued adoption | No |

**Honest note:** Only Titans pushes against my prior.

---

## Status

| Criterion | Status |
|:----------|:------:|
| External raters | ❌ |
| Prospective predictions | ✅ (check Dec 2027) |
| Rubric evolved from stress test | ✅ (STI v1.1 for MoE) |

**Use as:** Illustration of rubric mechanics. **Not as:** Evidence of predictive power.

---

## Glossary

| Abbrev | Full Name | Measures |
|:-------|:----------|:---------|
| **GA** | GEMM-Alignment | % of FLOPs in dense matrix multiplications |
| **MAL** | Memory Access Locality | Efficiency of GPU memory hierarchy usage |
| **STI** | Serving Topology Impact | Infrastructure change vs standard Transformers |
| **IM** | Infra Maturity | **Merged KM + FSM.** Combined because they rarely diverge. |
| *(KM)* | *Kernel Maturity* | *Existence of upstream/vendor kernels (merged into IM)* |
| *(FSM)* | *Framework Support* | *API stability & CI support (merged into IM)* |

**Note on IM Merge:** KM and FSM diverge only in rare cases (e.g., "abandoned research code" has kernels but no framework support). For production scoring, they move together.

---

## Version History

- **v1.0:** Initial 5-axis rubric (GA, MAL, KM, STI, FSM)
- **v1.1:** Merged KM+FSM into IM (4 axes). Refined STI for MoE (expert count + routing complexity).
