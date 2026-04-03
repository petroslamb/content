### Batch Run: [DATE] (IDs: [LIST])
**Operator:** [NAME] | **Start Time:** [TIME] | **Status:** IN_PROGRESS

---

#### Step 1: Add New Architectures
- [ ] `source papers/.venv/bin/activate` run?
- [ ] `git status` clean?
- [ ] **1.1** Scores validated against rubric?
- [ ] **1.2** Rows added to `scored_architectures.md` with `Analyzed=""`?
- [ ] **1.3** `python parse_scored_architectures.py` run?

#### Step 2: Discovery
- [ ] **2.1** `python hf_search_model_cards.py search --ids [IDS]` run?
- [ ] **2.2** HuggingFace papers page checked for citing models?
- [ ] Candidate URLs collected?

#### Step 3: Inspection
- [ ] **3.1** `python hf_search_model_cards.py inspect --ids [IDS]` run?
- [ ] **3.2** ArXiv HTML checked for param counts?
- [ ] **3.3** `python fetch_and_convert_papers.py --ids [IDS]` run?
- [ ] **3.3** `python inspect_markdown_params.py --ids [IDS]` run?
- [ ] Review output for parameter counts?

#### Step 4: Aggregation
- [ ] **4.1** `Model_Locations` deduplicated and updated?
- [ ] **4.2** `Param_Billions` deduplicated and updated?
- [ ] **4.3** `Analyzed = "analyzed"` set?
- [ ] **4.4** `python parse_scored_architectures.py` run (final sync)?

#### Step 5: Adoption Timeline (Optional)
- [ ] Any models ≥10B found?
- [ ] **5.2** `First_10B_Date` filled (YYYY-MM)?
- [ ] **5.2** `Adoption_Months` calculated?
- [ ] Evidence URL noted below?

---

**Findings:**
| ID | Param_Billions | Model_Locations | First_10B_Date | Notes |
|----|----------------|-----------------|----------------|-------|
| | | | | |

**Notes / Blockers:**
- (Add freeform notes here)

**Status:** COMPLETE / PARTIAL / BLOCKED

---
