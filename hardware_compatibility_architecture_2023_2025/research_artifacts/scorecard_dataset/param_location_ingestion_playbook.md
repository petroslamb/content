# Parameter & Location Ingestion Playbook

## Quick Start (TL;DR)

```bash
cd research_artifacts/scorecard_dataset/
source papers/.venv/bin/activate
```

**Checklist for adding a new architecture:**

1. [ ] Open `ingestion_journal.md`, paste `JOURNAL_TEMPLATE.md` at top
2. [ ] Validate scores (GA/MAL/PAR/STI/IM) before adding
3. [ ] Add row to `scored_architectures.md` with `Analyzed = ""`
4. [ ] Run `python parse_scored_architectures.py` to sync CSV
5. [ ] Run `python hf_search_model_cards.py search --ids <ID>` for discovery
6. [ ] Check HF papers page, model cards, ArXiv HTML for params
7. [ ] Run `python fetch_and_convert_papers.py --ids <ID>` for PDFs
8. [ ] Run `python inspect_markdown_params.py --ids <ID>` for extraction
9. [ ] Aggregate findings → update `Param_Billions`, `Model_Locations`
10. [ ] Set `Analyzed = "analyzed"` and sync CSV again
11. [ ] (Optional) Fill `First_10B_Date` and `Adoption_Months` if applicable

---

## Prerequisites

**Before you start any ingestion work:**

```bash
cd research_artifacts/scorecard_dataset/
source papers/.venv/bin/activate
```

**Source of Truth:**
- `scored_architectures.md` is canonical. All edits happen here.
- `scored_architectures.csv` is derived. Never edit directly.

**Journal Requirement:**
Every ingestion batch MUST be logged in `ingestion_journal.md`. See template:

```markdown
## Batch: [DATE] — IDs: [A1, A2, ...]
- [ ] Step 1: Scores validated
- [ ] Step 2: Rows added to markdown
- [ ] Step 3: CSV synced
- [ ] Step 4: Discovery (HF search)
- [ ] Step 5: Inspection (HF/ArXiv/PDF)
- [ ] Step 6: Aggregation complete
- [ ] Step 7: Analyzed flag set
- [ ] Step 8: Timeline filled (optional)
**Notes:** [Any issues or findings]
```

---

## Step 1: Add New Architectures

### 1.1 Validate Scores
Before adding rows, verify all proposed scores (GA, MAL, PAR, STI, IM, H, E, Zone) are consistent with the Gate-1 rubric.
- ✅ **Journal:** Mark Step 1 complete.

### 1.2 Add Rows to Markdown
- Assign a new `ID` (A*/B*/C*/D*/E* series)
- Add row with all columns. Initial state:
  - `Analyzed`: Leave empty (`""`)
  - `Param_Billions`: `[]`
  - `Model_Locations`: `[]`
  - `First_10B_Date`: empty
  - `Adoption_Months`: empty
- ✅ **Journal:** Mark Step 2 complete.

### 1.3 Sync CSV
```bash
python parse_scored_architectures.py
```
- ✅ **Journal:** Mark Step 3 complete.

---

## Step 2: Discovery (Automated Search)

### 2.1 HuggingFace Search
```bash
python hf_search_model_cards.py search --ids A5 B12
```
Collects candidate model URLs from HuggingFace.

### 2.2 HuggingFace Papers Page
For each ArXiv ID in `Source / Paper`:
- Visit `https://huggingface.co/papers/<ARXIV_ID>`
- Check "Mentions" / "Citing Models" for derived architectures
- Add relevant URLs to your pool

- ✅ **Journal:** Mark Step 4 complete.

---

## Step 3: Inspection (Parameter Extraction)

### 3.1 HuggingFace Model Cards
```bash
python hf_search_model_cards.py inspect --ids A5
```
Fetches README, extracts "7B parameters" style text.

### 3.2 ArXiv HTML
- Fetch ArXiv abstract page
- Regex search for parameter counts
- Validate title/authors match

### 3.3 PDF Deep Dive
```bash
python fetch_and_convert_papers.py --ids A5
python inspect_markdown_params.py --ids A5 --report candidates.md
```
- Downloads PDF, converts to markdown
- Extracts parameter counts with context
- Review `candidates.md` or console output

- ✅ **Journal:** Mark Step 5 complete.

---

## Step 4: Aggregation

### 4.1 Deduplicate Locations
- Collect all URLs from search + HF papers + manual
- Normalize (strip trailing slashes, lowercase hosts)
- Keep unique set

### 4.2 Deduplicate Parameters
- Convert all to float (billions)
- Remove exact duplicates
- If close but not identical (6.9B vs 7.0B), keep both for review

### 4.3 Write to Markdown
- Update `Model_Locations` with unique list
- Update `Param_Billions` with unique list
- Set `Analyzed = "analyzed"`

### 4.4 Final Sync
```bash
python parse_scored_architectures.py
```

- ✅ **Journal:** Mark Steps 6 and 7 complete.

---

## Step 5: Adoption Timeline (Optional)

If you find a model ≥10B parameters:

### 5.1 Find Deployment Date
- Check model card, blog post, or GitHub release
- Use first public release date (not paper date)

### 5.2 Fill Columns
- `First_10B_Date`: Format `YYYY-MM` (e.g., `2024-04`)
- `Adoption_Months`: Months from paper year to deployment

### 5.3 Document Evidence
Add source URL to journal notes.

- ✅ **Journal:** Mark Step 8 complete if applicable.

---

## Definition of Done

A row is complete when:
- [ ] `Analyzed = "analyzed"`
- [ ] `Param_Billions` is populated OR confirmed empty after all sources checked
- [ ] `Model_Locations` is populated OR confirmed empty
- [ ] Journal entry is complete with all checkboxes marked

Optional (for ≥10B models):
- [ ] `First_10B_Date` is filled
- [ ] `Adoption_Months` is calculated

---

## Troubleshooting

### ArXiv ID Not Found
- Check for typos in the ID (e.g., `2312.00752` not `2312.0752`)
- Some papers use different IDs (e.g., conference versions)
- Try searching by title on arxiv.org directly

### PDF Download Fails
- Check if the paper is on arXiv (some are conference-only)
- Try manual download and place in `papers/<ID>/pdf/`
- The script skips existing files, so you can retry safely

### Conflicting Parameter Counts
- Prefer HuggingFace metadata over PDF text
- If HF says "7B" and paper says "6.7B", use 7.0 (HF is usually rounded)
- If truly conflicting, keep both for human review

### Architecture is a "Technique" (No Model)
- Examples: FlashAttention, RoPE, LoRA
- These may have `Param_Billions = []` legitimately
- Set `Analyzed = "analyzed"` anyway after confirming no model exists

### Virtual Environment Issues
```bash
# If markitdown fails:
pip install markitdown[pdf]

# If tools can't find modules:
source papers/.venv/bin/activate
```

---

## What No Longer Exists

- **Manual "Seed Locations"**: HF search automation handles this
- **Waterfall Logic**: We aggregate all sources, don't stop at first hit
