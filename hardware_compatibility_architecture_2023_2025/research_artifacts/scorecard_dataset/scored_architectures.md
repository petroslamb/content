# Scored Architectures — Gate‑1 Hardware Friction Scorecard

> **Param weights tracking:** For ingestion and deduping, treat the CSV (`scored_architectures.csv`) as canonical. Per‑row weight analysis is marked via the `Param_Billions` and `Analyzed` columns; this markdown file is descriptive only.

**Goal:** Concrete, per‑architecture scores on the Gate‑1 rubric (GA/MAL/PAR/STI/IM → H/E/Zone) that we can use for calibration and simple models.  
**Scope:** Architectures and techniques that (a) appear in our research artifacts / scorecard, and (b) in the Fichtl et al. 2025 “End of Transformers?” survey or the `techniques_for_scoring.md` list.

All scores follow the definitions in the main scorecard:
- `H = GA + MAL + PAR` (0–6) — hardware throughput friendliness  
- `E = STI + IM` (0–4) — ecosystem / infra friction  
- Zone is interpreted from H/E (Green / Yellow / Orange / Red)

These are **opinionated but explicit**; they can be revised as we get better evidence.

---

## 1. Core Reference Architectures (From Our Scorecard)

| ID | Architecture | Year | Era | GA | MAL | PAR | **H** | STI | IM | **E** | Zone | Source / Paper | Notes | Analyzed | Section |
|----|-------------|------|-----|----|-----|-----|------:|-----|----|------:|------|----------------|-------|----------|---------|
| A1 | Transformer + FlashAttention (reference) | 2022 | 2018–2022 | 2 | 2 | 2 | **6** | 2 | 2 | **4** | 🟢 Green | Vaswani et al. 2017; Dao et al. 2022 | Baseline dense decoder‑only Transformer with FlashAttention; all heavy ops are GEMMs, tiled attention, fully upstream kernels. | analyzed | 1. Core Reference Architectures (From Our Scorecard) |
| A2 | GQA (Grouped‑Query Attention) | 2019 | 2018–2022 | 2 | 2 | 2 | **6** | 2 | 2 | **4** | 🟢 Green | Shazeer 2019; Llama/Gemma/Qwen model cards | Same kernels/topology as standard attention; fewer KV heads. Drop‑in change with universal adoption. | analyzed | 1. Core Reference Architectures (From Our Scorecard) |
| A3 | MLA (Multi‑Head Latent Attention, DeepSeek) | 2024 | 2023+ | 2 | 2 | 2 | **6** | 2 | 1 | **3** | 🟢 Low‑friction (DeepSeek‑biased) | DeepSeek‑V2/V3/R1 reports | Matmul‑heavy latent attention with compressed KV; excellent H, but IM=1 since infra is DeepSeek‑specific, not universal. | analyzed | 1. Core Reference Architectures (From Our Scorecard) |
| A4 | LSTM / GRU (LLM‑scale) | 1997 | pre‑2018 | 2 | 2 | 0 | **4** | 2 | 2 | **4** | 🔴 Hardware‑friction | Hochreiter & Schmidhuber 1997; Cho et al. 2014 | GEMM‑aligned and memory‑efficient, but strictly sequential over time (PAR=0). Gate‑1 hardware friction dominates at long sequences. | analyzed | 1. Core Reference Architectures (From Our Scorecard) |
| A5 | Mixtral‑8×7B (MoE) | 2023 | 2023+ | 2 | 1 | 2 | **5** | 1 | 2 | **3** | 🟡 Software friction | Mistral MoE report | Experts are standard FFNs (GA=2); routing/topology change (STI=1). Good kernels exist but infra still more complex than dense. | analyzed | 1. Core Reference Architectures (From Our Scorecard) |
| A6 | DeepSeek‑V3 (MoE + MLA/DSA) | 2024 | 2023+ | 2 | 1 | 2 | **5** | 1 | 1 | **2** | 🟡 Heavy software friction | DeepSeek‑V3/V3.2 papers | High‑end MoE with custom sparse attention; strong GA but topology changes (STI=1) and infra is DeepSeek‑specific (IM=1). | analyzed | 1. Core Reference Architectures (From Our Scorecard) |
| A7 | Pure Mamba / SSM (Falcon Mamba 7B) | 2023 | 2023+ | 1 | 1 | 1 | **3** | 2 | 1 | **3** | 🟠 Hardware‑biased friction | Gu et al. 2023; Falcon Mamba | Input/output matmuls, but core SSM op is a parallel scan with weaker tensor‑core utilization; infra partial but improving. | analyzed | 1. Core Reference Architectures (From Our Scorecard) |
| A8 | GLA / DeltaNet (linear‑attention hybrids) | 2023 | 2023+ | 2 | 1 | 1 | **4** | 2 | 1 | **3** | 🟠 Medium friction | Linear‑attention papers (GLA/DeltaNet) | Linear attention kernels can be GEMM‑friendly, but memory patterns/recall and infra are less mature than Flash. | analyzed | 1. Core Reference Architectures (From Our Scorecard) |
| A9 | KANs (Kolmogorov–Arnold Networks) | 2024 | 2023+ | 0 | 1 | 1 | **2** | 0 | 0 | **0** | 🔴 Research‑only | Liu et al. 2024 | Per‑edge spline evaluation yields many tiny, irregular ops (GA≈0, MAL≈1), no robust LLM‑scale infra; classic Red Gate‑1 failure. | analyzed | 1. Core Reference Architectures (From Our Scorecard) |
| A10 | Neural ODEs (sequence models) | 2018 | 2018–2022 | 0 | 0 | 1 | **1** | 1 | 0 | **1** | 🔴 Research‑only | Chen et al. 2018 | Iterative solvers with many small steps and poor locality; infra is research‑grade only. | analyzed | 1. Core Reference Architectures (From Our Scorecard) |



### 1.1 Pre‑Transformer Reference Architectures

| ID | Architecture | Year | Era | GA | MAL | PAR | **H** | STI | IM | **E** | Zone | Source / Paper | Notes | Analyzed | Section |
|----|-------------|------|-----|----|-----|-----|------:|-----|----|------:|------|----------------|-------|----------|---------|
| A11 | Vanilla RNN | 1990 | pre‑2018 | 2 | 2 | 0 | **4** | 2 | 2 | **4** | 🔴 Hardware‑friction | Elman 1990 | Classic recurrent network with purely sequential time‑step dependencies; GEMM‑aligned but PAR=0 makes training on long sequences hardware‑hostile. |  | 1.1 Pre‑Transformer Reference Architectures |
| A12 | Seq2Seq RNN (Encoder‑Decoder) | 2014 | pre‑2018 | 2 | 2 | 0 | **4** | 2 | 2 | **4** | 🔴 Hardware‑friction | Sutskever et al. 2014 | RNN encoder–decoder for sequence‑to‑sequence tasks; inherits the sequential bottleneck of RNNs despite architectural sophistication. |  | 1.1 Pre‑Transformer Reference Architectures |
| A13 | Bahdanau Attention (RNN + Soft Attention) | 2015 | pre‑2018 | 2 | 1 | 0 | **3** | 2 | 2 | **4** | 🟠 Orange | Bahdanau et al. 2015 | Adds soft attention over encoder states to Seq2Seq; improves modeling but does not remove RNN’s PAR=0 training bottleneck and materializes N×N attention. |  | 1.1 Pre‑Transformer Reference Architectures |


---

## 2. Architectures from Fichtl et al. 2025 Survey (Revised)

These scores start from the “brutally revised” table and incorporate our corrections (notably for Lightning Attention).

### 2.1 Production Attention Architectures

| ID | Architecture | Year | Era | GA | MAL | PAR | **H** | STI | IM | **E** | Zone | Source / Paper | Notes | Analyzed | Section |
|----|-------------|------|-----|----|-----|-----|------:|-----|----|------:|------|----------------|-------|----------|---------|
| B1 | Vanilla Transformer (non‑Flash) | 2017 | pre‑2018 | 2 | 1 | 2 | **5** | 2 | 2 | **4** | 🟢 Green | Vaswani et al. 2017 | Quadratic attention that materializes N×N; highly GEMM‑aligned but weaker MAL than Flash‑optimized variants. | analyzed | 2.1 Production Attention Architectures |
| B2 | Transformer + FlashAttention‑2 | 2023 | 2023+ | 2 | 2 | 2 | **6** | 2 | 2 | **4** | 🟢 Green | Dao et al. 2023 | Same as A1 with FA‑2 kernels; tiled SRAM‑resident attention, fully upstream support. | analyzed | 2.1 Production Attention Architectures |
| B3 | Lightning Attention | 2024 | 2023+ | 2 | 2 | 2 | **6** | 2 | 1 | **3** | 🟡 Yellow (infra‑limited) | Yang et al. 2024 (Lightning) | Sub‑quadratic, feature‑map‑based attention that can still be implemented as large GEMMs with good tiling; H restored to 6. Infra is not yet universally upstream (IM=1), so E=3. | analyzed | 2.1 Production Attention Architectures |
| B4 | MiniMax‑01 (Lightning + full attention) | 2025 | 2023+ | 2 | 1 | 2 | **5** | 2 | 1 | **3** | 🟡 Yellow | MiniMax‑01 2025 report | Hybrid stack using Lightning + full attention periodically. Good GA/PAR; MAL penalized due to mixed kernels and complexity; infra partially proprietary. | analyzed | 2.1 Production Attention Architectures |



### 2.2 Sub‑Quadratic Attention Variants

| ID | Architecture | Year | Era | GA | MAL | PAR | **H** | STI | IM | **E** | Zone | Source / Paper | Notes | Analyzed | Section |
|----|-------------|------|-----|----|-----|-----|------:|-----|----|------:|------|----------------|-------|----------|---------|
| B5 | Reformer (LSH attention) | 2020 | 2018–2022 | 1 | 1 | 2 | **4** | 1 | 1 | **2** | 🟡 Yellow | Kitaev et al. 2020 | LSH bucketing introduces irregular access and custom logic; some GEMMs remain, but hash/routing lowers GA/MAL and adds STI. | analyzed | 2.2 Sub‑Quadratic Attention Variants |
| B6 | Performer (FAVOR+) | 2020 | 2018–2022 | 1 | 1 | 2 | **4** | 1 | 0 | **1** | 🟠 Orange | Choromanski et al. 2020 | Random feature maps for softmax linearization; reasonable H but infra is still research‑grade (IM=0) at LLM scale. | analyzed | 2.2 Sub‑Quadratic Attention Variants |
| B19 | Longformer (Windowed + Global Attention) | 2020 | 2018–2022 | 1 | 1 | 2 | **4** | 2 | 1 | **3** | 🟡 Yellow | Beltagy et al. 2020 | Combines sliding‑window local attention with sparse global tokens; remains attention‑like but with more complex sparsity patterns and partial infra support. | analyzed | 2.2 Sub‑Quadratic Attention Variants |
| B20 | Linformer | 2020 | 2018–2022 | 1 | 1 | 2 | **4** | 1 | 0 | **1** | 🟠 Orange | Wang et al. 2020 | Projects keys/values into a low‑rank space to reduce complexity; introduces extra projections and lacks mature infra, keeping IM at 0. | analyzed | 2.2 Sub‑Quadratic Attention Variants |
| B21 | BigBird | 2020 | 2018–2022 | 1 | 1 | 2 | **4** | 2 | 1 | **3** | 🟡 Yellow | Zaheer et al. 2020 | Uses block, random, and global sparse attention patterns; keeps standard topology but requires specialized kernels and tuning. | analyzed | 2.2 Sub‑Quadratic Attention Variants |
| B22 | FNet | 2021 | 2018–2022 | 0 | 1 | 2 | **3** | 2 | 0 | **2** | 🟠 Orange | Lee‑Thorp et al. 2021 | Replaces attention with FFT mixing; highly non‑GEMM and research‑grade infra give GA=0 and IM=0 despite good PAR. | analyzed | 2.2 Sub‑Quadratic Attention Variants |
| B23 | AFT (Attention Free Transformer) | 2021 | 2018–2022 | 1 | 1 | 2 | **4** | 2 | 0 | **2** | 🟡 Yellow | Zhai et al. 2021 | Elementwise mixing with positional biases approximates attention with linear cost; infra remains research‑grade, so IM=0. | analyzed | 2.2 Sub‑Quadratic Attention Variants |



### 2.3 RNN‑Like Architectures

| ID | Architecture | Year | Era | GA | MAL | PAR | **H** | STI | IM | **E** | Zone | Source / Paper | Notes | Analyzed | Section |
|----|-------------|------|-----|----|-----|-----|------:|-----|----|------:|------|----------------|-------|----------|---------|
| B7 | RWKV‑7 | 2023 | 2023+ | 1 | 1 | 1 | **3** | 2 | 1 | **3** | 🟠 Orange | Peng et al. 2023 | RNN‑ish with channel‑mixing and time‑mixing; some GEMMs, but scan‑like behavior and custom kernels limit GA/MAL/PAR relative to standard attention. | analyzed | 2.3 RNN‑Like Architectures |
| B8 | xLSTM | 2024 | 2023+ | 1 | 1 | 0 | **2** | 2 | 1 | **3** | 🔴 Red | Beck et al. 2024 | Still fundamentally sequential (PAR=0) despite architectural tweaks; Gate‑1 parallelism bottleneck dominates. | analyzed | 2.3 RNN‑Like Architectures |
| B9 | HGRN2 | 2024 | 2023+ | 1 | 1 | 1 | **3** | 2 | 0 | **2** | 🟠 Orange | HGRN2 paper | Gated RNN with some parallel‑scan mitigation; infra remains research‑only / bespoke (IM=0). | analyzed | 2.3 RNN‑Like Architectures |



### 2.4 State‑Space Models and Hybrids

| ID | Architecture | Year | Era | GA | MAL | PAR | **H** | STI | IM | **E** | Zone | Source / Paper | Notes | Analyzed | Section |
|----|-------------|------|-----|----|-----|-----|------:|-----|----|------:|------|----------------|-------|----------|---------|
| B11 | S4 | 2021 | 2018–2022 | 1 | 1 | 2 | **4** | 2 | 1 | **3** | 🟡 Yellow | Gu et al. 2021 | FFT‑based SSM with good sequence‑parallelism; kernels are not GEMMs but are reasonably optimized; infra more niche than attention. | analyzed | 2.4 State‑Space Models and Hybrids |
| B12 | Hyena | 2023 | 2023+ | 1 | 1 | 2 | **4** | 2 | 1 | **3** | 🟡 Yellow | Poli et al. 2023 | Hierarchical convolution/FFT structure; strong PAR but non‑GEMM kernels and less common infra. | analyzed | 2.4 State‑Space Models and Hybrids |



### 2.5 Hybrid Architectures (Attention + SSM)

| ID | Architecture | Year | Era | GA | MAL | PAR | **H** | STI | IM | **E** | Zone | Source / Paper | Notes | Analyzed | Section |
|----|-------------|------|-----|----|-----|-----|------:|-----|----|------:|------|----------------|-------|----------|---------|
| B13 | Griffin (RG‑LRU hybrid) | 2024 | 2023+ | 1 | 1 | 1 | **3** | 2 | 1 | **3** | 🟠 Orange | De et al. 2024 | Fusion hybrid with recurrent components; we downgrade GA (1) because recurrence dominates effective kernel mix. | analyzed | 2.5 Hybrid Architectures (Attention + SSM) |
| B14 | Jamba (Mamba + Attention + MoE) | 2024 | 2023+ | 2 | 1 | 1 | **4** | 2 | 1 | **3** | 🟡 Yellow | Lenz et al. 2024 | Hybrid stack; attention parts are GEMM‑aligned, Mamba parts reduce PAR/MAL somewhat; infra is proprietary but solid. | analyzed | 2.5 Hybrid Architectures (Attention + SSM) |
| B15 | Samba (Sliding‑Window Attention + Mamba) | 2024 | 2023+ | 2 | 1 | 1 | **4** | 2 | 1 | **3** | 🟡 Yellow | Ren et al. 2024 | SW attention + Mamba layers; good H but mixed kernels and non‑universal infra keep it Yellow. | analyzed | 2.5 Hybrid Architectures (Attention + SSM) |
| B16 | Hymba (Fusion + Striped Hybrids) | 2024 | 2023+ | 2 | 1 | 1 | **4** | 2 | 1 | **3** | 🟡 Yellow | Dong et al. 2024 | NVIDIA‑stack hybrid (fusion + striped heads); GA solid, MAL/PAR slightly degraded vs pure attention, IM=1 due to vendor lock‑in. | analyzed | 2.5 Hybrid Architectures (Attention + SSM) |



### 2.6 Emerging Memory Systems

| ID | Architecture | Year | Era | GA | MAL | PAR | **H** | STI | IM | **E** | Zone | Source / Paper | Notes | Analyzed | Section |
|----|-------------|------|-----|----|-----|-----|------:|-----|----|------:|------|----------------|-------|----------|---------|
| B17 | Titans | 2024 | 2023+ | 1 | 1 | 1 | **3** | 0 | 0 | **0** | 🔴 Red | Behrouz et al. 2024 | Multi‑bank / multi‑type external memory; requires new distributed memory services and routing. No production‑grade infra yet. | analyzed | 2.6 Emerging Memory Systems |
| B18 | B’MOJO | 2024 | 2023+ | 1 | 1 | 1 | **3** | 0 | 0 | **0** | 🔴 Red | B’MOJO memory paper | Fading memory across banks and custom addressing; clearly new topology (STI=0) and research‑only kernels (IM=0). | analyzed | 2.6 Emerging Memory Systems |



### 2.7 Encoder‑Only Transformers (2018–2020)

| ID | Architecture | Year | Era | GA | MAL | PAR | **H** | STI | IM | **E** | Zone | Source / Paper | Notes | Analyzed | Section |
|----|-------------|------|-----|----|-----|-----|------:|-----|----|------:|------|----------------|-------|----------|---------|
| B24 | BERT | 2018 | 2018–2022 | 2 | 1 | 2 | **5** | 2 | 2 | **4** | 🟢 Green | Devlin et al. 2018 | Bidirectional encoder‑only Transformer using quadratic attention; same Gate‑1 profile as vanilla Transformer. | analyzed | 2.7 Encoder‑Only Transformers (2018–2020) |
| B25 | RoBERTa | 2019 | 2018–2022 | 2 | 1 | 2 | **5** | 2 | 2 | **4** | 🟢 Green | Liu et al. 2019 | Optimized BERT training and data; architecture remains standard Transformer. | analyzed | 2.7 Encoder‑Only Transformers (2018–2020) |
| B26 | ALBERT | 2019 | 2018–2022 | 2 | 1 | 2 | **5** | 2 | 2 | **4** | 🟢 Green | Lan et al. 2019 | Parameter‑sharing and factorization reduce memory but keep standard attention and topology. | analyzed | 2.7 Encoder‑Only Transformers (2018–2020) |
| B27 | XLNet | 2019 | 2018–2022 | 2 | 1 | 2 | **5** | 2 | 2 | **4** | 🟢 Green | Yang et al. 2019 | Permutation language modeling on a Transformer backbone; still quadratic attention with standard kernels. | analyzed | 2.7 Encoder‑Only Transformers (2018–2020) |
| B28 | ELECTRA | 2020 | 2018–2022 | 2 | 1 | 2 | **5** | 2 | 2 | **4** | 🟢 Green | Clark et al. 2020 | Discriminative pretraining objective on a vanilla Transformer encoder; no Gate‑1 architectural changes. | analyzed | 2.7 Encoder‑Only Transformers (2018–2020) |
| B29 | DeBERTa | 2020 | 2018–2022 | 2 | 1 | 2 | **5** | 2 | 2 | **4** | 🟢 Green | He et al. 2020 | Disentangled attention and position encoding but retains GEMM‑heavy quadratic attention and standard serving topology. | analyzed | 2.7 Encoder‑Only Transformers (2018–2020) |



### 2.8 Decoder‑Only / Unified Transformers (2019–2022)

| ID | Architecture | Year | Era | GA | MAL | PAR | **H** | STI | IM | **E** | Zone | Source / Paper | Notes | Analyzed | Section |
|----|-------------|------|-----|----|-----|-----|------:|-----|----|------:|------|----------------|-------|----------|---------|
| B30 | GPT‑2 | 2019 | 2018–2022 | 2 | 1 | 2 | **5** | 2 | 2 | **4** | 🟢 Green | Radford et al. 2019 | Decoder‑only Transformer with standard causal attention; same Gate‑1 profile as vanilla Transformer. | analyzed | 2.8 Decoder‑Only / Unified Transformers (2019–2022) |
| B31 | T5 | 2019 | 2018–2022 | 2 | 1 | 2 | **5** | 2 | 2 | **4** | 🟢 Green | Raffel et al. 2019 | Text‑to‑text encoder–decoder Transformer; quadratic attention in both encoder and decoder with standard kernels. | analyzed | 2.8 Decoder‑Only / Unified Transformers (2019–2022) |
| B32 | GPT‑3 | 2020 | 2018–2022 | 2 | 1 | 2 | **5** | 2 | 2 | **4** | 🟢 Green | Brown et al. 2020 | 175B‑parameter decoder‑only Transformer; scaling‑only change preserves Gate‑1 friction profile. | analyzed | 2.8 Decoder‑Only / Unified Transformers (2019–2022) |
| B33 | PaLM | 2022 | 2018–2022 | 2 | 1 | 2 | **5** | 2 | 2 | **4** | 🟢 Green | Chowdhery et al. 2022 | 540B‑parameter Transformer trained with Pathways; architecture remains standard quadratic attention. | analyzed | 2.8 Decoder‑Only / Unified Transformers (2019–2022) |



### 2.9 Mixture‑of‑Experts (Early Large‑Scale, 2021)

| ID | Architecture | Year | Era | GA | MAL | PAR | **H** | STI | IM | **E** | Zone | Source / Paper | Notes | Analyzed | Section |
|----|-------------|------|-----|----|-----|-----|------:|-----|----|------:|------|----------------|-------|----------|---------|
| B34 | Switch Transformer | 2021 | 2018–2022 | 2 | 1 | 2 | **5** | 1 | 1 | **2** | 🟡 Yellow | Fedus et al. 2021 | Large‑scale MoE with token‑level routing; expert FFNs are GEMM‑aligned but routing and expert parallelism introduce new topology and limited infra. | analyzed | 2.9 Mixture‑of‑Experts (Early Large‑Scale, 2021) |



### 2.10 Additional Foundation & Code Models (2019–2024)

| ID | Architecture | Year | Era | GA | MAL | PAR | **H** | STI | IM | **E** | Zone | Source / Paper | Notes | Analyzed | Section |
|----|-------------|------|-----|----|-----|-----|------:|-----|----|------:|------|----------------|-------|----------|---------|
| B35 | Mistral 7B | 2023 | 2023+ | 2 | 2 | 2 | **6** | 2 | 2 | **4** | 🟢 Green | Mistral AI 2023 | Sliding‑window decoder‑only Transformer; efficient windowed attention that outperforms Llama 2‑13B while preserving standard kernels. | analyzed | 2.10 Additional Foundation & Code Models (2019–2024) |
| B36 | Falcon 180B | 2023 | 2023+ | 2 | 1 | 2 | **5** | 2 | 2 | **4** | 🟢 Green | TII 2023 | 7B/40B/180B dense Transformer family; standard quadratic attention and MLP blocks trained on web‑scale data. | analyzed | 2.10 Additional Foundation & Code Models (2019–2024) |
| B37 | OPT | 2022 | 2018–2022 | 2 | 1 | 2 | **5** | 2 | 2 | **4** | 🟢 Green | Meta 2022 | 125M–175B GPT‑3‑style decoder‑only Transformers; open replication of GPT‑3 with standard quadratic attention and kernels. | analyzed | 2.10 Additional Foundation & Code Models (2019–2024) |
| B38 | BLOOM | 2022 | 2018–2022 | 2 | 1 | 2 | **5** | 2 | 2 | **4** | 🟢 Green | BigScience 2022 | 176B multilingual dense Transformer; standard decoder‑only architecture trained by a large collaborative effort. | analyzed | 2.10 Additional Foundation & Code Models (2019–2024) |
| B39 | OLMo | 2024 | 2023+ | 2 | 2 | 2 | **6** | 2 | 2 | **4** | 🟢 Green | AI2 2024 | Fully open stack (data, code, weights) with 7B/65B dense Transformers; strong engineering but no Gate‑1 architectural changes. | analyzed | 2.10 Additional Foundation & Code Models (2019–2024) |
| B40 | Yi 34B | 2024 | 2023+ | 2 | 2 | 2 | **6** | 2 | 2 | **4** | 🟢 Green | 01.AI 2024 | 6B/34B multilingual Transformer with GQA and modern training; standard dense attention stack. | analyzed | 2.10 Additional Foundation & Code Models (2019–2024) |
| B41 | Baichuan 2 | 2023 | 2023+ | 2 | 2 | 2 | **6** | 2 | 2 | **4** | 🟢 Green | Baichuan Inc. 2023 | 7B/13B Chinese‑focused dense Transformers; standard decoder‑only architecture with strong pretraining. | analyzed | 2.10 Additional Foundation & Code Models (2019–2024) |
| B42 | InternLM | 2023 | 2023+ | 2 | 2 | 2 | **6** | 2 | 2 | **4** | 🟢 Green | Shanghai AI Lab 2023 | 7B/20B dense Transformers with multimodal variants; standard attention stack with strong optimization. | analyzed | 2.10 Additional Foundation & Code Models (2019–2024) |
| B43 | ChatGLM | 2023 | 2023+ | 2 | 1 | 2 | **5** | 2 | 2 | **4** | 🟢 Green | Tsinghua GLM team 2023 | Bilingual (Chinese/English) GLM‑style Transformer; architecture remains dense attention with moderate MAL and strong infra support. | analyzed | 2.10 Additional Foundation & Code Models (2019–2024) |
| B44 | Chinchilla | 2022 | 2018–2022 | 2 | 1 | 2 | **5** | 2 | 2 | **4** | 🟢 Green | Hoffmann et al. 2022 | 70B dense Transformer used to derive compute‑optimal scaling laws; no architectural change vs Gopher‑style models. | analyzed | 2.10 Additional Foundation & Code Models (2019–2024) |
| B45 | Gopher | 2021 | 2018–2022 | 2 | 1 | 2 | **5** | 2 | 2 | **4** | 🟢 Green | Rae et al. 2021 | 280B dense Transformer from DeepMind; standard decoder‑only architecture that preceded Chinchilla. | analyzed | 2.10 Additional Foundation & Code Models (2019–2024) |
| B46 | StarCoder / StarCoder2 | 2024 | 2023+ | 2 | 2 | 2 | **6** | 2 | 2 | **4** | 🟢 Green | BigCode 2024 | 3B/7B/15B open code models built on standard decoder‑only Transformers; specialization comes from code data, not new kernels. | analyzed | 2.10 Additional Foundation & Code Models (2019–2024) |
| B47 | Code Llama | 2023 | 2023+ | 2 | 2 | 2 | **6** | 2 | 2 | **4** | 🟢 Green | Meta 2023 | 7B/13B/34B code‑specialized Llama 2 variants; dense Transformer with code‑focused training and tooling. | analyzed | 2.10 Additional Foundation & Code Models (2019–2024) |



### 2.11 Pre‑2023 Long‑Context Transformers

| ID | Architecture | Year | Era | GA | MAL | PAR | **H** | STI | IM | **E** | Zone | Source / Paper | Notes | Analyzed | Section |
|----|-------------|------|-----|----|-----|-----|------:|-----|----|------:|------|----------------|-------|----------|---------|
| B48 | Transformer‑XL | 2019 | 2018–2022 | 2 | 1 | 1 | **4** | 2 | 1 | **3** | 🟡 Yellow | Dai et al. 2019 | Segment‑level recurrence on top of attention; improves context length but introduces PAR=1 cross‑segment dependencies and extra infra friction. | analyzed | 2.11 Pre‑2023 Long‑Context Transformers |
| B49 | Perceiver IO | 2021 | 2018–2022 | 1 | 1 | 2 | **4** | 2 | 0 | **2** | 🟡 Yellow | Jaegle et al. 2021 | Perceiver‑style latent‑array cross‑attention applied to arbitrary modalities; strong flexibility but lower GA/IM and limited production adoption. | analyzed | 2.11 Pre‑2023 Long‑Context Transformers |



---

## 3. Additional Techniques from the Techniques List

These entries score frequently referenced primitives and training/infra techniques that are not tied to a single named model.

| ID | Architecture | Year | Era | GA | MAL | PAR | **H** | STI | IM | **E** | Zone | Source / Paper | Notes | Analyzed | Section |
|----|-------------|------|-----|----|-----|-----|------:|-----|----|------:|------|----------------|-------|----------|---------|
| C1 | RoPE (Rotary Position Embeddings) | 2021 | 2018–2022 | 2 | 2 | 2 | **6** | 2 | 2 | **4** | 🟢 Green | Su et al. 2021 | Weight‑only positional change; identical kernels and topology to standard attention. Pure Green Gate‑1 friction. | analyzed | 3. Additional Techniques from the Techniques List |
| C2 | RMSNorm | 2019 | 2018–2022 | 2 | 2 | 2 | **6** | 2 | 2 | **4** | 🟢 Green | Zhang & Sennrich 2019 | Normalization tweak with same matmul patterns and topology; essentially free from a Gate‑1 standpoint. | analyzed | 3. Additional Techniques from the Techniques List |
| C3 | LoRA / QLoRA | 2021 | 2018–2022 | 2 | 2 | 2 | **6** | 2 | 2 | **4** | 🟢 Green | Hu et al. 2021; Dettmers et al. 2023 | Low‑rank adapters plus (optionally) quantized base weights; still matmul‑dominated, no topology change, strong library support. | analyzed | 3. Additional Techniques from the Techniques List |
| C4 | Quantization for LLMs (Int8/Int4) | 2022 | 2018–2022 | 2 | 2 | 2 | **6** | 2 | 1 | **3** | 🟡 Yellow (software friction) | Dettmers et al. 2022; Frantar et al. 2022 | GEMM‑aligned low‑precision kernels; hardware side is excellent, but kernel availability and validation differences keep IM at 1. | analyzed | 3. Additional Techniques from the Techniques List |
| C5 | FlashAttention (kernel primitive) | 2022 | 2018–2022 | 2 | 2 | 2 | **6** | 2 | 2 | **4** | 🟢 Green | Dao et al. 2022 | IO‑aware attention kernel that avoids N×N materialization; now fully upstream and effectively Green for Gate‑1. | analyzed | 3. Additional Techniques from the Techniques List |
| C6 | Reversible Residual Networks (RevNets) | 2017 | pre‑2018 | 2 | 2 | 2 | **6** | 2 | 2 | **4** | 🟢 Green | Gomez et al. 2017 | Reversible blocks recompute activations instead of storing them; same GEMM workload and topology with slightly higher compute. | analyzed | 3. Additional Techniques from the Techniques List |
| C7 | Vendor‑Specific Kernel Stacks (TensorRT‑LLM / Triton / TPU XLA) | 2023 | 2023+ | 2 | 2 | 2 | **6** | 2 | 1 | **3** | 🟡 Yellow | NVIDIA / Google kernel & XLA docs | Highly optimized, GEMM‑aligned kernels for specific vendors; great H but IM=1 from the perspective of non‑vendor teams (stack‑specific). | analyzed | 3. Additional Techniques from the Techniques List |
| C8 | External Memory / RAG‑Style Systems | 2020 | 2018–2022 | 2 | 1 | 2 | **5** | 1 | 2 | **3** | 🟡 Yellow | Lewis et al. 2020; Wu et al. 2022 | Base model stays GEMM‑aligned; friction comes from added retrieval services (STI=1) and longer context windows. | analyzed | 3. Additional Techniques from the Techniques List |
| C9 | Capsule Networks | 2017 | pre‑2018 | 1 | 1 | 1 | **3** | 2 | 0 | **2** | 🟠 Orange | Sabour et al. 2017 | Vector “capsules” with routing‑by‑agreement; many small ops and routing passes, research‑grade infra only (IM=0). | analyzed | 3. Additional Techniques from the Techniques List |
| C10 | HyperNetworks | 2016 | pre‑2018 | 2 | 2 | 2 | **6** | 2 | 1 | **3** | 🟡 Yellow | Ha et al. 2016 | Secondary networks generating weights for a primary network; GEMM‑aligned but increases compute and relies on bespoke implementations (IM=1). | analyzed | 3. Additional Techniques from the Techniques List |
| C11 | Adaptive Computation Time / Universal Transformers | 2016 | pre‑2018 | 2 | 1 | 1 | **4** | 2 | 0 | **2** | 🟠 Orange | Graves 2016; Dehghani et al. 2018 | Token‑dependent halting/depth; data‑dependent control flow harms MAL/PAR and lacks mature infra. | analyzed | 3. Additional Techniques from the Techniques List |
| C12 | Layer Scale / Weighted Residuals | 2016 | pre‑2018 | 2 | 2 | 2 | **6** | 2 | 2 | **4** | 🟢 Green | Huang et al. 2016; Touvron et al. 2021 | Simple scaling factors on residuals; negligible kernel/topology impact and fully compatible with existing stacks. | analyzed | 3. Additional Techniques from the Techniques List |
| C13 | Perceiver‑Style / Hierarchical Cross‑Attention | 2021 | 2018–2022 | 2 | 1 | 2 | **5** | 2 | 1 | **3** | 🟡 Yellow | Jaegle et al. 2021 | Latent‑array cross‑attention and hierarchical patterns; still GEMM‑aligned but with more complex layouts and non‑universal infra. | analyzed | 3. Additional Techniques from the Techniques List |
| C14 | Learnable Routing Frameworks (PathNet / Graph HyperNetworks) | 2017 | pre‑2018 | 1 | 1 | 1 | **3** | 0 | 0 | **0** | 🔴 Red | Fernando et al. 2017; Zhang et al. 2018 | MoE‑like conditional execution with even more complex routing; effectively new topology and no production‑grade infra. | analyzed | 3. Additional Techniques from the Techniques List |
| C15 | Memory Networks / Neural Turing Machines | 2014 | pre‑2018 | 1 | 0 | 1 | **2** | 0 | 0 | **0** | 🔴 Red | Graves et al. 2014; Sukhbaatar et al. 2015 | Differentiable external memories with random access and iterative read/write; very poor MAL and topology/infra requirements. | analyzed | 3. Additional Techniques from the Techniques List |
| C16 | Forward‑Forward Algorithm | 2022 | 2018–2022 | 2 | 2 | 2 | **6** | 2 | 0 | **2** | 🟡 Yellow | Hinton 2022 | Two‑phase forward‑only training; hardware kernel shape is friendly, but no mature infra and higher training cost (extra passes). | analyzed | 3. Additional Techniques from the Techniques List |
| C17 | Sharpness‑Aware Minimization (SAM) | 2020 | 2018–2022 | 2 | 2 | 2 | **6** | 2 | 2 | **4** | 🟢 Green | Foret et al. 2020 | Training‑only optimization that doubles (or more) update cost but preserves kernels and topology; hardware Green, economic cost higher. | analyzed | 3. Additional Techniques from the Techniques List |
| C18 | Test‑Time Training | 2020 | 2018–2022 | 2 | 2 | 2 | **6** | 2 | 1 | **3** | 🟡 Yellow | Sun et al. 2020 | On‑the‑fly adaptation at inference with extra gradient steps; kernels/topology unchanged, but significant latency/compute overhead and limited infra. | analyzed | 3. Additional Techniques from the Techniques List |
| C19 | ByteNet | 2016 | pre‑2018 | 1 | 1 | 2 | **4** | 2 | 1 | **3** | 🟡 Yellow | Kalchbrenner et al. 2016 | Dilated causal convolutions for sequences (O(n log n)); convs map to GEMM but require custom kernels and have less mature infra than vanilla attention. | analyzed | 3. Additional Techniques from the Techniques List |
| C20 | WaveNet | 2016 | pre‑2018 | 1 | 1 | 2 | **4** | 2 | 1 | **3** | 🟡 Yellow | van den Oord et al. 2016 | Audio‑focused dilated causal convolutions; similar Gate‑1 profile to ByteNet with strong PAR but non‑GEMM‑centric kernels. | analyzed | 3. Additional Techniques from the Techniques List |
| C21 | QRNN | 2016 | pre‑2018 | 1 | 1 | 1 | **3** | 2 | 0 | **2** | 🟠 Orange | Bradbury et al. 2016 | Convolutional feature extraction plus recurrent pooling; some parallelism gains over RNNs but limited infra and non‑standard kernels. | analyzed | 3. Additional Techniques from the Techniques List |
| C22 | IndRNN | 2018 | 2018–2022 | 2 | 1 | 1 | **4** | 2 | 0 | **2** | 🟠 Orange | Li et al. 2018 | Independent recurrent neurons enabling better gradient flow and partial parallelization; still sequential in time and infra remains research‑grade. | analyzed | 3. Additional Techniques from the Techniques List |
| C23 | Temporal Convolutional Networks (TCN) | 2018 | 2018–2022 | 1 | 1 | 2 | **4** | 2 | 1 | **3** | 🟡 Yellow | Bai et al. 2018 | Temporal/dilated convolutions with good parallelism but conv‑heavy kernels and moderate infra maturity. | analyzed | 3. Additional Techniques from the Techniques List |

### 3.1 Final Pass Architectures (2018–2025)

| ID | Architecture | Year | Era | GA | MAL | PAR | **H** | STI | IM | **E** | Zone | Source / Paper | Notes | Analyzed | Section |
|----|-------------|------|-----|----|-----|-----|------:|-----|----|------:|------|----------------|-------|----------|---------|
| D1 | ELMo | 2018 | 2018–2022 | 2 | 1 | 0 | **3** | 2 | 2 | **4** | 🟠 Orange | Peters et al. 2018 | BiLSTM‑based contextual word embeddings; strongly sequential (PAR=0) and quickly eclipsed by Transformer‑based models; https://arxiv.org/abs/1802.05365. |  | 3.1 Final Pass Architectures (2018–2025) |
| D2 | ULMFiT | 2018 | 2018–2022 | 2 | 1 | 0 | **3** | 2 | 2 | **4** | 🟠 Orange | Howard & Ruder 2018 | LSTM‑based transfer learning for NLP with sequential bottlenecks (PAR=0); important historical baseline but hardware‑hostile at long sequences; https://arxiv.org/abs/1801.06146. |  | 3.1 Final Pass Architectures (2018–2025) |
| D3 | Megatron‑LM (model‑parallel training) | 2019 | 2018–2022 | 2 | 1 | 2 | **5** | 2 | 2 | **4** | 🟢 Green | Shoeybi et al. 2019 | Training framework for large Transformers using tensor/model parallelism and fused kernels; improves throughput without changing the core dense Transformer architecture; https://arxiv.org/abs/1909.08053. |  | 3.1 Final Pass Architectures (2018–2025) |
| D4 | GShard MoE | 2020 | 2018–2022 | 2 | 1 | 2 | **5** | 1 | 2 | **3** | 🟡 Yellow | Lepikhin et al. 2020 | Early large‑scale mixture‑of‑experts Transformer with conditional routing; experts remain GEMM‑aligned but routing/topology changes add STI=1 and infra complexity; https://arxiv.org/abs/2006.16668. |  | 3.1 Final Pass Architectures (2018–2025) |
| D5 | Synthesizer | 2020 | 2018–2022 | 1 | 1 | 2 | **4** | 2 | 0 | **2** | 🟡 Yellow | Tay et al. 2020 | Efficient attention variant replacing dot‑product scores with learned or random mixing weights; promising theory but limited infra and no production adoption; https://arxiv.org/abs/2005.00743. |  | 3.1 Final Pass Architectures (2018–2025) |
| D6 | Nyströmformer | 2021 | 2018–2022 | 1 | 1 | 2 | **4** | 2 | 0 | **2** | 🟡 Yellow | Xiong et al. 2021 | Nyström approximation to self‑attention for sub‑quadratic complexity; non‑standard kernels and weak ecosystem support keep it research‑only; https://arxiv.org/abs/2102.03902. |  | 3.1 Final Pass Architectures (2018–2025) |
| D7 | cosFormer | 2022 | 2018–2022 | 1 | 1 | 2 | **4** | 2 | 0 | **2** | 🟡 Yellow | Qin et al. 2022 | Linear attention via cosine re‑weighting of features; maintains parallelism but deviates from standard attention kernels and lacks robust deployment infra; https://arxiv.org/abs/2202.08791. |  | 3.1 Final Pass Architectures (2018–2025) |
| D8 | MEGA | 2022 | 2018–2022 | 1 | 1 | 1 | **3** | 2 | 0 | **2** | 🟠 Orange | Ma et al. 2022 | Moving‑average gated attention with hybrid EMA/attention structure; irregular ops and bespoke kernels yield H=3 with no production‑grade infra; https://arxiv.org/abs/2209.10655. |  | 3.1 Final Pass Architectures (2018–2025) |
| D9 | Megalodon | 2024 | 2023+ | 1 | 1 | 1 | **3** | 2 | 0 | **2** | 🟠 Orange | Ma et al. 2024 | Follow‑on to MEGA with “unlimited context” claims; retains complex non‑GEMM cores and remains research‑grade despite incremental improvements; https://arxiv.org/abs/2404.08801. |  | 3.1 Final Pass Architectures (2018–2025) |
| D10 | Based (linear attention) | 2024 | 2023+ | 1 | 1 | 2 | **4** | 2 | 0 | **2** | 🟡 Yellow | Arora & Dao 2024 | Stanford linear‑attention proposal targeting simpler long‑context kernels; still non‑standard relative to FlashAttention and lacks mature ecosystem support; https://arxiv.org/abs/2402.18668. |  | 3.1 Final Pass Architectures (2018–2025) |
| D11 | H3 (Hungry Hungry Hippos) | 2022 | 2018–2022 | 1 | 1 | 2 | **4** | 2 | 0 | **2** | 🟡 Yellow | Fu & Dao 2022 | SSM‑style hybrid with shift operations and attention‑like behavior; moderate hardware friendliness but no widespread infra or deployments; https://arxiv.org/abs/2212.14052. |  | 3.1 Final Pass Architectures (2018–2025) |
| D12 | DistilBERT | 2019 | 2018–2022 | 2 | 1 | 2 | **5** | 2 | 2 | **4** | 🟢 Green | Sanh et al. 2019 | Knowledge‑distilled BERT variant that compresses a standard Transformer while preserving GEMM‑aligned kernels and full ecosystem support; https://arxiv.org/abs/1910.01108. |  | 3.1 Final Pass Architectures (2018–2025) |
| D13 | BloombergGPT | 2023 | 2023+ | 2 | 1 | 2 | **5** | 2 | 1 | **3** | 🟡 Yellow | Wu et al. 2023 | Finance‑domain 50B‑scale dense Transformer; standard architecture with proprietary data and infra yielding IM=1 from an open ecosystem perspective; https://arxiv.org/abs/2303.17564. |  | 3.1 Final Pass Architectures (2018–2025) |
| D14 | Galactica | 2022 | 2018–2022 | 2 | 1 | 2 | **5** | 2 | 1 | **3** | 🟡 Yellow | Taylor et al. 2022 | Science‑focused dense Transformer; standard hardware profile but proprietary stack and eventual withdrawal despite strong training infra; https://arxiv.org/abs/2211.09085. |  | 3.1 Final Pass Architectures (2018–2025) |
| D15 | Med‑PaLM | 2022 | 2018–2022 | 2 | 1 | 2 | **5** | 2 | 1 | **3** | 🟡 Yellow | Singhal et al. 2022 | Medical‑domain PaLM‑style Transformer; architecture remains standard while domain‑specific data and closed infra limit general ecosystem accessibility; https://arxiv.org/abs/2212.13138. |  | 3.1 Final Pass Architectures (2018–2025) |
| D16 | CLIP | 2021 | 2018–2022 | 2 | 1 | 2 | **5** | 2 | 2 | **4** | 🟢 Green | Radford et al. 2021 | Multimodal dual‑encoder model (ViT image encoder + text Transformer) using standard attention; large‑scale contrastive training with fully mainstream kernels and infra; https://arxiv.org/abs/2103.00020. |  | 3.1 Final Pass Architectures (2018–2025) |



---

## 4. Notes and Next Steps

- These scores deliberately **err on the conservative side** for GA/MAL/PAR when kernels are non‑GEMM or infra is vendor‑specific; they should be revisited as real FLOP breakdowns or kernel traces become available.  
- For modeling, you can treat each row as one data point `(GA, MAL, PAR, STI, IM) → (H, E, Zone)` and add adoption labels (e.g., “frontier‑scale production” vs “research‑only”) on top.  
- Additional architectures from `techniques_for_scoring.md` (e.g., LoRA/QLoRA, quantization, RevNets, RAG, Capsules, HyperNetworks, ACT/Universal Transformers, SAM, test‑time training) can be added here as we pin down their GA/MAL/PAR/STI/IM scores.

### 4.1 Parameter Extraction Workflow (Param_Billions / Analyzed)

- **Source of truth:** `scored_architectures.csv` holds all parameter counts in `Param_Billions` (list of sizes in billions) plus an `Analyzed` flag. The markdown tables intentionally do **not** duplicate the sizes.
- **Scope of each pass:** When enriching parameters or locations, only touch rows with `Analyzed = ""`. Rows with `Analyzed = "analyzed"` are treated as frozen (even when `Param_Billions = []`).
- **Ingestion order for new IDs:**
  1. Add a new row with `Param_Billions = []`, `Analyzed = ""`, and fill `Model_Locations` with any known Hugging Face or arXiv links.  
  2. If a Hugging Face model card exists, read the “Parameters” section and populate `Param_Billions` manually; set `Analyzed = "analyzed"`.  
     - *Example:* For DistilBERT‑style rows, set something like `Param_Billions = [0.066, 0.134]` based on representative HF checkpoints and include those repos in `Model_Locations`.  
  3. For rows with arXiv `abs` URLs but no HF card, parse the **HTML landing page only** (no PDFs) for phrases like “7B parameters”, “125M to 175B parameters”, etc., normalize to billions, update `Param_Billions`, and set `Analyzed = "analyzed"`.
  4. For technique‑style IDs or papers without clean HTML parameter mentions, use the tooling in `scorecard_dataset/papers/`:
     - `fetch_and_convert_papers.py` — downloads canonical/representative PDFs (from arXiv and references in `techniques_for_scoring.md`) and dumps plain‑text Markdown into `papers/<ID>/markdown/`.
     - `parse_markdown_params.py` — searches those markdowns for “X B/M parameters” phrases, normalizes to billions, and updates `Param_Billions` (also merging arXiv `abs` URLs into `Model_Locations` and marking `Analyzed = "analyzed"`).
- **Finalization semantics:** Once all reasonable sources (HF cards, arXiv HTML, markdown from PDFs) have been checked for an ID, set `Analyzed = "analyzed"` even if `Param_Billions` remains `[]`. In that case, `Param_Billions = []` is an explicit “no reliable parameter info found after a full pass,” not “we haven’t looked yet.”
