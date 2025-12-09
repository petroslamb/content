# Hardware Friction Scorecard Dataset

**Status:** Active / Calibration Phase
**Primary Artifact:** `scored_architectures.md`

---

## Directory Overview

This directory contains the quantitative engine of the Hardware Friction project: a dataset of 100+ neural architectures scored against the "Gate-1" hardware compatibility rubric.

### 1. The Core Dataset
*   **`scored_architectures.md`** (Canonical Source):
    *   The single source of truth.
    *   Contains the human-readable scoring tables for all architectures (A-Series to E-Series).
    *   **Edit Policy:** All manual edits (scores, notes, new rows) MUST happen here.
*   **`scored_architectures.csv`** (Machine-Readable):
    *   **Derived Artifact.** Do not edit directly.
    *   Generated from the markdown file using `parse_scored_architectures.py`.
    *   Used by the experiment scripts for modeling.

### 2. Ingestion & Tools
*   **`param_location_ingestion_playbook.md`**:
    *   The rigorous protocol for adding new architectures. **Requires adherence to `ingestion_journal.md`.**
*   **`ingestion_journal.md`**:
    *   **The Ledger.** A persistent record of data ingestion batches. You must initialize new entries using `JOURNAL_TEMPLATE.md`.
*   **Pipeline Scripts:**
    *   `hf_search_model_cards.py`: Searching & inspecting Hugging Face.
    *   `fetch_and_convert_papers.py`: Downloading PDFs & converting to Markdown.
    *   `inspect_markdown_params.py`: Analyzing Markdowns for parameter counts (supports `--report`).
    *   `parse_scored_architectures.py`: Syncing Markdown → CSV.
*   **`utils.py`**:
    *   Centralized logging configuration.

### 3. Logs & Artifacts
*   **`logs/pipeline.log`**:
    *   Automated audit trail. Captures full arguments (DEBUG) and clean run history (INFO).
*   **`experiments/`**:
    *   Contains Python scripts (`predict_zones.py`) that train simple explainable models.

## How to Contribute

1.  **Read the Playbook:** `param_location_ingestion_playbook.md`.
2.  **Open the Journal:** Initialize your batch in `ingestion_journal.md`.
3.  **Execute & Log:** Follow the journal checklist strictly.
4.  **Edit Markdown:** Add your new architecture to `scored_architectures.md`.
5.  **Sync:** Run `python parse_scored_architectures.py`.
