# The Transformer Lock-In

*How co-evolution of hardware and architecture created a stable equilibrium that alternatives cannot escape.*

---

In 2023, Mamba promised to replace attention with elegant state-space math that scaled linearly with context. By 2024, the authors had rewritten the core algorithm to use matrix multiplications instead of scans. Their paper explains why:

> "We restrict the SSM structure to allow efficient computation via matrix multiplications on modern hardware accelerators."

The architecture changed to fit the hardware. The hardware did not budge.

This is **The Transformer Lock-In**: a stable equilibrium in which GPU silicon, software ecosystems, and institutional incentives align to ensure that every viable architecture either adopts the Transformer's computational pattern—or dies. Not because Transformers are mathematically optimal, but because a decade of co-evolution has locked in a single primitive as the substrate of modern deep learning: **the batched matrix multiplication**.

**A caveat up front:** I am not claiming hardware *caused* Transformers to dominate. Transformers emerged in 2017 on GPUs that already favored matrix multiplications. As Transformers scaled, NVIDIA optimized for them. As NVIDIA optimized, Transformers became even more efficient relative to alternatives. The feedback loop locked in. Whether hardware or architecture came first is now academically interesting but practically irrelevant. The reality in 2025 is structural: the lock-in is real, and every alternative architecture must navigate it or die.

---

## The Lock-In Mechanism: Two Reinforcing Gates

Alternatives face a two-gate filter:

**Gate 1: Hardware Compatibility**  
Can your architecture efficiently use NVIDIA's Tensor Cores—the specialized matrix-multiply units that deliver 1,000 TFLOPS on an H100? If not, you pay a 10–100× compute tax. At frontier scale ($50–100M training runs), that tax is fatal.

**Gate 2: Institutional Backing**  
Even if you clear Gate 1, you need a major lab to make it their strategic bet. Without that, your architecture lacks: large-scale validation, production tooling, ecosystem support, and the confidence needed for others to adopt it.

**The lock-in strength:** These gates reinforce each other. Poor hardware compatibility makes institutional bets unattractive (too risky, too expensive). Lack of institutional backing means no investment in custom kernels or hardware optimization (keeping friction high). Breaking out requires changing both simultaneously—a coordination problem no single actor can solve.

---

## Gate 1: The Hardware Primitive

A Transformer is not an abstract architecture. It is a specific compute pattern that happens to be precisely what NVIDIA's hardware executes fastest.

On an H100, approximately 1,000 Tensor Cores operate in parallel. Each Tensor Core instruction performs a 4×4 matrix multiply-accumulate in a single cycle. When these cores are saturated with large, batched matrix multiplications (GEMMs), the chip delivers roughly 1,000 TFLOPS in FP16. When the workload cannot be expressed as batched GEMMs, throughput drops by 10× to 100×.

The Transformer architecture is ~90% GEMMs by FLOP count: the Q/K/V projections, the attention matmul, the feedforward layers. Everything else—softmax, layer norms, residual adds—is negligible compute. FlashAttention made even the attention mechanism itself SRAM-resident and tiled, eliminating the only remaining memory bottleneck.

| **Architecture** | **Core Operation** | **Tensor Core Utilization** | **Relative Throughput** |
|------------------|-------------------|---------------------------|------------------------|
| Transformer (standard) | Batched GEMM | 80–90% | 1.0× (baseline) |
| Transformer (FlashAttention) | Tiled GEMM | 85–95% | 1.2–1.5× |
| Mamba-1 (parallel scan) | Sequential scan | 10–20% | 0.1–0.2× |
| Mamba-2 (GEMM-based) | Block-diagonal GEMM | 60–70% | 0.6–0.8× |
| LSTM/GRU | Recurrent matmul | <5% (train), 40–60% (inference) | 0.05–0.6× |
| Neural ODEs | Iterative solver | 5–15% | 0.05–0.15× |

**This is Gate 1's mechanism.** Any architecture that achieves high Tensor Core utilization will be competitive on cost-per-token. Any architecture that cannot will pay a compute tax. At frontier scale, a 10× tax on a $100M training run is a $900M deficit.

---

## The Lock-In Is Directional

NVIDIA is not building "AI chips." They are building **Transformer-optimized chips.**

The Blackwell architecture (B200, shipping 2024) includes a "Second-Generation Transformer Engine" and adds native FP4/FP6 Tensor Cores—lower-precision GEMMs, approximately 2× faster than H100's FP8. The Rubin architecture (R100, roadmapped for 2026–2027) headlines "3× Faster Attention" and disaggregated memory for million-token context windows.

What is absent from both roadmaps: any silicon support for the primitives that alternative architectures require—parallel scans (essential to SSMs), recurrence acceleration (essential to RNNs), or irregular memory access patterns (essential to mixture-of-experts routing and certain spline-based networks).

NVIDIA's roadmap from 2024 through 2027 is an implicit bet that Transformers will remain dominant through at least 2028. This is not neutral infrastructure; it is directional investment that narrows the competitive landscape for alternatives.

---

## Why Alternatives Fail: The Scan Bottleneck

A parallel scan is an O(N) sequential algorithm that propagates state from one token to the next. Even when chunked into blocks—as Mamba-1 and state-space models do—it cannot fully saturate Tensor Cores the way a batched matmul can. The fundamental issue is **data dependency**: each chunk's output depends on the previous chunk's final state, creating a bottleneck that cannot be parallelized away.

This is not a software limitation. It is a consequence of hardware architecture. Tensor Cores are designed for **data-parallel** operations on independent matrix tiles. Scans are **data-dependent**: they serialize across the sequence dimension. Clever kernel engineering can mitigate the penalty—Mamba-2 achieved a 2–3× speedup over Mamba-1 by restructuring its math—but cannot eliminate it.

The same analysis applies to:

- **LSTMs/GRUs**: High GEMM alignment for weight matrices, but O(N) sequential dependency over time steps. Training cannot parallelize across sequence length, making them uncompetitive at frontier scale.
- **Neural ODEs**: Fundamentally iterative solvers with many small matmuls and poor memory locality. Beautiful mathematics; catastrophic GPU economics.
- **Spline-based networks (e.g., KANs)**: Per-edge function evaluations cannot be batched. Hundreds of tiny, irregular operations starve Tensor Cores.

The hardware gate is not a subjective preference. It is the mechanical consequence of optimizing for FLOPS/dollar on NVIDIA GPUs.

---

## The Evidence: Three Architectures That Map the Lock-In

### 1. Mamba-2 (2024): Cleared Gate 1, Stuck at Gate 2

Mamba-1's elegance came from its parallel scan—a recurrence that propagated state efficiently over long sequences. But on H100s, the scan was a bottleneck. Mamba-2's authors explicitly redesigned the math to use block-diagonal GEMMs instead.

**The result:**
- Mamba-1's core operation: parallel scan (10-20% Tensor Core utilization)
- Mamba-2's core operation: matrix multiplication (60-70% utilization)
- Measured speedup on H100: 2–3× vs. Mamba-1

Mamba-2 survived by becoming **more Transformer-like in its compute pattern**, even though it retained the recurrence semantics. This is Gate 1 at work: the architecture bent to fit the silicon.

**But did it succeed?** As of December 2025, Mamba-2 remains research-only. No frontier lab has deployed a pure Mamba-2 model at 30B+ scale. The only production deployment is **Bamba** (IBM, 9B parameters)—a **hybrid** that mixes Mamba blocks with standard Transformer attention layers.

Bamba's existence proves two things:
1. GEMM-alignment (Gate 1) is necessary but not sufficient
2. The winning strategy isn't "replace Transformers"—it's "optimize within the Transformer frame"

Mamba-2 cleared the hardware gate but died at the institutional gate. No major lab made it their strategic bet.

### 2. RetNet (2023): The Ambiguous Failure

RetNet is the most revealing case study—because we don't actually know *why* it failed.

Microsoft Research published RetNet in July 2023. On paper: parallel training (GEMM-aligned), 8.4× faster inference, 70% memory savings, Transformer-matching perplexity up to 6.7B parameters. By the Gate 1 analysis, RetNet should have passed.

**Then Microsoft abandoned it.** Five months later: Phi-2 (dense Transformer). Then Phi-3 (MoE Transformer). Then Phi-4 (long-context Transformer). The co-authors didn't bet on their own architecture.

**Why? Three plausible explanations:**

**Explanation A: Hidden Technical Failure**  
Microsoft tried scaling to 13B/30B internally and hit quality degradation, training instability, or capability gaps. The research literature hints at a potential bottleneck: *"RetNet's hidden-state bottleneck might limit its ability to capture very long-range or arbitrary associations... in Transformers, any token can attend to any prior token directly, but in RetNet, information must flow through a fixed-size state."*

If this bottleneck manifests as poor performance on reasoning tasks or factual recall at scale, RetNet's abandonment is **hardware-rational**, not social. The low GEMM utilization might only emerge at 40-80 layers (frontier scale) where the recurrent state becomes a memory/bandwidth bottleneck.

**Explanation B: Institutional Risk Aversion**  
RetNet works fine, but Microsoft chose not to gamble on an unproven architecture when Transformers have a track record to 100B+ parameters. Research notes: *"Organizations are understandably cautious about abandoning a known-good architecture... without a clear demonstration of superiority."*

**Explanation C: Ecosystem Immaturity**  
RetNet lacks the tooling, kernels, and infrastructure that Transformers enjoy. *"Frameworks like Hugging Face Transformers only recently got unofficial RetNet implementations... inference servers needed modifications to handle state-space models."* The engineering tax was too high.

**What we know for certain:**  
2.5 years after publication, the largest RetNet model is 3B parameters (community-built). No 7B. No 13B. No frontier deployment. No major lab investing in it.

RetNet proves that **absence of published failure is not evidence of success.** The lock-in may have crushed it via hidden hardware friction that only emerges at scale (Gate 1)—or via institutional risk-aversion and ecosystem gaps (Gate 2)—or both. Without a 30B+ publicly trained model, we'll never know which gate killed it.

### 3. RWKV (2021–2024): Community Persistence Without Institutional Backing

RWKV is a pure RNN architecture (Receptance Weighted Key-Value) that achieves parallel training and O(N) inference. Unlike RetNet, it has been scaled to **14B parameters** by an open-source community—larger than any RetNet or Mamba-1 model.

**Why did RWKV scale further?**  
Not hardware optimization (it's fully recurrent, similar Tensor Core utilization to RetNet). The difference is **sustained community backing**. Developer BlinkDL and contributors spent years optimizing, training, and validating RWKV models. The 14B model roughly matches GPT-NeoX-20B (a Transformer) on perplexity benchmarks.

**But even RWKV hit the institutional gate:**  
No major lab adopted it. No frontier-scale deployment (30B+). Training the 14B model took longer than an equivalent Transformer, and community reports note struggles with certain reasoning tasks.

RWKV proves that **Gate 2 is independent of Gate 1**. You can have mediocre hardware compatibility and still scale to 14B—if you have persistent institutional backing (even from a distributed community). But without a major lab's resources, you won't reach 70B or 400B.

---

## The Rebels and the Coordination Problem

Alternative hardware exists. Cerebras's Wafer-Scale Engine-3 has 21 PB/s memory bandwidth—enough to make fine-grained recurrence economical. Groq's LPU is SRAM-only and efficient at sequential processing. SambaNova's dataflow architecture could plausibly accelerate scan-based models.

But these vendors collectively hold less than 5% of the AI accelerator market (by revenue), and they face a brutal chicken-and-egg problem:

1. **Researchers won't target niche hardware** until it has enough install base to matter.
2. **The install base won't grow** until there's a compelling software stack and frontier models.
3. **The software stack won't mature** until researchers and companies invest in it.

Breaking this loop requires a major frontier lab to make a **strategic bet**—the way Google did with TPUs in 2016. Google's TPU bet succeeded because:
- They mandated JAX/XLA as the software stack (ecosystem control)
- They deployed TPUs internally at massive scale (install base)
- They trained frontier models (PaLM, Gemini) exclusively on TPUs (validation)

Without all three, alternative hardware remains niche. As of 2025, no alternative vendor has secured that level of commitment from a frontier lab.

---

## What Would Falsify This Framework?

A useful thesis makes falsifiable predictions. Here are three for 2027–2028:

**1. No pure non-GEMM frontier model will emerge.**  
By 2028, no pure state-space or recurrent architecture (≥30B parameters, no attention mechanism) will rank as a top-tier LLM on standard benchmarks. Every high-performing "alternative" will be either a hybrid with attention layers or will use GEMM-aligned primitives.

**2. Titans-style external memory will remain research-only.**  
Architectures requiring explicit external memory modules (à la Titans, 2024) will not ship as flagship frontier models until dedicated hardware support emerges. The serving topology changes are too severe for current infrastructure.

**3. Alternative chip vendors will not exceed 10% market share without a frontier lab partnership.**  
Cerebras, Groq, and SambaNova will not collectively exceed 10% revenue share by 2028 unless a major lab (OpenAI, Anthropic, Meta, DeepSeek, Google) makes a strategic hardware commitment comparable to Google's TPU bet.

If any of these predictions fail—if a 40B pure SSM dominates benchmarks, or Groq captures 15% market share organically—the lock-in thesis needs revision. The predictions are designed to be crisp and observable.

---

## What This Means for Practitioners

### For Researchers

Your "alternative" architecture is converging toward the Transformer compute pattern whether you realize it or not. The successful research strategy is not to fight the lock-in but to understand which of your ideas can survive the two-gate filter.

**Heuristic:** If your innovation requires custom CUDA kernels that are not upstream in PyTorch or JAX, it will not scale without significant institutional backing. Plan accordingly: either secure that backing early, or design your architecture to use standard primitives. Mamba-2 succeeded where Mamba-1 struggled because it aligned with GEMMs.

### For Startups

Do not bet against the hardware moat unless you have a credible path through both gates. If your architecture is not GEMM-aligned, you are paying a 10–100× compute tax. That may be acceptable for a research demo; it is fatal at production scale.

**Heuristic:** If it's not in PyTorch upstream with optimized kernels, wait for the giants to pay the integration tax. You ride on their work once it lands. FlashAttention became viable for startups only after it was battle-tested at Meta and upstreamed to PyTorch. RetNet and Mamba-1 are not there yet.

### For Investors

The TAM for "alternative AI chips" is constrained by the coordination problem, not raw capability. Cerebras and Groq can build superior silicon for specific workloads, but they cannot unilaterally build superior ecosystem compatibility.

**Investment thesis filter:** Does the alternative chip vendor have a signed partnership with a frontier lab willing to train a 30B+ model exclusively on their hardware? If no, the path to 10%+ market share requires a 7–10 year time horizon and exceptional execution. Historical precedent: Google's TPU took 6 years and $billions in internal subsidies to reach maturity.

---

## Conclusion: The Local Optimum

We are in a stable equilibrium.

Transformers and GPU hardware co-evolved over the past decade. They shaped each other. Now they are locked together by:
- **Hardware specialization** (Tensor Cores optimized for GEMMs)
- **Software ecosystems** (PyTorch, JAX, vLLM all Transformer-native)
- **Economic incentives** (training a 100B Transformer is well-understood; training a 100B alternative is a costly experiment)
- **Institutional momentum** (every major lab has Transformer expertise, tooling, and validated scaling laws)

Breaking out requires simultaneously changing hardware, architecture, ecosystem, and economic incentives. No one currently has the capital, coordination, or incentive to do all four at once.

The alternatives that survive—Mamba-2, Bamba, RetNet (if it returns)—do so by **wearing the Transformer as a disguise**. They adopt GEMM-aligned compute patterns (Gate 1) and hybrid architectures that keep one foot in the proven Transformer world (Gate 2).

The Transformer monopoly is not accidental. It is structural. And it will not break until the structural constraints break first.

**The next architectural breakthrough will not replace the Transformer. It will optimize within its constraints.**

---

## Further Reading

- [**The Hardware Friction Map**](link) — The companion practitioner's guide with the Gate-1 checklist and friction rubric
- **The Scored Dataset** — 100+ architectures scored on the 5-axis friction rubric ([GitHub repository](link))
- **Mamba-2 Paper** — Section 3 on hardware-aware design (arXiv:2405.21060)
- **RetNet: A Successor to Transformer** — Microsoft Research (arXiv:2307.08621)
- **IBM Bamba Release** — Production hybrid SSM+Attention model (IBM Research Blog, 2025)
- **NVIDIA Blackwell/Rubin Announcements** — Official roadmaps (NVIDIA Blog)
- **SemiAnalysis** — Deep technical analysis of AI chip economics

---

*For questions, corrections, or case studies of architectures that escaped the lock-in, contact [author info]. This essay is part of a series on neural architecture economics. For the practitioner-focused Gate-1 checklist, see the companion "Hardware Friction Map" essay.*
