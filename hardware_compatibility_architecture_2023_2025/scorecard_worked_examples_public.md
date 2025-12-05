# Hardware Compatibility & Risk Profile v2.2 — Worked Examples

**The "First Gate" Filter.**
*An explanatory model for hardware viability. High scores mean "compatible," not "better."*

---

## The Multi-Gate Reality

Hardware compatibility (Gate 1) is necessary but not sufficient. Real success requires passing three gates:
1.  **Gate 1 (Hardware):** Can the chip do this efficiently? (This Scorecard)
2.  **Gate 2 (Training):** Does it learn efficiently? (Optimization, Stability)
3.  **Gate 3 (Scaling):** Does performance scale predictably? (Laws)

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
| **6** | **4** | 🟢 | **Drop-in.** Hardware compatible. |
| **5-6** | **<4** | 🟡 | **Viable with Will.** Hardware works, software/risk remains. |
| **<5** | **Any** | 🔴/🟠 | **Efficiency Bottleneck.** Hardware fights you. |

---

## Prospective Predictions (Dec 2025 → Dec 2027)

| Technique | H / E | Prediction | Primary Risk |
|:----------|:-----:|:-----------|:-------------|
| Differential Transformer | 6 / 2 | Should spread | Kernel complexity |
| Titans | 6 / 0 | Viable for Google | Software maturity |
| xLSTM | 4 / 2 | Niche only | Gate 1 (PAR=1) & Gate 3 (Scaling) |
| Mixture of Depths | 6 / 1 | Viable | Serving complexity |

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
- **v2.2:** Added "Downstream Risks" column (Multi-Gate View).
