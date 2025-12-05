# Bibliography and References

This bibliography collects the main external sources cited in the article
*“What Actually Works: The Hardware Compatibility Filter in Neural Architecture (2023–2025)”*.

---

Primary sources (papers, technical reports, official model cards/docs) back quantitative and architectural claims. Secondary sources (e.g., Wikipedia, third-party analyses) are used only for high-level summaries and inferred details of closed models and are explicitly labeled as such.

## 1. Mixture-of-Experts and Conditional Computation

- Fedus, W. et al. (2021). *Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity*. arXiv:2101.03961. Original large-scale sparse MoE for language models, establishing Switch as a practical scaling path. Available at: https://arxiv.org/abs/2101.03961
- Lepikhin, D. et al. (2020). *GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding*. arXiv:2006.16668. Introduces GShard and conditional computation techniques for scaling models across many devices. Available at: https://arxiv.org/abs/2006.16668
- Du, N. et al. (2021). *GLaM: Efficient Scaling of Language Models with Mixture-of-Experts*. arXiv:2112.06905. Demonstrates Google’s GLaM MoE architecture and its efficiency–quality trade-offs. Available at: https://arxiv.org/abs/2112.06905
- Zhou, Y. et al. (2022). *Mixture-of-Experts with Expert Choice Routing*. NeurIPS 2022. arXiv:2202.09368. Proposes expert-choice routing to improve MoE load balancing and training stability. Available at: https://arxiv.org/abs/2202.09368
- Shazeer, N. et al. (2017). *Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer*. arXiv:1701.06538. Early MoE paper showing sparsely-gated experts can scale to very large parameter counts. Available at: https://arxiv.org/abs/1701.06538
- Puigcerver, J. et al. (2023). *Soft Mixture of Experts*. arXiv:2308.00951. Representative “Soft MoE” work from Google scaling MoE with weighted expert combinations. Available at: https://arxiv.org/abs/2308.00951
- ST-MoE (Google Research, 2022). Large-scale sparse MoE (~269B parameters) with stabilized routing (e.g., z-loss) used as a modern reference point for training and inference cost vs dense baselines.
- *Mixture of Experts in the Era of Large Language Models* (2024). Survey of MoE architectures and deployment patterns in LLMs, covering Mixtral-8×7B, Grok-1, DBRX, Arctic, DeepSeek-V2/V3 and related systems. (Representative arXiv survey; see e.g. https://arxiv.org/ for the latest version.)
- FasterMoE context-length study (2023–2024). System benchmarking paper analyzing MoE throughput vs sequence length and batch size; used to derive context-length degradation curves in the MoE dataset.
- *Towards MoE Deployment: Mitigating Inefficiencies in Mixture-of-Experts Inference*. arXiv:2303.06182. Analyzes practical deployment inefficiencies of MoE and proposes mitigation strategies. Available at: https://arxiv.org/abs/2303.06182
- *Optimizing MoE Inference Time* (Aurora system, 2024). arXiv preprint focused on MoE inference optimization, providing ≈2.4–3.5× speedup numbers over dense baselines. (Representative link: search for title on https://arxiv.org/.)
- Mistral AI (2023–2024). *Mixtral 8×7B* technical report and Hugging Face model cards for `Mixtral-8x7B` and `Mixtral-8x7B-Instruct`. Documents the Mixtral sparse MoE architecture and its benchmark results. See e.g.: https://huggingface.co/mistralai/Mixtral-8x7B and https://huggingface.co/mistralai/Mixtral-8x7B-Instruct
- DeepSeek-AI (2024). *DeepSeek-V3 Technical Report*. arXiv:2412.19437 and associated Hugging Face model cards (e.g., `deepseek-ai/DeepSeek-V3`, `deepseek-ai/DeepSeek-V3.2-Exp`). Describes DeepSeek’s MoE + MLA architecture and long-context performance. Available at: https://arxiv.org/abs/2412.19437 and https://huggingface.co/deepseek-ai/DeepSeek-V3
- Riquelme, C. et al. (2021–2022). *Scaling Vision with Sparse Mixture of Experts* (Vision MoE / V-MoE). Extends MoE ideas to vision models, demonstrating benefits beyond NLP.
- NVIDIA GB200 NVL72 and related vendor documentation describing hardware optimized for large-context MoE workloads. Vendor materials illustrating hardware co-designed for large MoE and long-context serving.

---

## 2. Flash Attention and Infrastructure Lag

- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv:2205.14135. Introduces the original IO-aware tiling algorithm that makes exact attention memory-efficient and fast on GPUs. Available at: https://arxiv.org/abs/2205.14135
- Dao, T. et al. (2023). *FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning*. arXiv:2307.08691. Improves FlashAttention with better parallelism and work partitioning, increasing utilization. Available at: https://arxiv.org/abs/2307.08691
- PyTorch 2.0 / 2.2 release notes and documentation for `scaled_dot_product_attention` and the FlashAttention2 backend (Jan 2024). Framework integration evidence for FlashAttention-style kernels becoming standard. See e.g.: https://pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html
- IBM Granite 13B model card (first openly confirmed major model using FlashAttention). Early production confirmation of FlashAttention usage in a large open-weight model. Representative link: https://huggingface.co/ibm-granite
- Microsoft Phi-3 documentation (2024) referencing FlashAttention usage. Confirms FlashAttention in Microsoft’s Phi-3 models. Representative link: https://learn.microsoft.com/azure/ai-services/openai/
- Google Gemma 2 model card (2024) referencing FlashAttention2. Confirms FlashAttention2 adoption in Google’s Gemma 2 family. Representative link: https://ai.google.dev/gemma
- FlashAttention-3 Hopper (H100) technical reports and documentation (2024). Describes Hopper-optimized FA3 kernels and their performance characteristics. Available at: https://tridao.me/publications
- FlashInfer serving library documentation (2025) reporting ≈29–69% latency reductions in inference. Serving-level library built on FlashAttention kernels, showing end-to-end latency gains.
- *Efficient Large Language Models* (TMLR 2024). Survey of efficient attention mechanisms and LLM optimizations, covering hardware-efficient attention (FlashAttention family), compact attention (KV compression), sparse and linear attention methods.

---

## 3. State Space Models and Hybrid Architectures

- Gu, A. et al. (2021). *Efficiently Modeling Long Sequences with Structured State Spaces* (S4). arXiv:2111.00396. Introduces structured state-space models as efficient sequence models for long contexts. Available at: https://arxiv.org/abs/2111.00396
- Gu, A. and Dao, T. et al. (2023). *Mamba: Linear-Time Sequence Modeling with Selective State Spaces*. arXiv:2312.00752. Presents Mamba, a selective SSM with linear-time sequence modeling capabilities. Available at: https://arxiv.org/abs/2312.00752
- *From S4 to Mamba: A Comprehensive Survey* (2025). arXiv:2503.18970. Survey of structured state-space models, tracing the evolution from S4 to Mamba and summarizing empirical findings on scalability and limitations. Available at: https://arxiv.org/abs/2503.18970
- *A Survey of Mamba* (2025). arXiv:2408.01129 (June 2025 update). Consolidates empirical results and design variants of Mamba-style models, emphasizing their strengths up to ≈7B parameters and challenges at larger scales. Available at: https://arxiv.org/abs/2408.01129
- Falcon Mamba 7B model card and technical brief describing a 7B pure Mamba model trained on 5.5T tokens and benchmarks vs Llama 3.1 8B, Mistral 7B, Gemma 7B. Documents the strongest pure Mamba model and its comparative performance. Representative link: https://huggingface.co/tiiuae/falcon-mamba-7b
- AI21 Labs (2024). *Jamba* hybrid Mamba+Attention model (official blog and Hugging Face cards). Describes a production hybrid architecture that alternates Mamba and attention layers. Representative links: https://www.ai21.com/blog/jamba and https://huggingface.co/ai21labs/Jamba-v0.1
- TII (2024). *Falcon-H1* hybrid model combining attention and Mamba2-style blocks. Presents a parallel hybrid SSM+attention design over a range of scales. Representative link: https://huggingface.co/tiiuae
- Qwen3-Next technical reports and model cards describing linear attention (e.g., Gated DeltaNet) plus gated attention and MoE for capacity. Detail a frontier hybrid architecture combining linear attention, gated attention, and MoE for long context and capacity. Representative link: https://github.com/QwenLM/Qwen3
- NVIDIA Nemotron technical reports describing hybrid architectures incorporating Mamba-style SSM blocks for efficiency. Provide examples of efficiency-focused hybrids using SSM-like blocks. Representative link: https://www.nvidia.com/en-us/ai-data-center/nemotron/
- Falcon 2 (TII) documentation for hybrid architectures that incorporate SSM-style blocks. Confirms SSM-style components inside modern Falcon architectures. Representative link: https://huggingface.co/tiiuae/falcon-2-11b

---

## 4. Training and Optimization Techniques

- Foret, P. et al. (2020). *Sharpness-Aware Minimization for Efficiently Improving Generalization*. arXiv:2010.01412. Introduces SAM, an optimizer modification favoring flat minima for better generalization. Available at: https://arxiv.org/abs/2010.01412
- Progressive depth / curriculum training work demonstrating faster convergence via increasing depth over training (representative 2020–2023 literature). Represents modern progressive training schemes that improve convergence speed. (Representative body of work; search by “progressive depth curriculum training” on https://arxiv.org/.)
- Routing-aware optimization and load-balancing methods for MoE models (e.g., z-loss and auxiliary losses in ST-MoE-style work). Captures router-focused training techniques that stabilize and balance MoE experts. (Representative of the ST-MoE line of work; search by title on https://arxiv.org/.)
- Liu, K. et al. (2025). *Reinforcement Learning Meets Large Language Models: A Survey of Advancements and Applications Across the LLM Lifecycle*. arXiv:2509.16679. Survey of RL methods applied across pre-training, alignment fine-tuning, and reinforced reasoning for LLMs, with a focus on RLVR, datasets, benchmarks, and tooling. Available at: https://arxiv.org/abs/2509.16679
- Sun, H. and van der Schaar, M. (2025). *Inverse Reinforcement Learning Meets Large Language Model Post-Training: Basics, Advances, and Opportunities*. arXiv:2507.13158. Survey framing LLM alignment through inverse RL, emphasizing reward modeling from human data, evaluation metrics, and open challenges. Available at: https://arxiv.org/abs/2507.13158

---

## 5. Frontier Model Documentation and Model Cards

- Meta AI. *Llama 2* (7B/13B/70B) model card and technical report (2023). Documents the dense Llama 2 family and its core architectural choices. Representative link: https://ai.meta.com/llama/
- Meta AI. *Llama 3* and *Llama 3.1* model cards (e.g., `Meta-Llama-3-8B`, `Meta-Llama-3-70B`, `Meta-Llama-3.1-405B`) confirming GQA, RoPE, RMSNorm, and FlashAttention usage. Provide official confirmation of efficient attention and normalization patterns in Llama 3. Representative link: https://ai.meta.com/llama/
- Meta AI. *Llama 4* (Scout / Maverick) launch materials (2025) describing the MoE pivot from dense Llama 3. Establish Meta’s first public MoE architecture and its expert configuration. Representative link: https://ai.meta.com/blog/
- OpenAI. *GPT-4* system card and associated blog posts (2023). High-level description of GPT-4’s capabilities, training data, and safety considerations. Representative link: https://openai.com/index/gpt-4-system-card
- OpenAI. *GPT-4 Turbo* launch materials (2023). Documentation describing cost, latency, and context improvements for GPT-4 Turbo. Representative link: https://platform.openai.com/docs/models/gpt-4-turbo
- OpenAI. *GPT-4o* release blog and system card (May 2024). Introduces GPT-4o as a natively multimodal model with improved latency and cost. Representative link: https://openai.com/index/gpt-4o/
- OpenAI. *GPT-5* system card and launch posts (Aug 2025). Official materials describing GPT-5’s capabilities and deployment properties. Representative link: https://openai.com/
- SemiAnalysis and similar third-party technical analyses (secondary / inference sources) used for inferred architectural details of closed models. Independent analyses used to hypothesize MoE/architecture internals for closed models. Representative link: https://www.semianalysis.com/
- Google DeepMind. *Gemini* technical reports and the “Gemini (language model)” Wikipedia entry (secondary summary) describing MQA/GQA and multimodal transformer architecture. Official and secondary sources summarizing Gemini’s architecture and attention variants. Representative links: https://deepmind.google/technologies/gemini/ and https://en.wikipedia.org/wiki/Gemini_(language_model)
- Mistral AI. *Mistral 7B* paper (arXiv:2310.06825). Technical report on the Mistral 7B dense transformer and its performance. Available at: https://arxiv.org/abs/2310.06825
- Mistral AI. *Mixtral 8×7B* technical report and model cards confirming sparse MoE architecture (8 experts, 2 active per token). Describes the Mixtral MoE architecture and benchmark results. Representative links: https://mistral.ai/news/mixtral-of-experts/ and https://huggingface.co/mistralai/Mixtral-8x7B
- DeepSeek-AI. *DeepSeek-V2* technical report and GitHub configs. Documents DeepSeek V2’s architecture and training setup. Representative link: https://github.com/deepseek-ai
- DeepSeek-AI. *DeepSeek-V3* technical report (arXiv:2412.19437). Presents DeepSeek V3’s MoE + MLA architecture and performance. Available at: https://arxiv.org/abs/2412.19437
- DeepSeek-AI. *DeepSeek-R1* launch blog and model documentation (Jan 2025). Provides details on DeepSeek R1’s reasoning training and performance metrics. Representative link: https://www.deepseek.com/
- Anthropic. Claude model cards and system cards for Claude 2, Claude 3, and Claude 4.x. Summarize Claude family capabilities, context windows, and safety considerations. Representative link: https://www.anthropic.com/claude
- xAI. Grok-1 release repository (`xai-org/grok-1`) and x.ai blog posts for Grok 4.x (e.g., “Grok 4.1”). Provide open weights and architectural notes for Grok models. Available at: https://github.com/xai-org/grok-1 and https://x.ai/blog
- Gemma 2 model cards (Google, 2B/9B/27B) confirming GQA and key architectural details. Document Gemma 2’s architecture, GQA usage, and training setup. Representative link: https://ai.google.dev/gemma
- Llama 3.2 / 3.3 model cards confirming GQA and long context windows (e.g., 128K). Confirm GQA and extended context support in later Llama 3 releases. Representative link: https://ai.meta.com/llama/
- Qwen2.5 72B model card documenting GQA configuration, context length, and training setup. Official Qwen 2.5 documentation for attention configuration and context length. Representative link: https://huggingface.co/Qwen/Qwen2.5-72B
- Falcon 2 11B documentation describing GQA usage and training corpus. Describes Falcon 2’s architecture and training data, including GQA. Representative link: https://huggingface.co/tiiuae/falcon-2-11b
- Wikipedia entries: *“Llama (language model)”*, *“Claude (language model)”*, *“Gemini (language model)”* (secondary summaries, as of late 2025) for consolidated public overviews of architecture families. Secondary sources summarizing architecture families for quick reference. Available at: https://en.wikipedia.org/wiki/LLaMA, https://en.wikipedia.org/wiki/Claude_(language_model), and https://en.wikipedia.org/wiki/Gemini_(language_model)

---

## 6. Production Deployment, RAG, and Serving Systems

- Product and developer documentation from OpenAI (ChatGPT, GPTs), Anthropic (Claude), and Google (Gemini) describing retrieval-augmented workflows and tool/RAG patterns. Provide concrete examples of how major providers productize RAG and tool integration. Representative portals: https://platform.openai.com/docs, https://docs.anthropic.com, https://ai.google.dev
- DeepSpeed, Megatron-LM, FasterTransformer, AITemplate, Unsloth, and related open-source frameworks documenting FlashAttention and MoE support in production-grade stacks. Framework and serving documentation showing kernel and MoE support in real systems. See e.g.: https://github.com/microsoft/DeepSpeed, https://github.com/NVIDIA/Megatron-LM, https://github.com/NVIDIA/FasterTransformer, https://github.com/facebookincubator/AITemplate, https://github.com/unslothai/unsloth
- Command R / Command R+ (Cohere) product documentation highlighting long-context (128K+) capabilities and RAG-centric workflows. Vendor docs demonstrating long-context and retrieval-centric deployments. Representative link: https://docs.cohere.com/
- Llama 3.2 documentation describing extended context windows around 128K tokens. Confirms extended context support and associated techniques in Llama 3.2. Representative link: https://ai.meta.com/llama/
- xAI Grok 1.5 and related documentation noting long-context capabilities. Documentation describing Grok 1.5’s long-context features and usage. Representative link: https://x.ai/
- Qwen 3 and Qwen3-Next technical reports and model cards documenting 128K–256K context windows with sparse attention and memory strategies. Official sources describing Qwen’s long-context and sparse-attention strategies. Representative link: https://github.com/QwenLM
- *Beyond the Limits: Context Length Extension* (May 2024). Survey of long-context techniques, including memory-retrieval augmentation, modified positional encodings, SSM approaches, and sparse attention patterns. (Representative arXiv survey; search by title on https://arxiv.org/.)

---

## 7. Modular and Compositional Learning

- 2025 “Modular Machine Learning” framework papers on modular representations, modular models, and modular reasoning, used to validate the “compositional language” thesis. Introduce a formal framework for modular models and reasoning that aligns with the compositional architecture view. (Representative arXiv / conference work; search by title on https://arxiv.org/ or major conference proceedings.)
- Petros, P. (2024). *Neural Architecture Design as a Compositional Language* (previous post that the current work extends). Earlier article establishing the compositional architecture framing this work builds on. Available at: /Users/petros/Projects/content/Neural Architecture Design as a Compositional Language.md
- *Modularity in Deep Learning: A Survey* (2023). Survey of modularity across data, task, and model axes, and its impact on compositional generalization and training. (Representative survey; search by title on https://arxiv.org/.)

---

## 8. Additional 2025 Research Directions (Speculative / Emerging)

These references inform forward-looking observations and are not treated as production-standard techniques.

- 2025 “Neural Attention” paper replacing dot products in attention with small feed-forward networks to capture richer nonlinear interactions in research settings. (Speculative / emerging; search by title on https://arxiv.org/.)
- *Nested Learning* (Google Research, NeurIPS 2025), introducing a multi-level learning paradigm with attention as associative memory for continual learning. (Speculative / emerging; search by title on https://arxiv.org/.)
- Hybrid transformer with quantum self-attention applied to molecular generation (SMILES) demonstrating experimental quantum-enhanced NLP architectures (2025). (Speculative; search by title on https://arxiv.org/.)
- Transformer-based neural architecture search (2025) using auxiliary perplexity-based metrics to explore alternative attention computation strategies. (Speculative; search by title on https://arxiv.org/.)
