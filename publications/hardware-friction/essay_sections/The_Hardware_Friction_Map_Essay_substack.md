# The Hardware Friction Map

*Why economic costs—not benchmarks—determine which AI architectures ship.*

---

## TL;DR

- On 2023–2025 GPU stacks, **hardware and infrastructure economics (Gate 1)** are a better early predictor of which architectures ship than small‑scale benchmarks.  
- Techniques that stay close to **GEMMs + SRAM‑friendly memory access** and require no new serving topology (RoPE, RMSNorm, GQA, FlashAttention) diffuse quickly; ideas that fight this (pure SSMs at frontier scale, KANs, naive MoE at long context) become research curiosities or require massive capital.  
- The **Hardware Friction Map** gives a practitioner checklist (kernel shape, memory, parallelism, serving topology, infra maturity) to score new papers and predict adoption risk—especially for startups that don’t control their hardware stack.  
- Above Gate 1, **optimization behavior and scaling laws** still decide which low‑friction ideas win (e.g., Transformers vs LSTMs); the map is a viability filter, not an oracle.  
- The essay ends with explicit, falsifiable bets about Mixture‑of‑Depths, Titans‑style external memory, and pure SSM frontier models, so the framework can be tested—not just admired.

## Introduction

The last two years of neural architecture on GPU‑based LLM stacks can be summarized in one sentence: **Economics determines what survives.**

We often frame hardware compatibility as a binary physics test: "Does silicon reject this?" That is wrong. Hardware rejects nothing. It just charges a tax. You can run KANs. You can run pure Neural ODEs. They just cost 100x more per token than a dense matrix multiplication.

The mechanism isn't a "Compatibility Filter." It's a **Friction Map**.

Architecture isn't about finding the "smartest" math. It's about navigating the gradient of integration cost—from weight-only changes that ship in weeks, to kernel rewrites that take years, to cluster-level overhauls that kill startups.

---

## Gate 1: The Friction Map

Modern AI hardware heavily subsidizes specific behaviors: dense matrix multiplications (GEMMs) on tensor cores, hierarchical memory reuse (SRAM tiling), and massive data parallelism.

The further you deviate from these primitives, the higher your **Hardware Friction**—the engineering and compute cost required to make the architecture viable.

This essay is about **Gate 1: hardware and infrastructure viability**. Once an idea clears this gate, later gates—optimization behavior, scaling laws, and data quality—decide which low-friction architectures actually win. LSTMs, for example, were hardware-viable but lost to Transformers at Gates 2 and 3: they scaled worse and trained less reliably at frontier sizes.

### Zone 1: Low Friction (Green)
*Techniques that map perfectly to existing kernels and infrastructure.*
*   **Cost:** Retraining only.
*   **Adoption Speed:** ~1 retrain cycle (≲12–18 months).

Examples:
*   **Grouped-Query Attention (GQA).**
    *   **Mechanism:** Share KV heads to reduce memory bandwidth.
    *   **Adoption:** Published May 2023. Standard practice by April 2024 (Llama 3, Gemma, Qwen, Falcon, Mistral).
    *   **Why:** Required no new kernels; change the model definition, retrain, ship.
*   **RoPE / RMSNorm.**
    *   **Mechanism:** Swap positional encoding and normalization; still pure matmuls + elementwise ops.
    *   **Adoption:** Quietly became default in essentially every 2023–2025 LLM family.
    *   **Why:** Zero serving impact, trivial training integration.

### Zone 2: Kernel Friction (Yellow)
*Techniques that respect the memory hierarchy but require custom kernels.*
*   **Cost:** Kernel engineering + framework integration.
*   **Adoption Speed:** ~24 months, sometimes gated by eval/safety.

Examples:
*   **FlashAttention.**
    *   **Mechanism:** Tiled attention to minimize HBM traffic; same math, radically different memory pattern.
    *   **Adoption:** Published May 2022. PyTorch integration Jan 2024. Universal by mid‑2024.
*   **Quantization / QLoRA‑style low‑bit kernels.**
    *   **Mechanism:** Run matmuls in INT8/INT4 with specialized kernels.
    *   **Adoption:** Rapid in open‑source (bitsandbytes, 4‑bit loading), more cautious in hyperscaler stacks due to eval/safety, not hardware, friction.

### Zone 3: System Friction (Orange)
*Techniques that break the serving topology.*
*   **Cost:** Distributed system overhaul (routing, load balancing, state management).
*   **Adoption Speed:** ~36+ months.

Example:
*   **Mixture‑of‑Experts (MoE).**
    *   **Mechanism:** Sparse activation to decouple Params (capacity) from FLOPs (compute).
    *   **Resistance:** You can't just `pip install` an MoE cluster. You need router logic, expert parallelism (sharding experts across GPUs), and specialized serving stacks (vLLM/TensorRT‑LLM/FlashInfer updates).
    *   **Result:** Languished in “Google Research” limbo for ~3 years (2021–2023) before capital pressure forced the industry to pay the engineering cost.

### Zone 4: Prohibitive Friction (Red)
*Techniques that are architecturally misaligned with current GPU stacks.*
*   **Cost:** Both compute and engineering explode; viable only as research toys or vendor‑scale bets.

Examples:
*   **KANs (Kolmogorov‑Arnold Networks).**
*   **Pure SSMs at frontier scale (so far).** (See Appendix B for current SSM scale and hybrid evidence.)

## MoE and the "Capital Hammer"

MoE is the perfect example of **overcoming friction with capital**.

It didn't "pass" a filter. It sat in the High Friction zone until the economic pressure to scale beyond dense models became unbearable. Labs like DeepSeek and Meta paid the massive engineering tax to make it work.

But let's look at the receipts. The marketing claims "5-7x speedups." The reality is an **economic tradeoff**.

**The MoE Reality Check (2025 Data):**
*   **Real Throughput Gain:** ≈2.0-2.5x vs dense models of equal quality.


MoE isn't magic physics. It's a "Capital Hammer" that frontier labs used to smash through a throughput ceiling.

---

---

## Zone 4 in Practice: KANs and Pure SSMs

What happens when you fight the hardware's nature? You don't get "rejected"—you just get priced out.

**1. KANs (Kolmogorov-Arnold Networks):**
*   **Concept:** Learnable splines on edges. Theoretically attractive for expressivity.
*   **Friction:** Spline evaluation cannot be batched into large GEMMs. It fractures arithmetic density and thrashes caches.
*   **Result:** Efficient on paper, **prohibitively expensive per-token** on H100s. As of Dec 2025: zero credible production deployments at LLM scale.

**2. Pure SSMs (State Space Models):**
*   **Concept:** Linear-time sequence modeling (Mamba).
*   **Friction:** **Parallelism.** Transformers train all tokens in parallel. SSMs have a sequential dependency trace. Parallel-scan tricks mitigate this, but they don't fully erase the gap in training efficiency at very large scale.
*   **Result:** Great for inference, fragile for training efficiency once you push to frontier scales.
*   **Status (Dec 2025):** Pure SSMs stall at ~7B parameters. We see no public 13B+ pure SSM models; every large deployment (Jamba, Falcon‑H1, Qwen3‑Next, RWKV variants) uses **Hybrids** (Attention + SSM) to balance the friction. (For the underlying evidence, see **Appendix B — SSM Scale and Hybrid Dominance**.)

---

## The Startup Heuristic (Moat vs. Death)

This Friction Map is not symmetric. It depends on your bank account.

**For Google / Meta / DeepSeek:**
*   High Friction is a **MOAT**.
*   They can afford the 36-month engineering burn to rewrite kernels and cluster schedulers. If they make MoE work (DeepSeek-V3), and you can't, they win on unit economics.

**For Startups / Enterprise:**
*   High Friction is **DEATH**.
*   If you bet your startup on a Red Zone architecture (like training a pure Neural ODE foundation model), you will burn your runway debugging CUDA kernels before you verify your product.
*   **Rule (for product teams):** If it's not in PyTorch upstream, **don't build your company on it.** Wait for the giants to pave the road. If you are an infra startup, this is exactly the rule you’re breaking on purpose—but then your product *is* the friction.

---

## The Practitioner's Checklist

Stop asking "Is this architecture smart?" Start asking "What is the Friction Score?"

1.  **Kernel Shape (`GA`):** Can 90% of the FLOPs be expressed as big batched Matrix Multiplications (GEMMs)?
    *   *If No (KANs):* **Red Flag.**
2.  **Memory Access (`MAL`):** Does it tile efficiently into SRAM, or does it thrash HBM with large intermediate maps?
    *   *If Thrash (Standard Attention):* Needs a Flash-style kernel rewrite. **Yellow Flag.**
3.  **Parallelism (`PAR`):** Is training O(1) parallel (Transformers) or O(N) sequential (RNNs/Pure SSMs)?
    *   *If Sequential:* Training will be slow/expensive. **Orange Flag.**
4.  **Serving Topology (`STI`):** Does inference require complex routing or state management across nodes?
    *   *If Yes (MoE):* Requires custom serving stack. **Yellow Flag.**
5.  **Infra Maturity (`IM`):** Is the kernel available *today* in upstream vLLM/PyTorch?
    *   *If No:* You are the research team. Do you have the budget for that?

---

## Conclusion

We are not designing neural networks on a whiteboard. We are leasing time on silicon heaters.

The "Hardware Compatibility Filter" was a nice metaphor, but the **Friction Map** is the reality on today’s NVIDIA‑dominated GPU stacks. The industry has converged on a narrow set of primitives—GEMMs, Flash Attention, SwiGLU—not because we lack imagination, but because **economic friction kills everything else.**

Innovation hasn't stopped. It has just moved to where the friction is lower: **Training** (post‑training, data curation) and **Hybrids** (MoE, Attention+SSM). Gate 1 says which ideas are even economically viable to try at scale; Gates 2 and 3—optimization behavior and scaling laws—decide which of those low‑friction ideas become the next default.

Looking ahead, the Friction Map makes concrete bets:
*   **Mixture‑of‑Depths** will appear in at least one >20B production model by 2027 as a niche cost/latency optimization—but it will not replace standard depth everywhere.  
*   **Titans‑style external memory** will remain research‑only unless vendors add first‑class hardware support and someone demonstrates ≥2× end‑to‑end cost/performance gains on real workloads.  
*   **Pure SSM frontier models** (≥30B, no attention) will not become top‑tier LLMs by 2028 unless they adopt attention‑like mechanisms for global routing and in‑context learning.

If any of these are wrong—if, say, a 40B pure SSM or a Titans‑style memory model becomes a flagship frontier LLM—this map needs to be redrawn. That’s the point. A useful friction heuristic is one you can test in public.

Don't fight the friction. Map it, price it, and decide if you can afford the toll. For the underlying tables, timelines, and citations behind this essay, see **Appendix A–D**.
