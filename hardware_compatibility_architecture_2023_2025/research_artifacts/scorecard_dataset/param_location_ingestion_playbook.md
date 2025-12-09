# Parameter & Location Ingestion Playbook

## 0. Prerequisites

### 0.0 Source of Truth
- The canonical dataset is `scored_architectures.md`.  
- `scored_architectures.csv` is a **derived artifact**: `parse_scored_architectures.py` regenerates the CSV from the markdown tables and **overwrites all rows/columns**. Any edits must be made in the markdown; the CSV is read‑only from a human perspective.

### 0.1 Protocol: The Journal
**CRITICAL:** You must log your run.
1.  Open `research_artifacts/scorecard_dataset/ingestion_journal.md`.
2.  Paste the content of `JOURNAL_TEMPLATE.md` at the top.
3.  Fill in the Date and IDs.
4.  **As you proceed:** Check off the boxes. Do not skip this.

## 1. Adding New Architectures (Manual Entry Only)

When ingesting a new batch (e.g., from `techniques_for_scoring.md` or manual research):

### 1.1 Pre‑check: validate scores
- Before adding *any* rows to markdown or CSV, go through the new batch and verify that all proposed scores exist and make sense (GA, MAL, PAR, STI, IM, H, E, Zone).  
- If any score looks inconsistent with the Gate‑1 rubric or prior rows, **stop the process here**.
- ✅ **Journal Check:** Mark *Step 1.1* as complete.

### 1.2 Add rows to `scored_architectures.md`
- Assign a new `ID` (A*/B*/C*/D*/E* series).  
- In the relevant scorecard table, add a row with columns including at least:  
  - `ID`, `Architecture`, `Year`, `Era`, `GA`, `MAL`, `PAR`, `STI`, `IM`, `H`, `E`, `Zone`, `Source / Paper`, `Notes`, `Section`, `Analyzed`, `Param_Billions`, `Model_Locations`.  
- **Crucial Initial State:**
  - `Section`: Set to the appropriate section label.
  - `Analyzed`: **Leave Empty** (`""`).
  - `Param_Billions`: `[]`.
  - `Model_Locations`: `[]`.
- **Do not** try to find URLs or parameters manually at this stage unless you already have them handy. The automated pipeline (Step 2) is designed to find them for you.
- ✅ **Journal Check:** Mark *Step 1.2* as complete.

### 1.3 Regenerate the CSV (derived only)
- **Ensure you are in the environment:**
  ```bash
  # From research_artifacts/scorecard_dataset/
  source papers/.venv/bin/activate
  ```
- Run: `python parse_scored_architectures.py`
- This ensures the new rows exist in the derived CSV for the Python tools to read.
- ✅ **Journal Check:** Mark *Step 1.3* as complete.

---

## 2. Parameter & Location Discovery (The Ensemble)

**Goal:** Run an "Ensemble" of discovery methods on all rows where `Analyzed = ""`.
**Logic:** Unlike previous "waterfall" approaches, we run **ALL** applicable prongs (Search, HF, ArXiv, PDF) and then **aggregate** the findings.

### 2.0 Step 0 — Automated Discovery (Search)
- **Tool:** `hf_search_model_cards.py` in `search` mode.
- **Action:**
  1.  Run the search helper:
      ```bash
      python hf_search_model_cards.py search
      # Or for specific IDs:
      python hf_search_model_cards.py search --ids A5 B12
      ```
  2.  The script will print candidate URLs to your terminal.
  3.  **Collect** these URLs. You will use them to update the markdown in Step 2.2, but for now just pass them to Step 2.1.
  4.  ✅ **Journal Check:** Mark *Step 2.0* as complete in your journal. Note any missing architectures.

### 2.1 Step 1 — Gather Intelligence (The 3 Prongs)
Run these three prongs to harvest data. Findings are accumulative.

#### Prong A: Hugging Face Model Cards (High Confidence)
- **Tool:** `hf_search_model_cards.py` in `inspect` mode.
- **Action:**
    -  Run inspection on IDs that already have locations or were found in Step 2.0:
       ```bash
       python hf_search_model_cards.py inspect --ids A5
       ```
    -  The script fetches the README, looks for `7B parameters` style text, and prints suggestions.
    -  **Add to pool:** Resulting param counts.
    -  ✅ **Journal Check:** Mark *Step 2.1 (Prong A)* as complete.

#### Prong B: ArXiv HTML (Pivot & Validate)
- **Input:** `arxiv.org/abs/...` URLs from `Source / Paper` or `Notes`.
- **Action:**
    - Fetch the ArXiv HTML page.
    - **Hunt for Code:** Look for "Model Cards" section or links to Hugging Face.
    - If new HF links found -> **Run Prong A logic on them immediately.**
    - **Hunt for Params:** Regex search the HTML text for parameter counts.
    - **Add to pool:** `Model_Locations` (newly found HF links) and `Param_Billions`.
    - ✅ **Journal Check:** Mark *Step 2.1 (Prong B)* as complete.

#### Prong C: PDF → Markdown (Deep Dive)
- **Prerequisite:** `source papers/.venv/bin/activate` (Required for `markitdown`).
- **Input:** ArXiv IDs (from `Source / Paper` or `Notes`).
- **Source:** Defaults to `https://arxiv.org/pdf/<ARXIV_ID>.pdf`.
- **Tools:** `markitdown[pdf]` in `papers/.venv`.
- **Action:**
    1.  **Download/Locate:** Ensure `papers/<ID>/pdf/<ARXIV_ID>.pdf` exists.
        -   **Tool:** `python fetch_and_convert_papers.py --ids <ID>`
        -   *Note:* This script handles downloading AND converting to markdown automatically.
    2.  **Verify Content:** Read the top of the Markdown to confirm title match.
    3.  **Extract:** Context-aware search for "X parameters".
        -   **Tool:** `python inspect_markdown_params.py --ids <ID> --report candidates.md`
        -   **Action:** 
            -   Review the console output OR the `candidates.md` file.
            -   Look for explicit parameter counts (e.g., "7B") in the context of the *proposed* model, not a baseline.
            -   **Troubleshooting:** If you suspect a match was rejected (e.g. "7B tokens"), check `logs/pipeline.log`.
    -   **Add to pool:** `Param_Billions`.
    -   ✅ **Journal Check:** Mark *Step 2.1 (Prong C)* as complete. Note any findings in the journal.

### 2.2 Step 2 — Aggregation & Update (Finalize)
Once all prongs have run for a row, we perform a strict aggregation to ensure no duplicates.

1.  **Aggregate Locations (Unique Sets Only):**
    - Collect all URLs from {Manual Links} + {Step 2.0 Search Results} + {Step 2.1B ArXiv Findings}.
    - **Deduplication Rule:** Convert to a Set. Normalize strings (strip trailing slashes, lowercase hosts) to ensure `huggingface.co/A` and `huggingface.co/A/` are treated as identical.
    - **Outcome:** A sorted list of unique URLs.
    - ✅ **Journal Check:** Mark *Step 2.2 (Locations)* as complete.

2.  **Aggregate Parameters (Unique Sets Only):**
    - Collect all counts from {Prong A} + {Prong B} + {Prong C}.
    - **Deduplication Rule:** 
        - Convert all findings to float (billions).
        - Filter out duplicates (e.g., if HF says 7.0 and PDF says 7.0, keep one).
        - **Conflict Resolution:** If values are close but not identical (e.g., 6.9B vs 7.0B), keep both for human review unless one source is clearly authoritative (HF metadata > PDF text).
    - **Outcome:** A sorted list of unique parameter counts (e.g., `[7.0, 13.0]`).
    - ✅ **Journal Check:** Mark *Step 2.2 (Params)* as complete.

3.  **Write to Markdown:**
    - Update `Model_Locations` with the **unique** list.
    - Update `Param_Billions` with the **unique** list.
    - **Set `Analyzed = "analyzed"`**.
    - ✅ **Journal Check:** Mark *Step 2.2 (Write)* as complete.

4.  **Final Polish:**
    - Run `python parse_scored_architectures.py` one last time to sync the CSV.
    - ✅ **Journal Check:** Mark *Step 2.2 (Sync)* as complete. Verify `git diff` looks correct.

---

## 3. Finalization Semantics

- **Analyzed = "analyzed"**: We have thrown the kitchen sink (Search, HF, ArXiv, PDF) at this entry.
    - If `Param_Billions` is empty, it genuinely means we couldn't find a reliable number (or it's close weights).
    - If `Param_Billions` has values, they are the best available truth.

- **Analyzed = ""**: This row is pending processing. Do not use for `experiments/` modeling yet.

---

## 4. What No Longer Exists

- **Manual "Seed Locations"**: We moved HF search automation into Step 2.0 so humans don't have to copy-paste URLs.
- **Waterfall Logic**: We no longer stop at the first finding. We aggregate sources to handle cases where the paper lists the count but HF doesn't (or vice versa).
