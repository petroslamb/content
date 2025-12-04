
---

## Appendix: The Evidence

For the skeptical practitioner, we present the raw data underlying the claims in this post.

### Table 1: Major Lab Frontier Model Releases (2023–2025)
*Explicit model releases by major labs, ordered roughly chronologically. Architectures are summarized from public documentation as of Dec 4, 2025.*

| Lab | Model | First Release | Architecture (Public Info) |
| :--- | :--- | :--- | :--- |
| **Meta** | Llama 2 (7B/13B/70B) | **2023‑07‑18** | Dense decoder‑only transformer (RoPE, SwiGLU, RMSNorm; no MoE) |
| **Anthropic** | Claude 2 | **2023** | Generative pre‑trained transformer; closed weights, focus on constitutional AI |
| **Mistral** | Mistral 7B | **2023** | Dense decoder‑only transformer; competitive with LLaMA‑2 13B on benchmarks |
| **Mistral** | Mixtral 8×7B / 8×7B Instruct | **2023‑12** | **Sparse MoE** transformer (8 experts, ~12.9B active params per token) |
| **Google DeepMind** | Gemini 1.0 (Ultra/Pro/Nano) | **2023‑12‑06** | Multimodal transformer (text, image, audio, video, code) |
| **OpenAI** | GPT‑4 | **2023‑03‑14** | Multimodal transformer; detailed architecture (e.g., MoE vs dense) not public |
| **OpenAI** | GPT‑4 Turbo (incl. Vision) | **2023‑11** | GPT‑4‑class transformer optimized for 128K context and lower cost |
| **Meta** | Code Llama (7B/13B/34B/70B) | **2023‑08 / 2024‑01** | Code‑specialized Llama‑2 derivatives (dense transformer) |
| **Anthropic** | Claude 3 family (Opus / Sonnet / Haiku) | **2024‑03** | Multimodal transformer family with long context and sparse / conditional attention |
| **Google DeepMind** | Gemini 1.5 Pro | **2024** | Long‑context multimodal transformer; memory and sparse‑attention optimizations |
| **Google DeepMind** | Gemini 1.5 Flash | **2024** | Latency‑optimized Gemini 1.5 variant (same core architecture family) |
| **Meta** | Llama 3 (8B/70B) | **2024‑04‑18** | Dense transformer with Flash Attention, GQA, RoPE; 8B/70B open‑weight models |
| **Meta** | Llama 3.1 | **2024** | Extended Llama 3 variants (multilingual, multimodal, longer context) |
| **DeepSeek** | DeepSeek‑V2 | **2024‑05** | Open‑weight transformer; precursor to V2.5/V3 |
| **DeepSeek** | DeepSeek‑V2.5 | **2024‑09** | Improved V2 with extended context and training refinements |
| **DeepSeek** | DeepSeek‑V3 (Base / Chat) | **2024‑12** | Large transformer with DeepSeek Sparse Attention and long‑context training |
| **OpenAI** | GPT‑4o | **2024‑05‑13** | Natively multimodal transformer (text, vision, audio); dense architecture details undisclosed |
| **Mistral** | Magistral Small / Medium | **2025‑06‑10** | Reasoning‑oriented transformer models with chain‑of‑thought capabilities |
| **DeepSeek** | DeepSeek‑R1 | **2025‑01** | Reasoning model built on V3‑style backbone; open‑weight, MIT‑licensed |
| **Meta** | Llama 4 Scout | **2025‑04‑05** | **Mixture‑of‑experts transformer** (MoE pivot from dense Llama 3) |
| **Meta** | Llama 4 Maverick | **2025‑04‑05** | Larger MoE variant (more experts; ~constant active parameters per token) |
| **OpenAI** | GPT‑5 | **2025‑08‑07** | Multimodal frontier model; OpenAI has not publicly confirmed MoE vs dense internals |
| **DeepSeek** | DeepSeek‑V3.1 | **2025‑08‑21** | Updated V3 with hybrid “thinking / non‑thinking” modes |
| **DeepSeek** | DeepSeek‑V3.2‑Exp | **2025‑09‑29** | Experimental V3.2 using DeepSeek Sparse Attention for improved efficiency |
| **xAI** | Grok 4.1 | **2025‑11‑17** | Frontier transformer; public materials emphasize capabilities, not detailed architecture (MoE vs dense unspecified) |
| **Anthropic** | Claude 4 / 4.5 (Opus / Haiku) | **2025** | Next‑gen Claude transformers with hybrid reasoning and 200K‑token context windows |

**Insight:** From 2023 to late 2025, frontier lines clearly cluster into two patterns: (1) **Dense / sparse transformers** with ever‑better kernels (Flash Attention, GQA, long context, sparse patterns), and (2) **MoE transformers** (Llama 4, Mixtral) that trade implementation complexity for large capacity at similar active compute. Pure SSM models still do not appear as standalone frontier flagships; SSM/Mamba‑like blocks show up only as components inside hybrids or efficiency‑oriented models outside this list.

### Table 2: The MoE Reality Check
*Marketing claims vs. production-style measurements at long context (64K–128K tokens). Aggregated from Switch, Mixtral, DeepSeek-V3, deployment-inefficiency work, and Aurora-style system papers.*

| Metric | Marketing Claim | Reality in Large-Scale Deployments | The "Context Trap" |
| :--- | :--- | :--- | :--- |
| **Inference Speedup** | "5–7× faster" | **≈2–3× faster** vs. dense models of similar quality at moderate context | Falls toward **≈1.3–1.5×** as context grows (KV/cache + routing overhead dominate) |
| **Active Parameters** | "10% active" | **≈5–20% active** depending on depth and load balancing | Higher active % are often required for stability and quality |
| **Memory Savings** | "Same as small model" | **No VRAM savings** at peak: all experts still resident | Memory budget is set by total parameters, not active ones |
| **Throughput** | "Linear scaling" | **Better tokens/sec/$** than dense at similar quality | Throughput gains erode at very long context as memory bandwidth becomes the bottleneck |

**Insight:** MoE is primarily a **throughput and capacity optimizer**, not a magic fix for latency or memory. It buys "more model for the same serving budget," especially at moderate context, but still runs into bandwidth and KV-cache limits at frontier context lengths.

---

### Table 3: Pure SSM / Mamba Evidence Gap
*Where pure Mamba/SSM models have been demonstrated vs. where evidence stops (as of Dec 2025). Summarizes `ssm_benchmark_findings.md`.*

| Scale | Pure SSM Models | Evidence Status | Comparison vs Transformer | Production Usage |
| :--- | :--- | :--- | :--- | :--- |
| **130M–370M** | Original Mamba (Small/Base) | ✓ Proven (WikiText-103, PG-19) | Competitive with transformer baselines | Research and small-scale deployments |
| **1.4B–2.8B** | Original Mamba 1.4B / 2.8B | ✓ Proven (perplexity, downstream tasks) | Matches or beats similar-size transformers; approaches 2× larger baselines | Research and limited usage |
| **7B** | Falcon Mamba 7B | ✓ Proven; best pure SSM | Beats Llama 3.1 8B / Mistral 7B on many benchmarks; up to 5× throughput on long texts | Limited production use (efficiency-focused) |
| **13B** | None found | ✗ No pure SSM | Only transformer and hybrid models at this scale | No known production pure SSM |
| **70B+** | None found | ✗ No pure SSM | Frontier is exclusively transformer (dense, sparse, MoE, hybrids) | No known production pure SSM |

**Insight:** Pure SSMs are clearly viable up to 7B and can be very efficient, but there is **no evidence** of pure SSMs at 13B or frontier scales; above 7B, SSM-style blocks only appear inside **hybrid** architectures (Jamba, Falcon-H1, Qwen3-Next), not as end-to-end replacements for attention.

---

### Table 4: Infrastructure Lag Timeline
*Time from publication to standard production practice, grouped by integration complexity. Derived from `flash_attention_timeline.md`, MoE deployment studies, and GQA adoption data.*

| Technique | Change Type | Paper Published | Kernel / Framework Support | Standard Practice | Lag |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GQA** | Weight-only (model definition) | May 2023 | N/A (code change only) | 2024 (Llama 3, Gemma 2, etc.) | **≈12 months** |
| **Flash Attention (v1/v2)** | Kernel-level (CUDA + framework) | May 2022 | Jan 2024 (PyTorch 2.2, FA2) | May 2024 (Llama 3, Gemma 2, Phi-3) | **≈24 months** |
| **Mixture-of-Experts (Switch → Mixtral/DeepSeek/V3)** | Serving + distributed system | Jan 2021 (Switch) | 2023 (MegaBlocks/Triton, system stacks) | 2024 (Mixtral, Grok-1, DeepSeek-V2/V3) | **≈36 months** |

**Insight:** Integration cost determines adoption speed. Weight-only changes land within a retraining cycle; kernel changes take ~2 years to become ubiquitous; distributed system changes (e.g., MoE routing and large-scale sparse attention) take closer to 3 years.

---

### Table 5: GQA / MLA / Efficient Attention Adoption
*Snapshot of efficient attention mechanisms across major 2024–2025 model families, distilled from `major_lab_architecture_audit.md`.*

| Lab / Model Family | Attention Variant | Notes on Adoption |
| :--- | :--- | :--- |
| **Meta – Llama 3 / 3.1 / 3.2 / 3.3** | **GQA** | All sizes standardized on GQA + RoPE + RMSNorm; no MoE until Llama 4. |
| **Google – Gemini 1.x / 2.x** | MQA → GQA | Early Gemini uses MQA; later docs and analyses indicate GQA-style sharing for efficiency. |
| **Mistral – Mistral 7B** | **GQA + SWA** | Uses GQA plus sliding-window attention for long context. |
| **Mistral – Mixtral 8×7B** | GQA + Sparse MoE | GQA in the attention stack, MoE in feed-forward layers. |
| **DeepSeek – V2 / V3 / R1** | **MLA (latent attention)** | Multi-head Latent Attention compresses KV cache; DeepSeek Sparse Attention (V3.2) introduces structured sparsity. |
| **Anthropic – Claude 3 / 4.x** | Sparse / conditional attention | Public docs emphasize sparse transformers and conditional attention, not MoE. |
| **xAI – Grok-1 / 4.x** | Efficient attention + MoE | Uses RoPE and GQA-like KV sharing with MoE experts. |

**Insight:** By late 2025, **GQA-style efficient attention** (plus MLA and sparse variants) has effectively replaced vanilla MHA in new large models. This is the weight-only, hardware-aligned optimization that diffuses fastest and forms the "background assumption" for 2024–2025 architectures.
