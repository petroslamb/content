# What Actually Works: The Hardware Compatibility Filter in Neural Architecture (2023-2025)

**Status:** ✅ Published / Research Complete
**Confidence:** 0.98/1.0 (Exhaustive Literature Review + Quantitative Scorecard)
**Research Period:** Jan 2023 – Dec 2025

---

## 1. Executive Summary

This project investigates why certain neural architectures (Transformers, MoEs) dominate production while others (Capsules, Neural ODEs) remain research curiosities.

**The Core Thesis:** Architecture adoption is not determined by "physics" or pure capability, but by an **economic hardware filter**.
*   **Hardware Friction = Economic Cost:** The compatibility of an architecture's primitives with GPU hardware (Dense, GEMM-heavy) determines its "friction."
*   **The "Startup Heuristic":** High friction scales exponential cost for resource-constrained teams (startups, labs), while low friction (Transformers) allows for rapid iteration.

We measure this friction using the **Hardware Friction Scorecard**, a quantitative methodology located in `research_artifacts/scorecard_dataset/`.

---

## 2. Methodology: The Hardware Friction Scorecard

Located in: [`research_artifacts/scorecard_dataset/`](./research_artifacts/scorecard_dataset/)

Our primary methodological contribution is a rigorously defined "Gate-1" adoption filter. Architectures are scored on five axes to predict their production viability.

### The Scoring Rubric (0-10 Scale)
*   **Hardware Friendliness (H)**: Measured by **GA** (Global Access), **MAL** (Memory Access Locality), and **PAR** (Parallelism).
*   **Ecosystem Maturity (E)**: Measured by **STI** (Specialized Tooling Investment) and **IM** (Infrastructure Maturity).

### Zones of Adoption
*   🟢 **Green Zone (H≥5, E≥3):** Production-ready (e.g., Transformers, FlashAttention).
*   🟡 **Yellow Zone (Infra-Limited):** Viable but expensive (e.g., MoE, custom kernels).
*   🟠 **Orange Zone (Friction-Dominant):** Niche use cases (e.g., pure SSMs at scale).
*   🔴 **Red Zone (Hardware-Hostile):** Research only (e.g., Spiking NN, Capsules).

**Key Artifact:** [`scored_architectures.md`](./research_artifacts/scorecard_dataset/scored_architectures.md) contains the full scored dataset of 100+ architectures.

---

## 3. Key Findings (2023-2025)

Validated against 50+ sources and the [`EXHAUSTIVE_FINAL_COMPILATION.md`](./research_artifacts/EXHAUSTIVE_FINAL_COMPILATION.md).

1.  **Hardware Compatibility Predicts Adoption:** 100% of widespread production models (Llama, GPT-4, Claude) rely on GEMM-heavy, GPU-friendly primitives.
2.  **Infrastructure Lag is Predictable:** There is a consistent **24-36 month lag** from research paper to standardized production infrastructure (e.g., FlashAttention: May 2022 Paper → May 2024 Standard).
3.  **The "SSM Ceiling":** Pure State-Space Models (Mamba) have hit a ceiling at ~7B parameters. No frontier model (>70B) uses pure SSM; they all use **Hybrids** (Jamba, Qwen3-Next).
4.  **MoE is the Frontier Standard:** Mixture-of-Experts has won the high-end scaling war (DeepSeek-V3, Llama 4, Mixtral) due to economic efficiency, despite initial infrastructure complexity.

---

## 4. Repository Structure

### 📂 Main Article & Narrative
*   `long_article_sections/What_Actually_Works_2023_2025.md`: **Canonical Master Article**. The complete, polished text.
*   `essay_sections/`: Components of the shorter "Friction Map" essay.
*   `substack_drafts/`: Final markdown versions formatted for publication.

### 📊 Research & Methodology
*   `research_artifacts/scorecard_dataset/`: **(CRITICAL)** The quantitative dataset and scoring methodology.
    *   `scored_architectures.md`: The canonical detailed scoring tables.
    *   `param_location_ingestion_playbook.md`: Methodology for data ingestion (requires `ingestion_journal.md`).
*   `research_artifacts/EXHAUSTIVE_FINAL_COMPILATION.md`: Master summary of all 50+ research sources.

### 🧪 Supporting Evidence
*   `research_artifacts/moe_speedup_data_wip.md`: Meta-analysis of MoE throughput.
*   `research_artifacts/flash_attention_timeline.md`: Datapoints for the "Infrastructure Lag" finding.
*   `research_artifacts/SSM_benchmark_findings.md`: Evidence for the "SSM Ceiling."

---

## 6. Series Evolution: From "Filter" to "Friction Map"

This research has evolved beyond a single article into a multi-part series.

### Part 2: The Hardware Friction Map Essay
*   **Concept:** Moves from the binary "Hardware Compatibility Filter" to a graded **"Hardware Friction Map"**. It introduces the "Startup Heuristic"—how capital hides friction for hyperscalers but kills startups.
*   **Drafts:**
    *   Canonical Draft: [`essay_sections/The_Hardware_Friction_Map_Essay_substack.md`](./essay_sections/The_Hardware_Friction_Map_Essay_substack.md)
    *   Publication Candidate: [`substack_drafts/Substack_Hardware_Friction_Map_Essay_v2.md`](./substack_drafts/Substack_Hardware_Friction_Map_Essay_v2.md)

### Part 3: Critiques & Stress Tests
*   **Concept:** A transparent "Building in Public" meta-post detailing how we tried to break the Friction Map model and the critiques that survived.
*   **Location:** [`substack_drafts/Substack_Hardware_Friction_Map_Critiques_and_Stress_Tests.md`](./substack_drafts/Substack_Hardware_Friction_Map_Critiques_and_Stress_Tests.md)

---
