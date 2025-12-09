# Parameter & Location Ingestion Playbook

This file documents the **canonical workflow** for filling `Model_Locations`, `Param_Billions`, and `Analyzed` in `scored_architectures.md`. It replaces older hard‑coded helper scripts and is intended to be **source‑of‑truth for future passes**.

## 0. Source of Truth

- The canonical dataset is `scored_architectures.md`.  
- `scored_architectures.csv` is a **derived artifact**: `parse_scored_architectures.py` regenerates the CSV from the markdown tables and **overwrites all rows/columns**. Any edits must be made in the markdown; the CSV is read‑only from a human perspective.

## 1. Adding New Architectures

When ingesting a new batch (e.g., from `techniques_for_scoring.md` or manual research):

0. **Pre‑check: validate scores in the batch**  
   - Before adding *any* rows to markdown or CSV, go through the new batch and verify that all proposed scores exist and make sense (GA, MAL, PAR, STI, IM, H, E, Zone).  
   - If any score looks inconsistent with the Gate‑1 rubric or prior rows, **stop the process here** and report back (do not add those rows yet). The dataset should only be extended with scores you’re comfortable defending.

1. **Add rows to `scored_architectures.md`**  
   - Assign a new `ID` (A*/B*/C*/D*/E* series).  
   - In the relevant scorecard table, add a row with columns including at least:  
     - `ID`, `Architecture`, `Year`, `Era`, `GA`, `MAL`, `PAR`, `STI`, `IM`, `H`, `E`, `Zone`, `Source / Paper`, `Notes`, `Section`, `Analyzed`, `Param_Billions`, `Model_Locations`.  
   - For new rows, set:
     - `Section` to the appropriate section label (e.g., `3.2 Skipped Architectures (...)`).  
     - `Analyzed` empty.  
     - `Param_Billions` and `Model_Locations` to `[]` (empty JSON lists) or leave them blank and fill later.

2. **Seed locations for new rows (HF search + arXiv) — in Markdown**  
   - Work **directly in `scored_architectures.md`**. For each new architecture, update the `Model_Locations` cell so it contains:  
     - **At least one Hugging Face repo URL** if *any plausible* official model exists.  
     - And/or the canonical **arXiv `abs` URL** for the main paper.  
   - Always attempt an HF search for every new architecture:  
     - Use `huggingface_hub.HfApi().list_models(search=...)` with the architecture name and expected lab (e.g., `search="Llama 3"`, `author="meta-llama"`).  
     - For each candidate `modelId`, **verify** before adding:  
       - Owner/org matches the expected lab (e.g., `meta-llama`, `mistralai`, `tiiuae`, `bigscience`, `ai2`, `01-ai`, etc.).  
       - The `modelId` string clearly contains the architecture name / variant.  
       - The model card (README) mentions the correct paper title and/or arXiv ID from `Source / Paper` / `Notes`, and the described type/size matches the row.  
     - Only after passing these checks add `https://huggingface.co/{modelId}` to the `Model_Locations` cell (as a JSON list) in `scored_architectures.md`. If **no** candidate passes verification, leave HF entries empty and rely on arXiv/manual links.  
   - Example `Model_Locations` value:  
     - `["https://huggingface.co/meta-llama/Meta-Llama-3-8B", "https://arxiv.org/abs/2404.04652"]`  
   - Keep `Param_Billions = []` and `Analyzed = ""` for these new rows at this stage.

3. **Regenerate the CSV (derived only)**  
   - Run: `python parse_scored_architectures.py` from `scorecard_dataset/`.  
   - This parses the tables in `scored_architectures.md` and writes a fresh `scored_architectures.csv`, **overwriting all columns** (`Param_Billions`, `Model_Locations`, `Analyzed`, `Section`, etc.) with whatever is currently in the markdown.

## 2. Parameter Extraction Pipeline

Once new rows exist in the markdown (and thus in the derived CSV) with `Model_Locations` populated and `Analyzed = ""`, run the pipeline in this order. All *authoritative* edits (including weights and locations) should be made in `scored_architectures.md`; the CSV is regenerated afterward.

### 2.1 Step A — Hugging Face Model Cards (Preferred)

- **Scope:** Rows in `scored_architectures.md` with `Analyzed = ""` and at least one `huggingface.co/...` URL in `Model_Locations`.  
- **Action:** For each such row (edit the markdown table cells, not the CSV):
  1. Fetch the HF model page (HTML or raw README).  
  2. Search the text for phrases like:  
     - `7B parameters`, `70B-parameter`, `66M parameters`, `125M–175B parameters`, etc.  
  3. Normalize all counts to **billions** (M → ÷1000, B → as is).  
  4. Set the row’s `Param_Billions` cell in `scored_architectures.md` to a JSON list of representative sizes, e.g. `[7.0, 13.0, 70.0]`.  
  5. Ensure the HF URL(s) remain in `Model_Locations`.  
  6. Set `Analyzed = "analyzed"` for this row in the markdown.

If **no explicit parameter counts** are present on the HF page, do **not** guess; leave `Param_Billions = []` and continue to Step B.

### 2.2 Step B — ArXiv HTML Model Cards

- **Scope:** Rows still with `Analyzed = ""` in `scored_architectures.md` after Step A and at least one `https://arxiv.org/abs/...` in `Model_Locations` or `Notes`.  
- **Action:** For each such row:
  1. Fetch the ArXiv HTML landing page (or an `ar5iv` HTML mirror).  
  2. Scroll to the **“Model Cards” section at the bottom** (as in the Transformers paper and other HF‑integrated papers) and:
     - Extract any linked Hugging Face repos from that section (anchors pointing to `https://huggingface.co/...`).  
     - For each such repo, apply the same verification rules as in Step 1.3 (org, name, paper/arXiv match).  
     - Add verified HF URLs to the row’s `Model_Locations` cell in the markdown (merging with existing entries).
  3. Once new HF URLs are attached, re‑use the Step A logic on those rows:
     - Fetch the model cards for the newly discovered repos and mine them for parameter counts.  
     - Normalize to billions and update the `Param_Billions` cell in the markdown if parameters are explicitly stated.
  4. Ensure the `abs` URL remains in `Model_Locations`.  
  5. Set `Analyzed = "analyzed"` in `scored_architectures.md` once you have checked the HTML/model‑card section, even if no params or HF links are found.

If Steps A+B fail to yield parameter counts, move to Step C.

### 2.3 Step C — PDF → Markdown Fallback

- **Scope:** Rows still with `Analyzed = ""` in `scored_architectures.md` after Steps A+B.  
- **Tools:**  
  - Python **venv** under `scorecard_dataset/papers/.venv` (used only for this pipeline).  
  - The `markitdown` package (with PDF extras) inside that venv for robust PDF→Markdown conversion.  
  - `papers/fetch_and_convert_papers.py` — orchestrates fetching PDFs and calling `markitdown` to write markdown into `papers/<ID>/markdown/`.  
  - `papers/parse_markdown_params.py` — mines those markdown files for parameter mentions.

- **Action:**  
  1. Ensure the venv exists and has `markitdown[pdf]` installed, e.g.:  
     - `cd scorecard_dataset/papers && python -m venv .venv`  
     - `. .venv/bin/activate && pip install 'markitdown[pdf]'`  
  2. Run `papers/fetch_and_convert_papers.py` (using the venv’s Python) to populate `papers/<ID>/pdf/` and `papers/<ID>/markdown/` for IDs whose `Param_Billions` cells in `scored_architectures.md` are empty or `[]`; this script should call `markitdown` under the hood for each downloaded PDF.  
  3. Run `papers/parse_markdown_params.py` to:  
     - Search markdown text for “X M/B parameters” phrases.  
     - For each match, capture the surrounding snippet (line with the match ± 1–2 lines of context).  
     - The **agent (not the user)** inspects these snippets to decide whether each parameter count refers to the **target architecture** (e.g., “our Diffusion‑LM”) or to baselines/comparisons; only counts clearly tied to the target model are kept.  
     - Normalize the accepted counts to billions.  
     - Manually update the corresponding row’s `Param_Billions` and `Model_Locations` cells in `scored_architectures.md`.  
     - Set `Analyzed = "analyzed"` in the markdown for rows where parameters were found and confirmed this way.
  3. For any IDs where markdown parsing still yields no reliable parameter info, manually set `Analyzed = "analyzed"` in `scored_architectures.md` to indicate that all reasonable sources have been checked.

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
