# Hardware Compatibility Scorecard v1.0 — Worked Examples (Single-Author Draft)

**Scope:** 2023–2025 NVIDIA GPU stacks (A100/H100, CUDA 12.x, PyTorch 2.x)  
**Status:** Single-author worked examples. Not externally validated. Not evidence the scorecard predicts adoption.

---

## What This Is

Worked examples showing how to apply a 5-axis rubric to known architectures. All cases have known outcomes — this demonstrates the rubric's mechanics, not its predictive power.

**Limitations:** Confirmation bias likely. KM/FSM axes overlap in practice. Composite bands (8-10 green, etc.) are arbitrary. Speculative scores marked N/A.

---

## Axes (0–2 scale, higher = easier to productionize)

| Axis | Measures |
|:-----|:---------|
| **GA** | GEMM-Alignment: % FLOPs in big matmuls |
| **MAL** | Memory Access Locality: HBM↔SRAM efficiency |
| **KM** | Kernel Maturity: upstream vs novel kernels |
| **STI** | Serving Topology Impact: change vs dense Transformers |
| **FSM** | Framework Support Maturity: API stability, docs, CI |

---

## Scored Cases

| Architecture | GA | MAL | KM | STI | FSM | Total | Zone |
|:-------------|:--:|:---:|:--:|:---:|:---:|:-----:|:----:|
| Transformer + Flash | 2 | 2 | 2 | 2 | 2 | **10** | 🟢 |
| GQA | 2 | 2 | 2 | 2 | 2 | **10** | 🟢 |
| MLA | 2 | 2 | 2 | 2 | 1 | **9** | 🟢 |
| Mixtral MoE | 2 | 1 | 1 | 1 | 1 | **6** | 🟡 |
| Pure Mamba | 1 | 1 | 1 | 2 | 1 | **6** | 🟡 |
| KANs | 0 | 0 | 0 | N/A | 0 | **~2** | 🔴 |
| Neural ODEs | 0 | 0 | 0 | 1 | 0 | **1** | 🔴 |

**Note:** KAN's STI is marked N/A — no production deployments exist to verify serving topology assumptions.

---

## Composite Interpretation

| Score | Zone | Meaning |
|:-----:|:----:|:--------|
| 8–10 | 🟢 Green | Drop-in. ~12–24 month adoption. |
| 5–7 | 🟡 Yellow | Viable with effort. ~12–36 months. |
| 3–4 | 🟠 Orange | Research-to-production gap. 24–36+ months. |
| 0–2 | 🔴 Red | Research-only on current hardware. |

---

## Stress Tests

Cases exposing rubric limitations:

1. **Mamba ceiling:** Scores 6 ("viable with engineering") but no pure SSM above 7B exists. Compatibility ≠ scalability.
2. **Sparse attention obsolescence:** Would score 7-8, but was replaced by Flash (10). High score ≠ adoption when better alternatives exist.
3. **MoE variance:** Mixtral (8 experts) and DeepSeek V3 (256 experts) both score 6. Rubric too coarse.

---

## Prospective Predictions (Dec 2025)

Techniques with uncertain outcomes. Check back Dec 2027.

| Technique | Score | Prediction |
|:----------|:-----:|:-----------|
| Differential Transformer | 7 | Should spread if someone invests in kernels |
| Titans (Google) | 2 | Research-only; memory architecture too novel |
| xLSTM | 6 | May hit Mamba-like ceiling |
| Mixture of Depths | 6 | Serving complexity limits adoption |
| GLA/DeltaNet | 7 | More mature than Mamba; Qwen already uses it |

**One finding:** GLA scores +1 vs Mamba but has much higher adoption (Qwen). Suggests ecosystem investment matters more than compatibility for borderline cases.

---

## Known Weaknesses

1. **KM/FSM overlap.** Rarely score differently.
2. **Competitive dynamics ignored.** High score ≠ adoption if alternatives exist.
3. **Scaling not predicted.** Mamba is compatible but doesn't scale.
4. **Ecosystem investment not captured.** GLA's adoption advantage is Alibaba's investment, not hardware fit.

---

## Status

| Criterion | Status |
|:----------|:------:|
| External raters | ❌ |
| Prospective predictions | ✅ 5 cases, check Dec 2027 |
| Genuine finding | ✅ Ecosystem investment may dominate compatibility |

**Conclusion:** Worked examples, not validation. Use to understand rubric mechanics. Does not prove scorecard predicts adoption.
