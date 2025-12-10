# The Transformer Attractor

*Every "alternative" architecture either dies in the research lab—or survives by becoming a Transformer in disguise.*

---

In 2023, Mamba promised to replace attention with elegant state-space math that scaled linearly with context. By 2024, the authors had rewritten the core algorithm to use matrix multiplications instead of scans. Their paper explains why:

> "We restrict the SSM structure to allow efficient computation via matrix multiplications on modern hardware accelerators."

The architecture changed to fit the hardware. The hardware did not budge.

This is the **Transformer Attractor**: a stable equilibrium in which GPU silicon, software ecosystems, and economic incentives conspire to ensure that every viable architecture converges toward the same computational pattern. Not because Transformers are mathematically optimal, but because NVIDIA's ~85% market share in AI accelerators has hard-coded a single primitive into the substrate of modern deep learning: **the batched matrix multiplication**.

---

## The Attractor's Mechanism

A Transformer is not an abstract architecture. It is a specific compute pattern that happens to be precisely what NVIDIA's hardware executes fastest.

On an H100, approximately 1,000 Tensor Cores operate in parallel. Each Tensor Core instruction performs a 4×4 matrix multiply-accumulate in a single cycle. When these cores are saturated with large, batched matrix multiplications—the technical term is GEMMs (General Matrix Multiplies)—the chip delivers roughly 1,000 TFLOPS in FP16. When the workload cannot be expressed as batched GEMMs, throughput drops by 10× to 100×.

The Transformer architecture is ~90% GEMMs by FLOP count: the Q/K/V projections, the attention matmul, the feedforward layers. Everything else—softmax, layer norms, residual adds—is negligible compute. FlashAttention made even the attention mechanism itself SRAM-resident and tiled, eliminating the only remaining memory bottleneck.

**This is the attractor's gravity.** Any architecture that achieves high Tensor Core utilization will be competitive on cost-per-token. Any architecture that cannot will pay a 10–100× compute tax. At frontier scale—where a single training run costs $50–100M in compute—a 10× tax is a death sentence.

---

## The Lock-In Is Deliberate

NVIDIA is not building "AI chips." They are building **Transformer chips.**

The Blackwell architecture (B200, shipping 2024) includes a "Second-Generation Transformer Engine" and adds native FP4/FP6 Tensor Cores—lower-precision GEMMs, approximately 2× faster than H100's FP8. The Rubin architecture (R100, roadmapped for 2026–2027) headlines "3× Faster Attention" and disaggregated memory for million-token context windows.

What is absent from both roadmaps is any silicon support for the primitives that alternative architectures require: parallel scans (essential to SSMs), recurrence acceleration (essential to RNNs), or irregular memory access patterns (essential to mixture-of-experts routing and spline-based networks).

NVIDIA's roadmap from 2024 through 2027 is an implicit bet that Transformers will remain dominant through at least 2028. This is not neutral infrastructure; it is directional investment that narrows the competitive landscape for alternatives.

---

## Why Alternatives Fail: A Mechanism, Not a Conspiracy

A parallel scan is an O(N) sequential algorithm that propagates state from one token to the next. Even when chunked into blocks—as Mamba-1 and state-space models do—it cannot fully saturate Tensor Cores the way a batched matmul can. The fundamental issue is **data dependency**: each chunk's output depends on the previous chunk's final state, creating a bottleneck that cannot be parallelized away.

This is not a software limitation. It is a consequence of hardware architecture. Tensor Cores are designed for **data-parallel** operations on independent matrix tiles. Scans are **data-dependent**: they serialize across the sequence dimension. Clever kernel engineering can mitigate the penalty—Mamba-2 achieved a 2–3× speedup over Mamba-1 by restructuring its math—but cannot eliminate it.

The same analysis applies to:

- **LSTMs/GRUs**: High GEMM alignment for weight matrices, but O(N) sequential dependency over time steps. Training cannot parallelize, making them uncompetitive at frontier scale.
- **Neural ODEs**: Fundamentally iterative solvers with many small matmuls and poor memory locality. Beautiful mathematics; catastrophic GPU economics.
- **Spline-based networks (e.g., KANs)**: Per-edge function evaluations cannot be batched. Hundreds of tiny, irregular operations starve Tensor Cores.

The attractor is not a subjective preference. It is the mechanical consequence of optimizing for FLOPS/dollar on NVIDIA hardware.

---

## The Evidence: Three Architectures That Prove the Pattern

### 1. Mamba-2 (2024): The Conversion

Mamba-1's elegance came from its parallel scan—a recurrence that propagated state efficiently over long sequences. But on H100s, the scan was a bottleneck. Mamba-2's authors explicitly redesigned the math to use block-diagonal GEMMs instead.

The result:

- Mamba-1's core operation: parallel scan (poor Tensor Core utilization)
- Mamba-2's core operation: matrix multiplication (high Tensor Core utilization)
- Measured speedup on H100: 2–3× vs. Mamba-1

Mamba-2 survived by becoming **more Transformer-like in its compute pattern**, even though it retained the recurrence semantics. This is the attractor at work: the architecture bent to fit the silicon.

### 2. DeepSeek-MLA (2024): The Optimization

DeepSeek's V2 and V3 models did not attempt to replace attention. They optimized it. Multi-Head Latent Attention (MLA) projects tokens into a lower-dimensional latent space before attention, compressing the KV cache by approximately 8–10×.

The critical insight: MLA keeps all heavy operations as dense matmuls. The down-projection, the attention itself, and the up-projection are all standard GEMMs. Nothing about serving topology changes; only the latent dimension shrinks.

DeepSeek-MLA is not an "alternative" to Transformers. It is a **more efficient Transformer variant**, which is precisely why it shipped in production while pure SSMs remained research projects.

### 3. RetNet (2023): The Ghost Winner

Microsoft Research and Tsinghua published RetNet in July 2023. It was architecturally elegant: three compute modes—parallel (training), recurrent (inference), and chunkwise (long context)—with attention-competitive quality and lower memory footprint.

By the Gate-1 friction analysis, RetNet should have succeeded. Its parallel training mode is fully GEMM-aligned (GA=2), memory-efficient like FlashAttention (MAL=2), and fully parallelizable (PAR=2). The serving topology is standard—no exotic routing or memory systems (STI=2). **RetNet scores H≈6, matching Transformers on hardware compatibility.**

So why did it fail?

**The timeline tells the story.** As of December 2025—2.5 years after publication—the largest RetNet model is 3B parameters, released by small independent teams on HuggingFace. No 7B model. No frontier-scale deployment. No production serving stack.

**Microsoft itself abandoned it.** Five months after co-authoring the RetNet paper, Microsoft released Phi-2 as a dense Transformer. Then Phi-3. Then Phi-4. All Transformers, none RetNet. The institutional signal was clear: even the co-authors didn't bet on it.

RetNet proves that hardware compatibility is **necessary but not sufficient**. The attractor has three components: hardware primitives, architectural design, *and* institutional momentum. Without a major lab making it their strategic bet—the way Meta bet on Llama or DeepSeek bet on MLA—an architecture dies even if its friction scores are favorable.

This is a different failure mode than Mamba-1 (hardware-hostile) or Titans (topology-breaking). RetNet failed socially, not technically. And 2.5 years is long enough to know it's not coming back.

---

## The Rebels and Their Problem

Alternative hardware exists. Cerebras's Wafer-Scale Engine-3 has 21 PB/s memory bandwidth—enough to make fine-grained recurrence economical. Groq's LPU is SRAM-only and efficient at sequential processing. SambaNova's dataflow architecture could plausibly accelerate scan-based models.

But these vendors collectively hold less than 5% of the AI accelerator market (by revenue), and they face a brutal chicken-and-egg problem:

1. **Researchers won't target niche hardware** until it has enough install base to matter.
2. **The install base won't grow** until there's a compelling software stack and frontier models.
3. **The software stack won't mature** until researchers and companies invest in it.

Breaking this loop requires a major frontier lab to make a **strategic bet**—the way Google did with TPUs. Without that, the rebels will remain niche through at least 2028.

---

## The Honest Caveat: Cause or Consequence?

I am not claiming that hardware *caused* Transformers to dominate. The causal story is more nuanced:

**Transformers and GPUs co-evolved.** Transformers emerged in 2017 on GPUs that already favored matrix multiplications. As Transformers scaled, NVIDIA optimized for them. As NVIDIA optimized, Transformers became even more efficient relative to alternatives. The feedback loop locked in.

Whether the lock-in was cause or consequence is now academically interesting but practically irrelevant. The reality in 2024 is structural: NVIDIA's hardware roadmap is committed through 2027, and every alternative architecture must pay the tax that commitment imposes.

**What would falsify this framework?**

1. A pure non-GEMM architecture (SSM, RNN, or novel) that demonstrably scales better than Transformers at 100B+ parameters.
2. Alternative hardware (Cerebras, Groq, or new entrant) exceeding 10% market share without a frontier lab partnership.
3. NVIDIA adding scan cores or recurrence acceleration in a future architecture.

None of these are on the visible horizon through 2028.

---

## Three Predictions for 2027–2028

Useful frameworks make falsifiable predictions. Here are three:

**1. No pure SSM frontier model will emerge.**
By 2028, no pure state-space model (≥30B parameters, no attention mechanism) will rank as a top-tier LLM on standard benchmarks. Every high-performing "SSM" will be a hybrid with attention layers.

**2. Titans-style external memory will remain research-only.**
Architectures requiring explicit external memory modules (à la Titans, 2024) will not ship as flagship frontier models until dedicated hardware support emerges. The serving topology changes are too severe for current infrastructure.

**3. Alternative chip vendors will not exceed 5% market share without a frontier lab partnership.**
Cerebras, Groq, and SambaNova will remain niche through 2028 unless a major lab (OpenAI, Anthropic, Meta, DeepSeek, or equivalent) makes a strategic hardware commitment.

If any of these predictions are wrong—if a 40B pure SSM dominates benchmarks, or Groq captures 10% market share organically—the attractor thesis needs revision.

---

## What This Means for Practitioners

### For Researchers

Your "alternative" architecture is converging toward the Transformer compute pattern whether you realize it or not. The successful research strategy is not to fight the attractor but to understand which of your ideas can survive the hardware filter.

If your innovation requires custom CUDA kernels that are not upstream in PyTorch or JAX, it will not scale without significant institutional backing. Plan accordingly: either secure that backing, or design your architecture to use standard primitives.

### For Startups

Do not bet against the hardware moat. If your architecture is not GEMM-aligned, you are paying a 10–100× compute tax. That may be acceptable for a research demo; it is fatal at production scale.

**Heuristic:** If it's not in PyTorch upstream, don't build your company on it. Wait for the giants to pay the kernel tax. You ride on their work once it lands.

### For Investors

The TAM for "alternative AI chips" is constrained by lock-in, not capability. Cerebras and Groq can build superior silicon, but they cannot build superior PyTorch compatibility. Without a frontier lab partnership, the investment thesis for alternative chips requires a longer time horizon and higher risk tolerance than most portfolios can accommodate.

---

## Conclusion

We are in a local optimum.

Transformers and GPU hardware co-evolved over the past decade. They shaped each other. Now they are locked together in a stable equilibrium that resists perturbation.

Breaking out requires simultaneously changing hardware, architecture, ecosystem, and economic incentives. No one currently has the capital, coordination, or incentive to do all four at once.

The Transformer monopoly is not accidental. It is structural. And even its challengers—the Mambas, the RetNets, the MLAs—have survived only by aligning with it.

**The next architectural breakthrough will not replace the Transformer. It will wear it as a disguise.**

---

## Further Reading

- **The Hardware Friction Map** — The companion practitioner's guide with the Gate-1 checklist and friction rubric. [See companion essay]
- **The Scored Dataset** — 100+ architectures scored on the 5-axis friction rubric. [GitHub repository]
- **Mamba-2 Paper** — Section 3 on hardware-aware design (arXiv:2405.21060)
- **NVIDIA Blackwell/Rubin Announcements** — Official roadmaps (NVIDIA Blog)
- **SemiAnalysis** — Deep technical analysis of AI chip economics

---

*This essay is part of a series on neural architecture and hardware economics. For the practitioner-focused checklist and Gate-1 rubric, see "The Hardware Friction Map" companion essay.*
