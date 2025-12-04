# Data Collection Plan - Option C (Hybrid)

> **Status (Dec 2025):** Data collection is complete. All resulting research artifacts live in this `research_artifacts/` folder. This document is preserved as the original plan and has been lightly updated so filenames match the actual outputs.

**Strategy:** I collect public evidence → Write complete draft → You review and add insider knowledge → We iterate

**Timeline:** 
- Days 1-2: I collect public data (this plan)
- Days 3-6: I write complete draft (4,500-5,000 words)
- Day 7: You review, add insider knowledge, we iterate

---

## PHASE 1: PUBLIC EVIDENCE I NEED (Days 1-2)
*(For the concrete papers, arXiv IDs, and links that satisfy this plan, see `refs/research_references.md`.)*

### **Dataset 1: MoE Quantitative Meta-Analysis**

**Goal:** Create honest speedup distribution (not marketing claims)

**What I'll collect:**

| Data Point | Source | Method |
|------------|--------|--------|
| **Claimed speedups** | ArXiv papers mentioning MoE | Search: "mixture of experts" + "speedup" OR "faster" |
| **Context lengths** | Same papers | Extract: which context lengths tested |
| **Expert configurations** | Same papers | Extract: N experts, K active |
| **Models** | Same papers | Mixtral, DeepSeek, Switch, Grok reports |

**Papers/Reports to Find:**
- Switch Transformers (Fedus et al., 2021) - original benchmarks
- Mixtral-8×7B technical report (2024) - production numbers
- DeepSeek-V3 technical report (Dec 2024) - latest results
- Expert Choice Routing (2022) - comparison data
- Soft MoE (2023) - benchmark claims
- Any other MoE papers 2021-2025 with speedup claims

**Search queries I'll use:**
```
"mixture of experts" speedup arxiv 2021..2025
"MoE" inference latency benchmark
Mixtral speedup benchmark evaluation
DeepSeek-V3 performance benchmarks
```

**Output I'll create:**
```markdown
| Paper/Model | Context | Experts | Active | Claimed Speedup | Notes |
|-------------|---------|---------|--------|-----------------|-------|
| Switch-XXL  | 8K      | 128     | 1      | 4×             | vs T5-XXL |
| Mixtral-8×7B| 32K     | 8       | 2      | 5× (marketing) | vs Llama-70B |
| [aggregate 30+ entries] |
```

Then calculate:
- Median speedup by context length
- Distribution (min, max, quartiles)
- Reality check vs marketing claims

---

### **Dataset 2: Adoption Timeline Tracking**

**Goal:** Track technique adoption from publication to standard practice

#### **2a. Flash Attention Timeline**

**What I'll track:**

| Milestone | Date | Source |
|-----------|------|--------|
| Original paper published | May 2022 | ArXiv |
| PyTorch integration | ? | GitHub pytorch/pytorch commits |
| JAX/Flax integration | ? | GitHub google/flax commits |
| First major model using it | ? | Model cards, papers citing Flash Attention |
| Hugging Face Transformers support | ? | GitHub releases |
| "Standard practice" (majority use) | ~2024 | Aggregate evidence |

**Search queries:**
```
site:github.com pytorch flash attention commit
"FlashAttention" model card site:huggingface.co
papers citing FlashAttention arxiv 2023 2024
```

**I'll create adoption curve:**
```
2022: 0% (paper published)
2023-Q1: ~5% (early adopters)
2023-Q3: ~20% (PyTorch integration)
2024-Q1: ~60% (major frameworks)
2024-Q3: ~90%+ (standard)
```

#### **2b. MoE Adoption Timeline**

| Milestone | Date | Source |
|-----------|------|--------|
| Switch Transformers paper | Jan 2021 | ArXiv |
| First production use (GPT-4?) | 2023? | Inference from capabilities |
| Mixtral release | Dec 2023 | Mistral announcement |
| DeepSeek-V2/V3 | 2024 | Technical reports |
| Grok-1 | 2024 | xAI announcement |
| Multiple major labs using | 2024 | Aggregate evidence |

#### **2c. SSM/Mamba Timeline**

| Milestone | Date | Source |
|-----------|------|--------|
| S4 paper | 2022 | ArXiv |
| Mamba paper | Dec 2023 | ArXiv |
| Jamba (hybrid) | 2024 | AI21 announcement |
| Qwen3-Next (hybrid) | 2025 | Qwen announcement |
| Pure Mamba at 70B+ | ? | **Check if exists** |

---

### **Dataset 3: Major Lab Adoption Audit**

**Goal:** Which labs adopted which techniques (evidence-based)

**Labs to track:** OpenAI, Google (DeepMind), Meta, Anthropic, Microsoft

**Techniques to audit:**
- Flash Attention
- MoE (any variant)
- GQA (Grouped-Query Attention)
- Pure SSMs (Mamba)
- Hybrid architectures

**Sources I'll check:**

| Source Type | What to Look For | Method |
|-------------|-----------------|--------|
| **Model cards** | Technical architecture details | Search: "GPT-4 architecture", "Gemini technical report", "Llama 3 model card" |
| **Technical papers** | Papers from lab researchers | ArXiv author affiliations |
| **Blog posts** | Official announcements | company.com/blog search |
| **GitHub repos** | Open-source implementations | Search: organization repos |
| **Job postings** | Required skills (signal of what they use) | Search: "Flash Attention" site:openai.com/careers |

**I'll create an evidence table (mirroring the final appendix):**
```markdown
| Lab | Model | First Release | Architecture (Public Info) |
|-----|-------|---------------|----------------------------|
| Meta | Llama 2 (7B/13B/70B) | 2023‑07‑18 | Dense transformer (RoPE, SwiGLU, RMSNorm; no MoE) |
| Meta | Llama 3 / 3.1 | 2024 | Dense transformer with Flash Attention + GQA |
| Meta | Llama 4 (Scout/Maverick) | 2025‑04‑05 | Mixture‑of‑experts transformer (MoE pivot) |
| OpenAI | GPT‑4 / GPT‑4 Turbo / GPT‑4o | 2023‑2024 | Multimodal transformer; internals (MoE vs dense) not fully public |
| OpenAI | GPT‑5 | 2025‑08‑07 | Multimodal frontier model; architecture details undisclosed |
| Google DeepMind | Gemini 1.0 / 1.5 | 2023‑2024 | Multimodal transformer with MQA/GQA and long‑context optimizations |
| Mistral | Mistral 7B / Mixtral 8×7B | 2023 | Dense transformer (7B) and sparse MoE transformer (Mixtral) |
| DeepSeek | DeepSeek‑V2 / V3 / R1 | 2024‑2025 | Transformer with MLA, sparse attention, and MoE at frontier scale |
| Anthropic | Claude 3 / 4.x | 2024‑2025 | Sparse / conditional transformer (not MoE) |
| xAI | Grok series | 2023‑2025 | Frontier transformer; public docs emphasize MoE‑style scaling, details evolving |
```

**Search queries:**
```
"GPT-4" architecture details
"Gemini" technical report architecture
"Llama 3" model card architecture
site:openai.com "flash attention"
site:deepmind.google "mixture of experts"
```

---

### **Dataset 4: SSM Benchmark Aggregation**

**Goal:** Where does pure Mamba evidence stop?

**What I'll find:**

| Scale | Pure Mamba | Pure Transformer | Source | Notes |
|-------|------------|------------------|--------|-------|
| 130M  | ✓ Exists   | ✓ Exists         | Original Mamba paper | Perplexity comparison |
| 370M  | ✓ Exists   | ✓ Exists         | Original Mamba paper | Perplexity comparison |
| 1.4B  | ✓ Exists   | ✓ Exists         | Original Mamba paper | Perplexity comparison |
| 3B    | ✓ Exists   | ✓ Exists         | Follow-up work | "Matches Transformer-3B" |
| 7B    | ? Search   | ✓ Exists         | ? | Check if pure Mamba-7B exists |
| 13B   | ? Search   | ✓ Exists         | ? | Check if pure Mamba-13B exists |
| 70B+  | **? CRITICAL** | ✓ Exists | **Check absence** | This is the key question |

**Search queries:**
```
Mamba 7B benchmark arxiv
"Mamba" "70B" OR "70 billion" arxiv
pure SSM large scale arxiv 2024 2025
Mamba scale benchmark evaluation
```

**Key finding I expect:** Evidence stops around 3-7B. No pure Mamba at 70B+ scale.

**This absence IS the evidence** for my claim: "Pure SSMs haven't proven at frontier scale."

---

### **Dataset 5: Production Deployment Evidence**

**Goal:** Which techniques are in actual production (not just research)?

**What I'll track:**

| Technique | Production Evidence | Companies | Source |
|-----------|---------------------|-----------|--------|
| Flash Attention | ✓ Widespread | All major labs | Model serving, papers |
| MoE | ✓ Multiple labs | DeepSeek, Mistral, xAI, likely OpenAI/Google | Technical reports |
| GQA | ✓ Multiple labs | Meta (Llama 3), Google, Mistral | Model cards |
| RAG | ✓ Universal | OpenAI (GPTs), Anthropic, Google, everyone | Product features |
| Pure Mamba | ✗ Research only | Zyphra, small labs | No major lab deployment |

**Sources:**
- Company blog posts announcing features
- Model cards stating architecture
- Technical reports
- Product documentation

---

## PHASE 2: WHAT I CAN'T GET (Insider Knowledge YOU Can Add)

### **Gap 1: Actual Production Numbers**

**What's public:** Benchmark claims on standard datasets  
**What's private:** Real production performance (latency, cost, quality)

**Examples where insider knowledge helps:**
- "Mixtral claims 5× speedup" (public) vs "In production we see 2.3× on average" (insider)
- "MoE reduces cost" (public) vs "Actual cost reduction was 40% for us" (insider)

**Your contribution:** If you have access to real production data, add it with attribution

---

### **Gap 2: Adoption Friction**

**What's public:** Dates of integration  
**What's private:** WHY it took so long

**Examples:**
- "Flash Attention took 24 months to become standard" (I can measure)
- "Because kernel development required 6 months, then framework integration another 6, then validation at scale another 12" (insider knowledge)

**Your contribution:** If you know adoption blockers from conversations, add them

---

### **Gap 3: Architecture Confirmations**

**What's public:** Inferences from capabilities/performance  
**What's private:** Actual architecture details

**Examples:**
- "GPT-4 likely uses MoE based on..." (inference)
- "GPT-4 uses MoE with X experts" (confirmed, if you have source)

**Your contribution:** Any confirmed architecture details you can share/cite

---

### **Gap 4: Future Directions**

**What's public:** Published research directions  
**What's private:** What major labs are actually investing in

**Examples:**
- "Training innovation is the next frontier" (my thesis)
- "Major labs are investing heavily in X because Y" (insider trend knowledge)

**Your contribution:** Industry trends you're seeing that aren't public yet

---

## EXECUTION PLAN

### **Days 1-2: I Collect Public Data**

**Day 1 Morning:**
- MoE meta-analysis (search ArXiv, aggregate benchmarks)
- Create speedup distribution spreadsheet

**Day 1 Afternoon:**
- Flash Attention timeline (GitHub commits, integration dates)
- MoE timeline (model releases, announcements)

**Day 2 Morning:**
- Major lab adoption audit (model cards, papers, blogs)
- Create evidence table

**Day 2 Afternoon:**
- SSM benchmark search (find where evidence stops)
- Production deployment evidence

**Output:** Data collection summary document with all findings

---

### **Days 3-6: I Write Complete Draft**

**Day 3:** Act I - The Compatibility Filter (1,800 words)
- Flash Attention with adoption curve
- Compatibility winners/failures
- SSMs with benchmark reality check

**Day 4:** Act II - The Conditional Execution Revolution (1,400 words)
- Unifying pattern
- MoE with honest speedup numbers
- Failure mechanisms

**Day 5:** Act III - Infrastructure Lag + Training (800 words)
- Adoption dynamics model
- Architecture plateaued thesis

**Day 6:** Introduction + Conclusion + Polish (600 words)
- Intro with thesis
- Conclusion synthesis
- Voice check, remove hype

**Output:** Complete 4,500-5,000 word draft

---

### **Day 7: You Review & We Iterate**

**Your review focus:**
1. **Accuracy check:** Are my inferences correct? Any errors?
2. **Insider additions:** Add production numbers, adoption friction, confirmations
3. **Strategic additions:** Future directions, trends you're seeing
4. **Voice check:** Does it match the audience/voice guidelines?

**I iterate based on your feedback**

**Output:** Final A+++ post ready to publish

---

## WHAT I NEED FROM YOU NOW

**Immediate (before I start data collection):**

1. **Any data you already have handy?**
   - MoE production performance numbers?
   - Adoption timeline details?
   - Architecture confirmations?

2. **Any specific sources I should check?**
   - Internal reports you can share?
   - Specific papers I should prioritize?

3. **Any people I should mention asking?**
   - If you have industry connections who might share data

4. **Green light to start?**
   - Should I begin Day 1 data collection now?

---

## DELIVERABLE ARTIFACTS

Actual artifacts produced from this plan (all in `research_artifacts/`):

1. **`moe_speedup_data_wip.md`** - Aggregated MoE benchmark data with an honest speedup distribution
2. **`flash_attention_timeline.md`** - Flash Attention adoption timeline and infrastructure lag evidence
3. **`major_lab_architecture_audit.md`** - Evidence table of which labs use which techniques
4. **`ssm_benchmark_findings.md`** - Where pure Mamba / SSM evidence stops by scale
5. **`EXHAUSTIVE_FINAL_COMPILATION.md`** - Synthesized data collection summary and final research compilation
6. **`EXHAUSTIVE_FINAL_COMPILATION.md` (2025 updates section)** - Additional 2025 literature updates (DeepSeek-V3/R1, Llama 4, FlashAttention-3, long-context standards, MML, etc.)

Then Days 3-6 (completed): **Complete draft of the post** in `What_Actually_Works_2023_2025.md` and the Act/Appendix drafts in `article_sections/`.

Then Day 7 (ongoing): **Your review + iteration**

---

**Ready to start? Any specific guidance before I begin Day 1?**
