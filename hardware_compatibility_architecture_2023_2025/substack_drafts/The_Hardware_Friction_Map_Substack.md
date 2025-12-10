# The Hardware Friction Map
## A Gate-1 Survival Guide for Neural Architecture (2023–2025)

> **TL;DR:** On 2023–2025 GPU stacks, hardware economics (not benchmarks) determines which architectures ship. This essay gives you a friction map and practitioner checklist to predict adoption risk—especially if you're a startup without 50 kernel engineers.

---

## Introduction

The last two years of neural architecture on GPU‑based LLM stacks can be summarized in one sentence: **Economics determines what survives.**

We often frame hardware compatibility as a binary physics test: "Does silicon reject this?" That framing is wrong. Hardware rejects nothing. It just charges a tax. You can run KANs. You can run pure Neural ODEs. They just cost 100× more per token than a dense matrix multiplication.

The mechanism isn't a "Compatibility Filter." It's a **Friction Map**—a gradient of integration cost from weight-only changes that ship in weeks to kernel rewrites that take years to cluster-level overhauls that kill startups.

This essay is about **Gate 1: hardware and infrastructure viability**. Once an idea clears this gate, later gates—optimization behavior, scaling laws, data quality—decide which low-friction architectures actually win. LSTMs, for example, were hardware-viable but lost to Transformers at Gates 2–3 because they scaled worse and trained less reliably at frontier sizes.

---

## The Four Friction Zones

Modern AI hardware heavily subsidizes specific behaviors: dense matrix multiplications (GEMMs) on tensor cores, hierarchical memory reuse (SRAM tiling), and massive data parallelism. The further you deviate from these primitives, the higher your **Hardware Friction**—the engineering and compute cost required to make the architecture viable.

### Zone 1: Low Friction (🟢 Green)
*Techniques that map perfectly to existing kernels and infrastructure.*

**Cost:** Retraining only.  
**Adoption Speed:** ~12–18 months (one retrain cycle).

| Technique | Mechanism | Why It Ships Fast |
|-----------|-----------|-------------------|
| **GQA** | Share KV heads to cut memory bandwidth | Paper May 2023 → Standard April 2024 (Llama 3, Gemma, Qwen). Same kernels, smaller cache. |
| **RoPE / RMSNorm** | Swap positional encoding and normalization | Pure matmuls + elementwise ops. Zero serving impact. |

### Zone 2: Kernel Friction (🟡 Yellow)
*Techniques that respect the memory hierarchy but require custom kernels.*

**Cost:** Kernel engineering + framework integration.  
**Adoption Speed:** ~24 months, sometimes gated by eval/safety.

| Technique | Mechanism | Adoption Timeline |
|-----------|-----------|-------------------|
| **FlashAttention** | Tiled attention to minimize HBM traffic (same math, different memory pattern) | May 2022 → PyTorch Jan 2024 → Universal mid-2024 |
| **Quantization (INT8/4)** | Specialized low-bit matmul kernels | Fast in open-source; slower in hyperscaler stacks due to eval friction |

### Zone 3: System Friction (🟠 Orange)
*Techniques that break the serving topology.*

**Cost:** Distributed system overhaul (routing, load balancing, state management).  
**Adoption Speed:** ~36+ months.

| Technique | Mechanism | The Resistance |
|-----------|-----------|----------------|
| **MoE** | Sparse activation decoupling Params from FLOPs | Can't `pip install` an MoE cluster. Need router logic, expert parallelism, MoE-aware serving stacks. Languished in "Google Research" limbo 2021–2023 until capital pressure forced industry adoption. |

### Zone 4: Prohibitive Friction (🔴 Red)
*Techniques architecturally misaligned with current GPU stacks.*

**Cost:** Both compute and engineering explode.  
**Status:** Research toys or vendor-scale bets only.

| Technique | Friction Source | Dec 2025 Status |
|-----------|-----------------|-----------------|
| **KANs** | Per-edge spline evaluation can't batch into GEMMs; fractures arithmetic density, thrashes caches | Zero production deployments at LLM scale |
| **Pure SSMs (frontier scale)** | Sequential dependency trace (PAR=0 at very large scale); parallel-scan tricks don't fully erase the training gap | Stalls at ~7B. Every 13B+ deployment is a hybrid. |

---

## MoE and the "Capital Hammer"

MoE is the perfect example of **overcoming friction with capital**. It didn't "pass" a filter—it sat in the High Friction zone until the economic pressure to scale beyond dense models became unbearable. Labs like DeepSeek and Meta paid the massive engineering tax to make it work.

**The MoE Reality Check (2025 Data):**

| Metric | Marketing Claim | Reality |
|--------|-----------------|---------|
| **Inference Speedup** | "5–7× faster" | **≈2.0–2.5×** vs dense at short context |
| **The Context Trap** | Sustained speedup | Drops to **~1.3–1.5×** at 32K+ as routing + KV traffic dominate |
| **Memory Savings** | "Same as small model" | No VRAM savings at peak—all experts still resident |

MoE is a **throughput and capacity optimizer**, not a magic bullet. It's a Capital Hammer that frontier labs used to smash through a throughput ceiling.

---

## The Startup Heuristic: Moat vs. Death

This Friction Map is not symmetric. It depends on your bank account.

**For Google / Meta / DeepSeek:**
- High Friction is a **MOAT**
- They can afford the 36-month engineering burn to rewrite kernels and cluster schedulers
- If they make MoE work (DeepSeek-V3), and you can't, they win on unit economics

**For Startups / Enterprise:**
- High Friction is **DEATH**
- Betting on a Red Zone architecture means burning runway debugging CUDA kernels before verifying your product

> **The Rule (for product teams):** If it's not in PyTorch upstream, don't build your company on it. Wait for the giants to pave the road.
> 
> **The Exception:** If you are an infra startup, you're breaking this rule on purpose—because *your product is the friction*.

---

## The Practitioner's Checklist

Stop asking "Is this architecture smart?" Start asking "What is the Friction Score?"

| Question | Axis | Red Flag |
|----------|------|----------|
| Can 90% of FLOPs be big batched GEMMs? | **GA** | KANs fail this |
| Does it tile into SRAM, or thrash HBM with large intermediates? | **MAL** | Standard attention fails this (needs Flash) |
| Is training O(1) parallel or O(N) sequential? | **PAR** | RNNs/Pure SSMs fail this |
| Does inference require complex routing or state across nodes? | **STI** | MoE fails this |
| Is the kernel available today in upstream vLLM/PyTorch? | **IM** | If no, you are the research team |

---

## What We Deliberately Keep Spiky

Not every critique led to a change in this framework. Some tensions are deliberate:

**1. KANs and Neural ODEs as "Do Not Touch"**
- *Critique:* The treatment is a bit straw-manny—it doesn't dwell on their theoretical appeal.
- *Author stance:* Nuance is expensive; "Do not touch this" is cheap and useful for the intended reader. Specialists who truly care will read the detailed references.

**2. The Startup Heuristic's Over-Generality**
- *Critique:* "If it's not in PyTorch upstream, don't build on it" is obviously false for infra startups.
- *Author stance:* That's fine—the rule is not aimed at infra startups. The exception is explicit.

**3. Overclaimy Opening Lines**
- *Critique:* "Economics determines what survives" overstates Gate-1's role while later sections admit it's only one gate.
- *Author stance:* It's a blog post, not a legal contract. The hook can be punchier than the caveats.

---

## Falsifiable Predictions

A useful friction heuristic is one you can test in public. Here are the bets:

| Prediction | Timeframe | What Would Falsify It |
|------------|-----------|----------------------|
| **Mixture-of-Depths** will appear in at least one >20B production model as a niche cost/latency optimization | By 2027 | MoD never ships in production, or ships but fails to provide meaningful cost/latency gains |
| **Titans-style external memory** will remain research-only | Until vendors add first-class hardware support | A Titans-style model becomes a flagship frontier LLM without dedicated hardware |
| **Pure SSM frontier models** (≥30B, no attention) will not become top-tier LLMs | By 2028 | A 40B+ pure SSM dominates benchmarks without attention-like mechanisms |

If any of these are wrong—if a 40B pure SSM or Titans-style memory model becomes a flagship frontier LLM—this map needs to be redrawn. That's the point.

---

## Conclusion

We are not designing neural networks on a whiteboard. We are leasing time on silicon heaters.

The industry has converged on a narrow set of primitives—GEMMs, FlashAttention, SwiGLU—not because we lack imagination, but because **economic friction kills everything else** on today's NVIDIA-dominated GPU stacks.

Innovation hasn't stopped. It has moved to where the friction is lower: **Training** (post-training, data curation) and **Hybrids** (MoE, Attention+SSM).

Don't fight the friction. Map it, price it, and decide if you can afford the toll.

---

# Appendix A — MoE Throughput and the Context Trap

**Throughput vs Context Length (synthesized from 18 sources, 2017–2025)**

| Context Length | Throughput vs 128-token Baseline | Notes |
|----------------|----------------------------------|-------|
| 128 tokens | 1.0× (baseline) | "Marketing regime"—vendors quote 5–7× here |
| 1024 tokens | ~0.8× | ≈20% lower throughput |
| 2048 tokens | ~0.7× | ≈30% lower throughput |
| 16K–32K tokens | ~0.3–0.4× | "Context trap"—routing + KV traffic dominate |
| >32K (specialized) | up to ~10× vs naive | Architectures co-designed for long context (Qwen3-Next, DeepSeek-V3) claw back throughput |

---

# Appendix B — Pure SSM Scale and Hybrid Dominance

**Where Pure Mamba/SSM Exists (as of Dec 2025)**

| Scale | Architecture | Status |
|-------|-------------|--------|
| 130M–2.8B | Pure Mamba | ✓ Matches same-scale transformers |
| 7B | Falcon Mamba 7B | ✓ Outperforms Llama 3.1 8B, Mistral 7B |
| 13B+ | **No pure SSM** | ✗ Only hybrids (Jamba, Falcon-H1, Qwen3-Next) |

**Takeaway:** Pure SSMs are proven up to 7B. From 13B upwards, every deployment uses hybrids—state-space blocks for local/sequential structure, attention-like mechanisms for global routing and in-context learning.

---

# Appendix C — Gate-1 Friction Zones (Summary Table)

| Technique | Zone | H-Score | E-Score | Reason |
|-----------|------|---------|---------|--------|
| RoPE / RMSNorm | 🟢 Green | 6 | 4 | Pure matmuls + elementwise ops |
| GQA | 🟢 Green | 6 | 4 | Same kernels, smaller KV cache |
| FlashAttention | 🟡 Yellow | 6 | 4 | New kernels, same topology |
| MoE | 🟠 Orange | 5 | 2–3 | New topology, routing, expert parallelism |
| Pure SSMs (frontier) | 🟠 Orange | 3 | 3 | Training-parallelism gap at very large scale |
| KANs | 🔴 Red | 2 | 0 | Poor GEMM alignment; cache-unfriendly |

---

# Appendix D — The Hardware Friction Scorecard

> **Purpose:** Turn intuition into a repeatable rubric. This scorecard decomposes Gate-1 friction into five measurable axes.

## The 5-Axis Rubric

### Hardware Efficiency (H, max 6)

| Axis | Full Name | Measures | Score = 2 means... |
|------|-----------|----------|-------------------|
| **GA** | GEMM-Alignment | % of FLOPs in dense matmuls | ≥90% in big batched matmuls |
| **MAL** | Memory Locality | Memory access patterns | Tiled/fused; no giant N×N materializations |
| **PAR** | Parallelism | Sequential vs parallel | Training is O(1) parallel over sequence |

### Ecosystem Readiness (E, max 4)

| Axis | Full Name | Measures | Score = 2 means... |
|------|-----------|----------|-------------------|
| **STI** | Serving Topology | How much topology must change | Drop-in—standard tensor/pipeline parallel |
| **IM** | Infra Maturity | How upstream the kernels are | In upstream PyTorch/JAX or major inference stacks |

**Composite Scores:**
- **H-Score = GA + MAL + PAR** (0–6)
- **E-Score = STI + IM** (0–4)

## Zone Interpretation

| H-Score | E-Score | Zone | Interpretation |
|---------|---------|------|----------------|
| 6 | 4 | 🟢 Green | Drop-in ready. Safe bet. |
| 5–6 | <4 | 🟡 Yellow | High engineering cost, hardware is fine. |
| <5 | Any | 🔴/🟠 Red/Orange | Hardware friction. Only for labs with deep pockets. |

## Worked Examples

### Vanilla Transformer + FlashAttention
- **H = 6, E = 4 → 🟢 Green**
- All heavy lifting is dense matmuls. FlashAttention turns attention into a tiled, SRAM-resident kernel. Serving topology unchanged. Kernels upstream in PyTorch.

### Mixtral-8×7B (MoE)
- **H ≈ 5, E = 3 → 🟡 Yellow**
- Experts are standard FFNs (great GA); routing is small matmuls + top-k. Serving topology changes: router logic, expert parallelism, MoE-aware inference stacks.

### Pure Mamba (Falcon Mamba 7B)
- **H ≈ 3, E = 3 → 🟠 Orange**
- Input/output projections are dense matmuls. Core SSM operation is a parallel scan—less tensor-core friendly. No pure SSM frontier models exist; all big deployments are hybrids.

### KANs
- **H ≈ 2, E ≈ 0 → 🔴 Red**
- Per-edge spline evaluation cannot batch into GEMMs. Many tiny, irregular ops that thrash caches and starve tensor cores. Research code only—no robust LLM-scale implementation.

---

# Appendix E — References (Selected)

**Mixture-of-Experts**
- Fedus et al., 2021 — *"Switch Transformers"* (arXiv:2101.03961)
- DeepSeek-V3 and DeepSeek-R1 technical reports (2024–2025)
- Mixtral-8×7B technical report (Mistral, 2023)
- Meta Llama 4 (Scout/Maverick) model cards

**FlashAttention**
- Dao et al., 2022 — *"FlashAttention"* (arXiv:2205.14135)
- Dao et al., 2023 — *"FlashAttention-2"* (arXiv:2307.08691)
- PyTorch 2.2 release notes

**SSM / Mamba**
- Gu et al., 2021 — S4 (arXiv:2111.00396)
- Gu & Dao et al., 2023 — Mamba (arXiv:2312.00752)
- Falcon Mamba 7B, Jamba, Falcon-H1, Qwen3-Next technical reports

**Core LLM Architectures**
- Llama 2/3/4 (Meta), Gemma 2 (Google), Qwen2.5 (Alibaba), Mistral 7B, DeepSeek-V2/V3/R1

For the full bibliography, see the research notes linked alongside this essay and the scored architectures dataset on GitHub.
