# Remaining Data Collection - Execution Plan

**Current Status:** 3/7 datasets complete (MoE, Flash Attention, SSMs)  
**Confidence:** 0.90/1.0 (already A+++ territory)  
**Goal:** Get to 0.95/1.0 with comprehensive evidence

---

## Datasets Still Needed

### Dataset 4: Major Lab Architecture Audit (PRIORITY: HIGH)
**Goal:** Which labs use which techniques - create evidence table

**What to find:**
- **GQA adoption:** Meta (Llama 3), Google, Mistral - confirm with sources
- **MLA adoption:** DeepSeek-V3 confirmed, any others?
- **RoPE usage:** Which models use it? (Llama, others?)
- **RMSNorm vs LayerNorm:** Who switched and when?

**Search queries:**
```
"Llama 3" "grouped query attention" model card
"Gemini" architecture "multi-query attention" OR "grouped query"
Mistral 7B architecture GQA MQA
"RoPE" "rotary position" Llama GPT-4 adoption
RMSNorm vs LayerNorm 2024 models
```

**Deliverable:** Evidence table:
| Technique | OpenAI | Google | Meta | Anthropic | DeepSeek | Mistral | Evidence Links |

---

### Dataset 5: Production MoE Confirmations (PRIORITY: HIGH)
**Goal:** Which models ACTUALLY use MoE (confirmed vs inferred)

**What to find:**
- **Confirmed MoE models:** DeepSeek-V3, Mixtral, Grok-1, Deepseek-V2
- **Likely but unconfirmed:** GPT-4, Gemini (find architectural analysis)
- **Explicitly NOT MoE:** Claude (confirmed dense?), Llama 3 (confirmed dense)

**Search queries:**
```
"GPT-4" architecture analysis MoE evidence
"Gemini" mixture of experts architecture
"Claude 3" architecture dense OR MoE
"Llama 3" architecture dense transformer
DeepSeek-V2 MoE architecture details
```

**Deliverable:** Confirmed MoE models table with evidence strength

---

### Dataset 6: Attention Variant Adoption (PRIORITY: MEDIUM)
**Goal:** Quantify which attention variants are actually used in 2024 models

**What to find:**
- **GQA usage:** How many 2024 models use it?
- **MQA usage:** Older technique, who still uses?
- **Standard MHA:** How many still use vanilla multi-head?
- **Sparse attention:** Production deployments (DeepSeek, others)

**Search queries:**
```
"grouped query attention" 2024 models list
"multi-query attention" adoption 2024
models using GQA 2024 site:huggingface.co
DeepSeek sparse attention DSA production
```

**Deliverable:** Attention variant distribution among 2024 models

---

### Dataset 7: 2025 Architecture Trends (PRIORITY: LOW)
**Goal:** Catch any late-breaking papers or trends we missed

**What to find:**
- Any major 2025 architecture papers (post-December timeframe)
- New attention mechanisms gaining traction
- Production deployments announced recently

**Search queries:**
```
arxiv neural architecture 2025 survey
"attention mechanism" 2025 arxiv innovation
foundation model architecture 2025 trends
```

**Deliverable:** Any critical additions to the narrative

---

## Execution Order

**Phase 1: High Priority (Next 1 hour)**
1. Dataset 4: Major Lab Audit - 6 searches
2. Dataset 5: MoE Confirmations - 5 searches

**Phase 2: Medium Priority (30 min)**
3. Dataset 6: Attention Variants - 4 searches

**Phase 3: Low Priority (30 min, if needed)**
4. Dataset 7: 2025 Trends - 3 searches

**Total estimated time:** 2-3 hours of focused searching

---

## Expected Outcomes

**After completion:**
- Evidence table for all major lab architectures
- Confirmed vs inferred MoE models distinction
- Quantitative data on attention variant adoption
- Complete picture of 2024-2025 production landscape

**Confidence increase:**
- Current: 0.90/1.0
- After: 0.95/1.0 (near-perfect for literature-based research)

**What this enables:**
- Specific citations for every claim in Act I
- "X out of Y models use Z" quantitative statements
- Clear distinction between confirmed and inferred architectures
- Strengthened major lab audit

---

## Starting Now

Beginning with Dataset 4: Major Lab Architecture Audit
First search: Llama 3 GQA confirmation
