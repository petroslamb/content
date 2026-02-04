# Skeptic's Checklist Template

> **Purpose:** For every major claim in the paper, document what would make it false, what assumptions it rests on, and what the authors didn't address.

---

## How to Use

For each major claim in the paper you're synthesizing:
1. State the claim
2. Identify the assumptions
3. Identify potential failure modes
4. Note what the authors didn't say

---

## Claim Template

### Claim: [State the claim]

**Source:** [Paper section, page, or quote]

**Assumptions this rests on:**
- [ ] _______________________
- [ ] _______________________
- [ ] _______________________

**What would falsify this claim?**
- _______________________

**Failure modes the authors didn't address:**
- _______________________

**What I will add in my synthesis:**
- _______________________

---

## Example (ToolOrchestra)

### Claim: "An 8B orchestrator outperforms GPT-5 on HLE at 2.5x lower cost."

**Source:** Abstract, Table 1

**Assumptions:**
- [x] HLE benchmark is a valid measure of "intelligence"
- [x] TogetherAI pricing is representative of real-world costs
- [x] The training data (ToolScale) doesn't leak into HLE

**What would falsify this?**
- HLE contamination in ToolScale training data
- Self-hosted inference costs that differ from API pricing

**Failure modes not addressed:**
- What happens with non-NVIDIA infrastructure?
- Sensitivity to reward balance hyperparameters

**What I will add:**
- Note the pricing assumption explicitly
- Suggest readers verify with their own cost model

---

## Blank Template (Copy for each claim)

```markdown
### Claim: 

**Source:** 

**Assumptions:**
- [ ] 
- [ ] 
- [ ] 

**What would falsify this?**
- 

**Failure modes not addressed:**
- 

**What I will add:**
- 
```

---

*Complete one entry for each major claim before Phase 4 (Drafting).*
