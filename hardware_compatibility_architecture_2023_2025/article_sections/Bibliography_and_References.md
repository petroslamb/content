# Bibliography and References

This bibliography collects the main external sources cited in the article
*“What Actually Works: The Hardware Compatibility Filter in Neural Architecture (2023–2025)”*.

---

## 1. Mixture-of-Experts and Conditional Computation

- Fedus, W. et al. (2021). *Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity*. arXiv:2101.03961.
- Lepikhin, D. et al. (2020). *GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding*. arXiv:2006.16668.
- Du, N. et al. (2021). *GLaM: Efficient Scaling of Language Models with Mixture-of-Experts*. arXiv:2112.06905.
- Zhou, Y. et al. (2022). *Mixture-of-Experts with Expert Choice Routing*. NeurIPS 2022. arXiv:2202.09368.
- Shazeer, N. et al. (2017). *Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer*. arXiv:1701.06538.
- Representative “Soft MoE” work (circa 2023) from Google scaling MoE with dense-to-sparse transitions.
- ST-MoE (Google Research, 2022). Large-scale sparse MoE (~269B parameters) with stabilized routing (e.g., z-loss) used as a modern reference point for training and inference cost vs dense baselines.
- FasterMoE and related system papers analyzing MoE throughput vs sequence length and batch size.
- *Towards MoE Deployment: Mitigating Inefficiencies in Mixture-of-Experts Inference*. arXiv:2303.06182.
- Aurora-style MoE system work (2024) on optimizing MoE inference time, providing ≈2.4–3.5× speedup numbers over dense baselines.
- Mistral AI (2023–2024). *Mixtral 8×7B* technical report and Hugging Face model cards for `Mixtral-8x7B` and `Mixtral-8x7B-Instruct`.
- DeepSeek-AI (2024). *DeepSeek-V3 Technical Report*. arXiv:2412.19437 and associated Hugging Face model cards (e.g., `deepseek-ai/DeepSeek-V3`, `deepseek-ai/DeepSeek-V3.2-Exp`).
- Riquelme, C. et al. (2021–2022). *Scaling Vision with Sparse Mixture of Experts* (Vision MoE / V-MoE).
- NVIDIA GB200 NVL72 and related vendor documentation describing hardware optimized for large-context MoE workloads.

---

## 2. Flash Attention and Infrastructure Lag

- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv:2205.14135.
- Dao, T. et al. (2023). *FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning*. arXiv:2307.08691.
- PyTorch 2.0 / 2.2 release notes and documentation for `scaled_dot_product_attention` and the FlashAttention2 backend (Jan 2024).
- IBM Granite 13B model card (first openly confirmed major model using FlashAttention).
- Microsoft Phi-3 documentation (2024) referencing FlashAttention usage.
- Google Gemma 2 model card (2024) referencing FlashAttention2.
- FlashAttention-3 Hopper (H100) technical reports and documentation (2024).
- FlashInfer serving library documentation (2025) reporting ≈29–69% latency reductions in inference.

---

## 3. State Space Models and Hybrid Architectures

- Gu, A. et al. (2021). *Efficiently Modeling Long Sequences with Structured State Spaces* (S4). arXiv:2111.00396.
- Gu, A. and Dao, T. et al. (2023). *Mamba: Linear-Time Sequence Modeling with Selective State Spaces*. arXiv:2312.00752.
- Falcon Mamba 7B model card and technical brief describing a 7B pure Mamba model trained on 5.5T tokens and benchmarks vs Llama 3.1 8B, Mistral 7B, Gemma 7B.
- AI21 Labs (2024). *Jamba* hybrid Mamba+Attention model (official blog and Hugging Face cards).
- TII (2024). *Falcon-H1* hybrid model combining attention and Mamba2-style blocks.
- Qwen3-Next technical reports and model cards describing linear attention (e.g., Gated DeltaNet) plus gated attention and MoE for capacity.
- NVIDIA Nemotron technical reports describing hybrid architectures incorporating Mamba-style SSM blocks for efficiency.
- Falcon 2 (TII) documentation for hybrid architectures that incorporate SSM-style blocks.

---

## 4. Training and Optimization Techniques

- Foret, P. et al. (2020). *Sharpness-Aware Minimization for Efficiently Improving Generalization*. arXiv:2010.01412.
- Progressive depth / curriculum training work demonstrating faster convergence via increasing depth over training (representative 2020–2023 literature).
- Routing-aware optimization and load-balancing methods for MoE models (e.g., z-loss and auxiliary losses in ST-MoE-style work).

---

## 5. Frontier Model Documentation and Model Cards

- Meta AI. *Llama 2* (7B/13B/70B) model card and technical report (2023).
- Meta AI. *Llama 3* and *Llama 3.1* model cards (e.g., `Meta-Llama-3-8B`, `Meta-Llama-3-70B`, `Meta-Llama-3.1-405B`) confirming GQA, RoPE, RMSNorm, and FlashAttention usage.
- Meta AI. *Llama 4* (Scout / Maverick) launch materials (2025) describing the MoE pivot from dense Llama 3.
- OpenAI. *GPT-4* system card and associated blog posts (2023).
- OpenAI. *GPT-4 Turbo* launch materials (2023).
- OpenAI. *GPT-4o* release blog and system card (May 2024).
- OpenAI. *GPT-5* system card and launch posts (Aug 2025).
- SemiAnalysis and similar third-party technical analyses used for inferred architectural details of closed models.
- Google DeepMind. *Gemini* technical reports and the “Gemini (language model)” Wikipedia entry summarizing MQA/GQA and multimodal transformer architecture.
- Mistral AI. *Mistral 7B* paper (arXiv:2310.06825).
- Mistral AI. *Mixtral 8×7B* technical report and model cards confirming sparse MoE architecture (8 experts, 2 active per token).
- DeepSeek-AI. *DeepSeek-V2* technical report and GitHub configs.
- DeepSeek-AI. *DeepSeek-V3* technical report (arXiv:2412.19437).
- DeepSeek-AI. *DeepSeek-R1* launch blog and model documentation (Jan 2025).
- Anthropic. Claude model cards and system cards for Claude 2, Claude 3, and Claude 4.x.
- xAI. Grok-1 release repository (`xai-org/grok-1`) and x.ai blog posts for Grok 4.x (e.g., “Grok 4.1”).
- Gemma 2 model cards (Google, 2B/9B/27B) confirming GQA and key architectural details.
- Llama 3.2 / 3.3 model cards confirming GQA and long context windows (e.g., 128K).
- Qwen2.5 72B model card documenting GQA configuration, context length, and training setup.
- Falcon 2 11B documentation describing GQA usage and training corpus.
- Wikipedia entries: *“Llama (language model)”*, *“Claude (language model)”*, *“Gemini (language model)”* (as of late 2025) for consolidated public summaries of architecture families.

---

## 6. Production Deployment, RAG, and Serving Systems

- Product and developer documentation from OpenAI (ChatGPT, GPTs), Anthropic (Claude), and Google (Gemini) describing retrieval-augmented workflows and tool/RAG patterns.
- DeepSpeed, Megatron-LM, FasterTransformer, AITemplate, Unsloth, and related open-source frameworks documenting FlashAttention and MoE support in production-grade stacks.
- Command R / Command R+ (Cohere) product documentation highlighting long-context (128K+) capabilities and RAG-centric workflows.
- Llama 3.2 documentation describing extended context windows around 128K tokens.
- xAI Grok 1.5 and related documentation noting long-context capabilities.
- Qwen 3 and Qwen3-Next technical reports and model cards documenting 128K–256K context windows with sparse attention and memory strategies.

---

## 7. Modular and Compositional Learning

- 2025 “Modular Machine Learning” framework papers on modular representations, modular models, and modular reasoning, used to validate the “compositional language” thesis.
- Petros, P. (2024). *Neural Architecture Design as a Compositional Language* (previous post that the current work extends).

---

## 8. Additional 2025 Research Directions (Speculative / Emerging)

These references inform forward-looking observations and are not treated as production-standard techniques.

- 2025 “Neural Attention” paper replacing dot products in attention with small feed-forward networks to capture richer nonlinear interactions in research settings.
- *Nested Learning* (Google Research, NeurIPS 2025), introducing a multi-level learning paradigm with attention as associative memory for continual learning.
- Hybrid transformer with quantum self-attention applied to molecular generation (SMILES) demonstrating experimental quantum-enhanced NLP architectures (2025).
- Transformer-based neural architecture search (2025) using auxiliary perplexity-based metrics to explore alternative attention computation strategies.

