# Hardware Friction Map v2.3 — Worked Examples

**The "Cost Function" Filter.**
*A pedagogical map of infrastructure friction. Use to build intuition, not to make go/no-go decisions.*

---

## Status

- **External raters:** ❌
- **Data-calibrated model:** ❌ (See internal doc for roadmap)
- **Status:** **Intuition Pump.** A structured opinion, not a scientific instrument.

**Use as:** A heuristic for adoption risk. **Not as:** A guarantee of viability.

---

## The Friction = Risk Equation

This map estimates **adoption risk** for non-Google labs:
1.  **Hardware Friction (H):** Low score = High **Compute Cost** (low MFU).
2.  **Ecosystem Friction (E):** Low score = High **Engineering Cost** (rewriting kernels).

*Heuristic: If you don't have 50 kernel engineers, High Friction = Non-Starter.*

---

## 5-Axis Rubric (Gate 1 Only)

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
| **IM** | Infra Maturity | Upstream kernels + stable API | External libs | Research code only |

*STI v1.1 Refinement for MoE:* ≤16 experts = 2; 17-64 = 1; 65+ = 0.

---

## Scored Cases & Risk Profile

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

| H-Score | E-Score | Zone | Meaning |
|:-------:|:-------:|:----:|:--------|
| **6** | **4** | 🟢 | **Low Friction.** Drop-in ready. |
| **5-6** | **<4** | 🟡 | **Software Friction.** High Engineering Cost. (e.g., Titans) |
| **<5** | **Any** | 🔴/🟠 | **Hardware Friction.** High Compute Cost. (e.g., LSTM, Mamba) |

**The "Startup Heuristic":** A motivated lab (Google/Meta) can pay the **Engineering Cost** to fix low E. But for a startup or research group, **Software Friction** (Yellow) is a major risk, and **Hardware Friction** (Red) is likely fatal.

---

## Prospective Risk Analysis (Dec 2025 → Dec 2027)

| Technique | H / E | Adoption Risk | Primary Risk Factor |
|:----------|:-----:|:--------------|:--------------------|
| Differential Transformer | 6 / 2 | **Medium** | Kernel complexity (E) |
| Titans | 6 / 0 | **High (Non-Google)** | Software maturity (E) |
| xLSTM | 4 / 2 | **Very High** | Efficiency (H) & Scaling (Gate 3) |
| Mixture of Depths | 6 / 1 | **High** | Serving complexity (E) |

---

## Open Challenge: Towards a Calibrated Model

*This section outlines an **aspirational** research plan to upgrade this map from an "Intuition Pump" to a "Calibrated Filter."*

### 1. Target Variable
**"Adoption Velocity"** defined as: Months from *seminal paper* to *first production deployment at >10B parameter scale* (or equivalent commercial usage).
*   **Fast:** <12 months (e.g., FlashAttention, GQA).
*   **Slow/Stalled:** >36 months or never (e.g., Neural ODEs, Capsule Nets).

### 2. Dataset Scope
**N=50+ Primitives (2018–2025).**
*   **Inclusion Criteria:** Distinct architectural or training primitives (not just hyperparameters).
*   **Examples:** MoE (Sparse), SSMs (Mamba), Linear Attention, RWKV, KANs, LoRA, Quantization (A8W8 vs FP4), Sparse Attention patterns.

### 3. Operational Features (Binary/Categorical)
To replace qualitative judgments with reproducible scores:
*   **GA:** `Is_GEMM_Aligned` (0/1). *Definition: >90% FLOPs in dense matmuls?*
*   **MAL:** `Memory_Access_Pattern` (Categorical). *Classes: Tiled, Streamed, Random.*
*   **PAR:** `Sequential_Dependency` (0/1). *Definition: O(N) dependency on sequence length?*
*   **STI:** `Topology_Change` (Categorical). *Classes: None, Local, Global.*
*   **IM:** `Kernel_Availability` (0/1). *Definition: Exists in Triton/CUDA upstream?*

### 4. Modeling Plan
Fit a simple **Logistic Regression** or **Decision Tree** to predict `Fast_Adoption` (Y/N) from the operational features.
*   **Goal:** Identify which features have statistically significant predictive power.
*   **Hypothesis:** `Sequential_Dependency` (PAR) and `Topology_Change` (STI) are the dominant negative predictors.

*Open Challenge: We invite the community to build this dataset and test the hypothesis.*

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

## Version History

- **v1.0:** 5 axes. Single score.
- **v2.0:** Split score (H/E). Added PAR axis.
- **v2.1:** Renamed "Physics" to "Efficiency".
- **v2.2:** Multi-Gate Risk Profile.
- **v2.3:** Reframed as "Friction Map". Friction = Economic Cost.
- **v2.4:** "Adoption Risk Heuristic" (Startup vs Google).
- **v2.5:** Added formal Research Plan (Target, Dataset, Features).
