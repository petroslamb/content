# Why Transformers Work: A Convergent Synthesis

*Working Note v5.3 — February 5, 2026. Aligned to the local evidence bundle in `papers/` and the Feb 2026 syntheses in `new_evidence/` (evidence notes R1–R4 + `new_evidence/composition_and_limits_insights.md`). This draft reorganizes the evidence into a **core bundle** (R0/R1/R2/R4) plus an **extended** hypothesis (R3).*

---

## Guiding Question (Capability Bundle)

In the 2023–2026 decoder-only LLM regime (as scoped in §1.1), what set of internal capabilities must a sequence model satisfy simultaneously—and what training dynamics must reliably produce them—to reproduce the observed LLM capability package at scale (**separately** from the economic/hardware forces that sustain dominance)?

*Observed capability package (non-exhaustive):* reliable in-prompt use of information at long context (retrieval/extraction/copying), strong few-shot generalization from in-prompt examples, and robust performance under brittle evaluation/decoding constraints (e.g., exact-match extraction; answer-letter-only multiple choice).

---

## Abstract

“Why Transformers work” is not one mechanism. In the dominant 2023–2026 regime (dense autoregressive pretraining; deep residual stacks; accelerator-friendly kernels), the strongest evidence now supports a sharper, more localized story: **high-impact capabilities concentrate in small, specialized subcircuits**, especially a handful of attention heads that implement **selective in-context retrieval** and **few-shot task inference**. Transformers dominate not because every head is a global reasoner, but because the architecture and training dynamics reliably *discover and exploit* these bottlenecks—and the ecosystem runs them cheaply.

This note synthesizes the convergent constraints implied by the current paper set, labels what is Strong/Moderate/Speculative, and spells out falsification targets.

---

## Two-Page Spine (read this first)

### The one-line claim (capability, not dominance)

In the current decoder-only regime, LLM capability is best explained by a **small set of discoverable bottlenecks** implementing a minimal **Retrieve → Compile → Execute** pipeline (plus the training dynamics that reliably find and stabilize those bottlenecks).

### What “regime” means here (substrate assumptions)

This note is conditional on the mainstream setup:

- a **causal autoregressive decoder** (tokens only access prior tokens; generation is next-token sampling/decoding);
- **next-token prediction** training at every position;
- a deep residual stack (the **residual stream as a per-token workspace/highway**) + a tokenwise nonlinear “executor” step;
- gradient-based training via backprop (Adam/SGD-family);
- practical constraints where throughput/latency and GPU kernels shape what survives.

These are not “requirements” in the R-sense; they define the playing field.

### The core capability bundle (what must be implemented on top of the substrate)

We use four core requirements. Each is intended to be **implementation-agnostic** (Transformers are one implementation).

| Capability | What it must do (operational) | Why we think it’s load-bearing |
|---|---|---|
| **R0 — Executor + parametric substrate** | perform high-capacity **tokenwise rewrites** on a persistent workspace, using learned features/skills stored in weights | without a strong executor substrate, “mixed” information doesn’t reliably become brittle, correct outputs |
| **R1 — Sharp contextual readout** | retrieve/extract/copy from token-indexed in-prompt memory with **low-entropy selection** (G&A / sharp aggregation) | small probability leaks become format errors; evidence localizes to sparse causal heads |
| **R2 — Prompt compiler** | infer a task/hypothesis/program from in-prompt examples/instructions and make it causally drive behavior (FV/task-vector-like mechanisms) | few-shot behavior is not just copying; it requires a control signal that modulates execution |
| **R4 — Discoverability** | training reliably finds/stabilizes the sparse bottlenecks implementing R0–R2 (phase structure / circuit selection) | explains why these mechanisms appear late, concentrate in small circuits, and become causal |

**R3 (Extended):** “meso-level switchboard / subroutine switching” is kept as an extended hypothesis until it has a distinct causal signature beyond (a) token routing in R1 and (b) feature gating in R0.

### The working model families (F1–F3) and our current best-effort choice

We do not claim the causal pipeline is proven. We adopt a working model because it yields **distinct diagnostics** and **switch conditions**.

- **F1 (current default):** **Two-interface bottleneck** — an **evidence interface** (R1) plus a **program interface** (R2) feed an executor (R0).  
  *Signature:* **double dissociation + selective rescue** should exist (evidence can fail while program holds, and vice versa).
- **F2:** **Unified online update** — retrieval + adaptation are one primitive; robust double dissociation should fail.
- **F3:** **Parametric-first executor** — capability deltas mostly track R0 interventions/capacity allocation rather than sharp contextual readout bottlenecks.

Within F1, we use the minimal spine **Retrieve → Compile → Execute**, while explicitly noting that “Retrieve” often decomposes into **Gather → Select (aggregate)** (per the G&A evidence).

### The strongest empirical anchors (what the evidence bundle forces)

If you read nothing else, these are the load-bearing constraints:

- **R1 is sparse and causal:** a small subset of retrieval/G&A heads dominate long-context factuality and strict-format extraction; targeted interventions can collapse accuracy to random baselines. (Wu et al., 2024; Bick et al., 2025)
- **R2 has a concrete circuit family:** FV heads are a main causal driver of few-shot performance at scale, emerging later than induction scaffolding. (Yin & Steinhardt, 2025)
- **Memory scaling matters:** Transformers can implement copying/retrieval behaviors that fixed-state models cannot without memory scaling with length. (Jelassi et al., 2024)
- **Dominance ≠ capability:** the ecosystem has made attention kernels extremely efficient; this explains lock-in, not mechanistic necessity. (Dao et al., 2023)

### What would change our minds (pre-registered switch conditions)

- **Against F1 (toward F2):** repeated attempts to produce a clean **double dissociation** fail (program/evidence failures always track), and FV effects collapse into pure retrieval/copy accounts under better probes.
- **Against F1 (toward F3):** context-only tasks show weak sensitivity to contextual-readout bottlenecks but strong, selective sensitivity to executor/parametric interventions (beyond generic language degradation).
- **Against the bundle as a discriminator:** a non-attention family matches strict-format retrieval/extraction *and* shows no sharp aggregation bottleneck under G&A-style interventions without reintroducing an attention-like lookup elsewhere.

### Minimal diagnostic suite (what we need next)

- **R0:** **TODO** retrieval-intact / execution-broken dissociation (context-only), plus matched-budget executor-path interventions.
- **R1:** G&A-style aggregation probes (answer-letter-only multiple choice; strict extraction; needle-in-haystack), plus retrieval-head masking vs random masking.
- **R2:** few-shot probes with FV/induction controls; measure both few-shot accuracy and token-loss difference.
- **R4:** checkpoint runs and track circuit emergence timelines; test whether pruning/regularization shifts when bottlenecks appear.
- **R3 (promotion tests):** only after R0/R1/R2 are nailed down.

### How to read the rest

- §0 is the evidence-forced executive summary.
- §3 lists the **bottlenecks we can actually point to** and introduces the working model families.
- §4 defines the **core bundle** (R0/R1/R2/R4) and keeps R3 explicitly extended.
- §7 lists the falsification suite (what would make the story die).

---

## Evidential Legend

- **Strong**: causal ablations or localized mechanisms in pretrained(-like) models; replicated across model families; or tight quantitative bottlenecks.
- **Moderate**: controlled/synthetic settings with mechanistic clarity; plausible transfer to LLMs but not yet directly localized at scale.
- **Speculative**: conceptual extrapolation or untested unification; explicit tests proposed.

---

## 0. What the new evidence forces (Executive Summary)

### 0.1 Strong claims (high confidence)

1. **Selective in-context retrieval is sparse and causal.** Long-context factuality and extractive behavior depend heavily on a small set of “retrieval heads” (≈5% of heads; only ~3–6% exceed a nontrivial retrieval-score threshold, while ~45–73% have zero retrieval score); pruning them breaks retrieval and induces hallucination without necessarily destroying fluency. (Wu et al., 2024)

2. **Retrieval often decomposes into a Gather-and-Aggregate (G&A) bottleneck with sharp choke points.** Disabling a single gather/aggregate head can collapse *format-sensitive* multiple-choice accuracy (MMLU answer-letter selection) from **66% → 25%** in a pruned Llama-3.1-8B. In hybrids, disabling just a handful of attention heads selected for aggregation can drop MMLU **64.3% → 34.9%** while leaving knowledge-task accuracy ~stable (**70%**), and swapping in a single Transformer aggregate head can partially restore MMLU (**33% → 44%**, **50%** with two heads). (Bick et al., 2025)

3. **Few-shot ICL is dominated by function-vector (FV) heads, not induction alone.** FV heads are the primary causal drivers of few-shot performance in larger models; induction heads emerge early (≈1K steps) and can act as scaffolding, but FV mechanisms emerge later (≈16K steps) and dominate at scale. As long as a model preserves its top ~2% FV heads, it can retain reasonable ICL accuracy even when induction heads are ablated. (Yin & Steinhardt, 2025)

4. **Copying/retrieval separates growing memory from fixed-state models.** A 2-layer Transformer can copy strings of exponential length (in number of heads), while fixed-state sequence models are fundamentally limited by their latent state unless memory scales with length; empirically, Transformers outperform SSMs at copying and long-context retrieval. (Jelassi et al., 2024)

5. **Attention has been engineered to run close to GEMM efficiency on GPUs (dominance, not capability).** Baseline attention implementations often reach only **25–40%** of theoretical peak throughput, while FlashAttention-2 reports **50–73%** of theoretical max FLOPs/s on A100 and up to **225 TFLOPs/s per A100 (72% model FLOPs utilization)** in GPT-style training throughput measurements. (Dao et al., 2023)

### 0.2 Moderate claims (useful, but don’t overreach)

6. **Matching perplexity does not guarantee sharp extraction or strict format adherence.** A pure-Mamba model can score far below attention on tasks that punish format drift (e.g., IMDB **84.1 (attention) vs 48.8 (Mamba) vs 90.9 (hybrid)** for 1.3B models after 250B tokens, no MoE). A separate (anonymous) 2026 Mamba-3 artifact reports an extraction gap on a cloze/truncated retrieval suite (e.g., SWDE **48.9 (Transformer) vs 28.5 (Mamba-3)** at 1.5B), but should be treated as preliminary. (Lieber et al., 2024; mamba3, 2026)

7. **Multiple formal lenses converge on attention as an associative-memory / optimization primitive.** Softmax attention is equivalent to a modern Hopfield update (energy minimization), sequence layers can be derived as “test-time regression” memories, and in controlled settings attention can implement implicit gradient descent / meta-optimization. These lenses are not identical, but they mutually support the idea that attention is unusually compact for “retrieve + compute” in a forward pass. (Ramsauer et al., 2020; Wang et al., 2025; von Oswald et al., 2023; Dai et al., 2022; von Oswald et al., 2024)

8. **Training behaves like circuit selection with phase structure.** Grokking, progress measures, lottery tickets, and “grokking ↔ winning ticket” bridges jointly support a picture where generalizing subnetworks form gradually, then become behaviorally dominant late; this aligns with observed timelines where key heads (e.g., FV heads) emerge late in training. (Power et al., 2022; Nanda et al., 2023; Frankle & Carbin, 2019; Minegishi et al., 2025, *Bridging Lottery Ticket and Grokking*)

9. **Finite precision and constant depth impose real limits (and CoT is an escape hatch).** Decoder-only Transformers can suffer representational collapse / over-squashing (distinct sequences yielding nearly identical final-token representations), worsened by low-precision formats—constraining robust counting/copying. Separately, for direct-answer, constant-depth, finite-precision Transformers, expressiveness is bounded by small circuit classes (AC0/TC0-style); allowing **T** intermediate Chain-of-Thought steps increases effective serial computation and expands what’s solvable. (Barbero et al., 2024; Li et al., 2024; Merrill et al., 2024)

10. **Attention is computationally expressive, not just a routing primitive (expressivity ≠ learnability).** Softmax-attention-only layers (with linear maps) can be universal approximators for continuous Seq2Seq functions on compact domains, and can approximate gradient-descent-like updates in-context under constructive setups. (Hu et al., 2025)

11. **Compositional generalization has concrete mechanism candidates (binding + programs).** Variable binding can emerge in phases (random → heuristic → systematic) via residual-stream “addressable memory” plus specialized heads; RASP provides a programming-language model that makes “what a Transformer can implement” more explicit (selectors + element-wise ops). (Wu et al., 2025; Weiss et al., 2021)

12. **Test-time memory updates can shift the regime.** Titans introduces a learned long-term neural memory updated at test time and reports scaling beyond 2M-token contexts with improved needle-in-haystack behavior, suggesting “attention + learned memory” is a plausible next attractor. (Behrouz et al., 2025)

### 0.3 Brutal assessment (what’s weakest / most at risk)

- **R0 (executor + parametric substrate) is newly explicit and currently under-diagnosed**: we have strong motivation and partial mechanistic evidence for “MLPs as parametric memories,” but few clean dissociations showing “retrieval succeeded yet execution failed” under executor-path interventions.
- **The minimal causal pipeline is still best-effort, not proven**: multiple decompositions fit the evidence; we adopt working-model families (F1–F3) because they give distinct diagnostics and falsifiable switch conditions, not because we can derive them from first principles.
- **R3 is demoted to extended**: specialization/structure exists, but we lack decisive LLM-scale evidence that a distinct “meso switchboard” is *necessary* for the capability package (beyond token routing in R1 and feature gating in R0).
- **Hardware co-evolution is more ecosystem than theory**: FlashAttention-2 quantifies how far attention has been pushed toward GEMM-like efficiency, but this is primarily evidence for *dominance*, not for *capability*.
- **“G&A = FV = retrieval heads” is too strong as a literal identity**: the evidence supports **convergence on sparse, selective retrieval-like subcircuits**, not proven equivalence of head sets across tasks.

### 0.4 Confidence scorecard (Feb 2026)

| Requirement | Bundle role | Confidence | Why |
|---|---|---:|---|
| **R0 (executor + parametric substrate)** | **Core** | 6.5/10 | strong motivation + partial mechanistic evidence; missing clean “retrieval intact / execution broken” dissociations |
| **R1 (sharp contextual readout / G&A)** | **Core** | 9.5/10 | localized, causal, quantitative bottlenecks in real(-ish) models |
| **R2 (prompt compiler / FV / implicit optimization)** | **Core** | 8.5/10 | strong head-level causality + multiple mechanistic constructions |
| **R4 (trainability / circuit discovery)** | **Core** | 7.5/10 | strong phase/circuit evidence on algorithmic tasks; partial linkage to LLM bottlenecks |
| **R3 (meso switchboard / modularity)** | **Extended** | 6.0/10 | clear structure exists; weaker evidence of distinct causal necessity at LLM scale |

---

## 1. Two Questions, One Confusion: Capability vs Dominance

When people ask “why Transformers work,” they usually mean one of two things:

1. **Capability:** what computations the model class can represent and *learn* under realistic training.
2. **Dominance:** why it stays on top once good enough (infrastructure, kernels, training recipes, deployment economics).

This note treats them separately. Most mechanistic work constrains **capability**; the hardware/system work constrains **dominance**.

Within this repo, “dominance” is the hardware-friction story: how the core compute maps to accelerator primitives, and how quickly specialized tooling investment turns into mature infrastructure.

### 1.1 Regime assumptions (scope)

All claims are conditional on the mainstream regime:

- decoder-only **causal** generation (tokens only access prior tokens; autoregressive decoding feeds outputs back as inputs);
- **next-token prediction** at every position (teacher forcing / standard LM objective);
- deep residual stacks with normalization and a tokenwise nonlinear “executor” step (residual stream as the main information highway / per-token workspace);
- gradient-based training via backprop (Adam/SGD-family), where “what works” is strongly shaped by what is easy to optimize end-to-end;
- generation where decode-time latency/throughput matters;
- modern accelerators where dense matmuls are fast and memory bandwidth is precious.

**Architectural baseline (to avoid category errors):** this regime requires both **contextual memory** (token-indexed information in the KV cache / activations, accessed via some readout operator) and **parametric memory** (long-term information stored in weights, accessed via tokenwise compute). In Transformers, **attention** is the contextual readout mechanism and the **MLP/FFN path** is a dominant executor and a major locus of parametric capacity. The core bundle (R0/R1/R2/R4) is defined in terms of **functional capabilities** realized on top of this substrate (and the training dynamics that discover them), not in terms of a specific implementation. The common **MLP expansion** (`d_ff > d_model`) can be read as a practical allocation choice: increase local compute + parametric capacity without proportionally increasing cross-token bandwidth/KV-cache costs that scale with `d_model`. (Geva et al., 2020; Nichani et al., 2024)

Change the regime (explicit memory, different objectives, different hardware), and the bundle can change.

---

## 2. A Unifying Computational Frame (to prevent hand-wavy stories)

This essay uses four complementary “frames” that show up repeatedly across the evidence:

1. **Attention as energy-based associative memory (Hopfield) + sharp selection.** Softmax attention is equivalent to a modern Hopfield update rule; selectivity and fixed points vary by layer/head and can be characterized in that language. (Ramsauer et al., 2020; Hu et al., 2025)  
   *Use:* explains why exponential softmax selectivity matters for sharp retrieval and why different heads can behave qualitatively differently.

2. **Sequence layers as associative memory via test-time regression.** Many architectures (softmax attention, linear attention, SSMs, fast-weight layers, online learners) can be derived as “memorize then retrieve” regression layers; their differences come from which regression objective/approximation/normalization they implement. (Wang et al., 2025)  
   *Use:* turns “attention vs recurrence” into “which memory + which approximation,” clarifying where retrieval breaks.

3. **Attention as fast-weight / hypernetwork-style conditional computation.** Linear attention can be seen as a fast-weight programmer (outer-product memory updates), and multi-head attention can be reformulated as a hypernetwork where a low-dimensional latent code specifies key-query-specific operations. (Schlag et al., 2021; Schug et al., 2025)  
   *Use:* provides a concrete mechanism for conditional computation and compositional generalization that looks like routing without explicit gates.

4. **Transformers as sequence programs (RASP).** RASP maps attention into *selectors* and MLPs into element-wise operations, providing short “programs” for tasks like histograms, sorting, and Dyck languages and relating difficulty to the number of layers/heads required. (Weiss et al., 2021)  
   *Use:* makes compositional generalization and “algorithmic depth” discussions less metaphorical.

These frames do not “prove Transformers are optimal.” They constrain *what must be implemented* to match observed behaviors.

---

## 3. Cross-Cutting Convergence: Sparse, Selective Bottlenecks

Across retrieval, ICL, and routing work, a repeated pattern appears:

> **High-value behavior concentrates in small, specialized components, which become causal bottlenecks.**

### 3.0 Operational definitions (to keep “bottleneck” falsifiable)

- **Bottleneck (component-level):** a small set of components (often heads) such that targeted disabling causes a large, task-specific drop *compared to disabling the same number of random components*, and swapping/adding back those components largely recovers the behavior.
- **Sharp aggregation:** the model must select among a small number of candidate summaries with low ambiguity (argmax-like in effect). These are the settings where tiny probability mass “leakage” becomes a format error (e.g., wrong answer letter), and performance can collapse to a random baseline.
- **Routing:** input-dependent selection of which *computation path* dominates (head specialization, route structure, MoE expert choice, or threshold-like activation), distinct from mere content retrieval.

### 3.1 The bottlenecks we can actually point to

| Bottleneck name (paper) | What it does (operational) | Evidence type | Status |
|---|---|---|---|
| **Retrieval heads** (Wu et al., 2024) | redirect/copy relevant tokens from long context; supports long-context factuality and CoT reference | sparse + causal pruning | **Strong** |
| **Gather / Aggregate heads** (Bick et al.) | two-stage retrieval: gather summaries → aggregate/select sharply | targeted head disable + hybrid delegation | **Strong** |
| **Function-vector (FV) heads** (Yin & Steinhardt) | compute latent task representation driving few-shot behavior | head ablations + training-time emergence | **Strong** |
| **Variable-binding heads** (Wu et al., 2025) | route variable→value bindings via residual-stream “addressable memory”; supports systematic dereferencing | causal interventions in symbolic programs | **Moderate** |
| **Multi-phase ICL circuits** (Minegishi et al., 2025, *Beyond Induction Heads*) | circuit succession (non-context → semi-context → full-context) | mechanistic tracking in controlled setup | **Moderate** |
| **Attention sinks / thresholding** (Gao et al.) | use sink tokens (e.g., BOS) as thresholding for discrete decisions | circuit-level analysis in sparse models | **Moderate** |

### 3.2 Important caution: “same heads” is a hypothesis, not a fact

It’s tempting to say “retrieval heads = FV heads = G&A heads.” What we actually have is:

- multiple independent papers finding **sparse head subsets** with **causal impact** on different behaviors;
- a shared computational motif: **content-addressable selection + aggregation**.

The evidence supports **convergence on a motif**, not literal identity of head sets across tasks.

---

### 3.3 Working Models: Competing Minimal Pipelines (Best-Effort)

We do not claim the causal pipeline is proven. Multiple decompositions fit the current evidence. We adopt a **best-effort working model** because it yields the cleanest diagnostics and falsifiable predictions, and we state what evidence would make us switch.

#### Pipeline families (F1–F3)

**F1 — Two-interface bottleneck (Evidence + Program → Execute)**  
*Claim:* the model forms two separable internal interfaces:

- **Evidence interface (R1):** what to pull from the prompt now (token-indexed, sharp readout/aggregation).
- **Program interface (R2):** what mapping/criterion to apply (task representation inferred from demonstrations/instructions).

These feed an executor substrate (**R0**) that rewrites the per-token workspace; **R4** explains how training finds/stabilizes the sparse bottlenecks implementing these interfaces.  
*Key signature:* **double dissociation + selective rescue** exists (evidence can fail while program holds, and vice versa).

**F2 — Unified online update (single primitive for in-context use + adaptation)**  
*Claim:* “retrieval” and “adaptation” are largely the same underlying primitive (online regression / fast weights / implicit GD-like update). The evidence/program split is not fundamental; interventions should mostly hit a shared update mechanism rather than separable interfaces.  
*Key signature:* robust double dissociation fails; program failures track evidence failures (or the mechanism sets overlap heavily).

**F3 — Parametric-first executor (store/compute dominates; context is a bus)**  
*Claim:* the decisive substrate is parametric capacity + tokenwise rewrite (**R0**); contextual readout provides communication, but the capability package is dominated by what is stored/computed in the parametric substrate.  
*Key signature:* major capability deltas track executor/parametric interventions and capacity allocation more than contextual readout bottlenecks.

#### Within-F1 representations (A/B/C are granularity choices, not true alternatives)

- **A) Retrieve → Compile → Execute (minimal spine):** evidence readout → program inference → tokenwise execution.
- **B) Two-vector model (compressed shorthand):** “content/evidence” + “control/program” vectors drive execution (clean but risks vagueness).
- **C) Gather → Select → Program → Write (more concrete):** splits retrieval into candidate formation (gather) and sharp selection (aggregate), aligning with G&A evidence.

**Best-effort presentation choice (current):** use **A** as the spine (minimal pipeline), and explicitly note that retrieval often decomposes into **Gather/Select** (import the key win of C without multiplying moving parts). Treat **B** as a shorthand, not the primary exposition.

#### Best-effort selection heuristic (pre-registered)

We pick the working family that maximizes: evidence fit, distinct intervention signatures, coverage, falsifiability, and near-term actionability. Simplicity is a tiebreaker, not a free pass.

**TODO:** add a small score table once we define the minimal diagnostic suite below.

#### Switch conditions (what would make us change our mind)

- **TODO (F1 vs F2):** double dissociation fails under clean diagnostics (program/evidence failures always track), or FV-like effects collapse into improved retrieval/copy accounts under better probes.
- **TODO (F1 vs F3):** context-only tasks show weak sensitivity to contextual readout bottlenecks but strong, selective sensitivity to executor/parametric interventions (beyond generic language degradation).

#### Minimal diagnostic suite (placeholders)

- **TODO:** F1↔F2 adjudicator: “double dissociation + selective rescue” task family.
- **TODO:** F1↔F3 adjudicator: context-only vs parametric-only isolation + matched interventions.
- **TODO:** R0 adjudicator: retrieval-intact / execution-broken dissociation.

---

## 4. Core Capability Bundle (R0/R1/R2/R4), Evidence-Aligned

We organize the evidence around a **core capability bundle** that must be satisfied *simultaneously* under the regime:

- **R0:** execution substrate (workspace + executor + parametric capacity)
- **R1:** sharp contextual readout (retrieval / Gather-and-Aggregate)
- **R2:** prompt “compiler” (task inference / FV heads and related constructs)
- **R4:** trainability / circuit discovery (why training finds and stabilizes the sparse bottlenecks)

**R3** is retained as an **extended** hypothesis, with explicit promotion criteria, because “routing” is overloaded and the current necessity evidence is weaker.

### R0. Execution Substrate (Workspace + Executor + Parametric Capacity)

**Operational definition:** the model maintains a persistent per-token workspace across depth (residual highway) and applies a high-capacity tokenwise rewrite at each layer that can (i) construct nonlinear features from whatever context has been mixed into the token state, and (ii) store/use parametric associations/skills needed when the prompt does not explicitly contain the answer. In other words: once the right inputs are present in a token’s state (from contextual readout and/or a task representation), the model must have enough local compute and parametric capacity to execute the transformation and drive brittle outputs.

**Why it’s load-bearing:** attention (R1) is the communication/readout operator; “program” inference (R2) is the control signal. R0 is the executor that turns those into behavior. Without a strong executor substrate, the model can still mix information, but it becomes hard to reliably compute with mixed information (and to pack many reusable skills into weights).

**Status (Feb 2026):** **Moderate.** Strongly motivated by modern decoder design and partial evidence that FFN/MLP pathways behave like parametric/associative memory, but less cleanly localized as a small causal bottleneck than R1/R2.

#### Evidence we currently have (partial)

- **FFN/MLP pathways behave like key–value memories over learned patterns.** (Geva et al., 2020)
- **Factual recall capacity can be realized via parametric capacity and associative-memory constructions.** (Nichani et al., 2024)

#### Diagnostics we still need (TODO)

- **TODO (R0-D1):** a clean “retrieval succeeded but execution failed” dissociation (context-only).
- **TODO (R0-D2):** an attention-vs-executor ablation/patching dissociation with matched budgets.
- **TODO (R0-D3):** a capacity-allocation sensitivity result (executor capacity vs workspace/communication capacity) that predicts selective behavioral changes beyond perplexity.

#### Falsification target (R0)

> A model family reproduces the observed capability package at scale without an equivalent high-capacity tokenwise executor/parametric substrate (i.e., no meaningful local rewrite capacity beyond mixing), and executor-path ablations do not selectively impair “apply-the-rule” behaviors beyond generic language degradation.

### R1. Sharp In-Context Retrieval (G&A + retrieval heads)

**Operational definition:** given a query embedded in the current context, the model can (a) locate relevant spans/items anywhere in-context and (b) select/compose the right item(s) with sufficiently **sharp discrimination** to support extraction and strict formats.

This avoids the ambiguous phrase “random access.” What matters is **selective readout** from token-indexed memory (KV cache / residual stream).

*Frame mapping:* this is where **Hopfield selectivity** (sharp fixed points) and **test-time regression** (parametric vs non-parametric memory) do the most explanatory work. (Ramsauer et al., 2020; Wang et al., 2025)

#### R1.1 Mechanistic claim: retrieval decomposes into Gather-and-Aggregate

**Strong:** Retrieval in real models localizes to a two-stage pattern:

- **Gather:** condense candidate information into summary tokens (often end-of-segment tokens like newline).
- **Aggregate:** attend over summaries to select the right one (often argmax-like).

Transformers and SSMs both exhibit the pattern, but SSM implementations tend to be smoother and have trouble reproducing sharp aggregation cheaply. (Bick et al., 2025)

#### R1.2 Load-bearing evidence

- **Sparse, intrinsic, causal retrieval heads** drive long-context factuality; masking them causes retrieval failure/hallucination and affects CoT reasoning that must refer back to context. Retrieval is sparse: only ~3–6% of heads cross a nontrivial retrieval-score threshold, while ~45–73% have zero retrieval score. (Wu et al., 2024)
- **Copying separates growing vs fixed memory.** A 2-layer Transformer can copy strings of exponential length (in number of heads), while fixed-state models cannot copy arbitrary long strings unless their state scales with length; pretrained Transformers outperform SSMs on copying and retrieval. (Jelassi et al., 2024)
- **Format-sensitive multiple choice can be bottlenecked by aggregation, not knowledge.** Disabling a single gather/aggregate head in a pruned Llama-3.1-8B collapses MMLU answer-letter selection **66% → 25%** (random), even though “knowledge” is distributed. (Bick et al., 2025)
- **Hybrid wins localize to the Aggregate stage.** In Zamba2-7B, disabling nine attention heads selected for MMLU aggregation drops MMLU **64.3% → 34.9%** while knowledge-task accuracy stays at **70%**; in a hybrid replacement experiment, swapping in a single Transformer layer/head containing prominent G&A heads restores MMLU **33% → 44%** (and **50%** with two heads). (Bick et al., 2025)
- **Mechanistic differences across “efficient” architectures are real.** Transformers/Based solve associative recall via induction; Mamba’s success depends heavily on short convolutions for association; H3/Hyena fail on associative recall. (Arora et al., 2025)
- **Parametric vs contextual memory matters.** FFN layers act like key-value memories over training patterns (Geva et al., 2020), and factual recall capacity can be achieved via either attention or MLP capacity in synthetic constructions (Nichani et al., 2024). This helps explain why some “knowledge” tasks survive retrieval-head ablations while extraction/factuality collapses. (Wu et al., 2024; Nichani et al., 2024)

#### R1.3 Why this discriminates architectures (synthesis, careful)

**Moderate:** The test-time regression framework reframes “attention vs recurrence” as **non-parametric vs parametric memory**: parametric regression layers tend to admit efficient recurrences (fixed-size state updates), while non-parametric layers like softmax attention do not, and can therefore represent token-indexed associations without compressing them into a fixed state. (Wang et al., 2025)

This supports a cautious discriminator hypothesis: **low-entropy selection over many candidates** (sharp aggregation) is easier to implement when you can represent many candidates explicitly (KV cache) and apply an exponential-kernel selection step, than when you must compress candidates into a fixed-size state or a linearized kernel. SSD further shows SSMs can be written in attention-like quadratic form, but the efficient linear-time implementations are still constrained by state size and approximation choices. (Wang et al., 2025; Dao & Gu, 2024)

#### R1.4 Counterevidence and boundary conditions

- **Local attention sets a hard coverage ceiling.** Griffin can solve phonebook lookup up to its local window size (1024), then degrades when the relevant entry falls outside the window. (De et al., 2024)
- **Decoder-only stacks can collapse information at long lengths (precision matters).** Distinct sequences can yield arbitrarily close final-token representations (“representational collapse”), and causal masking can over-squash early-token information—effects exacerbated by low-precision formats—constraining robust counting/copying without mitigations. (Barbero et al., 2024)
- **Explicit memory augmentation can dominate at extreme lengths.** Memory-augmented recurrent models can handle orders-of-magnitude longer inputs (up to ~11M elements in BABILong), changing the regime. (Kuratov et al., 2024)

#### Falsification target (R1)

> A non-attention architecture matches Transformers on extraction/format-sensitive retrieval *and* shows no concentrated “sharp aggregation” bottleneck under G&A-style interventions—without reintroducing an attention-like sparse lookup somewhere else.

---

### R2. Inference-Time Learning (ICL as computation, not just copying)

**Operational definition:** the forward pass can infer a task/hypothesis from examples in the prompt and apply it, behaving like an inner-loop learner (gradient descent, Bayesian inference, algorithm selection, etc.) without parameter updates.

*Frame mapping:* this is where the **optimization/meta-learning lenses** (GD/Bayes/mesa) need to cash out in concrete circuits (e.g., FV heads), rather than staying as “possible in principle.” (von Oswald et al., 2023; Xie et al., 2022; Yin & Steinhardt, 2025)

#### R2.1 Mechanistic claim: induction is real scaffolding; FV heads are the main causal driver at scale

- **Induction circuits exist** and explain a broad class of in-context copying patterns. (Olsson et al., 2022)
- **FV heads drive few-shot accuracy** and emerge later than induction heads; many FV heads begin as induction-like heads and transition later. Quantitatively, induction heads emerge around step ~1K (in Pythia training), while FV heads appear around ~16K; preserving a model’s top ~2% FV heads can retain reasonable few-shot ICL accuracy even if induction heads are ablated. (Yin & Steinhardt, 2025)
- **ICL circuit emergence can be multi-phase** (non-context → semi-context → full-context) in controlled meta-learning settings, consistent with “capability as circuit succession.” (Minegishi et al., 2025, *Beyond Induction Heads*)

**Practical caution:** “few-shot ICL accuracy” and “token-loss difference” probe different things; ablations can affect them differently, which helps explain why some prior work over-attributed ICL to induction alone. (Yin & Steinhardt, 2025)

#### R2.2 Formal lenses that now have concrete grounding

**Moderate:** in controlled settings, transformers can be constructed or shown to implement:

- **gradient-descent-like updates** in a forward pass (von Oswald et al., 2023; Dai et al., 2022),
- **mesa-optimization** algorithms that arise under next-token training on synthetic sequence prediction tasks (von Oswald et al., 2024),
- **Bayesian inference over latent concepts** as a route to ICL (Xie et al., 2022),
- **function-class learning** matching classical estimators for several families (Garg et al., 2022),
- **universal approximation guarantees** for ICL via constructive transformers solving Lasso-like representations at test time. (Li et al., 2025)
- **attention-only universality (expressivity)**: attention-only layers (with linear maps + softmax selection) can be universal approximators for continuous Seq2Seq functions on compact domains and can approximate gradient-descent-like updates in-context under constructive setups. (Hu et al., 2025)

These do not prove “LLMs literally run GD,” but they constrain what’s *possible* and what training can discover.

#### R2.3 New synthesis: Hopfield ↔ optimization is complementary, not competing

**Speculative (but supported by convergent framing):** The Hopfield view (attention as energy minimization over patterns) and the meta-optimization view (attention as implicit update rule) can be treated as two angles on the same primitive: **softmax attention performs a sharp, differentiable selection-and-update step**. That same step can be used for (a) retrieving relevant examples, and (b) computing an in-context hypothesis or task vector that modulates downstream computation.

#### R2.4 Thinking time as effective depth (CoT as serial compute)

**Moderate (theory + synthetic evidence):** A useful separation is between “what happens in one forward pass” and “what happens with additional autoregressive steps.”

- Without CoT, **direct-answer** constant-depth, finite-precision decoder-only Transformers are bounded by small circuit classes (prior TC0-style bounds; and an AC0 bound under constant-bit precision). (Merrill et al., 2024; Li et al., 2024)
- With **T** intermediate CoT steps, a constant-depth Transformer can simulate circuits of size **T** (under the paper’s precision/embedding assumptions), effectively buying serial computation proportional to thinking length. Empirically this matters on inherently serial problems (e.g., permutation composition / iterated squaring / circuit value) in the studied regime. (Li et al., 2024)

This is not “ICL” in the narrow few-shot sense, but it is **inference-time computation** that helps explain why “thinking tokens” can change the capability envelope.

#### Falsification target (R2)

> A model family matches Transformer few-shot ICL while lacking any FV-like head family (or equivalent latent task representation) and showing no evidence of forward-pass inner-loop computation in controlled probes.

---

### R3 (Extended). Meso-Level Switchboard (Subroutine Switching)

**Clarification: “routing” is overloaded.**

- **Token routing** (softmax selecting positions within a head) is part of **R1** (sharp contextual readout/aggregation).
- **Feature/path gating** inside tokenwise nonlinearities is part of **R0** (executor substrate).
- **R3 (here)** is narrower: input/state-dependent switching between distinct internal subroutines/circuit paths (“mode control”), beyond what is already explained by R0/R1/R2.

**Operational definition:** the model conditionally selects *which computation path dominates* (stage controllers, mode switches, modular subcircuits, expert-like specialization) in a way that is causally necessary for some part of the capability package.

**Why R3 is not core (yet):** we have strong descriptive evidence that specialization/structure exists, but limited LLM-scale evidence that a distinct “switchboard” mechanism is *necessary* (as opposed to an emergent/efficient organization of R0+R1+R2).

**Promotion criterion:** upgrade R3 to core only if we can specify a diagnostic with a distinct intervention signature:

- removing/scrambling a candidate “mode/switch” signal (or forcing effectively static mixing) causes selective collapse on subroutine-switch inputs while leaving core R0/R1/R2 behaviors largely intact, and
- restoring the switch signal rescues performance.

*Frame mapping:* the most concrete story here is “conditional compute without explicit gates”: multi-head attention as a hypernetwork/fast-weight system, plus threshold-like primitives (attention sinks) that can approximate discrete routing. (Schug et al., 2025; Gao et al., 2025)

#### R3.1 Evidence we have (and what it does / doesn’t show)

- **Head-type diversity is real and broad.** A survey catalogues 30+ attention head types and proposes a staged framework (knowledge recall → identification → latent reasoning → expression preparation). (Zheng et al., 2024)
- **Routes are extractable at scale and show structure.** Attribution-based “information flow routes” show clustering by part-of-speech and subword position, plus domain-specialized components that activate for code/multilingual domains. (Ferrando & Voita, 2024)
- **MoE routing is not purely context-free.** Routing decisions correlate with semantic associations and are modulated by context, with encoder/decoder differences. (Arnold et al., 2024) A broader MoE analysis finds routing often favors experts with larger output norms, suggesting a practical “winner-take-loudest” routing tendency. (Lo et al., 2024)
- **Attention can implement threshold-like discrete selection.** In weight-sparse transformer circuits, “attention sinks” enable softmax to act like a threshold (q·k vs a large sink logit), turning continuous features into near-binary routing signals. (Gao et al., 2025)
- **Circuit-level edits can transfer (at least partially) across sparsity.** Bridging experiments suggest some interpretable perturbations discovered in weight-sparse “model organisms” can be mapped into corresponding dense-model perturbations with behaviorally consistent effects. (Gao et al., 2025)
- **Compositional generalization has a concrete mechanism candidate.** Reformulating attention as a hypernetwork yields latent codes predictive of subtasks on unseen compositions; increasing hypernetwork expressivity improves compositional generalization on abstract reasoning tasks. (Schug et al., 2025)
- **Variable binding can emerge as residual-stream addressable memory.** In symbolic program dereferencing, training shows a three-phase trajectory (random → heuristic → systematic), with specialized heads routing variable–value bindings across token positions and layers. (Wu et al., 2025)
- **RASP provides a constructive “what algorithms fit” language.** RASP programs compile to selector patterns and element-wise ops, giving compact solutions for tasks like sorting/histograms/Dyck and relating them to required layers/heads. (Weiss et al., 2021)
- **Multi-head specialization can implement “stage control.”** In a symbolic path-finding setting, a 1-layer transformer uses one head to advance within the current stage and another “stage controller” head to detect when to switch stages (backward → forward), enabling multi-stage reasoning in a single autoregressive pass. (**Moderate**) (Yang et al., 2025)

**Brutal reading:** this is strong evidence that conditional structure exists, but still limited evidence that “routing as such” is the decisive discriminator between whole architecture families in the wild.

#### Falsification / promotion target (R3)

> A model family matches Transformers on tasks where success requires switching between distinct internal stages/subroutines (not just retrieving different content), and forcing effectively static mixing (or scrambling the candidate controller signal) has no selective effect—suggesting no distinct “switchboard” beyond R0/R1/R2 is needed.

---

### R4. Trainability and Circuit Discovery (optimization as selection)

**Operational definition:** the architecture + training setup reliably discovers and stabilizes the small, specialized mechanisms implicated in the **core bundle** (R0/R1/R2), and (if extended hypotheses like R3 turn out to be necessary) discovers those as well—without brittle, per-scale heroics.

#### R4.1 Evidence that training is phase-structured circuit selection

- **Grokking:** generalization can appear *long after* memorization in algorithmic tasks; weight decay strongly affects the transition. (Power et al., 2022)
- **Mechanistic progress measures:** training dynamics can be decomposed into memorization → circuit formation → cleanup; “sudden” behavioral transitions can reflect gradual circuit amplification plus late removal of memorizing components. (Nanda et al., 2023)
- **Lottery tickets:** sparse subnetworks with specific initializations can train unusually well and match dense performance; reinitialization destroys the effect. (Frankle & Carbin, 2019)
- **Bridging LTH and grokking:** “grokked tickets” (tickets extracted during generalization) reduce delayed generalization, supporting “good structure discovery” as causal. (Minegishi et al., 2025, *Bridging Lottery Ticket and Grokking*)
- **Symbolic variable binding shows a phase transition.** A Transformer trained on variable dereferencing exhibits a three-phase trajectory, with a late transition to a systematic binding/lookup mechanism mediated by specialized heads. (**Moderate**) (Wu et al., 2025)
- **Scaling + phase transitions:** loss scales predictably with size/data/compute (Kaplan et al., 2020), but some downstream abilities can appear abruptly at scale (Wei et al., 2022). The coexistence of smooth loss scaling and discontinuous benchmark jumps is consistent with “circuits emerge and suddenly dominate.” (**Moderate**)

#### R4.2 Connection back to core bottlenecks (R1/R2 on R0)

**Speculative (but testable):** The sparse bottlenecks in R1/R2 (retrieval heads, FV heads) look like the kind of “winning ticket circuits” that training must discover. The observed timeline—induction early, FV later (Yin & Steinhardt, 2025)—mirrors a grokking-like story: early mechanisms fit training, later mechanisms generalize and become dominant.

#### Falsification target (R4)

> A model family that (i) trains reliably at scale but (ii) never develops sparse, causal bottlenecks analogous to contextual readout and task-inference circuits—yet matches Transformer performance on retrieval and few-shot ICL diagnostics.

---

## 5. Why Displacement Is Hard: The Selection Regime (Training + Hardware)

Even if an alternative can, in principle, satisfy the **core bundle** (R0/R1/R2/R4), it must pass two practical gates:

- **Gate 1 — Training viability:** stable optimization at the target scale (depth, width, data, long runs).
- **Gate 2 — Hardware economics:** competitive throughput/latency on real accelerators.

### 5.1 Hardware reality check (what we can actually claim)

**Strong for dominance, weak for capability:** attention has received enormous systems-level optimization. FlashAttention-2 reports that baseline attention kernels often reach only **25–40%** of theoretical peak FLOPs/s, while their IO-aware tiling + scheduling reaches **50–73%** on A100 and up to **225 TFLOPs/s per A100 (72% model FLOPs utilization)** in GPT-style training throughput measurements. (Dao et al., 2023)

From the scorecard perspective, this is the “GEMM lottery” in action:

- **GA (Global Access) / PAR (Parallelism):** the hot path is dominated by matmuls that saturate tensor cores and parallelize well.
- **MAL (Memory Access Locality):** the remaining pain (memory IO, shared-memory traffic) has been attacked with locality-aware kernels.
- **STI (Specialized Tooling Investment) → IM (Infrastructure Maturity):** high tooling investment has largely “paid off,” turning into mature infra (FlashAttention, compiler stacks, inference engines).

**Mechanistic ↔ hardware link:** long-context inference is often KV-cache bound. Wu et al. note that for LLaMA-2-7B a 100K-token KV cache can require **>50GB** (vs **<1GB** at 2K), and argue most heads are non-retrieval—suggesting targeted KV-cache pruning/compression keyed to retrieval heads as a plausible deployment lever. (Wu et al., 2024)

SSMs also pursue hardware-aware algorithms (e.g., selective SSM parallelization; SSD dual forms), but the ecosystem has already made “Transformer kernels + infra” a moving target. (Gu & Dao, 2024; Dao & Gu, 2024)

**Constraint:** do not confuse “fast on GPUs” with “more capable.” It mainly explains lock-in.

---

## 6. Counterexamples and Boundaries (where the synthesis should break)

This note is not a claim that “attention is the unique road.”

- **ICL can appear in non-Transformer families** in synthetic concept-inference regimes (LSTMs in GINC). (Xie et al., 2022)
- **Explicit memory augmentation can beat vanilla attention** on extreme-length benchmarks. (Kuratov et al., 2024)
- **SSMs can match or beat Transformers on perplexity at some scales**, and can implement retrieval-like behavior, but tend to struggle on sharp aggregation, extraction, and strict formats unless hybridized. (Bick et al., 2025; Lieber et al., 2024; Arora et al., 2025)
- **Both Transformers and common SSMs have formal state-tracking limits at constant depth/precision.** TC0-style bounds (and related results) constrain inherently sequential state tracking unless you add extra “time” (CoT steps), more expressive recurrence, or explicit memory. (Merrill et al., 2024; Li et al., 2024)
- **Decoder-only Transformers can lose information over length (over-squashing / collapse).** This is a practical boundary case for robust counting/copying under long contexts and low precision, and motivates mitigations and alternative memory designs. (Barbero et al., 2024)
- **SSMs have complementary strengths on some language classes.** Formal-language analyses show SSMs can length-generalize on some star-free state-tracking tasks and bounded hierarchical structure regimes where Transformers can fail empirically, supporting a hybrid “state + retrieval” picture. (Sarrof et al., 2024)
- **Test-time neural memory is an explicit regime shift.** Titans adds a learned long-term memory updated at test time and reports scaling beyond 2M-token contexts with strong needle-in-haystack performance, changing what “long context” even means. (Behrouz et al., 2025)

So the thesis is conditional:

> Under the current regime, the easiest-to-train, easiest-to-run way to satisfy the **core bundle** (R0/R1/R2/R4) is still Transformer-style attention—often because the crucial computations are sparse and attention implements them compactly.

---

## 7. Falsification Experiments (make the bundle die if it’s wrong)

The goal is to falsify the **bundle claim**, not defend Transformers.

### 7.1 Mechanism-level bundle test

For a candidate architecture at matched scale/compute:

1. **R0:** identify an executor/parametric substrate and test for retrieval-vs-execution dissociations (**TODO diagnostics**; matched intervention budgets).
2. **R1:** identify any retrieval bottleneck; test G&A-like interventions (gather vs aggregate disable).
3. **R2:** identify FV-like or task-vector mechanisms; ablate them vs induction-like heads.
4. **R4:** track emergence across training (do critical circuits appear late? can pruning accelerate/retard them?).

**Optional (R3 promotion tests):** test for distinct stage/mode switching beyond R0/R1/R2 by forcing effectively static mixing or scrambling suspected controller signals and checking for selective collapse + rescue.

**Minimal bundle test suite (concrete, format-sensitive):**

- **R0 (executor):** **TODO** retrieval-intact / execution-broken task family + executor-path interventions (matched to R1/R2 budgets).
- **R1 (aggregation):** MMLU-style answer-letter selection (A/B/C/D) with strict decoding; measure collapse toward the 25% random baseline under aggregate-head interventions. (Bick et al., 2025)
- **R1 (extraction):** semi-structured extraction (e.g., SWDE-style) with exact-match scoring; include distractors and format constraints.
- **R1 (long-context):** needle-in-a-haystack factual retrieval at varying depths; verify a sparse retrieval-head set and test targeted masking vs random masking. (Wu et al., 2024)
- **R1 (copying):** synthetic copying/repeat tasks with length generalization; compare “growing memory” models to fixed-state models at matched scale/compute. (Jelassi et al., 2024)
- **R1 (precision stress):** counting/copying under longer contexts and reduced precision to test for representational collapse / over-squashing failure modes. (Barbero et al., 2024)
- **R2 (few-shot):** few-shot classification/regression probes; report both *few-shot accuracy* and *token-loss difference*, and ablate FV heads with induction-head exclusion. (Yin & Steinhardt, 2025)
- **R2 (serial compute):** permutation composition / iterated squaring / circuit value with and without CoT; measure “depth vs thinking tokens” tradeoffs. (Li et al., 2024; Merrill et al., 2024)
- **R3 (promotion test / stage switches):** tasks with explicit multi-stage traces (e.g., backward→forward scratchpad); test for a small “stage controller” mechanism and measure degradation when forcing static mixing. (Yang et al., 2025)
- **R3 (promotion test / binding):** variable dereferencing with distractors; test for phase transitions and localized binding/lookup circuitry. (Wu et al., 2025)
- **R4 (emergence):** checkpoint the run and track when retrieval/FV bottlenecks appear (and whether pruning/regularization shifts their emergence).

### 7.2 A concrete “drop-in replacement” falsifier

> Train a pure SSM/linear-attention family to match Transformer performance on extraction/format-sensitive retrieval *and* demonstrate it has no sparse sharp-selection bottleneck analogous to aggregate heads.

If this succeeds, the strongest version of R1-as-discriminator is wrong, and the synthesis must update.

---

## 8. What Would Strengthen or Break This Note Next?

High-value next evidence (some is not in the current bundle):

1. **Direct overlap mapping**: are retrieval heads, G&A heads, and FV heads the same components, partially overlapping, or disjoint? (requires joint instrumentation across tasks)
2. **Causal routing tests at LLM scale**: show that specific routing structures are *necessary* for downstream generalization, not just present.
3. **Sharper negative results**: identify tasks where pure SSMs truly match sharp aggregation *without* attention-like quadratic steps.
4. **Regime shifts**: more work like BABILong that changes the memory regime (external/recurrent memory, retrieval augmentation) and compares mechanisms fairly.

---

## Appendix A: Citations (auditable in `papers/`)

*arXiv identifiers below are decoded from each markdown artifact’s header (the PDF→MD conversion includes a reversible arXiv stamp).*

- `Vaswani_Attention_2017.md` — Vaswani et al., *Attention Is All You Need* (2017). arXiv:1706.03762v7
- `Ramsauer_Hopfield_2020.md` — Ramsauer et al., *Hopfield Networks is All You Need* (2020). arXiv:2008.02217v3
- `Ba_FastWeights_2016.md` — Ba et al., *Using Fast Weights to Attend to the Recent Past* (2016). arXiv:1610.06258v3
- `LinearTransformers_FastWeights_2021.md` — Schlag et al., *Linear Transformers Are Secretly Fast Weight Programmers* (2021). arXiv:2102.11174v3
- `AttentionHypernetwork_2024.md` — Schug et al., *Attention as a Hypernetwork* (ICLR 2025). arXiv:2406.05816v4
- `TransformersLearnReasoning_2025.md` — Yang et al., *Multi-head Transformers Provably Learn Symbolic Multi-step Reasoning via Gradient Descent* (2025). arXiv:2508.08222v2
- `FFN_KeyValue_Memory_2020.md` — Geva et al., *Transformer Feed-Forward Layers Are Key-Value Memories* (2020). arXiv:2012.14913v2
- `FactualRecall_AssociativeMemory_2024.md` — Nichani et al., *Understanding Factual Recall in Transformers via Associative Memories* (2024). arXiv:2412.06538v1
- `RetrievalHead_LongContext_2024.md` — Wu et al., *Retrieval Head Mechanistically Explains Long-Context Factuality* (2024). arXiv:2404.15574v1
- `SSM_SkillGap_GatherAggregate_2025.md` — Bick et al., *Understanding the Skill Gap in Recurrent LMs: Gather-and-Aggregate* (2025). arXiv:2504.18574v2
- `TestTimeRegression_2025.md` — Wang et al., *Test-time regression: associative memory sequence layers* (2025). arXiv:2501.12352v3
- `Mamba2_SSM_Duality_2024.md` — Dao & Gu, *Transformers are SSMs… Structured State Space Duality* (2024). arXiv:2405.21060v1
- `Gu_Mamba_2024.md` — Gu & Dao, *Mamba: Linear-Time Sequence Modeling with Selective State Spaces* (2024). arXiv:2312.00752v2
- `SSM_Transformer_MechanisticEval_2025.md` — Arora et al., *Mechanistic Evaluation of Transformers and State Space Models* (2025). arXiv:2505.15105v3
- `Lieber_Jamba_2024.md` — Lieber et al., *Jamba: A Hybrid Transformer-Mamba Language Model* (2024). arXiv:2403.19887v2
- `mamba3.md` — *Mamba-3* (ICLR 2026 submission; anonymous; no arXiv identifier in artifact)
- `De_Griffin_2024.md` — De et al., *Griffin: Mixing Gated Linear Recurrences with Local Attention* (2024). arXiv:2402.19427v1
- `BABILong_11M_Haystack_2024.md` — Kuratov et al., *In Search of Needles in a 11M Haystack…* (2024). arXiv:2402.10790v2
- `Olsson_InductionHeads_2022.md` — Olsson et al., *In-context Learning and Induction Heads* (2022). Transformer Circuits Thread (transformer-circuits.pub; no arXiv in artifact)
- `WhichAttentionHeads_ICL_2025.md` — Yin & Steinhardt, *Which Attention Heads Matter for In-Context Learning?* (2025). arXiv:2502.14010v1
- `BeyondInductionHeads_Circuits_2025.md` — Minegishi et al., *Beyond Induction Heads… Multi-Phase Circuit Emergence* (2025). arXiv:2505.16694v2
- `VonOswald_GradientDescent_2023.md` — von Oswald et al., *Transformers Learn In-Context by Gradient Descent* (2023). arXiv:2212.07677v2
- `MesaOptimization_Transformers_2023.md` — von Oswald et al., *Uncovering mesa-optimization algorithms in Transformers* (2024). arXiv:2309.05858v2
- `WhyCanGPT_ICL_2022.md` — Dai et al., *Why Can GPT Learn In-Context?* (2022). arXiv:2212.10559v3
- `Xie_BayesianInference_2022.md` — Xie et al., *In-Context Learning as Implicit Bayesian Inference* (2022). arXiv:2111.02080v6
- `Garg_ImpliticLearning_2022.md` — Garg et al., *What Can Transformers Learn In-Context?* (2022). arXiv:2208.01066v3
- `UniversalApprox_ICL_2025.md` — Li et al., *Transformers Meet In-Context Learning: Universal Approximation Theory* (2025). arXiv:2506.05200v2
- `attention_heads_survey_2024.md` — Zheng et al., *Attention Heads of LLMs: A Survey* (2024). arXiv:2409.03752v3
- `information_flow_routes_2024.md` — Ferrando & Voita, *Information Flow Routes* (2024). arXiv:2403.00824v2
- `weight_sparse_circuits_2024.md` — Gao et al., *Weight-sparse transformers have interpretable circuits* (2025). arXiv:2511.13653v1
- `moe_routing_context_2024.md` — Arnold et al., *Routing in Sparsely-gated LMs responds to Context* (2024). arXiv:2409.14107v1
- `MoE_LLMs_CloserLook_2024.md` — Lo et al., *A Closer Look into Mixture-of-Experts in LLMs* (2024). arXiv:2406.18219v3
- `Kaplan_ScalingLaws_2020.md` — Kaplan et al., *Scaling Laws for Neural Language Models* (2020). arXiv:2001.08361v1
- `Wei_EmergentAbilities_2022.md` — Wei et al., *Emergent Abilities of Large Language Models* (2022). arXiv:2206.07682v2
- `Power_Grokking_2022.md` — Power et al., *Grokking: Generalization Beyond Overfitting…* (2022). arXiv:2201.02177v1
- `ProgressMeasures_Grokking_2023.md` — Nanda et al., *Progress measures for grokking via mechanistic interpretability* (ICLR 2023). arXiv:2301.05217v3
- `Frankle_LotteryTicket_2019.md` — Frankle & Carbin, *The Lottery Ticket Hypothesis* (ICLR 2019). arXiv:1803.03635v5
- `BridgingLTH_Grokking_2023.md` — Minegishi et al., *Bridging Lottery Ticket and Grokking* (TMLR 2025). arXiv:2310.19470v3
- `FlashAttention2_2023.md` — Dao et al., *FlashAttention-2* (2023). arXiv:2307.08691v1
- `Weiss_RASP_2021.md` — Weiss et al., *Thinking Like Transformers* (ICML 2021). arXiv:2106.06981v2
- `Jelassi_RepeatAfterMe_2024.md` — Jelassi et al., *Repeat After Me: Transformers are Better than State Space Models at Copying* (ICML 2024). arXiv:2402.01032v2
- `Bordt_TransformersNeedGlasses_2024.md` — Barbero et al., *Transformers need glasses! Information over-squashing in language tasks* (NeurIPS 2024). arXiv:2406.04267v2
- `Merrill_IllusionOfState_2024.md` — Merrill et al., *The Illusion of State in State-Space Models* (ICML 2024). arXiv:2404.08819v3
- `Sarrof_SSM_ExpressiveCapacity_2024.md` — Sarrof et al., *The Expressive Capacity of State Space Models: A Formal Language Perspective* (NeurIPS 2024). arXiv:2405.17394v3
- `Feng_CoT_SerialProblems_2024.md` — Li et al., *Chain of Thought Empowers Transformers to Solve Inherently Serial Problems* (2024). arXiv:2402.12875v4
- `Li_UniversalApprox_Softmax_2025.md` — Hu et al., *Universal Approximation with Softmax Attention* (2025). arXiv:2504.15956v2
- `Valipour_VariableBinding_2025.md` — Wu et al., *How Do Transformers Learn Variable Binding in Symbolic Programs?* (2025). arXiv:2505.20896v2
- `Behrouz_Titans_2025.md` — Behrouz et al., *Titans: Learning to Memorize at Test Time* (2025). arXiv:2501.00663v1
