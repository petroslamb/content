# Research References (Core Citations)

> Centralized list of key external references used across the datasets in this `research_artifacts/` folder. This file exists so the `data_collection_plan.md` can point to a single place for the concrete sources it assumes.

---

## 1. MoE Quantitative Meta-Analysis

- **Switch Transformers (original MoE benchmarks)**  
  - Fedus et al., 2021, *“Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity”*  
  - arXiv:2101.03961

- **GShard & GLaM (early large‑scale MoE from Google)**  
  - Lepikhin et al., 2020, *“GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding”*  
  - arXiv:2006.16668  
  - Du et al., 2021, *“GLaM: Efficient Scaling of Language Models with Mixture-of-Experts”*  
  - arXiv:2112.06905

- **Expert Choice Routing**  
  - Zhou et al., 2022, *“Mixture-of-Experts with Expert Choice Routing”* (NeurIPS 2022)  
  - arXiv:2202.09368

- **Soft MoE**  
  - Representative: Google research on dense-to-sparse MoE variants (2023 era). Exact variant depends on which paper you prefer to anchor; this slot is for “Soft MoE, 2023”.

- **ST‑MoE (Google Research, 2022)**  
  - Large‑scale sparse MoE (≈269B parameters) with stabilized routing (z‑loss), used as a modern reference point for efficient training and inference cost vs dense baselines.

- **“Outrageously Large Neural Networks” (Shazeer et al., 2017)**  
  - Early MoE paper demonstrating 137B‑parameter sparse models on 1B Word Benchmark and WMT translation tasks; provides historical context for MoE scaling.

- **FasterMoE / Context‑Length Studies**  
  - System papers/benchmarks (e.g., FasterMoE) analyzing MoE throughput vs sequence length and batch size, used for the context‑length degradation curves in `EXHAUSTIVE_FINAL_COMPILATION.md`.

- **MoE Deployment Inefficiencies / Honest Speedups**  
  - *“Towards MoE Deployment: Mitigating Inefficiencies in Mixture-of-Experts Inference”*  
  - arXiv:2303.06182

- **Aurora System (Optimizing MoE Inference Time)**  
  - 2024 system paper on MoE inference optimization (Aurora‑style architecture), used for 2.38–3.54× speedup numbers.

- **Mixtral 8×7B**  
  - Mistral AI, 2023–2024: official technical report + Hugging Face model card for `Mixtral-8x7B` and `Mixtral-8x7B-Instruct`.  
  - Confirms sparse MoE architecture (8 experts, 2 active; 46.7B total, 12.9B active).

- **DeepSeek‑V3**  
  - DeepSeek‑AI et al., 2024, *“DeepSeek-V3 Technical Report”*  
  - arXiv:2412.19437 and Hugging Face config/model cards for `deepseek-ai/DeepSeek-V3` and `DeepSeek-V3.2-Exp`.

- **V‑MoE (Vision Mixture‑of‑Experts)**  
  - Riquelme et al., 2021–2022, *“Scaling Vision with Sparse Mixture of Experts”* (Vision MoE / V‑MoE), demonstrating MoE benefits beyond NLP on ImageNet and related benchmarks.

- **GB200 NVL72 / Hardware for MoE**  
  - Vendor and technical documentation for NVIDIA GB200 NVL72 and similar systems optimized for large‑context MoE workloads; used as evidence of hardware co‑evolving with MoE requirements.

---

## 2. Flash Attention & Infrastructure Lag

- **FlashAttention (v1)**  
  - Tri Dao et al., 2022, *“FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness”*  
  - arXiv:2205.14135

- **FlashAttention‑2**  
  - Dao et al., 2023, *“FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning”*  
  - arXiv:2307.08691

- **PyTorch Integration**  
  - PyTorch 2.0/2.2 release notes and documentation for `scaled_dot_product_attention` and FlashAttention2 backend (Jan 2024).

- **Framework & Model Evidence**  
  - IBM Granite 13B model card (first openly confirmed major model using FlashAttention).  
  - Microsoft Phi‑3 docs (2024) noting FlashAttention usage.  
  - Google Gemma 2 model card (2024) referencing FlashAttention2.

- **FlashAttention‑3 & FlashInfer**  
  - FlashAttention‑3 Hopper (H100) kernels, 2024 technical reports and docs.  
  - FlashInfer (2025) serving library docs claiming ≈29–69% latency reductions in inference.

---

## 3. SSM / Mamba Evidence

- **S4 & Structured State Space Models**  
  - Gu et al., 2021, *“Efficiently Modeling Long Sequences with Structured State Spaces”* (S4).  
  - arXiv:2111.00396

- **Mamba (Original Paper)**  
  - Gu & Dao et al., Dec 2023, *“Mamba: Linear-Time Sequence Modeling with Selective State Spaces”*  
  - arXiv:2312.00752 (representative; check latest version).

- **Falcon Mamba 7B**  
  - TII Falcon Mamba 7B model card / technical brief, describing:  
    - 7B pure Mamba, 5.5T tokens, benchmarks vs Llama 3.1 8B, Mistral 7B, Gemma 7B.

- **Hybrid Architectures (SSM + Attention)**  
  - **Jamba (AI21, 2024)** – hybrid Mamba+Attention model (official AI21 blog + HF cards).  
  - **Falcon‑H1 (TII, 2024)** – hybrid attention+Mamba2 blocks.  
  - **Qwen3‑Next (2025)** – linear attention (Gated DeltaNet) + gated attention + MoE; official Qwen3‑Next technical report and model cards.

- **2025 SSM/Mamba Surveys**  
  - *“From S4 to Mamba: A Comprehensive Survey”* (arXiv:2503.18970, May 2025).  
  - *“A Survey of Mamba”* (arXiv:2408.01129, updated June 2025).  
  - These surveys consolidate the “hybrid > pure SSM” consensus and emphasize lack of pure large‑scale SSM frontiers.

---

## 4. Major Lab Architectures & Adoption

- **Meta – Llama Family**  
  - Llama 2 (7B/13B/70B) papers + model cards (2023).  
  - Llama 3 and 3.1 model cards (`Meta-Llama-3-8B`, `Meta-Llama-3.1-405B` etc.) confirming GQA, RoPE, RMSNorm, FlashAttention.  
  - Wikipedia *“Llama (language model)”* page (last updated Dec 2025) confirming Llama 4 (Scout/Maverick) as MoE.

- **OpenAI – GPT‑4/4o/5**  
  - GPT‑4 system card and blog posts (2023).  
  - GPT‑4o release posts (May 2024).  
  - GPT‑5 system card and launch posts (Aug 7, 2025).  
  - 3rd‑party technical analyses (e.g., SemiAnalysis) for inferred MoE internals.

- **Google DeepMind – Gemini**  
  - Gemini technical reports and the *“Gemini (language model)”* Wikipedia page, confirming MQA/GQA and multimodal transformer architecture.

- **Mistral – Mistral 7B & Mixtral 8×7B**  
  - Mistral 7B paper: *“Mistral 7B”* (arXiv:2310.06825).  
  - Mixtral technical report + HF model cards, confirming sparse MoE architecture (8 experts, 2 active token‑wise).

- **DeepSeek – V2 / V3 / R1**  
  - DeepSeek‑V2 technical report + GitHub config (`deepseek-ai/DeepSeek-V2`).  
  - DeepSeek‑V3 technical report (arXiv:2412.19437).  
  - DeepSeek‑R1 launch blog + model docs (Jan 2025).

- **Anthropic – Claude**  
  - Claude model cards and system cards (Claude 2, 3, 4.x).  
  - Wikipedia *“Claude (language model)”* page summarizing sparse / conditional transformer architecture.

- **xAI – Grok**  
  - xAI Grok‑1 release GitHub repo (`xai-org/grok-1`).  
  - x.ai news posts for Grok 4.x (e.g., “Grok 4.1” blog on x.ai).

- **Other 2024–2025 Open‑Weight Models Used for GQA Stats**  
  - Gemma 2 model cards (Google, 2B/9B/27B) confirming GQA and architecture details.  
  - Llama 3.2 / 3.3 model cards (Meta) confirming GQA, long‑context (e.g., 128K) and performance vs earlier Llama models.  
  - Qwen2.5 72B model card (Alibaba) documenting GQA configuration, context length, and training setup.  
  - Falcon 2 11B docs (TII) describing GQA usage and training corpus size.

---

## 5. Production Deployment & RAG

- **RAG as Standard Long‑Context Strategy**  
  - Product docs / blog posts from OpenAI (ChatGPT, GPTs), Anthropic (Claude), Google (Gemini) describing retrieval‑augmented workflows and tool/RAG usage.

- **Framework / Serving Libraries**  
  - DeepSpeed, Megatron‑LM, FasterTransformer, AITemplate, Unsloth, and related repos confirming FlashAttention and MoE support in production‑grade stacks.

- **Long‑Context Frontier Models (128K–256K)**  
  - Llama 3.2 model docs describing extended context windows around 128K.  
  - Grok 1.5 and related xAI documentation noting long‑context capabilities.  
  - Command R / Command R+ (Cohere) product docs highlighting 128K+ contexts.  
  - Qwen 3 and Qwen3‑Next technical reports and model cards documenting 128K standard and ~256K frontier context windows with sparse attention + memory strategies.

---

## 6. Modular / Compositional Learning

- **Modular Machine Learning Framework (MML)**  
  - 2025 “Modular Machine Learning” paradigm papers (modular representation, modular models, modular reasoning), used as validation for the “compositional language” thesis and summarized in the 2025 literature updates section of `EXHAUSTIVE_FINAL_COMPILATION.md`.

- **Compositional Architecture Predecessor**  
  - “Neural Architecture Design as a Compositional Language” (your previous post), which the current work extends; used mainly for framing rather than empirical evidence.

---

## 7. Additional 2025 Research Directions (Not Yet Production‑Standard)

These references inform the “speculative / future directions” parts of `EXHAUSTIVE_FINAL_COMPILATION.md` but are **not** treated as production‑proven techniques.

- **Neural Attention (Updated 2025)**  
  - 2025 paper replacing dot products in attention with small feed‑forward networks to capture richer nonlinear interactions; improves perplexity and vision benchmarks in research settings.

- **Nested Learning (Google Research, NeurIPS 2025)**  
  - Introduces a multi‑level learning paradigm with attention viewed as associative memory; addresses catastrophic forgetting and continual learning from a theoretical angle.

- **Hybrid Transformer with Quantum Self‑Attention (2025)**  
  - Quantum‑classical self‑attention applied to molecular generation (SMILES), demonstrating experimental quantum‑enhanced NLP architectures.

- **Transformer‑based Neural Architecture Search (2025)**  
  - NAS methods using transformers and perplexity‑based auxiliary metrics to search alternative attention computation strategies.

---

**Note:** This file is intentionally high‑level: it records “which paper/report/URL backs which claim” at the granularity the `data_collection_plan.md` assumes. For exact benchmark numbers and per‑model stats, see the individual datasets:

- `moe_speedup_data_wip.md`  
- `flash_attention_timeline.md`  
- `ssm_benchmark_findings.md`  
- `major_lab_architecture_audit.md`  
- `EXHAUSTIVE_FINAL_COMPILATION.md`
