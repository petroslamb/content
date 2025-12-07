# Techniques Available for Gate‑1 Hardware Friction Scoring

**Goal:** Canonical list of techniques/primitives we can score along the Gate‑1 hardware/infra axes (GA/MAL/PAR/STI/IM).  
**Scope:** 2017–2025 LLM‑relevant techniques that already appear in the research artifacts, essay, or scorecard.

Each entry includes:
- **Canonical paper or source** (for definition and baseline evidence)  
- **Short summary** (what the technique does / why it matters for Gate‑1)

This is a **living list**: add new techniques here before scoring them in the scorecard dataset.
When a technique has already been scored in the Gate‑1 dataset, it is marked with a short **Status** line.

---

## 1. RoPE (Rotary Position Embeddings, 2021)

- **Canonical paper:** *RoFormer: Enhanced Transformer with Rotary Position Embedding* (Su et al., 2021).  
- **Summary:** Replaces absolute/sinusoidal position encodings with a rotary scheme applied inside attention. Keeps computation in standard matmuls while improving extrapolation and long‑range behavior. Gate‑1 relevance: weight‑only architectural tweak with excellent GA/MAL/PAR and essentially zero STI/IM friction.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C1).

---

## 2. RMSNorm (Root Mean Square Layer Normalization, 2019)

- **Canonical paper:** *Root Mean Square Layer Normalization* (Zhang & Sennrich, 2019).  
- **Summary:** Variant of LayerNorm that normalizes by the root‑mean‑square of activations, simplifying the operation and improving training stability in large LLMs. Gate‑1 relevance: drop‑in normalization change; same kernel classes and topology, purely Green‑zone friction.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C2).

---

## 3. LoRA / QLoRA (Low‑Rank Adapters and Quantized LoRA, 2021–2023)

- **Canonical papers:**  
  - *LoRA: Low‑Rank Adaptation of Large Language Models* (Hu et al., 2021).  
  - *QLoRA: Efficient Finetuning of Quantized LLMs* (Dettmers et al., 2023).  
- **Summary:** LoRA adds low‑rank adapter matrices to existing weight matrices; QLoRA combines this with low‑bit quantization of base weights. Gate‑1 relevance: high GA/MAL/PAR (still matmuls), no topology change, modest IM friction; massively reduces fine‑tuning cost without touching core serving topology.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C3).

---

## 4. Quantization for LLMs (Int8/Int4 Kernels, 2022)

- **Representative papers:**  
  - *LLM.int8(): 8‑bit Matrix Multiplication for Transformers at Scale* (Dettmers et al., 2022).  
  - *GPTQ: Accurate Post‑Training Quantization for Generative Pre‑trained Transformers* (Frantar et al., 2022).  
- **Summary:** Reduce precision of weights/activations (e.g., 8‑bit, 4‑bit) with specialized kernels to cut memory and improve throughput. Gate‑1 relevance: remains GEMM‑aligned but sensitive to kernel availability and numerical quirks; typically Yellow on IM/STI, Green on GA/MAL/PAR.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C4).

---

## 5. FlashAttention (2022)

- **Canonical paper:** *FlashAttention: Fast and Memory‑Efficient Exact Attention with IO‑Awareness* (Dao et al., 2022).  
- **Summary:** Rewrites attention as a tiled, SRAM‑aware kernel that avoids materializing the full \(N \times N\) attention matrix, dramatically improving memory locality and throughput. Gate‑1 relevance: archetypal Yellow kernel‑level optimization—excellent GA/MAL/PAR, zero topology change, high but one‑time IM friction.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C5).

---

## 6. Vanilla Transformer + FlashAttention (Reference Architecture, 2017–2022)

- **Canonical paper:** *Attention Is All You Need* (Vaswani et al., 2017) + FlashAttention (Dao et al., 2022).  
- **Summary:** Decoder‑only Transformer with standard MHA, MLP blocks, and FlashAttention as the drop‑in attention kernel. Gate‑1 relevance: serves as the **Green reference point** in the scorecard (H = 6, E = 4) for dense LLM stacks on 2023–2025 GPUs.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (A1/B2).

---

## 7. GQA / MQA / MLA (Efficient Attention Variants, 2019–2024)

- **Representative papers/sources:**  
  - *Fast Transformer Decoding: One Write‑Head is All You Need* (Shazeer, 2019) — Multi‑Query Attention (MQA).  
  - Public docs/model cards for Llama 3/4, Gemma 2, Qwen2.5, DeepSeek‑V2/V3/R1 describing GQA/MLA.  
- **Summary:** Reduce KV heads (MQA/GQA) or compress KV cache into a latent space (MLA) while keeping Q heads high. Gate‑1 relevance: keep attention GEMM‑aligned, shrink KV bandwidth and memory; topology unchanged. These are core Green primitives with minor IM friction during rollout.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (A2–A3).

---

## 8. Mixture‑of‑Experts (MoE) Transformers, 2017–2021)

- **Representative papers:**  
  - *Outrageously Large Neural Networks: The Sparsely‑Gated Mixture‑of‑Experts Layer* (Shazeer et al., 2017).  
  - *Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity* (Fedus et al., 2021).  
- **Summary:** Replace some dense MLP blocks with many expert MLPs, routing each token to a subset of experts to increase parameter count without proportional FLOPs. Gate‑1 relevance: excellent GA but high system‑level friction—new routing, expert parallelism, and serving topology (Orange/Red for startups, Yellow for frontier labs with capital).
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (A5–A6).

---

## 9. Pure Mamba / SSM (State Space Models, 2021–2023)

- **Canonical paper:** *Mamba: Linear‑Time Sequence Modeling with Selective State Spaces* (Gu et al., 2023).  
- **Summary:** Uses selective state‑space models instead of attention to achieve linear‑time sequence modeling, with strong long‑sequence throughput and linear memory. Gate‑1 relevance: input/output layers are GEMM‑aligned, but the core SSM operation is a parallel scan with weaker GPU parallelism; mid‑range GA/MAL, good STI, mixed IM—Orange in the scorecard at large scales.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (A7).

---

## 10. Hybrid SSM + Attention Architectures (2024–2025)

- **Representative sources:**  
  - *Jamba: Hybrid State Space Model and Attention Architecture* (AI21 Labs, 2024).  
  - Falcon‑H1 technical docs (TII, 2024).  
  - Qwen3‑Next technical report (Alibaba/Qwen team, 2025).  
- **Summary:** Combine SSM blocks with attention (and often MoE) to leverage SSM efficiency for local/sequential structure and attention for global routing and in‑context learning. Gate‑1 relevance: generally good GA/MAL/STI with modest additional kernel complexity; used as evidence that hybrids, not pure SSMs, are the scalable path at large sizes.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (B14–B16).

---

## 11. Linear‑Attention Variants (Performer, Nyströmformer, GLA/DeltaNet, 2020–2024)

- **Representative papers:**  
  - *Rethinking Attention with Performers* (Choromanski et al., 2020).  
  - *Nyströmformer: A Nyström‑Based Algorithm for Approximating Self‑Attention* (Xiong et al., 2021).  
  - GLA/DeltaNet long‑context attention variants (2023–2025 papers).  
- **Summary:** Replace softmax attention with low‑rank or kernelized approximations to achieve linear or sub‑quadratic complexity. Gate‑1 relevance: typically GEMM‑friendly with improved memory behavior but non‑universal infra support; friction is mostly IM, with adoption limited by mixed empirical wins vs Flash‑optimized standard attention.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (A8, B5–B6).

---

## 12. Reversible Residual Networks (RevNets, 2017)

- **Canonical paper:** *The Reversible Residual Network: Backpropagation Without Storing Activations* (Gomez et al., 2017).  
- **Summary:** Design residual blocks so that activations can be recomputed from outputs, reducing activation memory at the cost of extra compute. Gate‑1 relevance: Green on GA/MAL/PAR and STI/IM, but historically low adoption in LLMs—an important low‑friction, low‑adoption counter‑example.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C6).

---

## 13. LSTM / GRU (Recurrent Networks, 1997–2014)

- **Canonical papers:**  
  - *Long Short‑Term Memory* (Hochreiter & Schmidhuber, 1997).  
  - *Learning Phrase Representations using RNN Encoder–Decoder for Statistical Machine Translation* (Cho et al., 2014) — GRU.  
- **Summary:** Recurrent architectures with gating mechanisms that dominated pre‑Transformer sequence modeling. Gate‑1 relevance: quite GEMM‑aligned and memory‑efficient, but with strictly sequential dependencies over time (PAR = 0), making large‑scale training on long sequences hardware‑hostile compared to Transformers.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (A4).

---

## 13a. Vanilla RNN (Elman Networks, 1990)

- **Canonical paper:** *Finding Structure in Time* (Elman, 1990).  
- **Summary:** The classic simple recurrent network with a single recurrent hidden state updated at each time step. Gate‑1 relevance: heavily GEMM‑aligned but strictly sequential over sequence length (PAR = 0), making it a pre‑Transformer baseline with strong hardware friction for long‑context training.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (A11).

---

## 13b. Seq2Seq RNN (Encoder–Decoder, 2014)

- **Canonical paper:** *Sequence to Sequence Learning with Neural Networks* (Sutskever et al., 2014).  
- **Summary:** An encoder–decoder architecture built from recurrent networks for sequence‑to‑sequence tasks (e.g., machine translation), relying on a fixed‑size bottleneck vector. Gate‑1 relevance: inherits the sequential training bottleneck (PAR = 0) of RNNs despite being a major architectural milestone.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (A12).

---

## 13c. Bahdanau Attention (RNN + Soft Attention, 2015)

- **Canonical paper:** *Neural Machine Translation by Jointly Learning to Align and Translate* (Bahdanau et al., 2015).  
- **Summary:** Augments RNN encoder–decoder models with soft attention over encoder states, improving translation quality by learning alignments jointly with decoding. Gate‑1 relevance: adds N×N attention matrices on top of sequential RNN computation; improves modeling but does not significantly change the PAR = 0 hardware bottleneck.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (A13).

---

## 14. KANs (Kolmogorov–Arnold Networks, 2024)

- **Canonical paper:** *Kolmogorov–Arnold Networks* (Liu et al., 2024).  
- **Summary:** Replace standard linear layers and fixed activations with spline‑based, learnable functions on edges, motivated by Kolmogorov–Arnold representation theorems. Gate‑1 relevance: per‑edge spline evaluation does not batch into a few large GEMMs, leading to many small, irregular ops—very poor GA/MAL and IM, a Red‑zone hardware‑friction example.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (A9).

---

## 15. Neural ODEs (2018)

- **Canonical paper:** *Neural Ordinary Differential Equations* (Chen et al., 2018).  
- **Summary:** Treat depth as continuous and use ODE solvers to define the network, integrating dynamics instead of stacking discrete layers. Gate‑1 relevance: iterative solvers require many small matmuls and function evaluations with poor parallelism and memory locality, making them strongly hardware‑unfriendly for LLM‑scale workloads.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (A10).

---

## 16. Vendor‑Specific Kernel Stacks / Proprietary Sparse Engines (≈2023–2025)

- **Representative sources:**  
  - NVIDIA TensorRT‑LLM, Triton kernels, and sparse/tensor‑core optimization docs.  
  - TPU / accelerator‑specific kernel and XLA documentation from Google and others.  
- **Summary:** Hardware‑ and vendor‑specific kernel stacks (e.g., custom sparse kernels, fused attention, MoE routing) that significantly improve utilization on specific architectures but are not universally available. Gate‑1 relevance: can drastically lower friction for certain techniques on a given stack while effectively raising friction for competitors; important when scoring techniques from the perspective of non‑vendor labs and startups.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C7).

---

## 17. External Memory and Retrieval (RAG / Memorizing Transformers / RAPTOR‑Style Systems, 2014–2022)

- **Representative papers:**  
  - *End‑To‑End Memory Networks* (Sukhbaatar et al., 2015).  
  - *Neural Turing Machines* (Graves et al., 2014).  
  - *Retrieval‑Augmented Generation for Knowledge‑Intensive NLP* (Lewis et al., 2020).  
  - *Memorizing Transformers* (Wu et al., 2022).  
- **Summary:** Architectures that bolt on large external memories or retrieval systems (vector stores, document indexes) to augment a base model, often via cross‑attention over retrieved context. Gate‑1 relevance: can keep core compute GEMM‑aligned but introduce non‑trivial STI (extra services, I/O, latency) and IM (serving infra) friction; critical for understanding why RAG is production‑ready while earlier memory‑network/NTM variants largely failed to scale.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C8, C15).

---

## 18. Capsule Networks (2017)

- **Canonical paper:** *Dynamic Routing Between Capsules* (Sabour, Frosst & Hinton, 2017).  
- **Summary:** Replace scalar neurons with vector “capsules” and routing‑by‑agreement mechanisms intended to capture part–whole relationships explicitly. Gate‑1 relevance: routing and many small matmuls/activations create poor GA/MAL characteristics and complex kernels; despite theoretical appeal, they have not scaled to LLM‑style workloads and function as a high‑friction failure case alongside KANs and Neural ODEs.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C9).

---

## 19. HyperNetworks (2016)

- **Canonical paper:** *HyperNetworks* (Ha, Dai & Le, 2016).  
- **Summary:** Use a secondary network to generate the weights of a primary network conditionally on some context. Gate‑1 relevance: typically retains GEMM‑aligned compute but increases parameter count and training/inference FLOPs; hardware friction arises from extra passes and memory use rather than new kernel classes. Important historically and as a conceptual ancestor of adapter‑style methods like LoRA.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C10).

---

## 20. Adaptive Computation Time (ACT) and Universal Transformers (2016–2018)

- **Canonical papers:**  
  - *Adaptive Computation Time for Recurrent Neural Networks* (Graves, 2016).  
  - *Universal Transformers* (Dehghani et al., 2018).  
- **Summary:** Allow different tokens or positions to use different amounts of computation (e.g., dynamic halting over layers or time). Gate‑1 relevance: introduces data‑dependent control flow that reduces effective parallelism and complicates efficient batching on GPUs (PAR and MAL penalties), helping explain why these ideas remain largely research‑only despite conceptual elegance.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C11).

---

## 21. Layer Scale / Weighted Residuals (2016–2021)

- **Representative papers:**  
  - *Deep Networks with Stochastic Depth* (Huang et al., 2016) — related residual scaling ideas.  
  - *CaiT: Going Deeper with Image Transformers* (Touvron et al., 2021) — LayerScale in vision transformers.  
- **Summary:** Modify residual connections with learned or fixed scaling factors to stabilize very deep networks. Gate‑1 relevance: essentially free on GA/MAL/PAR/STI (simple elementwise ops), with negligible kernel or topology impact; serves as a clear example of a Green‑zone technique whose adoption is governed almost entirely by training dynamics and stability, not hardware friction.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C12).

---

## 22. Cross‑Attention Patterns (Perceiver‑Style and Hierarchical Transformers, 2021)

- **Representative papers:**  
  - *Perceiver: General Perception with Iterative Attention* (Jaegle et al., 2021).  
  - *Perceiver IO: A General Architecture for Structured Inputs & Outputs* (Jaegle et al., 2021).  
- **Summary:** Use asymmetric cross‑attention (e.g., small latent arrays attending to large inputs) and hierarchical attention patterns to handle very high‑dimensional inputs. Gate‑1 relevance: stays within GEMM‑friendly attention but changes sequence/latents layout and memory patterns; friction shows up mainly as MAL/STI complexity when mapping to existing inference stacks.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C13).

---

## 23. Learnable Routing Frameworks (PathNet, Graph HyperNetworks, 2017–2018)

- **Representative papers:**  
  - *PathNet: Evolution Channels Gradient Descent in Super Neural Networks* (Fernando et al., 2017).  
  - *Graph HyperNetworks for Neural Architecture Search* (Zhang et al., 2018).  
- **Summary:** Mechanisms that learn which sub‑paths or modules to activate within a larger super‑network, often combining evolutionary search or hypernetworks with routing. Gate‑1 relevance: architecturally similar to MoE‑style conditional execution but typically with even higher control‑flow complexity and weaker infra support, making them high‑friction and largely historical/experimental for LLM‑scale systems.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C14).

---

## 24. Memory Networks and Neural Turing Machines (Historical External‑Memory Precursors, 2014–2015)

- **Canonical papers:**  
  - *Neural Turing Machines* (Graves et al., 2014).  
  - *End‑To‑End Memory Networks* (Sukhbaatar et al., 2015).  
- **Summary:** Early architectures that combined neural controllers with differentiable external memories. Gate‑1 relevance: heavy random memory access and iterative read/write operations made them difficult to scale efficiently on GPUs; they are key negative cases for the friction map, later superseded in practice by simpler, more infra‑friendly RAG and memorizing‑Transformer designs.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C15).

---

## 25. Forward‑Forward Algorithm (2022)

- **Canonical paper:** *The Forward‑Forward Algorithm: Some Preliminary Investigations* (Hinton, 2022).  
- **Summary:** Training rule that replaces backpropagation with two forward passes (positive and negative phases) and a local “goodness” objective per layer. Gate‑1 relevance: per‑step compute can remain GEMM‑aligned, but training requires extra passes and carefully staged data, increasing total training cost; as of 2025 it is a speculative, research‑only alternative rather than a production‑relevant primitive.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C16).

---

## 26. Sharpness‑Aware Minimization (SAM, 2020)

- **Canonical paper:** *Sharpness‑Aware Minimization for Efficiently Improving Generalization* (Foret et al., 2020).  
- **Summary:** Optimization method that perturbs weights in the direction of the loss gradient and optimizes for parameters that minimize the worst‑case loss in a small neighborhood, improving generalization. Gate‑1 relevance: doubles (or more) the effective number of forward/backward evaluations per update but doesn’t change kernels or topology; Green on GA/MAL/STI but with a clear training‑cost multiplier that matters when reasoning about total compute friction.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C17).

---

## 27. Test‑Time Training (2020)

- **Canonical paper:** *Test‑Time Training with Self‑Supervision for Generalization Under Distribution Shifts* (Sun et al., 2020), plus later LLM‑oriented variants.  
- **Summary:** Adapt model parameters or small adapters on‑the‑fly at inference using self‑supervised losses on the test input. Gate‑1 relevance: dramatically increases per‑request compute and latency (multiple gradient steps per query) while leaving kernels/topology unchanged; important as a high‑friction inference strategy even when GA/MAL/PAR are individually good.
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C18).

---

## 28. ByteNet (2016)

- **Canonical paper:** *Neural Machine Translation in Linear Time* (Kalchbrenner et al., 2016).  
- **Summary:** Uses stacks of dilated causal convolutions to model sequences with O(n log n) receptive fields, avoiding explicit recurrence. Gate‑1 relevance: parallel over tokens (good PAR) but relies on convolutional kernels rather than pure GEMMs and requires specialized implementations, leading to GA/MAL penalties and moderate infra maturity.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C19).

---

## 29. WaveNet (2016)

- **Canonical paper:** *WaveNet: A Generative Model for Raw Audio* (van den Oord et al., 2016).  
- **Summary:** An autoregressive audio model based on dilated causal convolutions, achieving high‑quality waveform generation. Gate‑1 relevance: similar hardware profile to ByteNet—good parallelism but conv‑heavy kernels and domain‑specific infra make it less attractive as a general LLM primitive.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C20).

---

## 30. QRNN (Quasi‑Recurrent Neural Network, 2016)

- **Canonical paper:** *Quasi‑Recurrent Neural Networks* (Bradbury et al., 2016).  
- **Summary:** Combines convolutional layers with a simple recurrent pooling step to gain some parallelism over standard RNNs while keeping temporal recurrence. Gate‑1 relevance: partially improves PAR and remains convolution‑/GEMM‑friendly but depends on non‑standard kernels and has limited modern infra support.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C21).

---

## 31. IndRNN (Independent Recurrent Neural Network, 2018)

- **Canonical paper:** *Independently Recurrent Neural Network (IndRNN)* (Li et al., 2018).  
- **Summary:** Designs recurrent units whose neurons have independent recurrent connections, improving gradient flow and enabling deeper recurrent stacks. Gate‑1 relevance: keeps GEMM‑friendly operations but remains sequential across time; partial parallelism gains and research‑grade infra yield an Orange‑zone friction profile.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C22).

---

## 32. Temporal Convolutional Networks (TCN, 2018)

- **Canonical paper:** *An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling* (Bai et al., 2018).  
- **Summary:** Uses temporal/dilated convolutions as a generic alternative to RNNs for sequence modeling, achieving good parallelism and stable training. Gate‑1 relevance: fully parallel over sequence but conv‑heavy and less GEMM‑centric than Transformers; infra support is decent but not as universal, placing TCNs near other pre‑Transformer conv architectures in Yellow friction.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (C23).

---

## 28. Vanilla Transformer (Non‑Flash, Quadratic Attention, 2017)

- **Canonical paper:** *Attention Is All You Need* (Vaswani et al., 2017).  
- **Summary:** Standard decoder‑only Transformer with multi‑head self‑attention and MLP blocks, using naive quadratic attention that materializes N×N attention matrices. Gate‑1 relevance: essentially perfect GEMM alignment and good parallelism, but only moderate memory locality (large intermediates), making it slightly worse on MAL than Flash‑optimized variants while remaining a Green baseline on 2023–2025 GPUs.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (B1).

---

## 29. Lightning Attention (Sub‑Quadratic Feature‑Map Attention, 2024)

- **Canonical paper:** *Lightning Attention: Fast and Accurate Exact Attention with Linear Complexity* (Yang et al., 2024, arXiv:2405.17381).  
- **Summary:** Replaces softmax attention with a feature‑map based construction that yields linear‑time attention while remaining implementable via large GEMMs and carefully tiled kernels. Gate‑1 relevance: maintains strong GA/MAL/PAR comparable to FlashAttention, but infra maturity is lower (not yet as universally upstream), so friction is mainly on IM rather than raw hardware throughput.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (B3).

---

## 30. Reformer (LSH‑Based Attention, 2020)

- **Canonical paper:** *Reformer: The Efficient Transformer* (Kitaev, Kaiser & Levskaya, 2020, arXiv:2001.04451).  
- **Summary:** Uses locality‑sensitive hashing (LSH) to approximate attention in sub‑quadratic time, introducing bucketed attention patterns and reversible layers. Gate‑1 relevance: still leverages GEMMs but adds irregular hashing, custom bucketing logic, and more complex memory patterns, which lowers GA/MAL slightly and introduces STI/IM friction relative to standard attention.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (B5).

---

## 31. RWKV (Recurrent‑Style Sequence Models, 2023)

- **Canonical paper:** *RWKV: Reinventing RNNs for the Transformer Era* (Peng et al., 2023, arXiv:2305.13048).  
- **Summary:** Channel‑mixing and time‑mixing blocks that mimic Transformer behavior in an RNN‑like architecture with recurrent state, aiming to combine RNN efficiency with attention‑like capabilities. Gate‑1 relevance: uses some large matmuls but relies on scan‑like updates over sequence, leading to middling GA/MAL/PAR and making it hardware‑less‑friendly than fully parallel attention at long context.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (B7).

---

## 32. xLSTM (Extended LSTM Variants, 2024)

- **Canonical paper:** *xLSTM: Extended Long Short‑Term Memory Networks* (Beck et al., 2024, arXiv:2405.04517).  
- **Summary:** Enhances classic LSTMs with architectural refinements (e.g., multiplicative coupling, improved gating) to improve modeling power and efficiency, while retaining the fundamental recurrent structure. Gate‑1 relevance: still exhibits true O(N) sequential dependencies across time steps (PAR=0); despite reasonable GEMM/memory behavior, this sequential bottleneck makes it a Red‑zone architecture for long‑sequence LLM‑style workloads.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (B8).

---

## 40. BERT‑Family Encoder‑Only Transformers (2018–2020)

- **Canonical papers:**  
  - *BERT: Pre‑training of Deep Bidirectional Transformers for Language Understanding* (Devlin et al., 2018).  
  - *RoBERTa: A Robustly Optimized BERT Pretraining Approach* (Liu et al., 2019).  
  - *ALBERT: A Lite BERT for Self‑Supervised Learning of Language Representations* (Lan et al., 2019).  
  - *XLNet: Generalized Autoregressive Pretraining for Language Understanding* (Yang et al., 2019).  
  - *ELECTRA: Pre‑training Text Encoders as Discriminators Rather Than Generators* (Clark et al., 2020).  
  - *DeBERTa: Decoding‑enhanced BERT with Disentangled Attention* (He et al., 2020).  
- **Summary:** Encoder‑only Transformer variants that refine pretraining objectives, data, or parameter sharing while keeping the core quadratic attention + MLP backbone intact. Gate‑1 relevance: all share the vanilla Transformer’s Gate‑1 profile (H≈5, E≈4) on 2018–2022 GPUs.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (B24–B29).

---

## 41. GPT / T5 / PaLM‑Style Decoder/Unified Transformers (2019–2022)

- **Canonical papers:**  
  - *Language Models are Unsupervised Multitask Learners* (GPT‑2; Radford et al., 2019).  
  - *Exploring the Limits of Transfer Learning with a Unified Text‑to‑Text Transformer* (T5; Raffel et al., 2019).  
  - *Language Models are Few‑Shot Learners* (GPT‑3; Brown et al., 2020).  
  - *PaLM: Scaling Language Modeling with Pathways* (Chowdhery et al., 2022).  
- **Summary:** Large‑scale decoder‑only and encoder‑decoder Transformers that primarily push scale, data, and training strategy while keeping the quadratic attention architecture unchanged. Gate‑1 relevance: same H/E profile as vanilla Transformer; innovations are in scale and optimization, not hardware‑friction properties.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (B30–B33).

---

## 42. Additional Efficient Attention Variants (Linformer, BigBird, FNet, AFT, 2020–2021)

- **Canonical papers:**  
  - *Linformer: Self‑Attention with Linear Complexity* (Wang et al., 2020).  
  - *BigBird: Transformers for Longer Sequences* (Zaheer et al., 2020).  
  - *FNet: Mixing Tokens with Fourier Transforms* (Lee‑Thorp et al., 2021).  
  - *Attention Free Transformer* (AFT; Zhai et al., 2021).  
- **Summary:** A family of efficient attention variants that reduce complexity via low‑rank projections, sparse patterns, Fourier mixing, or elementwise mixing with positional biases. Gate‑1 relevance: all maintain reasonable or good PAR but introduce non‑standard kernels and, in cases like FNet, non‑GEMM‑dominated workloads, and lack mature infra, which keeps their H/E below Flash‑optimized attention and limits adoption.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (B20–B23).

---

## 43. Switch Transformer (Large‑Scale MoE, 2021)

- **Canonical paper:** *Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity* (Fedus et al., 2021).  
- **Summary:** Introduces large‑scale token‑routed MoE layers into a Transformer backbone, activating a small subset of expert FFNs per token to scale parameters without proportional FLOPs. Gate‑1 relevance: experts are GEMM‑aligned (good GA), but routing and expert parallelism require new serving topology and have limited infra maturity relative to dense Transformers.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (B34).

---

## 33. HGRN2 (Gated Recurrent Networks with Parallel Scan, 2024)

- **Canonical paper:** *HGRN2: Hierarchical Gated Recurrent Networks* (HGRN2 authors, 2024).  
- **Summary:** A gated recurrent architecture that introduces hierarchical and partially parallelizable update rules to mitigate some limitations of classic RNNs, often leveraging parallel scan primitives for efficiency. Gate‑1 relevance: improves PAR relative to pure LSTMs but still relies on non‑standard kernels and bespoke implementations, leaving it with moderate GA/MAL and low IM (research‑grade infra).  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (B9).

---

## 34. S4 (Structured State Space Sequence Model, 2021)

- **Canonical paper:** *Efficiently Modeling Long Sequences with Structured State Spaces* (Gu et al., 2021, arXiv:2111.00396).  
- **Summary:** Introduces a structured state‑space model using carefully parameterized linear dynamical systems and FFT‑based convolutions to model long sequences efficiently. Gate‑1 relevance: achieves strong sequence‑parallelism (good PAR) with reasonably optimized FFT kernels, but departs from pure GEMM workloads and relies on specialized implementations, placing it in a Yellow zone of moderate GA/MAL and non‑universal infra.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (B11).

---

## 35. Hyena (Hierarchical Convolution/FFT Sequence Model, 2023)

- **Canonical paper:** *Hyena Hierarchy: Towards Larger Convolutional Language Models* (Poli et al., 2023, arXiv:2302.10866).  
- **Summary:** Uses hierarchical convolutional/FFT operators as an alternative to attention for long‑range dependencies, achieving sub‑quadratic complexity with strong throughput on long sequences. Gate‑1 relevance: parallel and fairly memory‑efficient but relies on non‑GEMM kernels and less mature infra than attention, leading to similar Yellow‑zone friction as S4.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (B12).

---

## 36. Griffin (RG‑LRU Hybrid Sequence Model, 2024)

- **Canonical paper:** *Griffin: Mixing Recurrent and Attention Mechanisms for Efficient Sequence Modeling* (De et al., 2024, arXiv:2402.19427).  
- **Summary:** Fusion hybrid that combines recurrent gated linear units (e.g., LRU‑like recurrences) with attention‑style components to balance efficiency and expressivity. Gate‑1 relevance: effective kernel mix is not GEMM‑dominant due to recurrent components, leading to middling GA/MAL/PAR and keeping it in an Orange zone despite relatively friendly serving topology.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (B13).

---

## 37. Hybrid SSM + Attention (Jamba / Samba / Hymba, 2024)

- **Representative papers:**  
  - *Jamba: Hybrid State‑Space Model and Attention Architecture* (Lenz et al., 2024, arXiv:2403.19887).  
  - *Samba: Hybrid Sliding‑Window Attention and Mamba* (Ren et al., 2024, arXiv:2406.07522).  
  - *Hymba: Fusion and Striped Hybrid Architectures* (Dong et al., 2024, arXiv:2411.13676).  
- **Summary:** Concrete hybrid instantiations that mix Mamba/SSM blocks with attention (and sometimes MoE) to get the benefits of both (local efficiency + global routing), often optimized for specific vendor stacks (e.g., NVIDIA). Gate‑1 relevance: attention components keep GA high; SSM components plus custom routing slightly degrade MAL/PAR and rely on non‑universal kernels, yielding Yellow‑zone friction driven mostly by IM and increased system complexity.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (B14–B16).

---

## 38. Titans‑Style External Memory Systems (Titans / B’MOJO, 2024–2025)

- **Representative papers:**  
  - *Titans: Scaling Transformer Memory with Multi‑Type External Banks* (Behrouz et al., 2024, arXiv:2501.00663).  
  - B’MOJO fading‑memory architectures (2024).  
- **Summary:** Architectures that attach large, structured external memories (with multiple banks or memory types) to a base model, requiring complex addressing, routing, and often separate memory services. Gate‑1 relevance: core compute may remain GEMM‑friendly, but serving topology and infra demands are extreme (new distributed memory services, routing logic, and no mature tooling), placing them firmly in Red for non‑vendor teams despite their conceptual appeal.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (B17–B18).

---

## 39. MiniMax‑01 Hybrid Stack (Lightning + Full Attention, 2025)

- **Canonical paper:** *MiniMax‑01: Production‑Scale Linear Attention and Hybrid Transformers* (MiniMax, 2025, arXiv:2501.08313).  
- **Summary:** A practical production stack that combines Lightning Attention for most layers with periodic full softmax attention blocks, aiming to balance linear‑time efficiency with robust long‑range behavior. Gate‑1 relevance: heavy use of GEMM‑friendly Lightning kernels gives strong GA/PAR, but mixed kernels and proprietary infra create some MAL and IM friction; overall a Yellow‑zone architecture for Gate‑1 viability.  
- **Status:** Scored in `scorecard_dataset/scored_architectures.md` (B4).
