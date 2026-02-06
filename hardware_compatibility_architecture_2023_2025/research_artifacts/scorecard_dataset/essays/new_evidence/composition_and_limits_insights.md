# New Evidence: Compositional Generalization & Theoretical Limits

**Status:** Processed
**Date:** Feb 4, 2026
**Papers Analyzed:**
1.  **Valipour et al. (2025):** How Do Transformers Learn Variable Binding in Symbolic Programs?
2.  **Feng et al. (2024):** Chain of Thought Empowers Transformers to Solve Inherently Serial Problems
3.  **Weiss et al. (2021):** Thinking Like Transformers (RASP)
4.  **Merrill et al. (2024):** The Illusion of State in State-Space Models
5.  **Jelassi et al. (2024):** Repeat After Me: Transformers are Better than State Space Models at Copying
6.  **Bordt et al. (2024):** Transformers Need Glasses: Information Over-Squashing in Language Tasks
7.  **Behrouz et al. (2025):** Titans: Learning to Memorize at Test Time
8.  **Sarrof et al. (2024):** The Expressive Capacity of State Space Models
9.  **Li et al. (2025):** Universal Approximation with Softmax Attention

---

## Executive Synthesis
This batch of papers provides rigorous theoretical and empirical grounding for the **Hybrid Hypothesis** (Transformers + Recurrence) and clarifies the **Theoretical Limits** of pure attention.

*   **The Hybrid Imperative:** We now have clean separations on *memory behavior*. Depth-2 Transformers can implement copying at lengths exponential in a size parameter, while fixed-state SSMs provably cannot copy uniform inputs beyond their state memory without scaling memory ~linearly with length (Jelassi). Conversely, SSMs admit length-generalizing constructions for star-free state-tracking languages and bounded-depth Dyck tasks where Transformers often fail to length-generalize empirically (Sarrof). Merrill formalizes that common SSMs are simulable in **TC0** (and treats standard finite-precision Transformers similarly), while Bordt shows finite-precision decoder-only Transformers can exhibit representational collapse / over-squashing—together motivating hybrid memory designs. **Titans** (Behrouz) is one such convergence: attention as short-term memory + a learned long-term neural memory updated at test time.
*   **Escaping Constant-Depth Bounds:** For constant-depth decoder-only Transformers that answer directly (no CoT), expressiveness is upper-bounded by **AC0** under constant-bit precision and by **TC0** under log-precision (Feng; Merrill-style TC0 framing). This does *not* rule out many “parallel-friendly” problems (e.g., modular addition; even parity with log-precision), but under standard conjectures it rules out many **NC1-hard / inherently-serial** tasks at low depth (e.g., permutation-group word problems / circuit value). CoT provides extra sequential steps; with **T** CoT steps, a constant-depth Transformer can simulate circuits of **size T**, strictly increasing expressivity as T grows (Feng).
*   **Mechanism of Universality (Expressivity, not learnability):** (Softmax-)attention-only layers (with linear maps) are universal approximators for **continuous** Seq2Seq functions on compact domains; softmax can implement near-argmax interpolation, acting like a “generalized ReLU” selector (Li). This challenges the oversimplified “attention routes, MLP computes” trope at the level of expressivity.

---

## Theme 1: The "State" of State Space Models (SSMs vs. Transformers)
*Gap Addressed: Why Hybrids Win / R1 (Retrieval) vs. R3 (Routing)*

### 1. The Retrieval Gap (Evidence for Transformers)
*   **Jelassi (2024)** proves a fundamental separation:
    *   **Theory:** A 2-layer Transformer can copy strings of exponential length (in number of heads). An SSM (fixed state size) fails unless state grows linearly with input ($d \approx L$).
    *   **Empirical:** Transformers learn copying ~100x faster than Mamba/LSTMs and generalize better to longer sequences.
    *   *Significance:* Strong evidence that fixed-state SSMs are **not** a drop-in replacement for attention-based *in-context copying / long-context retrieval inside the model*: to match, they need state/memory scaling with length or an explicit external memory / attention-like access mechanism.

### 2. The State-Tracking Edge (Evidence for SSMs)
*   **Sarrof (2024)** provides the counter-narrative:
    *   **Star-Free Languages:** SSMs (Mamba) have length-generalizing constructions and strong empirical length generalization on "star-free" state-tracking languages (e.g., Flip-Flop), whereas Transformers show mixed results and often fail to length-generalize even on some star-free cases.
    *   **Bounded Hierarchy:** SSMs can model **bounded-depth** Dyck languages (Dyck$_{K,h}$) with optimal memory *without* stacks, challenging the assumption that attention is effectively mandatory for bounded hierarchy (this does **not** imply solving unbounded Dyck-$k$).
    *   *Significance:* SSMs are not "strictly worse"; they are specialized for *state maintenance*. This supports the architectural split in Hybrids: SSM layers for state/syntax, Attention layers for retrieval/semantics.

### 3. The "Illusion" of Infinite Memory
*   **Merrill (2024)** serves as a reality check for SSM hype:
    *   **TC0 Limit:** Standard SSMs (S4, Mamba) are in **TC0** (and Merrill treats standard finite-precision Transformers similarly). Under the standard conjecture **TC0 ≠ NC1**, they cannot solve **NC1-hard** state-tracking problems (e.g., permutation-group word problems / permutation composition) at constant depth, while RNN-style extensions can.
    *   *Insight:* The "state" in Mamba is not a true recurrent state in the expressive sense (infinite depth); it's a compressed summary subject to similar bounds as attention, just with different trade-offs (compression vs. access).

---

## Theme 2: Limits of Pure Attention & The CoT Escape Hatch
*Gap Addressed: Theoretical Limits / R4 (Scaling)*

### 1. Representational Collapse
*   **Bordt (2024)** identifies a physical limit:
    *   **The Phenomenon:** Distinct sequences can yield arbitrarily close final-token representations ("representational collapse"); finite (and especially lower) floating-point precision can make this collapse manifest at shorter lengths.
    *   **Over-squashing:** Information from early tokens decays/squashes as it propagates, distinct from vanishing gradients.
    *   *Significance:* This imposes practical constraints on long-context copying/counting in standard decoder-only, finite-precision stacks; it motivates precision/memory interventions and architectural changes (Bordt proposes simple mitigations), and adds pressure toward neural/external memory hybrids (Titans) or distinct state variables (SSMs).

### 2. CoT as Complexity Class Expansion
*   **Feng (2024)** offers the theoretical justification for "System 2" thinking:
    *   **The Bound:** For constant-depth, finite-precision Transformers that answer directly (no CoT), expressiveness is upper-bounded by **AC0** (constant-bit precision) or **TC0** (log-precision). This rules out many NC1-hard / inherently-serial tasks at low depth under standard conjectures (e.g., permutation composition / circuit value), but does **not** rule out modular addition (in TC0) and does not rule out parity under log-precision.
    *   **The Escape:** With **T** CoT steps, a constant-depth Transformer can simulate circuits of **size T** (hence enabling T serial steps).
    *   *Key Finding:* CoT can make some problems solvable that are impossible for a *fixed-depth, direct-answer* Transformer in a single forward pass (under the paper’s precision/complexity assumptions).
    *   *Significance:* "Thinking time" isn't just about error correction; it's about fundamentally changing the *computational class* of the model.

### 3. Attention is All You Need (Literally)
*   **Li (2025)** strengthens the core foundation:
    *   **Universality:** One layer of (multi-head) Attention + Softmax is a universal approximator for **continuous** Seq2Seq functions on compact domains (with linear maps).
    *   **Mechanism:** Softmax acts as a selector for interpolation points (effectively a "Generalized ReLU").
    *   *Significance:* At the level of expressivity, refutes the simplistic idea that Attention = Routing and MLP = Compute; attention itself can implement rich computation.

---

## Theme 3: Compositional Generalization Mechanisms (R3)
*Gap Addressed: R3 (Flexible Routing)*

### 1. How Binding Happens
*   **Valipour (2025)** visualizes the learning trajectory:
    *   **3 Stages:** Random -> Heuristic -> Systematic Variable Binding.
    *   **The "Residual Memory":** The model uses the residual stream as an addressable memory, writing variable-value pairs to specific subspaces.
    *   **Head Specialization:** Specific heads emerge solely for "binding" (routing value to variable) and "lookup".

### 2. RASP as the Computational Frame
*   **Weiss (2021)** gives us the language:
    *   **RASP:** A programming language for Transformers.
    *   *Selectors:* The primitive of attention.
    *   *Element-wise:* The primitive of MLPs.
    *   *Significance:* Helps formalize *what* algorithms a Transformer can easily learn (those compilable to RASP) vs. those that are hard (requires indices/loops).

---

## Synthesis for Essay Integration

| Insight | Integration Point |
| :--- | :--- |
| **Separation Theorem** (Jelassi/Sarrof) | **Part II (Hybrids):** Define the "Pareto Frontier" of Memory. Transformers = Retrieval (R1), SSMs = State (State-Tracking). |
| **CoT $\rightarrow$ Escape TC0** (Feng) | **Theoretical Limits:** Explain *why* next-token prediction isn't enough for reasoning. The model needs "depth" (steps) to simulate serial logic. |
| **Neural Memory** (Behrouz) | **Future Directions:** The "Titans" architecture as the logical next step after Hybrids—learning to memorize *at test time* (Meta-learning). |
| **Attention = Interpolation** (Li) | **Computational Frames:** Upgrade the description of the attention mechanism from just "routing" to "universal approximation via interpolation". |
| **Variable Binding Phases** (Valipour) | **R3 (Compositionality):** Add the "3-Phase Learning" model to explain grokking/emergence of symbolic reasoning. |
