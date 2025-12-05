# Hardware Friction Map — A+++ Research Supplement (Draft v0.1)

**Goal:** Provide enough structured evidence and counter‑evidence for the Hardware Friction Map thesis to upgrade the essay from “strong manifesto” to **A+++‑grade**, evidence‑backed Gate‑1 framework for 2023–2025 GPU‑based LLM architectures.

This file is meant to be read alongside:
- `research_artifacts/EXHAUSTIVE_FINAL_COMPILATION.md`
- `research_artifacts/moe_speedup_data_wip.md`
- `research_artifacts/flash_attention_timeline.md`
- `research_artifacts/ssm_benchmark_findings.md`
- `research_artifacts/major_lab_architecture_audit.md`

It does **not** re‑argue the core thesis. Instead it:
1. Extends the adoption dataset beyond GQA / Flash / MoE.  
2. Provides **negative cases** (where friction alone doesn’t explain outcomes).  
3. Adds **forward‑looking predictions** tied directly to the map, with falsifiable conditions.

---

## 1. Scope and Definitions

**Scope (explicit):**
- Domain: 2023–2025 frontier‑scale *LLM‑style* architectures on NVIDIA‑class GPU clusters.  
- Gate: **Gate 1** only — hardware + infra viability (“friction”).  
- Excluded: Training algorithms, data, safety constraints, product/market factors except where noted.

**Friction Axes (from scorecard):**
- `GA` — GEMM Alignment (kernel shape)  
- `MAL` — Memory Access / Locality  
- `PAR` — Parallelism (training)  
- `STI` — Serving Topology change  
- `IM` — Infra Maturity (upstream kernels & tooling)

We approximate “zones” (Green/Yellow/Orange/Red) with these axes:
- **Green:** High `GA`, good `MAL`, parallel training (`PAR` good), `STI`=drop‑in, `IM`=mature.  
- **Yellow:** Good hardware axes but non‑trivial `STI` or `IM` burden (kernel or serving work).  
- **Orange/Red:** Low `GA`/`MAL`/`PAR` (hardware hostile) regardless of `STI`/`IM`.

---

## 2. Extended Adoption Dataset (More Than 3 Points)

This section extends the friction/adoption table to include several additional primitives beyond the “canonical three” (GQA, Flash, MoE).

### 2.1 Weight‑Only / Architectural Tweaks (Mostly Green)

These are **Gate‑1 Green**: they change weights or local structure but require no new kernel classes and no serving topology changes.

#### 2.1.1 RoPE (Rotary Position Embeddings)

- **Type:** Positional encoding / weight‑only.  
- **Friction:**  
  - `GA` – High (still matmuls).  
  - `MAL` – Neutral (same memory pattern as vanilla attention).  
  - `PAR` – High (no new sequential dependencies).  
  - `STI` – None; architecture‑internal.  
  - `IM` – Fully supported in all major frameworks by 2024.  
- **Adoption:**  
  - Used in Llama 2, Llama 3, Mistral 7B, Gemma, Qwen families, etc.  
  - Effective standard for 2023–2025 LLMs.  
- **Timeline:** Roughly ≤1 retrain cycle (sub‑18 months) from early RoPE papers to universal use in open‑weights LLMs.  
- **Takeaway:** Archetypal weight‑only Green primitive: easy to adopt, quickly becomes default.

#### 2.1.2 RMSNorm (Root‑Mean‑Square LayerNorm)

- **Type:** Normalization change (LayerNorm→RMSNorm).  
- **Friction:**  
  - `GA` – High; same matmul kernels.  
  - `MAL` – Same as LayerNorm.  
  - `PAR` – Unchanged.  
  - `STI` – None.  
  - `IM` – Implementable in a few lines; widely available.  
- **Adoption:**  
  - Used by Llama, Gemma, Qwen, DeepSeek, etc.  
  - Essentially standard in modern LLMs by 2024.  
- **Timeline:** Similar to RoPE — a couple of major releases.  
- **Takeaway:** Another strong Green. Confirms that “LayerNorm→RMSNorm” level changes diffuse quickly when they touch only weights/graph internals.

#### 2.1.3 LoRA / QLoRA (Low‑Rank Adapters)

- **Type:** Fine‑tuning method; doesn’t change base architecture.  
- **Friction:**  
  - `GA` – High (still matmuls).  
  - `MAL` – Adds small extra matrices; negligible.  
  - `PAR` – Intact.  
  - `STI` – None for base serving; adapters sometimes merged or kept separate.  
  - `IM` – Very strong; multiple open libraries, framework support.  
- **Adoption:**  
  - De facto standard for community‑scale fine‑tuning; widely used in 2023–2025.  
  - Less central at frontier labs (who often fine‑tune full weights), but ubiquitous in open ecosystem.  
- **Timeline:** <12 months from popularization to standard practice in open‑source LLM ecosystem.  
- **Takeaway:** Confirms that **Green + direct cost savings** (training compute) → extremely fast adoption.

### 2.2 Kernel‑Level Changes (Yellow)

These require new kernels but preserve overall serving topology.

#### 2.2.1 FlashAttention (Recap, Extended)

Already covered in `flash_attention_timeline.md` and `EXHAUSTIVE_FINAL_COMPILATION.md`, but included here for completeness.

- **Type:** Attention kernel rewrite.  
- **Friction:**  
  - `GA` – High (remains GEMM‑heavy).  
  - `MAL` – Greatly improved (tiling, SRAM reuse).  
  - `PAR` – High.  
  - `STI` – None (drop‑in for attention).  
  - `IM` – Initially limited; now fully upstream (PyTorch, Triton, vendor kernels).  
- **Adoption:** Universal by 2024–2025 across major LLMs.  
- **Timeline:** ≈24 months (paper → upstream → “everyone uses it”).  
- **Takeaway:** Prototypical Yellow: clearly beneficial but needs serious kernel engineering and framework work.

#### 2.2.2 Quantization (Int8/Int4, QLoRA‑style)

- **Type:** Kernel‑sensitive optimization; sometimes weight‑only, often requires custom matmul kernels and kernel‑friendly layouts.  
- **Friction:**  
  - `GA` – High in principle, but practice depends on kernel availability.  
  - `MAL` – Improved (fewer bytes); sometimes new alignment constraints.  
  - `PAR` – High.  
  - `STI` – None; same topology.  
  - `IM` – Mixed: good in some stacks (bitsandbytes, TensorRT‑LLM), partial elsewhere.  
- **Adoption:**  
  - Very wide in open‑source inference tools (4‑bit/8‑bit loading).  
  - More conservative at hyperscalers due to quality & safety QA concerns.  
- **Timeline:** Multiple waves since ~2018; 4‑bit LLM quantization became mainstream in 2023–2024 in open‑source.  
- **Takeaway:** High **Green/Yellow** from a hardware perspective, but adoption shows that **quality/safety gating** (Gate‑2/3) can slow diffusion even when friction is relatively low.

### 2.3 System‑Level Changes (Orange/Red)

#### 2.3.1 Mixture‑of‑Experts (MoE) (Recap)

Already deeply covered, but we list it explicitly for contrast.

- **Type:** Routing + expert parallelism; cluster‑level.  
- **Friction:**  
  - `GA` – High.  
  - `MAL` – Fine if engineered; complicated by routing.  
  - `PAR` – High at kernel level, complicated at system level.  
  - `STI` – High (new topology; expert sharding, load balancing).  
  - `IM` – Historically low; improving rapidly (vLLM/TensorRT‑LLM).  
- **Adoption:** Frontier only (DeepSeek‑V3/R1, Llama 4, Mixtral, etc.).  
- **Timeline:** 36–48 months from original Switch to mainstream frontier use.  
- **Takeaway:** High friction + high upside + capital → eventually wins at top of the market, but remains inaccessible to most teams.

#### 2.3.2 Reversible Residual Networks (RevNets) as a “Low‑Friction but Low‑Value” Case

- **Type:** Memory‑saving residual architecture originally popularized in vision.  
- **Friction:**  
  - `GA` – High; still matmuls.  
  - `MAL` – Similar to standard residual nets.  
  - `PAR` – Intact.  
  - `STI` – None.  
  - `IM` – Straightforward; reversible blocks are expressible in existing frameworks.  
- **Adoption in LLMs:** Minimal; RevNets have not become standard despite being hardware‑friendly.  
- **Reason:** The trade‑off (extra compute and complexity in exchange for lower activation memory) doesn’t win enough in practice once Flash/Checkpointing and memory optimizers are in play.  
- **Takeaway:** This is an important **negative case**: the friction map would score RevNets Green/Yellow, but adoption remained low. Hardware friction was not the binding constraint; overall utility vs complexity was.

#### 2.3.3 Linear Attention Variants (Performer, Nyströmformer, etc.)

- **Type:** Alternatives to softmax attention with linear or sub‑quadratic complexity.  
- **Friction:**  
  - `GA` – Moderate/High (still mostly matmul‑based).  
  - `MAL` – Better streaming properties in principle.  
  - `PAR` – High.  
  - `STI` – None; same overall topology.  
  - `IM` – Libraries exist, but not as deeply embedded in mainstream stacks as Flash.  
- **Adoption:**  
  - Some use in research and specialized models, but no broad replacement of softmax attention in frontier LLMs.  
- **Reason:** In many realistic regimes, Flash‑optimized attention plus other tricks are “good enough”; linear attention’s benefits aren’t large enough to force a wholesale migration.  
- **Takeaway:** Another negative case: friction is not the blocker (they’re fairly hardware‑friendly), but empirically observed gains vs standard attention don’t justify the switch at scale.

---

## 3. Explicit Negative and Edge Cases (Falsifiability)

To make the friction map more than a just‑so story, we need to highlight cases where it **doesn’t** explain outcomes cleanly.

### 3.1 Low‑Friction, Low Adoption (RevNets, Linear Attention)

As above:
- **RevNets**: Green/Yellow on friction; low impact in LLMs.  
- **Linear Attention**: Greenish on friction; limited adoption vs Flash + standard attention.

Implication:  
> Hardware friction is a **necessary** gate for large‑scale adoption, but not **sufficient**. Gains must be large enough, and the ecosystem inertia small enough, to justify switching.

### 3.2 High‑Friction, Still Rational (MoE, Vendor‑Specific Kernels)

- **MoE**: High friction but rational for frontier labs because the upside in quality/throughput is large and they control the infra.  
- **Vendor‑Specific Kernels/Stacks** (e.g., custom sparse kernels, TPUs, proprietary inference engines): High friction for everyone except the vendor/owner, but still pursued for strategic reasons (moat, differentiation).

Implication:  
> Some actors *choose* high‑friction paths for strategic reasons (moats, IP), especially when they own the stack. The map predicts these as “Red/Orange for normal teams,” which is correct for the target audience (startups), but not universally “bad ideas.”

---

## 4. Forward‑Looking Predictions (A+++ Requirements)

This section turns the friction map from a retrospective narrative into a **predictive framework** with falsifiable claims.

### 4.1 Prediction Template

For each candidate technique:
1. Assign friction zone (Green/Yellow/Orange/Red) with a short justification using `GA/MAL/PAR/STI/IM`.  
2. Predict:
   - Time to first production deployment at >10B parameters.  
   - Whether it will become “standard practice” (like Flash/GQA) by end‑2027 in mainstream LLM stacks.  
3. State **falsifiers**: what concrete event would prove the prediction wrong.

### 4.2 Candidate 1: Mixture‑of‑Depths (MoD)

**Brief:** Selectively skipping/activating transformer layers per token for depth sparsity.

- **Friction Assessment:**  
  - `GA` – High (still matmuls).  
  - `MAL` – Similar to standard blocks, but with dynamic patterns.  
  - `PAR` – Training still batched; modest extra control‑flow complexity.  
  - `STI` – Moderate: serving path needs per‑token depth routing, but not a MoE‑style cross‑node shuffle.  
  - `IM` – Research‑grade code exists; not yet universalized in vLLM/TensorRT‑LLM.
- **Zone:** **Yellow/Orange boundary** — system‑side complexity, but significantly lower than MoE’s expert parallelism.

**Prediction (Dec 2025 → Dec 2027):**
- At least one **>20B** Mixture‑of‑Depths model will be deployed in a production setting where cost/latency matter (not just a research demo).  
- MoD will **not** become a universal primitive like GQA/Flash; it will be a niche tool for cost‑sensitive or latency‑sensitive products.

**Falsifiers:**
- Strong falsification: By Dec 2027, multiple major open‑weights models (Llama‑class, Qwen‑class) ship with MoD as a standard component *and* major inference stacks (vLLM/TensorRT‑LLM) expose first‑class MoD support.  
- Partial falsification: No visible >10B MoD deployment at all; suggests friction or benefits were badly mis‑estimated.

### 4.3 Candidate 2: Titans‑Style Architectures (Big External Memory Modules)

**Brief:** Architectures that bolt on large, learned memory modules or associative memory beyond normal KV caches.

- **Friction Assessment:**  
  - `GA` – Often high (still GEMMy), but can be hurt by irregular memory access.  
  - `MAL` – Typically poor without careful design (large random accesses).  
  - `PAR` – Depends on memory access patterns; could be okay or ugly.  
  - `STI` – High: serving needs extra state management and possibly new storage backends.  
  - `IM` – Research prototypes only; tooling immature.
- **Zone:** **Orange/Red** — clearly higher friction than MoE for most current stacks.

**Prediction (Dec 2025 → Dec 2028):**
- Titans‑style external memory modules will see **research interest** but will *not* become standard in frontier LLMs **unless**:  
  - a major vendor (NVIDIA, Google) exposes first‑class hardware support (e.g., specialized memory ops) **and**  
  - at least one lab demonstrates a ≥2× *end‑to‑end* cost/performance improvement on real workloads.

**Falsifiers:**
- By Dec 2028, if a top‑5 frontier model uses a Titans‑like memory module at scale **and** A/B tests show ≥2× effective cost/performance improvement vs similarly trained Transformer/MoE baselines, this prediction is wrong.

### 4.4 Candidate 3: Pure SSM Frontier Models

**Brief:** Large (>30B) pure SSM LLMs that avoid attention entirely.

- **Friction Assessment (Gate‑1):**  
  - `GA` – Moderate/High; some SSM kernels are GEMM‑friendly, others less so.  
  - `MAL` – Reasonable, often streaming‑friendly.  
  - `PAR` – This is the crucial axis: sequential dependencies plus only partial parallel‑scan mitigation.  
  - `STI` – None; topology is similar to Transformer.  
  - `IM` – Improving but not yet universal.
- **Zone:** **Orange** — parallelism friction dominates at very large scales.

**Prediction (Dec 2025 → Dec 2028):**
- No pure SSM LLM ≥30B parameters will become a **top‑tier frontier model** (by the usual leaderboards / lab claims) without some attention‑like component for global routing/in‑context learning.

**Falsifiers:**
- A public, well‑documented ≥30B **pure SSM** model that:  
  - matches or beats same‑scale Transformer/MoE baselines on broad evaluation suites, and  
  - is used in serious production or flagship products by a major lab.

---

## 5. Where Friction is Necessary but Not Sufficient

To avoid overclaiming, we explicitly tag areas where the friction map is **only one axis**.

### 5.1 Cases Where Non‑Friction Factors Dominate

- **Quantization:**  
  - Hardware friction is relatively low, but quality/safety concerns plus complexity of verifying numerical behavior slow adoption at hyperscalers.  
  - Here, Eval‑and‑Risk (Gate‑2/3) is the main bottleneck.

- **Linear Attention:**  
  - Hardware‑friendly but often underwhelming vs Flash‑optimized standard attention on real tasks.  
  - Here, empirical performance and ecosystem inertia dominate.

### 5.2 Implication for the Essay

In the essay, these should be surfaced as **caveats**:
- Gate‑1 friction is a strong *filter* on what can even be considered at scale.  
- It does **not** choose among all feasible candidates; Gates 2 and 3 (optimization and scaling behavior, data, governance) do.

---

## 6. Summary: What This Enables for the A+++ Essay

This supplement gives you:

1. **A richer dataset**: More primitives (RoPE, RMSNorm, LoRA/QLoRA, quantization, RevNets, linear attention) scored on friction vs adoption.  
2. **Negative and edge cases**: RevNets and linear attention as low‑friction/low‑adoption; MoE and vendor stacks as high‑friction but rational for some actors.  
3. **Explicit predictive bets**: MoD, Titans‑style memory, and pure SSM frontier models, with falsifiers and timelines.  
4. **Scope guardrails**: Clear articulation of where friction is necessary but not sufficient, and where other gates dominate.

If you thread these elements into the essay (selectively, not exhaustively), you move it from “strong, opinionated summary of 2023–2025” to a *calibrated, testable framework* that serious practitioners can both use and argue with—which is the real A+++ bar.

