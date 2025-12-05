# Hardware/Infra Viability Scorecard (v1.1)

**The "First Gate" Filter.**

This scorecard measures **viability**, not success. It answers: *"Can this idea survive contact with 2023–2025 GPUs?"*
It does **NOT** predict which architecture will win. High scores mean "compatible," not "better."

---

## 4-Axis Rubric

| Axis | Measures | 2 | 1 | 0 |
|:-----|:---------|:--|:--|:--|
| **GA** | GEMM-Alignment | ≥90% FLOPs in batched matmuls | 50-90% | <50% or non-GEMM core ops |
| **MAL** | Memory Locality | Tiled/fused, no O(n²) | Partial tiling | Materializes large intermediates |
| **STI** | Serving Topology | Drop-in | Localized changes | New topology class |
| **IM** | Infra Maturity | Upstream kernels + stable API | Maintained external libs | Research code only |

*KM and FSM merged into IM — they rarely scored differently.*

**STI for MoE (v1.1 refinement):** For MoE architectures, STI accounts for expert count and routing complexity:
- ≤16 experts with static routing → STI=2
- 17-64 experts or load-balanced routing → STI=1  
- 65+ experts or dynamic routing → STI=0

*This refinement evolved from stress-testing v1.0, which couldn't distinguish 8-expert from 256-expert designs. Expect future revisions as more edge cases are scored.*

---

## Scored Cases (Viability ≠ Success)

| Architecture | GA | MAL | STI | IM | Total | Zone |
|:-------------|:--:|:---:|:---:|:--:|:-----:|:----:|
| Transformer + Flash | 2 | 2 | 2 | 2 | **8** | 🟢 |
| GQA | 2 | 2 | 2 | 2 | **8** | 🟢 |
| MLA | 2 | 2 | 2 | 1 | **7** | 🟢 |
| **LSTM / GRU** | **2** | **2** | **2** | **2** | **8** | 🟢 |
| Mixtral 8×7B | 2 | 1 | 2 | 1 | **6** | 🟡 |
| DeepSeek V3 (256 exp) | 2 | 1 | 1 | 1 | **5** | 🟡 |
| Pure Mamba | 1 | 1 | 2 | 1 | **5** | 🟡 |
| GLA/DeltaNet | 2 | 1 | 2 | 1 | **6** | 🟡 |
| KANs | 0 | 0 | N/A | 0 | — | 🔴 |
| Neural ODEs | 0 | 0 | 1 | 0 | **1** | 🔴 |

**Crucial Lesson:** LSTM scores **8 (Green)** but is a "losing" architecture for LLMs. This proves the scorecard only measures *hardware fit*, not expressivity or scaling laws.

---

## Zone Interpretation

| Score | Zone | Meaning |
|:-----:|:----:|:--------|
| 7–8 | 🟢 | **Hardware Compatible.** (Does not imply model quality) |
| 4–6 | 🟡 | **Viable with Effort.** (Requires engineering investment) |
| 2–3 | 🟠 | **Infra Gap.** (Hard to productionize) |
| 0–1 | 🔴 | **Incompatible.** (Research-only on current stack) |

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

- **External raters:** ❌
- **Prospective predictions:** ✅ (check Dec 2027)

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

- **v1.0:** Initial 5-axis rubric.
- **v1.1:** Merged KM+FSM into IM (4 axes). Refined STI for MoE.
