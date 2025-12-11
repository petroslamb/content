# The Hardware Friction Scorecard (v2.3)

> **Companion to:** *“The Hardware Friction Map”* and *“What Actually Works: The Hardware Compatibility Filter in Neural Architecture (2023–2025)”*  
> **Scope:** Gate‑1 viability only — how hard it is to make a new architecture economically runnable on 2023–2025 NVIDIA GPU stacks. Not a full “who wins” oracle.

Modern LLM stacks don’t care how elegant your architecture is. They care about whether it can be expressed as big GEMMs on tensor cores, tile cleanly into SRAM, and fit inside the serving topology your infra already understands.

The **Hardware Friction Scorecard** turns that reality into a simple Gate‑1 rubric:

- **H (Hardware Friction):** How friendly is this idea to GPU throughput?  
- **E (Ecosystem Friction):** How much engineering does it take to get good kernels and serving?

Use this scorecard as a **survival heuristic** for non‑Google labs and startups. If you don’t have 50 kernel engineers, High Friction is not “interesting” — it’s usually fatal.

---

## What This Scorecard Is (and Isn’t)

This is **Table 1: Hardware + Infra Viability**, not a calibrated law of “what survives” in neural architecture.

- It shows how to apply the Friction Map rubric (GA/MAL/PAR/STI/IM) to real architectures.  
- It is a **single‑author worked‑example set**, not a statistically calibrated model.  
- Scores were assigned **after** we knew which models shipped, so they’re vulnerable to hindsight bias.

Later gates still matter:

1. **Training dynamics (Gate 2):** Does it actually learn efficiently? (LSTMs fail here.)  
2. **Scaling laws (Gate 3):** Does performance scale predictably with compute? (Pure Mamba is unproven above 7B.)  
3. **Ecosystem backing:** Do major labs and frameworks support it, or are you alone?

The Friction Map essay lives at the narrative level. This scorecard is the quantitative underside.

---

## The Friction = Risk Equation

For a non‑Google lab, adoption risk is dominated by two numbers:

1. **Hardware Friction (H):** Low H‑score ⇒ high compute cost (low MFU, wasted tensor cores).  
2. **Ecosystem Friction (E):** Low E‑score ⇒ high engineering cost (rewriting kernels and serving stacks).

We can summarize this in one practical rule:

> **Startup Heuristic:** If you don’t have 50 kernel engineers, High Friction is a non‑starter. Let bigger labs pay the kernel tax; you ride on their work once it lands upstream.

Scope for this version:

- **Hardware:** 2023–2025 NVIDIA GPU stacks (A100/H100, CUDA 12.x).  
- **Frameworks:** PyTorch 2.x, JAX+XLA, plus common inference stacks (vLLM, TensorRT‑LLM).  
- **Scoring date:** December 2025.

---

## The 5‑Axis Gate‑1 Rubric

The scorecard decomposes Gate‑1 friction into five axes. Three are hardware‑throughput axes (H), two are ecosystem axes (E).

### Hardware Efficiency (H, max 6) — The “Throughput Gate”

| Axis | Full Name | H/E | Measures |
|:-----|:----------|:----|:---------|
| **GA** | GEMM‑Alignment | H | % of FLOPs in dense matmuls on tensor cores |
| **MAL** | Memory Locality | H | How well memory access patterns tile into SRAM / avoid O(n²) intermediates |
| **PAR** | Parallelism | H | O(1) parallel vs O(N) sequential dependencies in training |

- **GA = 2:** ≥90% of FLOPs in big batched matmuls.  
- **MAL = 2:** Tiled / fused; no giant N×N materializations.  
- **PAR = 2:** Training is effectively O(1) parallel over sequence length.

### Ecosystem Readiness (E, max 4) — The “Software Gate”

| Axis | Full Name | H/E | Measures |
|:-----|:----------|:----|:---------|
| **STI** | Serving Topology | E | How much the serving topology must change vs a vanilla Transformer |
| **IM** | Infra Maturity | E | How “upstream” the kernels and tooling are |

- **STI = 2:** Drop‑in — standard tensor/pipeline parallel, no new topology class.  
- **IM = 2:** Kernels exist in upstream PyTorch/JAX or widely‑used inference stacks.

For Mixture‑of‑Experts, we refine **STI**:

- ≤16 experts ⇒ STI = 2 (locally complex but topologically simple).  
- 17–64 experts ⇒ STI = 1.  
- ≥65 experts ⇒ STI = 0 (a new topology class and serious routing pain).

From these axes we compute:

- **H‑Score = GA + MAL + PAR** (0–6)  
- **E‑Score = STI + IM** (0–4)

---

## Worked Examples (Property‑Based, Not Hype‑Based)

These cases show how the rubric applies to real architectures. The point is to score **properties of the technique itself**, not how popular it is.

### 1. Vanilla Transformer + FlashAttention (Reference Architecture)

- **H/E:** H = 6, E = 4 → 🟢 Low Friction  
- **Why it wins:**  
  - All the heavy lifting is dense matmuls (QKV projections, attention, MLPs).  
  - FlashAttention turns attention into a tiled, SRAM‑resident kernel; the N×N matrix never lives in HBM.  
  - Serving topology is unchanged: same tensor/pipeline parallel patterns, just faster kernels.  
  - Kernels are upstream in PyTorch (`scaled_dot_product_attention` dispatches to FlashAttention2).

This is the friction baseline in 2025. Everything else is a deviation.

### 2. GQA (Grouped‑Query Attention)

- **H/E:** H = 6, E = 4 → 🟢 Low Friction  
- Mechanically, GQA is just **MHA with fewer KV heads**:
  - Same matmul structure; we simply share KV heads across groups of Q heads.  
  - KV cache shrinks by up to 8×, cutting memory bandwidth.  
  - No new kernels, no new topology, no serving changes — just a config and retrain.

Result: GQA transitioned from paper (May 2023) to standard practice (Llama 3, Gemma 2, Qwen, etc.) in about a year.

### 3. MLA (Multi‑Head Latent Attention)

- **H/E:** H = 6, E = 3 → 🟢 Low Friction (DeepSeek‑biased)  
- Mechanism:
  - Down‑project tokens into a lower‑dimensional latent space, run attention there, and store a compressed KV cache.  
  - All heavy ops remain dense matmuls (very high GA, good MAL).  
  - Serving topology looks like standard attention; only the latent dimension changes.
- Ecosystem:
  - Implemented in DeepSeek’s models and libraries, not yet a generic PyTorch primitive (IM = 1).

Net: Great Gate‑1 profile, but not fully “boring” infrastructure yet.

### 4. LSTM / GRU — The Efficiency Counter‑Example

- **H/E:** H ≈ 4, E = 4 → 🔴 High Hardware Friction (despite good E)  
- Why this matters:
  - LSTMs are actually quite GEMM‑aligned and memory‑efficient.  
  - The fatal flaw is **PAR = 0**: they have an O(N) sequential dependency over time steps, so training cannot fully parallelize over sequence length.

Gate‑1 says “maybe okay with effort,” but Gates 2–3 (training dynamics and scaling laws) killed them as frontier LLM contenders.

### 5. Mixtral‑8×7B and DeepSeek‑V3 — MoE in Practice

- **Mixtral 8×7B:** H ≈ 5, E = 3 → 🟡 Software Friction  
- **DeepSeek‑V3 (~256 experts):** H ≈ 5, E = 2 → 🟡 Heavy Software Friction  
- Shared properties:
  - Experts are standard FFNs (great GA); routing is small matmuls + top‑k.  
  - Memory locality is decent but not perfect; which experts light up depends on content.  
  - Serving topology changes: you now need router logic, expert parallelism, and MoE‑aware inference stacks.

MoE sits squarely in the **System Friction** zone. It’s not disallowed by hardware; it just demands years of engineering and serious capital to pay the tax.

### 6. Pure Mamba / SSM (Falcon Mamba 7B)

- **H/E:** H ≈ 3, E = 3 → 🟠 Hardware‑Biased Friction  
- Good news:
  - Input/output projections are dense matmuls; no quadratic attention matrix.  
  - Great long‑sequence throughput at modest scale.
- Bad news:
  - The core SSM operation is a **parallel scan over sequence state**, not a big batched matmul.  
  - That scan is less amenable to full tensor‑core saturation; GA and MAL are middling.

As of Dec 2025, pure SSMs are competitive up to ~7B, but **no pure SSM frontier models** exist. All the big deployments (Jamba, Falcon‑H1, Qwen3‑Next) are hybrids.

### 7. GLA / DeltaNet (Linear‑Attention Hybrids)

- **H/E:** H ≈ 4, E = 3 → 🟠 Medium Friction  
- Favorable traits:
  - Linear attention can be highly GEMM‑friendly.  
  - Topology is standard dense Transformer; no routing.
- Trade‑offs:
  - Memory locality and recall behavior are trickier than FlashAttention.  
  - Infra is available (e.g., Triton kernels in `fla`), but not as universal as FlashAttention.

Gate‑1 is fine; Gates 2–3 (expressivity and recall limits) are the real question.

### 8. KANs (Kolmogorov–Arnold Networks)

- **H/E:** H ≈ 2, E ≈ 0 → 🔴 Hardware Friction (Gate‑1 fail)  
- Core issue:
  - Per‑edge spline evaluation **cannot be batched into a small number of big GEMMs**.  
  - You get many tiny, irregular ops that thrash caches and starve tensor cores.
- Ecosystem:
  - Research code exists; there is no robust, upstream, LLM‑scale implementation.

On paper, KANs are expressive and sample‑efficient. On 2025 GPUs, they’re simply too expensive per token to be viable for most real workloads.

### 9. Neural ODEs

- **H/E:** H ≈ 1, E ≈ 1 → 🔴 Research‑Only  
- Friction profile:
  - ODE solvers are fundamentally iterative: lots of small matmuls per step, repeated many times.  
  - Very poor memory locality and parallelism over time.  
  - Infrastructure exists (`torchdiffeq`), but it’s research‑grade, not tuned for trillion‑token LLM training.

Neural ODEs are a textbook case of a beautiful idea at war with today’s silicon economics.

---

## Zone Interpretation (H/E → Risk)

Compressing the H/E scores into zones:

| H‑Score | E‑Score | Zone | Interpretation |
|:-------:|:-------:|:-----|:---------------|
| **6**   | **4**   | 🟢   | **Low Friction.** Drop‑in ready (Transformer + Flash, GQA). |
| **5–6** | **<4**  | 🟡   | **Software Friction.** High engineering cost, hardware is fine (Titans, large‑expert MoE). |
| **<5**  | Any     | 🔴/🟠 | **Hardware Friction.** Compute cost or parallelism problems (LSTM, pure Mamba, KANs). |

Read this as:

- **Green:** Safe bets. If you get the training right, Gate‑1 will not be your bottleneck.  
- **Yellow:** Only do this if you are an infra lab or vendor; you’re buying a moat with engineering burn.  
- **Orange/Red:** Treat as research or as a deliberate “we are the infra company” bet.

---

## From Intuition Pump to Calibrated Filter (Open Challenge)

Right now, this scorecard is an **intuition pump**: a structured opinion, not a scientific instrument. To turn it into a calibrated predictor, we’d need:

1. **External raters.** 2–3 independent scorers for each architecture. If agreement is <80%, the rubric is too fuzzy.  
2. **Prospective predictions.** Score new primitives before they’re widely deployed, then check back in 12–24 months.

One obvious target variable:

- **Adoption Velocity:** Months from a seminal paper to the first production deployment at >10B parameters (or equivalent commercial usage).  
  - *Fast:* <12 months (e.g., FlashAttention, GQA).  
  - *Slow / Stalled:* >36 months or never (e.g., Neural ODEs, Capsule Nets).

And a minimal feature set:

- `Is_GEMM_Aligned` (binary GA).  
- `Memory_Access_Pattern` (Tiled / Streamed / Random).  
- `Sequential_Dependency` (parallel vs scan vs fully sequential).  
- `Topology_Change` (None / Local / Global).  
- `Kernel_Availability` (Upstream / External lib / Research only).

Fitting even a simple logistic regression or decision tree on ~50 primitives (2018–2025) would tell us:

- Which axes actually carry predictive weight.  
- Whether **parallelism** (PAR) and **topology change** (STI) are as dominant as this qualitative map suggests.

If you end up building that dataset — or violently disagree with these scores — I’d be thrilled to be wrong in public. That’s how the Friction Map gets sharper.

