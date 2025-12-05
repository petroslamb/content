# The Hardware Compatibility Filter

*Why GPU primitives—not benchmarks—explain which AI architectures actually make it to production.*

---

The last two years of neural architecture can be summarized in one sentence: **hardware compatibility determines what survives.**

FlashAttention won not because it was smarter, but because it respected the GPU memory hierarchy. Mixture-of-Experts took 36 months to go from research to production because serving infrastructure had to catch up. Pure State Space Models have stalled at 7B parameters because they fight the GPU's need for parallelism. KANs generated enormous hype and zero production deployments because spline evaluations don't map to tensor cores.

This isn't about which ideas are "better." It's about which computations silicon can efficiently express.

---

## The Filter in Action

Modern GPUs are optimized around three properties: dense matrix multiplications on tensor cores, hierarchical memory (small fast SRAM, large slow HBM), and massive parallelism. Techniques that align with these properties spread quickly. Techniques that fight them stall—regardless of benchmark results.

**FlashAttention** is the canonical example. Published in May 2022, it didn't propose new math. It proposed a new memory access pattern. Standard attention materializes a massive N×N matrix in HBM, reading and writing gigabytes per token. FlashAttention tiles the computation so blocks fit in SRAM, computes attention locally, and discards intermediates without ever writing the full matrix.

The result: 2-4× speedups and 10-20× memory savings at long sequences. Same exact math. Different relationship with the hardware.

It took 24 months—until PyTorch 2.2 in January 2024—for FlashAttention to become a standard library call. By May 2024, every major model (Llama 3, Gemma 2, Phi-3) relied on it by default. The technique was proven in 2022. The infrastructure caught up in 2024.

**Grouped-Query Attention (GQA)** moved faster. Published in May 2023, it was standard practice by April 2024—roughly 12 months. Why? Because it's a weight-only change. Share Key and Value heads across multiple Query heads. The KV cache shrinks by 8×. Memory bandwidth drops. But no new kernels are required. You change the model definition, retrain, and ship.

The pattern is clear: **integration cost predicts adoption speed.**

---

## The Infrastructure Lag Model

Looking across techniques from 2021-2025, a consistent timeline emerges:

**Level 1: Weight-only changes (12-18 months)**
Examples: GQA, RoPE, RMSNorm. You modify the model definition. No new CUDA kernels. No changes to serving infrastructure. Adoption is gated by retraining cycles.

**Level 2: Kernel-level changes (24-30 months)**
Examples: FlashAttention. You need custom CUDA or Triton kernels. These must be written, optimized, tested, integrated into libraries, merged into frameworks, and validated in production stacks. Each step takes time.

**Level 3: Serving infrastructure changes (36-48 months)**
Examples: Mixture-of-Experts. Not just kernels—you need new distributed system behaviors. How do you shard experts across nodes? How do you balance load at inference time? How do you handle stragglers? This requires changes to vLLM, TensorRT-LLM, and internal serving stacks at every major lab.

Switch Transformers were published in January 2021. Mixtral shipped in December 2023. Llama 4 (Meta's first MoE) arrived in April 2025. That's 36-48 months from research to mainstream.

This model is falsifiable. If a kernel-level technique becomes standard in under a year, or a serving-level technique diffuses in a single retraining cycle, the model is wrong. As of late 2025, it holds.

---

## What Didn't Work

The filter is easier to see in what failed.

**KANs (Kolmogorov-Arnold Networks)** proposed learnable spline-based activations instead of fixed weights. Theoretically elegant. Small-scale benchmarks looked promising. But spline evaluation doesn't map to dense matrix multiplication. Each edge requires per-token evaluation of basis functions—exactly the kind of irregular, fine-grained computation GPUs hate.

As of December 2025: no production deployments at any scale. The hardware compatibility filter rejected them.

**Pure State Space Models (Mamba)** promised linear-time sequence modeling. Replace attention's O(n²) with a recurrent state that updates in O(n). The math is beautiful. The efficiency gains are real—at small scale.

But SSMs have a parallelism problem. Transformers process all tokens simultaneously during training. SSMs have sequential state dependencies: state t depends on state t-1. Mamba's parallel scan algorithm mitigates this, but the fundamental operation is still harder to parallelize than brute-force attention matmuls.

The evidence is striking. Pure Mamba exists and works at 130M, 1.4B, 2.8B, and 7B (Falcon Mamba). But there's no public evidence of a pure SSM at 13B, 70B, or frontier scale. Every large SSM-style deployment is a hybrid—Mamba layers mixed with attention layers. The hybrids work because attention handles global dependencies while SSM handles local efficiency. Pure SSMs haven't crossed the scaling threshold.

**Neural ODEs** won NeurIPS Best Paper in 2018. Continuous depth! Infinite adaptability! ODE solvers run iteratively and sequentially. They fight the GPU's need for massive, regular parallel batches. Zero adoption in frontier LLMs.

The lesson: compositionality that survives is **permissive**, not **prescriptive**. MoE provides a pool of experts and a router, but doesn't dictate what experts should learn—gradient descent figures that out. Neural ODEs and Capsule Networks tried to design the structure explicitly. They didn't cross the production chasm.

---

## MoE: The Reality Check

Mixture-of-Experts is the success story of 2024-2025—but strip away the marketing spin.

Vendors claim "5-7× speedups." Reality: **2-3× throughput improvement** over dense models of similar quality, with a median around 2.1-2.5× in production-style measurements.

The mechanism is real: DeepSeek-V3 has 671B total parameters but activates only 37B per token. You get the intelligence of a massive model with the latency of a smaller one. Meta's Llama 4 pivot (Scout: 109B total / 17B active; Maverick: 400B total / 17B active) confirms that MoE is now first-class at frontier labs.

But there's a trap. As context length grows, MoE's advantage shrinks. At short context (~128 tokens), you get the full 2-3× throughput benefit. At medium context (1-2K tokens), throughput erodes ~30%. At very long context (32K+), the effective advantage falls to ~1.3-1.5× as KV cache traffic and routing overhead dominate.

MoE is a **throughput and capacity optimizer**, not a magic fix. It buys "more model for the same serving budget"—but still runs into memory bandwidth limits at frontier context lengths.

---

## The Implication: Architecture Is Slowing

The last widely adopted fundamental primitive—attention—was introduced in 2017. Since then, we've seen refinements (Flash, GQA, MLA), composition operators (MoE), and hybrids (attention + SSM). But no clearly dominant replacement at frontier scale.

Hardware constraints have narrowed the space of acceptable operations tightly around dense matrix multiplication. Novel primitives must clear a high bar: they need to be expressible as big GEMMs, respect the memory hierarchy, and scale to production serving—or they remain research curiosities.

This doesn't mean architecture innovation has stopped. SSM-style blocks, hybrids, and long-context variants are active research areas. But the center of gravity has shifted.

**DeepSeek-R1** (January 2025) achieved state-of-the-art reasoning—79.8% on AIME, 97.3% on MATH-500—rivaling OpenAI's o1-class models. The architecture? MoE + MLA. The same primitives as DeepSeek-V3. The breakthrough came from **training**: large-scale reinforcement learning (GRPO) and a carefully engineered reasoning curriculum.

The architecture is the container. Training is the contents. We've spent 8 years optimizing the container. It's efficient, scalable, and hardware-compatible. Now we're learning how to fill it.

---

## The Practitioner's Heuristic

When evaluating a new paper or technique, ask:

1. **Does it map to GPU primitives?** Can the core operations be expressed as large batched matmuls? If not, treat it as a research bet, not a near-term production candidate.

2. **What's the integration level?** Weight-only changes ship in 12 months. Kernel changes take 24. Serving changes take 36. Plan accordingly.

3. **Is there frontier-scale evidence?** If the largest public deployment is 7B, don't assume it scales to 70B. Scaling has its own failure modes.

For concrete decisions:
- **Adopt now:** FlashAttention, GQA, RoPE, RMSNorm (all green-zone, upstream support)
- **Invest with eyes open:** MoE for scaling beyond 10B if you have serving budget
- **Track but don't bet on:** Pure SSMs until evidence above 7B appears
- **Ignore for production:** KANs, Neural ODEs, anything without production-grade kernels

---

## Conclusion

We are not designing neural networks in a vacuum. We are discovering which computations silicon can efficiently express.

The techniques that map naturally to GPU primitives—dense matmuls, tiled memory access, massive parallelism—survive and spread. The techniques that fight them become footnotes, regardless of their theoretical elegance.

For the foreseeable future on today's GPU-centric stacks, the leverage is in training innovation—RL-style post-training, data curation, optimization—not in searching for a wholesale "next Transformer."

The architecture wars haven't ended. But they've entered a slower phase. The competitive frontier is how we **train** and **use** the architectures we already have.

---

*For a detailed framework to evaluate new architectures, see the [Hardware Compatibility Design Review Kit](./Hardware_Compatibility_Design_Review_Kit_v1.md)—a 5-axis scorecard with calibrated examples.*
