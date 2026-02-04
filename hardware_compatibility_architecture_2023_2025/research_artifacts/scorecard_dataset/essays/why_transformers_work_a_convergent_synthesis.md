# Why Transformers Work: A Convergent Synthesis

*Working Note v3.0 — February 2026*

---

## Abstract

Transformers dominate large-scale language modeling. Many “explanations” describe different aspects of the same system: attention as associative memory, in-context learning as implicit optimization, attention heads as routing circuits over a shared residual stream, and scaling as a training-time selection process. This note treats those interpretations as **constraints** rather than as a single unified mechanism.

**Thesis (regime-conditional):** Under today’s regime—dense autoregressive pretraining, deep residual stacks, large-batch Adam/SGD, and GPU-centric kernels—self-attention is not uniquely optimal on any one axis. It is unusually good at meeting a *bundle* of requirements simultaneously. Alternatives often improve one dimension (e.g., asymptotic efficiency) while leaving at least one requirement partially met or empirically unverified; hybrids that reintroduce attention specifically for retrieval tend to recover performance.

We propose four operational requirements that recur across methodologically distinct lines of work:

1. **Content-addressable random access** (associative retrieval from arbitrary positions)
2. **Inference-time learning** (inner-loop adaptation; implicit optimization/inference in the forward pass)
3. **Input-dependent routing** (conditional information flow; variable dependency graphs)
4. **Scalable optimization substrate** (stable deep training and compositional refinement at scale)

This is a position piece. Claims are labeled by evidential status, and we specify falsification experiments and displacement conditions.

---

## 1. Two Questions, One Confusion

When people ask “why Transformers work,” they often conflate two questions:

1. **Capability:** What properties make Transformers effective sequence models at scale?
2. **Dominance:** What forces make them hard to displace once they are effective?

Hardware fit and ecosystem lock-in are powerful answers to (2), but incomplete answers to (1). This note addresses both, explicitly separating **functional requirements** from the **selection regime** that amplifies them.

### 1.1 Scope and Regime Assumptions

This synthesis is about the regime in which Transformers actually dominate:

- autoregressive next-token training on large, heterogeneous corpora
- deep residual stacks trained with standard optimizers (Adam/AdamW/SGD variants)
- GPU/TPU accelerators where GEMM-like kernels and high arithmetic intensity matter
- deployment that values both quality and throughput

If a future regime changes these constraints (e.g., different objectives, compute substrates, or retrieval-augmented training), some conclusions may stop applying.

---

## 2. Method: Convergent Constraints, Not a Single Mechanism

We draw on “interpretations” of Transformers that use different methods:

| Lens | Representative work | Core method |
|------|---------------------|-------------|
| Associative memory | Ramsauer et al. (2020); Ba et al. (2016) | energy / fast-weights analysis |
| ICL as optimization | Von Oswald et al. (2023); Garg et al. (2022) | closed-form equivalences; meta-learning |
| ICL as inference | Xie et al. (2022) | Bayesian framing; synthetic data |
| Mechanistic circuits | Elhage et al. (2021); Olsson et al. (2022) | causal interventions; activation patching |
| Compression view | Delétang et al. (2024) | information-theoretic framing |
| Training dynamics | Frankle & Carbin (2019); Power et al. (2022) | optimization dynamics; implicit sparsity |

These lenses are not “independent” in a sociological sense—they mostly study Transformers. The claim is weaker: their **methodologies differ**, and their intersection suggests constraints that are difficult to dismiss as a single analytical artifact.

### 2.1 What Would Make “Convergence” Non-Informative?

Convergence is unhelpful if the lenses are merely re-descriptions of the same property. We therefore treat the requirements below as *separable* hypotheses and propose targeted tests (Section 10) that can differentially break them.

---

## 3. Four Operational Requirements

Each requirement is (i) a functional capability, (ii) tied to at least one operational test, and (iii) potentially satisfiable by non-attention mechanisms. The synthesis is falsified if the bundle is incomplete or misidentified.

### R1. Content-Addressable Random Access (Associative Retrieval)

**Definition:** The model can retrieve information from arbitrary positions in context based on content similarity or keying, without compressing the entire past into a fixed-size state.

**Why it matters:** Language (and many sequence domains) frequently requires “needle-like” access: retrieving a specific entity, value, or span conditioned on a query. Fixed-state models face an information bottleneck; windowed models face a coverage bottleneck.

**Evidence in Transformers:**
- Softmax attention is equivalent to a modern Hopfield network update under a particular formulation (Ramsauer et al., 2020).
- Fast weights frame attention-like mechanisms as a rapidly updated associative memory (Ba et al., 2016).
- Induction heads provide a mechanistic example of pattern completion via copying from earlier context (Olsson et al., 2022).
- In recent non-attention SSM work, authors explicitly report a remaining retrieval limitation relative to Transformer baselines and recommend hybrid retrieval mechanisms (Anonymous, 2026). In their retrieval suite, a 1.5B Mamba-3 variant reports **SWDE 28.5** versus **Transformer 48.9** (Anonymous, 2026, Table 2).

**Operational tests (examples):**
- key–value / associative recall tasks as a function of context length
- semi-structured extraction tasks (e.g., SWDE-like cloze extraction as used in Anonymous, 2026)
- “phonebook lookup” style retrieval under context lengths that exceed any local window (De et al., 2024)

**Working definition (for this note):** A mechanism counts as “random-access retrieval” if it allows a query-dependent read of *arbitrary* stored items whose capacity scales with context length (not just a fixed-size state or fixed window). This includes explicit key–value memory, kNN-style retrieval, or attention-like sparse lookup; it excludes purely fixed-state recurrence without such a read path.

**Falsification target:** A non-attention architecture matches attention within a small margin on these retrieval tests at scale *without introducing an attention-like random-access mechanism*.

---

### R2. Inference-Time Learning (Implicit Optimization / Inference)

**Definition:** The forward pass performs computation that is well-modeled as an inner-loop update: fitting or inferring a task/hypothesis from context examples and applying it to new inputs.

**Why it matters:** LLMs are used as instruction followers and few-shot learners. If this behavior is robust, architectures that cannot implement algorithmic adaptation in a single forward pass are at a disadvantage.

**Evidence in Transformers:**
- Transformers can learn in-context by implementing gradient-descent-like updates in their layers in controlled settings (Von Oswald et al., 2023).
- In synthetic function-learning, Transformers trained on data from a function family can match optimal estimators (e.g., OLS in linear regression) (Garg et al., 2022).
- ICL can also appear in LSTMs on specific synthetic datasets, suggesting the phenomenon is not unique to attention, though its realizability and scaling may differ (Xie et al., 2022).

**Operational tests (examples):**
- synthetic regression/classification ICL with known Bayes/OLS optima
- probing whether layer-wise updates match GD/OLS/Bayesian posterior predictions
- ablations that selectively disrupt the mechanisms hypothesized to implement the update (e.g., disabling certain attention patterns) and measuring ICL degradation

**Falsification target:** An architecture lacking iterative refinement mechanisms (or with deliberate constraints that preclude GD-like updates) matches Transformer ICL performance on the same controlled tasks.

---

### R3. Input-Dependent Routing (Conditional Information Flow)

**Definition:** The model can route information based on the input, effectively inducing a variable dependency graph over tokens. The computation is not fixed-pattern (as in pure convolutions with fixed kernels or strict recurrence with fixed-state updates).

**Why it matters:** Natural language dependencies are long-range but irregular. Efficient prediction/compression benefits from being able to “connect” arbitrary spans when needed and ignore them otherwise.

**Evidence in Transformers:**
- The circuits framework models attention heads as information movement operations over a shared residual stream, enabling compositional, input-dependent behavior (Elhage et al., 2021).
- Architectures proposed as attention alternatives often explicitly target “data-controlled” or conditional operators, suggesting this property is viewed as central even outside attention (Poli et al., 2023).
- Language modeling can be viewed as compression; this view emphasizes the value of exploiting input-dependent structure rather than fixed-pattern processing (Delétang et al., 2024).

**Operational tests (examples):**
- tasks with irregular long-range dependencies where the relevant span location varies per example
- interventions that force fixed routing patterns (e.g., fixed-stride or static attention) and measure degradation relative to full attention

**Falsification target:** Fixed-pattern architectures (no conditional routing) match attention on these variable-structure tasks at scale.

---

### R4. Scalable Optimization Substrate (Deep, Stable, Compositional Training)

**Definition:** The architecture supports stable optimization at depth and scale, enabling long training runs to discover and refine internal structure (circuits, sparse subnetworks, algorithmic behavior) without chronic instability.

**Why it matters:** Many “better in principle” sequence models fail because they do not train as reliably at scale, or because the training compute needed to reach parity is economically prohibitive.

**Evidence (regime-level, not Transformer-specific):**
- Dense networks can contain sparse subnetworks that train effectively, consistent with the view that training can select structure within an overparameterized model (Frankle & Carbin, 2019).
- Generalization can emerge late in training even after overfitting, consistent with extended optimization reorganizing representations (Power et al., 2022).
- Transformers empirically scale stably across many settings; this note treats that fact as an input condition rather than as something “explained” by LTH/grokking.

**Operational tests (examples):**
- head-to-head scaling runs with matched token and parameter budgets measuring stability, convergence speed, and final perplexity
- ablations on residual/norm pathways measuring gradient pathologies and training collapse rates
- measuring whether late-stage generalization dynamics (grokking-like behavior) occur comparably across architectures under controlled curricula

**Falsification target:** Architectures without residual-like stabilization train as stably as residualized baselines at scale and match downstream capability.

---

## 4. The Synthesis: Why the Bundle Matters

The core claim is not “attention is the unique mechanism.” It is:

> **Bundle claim:** Under current regimes, competitive architectures must satisfy *all four* requirements well enough. Attention is a compact way to satisfy the bundle simultaneously.

This helps explain two empirical patterns:

1. **Tradeoffs in pure alternatives:** Subquadratic models can improve long-context efficiency, but often retain a gap on random-access retrieval or on some forms of in-context behavior.
2. **Strength of hybrids:** Hybrids that reintroduce even a small amount of attention specifically for retrieval can recover performance, suggesting retrieval is a particularly discriminating requirement.

The bundle claim can be wrong in two ways: (i) the requirements are incomplete (missing a fifth), or (ii) one of the requirements is not actually necessary (a red herring). Section 10 proposes tests to discriminate.

---

## 5. Evidence Map (February 2026)

This table is deliberately conservative: it distinguishes direct evidence from plausibility.

**Legend**
- **Strong:** explicitly evaluated on an operational test relevant to the requirement
- **Partial:** mechanism plausibly supports the requirement but is constrained (window/state) or only shown on limited/synthetic setups
- **Gap:** paper reports a meaningful deficit relative to attention baselines on a relevant test
- **Unknown:** no clear evaluation found in the cited sources

| Architecture | R1 Retrieval | R2 ICL / implicit update | R3 Conditional routing | R4 Stable scaling | Evidence anchors |
|--------------|-------------|--------------------------|------------------------|------------------|------------------|
| **Transformer (attention)** | Strong | Strong | Strong | Strong | Ramsauer; Olsson; Von Oswald; Garg; Elhage |
| **Mamba (selective SSM)** | Partial | Gap/Partial | Partial | Strong | Gu & Dao; Lieber (Table 6) |
| **Mamba-3 (SSM)** | Gap | Unknown | Partial | Strong | Anonymous (Table 2; conclusion) |
| **RetNet (retention)** | Partial | Partial | Partial | Strong | Sun et al. |
| **Hyena** | Partial | Unknown | Partial | Strong | Poli et al. |
| **Griffin / Hawk (hybrid recurrence + local attn)** | Gap (window-limited) | Unknown | Partial | Strong | De et al. |
| **xLSTM** | Partial | Unknown | Unknown | Partial | Beck et al. |
| **Jamba (hybrid Transformer–Mamba)** | Strong (via attention) | Strong | Strong | Strong | Lieber et al. |

**Notes**
- “Strong/Partial/Gap” is about the *specific requirement tests*, not overall model quality.
- Many results are not strict head-to-head comparisons (different token budgets, context lengths, recipes). Treat the map as an evidence ledger, not as a final ranking.

**Key quantitative anchors (for the evidence map above):**
- Anonymous (2026, Table 2): SWDE extraction **48.9** (Transformer) vs **28.5** (Mamba-3 SISO), 1.5B models.
- Lieber et al. (2024, Table 6): IMDB accuracy **84.1** (attention) vs **48.8** (Mamba) vs **90.9** (hybrid), 1.3B models after 250B tokens.
- De et al. (2024, phonebook lookup): Griffin’s retrieval degrades once the phonebook exceeds its **1024** local-attention window.

---

## 6. The Selection Regime: Why Displacement Is Hard

Even if an alternative can satisfy the bundle, it must pass two practical gates:

**Gate 1 — Training viability:** stable end-to-end optimization at scale with acceptable engineering complexity.

**Gate 2 — Hardware economics:** competitive throughput on current accelerators. In practice, this rewards GEMM-dominant computation and kernels with high arithmetic intensity.

### 6.1 Co-evolution of kernels and hardware

Algorithmic improvements such as FlashAttention reduce attention’s memory/IO costs and improve throughput (Dao et al., 2022; Dao, 2023). The net effect is that alternatives compete against a baseline that keeps improving.

This does not prove attention is “optimal.” It explains why an alternative must beat a moving target: not just the architecture, but the architecture plus the ecosystem of kernels and hardware.

---

## 7. Counterexample Analysis: What Alternatives Actually Show

This section summarizes what the *papers themselves* establish and what remains open.

### 7.1 Mamba (Gu & Dao, 2024)

Mamba explicitly identifies a weakness of prior subquadratic models as inability to do “content-based reasoning,” and introduces **selective** (input-dependent) SSM parameters to address it (Gu & Dao, 2024):

> “We identify that a key weakness of such models is their inability to perform content-based reasoning, and make several improvements.”

On synthetic copying/induction tasks, it performs strongly and extrapolates to long lengths. The open question is whether this closes the gap on **random-access retrieval** in real-world extraction and format-sensitive ICL settings.

### 7.2 Griffin / Hawk (De et al., 2024)

Griffin mixes gated recurrence with **local attention** (windowed). On a phonebook lookup task, Griffin can solve retrieval up to its local attention window and then degrades once the relevant information falls outside the window (De et al., 2024). This is a concrete example of a *coverage bottleneck* rather than an information bottleneck.

### 7.3 xLSTM (Beck et al., 2024)

xLSTM is an attempt to fix specific LSTM limitations (nearest-neighbor search, rare token prediction, parallelizability) via exponential gating and matrix memory (Beck et al., 2024). It demonstrates that state-based models can be improved substantially, but it does not (by itself) establish attention-like random access over arbitrary contexts.

### 7.4 Mamba-3 (Anonymous, 2026)

Mamba-3 reports improved quality/efficiency and new capabilities (e.g., state tracking), but its authors explicitly flag retrieval as a remaining limitation relative to attention baselines and recommend hybrid retrieval mechanisms (Anonymous, 2026):

> “A limitation remains in retrieval, where fixed-state architectures lags attention-based models.”

In their retrieval suite (1.5B models, cloze-formatted tasks truncated to 2K), the Transformer baseline reports **SWDE 48.9** while Mamba-3 (SISO) reports **28.5** (Anonymous, 2026, Table 2).

### 7.5 Hybrids as a diagnostic (Lieber et al., 2024)

In Jamba, adding attention layers to an SSM-heavy backbone recovers performance on tasks where pure Mamba underperforms attention, and the paper’s qualitative analysis points to format adherence issues in pure Mamba (Lieber et al., 2024). Quantitatively, in their 1.3B experiment after 250B tokens, IMDB accuracy is **84.1** (attention), **48.8** (Mamba), and **90.9** (hybrid) (Lieber et al., 2024, Table 6).

### 7.6 The recurring pattern

Across these examples, the most consistent unresolved weakness is **content-addressable random access** (R1), especially on semi-structured extraction and tasks where the “right” information is sparse and far away. This is not a proof; it is the current best candidate for the discriminating requirement.

---

## 8. Epistemic Status and Limitations

> [!IMPORTANT]
> This note is **not** a mechanistic theory of intelligence. It is a **constraint-based synthesis** designed to be falsifiable.

### What this note claims (as hypotheses)

1. The four requirements are a useful decomposition of “what has to go right” for frontier-scale sequence modeling under current regimes.
2. Current evidence suggests R1 (random-access retrieval) is a frequent limiting factor for pure non-attention alternatives.
3. The selection regime (training viability + hardware economics) amplifies the advantage of architectures that already satisfy the bundle.

### What it does not claim

1. That attention is the only way to satisfy the requirements.
2. That the requirements are complete or permanently relevant.
3. That existing evidence cleanly separates architecture effects from training-recipe effects.

---

## 9. The Mechanism We Decline to Claim: “Universality”

A tempting stronger claim is:

> Attention is successful because Transformers are (differentiably) universal computers over sequences.

Transformers with positional encodings can be shown Turing-complete under idealized assumptions (e.g., rational arithmetic and hard attention variants) (Pérez et al., 2019). This is intellectually interesting but weak as an explanation of empirical success: Turing completeness is common and non-discriminating, and the assumptions used in proofs are far from the training regime.

The constraint-based framing is stronger epistemically: it can be falsified by an architecture that satisfies the requirements but still underperforms, or by an architecture that violates one requirement but matches attention anyway.

---

## 10. Falsification Experiments

The goal is to falsify the **bundle claim**, not to defend attention.

### 10.1 Master test (bundle test)

**Hypothesis:** Any architecture that satisfies R1–R4 should match a Transformer baseline at matched scale and compute.

**Protocol sketch:**
1. Design an architecture with explicit mechanisms intended to satisfy each requirement.
2. Verify satisfaction with the operational tests in Section 3 (separately for each requirement).
3. Pretrain with matched parameter count and token budget (e.g., ~7B class, fixed tokens).
4. Evaluate on a frozen suite that includes:
   - general LM quality (perplexity / held-out loss)
   - retrieval/extraction (the same suite used in Anonymous, 2026, if available)
   - controlled ICL tasks (Garg/Von Oswald-style)
   - variable-structure long-range tasks (routing stress tests)

**Falsification:** If the architecture passes the operational tests for R1–R4 but still underperforms attention by a clear margin, the requirement bundle is incomplete.

### 10.2 Requirement isolation tests

The isolation tests below are deliberately “surgical”: break one capability while holding others fixed.

| Requirement | Intervention | Expected impact if requirement matters |
|------------|--------------|-----------------------------------------|
| R1 Retrieval | remove/limit random-access mechanism | large drop on extraction/lookup; small drop on local tasks |
| R2 ICL | constrain depth/iterative update capacity | controlled ICL tasks degrade disproportionately |
| R3 Routing | force static/fixed routing patterns | variable-dependency tasks degrade |
| R4 Scaling | remove residual-like stabilization | training instability or slower convergence |

The key is **differential** effects: if two “requirements” always move together under interventions, they are not separable and the decomposition is wrong.

---

## 11. Predictions (2026–2028)

These are conditional predictions intended to be checkable with a frozen evaluation suite.

1. **Retrieval remains the main differentiator:** Pure fixed-state models will continue to lag attention baselines on semi-structured extraction tasks at comparable scale unless they add an attention-like random-access component.
2. **Hybrids persist:** Competitive long-context models will increasingly use hybrids (SSM/conv for throughput + attention for retrieval) until a unified non-attention mechanism matches attention on R1.
3. **Kernel pressure continues:** The performance gap on Gate 2 will keep moving as attention kernels improve, raising the bar for pure alternatives.

If these predictions fail (e.g., a pure SSM closes the extraction gap cleanly without attention-like mechanisms), the synthesis should be revised accordingly.

---

## 12. Competing Explanations (and how to discriminate)

### Path dependence / lock-in

Lock-in explains persistence, but does not alone explain early competitive advantage. Discriminant: show that at equal compute in the pre-lock-in period, attention offers no advantage over alternatives on the requirements above.

### “It’s just GEMM”

GEMM alignment is a necessary constraint under GPU economics, but not sufficient. Discriminant: construct GEMM-heavy architectures without random-access retrieval and test whether they close the extraction gap.

### “We don’t know”

This is probably the most accurate meta-position. The value of the synthesis is that it makes this ignorance actionable: it proposes tests that can collapse uncertainty into evidence.

---

## 13. Conclusion

This note argues that attention’s success is best viewed as **bundle satisfaction under a regime**. The strongest current evidence for a discriminating factor is R1: content-addressable random access. The rest of the requirements matter insofar as they determine whether an architecture can scale, adapt, and route information under real training/economic constraints.

If a future architecture satisfies R1–R4 without self-attention and matches Transformers at scale, this synthesis will have served its purpose: it will have identified the right constraints even if it misidentified the only mechanism. If it fails, it will have provided a clear record of what to update.

---

## Appendix A: Full Citations

1. **Vaswani, A., Shazeer, N., Parmar, N., et al.** (2017). Attention Is All You Need. *NeurIPS*. arXiv:1706.03762
2. **Ramsauer, H., Schäfl, B., Lehner, J., et al.** (2020). Hopfield Networks is All You Need. *NeurIPS*. arXiv:2008.02217
3. **Ba, J., Hinton, G. E., Mnih, V., & Ionescu, C.** (2016). Using Fast Weights to Attend to the Recent Past. *NeurIPS*. arXiv:1610.06258
4. **Von Oswald, J., Niklasson, E., Randazzo, E., et al.** (2023). Transformers learn in-context by gradient descent. *ICML*. arXiv:2212.07677
5. **Garg, S., Tsipras, D., Liang, P., & Valiant, G.** (2022). What Can Transformers Learn In-Context? *NeurIPS*. arXiv:2208.01066
6. **Xie, S. M., Raghunathan, A., Liang, P., & Ma, T.** (2022). An Explanation of In-context Learning as Implicit Bayesian Inference. *ICLR*. arXiv:2111.02080
7. **Elhage, N., Nanda, N., Olsson, C., et al.** (2021). A Mathematical Framework for Transformer Circuits. *Anthropic*. transformer-circuits.pub
8. **Olsson, C., Elhage, N., Nanda, N., et al.** (2022). In-context Learning and Induction Heads. *Anthropic*. arXiv:2209.11895
9. **Delétang, G., Ruoss, A., Grau-Moya, J., et al.** (2024). Language Modeling is Compression. *ICLR*. arXiv:2309.10668
10. **Frankle, J., & Carbin, M.** (2019). The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks. *ICLR*. arXiv:1803.03635
11. **Power, A., Burda, Y., Edwards, H., Babuschkin, I., & Misra, V.** (2022). Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets. *ICLR*. arXiv:2201.02177
12. **Gu, A., & Dao, T.** (2024). Mamba: Linear-Time Sequence Modeling with Selective State Spaces. *ICLR*. arXiv:2312.00752
13. **Lieber, O., Sharir, O., Lentz, B., et al.** (2024). Jamba: A Hybrid Transformer-Mamba Language Model. *AI21 Labs*. arXiv:2403.19887
14. **De, S., Smith, S. L., Fernando, A., et al.** (2024). Griffin: Mixing Gated Linear Recurrences with Local Attention for Efficient Language Models. *Google DeepMind*. arXiv:2402.19427
15. **Beck, M., Pöppel, K., Spanring, M., et al.** (2024). xLSTM: Extended Long Short-Term Memory. *arXiv*. arXiv:2405.04517
16. **Sun, Y., Dong, L., Huang, S., et al.** (2023). Retentive Network: A Successor to Transformer for Large Language Models. *Microsoft*. arXiv:2307.08621
17. **Poli, M., Massaroli, S., Nguyen, E., et al.** (2023). Hyena Hierarchy: Towards Larger Convolutional Language Models. *Stanford*. arXiv:2302.10866
18. **Pérez, J., Barceló, P., & Marinkovic, J.** (2019). On the Turing Completeness of Modern Neural Network Architectures. *ICLR*. arXiv:1901.03429
19. **Dao, T., Fu, D. Y., Ermon, S., Rudra, A., & Ré, C.** (2022). FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness. *NeurIPS*. arXiv:2205.14135
20. **Dao, T.** (2023). FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning. *arXiv*. arXiv:2307.08691
21. **Anonymous.** (2026). Mamba-3: Improved Sequence Modeling Using State Space Principles. *Under review at ICLR 2026*.

---

## Appendix B: Relation to Companion Essays

This synthesis relates to:

- The Transformer Attractor (Substack): the two-gate trap and hardware economics
- Part II: The Retrieval Bottleneck: hybrid architectures and retrieval gaps
- Literature Map: catalog of interpretation threads
