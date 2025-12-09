### Batch Run: [DATE] (IDs: [LIST])
**Operator:** [NAME] | **Start Time:** [TIME] | **Status:** IN_PROGRESS

#### 1. Preparation & Manual Entry
- [ ] `source papers/.venv/bin/activate` run?
- [ ] Checked `git status` for clean state?
- [ ] **Section 1: Manual Entry**
    - [ ] **Step 1.1 (Pre-check):** Scores validated against rubric?
    - [ ] **Step 1.2 (Add Rows):** Rows added with `Analyzed=""`?
    - [ ] **Step 1.3 (Sync):** `python parse_scored_architectures.py` run?

#### 2. Execution (The Ensemble)
**Step 2.0: Automated Search**
- [ ] Run `python hf_search_model_cards.py search --ids [IDS]`
- [ ] Review candidates. (Note missing architectures in findings below).

**Step 2.1: Gather Intelligence (3 Prongs)**
*Prong A: Hugging Face Inspection*
- [ ] Run `python hf_search_model_cards.py inspect --ids [IDS]`
- [ ] Review output for explicit parameter counts.

*Prong B: ArXiv HTML (Manual Pivot)*
- [ ] (If applicable) Visit ArXiv pages for IDs with no HF models.
- [ ] Check for "Model Card" sections or links to repo.

*Prong C: PDF Deep Dive*
- [ ] Run `python fetch_and_convert_papers.py --ids [IDS]` (Downloads & converts)
- [ ] Run `python inspect_markdown_params.py --ids [IDS] --report candidates.md`
- [ ] Review `candidates.md` artifact.

#### 3. Finalization
**Step 2.2: Aggregation & Update**
- [ ] **Step 2.2 (Locations):** Deduplicate URLs? `Model_Locations` updated?
- [ ] **Step 2.2 (Params):** Deduplicate counts? `Param_Billions` updated?
- [ ] **Step 2.2 (Write):** Marked `Analyzed="analyzed"`?
- [ ] **Step 2.2 (Sync):** `python parse_scored_architectures.py` run?
- [ ] **Cleanup:** `rm candidates.md`?

**Notes / Blockers:**
- (Add freeform notes here)

---
