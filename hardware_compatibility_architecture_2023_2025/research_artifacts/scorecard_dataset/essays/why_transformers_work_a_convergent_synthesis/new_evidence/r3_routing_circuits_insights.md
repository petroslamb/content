# Paper Insights Summary

*Extracted from 4 papers downloaded Feb 2026*

---

## Papers Reviewed

1. **Attention Heads Survey** (Tsinghua/IAAR, Dec 2024)
2. **Information Flow Routes** (Meta AI, Apr 2024)
3. **Weight-Sparse Circuits** (OpenAI, Nov 2025)
4. **MoE Routing Context** (pending review)

---

## STRENGTHENING EVIDENCE (supports existing claims)

### For R1: Content-Addressable Memory

| Paper | Finding | Quote/Data |
|-------|---------|------------|
| Attention Heads Survey | **Retrieval Heads** explicitly identified as separate functional category | "Retrieval Head can accurately locate specific tokens in long texts" (§4.3.1) |
| Weight-Sparse Circuits | String-closing circuit uses content-addressable lookup | Quote type classifier → attention key → retrieve matching token (Fig 4) |

### For R2: Implicit Optimization

| Paper | Finding | Quote/Data |
|-------|---------|------------|
| Attention Heads Survey | **Memory Heads** perform inference-time knowledge retrieval | "capable of retrieving content related to the current problem from the model's parametric knowledge" |

### For R3: Flexible Routing

| Paper | Finding | Quote/Data |
|-------|---------|------------|
| Attention Heads Survey | **30+ specialized head types** catalogued with distinct functions | Taxonomy in Fig 7: from Induction Heads to Name Movers to Truthfulness Heads |
| Information Flow Routes | Routing patterns cluster by POS tag | t-SNE shows distinct clusters for function words vs content words (Fig 8) |
| Weight-Sparse Circuits | Task-specific circuits are **16x smaller** in sparse models | "Sparse model circuits are roughly 16-fold smaller" (Fig 2) |

### For R4: Training Dynamics

| Paper | Finding | Quote/Data |
|-------|---------|------------|
| Weight-Sparse Circuits | Scaling improves capability-interpretability frontier | Larger models with same L0 improve both metrics (Fig 3) |

---

## NEW FINDINGS (potential additions to essay)

### 1. The "Attention Sink" Phenomenon
**Source:** Weight-Sparse Circuits, §3.2.2

**What it is:** Attention heads use "sink tokens" (typically BOS) as a **thresholding mechanism** for discrete decisions. The softmax acts as a threshold when comparing query activation against a large sink logit.

**Why it matters for synthesis:** Attention implements **discrete logical operations** (counting, thresholding) via continuous softmax—a computational primitive that SSMs with fixed state updates may not naturally develop.

**Potential new claim:** Attention enables implicit discrete computation within continuous optimization, which may explain why hybrids need attention for structured tasks.

---

### 2. Domain Specialization of Heads
**Source:** Information Flow Routes, §4

**What it is:** Some attention heads **only activate for specific domains** (coding, multilingual text) and remain inactive otherwise. This is emergent, not architecturally enforced.

**Why it matters for synthesis:** Attention allows **modular specialization without explicit routing gates** (unlike MoE). SSMs with fixed state dynamics may not develop this naturally.

**Potential new claim:** Attention supports emergent domain specialization as a side-effect of content-dependency (R3), which is a capability not captured by the current 4 requirements.

---

### 3. The 4-Stage Cognitive Framework
**Source:** Attention Heads Survey, §4.1

**What it is:** Authors map attention head functions to human cognitive stages:
- **Knowledge Recalling** (Memory Heads, Retrieval Heads)
- **In-Context Identification** (Induction Heads, Name Movers, Syntactic Heads)
- **Latent Reasoning** (Truthfulness Heads, Accuracy Heads)
- **Expression Preparation** (Amplification Heads)

**Why it matters for synthesis:** This maps almost 1:1 to the essay's 4 requirements:
- R1 (Memory) ↔ Knowledge Recalling
- R2 (Implicit Opt) ↔ Latent Reasoning
- R3 (Routing) ↔ In-Context Identification
- R4 (Training) ↔ Enables all stages

**Potential new claim:** The 4-requirement framework has independent support from cognitive neuroscience analogies (Table 1 in paper cites 8 papers on LLM-brain parallels).

---

### 4. Bridges Show Dense/Sparse Circuit Equivalence
**Source:** Weight-Sparse Circuits, §3.3

**What it is:** OpenAI trained sparse "interpretable twins" coupled to dense models. Key finding: **adversarial attacks discovered on sparse circuits transfer to dense models.**

**Why it matters for synthesis:** Same underlying mechanisms exist in both. This validates that mechanistic circuit analysis is not an artifact of sparsity.

**Potential new test:** If SSMs had the same circuits as Transformers, attacks should transfer. If they don't, it's evidence of fundamentally different computation (supporting R1 as discriminator).

---

### 5. Previous Token + Subword Merging Heads Are Universal
**Source:** Information Flow Routes, §4.3

**What it is:** Two head functions are "always important" across all predictions:
- Previous token heads (positional)
- Subword merging heads (combining BPE pieces)

**Why it matters for synthesis:** These are **universally important** across domains—they're infrastructure, not task-specific. SSMs handle previous token naturally, but subword merging may require explicit state design.

---

## RECOMMENDED ADDITIONS TO v3.0

### High Priority (strong evidence)
1. **Add to R3 section:** 30+ specialized head types confirm routing diversity
2. **Add to §7:** Attention sink as discrete computation primitive

### Medium Priority (novel but speculative)
3. **New subsection:** Domain specialization as emergent capability
4. **Connect to cognitive science:** 4-requirement ↔ 4-stage cognitive mapping

### Low Priority (for future work)
5. Circuit transfer attacks as SSM diagnostic
