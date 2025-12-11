# Dive 3: Multi-Objective Reward Design
## Introduction

This part explains how ToolOrchestra turns several conflicting goals—accuracy, cost, latency, and user preferences—into a single learning signal. It walks through the reward design in increasing depth so you can see both the intuition and the precise math behind preference-aware orchestration.


## 🌊 Surface Level: Juggling Multiple Goals

**The challenge**: The orchestrator needs to be:
- Accurate (solve the problem correctly)
- Cheap (don't call expensive models unnecessarily)
- Fast (minimize latency)
- Aligned (follow user preferences)

These goals conflict! Being accurate might require expensive models. Being fast might sacrifice accuracy.

**ToolOrchestra's solution**: Create a single reward score that balances all these goals, weighted by user preferences.

## 🏊 Shallow Dive: The Three Reward Components

### Component 1: Outcome Reward (Did We Solve It?)

```python
r_outcome(trajectory) = 1 if correct else 0
```

**Simple, right?** Not quite. How do we check "correct"?

**Problem**: Answers come in many forms
- Mathematical: "4", "4.0", "4.00", "four"
- Names: "JFK", "John F. Kennedy", "President Kennedy"
- Dates: "1963-11-22", "November 22, 1963", "Nov 22, '63"

**Solution**: Use GPT-5 as a judge
- Give it the gold answer and the model's answer
- Ask: "Are these semantically equivalent?"
- This allows flexible matching while remaining reliable

**Limitation**: GPT-5 as judge isn't perfect. It can make mistakes, especially on:
- Numerical precision (is 3.14 equivalent to π?)
- Negations ("not X" vs. "X is false")
- Contextual meanings

### Component 2: Efficiency Rewards (How Much Did It Cost?)

Two sub-components:

**r_compute(trajectory) = -$(trajectory)**
- Sum up costs of all tool calls
- Proprietary models: Use published API pricing (GPT-5: $30/M input tokens)
- Open models: Use third-party hosting pricing for standardization

Example:
```
Turn 1: Call GPT-5 (1000 tokens in, 500 out) = $0.05
Turn 2: Call Qwen-32B (500 tokens in, 200 out) = $0.003
Turn 3: Call local search (0 external cost) = $0.0001
Total compute cost = $0.0531
r_compute = -0.0531
```

**r_latency(trajectory) = -Clock(trajectory)**
- Wall-clock time from start to finish
- Includes API call latency, model inference time, tool execution time

Example:
```
Turn 1: GPT-5 call = 3.2 seconds
Turn 2: Qwen-32B call = 1.5 seconds
Turn 3: Local search = 0.3 seconds
Total latency = 5.0 seconds
r_latency = -5.0
```

**Why negative rewards?** Because we want to minimize cost and latency. In RL, we maximize reward, so negative cost means "less cost = higher reward."

### Component 3: Preference Reward (Did We Follow User Wishes?)

This is the most innovative component.

**Idea**: Different users have different priorities
- Researcher: Wants accuracy, doesn't care about cost
- Startup: Wants cheap, can sacrifice some accuracy
- Real-time app: Wants fast, uses local models

**Implementation**: Let users specify preferences as a vector

```python
# Example preference vector
P = [
    p_web_search,      # How much user wants web search used
    p_local_search,    # How much user wants local search used
    p_GPT5,           # How much user wants GPT-5 used
    p_Qwen_32B,       # How much user wants Qwen-32B used
    # ... one entry per tool ...
    p_outcome,        # How much user cares about accuracy
    p_compute,        # How much user cares about cost
    p_latency         # How much user cares about speed
]
```

Each p_i ∈ [0, 1], where 1 = "strongly prefer" and 0 = "don't care"

**How it's computed**:

1. Track tool usage in trajectory:
```python
M_trajectory = [
    count(web_search_calls),
    count(local_search_calls),
    count(GPT5_calls),
    count(Qwen_32B_calls),
    # ... one entry per tool ...
    r_outcome,  # 0 or 1
    r_compute,  # negative cost
    r_latency   # negative time
]
```

2. Normalize across batch:
```python
M_normalized[i] = (M[i] - batch_min[i]) / (batch_max[i] - batch_min[i])
```

This puts everything on [0, 1] scale where 1 = "best in batch" and 0 = "worst in batch"

3. Dot product with preferences:
```python
preference_reward = M_normalized · P
```

This is just: sum of (normalized_metric × user_preference)

**Intuition**: If user wants fast (high p_latency) and trajectory is fastest in batch (normalized latency ≈ 1), that contributes positively to reward.

## 🤿 Deep Dive: The Mathematics of Multi-Objective Optimization

### Why Combining Rewards is Hard

In single-objective RL: R(s,a) → ℝ (one number)

In multi-objective RL: R(s,a) → ℝ^n (vector of numbers)

**Problem**: There's no single "best" solution. Instead, there's a **Pareto frontier** of solutions where you can't improve one objective without hurting another.

Example:
```
Trajectory A: 90% accurate, $1.00 cost
Trajectory B: 85% accurate, $0.50 cost
```

Which is better? Depends on user preferences!

### Scalarization: Converting Multi-Objective to Single-Objective

**Linear scalarization**: R_total = w_1 × R_1 + w_2 × R_2 + ... + w_n × R_n

Where w_i are weights representing importance.

**ToolOrchestra's approach** is a sophisticated form of scalarization:

```
R(τ) = M_τ^normalized · P  if solved, else 0
```

**The "if solved, else 0" part is crucial**:
- Only successful trajectories get positive reward
- Among successful trajectories, prefer those matching user preferences
- Unsuccessful trajectories get 0, regardless of cost/latency

This encodes: **Correctness is non-negotiable, then optimize for preferences**

### Normalization: Why It Matters

Without normalization:
```
Tool A: Called 10 times (large number)
Tool B: Called 2 times (small number)
Cost: $0.50 (medium number)
```

Dot product would be dominated by large numbers (tool A calls).

With normalization:
```
Tool A: 1.0 (most in batch)
Tool B: 0.2 (20% of max in batch)  
Cost: 0.5 (50% of max in batch)
```

All metrics contribute equally to the final reward.

**Technical detail**: Min-max normalization

```python
normalized_value = (value - min_in_batch) / (max_in_batch - min_in_batch)
```

**Edge case**: If max_in_batch == min_in_batch (all trajectories same), set to 0 (ignore this metric).

**Why this works**: 
- Puts all metrics on same [0,1] scale
- 1 = best in batch, 0 = worst in batch
- Relative comparison (like GRPO advantage)

### The Full Reward Computation (Step by Step)

Let's trace through a concrete example:

**Setup**:
- Batch of 4 rollouts for a task
- User preference: P = [0, 1, 0, 1, 1, 0.5, 0.2]
  - (Don't care about web search, want local search, don't want GPT-5, want Qwen-32B, want accuracy, somewhat care about cost, barely care about latency)

**Rollout 1**:
- Calls: [Web=1, Local=3, GPT5=0, Qwen=2]
- Outcome: Correct (r_outcome=1)
- Cost: $0.20 (r_compute=-0.20)
- Latency: 8s (r_latency=-8)

**Rollout 2**:
- Calls: [Web=0, Local=5, GPT5=1, Qwen=1]
- Outcome: Correct (r_outcome=1)
- Cost: $0.60 (r_compute=-0.60)
- Latency: 12s (r_latency=-12)

**Rollout 3**:
- Calls: [Web=2, Local=1, GPT5=0, Qwen=3]
- Outcome: Wrong (r_outcome=0)
- Cost: $0.30 (r_compute=-0.30)
- Latency: 10s (r_latency=-10)

**Rollout 4**:
- Calls: [Web=0, Local=4, GPT5=0, Qwen=2]
- Outcome: Correct (r_outcome=1)
- Cost: $0.15 (r_compute=-0.15)
- Latency: 7s (r_latency=-7)

**Step 1: Form M vectors**
```
M_1 = [1, 3, 0, 2, 1, -0.20, -8]
M_2 = [0, 5, 1, 1, 1, -0.60, -12]
M_3 = [2, 1, 0, 3, 0, -0.30, -10]
M_4 = [0, 4, 0, 2, 1, -0.15, -7]
```

**Step 2: Find min and max across batch**
```
min = [0, 1, 0, 1, 0, -0.60, -12]
max = [2, 5, 1, 3, 1, -0.15, -7]
range = [2, 4, 1, 2, 1, 0.45, 5]
```

**Step 3: Normalize each rollout**
```
M_1_norm = [
    (1-0)/2 = 0.5,     # Web calls
    (3-1)/4 = 0.5,     # Local calls
    (0-0)/1 = 0,       # GPT5 calls
    (2-1)/2 = 0.5,     # Qwen calls
    (1-0)/1 = 1,       # Outcome
    (-0.20-(-0.60))/0.45 = 0.89,  # Cost (less negative = cheaper = better)
    (-8-(-12))/5 = 0.8  # Latency (less negative = faster = better)
]

M_2_norm = [0, 1, 1, 0, 1, 0, 0]
M_3_norm = [1, 0, 0, 1, 0, 0.67, 0.4]
M_4_norm = [0, 0.75, 0, 0.5, 1, 1, 1]
```

**Step 4: Compute dot product with preferences**
```
P = [0, 1, 0, 1, 1, 0.5, 0.2]

R(τ_1) = [0.5, 0.5, 0, 0.5, 1, 0.89, 0.8] · [0, 1, 0, 1, 1, 0.5, 0.2]
       = 0×0 + 0.5×1 + 0×0 + 0.5×1 + 1×1 + 0.89×0.5 + 0.8×0.2
       = 0 + 0.5 + 0 + 0.5 + 1 + 0.445 + 0.16
       = 2.605

R(τ_2) = [0, 1, 1, 0, 1, 0, 0] · [0, 1, 0, 1, 1, 0.5, 0.2]
       = 0 + 1 + 0 + 0 + 1 + 0 + 0
       = 2.0

R(τ_3) = 0  (because outcome = 0, wrong answer)

R(τ_4) = [0, 0.75, 0, 0.5, 1, 1, 1] · [0, 1, 0, 1, 1, 0.5, 0.2]
       = 0 + 0.75 + 0 + 0.5 + 1 + 0.5 + 0.2
       = 2.95
```

**Interpretation**:
- Rollout 4 gets highest reward (2.95) - correct, cheap, fast, uses preferred tools
- Rollout 1 gets 2.605 - correct but not as well aligned with preferences
- Rollout 2 gets 2.0 - correct but expensive, slow, used GPT-5 (user didn't want)
- Rollout 3 gets 0 - wrong answer, doesn't matter how cheap it was

**Step 5: Compute GRPO advantages**
```
mean = (2.605 + 2.0 + 0 + 2.95) / 4 = 1.89
std = 1.20

A(τ_1) = (2.605 - 1.89) / 1.20 = 0.60
A(τ_2) = (2.0 - 1.89) / 1.20 = 0.09
A(τ_3) = (0 - 1.89) / 1.20 = -1.58
A(τ_4) = (2.95 - 1.89) / 1.20 = 0.88
```

**Training update**: 
- Increase probability of actions in rollout 4 (highest advantage)
- Slightly increase probability of actions in rollout 1
- Barely change rollout 2
- Decrease probability of actions in rollout 3

This teaches the orchestrator: "Do more stuff like rollout 4, less like rollout 3"

## 🔬 Research Depth: Pareto Optimality and Multi-Objective RL

### The Pareto Frontier

In multi-objective optimization, a solution is **Pareto optimal** if you can't improve any objective without worsening another.

**Example with 2 objectives (accuracy vs. cost)**:
```
Solutions on Pareto frontier:
A: 95% accurate, $1.00
B: 90% accurate, $0.50
C: 80% accurate, $0.20

Solutions NOT on frontier:
D: 90% accurate, $1.00  (B is better: same accuracy, lower cost)
E: 70% accurate, $0.30  (C is better: higher accuracy, similar cost)
```

**Visualization**:
```
Accuracy
100% |  A
 95% |  •
 90% |    B
 85% |    
 80% |      C
 75% |
 70% |        E ← Dominated
     |          D ← Dominated
     +-------------|-------|-------|
        $0.20   $0.50   $1.00   Cost
```

### Scalarization and Pareto Solutions

**Key theorem**: For any set of positive weights w_i, the solution that maximizes ∑ w_i × R_i is Pareto optimal.

**Intuition**: If there were a solution that improved all objectives, the weighted sum would increase.

**ToolOrchestra's approach**: User preferences define weights, so the trained policy learns to find Pareto-optimal solutions for different weight vectors.

### Limitations of Linear Scalarization

**Problem**: Linear scalarization can't find solutions in non-convex regions of the Pareto frontier.

**Example**: Suppose the Pareto frontier has a "dip":
```
Objective 2
    |    A     C
    |      \  /
    |       B     ← B is Pareto optimal but unreachable by linear scalarization
    |____________ Objective 1
```

**Why**: Linear combinations of A and C can never produce B.

**ToolOrchestra's mitigation**: The diverse tool configurations during training expose the model to varied trade-off landscapes, implicitly exploring different regions of the Pareto frontier.

### Connection to Multi-Task Learning

**Multi-task learning**: Train one model on multiple tasks simultaneously
- Challenge: Balancing gradients from different tasks
- Common solution: Weighted loss with task weights

**Multi-objective RL**: Train one policy for multiple objectives
- Challenge: Balancing rewards from different objectives
- ToolOrchestra solution: User-specified preference weights

**Research parallel**: 
- Multi-task learning: GradNorm (Chen et al., 2018) - automatically balance gradient magnitudes
- Multi-objective RL: Could we automatically balance reward scales instead of manual normalization?

### Open Research Questions

1. **Adaptive weights**: Current approach uses fixed user preferences. Could preferences adapt during trajectory based on how the problem unfolds?

2. **Pareto frontier approximation**: Could we train an ensemble of policies, each optimizing different points on the Pareto frontier, then select at test time?

3. **Constraint-based formulation**: Instead of scalarization, formulate as: Maximize accuracy subject to cost < $0.50, latency < 10s. This is **constrained RL**, an active research area.

4. **User preference learning**: Instead of explicit preference vectors, could we learn preferences from user behavior? This connects to **inverse RL** and **preference learning**.

---


## Conclusion

By the end of this part, the idea of "multi-objective reward" should feel concrete rather than abstract: correctness is treated as non-negotiable, and within the successful trajectories the model is nudged toward cost-, latency-, and preference-aware behavior. That framing carries forward into the empirical results, where improvements are measured not just in raw accuracy but in cost-effectiveness and controllability.

## Academic Papers

35. **Multi-Objective Reinforcement Learning Survey**
    - Roijers, D.M., Vamplew, P., Whiteson, S., & Dazeley, R. (2013). "A Survey of Multi-Objective Sequential Decision-Making." *Journal of Artificial Intelligence Research*, 48, 67-113
    - https://www.jair.org/index.php/jair/article/view/10806

36. **Pareto Optimality in RL**
    - Van Moffaert, K., & Nowé, A. (2014). "Multi-objective Reinforcement Learning using Sets of Pareto Dominating Policies." *Journal of Machine Learning Research*, 15(107), 3483-3512
    - https://www.jmrl.org/papers/v15/vanmoffaert14a.html

37. **Scalarization Methods**
    - Roijers, D.M., & Whiteson, S. (2017). "Multi-Objective Decision Making." *Synthesis Lectures on Artificial Intelligence and Machine Learning*
    - https://www.morganclaypool.com/doi/abs/10.2200/S00765ED1V01Y201704AIM034

38. **Preference Learning**
    - Wirth, C., Akrour, R., Neumann, G., & Fürnkranz, J. (2017). "A Survey of Preference-Based Reinforcement Learning Methods." *Journal of Machine Learning Research*, 18(136), 1-46
    - https://www.jmrl.org/papers/v18/16-634.html

39. **RLHF (Reinforcement Learning from Human Feedback)**
    - Christiano, P.F., Leike, J., Brown, T.B., et al. (2017). "Deep Reinforcement Learning from Human Preferences." *NIPS 2017*
    - https://arxiv.org/abs/1706.03741

40. **DPO (Direct Preference Optimization)**
    - Rafailov, R., Sharma, A., Mitchell, E., et al. (2024). "Direct Preference Optimization: Your Language Model is Secretly a Reward Model." *NeurIPS 2024*
    - https://arxiv.org/abs/2305.18290

41. **Constitutional AI**
    - Bai, Y., Kadavath, S., Kundu, S., et al. (2022). "Constitutional AI: Harmlessness from AI Feedback." *arXiv:2212.08073*
    - https://arxiv.org/abs/2212.08073

42. **Multi-Objective Optimization in AI**
    - Deb, K., Pratap, A., Agarwal, S., & Meyarivan, T. (2002). "A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II." *IEEE Transactions on Evolutionary Computation*
    - https://ieeexplore.ieee.org/document/996017

43. **Reward Shaping**
    - Ng, A.Y., Harada, D., & Russell, S. (1999). "Policy Invariance Under Reward Transformations: Theory and Application to Reward Shaping." *ICML 1999*
    - http://www.robotics.stanford.edu/~ang/papers/shaping-icml99.pdf

## Blog Posts and Tutorials

44. **Pareto Efficiency Explained**
    - "Understanding Pareto Optimality in Multi-Objective Optimization"
    - https://towardsdatascience.com/pareto-optimality-in-multi-objective-optimization-3d2e8b5d2b5d

45. **RLHF Deep Dive**
    - Chip Huyen. "RLHF: Reinforcement Learning from Human Feedback"
    - https://huyenchip.com/2023/05/02/rlhf.html

46. **Anthropic's RLHF Process**
    - "Training a Helpful and Harmless Assistant with RLHF"
    - https://www.anthropic.com/index/training-a-helpful-and-harmless-assistant-with-reinforcement-learning-from-human-feedback

47. **DPO vs RLHF**
    - Hugging Face Blog. "Preference Tuning LLMs with Direct Preference Optimization"
    - https://huggingface.co/blog/dpo-trl

48. **Multi-Objective Optimization Tutorial**
    - "Multi-Objective Optimization: A Tutorial"
    - https://machinelearningmastery.com/multi-objective-optimization-with-python/

49. **Reward Design Best Practices**
    - DeepMind. "Specification Gaming: The Flip Side of AI Ingenuity"
    - https://www.deepmind.com/blog/specification-gaming-the-flip-side-of-ai-ingenuity

## GitHub Repositories

50. **MORL-Baselines**
    - Multi-Objective RL implementations
    - https://github.com/LucasAlegre/morl-baselines

51. **TRL with Preference Learning**
    - https://github.com/huggingface/trl/tree/main/examples/research_projects/stack_llama_2

52. **Reward Modeling Code**
    - OpenAssistant Reward Model
    - https://github.com/LAION-AI/Open-Assistant

53. **DPO Implementation**
    - https://github.com/eric-mitchell/direct-preference-optimization

54. **Pareto Frontier Visualization**
    - https://github.com/pchtsp/pareto

## Tools and Libraries

55. **Pymoo: Multi-Objective Optimization**
    - https://pymoo.org/

56. **Platypus: Multi-Objective Optimization Library**
    - https://github.com/Project-Platypus/Platypus

---

