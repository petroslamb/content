# Dive 8: Preference Learning and User Alignment
## Introduction

This part is about preferences and alignment: how different users can want different trade-offs, and how an orchestrator can adapt without retraining from scratch. It walks through the mechanism that lets ToolOrchestra condition its behavior on explicit or implicit user priorities.


## 🌊 Surface Level: Different Users, Different Needs

**The insight**: No single "best" way to solve a task.

**User A (Researcher)**:
- Priority: Accuracy
- Cost: Doesn't matter (grant funded)
- Preference: "Use best models, I don't care about cost"

**User B (Startup)**:
- Priority: Cost-effectiveness
- Accuracy: Good enough is fine
- Preference: "Stay under budget, 80% accuracy is fine"

**User C (Real-time App)**:
- Priority: Speed
- Cost: Moderate constraint
- Preference: "Answer within 2 seconds, use local models"

**ToolOrchestra's innovation**: One model adapts to all three!

## 🏊 Shallow Dive: The Preference Mechanism

### Specifying Preferences

**Input**: Preference vector P
```python
P = [
    # Tool preferences (0 = avoid, 1 = prefer)
    p_web_search,      # 0.5 (neutral)
    p_local_search,    # 1.0 (prefer - privacy)
    p_code_interpreter, # 1.0 (prefer - free)
    p_GPT5,           # 0.0 (avoid - expensive)
    p_GPT5_mini,      # 0.7 (okay - cheaper)
    p_Qwen_32B,       # 0.9 (prefer - good and cheap)
    p_Math_72B,       # 0.8 (prefer for math)
    
    # Objective preferences
    p_outcome,        # 1.0 (always want correctness)
    p_compute,        # 0.8 (care about cost)
    p_latency         # 0.3 (don't care much about speed)
]
```

**Natural language version** (what user actually says):
```
"I want accurate answers, but please be cost-conscious. 
Use local search when possible for privacy. 
I don't mind waiting a bit longer."
```

**Conversion** (LLM generates P from natural language):
```python
def nl_to_preference_vector(user_instruction, available_tools):
    prompt = f"""
    User said: "{user_instruction}"
    Available tools: {available_tools}
    
    Convert to preference vector where:
    - 1.0 = strongly prefer
    - 0.5 = neutral
    - 0.0 = avoid if possible
    
    Output JSON with preference for each tool and objective.
    """
    
    vector_json = llm(prompt)
    return parse_preference_vector(vector_json)
```

### How Preferences Affect Behavior

**Example task**: "What is the capital of Kyrgyzstan?"

**Preference Set 1** (Accuracy-focused):
```python
P = [0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 0.2, 0.1]
# Prefers GPT-5, cares about accuracy, ignores cost
```

**Model behavior**:
```
Turn 1: Call GPT-5("What is the capital of Kyrgyzstan?")
Result: "Bishkek"
Done!

Cost: $0.03
Reward: High (used preferred tool, correct answer)
```

**Preference Set 2** (Cost-focused):
```python
P = [1.0, 1.0, 1.0, 0.0, 0.5, 0.9, 1.0, 0.9, 0.1]
# Avoids GPT-5, prefers cheap tools, cares about cost
```

**Model behavior**:
```
Turn 1: Call local_search("capital of Kyrgyzstan")
Result: "Bishkek (formerly Frunze)"
Done!

Cost: $0.0001
Reward: High (used preferred tool, correct, cheap)
```

**Both solve the task, but differently based on preferences!**

### Learning to Respect Preferences

**During training**, model sees diverse preference vectors:

**Training example 1**:
```python
Task: "Calculate 123 × 456"
Preference: [high_cost_sensitivity]

Model tries:
- Rollout A: Call GPT-5 → Correct → Reward: 0.8 (correct but expensive)
- Rollout B: Call code_interpreter → Correct → Reward: 1.5 (correct and cheap)

Update: Increase probability of Rollout B behavior
```

**Training example 2**:
```python
Task: "Prove Fermat's Last Theorem"
Preference: [high_cost_sensitivity]

Model tries:
- Rollout A: Call code_interpreter → Wrong → Reward: 0 (incorrect)
- Rollout B: Call GPT-5 → Correct → Reward: 1.2 (correct, worth the cost)

Update: Increase probability of Rollout B behavior
```

**What model learns**:
- For simple tasks: Cheap tools satisfy cost-sensitive preferences
- For hard tasks: Expensive tools necessary even with cost-sensitive preferences
- Trade-off depends on task difficulty

## 🤿 Deep Dive: The Mathematics of Preference Alignment

### Formalizing User Preferences

**Multi-objective optimization framework**:

**User utility function** (what user actually cares about):
```
U(τ) = w_accuracy × accuracy(τ) 
       - w_cost × cost(τ) 
       - w_latency × latency(τ)
       + w_privacy × privacy(τ)
       + ...
```

Where w_i are user-specific weights.

**Problem**: User doesn't know exact weights!
- User can say "I care more about cost than latency"
- But can't quantify "how much more"

**ToolOrchestra's solution**: Preference vector as proxy for weights
```
P[i] ∈ [0,1] represents strength of preference
Not exact weights, but relative importance
```

**Reward computation**:
```
R(τ) = M_τ^normalized · P
```

This approximates user utility through linear scalarization.

### Why Normalization is Critical

**Without normalization**, preferences don't work:

**Example**:
```python
Trajectory A:
- GPT5 calls: 1
- Local search calls: 10
- Cost: $0.10

Trajectory B:
- GPT5 calls: 0
- Local search calls: 5
- Cost: $0.05

Preference: [p_GPT5=0, p_local=1, p_cost=1]
# User wants: avoid GPT5, use local search, be cheap

# Without normalization:
R(A) = 0×1 + 1×10 + 1×(-0.10) = 9.9
R(B) = 0×0 + 1×5 + 1×(-0.05) = 4.95

# A gets higher reward despite using GPT5!
# Because 10 local calls >> $0.10 cost difference
```

**With normalization** (within batch):
```python
Batch: [Trajectory A, Trajectory B, ...]

# Normalize each metric to [0,1]
M_A_norm = [(1-0)/(1-0), (10-5)/(10-5), (0.10-0.05)/(0.10-0.05)]
         = [1.0, 1.0, 1.0]

M_B_norm = [(0-0)/(1-0), (5-5)/(10-5), (0.05-0.05)/(0.10-0.05)]
         = [0.0, 0.0, 0.0]

# With preferences [p_GPT5=0, p_local=1, p_cost=1]:
# (Note: cost is inverted - lower cost = higher normalized value)

M_A_norm (corrected) = [1.0, 1.0, 0.0]  # worst cost
M_B_norm (corrected) = [0.0, 0.0, 1.0]  # best cost

R(A) = 0×1.0 + 1×1.0 + 1×0.0 = 1.0
R(B) = 0×0.0 + 1×0.0 + 1×1.0 = 1.0

# Now they're equal, need more rollouts to differentiate
```

Normalization ensures all metrics contribute on equal scale.

### Preference Generalization

**Training distribution**: Randomly sampled preference vectors

**Test time**: User provides specific preference

**Question**: Does training generalize to arbitrary test preferences?

**Theoretical perspective** (from multi-task learning):

If training preferences are **dense** in preference space:
```
Preference space: P ∈ [0,1]^n
Training coverage: Sample uniformly
Result: Model learns smooth function from P to behavior
Generalization: Interpolation between training preferences
```

**ToolOrchestra's approach**:
- Generate diverse (P, task) pairs
- Each task gets multiple preference vectors
- Covers preference space reasonably well

**Empirical evidence**:
- Table 3 shows 46.7 score on preference-aware eval
- GPT-5 gets only 34.6
- Suggests model learned to follow preferences, not memorize specific P vectors

### The Pareto Frontier Revisited

**Connection to preferences**:

Different preferences = different points on Pareto frontier

**Visualization**:
```
Accuracy
100%|
    |    P1: [p_accuracy=1, p_cost=0]
 90%|    • ← Selects high-accuracy, high-cost point
    |     \
 80%|      • ← P2: [p_accuracy=0.7, p_cost=0.3]
    |       \
 70%|        • ← P3: [p_accuracy=0.5, p_cost=0.5]
    |         \
 60%|          • ← P4: [p_accuracy=0.3, p_cost=0.7]
    |           \
 50%|            • ← P5: [p_accuracy=0, p_cost=1]
    +-------------|-------|-------|
      $1.00    $0.50   $0.10   Cost
```

**ToolOrchestra learns to trace the Pareto frontier**:
- Different P vectors → Different points selected
- Model learns implicit trade-off function
- Can approximate any point by setting P appropriately

**Limitation**: Can only reach Pareto-optimal points
- Sub-optimal points (inside frontier) aren't reachable
- This is actually good! (We want optimal solutions)

## 🔬 Research Depth: Inverse RL and Preference Learning

### Connection to Inverse Reinforcement Learning

**Inverse RL**: Learn reward function from demonstrations

**Standard RL**: Given R, learn π
**Inverse RL**: Given π (demonstrations), learn R

**ToolOrchestra hybrid approach**:
- Start with base reward (accuracy)
- Add preference-based modulation (P · M)
- This is partial inverse RL

**Full inverse RL for tools** (future direction):
```python
# Collect user demonstrations
demonstrations = [
    (task_1, trajectory_1),  # User's solution
    (task_2, trajectory_2),
    ...
]

# Infer user's reward function
R_user = inverse_rl_algorithm(demonstrations)

# Use inferred reward for RL
train_orchestrator(R_user)
```

**Benefits**:
- Learns from user behavior, not explicit preferences
- Captures implicit preferences user can't articulate
- Personalizes to individual users

**Challenges**:
- Requires many demonstrations (expensive)
- Demonstrations must be expert-quality
- Reward function may not be recoverable (ill-posed problem)

### Preference Learning from Comparisons

**Alternative approach**: Learn from pairwise comparisons

**Setup**:
```python
# Show user two solutions
solution_A = orchestrator.solve(task, preference=P_A)
solution_B = orchestrator.solve(task, preference=P_B)

# User picks preferred solution
user_preference = which_is_better(solution_A, solution_B)
# User: "I prefer B because it was faster"
```

**Bradley-Terry model** for preference learning:
```
P(A ≻ B) = exp(R(A)) / (exp(R(A)) + exp(R(B)))
```

**Train reward model to match preferences**:
```python
def train_reward_model(comparisons):
    reward_model = initialize_model()
    
    for (solution_A, solution_B, preference) in comparisons:
        # Compute probability under current model
        r_A = reward_model(solution_A)
        r_B = reward_model(solution_B)
        p_A_preferred = sigmoid(r_A - r_B)
        
        # Loss: Match user's actual preference
        if preference == "A":
            loss = -log(p_A_preferred)
        else:
            loss = -log(1 - p_A_preferred)
        
        # Update reward model
        reward_model.update(loss)
    
    return reward_model
```

**Then use learned reward for RL**:
```python
# Generate trajectories
trajectories = orchestrator.rollout(task)

# Score with learned reward model
rewards = [reward_model(τ) for τ in trajectories]

# GRPO update
update_orchestrator(trajectories, rewards)
```

**This is how ChatGPT was trained!** (RLHF)
- Collect human preference comparisons
- Train reward model
- Use reward model for RL

**ToolOrchestra could extend to this**:
- Current: Explicit preference vectors
- Future: Learned preference models from user feedback
- Benefit: More accurate alignment, captures nuanced preferences

### Multi-Stakeholder Preferences

**Real-world complication**: Multiple stakeholders with different preferences

**Example**:
- **User**: Wants fast answers
- **Developer**: Wants low cost (infrastructure)
- **Society**: Wants privacy-preserving (no data leakage)

**How to balance?**

**Approach 1: Weighted combination**
```python
P_combined = w_user × P_user + w_dev × P_dev + w_society × P_society
```

Who sets weights? How to decide?

**Approach 2: Constraints**
```python
# Optimize user utility subject to constraints
maximize: user_utility(τ)
subject to:
    cost(τ) < developer_budget
    privacy_score(τ) > society_threshold
```

This is **constrained RL**.

**Approach 3: Social choice theory**
- Stakeholders vote on solutions
- Aggregation function (e.g., Condorcet)
- Policy trained to satisfy aggregated preferences

**Open research area**: Multi-stakeholder RL for AI systems
- Relevant to: AI governance, alignment
- ToolOrchestra provides technical foundation

---


## Conclusion

The key conclusion from this part is that preferences don’t have to be an afterthought bolted onto an otherwise fixed policy. By baking them directly into the reward and training loop, ToolOrchestra learns to trace out different points on the accuracy–cost–latency frontier and to adapt behavior to different users, which is essential for real-world deployment.

## Academic Papers

150. **Bradley-Terry Model**
     - Bradley, R.A., & Terry, M.E. (1952). "Rank Analysis of Incomplete Block Designs: I. The Method of Paired Comparisons." *Biometrika*
     - https://www.jstor.org/stable/2334029

151. **Inverse Reinforcement Learning**
     - Abbeel, P., & Ng, A.Y. (2004). "Apprenticeship Learning via Inverse Reinforcement Learning." *ICML 2004*
     - https://ai.stanford.edu/~ang/papers/icml04-apprentice.pdf

152. **Maximum Entropy IRL**
     - Ziebart, B.D., et al. (2008). "Maximum Entropy Inverse Reinforcement Learning." *AAAI 2008*
     - https://www.aaai.org/Papers/AAAI/2008/AAAI08-227.pdf

153. **RLHF Detailed**
     - Ouyang, L., et al. (2022). "Training Language Models to Follow Instructions with Human Feedback." *NeurIPS 2022*
     - https://arxiv.org/abs/2203.02155

154. **InstructGPT**
     - Same as above (Ouyang et al.)

155. **Reward Model Training**
     - Stiennon, N., et al. (2020). "Learning to Summarize from Human Feedback." *NeurIPS 2020*
     - https://arxiv.org/abs/2009.01325

156. **DPO Mathematical Analysis**
     - Rafailov, R., et al. (2024). "Direct Preference Optimization: Your Language Model is Secretly a Reward Model." *NeurIPS 2024*
     - https://arxiv.org/abs/2305.18290

157. **KTO (Kahneman-Tversky Optimization)**
     - Ethayarajh, K., et al. (2024). "KTO: Model Alignment as Prospect Theoretic Optimization." *arXiv:2402.01306*
     - https://arxiv.org/abs/2402.01306

158. **Personalized RLHF**
     - Jang, J., et al. (2023). "Personalized Soups: Personalized Large Language Model Alignment via Post-hoc Parameter Merging." *arXiv:2310.11564*
     - https://arxiv.org/abs/2310.11564

159. **Social Choice Theory in AI**
     - Conitzer, V., et al. (2024). "Social Choice for AI Alignment." *AAAI 2024*
     - https://arxiv.org/abs/2310.20427

## Blog Posts and Tutorials

160. **RLHF Implementation Guide**
     - "Illustrating Reinforcement Learning from Human Feedback"
     - https://huggingface.co/blog/rlhf

161. **DPO Tutorial**
     - "Fine-tuning with Direct Preference Optimization"
     - https://huggingface.co/blog/dpo-trl

162. **Preference Learning Overview**
     - "Learning from Human Preferences"
     - https://openai.com/research/learning-from-human-preferences

163. **Constitutional AI Explained**
     - "Constitutional AI: Harmlessness from AI Feedback"
     - https://www.anthropic.com/index/constitutional-ai-harmlessness-from-ai-feedback

164. **Multi-Stakeholder AI**
     - "Whose Values Should AI Align With?"
     - https://www.alignmentforum.org/posts/

## GitHub Repositories

165. **TRL (Transformer Reinforcement Learning)**
     - Full RLHF pipeline
     - https://github.com/huggingface/trl

166. **Open Assistant**
     - Open-source ChatGPT alternative with RLHF
     - https://github.com/LAION-AI/Open-Assistant

167. **DPO Trainer**
     - https://github.com/huggingface/trl/tree/main/examples/research_projects/stack_llama_2

168. **RewardBench**
     - Benchmark for reward models
     - https://github.com/allenai/reward-bench

169. **Preference Dataset Collection**
     - Anthropic HH-RLHF dataset
     - https://github.com/anthropics/hh-rlhf

---

