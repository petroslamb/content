# Why Transformers Work: A Convergent Synthesis

*Working Note v4.0 — February 2026 (rewritten to align with the 2024–2025 mechanistic evidence in `papers/` and the Feb 2026 evidence notes).*

---

## Abstract

“Why Transformers work” is not one answer. It’s a bundle of properties that (i) enable strong sequence modeling *capabilities* and (ii) survive a brutal *selection regime* (trainability + hardware economics).

This rewrite makes one change from v3.0: it treats recent mechanistic findings as the **primary constraints**. In particular, several independent threads now point to a surprisingly *localized* picture:

- in-context retrieval in real models concentrates in a small set of heads and can be decomposed into a **Gather-and-Aggregate (G&A)** mechanism (Wu et al., 2024; Bick et al., 2025);
- few-shot in-context learning depends primarily on **function vector (FV) heads**, many of which *develop out of* induction-like heads during training (Yin & Steinhardt, 2025);
- “routing” is not just an architectural metaphor: attention head types are diverse and specialized, routes cluster by token/function properties, and MoE routing responds to context (IAAR survey, 2024; Ferrando & Voita, 2024; Arnold et al., 2024);
- training is plausibly a **circuit selection process**: generalization can appear long after memorization (grokking) and sparse subnetworks can be unusually trainable (Power et al., 2022; Frankle & Carbin, 2019); sparse-transformer work suggests circuits found in small interpretable models can meaningfully transfer to dense ones via bridging (Gao et al., 2024).

**Thesis (regime-conditional):** Under today’s dominant regime (dense autoregressive pretraining, deep residualized stacks, and accelerator-friendly implementations), Transformers are not “uniquely optimal” on a single axis. They are unusually good at *simultaneously* supporting (R1) sharp in-context retrieval (G&A), (R2) inference-time learning (FV/implicit optimization), (R3) input-dependent routing/modular specialization, and (R4) training dynamics that reliably discover and refine such mechanisms.

This is a position piece. I label the main claims by evidential status and list falsification experiments.

---

## Evidential Legend (used throughout)

- **Strong:** causal ablations / localized mechanism in pretrained(-like) models; or replicated across model families.
- **Moderate:** controlled/synthetic settings with a clean mechanistic mapping; plausible transfer to LLMs.
- **Speculative:** conceptual synthesis or extrapolation; proposed tests included.

---

## 1. Two Questions, One Confusion

When people ask “why Transformers work,” they often conflate:

1. **Capability:** what computations and representational tricks the model class supports.
2. **Dominance:** why this class is hard to displace once it’s good (training recipes, kernels, tooling, deployment).

This note addresses both, but keeps them separate.

### 1.1 Regime Assumptions (what this note is about)

This synthesis is scoped to the regime where decoder-only Transformers dominate:

- next-token (autoregressive) pretraining on large heterogeneous corpora;
- deep residualized stacks with normalization + MLP sublayers;
- deployment that prizes both quality and throughput;
- accelerators where dense matrix multiplies are cheap and memory bandwidth is precious.

If objectives, data, or compute substrates change, the bundle can change.

---

## 2. Method: Convergent Constraints + Mechanistic Bottlenecks

The “many lenses” story is still useful, but v4.0 weights **mechanistic bottlenecks** more heavily than broad metaphors.

Two newer unifications help keep the synthesis honest:

1. **Sequence layers as associative memory / test-time regression.** Many “different” layers (softmax attention, linear attention, SSMs, fast-weight layers, online learners) can be derived as instances of “memorize then retrieve” regression layers; their differences show up as *which regression objective/approximation* they implement (Wang et al., 2025).
2. **SSMs and attention are mathematically close in some regimes.** Structured State Space Duality (SSD) connects selective SSMs to attention-like quadratic forms via semiseparable matrices and yields efficient algorithms that mix linear and quadratic views (Dao & Gu, 2024).

So the question is not “attention vs. no attention.” It’s:

> Which mechanisms (and approximations) do we need to get the observed behaviors, and which ones are easiest to discover and run under the current regime?

---

## 3. Four Requirements (re-specified to match the new evidence)

The requirements are *capability* constraints, not a claim of architectural uniqueness.

### R1. In-Context Retrieval With Sharp Selection (G&A)

**Definition (operational):** Given a query embedded in the current context, the model can reliably (a) locate relevant spans/items anywhere in the context and (b) **select/compose** the right item(s) with sufficiently *sharp* discrimination to support extraction and strict formats.

This version intentionally avoids the ambiguous phrase “random access.” What matters in practice is *selective readout* from a token-indexed memory (KV cache / residual stream), not hardware-addressed random access.

#### Mechanism: Gather-and-Aggregate (G&A)

**Strong:** Recent work localizes in-context retrieval to a two-stage mechanism:

- **Gather:** condense relevant segments into summary tokens (often end-of-segment tokens such as newline).
- **Aggregate:** attend over those summaries to pick the correct one (often argmax-like selection).

This shows up in Transformers and, strikingly, also in SSM-based LMs—but the SSM implementations are typically **smoother/less discrete**, requiring more “weak” heads/channels to approximate what a few sharp attention heads do (Bick et al., 2025).

#### Evidence (selected, load-bearing)

- **Retrieval heads are sparse, intrinsic, and causal** for long-context factuality: a small fraction (<5%) of attention heads largely implement conditional copy/redirect; masking them causes needle-in-haystack failure and hallucination; effects extend to extractive QA and CoT-style prompting where intermediate steps must refer back to the prompt (Wu et al., 2024).
- **MMLU-style multiple-choice can be bottlenecked by retrieval/format mechanics, not knowledge:** disabling a single gather/aggregate head in a pruned Llama-3.1-8B variant collapses answer-letter selection to random-guessing levels (66% → 25%), and hybrid SSM–attention models delegate the aggregate role to attention layers (Bick et al., 2025).
- **Hybrids are a diagnostic, not just an engineering hack:** replacing only the teacher’s aggregate head(s) into a distilled SSM recovers a large portion of MMLU (33% → 50%), suggesting the capability gap can be concentrated in the aggregate step (Bick et al., 2025). A separate hybrid study shows pure Mamba can fail badly on datasets where strict output format matters (e.g., IMDB), while an attention–Mamba hybrid recovers performance and format adherence (Lieber et al., 2024).

#### Why this discriminates architectures

**Moderate → Strong synthesis:** Test-time regression theory explains why “sharp selection” is not a cosmetic detail. Linear-attention-style approximations can be viewed as crude least-squares memories that ignore covariance structure, which degrades associative recall; adding gating/forgetting trades capacity for recency (Wang et al., 2025). SSD shows SSMs can be written in attention-like quadratic form, but state size and approximation choices still impose real constraints (Dao & Gu, 2024).

#### Operational tests

- **Segmented extraction:** long semi-structured contexts where the “right” span is sparse and format-sensitive (e.g., cloze-style extraction; SWDE-like setups).
- **Needle-in-haystack with distractors:** locate a specific injected string/value under varying context length and distraction rate (Wu et al., 2024).
- **G&A ablations:** disable identified gather vs aggregate heads and measure differential degradation (Bick et al., 2025).

#### Falsification target (R1)

> A non-attention architecture matches Transformers on extraction/format-sensitive retrieval *and* passes G&A-style ablations (i.e., shows no concentrated sharp-selection bottleneck), without reintroducing an attention-like sparse lookup.

---

### R2. Inference-Time Learning (Few-Shot ICL as Computation, Not Just Copying)

**Definition (operational):** The forward pass can infer a task/hypothesis from examples in the prompt and apply it, behaving like an inner-loop learner (gradient descent, Bayesian inference, or other learned update rules).

#### Mechanisms (now better separated)

1. **Induction circuits (copying) are real but incomplete.** Induction heads explain in-context copying patterns (Olsson et al., 2022).
2. **Function vector (FV) heads drive few-shot ICL performance.** Ablations across many models show few-shot ICL depends primarily on FV heads, especially at larger scales; many FV heads start as induction-like heads early in training and transition later (Yin & Steinhardt, 2025).
3. **Implicit optimization/inference lenses are mechanistically grounded in controlled settings.** A weight construction shows linear self-attention can implement a gradient-descent-like update on regression loss; trained models can match the construction on regression tasks (von Oswald et al., 2023). A complementary framing models ICL as implicit Bayesian inference over latent concepts (Xie et al., 2022). Synthetic function-learning work shows Transformers can match optimal estimators (e.g., OLS) for some families (Garg et al., 2022).
4. **ICL can be multi-phase at the circuit level.** In a controlled in-context meta-learning setup, distinct circuits appear across phases (non-context → semi-context → full-context), making “ICL emergence” more like circuit succession than a single switch (Minegishi et al., 2025).

#### Evidence (selected, load-bearing)

- **FV heads emerge later than induction heads and matter more for few-shot accuracy:** in Pythia models, induction heads appear around step ~1k while FV heads appear around ~16k; ablating FV heads degrades few-shot ICL much more than ablating induction heads (Yin & Steinhardt, 2025).
- **Mechanistic equivalence to GD in a tractable setting:** linear self-attention can be constructed to perform a GD step; trained attention-only Transformers on regression tasks show weights that match or closely resemble the construction (von Oswald et al., 2023).
- **ICL is not unique to Transformers in synthetic settings:** LSTMs can show ICL in concept-inference datasets, suggesting the phenomenon is not strictly attention-exclusive, though scaling and robustness may differ (Xie et al., 2022).

#### Operational tests

- synthetic regression/classification ICL with known Bayes/OLS optima (Garg et al., 2022);
- ablate FV heads vs induction heads and compare the impact on few-shot accuracy vs token-loss-difference metrics (Yin & Steinhardt, 2025);
- track circuit emergence across training checkpoints (Minegishi et al., 2025; Yin & Steinhardt, 2025).

#### Falsification target (R2)

> A model class with deliberately constrained “inner-loop computation” matches Transformer few-shot ICL *and* lacks an FV-like head family (or equivalent latent task representation) under comparable training.

---

### R3. Input-Dependent Routing and Modular Specialization (Beyond Retrieval)

**Definition (operational):** The model can conditionally route information and computation based on the input, yielding modular specialization (head types, routes, experts) without hand-designed gating.

This requirement is distinct from R1: *R1 is about retrieving the right content; R3 is about selecting the right computation/circuit path*.

#### Evidence (selected)

- **Head-type diversity and specialization:** A 2024 survey catalogs >30 attention head types, including retrieval/memory heads, induction variants, and other specialized functions (IAAR survey, 2024).
- **Routes are extractable at scale and show structure:** attribution-based “information flow routes” reveal that important components vary with part-of-speech and subword position; previous-token heads and subword-merging heads are broadly important infrastructure; domain-specialized components activate for coding/multilingual domains (Ferrando & Voita, 2024).
- **Softmax + sinks can implement thresholding-like operations:** in an interpretable sparse-transformer setting, attention sinks enable discrete decisions by turning softmax into a thresholding mechanism (Gao et al., 2024). This is a plausible primitive for “sharp routing” and selection.
- **MoE routing responds to context (not only token identity/position):** routing choices correlate with semantic associations and are modulated by contextual cues; effects differ between encoder and decoder routing behavior (Arnold et al., 2024).

#### Operational tests

- “route extraction” across domains and token classes; measure modular specialization and context dependence (Ferrando & Voita, 2024);
- interventions that force static routing patterns and test degradation on tasks with variable dependency structure;
- in MoE models, measure sensitivity of token→expert assignment to context perturbations (Arnold et al., 2024).

#### Falsification target (R3)

> Architectures with fixed-pattern mixing (no input-dependent routing / specialization) match Transformers on tasks where the relevant computational subroutine varies strongly with input (domain shifts, syntactic roles, format switches).

---

### R4. Trainability and Circuit Discovery (Optimization as Selection)

**Definition (operational):** The architecture + training setup reliably discovers and refines the small, specialized mechanisms in R1–R3 without requiring brittle, hand-tuned interventions for every new scale.

This requirement is about *discoverability and stability*, not about any single mathematical property.

#### Evidence (selected)

- **Generalization can be delayed by orders of magnitude:** in algorithmic tasks, training accuracy can reach near-perfect quickly while validation/generalization stays near chance until vastly later (“grokking”) (Power et al., 2022).
- **Overparameterized networks can contain unusually trainable sparse subnetworks:** “winning tickets” can match full-network accuracy when trained in isolation with the right initialization; random reinitialization breaks the effect (Frankle & Carbin, 2019).
- **Sparse circuits can be extracted and can map to dense behavior:** weight-sparse Transformers yield unusually interpretable circuits; scaling sparse models improves the capability–interpretability Pareto frontier; “bridges” suggest some circuit-level manipulations/attacks transfer to similarly capable dense models (Gao et al., 2024).

#### Why this matters for Transformers specifically (careful phrasing)

**Speculative (but testable):** The emerging picture from R1–R3 is that many high-value capabilities concentrate in small sets of components (retrieval heads, FV heads, specialized routes). R4 is the claim that a viable architecture must (a) allow such localization and (b) make it discoverable by gradient-based training under realistic budgets.

#### Operational tests

- track whether a model family develops sparse bottlenecks analogous to retrieval/FV heads across scales and training time;
- measure “late-phase” capability emergence under extended training or regularization changes (Power et al., 2022);
- prune/ablate candidate subnetworks early vs late in training and compare recoverability (Frankle & Carbin, 2019; Gao et al., 2024).

#### Falsification target (R4)

> A family that lacks the architectural affordances usually associated with stable deep training nevertheless (i) trains reliably at scale and (ii) develops equally sharp G&A / FV / routing mechanisms under similar budgets.

---

## 4. The Synthesis (v4.0): Why the Bundle Matters

The core claim remains:

> **Bundle claim:** under current regimes, competitive architectures must satisfy R1–R4 well enough *at the same time*.

What’s new is that the “bundle” can now be stated in more mechanistic language:

- **R1:** sharp retrieval is not “global attention everywhere,” it is often a *small* G&A subnetwork.
- **R2:** few-shot ICL is not “induction everywhere,” it is often a *small* FV-driven subnetwork that emerges later.
- **R3:** routing/specialization is visible as structured routes, head taxonomies, and context-sensitive gating.
- **R4:** training must *find* these sparse mechanisms and keep them stable; late-phase changes and winning-ticket-like effects make “train longer” and “train bigger” meaningful levers.

This bundle framing explains two observed patterns:

1. **Pure alternatives often look close on perplexity but fail on sharp retrieval/format.** Hybrids that restore attention for aggregation frequently recover performance where pure SSMs struggle (Lieber et al., 2024; Bick et al., 2025; mamba3, 2026).
2. **“Why do a few attention layers help so much?”** Because they can implement the **aggregate** step sharply and cheaply, and because the relevant computation is concentrated (Bick et al., 2025).

---

## 5. Evidence Ledger (February 2026, updated)

**Legend:** Strong / Partial / Gap / Unknown refers to whether the paper set in `papers/` provides direct operational evidence for the requirement as specified in Section 3.

| Architecture family | R1 (G&A retrieval) | R2 (few-shot ICL) | R3 (routing/specialization) | R4 (trainability / discovery) | Evidence anchors |
|---|---|---|---|---|---|
| **Transformer** | **Strong** | **Strong** | **Strong** | **Strong/Moderate** | Wu’24; Bick’25; Yin’25; Ferrando’24; Gao’24 |
| **Mamba / SSM** | Partial/Gap (sharp aggregate) | Partial/Unknown | Partial | Moderate | Gu’24; Dao&Gu’24; Lieber’24; Bick’25; mamba3’26 |
| **Local-attn hybrids (Griffin/Hawk)** | Gap (window/coverage) | Unknown | Partial | Moderate | De’24 |
| **Conv/SSM (Hyena/H3)** | Gap on AR | Unknown | Partial | Moderate | Poli’23; Arora’25 |
| **RetNet / gated linear attention** | Partial | Unknown | Partial | Moderate | Sun’23; Wang’25 |
| **Memory-augmented recurrence (BABILong)** | Strong (at extreme lengths) | Unknown | Unknown | Unknown | Kuratov et al., 2024 |

**Key quantitative anchors (auditable in `papers/`)**

- **G&A bottleneck on MMLU format:** disabling a single gather/aggregate head in a pruned Llama-3.1-8B reduces MMLU 66% → 25% (Bick et al., 2025).
- **Hybrid delegation:** ablating a handful of attention heads in a hybrid (Zamba2-7B) reduces MMLU 64.3% → 34.9% while knowledge tasks stay ~70% (Bick et al., 2025).
- **Format-sensitive benchmark gap:** IMDB accuracy 84.1 (attention) vs 48.8 (Mamba) vs 90.9 (attention–Mamba hybrid), 1.3B after 250B tokens (Lieber et al., 2024).
- **Extraction gap in Mamba-3 retrieval suite:** SWDE 48.9 (Transformer) vs 28.5 (Mamba-3 SISO) at 1.5B, with cloze-style tasks truncated to 2K (mamba3, 2026).
- **Griffin window limit:** phonebook lookup degrades once relevant info falls outside the 1024 local-attention window (De et al., 2024).
- **FV heads timing:** induction ~step 1k, FV ~step 16k (Pythia training), and FV head ablations dominate few-shot ICL degradation (Yin & Steinhardt, 2025).

---

## 6. Selection Regime: Why Displacement Is Hard (and what “hardware fit” really means)

Even if an alternative matches the bundle in principle, it must pass two practical gates:

**Gate 1 — Training viability:** can you train it end-to-end at the target scale without heroics?

**Gate 2 — Hardware economics:** can it run with competitive throughput/latency on real accelerators?

These gates create path dependence: once a stack (architecture + kernels + infra) clears both, it becomes a moving target.

Two papers in `papers/` illustrate the shape of Gate 2:

- Selective SSMs can be less efficient than Transformers on modern accelerators because they don’t naturally map to matrix-multiplication units; SSD reframes them in structured-matrix terms and yields faster algorithms plus larger state sizes (Dao & Gu, 2024).
- Mamba-3 emphasizes optimized inference kernels and decode latency as first-class constraints, reflecting the economic pressure toward implementations that win on deployment metrics (mamba3, 2026).

This does not prove attention is “optimal.” It explains why any displacement must beat an ecosystem, not just a layer type.

---

## 7. Counterexample Analysis (updated): What Alternatives Actually Show

### 7.1 SSMs are close—but the bottleneck can be tiny

Mechanistic work suggests that the Transformer–SSM gap can concentrate in a small number of retrieval-critical components (Bick et al., 2025). This reframes the debate:

- it’s not “SSMs can’t do retrieval,” it’s “SSMs struggle to implement **sharp aggregation** cheaply enough.”
- hybrids work because they offload the aggregate step to attention (Lieber et al., 2024; Bick et al., 2025).

### 7.2 “Long context” is not one capability

The retrieval-head paper distinguishes long-context *factuality / extractive QA* from tasks that can be solved by parametric knowledge; masking retrieval heads damages the former far more (Wu et al., 2024). This matters for evaluation: some benchmarks are retrieval-format heavy (MMLU letter selection), others are closer to parametric recall, and prompting style (answer-only vs CoT) can change which subsystem is used (Wu et al., 2024; Bick et al., 2025).

### 7.3 Local attention buys speed, but it sets a hard coverage ceiling

Griffin shows that even a small local-attention component can match Transformers on some copying tasks and extrapolate well, but phonebook-style retrieval degrades once the relevant entry exits the local window (De et al., 2024).

### 7.4 Memory augmentation changes the game (and the regime)

BABILong shows that recurrent memory augmentation can process orders-of-magnitude longer inputs (millions of elements) than standard Transformer contexts on a needle-like benchmark (Kuratov et al., 2024). This is real counterevidence to “only attention can ever retrieve,” but it also changes the regime: explicit external/recurrent memory + fine-tuning is not “drop-in replacement for dense pretraining” yet.

---

## 8. Epistemic Status and Limitations (tightened)

> [!IMPORTANT]
> This note is **not** a claim that “attention is the unique road to intelligence.”
> It is a mechanistically informed **constraint bundle** for the current dominant regime.

### What this note claims

1. **Strong:** Sharp in-context retrieval in today’s LLMs is well modeled as a G&A bottleneck localized to a small set of heads/channels (Wu et al., 2024; Bick et al., 2025).
2. **Strong:** Few-shot ICL performance depends primarily on FV heads; induction circuits alone are not the main driver at scale (Yin & Steinhardt, 2025).
3. **Moderate:** Many architectures can be derived as “test-time regression” layers; differences in approximations/normalization/gating help explain retrieval deficits (Wang et al., 2025; Dao & Gu, 2024).
4. **Moderate:** Training can be usefully viewed as circuit discovery/selection (grokking, lottery tickets), and sparse-circuit work strengthens the case that “circuits are real enough to manipulate” (Power et al., 2022; Frankle & Carbin, 2019; Gao et al., 2024).

### What this note does not claim

- that the four requirements are complete or permanent;
- that all cited effects cleanly isolate architecture vs training recipe;
- that today’s benchmarks perfectly measure “reasoning” vs “retrieval” vs “format adherence.”

---

## 9. The Mechanism We Decline to Claim: “Universality”

“Transformers work because they are universal computers” is too weak to be discriminative. Turing completeness results exist under idealized assumptions, but many model classes are universal in the same sense and the proofs don’t explain why certain mechanisms are learned reliably under today’s training regime (Pérez et al., 2019).

The more discriminative story is the bundle: sharp G&A retrieval + FV-driven ICL + conditional routing + discoverability at scale.

---

## 10. Falsification Experiments (updated to match v4.0 mechanisms)

The goal is to falsify the **bundle claim**, not to defend Transformers.

### 10.1 Master test (bundle test)

**Hypothesis:** Any architecture that satisfies R1–R4 should match a Transformer baseline at matched scale and training compute.

**Protocol sketch:**
1. Specify explicit mechanisms for (i) G&A-like sharp retrieval, (ii) FV-like task representation / in-context update, (iii) conditional routing, (iv) stable discoverability.
2. Verify them with operational tests below.
3. Pretrain at matched token/parameter/compute budgets.
4. Evaluate on a frozen suite containing:
   - extraction / long-context factuality;
   - format-sensitive multiple-choice (to isolate “aggregate”);
   - controlled ICL tasks (regression/classification);
   - routing stress tests (domain shifts; structured prompts).

**Falsification:** If the model passes the mechanism tests but still underperforms by a clear margin, the bundle is missing a key requirement or mis-specified.

### 10.2 Isolation tests (now tied to specific mechanisms)

| Requirement | Surgical intervention | Expected differential impact if requirement matters |
|---|---|---|
| **R1** | disable gather vs aggregate heads | extraction/format tasks collapse; local LM less affected |
| **R2** | ablate FV heads vs induction heads | few-shot ICL collapses mainly with FV ablation |
| **R3** | force static routing / freeze expert assignments | domain-shift and variable-structure tasks degrade |
| **R4** | shorten training / alter regularization | late-emerging circuits/capabilities fail to appear (grokking-like delays) |

The key is **differentiality**: if two requirements always move together, the decomposition is wrong.

---

## 11. Conclusion

With the 2024–2025 mechanistic evidence in hand, the most useful answer to “why Transformers work” is no longer “because attention is global.” It is:

1. Transformers reliably learn **tiny but powerful subsystems**: G&A retrieval heads, FV heads, and specialized routes.
2. Softmax attention (plus the residual stream) is an unusually compact substrate for **sharp selection** and **conditional computation**.
3. The current regime selects for architectures that (a) can discover these mechanisms under gradient descent and (b) run competitively on real hardware.

If a future architecture matches Transformers on sharp aggregation, FV-driven ICL, and discoverability—without attention—this synthesis should update by replacing the mechanism, not by abandoning the constraints.

---

## Appendix A: Citations (auditable in `essays/papers/`)

1. **Vaswani et al.** (2017). *Attention Is All You Need.* arXiv:1706.03762
2. **Ramsauer et al.** (2020). *Hopfield Networks is All You Need.* arXiv:2008.02217
3. **Ba et al.** (2016). *Using Fast Weights to Attend to the Recent Past.* arXiv:1610.06258
4. **Elhage et al.** (2021). *A Mathematical Framework for Transformer Circuits.* (Anthropic) transformer-circuits.pub
5. **Olsson et al.** (2022). *In-context Learning and Induction Heads.* arXiv:2209.11895
6. **Wu et al.** (2024). *Retrieval Head Mechanistically Explains Long-Context Factuality.* arXiv:2404.17551 (as in `RetrievalHead_LongContext_2024.md`)
7. **Bick et al.** (2025). *Understanding the Skill Gap in Recurrent Language Models: The Role of the Gather-and-Aggregate Mechanism.* arXiv:2506.??? (as in `SSM_SkillGap_GatherAggregate_2025.md`)
8. **Wang, Shi & Fox** (2025). *Test-time regression: a unifying framework for designing sequence models with associative memory.* arXiv:2503.23211 (as in `TestTimeRegression_2025.md`)
9. **Dao & Gu** (2024). *Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality.* arXiv:2405.?? (as in `Mamba2_SSM_Duality_2024.md`)
10. **Gu & Dao** (2024). *Mamba: Linear-Time Sequence Modeling with Selective State Spaces.* arXiv:2312.00752
11. **Lieber et al.** (2024). *Jamba: A Hybrid Transformer-Mamba Language Model.* arXiv:2403.19887
12. **Yin & Steinhardt** (2025). *Which Attention Heads Matter for In-Context Learning?* arXiv:2501.01041 (as in `WhichAttentionHeads_ICL_2025.md`)
13. **von Oswald et al.** (2023). *Transformers learn in-context by gradient descent.* arXiv:2212.07677
14. **Garg et al.** (2022). *What Can Transformers Learn In-Context?* arXiv:2208.01066
15. **Xie et al.** (2022). *An Explanation of In-context Learning as Implicit Bayesian Inference.* arXiv:2111.02080
16. **Minegishi et al.** (2025). *Beyond Induction Heads: In-Context Meta Learning Induces Multi-Phase Circuit Emergence.* arXiv:2409.?? (as in `BeyondInductionHeads_Circuits_2025.md`)
17. **Ferrando & Voita** (2024). *Information Flow Routes: Automatically Interpreting Language Models at Scale.* arXiv:2404.28000 (as in `information_flow_routes_2024.md`)
18. **IAAR survey** (2024). *Attention Heads Survey.* (as in `attention_heads_survey_2024.md`)
19. **Arnold et al.** (2024). *Routing in Sparsely-gated Language Models responds to Context.* arXiv:2409.07014 (as in `moe_routing_context_2024.md`)
20. **Gao et al.** (2024). *Weight-sparse transformers have interpretable circuits.* arXiv:2511.13653 (as in `weight_sparse_circuits_2024.md`)
21. **Power et al.** (2022). *Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets.* arXiv:2201.02177
22. **Frankle & Carbin** (2019). *The Lottery Ticket Hypothesis.* arXiv:1803.03635
23. **De et al.** (2024). *Griffin: Mixing Gated Linear Recurrences with Local Attention for Efficient Language Models.* arXiv:2402.19427
24. **Kuratov et al.** (2024). *In Search of Needles in a 11M Haystack: Recurrent Memory Finds What LLMs Miss.* arXiv:2409.07012 (as in `BABILong_11M_Haystack_2024.md`)
25. **Pérez et al.** (2019). *On the Turing Completeness of Modern Neural Network Architectures.* arXiv:1901.03429
