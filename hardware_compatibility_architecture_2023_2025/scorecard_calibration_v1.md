# Hardware Friction Map v2.3 — Worked Examples & Stress Tests (Single-Author Draft)

**The "Cost Function" Filter.**
*Measures infrastructure friction (Cost), not physical impossibility. High friction = High cost.*

---

## The Friction = Cost Equation

This map predicts the **cost** of making an architecture work:
1.  **Hardware Friction (H):** Low score = High **Compute Cost** (low MFU, wasted cycles).
2.  **Ecosystem Friction (E):** Low score = High **Engineering Cost** (rewriting kernels).

*Viability = Value - (Compute Cost + Engineering Cost).*

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

## 5-Axis Rubric (v2.1)

### Hardware Efficiency (Max 6) — The "Throughput" Gate
| Axis | Measures | 2 | 1 | 0 |
|:-----|:---------|:--|:--|:--|
| **GA** | GEMM-Alignment | ≥90% FLOPs in batched matmuls | 50-90% | <50% or non-GEMM core ops |
| **MAL** | Memory Locality | Tiled/fused, no O(n²) | Partial tiling | Materializes large intermediates |
| **PAR** | Parallelism | O(1) parallel (no seq dependency) | O(log N) scan / tree | O(N) sequential dependency |

### Ecosystem Readiness (Max 4) — The "Software" Gate
| Axis | Measures | 2 | 1 | 0 |
|:-----|:---------|:--|:--|:--|
| **STI** | Serving Topology | Drop-in | Localized changes | New topology class |
| **IM** | Infra Maturity | Upstream kernels + stable API | Maintained external libs | Research code only |

*STI v1.1 Refinement for MoE:* ≤16 experts = 2; 17-64 = 1; 65+ = 0.

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

### 4. LSTM / GRU (The "Efficiency Fail" Counter-Example)

| Axis | Score | Property-Based Justification |
|:-----|:-----:|:-------------|
| GA | **2** | Standard LSTM cell is GEMM-aligned. |
| MAL | **2** | State size is small. |
| PAR | **0** | **Sequential dependency:** `h_t` depends on `h_{t-1}`. Cannot parallelize over sequence length. |
| STI | **2** | Standard topology. |
| IM | **2** | Ancient, stable support. |
| **H/E** | **4 / 4** | **Red (Efficiency Fail).** PAR=0 kills the Hardware score. |

---

### 5. ByteNet / Conv-LM (The "Gate 2 Fail" Counter-Example)

| Axis | Score | Property-Based Justification |
|:-----|:-----:|:-------------|
| GA | **2** | Convolutions are GEMMs. |
| MAL | **1** | Sliding window requires careful buffering/caching. |
| PAR | **2** | Fully parallel (O(1) depth). |
| STI | **2** | Standard topology. |
| IM | **2** | Supported by all frameworks. |
| **H/E** | **5 / 4** | **Yellow/Green.** Passes Gate 1 (Hardware) but fails Gate 2 (Optimization/Scaling). |

---

### 6. Mixtral 8×7B MoE

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

## Scored Cases & Risk Profile (Summary)

| Architecture | H-Score | E-Score | Zone | Downstream Risks (Gates 2-3) |
|:-------------|:-------:|:-------:|:----:|:-----------------------------|
| Transformer + Flash | **6** | **4** | 🟢 | **None.** (Reference Architecture) |
| GQA | **6** | **4** | 🟢 | **None.** (Weight-only change) |
| MLA | **6** | **3** | 🟢 | **Low.** (DeepSeek-specific impl) |
| **ByteNet (Conv)** | **5** | **4** | 🟡 | **Gate 2 Fail:** Optimization difficulty, context scaling limits. |
| **LSTM / GRU** | **4** | **4** | 🔴 | **Gate 2 Fail:** Vanishing gradients, non-parallelizable. |
| Mixtral 8×7B | **5** | **3** | 🟡 | **Gate 3 Risk:** Expert utilization at scale. |
| DeepSeek V3 | **5** | **2** | 🟡 | **Gate 3 Risk:** Massive routing complexity. |
| Pure Mamba | **3** | **3** | 🟠 | **Gate 3 Risk:** Scaling laws unproven >7B. |
| GLA/DeltaNet | **4** | **3** | 🟠 | **Gate 2 Risk:** Recall/Associative memory limits. |
| Titans (Hypothetical) | **6** | **0** | 🟡 | **Gate 2 Risk:** Memory module optimization. |
| KANs | **2** | **—** | 🔴 | **Gate 1 Fail:** Fundamental hardware mismatch. |

---

## Zone Interpretation

| Score | Zone | Meaning |
|:-----:|:----:|:--------|
| 7–8 | 🟢 | Drop-in ready |
| 4–6 | 🟡 | Viable with engineering effort |
| 2–3 | 🟠 | Research-to-production gap |
| 0–1 | 🔴 | Research-only |

---

## Known Limitations (The "Later Tables")

This is **Table 1** (Hardware). Real success requires passing later gates:
1.  **Training Dynamics:** Does it learn as efficiently as Transformers? (LSTM fails here)
2.  **Scaling Laws:** Does performance scale predictably with compute? (Mamba unproven here)
3.  **Ecosystem:** Is there institutional backing? (GLA vs Mamba)

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

| Abbrev | Full Name | Type | Measures |
|:-------|:----------|:-----|:---------|
| **GA** | GEMM-Alignment | H | % of FLOPs in dense matmuls |
| **MAL** | Memory Locality | H | Efficiency of memory hierarchy |
| **PAR** | Parallelism | H | Sequential vs Parallel execution |
| **STI** | Serving Topology | E | Infra change vs Transformers |
| **IM** | Infra Maturity | E | Kernel/Framework availability |

---

## Version History & Decision Log

### v2.3 (December 2025) — The "Friction Map" Reframe
**Changes:**
1.  **Reframed as "Cost Function":**
    *   *Reasoning:* "Viability" implied binary outcomes. "Friction" implies cost.
    *   *Decision:* Defined Friction = Economic Cost (Compute + Engineering).
2.  **Renamed Title:** "Hardware Friction Map".

### v2.2 (December 2025) — The "Multi-Gate" Update
**Changes:**
1.  **Added "Downstream Risks" Column:**
    *   *Reasoning:* "Green" hardware scores (ByteNet, LSTM) were misleading. They pass Gate 1 (Hardware) but fail Gate 2 (Optimization) or Gate 3 (Scaling).
    *   *Decision:* Explicitly listed these risks to validate the "First Gate" framing.
2.  **Renamed Title:** "Hardware Compatibility & Risk Profile".

### v2.1 (December 2025) — The "Efficiency" Reframe
**Changes:**
1.  **Renamed "Physics" to "Efficiency":**
    *   *Reasoning:* Calling H<5 a "Physics Constraint" was overconfident. LSTMs (H=4) are inefficient, not physically impossible.
    *   *Decision:* Renamed to "Hardware Efficiency" and "Efficiency Bottleneck."
2.  **Softened Claims:** Explicitly labeled as an "explanatory model" rather than a decision rule.

### v2.0 (December 2025) — The "Physics vs. Software" Split
**Changes:**
1.  **Added PAR (Parallelism) Axis:**
    *   *Reasoning:* LSTMs scored Green (8) in v1.1 despite being hardware-incompatible due to sequential dependencies.
    *   *Decision:* Added PAR axis. LSTMs now score H=4 (Red).
2.  **Split Score (H / E):**
    *   *Reasoning:* A single score conflated physics (hard) with ecosystem (soft).
    *   *Decision:* Split into Hardware Fit (Max 6) and Ecosystem Readiness (Max 4).
3.  **Institutional Will Rule:**
    *   *Decision:* Defined rule: "Will can fix low E, but not low H."

### v1.1 (December 2025) — The "First Gate" Reframe
**Changes:**
1.  **Reframed as "Viability Scorecard":** Explicitly stated that high scores mean "compatible," not "better."
2.  **Added LSTM Counter-Example:** Added LSTM (Score 8) to prove that hardware compatibility does not guarantee success. This forces the rubric to admit it ignores training dynamics and scaling laws.
3.  **Merged KM + FSM → IM:** (See below)
4.  **Refined STI for MoE:** (See below)

### v1.1 (December 2025) — The "Simplification & Granularity" Update
**Changes:**
1.  **Merged KM + FSM → IM (Infra Maturity):**
    *   *Reasoning:* In v1.0, these axes had >90% correlation. It was rare to find a technique with upstream kernels (KM=2) but no framework support (FSM=0), or vice versa. Keeping them separate created false precision and "axis leakage" in justifications.
    *   *Decision:* Merge into a single "Infra Maturity" axis. If a technique has kernels, it generally has a library.
2.  **Refined STI for MoE:**
    *   *Reasoning:* v1.0 gave Mixtral (8 experts) and DeepSeek V3 (256 experts) the same STI score (1). This failed to capture the massive serving complexity difference (all-to-all comms, memory bandwidth) of high-expert-count models.
    *   *Decision:* Split STI for MoE based on expert count (≤16 vs >64) and routing type. This successfully differentiates the scores (Mixtral=6, DeepSeek=5).

### v1.0 (December 2025) — Initial Draft
**Scope:** 5 Axes (GA, MAL, KM, STI, FSM)
*   *Hypothesis:* Hardware compatibility is the primary filter for adoption.
*   *Design:* Created 5 axes based on first-principles analysis of GPU execution (compute, memory, kernels, topology, software).
*   *Outcome:* successfully predicted "Green Zone" techniques (Flash, GQA) but failed to explain "Yellow Zone" nuances (Mamba ceiling, MoE variance).
