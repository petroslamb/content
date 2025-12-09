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
    *   The rigorous protocol for adding new architectures, finding parameter counts, and verifying model existence via Hugging Face / ArXiv.
*   **`parse_scored_architectures.py`**:
    *   Script to convert the canonical Markdown tables into the CSV format.
*   **`hf_search_model_cards.py`**:
    *   Utility to help verify model existence on Hugging Face during ingestion.

### 3. Experiments & calibration
*   **`experiments/`**:
    *   Contains Python scripts (`predict_zones.py`) that train simple explainable models (Logistic Regression, Decision Trees) to predict the "Zone" (Green/Yellow/Red) from the component scores (GA/MAL/PAR/STI/IM).
*   **`papers/`**:
    *   Storage for raw PDF papers and their markdown conversions, used for deep-dive parameter verification when model cards are missing.

---

## How to Contribute

1.  **Read the Playbook:** `param_location_ingestion_playbook.md` is mandatory reading.
2.  **Edit Markdown First:** Add your new architecture to `scored_architectures.md`.
3.  **Regenerate CSV:** Run `python parse_scored_architectures.py` to update the dataset.
4.  **Verify:** Check if your new row appears correctly in the CSV and doesn't break the predictive models in `experiments/`.
