# Parameter & Location Ingestion Playbook

This file documents the **canonical workflow** for filling `Model_Locations`, `Param_Billions`, and `Analyzed` in `scored_architectures.csv`. It replaces older hard‑coded helper scripts and is intended to be **source‑of‑truth for future passes**.

## 0. Source of Truth

- The canonical dataset is `scored_architectures.csv`.  
- `scored_architectures.md` is the human‑readable table view; `parse_scored_architectures.py` regenerates the CSV from the markdown tables while preserving metadata columns (`Param_Billions`, `Model_Locations`, `Analyzed`, `Section`) where possible.

## 1. Adding New Architectures

When ingesting a new batch (e.g., from `techniques_for_scoring.md` or manual research):

0. **Pre‑check: validate scores in the batch**  
   - Before adding *any* rows to markdown or CSV, go through the new batch and verify that all proposed scores exist and make sense (GA, MAL, PAR, STI, IM, H, E, Zone).  
   - If any score looks inconsistent with the Gate‑1 rubric or prior rows, **stop the process here** and report back (do not add those rows yet). The dataset should only be extended with scores you’re comfortable defending.

1. **Add rows to `scored_architectures.md`**  
   - Assign a new `ID` (A*/B*/C*/D* series).  
   - Fill `Architecture`, `Year`, `Era`, `GA`, `MAL`, `PAR`, `STI`, `IM`, `H`, `E`, `Zone`, `Source / Paper`, `Notes`.  
   - Leave `Analyzed` empty for now.

2. **Regenerate the CSV**  
   - Run: `python parse_scored_architectures.py` from `scorecard_dataset/`.  
   - This writes an updated `scored_architectures.csv` with all rows and preserves any existing `Param_Billions`, `Model_Locations`, and `Analyzed` for old IDs.

3. **Seed locations for new rows (manual)**  
   - For each new architecture, edit `scored_architectures.csv` (or use a small helper) to ensure `Model_Locations` contains:  
     - At least one **Hugging Face repo URL** if a representative model exists.  
     - And/or the canonical **arXiv `abs` URL** for the main paper.  
   - Example:  
     - `["https://huggingface.co/meta-llama/Meta-Llama-3-8B", "https://arxiv.org/abs/2404.04652"]`  
   - Keep `Param_Billions = []` and `Analyzed = ""` for these new rows at this stage.

## 2. Parameter Extraction Pipeline

Once new rows exist in the CSV with `Model_Locations` populated and `Analyzed = ""`, run the pipeline in this order:

### 2.1 Step A — Hugging Face Model Cards (Preferred)

- **Scope:** Rows with `Analyzed = ""` and at least one `huggingface.co/...` URL in `Model_Locations`.  
- **Action:** For each such row:
  1. Fetch the HF model page (HTML or raw README).  
  2. Search the text for phrases like:  
     - `7B parameters`, `70B-parameter`, `66M parameters`, `125M–175B parameters`, etc.  
  3. Normalize all counts to **billions** (M → ÷1000, B → as is).  
  4. Set `Param_Billions` to a JSON list of representative sizes, e.g. `[7.0, 13.0, 70.0]`.  
  5. Ensure the HF URL(s) remain in `Model_Locations`.  
  6. Set `Analyzed = "analyzed"` for this row.

If **no explicit parameter counts** are present on the HF page, do **not** guess; leave `Param_Billions = []` and continue to Step B.

### 2.2 Step B — ArXiv HTML Landing Pages

- **Scope:** Rows still with `Analyzed = ""` after Step A and at least one `https://arxiv.org/abs/...` in `Model_Locations` or `Notes`.  
- **Action:** For each such row:
  1. Fetch the ArXiv HTML landing page (or an HTML mirror such as `ar5iv`).  
  2. Search for parameter phrases as in Step A and normalize to billions.  
  3. If found, set `Param_Billions` accordingly.  
  4. Ensure the `abs` URL is present in `Model_Locations`.  
  5. Set `Analyzed = "analyzed"` once you have checked the HTML, even if no params are found.

If Step A+B fail to yield parameter counts, move to Step C.

### 2.3 Step C — PDF → Markdown Fallback

- **Scope:** Rows still with `Analyzed = ""` after Steps A+B.  
- **Tools:**  
  - `papers/fetch_and_convert_papers.py` — download canonical PDFs and convert them to plain‑text markdown under `papers/<ID>/markdown/`.  
  - `papers/parse_markdown_params.py` — mine those markdown files for parameter mentions.

- **Action:**  
  1. Run `papers/fetch_and_convert_papers.py` to populate `papers/<ID>/pdf/` and `papers/<ID>/markdown/` for IDs with empty `Param_Billions`.  
  2. Run `papers/parse_markdown_params.py` to:  
     - Search markdown text for “X M/B parameters” phrases.  
     - Normalize counts to billions.  
     - Update `Param_Billions` and merge any discovered `arxiv.org/abs/...` URLs into `Model_Locations`.  
     - Set `Analyzed = "analyzed"` for rows where parameters were found.
  3. For any IDs where markdown parsing still yields no reliable parameter info, manually set `Analyzed = "analyzed"` to indicate that all reasonable sources have been checked.

## 3. Finalization Semantics

- After Steps A–C have been reasonably applied to an ID:
  - If parameter counts were found, `Param_Billions` is a non‑empty list and `Analyzed = "analyzed"`.  
  - If nothing trustworthy was found, **leave** `Param_Billions = []` and explicitly set `Analyzed = "analyzed"` to mean:
    - “We looked at HF, ArXiv HTML, and (if applicable) PDFs/markdown; there is no clear, citable parameter scale.”
- Downstream scripts and analyses should treat:
  - `Analyzed = ""` as “do not use this row yet in parameter‑based modeling.”  
  - `Analyzed = "analyzed"` with `Param_Billions = []` as “safe to include, but interpret as ‘no known parameter scale’ rather than missing data.”

## 4. What No Longer Exists

- Older helper scripts that used **hard‑coded mappings** for locations or parameters (e.g., `augment_scored_architectures_with_locations.py`, `augment_scored_architectures_with_params.py`) have been removed.  
- All parameter and location information should now come from:
  - Explicit manual entries in `Model_Locations` / `Param_Billions`.  
  - The HF → ArXiv HTML → PDF→markdown pipeline described above.
