# From-Scratch, Non-Forcing Hypothesis (v0)

**Status:** Draft  
**Date:** Feb 6, 2026  
**Goal:** Replace category-first framing with a minimal equation-first hypothesis that can be falsified, merged, or deleted as evidence arrives.

---

## 1) Anti-Forcing Rules

We commit to the following rules before adding new evidence:

1. Start from transformer operations, not paper taxonomies.
2. Define the smallest set of primitives needed to explain behavior.
3. Pre-register rival hypotheses that could also explain the same evidence.
4. Every primitive must have a unique causal signature and a kill criterion.
5. If two primitives cannot be causally separated, merge them.
6. If a primitive only survives by broad wording, delete it.

---

## 2) Minimal Equation-First Hypothesis

At layer `l`, token state update is:

`x_i^{l+1} = x_i^l + F_l( x_i^l, Σ_j A_{ij}^l V_l x_j^l )`

with

`A^l = softmax(Q_l X_l · (K_l X_l)^T + mask + pos)`

and normalization/stability operators applied per architecture.

From this, propose a minimal capability hypothesis `H*`:

> Transformer capability is the iterative composition of **selective cross-token transport** and **local nonlinear rewrite** on a persistent token workspace, under a stable optimization regime.

No `R` labels are assumed here.

---

## 3) Primitive Set (S1–S5)

### S1. Identity Persistence (anti-collapse substrate)
Token identity and distinguishability must persist across depth (residual path + normalization/stability choices).

**Kill criterion:** Deep stacks without an equivalent anti-collapse mechanism match capability package with no selective degradation in long-context or strict-format tasks.

### S2. Selective Transport
The model must perform high-contrast, input-dependent transfer across token positions (not uniform mixing).

**Kill criterion:** Architectures with only smooth/global mixing match extraction and format-sensitive retrieval without introducing an attention-like sharp selector elsewhere.

### S3. Local Nonlinear Rewrite
After transport, each token undergoes high-capacity local rewrite (feature construction, rule application, parametric lookup/use).

**Kill criterion:** Architectures with minimal local rewrite (mostly mixing) match rule-application and brittle formatting behaviors under matched scale.

### S4. Iterative Composition (depth/time as compute budget)
Complex behavior emerges by repeated composition across layers and autoregressive steps; one-step operators become algorithm-like via iteration.

**Kill criterion:** Same tasks are solved equally well when depth/time is strongly constrained, without equivalent alternative compute path.

### S5. Discoverability Under Training
Optimization reliably discovers sparse/useful configurations of S1–S4 at scale.

**Kill criterion:** Competing families match capability while showing no analogous discovered bottlenecks or phase-structured emergence.

---

## 4) Rival Hypotheses (pre-registered)

### RH-A: Retrieval-Dominant
S2 explains most observed gains; S3 is secondary.

**Prediction:** Strong retrieval interventions cause large drops; local-rewrite interventions mostly track generic degradation.

### RH-B: Rewrite-Dominant
S3 is primary; S2 can be relatively weak if local compute is strong.

**Prediction:** Local rewrite interventions selectively break reasoning/formatting while retrieval remains mostly intact.

### RH-C: Update-Rule Dominant
Inference-time gains come mainly from implicit memory-update dynamics, not selective transport sharpness.

**Prediction:** Models with weaker selectors but stronger update rules close most gaps on ICL/reasoning.

### RH-D: Optimization-Only Story
Architecture details are secondary; training regime alone explains outcomes.

**Prediction:** Multiple divergent architectures converge to same capability profile under similar optimization/data.

---

## 5) Evidence Ingestion Template (required for every new paper)

For each paper, fill these fields:

1. **Claim tested:** Which `S` (or rival) does this directly test?
2. **Predicted by `H*`?** yes/no/partial.
3. **Predicted by rivals?** list.
4. **Causal strength:** descriptive / correlational / intervention / replacement.
5. **Update sign:** `+`, `-`, or `0` for each `S` and each rival.
6. **Merge/Delete trigger:** does this force primitive merge or deletion?

A paper that cannot be mapped to at least one registered prediction does not count as support.

---

## 6) Decision Policy (to avoid category forcing)

After each evidence batch:

1. If a primitive has no unique intervention signature after 2 batches, merge it.
2. If a primitive survives only by wording expansion, delete it.
3. If a rival explains equal evidence with fewer assumptions, prefer rival.
4. Keep only the minimal surviving primitive set.

---

## 7) Mapping Back to Current `R` Framework (optional, not assumed)

Current best mapping if we still want `R` labels for communication:

- `S1 + part of S3` -> `R0`
- `S2` -> `R1`
- `part of S4` + task-state effects -> `R2`
- optional routing special case of `S2/S3` interactions -> `R3` (extended only)
- `S5` -> `R4`

If this mapping causes overlap that cannot be causally separated, the `R` split should be revised, not defended.

