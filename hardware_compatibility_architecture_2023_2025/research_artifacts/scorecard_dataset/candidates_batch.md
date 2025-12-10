# Inspection Report: Candidate Parameters

**Generated:** 2025-12-10 11:57:26

## ID: A5
### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 52 | **Candidates:** `7.0B`

```text
    50: 
    51: We introduce Mixtral 8x7B, a Sparse Mixture of Experts (SMoE) language
>>> 52: model. Mixtral has the same architecture as Mistral 7B, with the difference
    53: that each layer is composed of 8 feedforward blocks (i.e. experts). For every
    54: token, at each layer, a router network selects two experts to process the current
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 57 | **Candidates:** `13.0B, 47.0B`

```text
    55: state and combine their outputs. Even though each token only sees two experts,
    56: the selected experts can be different at each timestep. As a result, each token
>>> 57: has access to 47B parameters, but only uses 13B active parameters during
    58: inference. Mixtral was trained with a context size of 32k tokens and it outperforms
    59: or matches Llama 2 70B and GPT-3.5 across all evaluated benchmarks.
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 64 | **Candidates:** `70.0B`

```text
    62: generation, and multilingual benchmarks. We also provide a model fine-
    63: tuned to follow instructions, Mixtral 8x7B – Instruct, that surpasses GPT-3.5
>>> 64: Turbo, Claude-2.1, Gemini Pro, and Llama 2 70B – chat model on human bench-
    65: marks. Both the base and instruct models are released under the Apache 2.0 license.
    66: 
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 74 | **Candidates:** `7.0B`

```text
    72: Introduction
    73: 
>>> 74: In this paper, we present Mixtral 8x7B, a sparse mixture of experts model (SMoE) with open weights,
    75: licensed under Apache 2.0. Mixtral outperforms Llama 2 70B and GPT-3.5 on most benchmarks. As
    76: it only uses a subset of its parameters for every token, Mixtral allows faster inference speed at low
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 98 | **Candidates:** `7.0B`

```text
    96: regardless of the sequence length and the location of the information in the sequence.
    97: 
>>> 98: We also present Mixtral 8x7B – Instruct, a chat model fine-tuned to follow instructions using
    99: supervised fine-tuning and Direct Preference Optimization [25]. Its performance notably surpasses
    100: that of GPT-3.5 Turbo, Claude-2.1, Gemini Pro, and Llama 2 70B – chat model on human evaluation
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 100 | **Candidates:** `70.0B`

```text
    98: We also present Mixtral 8x7B – Instruct, a chat model fine-tuned to follow instructions using
    99: supervised fine-tuning and Direct Preference Optimization [25]. Its performance notably surpasses
>>> 100: that of GPT-3.5 Turbo, Claude-2.1, Gemini Pro, and Llama 2 70B – chat model on human evaluation
    101: benchmarks. Mixtral – Instruct also demonstrates reduced biases, and a more balanced sentiment
    102: profile in benchmarks such as BBQ, and BOLD.
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 301 | **Candidates:** `13.0B`

```text
    299: Size and Efficiency. We compare our performance to the Llama 2 family, aiming to understand
    300: Mixtral models’ efficiency in the cost-performance spectrum (see Figure 3). As a sparse Mixture-
>>> 301: of-Experts model, Mixtral only uses 13B active parameters for each token. With 5x lower active
    302: parameters, Mixtral is able to outperform Llama 2 70B across most categories.
    303: 
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 302 | **Candidates:** `70.0B`

```text
    300: Mixtral models’ efficiency in the cost-performance spectrum (see Figure 3). As a sparse Mixture-
    301: of-Experts model, Mixtral only uses 13B active parameters for each token. With 5x lower active
>>> 302: parameters, Mixtral is able to outperform Llama 2 70B across most categories.
    303: 
    304: Note that this analysis focuses on the active parameter count (see Section 2.1), which is directly
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 532 | **Candidates:** `70.0B`

```text
    530: Figure 6: LMSys Leaderboard. (Screenshot from Dec 22, 2023) Mixtral 8x7B Instruct v0.1 achieves an Arena
    531: Elo rating of 1121 outperforming Claude-2.1 (1117), all versions of GPT-3.5-Turbo (1117 best), Gemini Pro
>>> 532: (1111), and Llama-2-70b-chat (1077). Mixtral is currently the best open-weights model by a large margin.
    533: 
    534: 3https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 676 | **Candidates:** `7.0B`

```text
    674: 
    675: In this paper, we introduced Mixtral 8x7B, the first mixture-of-experts network to reach a state-of-the-
>>> 676: art performance among open-source models. Mixtral 8x7B Instruct outperforms Claude-2.1, Gem-
    677: ini Pro, and GPT-3.5 Turbo on human evaluation benchmarks. Because it only uses two experts at each
    678: time step, Mixtral only uses 13B active parameters per token while outperforming the previous best
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 678 | **Candidates:** `13.0B`

```text
    676: art performance among open-source models. Mixtral 8x7B Instruct outperforms Claude-2.1, Gem-
    677: ini Pro, and GPT-3.5 Turbo on human evaluation benchmarks. Because it only uses two experts at each
>>> 678: time step, Mixtral only uses 13B active parameters per token while outperforming the previous best
    679: model using 70B parameters per token (Llama 2 70B). We are making our trained and fine-tuned mod-
    680: els publicly available under the Apache 2.0 license. By sharing our models, we aim to facilitate the de-
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 679 | **Candidates:** `70.0B`

```text
    677: ini Pro, and GPT-3.5 Turbo on human evaluation benchmarks. Because it only uses two experts at each
    678: time step, Mixtral only uses 13B active parameters per token while outperforming the previous best
>>> 679: model using 70B parameters per token (Llama 2 70B). We are making our trained and fine-tuned mod-
    680: els publicly available under the Apache 2.0 license. By sharing our models, we aim to facilitate the de-
    681: velopment of new techniques and applications that can benefit a wide range of industries and domains.
```

---

## ID: A6
### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 11 | **Candidates:** `21.0B, 236.0B`

```text
    9: 
    10: We present DeepSeek-V2, a strong Mixture-of-Experts (MoE) language model characterized by
>>> 11: economical training and efficient inference. It comprises 236B total parameters, of which 21B
    12: are activated for each token, and supports a context length of 128K tokens. DeepSeek-V2 adopts
    13: innovative architectures including Multi-head Latent Attention (MLA) and DeepSeekMoE.
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 21 | **Candidates:** `21.0B`

```text
    19: DeepSeek-V2 on a high-quality and multi-source corpus consisting of 8.1T tokens, and further
    20: perform Supervised Fine-Tuning (SFT) and Reinforcement Learning (RL) to fully unlock its
>>> 21: potential. Evaluation results show that, even with only 21B activated parameters, DeepSeek-V2
    22: and its chat versions still achieve top-tier performance among open-source models. The model
    23: checkpoints are available at https://github.com/deepseek-ai/DeepSeek-V2.
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 212 | **Candidates:** `16.0B`

```text
    210: A Contributions and Acknowledgments
    211: 
>>> 212: B DeepSeek-V2-Lite: A 16B Model Equipped with MLA and DeepSeekMoE
    213: 
    214: 2
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 337 | **Candidates:** `21.0B, 236.0B`

```text
    335: problem, we introduce DeepSeek-V2, a strong open-source Mixture-of-Experts (MoE) language
    336: model, characterized by economical training and efficient inference through an innovative
>>> 337: Transformer architecture. It is equipped with a total of 236B parameters, of which 21B are
    338: activated for each token, and supports a context length of 128K tokens.
    339: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 371 | **Candidates:** `21.0B`

```text
    369: We evaluate DeepSeek-V2 on a wide range of benchmarks in English and Chinese, and
    370: compare it with representative open-source models. Evaluation results show that even with only
>>> 371: 21B activated parameters, DeepSeek-V2 still achieves top-tier performance among open-source
    372: models and becomes the strongest open-source MoE language model. Figure 1(a) highlights
    373: that, on MMLU, DeepSeek-V2 achieves top-ranking performance with only a small number
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 374 | **Candidates:** `67.0B`

```text
    372: models and becomes the strongest open-source MoE language model. Figure 1(a) highlights
    373: that, on MMLU, DeepSeek-V2 achieves top-ranking performance with only a small number
>>> 374: of activated parameters. In addition, as shown in Figure 1(b), compared with DeepSeek 67B,
    375: DeepSeek-V2 saves 42.5% of training costs, reduces the KV cache by 93.3%, and boosts the
    376: maximum generation throughput to 5.76 times. We also evaluate DeepSeek-V2 Chat (SFT) and
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 395 | **Candidates:** `2.4B, 15.7B`

```text
    393: In order to facilitate further research and development on MLA and DeepSeekMoE, we also
    394: release DeepSeek-V2-Lite, a smaller model equipped with MLA and DeepSeekMoE, for the
>>> 395: open-source community. It has a total of 15.7B parameters, where 2.4B are activated for each
    396: token. Detailed descriptions about DeepSeek-V2-Lite can be found in Appendix B.
    397: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1056 | **Candidates:** `21.0B`

```text
    1054: bottlenecks (i.e., the compressed latent vectors and the intermediate hidden states of routed
    1055: experts) to ensure stable training. Under this configuration, DeepSeek-V2 comprises 236B total
>>> 1056: parameters, of which 21B are activated for each token.
    1057: 
    1058: Training Hyper-Parameters. We employ the AdamW optimizer (Loshchilov and Hutter, 2017)
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1190 | **Candidates:** `22.0B, 70.0B`

```text
    1188: In Table 2, we compare DeepSeek-V2 with several representative open-source models, includ-
    1189: ing DeepSeek 67B (DeepSeek-AI, 2024) (our previous release), Qwen1.5 72B (Bai et al., 2023),
>>> 1190: LLaMA3 70B (AI@Meta, 2024), and Mixtral 8x22B (Mistral, 2024). We evaluate all these models
    1191: with our internal evaluation framework, and ensure that they share the same evaluation setting.
    1192: Overall, with only 21B activated parameters, DeepSeek-V2 significantly outperforms DeepSeek
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1192 | **Candidates:** `21.0B`

```text
    1190: LLaMA3 70B (AI@Meta, 2024), and Mixtral 8x22B (Mistral, 2024). We evaluate all these models
    1191: with our internal evaluation framework, and ensure that they share the same evaluation setting.
>>> 1192: Overall, with only 21B activated parameters, DeepSeek-V2 significantly outperforms DeepSeek
    1193: 67B on almost all benchmarks, and achieves top-tier performance among open-source models.
    1194: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1193 | **Candidates:** `67.0B`

```text
    1191: with our internal evaluation framework, and ensure that they share the same evaluation setting.
    1192: Overall, with only 21B activated parameters, DeepSeek-V2 significantly outperforms DeepSeek
>>> 1193: 67B on almost all benchmarks, and achieves top-tier performance among open-source models.
    1194: 
    1195: Further, we elaborately compare DeepSeek-V2 with its open-source counterparts one by
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1196 | **Candidates:** `72.0B`

```text
    1194: 
    1195: Further, we elaborately compare DeepSeek-V2 with its open-source counterparts one by
>>> 1196: one. (1) Compared with Qwen1.5 72B, another model that supports both Chinese and English,
    1197: DeepSeek-V2 demonstrates overwhelming advantages on the majority of English, code, and
    1198: math benchmarks. As for Chinese benchmarks, Qwen1.5 72B shows better performance on
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1482 | **Candidates:** `21.0B`

```text
    1480: models are evaluated in our internal framework and share the same evaluation setting. Bold
    1481: denotes the best and underline denotes the second-best. Scores with a gap smaller than 0.3
>>> 1482: are regarded as at the same level. With only 21B activated parameters, DeepSeek-V2 achieves
    1483: top-tier performance among open-source models.
    1484: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1497 | **Candidates:** `70.0B`

```text
    1495: English capabilities with LLaMA3 70B. However, even with much fewer training tokens and
    1496: activated parameters, DeepSeek-V2 still demonstrates comparable code and math capability
>>> 1497: with LLaMA3 70B. Also, as a bilingual language model, DeepSeek-V2 outperforms LLaMA3
    1498: 
    1499: 15
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1512 | **Candidates:** `67.0B`

```text
    1510: Training Costs. Since DeepSeek-V2 activates fewer parameters for each token and requires
    1511: fewer FLOPs than DeepSeek 67B, training DeepSeek-V2 will be more economical than training
>>> 1512: DeepSeek 67B theoretically. Although training an MoE model will introduce additional commu-
    1513: nication overheads, through our operator and communication optimizations, the training for
    1514: DeepSeek-V2 can attain a relatively high Model FLOPs Utilization (MFU). During our practical
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1693 | **Candidates:** `22.0B`

```text
    1691: V2 Chat (SFT) demonstrates slightly lower scores than Qwen1.5 72B Chat on multi-subject
    1692: multiple-choice tasks, consistent with the performance observed from their base versions. When
>>> 1693: compared with the state-of-the-art open-source MoE model, Mixtral 8x22B Instruct, DeepSeek-
    1694: V2 Chat (SFT) exhibits better performance on most benchmarks, except for NaturalQuestions
    1695: and IFEval. Furthermore, in comparison to the state-of-the-art open-source model LLaMA3 70B
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1695 | **Candidates:** `70.0B`

```text
    1693: compared with the state-of-the-art open-source MoE model, Mixtral 8x22B Instruct, DeepSeek-
    1694: V2 Chat (SFT) exhibits better performance on most benchmarks, except for NaturalQuestions
>>> 1695: and IFEval. Furthermore, in comparison to the state-of-the-art open-source model LLaMA3 70B
    1696: Chat, DeepSeek-V2 Chat (SFT) shows similar performance in code and math related benchmarks.
    1697: LLaMA3 70B Chat exhibits better performance on MMLU and IFEval, while DeepSeek-V2 Chat
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1963 | **Candidates:** `70.0B`

```text
    1961: Table 3 | Comparison among DeepSeek-V2 Chat (SFT), DeepSeek-V2 Chat (RL), and other
    1962: representative open-source chat models. Regarding TriviaQA and NaturalQuestions, it is
>>> 1963: worth noting that chat models, such as LLaMA3 70B Instruct, might not strictly adhere to the
    1964: format constraints typically specified in the few-shot setting. Consequently, this can lead to
    1965: underestimation of certain models in our evaluation framework.
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2404 | **Candidates:** `21.0B`

```text
    2402: stronger performance, and meanwhile saves 42.5% of training costs, reduces the KV cache
    2403: by 93.3%, and boosts the maximum generation throughput to 5.76 times. Evaluation results
>>> 2404: further demonstrate that with only 21B activated parameters, DeepSeek-V2 achieves top-tier
    2405: performance among open-source models and becomes the strongest open-source MoE model.
    2406: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2923 | **Candidates:** `16.0B`

```text
    2921: 
    2922: 
>>> 2923: B. DeepSeek-V2-Lite: A 16B Model Equipped with MLA and DeepSeekMoE
    2924: 
    2925: B.1. Model Description
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2934 | **Candidates:** `15.7B`

```text
    2932: Each MoE layer consists of 2 shared experts and 64 routed experts, where the intermediate
    2933: hidden dimension of each expert is 1408. Among the routed experts, 6 experts will be activated
>>> 2934: for each token. Under this configuration, DeepSeek-V2-Lite comprises 15.7B total parameters, of
    2935: which 2.4B are activated for each token.
    2936: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3357 | **Candidates:** `7.0B`

```text
    3355: D.1. Ablation of MHA, GQA, and MQA
    3356: 
>>> 3357: We show the evaluation results for 7B dense models with MHA, GQA, and MQA on four hard
    3358: benchmarks in Table 8. All of these three models are trained on 1.33T tokens, and share the same
    3359: architecture except for the attention mechanisms. In addition, for a fair comparison, we align
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3360 | **Candidates:** `7.0B`

```text
    3358: benchmarks in Table 8. All of these three models are trained on 1.33T tokens, and share the same
    3359: architecture except for the attention mechanisms. In addition, for a fair comparison, we align
>>> 3360: the number of parameters of them to around 7B by adjusting the number of layers. From the
    3361: table, we can find that MHA demonstrates significant advantages over GQA and MQA on these
    3362: benchmarks.
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3368 | **Candidates:** `16.0B`

```text
    3366: In Table 9, we show the evaluation results for MoE models equipped with MLA and MHA,
    3367: respectively, on four hard benchmarks. For a solid conclusion, we train and evaluate models
>>> 3368: across two scales. Two small MoE models comprise about 16B total parameters, and we train
    3369: them on 1.33T tokens. Two large MoE models comprise about 250B total parameters, and we
    3370: train them on 420B tokens. Also, two small MoE models and two large MoE models respectively
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3369 | **Candidates:** `250.0B`

```text
    3367: respectively, on four hard benchmarks. For a solid conclusion, we train and evaluate models
    3368: across two scales. Two small MoE models comprise about 16B total parameters, and we train
>>> 3369: them on 1.33T tokens. Two large MoE models comprise about 250B total parameters, and we
    3370: train them on 420B tokens. Also, two small MoE models and two large MoE models respectively
    3371: share the same architecture except for the attention mechanisms. From the table, we can observe
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3423 | **Candidates:** `7.0B`

```text
    3421: 43.5
    3422: 
>>> 3423: Table 8 | Comparison among 7B dense models with MHA, GQA, and MQA, respectively. MHA
    3424: demonstrates significant advantages over GQA and MQA on hard benchmarks.
    3425: 
```

---

## ID: A7
### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 62 | **Candidates:** `3.0B`

```text
    60: inference (5× higher throughput than Transformers) and linear scaling in sequence length, and its performance improves
    61: on real data up to million-length sequences. As a general sequence model backbone, Mamba achieves state-of-the-art
>>> 62: performance across several modalities such as language, audio, and genomics. On language modeling, our Mamba-3B model
    63: outperforms Transformers of the same size and matches Transformers twice its size, both in pretraining and downstream
    64: evaluation.
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 137 | **Candidates:** `1.0B`

```text
    135: 
    136: • Language Modeling. Mamba is the first linear-time sequence model that truly achieves Transformer-quality performance,
>>> 137: both in pretraining perplexity and downstream evaluations. With scaling laws up to 1B parameters, we show that Mamba
    138: exceeds the performance of a large range of baselines, including very strong modern Transformer training recipes based
    139: on LLaMa (Touvron et al. 2023). Our Mamba language model has 5× generation throughput compared to Transformers
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 140 | **Candidates:** `3.0B`

```text
    138: exceeds the performance of a large range of baselines, including very strong modern Transformer training recipes based
    139: on LLaMa (Touvron et al. 2023). Our Mamba language model has 5× generation throughput compared to Transformers
>>> 140: of similar size, and Mamba-3B’s quality matches that of Transformers twice its size (e.g. 4 points higher avg. on common
    141: sense reasoning compared to Pythia-3B and even exceeding Pythia-7B).
    142: 
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 752 | **Candidates:** `20.0B`

```text
    750: Table 3: (Zero-shot Evaluations.) Best results for each size in bold. We compare against open source LMs with various tokenizers,
    751: trained for up to 300B tokens. Pile refers to the validation split, comparing only against models trained on the same dataset and tokenizer
>>> 752: (GPT-NeoX-20B). For each model size, Mamba is best-in-class on every single evaluation result, and generally matches baselines at twice
    753: the model size.
    754: 
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 1147 | **Candidates:** `0.001B`

```text
    1145: compare the HyenaDNA and Mamba models, as quadratic attention becomes prohibitively expensive at longer sequence
    1146: lengths. We pretrain models on sequence lengths 210 = 1024, 212 = 4096, 214 = 16384, 216 = 65536, 218 = 262144,
>>> 1147: 220 = 1048576. We fix a model size of 6 layers by width 128 (about 1.3M-1.4M parameters). Models were trained for 20𝐾
    1148: gradient steps for a total of ≈ 330𝐵 tokens. The longer sequence lengths used sequence length warmup similar to (Nguyen,
    1149: Poli, et al. 2023).
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 1361 | **Candidates:** `0.006B`

```text
    1359: 0.19
    1360: 
>>> 1361: Table 5: (SC09 Model Ablations) Models with 6M parameters. In
    1362: SaShiMi’s U-Net backbone, there are 8 center blocks operating on
    1363: sequence length 1000, sandwiched on each side by 8 outer blocks on
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 1438 | **Candidates:** `6.9B`

```text
    1436: (FlashAttention-2 (Dao 2024)) beyond sequence length 2K, and up to 20-40× faster than a standard scan implementation
    1437: in PyTorch. Mamba achieves 4-5× higher inference throughput than a Transformer of similar size, since without the
>>> 1438: KV cache it can use much higher batch sizes. For example, a Mamba-6.9B (untrained) would have higher inference
    1439: throughput than a 5× smaller Transformer-1.3B. Details in Appendix E.5, which additionally includes a benchmark of
    1440: memory consumption.
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 1447 | **Candidates:** `0.35B`

```text
    1445: 4.6 Model Ablations
    1446: We perform a series of detailed ablations on components of our model, focusing on the setting of language modeling with
>>> 1447: size ≈ 350M models at Chinchilla token counts (same setting as Figure 4).
    1448: 
    1449: 4.6.1 Architecture
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 1743 | **Candidates:** `7.0B`

```text
    1741: Scaling. Our empirical evaluation is limited to small model sizes, below the threshold of most strong open source LLMs
    1742: (e.g. Llama (Touvron et al. 2023)) as well as other recurrent models such as RWKV (B. Peng et al. 2023) and RetNet (Y. Sun
>>> 1743: et al. 2023), which have been evaluated at the 7B parameter scale and beyond. It remains to assess whether Mamba still
    1744: compares favorably at these larger sizes. We also note that scaling SSMs may involve further engineering challenges and
    1745: adjustments to the model that are not discussed in this paper.
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 1797 | **Candidates:** `20.0B`

```text
    1795: Natural Language”. In: Proceedings of the AAAI conference on Artificial Intelligence. Vol. 34. 2020.
    1796: Sid Black, Stella Biderman, Eric Hallahan, Quentin Anthony, Leo Gao, Laurence Golding, Horace He, Connor Leahy,
>>> 1797: Kyle McDonell, Jason Phang, et al. “Gpt-NeoX-20B: An Open-source Autoregressive Language Model”. In: arXiv
    1798: preprint arXiv:2204.06745 (2022).
    1799: 
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 2439 | **Candidates:** `1.0B`

```text
    2437: is similar to our Induction Heads extrapolation experiment (Table 2).
    2438: 
>>> 2439: • LongNet (Ding et al. 2023), which claimed to scale to 1B length but only evaluated on length < 100𝐾 for actual tasks.
    2440: 
    2441: • Hyena and HyenaDNA (Nguyen, Poli, et al. 2023; Poli et al. 2023), which claimed to leverage up to 1M context. How-
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 2739 | **Candidates:** `0.001B, 1.3B`

```text
    2737: 
    2738: Model Sizes. Table 12 specifies the model sizes we use for scaling laws. This is taken directly from the GPT3 specifi-
>>> 2739: cations (Brown et al. 2020), with very minor modifications. First, we changed the batch size of the 1.3B model from 1M
    2740: tokens to 0.5M tokens, since we did not use enough parallelization to require the larger batch size. Second, we changed the
    2741: number of training steps and total tokens to roughly match Chinchilla scaling laws (Hoffmann et al. 2022), which specify
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 2904 | **Candidates:** `1.3B`

```text
    2902: 
    2903: This pretraining procedure is the same as the scaling law protocol, but extended to 300B tokens and with the GPT-NeoX
>>> 2904: tokenizer (Black et al. 2022) instead of GPT2 tokenizer. For the 1.3B model, we use a batch size of 1M tokens to be consistent
    2905: with the GPT3 specifications. We report the perplexity on the Pile validation set, and for this metric only compare to
    2906: models trained on the same dataset and with the same tokenizer, in particular Pythia and RWKV.
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 3186 | **Candidates:** `0.004B`

```text
    3184: E.4.1 YouTubeMix Audio Pretraining
    3185: Model. We use a model with 3 blocks per stage (3 × 5 = 15 total Mamba blocks), pooling factor 𝑝 = 16, and outer
>>> 3186: dimension 𝐷 = 64, for about 3.5M parameters.
    3187: 
    3188: Dataset. The data is mu-law encoded at 8 bits, so the model is modeling discrete tokens with a vocab size of 256.
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 3202 | **Candidates:** `0.006B`

```text
    3200: 
    3201: Additional Ablations: SSM Parameterizations. We investigate SSM parameterizations on long-form audio waveform
>>> 3202: pretraining in the setting of Figure 7. The setting is modified slightly to use larger models (8 layers and 𝐷 = 64 for 6M
    3203: params, the SaShiMi default), shorter sequences (211 = 2048 to 218 = 262144 instead of 213 to 220), lower LR (0.001 from
    3204: 0.002), and shorter training cycles (100K instead of 200K steps).
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 3246 | **Candidates:** `0.006B`

```text
    3244: pooling factor 4. The S4+MLP block has roughly 2𝐷 2 + 4𝐷 2 parameters (expansion factor 2 in the MLP). The Transformer
    3245: block has 4𝐷 2 + 2𝐷 2 parameters (expansion factor 1 in the MLP). The Mamba block has the usual ≈ 6𝐷 2 parameters. All
>>> 3246: models have roughly 6M total parameters.
    3247: 
    3248: E.5 Efficiency Benchmark
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 3310 | **Candidates:** `1.4B, 6.9B`

```text
    3308: We measure with BF16 inputs, which is the data type most commonly used for large scale training.
    3309: 
>>> 3310: End-to-end Inference. We measure the inference throughput of a Mamba 1.4B model and an untrained Mamba 6.9B
    3311: model, against a standard Transformer (GPT3 architecture) at 1.3B and 6.7B size. We use the standard Transformer
    3312: implementation in the Huggingface transformers library.
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 3311 | **Candidates:** `1.3B, 6.7B`

```text
    3309: 
    3310: End-to-end Inference. We measure the inference throughput of a Mamba 1.4B model and an untrained Mamba 6.9B
>>> 3311: model, against a standard Transformer (GPT3 architecture) at 1.3B and 6.7B size. We use the standard Transformer
    3312: implementation in the Huggingface transformers library.
    3313: 
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 3320 | **Candidates:** `0.125B`

```text
    3318: 
    3319: Memory Benchmark. The memory usage simply scales proportionally to the size of the activation tensors, as with
>>> 3320: most deep sequence models. We report measurements of the training memory requirements of 125M models on 1 A100
    3321: 80GB GPU. Each batch consists of sequences of length 2048. We compare to the most memory-efficient Transformer
    3322: implementation we are aware of (with kernel fusion from torch.compile and with FlashAttention-2). Table 15 shows that
```

---

## ID: A8
### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 152 | **Candidates:** `0.34B, 1.3B, 15.0B`

```text
    150: gated linear attention (GLA) Transformer on moderate-scale
    151: language modeling benchmarks, where we train models with
>>> 152: 340M/1.3B parameters on 15B/100B tokens, respectively.
    153: We find that the GLA Transformer performs favorably
    154: against a strong LLaMA architecture Transformer baseline
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 1233 | **Candidates:** `0.34B`

```text
    1231: acc ↑
    1232: 
>>> 1233: 340M Params Transformer++ 28.39 42.69
    1234: 15B Tokens
    1235: 32.33 49.19
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 1243 | **Candidates:** `1.3B`

```text
    1241: GLA
    1242: 
>>> 1243: 1.3B Params
    1244: 100B Tokens RetNet
    1245: Mamba
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 1330 | **Candidates:** `0.34B, 1.3B`

```text
    1328: 
    1329: Table 2: GLA Transformer results against Transformer++ (Touvron et al., 2023), RetNet (Sun et al., 2023a), and Mamba (Gu & Dao, 2023).
>>> 1330: All models are trained on the same subset of the SlimPajama dataset with the Mistral tokenizer. The 340M/1.3B models are trained for
    1331: 15B/100B tokens respectively. The individual task performance is via zero-shot. We report the main results on the same set of tasks reported
    1332: by Gu & Dao (2023). See Appendix D for results on other benchmarks, including 5-shot results. The last column shows the average over all
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 1359 | **Candidates:** `0.34B, 1.3B`

```text
    1357: 
    1358: Training details. We train all models from scratch at
>>> 1359: two scales: 340M and 1.3B. All models are trained with
    1360: AdamW (Loshchilov & Hutter, 2018) using a maximum
    1361: learning rate of 3e-4. The 340M models are trained on 15B
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 1361 | **Candidates:** `0.34B, 15.0B`

```text
    1359: two scales: 340M and 1.3B. All models are trained with
    1360: AdamW (Loshchilov & Hutter, 2018) using a maximum
>>> 1361: learning rate of 3e-4. The 340M models are trained on 15B
    1362: tokens with a batch size of 0.5M tokens, while the 1.3B
    1363: models are trained on 100B tokens with a batch size of
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 1362 | **Candidates:** `1.3B`

```text
    1360: AdamW (Loshchilov & Hutter, 2018) using a maximum
    1361: learning rate of 3e-4. The 340M models are trained on 15B
>>> 1362: tokens with a batch size of 0.5M tokens, while the 1.3B
    1363: models are trained on 100B tokens with a batch size of
    1364: 2M tokens. We use a cosine learning rate schedule with
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 1535 | **Candidates:** `1.3B, 100.0B`

```text
    1533: 20
    1534: 
>>> 1535: Figure 5: Length extrapolation on the test set of SlimPajama and PG19. We pretrain 1.3B models from scratch on SlimPajama for 100B
    1536: tokens with different training length. ∗ indicates models using truncated BPTT with over 12 segments that are each of 2K-length.
    1537: 
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 1539 | **Candidates:** `0.34B`

```text
    1537: 
    1538: Scale
>>> 1539: 340M Params
    1540: 15B Tokens
    1541: 
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 1542 | **Candidates:** `1.3B`

```text
    1540: 15B Tokens
    1541: 
>>> 1542: 1.3B Params
    1543: 100B Tokens
    1544: 
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 1661 | **Candidates:** `1.3B`

```text
    1659: 
    1660: Fig. 6 shows the throughput and memory usage as a function
>>> 1661: of the sequence length and batch size for the different 1.3B
    1662: models on a single H100 GPU.10 Here GLA adopts the
    1663: 
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 1696 | **Candidates:** `0.34B, 7.0B`

```text
    1694: 14.61
    1695: 
>>> 1696: Table 4: Ablation study results on the 340M model trained for 7B
    1697: tokens. We evaluate the model variants via the average perplexity
    1698: of the last 200 training steps.
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 2325 | **Candidates:** `175.0B`

```text
    2323: Qin, Z., Li, D., Sun, W., Sun, W., Shen, X., Han, X., Wei,
    2324: Y., Lv, B., Yuan, F., Luo, X., et al. Scaling transnormer to
>>> 2325: 175 billion parameters. arXiv preprint arXiv:2307.14995,
    2326: 2023b.
    2327: 
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 3932 | **Candidates:** `0.34B, 1.3B, 15.0B`

```text
    3930: 
    3931: Table 5: Extended zero- and five-shot performance results. All models are trained on the same subset of SlimPajama dataset with Mistral
>>> 3932: tokenizer. The 340M/1.3B models are trained for 15B/100B tokens respectively. The last column shows the average of all accuracies.
    3933: 
    3934: D Additional Experimental Results
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 3936 | **Candidates:** `1.3B`

```text
    3934: D Additional Experimental Results
    3935: 
>>> 3936: The complete results on all 11 tasks, including the 5-shot results for the 1.3B models, are shown in Table 5.
    3937: 
    3938: 23
```

---

