# Hardware Compatibility Scorecard v1.0 — Worked Examples

**Single-author draft. Not externally validated.**

---

## 4-Axis Rubric (Revised)

KM and FSM merged into **Infra Maturity** — they rarely scored differently in practice.

| Axis | Measures | 2 | 1 | 0 |
|:-----|:---------|:--|:--|:--|
| **GA** | GEMM-Alignment | ≥90% FLOPs in batched matmuls | 50-90% | <50% or non-GEMM core ops |
| **MAL** | Memory Locality | Tiled/fused, no O(n²) | Partial tiling | Materializes large intermediates |
| **STI** | Serving Topology | Drop-in | Localized changes (e.g., MoE routing) | New topology class |
| **IM** | Infra Maturity | Upstream kernels + stable API | Maintained external libs | Research code only |

---

## Scored Cases (Single-Author Examples — Not a Benchmark)

| Architecture | GA | MAL | STI | IM | Total | Zone | Note |
|:-------------|:--:|:---:|:---:|:--:|:-----:|:----:|:-----|
| Transformer + Flash | 2 | 2 | 2 | 2 | **8** | 🟢 | Reference case |
| GQA | 2 | 2 | 2 | 2 | **8** | 🟢 | Weight-only change |
| MLA | 2 | 2 | 2 | 1 | **7** | 🟢 | DeepSeek-only impl |
| Mixtral MoE | 2 | 1 | 1 | 1 | **5** | 🟡 | See STI revision below |
| Pure Mamba | 1 | 1 | 2 | 1 | **5** | 🟡 | Ceiling at 7B not captured |
| GLA/DeltaNet | 2 | 1 | 2 | 1 | **6** | 🟡 | Qwen uses this |
| KANs | 0 | 0 | N/A | 0 | **~0** | 🔴 | No deployments to verify STI |
| Neural ODEs | 0 | 0 | 1 | 0 | **1** | 🔴 | Never crossed for LLMs |

---

## Composite Interpretation

| Score | Zone | Meaning |
|:-----:|:----:|:--------|
| 7–8 | 🟢 | Drop-in. 12–24 months. |
| 4–6 | 🟡 | Viable with effort. 12–36 months. |
| 2–3 | 🟠 | Research gap. 24–36+ months. |
| 0–1 | 🔴 | Research-only. |

---

## Rubric Revision: STI for MoE (v1.1 proposal)

**Problem:** Mixtral (8 experts) and DeepSeek V3 (256 experts) both score STI=1, but their serving complexity differs significantly.

**Proposed fix:** Split STI into sub-dimensions for conditional computation:

| STI-a (Expert Count) | Score |
|:---------------------|:-----:|
| ≤16 experts | 2 |
| 17–64 experts | 1 |
| 65+ experts | 0 |

| STI-b (Routing) | Score |
|:----------------|:-----:|
| Static top-k | 2 |
| Load-balanced | 1 |
| Dynamic/elastic | 0 |

**Re-scored with revised STI:**
- Mixtral 8×7B: STI-a=2, STI-b=2 → STI=2. New total: **6** (was 5).
- DeepSeek V3: STI-a=0, STI-b=1 → STI=0.5 → round to 1. Total unchanged: **5**.

**Conclusion:** This revision creates meaningful separation. Consider adopting in v1.1.

---

## Stress Tests (Known Failure Modes of v1.0)

1. **Mamba ceiling:** Scores 5 ("viable with effort") but no pure SSM above 7B. Compatibility ≠ scalability. *Status: Known limitation, not fixable with current axes.*

2. **Sparse attention obsolescence:** Would score 6-7, but was replaced by Flash (8). *Status: Rubric doesn't capture competitive dynamics.*

3. **GLA vs Mamba adoption gap:** GLA scores +1 higher but has much more traction due to Alibaba investment. *Status: Ecosystem investment not captured.*

---

## Prospective Predictions (Dec 2025 → Dec 2027)

| Technique | Score | Prediction | Pushes my prior? |
|:----------|:-----:|:-----------|:----------------:|
| Differential Transformer | 6 | Should spread with kernel work | No |
| Titans | 2 | Research-only | Slightly — worse than I expected |
| xLSTM | 5 | May hit Mamba ceiling | No |
| Mixture of Depths | 5 | Serving complexity limits adoption | No |
| GLA/DeltaNet | 6 | Continued adoption | No |

**Honest note:** Only Titans pushes against my prior. The rest confirm what I already believed.

---

## Status

- **External raters:** ❌
- **Prospective predictions:** ✅ (check Dec 2027)
- **Rubric revision from stress test:** ✅ (STI split proposed)

**Use this as:** Illustration of rubric mechanics. **Not as:** Evidence the scorecard predicts adoption.
