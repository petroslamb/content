# Research Artifacts: Essays & Working Notes
**Context:** `hardware_compatibility_architecture_2023_2025`

This directory houses the research into why the Transformer architecture has become the dominant species in AI.

## 🎯 **Current Goal:** A+++ Working Note
We are constructing a new theoretical framework for *why* Transformers work mechanistically. This moves beyond "universal approximation" and "hardware luck" to specific, falsifiable claims about the architecture's internal dynamics.

**Primary Draft:**
*   **[why_transformers_work_a_convergent_synthesis.md](why_transformers_work_a_convergent_synthesis.md)**
    *   **Status:** *Active Draft (v5.3 — February 5, 2026).*
    *   **The Framework:** **"Convergent Synthesis."**
    *   **Two-page spine:** **[two_page_spine.md](two_page_spine.md)**
    *   **Key Thesis:** High-impact capabilities concentrate in **sparse, specialized subcircuits** (approx 5% of heads). The current best-effort “core bundle” framing is:
        1.  **R0:** executor + parametric substrate (tokenwise rewrite capacity + long-term memory in weights).
        2.  **R1:** sharp contextual readout (Gather-and-Aggregate / retrieval heads).
        3.  **R2:** prompt compiler (Function Vectors / task inference).
        4.  **R4:** circuit discovery (why training finds/stabilizes these bottlenecks).
        *   **R3 (routing/modularity)** is treated as an **extended** hypothesis until it has a distinct causal signature.
    *   **Objective:** Synthesize the evidence in `new_evidence/` into a rigorous, falsifiable theory of this "Grey Box."
    *   **Brutal rubric + last scored version:** **[why_transformers_work_a_convergent_synthesis_rubric_assessment.md](why_transformers_work_a_convergent_synthesis_rubric_assessment.md)** (v5.2)

---

## 📚 Published Context (The "Outside" View)

Our previous work established the external economic and institutional constraints (the "Gates") that filter architectures before they even get to prove their capability.

1.  **[The_Transformer_Attractor_Substack.md](The_Transformer_Attractor_Substack.md)** (Gate 2: Institutional)
    *   **Status:** *Published.*
    *   **Core Argument:** The "Transformer Attractor." Institutional backing and ecosystem lock-in create a trap where alternatives die unless they adopt Transformer-like compute patterns.
2.  **[The_Hardware_Friction_Map_Substack.md](The_Hardware_Friction_Map_Substack.md)** (Gate 1: Hardware)
    *   **Status:** *Published.*
    *   **Core Argument:** The "Friction Map." Unchangeable hardware constraints (GEMM-alignment) determine survival.

**Relationship:** The published essays explain *survival* (why non-Transformers die). The current working note explains *capability* (why the survivor actually works), with “dominance” treated as a separate selection story (hardware + institutions).

---

## 📂 Evidence Structure

### `new_evidence/`
The "Convergent Synthesis" is built on these evidence pillars, distilled from recent papers:
*   `from_scratch_non_forcing_hypothesis.md`: **Method reset.** Equation-first, minimal-primitives hypothesis (S1–S5) with pre-registered rivals and deletion/merge rules to avoid forced categories.
*   `r0_preconditions_insights.md`: **R0 (Preconditions).** Why “attention alone” degenerates (rank collapse), and why residual+MLP+normalization are load-bearing substrate assumptions.
*   `r1_retrieval_insights.md`: **R1 (Retrieval).** Evidence for "Sharp Retrieval" and Gather-and-Aggregate mechanisms.
*   `r2_icl_insights.md`: **R2 (In-Context Learning).** Evidence for Function Vectors and Induction Heads.
*   `r3_routing_circuits_insights.md`: **R3 (Routing, extended).** Evidence for Conditional Routing and Modular Specialization (necessity not yet nailed down).
*   `r4_scaling_insights.md`: **R4 (Discovery).** Evidence for how training finds these circuits (Grokking, Phases).
*   `composition_and_limits_insights.md`: **Limits.** Where the synthesis breaks (Compositional Generalization).

### `papers/`
Raw Markdown conversions of relevant arXiv papers.
*   Serves as the **audit trail** and **source of truth**.
*   All citations in the essay must map back to a file in this folder.
