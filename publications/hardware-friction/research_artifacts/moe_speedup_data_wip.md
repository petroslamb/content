# MoE Speedup Data Collection & 2025 Reality Check

## Sources Collected (Day 1 - Batch 1)

### 1. Switch Transformers (Fedus et al., 2021)
**Source:** arXiv:2101.03961
**Claims:**
- 7× pre-training speedup for T5-Base/Large-based models
- 4× speedup vs T5-XXL for trillion parameter models
- 5× mean speedup over mT5-Base (multilingual, 91% languages >4×)

**Context:** Pre-training speedup, compared to dense equivalents
**Expert config:** Not specified in summary (need full paper)

---

### 2. Mixtral 8×7B (Mistral AI, 2024)
**Source:** Official technical report
**Claims:**
- 6× faster inference than Llama 2 70B on most benchmarks
- 46.7B total params, 12.9B active per token
- Matches/outperforms GPT-3.5 on majority of benchmarks

**Hardware-specific (NVIDIA H100 + TensorRT-LLM):**
- FP8 precision: 50% more throughput vs FP16
- 38.4 requests/second streaming mode
- 21,000 tokens/second at batch size 1,024

**Context:** Inference speedup, production deployment
**Expert config:** 8 experts, 2 active per token

---

### 3. DeepSeek-V3 (DeepSeek AI, Dec 2024)
**Source:** arXiv technical report
**Specs:**
- 671B total parameters, 37B active per token
- State-of-the-art on MMLU (88.5), MATH-500 (90.2%), HumanEval (65.2%)
- Training efficiency: 2.788M H800 GPU hours

**Performance:**
- Outperforms GPT-4o on MATH-500
- Comparable to Claude-3.5 Sonnet on knowledge benchmarks
- Top coding competition performance (LiveCodeBench)

**Note:** Doesn't specify direct speedup claim vs dense, but demonstrates efficiency at massive scale
**Expert config:** MoE with MLA (Multi-head Latent Attention)

---

### 4. Expert Choice Routing (Google Research, NeurIPS 2022)
**Source:** NeurIPS 2022 paper
**Claims:**
- 2× faster training convergence at 8B/64E scale vs top-2 gating
- Improved perplexity scaling as experts increase
- Outperforms T5 dense in 7/11 GLUE/SuperGLUE tasks with smaller activation cost

**Key innovation:** Perfect load balancing, variable experts per token
**Context:** Training speedup, load balancing improvement

---

### 5. MoE Deployment Inefficiencies Study (2023)
**Source:** arXiv:2303.06182 "Towards MoE Deployment"
**CRITICAL FINDING - THE REALITY CHECK:**
- MoE can be **15× SLOWER** for LM, **3× slower** for MT vs FLOP-equivalent dense models
- Reason: Communication overhead, low GPU utilization

**Optimization results:**
- Dynamic gating improves throughput 6.21-11.23× for LM
- Reduces memory up to 1.36×

**This is the HONEST data:** Without optimization, MoE is slower. With optimization, gets speedup.

---

### 6. Aurora System (2024)
**Source:** arXiv "Optimizing MoE Inference Time"
**Claims:**
- 2.38× speedup in homogeneous clusters
- 3.54× speedup in heterogeneous GPU environments
- 1.5× GPU utilization improvement

**Focus:** System-level optimization addressing communication overhead

---

### 7. MoE-Inference-Bench (2024/2025)
**Source:** Benchmarking suite
**Findings:**
- FP8 quantization: 20-30% higher throughput vs FP16 on H100
- No significant accuracy loss with FP8

---

## Initial Analysis (Pre‑2025 Data)

### Speedup Claims Distribution
**Pre-training:**
- Switch: 4-7× (vs dense equivalent)
- Expert Choice: 2× convergence

**Inference:**
- Mixtral: 6× (vs Llama 2 70B, likely marketing claim)
- Aurora: 2.38-3.54× (system optimization)
- MoE without optimization: 0.07-0.33× (3-15× SLOWER!)

**Reality Check Pattern (pre‑2025):**
- Marketing claims: 5–7×
- Optimized systems: 2–3.5×
- Poorly implemented: 0.07–0.33× (negative speedup!)

### Updated 2025 View (DeepSeek‑V3/R1, FlashInfer, New Benchmarks)

The 2025 literature search (consolidated in `EXHAUSTIVE_FINAL_COMPILATION.md`, plus the DeepSeek‑V3 report and MoE deployment studies) refines this picture:

- **DeepSeek‑V3 (671B / 37B active):**
  - Confirms MoE at true frontier scale with competitive training cost (~US$6M reported).
  - Uses MLA + MoE to keep active parameters low while matching or beating dense baselines.
- **Frontier MoE deployments (2024–2025):**
  - Consistently report **≈2–3× throughput gains** vs dense models of similar quality when systems are well‑engineered (expert sharding, communication optimization, FP8, router tweaks).
  - Latency improvements per single stream are more modest; main benefit is tokens/sec/$ at scale.
- **FlashInfer (2025):**
  - Adds an additional **≈1.3–1.7×** latency reduction on top of existing MoE kernels for some serving setups, tightening the “realistic” speedup range.

### Consolidated 2025 Numbers

- **Marketing narrative:** “5–7× faster” persists in launch materials.
- **Realistic production range:** **≈2–3× tokens/sec** vs dense models of comparable quality at moderate context.


**Honest median estimate (Dec 2025):** ≈2–3× throughput improvement for well‑optimized MoE deployments, with strong variance based on system quality.

---

## Status

- Dataset now incorporates:
  - Early MoE literature (Switch, Expert Choice, deployment‑inefficiency work).
  - 2024–2025 frontier models (Mixtral‑8×7B, DeepSeek‑V3) and serving libraries (FlashInfer).
- Used directly in:
  - `long_article_sections/Act_II_The_Conditional_Execution_Revolution.md`
  - `long_article_sections/Appendix_Evidence.md` (Table 2: “MoE Reality Check”).

Further additions should focus on **new large‑scale deployment case studies**, not small‑scale toy benchmarks.
