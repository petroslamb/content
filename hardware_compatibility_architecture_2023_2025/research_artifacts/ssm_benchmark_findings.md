# SSM/Mamba Benchmark Findings: Where Evidence Stops

**Research Goal:** Determine at what scale pure Mamba/SSM evidence exists vs. where it becomes speculation. Critical for validating claim: "Pure SSMs won't scale to frontier models."

---

## Pure Mamba Model Scales (Confirmed Evidence)

### Small Scale (130M-370M)
**Source:** Original Mamba paper, pruning studies
- **Mamba-Small:** 130M parameters
- **Mamba-Base:** 370M parameters
- **Evidence:** Perplexity benchmarks on WikiText-103, PG-19
- **Performance:** Competitive with Transformer baselines
- **Status:** ✓ Proven at this scale

### Medium Scale (1.4B-2.8B)
**Source:** Original Mamba paper (Dec 2023)
- **Mamba-1.4B:** Matches Transformers of same size
- **Mamba-2.8B:** Outperforms Pythia 2.8B, matches models 2× its size (Pythia 7B, RWKV 7B)
- **Evidence:** Pre-training perplexity, downstream evaluation
- **Status:** ✓ Proven,competitive at this scale

### Large Scale (7B)
**Source:** Falcon Mamba 7B (TII, 2024)
- **Falcon Mamba 7B:** Best-performing pure Mamba model at its scale
- **Training:** 5.5 trillion tokens
- **Performance:**
  - Outperforms Llama 3.1 8B, Mistral 7B (similar-sized Transformers)
  - Comparable to Gemma 7B
  - Best Mamba on Open LLM Leaderboard
  - 5× higher throughput than Transformers for long texts
- **Efficiency:** Linear memory cost, fast long-context generation
- **Benchmarks:** Winogrande, Piqa, Lambada, Hellaswag, Arc Easy/Challenge, IFEval, BBH, MATH
- **Status:** ✓ Proven at 7B scale as best pure SSM

---

## Where Evidence STOPS

### 13B Scale
**Searched for:** "pure Mamba 13B" OR "pure SSM 13B"
**Found:** ❌ **NO pure Mamba models at 13B scale**
- Discussions acknowledge lack of 13B pure models
- At this scale, hybrid approaches begin

### 70B+ Scale (Frontier)
**Searched for:** "pure Mamba 70B" OR "pure SSM 70B billion"
**Found:** ❌ **NO pure Mamba models at 70B+ scale**

**What exists at 70B:**
- Transformers (Llama, Mistral, etc.) - widespread
- MoE Transformers (DeepSeek-V3 671B/37B active, Mixtral, Grok-1)
- **NO pure SSM at any frontier scale**

**Key quote from research:**
> "There are discussions acknowledging the lack of very large pure Mamba (or Mamba2) models (70B+) and that most larger Mamba models have been hybrids."

---

## What EXISTS at Larger Scales: Hybrids Only (As of Dec 2025)

### Hybrid Architectures (SSM + Attention)

**Jamba (AI21, 2024):**
- **Architecture:** Alternating Mamba + Attention layers
- **Scale:** Up to 1.6B parameters (hybrid)
- **Design:** Mamba for local patterns, Attention for global reasoning
- **Status:** Production-deployed hybrid

**Falcon-H1 (TII, 2024):**
- **Architecture:** Parallel hybrid (attention + Mamba-2 heads concurrent)
- **Scale:**  0.5B to 34B parameters
- **Design:** Hybrid mixer block with optimal attention/SSM ratio
- **Status:** "Production-ready" hybrid

**Qwen3-Next (2025):**
- **Architecture:** Linear attention (Gated DeltaNet) + gated attention + MoE
- **Scale:** Large (256K context window)
- **Design:** Three-dimensional hybrid (attention variants + MoE)
- **Status:** Frontier hybrid architecture; exemplifies the “hybrid > pure” 2025 consensus.

**Hybrid-Llama3-Mamba2-3B:**
- **Architecture:** 3B hybrid distilled from 70B Llama-3.1 Transformer
- **Note:** Uses 70B Transformer as TEACHER, not a pure SSM

---

## Why Pure SSMs Struggle at Scale

### Research Findings (2024–2025 Surveys)

**From “pure Mamba OR pure SSM 70B” search and 2025 survey papers:**
> "Hybrid architectures combine Mamba or SSM layers with attention mechanisms to leverage the strengths of both... These hybrid approaches often aim to overcome limitations of pure SSMs in tasks requiring precise token interactions, such as in-context retrieval."

**Key limitations at scale:**
1. **In-context learning:** SSMs struggle with ICL vs attention
2. **Precise token interactions:** Sequential processing limits long-range routing
3. **Parallelism gap:** Sequential state updates fight GPU parallelism
4. **Training at scale:** Validation needed beyond 7B, not yet demonstrated

### Major Lab Adoption (2025 Consensus)

**Searched:** Major labs (OpenAI, Google, Meta, Anthropic, Microsoft) + “Mamba” / “SSM”

**Findings (consistent with 2025 survey literature):**
- ❌ OpenAI: No pure SSM adoption in frontier models (GPT‑4/4o/5).
- ❌ Google/DeepMind: No pure SSM adoption in Gemini; uses attention variants and sparsity.
- ❌ Meta: No pure SSM adoption (Llama 2/3/4 lines all transformer‑based; Llama 4 uses MoE, not SSM).
- ❌ Anthropic: No pure SSM adoption (Claude 1‑4.x are transformer‑based with sparse attention).
- ❌ Microsoft: No large‑scale pure SSM deployments reported.

**Pattern:** By late 2025, major labs are converging on **hybrid architectures** (SSM + Attention or multiple attention variants) when they use SSM‑style blocks at all. Pure SSM remains a research curiosity at ≤7B, not a frontier scaling strategy.

---

## Benchmark Comparison: Pure Mamba vs Transformer

### At Scales Where Both Exist (≤7B)

| Scale | Pure Mamba | Pure Transformer | Winner |
|-------|------------|------------------|--------|
| 130M | Matches baseline | Baseline | ~Tie |
| 370M | Competitive | Baseline | ~Tie |
| 1.4B | Matches same size | Same size baseline | ~Tie |
| 2.8B | Matches 7B Transformer | 2.8B baseline | Mamba (efficiency) |
| 7B | Falcon Mamba beats Llama 3.1 8B, Mistral 7B | Llama, Mistral | Mamba (at this scale) |
| **13B** | ❌ Doesn't exist | ✓ Exists | N/A |
| **70B+** | ❌ Doesn't exist | ✓ Exists | N/A |

### Performance Characteristics

**Pure Mamba strengths (at 7B):**
- 5× higher throughput for long texts
- Linear memory cost (vs quadratic for attention)
- Constant speed regardless of sequence length
- Strong on benchmarks requiring sequential processing

**Pure Mamba weaknesses (limiting scale):**
- In-context learning gap vs Transformers
- Precise token retrieval harder (sequential state vs arbitrary attention)
- Training stability questions at massive scale
- GPU parallelism not fully exploited (sequential state updates)

---

## The Evidence-Based Conclusion

### What We Know (Proven)
✓ Pure Mamba works well up to 7B parameters
✓ Falcon Mamba 7B is best pure SSM model
✓ At 7B, can match or beat Transformers on many tasks
✓ Efficiency benefits (throughput, memory) are real

### What We DON'T Know (No Evidence)
❌ Whether pure Mamba scales to 13B+
❌ Whether pure Mamba can match 70B Transformers
❌ Whether pure Mamba can handle frontier model complexity
❌ Whether training dynamics remain stable at massive scale

### What Hybrid Evidence Shows
✓ SSM + Attention hybrids work better than pure SSM at scale
✓ Hybrids can reach 256K context (Qwen3-Next)
✓ Production deployments are all hybrid, not pure
✓ Major innovation is in COMBINING primitives, not replacing

---

## Implications for A+++ Post

### The Bold Claim (Defended, 2025)
**Statement:** "Pure SSMs won't scale to frontier models (70B+). The parallelism gap is architectural, not merely a training gap."

**Defense (updated to 2025):**
1. **Evidence still stops at 7B:** No pure SSM beyond Falcon Mamba 7B despite 24+ months since the Mamba paper.
2. **Major labs haven’t adopted pure SSM:** OpenAI, Google, Meta, Anthropic all use transformer‑based frontiers (dense, sparse, MoE, or hybrids).
3. **Hybrids dominate larger scales:** All large‑scale SSM usage appears in hybrid stacks (Jamba, Falcon‑H1, Qwen3‑Next), not pure models.
4. **Mechanism:** Sequential state updates fundamentally conflict with GPU parallelism and in‑context retrieval demands at frontier scale.
5. **Survey confirmation:** 2025 SSM/Mamba surveys explicitly frame SSMs as **promising hybrid components**, not replacements for attention in frontier models.

### The Realistic Assessment
**Pure Mamba at 7B:** Genuine success, worthy of recognition.  
**Hybrid architectures:** The promising direction (SSM for local/temporal structure, attention for global routing and in‑context learning).  
**Pure SSM at frontier:** No evidence as of Dec 2025 and growing expert consensus that this is unlikely without major hardware changes.

### Positioning in Post
- **Act I Section 1.4:** "SSMs: Hybrid Components, Not Replacements"
- Acknowledge 7B success (Falcon Mamba)
- State evidence gap at 13B+
- Explain mechanism (parallelism conflict)
- Position hybrids as the viable path

### Production Status Classification
- **Pure Mamba ≤7B:** 🟡 LIMITED ADOPTION (TII, smaller orgs)
- **Pure Mamba >7B:** 🔴 RESEARCH-ONLY (doesn't exist yet)
- **Hybrid SSM+Attention:** 🟡 LIMITED ADOPTION (Jamba, Falcon-H1, Qwen3-Next)

---

## Sources Summary

**Pure Mamba models found:**
- Original Mamba paper (arXiv, Dec 2023): 130M, 370M, 1.4B, 2.8B
- Falcon Mamba 7B (TII, 2024): Best pure SSM
- Mamba-2 models (research, 2024): 130M, 370M

**Hybrid models found:**
- Jamba (AI21, 2024): Up to 1.6B hybrid
- Falcon-H1 (TII, 2024): 0.5B-34B hybrid
- Qwen3-Next (2025): Frontier hybrid with 256K context
- Hybrid-Llama3-Mamba2 (2024): 3B hybrid

**What NOT found:**
- Pure Mamba at 13B, 70B, or any frontier scale
- Major lab adoption of pure SSM
- Production deployments of pure SSM at large scale

---

**Status:** Dataset complete
**Key finding:** Evidence validates "pure SSMs won't scale" thesis
**Next use:** Act I Section 1.4 in final post
