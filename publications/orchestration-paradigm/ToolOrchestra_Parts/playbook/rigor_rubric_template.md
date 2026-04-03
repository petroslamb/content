# Rigor Rubric: Auditor-Explainer Template

> **Purpose:** Define a hybrid voice that *explains* complex papers while *auditing* their claims through cross-paper synthesis and verification.

---

## 1. The Persona: Auditor-Explainer

**Core philosophy:**
> "We do not summarize the paper; we verify it against the literature and explain where it fits."

**Your role:**
- **Explainer:** Make complex ideas accessible without dumbing them down.
- **Auditor:** Cross-reference claims against related papers. Surface what the authors didn't cite, didn't test, or got wrong.

**The output:** A synthesis that a reader couldn't produce by reading the paper alone—because you've connected it to papers the authors didn't connect, and challenged claims they didn't challenge.

---

## 2. The Verification Signals

Every paragraph must pass at least one of these signals.

### Signal A: Cross-Paper Synthesis
- **Question:** Have you connected this claim to related work the authors didn't cite?
- **Fail:** "The paper uses GRPO for training."
- **Pass:** "The paper uses GRPO (Shao et al., 2024), but does not compare to RLHF baselines (Ouyang et al., 2022) or Constitutional AI's reward hierarchy (Anthropic, 2022). This matters because..."

### Signal B: Claim Verification
- **Question:** Have you checked if this claim is reproducible or falsifiable?
- **Fail:** "The system achieves 37.1% on HLE."
- **Pass:** "The system achieves 37.1% on HLE. This assumes TogetherAI pricing ($X/1M tokens). At self-hosted rates, the breakeven shifts to Y."

### Signal C: Gap Identification
- **Question:** What did the authors *not* address that the related literature does?
- **Fail:** "The paper trains an orchestrator."
- **Pass:** "The paper assumes benign tools. It does not engage with adversarial tool use (Smith et al., 2024) or prompt injection at the tool level. This is a critical gap for production systems."

### Signal D: Accessible Mechanism
- **Question:** Can a non-expert understand *how* this works after reading your explanation?
- **Fail:** "The orchestrator uses RL."
- **Pass:** "The orchestrator learns which tool to call by trial and error. Each successful task gives a +1 reward; each wasted API call gives a cost penalty. Over millions of trials, it learns the cheapest path to correct answers."

---

## 3. The Synthesis Requirements

For each Part in your series, you must:

| Requirement | How to Check |
|---|---|
| **Cite at least 2 papers the authors didn't cite** | Cross-reference the Related Work section against your own literature search |
| **Identify 1 assumption the authors don't justify** | Look for "we assume," "we use," or unstated prerequisites |
| **Propose 1 failure mode not discussed** | Ask: "What breaks if X assumption is violated?" |
| **Provide 1 concrete verification step the reader can do** | E.g., "Recalculate using your own API pricing" |

---

## 4. Banned Patterns

| Banned | Why | Replace With |
|---|---|---|
| "The authors claim..." (without verification) | Passive acceptance | "The authors claim X, which aligns with / contradicts Y (citation)." |
| "This is novel because the authors say so" | No independent check | "This differs from prior work (A, B) by specifically changing Z." |
| "Revolutionary," "Elegant," "State-of-the-art" | Adjectives without data | Cite benchmark numbers or direct comparisons |
| Repeating the abstract | Zero value-add | Start with what the abstract *doesn't* tell you |

---

## 5. Structural Rules

- [ ] Each Part includes an **Annotated Bibliography** (not just a reference list—explain *why* each paper matters)
- [ ] Each Part includes a **"What the Paper Doesn't Say"** section
- [ ] Each Part connects to at least one paper *not* in the original paper's references
- [ ] No conclusion paragraphs—end when the evidence runs out

---

## 6. Quality Checklist (Before Publishing)

For each Part, verify:

- [ ] I have cited **at least 3 external papers** not cited by the authors
- [ ] I have identified **at least 1 unverified assumption**
- [ ] I have proposed **at least 1 failure mode**
- [ ] A reader who reads only my Part **understands the mechanism** without reading the original paper
- [ ] A reader who has read the original paper **learns something new** from my synthesis

---

*Complete this rubric before Phase 3 (Modeling). Apply it during Phase 4 (Drafting) and Phase 5 (Verification).*

---

## Quick Reference: The 6 Phases

| Phase | Goal | Key Output |
|---|---|---|
| **1. Research** | Deep understanding of paper + literature | `papers/` directory, Annotated Bibliography v0 |
| **2. Strategy** | Lock structure, voice, promotion plan | This rubric, bundling strategy, promotion plan |
| **3. Modeling** | Outline every Part before writing | `outline/part_XX.md`, Skeptic's Checklist |
| **4. Drafting** | Write against the rubric | Draft Parts (no structural changes) |
| **5. Verification** | Audit for accuracy and style | Synthesis Assessment, final polish |
| **6. Distribution** | Execute promotion plan | Track traction, iterate |
