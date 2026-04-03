# Inspection Report: Candidate Parameters

**Generated:** 2025-12-10 11:55:23

## ID: A3
### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 11 | **Candidates:** `21.0B, 236.0B`

```text
    9: 
    10: We present DeepSeek-V2, a strong Mixture-of-Experts (MoE) language model characterized by
>>> 11: economical training and efficient inference. It comprises 236B total parameters, of which 21B
    12: are activated for each token, and supports a context length of 128K tokens. DeepSeek-V2 adopts
    13: innovative architectures including Multi-head Latent Attention (MLA) and DeepSeekMoE.
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 21 | **Candidates:** `21.0B`

```text
    19: DeepSeek-V2 on a high-quality and multi-source corpus consisting of 8.1T tokens, and further
    20: perform Supervised Fine-Tuning (SFT) and Reinforcement Learning (RL) to fully unlock its
>>> 21: potential. Evaluation results show that, even with only 21B activated parameters, DeepSeek-V2
    22: and its chat versions still achieve top-tier performance among open-source models. The model
    23: checkpoints are available at https://github.com/deepseek-ai/DeepSeek-V2.
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 212 | **Candidates:** `16.0B`

```text
    210: A Contributions and Acknowledgments
    211: 
>>> 212: B DeepSeek-V2-Lite: A 16B Model Equipped with MLA and DeepSeekMoE
    213: 
    214: 2
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 337 | **Candidates:** `21.0B, 236.0B`

```text
    335: problem, we introduce DeepSeek-V2, a strong open-source Mixture-of-Experts (MoE) language
    336: model, characterized by economical training and efficient inference through an innovative
>>> 337: Transformer architecture. It is equipped with a total of 236B parameters, of which 21B are
    338: activated for each token, and supports a context length of 128K tokens.
    339: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 371 | **Candidates:** `21.0B`

```text
    369: We evaluate DeepSeek-V2 on a wide range of benchmarks in English and Chinese, and
    370: compare it with representative open-source models. Evaluation results show that even with only
>>> 371: 21B activated parameters, DeepSeek-V2 still achieves top-tier performance among open-source
    372: models and becomes the strongest open-source MoE language model. Figure 1(a) highlights
    373: that, on MMLU, DeepSeek-V2 achieves top-ranking performance with only a small number
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 374 | **Candidates:** `67.0B`

```text
    372: models and becomes the strongest open-source MoE language model. Figure 1(a) highlights
    373: that, on MMLU, DeepSeek-V2 achieves top-ranking performance with only a small number
>>> 374: of activated parameters. In addition, as shown in Figure 1(b), compared with DeepSeek 67B,
    375: DeepSeek-V2 saves 42.5% of training costs, reduces the KV cache by 93.3%, and boosts the
    376: maximum generation throughput to 5.76 times. We also evaluate DeepSeek-V2 Chat (SFT) and
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 395 | **Candidates:** `2.4B, 15.7B`

```text
    393: In order to facilitate further research and development on MLA and DeepSeekMoE, we also
    394: release DeepSeek-V2-Lite, a smaller model equipped with MLA and DeepSeekMoE, for the
>>> 395: open-source community. It has a total of 15.7B parameters, where 2.4B are activated for each
    396: token. Detailed descriptions about DeepSeek-V2-Lite can be found in Appendix B.
    397: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1056 | **Candidates:** `21.0B`

```text
    1054: bottlenecks (i.e., the compressed latent vectors and the intermediate hidden states of routed
    1055: experts) to ensure stable training. Under this configuration, DeepSeek-V2 comprises 236B total
>>> 1056: parameters, of which 21B are activated for each token.
    1057: 
    1058: Training Hyper-Parameters. We employ the AdamW optimizer (Loshchilov and Hutter, 2017)
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1190 | **Candidates:** `22.0B, 70.0B`

```text
    1188: In Table 2, we compare DeepSeek-V2 with several representative open-source models, includ-
    1189: ing DeepSeek 67B (DeepSeek-AI, 2024) (our previous release), Qwen1.5 72B (Bai et al., 2023),
>>> 1190: LLaMA3 70B (AI@Meta, 2024), and Mixtral 8x22B (Mistral, 2024). We evaluate all these models
    1191: with our internal evaluation framework, and ensure that they share the same evaluation setting.
    1192: Overall, with only 21B activated parameters, DeepSeek-V2 significantly outperforms DeepSeek
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1192 | **Candidates:** `21.0B`

```text
    1190: LLaMA3 70B (AI@Meta, 2024), and Mixtral 8x22B (Mistral, 2024). We evaluate all these models
    1191: with our internal evaluation framework, and ensure that they share the same evaluation setting.
>>> 1192: Overall, with only 21B activated parameters, DeepSeek-V2 significantly outperforms DeepSeek
    1193: 67B on almost all benchmarks, and achieves top-tier performance among open-source models.
    1194: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1193 | **Candidates:** `67.0B`

```text
    1191: with our internal evaluation framework, and ensure that they share the same evaluation setting.
    1192: Overall, with only 21B activated parameters, DeepSeek-V2 significantly outperforms DeepSeek
>>> 1193: 67B on almost all benchmarks, and achieves top-tier performance among open-source models.
    1194: 
    1195: Further, we elaborately compare DeepSeek-V2 with its open-source counterparts one by
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1196 | **Candidates:** `72.0B`

```text
    1194: 
    1195: Further, we elaborately compare DeepSeek-V2 with its open-source counterparts one by
>>> 1196: one. (1) Compared with Qwen1.5 72B, another model that supports both Chinese and English,
    1197: DeepSeek-V2 demonstrates overwhelming advantages on the majority of English, code, and
    1198: math benchmarks. As for Chinese benchmarks, Qwen1.5 72B shows better performance on
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1482 | **Candidates:** `21.0B`

```text
    1480: models are evaluated in our internal framework and share the same evaluation setting. Bold
    1481: denotes the best and underline denotes the second-best. Scores with a gap smaller than 0.3
>>> 1482: are regarded as at the same level. With only 21B activated parameters, DeepSeek-V2 achieves
    1483: top-tier performance among open-source models.
    1484: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1497 | **Candidates:** `70.0B`

```text
    1495: English capabilities with LLaMA3 70B. However, even with much fewer training tokens and
    1496: activated parameters, DeepSeek-V2 still demonstrates comparable code and math capability
>>> 1497: with LLaMA3 70B. Also, as a bilingual language model, DeepSeek-V2 outperforms LLaMA3
    1498: 
    1499: 15
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1512 | **Candidates:** `67.0B`

```text
    1510: Training Costs. Since DeepSeek-V2 activates fewer parameters for each token and requires
    1511: fewer FLOPs than DeepSeek 67B, training DeepSeek-V2 will be more economical than training
>>> 1512: DeepSeek 67B theoretically. Although training an MoE model will introduce additional commu-
    1513: nication overheads, through our operator and communication optimizations, the training for
    1514: DeepSeek-V2 can attain a relatively high Model FLOPs Utilization (MFU). During our practical
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1693 | **Candidates:** `22.0B`

```text
    1691: V2 Chat (SFT) demonstrates slightly lower scores than Qwen1.5 72B Chat on multi-subject
    1692: multiple-choice tasks, consistent with the performance observed from their base versions. When
>>> 1693: compared with the state-of-the-art open-source MoE model, Mixtral 8x22B Instruct, DeepSeek-
    1694: V2 Chat (SFT) exhibits better performance on most benchmarks, except for NaturalQuestions
    1695: and IFEval. Furthermore, in comparison to the state-of-the-art open-source model LLaMA3 70B
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1695 | **Candidates:** `70.0B`

```text
    1693: compared with the state-of-the-art open-source MoE model, Mixtral 8x22B Instruct, DeepSeek-
    1694: V2 Chat (SFT) exhibits better performance on most benchmarks, except for NaturalQuestions
>>> 1695: and IFEval. Furthermore, in comparison to the state-of-the-art open-source model LLaMA3 70B
    1696: Chat, DeepSeek-V2 Chat (SFT) shows similar performance in code and math related benchmarks.
    1697: LLaMA3 70B Chat exhibits better performance on MMLU and IFEval, while DeepSeek-V2 Chat
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1963 | **Candidates:** `70.0B`

```text
    1961: Table 3 | Comparison among DeepSeek-V2 Chat (SFT), DeepSeek-V2 Chat (RL), and other
    1962: representative open-source chat models. Regarding TriviaQA and NaturalQuestions, it is
>>> 1963: worth noting that chat models, such as LLaMA3 70B Instruct, might not strictly adhere to the
    1964: format constraints typically specified in the few-shot setting. Consequently, this can lead to
    1965: underestimation of certain models in our evaluation framework.
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2404 | **Candidates:** `21.0B`

```text
    2402: stronger performance, and meanwhile saves 42.5% of training costs, reduces the KV cache
    2403: by 93.3%, and boosts the maximum generation throughput to 5.76 times. Evaluation results
>>> 2404: further demonstrate that with only 21B activated parameters, DeepSeek-V2 achieves top-tier
    2405: performance among open-source models and becomes the strongest open-source MoE model.
    2406: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2923 | **Candidates:** `16.0B`

```text
    2921: 
    2922: 
>>> 2923: B. DeepSeek-V2-Lite: A 16B Model Equipped with MLA and DeepSeekMoE
    2924: 
    2925: B.1. Model Description
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2934 | **Candidates:** `15.7B`

```text
    2932: Each MoE layer consists of 2 shared experts and 64 routed experts, where the intermediate
    2933: hidden dimension of each expert is 1408. Among the routed experts, 6 experts will be activated
>>> 2934: for each token. Under this configuration, DeepSeek-V2-Lite comprises 15.7B total parameters, of
    2935: which 2.4B are activated for each token.
    2936: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3357 | **Candidates:** `7.0B`

```text
    3355: D.1. Ablation of MHA, GQA, and MQA
    3356: 
>>> 3357: We show the evaluation results for 7B dense models with MHA, GQA, and MQA on four hard
    3358: benchmarks in Table 8. All of these three models are trained on 1.33T tokens, and share the same
    3359: architecture except for the attention mechanisms. In addition, for a fair comparison, we align
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3360 | **Candidates:** `7.0B`

```text
    3358: benchmarks in Table 8. All of these three models are trained on 1.33T tokens, and share the same
    3359: architecture except for the attention mechanisms. In addition, for a fair comparison, we align
>>> 3360: the number of parameters of them to around 7B by adjusting the number of layers. From the
    3361: table, we can find that MHA demonstrates significant advantages over GQA and MQA on these
    3362: benchmarks.
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3368 | **Candidates:** `16.0B`

```text
    3366: In Table 9, we show the evaluation results for MoE models equipped with MLA and MHA,
    3367: respectively, on four hard benchmarks. For a solid conclusion, we train and evaluate models
>>> 3368: across two scales. Two small MoE models comprise about 16B total parameters, and we train
    3369: them on 1.33T tokens. Two large MoE models comprise about 250B total parameters, and we
    3370: train them on 420B tokens. Also, two small MoE models and two large MoE models respectively
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3369 | **Candidates:** `250.0B`

```text
    3367: respectively, on four hard benchmarks. For a solid conclusion, we train and evaluate models
    3368: across two scales. Two small MoE models comprise about 16B total parameters, and we train
>>> 3369: them on 1.33T tokens. Two large MoE models comprise about 250B total parameters, and we
    3370: train them on 420B tokens. Also, two small MoE models and two large MoE models respectively
    3371: share the same architecture except for the attention mechanisms. From the table, we can observe
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3423 | **Candidates:** `7.0B`

```text
    3421: 43.5
    3422: 
>>> 3423: Table 8 | Comparison among 7B dense models with MHA, GQA, and MQA, respectively. MHA
    3424: demonstrates significant advantages over GQA and MQA on hard benchmarks.
    3425: 
```

---

