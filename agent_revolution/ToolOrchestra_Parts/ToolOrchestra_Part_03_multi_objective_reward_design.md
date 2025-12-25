# The Orchestration Paradigm Series: Dive 3
*How do you optimize for multiple objectives at once?*

## Introduction

The previous dive established that orchestration requires reinforcement learning—trial, feedback, and adjustment. But what exactly should the reward signal measure? If you only reward accuracy, the orchestrator will call the most expensive model for every question. If you only reward cost-efficiency, it'll guess cheaply and get everything wrong. Real orchestration requires balancing conflicting goals: being accurate enough while remaining cheap enough while staying fast enough while respecting user preferences.

This is the problem of multi-objective optimization, and ToolOrchestra's solution is both elegant and practical. This dive explains how to combine conflicting objectives into a single reward signal that trains genuinely useful behavior.

---

## 🌊 Surface Level: The Restaurant Menu Problem

Imagine choosing between restaurants. You care about three things: taste, price, and speed. The fancy restaurant serves amazing food but costs $100 and takes two hours. The fast food joint is cheap and instant but the food is mediocre. The neighborhood bistro balances all three moderately well.

Which is "best"? The answer depends on context. For a special anniversary, you might accept high cost and long wait for great taste. For a rushed lunch, you prioritize speed. On a tight budget, price dominates. There's no universally best option—only best given your current priorities.

Now consider an AI orchestrator choosing between:
- Call GPT-5: Likely accurate, expensive ($0.10/call), slow (3 seconds)
- Call local model: Possibly accurate, cheap ($0.001), fast (0.2 seconds)
- Call specialized model: Accurate for specific tasks, moderate cost ($0.01), moderate speed

The orchestrator faces the same problem as the restaurant chooser. There's no universally best tool—only best given the current task and user priorities. A researcher with grant funding might want maximum accuracy regardless of cost. A startup might need good-enough accuracy at minimal cost. A real-time application might prioritize speed above all else.

ToolOrchestra's reward design captures these trade-offs. It combines accuracy, cost, latency, and user preferences into a single number that the reinforcement learning algorithm can optimize. Different preference weightings lead to different optimal behaviors, allowing one trained model to serve users with different priorities.

---

## 🏊 Shallow Dive: The Three Objectives

ToolOrchestra's reward function combines three types of objectives, each capturing a different aspect of good orchestration.

### Objective 1: Outcome Reward

The most fundamental requirement is solving the task correctly. A trajectory that produces the wrong answer is not useful, no matter how efficiently it ran.

The outcome reward is binary for most benchmarks: either the answer matches the ground truth (reward = 1) or it doesn't (reward = 0). For some benchmarks, partial credit exists—HLE uses the paper's original scoring, FRAMES has degrees of correctness.

When ground truth isn't available (as in real deployment), ToolOrchestra uses an LLM-as-judge approach: GPT-5 evaluates whether the orchestrator's answer is correct. This introduces potential bias—GPT-5 might favor answers that look like GPT-5 generated them—but empirically works well enough for training.

**Why binary?** Continuous correctness rewards (like cosine similarity to the correct answer) can be gamed. The model might learn to produce outputs that score high on the proxy metric while being substantively wrong. Binary rewards are harder to game: either you got it right or you didn't.

### Objective 2: Efficiency Rewards

Even correct answers can be wasteful. Calling GPT-5 ten times when one call would suffice burns money and time without benefit. The efficiency rewards penalize this waste.

**Compute cost** is measured in dollars: the sum of all API call costs during the trajectory. Each call to GPT-5 costs approximately $0.03-0.10 depending on input/output length. Calls to smaller models cost $0.001-0.01. Local tools (search, code execution) are essentially free. The reward penalizes total cost: higher cost = lower reward component.

**Latency** is measured in seconds: the total time from task receipt to final answer. Sequential tool calls add up—a trajectory with 10 calls averaging 2 seconds each takes 20+ seconds. Parallel execution where possible reduces this, but the orchestrator's sequential nature limits parallelism. The reward penalizes total latency: longer = lower reward component.

**The trade-off is explicit.** A trajectory with 95% accuracy and $0.02 cost might be better than one with 98% accuracy and $0.10 cost, depending on the weights. The reward design lets these trade-offs be tuned rather than hard-coded.

### Objective 3: Preference Alignment

Different users have different priorities. A research organization might say "maximize accuracy, ignore cost." A startup might say "keep costs under $0.01 per query, accuracy can suffer." A real-time application might say "respond within 2 seconds no matter what."

The preference reward captures this through a **preference vector P**: a set of weights indicating how much the user cares about each dimension. The reward computes a dot product between normalized metrics and P, so trajectories that align with stated preferences score higher.

Consider two users analyzing the same trajectory:
- **User A (accuracy-focused, P = [1.0, 0.1, 0.1])**: Values the outcome reward 10x more than efficiency.
- **User B (cost-focused, P = [0.5, 1.0, 0.5])**: Values cost efficiency strongly, outcome moderately.

The same trajectory might score highly for User A (because it got the answer right, even at high cost) but poorly for User B (because the cost was high, even though the answer was right). Training on diverse preference vectors teaches the orchestrator to adapt its behavior to different prioritizations.

---

## 🤿 Deep Dive: The Mathematics of Multi-Objective Reward

### The Scalarization Approach

Multi-objective optimization traditionally handles conflicting objectives through **scalarization**: converting the multi-dimensional objective space into a single scalar value. The most common approach is linear scalarization—a weighted sum of objectives:

R(τ) = w₁ × Accuracy(τ) + w₂ × (−Cost(τ)) + w₃ × (−Latency(τ))

The weights determine relative importance. If w₁ is large, accuracy dominates. If w₂ is large, cost matters most.

**The problem with fixed weights** is that they build in a single preference. The trained model optimizes for that preference but cannot adapt to different users. ToolOrchestra addresses this by conditioning on a preference vector P that varies across training examples and at inference time.

### Normalization: Making Dimensions Comparable

Raw metrics have incompatible scales. Accuracy is between 0 and 1. Cost might be between $0.001 and $1.00. Latency might be between 0.1 and 100 seconds. A weighted sum of these raw values would be dominated by whichever has the largest magnitude, regardless of weights.

ToolOrchestra uses **batch normalization** within training batches. For each batch of rollouts, each metric is normalized to zero mean and unit variance:

M_normalized = (M_raw - μ_batch) / σ_batch

This puts all metrics on comparable scales. A trajectory one standard deviation better than average on accuracy contributes equally to reward as one that's one standard deviation better than average on cost—modulo the preference weights.

### The Complete Reward Formula

Putting together the pieces, ToolOrchestra's reward for a trajectory τ is:

R(τ) = (Outcome(τ) > threshold) × (M_normalized(τ) · P)

Breaking this down:
- **Outcome gate**: If the answer is wrong (Outcome < threshold), the whole reward is zero. No efficiency bonus for incorrect answers.
- **Metric vector M**: Contains normalized values for each dimension—tool-specific preferences, outcome quality, compute cost, latency.
- **Preference vector P**: User-specified weights indicating relative importance.
- **Dot product**: Computes alignment between the trajectory's metrics and the user's preferences.

The gating by correctness is crucial. Without it, the model might learn to produce fast, cheap, wrong answers when cost or latency preferences are high. The gate ensures that only correct trajectories contribute to learning—efficiency is a second-order consideration after accuracy.

### A Worked Example

Let's trace through a concrete example to see how rewards are computed.

**Task**: "What is the capital of Kyrgyzstan?"  
**User preference P**: [0.5 (accuracy), 0.8 (cost), 0.3 (latency)]  
**Rollouts in batch**:

| Rollout | Answer | Correct | Cost | Latency |
|---------|--------|---------|------|---------|
| A | Bishkek | Yes | $0.05 | 3.2s |
| B | Bishkek | Yes | $0.001 | 0.4s |
| C | Almaty | No | $0.002 | 0.3s |
| D | Bishkek | Yes | $0.10 | 5.1s |

**Step 1: Compute raw metrics**

Correct mask: [1, 1, 0, 1] (Rollout C is wrong)

**Step 2: Normalize within batch (correct rollouts only)**

Cost: mean = 0.050, std = 0.040  
Latency: mean = 2.9s, std = 1.94s

Normalized costs:
- A: (0.05 - 0.050) / 0.040 = 0.0
- B: (0.001 - 0.050) / 0.040 = −1.22 (better than average)
- D: (0.10 - 0.050) / 0.040 = +1.25 (worse than average)

Normalized latencies:
- A: (3.2 - 2.9) / 1.94 = +0.15 (slightly worse)
- B: (0.4 - 2.9) / 1.94 = −1.29 (better than average)
- D: (5.1 - 2.9) / 1.94 = +1.13 (worse than average)

**Step 3: Compute preference-weighted rewards**

R(A) = 0.5 × 1 + 0.8 × (−0.0) + 0.3 × (−0.15) = 0.5 − 0.045 = 0.455  
R(B) = 0.5 × 1 + 0.8 × (+1.22) + 0.3 × (+1.29) = 0.5 + 0.98 + 0.39 = **1.87** ⭐  
R(C) = 0 (wrong answer, gated out)  
R(D) = 0.5 × 1 + 0.8 × (−1.25) + 0.3 × (−1.13) = 0.5 − 1.0 − 0.34 = −0.84

**Result**: Rollout B (cheap, fast, correct) gets highest reward. Rollout D (expensive, slow, correct) gets lowest among correct answers. Rollout C (wrong) gets zero regardless of how efficient it was.

The gradient update will increase the probability of actions in Rollout B and decrease the probability of actions in Rollout D. Over many updates, the orchestrator learns that for this preference vector, cheap solutions are strongly preferred.

---

## 🔬 Research Depth: Pareto Optimality and Preference Learning

### The Pareto Frontier

Multi-objective optimization has a rich theory centered on **Pareto optimality**. A solution is Pareto-optimal if no objective can be improved without worsening another.

Consider all possible orchestration strategies plotted in accuracy-cost space:

```
Accuracy
100%|      + Pareto-optimal strategies
    |    +   (cannot improve one without hurting other)
 90%|  +   +
    |     +
 80%|   +   +
    |      +
 70%|       +
    +-----------+--------+--------
      $0.01   $0.05   $0.10   Cost
```

Points on the upper-left frontier are Pareto-optimal: you cannot improve accuracy without increasing cost, or reduce cost without sacrificing accuracy. Points away from the frontier are dominated—there's a better point that's both more accurate and cheaper.

**ToolOrchestra aims to learn strategies on the Pareto frontier.** Different preference vectors select different points on the frontier. High accuracy preference selects the upper-left corner (expensive but accurate). High cost preference selects the lower-right corner (cheap but less accurate). Intermediate preferences select points in between.

### Why Linear Scalarization Works (and When It Doesn't)

Linear scalarization (weighted sums) is mathematically guaranteed to find Pareto-optimal points—with one caveat. It can only find points on the **convex hull** of the Pareto frontier. If the frontier has concave regions, linear scalarization cannot reach points in those regions regardless of weight choices.

For ToolOrchestra's cost-accuracy trade-off, the frontier is likely convex: doubling accuracy doesn't require more than doubling cost. This makes linear scalarization reasonable. For other problems where the frontier might be concave, more sophisticated approaches (Chebyshev scalarization, constraint-based optimization) might be needed.

### Preference Learning: Could We Infer P?

ToolOrchestra assumes preference vectors are specified explicitly by users. But what if users can't articulate their preferences? What if they'd rather just approve or reject proposed solutions?

This connects to **inverse reinforcement learning** and **preference learning from comparisons**. Given user behavior (approvals, rejections, explicit comparisons), algorithms like Bradley-Terry or the methods behind RLHF can infer an underlying preference model.

ToolOrchestra doesn't implement this, but the architecture supports it. The preference-conditioned policy could be trained on inferred preferences just as well as stated ones. This is a natural extension for production systems where gathering explicit preference vectors might be impractical.

### Multi-Stakeholder Preferences

A final complication: in real deployments, multiple stakeholders may have conflicting preferences. The end user wants fast answers. The developer wants low costs. The organization wants compliance and safety. Society wants privacy preservation.

How should these be balanced? This is fundamentally a social choice question, not just a technical one. ToolOrchestra's preference vector could represent an aggregated preference, but who decides the aggregation weights?

Research on **multi-stakeholder AI** and **social choice for AI alignment** addresses these questions. ToolOrchestra's technical infrastructure—conditioning policy on explicit preference parameters—is compatible with whatever aggregation scheme is chosen. The hard questions are about governance, not optimization.

---

## Conclusion

Multi-objective reward design is what makes ToolOrchestra useful in practice. A system that only optimizes accuracy would be too expensive. A system that only optimizes cost would produce garbage. The combination—accuracy when it matters, efficiency when it suffices, aligned with user priorities—enables deployment across diverse contexts.

The key technical choices are: binary gating on correctness (don't reward efficient wrong answers), batch normalization (make dimensions comparable), and preference conditioning (allow runtime control over trade-offs). Together, these transform the messy multi-objective problem into a clean single-objective that reinforcement learning can handle.

The next dive examines where the training data comes from. Real orchestration data is scarce—how do you generate enough high-quality examples to train a robust orchestrator?

---

## References

### Multi-Objective Optimization

1. **Pareto Optimality in ML**
   - Sener, O., & Koltun, V. (2018). "Multi-Task Learning as Multi-Objective Optimization." *NeurIPS 2018*
   - https://arxiv.org/abs/1810.04650

2. **Scalarization Methods**
   - Miettinen, K. (1999). "Nonlinear Multiobjective Optimization." Springer
   - https://link.springer.com/book/10.1007/978-1-4615-5563-6

### Preference Learning

3. **Preference Learning Survey**
   - Fürnkranz, J., & Hüllermeier, E. (2010). "Preference Learning." Springer
   - https://link.springer.com/book/10.1007/978-3-642-14125-6

4. **Bradley-Terry Model**
   - Bradley, R.A., & Terry, M.E. (1952). "Rank Analysis of Incomplete Block Designs." *Biometrika*
   - https://www.jstor.org/stable/2334029

### Reward Design

5. **Reward Design in RL**
   - Hadfield-Menell, D., et al. (2017). "Inverse Reward Design." *NeurIPS 2017*
   - https://arxiv.org/abs/1711.02827

6. **Reward Hacking**
   - Skalse, J., et al. (2022). "Defining and Characterizing Reward Gaming." *NeurIPS 2022*
   - https://arxiv.org/abs/2209.13085

### Cost-Aware AI

7. **FrugalGPT**
   - Chen, Y., et al. (2024). "FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance." *arXiv:2305.05176*
   - https://arxiv.org/abs/2305.05176

8. **RouteLLM**
   - Ong, I., et al. (2024). "RouteLLM: Learning to Route LLMs with Preference Data." *arXiv:2406.18665*
   - https://arxiv.org/abs/2406.18665

---
