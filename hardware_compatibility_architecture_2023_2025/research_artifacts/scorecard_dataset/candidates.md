# Inspection Report: Candidate Parameters

**Generated:** 2025-12-09 22:48:57

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
**Line:** 16 | **Candidates:** `67.0B`

```text
    14: MLA guarantees efficient inference through significantly compressing the Key-Value (KV) cache
    15: into a latent vector, while DeepSeekMoE enables training strong models at an economical
>>> 16: cost through sparse computation. Compared with DeepSeek 67B, DeepSeek-V2 achieves
    17: significantly stronger performance, and meanwhile saves 42.5% of training costs, reduces the
    18: KV cache by 93.3%, and boosts the maximum generation throughput to 5.76 times. We pretrain
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
**Line:** 69 | **Candidates:** `67.0B`

```text
    67: 
    68: Figure 1 | (a) MMLU accuracy vs. activated parameters, among different open-source models.
>>> 69: (b) Training costs and inference efficiency of DeepSeek 67B (Dense) and DeepSeek-V2.
    70: 
    71: 020406080100Activated Parameters (Billions)556065707580Performance (MMLU)DeepSeek-V2DeepSeek 67BLLaMA 1 33BLLaMA 1 65BLLaMA 2 13BLLaMA 2 34BLLaMA 2 70BLLaMA 3 8BLLaMA 3 70BMistral 7BMixtral 8x7BMixtral 8x22BCommand RCommand R+Grok-1DBRXQwen1.5 32BQwen1.5 72BLLaMA 1 FamilyLLaMA 2 FamilyLLaMA 3 FamilyMixtral FamilyCommand R FamilyQwen1.5 Family050100150200250300DeepSeek-V2DeepSeek 67Bsaving 42.5% oftraining costsTraining Costs (K GPU Hours/T Tokens)0100200300400DeepSeek-V2DeepSeek 67Breducing KV cache by 93.3%KV Cache for Generation (KB/Token)01000020000300004000050000DeepSeek-V2DeepSeek 67B576% of maximum throughputMaximum Generation Throughput (Tokens/Sec)
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 71 | **Candidates:** `7.0B, 8.0B, 13.0B, 22.0B, 32.0B, 33.0B, 34.0B, 65.0B, 67.0B, 70.0B, 72.0B`

```text
    69: (b) Training costs and inference efficiency of DeepSeek 67B (Dense) and DeepSeek-V2.
    70: 
>>> 71: 020406080100Activated Parameters (Billions)556065707580Performance (MMLU)DeepSeek-V2DeepSeek 67BLLaMA 1 33BLLaMA 1 65BLLaMA 2 13BLLaMA 2 34BLLaMA 2 70BLLaMA 3 8BLLaMA 3 70BMistral 7BMixtral 8x7BMixtral 8x22BCommand RCommand R+Grok-1DBRXQwen1.5 32BQwen1.5 72BLLaMA 1 FamilyLLaMA 2 FamilyLLaMA 3 FamilyMixtral FamilyCommand R FamilyQwen1.5 Family050100150200250300DeepSeek-V2DeepSeek 67Bsaving 42.5% oftraining costsTraining Costs (K GPU Hours/T Tokens)0100200300400DeepSeek-V2DeepSeek 67Breducing KV cache by 93.3%KV Cache for Generation (KB/Token)01000020000300004000050000DeepSeek-V2DeepSeek 67B576% of maximum throughputMaximum Generation Throughput (Tokens/Sec)
    72: 
    73: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 82 | **Candidates:** `0.002B`

```text
    80: 2 Architecture
    81: 
>>> 82: 2.1 Multi-Head Latent Attention: Boosting Inference Efficiency . . . . . . . . . . . . .
    83: 
    84: 2.1.1 Preliminaries: Standard Multi-Head Attention . . . . . . . . . . . . . . . .
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 94 | **Candidates:** `2.1B`

```text
    92: 2.2 DeepSeekMoE: Training Strong Models at Economical Costs . . . . . . . . . . . .
    93: 
>>> 94: 2.2.1 Basic Architecture
    95: 
    96: . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
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
**Line:** 277 | **Candidates:** `0.001B`

```text
    275: 
    276: 
>>> 277: B.1 Model Description .
    278: 
    279: .
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
**Line:** 361 | **Candidates:** `67.0B`

```text
    359: 
    360: We construct a high-quality and multi-source pre-training corpus consisting of 8.1T tokens.
>>> 361: Compared with the corpus used in DeepSeek 67B (our previous release) (DeepSeek-AI, 2024), this
    362: corpus features an extended amount of data, especially Chinese data, and higher data quality. We
    363: first pretrain DeepSeek-V2 on the full pre-training corpus. Then, we collect 1.5M conversational
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 363 | **Candidates:** `0.002B`

```text
    361: Compared with the corpus used in DeepSeek 67B (our previous release) (DeepSeek-AI, 2024), this
    362: corpus features an extended amount of data, especially Chinese data, and higher data quality. We
>>> 363: first pretrain DeepSeek-V2 on the full pre-training corpus. Then, we collect 1.5M conversational
    364: sessions, which encompass various domains such as math, code, writing, reasoning, safety, and
    365: more, to perform Supervised Fine-Tuning (SFT) for DeepSeek-V2 Chat (SFT). Finally, we follow
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
**Line:** 423 | **Candidates:** `67.0B`

```text
    421: and DeepSeekMoE in this section. For other tiny details (e.g., layer normalization and the
    422: activation function in FFNs), unless specifically stated, DeepSeek-V2 follows the settings of
>>> 423: DeepSeek 67B (DeepSeek-AI, 2024).
    424: 
    425: 2.1. Multi-Head Latent Attention: Boosting Inference Efficiency
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 597 | **Candidates:** `67.0B`

```text
    595: 2.1.3. Decoupled Rotary Position Embedding
    596: 
>>> 597: Following DeepSeek 67B (DeepSeek-AI, 2024), we intend to use the Rotary Position Embed-
    598: ding (RoPE) (Su et al., 2024) for DeepSeek-V2. However, RoPE is incompatible with low-rank
    599: KV compression. To be specific, RoPE is position-sensitive for both keys and queries. If we apply
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 838 | **Candidates:** `2.0B`

```text
    836: 
    837: 
>>> 838: For DeepSeek-V2, beyond the naive top-K selection of routed experts, we additionally ensure
    839: that the target experts of each token will be distributed on at most 𝑀 devices. To be specific, for
    840: each token, we first select 𝑀 devices that have experts with the highest affinity scores in them.
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1018 | **Candidates:** `67.0B`

```text
    1016: 3.1.1. Data Construction
    1017: 
>>> 1018: While maintaining the same data processing stages as for DeepSeek 67B (DeepSeek-AI, 2024),
    1019: we extend the amount of data and elevate the data quality. In order to enlarge our pre-training
    1020: corpus, we explore the potential of the internet data and optimize our cleaning processes, thus
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1034 | **Candidates:** `67.0B`

```text
    1032: 
    1033: 
>>> 1034: We adopt the same tokenizer as used in DeepSeek 67B, which is built based on the Byte-level
    1035: Byte-Pair Encoding (BBPE) algorithm and has a vocabulary size of 100K. Our tokenized pre-
    1036: training corpus contains 8.1T tokens, where Chinese tokens are approximately 12% more than
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1055 | **Candidates:** `236.0B`

```text
    1053: layers after the compressed latent vectors, and multiply additional scaling factors at the width
    1054: bottlenecks (i.e., the compressed latent vectors and the intermediate hidden states of routed
>>> 1055: experts) to ensure stable training. Under this configuration, DeepSeek-V2 comprises 236B total
    1056: parameters, of which 21B are activated for each token.
    1057: 
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
**Line:** 1133 | **Candidates:** `2.0B`

```text
    1131: 13
    1132: 
>>> 1133: 1K12K24K35K47K58K70K81K93K104K116K128KContext Length (#Tokens)09182736455564738291100Document Depth Percent (%)Pressure Testing DeepSeek-V2 Base 128K Context via "Needle In A HayStack"12345678910Score
    1134: in our HAI-LLM framework. Included benchmarks are categorized and listed as follows, where
    1135: underlined benchmarks are in Chinese:
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1189 | **Candidates:** `67.0B, 72.0B`

```text
    1187: 
    1188: In Table 2, we compare DeepSeek-V2 with several representative open-source models, includ-
>>> 1189: ing DeepSeek 67B (DeepSeek-AI, 2024) (our previous release), Qwen1.5 72B (Bai et al., 2023),
    1190: LLaMA3 70B (AI@Meta, 2024), and Mixtral 8x22B (Mistral, 2024). We evaluate all these models
    1191: with our internal evaluation framework, and ensure that they share the same evaluation setting.
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
**Line:** 1198 | **Candidates:** `72.0B`

```text
    1196: one. (1) Compared with Qwen1.5 72B, another model that supports both Chinese and English,
    1197: DeepSeek-V2 demonstrates overwhelming advantages on the majority of English, code, and
>>> 1198: math benchmarks. As for Chinese benchmarks, Qwen1.5 72B shows better performance on
    1199: 
    1200: 14
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1279 | **Candidates:** `0.002B`

```text
    1277: 0-shot
    1278: 
>>> 1279: DeepSeek Qwen1.5 Mixtral LLaMA 3
    1280: 
    1281: 67B
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1281 | **Candidates:** `67.0B`

```text
    1279: DeepSeek Qwen1.5 Mixtral LLaMA 3
    1280: 
>>> 1281: 67B
    1282: 
    1283: Dense
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1284 | **Candidates:** `67.0B`

```text
    1282: 
    1283: Dense
>>> 1284: 67B
    1285: 67B
    1286: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1285 | **Candidates:** `67.0B`

```text
    1283: Dense
    1284: 67B
>>> 1285: 67B
    1286: 
    1287: 0.642
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1319 | **Candidates:** `72.0B`

```text
    1317: 88.5
    1318: 
>>> 1319: 72B
    1320: 
    1321: 8x22B
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1321 | **Candidates:** `22.0B`

```text
    1319: 72B
    1320: 
>>> 1321: 8x22B
    1322: 
    1323: 70B
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1323 | **Candidates:** `70.0B`

```text
    1321: 8x22B
    1322: 
>>> 1323: 70B
    1324: 
    1325: Dense
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1326 | **Candidates:** `72.0B`

```text
    1324: 
    1325: Dense
>>> 1326: 72B
    1327: 72B
    1328: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1327 | **Candidates:** `72.0B`

```text
    1325: Dense
    1326: 72B
>>> 1327: 72B
    1328: 
    1329: 0.637
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1362 | **Candidates:** `39.0B`

```text
    1360: 
    1361: MoE
>>> 1362: 39B
    1363: 141B
    1364: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1363 | **Candidates:** `141.0B`

```text
    1361: MoE
    1362: 39B
>>> 1363: 141B
    1364: 
    1365: 0.623
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1398 | **Candidates:** `70.0B`

```text
    1396: 
    1397: Dense
>>> 1398: 70B
    1399: 70B
    1400: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1399 | **Candidates:** `70.0B`

```text
    1397: Dense
    1398: 70B
>>> 1399: 70B
    1400: 
    1401: 0.602
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1444 | **Candidates:** `21.0B`

```text
    1442: 
    1443: MoE
>>> 1444: 21B
    1445: 236B
    1446: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1445 | **Candidates:** `236.0B`

```text
    1443: MoE
    1444: 21B
>>> 1445: 236B
    1446: 
    1447: 0.606
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
**Line:** 1486 | **Candidates:** `72.0B`

```text
    1484: 
    1485: multi-subject multiple-choice tasks while DeepSeek-V2 is comparable or better on others. Note
>>> 1486: that for the CHID benchmark, the tokenizer of Qwen1.5 72B will encounter errors in our
    1487: evaluation framework, so we leave the CHID score blank for Qwen1.5 72B. (2) Compared with
    1488: Mixtral 8x22B, DeepSeek-V2 achieves comparable or better English performance, except for
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1487 | **Candidates:** `72.0B`

```text
    1485: multi-subject multiple-choice tasks while DeepSeek-V2 is comparable or better on others. Note
    1486: that for the CHID benchmark, the tokenizer of Qwen1.5 72B will encounter errors in our
>>> 1487: evaluation framework, so we leave the CHID score blank for Qwen1.5 72B. (2) Compared with
    1488: Mixtral 8x22B, DeepSeek-V2 achieves comparable or better English performance, except for
    1489: TriviaQA, NaturalQuestions, and HellaSwag, which are closely related to English commonsense
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1488 | **Candidates:** `22.0B`

```text
    1486: that for the CHID benchmark, the tokenizer of Qwen1.5 72B will encounter errors in our
    1487: evaluation framework, so we leave the CHID score blank for Qwen1.5 72B. (2) Compared with
>>> 1488: Mixtral 8x22B, DeepSeek-V2 achieves comparable or better English performance, except for
    1489: TriviaQA, NaturalQuestions, and HellaSwag, which are closely related to English commonsense
    1490: knowledge. Notably, DeepSeek-V2 outperforms Mixtral 8x22B on MMLU. On code and math
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1490 | **Candidates:** `22.0B`

```text
    1488: Mixtral 8x22B, DeepSeek-V2 achieves comparable or better English performance, except for
    1489: TriviaQA, NaturalQuestions, and HellaSwag, which are closely related to English commonsense
>>> 1490: knowledge. Notably, DeepSeek-V2 outperforms Mixtral 8x22B on MMLU. On code and math
    1491: benchmarks, DeepSeek-V2 demonstrates comparable performance with Mixtral 8x22B. Since
    1492: Mixtral 8x22B is not specifically trained on Chinese data, its Chinese capability lags far behind
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1491 | **Candidates:** `22.0B`

```text
    1489: TriviaQA, NaturalQuestions, and HellaSwag, which are closely related to English commonsense
    1490: knowledge. Notably, DeepSeek-V2 outperforms Mixtral 8x22B on MMLU. On code and math
>>> 1491: benchmarks, DeepSeek-V2 demonstrates comparable performance with Mixtral 8x22B. Since
    1492: Mixtral 8x22B is not specifically trained on Chinese data, its Chinese capability lags far behind
    1493: DeepSeek-V2. (3) Compared with LLaMA3 70B, DeepSeek-V2 is trained on fewer than a quarter
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1492 | **Candidates:** `22.0B`

```text
    1490: knowledge. Notably, DeepSeek-V2 outperforms Mixtral 8x22B on MMLU. On code and math
    1491: benchmarks, DeepSeek-V2 demonstrates comparable performance with Mixtral 8x22B. Since
>>> 1492: Mixtral 8x22B is not specifically trained on Chinese data, its Chinese capability lags far behind
    1493: DeepSeek-V2. (3) Compared with LLaMA3 70B, DeepSeek-V2 is trained on fewer than a quarter
    1494: of English tokens. Therefore, we acknowledge that DeepSeek-V2 still has a slight gap in basic
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1493 | **Candidates:** `70.0B`

```text
    1491: benchmarks, DeepSeek-V2 demonstrates comparable performance with Mixtral 8x22B. Since
    1492: Mixtral 8x22B is not specifically trained on Chinese data, its Chinese capability lags far behind
>>> 1493: DeepSeek-V2. (3) Compared with LLaMA3 70B, DeepSeek-V2 is trained on fewer than a quarter
    1494: of English tokens. Therefore, we acknowledge that DeepSeek-V2 still has a slight gap in basic
    1495: English capabilities with LLaMA3 70B. However, even with much fewer training tokens and
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1495 | **Candidates:** `70.0B`

```text
    1493: DeepSeek-V2. (3) Compared with LLaMA3 70B, DeepSeek-V2 is trained on fewer than a quarter
    1494: of English tokens. Therefore, we acknowledge that DeepSeek-V2 still has a slight gap in basic
>>> 1495: English capabilities with LLaMA3 70B. However, even with much fewer training tokens and
    1496: activated parameters, DeepSeek-V2 still demonstrates comparable code and math capability
    1497: with LLaMA3 70B. Also, as a bilingual language model, DeepSeek-V2 outperforms LLaMA3
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
**Line:** 1502 | **Candidates:** `70.0B`

```text
    1500: 
    1501: 
>>> 1502: 70B overwhelmingly on Chinese benchmarks.
    1503: 
    1504: Finally, it is worth mentioning that certain prior studies (Hu et al., 2024) incorporate SFT
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1511 | **Candidates:** `67.0B`

```text
    1509: 
    1510: Training Costs. Since DeepSeek-V2 activates fewer parameters for each token and requires
>>> 1511: fewer FLOPs than DeepSeek 67B, training DeepSeek-V2 will be more economical than training
    1512: DeepSeek 67B theoretically. Although training an MoE model will introduce additional commu-
    1513: nication overheads, through our operator and communication optimizations, the training for
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
**Line:** 1515 | **Candidates:** `67.0B`

```text
    1513: nication overheads, through our operator and communication optimizations, the training for
    1514: DeepSeek-V2 can attain a relatively high Model FLOPs Utilization (MFU). During our practical
>>> 1515: training on the H800 cluster, for training on each trillion tokens, DeepSeek 67B requires 300.6K
    1516: GPU hours, while DeepSeek-V2 needs only 172.8K GPU hours, i.e., sparse DeepSeek-V2 can
    1517: save 42.5% training costs compared with dense DeepSeek 67B.
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1517 | **Candidates:** `67.0B`

```text
    1515: training on the H800 cluster, for training on each trillion tokens, DeepSeek 67B requires 300.6K
    1516: GPU hours, while DeepSeek-V2 needs only 172.8K GPU hours, i.e., sparse DeepSeek-V2 can
>>> 1517: save 42.5% training costs compared with dense DeepSeek 67B.
    1518: 
    1519: Inference Efficiency.
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1523 | **Candidates:** `6.0B`

```text
    1521: its parameters into the precision of FP8. In addition, we also perform KV cache quantiza-
    1522: tion (Hooper et al., 2024; Zhao et al., 2023) for DeepSeek-V2 to further compress each element
>>> 1523: in its KV cache into 6 bits on average. Benefiting from MLA and these optimizations, actually
    1524: deployed DeepSeek-V2 requires significantly less KV cache than DeepSeek 67B, and thus can
    1525: serve a much larger batch size. We evaluate the generation throughput of DeepSeek-V2 based
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1524 | **Candidates:** `67.0B`

```text
    1522: tion (Hooper et al., 2024; Zhao et al., 2023) for DeepSeek-V2 to further compress each element
    1523: in its KV cache into 6 bits on average. Benefiting from MLA and these optimizations, actually
>>> 1524: deployed DeepSeek-V2 requires significantly less KV cache than DeepSeek 67B, and thus can
    1525: serve a much larger batch size. We evaluate the generation throughput of DeepSeek-V2 based
    1526: on the prompt and generation length distribution from the actually deployed DeepSeek 67B
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1525 | **Candidates:** `2.0B`

```text
    1523: in its KV cache into 6 bits on average. Benefiting from MLA and these optimizations, actually
    1524: deployed DeepSeek-V2 requires significantly less KV cache than DeepSeek 67B, and thus can
>>> 1525: serve a much larger batch size. We evaluate the generation throughput of DeepSeek-V2 based
    1526: on the prompt and generation length distribution from the actually deployed DeepSeek 67B
    1527: service. On a single node with 8 H800 GPUs, DeepSeek-V2 achieves a generation throughput
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1526 | **Candidates:** `67.0B`

```text
    1524: deployed DeepSeek-V2 requires significantly less KV cache than DeepSeek 67B, and thus can
    1525: serve a much larger batch size. We evaluate the generation throughput of DeepSeek-V2 based
>>> 1526: on the prompt and generation length distribution from the actually deployed DeepSeek 67B
    1527: service. On a single node with 8 H800 GPUs, DeepSeek-V2 achieves a generation throughput
    1528: exceeding 50K tokens per second, which is 5.76 times the maximum generation throughput of
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1529 | **Candidates:** `67.0B`

```text
    1527: service. On a single node with 8 H800 GPUs, DeepSeek-V2 achieves a generation throughput
    1528: exceeding 50K tokens per second, which is 5.76 times the maximum generation throughput of
>>> 1529: DeepSeek 67B. In addition, the prompt input throughput of DeepSeek-V2 exceeds 100K tokens
    1530: per second.
    1531: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1537 | **Candidates:** `0.0B, 0.001B, 0.002B`

```text
    1535: 
    1536: Building upon our prior research (DeepSeek-AI, 2024), we curate our instruction tuning datasets
>>> 1537: to include 1.5M instances, comprising 1.2M instances for helpfulness and 0.3M instances for
    1538: safety. In comparison to the initial version, we improve the data quality to mitigate hallucinatory
    1539: responses and enhance writing proficiency. We fine-tune DeepSeek-V2 with 2 epochs, and
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1548 | **Candidates:** `22.0B, 70.0B, 72.0B`

```text
    1546: our model on open-ended conversation benchmarks including MT-Bench (Zheng et al., 2023),
    1547: AlpacaEval 2.0 (Dubois et al., 2024), and AlignBench (Liu et al., 2023). For comparison, we also
>>> 1548: evaluate Qwen1.5 72B Chat, LLaMA-3-70B Instruct, and Mistral-8x22B Instruct in our evaluation
    1549: framework and settings. As for DeepSeek 67B Chat, we directly refer to the evaluation results
    1550: reported in our previous release.
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1549 | **Candidates:** `67.0B`

```text
    1547: AlpacaEval 2.0 (Dubois et al., 2024), and AlignBench (Liu et al., 2023). For comparison, we also
    1548: evaluate Qwen1.5 72B Chat, LLaMA-3-70B Instruct, and Mistral-8x22B Instruct in our evaluation
>>> 1549: framework and settings. As for DeepSeek 67B Chat, we directly refer to the evaluation results
    1550: reported in our previous release.
    1551: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1689 | **Candidates:** `72.0B`

```text
    1687: 
    1688: As for the comparisons with other models, we first compare DeepSeek-V2 Chat (SFT)
>>> 1689: with Qwen1.5 72B Chat, and find that DeepSeek-V2 Chat (SFT) surpasses Qwen1.5 72B Chat
    1690: on almost all of English, math, and code benchmarks. On Chinese benchmarks, DeepSeek-
    1691: V2 Chat (SFT) demonstrates slightly lower scores than Qwen1.5 72B Chat on multi-subject
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1691 | **Candidates:** `72.0B`

```text
    1689: with Qwen1.5 72B Chat, and find that DeepSeek-V2 Chat (SFT) surpasses Qwen1.5 72B Chat
    1690: on almost all of English, math, and code benchmarks. On Chinese benchmarks, DeepSeek-
>>> 1691: V2 Chat (SFT) demonstrates slightly lower scores than Qwen1.5 72B Chat on multi-subject
    1692: multiple-choice tasks, consistent with the performance observed from their base versions. When
    1693: compared with the state-of-the-art open-source MoE model, Mixtral 8x22B Instruct, DeepSeek-
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
**Line:** 1697 | **Candidates:** `70.0B`

```text
    1695: and IFEval. Furthermore, in comparison to the state-of-the-art open-source model LLaMA3 70B
    1696: Chat, DeepSeek-V2 Chat (SFT) shows similar performance in code and math related benchmarks.
>>> 1697: LLaMA3 70B Chat exhibits better performance on MMLU and IFEval, while DeepSeek-V2 Chat
    1698: (SFT) showcases stronger performance on Chinese tasks. Ultimately, DeepSeek-V2 Chat (RL)
    1699: demonstrates further enhanced performance in both mathematical and coding tasks compared
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1709 | **Candidates:** `22.0B, 72.0B`

```text
    1707: DeepSeek-V2 Chat (SFT). This outcome showcases the effectiveness of our RL training in achiev-
    1708: ing improved alignment. In comparison to other open-source models, DeepSeek-V2 Chat (RL)
>>> 1709: demonstrates superior performance over Mistral 8x22B Instruct and Qwen1.5 72B Chat on both
    1710: benchmarks. When compared with LLaMA3 70B Instruct, DeepSeek-V2 Chat (RL) showcases
    1711: competitive performance on MT-Bench and notably outperforms it on AlpacaEval 2.0. These
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1710 | **Candidates:** `70.0B`

```text
    1708: ing improved alignment. In comparison to other open-source models, DeepSeek-V2 Chat (RL)
    1709: demonstrates superior performance over Mistral 8x22B Instruct and Qwen1.5 72B Chat on both
>>> 1710: benchmarks. When compared with LLaMA3 70B Instruct, DeepSeek-V2 Chat (RL) showcases
    1711: competitive performance on MT-Bench and notably outperforms it on AlpacaEval 2.0. These
    1712: results highlight the strong performance of DeepSeek-V2 Chat (RL) in generating high-quality
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1727 | **Candidates:** `0.003B`

```text
    1725: # Shots
    1726: 
>>> 1727: DeepSeek Qwen 1.5 LLaMA3 Mixtral DeepSeek-V2 DeepSeek-V2
    1728: 67B Chat 72B Chat 70B Inst. 8x22B Inst. Chat (SFT)
    1729: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1728 | **Candidates:** `22.0B, 67.0B, 70.0B, 72.0B`

```text
    1726: 
    1727: DeepSeek Qwen 1.5 LLaMA3 Mixtral DeepSeek-V2 DeepSeek-V2
>>> 1728: 67B Chat 72B Chat 70B Inst. 8x22B Inst. Chat (SFT)
    1729: 
    1730: Chat (RL)
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1742 | **Candidates:** `67.0B`

```text
    1740: 4K
    1741: Dense
>>> 1742: 67B
    1743: 67B
    1744: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1743 | **Candidates:** `67.0B`

```text
    1741: Dense
    1742: 67B
>>> 1743: 67B
    1744: 
    1745: 32K
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1747 | **Candidates:** `72.0B`

```text
    1745: 32K
    1746: Dense
>>> 1747: 72B
    1748: 72B
    1749: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1748 | **Candidates:** `72.0B`

```text
    1746: Dense
    1747: 72B
>>> 1748: 72B
    1749: 
    1750: 8K
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1752 | **Candidates:** `70.0B`

```text
    1750: 8K
    1751: Dense
>>> 1752: 70B
    1753: 70B
    1754: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1753 | **Candidates:** `70.0B`

```text
    1751: Dense
    1752: 70B
>>> 1753: 70B
    1754: 
    1755: TriviaQA
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1879 | **Candidates:** `39.0B`

```text
    1877: 64K
    1878: MoE
>>> 1879: 39B
    1880: 141B
    1881: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1880 | **Candidates:** `141.0B`

```text
    1878: MoE
    1879: 39B
>>> 1880: 141B
    1881: 
    1882: 80.0
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1907 | **Candidates:** `21.0B`

```text
    1905: 128K
    1906: MoE
>>> 1907: 21B
    1908: 236B
    1909: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1908 | **Candidates:** `236.0B`

```text
    1906: MoE
    1907: 21B
>>> 1908: 236B
    1909: 
    1910: 85.4
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1935 | **Candidates:** `21.0B`

```text
    1933: 128K
    1934: MoE
>>> 1935: 21B
    1936: 236B
    1937: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1936 | **Candidates:** `236.0B`

```text
    1934: MoE
    1935: 21B
>>> 1936: 236B
    1937: 
    1938: 86.7
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
**Line:** 1971 | **Candidates:** `67.0B`

```text
    1969: MT-Bench AlpacaEval 2.0
    1970: 
>>> 1971: DeepSeek 67B Chat
    1972: Mistral 8x22B Instruct v0.1
    1973: Qwen1.5 72B Chat
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1972 | **Candidates:** `22.0B`

```text
    1970: 
    1971: DeepSeek 67B Chat
>>> 1972: Mistral 8x22B Instruct v0.1
    1973: Qwen1.5 72B Chat
    1974: LLaMA3 70B Instruct
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1973 | **Candidates:** `72.0B`

```text
    1971: DeepSeek 67B Chat
    1972: Mistral 8x22B Instruct v0.1
>>> 1973: Qwen1.5 72B Chat
    1974: LLaMA3 70B Instruct
    1975: DeepSeek-V2 Chat (SFT)
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1974 | **Candidates:** `70.0B`

```text
    1972: Mistral 8x22B Instruct v0.1
    1973: Qwen1.5 72B Chat
>>> 1974: LLaMA3 70B Instruct
    1975: DeepSeek-V2 Chat (SFT)
    1976: DeepSeek-V2 Chat (RL)
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1995 | **Candidates:** `72.0B`

```text
    1993: controlled win rate as the metric.
    1994: 
>>> 1995: 72B Chat on both Chinese reasoning and language. Moreover, both DeepSeek-V2 Chat (SFT)
    1996: and DeepSeek-V2 Chat (RL) outperform GPT-4-0613 and ERNIEBot 4.0, solidifying the position
    1997: of our models in the top-tier LLMs that support Chinese. Specifically, DeepSeek-V2 Chat (RL)
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2061 | **Candidates:** `72.0B`

```text
    2059: Moonshot-v1-32k-202404*（月之暗面） 7.22
    2060: 7.19
>>> 2061: Qwen1.5-72B-Chat*
    2062: 6.43
    2063: DeepSeek-67B-Chat
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2063 | **Candidates:** `67.0B`

```text
    2061: Qwen1.5-72B-Chat*
    2062: 6.43
>>> 2063: DeepSeek-67B-Chat
    2064: ChatGLM-Turbo（智谱清言）
    2065: 6.24
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2069 | **Candidates:** `34.0B`

```text
    2067: 6.14
    2068: 6.12
>>> 2069: Yi-34B-Chat*
    2070: 6.08
    2071: GPT-3.5-Turbo-0613
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2077 | **Candidates:** `14.0B`

```text
    2075: 5.74
    2076: 5.72
>>> 2077: Qwen-14B-Chat
    2078: 5.25
    2079: Baichuan2-13B-Chat
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2079 | **Candidates:** `13.0B`

```text
    2077: Qwen-14B-Chat
    2078: 5.25
>>> 2079: Baichuan2-13B-Chat
    2080: 4.97
    2081: ChatGLM3-6B
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2081 | **Candidates:** `6.0B`

```text
    2079: Baichuan2-13B-Chat
    2080: 4.97
>>> 2081: ChatGLM3-6B
    2082: 4.97
    2083: Baichuan2-7B-Chat
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2083 | **Candidates:** `7.0B`

```text
    2081: ChatGLM3-6B
    2082: 4.97
>>> 2083: Baichuan2-7B-Chat
    2084: 4.96
    2085: InternLM-20B
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2085 | **Candidates:** `20.0B`

```text
    2083: Baichuan2-7B-Chat
    2084: 4.96
>>> 2085: InternLM-20B
    2086: 4.91
    2087: Qwen-7B-Chat
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2087 | **Candidates:** `7.0B`

```text
    2085: InternLM-20B
    2086: 4.91
>>> 2087: Qwen-7B-Chat
    2088: 4.48
    2089: ChatGLM2-6B
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2089 | **Candidates:** `6.0B`

```text
    2087: Qwen-7B-Chat
    2088: 4.48
>>> 2089: ChatGLM2-6B
    2090: 3.65
    2091: InternLM-Chat-7B
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2091 | **Candidates:** `7.0B`

```text
    2089: ChatGLM2-6B
    2090: 3.65
>>> 2091: InternLM-Chat-7B
    2092: 3.57
    2093: Chinese-LLaMA-2-7B-Chat
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2093 | **Candidates:** `7.0B`

```text
    2091: InternLM-Chat-7B
    2092: 3.57
>>> 2093: Chinese-LLaMA-2-7B-Chat
    2094: 3.35
    2095: LLaMA-2-13B-Chinese-Chat
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2095 | **Candidates:** `13.0B`

```text
    2093: Chinese-LLaMA-2-7B-Chat
    2094: 3.35
>>> 2095: LLaMA-2-13B-Chinese-Chat
    2096: 
    2097: 7.73
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2401 | **Candidates:** `67.0B`

```text
    2399: In addition to strong performance, it is also characterized by economical
    2400: training and efficient inference, benefiting from its innovative architecture including MLA and
>>> 2401: DeepSeekMoE. In practice, compared with DeepSeek 67B, DeepSeek-V2 achieves significantly
    2402: stronger performance, and meanwhile saves 42.5% of training costs, reduces the KV cache
    2403: by 93.3%, and boosts the maximum generation throughput to 5.76 times. Evaluation results
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
**Line:** 2432 | **Candidates:** `0.003B`

```text
    2430: References
    2431: 
>>> 2432: AI@Meta. Llama 3 model card, 2024. URL https://github.com/meta-llama/llama3/bl
    2433: 
    2434: ob/main/MODEL_CARD.md.
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2508 | **Candidates:** `2.019B`

```text
    2506: T. Solorio, editors, Proceedings of the 2019 Conference of the North American Chapter of the
    2507: Association for Computational Linguistics: Human Language Technologies, NAACL-HLT
>>> 2508: 2019, Minneapolis, MN, USA, June 2-7, 2019, Volume 1 (Long and Short Papers), pages 2368–
    2509: 2378. Association for Computational Linguistics, 2019. doi: 10.18653/V1/N19-1246. URL
    2510: https://doi.org/10.18653/v1/n19-1246.
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2547 | **Candidates:** `0.01B`

```text
    2545: 
    2546: C. Hooper, S. Kim, H. Mohammadzadeh, M. W. Mahoney, Y. S. Shao, K. Keutzer, and A. Gholami.
>>> 2547: Kvquant: Towards 10 million context length LLM inference with KV cache quantization. CoRR,
    2548: abs/2401.18079, 2024. URL https://doi.org/10.48550/arXiv.2401.18079.
    2549: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2614 | **Candidates:** `22.0B`

```text
    2612: Mistral. Cheaper, better, faster, stronger: Continuing to push the frontier of ai and making it
    2613: 
>>> 2614: accessible to all, 2024. URL https://mistral.ai/news/mixtral-8x22b.
    2615: 
    2616: OpenAI. Introducing ChatGPT, 2022. URL https://openai.com/blog/chatgpt.
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2696 | **Candidates:** `2020.0B`

```text
    2694: nese language understanding evaluation benchmark. In D. Scott, N. Bel, and C. Zong, editors,
    2695: Proceedings of the 28th International Conference on Computational Linguistics, COLING
>>> 2696: 2020, Barcelona, Spain (Online), December 8-13, 2020, pages 4762–4772. International Com-
    2697: mittee on Computational Linguistics, 2020. doi: 10.18653/V1/2020.COLING-MAIN.419. URL
    2698: https://doi.org/10.18653/v1/2020.coling-main.419.
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2917 | **Candidates:** `2.0B`

```text
    2915: and Wangding Zeng have made key innovations in the research of the MLA architecture.
    2916: Furthermore, we’d like to thank Jianlin Su for his helpful discussion on position embedding.
>>> 2917: We thank all those who have contributed to DeepSeek-V2 but are not mentioned in the paper.
    2918: DeepSeek believes that innovation, novelty, and curiosity are essential in the path to AGI.
    2919: 
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
**Line:** 2929 | **Candidates:** `512.0B`

```text
    2927: Architectures. DeepSeek-V2-Lite has 27 layers and a hidden dimension of 2048. It also employs
    2928: MLA and has 16 attention heads, where each head has a dimension of 128. Its KV compression
>>> 2929: dimension is 512, but slightly different from DeepSeek-V2, it does not compress the queries.
    2930: For the decoupled queries and key, it has a per-head dimension of 64. DeepSeek-V2-Lite also
    2931: employs DeepSeekMoE, and all FFNs except for the first layer are replaced with MoE layers.
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
**Line:** 2935 | **Candidates:** `2.4B`

```text
    2933: hidden dimension of each expert is 1408. Among the routed experts, 6 experts will be activated
    2934: for each token. Under this configuration, DeepSeek-V2-Lite comprises 15.7B total parameters, of
>>> 2935: which 2.4B are activated for each token.
    2936: 
    2937: Benchmark
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2939 | **Candidates:** `7.0B, 16.0B`

```text
    2937: Benchmark
    2938: 
>>> 2939: DeepSeek 7B DeepSeekMoE 16B DeepSeek-V2-Lite
    2940: 
    2941: Architecture
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2949 | **Candidates:** `6.9B`

```text
    2947: MHA+Dense
    2948: 4K
>>> 2949: 6.9B
    2950: 6.9B
    2951: 2T
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2950 | **Candidates:** `6.9B`

```text
    2948: 4K
    2949: 6.9B
>>> 2950: 6.9B
    2951: 2T
    2952: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2955 | **Candidates:** `2.8B`

```text
    2953: MHA+MoE
    2954: 4K
>>> 2955: 2.8B
    2956: 16.4B
    2957: 2T
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2956 | **Candidates:** `16.4B`

```text
    2954: 4K
    2955: 2.8B
>>> 2956: 16.4B
    2957: 2T
    2958: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2961 | **Candidates:** `2.4B`

```text
    2959: MLA+MoE
    2960: 32K
>>> 2961: 2.4B
    2962: 15.7B
    2963: 5.7T
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2962 | **Candidates:** `15.7B`

```text
    2960: 32K
    2961: 2.4B
>>> 2962: 15.7B
    2963: 5.7T
    2964: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3049 | **Candidates:** `7.0B, 16.0B`

```text
    3047: 64.3
    3048: 
>>> 3049: Table 6 | Performance of DeepSeek-V2-Lite, DeepSeekMoE 16B, and DeepSeek 7B.
    3050: 
    3051: Training Details. DeepSeek-V2-Lite is also trained from scratch on the same pre-training
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3075 | **Candidates:** `7.0B`

```text
    3073: DeepSeek DeepSeekMoE DeepSeek-V2-Lite
    3074: 
>>> 3075: 7B Chat
    3076: 
    3077: 16B Chat
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3077 | **Candidates:** `16.0B`

```text
    3075: 7B Chat
    3076: 
>>> 3077: 16B Chat
    3078: 
    3079: Chat
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3117 | **Candidates:** `6.9B`

```text
    3115: 
    3116: 4K
>>> 3117: 6.9B
    3118: 6.9B
    3119: 2T
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3118 | **Candidates:** `6.9B`

```text
    3116: 4K
    3117: 6.9B
>>> 3118: 6.9B
    3119: 2T
    3120: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3141 | **Candidates:** `2.8B`

```text
    3139: 
    3140: 4K
>>> 3141: 2.8B
    3142: 16.4B
    3143: 2T
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3142 | **Candidates:** `16.4B`

```text
    3140: 4K
    3141: 2.8B
>>> 3142: 16.4B
    3143: 2T
    3144: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3166 | **Candidates:** `2.4B`

```text
    3164: MLA+MoE
    3165: 32K
>>> 3166: 2.4B
    3167: 15.7B
    3168: 5.7T
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3167 | **Candidates:** `15.7B`

```text
    3165: 32K
    3166: 2.4B
>>> 3167: 15.7B
    3168: 5.7T
    3169: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3189 | **Candidates:** `7.0B, 16.0B`

```text
    3187: 62.5
    3188: 
>>> 3189: Table 7 | Performance of DeepSeek-V2-Lite Chat, DeepSeekMoE 16B Chat, and DeepSeek 7B
    3190: Chat.
    3191: 
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
**Line:** 3383 | **Candidates:** `7.0B`

```text
    3381: # Shots
    3382: 
>>> 3383: Dense 7B
    3384: Dense 7B
    3385: Dense 7B
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3384 | **Candidates:** `7.0B`

```text
    3382: 
    3383: Dense 7B
>>> 3384: Dense 7B
    3385: Dense 7B
    3386: w/ MQA w/ GQA (8 Groups) w/ MHA
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3385 | **Candidates:** `7.0B`

```text
    3383: Dense 7B
    3384: Dense 7B
>>> 3385: Dense 7B
    3386: w/ MQA w/ GQA (8 Groups) w/ MHA
    3387: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3402 | **Candidates:** `7.1B`

```text
    3400: 5-shot
    3401: 
>>> 3402: 7.1B
    3403: 
    3404: 33.2
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3409 | **Candidates:** `6.9B`

```text
    3407: 34.6
    3408: 
>>> 3409: 6.9B
    3410: 
    3411: 35.6
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3416 | **Candidates:** `6.9B`

```text
    3414: 38.4
    3415: 
>>> 3416: 6.9B
    3417: 
    3418: 37.0
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

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3458 | **Candidates:** `2.5B`

```text
    3456: 5-shot
    3457: 
>>> 3458: 2.5B
    3459: 15.8B
    3460: 110.6K
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3459 | **Candidates:** `15.8B`

```text
    3457: 
    3458: 2.5B
>>> 3459: 15.8B
    3460: 110.6K
    3461: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3467 | **Candidates:** `2.4B`

```text
    3465: 52.3
    3466: 
>>> 3467: 2.4B
    3468: 15.7B
    3469: 15.6K
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3468 | **Candidates:** `15.7B`

```text
    3466: 
    3467: 2.4B
>>> 3468: 15.7B
    3469: 15.6K
    3470: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3476 | **Candidates:** `25.0B`

```text
    3474: 53.4
    3475: 
>>> 3476: 25.0B
    3477: 250.8B
    3478: 860.2K
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3477 | **Candidates:** `250.8B`

```text
    3475: 
    3476: 25.0B
>>> 3477: 250.8B
    3478: 860.2K
    3479: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3485 | **Candidates:** `21.5B`

```text
    3483: 60.7
    3484: 
>>> 3485: 21.5B
    3486: 247.4B
    3487: 34.6K
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3486 | **Candidates:** `247.4B`

```text
    3484: 
    3485: 21.5B
>>> 3486: 247.4B
    3487: 34.6K
    3488: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3504 | **Candidates:** `22.0B`

```text
    3502: slightly worse on the test sets that are closely associated with specific regional cultures. For
    3503: example, when evaluated on MMLU, although DeepSeek-V2 achieves comparable or superior
>>> 3504: performance on the majority of testsets compared with its competitors like Mixtral 8x22B, it still
    3505: lags behind on the Humanity-Moral subset, which is mainly associated with American values.
    3506: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3508 | **Candidates:** `0.42B`

```text
    3506: 
    3507: Further, we conduct a manual analysis on this subset. Three well-educated human annotators
>>> 3508: conduct independent annotations on 420 moral scenarios from the MMLU Humanity-Moral
    3509: subset. Then, we compute the agreement among their annotations and the ground-truth label. As
    3510: shown in Table 10, three human annotators and the ground-truth label exhibit a low agreement
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3554 | **Candidates:** `0.42B`

```text
    3552: 100.0%
    3553: 
>>> 3554: Table 10 | Three well-educated human annotators conduct independent annotations on 420 moral
    3555: scenarios from the MMLU Humanity-Moral subset, on which DeepSeek-V2 and its competitive
    3556: models demonstrate performance inconsistency. Three annotators and the ground-truth label
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3569 | **Candidates:** `110.0B`

```text
    3567: DeepSeek-V2 Chat (RL)
    3568: Ernie-bot 4.0
>>> 3569: Qwen-110B-Chat
    3570: GLM-4
    3571: Xinghuo 3.5
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3572 | **Candidates:** `72.0B`

```text
    3570: GLM-4
    3571: Xinghuo 3.5
>>> 3572: Qwen-72B-Chat
    3573: ChatGLM-Turbo
    3574: GPT-3.5-Turbo
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3575 | **Candidates:** `14.0B`

```text
    3573: ChatGLM-Turbo
    3574: GPT-3.5-Turbo
>>> 3575: Qwen-14B-Chat
    3576: ChatGLM3-6B
    3577: Xinghuo 3.0
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3576 | **Candidates:** `6.0B`

```text
    3574: GPT-3.5-Turbo
    3575: Qwen-14B-Chat
>>> 3576: ChatGLM3-6B
    3577: Xinghuo 3.0
    3578: Baichuan2-13B-Chat
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3578 | **Candidates:** `13.0B`

```text
    3576: ChatGLM3-6B
    3577: Xinghuo 3.0
>>> 3578: Baichuan2-13B-Chat
    3579: Ernie-3.5-turbo
    3580: Chinese-Alpaca2-13B
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3580 | **Candidates:** `13.0B`

```text
    3578: Baichuan2-13B-Chat
    3579: Ernie-3.5-turbo
>>> 3580: Chinese-Alpaca2-13B
    3581: 
    3582: 5
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3654 | **Candidates:** `0.006B`

```text
    3652: 18.58
    3653: 
>>> 3654: Table 11 | SC-Math6 Model Reasoning Level. “R Level” stands for Reasoning Level, “Comp.
    3655: Score” stands for Comprehensive Score, “Reas. Steps Score” stands for Reasoning Steps Score,
    3656: and “OvrAcc Score” stands for Overall Accuracy Score.
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3685 | **Candidates:** `22.0B, 67.0B, 70.0B, 72.0B`

```text
    3683: 34
    3684: 
>>> 3685: 657075808590HumanEval (Pass@1)15202530354045LiveCodeBench (Pass@1)DeepSeek-V2-Chat-RLDeepSeek 67BMixtral 8x22BMistral LargeQwen MaxQwen1.5 72BGPT-4-Turbo-1106GPT-4-0613Claude OpusClaude SonnetClaude HaikuLLaMA3-70B-Chat
    3686: PROMPT
    3687: Question: A sample in a cylindrical container has a cylindrical shape and a
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4037 | **Candidates:** `0.04B`

```text
    4035: 
    4036: PROMPT
>>> 4037: Q: Max can mow the lawn in 40 minutes. If it takes him twice that long to
    4038: fertilize the lawn, how long will it take him to both mow and fertilize the lawn?
    4039: A: Let’s think step by step. It takes Max 2 * 40 minutes = 80 minutes to fertilize
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4039 | **Candidates:** `0.04B, 0.08B`

```text
    4037: Q: Max can mow the lawn in 40 minutes. If it takes him twice that long to
    4038: fertilize the lawn, how long will it take him to both mow and fertilize the lawn?
>>> 4039: A: Let’s think step by step. It takes Max 2 * 40 minutes = 80 minutes to fertilize
    4040: the lawn. In total, Max takes 80 minutes + 40 minutes = 120 minutes to both
    4041: mow and fertilize the lawn. The answer is 120.
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4040 | **Candidates:** `0.04B, 0.08B, 0.12B`

```text
    4038: fertilize the lawn, how long will it take him to both mow and fertilize the lawn?
    4039: A: Let’s think step by step. It takes Max 2 * 40 minutes = 80 minutes to fertilize
>>> 4040: the lawn. In total, Max takes 80 minutes + 40 minutes = 120 minutes to both
    4041: mow and fertilize the lawn. The answer is 120.
    4042: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4055 | **Candidates:** `4.0B, 14.0B`

```text
    4053: years old. So, Tim is 17 - 5 = 12 years younger than Jenny. The answer is 12.
    4054: 
>>> 4055: Q: The school has 14 boys and 10 girls. If 4 boys and 3 girls drop out, how
    4056: many boys and girls are left?
    4057: A: Let’s think step by step. There are 14 boys - 4 boys = 10 boys left. There are
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4057 | **Candidates:** `4.0B, 10.0B, 14.0B`

```text
    4055: Q: The school has 14 boys and 10 girls. If 4 boys and 3 girls drop out, how
    4056: many boys and girls are left?
>>> 4057: A: Let’s think step by step. There are 14 boys - 4 boys = 10 boys left. There are
    4058: 10 girls - 3 girls = 7 girls left. In total there are 10 boys + 7 girls = 17 boys and
    4059: girls left. The answer is 17.
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4058 | **Candidates:** `10.0B, 17.0B`

```text
    4056: many boys and girls are left?
    4057: A: Let’s think step by step. There are 14 boys - 4 boys = 10 boys left. There are
>>> 4058: 10 girls - 3 girls = 7 girls left. In total there are 10 boys + 7 girls = 17 boys and
    4059: girls left. The answer is 17.
    4060: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4062 | **Candidates:** `4.0B`

```text
    4060: 
    4061: Q: Building one birdhouse requires 7 planks and 20 nails. If 1 nail costs 0.05,
>>> 4062: and one plank costs 3, what is the cost, in dollars, to build 4 birdhouses?
    4063: A: Let’s think step by step. The cost of the planks for one birdhouse is 7 * 3 =
    4064: 21. And the nails are a cost of 20 * 0.05 = 1 for each birdhouse. So to build one
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4065 | **Candidates:** `4.0B`

```text
    4063: A: Let’s think step by step. The cost of the planks for one birdhouse is 7 * 3 =
    4064: 21. And the nails are a cost of 20 * 0.05 = 1 for each birdhouse. So to build one
>>> 4065: birdhouse one will need 21 + 1 = 22. So the cost of building 4 birdhouses is at 4
    4066: * 22 = 88. The answer is 88.
    4067: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4077 | **Candidates:** `0.027B`

```text
    4075: 
    4076: Q: Angela is a bike messenger in New York. She needs to deliver 8 times
>>> 4077: as many packages as meals. If she needs to deliver 27 meals and packages
    4078: combined, how many meals does she deliver?
    4079: A: Let’s think step by step. Let p be the number of packages Angela delivers and
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4080 | **Candidates:** `0.008B`

```text
    4078: combined, how many meals does she deliver?
    4079: A: Let’s think step by step. Let p be the number of packages Angela delivers and
>>> 4080: m be the number of meals. We know that p + m = 27 and p = 8m. Substituting
    4081: the second equation into the first equation, we get 8m + m = 27. Combining
    4082: like terms, we get 9m = 27. Dividing both sides by 9, we get m = 3. The answer
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4081 | **Candidates:** `0.008B`

```text
    4079: A: Let’s think step by step. Let p be the number of packages Angela delivers and
    4080: m be the number of meals. We know that p + m = 27 and p = 8m. Substituting
>>> 4081: the second equation into the first equation, we get 8m + m = 27. Combining
    4082: like terms, we get 9m = 27. Dividing both sides by 9, we get m = 3. The answer
    4083: is 3.
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4082 | **Candidates:** `0.009B`

```text
    4080: m be the number of meals. We know that p + m = 27 and p = 8m. Substituting
    4081: the second equation into the first equation, we get 8m + m = 27. Combining
>>> 4082: like terms, we get 9m = 27. Dividing both sides by 9, we get m = 3. The answer
    4083: is 3.
    4084: 
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4091 | **Candidates:** `0.004B`

```text
    4089: years old. The answer is 19.
    4090: 
>>> 4091: Q: Indras has 6 letters in her name. Her sister’s name has 4 more letters than
    4092: half of the letters in Indras’ name. How many letters are in Indras and her
    4093: sister’s names?
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4362 | **Candidates:** `0.003B`

```text
    4360: Do you know how many kinds of earthworms there are?There are about 1800
    4361: kinds in the world! They can be brown,purple,green.They can be as small as 3
>>> 4362: cm long and as large as 3 m long.
    4363: The best time to see earthworms is at night,especially a cool,damp night.That’s
    4364: when they come up from their burrows to hunt for food.Earthworms don’t
```

---

### File: `DeepSeek_V2_V3_R1_reports_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4427 | **Candidates:** `1966.0B`

```text
    4425: A: Muumi
    4426: Q: "What English model, with her short-haired androgynous look, born Lesley
>>> 4427: Hornby, was discovered in 1966 by Nigel Davies when she was 16 and weighed
    4428: 6 stone (41 kg, 91 lbs), and became ""The Face of ’66"" with her high fashion
    4429: mod look created by Mary Quant?"
```

---

