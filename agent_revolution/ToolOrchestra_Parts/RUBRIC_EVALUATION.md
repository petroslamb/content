# The Engineering Rigor Rubric
# Manifesto: The System Auditor

> [!NOTE]
> **Status:** Permanent Design Standard
> **Role:** The constitution for the "ToolOrchestra" series.
> **Philosophy:** We do not sell the paper. We reverse-engineer it to find where verify the system breaks.

---

## 1. The Core Philosophy: "The System Auditor"

To write a definitive guide, we must assume the role of an auditor, not a promoter.

*   **Promoter says:** "The orchestrator intelligently adapts to user preferences."
*   **Auditor says:** "The orchestrator conditions its policy on a prepended token vector. If this vector is not normalized, gradients explode."

### The 4 Commandments
1.  **Mechanics over Metaphors:** If you use an analogy (e.g., "Conductor"), you must immediately explain the technical implementation (e.g., "Sequential decision process over a jagged action space").
2.  **Constraints are Alpha:** The most valuable information for an engineer is *where the system breaks*. Every part must explicitly list its dependencies and failure modes.
3.  **Economics are Physics:** In GenAI, cost and latency are not "features": they are physical laws. Treat token costs and inference time as hard constraints.
4.  **No Adjectives:** "Elegant", "Robust", "Seamless", "Revolutionary" are banned. Use data.

---

## 2. The Evaluation Signals

Every paragraph in the series is measured against these four signals.

### Signal A: The Mechanic
*   **Question:** Does this text explain *how* the state changes?
*   **Fail:** "It learns to route tasks."
*   **Pass:** "It optimizes a policy $\pi_\theta(a|s)$ where the action space $A$ is the set of valid JSON tool calls."

### Signal B: The Dependency
*   **Question:** What must be true for this to work?
*   **Fail:** "It works with any tool."
*   **Pass:** "It requires every tool to have a descriptive docstring < 500 tokens. Performance degrades linearly with description ambiguity."

### Signal C: The Economics
*   **Question:** Is the arbitrage viable?
*   **Fail:** "It saves money."
*   **Pass:** "The system is viable only when $Cost(Orchestrator) + Cost(Tool) < Cost(GPT-5)$. For 8B models, this breakeven point is at ~500 input tokens."

### Signal D: Density
*   **Question:** Is this sentence necessary?
*   **Fail:** "In the rapidly evolving landscape of AI, this is paramount." (0 bits of info)
*   **Pass:** "We use PPO with a KL penalty of 0.1." (High information density)

---

## 3. The Structural Blueprint

The series consists of 4 thematic bundles ("Issues"). This structure respects the "Meal vs. Snack" content rule.

### Issue 1: The Algorithm (Theory)
*   **Parts:** 00, 01, 02, 03
*   **Theme:** "Why we need RL, and how GRPO works."
*   **Goal:** Establish the Arbitrage Thesis and the Mathematical Foundation.
*   **Target:** ML Researchers & Algo Engineers.

### Issue 2: The Factory (Infrastructure)
*   **Parts:** 04, 05, 06
*   **Theme:** "The hidden cost of Data, Evals, and H100s."
*   **Goal:** Demystify the "Supply Chain" of synthetic data and the "Physicality" of training.
*   **Target:** Data Engineers & MLOps Architects.

### Issue 3: The Behavior (Strategy)
*   **Parts:** 07, 08, 09
*   **Theme:** "Emergent State Machines and Alignment Traps."
*   **Goal:** Analyze the runtime behavior, specifically how it breaks (generalization failure, prompt injection).
*   **Target:** AI Product Engineers & Security Auditors.

### Issue 4: The Reality (Implications)
*   **Parts:** 10, 11, 12
*   **Theme:** "History, Future Risks, and Production Nightmares."
*   **Goal:** Connect the lineage (past) to production risks (present) and unsolved frontiers (future).
*   **Target:** CTOs & Senior Leaders.

---

## 4. Execution Guidelines

1.  **Assume the reader is smart:** Do not explain what "Attention" is. Explain how *this specific* attention mask differs.
2.  **Break prose with Code:** Engineers read code faster than text. Use Python/Pseudocode for logic.
3.  **Visuals are text:** Use ASCII diagrams or Mermaid definitions for flows.
4.  **No Conclusion Paragraphs:** End when the data runs out. Do not summarize what you just said.

---

*This document serves as the permanent style guide for the ToolOrchestra series.*
