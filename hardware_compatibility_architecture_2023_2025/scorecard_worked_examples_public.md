# Hardware/Infra Viability Scorecard v2.1 — Worked Examples

**The "First Gate" Filter.**
*An explanatory model for hardware viability. High scores mean "compatible," not "better."*

---

## The v2.1 Split: Efficiency vs. Software

A single score hides the problem. v2.1 splits the score into two dimensions:
1.  **Hardware Efficiency (H):** Can the chip do this efficiently? (Throughput/Scaling). *Hard constraint.*
2.  **Ecosystem Readiness (E):** Does the software exist? (Infra). *Fixable with "Institutional Will".*

---

## 5-Axis Rubric

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

## Scored Cases (H / E)

| Architecture | GA | MAL | PAR | **H-Score** | STI | IM | **E-Score** | Zone |
|:-------------|:--:|:---:|:---:|:-----------:|:---:|:--:|:-----------:|:----:|
| Transformer + Flash | 2 | 2 | 2 | **6** | 2 | 2 | **4** | 🟢 |
| GQA | 2 | 2 | 2 | **6** | 2 | 2 | **4** | 🟢 |
| MLA | 2 | 2 | 2 | **6** | 2 | 1 | **3** | 🟢 |
| **LSTM / GRU** | 2 | 2 | 0 | **4** | 2 | 2 | **4** | 🔴 |
| **ByteNet (Conv)** | 2 | 1 | 2 | **5** | 2 | 2 | **4** | 🟡 |
| Pure Mamba | 1 | 1 | 1 | **3** | 2 | 1 | **3** | 🟠 |
| Mixtral 8×7B | 2 | 1 | 2 | **5** | 2 | 1 | **3** | 🟡 |
| DeepSeek V3 | 2 | 1 | 2 | **5** | 1 | 1 | **2** | 🟡 |
| GLA/DeltaNet | 2 | 1 | 1 | **4** | 2 | 1 | **3** | 🟠 |
| Titans (Hypothetical) | 2 | 2 | 2 | **6** | 0 | 0 | **0** | 🟡 |
| KANs | 0 | 0 | 2 | **2** | N/A | 0 | **—** | 🔴 |

---

## Zone Interpretation

| H-Score | E-Score | Zone | Meaning |
|:-------:|:-------:|:----:|:--------|
| **6** | **4** | 🟢 | **Drop-in.** Efficient, software exists. |
| **5-6** | **<4** | 🟡 | **Viable with Will.** Efficient, but you must build the software. (e.g., Titans) |
| **<5** | **Any** | 🔴/🟠 | **Efficiency Bottleneck.** Hardware fights you. Will cannot fix this easily. (e.g., LSTM, Mamba) |

**The "Institutional Will" Rule:** A motivated lab (Google/Meta) can ignore a low **E-Score** if the **H-Score** is high (5-6). No amount of will fixes a low **H-Score** without new hardware.

**Counter-Examples:**
1.  **LSTM (H=4):** Fails Efficiency (PAR=0). Dead.
2.  **ByteNet (H=5):** Passes Efficiency, but fails **Gate 2** (Optimization/Scaling). Dead.

---

## Prospective Predictions (Dec 2025 → Dec 2027)

| Technique | H / E | Prediction | Pushes prior? |
|:----------|:-----:|:-----------|:-------------:|
| Differential Transformer | 6 / 2 | Should spread (H=6) | No |
| Titans | 6 / 0 | Viable for Google (H=6) | Yes |
| xLSTM | 4 / 2 | Limited by PAR=1 (scan) | No |
| Mixture of Depths | 6 / 1 | Viable if serving solved | No |

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

- **v1.0:** 5 axes (GA, MAL, KM, STI, FSM). Single score.
- **v1.1:** Merged KM+FSM. Refined STI.
- **v2.0:** Split score. Added PAR axis.
- **v2.1:** Renamed "Physics" to "Efficiency" to avoid overclaiming.
