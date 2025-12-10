# The Hardware Friction Map
## A Gate-1 Survival Guide for Neural Architecture (2023–2025)

*How to predict which ideas will ship and which will die on the compute tax.*

---

In December 2024, DeepSeek shipped V3—a 671B-parameter model with 256 experts. Training it required rewriting the entire cluster scheduler, custom-building routing kernels, and six months of dedicated infrastructure work before the first training run began. The architecture paper devotes **three full pages** to distributed expert placement alone.

Three months earlier, Meta trained Llama 3.1 405B using essentially the same stack as Llama 2. Same PyTorch primitives. Same GPU topology. Same serving infrastructure. The only novel engineering was for long-context FlashAttention kernels that already had upstream support.

Both models pushed to 400B+ parameters. One required rebuilding the infrastructure from scratch. The other didn't. **This is the friction map.**

---

## Introduction

The last two years of neural architecture on GPU-based LLM stacks can be summarized in one sentence: **Economics determines what survives.**

Hardware rejects nothing—it just charges a tax. You can run KANs. You can run pure Neural ODEs. They just cost 100× more per token than a dense matrix multiplication. The mechanism isn't a binary "Compatibility Filter." It's a **Friction Map**—a gradient of integration cost from weight-only changes that ship in weeks, to kernel rewrites that take years, to cluster-level overhauls that kill startups.

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
**Adoption Speed:** ~20–24 months, sometimes gated by eval/safety validation.

| Technique | Mechanism | Adoption Timeline |
|-----------|-----------|-------------------|
| **FlashAttention** | Tiled attention to minimize HBM traffic (same math, different memory pattern) | May 2022 → PyTorch 2.2 (Jan 2024) → Universal mid-2024 |
| **Quantization (INT8/4)** | Specialized low-bit matmul kernels | Fast in open-source; slower in hyperscaler stacks due to eval friction |

### Zone 3: System Friction (🟠 Orange)
*Techniques that break the serving topology.*

**Cost:** Distributed system overhaul (routing, load balancing, state management).  
**Adoption Speed:** ~36+ months.

| Technique | Mechanism | The Resistance |
|-----------|-----------|----------------|
| **MoE** | Sparse activation decoupling Params from FLOPs | Can't `pip install` an MoE cluster. Need router logic, expert parallelism, MoE-aware serving stacks. Languished in "Google Research" limbo 2021–2023 until capital pressure forced industry adoption. |
| **Pure SSMs (mid-scale)** | Sequential dependency in training (PAR < 2) | Parallel-scan tricks help but don't fully erase training gap. Viable at ≤7B; friction increases with scale. See "SSM Scale Dependence" section below. |

### Zone 4: Prohibitive Friction (🔴 Red)
*Techniques architecturally misaligned with current GPU stacks.*

**Cost:** Both compute and engineering explode.  
**Status:** Research toys or vendor-scale bets only.

| Technique | Friction Source | Dec 2025 Status |
|-----------|-----------------|-----------------|
| **KANs** | Each edge evaluates a learned spline—hundreds of tiny ops that can't fuse into GEMMs, dropping tensor core utilization to ~10% | Zero production deployments at LLM scale |
| **Pure SSMs (frontier scale, ≥13B)** | Training parallelism gap compounds at scale; memory bandwidth for state propagation becomes bottleneck | Every 13B+ deployment is a hybrid (Jamba, Falcon-H1, Qwen3-Next) |
| **Neural ODEs** | Iterative solvers with irregular step sizes; poor memory locality; 5-15% Tensor Core utilization | Theoretically elegant; economically unshippable |

---

## FlashAttention: The Yellow Zone Template

FlashAttention is the canonical example of kernel friction—technically beneficial from Day 1, but taking 20+ months to reach universal adoption:

- **May 2022:** Paper published (arXiv:2205.14135). Demonstrated 2-4× speedup and memory savings.
- **Dec 2022:** Beta `flash-attn` package released (v0.2). Requires manual installation, Ampere+ GPUs only.
- **Jul 2023:** FlashAttention-2 released with improved parallelism. Early adopters (Meta, Mistral) integrate into training pipelines.
- **Jan 2024:** PyTorch 2.2 integrates FlashAttention-v2 into `scaled_dot_product_attention`. No longer requires external dependency.
- **Mid-2024:** Universal adoption. vLLM, TensorRT-LLM, and all major inference stacks default to FlashAttention.

**Why 20 months?** Not because FlashAttention was hard to write—the core kernel existed in 2022. The delay was:
1. **Framework integration** (~8 months): Getting upstream into PyTorch required API standardization and extensive testing
2. **Production validation** (~6 months): Hyperscalers needed to verify identical numerical behavior at scale
3. **Ecosystem tooling** (~6 months): Inference stacks (vLLM, TGI) needed to adopt the new API

This is the tax for kernel-level innovation: even when the algorithm works, **the ecosystem takes 2 years to catch up**.

---

## MoE: The Orange Zone Template

Mixture-of-Experts tells a different story—36+ months from "research curiosity" to "production standard," because the friction was *systemic*, not just kernel-level:

- **Jan 2021:** Switch Transformer published (Google, arXiv:2101.03961). Demonstrated MoE at 1.6T parameters. Industry reaction: "Interesting, but we don't have the infra."
- **2021–2023:** MoE languishes in "Google Research limbo." No open-source MoE stack. Custom routing, load balancing, and expert parallelism required. Training runs needed full-time infra teams.
- **Dec 2023:** Mixtral 8×7B released (Mistral). First open-source MoE that *mattered*—competitive with Llama 2 70B at fraction of inference cost. Proved MoE could be packaged.
- **May 2024:** DeepSeek-V2 (236B total, 21B active). Demonstrated MoE + MLA at scale with optimized routing.
- **Dec 2024:** DeepSeek-V3 (671B total, 37B active, 256 experts). Full cluster rewrite. Three pages of the paper devoted to expert placement. Set new throughput benchmarks.

**Why 36+ months?** MoE didn't just need kernels—it needed:
1. **Routing logic:** Top-k selection, load balancing, auxiliary losses
2. **Expert parallelism:** Distributing 256 experts across nodes
3. **MoE-aware serving:** vLLM and TensorRT-LLM only added robust MoE support in late 2024
4. **Capital commitment:** No one would pay the engineering tax until dense models hit scaling ceilings

MoE is the perfect example of **overcoming friction with capital**. It didn't "pass" a filter—it sat in the High Friction zone until the economic pressure to scale beyond dense models became unbearable. Labs like DeepSeek and Meta paid the massive engineering tax to make it work.

**The MoE Reality Check (2025 Data):**

| Metric | Marketing Claim | Reality |
|--------|-----------------|---------|
| **Inference Speedup** | "5–7× faster" | **≈2.0–2.5×** vs dense at short context |
| **The Context Trap** | Sustained speedup | Drops to **~1.3–1.5×** at 32K+ as routing + KV traffic dominate |
| **Memory Savings** | "Same as small model" | No VRAM savings at peak—all experts still resident |

MoE is a **throughput and capacity optimizer**, not a magic bullet. It's a Capital Hammer that frontier labs used to smash through a throughput ceiling.

---

## SSM Scale Dependence: The 7B Cliff

The friction zone for State Space Models is **not constant—it depends on scale**. This nuance is critical for understanding why Mamba simultaneously "works" and "fails":

**At ≤7B scale (🟠 Orange Zone):**
Pure SSMs are **production-viable**. Falcon Mamba 7B (Sept 2024) outperformed Llama 3.1 8B and Mistral 7B on multiple benchmarks while offering faster inference. The training parallelism penalty exists but is survivable—community teams and mid-sized labs can absorb the compute tax.

| Model | Scale | Status | Performance |
|-------|-------|--------|-------------|
| Mamba-1/2 (130M–2.8B) | Small | ✓ Viable | Matches same-scale Transformers |
| Falcon Mamba 7B | Mid | ✓ Viable | Outperforms Llama 3.1 8B, Mistral 7B |

**At ≥13B scale (🔴 Red Zone):**
The friction becomes **prohibitive**. Every 13B+ deployment is a hybrid—state-space blocks for local/sequential structure paired with attention layers for global routing. The training parallelism gap compounds: what's a 1.5× tax at 7B becomes a 3-5× tax at 65B due to communication overhead in distributed training.

| Model | Scale | Architecture | Why Hybrid? |
|-------|-------|--------------|-------------|
| Jamba (AI21, 52B active) | Large | SSM + Attention | Attention handles "routing" across experts |
| Falcon-H1 (140B total) | Large | SSM + Attention | SSM for local context, Attention for global |
| Qwen3-Next (unreleased) | Frontier | SSM + Attention | Betting on hybrid for long-context efficiency |

**Why the cliff at 13B?**
1. **Training parallelism**: SSM's sequential dependency requires more synchronization across GPUs. At 7B on 8 GPUs, the overhead is tolerable. At 65B on 512 GPUs, it dominates.
2. **Memory bandwidth**: SSM hidden state must propagate sequentially. At scale, HBM bandwidth becomes the bottleneck, not compute.
3. **Institutional risk**: Labs willing to spend $50M+ on a training run won't accept a 3× compute tax when hybrids offer SSM benefits with Transformer reliability.

**The practical heuristic:** If you're building at ≤7B, pure SSM is a legitimate option (Orange zone). If you're building at ≥13B, plan for a hybrid or accept Red-zone friction.

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

**The Cautionary Tale:**

A Series A startup in 2022 bet their inference stack on a custom Mamba implementation. They believed pure SSMs would dominate long-context workloads. Eighteen months and $8M of engineering burn later, they pivoted to Llama 2 with vLLM—shipping in three weeks what took them over a year to half-finish. The SSM kernels worked; the ecosystem around them didn't exist.

The architecture was viable. The *friction* killed them.

> **The Rule (for product teams):** If it's not in PyTorch upstream, don't build your company on it. Wait for the giants to pave the road.
> 
> **The Exception:** If you are an infra startup, you're breaking this rule on purpose—because *your product is the friction*.

---

## The Hardware Friction Scorecard

Turn intuition into a repeatable rubric. This scorecard decomposes Gate-1 friction into five measurable axes.

### The 5-Axis Rubric

**Hardware Efficiency (H, max 6)**

| Axis | Full Name | Measures | Score = 2 means... |
|------|-----------|----------|-------------------|
| **GA** | GEMM-Alignment | % of FLOPs in dense matmuls | ≥90% in big batched matmuls |
| **MAL** | Memory Locality | Memory access patterns | Tiled/fused; no giant N×N materializations |
| **PAR** | Parallelism | Sequential vs parallel | Training is O(1) parallel over sequence |

**Ecosystem Readiness (E, max 4)**

| Axis | Full Name | Measures | Score = 2 means... |
|------|-----------|----------|-------------------|
| **STI** | Serving Topology | How much topology must change | Drop-in—standard tensor/pipeline parallel |
| **IM** | Infra Maturity | How upstream the kernels are | In upstream PyTorch/JAX or major inference stacks |

**Composite Scores:**
- **H-Score = GA + MAL + PAR** (0–6)
- **E-Score = STI + IM** (0–4)

### Zone Interpretation

| H-Score | E-Score | Zone | Interpretation |
|---------|---------|------|----------------|
| 6 | 4 | 🟢 Green | Drop-in ready. Safe bet. |
| 5–6 | <4 | 🟡 Yellow | High engineering cost, hardware is fine. |
| <5 | Any | 🔴/🟠 Red/Orange | Hardware friction. Only for labs with deep pockets. |

### Worked Examples

**Vanilla Transformer + FlashAttention**
- **H = 6, E = 4 → 🟢 Green**
- All heavy lifting is dense matmuls. FlashAttention turns attention into a tiled, SRAM-resident kernel. Serving topology unchanged. Kernels upstream in PyTorch.

**Mixtral-8×7B (MoE)**
- **H ≈ 5, E = 3 → 🟡 Yellow**
- Experts are standard FFNs (great GA); routing is small matmuls + top-k. Serving topology changes: router logic, expert parallelism, MoE-aware inference stacks.

**Pure Mamba (Falcon Mamba 7B)**
- **H ≈ 4, E = 3 → 🟠 Orange**
- Input/output projections are dense matmuls. Core SSM operation is a parallel scan—less tensor-core friendly. Viable at 7B scale; friction increases dramatically beyond 13B.

**KANs**
- **H ≈ 2, E ≈ 0 → 🔴 Red**
- Per-edge spline evaluation cannot batch into GEMMs. Many tiny, irregular ops that thrash caches and starve tensor cores. Research code only—no robust LLM-scale implementation.

**How to use this on a new technique:**
1. Score each axis (0/1/2) based on the rubric
2. Compute H-Score and E-Score
3. Map to zone
4. Ask: "Can I afford this friction given my resources?"

---

## Falsifiable Predictions

A useful friction heuristic is one you can test in public. Here are the bets—designed to be **crisp, measurable, and risky**:

| Prediction | Timeframe | Falsification Criteria |
|------------|-----------|----------------------|
| **Mixture-of-Depths** will appear in ≥3 frontier models (>70B params) as a cost/latency optimization, achieving ≥15% measured latency reduction at 32K+ context | By Dec 2027 | MoD appears in <3 frontier models, OR ships but fails to achieve ≥15% latency improvement at long context |
| **Titans-style external memory** will remain research-only until a major accelerator vendor (NVIDIA, AMD, Cerebras, Groq) announces dedicated memory hierarchy support ≥6 months before model deployment | Through 2028 | A Titans-style model ships as a flagship frontier LLM using only current-gen hardware with no vendor-announced memory optimization |
| **No pure SSM frontier model** (≥30B params, zero attention layers) will rank in the top 10 on Chatbot Arena or equivalent composite benchmark | Through Dec 2028 | A 40B+ pure SSM model achieves top-10 ranking on Chatbot Arena without attention-like mechanisms |
| **Groq** will not achieve profitability by 2028 unless they secure a multi-year contract with a frontier lab committing to train ≥1 flagship model (30B+) exclusively on LPU hardware | Through Dec 2028 | Groq achieves profitability by 2028 without such a contract |

These predictions are designed to be **falsifiable**—if any are wrong, the friction map needs to be redrawn. That's the point.

---

## Conclusion: The Geometry of What Ships

We are not designing neural networks on a whiteboard. We are leasing time on silicon heaters.

The industry has converged on a narrow set of primitives—GEMMs, FlashAttention, SwiGLU—not because we lack imagination, but because **economic friction kills everything else** on today's NVIDIA-dominated GPU stacks. Innovation hasn't stopped. It has moved to where the friction is lower: **Training** (post-training, data curation) and **Hybrids** (MoE, Attention+SSM).

**The friction map is calcifying, not softening.** NVIDIA's Rubin roadmap (2026) promises "3× faster Transformer layer performance" and HBM4 optimized for million-token context. Every silicon generation optimizes harder for GEMMs. The window for alternative architectures to prove viability is narrowing—not because alternatives can't work, but because the cost of making them work rises with every hardware generation.

Don't fight the friction. Map it, price it, and decide if you can afford the toll.

The Transformer doesn't need to be optimal. It just needs to be **good enough—and too expensive to escape**.

---

## Author's Note: What Stays Spiky

Not every simplification in this essay is accidental:

**KANs and Neural ODEs get dismissed quickly.** The theoretical appeal is real; the production path is not. Specialists who disagree know where to find the papers.

**The Startup Heuristic is a generalization.** Of course infra startups break the rule—that's their business model. The exception is noted.

**"Economics determines what survives" overstates Gate-1's role.** It's a hook, not a legal contract. Gates 2 and 3 (scaling laws, training dynamics) kill plenty of hardware-viable architectures.

These are author choices, not oversights. Disagree with them publicly—that's how good ideas improve.

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
| Pure SSMs (≤7B) | 🟠 Orange | 4 | 3 | Training-parallelism gap manageable at mid-scale |
| Pure SSMs (≥13B) | 🔴 Red | 3 | 2 | Training-parallelism gap compounds; hybrids required |
| KANs | 🔴 Red | 2 | 0 | Poor GEMM alignment; cache-unfriendly |

---

# Appendix D — References (Selected)

**Mixture-of-Experts**
- Fedus et al., 2021 — *"Switch Transformers"* (arXiv:2101.03961)
- DeepSeek-V3 and DeepSeek-R1 technical reports (2024–2025)
- Mixtral-8×7B technical report (Mistral, 2023)
- Meta Llama 4 (Scout/Maverick) model cards

**FlashAttention**
- Dao et al., 2022 — *"FlashAttention"* (arXiv:2205.14135)
- Dao et al., 2023 — *"FlashAttention-2"* (arXiv:2307.08691)
- PyTorch 2.2 release notes (Jan 2024)

**SSM / Mamba**
- Gu et al., 2021 — S4 (arXiv:2111.00396)
- Gu & Dao et al., 2023 — Mamba (arXiv:2312.00752)
- Falcon Mamba 7B, Jamba, Falcon-H1, Qwen3-Next technical reports

**Core LLM Architectures**
- Llama 2/3/4 (Meta), Gemma 2 (Google), Qwen2.5 (Alibaba), Mistral 7B, DeepSeek-V2/V3/R1

For the full bibliography, see the research notes linked alongside this essay and the scored architectures dataset on GitHub.
