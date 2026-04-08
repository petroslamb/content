# Revision 2 Blueprint: Neural Architecture Design as a Compositional Language

This blueprint maps the conceptual and structural architecture for the "High-Fidelity" refinement of the flagship essay.

## 1. Thematology (The Conceptual Engines)

| Theme | The "Scaffold" Principle | Goal for Revision 2 |
|:---|:---|:---|
| **Scaffold vs Blueprint** | Architecture is a capacity space, not a rigid machine. | Establish the "Grammar" as a search space for gradient descent. |
| **Compositional Uniformity** | Stacked identical blocks win over custom hierarchies. | Detail the stability benefits (hyperparameters, parallelization). |
| **The Ensemble Fabric** | ResNets consist of $2^n$ overlapping shallow paths. | **[NEW]** Pivot from "Deep Hierarchy" to "Robust Consensus." |
| **The Gating Syntax** | Multiplicative operators ($\times$) provide the "Logic Gate." | **[NEW]** Balance the Additive Residual ($+$) with Gated MLPs ($x \cdot \sigma(x \cdot W)$). |
| **The Normalization Leveler** | Blocks require "Syntactic Agreement" to be composed. | **[NEW]** Frame RMSNorm as the essential leveler for summation. |
| **Optimization-First** | Architecture is good if it creates a smooth loss surface. | Link to the Li et al. (2018) "Loss Landscape" research. |

## 2. Structural Architecture (The Arc)

### Part 1: The Principle Summary (The Hook)
*   **Objective**: Contrast "Designing a machine" with "Writing a grammar."
*   **Tone**: Insightful, vocabulary-changing.
*   **Key Moves**: The move from `if-then` logic to `Search Space` creation.

### Part 2: The Historical Genealogy (The Eras)
*   **Era 1: The Hand-Crafted Hierarchy (2012-2015)**
    *   AlexNet (Custom) vs. VGGNet (Uniformity).
*   **Era 2: The Modular Revolution (2015-2017)**
    *   ResNet (The breakthrough of Residuals) vs. Inception (The parallel committee).
*   **Era 3: The Universal Block (2017-2019)**
    *   Transformers ($Q, K, V$) and the birth of a unified scaling unit.
*   **Era 4: The Strategic Design Space (2017-2023)**
    *   NAS (Search) and RegNet (Designing the principles of the space).
*   **Era 5: The Understanding Era (2019-2023)**
    *   Scaling Laws, Lottery Tickets, and Loss Landscapes.
*   **Era 6: The Hybrid Era (2023-Present)**
    *   Learned non-uniformity (MoE) and Alternative Primitives (Mamba).

### Part 3: The Detailed Synthesis (The Theory)
*   Drafting the 6 "Design Principles" (Uniformity, Residuals, Swappability, etc.).
*   Connecting each principle to a specific local source in `sources/markdown/`.

### Part 4: The Horizon (The Future)
*   Forecast: Dynamic Architectures and Cross-Modal Composability.
*   The "DR Tulu" Shift: From designing blocks to designing training scaffolds.

### Part 5: The Closing Argument (The Thesis)
*   Architects as "Grammarians of Computation."
*   Final validation of the "Scaffold Hypothesis."

## 3. Success Rubric (Revision 2 Goals)
To reach an "outstanding" (9+) score as per `workflows/essay-iteration`, the draft must satisfy:

| Axis | Goal | Score (0-10) |
|:---|:---|:---|
| **Technical Fidelity** | Every "Principle" is backed by a specific result from `sources/`. | |
| **Conceptual Clarity** | The "Grammar" analogy explains *Gating* and *Refinement* as operators. | |
| **Historical Lineage** | The move from AlexNet to DR Tulu feels like an inevitable logical progression. | |
| **Voice Consistency** | Adheres to the specific "Auditor Tone" and "Ban List" in `voice_consistency_guide.md`. | |
| **Evidence density** | Citations are integrated into the narrative flow, not just appended. | |

## 4. Evidence Mapping (Local Sources)
The following sources in `sources/markdown/` must be cross-referenced for data points:
- [x] `2015_ResNet.md` - Extraction of the bottleneck formula.
- [x] `2016_ResNet_Ensembles.md` - The "Ensemble Fabric" theory.
- [x] `2017_Transformers.md` - Extraction of the $Q, K, V$ operator.
- [x] `2019_BERT_Attention.md` - Mapping the functional hierarchy metrics.
- [x] `2018_Loss_Landscapes.md` - Context for "Optimization Geometry."
- [x] `2020_Scaling_Laws.md` - Power law coefficients for the scaling section.
- [x] `2024_Mixtral.md` - The Gating Syntax and MoE routing.
- [x] `2025_DR_Tulu.md` - Context for the "Training Scaffolds" era.

## 4. Revision Status
- **Current Version**: Substack Snapshot (Nov 2025).
- **Target Revision**: Revision 2 (High-Fidelity Research Memo + Idea Essay).
- **Audit Requirement**: Correct the "Citation Drift" (the 3 missing papers).
