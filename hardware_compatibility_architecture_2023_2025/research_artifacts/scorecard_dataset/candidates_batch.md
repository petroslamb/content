# Inspection Report: Candidate Parameters

**Generated:** 2025-12-09 23:45:10

## ID: A4
### File: `Hochreiter_1997_https_arxiv_org_abs_1406_1078_1406.1078.md`
**Line:** 217 | **Candidates:** `1.0B`

```text
    215: quence by predicting the next symbol yt given the
    216: hidden state h(cid:104)t(cid:105). However, unlike the RNN de-
>>> 217: scribed in Sec. 2.1, both yt and h(cid:104)t(cid:105) are also con-
    218: ditioned on yt−1 and on the summary c of the input
    219: sequence. Hence, the hidden state of the decoder
```

---

### File: `Hochreiter_1997_https_arxiv_org_abs_1406_1078_1406.1078.md`
**Line:** 659 | **Candidates:** `0.005B, 0.421B`

```text
    657: of the WMT’14 translation task. The bilingual
    658: corpora include Europarl (61M words), news com-
>>> 659: mentary (5.5M), UN (421M), and two crawled
    660: corpora of 90M and 780M words respectively.
    661: The last two corpora are quite noisy. To train
```

---

### File: `Hochreiter_1997_https_arxiv_org_abs_1406_1078_1406.1078.md`
**Line:** 660 | **Candidates:** `0.09B`

```text
    658: corpora include Europarl (61M words), news com-
    659: mentary (5.5M), UN (421M), and two crawled
>>> 660: corpora of 90M and 780M words respectively.
    661: The last two corpora are quite noisy. To train
    662: the French language model, about 712M words of
```

---

### File: `Hochreiter_1997_https_arxiv_org_abs_1406_1078_1406.1078.md`
**Line:** 680 | **Candidates:** `0.348B`

```text
    678: selected a subset of 418M words out of more
    679: than 2G words for language modeling and a
>>> 680: subset of 348M out of 850M words for train-
    681: ing the RNN Encoder–Decoder. We used the
    682: test set newstest2012 and 2013 for data
```

---

### File: `Hochreiter_1997_https_arxiv_org_abs_1406_1078_1406.1078.md`
**Line:** 740 | **Candidates:** `0.1B`

```text
    738: neural networks.
    739: 
>>> 740: similarly. We used rank-100 matrices, equivalent
    741: to learning an embedding of dimension 100 for
    742: each word. The activation function used for ˜h in
```

---

### File: `Hochreiter_1997_https_arxiv_org_abs_1406_1078_1406.1078.md`
**Line:** 747 | **Candidates:** `0.5B`

```text
    745: the output is implemented as a deep neural net-
    746: work (Pascanu et al., 2014) with a single interme-
>>> 747: diate layer having 500 maxout units each pooling
    748: 2 inputs (Goodfellow et al., 2013).
    749: 
```

---

### File: `Hochreiter_1997_https_arxiv_org_abs_1406_1078_1406.1078.md`
**Line:** 1248 | **Candidates:** `1.155B`

```text
    1246: Pascal Vincent, and Christian Janvin. 2003. A neu-
    1247: ral probabilistic language model. J. Mach. Learn.
>>> 1248: Res., 3:1137–1155, March.
    1249: 
    1250: [Bengio et al.2013] Y.
```

---

## ID: A5
### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 51 | **Candidates:** `7.0B`

```text
    49: Abstract
    50: 
>>> 51: We introduce Mixtral 8x7B, a Sparse Mixture of Experts (SMoE) language
    52: model. Mixtral has the same architecture as Mistral 7B, with the difference
    53: that each layer is composed of 8 feedforward blocks (i.e. experts). For every
```

---

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
**Line:** 59 | **Candidates:** `70.0B`

```text
    57: has access to 47B parameters, but only uses 13B active parameters during
    58: inference. Mixtral was trained with a context size of 32k tokens and it outperforms
>>> 59: or matches Llama 2 70B and GPT-3.5 across all evaluated benchmarks.
    60: In
    61: particular, Mixtral vastly outperforms Llama 2 70B on mathematics, code
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 61 | **Candidates:** `70.0B`

```text
    59: or matches Llama 2 70B and GPT-3.5 across all evaluated benchmarks.
    60: In
>>> 61: particular, Mixtral vastly outperforms Llama 2 70B on mathematics, code
    62: generation, and multilingual benchmarks. We also provide a model fine-
    63: tuned to follow instructions, Mixtral 8x7B – Instruct, that surpasses GPT-3.5
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 63 | **Candidates:** `7.0B`

```text
    61: particular, Mixtral vastly outperforms Llama 2 70B on mathematics, code
    62: generation, and multilingual benchmarks. We also provide a model fine-
>>> 63: tuned to follow instructions, Mixtral 8x7B – Instruct, that surpasses GPT-3.5
    64: Turbo, Claude-2.1, Gemini Pro, and Llama 2 70B – chat model on human bench-
    65: marks. Both the base and instruct models are released under the Apache 2.0 license.
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
**Line:** 75 | **Candidates:** `70.0B`

```text
    73: 
    74: In this paper, we present Mixtral 8x7B, a sparse mixture of experts model (SMoE) with open weights,
>>> 75: licensed under Apache 2.0. Mixtral outperforms Llama 2 70B and GPT-3.5 on most benchmarks. As
    76: it only uses a subset of its parameters for every token, Mixtral allows faster inference speed at low
    77: batch-sizes, and higher throughput at large batch-sizes.
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 86 | **Candidates:** `70.0B`

```text
    84: 
    85: Mixtral is pretrained with multilingual data using a context size of 32k tokens. It either matches
>>> 86: or exceeds the performance of Llama 2 70B and GPT-3.5, over several benchmarks. In particular,
    87: 
    88: 
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 94 | **Candidates:** `70.0B`

```text
    92: 
    93: Mixtral demonstrates superior capabilities in mathematics, code generation, and tasks that require
>>> 94: multilingual understanding, significantly outperforming Llama 2 70B in these domains. Experiments
    95: show that Mixtral is able to successfully retrieve information from its context window of 32k tokens,
    96: regardless of the sequence length and the location of the information in the sequence.
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
**Line:** 103 | **Candidates:** `7.0B`

```text
    101: benchmarks. Mixtral – Instruct also demonstrates reduced biases, and a more balanced sentiment
    102: profile in benchmarks such as BBQ, and BOLD.
>>> 103: We release both Mixtral 8x7B and Mixtral 8x7B – Instruct under the Apache 2.0 license1, free for
    104: academic and commercial usage, ensuring broad accessibility and potential for diverse applications.
    105: To enable the community to run Mixtral with a fully open-source stack, we submitted changes to
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 232 | **Candidates:** `70.0B`

```text
    230: Figure 2: Performance of Mixtral and different Llama models on a wide range of benchmarks. All models
    231: were re-evaluated on all metrics with our evaluation pipeline for accurate comparison. Mixtral outperforms or
>>> 232: matches Llama 2 70B on all benchmarks. In particular, it is vastly superior in mathematics and code generation.
    233: 
    234: 3
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 250 | **Candidates:** `7.0B`

```text
    248: TriQA HumanE MBPP Math GSM8K
    249: 
>>> 250: LLaMA 2 7B
    251: 
    252: 7B
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 252 | **Candidates:** `7.0B`

```text
    250: LLaMA 2 7B
    251: 
>>> 252: 7B
    253: 
    254: 44.4% 77.1% 69.5% 77.9% 68.7% 43.2% 17.5% 56.6% 11.6% 26.1% 3.9% 16.0%
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 256 | **Candidates:** `13.0B`

```text
    254: 44.4% 77.1% 69.5% 77.9% 68.7% 43.2% 17.5% 56.6% 11.6% 26.1% 3.9% 16.0%
    255: 
>>> 256: LLaMA 2 13B
    257: 
    258: LLaMA 1 33B
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 258 | **Candidates:** `33.0B`

```text
    256: LLaMA 2 13B
    257: 
>>> 258: LLaMA 1 33B
    259: 
    260: LLaMA 2 70B
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 260 | **Candidates:** `70.0B`

```text
    258: LLaMA 1 33B
    259: 
>>> 260: LLaMA 2 70B
    261: 
    262: 13B
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 262 | **Candidates:** `13.0B`

```text
    260: LLaMA 2 70B
    261: 
>>> 262: 13B
    263: 
    264: 33B
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 264 | **Candidates:** `33.0B`

```text
    262: 13B
    263: 
>>> 264: 33B
    265: 
    266: 70B
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 266 | **Candidates:** `70.0B`

```text
    264: 33B
    265: 
>>> 266: 70B
    267: 
    268: 55.6% 80.7% 72.9% 80.8% 75.2% 48.8% 16.7% 64.0% 18.9% 35.4% 6.0% 34.3%
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 274 | **Candidates:** `7.0B`

```text
    272: 69.9% 85.4% 80.4% 82.6% 79.9% 56.5% 25.4% 73.0% 29.3% 49.8% 13.8% 69.6%
    273: 
>>> 274: Mistral 7B
    275: 
    276: 7B
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 276 | **Candidates:** `7.0B`

```text
    274: Mistral 7B
    275: 
>>> 276: 7B
    277: 
    278: 62.5% 81.0% 74.2% 82.2% 80.5% 54.9% 23.2% 62.5% 26.2% 50.2% 12.7% 50.0%
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 280 | **Candidates:** `7.0B`

```text
    278: 62.5% 81.0% 74.2% 82.2% 80.5% 54.9% 23.2% 62.5% 26.2% 50.2% 12.7% 50.0%
    279: 
>>> 280: Mixtral 8x7B
    281: 
    282: 13B
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 282 | **Candidates:** `13.0B`

```text
    280: Mixtral 8x7B
    281: 
>>> 282: 13B
    283: 
    284: 70.6% 84.4% 77.2% 83.6% 83.1% 59.7% 30.6% 71.5% 40.2% 60.7% 28.4% 74.4%
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 286 | **Candidates:** `70.0B`

```text
    284: 70.6% 84.4% 77.2% 83.6% 83.1% 59.7% 30.6% 71.5% 40.2% 60.7% 28.4% 74.4%
    285: 
>>> 286: Table 2: Comparison of Mixtral with Llama. Mixtral outperforms or matches Llama 2 70B performance on
    287: almost all popular benchmarks while using 5x fewer active parameters during inference.
    288: 
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 290 | **Candidates:** `7.0B, 13.0B, 70.0B`

```text
    288: 
    289: Figure 3: Results on MMLU, commonsense reasoning, world knowledge and reading comprehension,
>>> 290: math and code for Mistral (7B/8x7B) vs Llama 2 (7B/13B/70B). Mixtral largely outperforms Llama 2 70B
    291: on all benchmarks, except on reading comprehension benchmarks while using 5x lower active parameters. It
    292: is also vastly superior to Llama 2 70B on code and math.
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 292 | **Candidates:** `70.0B`

```text
    290: math and code for Mistral (7B/8x7B) vs Llama 2 (7B/13B/70B). Mixtral largely outperforms Llama 2 70B
    291: on all benchmarks, except on reading comprehension benchmarks while using 5x lower active parameters. It
>>> 292: is also vastly superior to Llama 2 70B on code and math.
    293: 
    294: Detailed results for Mixtral, Mistral 7B and Llama 2 7B/13B/70B and Llama 1 34B2 are reported
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 294 | **Candidates:** `7.0B, 13.0B, 34.0B, 70.0B`

```text
    292: is also vastly superior to Llama 2 70B on code and math.
    293: 
>>> 294: Detailed results for Mixtral, Mistral 7B and Llama 2 7B/13B/70B and Llama 1 34B2 are reported
    295: in Table 2. Figure 2 compares the performance of Mixtral with the Llama models in different
    296: categories. Mixtral surpasses Llama 2 70B across most metrics. In particular, Mixtral displays a
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 296 | **Candidates:** `70.0B`

```text
    294: Detailed results for Mixtral, Mistral 7B and Llama 2 7B/13B/70B and Llama 1 34B2 are reported
    295: in Table 2. Figure 2 compares the performance of Mixtral with the Llama models in different
>>> 296: categories. Mixtral surpasses Llama 2 70B across most metrics. In particular, Mixtral displays a
    297: superior performance in code and mathematics benchmarks.
    298: 
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
**Line:** 307 | **Candidates:** `47.0B, 70.0B`

```text
    305: proportional to the inference compute cost, but does not consider the memory costs and hardware
    306: utilization. The memory costs for serving Mixtral are proportional to its sparse parameter count,
>>> 307: 47B, which is still smaller than Llama 2 70B. As for device utilization, we note that the SMoEs layer
    308: introduces additional overhead due to the routing mechanism and due to the increased memory loads
    309: when running more than one expert per device. They are more suitable for batched workloads where
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 312 | **Candidates:** `7.0B, 70.0B`

```text
    310: one can reach a good degree of arithmetic intensity.
    311: 
>>> 312: Comparison with Llama 2 70B and GPT-3.5. In Table 3, we report the performance of Mixtral 8x7B
    313: compared to Llama 2 70B and GPT-3.5. We observe that Mixtral performs similarly or above the
    314: two other models. On MMLU, Mixtral obtains a better performance, despite its significantly smaller
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 313 | **Candidates:** `70.0B`

```text
    311: 
    312: Comparison with Llama 2 70B and GPT-3.5. In Table 3, we report the performance of Mixtral 8x7B
>>> 313: compared to Llama 2 70B and GPT-3.5. We observe that Mixtral performs similarly or above the
    314: two other models. On MMLU, Mixtral obtains a better performance, despite its significantly smaller
    315: capacity (47B tokens compared to 70B). For MT Bench, we report the performance of the latest
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 315 | **Candidates:** `70.0B`

```text
    313: compared to Llama 2 70B and GPT-3.5. We observe that Mixtral performs similarly or above the
    314: two other models. On MMLU, Mixtral obtains a better performance, despite its significantly smaller
>>> 315: capacity (47B tokens compared to 70B). For MT Bench, we report the performance of the latest
    316: GPT-3.5-Turbo model available, gpt-3.5-turbo-1106.
    317: 
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 318 | **Candidates:** `34.0B`

```text
    316: GPT-3.5-Turbo model available, gpt-3.5-turbo-1106.
    317: 
>>> 318: 2Since Llama 2 34B was not open-sourced, we report results for Llama 1 34B.
    319: 
    320: 4
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 323 | **Candidates:** `70.0B`

```text
    321: 
    322: 
>>> 323: LLaMA 2 70B
    324: 
    325: GPT-3.5
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 327 | **Candidates:** `7.0B`

```text
    325: GPT-3.5
    326: 
>>> 327: Mixtral 8x7B
    328: 
    329: MMLU
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 392 | **Candidates:** `70.0B`

```text
    390: 8.30
    391: 
>>> 392: Table 3: Comparison of Mixtral with Llama 2 70B and GPT-3.5. Mixtral outperforms or matches Llama 2
    393: 70B and GPT-3.5 performance on most metrics.
    394: 
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 393 | **Candidates:** `70.0B`

```text
    391: 
    392: Table 3: Comparison of Mixtral with Llama 2 70B and GPT-3.5. Mixtral outperforms or matches Llama 2
>>> 393: 70B and GPT-3.5 performance on most metrics.
    394: 
    395: Evaluation Differences. On some benchmarks, there are some differences between our evaluation
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 399 | **Candidates:** `0.003B`

```text
    397: on TriviaQA, we do not provide Wikipedia contexts.
    398: 
>>> 399: 3.1 Multilingual benchmarks
    400: 
    401: Compared to Mistral 7B, we significantly upsample the proportion of multilingual data during
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 401 | **Candidates:** `7.0B`

```text
    399: 3.1 Multilingual benchmarks
    400: 
>>> 401: Compared to Mistral 7B, we significantly upsample the proportion of multilingual data during
    402: pretraining. The extra capacity allows Mixtral to perform well on multilingual benchmarks while
    403: maintaining a high accuracy in English. In particular, Mixtral significantly outperforms Llama 2 70B
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 403 | **Candidates:** `70.0B`

```text
    401: Compared to Mistral 7B, we significantly upsample the proportion of multilingual data during
    402: pretraining. The extra capacity allows Mixtral to perform well on multilingual benchmarks while
>>> 403: maintaining a high accuracy in English. In particular, Mixtral significantly outperforms Llama 2 70B
    404: in French, German, Spanish, and Italian, as shown in Table 4.
    405: 
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 423 | **Candidates:** `33.0B`

```text
    421: Arc-c HellaS MMLU
    422: 
>>> 423: LLaMA 1 33B
    424: LLaMA 2 70B
    425: Mixtral 8x7B
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 424 | **Candidates:** `70.0B`

```text
    422: 
    423: LLaMA 1 33B
>>> 424: LLaMA 2 70B
    425: Mixtral 8x7B
    426: 
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 425 | **Candidates:** `7.0B`

```text
    423: LLaMA 1 33B
    424: LLaMA 2 70B
>>> 425: Mixtral 8x7B
    426: 
    427: 33B
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 427 | **Candidates:** `33.0B`

```text
    425: Mixtral 8x7B
    426: 
>>> 427: 33B
    428: 70B
    429: 13B
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 428 | **Candidates:** `70.0B`

```text
    426: 
    427: 33B
>>> 428: 70B
    429: 13B
    430: 
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 429 | **Candidates:** `13.0B`

```text
    427: 33B
    428: 70B
>>> 429: 13B
    430: 
    431: 42.9% 65.4% 49.0%
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 444 | **Candidates:** `70.0B`

```text
    442: 
    443: Table 4: Comparison of Mixtral with Llama on Multilingual Benchmarks. On ARC Challenge, Hellaswag,
>>> 444: and MMLU, Mixtral outperforms Llama 2 70B on 4 languages: French, German, Spanish, and Italian.
    445: 
    446: 3.2 Long range performance
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 462 | **Candidates:** `3.3B`

```text
    460: 
    461: 
>>> 462: 3.3 Bias Benchmarks
    463: 
    464: To identify possible flaws to be corrected
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 480 | **Candidates:** `70.0B`

```text
    478: for bias benchmarking across five domains.
    479: 
>>> 480: Llama 2 70B
    481: 
    482: Mixtral 8x7B
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 482 | **Candidates:** `7.0B`

```text
    480: Llama 2 70B
    481: 
>>> 482: Mixtral 8x7B
    483: 
    484: BBQ accuracy
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 509 | **Candidates:** `70.0B`

```text
    507: 0.232 ± 0.052
    508: 
>>> 509: Figure 5: Bias Benchmarks. Compared Llama 2 70B,
    510: Mixtral presents less bias (higher accuracy on BBQ, lower
    511: std on BOLD) and displays more positive sentiment (higher
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 515 | **Candidates:** `0.002B`

```text
    513: 
    514: We benchmark Llama 2 and Mixtral on BBQ and BOLD with our evaluation framework and report
>>> 515: the results in Table 5. Compared to Llama 2, Mixtral presents less bias on the BBQ benchmark
    516: (56.0% vs 51.5%). For each group in BOLD, a higher average sentiment score means more positive
    517: sentiments and a lower standard deviation indicates less bias within the group. Overall, Mixtral
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 528 | **Candidates:** `70.0B`

```text
    526: score of 8.30 on MT-Bench [33] (see Table 2), making it the best open-weights model as of December
    527: 2023. Independent human evaluation conducted by LMSys is reported in Figure 63 and shows that
>>> 528: Mixtral – Instruct outperforms GPT-3.5-Turbo, Gemini Pro, Claude-2.1, and Llama 2 70B chat.
    529: 
    530: Figure 6: LMSys Leaderboard. (Screenshot from Dec 22, 2023) Mixtral 8x7B Instruct v0.1 achieves an Arena
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 530 | **Candidates:** `7.0B`

```text
    528: Mixtral – Instruct outperforms GPT-3.5-Turbo, Gemini Pro, Claude-2.1, and Llama 2 70B chat.
    529: 
>>> 530: Figure 6: LMSys Leaderboard. (Screenshot from Dec 22, 2023) Mixtral 8x7B Instruct v0.1 achieves an Arena
    531: Elo rating of 1121 outperforming Claude-2.1 (1117), all versions of GPT-3.5-Turbo (1117 best), Gemini Pro
    532: (1111), and Llama-2-70b-chat (1077). Mixtral is currently the best open-weights model by a large margin.
```

---

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 531 | **Candidates:** `1117.0B`

```text
    529: 
    530: Figure 6: LMSys Leaderboard. (Screenshot from Dec 22, 2023) Mixtral 8x7B Instruct v0.1 achieves an Arena
>>> 531: Elo rating of 1121 outperforming Claude-2.1 (1117), all versions of GPT-3.5-Turbo (1117 best), Gemini Pro
    532: (1111), and Llama-2-70b-chat (1077). Mixtral is currently the best open-weights model by a large margin.
    533: 
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
**Line:** 675 | **Candidates:** `7.0B`

```text
    673: 6 Conclusion
    674: 
>>> 675: In this paper, we introduced Mixtral 8x7B, the first mixture-of-experts network to reach a state-of-the-
    676: art performance among open-source models. Mixtral 8x7B Instruct outperforms Claude-2.1, Gem-
    677: ini Pro, and GPT-3.5 Turbo on human evaluation benchmarks. Because it only uses two experts at each
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

### File: `Mistral_MoE_report_https_arxiv_org_abs_2401_04088_2401.04088.md`
**Line:** 773 | **Candidates:** `7.0B`

```text
    771: [18] Albert Q Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh
    772: Chaplot, Diego de las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile
>>> 773: Saulnier, et al. Mistral 7b. arXiv preprint arXiv:2310.06825, 2023.
    774: 
    775: [19] Mandar Joshi, Eunsol Choi, Daniel S Weld, and Luke Zettlemoyer. Triviaqa: A large
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
**Line:** 16 | **Candidates:** `67.0B`

```text
    14: MLA guarantees efficient inference through significantly compressing the Key-Value (KV) cache
    15: into a latent vector, while DeepSeekMoE enables training strong models at an economical
>>> 16: cost through sparse computation. Compared with DeepSeek 67B, DeepSeek-V2 achieves
    17: significantly stronger performance, and meanwhile saves 42.5% of training costs, reduces the
    18: KV cache by 93.3%, and boosts the maximum generation throughput to 5.76 times. We pretrain
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
**Line:** 69 | **Candidates:** `67.0B`

```text
    67: 
    68: Figure 1 | (a) MMLU accuracy vs. activated parameters, among different open-source models.
>>> 69: (b) Training costs and inference efficiency of DeepSeek 67B (Dense) and DeepSeek-V2.
    70: 
    71: 020406080100Activated Parameters (Billions)556065707580Performance (MMLU)DeepSeek-V2DeepSeek 67BLLaMA 1 33BLLaMA 1 65BLLaMA 2 13BLLaMA 2 34BLLaMA 2 70BLLaMA 3 8BLLaMA 3 70BMistral 7BMixtral 8x7BMixtral 8x22BCommand RCommand R+Grok-1DBRXQwen1.5 32BQwen1.5 72BLLaMA 1 FamilyLLaMA 2 FamilyLLaMA 3 FamilyMixtral FamilyCommand R FamilyQwen1.5 Family050100150200250300DeepSeek-V2DeepSeek 67Bsaving 42.5% oftraining costsTraining Costs (K GPU Hours/T Tokens)0100200300400DeepSeek-V2DeepSeek 67Breducing KV cache by 93.3%KV Cache for Generation (KB/Token)01000020000300004000050000DeepSeek-V2DeepSeek 67B576% of maximum throughputMaximum Generation Throughput (Tokens/Sec)
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 71 | **Candidates:** `7.0B, 8.0B, 13.0B, 22.0B, 32.0B, 33.0B, 34.0B, 65.0B, 67.0B, 70.0B, 72.0B`

```text
    69: (b) Training costs and inference efficiency of DeepSeek 67B (Dense) and DeepSeek-V2.
    70: 
>>> 71: 020406080100Activated Parameters (Billions)556065707580Performance (MMLU)DeepSeek-V2DeepSeek 67BLLaMA 1 33BLLaMA 1 65BLLaMA 2 13BLLaMA 2 34BLLaMA 2 70BLLaMA 3 8BLLaMA 3 70BMistral 7BMixtral 8x7BMixtral 8x22BCommand RCommand R+Grok-1DBRXQwen1.5 32BQwen1.5 72BLLaMA 1 FamilyLLaMA 2 FamilyLLaMA 3 FamilyMixtral FamilyCommand R FamilyQwen1.5 Family050100150200250300DeepSeek-V2DeepSeek 67Bsaving 42.5% oftraining costsTraining Costs (K GPU Hours/T Tokens)0100200300400DeepSeek-V2DeepSeek 67Breducing KV cache by 93.3%KV Cache for Generation (KB/Token)01000020000300004000050000DeepSeek-V2DeepSeek 67B576% of maximum throughputMaximum Generation Throughput (Tokens/Sec)
    72: 
    73: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 82 | **Candidates:** `0.002B`

```text
    80: 2 Architecture
    81: 
>>> 82: 2.1 Multi-Head Latent Attention: Boosting Inference Efficiency . . . . . . . . . . . . .
    83: 
    84: 2.1.1 Preliminaries: Standard Multi-Head Attention . . . . . . . . . . . . . . . .
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 94 | **Candidates:** `2.1B`

```text
    92: 2.2 DeepSeekMoE: Training Strong Models at Economical Costs . . . . . . . . . . . .
    93: 
>>> 94: 2.2.1 Basic Architecture
    95: 
    96: . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
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
**Line:** 277 | **Candidates:** `0.001B`

```text
    275: 
    276: 
>>> 277: B.1 Model Description .
    278: 
    279: .
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
**Line:** 361 | **Candidates:** `67.0B`

```text
    359: 
    360: We construct a high-quality and multi-source pre-training corpus consisting of 8.1T tokens.
>>> 361: Compared with the corpus used in DeepSeek 67B (our previous release) (DeepSeek-AI, 2024), this
    362: corpus features an extended amount of data, especially Chinese data, and higher data quality. We
    363: first pretrain DeepSeek-V2 on the full pre-training corpus. Then, we collect 1.5M conversational
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 363 | **Candidates:** `0.002B`

```text
    361: Compared with the corpus used in DeepSeek 67B (our previous release) (DeepSeek-AI, 2024), this
    362: corpus features an extended amount of data, especially Chinese data, and higher data quality. We
>>> 363: first pretrain DeepSeek-V2 on the full pre-training corpus. Then, we collect 1.5M conversational
    364: sessions, which encompass various domains such as math, code, writing, reasoning, safety, and
    365: more, to perform Supervised Fine-Tuning (SFT) for DeepSeek-V2 Chat (SFT). Finally, we follow
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
**Line:** 423 | **Candidates:** `67.0B`

```text
    421: and DeepSeekMoE in this section. For other tiny details (e.g., layer normalization and the
    422: activation function in FFNs), unless specifically stated, DeepSeek-V2 follows the settings of
>>> 423: DeepSeek 67B (DeepSeek-AI, 2024).
    424: 
    425: 2.1. Multi-Head Latent Attention: Boosting Inference Efficiency
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 597 | **Candidates:** `67.0B`

```text
    595: 2.1.3. Decoupled Rotary Position Embedding
    596: 
>>> 597: Following DeepSeek 67B (DeepSeek-AI, 2024), we intend to use the Rotary Position Embed-
    598: ding (RoPE) (Su et al., 2024) for DeepSeek-V2. However, RoPE is incompatible with low-rank
    599: KV compression. To be specific, RoPE is position-sensitive for both keys and queries. If we apply
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 838 | **Candidates:** `2.0B`

```text
    836: 
    837: 
>>> 838: For DeepSeek-V2, beyond the naive top-K selection of routed experts, we additionally ensure
    839: that the target experts of each token will be distributed on at most 𝑀 devices. To be specific, for
    840: each token, we first select 𝑀 devices that have experts with the highest affinity scores in them.
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1018 | **Candidates:** `67.0B`

```text
    1016: 3.1.1. Data Construction
    1017: 
>>> 1018: While maintaining the same data processing stages as for DeepSeek 67B (DeepSeek-AI, 2024),
    1019: we extend the amount of data and elevate the data quality. In order to enlarge our pre-training
    1020: corpus, we explore the potential of the internet data and optimize our cleaning processes, thus
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1034 | **Candidates:** `67.0B`

```text
    1032: 
    1033: 
>>> 1034: We adopt the same tokenizer as used in DeepSeek 67B, which is built based on the Byte-level
    1035: Byte-Pair Encoding (BBPE) algorithm and has a vocabulary size of 100K. Our tokenized pre-
    1036: training corpus contains 8.1T tokens, where Chinese tokens are approximately 12% more than
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1055 | **Candidates:** `236.0B`

```text
    1053: layers after the compressed latent vectors, and multiply additional scaling factors at the width
    1054: bottlenecks (i.e., the compressed latent vectors and the intermediate hidden states of routed
>>> 1055: experts) to ensure stable training. Under this configuration, DeepSeek-V2 comprises 236B total
    1056: parameters, of which 21B are activated for each token.
    1057: 
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
**Line:** 1133 | **Candidates:** `2.0B`

```text
    1131: 13
    1132: 
>>> 1133: 1K12K24K35K47K58K70K81K93K104K116K128KContext Length (#Tokens)09182736455564738291100Document Depth Percent (%)Pressure Testing DeepSeek-V2 Base 128K Context via "Needle In A HayStack"12345678910Score
    1134: in our HAI-LLM framework. Included benchmarks are categorized and listed as follows, where
    1135: underlined benchmarks are in Chinese:
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1189 | **Candidates:** `67.0B, 72.0B`

```text
    1187: 
    1188: In Table 2, we compare DeepSeek-V2 with several representative open-source models, includ-
>>> 1189: ing DeepSeek 67B (DeepSeek-AI, 2024) (our previous release), Qwen1.5 72B (Bai et al., 2023),
    1190: LLaMA3 70B (AI@Meta, 2024), and Mixtral 8x22B (Mistral, 2024). We evaluate all these models
    1191: with our internal evaluation framework, and ensure that they share the same evaluation setting.
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
**Line:** 1198 | **Candidates:** `72.0B`

```text
    1196: one. (1) Compared with Qwen1.5 72B, another model that supports both Chinese and English,
    1197: DeepSeek-V2 demonstrates overwhelming advantages on the majority of English, code, and
>>> 1198: math benchmarks. As for Chinese benchmarks, Qwen1.5 72B shows better performance on
    1199: 
    1200: 14
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1279 | **Candidates:** `0.002B`

```text
    1277: 0-shot
    1278: 
>>> 1279: DeepSeek Qwen1.5 Mixtral LLaMA 3
    1280: 
    1281: 67B
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1281 | **Candidates:** `67.0B`

```text
    1279: DeepSeek Qwen1.5 Mixtral LLaMA 3
    1280: 
>>> 1281: 67B
    1282: 
    1283: Dense
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1284 | **Candidates:** `67.0B`

```text
    1282: 
    1283: Dense
>>> 1284: 67B
    1285: 67B
    1286: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1285 | **Candidates:** `67.0B`

```text
    1283: Dense
    1284: 67B
>>> 1285: 67B
    1286: 
    1287: 0.642
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1319 | **Candidates:** `72.0B`

```text
    1317: 88.5
    1318: 
>>> 1319: 72B
    1320: 
    1321: 8x22B
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1321 | **Candidates:** `22.0B`

```text
    1319: 72B
    1320: 
>>> 1321: 8x22B
    1322: 
    1323: 70B
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1323 | **Candidates:** `70.0B`

```text
    1321: 8x22B
    1322: 
>>> 1323: 70B
    1324: 
    1325: Dense
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1326 | **Candidates:** `72.0B`

```text
    1324: 
    1325: Dense
>>> 1326: 72B
    1327: 72B
    1328: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1327 | **Candidates:** `72.0B`

```text
    1325: Dense
    1326: 72B
>>> 1327: 72B
    1328: 
    1329: 0.637
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1362 | **Candidates:** `39.0B`

```text
    1360: 
    1361: MoE
>>> 1362: 39B
    1363: 141B
    1364: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1363 | **Candidates:** `141.0B`

```text
    1361: MoE
    1362: 39B
>>> 1363: 141B
    1364: 
    1365: 0.623
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1398 | **Candidates:** `70.0B`

```text
    1396: 
    1397: Dense
>>> 1398: 70B
    1399: 70B
    1400: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1399 | **Candidates:** `70.0B`

```text
    1397: Dense
    1398: 70B
>>> 1399: 70B
    1400: 
    1401: 0.602
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1444 | **Candidates:** `21.0B`

```text
    1442: 
    1443: MoE
>>> 1444: 21B
    1445: 236B
    1446: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1445 | **Candidates:** `236.0B`

```text
    1443: MoE
    1444: 21B
>>> 1445: 236B
    1446: 
    1447: 0.606
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
**Line:** 1486 | **Candidates:** `72.0B`

```text
    1484: 
    1485: multi-subject multiple-choice tasks while DeepSeek-V2 is comparable or better on others. Note
>>> 1486: that for the CHID benchmark, the tokenizer of Qwen1.5 72B will encounter errors in our
    1487: evaluation framework, so we leave the CHID score blank for Qwen1.5 72B. (2) Compared with
    1488: Mixtral 8x22B, DeepSeek-V2 achieves comparable or better English performance, except for
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1487 | **Candidates:** `72.0B`

```text
    1485: multi-subject multiple-choice tasks while DeepSeek-V2 is comparable or better on others. Note
    1486: that for the CHID benchmark, the tokenizer of Qwen1.5 72B will encounter errors in our
>>> 1487: evaluation framework, so we leave the CHID score blank for Qwen1.5 72B. (2) Compared with
    1488: Mixtral 8x22B, DeepSeek-V2 achieves comparable or better English performance, except for
    1489: TriviaQA, NaturalQuestions, and HellaSwag, which are closely related to English commonsense
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1488 | **Candidates:** `22.0B`

```text
    1486: that for the CHID benchmark, the tokenizer of Qwen1.5 72B will encounter errors in our
    1487: evaluation framework, so we leave the CHID score blank for Qwen1.5 72B. (2) Compared with
>>> 1488: Mixtral 8x22B, DeepSeek-V2 achieves comparable or better English performance, except for
    1489: TriviaQA, NaturalQuestions, and HellaSwag, which are closely related to English commonsense
    1490: knowledge. Notably, DeepSeek-V2 outperforms Mixtral 8x22B on MMLU. On code and math
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1490 | **Candidates:** `22.0B`

```text
    1488: Mixtral 8x22B, DeepSeek-V2 achieves comparable or better English performance, except for
    1489: TriviaQA, NaturalQuestions, and HellaSwag, which are closely related to English commonsense
>>> 1490: knowledge. Notably, DeepSeek-V2 outperforms Mixtral 8x22B on MMLU. On code and math
    1491: benchmarks, DeepSeek-V2 demonstrates comparable performance with Mixtral 8x22B. Since
    1492: Mixtral 8x22B is not specifically trained on Chinese data, its Chinese capability lags far behind
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1491 | **Candidates:** `22.0B`

```text
    1489: TriviaQA, NaturalQuestions, and HellaSwag, which are closely related to English commonsense
    1490: knowledge. Notably, DeepSeek-V2 outperforms Mixtral 8x22B on MMLU. On code and math
>>> 1491: benchmarks, DeepSeek-V2 demonstrates comparable performance with Mixtral 8x22B. Since
    1492: Mixtral 8x22B is not specifically trained on Chinese data, its Chinese capability lags far behind
    1493: DeepSeek-V2. (3) Compared with LLaMA3 70B, DeepSeek-V2 is trained on fewer than a quarter
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1492 | **Candidates:** `22.0B`

```text
    1490: knowledge. Notably, DeepSeek-V2 outperforms Mixtral 8x22B on MMLU. On code and math
    1491: benchmarks, DeepSeek-V2 demonstrates comparable performance with Mixtral 8x22B. Since
>>> 1492: Mixtral 8x22B is not specifically trained on Chinese data, its Chinese capability lags far behind
    1493: DeepSeek-V2. (3) Compared with LLaMA3 70B, DeepSeek-V2 is trained on fewer than a quarter
    1494: of English tokens. Therefore, we acknowledge that DeepSeek-V2 still has a slight gap in basic
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1493 | **Candidates:** `70.0B`

```text
    1491: benchmarks, DeepSeek-V2 demonstrates comparable performance with Mixtral 8x22B. Since
    1492: Mixtral 8x22B is not specifically trained on Chinese data, its Chinese capability lags far behind
>>> 1493: DeepSeek-V2. (3) Compared with LLaMA3 70B, DeepSeek-V2 is trained on fewer than a quarter
    1494: of English tokens. Therefore, we acknowledge that DeepSeek-V2 still has a slight gap in basic
    1495: English capabilities with LLaMA3 70B. However, even with much fewer training tokens and
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1495 | **Candidates:** `70.0B`

```text
    1493: DeepSeek-V2. (3) Compared with LLaMA3 70B, DeepSeek-V2 is trained on fewer than a quarter
    1494: of English tokens. Therefore, we acknowledge that DeepSeek-V2 still has a slight gap in basic
>>> 1495: English capabilities with LLaMA3 70B. However, even with much fewer training tokens and
    1496: activated parameters, DeepSeek-V2 still demonstrates comparable code and math capability
    1497: with LLaMA3 70B. Also, as a bilingual language model, DeepSeek-V2 outperforms LLaMA3
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
**Line:** 1502 | **Candidates:** `70.0B`

```text
    1500: 
    1501: 
>>> 1502: 70B overwhelmingly on Chinese benchmarks.
    1503: 
    1504: Finally, it is worth mentioning that certain prior studies (Hu et al., 2024) incorporate SFT
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1511 | **Candidates:** `67.0B`

```text
    1509: 
    1510: Training Costs. Since DeepSeek-V2 activates fewer parameters for each token and requires
>>> 1511: fewer FLOPs than DeepSeek 67B, training DeepSeek-V2 will be more economical than training
    1512: DeepSeek 67B theoretically. Although training an MoE model will introduce additional commu-
    1513: nication overheads, through our operator and communication optimizations, the training for
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
**Line:** 1515 | **Candidates:** `67.0B`

```text
    1513: nication overheads, through our operator and communication optimizations, the training for
    1514: DeepSeek-V2 can attain a relatively high Model FLOPs Utilization (MFU). During our practical
>>> 1515: training on the H800 cluster, for training on each trillion tokens, DeepSeek 67B requires 300.6K
    1516: GPU hours, while DeepSeek-V2 needs only 172.8K GPU hours, i.e., sparse DeepSeek-V2 can
    1517: save 42.5% training costs compared with dense DeepSeek 67B.
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1517 | **Candidates:** `67.0B`

```text
    1515: training on the H800 cluster, for training on each trillion tokens, DeepSeek 67B requires 300.6K
    1516: GPU hours, while DeepSeek-V2 needs only 172.8K GPU hours, i.e., sparse DeepSeek-V2 can
>>> 1517: save 42.5% training costs compared with dense DeepSeek 67B.
    1518: 
    1519: Inference Efficiency.
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1523 | **Candidates:** `6.0B`

```text
    1521: its parameters into the precision of FP8. In addition, we also perform KV cache quantiza-
    1522: tion (Hooper et al., 2024; Zhao et al., 2023) for DeepSeek-V2 to further compress each element
>>> 1523: in its KV cache into 6 bits on average. Benefiting from MLA and these optimizations, actually
    1524: deployed DeepSeek-V2 requires significantly less KV cache than DeepSeek 67B, and thus can
    1525: serve a much larger batch size. We evaluate the generation throughput of DeepSeek-V2 based
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1524 | **Candidates:** `67.0B`

```text
    1522: tion (Hooper et al., 2024; Zhao et al., 2023) for DeepSeek-V2 to further compress each element
    1523: in its KV cache into 6 bits on average. Benefiting from MLA and these optimizations, actually
>>> 1524: deployed DeepSeek-V2 requires significantly less KV cache than DeepSeek 67B, and thus can
    1525: serve a much larger batch size. We evaluate the generation throughput of DeepSeek-V2 based
    1526: on the prompt and generation length distribution from the actually deployed DeepSeek 67B
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1525 | **Candidates:** `2.0B`

```text
    1523: in its KV cache into 6 bits on average. Benefiting from MLA and these optimizations, actually
    1524: deployed DeepSeek-V2 requires significantly less KV cache than DeepSeek 67B, and thus can
>>> 1525: serve a much larger batch size. We evaluate the generation throughput of DeepSeek-V2 based
    1526: on the prompt and generation length distribution from the actually deployed DeepSeek 67B
    1527: service. On a single node with 8 H800 GPUs, DeepSeek-V2 achieves a generation throughput
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1526 | **Candidates:** `67.0B`

```text
    1524: deployed DeepSeek-V2 requires significantly less KV cache than DeepSeek 67B, and thus can
    1525: serve a much larger batch size. We evaluate the generation throughput of DeepSeek-V2 based
>>> 1526: on the prompt and generation length distribution from the actually deployed DeepSeek 67B
    1527: service. On a single node with 8 H800 GPUs, DeepSeek-V2 achieves a generation throughput
    1528: exceeding 50K tokens per second, which is 5.76 times the maximum generation throughput of
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1529 | **Candidates:** `67.0B`

```text
    1527: service. On a single node with 8 H800 GPUs, DeepSeek-V2 achieves a generation throughput
    1528: exceeding 50K tokens per second, which is 5.76 times the maximum generation throughput of
>>> 1529: DeepSeek 67B. In addition, the prompt input throughput of DeepSeek-V2 exceeds 100K tokens
    1530: per second.
    1531: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1537 | **Candidates:** `0.0B, 0.001B, 0.002B`

```text
    1535: 
    1536: Building upon our prior research (DeepSeek-AI, 2024), we curate our instruction tuning datasets
>>> 1537: to include 1.5M instances, comprising 1.2M instances for helpfulness and 0.3M instances for
    1538: safety. In comparison to the initial version, we improve the data quality to mitigate hallucinatory
    1539: responses and enhance writing proficiency. We fine-tune DeepSeek-V2 with 2 epochs, and
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1548 | **Candidates:** `22.0B, 70.0B, 72.0B`

```text
    1546: our model on open-ended conversation benchmarks including MT-Bench (Zheng et al., 2023),
    1547: AlpacaEval 2.0 (Dubois et al., 2024), and AlignBench (Liu et al., 2023). For comparison, we also
>>> 1548: evaluate Qwen1.5 72B Chat, LLaMA-3-70B Instruct, and Mistral-8x22B Instruct in our evaluation
    1549: framework and settings. As for DeepSeek 67B Chat, we directly refer to the evaluation results
    1550: reported in our previous release.
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1549 | **Candidates:** `67.0B`

```text
    1547: AlpacaEval 2.0 (Dubois et al., 2024), and AlignBench (Liu et al., 2023). For comparison, we also
    1548: evaluate Qwen1.5 72B Chat, LLaMA-3-70B Instruct, and Mistral-8x22B Instruct in our evaluation
>>> 1549: framework and settings. As for DeepSeek 67B Chat, we directly refer to the evaluation results
    1550: reported in our previous release.
    1551: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1689 | **Candidates:** `72.0B`

```text
    1687: 
    1688: As for the comparisons with other models, we first compare DeepSeek-V2 Chat (SFT)
>>> 1689: with Qwen1.5 72B Chat, and find that DeepSeek-V2 Chat (SFT) surpasses Qwen1.5 72B Chat
    1690: on almost all of English, math, and code benchmarks. On Chinese benchmarks, DeepSeek-
    1691: V2 Chat (SFT) demonstrates slightly lower scores than Qwen1.5 72B Chat on multi-subject
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1691 | **Candidates:** `72.0B`

```text
    1689: with Qwen1.5 72B Chat, and find that DeepSeek-V2 Chat (SFT) surpasses Qwen1.5 72B Chat
    1690: on almost all of English, math, and code benchmarks. On Chinese benchmarks, DeepSeek-
>>> 1691: V2 Chat (SFT) demonstrates slightly lower scores than Qwen1.5 72B Chat on multi-subject
    1692: multiple-choice tasks, consistent with the performance observed from their base versions. When
    1693: compared with the state-of-the-art open-source MoE model, Mixtral 8x22B Instruct, DeepSeek-
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
**Line:** 1697 | **Candidates:** `70.0B`

```text
    1695: and IFEval. Furthermore, in comparison to the state-of-the-art open-source model LLaMA3 70B
    1696: Chat, DeepSeek-V2 Chat (SFT) shows similar performance in code and math related benchmarks.
>>> 1697: LLaMA3 70B Chat exhibits better performance on MMLU and IFEval, while DeepSeek-V2 Chat
    1698: (SFT) showcases stronger performance on Chinese tasks. Ultimately, DeepSeek-V2 Chat (RL)
    1699: demonstrates further enhanced performance in both mathematical and coding tasks compared
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1709 | **Candidates:** `22.0B, 72.0B`

```text
    1707: DeepSeek-V2 Chat (SFT). This outcome showcases the effectiveness of our RL training in achiev-
    1708: ing improved alignment. In comparison to other open-source models, DeepSeek-V2 Chat (RL)
>>> 1709: demonstrates superior performance over Mistral 8x22B Instruct and Qwen1.5 72B Chat on both
    1710: benchmarks. When compared with LLaMA3 70B Instruct, DeepSeek-V2 Chat (RL) showcases
    1711: competitive performance on MT-Bench and notably outperforms it on AlpacaEval 2.0. These
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1710 | **Candidates:** `70.0B`

```text
    1708: ing improved alignment. In comparison to other open-source models, DeepSeek-V2 Chat (RL)
    1709: demonstrates superior performance over Mistral 8x22B Instruct and Qwen1.5 72B Chat on both
>>> 1710: benchmarks. When compared with LLaMA3 70B Instruct, DeepSeek-V2 Chat (RL) showcases
    1711: competitive performance on MT-Bench and notably outperforms it on AlpacaEval 2.0. These
    1712: results highlight the strong performance of DeepSeek-V2 Chat (RL) in generating high-quality
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1727 | **Candidates:** `0.003B`

```text
    1725: # Shots
    1726: 
>>> 1727: DeepSeek Qwen 1.5 LLaMA3 Mixtral DeepSeek-V2 DeepSeek-V2
    1728: 67B Chat 72B Chat 70B Inst. 8x22B Inst. Chat (SFT)
    1729: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1728 | **Candidates:** `22.0B, 67.0B, 70.0B, 72.0B`

```text
    1726: 
    1727: DeepSeek Qwen 1.5 LLaMA3 Mixtral DeepSeek-V2 DeepSeek-V2
>>> 1728: 67B Chat 72B Chat 70B Inst. 8x22B Inst. Chat (SFT)
    1729: 
    1730: Chat (RL)
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1742 | **Candidates:** `67.0B`

```text
    1740: 4K
    1741: Dense
>>> 1742: 67B
    1743: 67B
    1744: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1743 | **Candidates:** `67.0B`

```text
    1741: Dense
    1742: 67B
>>> 1743: 67B
    1744: 
    1745: 32K
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1747 | **Candidates:** `72.0B`

```text
    1745: 32K
    1746: Dense
>>> 1747: 72B
    1748: 72B
    1749: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1748 | **Candidates:** `72.0B`

```text
    1746: Dense
    1747: 72B
>>> 1748: 72B
    1749: 
    1750: 8K
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1752 | **Candidates:** `70.0B`

```text
    1750: 8K
    1751: Dense
>>> 1752: 70B
    1753: 70B
    1754: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1753 | **Candidates:** `70.0B`

```text
    1751: Dense
    1752: 70B
>>> 1753: 70B
    1754: 
    1755: TriviaQA
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1879 | **Candidates:** `39.0B`

```text
    1877: 64K
    1878: MoE
>>> 1879: 39B
    1880: 141B
    1881: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1880 | **Candidates:** `141.0B`

```text
    1878: MoE
    1879: 39B
>>> 1880: 141B
    1881: 
    1882: 80.0
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1907 | **Candidates:** `21.0B`

```text
    1905: 128K
    1906: MoE
>>> 1907: 21B
    1908: 236B
    1909: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1908 | **Candidates:** `236.0B`

```text
    1906: MoE
    1907: 21B
>>> 1908: 236B
    1909: 
    1910: 85.4
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1935 | **Candidates:** `21.0B`

```text
    1933: 128K
    1934: MoE
>>> 1935: 21B
    1936: 236B
    1937: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1936 | **Candidates:** `236.0B`

```text
    1934: MoE
    1935: 21B
>>> 1936: 236B
    1937: 
    1938: 86.7
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
**Line:** 1971 | **Candidates:** `67.0B`

```text
    1969: MT-Bench AlpacaEval 2.0
    1970: 
>>> 1971: DeepSeek 67B Chat
    1972: Mistral 8x22B Instruct v0.1
    1973: Qwen1.5 72B Chat
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1972 | **Candidates:** `22.0B`

```text
    1970: 
    1971: DeepSeek 67B Chat
>>> 1972: Mistral 8x22B Instruct v0.1
    1973: Qwen1.5 72B Chat
    1974: LLaMA3 70B Instruct
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1973 | **Candidates:** `72.0B`

```text
    1971: DeepSeek 67B Chat
    1972: Mistral 8x22B Instruct v0.1
>>> 1973: Qwen1.5 72B Chat
    1974: LLaMA3 70B Instruct
    1975: DeepSeek-V2 Chat (SFT)
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1974 | **Candidates:** `70.0B`

```text
    1972: Mistral 8x22B Instruct v0.1
    1973: Qwen1.5 72B Chat
>>> 1974: LLaMA3 70B Instruct
    1975: DeepSeek-V2 Chat (SFT)
    1976: DeepSeek-V2 Chat (RL)
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 1995 | **Candidates:** `72.0B`

```text
    1993: controlled win rate as the metric.
    1994: 
>>> 1995: 72B Chat on both Chinese reasoning and language. Moreover, both DeepSeek-V2 Chat (SFT)
    1996: and DeepSeek-V2 Chat (RL) outperform GPT-4-0613 and ERNIEBot 4.0, solidifying the position
    1997: of our models in the top-tier LLMs that support Chinese. Specifically, DeepSeek-V2 Chat (RL)
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2061 | **Candidates:** `72.0B`

```text
    2059: Moonshot-v1-32k-202404*（月之暗面） 7.22
    2060: 7.19
>>> 2061: Qwen1.5-72B-Chat*
    2062: 6.43
    2063: DeepSeek-67B-Chat
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2063 | **Candidates:** `67.0B`

```text
    2061: Qwen1.5-72B-Chat*
    2062: 6.43
>>> 2063: DeepSeek-67B-Chat
    2064: ChatGLM-Turbo（智谱清言）
    2065: 6.24
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2069 | **Candidates:** `34.0B`

```text
    2067: 6.14
    2068: 6.12
>>> 2069: Yi-34B-Chat*
    2070: 6.08
    2071: GPT-3.5-Turbo-0613
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2077 | **Candidates:** `14.0B`

```text
    2075: 5.74
    2076: 5.72
>>> 2077: Qwen-14B-Chat
    2078: 5.25
    2079: Baichuan2-13B-Chat
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2079 | **Candidates:** `13.0B`

```text
    2077: Qwen-14B-Chat
    2078: 5.25
>>> 2079: Baichuan2-13B-Chat
    2080: 4.97
    2081: ChatGLM3-6B
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2081 | **Candidates:** `6.0B`

```text
    2079: Baichuan2-13B-Chat
    2080: 4.97
>>> 2081: ChatGLM3-6B
    2082: 4.97
    2083: Baichuan2-7B-Chat
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2083 | **Candidates:** `7.0B`

```text
    2081: ChatGLM3-6B
    2082: 4.97
>>> 2083: Baichuan2-7B-Chat
    2084: 4.96
    2085: InternLM-20B
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2085 | **Candidates:** `20.0B`

```text
    2083: Baichuan2-7B-Chat
    2084: 4.96
>>> 2085: InternLM-20B
    2086: 4.91
    2087: Qwen-7B-Chat
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2087 | **Candidates:** `7.0B`

```text
    2085: InternLM-20B
    2086: 4.91
>>> 2087: Qwen-7B-Chat
    2088: 4.48
    2089: ChatGLM2-6B
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2089 | **Candidates:** `6.0B`

```text
    2087: Qwen-7B-Chat
    2088: 4.48
>>> 2089: ChatGLM2-6B
    2090: 3.65
    2091: InternLM-Chat-7B
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2091 | **Candidates:** `7.0B`

```text
    2089: ChatGLM2-6B
    2090: 3.65
>>> 2091: InternLM-Chat-7B
    2092: 3.57
    2093: Chinese-LLaMA-2-7B-Chat
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2093 | **Candidates:** `7.0B`

```text
    2091: InternLM-Chat-7B
    2092: 3.57
>>> 2093: Chinese-LLaMA-2-7B-Chat
    2094: 3.35
    2095: LLaMA-2-13B-Chinese-Chat
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2095 | **Candidates:** `13.0B`

```text
    2093: Chinese-LLaMA-2-7B-Chat
    2094: 3.35
>>> 2095: LLaMA-2-13B-Chinese-Chat
    2096: 
    2097: 7.73
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2401 | **Candidates:** `67.0B`

```text
    2399: In addition to strong performance, it is also characterized by economical
    2400: training and efficient inference, benefiting from its innovative architecture including MLA and
>>> 2401: DeepSeekMoE. In practice, compared with DeepSeek 67B, DeepSeek-V2 achieves significantly
    2402: stronger performance, and meanwhile saves 42.5% of training costs, reduces the KV cache
    2403: by 93.3%, and boosts the maximum generation throughput to 5.76 times. Evaluation results
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
**Line:** 2432 | **Candidates:** `0.003B`

```text
    2430: References
    2431: 
>>> 2432: AI@Meta. Llama 3 model card, 2024. URL https://github.com/meta-llama/llama3/bl
    2433: 
    2434: ob/main/MODEL_CARD.md.
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2508 | **Candidates:** `2.019B`

```text
    2506: T. Solorio, editors, Proceedings of the 2019 Conference of the North American Chapter of the
    2507: Association for Computational Linguistics: Human Language Technologies, NAACL-HLT
>>> 2508: 2019, Minneapolis, MN, USA, June 2-7, 2019, Volume 1 (Long and Short Papers), pages 2368–
    2509: 2378. Association for Computational Linguistics, 2019. doi: 10.18653/V1/N19-1246. URL
    2510: https://doi.org/10.18653/v1/n19-1246.
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2547 | **Candidates:** `0.01B`

```text
    2545: 
    2546: C. Hooper, S. Kim, H. Mohammadzadeh, M. W. Mahoney, Y. S. Shao, K. Keutzer, and A. Gholami.
>>> 2547: Kvquant: Towards 10 million context length LLM inference with KV cache quantization. CoRR,
    2548: abs/2401.18079, 2024. URL https://doi.org/10.48550/arXiv.2401.18079.
    2549: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2614 | **Candidates:** `22.0B`

```text
    2612: Mistral. Cheaper, better, faster, stronger: Continuing to push the frontier of ai and making it
    2613: 
>>> 2614: accessible to all, 2024. URL https://mistral.ai/news/mixtral-8x22b.
    2615: 
    2616: OpenAI. Introducing ChatGPT, 2022. URL https://openai.com/blog/chatgpt.
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2696 | **Candidates:** `2020.0B`

```text
    2694: nese language understanding evaluation benchmark. In D. Scott, N. Bel, and C. Zong, editors,
    2695: Proceedings of the 28th International Conference on Computational Linguistics, COLING
>>> 2696: 2020, Barcelona, Spain (Online), December 8-13, 2020, pages 4762–4772. International Com-
    2697: mittee on Computational Linguistics, 2020. doi: 10.18653/V1/2020.COLING-MAIN.419. URL
    2698: https://doi.org/10.18653/v1/2020.coling-main.419.
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2917 | **Candidates:** `2.0B`

```text
    2915: and Wangding Zeng have made key innovations in the research of the MLA architecture.
    2916: Furthermore, we’d like to thank Jianlin Su for his helpful discussion on position embedding.
>>> 2917: We thank all those who have contributed to DeepSeek-V2 but are not mentioned in the paper.
    2918: DeepSeek believes that innovation, novelty, and curiosity are essential in the path to AGI.
    2919: 
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
**Line:** 2929 | **Candidates:** `512.0B`

```text
    2927: Architectures. DeepSeek-V2-Lite has 27 layers and a hidden dimension of 2048. It also employs
    2928: MLA and has 16 attention heads, where each head has a dimension of 128. Its KV compression
>>> 2929: dimension is 512, but slightly different from DeepSeek-V2, it does not compress the queries.
    2930: For the decoupled queries and key, it has a per-head dimension of 64. DeepSeek-V2-Lite also
    2931: employs DeepSeekMoE, and all FFNs except for the first layer are replaced with MoE layers.
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
**Line:** 2935 | **Candidates:** `2.4B`

```text
    2933: hidden dimension of each expert is 1408. Among the routed experts, 6 experts will be activated
    2934: for each token. Under this configuration, DeepSeek-V2-Lite comprises 15.7B total parameters, of
>>> 2935: which 2.4B are activated for each token.
    2936: 
    2937: Benchmark
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2939 | **Candidates:** `7.0B, 16.0B`

```text
    2937: Benchmark
    2938: 
>>> 2939: DeepSeek 7B DeepSeekMoE 16B DeepSeek-V2-Lite
    2940: 
    2941: Architecture
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2949 | **Candidates:** `6.9B`

```text
    2947: MHA+Dense
    2948: 4K
>>> 2949: 6.9B
    2950: 6.9B
    2951: 2T
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2950 | **Candidates:** `6.9B`

```text
    2948: 4K
    2949: 6.9B
>>> 2950: 6.9B
    2951: 2T
    2952: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2955 | **Candidates:** `2.8B`

```text
    2953: MHA+MoE
    2954: 4K
>>> 2955: 2.8B
    2956: 16.4B
    2957: 2T
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2956 | **Candidates:** `16.4B`

```text
    2954: 4K
    2955: 2.8B
>>> 2956: 16.4B
    2957: 2T
    2958: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2961 | **Candidates:** `2.4B`

```text
    2959: MLA+MoE
    2960: 32K
>>> 2961: 2.4B
    2962: 15.7B
    2963: 5.7T
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 2962 | **Candidates:** `15.7B`

```text
    2960: 32K
    2961: 2.4B
>>> 2962: 15.7B
    2963: 5.7T
    2964: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3049 | **Candidates:** `7.0B, 16.0B`

```text
    3047: 64.3
    3048: 
>>> 3049: Table 6 | Performance of DeepSeek-V2-Lite, DeepSeekMoE 16B, and DeepSeek 7B.
    3050: 
    3051: Training Details. DeepSeek-V2-Lite is also trained from scratch on the same pre-training
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3075 | **Candidates:** `7.0B`

```text
    3073: DeepSeek DeepSeekMoE DeepSeek-V2-Lite
    3074: 
>>> 3075: 7B Chat
    3076: 
    3077: 16B Chat
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3077 | **Candidates:** `16.0B`

```text
    3075: 7B Chat
    3076: 
>>> 3077: 16B Chat
    3078: 
    3079: Chat
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3117 | **Candidates:** `6.9B`

```text
    3115: 
    3116: 4K
>>> 3117: 6.9B
    3118: 6.9B
    3119: 2T
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3118 | **Candidates:** `6.9B`

```text
    3116: 4K
    3117: 6.9B
>>> 3118: 6.9B
    3119: 2T
    3120: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3141 | **Candidates:** `2.8B`

```text
    3139: 
    3140: 4K
>>> 3141: 2.8B
    3142: 16.4B
    3143: 2T
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3142 | **Candidates:** `16.4B`

```text
    3140: 4K
    3141: 2.8B
>>> 3142: 16.4B
    3143: 2T
    3144: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3166 | **Candidates:** `2.4B`

```text
    3164: MLA+MoE
    3165: 32K
>>> 3166: 2.4B
    3167: 15.7B
    3168: 5.7T
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3167 | **Candidates:** `15.7B`

```text
    3165: 32K
    3166: 2.4B
>>> 3167: 15.7B
    3168: 5.7T
    3169: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3189 | **Candidates:** `7.0B, 16.0B`

```text
    3187: 62.5
    3188: 
>>> 3189: Table 7 | Performance of DeepSeek-V2-Lite Chat, DeepSeekMoE 16B Chat, and DeepSeek 7B
    3190: Chat.
    3191: 
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
**Line:** 3383 | **Candidates:** `7.0B`

```text
    3381: # Shots
    3382: 
>>> 3383: Dense 7B
    3384: Dense 7B
    3385: Dense 7B
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3384 | **Candidates:** `7.0B`

```text
    3382: 
    3383: Dense 7B
>>> 3384: Dense 7B
    3385: Dense 7B
    3386: w/ MQA w/ GQA (8 Groups) w/ MHA
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3385 | **Candidates:** `7.0B`

```text
    3383: Dense 7B
    3384: Dense 7B
>>> 3385: Dense 7B
    3386: w/ MQA w/ GQA (8 Groups) w/ MHA
    3387: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3402 | **Candidates:** `7.1B`

```text
    3400: 5-shot
    3401: 
>>> 3402: 7.1B
    3403: 
    3404: 33.2
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3409 | **Candidates:** `6.9B`

```text
    3407: 34.6
    3408: 
>>> 3409: 6.9B
    3410: 
    3411: 35.6
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3416 | **Candidates:** `6.9B`

```text
    3414: 38.4
    3415: 
>>> 3416: 6.9B
    3417: 
    3418: 37.0
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

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3458 | **Candidates:** `2.5B`

```text
    3456: 5-shot
    3457: 
>>> 3458: 2.5B
    3459: 15.8B
    3460: 110.6K
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3459 | **Candidates:** `15.8B`

```text
    3457: 
    3458: 2.5B
>>> 3459: 15.8B
    3460: 110.6K
    3461: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3467 | **Candidates:** `2.4B`

```text
    3465: 52.3
    3466: 
>>> 3467: 2.4B
    3468: 15.7B
    3469: 15.6K
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3468 | **Candidates:** `15.7B`

```text
    3466: 
    3467: 2.4B
>>> 3468: 15.7B
    3469: 15.6K
    3470: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3476 | **Candidates:** `25.0B`

```text
    3474: 53.4
    3475: 
>>> 3476: 25.0B
    3477: 250.8B
    3478: 860.2K
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3477 | **Candidates:** `250.8B`

```text
    3475: 
    3476: 25.0B
>>> 3477: 250.8B
    3478: 860.2K
    3479: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3485 | **Candidates:** `21.5B`

```text
    3483: 60.7
    3484: 
>>> 3485: 21.5B
    3486: 247.4B
    3487: 34.6K
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3486 | **Candidates:** `247.4B`

```text
    3484: 
    3485: 21.5B
>>> 3486: 247.4B
    3487: 34.6K
    3488: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3504 | **Candidates:** `22.0B`

```text
    3502: slightly worse on the test sets that are closely associated with specific regional cultures. For
    3503: example, when evaluated on MMLU, although DeepSeek-V2 achieves comparable or superior
>>> 3504: performance on the majority of testsets compared with its competitors like Mixtral 8x22B, it still
    3505: lags behind on the Humanity-Moral subset, which is mainly associated with American values.
    3506: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3508 | **Candidates:** `0.42B`

```text
    3506: 
    3507: Further, we conduct a manual analysis on this subset. Three well-educated human annotators
>>> 3508: conduct independent annotations on 420 moral scenarios from the MMLU Humanity-Moral
    3509: subset. Then, we compute the agreement among their annotations and the ground-truth label. As
    3510: shown in Table 10, three human annotators and the ground-truth label exhibit a low agreement
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3554 | **Candidates:** `0.42B`

```text
    3552: 100.0%
    3553: 
>>> 3554: Table 10 | Three well-educated human annotators conduct independent annotations on 420 moral
    3555: scenarios from the MMLU Humanity-Moral subset, on which DeepSeek-V2 and its competitive
    3556: models demonstrate performance inconsistency. Three annotators and the ground-truth label
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3569 | **Candidates:** `110.0B`

```text
    3567: DeepSeek-V2 Chat (RL)
    3568: Ernie-bot 4.0
>>> 3569: Qwen-110B-Chat
    3570: GLM-4
    3571: Xinghuo 3.5
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3572 | **Candidates:** `72.0B`

```text
    3570: GLM-4
    3571: Xinghuo 3.5
>>> 3572: Qwen-72B-Chat
    3573: ChatGLM-Turbo
    3574: GPT-3.5-Turbo
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3575 | **Candidates:** `14.0B`

```text
    3573: ChatGLM-Turbo
    3574: GPT-3.5-Turbo
>>> 3575: Qwen-14B-Chat
    3576: ChatGLM3-6B
    3577: Xinghuo 3.0
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3576 | **Candidates:** `6.0B`

```text
    3574: GPT-3.5-Turbo
    3575: Qwen-14B-Chat
>>> 3576: ChatGLM3-6B
    3577: Xinghuo 3.0
    3578: Baichuan2-13B-Chat
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3578 | **Candidates:** `13.0B`

```text
    3576: ChatGLM3-6B
    3577: Xinghuo 3.0
>>> 3578: Baichuan2-13B-Chat
    3579: Ernie-3.5-turbo
    3580: Chinese-Alpaca2-13B
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3580 | **Candidates:** `13.0B`

```text
    3578: Baichuan2-13B-Chat
    3579: Ernie-3.5-turbo
>>> 3580: Chinese-Alpaca2-13B
    3581: 
    3582: 5
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3654 | **Candidates:** `0.006B`

```text
    3652: 18.58
    3653: 
>>> 3654: Table 11 | SC-Math6 Model Reasoning Level. “R Level” stands for Reasoning Level, “Comp.
    3655: Score” stands for Comprehensive Score, “Reas. Steps Score” stands for Reasoning Steps Score,
    3656: and “OvrAcc Score” stands for Overall Accuracy Score.
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 3685 | **Candidates:** `22.0B, 67.0B, 70.0B, 72.0B`

```text
    3683: 34
    3684: 
>>> 3685: 657075808590HumanEval (Pass@1)15202530354045LiveCodeBench (Pass@1)DeepSeek-V2-Chat-RLDeepSeek 67BMixtral 8x22BMistral LargeQwen MaxQwen1.5 72BGPT-4-Turbo-1106GPT-4-0613Claude OpusClaude SonnetClaude HaikuLLaMA3-70B-Chat
    3686: PROMPT
    3687: Question: A sample in a cylindrical container has a cylindrical shape and a
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4037 | **Candidates:** `0.04B`

```text
    4035: 
    4036: PROMPT
>>> 4037: Q: Max can mow the lawn in 40 minutes. If it takes him twice that long to
    4038: fertilize the lawn, how long will it take him to both mow and fertilize the lawn?
    4039: A: Let’s think step by step. It takes Max 2 * 40 minutes = 80 minutes to fertilize
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4039 | **Candidates:** `0.04B, 0.08B`

```text
    4037: Q: Max can mow the lawn in 40 minutes. If it takes him twice that long to
    4038: fertilize the lawn, how long will it take him to both mow and fertilize the lawn?
>>> 4039: A: Let’s think step by step. It takes Max 2 * 40 minutes = 80 minutes to fertilize
    4040: the lawn. In total, Max takes 80 minutes + 40 minutes = 120 minutes to both
    4041: mow and fertilize the lawn. The answer is 120.
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4040 | **Candidates:** `0.04B, 0.08B, 0.12B`

```text
    4038: fertilize the lawn, how long will it take him to both mow and fertilize the lawn?
    4039: A: Let’s think step by step. It takes Max 2 * 40 minutes = 80 minutes to fertilize
>>> 4040: the lawn. In total, Max takes 80 minutes + 40 minutes = 120 minutes to both
    4041: mow and fertilize the lawn. The answer is 120.
    4042: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4055 | **Candidates:** `4.0B, 14.0B`

```text
    4053: years old. So, Tim is 17 - 5 = 12 years younger than Jenny. The answer is 12.
    4054: 
>>> 4055: Q: The school has 14 boys and 10 girls. If 4 boys and 3 girls drop out, how
    4056: many boys and girls are left?
    4057: A: Let’s think step by step. There are 14 boys - 4 boys = 10 boys left. There are
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4057 | **Candidates:** `4.0B, 10.0B, 14.0B`

```text
    4055: Q: The school has 14 boys and 10 girls. If 4 boys and 3 girls drop out, how
    4056: many boys and girls are left?
>>> 4057: A: Let’s think step by step. There are 14 boys - 4 boys = 10 boys left. There are
    4058: 10 girls - 3 girls = 7 girls left. In total there are 10 boys + 7 girls = 17 boys and
    4059: girls left. The answer is 17.
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4058 | **Candidates:** `10.0B, 17.0B`

```text
    4056: many boys and girls are left?
    4057: A: Let’s think step by step. There are 14 boys - 4 boys = 10 boys left. There are
>>> 4058: 10 girls - 3 girls = 7 girls left. In total there are 10 boys + 7 girls = 17 boys and
    4059: girls left. The answer is 17.
    4060: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4062 | **Candidates:** `4.0B`

```text
    4060: 
    4061: Q: Building one birdhouse requires 7 planks and 20 nails. If 1 nail costs 0.05,
>>> 4062: and one plank costs 3, what is the cost, in dollars, to build 4 birdhouses?
    4063: A: Let’s think step by step. The cost of the planks for one birdhouse is 7 * 3 =
    4064: 21. And the nails are a cost of 20 * 0.05 = 1 for each birdhouse. So to build one
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4065 | **Candidates:** `4.0B`

```text
    4063: A: Let’s think step by step. The cost of the planks for one birdhouse is 7 * 3 =
    4064: 21. And the nails are a cost of 20 * 0.05 = 1 for each birdhouse. So to build one
>>> 4065: birdhouse one will need 21 + 1 = 22. So the cost of building 4 birdhouses is at 4
    4066: * 22 = 88. The answer is 88.
    4067: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4077 | **Candidates:** `0.027B`

```text
    4075: 
    4076: Q: Angela is a bike messenger in New York. She needs to deliver 8 times
>>> 4077: as many packages as meals. If she needs to deliver 27 meals and packages
    4078: combined, how many meals does she deliver?
    4079: A: Let’s think step by step. Let p be the number of packages Angela delivers and
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4080 | **Candidates:** `0.008B`

```text
    4078: combined, how many meals does she deliver?
    4079: A: Let’s think step by step. Let p be the number of packages Angela delivers and
>>> 4080: m be the number of meals. We know that p + m = 27 and p = 8m. Substituting
    4081: the second equation into the first equation, we get 8m + m = 27. Combining
    4082: like terms, we get 9m = 27. Dividing both sides by 9, we get m = 3. The answer
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4081 | **Candidates:** `0.008B`

```text
    4079: A: Let’s think step by step. Let p be the number of packages Angela delivers and
    4080: m be the number of meals. We know that p + m = 27 and p = 8m. Substituting
>>> 4081: the second equation into the first equation, we get 8m + m = 27. Combining
    4082: like terms, we get 9m = 27. Dividing both sides by 9, we get m = 3. The answer
    4083: is 3.
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4082 | **Candidates:** `0.009B`

```text
    4080: m be the number of meals. We know that p + m = 27 and p = 8m. Substituting
    4081: the second equation into the first equation, we get 8m + m = 27. Combining
>>> 4082: like terms, we get 9m = 27. Dividing both sides by 9, we get m = 3. The answer
    4083: is 3.
    4084: 
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4091 | **Candidates:** `0.004B`

```text
    4089: years old. The answer is 19.
    4090: 
>>> 4091: Q: Indras has 6 letters in her name. Her sister’s name has 4 more letters than
    4092: half of the letters in Indras’ name. How many letters are in Indras and her
    4093: sister’s names?
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4362 | **Candidates:** `0.003B`

```text
    4360: Do you know how many kinds of earthworms there are?There are about 1800
    4361: kinds in the world! They can be brown,purple,green.They can be as small as 3
>>> 4362: cm long and as large as 3 m long.
    4363: The best time to see earthworms is at night,especially a cool,damp night.That’s
    4364: when they come up from their burrows to hunt for food.Earthworms don’t
```

---

### File: `DeepSeek_V3_V3_2_papers_https_arxiv_org_abs_2405_04434_2405.04434.md`
**Line:** 4427 | **Candidates:** `1966.0B`

```text
    4425: A: Muumi
    4426: Q: "What English model, with her short-haired androgynous look, born Lesley
>>> 4427: Hornby, was discovered in 1966 by Nigel Davies when she was 16 and weighed
    4428: 6 stone (41 kg, 91 lbs), and became ""The Face of ’66"" with her high fashion
    4429: mod look created by Mary Quant?"
```

---

## ID: A7
### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 44 | **Candidates:** `0.001B`

```text
    42: Albert Gu∗1 and Tri Dao∗2
    43: 
>>> 44: 1Machine Learning Department, Carnegie Mellon University
    45: 2Department of Computer Science, Princeton University
    46: agu@cs.cmu.edu, tri@tridao.me
```

---

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
**Line:** 124 | **Candidates:** `0.001B`

```text
    122: scales linearly in sequence length during training, and unrolling the model autoregressively during inference requires only
    123: constant time per step since it does not require a cache of previous elements. (iii) Long context: the quality and efficiency
>>> 124: together yield performance improvements on real data up to sequence length 1M.
    125: 
    126: We empirically validate Mamba’s potential as a general sequence FM backbone, in both pretraining quality and domain-
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
**Line:** 141 | **Candidates:** `3.0B, 7.0B`

```text
    139: on LLaMa (Touvron et al. 2023). Our Mamba language model has 5× generation throughput compared to Transformers
    140: of similar size, and Mamba-3B’s quality matches that of Transformers twice its size (e.g. 4 points higher avg. on common
>>> 141: sense reasoning compared to Pythia-3B and even exceeding Pythia-7B).
    142: 
    143: Model code and pre-trained checkpoints are open-sourced at https://github.com/state-spaces/mamba.
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 161 | **Candidates:** `0.004B`

```text
    159: 1-dimensional function or sequence 𝑥 (𝑡) ∈ R ↦→ 𝑦 (𝑡) ∈ R through an implicit latent state ℎ(𝑡) ∈ R𝑁 .
    160: 
>>> 161: Concretely, S4 models are defined with four parameters (Δ, 𝑨, 𝑩, 𝑪), which define a sequence-to-sequence transformation
    162: in two stages.
    163: 
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 169 | **Candidates:** `1.0B`

```text
    167: (1a)
    168: 
>>> 169: (1b)
    170: 
    171: ℎ𝑡 = 𝑨ℎ𝑡 −1 + 𝑩𝑥𝑡
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 176 | **Candidates:** `2.0B`

```text
    174: (2a)
    175: 
>>> 176: (2b)
    177: 
    178: 𝑘
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 186 | **Candidates:** `3.0B`

```text
    184: (3a)
    185: 
>>> 186: (3b)
    187: 
    188: Discretization. The first stage transforms the “continuous parameters” (Δ, 𝑨, 𝑩) to “discrete parameters” (𝑨, 𝑩) through
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 219 | **Candidates:** `3.0B`

```text
    217: ProjectDiscretize𝑥!ℎ!"#ℎ!𝑦!𝐴𝐶!𝐵!Selection MechanismGPU SRAMGPU HBM∆!Selective State Space ModelwithHardware-aware State Expansion
    218: called linear time invariance (LTI), which is deeply connected to recurrence and convolutions. Informally, we think of
>>> 219: LTI SSMs as being equivalent to any linear recurrence (2a) or convolution (3b), and use LTI as an umbrella term for these
    220: classes of models.
    221: 
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 244 | **Candidates:** `0.004B`

```text
    242: convolutional) models at large (deep learning).
    243: 
>>> 244: Throughout this entire paper we use the term “SSM” to refer exclusively to the class of structured SSMs or S4 models (Gu,
    245: Goel, and Ré 2022; Gu, Gupta, et al. 2022; Gupta, Gu, and Berant 2022; Hasani et al. 2023; Ma et al. 2023; Smith, Warrington,
    246: and Linderman 2023) and use these terms interchangeably. For convenience we may also include derivatives of such
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 264 | **Candidates:** `3.0B`

```text
    262: shift-SSM, before the main SSM layer.
    263: 
>>> 264: • Hyena (Poli et al. 2023) uses the same architecture as H3 but replaces the S4 layer with an MLP-parameterized global
    265: 
    266: convolution (Romero et al. 2021).
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 291 | **Candidates:** `0.003B`

```text
    289: even MLP blocks (Section 3.4). Finally, we discuss some additional properties of selection mechanisms (Section 3.5).
    290: 
>>> 291: 3.1 Motivation: Selection as a Means of Compression
    292: We argue that a fundamental problem of sequence modeling is compressing context into a smaller state. In fact, we can
    293: view the tradeoffs of popular sequence models from this point of view. For example, attention is both effective and
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 388 | **Candidates:** `0.003B`

```text
    386: used LTI (non-selective) models, most commonly in the form of global convolutions.
    387: 
>>> 388: 3.3.1 Motivation of Prior Models
    389: 
    390: We first revisit this motivation and overview our approach to overcome limitations of prior methods.
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 393 | **Candidates:** `0.001B`

```text
    391: 
    392: • At a high level, recurrent models such as SSMs always balance a tradeoff between expressivity and speed: as discussed in
>>> 393: Section 3.1, models with larger hidden state dimension should be more effective but slower. Thus we want to maximize
    394: hidden state dimension without paying speed and memory costs.
    395: 
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 469 | **Candidates:** `3.0B`

```text
    467: 
    468: 
>>> 469: Figure 3: (Architecture.) Our simplified block design combines the H3 block, which is the basis of most SSM architectures, with
    470: the ubiquitous MLP block of modern neural networks. Instead of interleaving these two blocks, we simply repeat the Mamba block
    471: homogenously. Compared to the H3 block, Mamba replaces the first multiplicative gate with an activation function. Compared to
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 471 | **Candidates:** `3.0B`

```text
    469: Figure 3: (Architecture.) Our simplified block design combines the H3 block, which is the basis of most SSM architectures, with
    470: the ubiquitous MLP block of modern neural networks. Instead of interleaving these two blocks, we simply repeat the Mamba block
>>> 471: homogenously. Compared to the H3 block, Mamba replaces the first multiplicative gate with an activation function. Compared to
    472: the MLP block, Mamba adds an SSM to the main branch. For 𝜎 we use the SiLU / Swish activation (Hendrycks and Gimpel 2016;
    473: Ramachandran, Zoph, and Quoc V Le 2017).
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 569 | **Candidates:** `0.006B`

```text
    567: Δ (Uniform([0.001, 0.1])),
    568: 
>>> 569: Remark 3.1. For brevity in our experimental results, we sometimes abbreviate selective SSMs as S6 models, because they are
    570: S4 models with a selection mechanism and computed with a scan.
    571: 
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 570 | **Candidates:** `0.004B`

```text
    568: 
    569: Remark 3.1. For brevity in our experimental results, we sometimes abbreviate selective SSMs as S6 models, because they are
>>> 570: S4 models with a selection mechanism and computed with a scan.
    571: 
    572: 9
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
**Line:** 759 | **Candidates:** `0.13B`

```text
    757: Token.
    758: 
>>> 759: Hybrid H3-130M GPT2
    760: NeoX
    761: Pythia-160M
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 761 | **Candidates:** `0.16B`

```text
    759: Hybrid H3-130M GPT2
    760: NeoX
>>> 761: Pythia-160M
    762: NeoX
    763: Mamba-130M
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 763 | **Candidates:** `0.13B`

```text
    761: Pythia-160M
    762: NeoX
>>> 763: Mamba-130M
    764: 
    765: Hybrid H3-360M GPT2
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 765 | **Candidates:** `0.36B`

```text
    763: Mamba-130M
    764: 
>>> 765: Hybrid H3-360M GPT2
    766: NeoX
    767: Pythia-410M
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 767 | **Candidates:** `0.41B`

```text
    765: Hybrid H3-360M GPT2
    766: NeoX
>>> 767: Pythia-410M
    768: NeoX
    769: Mamba-370M
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 769 | **Candidates:** `0.37B`

```text
    767: Pythia-410M
    768: NeoX
>>> 769: Mamba-370M
    770: 
    771: Pythia-1B
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 771 | **Candidates:** `1.0B`

```text
    769: Mamba-370M
    770: 
>>> 771: Pythia-1B
    772: Mamba-790M
    773: 
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 772 | **Candidates:** `0.79B`

```text
    770: 
    771: Pythia-1B
>>> 772: Mamba-790M
    773: 
    774: GPT-Neo 1.3B
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 774 | **Candidates:** `1.3B`

```text
    772: Mamba-790M
    773: 
>>> 774: GPT-Neo 1.3B
    775: Hybrid H3-1.3B
    776: OPT-1.3B
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 775 | **Candidates:** `1.3B`

```text
    773: 
    774: GPT-Neo 1.3B
>>> 775: Hybrid H3-1.3B
    776: OPT-1.3B
    777: Pythia-1.4B
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 776 | **Candidates:** `1.3B`

```text
    774: GPT-Neo 1.3B
    775: Hybrid H3-1.3B
>>> 776: OPT-1.3B
    777: Pythia-1.4B
    778: RWKV-1.5B
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 777 | **Candidates:** `1.4B`

```text
    775: Hybrid H3-1.3B
    776: OPT-1.3B
>>> 777: Pythia-1.4B
    778: RWKV-1.5B
    779: Mamba-1.4B
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 778 | **Candidates:** `1.5B`

```text
    776: OPT-1.3B
    777: Pythia-1.4B
>>> 778: RWKV-1.5B
    779: Mamba-1.4B
    780: 
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 779 | **Candidates:** `1.4B`

```text
    777: Pythia-1.4B
    778: RWKV-1.5B
>>> 779: Mamba-1.4B
    780: 
    781: GPT-Neo 2.7B
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 781 | **Candidates:** `2.7B`

```text
    779: Mamba-1.4B
    780: 
>>> 781: GPT-Neo 2.7B
    782: Hybrid H3-2.7B
    783: OPT-2.7B
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 782 | **Candidates:** `2.7B`

```text
    780: 
    781: GPT-Neo 2.7B
>>> 782: Hybrid H3-2.7B
    783: OPT-2.7B
    784: Pythia-2.8B
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 783 | **Candidates:** `2.7B`

```text
    781: GPT-Neo 2.7B
    782: Hybrid H3-2.7B
>>> 783: OPT-2.7B
    784: Pythia-2.8B
    785: RWKV-3B
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 784 | **Candidates:** `2.8B`

```text
    782: Hybrid H3-2.7B
    783: OPT-2.7B
>>> 784: Pythia-2.8B
    785: RWKV-3B
    786: Mamba-2.8B
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 785 | **Candidates:** `3.0B`

```text
    783: OPT-2.7B
    784: Pythia-2.8B
>>> 785: RWKV-3B
    786: Mamba-2.8B
    787: 
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 786 | **Candidates:** `2.8B`

```text
    784: Pythia-2.8B
    785: RWKV-3B
>>> 786: Mamba-2.8B
    787: 
    788: GPT-J-6B
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 788 | **Candidates:** `6.0B`

```text
    786: Mamba-2.8B
    787: 
>>> 788: GPT-J-6B
    789: OPT-6.7B
    790: Pythia-6.9B
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 789 | **Candidates:** `6.7B`

```text
    787: 
    788: GPT-J-6B
>>> 789: OPT-6.7B
    790: Pythia-6.9B
    791: RWKV-7.4B
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 790 | **Candidates:** `6.9B`

```text
    788: GPT-J-6B
    789: OPT-6.7B
>>> 790: Pythia-6.9B
    791: RWKV-7.4B
    792: 
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 791 | **Candidates:** `7.4B`

```text
    789: OPT-6.7B
    790: Pythia-6.9B
>>> 791: RWKV-7.4B
    792: 
    793: NeoX
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 1116 | **Candidates:** `4.5B`

```text
    1114: For pretraining, we largely follow a standard causal language modeling (next token prediction) setup for the training and
    1115: model details (see also Appendix E.2). For the dataset, we largely follow the setup of HyenaDNA (Nguyen, Poli, et al. 2023),
>>> 1116: which uses the HG38 dataset for pretraining consisting of a single human genome with about 4.5 billion tokens (DNA base
    1117: pairs) in the training split.
    1118: 
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
**Line:** 1153 | **Candidates:** `0.001B`

```text
    1151: Figure 5 (Right) shows that Mamba is able to make use of longer context even up to extremely long
    1152: Results.
>>> 1153: sequences of length 1M, and its pretraining perplexity improves as the context increases. On the other hand, the
    1154: HyenaDNA model gets worse with sequence length. This is intuitive from the discussion in Section 3.5 on properties of the
    1155: selection mechanism. In particular, LTI models cannot selectively ignore information; from a convolutional perspective, a
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 1271 | **Candidates:** `0.035B`

```text
    1269: Test
    1270: 
>>> 1271: 35.0M
    1272: 4.2M
    1273: 5.8M
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 1272 | **Candidates:** `0.004B`

```text
    1270: 
    1271: 35.0M
>>> 1272: 4.2M
    1273: 5.8M
    1274: 
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 1273 | **Candidates:** `0.006B`

```text
    1271: 35.0M
    1272: 4.2M
>>> 1273: 5.8M
    1274: 
    1275: 19.1M
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 1275 | **Candidates:** `0.019B`

```text
    1273: 5.8M
    1274: 
>>> 1275: 19.1M
    1276: 24.1M
    1277: 23.0M
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 1276 | **Candidates:** `0.024B`

```text
    1274: 
    1275: 19.1M
>>> 1276: 24.1M
    1277: 23.0M
    1278: 
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 1277 | **Candidates:** `0.023B`

```text
    1275: 19.1M
    1276: 24.1M
>>> 1277: 23.0M
    1278: 
    1279: 6.1M
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 1279 | **Candidates:** `0.006B`

```text
    1277: 23.0M
    1278: 
>>> 1279: 6.1M
    1280: 24.3M
    1281: 
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 1280 | **Candidates:** `0.024B`

```text
    1278: 
    1279: 6.1M
>>> 1280: 24.3M
    1281: 
    1282: -
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 1361 | **Candidates:** `0.006B, 0.009B`

```text
    1359: 0.19
    1360: 
>>> 1361: Table 5: (SC09 Model Ablations) Models with 6M parameters. In
    1362: SaShiMi’s U-Net backbone, there are 8 center blocks operating on
    1363: sequence length 1000, sandwiched on each side by 8 outer blocks on
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 1365 | **Candidates:** `40.0B`

```text
    1363: sequence length 1000, sandwiched on each side by 8 outer blocks on
    1364: sequence length 4000, sandwiched by 8 outer blocks on sequence
>>> 1365: length 16000 (40 blocks total). The architecture of the 8 center
    1366: blocks are ablated independently of the rest. Note that Transformers
    1367: (MHA+MLP) were not tested in the more important outer blocks
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
**Line:** 1439 | **Candidates:** `1.3B`

```text
    1437: in PyTorch. Mamba achieves 4-5× higher inference throughput than a Transformer of similar size, since without the
    1438: KV cache it can use much higher batch sizes. For example, a Mamba-6.9B (untrained) would have higher inference
>>> 1439: throughput than a 5× smaller Transformer-1.3B. Details in Appendix E.5, which additionally includes a benchmark of
    1440: memory consumption.
    1441: 
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 1445 | **Candidates:** `0.005B`

```text
    1443: as a recurrent model, Mamba can achieve 5× higher throughput than Transformers.
    1444: 
>>> 1445: 4.6 Model Ablations
    1446: We perform a series of detailed ablations on components of our model, focusing on the setting of language modeling with
    1447: size ≈ 350M models at Chinchilla token counts (same setting as Figure 4).
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
**Line:** 2308 | **Candidates:** `0.004B`

```text
    2306: 
    2307: • S5 (Smith, Warrington, and Linderman 2023) independently discovered the diagonal SSM approximation, and is the
>>> 2308: first S4 model to be computed recurrently with the parallel scan. However, this required lowering the effective state
    2309: dimension, which they accomplished by switching the SSM dimensions from a SISO (single-input single-output) to
    2310: MIMO (multi-input multi-output) formulation. Our proposed S6 shares the scan, but differs by (i) keeping the SISO
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 2363 | **Candidates:** `3.0B`

```text
    2361: (indeed, the Selective Copying task can even be viewed as coming pre-masked if the noise tokens are embedded to 0).
    2362: 
>>> 2363: • RetNet (Y. Sun et al. 2023) is also based on Linear Attention and very similar to H3, but reduces the inner S4 layer to a
    2364: special case where the state dimension is 𝑁 = 1. Although not framed as such, its recurrence can be viewed as a special
    2365: case of a linear SSM.
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 2369 | **Candidates:** `3.0B`

```text
    2367: Its primary source of improvement is using a linear attention with large head dimension, which can be viewed as another
    2368: method to perform input-dependent state expansion. Using a larger head dimension in the context of linear attention
>>> 2369: variants was first done by H3, but not extensively used since this requires a proportional amount of extra computation.
    2370: RetNet avoids this with an alternate way to parallelize the computation with a variant of standard multi-head attention
    2371: instead of convolutions, made feasible by their particular special case of SSMs which acts as a simple EMA.
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 2436 | **Candidates:** `0.001B`

```text
    2434: 
    2435: • Recurrent Memory Transformer (Bulatov, Kuratov, and Burtsev 2023), a lightweight wrapper around a Transformer
>>> 2436: backbone. It showed ability to generalize up to 1M sequences but only on synthetic memorization tasks; their main result
    2437: is similar to our Induction Heads extrapolation experiment (Table 2).
    2438: 
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
**Line:** 2441 | **Candidates:** `0.001B`

```text
    2439: • LongNet (Ding et al. 2023), which claimed to scale to 1B length but only evaluated on length < 100𝐾 for actual tasks.
    2440: 
>>> 2441: • Hyena and HyenaDNA (Nguyen, Poli, et al. 2023; Poli et al. 2023), which claimed to leverage up to 1M context. How-
    2442: ever, their experiments trained on proportionally more data at longer contexts, making it hard to conclude if quality
    2443: improvements at 1M context are due to context length or due to more data and computation.
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 2443 | **Candidates:** `0.001B`

```text
    2441: • Hyena and HyenaDNA (Nguyen, Poli, et al. 2023; Poli et al. 2023), which claimed to leverage up to 1M context. How-
    2442: ever, their experiments trained on proportionally more data at longer contexts, making it hard to conclude if quality
>>> 2443: improvements at 1M context are due to context length or due to more data and computation.
    2444: 
    2445: • Sparse Transformer (Child et al. 2019) showed a proof-of-concept of using a strided sparse attention Transformer to
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 2569 | **Candidates:** `0.069B`

```text
    2567: 137K
    2568: 153K
>>> 2569: 69M∗
    2570: 74K
    2571: 
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 2705 | **Candidates:** `12.0B, 20.0B`

```text
    2703: 
    2704: optimized Transformer implementation with FlashAttention. In particular, each attention layer (FlashAttention) stores
>>> 2705: around 12 bytes of activations per token, an each MLP layer stores around 20 bytes of activations per token, for a total of
    2706: 32 bytes ((assuming mixed-precision training in FP16 or BF16)). Each selective SSM stores around 16 bytes of activations
    2707: per token. Hence two layers of selective SSMs have around the same activation memory as an attention layer and an MLP
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 2706 | **Candidates:** `16.0B, 32.0B`

```text
    2704: optimized Transformer implementation with FlashAttention. In particular, each attention layer (FlashAttention) stores
    2705: around 12 bytes of activations per token, an each MLP layer stores around 20 bytes of activations per token, for a total of
>>> 2706: 32 bytes ((assuming mixed-precision training in FP16 or BF16)). Each selective SSM stores around 16 bytes of activations
    2707: per token. Hence two layers of selective SSMs have around the same activation memory as an attention layer and an MLP
    2708: layer.
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
**Line:** 2768 | **Candidates:** `0.125B`

```text
    2766: Tokens
    2767: 
>>> 2768: 125M
    2769: 350M
    2770: 760M
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 2769 | **Candidates:** `0.35B`

```text
    2767: 
    2768: 125M
>>> 2769: 350M
    2770: 760M
    2771: 1.3B
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 2770 | **Candidates:** `0.76B`

```text
    2768: 125M
    2769: 350M
>>> 2770: 760M
    2771: 1.3B
    2772: 
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 2771 | **Candidates:** `1.3B`

```text
    2769: 350M
    2770: 760M
>>> 2771: 1.3B
    2772: 
    2773: 12
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 2803 | **Candidates:** `2.5B`

```text
    2801: 0.5M tokens
    2802: 
>>> 2803: 2.5B
    2804: 7B
    2805: 15B
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 2804 | **Candidates:** `7.0B`

```text
    2802: 
    2803: 2.5B
>>> 2804: 7B
    2805: 15B
    2806: 26B
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 2805 | **Candidates:** `15.0B`

```text
    2803: 2.5B
    2804: 7B
>>> 2805: 15B
    2806: 26B
    2807: 
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 2806 | **Candidates:** `26.0B`

```text
    2804: 7B
    2805: 15B
>>> 2806: 26B
    2807: 
    2808: • gradient clip value 1.0
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 2835 | **Candidates:** `3.0B`

```text
    2833: SwiGLU MLP (Shazeer 2020), and the improved training recipe above.
    2834: 
>>> 2835: • Hyena: Interleaving a Hyena block (the H3 block with S4 replaced by a global convolution parameterized by an MLP) with
    2836: standard MLP blocks. The MLP blocks have expansion factor 2 instead of 4 and the number of layers is correspondingly
    2837: increased by 1.5× to preserve parameter count.
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
**Line:** 2954 | **Candidates:** `4.5B`

```text
    2952: 
    2953: The dataset follows the splits from the prior Enformer work on genomics (Avsec et al. 2021); the training split contains a
>>> 2954: total of 𝑆 = 34021 segments of length 217 = 131072 that cover the genome, for a total of approximately 4.5 billion tokens
    2955: (DNA base pairs). These segments are pairs of (chromosome number, starting index, ending index), and can be extended if
    2956: necessary (e.g. to get longer segments).
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 2985 | **Candidates:** `3.0B`

```text
    2983: • HyenaDNA: the Hyena model from Nguyen, Poli, et al. (2023) and Poli et al. (2023), which is roughly a Transformer with
    2984: 
>>> 2985: the MHA block replaced by an H3 block using a global convolution parameterized by an MLP.
    2986: 
    2987: • Mamba: the standard Mamba architecture.
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 3014 | **Candidates:** `0.001B, 0.004B, 0.007B, 0.019B, 0.041B`

```text
    3012: 512
    3013: 
>>> 3014: 250K 700K 1.4M 3.5M 7.0M 19.3M 40.7M
    3015: 
    3016: Note that the number of blocks for Mamba is doubled, because one Transformer “layer” includes both the MHA and MLP
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 3072 | **Candidates:** `0.004B`

```text
    3070: warmup with 1 epoch at length 214 = 16384, 1 epoch at length 215 = 32768, 1 epoch at length 216 = 65536, and so on up to
    3071: the maximum sequence length. For example, the model with 220 = 1048576 context undergoes 6 epochs of sequence length
>>> 3072: warmup before 4 more epochs at its maximum sequence length.
    3073: 
    3074: The learning rate for all Hyena models is 4e − 5, while the learning rate for all Mamba models is 1e − 4. These were found
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 3106 | **Candidates:** `0.001B`

```text
    3104: 220
    3105: 
>>> 3106: HyenaDNA 1.4M
    3107: 1.4M
    3108: Mamba
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 3107 | **Candidates:** `0.001B`

```text
    3105: 
    3106: HyenaDNA 1.4M
>>> 3107: 1.4M
    3108: Mamba
    3109: 
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 3127 | **Candidates:** `0.007B`

```text
    3125: Mamba
    3126: 
>>> 3127: 7M
    3128: 
    3129: 30.00
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 3185 | **Candidates:** `3.0B`

```text
    3183: 
    3184: E.4.1 YouTubeMix Audio Pretraining
>>> 3185: Model. We use a model with 3 blocks per stage (3 × 5 = 15 total Mamba blocks), pooling factor 𝑝 = 16, and outer
    3186: dimension 𝐷 = 64, for about 3.5M parameters.
    3187: 
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
**Line:** 3188 | **Candidates:** `8.0B`

```text
    3186: dimension 𝐷 = 64, for about 3.5M parameters.
    3187: 
>>> 3188: Dataset. The data is mu-law encoded at 8 bits, so the model is modeling discrete tokens with a vocab size of 256.
    3189: The dataset consists of clips of up to 1 minute long, or length 960000, which is subsampled and divided into segments of any
    3190: desired sequence length. Since the architecture involves two stages of pooling by a factor of 16, and we want the resulting
```

---

### File: `Gu_et_al_2023_https_arxiv_org_abs_2312_00752_2312.00752.md`
**Line:** 3189 | **Candidates:** `0.001B`

```text
    3187: 
    3188: Dataset. The data is mu-law encoded at 8 bits, so the model is modeling discrete tokens with a vocab size of 256.
>>> 3189: The dataset consists of clips of up to 1 minute long, or length 960000, which is subsampled and divided into segments of any
    3190: desired sequence length. Since the architecture involves two stages of pooling by a factor of 16, and we want the resulting
    3191: sequence length to be a a multiple of 8 for hardware efficiency, the longest possible sequence is 468 × 2048 = 958464. The
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
**Line:** 3270 | **Candidates:** `0.125B`

```text
    3268:  1 E Q F E  7  
    3269: 
>>> 3270: Table 15: (Memory benchmark.) Mamba’s memory footprint is comparable to the most optimized Transformer. Results for 125M
    3271: models.
    3272: 
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
**Line:** 83 | **Candidates:** `0.001B`

```text
    81: ash-linear-attention
    82: 
>>> 83: *Equal contribution 1Massachusetts Institute of Technology
    84: 2MIT-IBM Watson AI Lab. Correspondence to: Songlin Yang
    85: <yangsl66@mit.edu>, Bailin Wang <bailinw@mit.edu>.
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 84 | **Candidates:** `0.002B`

```text
    82: 
    83: *Equal contribution 1Massachusetts Institute of Technology
>>> 84: 2MIT-IBM Watson AI Lab. Correspondence to: Songlin Yang
    85: <yangsl66@mit.edu>, Bailin Wang <bailinw@mit.edu>.
    86: 
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 117 | **Candidates:** `2022.0B`

```text
    115: for linear attention are not I/O aware and thus, in practice,
    116: slower than optimized implementations of softmax attention
>>> 117: (Dao et al., 2022b; Dao, 2023) on moderate sequence lengths.
    118: 
    119: From a performance standpoint, linear attention has gener-
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 124 | **Candidates:** `2023.0B`

```text
    122: et al., 2021). Recent variants of linear attention such as
    123: RetNet (Sun et al., 2023a) and TransNormerLLM (Qin et al.,
>>> 124: 2023b) obtain significant improvements by multiplying
    125: the current hidden state with a decay factor before the
    126: RNN update. However, these works use a global, data-
```

---

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
**Line:** 163 | **Candidates:** `2.0B`

```text
    161: has significantly higher throughput than a similarly sized
    162: Mamba model.
>>> 163: 2 Background: Linear Attention
    164: We first give a brief background on linear attention layers.
    165: For notation we use bold upper-case letters for matrices (e.g.,
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 253 | **Candidates:** `0.001B`

```text
    251: (1)
    252: 
>>> 253: Eq. 1 makes it clear that a linear attention layer is essentially a
    254: linear recurrent layer with matrix-valued hidden states St that
    255: t vt = (xtWK)T(xtWV ).1
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 356 | **Candidates:** `2022.0B`

```text
    354: We describe FLASHLINEARATTENTION, an I/O-aware,
    355: hardware-efficient algorithm for linear attention in the spirit
>>> 356: of FLASHATTENTION (Dao et al., 2022b; Dao, 2023). We
    357: first discuss aspects of hardware that should be taken into
    358: account for a practically efficient implementation.
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 468 | **Candidates:** `2023.0B`

```text
    466: Parallel form. The parallel form could be as efficient
    467: as FLASHATTENTION using similar I/O optimization
>>> 468: techniques, as demonstrated by Qin et al. (2023b). However,
    469: the high number of FLOPs (due to the quadratic complexity)
    470: makes the long-sequence training expensive, the same issue
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 672 | **Candidates:** `2023.0B`

```text
    670: instability of linear attention in long-context tasks (Buckman
    671: & Gelada, 2024). Recent works (Sun et al., 2023a; Qin et al.,
>>> 672: 2023b) obtain better performance through incorporating
    673: a global, non-data-dependent decay factor3 γ ∈ (0,1) into
    674: linear attention: St = γSt−1 + kT
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 741 | **Candidates:** `2024.0B`

```text
    739: GateLoop (Katsch, 2023)
    740: Gt = αT
>>> 741: HGRN-2 (Qin et al., 2024b)
    742: Gt = αT
    743: RWKV-6 (Peng et al., 2024)
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 818 | **Candidates:** `2024.0B`

```text
    816: followed by sigmoid on xt (see §4.4). Note that the above
    817: formulation is general and encompasses several recent RNNs
>>> 818: (Katsch, 2023; Qin et al., 2024b; Peng et al., 2024). Thus,
    819: the hardware-efficient GLA implementation (described next)
    820: could be directly used or adapted to other models.
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 990 | **Candidates:** `2023.0B`

```text
    988: 
    989: 6This form resembles extrapolatable position encoding (Sun
>>> 990: et al., 2023b) in that the term inside the exponential can be viewed
    991: as a data-dependent relative position factor.
    992: 
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 1068 | **Candidates:** `2022.0B`

```text
    1066: scheme, where a chunk is further divided into sub-chunks
    1067: (i.e., another level of tiling) in the spirit of classic tiling
>>> 1068: techniques (Dao et al., 2022b). The attention-like matrix
    1069: P ∈ RL×L is then computed in a chunkwise manner, as
    1070: illustrated in Figure 3. Concretely, the interactions between
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
**Line:** 1331 | **Candidates:** `15.0B`

```text
    1329: Table 2: GLA Transformer results against Transformer++ (Touvron et al., 2023), RetNet (Sun et al., 2023a), and Mamba (Gu & Dao, 2023).
    1330: All models are trained on the same subset of the SlimPajama dataset with the Mistral tokenizer. The 340M/1.3B models are trained for
>>> 1331: 15B/100B tokens respectively. The individual task performance is via zero-shot. We report the main results on the same set of tasks reported
    1332: by Gu & Dao (2023). See Appendix D for results on other benchmarks, including 5-shot results. The last column shows the average over all
    1333: benchmarks that use (normalized) accuracy as the metric.
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 1345 | **Candidates:** `100.0B`

```text
    1343: SlimPajama dataset (Soboleva et al., 2023) and tokenize it
    1344: using the Mistral tokenizer (Jiang et al., 2023). The original
>>> 1345: dataset contains 627B tokens; we use a 100B subset.
    1346: 
    1347: Baselines. We evaluate GLA against three baselines:
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
**Line:** 1365 | **Candidates:** `0.34B, 0.5B, 1.3B`

```text
    1363: models are trained on 100B tokens with a batch size of
    1364: 2M tokens. We use a cosine learning rate schedule with
>>> 1365: a warmup of 0.5B/1B tokens for the 340M/1.3B settings,
    1366: respectively. The initial and final learning rates are 3e-5. We
    1367: use a weight decay of 0.01, and gradient clipping of 1.0.
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 1369 | **Candidates:** `0.005B`

```text
    1367: use a weight decay of 0.01, and gradient clipping of 1.0.
    1368: 
>>> 1369: 5.2 Main Results
    1370: 
    1371: In addition to perplexity (ppl) on Wikitext (Wiki.), we
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 1454 | **Candidates:** `2023.0B`

```text
    1452: The synthetic MQAR task (Arora et al., 2023a) is a more
    1453: challenging multi-query version of the induction head task
>>> 1454: (Fu et al., 2023b) in which a model has to recall the token
    1455: following a query token multiple times. We follow Arora
    1456: et al. (2023a)’s experimental setting and compare GLA
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
**Line:** 1597 | **Candidates:** `2023.0B`

```text
    1595: 
    1596: Following Arora et al. (2024), we also test our models on
>>> 1597: three real recall-intensive tasks: FDA (Arora et al., 2023b),
    1598: SWDE (Lockard et al., 2019), and SQUAD (Rajpurkar et al.,
    1599: 2018). These tasks focus on information extraction or read-
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 1617 | **Candidates:** `1.3B`

```text
    1615: hence this approach has minimal overhead comparable to
    1616: the standard 2K-length training strategy (where the initial
>>> 1617: hidden state is always set to zero). We pretrain 1.3B Mamba,
    1618: 
    1619: 8We split a 24K input sequence into 12 segments. The final state
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 1644 | **Candidates:** `0.34B`

```text
    1642: 
    1643: Ablations. We conduct a small-scale ablation study
>>> 1644: by training the 340M GLA variants for 7B tokens. We
    1645: investigate (i) the importance of having both fine-grained
    1646: and data-dependent gating and (ii) the influence of head
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
**Line:** 1667 | **Candidates:** `2023.0B`

```text
    1665: ter length extrapolation, these methods still have difficulty generaliz-
    1666: ing significantly beyond context lengths seen during training (Press
>>> 1667: et al., 2021; Sun et al., 2023b; Li et al., 2023c).
    1668: 
    1669: 10We use the official implementation for Mamba, the fused ver-
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
**Line:** 1716 | **Candidates:** `7.0B`

```text
    1714: GLA become even more favorable compared to Mamba at
    1715: larger scales. Specifically, when scaled to larger sizes (e.g.,
>>> 1716: > 7B), GLA can be more efficient than Mamba because
    1717: of better use of tensor cores and GLA’s compatibility
    1718: with tensor parallelism.11 Insofar as we are interested in
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 1834 | **Candidates:** `2023.0B`

```text
    1832: training. This simple strategy has been shown to be effective
    1833: in moderate-scale experiments conducted by HGRN (Qin
>>> 1834: et al., 2023b). RWKV-v6 (Peng et al., 2024) and Mamba
    1835: (Gu & Dao, 2023) also use data-dependent decay rates
    1836: that are reminiscent of forget gates. In the context of linear
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 1906 | **Candidates:** `2023.0B`

```text
    1904: A., Trummer, I., and R´e, C. Language Models Enable
    1905: Simple Systems for Generating Structured Views of
>>> 1906: Heterogeneous Data Lakes, April 2023b. URL http:
    1907: //arxiv.org/abs/2304.09433. arXiv:2304.09433 [cs].
    1908: 
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 1920 | **Candidates:** `7.24B`

```text
    1918: Scientific Re-
    1919: benchmark for scholarly knowledge.
>>> 1920: ports, 13(1):7240, May 2023.
    1921: ISSN 2045-2322. doi:
    1922: 10.1038/s41598-023-33607-z.
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 2020 | **Candidates:** `2022.0B`

```text
    2018: Dao, T., Fu, D. Y., Ermon, S., Rudra, A., and R´e, C.
    2019: Flashattention: Fast and memory-efficient exact attention
>>> 2020: with io-awareness. In NeurIPS, 2022b.
    2021: 
    2022: Fu, D. Y., Arora, S., Grogan, J., Johnson, I., Eyuboglu, S.,
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 2031 | **Candidates:** `2023.0B`

```text
    2029: ing with state space models. In The Eleventh International
    2030: Conference on Learning Representations, ICLR 2023, Ki-
>>> 2031: gali, Rwanda, May 1-5, 2023. OpenReview.net, 2023b.
    2032: 
    2033: Fu, D. Y., Epstein, E. L., Nguyen, E., Thomas, A.,
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 2069 | **Candidates:** `2021.0B`

```text
    2067: A., and R’e, C. Combining recurrent, convolutional, and
    2068: continuous-time models with linear state-space layers.
>>> 2069: Neural Information Processing Systems, 2021b. URL
    2070: https://arxiv.org/abs/2110.13985v1.
    2071: 
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 2103 | **Candidates:** `2022.0B`

```text
    2101: Szepesv´ari, C., Niu, G., and Sabato, S. (eds.), Interna-
    2102: tional Conference on Machine Learning, ICML 2022,
>>> 2103: 17-23 July 2022, Baltimore, Maryland, USA, volume
    2104: 162 of Proceedings of Machine Learning Research, pp.
    2105: 9099–9117. PMLR, 2022.
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 2114 | **Candidates:** `7.0B`

```text
    2112: Jiang, A. Q., Sablayrolles, A., Mensch, A., Bamford, C.,
    2113: Chaplot, D. S., Casas, D. d. l., Bressand, F., Lengyel, G.,
>>> 2114: Lample, G., Saulnier, L., et al. Mistral 7b. ArXiv preprint,
    2115: abs/2310.06825, 2023.
    2116: 
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 2164 | **Candidates:** `2023.0B`

```text
    2162: N. (eds.), Proceedings of the 61st Annual Meeting of the
    2163: Association for Computational Linguistics (Volume 1:
>>> 2164: Long Papers), Toronto, Canada, July 2023b. Association
    2165: for Computational Linguistics.
    2166: 
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 2199 | **Candidates:** `3.056B`

```text
    2197: American Chapter of the Association for Computational
    2198: Linguistics: Human Language Technologies, Volume 1
>>> 2199: (Long and Short Papers), pp. 3047–3056, Minneapolis,
    2200: Minnesota, June 2019. Association for Computational
    2201: doi: 10.18653/v1/N19- 1309. URL
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 2235 | **Candidates:** `0.03B`

```text
    2233: nets over sequence length. In 6th International Conference
    2234: on Learning Representations, ICLR 2018, Vancouver,
>>> 2235: BC, Canada, April 30 - May 3, 2018, Conference Track
    2236: Proceedings. OpenReview.net, 2018.
    2237: 
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
**Line:** 2326 | **Candidates:** `2023.0B`

```text
    2324: Y., Lv, B., Yuan, F., Luo, X., et al. Scaling transnormer to
    2325: 175 billion parameters. arXiv preprint arXiv:2307.14995,
>>> 2326: 2023b.
    2327: 
    2328: Qin, Z., Yang, S., and Zhong, Y.
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 2352 | **Candidates:** `2024.0B`

```text
    2350: Qin, Z., Yang, S., Sun, W., Shen, X., Li, D., Sun, W., and
    2351: Zhong, Y. Hgrn2: Gated linear rnns with state expansion.
>>> 2352: arXiv preprint arXiv:2404.07904, 2024b.
    2353: 
    2354: Rae, J. W., Potapenko, A., Jayakumar, S. M., Hillier, C., and
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 2491 | **Candidates:** `627.0B`

```text
    2489: 
    2490: Soboleva, D., Al-Khateeb, F., Myers, R., Steeves, J. R.,
>>> 2491: Hestness, J., and Dey, N. SlimPajama: A 627B token
    2492: cleaned and deduplicated version of RedPajama, 2023.
    2493: 
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 2510 | **Candidates:** `2023.0B`

```text
    2508: Linguistics (Volume 1: Long Papers), ACL 2023,
    2509: Toronto, Canada, July 9-14, 2023, pp. 14590–14604.
>>> 2510: Association for Computational Linguistics, 2023b. doi:
    2511: 10.18653/V1/2023.ACL-LONG.816.
    2512: 
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 2541 | **Candidates:** `2024.0B`

```text
    2539: Wang, J., Gangavarapu, T., Yan, J. N., and Rush, A. M.
    2540: Mambabyte: Token-free selective state space model.
>>> 2541: arXiv preprint arXiv:2401.13660, 2024b.
    2542: 
    2543: 14
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 2558 | **Candidates:** `2023.0B`

```text
    2556: et al., 2021; Zhang et al., 2024; Kacham et al., 2023) or simply an identity map (Mao, 2022). ϕ2 is often an element-wise
    2557: (activation) function that makes the resulting ϕ a positive feature map, such as 1+elu (Katharopoulos et al., 2020), ReLU
>>> 2558: (Kasai et al., 2021), exp(·) (Zhang et al., 2024; Choromanski et al., 2021). Some work (Qin et al., 2023b; Sun et al., 2023a;
    2559: Mao, 2022) suggests that a positive feature map might not be necessary.
    2560: 
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 2579 | **Candidates:** `0.002B`

```text
    2577: that directly increasing dkey is effective (Sun et al., 2023a; Mao, 2022; Zhang & Cai, 2022); however, the total parameters
    2578: are hard to control with the increase of dkey. Parameter-efficient methods often keep dkey intact and increase ddot instead.
>>> 2579: Higher order polynomial kernels with order p ≥ 2 map dkey to a much higher ddot = O(dp
    2580: key) (Arora et al., 2023a; Kacham
    2581: et al., 2023). Schlag et al. (2021) propose the Deterministic Parameter-Free Projection (DPFP), while Pramanik et al. (2023)
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 2620 | **Candidates:** `2021.0B`

```text
    2618: for efficient sequence modeling has also been studied in works such as Dynamic Convolution (Wu et al., 2019), Long Convolu-
    2619: tion (Fu et al., 2023c; Qin et al., 2023a; Poli et al., 2023; Massaroli et al., 2023; Li et al., 2023d; Romero et al., 2021), and State
>>> 2620: Space Models (Gu et al., 2021a; Gupta & Berant, 2022; Gu et al., 2021b; Hasani et al., 2022; Smith et al., 2023; Ma et al., 2023).
    2621: 
    2622: A.2 Sequence parallelism
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 2626 | **Candidates:** `2023.0B`

```text
    2624: The chunk-wise parallel form of linear Transformers resembles the two-stage parallel prefix sum (or parallel scan) algorithm
    2625: (Blelloch, 1990), which also combine chunk-wise parallel computations with inter-chunk communication (Chaurasia et al.,
>>> 2626: 2015). It also resembles sequence parallelism used for accelerating attention-based Transformers (Li et al., 2023b), which has
    2627: recently received much attention for long-sequence modeling (Liu et al., 2023; Li et al., 2023a; Brandon et al., 2023). Sequence-
    2628: level parallelism also constitutes the main improvement of FlashAttention-2 (Dao, 2023) over FlashAttention-1 (Dao et al.,
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 2629 | **Candidates:** `2022.0B`

```text
    2627: recently received much attention for long-sequence modeling (Liu et al., 2023; Li et al., 2023a; Brandon et al., 2023). Sequence-
    2628: level parallelism also constitutes the main improvement of FlashAttention-2 (Dao, 2023) over FlashAttention-1 (Dao et al.,
>>> 2629: 2022b). The main differences between these works are that (i) the chunk-level parallel form of linear Transformer needs only
    2630: a single pass due to the linear complexity, while the sequence parallelism in Transformers needs L/C passes (i.e., left-to-right
    2631: scan of key/value blocks for each query block) due to the inherent quadratic complexity, and (ii) the order of matrix multiplica-
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 2730 | **Candidates:** `2022.0B`

```text
    2728: can better align butterfly operators to GPUs. In practice it is important to reduce HBM I/O cost using techniques such as
    2729: tiling and recomputation and leverage tensor cores as much as possible. Our FLASHLINEARATTENTION is similar in spirit
>>> 2730: to FLASHATTENTION (Dao et al., 2022b; Dao, 2023) and FLASHCONVFFT (Fu et al., 2023d), which implement I/O-aware
    2731: versions of neural network layers to enable practical wallclock speedups. Concurrent work by Qin et al. (2024a) also proposes
    2732: an I/O-aware version of linear attention, which is similar to the non-materialization version of FLASHLINEARATTENTION.
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 2907 | **Candidates:** `4.0B`

```text
    2905: Gated Linear Attention Transformers with Hardware-Efficient Training
    2906: 
>>> 2907: Algorithm 4 Backward pass for gated linear attention (w. materialization)
    2908: Input: Q,K,G ∈ RL×dk , V,O,dO ∈ RL×dv , chunk size C
    2909: 
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 3009 | **Candidates:** `6.0B`

```text
    3007: Gated Linear Attention Transformers with Hardware-Efficient Training
    3008: 
>>> 3009: Algorithm 6 Backward pass for gated linear attention (w/o. materialization)
    3010: Input: Q,K,G ∈ RL×dk , V,O,dO ∈ RL×dv , chunk size C
    3011: 
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 3486 | **Candidates:** `0.0B`

```text
    3484: ∈ R1×dv for j ∈ [1,C], i ∈ [0,L/C − 1]. Subsequently, we have
    3485: 
>>> 3486: [i+1]. For initial values, we set S0 = 0, B0 = 1, D0 = 1.
    3487: [i] encodes the cumulative decay from the start of a chunk which will be used to propagate the hidden states
    3488: [i] encodes the decay to the end of a chunk which will be used to accumulate information
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 3507 | **Candidates:** `1.0B`

```text
    3505: to be added to the next hidden state S[i+1].
    3506: 
>>> 3507: The chunkwise form given here is a generalization of several existing forms for linear attention. If we set Aij = 1, Bij = 1,
    3508: it reduces to the chunk-wise form presented in the main paper for vanilla linear attention; if we set Aij = 1, Bij = γi+1, it
    3509: becomes RetNet’s chunk-wise form (Sun et al., 2023a). As such, our formulation can be regarded as a generalized chunk-wise
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 3508 | **Candidates:** `1.0B`

```text
    3506: 
    3507: The chunkwise form given here is a generalization of several existing forms for linear attention. If we set Aij = 1, Bij = 1,
>>> 3508: it reduces to the chunk-wise form presented in the main paper for vanilla linear attention; if we set Aij = 1, Bij = γi+1, it
    3509: becomes RetNet’s chunk-wise form (Sun et al., 2023a). As such, our formulation can be regarded as a generalized chunk-wise
    3510: parallel form for linear attention that enables fine-grained data-dependent decay.
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 3719 | **Candidates:** `0.34B`

```text
    3717: 
    3718: 0-shot
>>> 3719: Transformer++ 340M
    3720: RetNet 350M
    3721: Mamba 350M
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 3720 | **Candidates:** `0.35B`

```text
    3718: 0-shot
    3719: Transformer++ 340M
>>> 3720: RetNet 350M
    3721: Mamba 350M
    3722: GLA-Transformer 340M
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 3721 | **Candidates:** `0.35B`

```text
    3719: Transformer++ 340M
    3720: RetNet 350M
>>> 3721: Mamba 350M
    3722: GLA-Transformer 340M
    3723: 
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 3722 | **Candidates:** `0.34B`

```text
    3720: RetNet 350M
    3721: Mamba 350M
>>> 3722: GLA-Transformer 340M
    3723: 
    3724: 0-shot
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 3725 | **Candidates:** `1.3B`

```text
    3723: 
    3724: 0-shot
>>> 3725: Transformer++ 1.3B
    3726: RetNet 1.3B
    3727: Mamba 1.3B
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 3726 | **Candidates:** `1.3B`

```text
    3724: 0-shot
    3725: Transformer++ 1.3B
>>> 3726: RetNet 1.3B
    3727: Mamba 1.3B
    3728: GLA-Transformer 1.3B
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 3727 | **Candidates:** `1.3B`

```text
    3725: Transformer++ 1.3B
    3726: RetNet 1.3B
>>> 3727: Mamba 1.3B
    3728: GLA-Transformer 1.3B
    3729: 
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 3728 | **Candidates:** `1.3B`

```text
    3726: RetNet 1.3B
    3727: Mamba 1.3B
>>> 3728: GLA-Transformer 1.3B
    3729: 
    3730: 5-shot
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 3731 | **Candidates:** `1.3B`

```text
    3729: 
    3730: 5-shot
>>> 3731: Transformer++ 1.3B
    3732: RetNet 1.3B
    3733: Mamba 1.3B
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 3732 | **Candidates:** `1.3B`

```text
    3730: 5-shot
    3731: Transformer++ 1.3B
>>> 3732: RetNet 1.3B
    3733: Mamba 1.3B
    3734: GLA-Transformer 1.3B
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 3733 | **Candidates:** `1.3B`

```text
    3731: Transformer++ 1.3B
    3732: RetNet 1.3B
>>> 3733: Mamba 1.3B
    3734: GLA-Transformer 1.3B
    3735: 
```

---

### File: `Linear_attention_papers_https_arxiv_org_abs_2312_06635_2312.06635.md`
**Line:** 3734 | **Candidates:** `1.3B`

```text
    3732: RetNet 1.3B
    3733: Mamba 1.3B
>>> 3734: GLA-Transformer 1.3B
    3735: 
    3736: 28.39
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

