# R0 (Architecture Preconditions) — Evidence Synthesis

**Status:** Processed  
**Date:** Feb 6, 2026  
**Purpose:** Add load-bearing evidence about *preconditions* (what must be true of the architecture + stack for the rest of the R-bundle to even make sense).

## Papers Analyzed

1. **Dong et al. (2021)** — *Pure attention degenerates (rank collapse); skip + MLP counteract.*  
   - Local: [`Dong_AttentionNotAllYouNeed_2021`](../papers/Dong_AttentionNotAllYouNeed_2021.md)
2. **Edelman et al. (2021)** — *Self-attention creates sparse variables; sample complexity ~ log(context length).*  
   - Local: [`Edelman_VariableCreation_Attention_2021`](../papers/Edelman_VariableCreation_Attention_2021.md)
3. **Weiss et al. (2021)** — *RASP: a programming model for Transformer computation (attention + FFN primitives).*  
   - Local: [`Weiss_RASP_2021`](../papers/Weiss_RASP_2021.md)
4. **Zhong et al. (2025)** — *Associative memory lens: exp-kernel (attention) vs ReLU-kernel (FFN); retrieval SNR; memory update dynamics.*  
   - Local: [`Zhong_AssociativeMemory_2025`](../papers/Zhong_AssociativeMemory_2025.md)
5. **Sun et al. (2024)** — *“Layers as painters”: middle-layer representation shared enough to skip/reorder/parallelize; weight-sharing is catastrophic.*  
   - Local: [`Sun_TransformerLayersAsPainters_2024`](../papers/Sun_TransformerLayersAsPainters_2024.md)
6. **Turner (2023)** — *Clean mathematical description; why residual connections + LayerNorm are used for stability.*  
   - Local: [`Turner_AnIntroductionToTransformers_2023`](../papers/Turner_AnIntroductionToTransformers_2023.md)

---

## Executive Synthesis (what this bundle forces)

1. **“Attention alone” is not a viable substrate at depth.** Pure multi-head self-attention has an intrinsic bias toward *token uniformity* / *rank-1 collapse* as depth grows; this is prevented primarily by **skip connections** (residual highway) and secondarily by **MLPs** (nonlinearity + local rewrite capacity). (Dong)
2. **Self-attention has a *specific* inductive bias (not “no bias”):** bounded-norm attention heads preferentially implement **sparse variable creation**, enabling long-range sparse dependencies with sample complexity scaling only **logarithmically** in context length. (Edelman)
3. **Attention and FFNs can be unified as associative memories with different kernels:** softmax attention’s **exponential kernel** yields far sharper retrieval than linear kernels; FFNs can be interpreted as a **ReLU-kernel** associative memory (more compressive / polysemantic but noisier retrieval). (Zhong)
4. **Residual highways appear to create a “common language” across middle layers:** many middle layers are robust to being skipped, reordered, or partially parallelized (graceful degradation), but **are not redundant** (weight sharing is catastrophic). (Sun)
5. **LayerNorm is mostly a stability scaffold (magnitude/gradient control), not the mechanism that prevents attention’s degeneracy.** In particular, Dong’s rank-collapse analysis treats LN as non-essential for preventing rank collapse, while Turner motivates LN as stabilizing activations during deep composition. (Dong, Turner)

**Net effect for Convergent Synthesis:** R0 should explicitly include **(i) a persistent workspace (residual stream), (ii) a tokenwise nonlinear rewrite operator (MLP/FFN), and (iii) normalization/stability scaffolding** as *preconditions* for R1/R2-style sparse bottlenecks to exist and remain usable at depth.

---

## 1) Pure Attention Degeneracy: Rank Collapse and Token Uniformity (Dong 2021)

### What they prove (simplified)

- In a **Self-Attention Network (SAN)** made only of stacked multi-head self-attention (no skip connections, no MLP), the output **converges doubly exponentially** with depth to a **rank-1 matrix with identical rows** (tokens become indistinguishable).  
- They analyze SANs via a **path decomposition**: the multi-head network can be decomposed into a sum over many single-head “paths” across depth; each path collapses quickly, and the ensemble collapses too.

### What stops the collapse (and how)

- **Skip connections are crucial:** enabling paths that *skip* layers creates short paths, including a length-0 path that preserves the input residual. They provide a simple lower-bound claim showing the residual can be preserved under some parametrizations, even as depth grows.  
- **MLPs help:** adding per-layer MLPs (nonlinear tokenwise maps) slows collapse; their bounds show the convergence rate depends on the MLP Lipschitz constants (more powerful MLPs counteract collapse more).
- **LayerNorm “plays no role” for rank collapse (in their analysis):** LN does not address the core rank-collapse mechanism in the same way skip/MLP do.

### Why this matters for our note (R0 preconditions)

- **Residual stream = persistent workspace** isn’t just “for gradients”; it is a direct structural route around attention’s degeneration.
- **Tokenwise MLP rewrite** isn’t just “extra capacity”; it is part of the anti-degeneracy mechanism and provides local compute needed by the executor view of R0.
- **Architectural implication:** any “Transformer replacement” that removes/weakens residual+MLP needs *another* explicit anti-degeneracy mechanism, or it risks token-uniformity failure modes at depth.

---

## 2) Sparse Variable Creation: A Theoretical Inductive Bias for “Variable Binding” (Edelman 2021)

### Core claim

Edelman et al. formalize an inductive bias they call **sparse variable creation**:

- A bounded-norm self-attention head can represent **sparse functions** of the input sequence (depends on only `s ≪ T` coordinates) with **sample complexity scaling as `O(s log T)`** (logarithmic in context length `T`).
- They also provide representational constructions: Transformer heads (optionally composed with a small MLP) can exactly represent broad families of `s`-sparse Boolean functions with bounded norms (under natural input mappings).

### Why this matters for our note (R1/R2 interface + “preconditions”)

This gives a rigorous backing to a “variable creation / binding” story:

- Attention is naturally suited to **select a small subset of positions** (variables) from a long context and pass them forward for downstream compute.
- Combined with a tokenwise MLP, this becomes a canonical pattern: **(select variables) → (compute with them)**.

Also note the subtlety: “Transformers have weak inductive biases” is at best incomplete. These results describe *specific* statistical preferences (sparse selection) that become powerful in the large-data regime.

---

## 3) Associative Memory Unification: Why Softmax is Sharp and FFNs are Compressive (Zhong 2025)

### Retrieval capacity via SNR (their framing)

They define a retrieval Signal-to-Noise Ratio (SNR) for associative memories and analyze how capacity scales under different kernels:

- **Linear kernel (linear attention / outer-product memory):** inverse SNR scales roughly as `N / d_k`, implying reliable recall typically needs `d_k ≳ N` for `N` stored items.
- **Exponential kernel (softmax attention):** inverse SNR scales much more favorably; they argue the effective dimensionality requirements drop dramatically (their headline: from `O(N)` in the linear case to `O(log^2 N)` under an exponential kernel with standard temperature scaling).

### FFN as associative memory (ReLU kernel)

They show a standard 2-layer FFN with ReLU can be rewritten as an associative memory with **ReLU kernel** `κ(x, y) = ReLU(xᵀy)`:

- ReLU improves recall vs linear by zeroing negative similarities, but is still much noisier than exponential-kernel attention.
- They propose a qualitative explanation: **FFNs benefit from polysemantic superposition** (compressed, long-term storage), whereas attention benefits from **monosemantic precision** for in-context retrieval.

### Why this matters for our note

This supports the *division of labor* implicit in the R-bundle:

- **R1 (sharp contextual readout):** softmax attention as a sharp kernelized retrieval mechanism.
- **R0 (parametric substrate / executor):** FFNs as a compressive associative memory + tokenwise compute substrate.

---

## 4) Middle-Layer “Common Language”: Reordering/Skipping Works (but Weight Sharing Doesn’t) (Sun 2024)

### Key observations (frozen models)

- Middle layers of large pretrained Transformers appear to share a representation space enough that performance can degrade **gracefully** when:
  - skipping some middle layers,
  - switching the order of neighboring layers,
  - running middle layers in parallel and averaging outputs.
- But **replacing many middle-layer weights with a single layer’s weights (weight sharing / repeated middle layer)** is **catastrophic** — suggesting middle layers are not redundant even if their representations are “compatible.”

### Why this matters for R0 preconditions

This is strongly suggestive of the residual-stream view of R0:

- Residual connections encourage layers to implement **incremental updates** in a shared coordinate system (“speak the same language”).
- Yet the catastrophic failure under weight-sharing is a warning: “shared representation space” ≠ “same function.” Middle layers can be *compatible but specialized*.

---

## 5) Training Stability Scaffolding: Residuals + LayerNorm (Turner 2023)

Turner’s note doesn’t aim to be new mechanistic evidence, but it cleanly states why modern Transformer stacks are built the way they are:

- **Residual connections:** stabilize learning and encourage mild per-layer updates around an identity map.
- **LayerNorm / token normalization:** stabilizes magnitude as nonlinearities compose through depth and is empirically more stable than alternatives like BatchNorm for Transformers.

This supports treating residual+norm as part of the **regime assumptions** for the rest of the evidence bundle.

---

## Implications / How this should update the main working note (for later discussion)

1. **Promote “residual + MLP” from implementation detail to R0 precondition.** Dong makes it hard to claim that “attention is the main thing” in any mechanistic sense that ignores degeneracy without these components.
2. **Strengthen the R0 → (R1, R2) story as a canonical 2-step pipeline:** sparse variable selection (attention) plus tokenwise compute (MLP) is a clean mechanistic template consistent with Edelman (variable creation) and Zhong (kernelized memory division).
3. **Clarify what we mean by “weak inductive bias.”** Attention is flexible, but it still has identifiable inductive biases (uniformity pressure; sparse-variable creation) that matter for scaling and for failure modes.
4. **Add a stability footnote to R4:** LayerNorm and residuals are plausibly required to *reach* the sparse circuit regime, even if they are not the mechanism of the circuits once learned.

