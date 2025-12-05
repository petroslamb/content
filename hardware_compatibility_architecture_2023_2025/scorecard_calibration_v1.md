# Hardware Compatibility Scorecard v1.0 — Worked Examples & Stress Tests (Single-Author Draft)

**Scope:** 2023–2025 NVIDIA GPU stacks (A100/H100, CUDA 12.x, PyTorch 2.x / JAX+XLA)  
**Scoring date:** December 2025  
**Status:** Single-author draft. Not externally validated.

---

## What This Document Is (And Isn't)

**This is a single-author worked example set, not a validated calibration.**

The scores below show how to apply the rubric to known architectures. They demonstrate the rubric's mechanics, not its predictive power. All cases are archetypal—easy examples where the adoption story is already known. Nothing here forces the rubric to disagree with prior intuitions.

**Explicit limitations:**
1. **Confirmation bias:** Scores were assigned after knowing adoption outcomes.
2. **Axis leakage:** KM and FSM overlap in practice; many justifications blur these axes.
3. **Tautological bands:** Composite thresholds (8-10 = green, etc.) were defined first, then examples scored to fit.
4. **No surprises:** All scored cases are archetypes with known outcomes. The rubric was never forced to tell us something we didn't already believe.
5. **Speculative entries:** KAN's STI=2 is explicitly speculative (no deployments to verify), but still appears in the summary table.

**What would make this a real calibration:**
- **External raters:** 2-3 independent scorers on the same cases. If agreement <80%, revise rubric.
- **Genuinely borderline cases:** Score techniques with unknown outcomes and let the rubric predict something.
- **Prospective test:** Score a new technique before observing adoption; check back in 12-24 months.

---

## Axes Reference

| Axis | Measures | 2 = Best | 0 = Worst |
|:-----|:---------|:---------|:----------|
| **GA** (GEMM-Alignment) | % of FLOPs in big matmuls | ≥90% in GEMMs | <50% in GEMMs |
| **MAL** (Memory Access Locality) | HBM↔SRAM efficiency | Tiled/fused, no O(n²) materialization | Large intermediates, memory-bound |
| **KM** (Kernel Maturity) | Who maintains kernels | Upstream/vendor | You own novel kernels |
| **STI** (Serving Topology Impact) | Change vs dense Transformers | Drop-in | New topology class |
| **FSM** (Framework Support Maturity) | API stability, docs, CI | First-class in major frameworks | Research/prototype only |

---

## Worked Examples

These scores demonstrate how the rubric applies. Justifications aim to be **property-based** (measuring the technique itself) rather than **adoption-based** (who uses it).

---

### 1. Vanilla Transformer + FlashAttention

| Axis | Score | Property-Based Justification |
|:-----|:-----:|:--------------|
| GA | **2** | QKV projections: batched matmul. Attention: QK^T matmul + softmax + V matmul. MLP: two dense matmuls. All dispatch to cuBLAS. No scatter/gather, no per-token branching. |
| MAL | **2** | FlashAttention's algorithm loads Q/K/V blocks into SRAM, computes softmax incrementally, writes output blocks. Full N×N attention matrix never exists in HBM. Measured: ~10-20× memory reduction vs naive at long sequences. |
| KM | **2** | `torch.nn.functional.scaled_dot_product_attention` in PyTorch 2.2+ dispatches to FlashAttention2 backend. No custom CUDA required by user. Kernel maintained by PyTorch core + Dao AI Lab. |
| STI | **2** | Same tensor/pipeline parallel sharding as pre-Flash Transformers. FlashAttention is a kernel swap; serving topology unchanged. |
| FSM | **2** | Stable API: `F.scaled_dot_product_attention`. Documented. CI-backed. Tested against CUDA 11.8-12.x and PyTorch 2.0-2.2+. |
| **Total** | **10** | |

---

### 2. Grouped-Query Attention (GQA)

| Axis | Score | Property-Based Justification |
|:-----|:-----:|:--------------|
| GA | **2** | Identical matmul structure to MHA. Q projection: `[batch, seq, heads, d] @ W_q`. K/V projections: fewer heads, same op type. No new compute patterns. |
| MAL | **2** | KV cache per token: `num_kv_heads × d` instead of `num_heads × d`. 8 query heads sharing 1 KV head → 8× reduction in KV cache size and bandwidth. |
| KM | **2** | No new kernels. Same attention kernels as MHA. The only change is weight tensor shapes in model definition. |
| STI | **2** | KV cache is smaller but same structure. No sharding changes. No routing. |
| FSM | **2** | Supported in HuggingFace `transformers`, PyTorch, JAX. Config change: `num_key_value_heads` parameter. Standard model loading. |
| **Total** | **10** | |

---

### 3. Multi-Head Latent Attention (MLA)

| Axis | Score | Property-Based Justification |
|:-----|:-----:|:--------------|
| GA | **2** | Down-projection: `[batch, seq, d] @ W_down → [batch, seq, latent_d]`. Up-projection for attention. All dense matmuls. |
| MAL | **2** | KV cache stores latent vectors (smaller than full K/V). Cache size: `latent_d` per token instead of `heads × d_k`. Designed for 128K+ context. |
| KM | **2** | Standard linear layers (nn.Linear). No novel kernel semantics. Projection shapes differ from MHA but use same cuBLAS primitives. |
| STI | **2** | Same sharding as dense attention. Latent dimension is a model config, not a topology change. |
| FSM | **1** | Not in vanilla PyTorch. Requires DeepSeek's model code or manual implementation. No upstream API. HuggingFace has DeepSeek models but not a generic MLA module. |
| **Total** | **9** | |

---

### 4. Mixtral-style MoE (8×7B)

| Axis | Score | Property-Based Justification |
|:-----|:-----:|:--------------|
| GA | **2** | Expert FFNs: standard dense matmuls (`W1`, `W2`, `W3`). Router: small matmul + top-k. >95% FLOPs in cuBLAS ops. |
| MAL | **1** | Expert weights (~7B × 8 = 56B params) resident in HBM. Per-token routing means different experts activated → weight loading patterns less predictable. At high expert counts or low batch size, weight movement becomes bottleneck. Not tiled like Flash. |
| KM | **1** | Requires MoE-specific dispatch kernels (token-to-expert routing, sparse matmul). MegaBlocks, Triton MoE kernels exist and are maintained. Not upstream in vanilla PyTorch. |
| STI | **1** | Experts must be sharded. Router load balancing at inference. All-to-all communication for distributed expert placement. Frameworks like vLLM and TensorRT-LLM support Mixtral, but required explicit MoE extensions. |
| FSM | **1** | HuggingFace `transformers` supports Mixtral. vLLM has MoE backend. But: requires MoE-aware serving stack, not vanilla `model.generate()`. Lag behind dense model support in new features. |
| **Total** | **6** | |

---

### 5. Pure Mamba / SSM (Falcon Mamba 7B)

| Axis | Score | Property-Based Justification |
|:-----|:-----:|:--------------|
| GA | **1** | Input/output projections: dense matmuls. **Core SSM operation: parallel scan over states.** The selective scan is NOT a GEMM — it's an associative scan with per-position gating. Estimated: 60-70% FLOPs in matmuls, 30-40% in SSM ops. |
| MAL | **1** | No O(n²) attention matrix — good. But: state is updated per position, written/read per layer. Not Flash-level fusion across sequence. Better than naive attention, worse than FlashAttention. |
| KM | **1** | `mamba-ssm` package provides CUDA kernels for selective scan. Maintained by Mamba authors. Used in production at small/medium scale (TII Falcon). Not upstream in PyTorch/JAX. |
| STI | **2** | No routing, no expert sharding. Dense tensor structure. Same parallelism patterns as dense Transformer. |
| FSM | **1** | Requires `mamba-ssm` or `causal-conv1d` packages. Not in vanilla PyTorch. HuggingFace has Mamba models but it's an external dependency, not built-in. |
| **Total** | **6** | |

**⚠️ RUBRIC CRACK:** Mamba scores 6 (Yellow = "viable with engineering"), but there's no public evidence of pure SSM scaling past 7B. The rubric predicts "should work with effort"; reality shows a ceiling. **This is a failure of the rubric's predictive power** — compatibility alone doesn't predict scaling success.

---

### 6. KANs (Kolmogorov-Arnold Networks)

| Axis | Score | Property-Based Justification |
|:-----|:-----:|:--------------|
| GA | **0** | Core operation: per-edge spline evaluation. Each edge has learnable B-spline basis functions evaluated per token. Not expressible as batched dense matmuls. Tensor cores largely idle. |
| MAL | **0** | Many small, irregular ops. Spline coefficients accessed per edge, per token. No natural tiling structure. Memory access patterns don't coalesce across tokens. |
| KM | **0** | No production-grade GPU kernels. Reference implementations use PyTorch tensor ops (slow) or experimental CUDA. No maintained library. |
| STI | **2** | Would use standard dense topology IF deployed. No routing. This is speculative — no production deployments exist to verify. |
| FSM | **0** | Research code only. `pykan` repo exists but not optimized for scale. Breaks with framework updates. |
| **Total** | **2** | |

---

### 7. Neural ODEs

| Axis | Score | Property-Based Justification |
|:-----|:-----:|:--------------|
| GA | **0** | ODE solvers (Dormand-Prince, RK45) are iterative. Each step: evaluate network, compute gradients, update state. Many small matmuls per forward pass. Tensor cores underutilized due to iteration overhead. |
| MAL | **0** | Repeated function evaluations through same network weights. Hard to fuse across solver steps. Solver state written/read repeatedly. |
| KM | **0** | `torchdiffeq` exists but not optimized for LLM-scale inference. No production-grade ODE kernels integrated with serving stacks. |
| STI | **1** | Variable compute depth (solver steps depend on tolerance). Complicates batching — different sequences may need different steps. Not completely incompatible, but not predictable resource usage. |
| FSM | **0** | `torchdiffeq` is maintained but research-focused. Not tested against production workloads. No CI for LLM-scale. |
| **Total** | **1** | |

---

## Stress Tests: Where the Rubric Might Break

These cases expose limitations of the current rubric.

---

### Stress Test 1: Sparse Attention (BigBird, Longformer)

**The question:** Block-sparse attention reduces O(n²) to O(n). Some production use (early long-context models). Why didn't it become default like Flash?

| Axis | Tentative Score | Reasoning |
|:-----|:---------------:|:----------|
| GA | 2 | Block-sparse matmuls still dispatch to GEMMs (just smaller blocks). |
| MAL | 1-2 | Avoids full O(n²), but irregular block patterns may fragment memory access. |
| KM | 1 | Required custom kernels (DeepSpeed, Triton sparse). Not upstream. |
| STI | 2 | Same serving topology as dense. |
| FSM | 1 | External libraries. Never hit vanilla PyTorch. |
| **Total** | **7-8** | |

**The problem:** Score 7-8 = Green/Yellow, predicting adoption. But sparse attention was **replaced** by FlashAttention, not adopted broadly. Flash (score 10) solved the same problem more completely.

**Interpretation:** High score doesn't guarantee adoption — a higher-scoring alternative can obsolete you. The rubric measures compatibility, not competitive position.

---

### Stress Test 2: Linear Attention (RetNet, RWKV)

**The question:** RWKV has a real community and production deployments. How does it compare to Mamba (also score 6)?

| Axis | Tentative Score | Reasoning |
|:-----|:---------------:|:----------|
| GA | 1 | Linear attention is matrix multiplications, but with different structure (no softmax). Still fundamentally matmul-based. |
| MAL | 1-2 | No O(n²) matrix. Recurrent formulation has state per position. Similar to Mamba. |
| KM | 1 | RWKV has maintained CUDA kernels (rwkv package). Not upstream. |
| STI | 2 | Standard dense topology. |
| FSM | 1 | HuggingFace supports RWKV. External package required for kernels. |
| **Total** | **6-7** | |

**The problem:** RWKV scores ~6, same as Mamba. But RWKV has more production traction (real community, models up to 14B). Mamba has more research prestige but less deployment. The rubric doesn't distinguish them.

**Interpretation:** The rubric measures hardware compatibility, not product-market fit or community momentum.

---

### Stress Test 3: Speculative Decoding

**The question:** Speculative decoding is spreading rapidly in production. Is it even in scope?

**Answer:** Speculative decoding is a **serving optimization**, not an architecture primitive. It doesn't change the model — it changes how inference is scheduled (draft + verify). The rubric doesn't apply; this is out of scope.

**Meta-lesson:** Clearly define scope. The rubric is for architecture primitives, not serving tricks, training recipes, or quantization schemes.

---

### Stress Test 4: The Mamba Ceiling Problem

**The problem:** Mamba scores 6 (Yellow = "viable with engineering"). But:
- No pure SSM above 7B in public record
- All large SSM deployments are hybrids
- The rubric predicted "should work with effort"; reality shows a ceiling

**Possible explanations:**
1. **Training dynamics:** SSMs may require different training recipes that haven't been developed yet. This is outside the rubric's scope.
2. **In-context learning:** SSMs may struggle with long-range arbitrary dependencies that attention handles. This is an architectural limitation, not hardware compatibility.
3. **Investment:** No major lab has seriously tried to scale pure SSM. Absence of evidence ≠ evidence of absence.

**Interpretation:** The rubric measures "can you ship this on current hardware?" It doesn't measure "does the architecture work at frontier scale?" Those are different questions.

---

### Stress Test 5: MoE Variance

**The problem:** Mixtral (8 experts) and DeepSeek V3 (256 experts with auxiliary losses) both score 6. But their serving complexity is very different.

**Possible fix:** Add granularity. Break STI into:
- **STI-a (Expert count complexity):** 8 experts = 2, 64 experts = 1, 256+ = 0
- **STI-b (Routing complexity):** Static top-k = 2, Load-balanced = 1, Dynamic elastic = 0

**Status:** Not implemented. Current rubric is too coarse for MoE variants.

---

## Prospective Predictions: Genuinely Uncertain Cases

These techniques have **unknown adoption outcomes** as of December 2025. The rubric predicts something; we'll see if it's right.

---

### Prediction 1: Differential Transformer (Microsoft, Oct 2024)

**What it is:** Subtracts one attention map from another to reduce noise. Claims 65% efficiency with comparable quality.

**My prior:** "This should spread quickly — it's a drop-in attention variant with no new primitives."

| Axis | Score | Reasoning |
|:-----|:-----:|:----------|
| GA | **2** | Still all matmuls. QK₁^T - QK₂^T is just two attention computations followed by subtraction. cuBLAS throughout. |
| MAL | **2** | Should be implementable with Flash-style tiling. Two attention streams, but same memory access patterns. No O(n²) materialization required. |
| KM | **1** | Not upstream. Requires custom implementation. But the kernels are attention kernels — known class, should be straightforward to adapt FlashAttention. |
| STI | **2** | Same serving topology as standard attention. No routing, no sharding changes. |
| FSM | **0** | Research code only as of Dec 2025. Open-source on GitHub but not in any framework. No docs, no CI. |
| **Total** | **7** | |

**Rubric prediction:** Yellow zone (7). Should be adoptable with kernel work. Expect 12-24 months if someone invests.

**Current status (Dec 2025):** Research only. No production deployments. Microsoft hasn't integrated into Azure models.

**Test:** If Differential Attention is standard by Dec 2027, rubric predicts correctly. If it's abandoned, we need to understand why (competing techniques? no real advantage? something else?).

**Does this surprise me?** **No.** Score 7 aligns with my intuition: good idea, needs kernel investment, not blocking. The rubric confirms my prior.

---

### Prediction 2: Titans (Google, Jan 2025)

**What it is:** Neural long-term memory architecture with "surprise" metric for memory management. Claims 2M+ token context.

**My prior:** "This sounds complex. Memory retrieval during inference could be a topology nightmare."

| Axis | Score | Reasoning |
|:-----|:-----:|:----------|
| GA | **1** | Memory retrieval/update involves custom operations beyond standard matmuls. The "surprise" metric computation and adaptive forgetting are not GEMM-friendly. Some matmuls in attention portions. |
| MAL | **1** | Memory modules require reading/writing persistent state. Not clear how tiled this can be. Long-term memory implies HBM traffic for state management. |
| KM | **0** | No implementations exist outside Google Research paper. Novel kernel semantics for memory operations. You'd own all of this. |
| STI | **0** | Persistent memory across requests? Memory updates during inference? This could require fundamentally new serving paradigms. Not compatible with stateless request handling. |
| FSM | **0** | Paper-only. No code released (as of Dec 2025). |
| **Total** | **2** | |

**Rubric prediction:** Red zone (2). Research-only on current stacks. Expect 36+ months if ever.

**Current status (Dec 2025):** Paper just released. No known implementations outside Google.

**Test:** If Titans-style memory becomes standard by 2027, rubric is WRONG. If it remains research-only or is heavily modified to remove the hard parts, rubric is right.

**Does this surprise me?** **Slightly.** My prior was "complex but Google might push it." The rubric says "red zone, unlikely." If Google has internal Titans deployments by 2026, the rubric missed something (institutional investment can override compatibility concerns).

---

### Prediction 3: xLSTM (May 2024)

**What it is:** Extended LSTM with exponential gating. mLSTM uses matrix memory. Claims competitive with Transformers at scale.

**My prior:** "Recurrent architectures have fundamental parallelism problems. This probably hits the same ceiling as Mamba."

| Axis | Score | Reasoning |
|:-----|:-----:|:----------|
| GA | **1** | Matrix memory (mLSTM) adds more matmul operations than original LSTM. But recurrent structure means sequential state dependencies. Not fully GEMM-friendly. |
| MAL | **1** | State is updated per position. Better than O(n²) but not Flash-level. Repeated state read/write per layer. |
| KM | **1** | NXAI (Hochreiter's company) maintains implementations. Some CUDA kernels exist. Not upstream. |
| STI | **2** | Standard dense topology. No routing, no expert sharding. Same parallelism patterns as transformers at layer level (pipeline/tensor parallel). |
| FSM | **1** | External packages exist. HuggingFace has some support. Active development at NXAI. |
| **Total** | **6** | |

**Rubric prediction:** Yellow zone (6). Same as Mamba. "Viable with engineering" but may hit scaling ceiling.

**Current status (Dec 2025):** 7B models demonstrated. NXAI developing commercial products. No frontier-scale (70B+) deployments.

**Test:** If xLSTM reaches 70B+ in production, rubric was too pessimistic about recurrent architectures. If it stalls at 7-14B like Mamba, rubric correctly identified the pattern.

**Does this surprise me?** **No.** Score 6 matches Mamba, which matches my intuition. But this is a weak prediction — I already believe recurrent architectures hit a ceiling.

---

### Prediction 4: Mixture of Depths (Google, April 2024)

**What it is:** Skip layers dynamically per-token. Some tokens get full compute, others bypass layers.

**My prior:** "This should be easier than MoE — you're not adding experts, just skipping. But variable compute might complicate batching."

| Axis | Score | Reasoning |
|:-----|:-----:|:----------|
| GA | **2** | When compute happens, it's standard matmuls. Skipping is just conditional bypass. No new primitives. |
| MAL | **2** | Skipped layers = less compute and less memory traffic. If anything, this improves MAL. |
| KM | **1** | Requires custom logic for conditional layer execution. Not upstream. But simpler than MoE routing — just a binary skip decision. |
| STI | **1** | Variable compute per token complicates batching. Different tokens in a batch may need different layers. Not as bad as MoE (no routing across experts), but not drop-in either. Inference serving needs to handle variable paths. |
| FSM | **0** | Paper code only. Not in HuggingFace or any serving framework. |
| **Total** | **6** | |

**Rubric prediction:** Yellow zone (6). Same complexity tier as MoE. Needs serving work, but no fundamental blockers.

**Current status (Dec 2025):** Google using internally in some capacity (inferred from efficiency focus). No public models released with MoD.

**Test:** If MoD becomes standard in LLM serving by 2027, rubric is correct. If it's quietly abandoned in favor of MoE (which already has infrastructure), rubric would have missed competitive dynamics.

**Does this surprise me?** **Mildly.** I expected maybe score 7-8 (easier than MoE). The STI penalty for variable compute brings it down to 6said. This could be right — dynamic layer skipping is legitimately harder to batch than static graphs.

---

### Prediction 5: Gated Linear Attention (GLA) / DeltaNet

**What it is:** Linear attention with data-dependent gating. Qwen3-Next uses Gated DeltaNet. Nemotron-Flash-1B uses DeltaNet+Mamba2 hybrid.

**My prior:** "This is more mature than pure Mamba — actual production deployments exist. Should score higher."

| Axis | Score | Reasoning |
|:-----|:-----:|:----------|
| GA | **1-2** | Linear attention is more GEMM-friendly than selective scan, but gating adds per-position operations. Estimates vary. Call it 1.5 → round to **2** because the linear structure avoids Mamba's parallel scan. |
| MAL | **1** | Linear-time complexity, but state updates per position. Similar to Mamba. Not Flash-level fusion. |
| KM | **1** | fla package (fla-org/flash-linear-attention) provides Triton kernels. Actively maintained. Not upstream. Used by Qwen. |
| STI | **2** | Standard dense topology. No routing. |
| FSM | **1** | External packages. HuggingFace supports Qwen3-Next. sglang/vLLM deployment guides exist. |
| **Total** | **7** | |

**Rubric prediction:** Yellow zone (7). More mature than pure Mamba. Should see continued adoption.

**Current status (Dec 2025):** Qwen3-Next deployed. Nemotron-Flash uses DeltaNet. Real production deployments exist.

**Surprise check:** Score 7 vs Mamba's 6 — GLA scores HIGHER. This suggests it should have better adoption. **This matches reality** (Qwen3-Next is more production-ready than Falcon Mamba).

**Does this surprise me?** **Actually yes.** I expected to confirm my prior (GLA > Mamba). But the rubric gave only +1 point difference, which seems small given the apparent adoption gap. Either:
1. The rubric is correctly detecting that the compatibility difference is small, and adoption difference is driven by other factors (Alibaba's investment, not compatibility).
2. Or GLA should score 8, not 7.

This is a **genuine finding**: the rubric suggests GLA's adoption advantage over Mamba is NOT primarily about hardware compatibility — it's about ecosystem investment.

---

## Summary of Prospective Predictions

| Technique | Score | Prediction | Can Falsify By |
|:----------|:-----:|:-----------|:---------------|
| Differential Transformer | 7 | Yellow; adoptable with kernel work | If abandoned despite low barriers → rubric wrong |
| Titans | 2 | Red; research-only | If deployed at scale by 2027 → rubric wrong |
| xLSTM | 6 | Yellow; may hit Mamba-like ceiling | If scales to 70B+ → rubric too pessimistic |
| Mixture of Depths | 6 | Yellow; serving complexity hurts | If becomes standard → rubric right; if abandoned → competitive dynamics matter more |
| GLA/DeltaNet | 7 | Yellow; more mature than Mamba | Already partially confirmed — production deployments exist |

**One genuine finding:** GLA's score (7) is only +1 higher than Mamba (6), but GLA has significantly more production traction. This suggests the rubric measures compatibility but **not** ecosystem investment, which may be a larger driver of adoption for borderline techniques.

---

## Known Rubric Weaknesses

1. **KM and FSM overlap.** If kernels are upstream (KM=2), framework support is usually mature (FSM=2). Independent scoring is difficult.

2. **Adoption-based reasoning creeps in.** It's hard to score FSM without mentioning who uses the technique. Property-based framing: "Is there a stable API with docs and CI?" But verifying this requires checking adoption.

3. **Competitive dynamics ignored.** High score ≠ adoption. A technique can be compatible but lose to a more compatible alternative (sparse attention vs Flash).

4. **Scaling success not predicted.** Compatibility ≠ scalability. Mamba is compatible (score 6) but hasn't scaled past 7B. The rubric doesn't explain why.

5. **Composite bands are arbitrary.** Why is 8-10 "green" and 5-7 "yellow"? These thresholds were set by intuition, not derived from data.

6. **Ecosystem investment not captured.** (New finding from prospective predictions.) GLA scores 7 vs Mamba's 6 — only +1 difference — but GLA has significantly more production traction due to Alibaba's investment in Qwen. The rubric measures hardware compatibility, not "who is pushing this." Institutional backing may matter more than compatibility for borderline techniques.

---

## What Would Strengthen This

1. **External raters.** Have 2-3 ML infra engineers score the same 10 cases. If agreement <80%, revise rubric definitions.

2. **Predictive test.** Score a new technique BEFORE observing adoption. Check back in 12-24 months. Currently all scoring is retrospective.

3. **Failure cases.** Find a technique that scores high but failed, or scores low but succeeded. These would force rubric revision.

4. **Finer granularity for MoE.** Current STI doesn't distinguish 8-expert from 256-expert designs.

---

## Summary Table

| Architecture | GA | MAL | KM | STI | FSM | Total | Zone | Notes |
|:-------------|:--:|:---:|:--:|:---:|:---:|:-----:|:----:|:------|
| Transformer + Flash | 2 | 2 | 2 | 2 | 2 | **10** | 🟢 | Reference case |
| GQA | 2 | 2 | 2 | 2 | 2 | **10** | 🟢 | Weight-only change |
| MLA | 2 | 2 | 2 | 2 | 1 | **9** | 🟢 | FSM limited by DeepSeek-only impl |
| Mixtral MoE | 2 | 1 | 1 | 1 | 1 | **6** | 🟡 | Coarse; doesn't capture expert variance |
| Pure Mamba | 1 | 1 | 1 | 2 | 1 | **6** | 🟡 | ⚠️ Ceiling not predicted by score |
| KANs | 0 | 0 | 0 | 2 | 0 | **2** | 🔴 | STI=2 is speculative |
| Neural ODEs | 0 | 0 | 0 | 1 | 0 | **1** | 🔴 | Never crossed for LLMs |

---

## Calibration Status

| Criterion | Status |
|:----------|:------:|
| External raters | ❌ Not done |
| Prospective predictions | ✅ 5 uncertain techniques scored (Dec 2025); check back Dec 2027 |
| Failure cases identified | ⚠️ Mamba ceiling, sparse attention obsolescence, GLA vs Mamba adoption gap |
| Property-based justifications | ⚠️ Partial; adoption creeps in |
| Stress tests documented | ✅ Done |
| Genuine finding | ✅ Ecosystem investment may dominate compatibility for borderline techniques |

**Conclusion:** This is now a worked example set WITH prospective predictions. The 5 uncertain cases (Differential Transformer, Titans, xLSTM, Mixture of Depths, GLA/DeltaNet) can be checked in 24 months to test predictive power. One genuine finding emerged: ecosystem investment (not captured by the rubric) may explain adoption gaps better than hardware compatibility for techniques in the yellow zone.

---

## Glossary: Axes Reference

### GA — GEMM-Alignment

**What it measures:** The percentage of floating-point operations (FLOPs) in the technique's forward pass that execute as large, batched dense matrix multiplications (GEMMs) on tensor cores.

**Why it matters:** Modern GPUs (A100, H100) are optimized around tensor cores that perform dense matrix multiplications extremely efficiently. Operations that cannot be expressed as GEMMs—scatter/gather, per-token branching, iterative solvers—leave tensor cores idle and underutilize the hardware.

**Scoring:**
- **2:** ≥90% of FLOPs in batched dense matmuls/convolutions backed by cuBLAS/cuDNN. Control flow and elementwise ops are negligible overhead.
- **1:** 50–90% of FLOPs in GEMMs, but a significant fraction in irregular operations that can bottleneck at scale.
- **0:** <50% of FLOPs in GEMMs, or key steps cannot be decomposed into large matmuls without algorithm changes.

---

### MAL — Memory Access Locality

**What it measures:** How efficiently the technique uses the GPU memory hierarchy—specifically, how much it minimizes data movement between HBM (high-bandwidth memory, off-chip, slower) and SRAM (on-chip cache, faster).

**Why it matters:** Memory bandwidth, not compute, is often the bottleneck. Techniques that tile computation into SRAM, fuse operations to avoid intermediate writes, and avoid materializing large tensors (like O(n²) attention matrices) run faster than those that repeatedly read/write from HBM.

**Scoring:**
- **2:** Critical paths are tiled/fused. Key tensors load once into SRAM and are reused. O(n²) intermediates avoided. Example: FlashAttention.
- **1:** Some tiling/fusion, but large intermediates or repeated HBM traffic become bottlenecks at scale.
- **0:** Routinely materializes large tensors and re-reads from HBM. Kernel is clearly memory-bound.

---

### KM — Kernel Maturity

**What it measures:** Who maintains the GPU kernel code required to execute this technique efficiently.

**Why it matters:** Novel techniques often require custom CUDA or Triton kernels. If you must write, optimize, and maintain these kernels yourself, the integration cost is high and the risk of bugs or performance regressions increases. If kernels are upstream in PyTorch/JAX or maintained by a vendor, the burden is shared.

**Scoring:**
- **2:** Implementable using only upstream kernels from major frameworks (PyTorch, JAX) or vendor libraries (cuBLAS, cuDNN). No custom GPU code required.
- **1:** Requires additional kernels, but they exist as actively maintained open-source implementations used in production. You integrate, not invent.
- **0:** Requires novel kernel semantics with no production-grade implementation. You own the entire kernel lifecycle.

---

### STI — Serving Topology Impact

**What it measures:** How much the serving infrastructure must change compared to a standard dense Transformer LLM stack (tensor parallelism, pipeline parallelism, static graphs).

**Why it matters:** Serving infrastructure is expensive to modify. Techniques that require new sharding strategies, routing logic, load balancing, or communication patterns take longer to deploy and are harder to maintain. Drop-in replacements (like FlashAttention) spread faster than techniques requiring topology changes (like MoE).

**Scoring:**
- **2:** Works with same parallelization/topology as dense Transformers. No new routing, sharding, or load-balancing required.
- **1:** Requires localized changes (e.g., static expert placement, router load balancing) but fits existing framework concepts.
- **0:** Requires qualitatively new topology: dynamic expert movement, non-standard consistency protocols, or complex scheduling.

---

### FSM — Framework Support Maturity

**What it measures:** The stability and completeness of framework-level integration—APIs, documentation, CI testing, and compatibility with current software stacks.

**Why it matters:** Even if kernels exist, poor API design, missing documentation, or lack of CI means the technique will break unexpectedly across framework or driver upgrades. First-class framework support (stable APIs, tested against multiple CUDA versions) reduces friction and accelerates adoption.

**Scoring:**
- **2:** Exposed through stable, documented APIs in a major framework's standard release. CI-backed. Compatible with current CUDA/driver stacks.
- **1:** Available via actively maintained third-party libraries that integrate with major frameworks but are not upstream. May lag releases.
- **0:** Only research/prototype code. No maintained library. Frequent breakage with framework updates.
