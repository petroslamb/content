# Appendix — Evidence for the Hardware Friction Map

This appendix collects the minimum on‑page evidence needed to support the main claims in *The Hardware Friction Map* essay when published as a standalone Substack piece.

It is not exhaustive; the full research notebooks and datasets live in the project’s research artifacts. This appendix prioritizes:
- MoE throughput vs context length.  
- Pure SSM scale vs hybrid dominance.  
- A compact Gate‑1 friction zones table.

---

## Appendix A — MoE Throughput

**Honest MoE Speedups (2017–2025, synthesized from 18 sources)**

| Context Length | Throughput vs 128‑token baseline | Notes |
|----------------|-----------------------------------|-------|
| 128 tokens     | 1.0× (baseline)                   | “Marketing regime” — vendors quote 5–7× vs dense here. |
| 256–512 tokens | ~0.9–1.0×                         | Minor degradation; most MoE speedup preserved. |
| 1024 tokens    | ~0.8×                             | ≈20% lower throughput vs 128 tokens. |
| 2048 tokens    | ~0.7×                             | ≈30% lower throughput vs 128 tokens. |
| 4096 tokens    | ~0.5–0.6×                         | Quadratic scaling dominates without specialized tricks. |

| >32K (Qwen3‑Next, specialized) | up to ~10× vs naive MoE | Architectures co‑designed for long context (256K) claw back throughput. |

**Summary:**
- Well‑optimized MoE delivers ≈2.0–2.5× throughput vs dense at short context (where most marketing numbers are measured).  
- As context grows, speedups erode sharply unless you redesign the entire memory and routing path (e.g., Qwen3‑Next, DeepSeek‑V3).  
- MoE is a **throughput and capacity optimization**, not a magic 7× that holds at 32K+ contexts.

---

## Appendix B — Pure SSM Scale and Hybrid Dominance

**Where Pure Mamba/SSM Exists (as of Dec 2025)**  
(condensed from the SSM/mamba evidence survey)

| Scale | Architecture                | Notes                                                    |
|-------|----------------------------|----------------------------------------------------------|
| 130M  | Pure Mamba                 | Matches transformer baselines on standard benchmarks.    |
| 370M  | Pure Mamba                 | Competitive with same‑scale transformers.                |
| 1.4B  | Pure Mamba                 | Competitive with same‑scale transformers.                |
| 2.8B  | Pure Mamba                 | Matches or beats 2.8B transformers; approaches 7B baselines. |
| 7B    | Falcon Mamba 7B (pure)     | Outperforms Llama 3.1 8B, Mistral 7B; strong long‑seq throughput. |
| 13B+  | **No pure SSM models found** | Above this scale, only **hybrids** are deployed (SSM + attention or variants). |

**Representative large hybrids:**
- **Jamba (AI21):** Alternating Mamba + attention blocks.  
- **Falcon‑H1 (TII):** Parallel hybrid blocks (attention + Mamba‑2 heads).  
- **Qwen3‑Next:** Linear attention + gated attention + MoE; three‑way hybrid.  
- **RWKV variants:** RNN‑like state updates with attention‑like components.

**Takeaways:**
- Pure SSMs are **proven and competitive** up to 7B.  
- From ~13B upwards, every serious architecture we see in the wild uses **hybrids**—state‑space blocks for local/sequential structure, attention‑like mechanisms for global routing and in‑context learning.  
- The essay’s bet (“pure SSMs will not be frontier without attention‑like components”) is a statement about this **observed ceiling plus the parallelism gap**, not a mathematical impossibility.

---

## Appendix C — Gate‑1 Friction Zones (Mini Table)

This table maps a few representative techniques into Gate‑1 friction zones. It is intentionally small; the full scorecard includes more axes and more entries.

| Technique                  | Type              | Gate‑1 Friction Zone | Reason (sketch)                                  |
|---------------------------|-------------------|----------------------|--------------------------------------------------|
| RoPE / RMSNorm            | Weight‑only tweak | 🟢 Green             | Pure matmuls + elementwise ops; no serving change. |
| GQA                       | Weight‑only tweak | 🟢 Green             | Same kernels, smaller KV cache; drop‑in.         |
| LoRA / QLoRA              | Fine‑tuning method| 🟢/🟡 Green‑ish      | Matmul‑friendly; infra friction mainly eval/tooling. |
| FlashAttention            | Kernel rewrite    | 🟡 Yellow            | New kernels + framework integration, same topology. |
| Quantization (Int8/Int4)  | Kernel variant    | 🟡 Yellow            | New kernels, easier serving; slowed by eval/safety. |
| Mixture‑of‑Experts (MoE)  | System‑level      | 🟠/🔴 Orange/Red     | New topology, routing, expert parallelism.       |
| Pure SSMs at frontier     | Architectural     | 🟠 Orange            | Training‑parallelism gap at very large scale.    |
| KANs                      | Architectural     | 🔴 Red               | Poor GEMM alignment; hard to batch, cache‑unfriendly. |

**What this shows:**
- Genuinely low‑friction (Green) primitives like RoPE/RMSNorm/GQA diffuse quickly once they demonstrate clear benefits.  
- Medium‑friction (Yellow) primitives like FlashAttention and quantization diffuse on a 1.5–2‑year cadence, gated by kernel and ecosystem work.  
- High‑friction (Orange/Red) ideas (MoE, pure SSMs at frontier, KANs) either:  
  - remain research toys,  
  - or require **massive capital and infra control** to deploy (MoE at frontier labs).

---

## Appendix D — References (Selected)

This is a non‑exhaustive list of the most important external references underpinning the essay. It is curated for Substack readability; the full bibliography is in the project’s master references.

**Mixture‑of‑Experts**
- Fedus et al., 2021 — *“Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity”* (arXiv:2101.03961).  
- Shazeer et al., 2017 — *“Outrageously Large Neural Networks”* (early MoE).  
- Du et al., 2021 — *“GLaM: Efficient Scaling of Language Models with Mixture-of-Experts”*.  
- DeepSeek‑V3 and DeepSeek‑R1 technical reports (2024–2025).  
- Mixtral‑8×7B technical report (Mistral, 2023–2024).  
- Meta Llama 4 (Scout/Maverick) model cards (first Llama MoE generation).

**FlashAttention & Kernels**
- Tri Dao et al., 2022 — *“FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness”* (arXiv:2205.14135).  
- Tri Dao et al., 2023 — *“FlashAttention‑2”* (arXiv:2307.08691).  
- PyTorch 2.2 release notes for `scaled_dot_product_attention` with FlashAttention backends.

**SSM / Mamba**
- Gu et al., 2021 — *“Efficiently Modeling Long Sequences with Structured State Spaces (S4)”* (arXiv:2111.00396).  
- Gu & Dao et al., 2023 — *“Mamba: Linear-Time Sequence Modeling with Selective State Spaces”* (arXiv:2312.00752).  
- Falcon Mamba 7B model card and technical brief (TII, 2024).  
- Jamba, Falcon‑H1, and Qwen3‑Next technical reports (hybrid architectures).

**Core LLM Architectures**
- Llama 2/3/4 technical reports and model cards (Meta).  
- Gemma 2 technical report (Google).  
- Qwen2.5 and Qwen3‑Next technical reports (Alibaba).  
- Mistral 7B and Mixtral‑8×7B technical reports (Mistral).  
- DeepSeek‑V2/V3/R1 technical reports.

**Other Primitives & Outliers**
- KANs (Kolmogorov‑Arnold Networks) original paper.  
- Neural ODEs — Chen et al., 2018 *“Neural Ordinary Differential Equations”* (NeurIPS Best Paper).  
- Representative linear‑attention papers (e.g., Performer, Nyströmformer).  
- RevNet / Reversible Residual Network papers (memory‑free backprop).

For a fuller, systematically organized bibliography, see the “Research References (Core Citations)” document in the project’s references.

