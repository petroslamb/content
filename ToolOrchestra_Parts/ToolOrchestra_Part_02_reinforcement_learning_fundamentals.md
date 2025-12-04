# Dive 2: Reinforcement Learning Fundamentals
## Introduction

This part gives the reinforcement learning foundations you need to understand how ToolOrchestra is actually trained. It connects familiar ideas like states, actions, rewards, and policies to the concrete setting of an orchestrator that interacts with tools over many turns.


## 🌊 Surface Level: What is Reinforcement Learning?

**Simple analogy**: Training a dog.
- Dog does something (action)
- You say "good dog!" or "bad dog!" (reward)
- Dog learns which actions lead to treats

**In ToolOrchestra**:
- Orchestrator tries different tool combinations (actions)
- Gets reward based on: Did it solve the problem? How much did it cost? Did it match user preferences?
- Learns which tool combinations work for which problems

## 🏊 Shallow Dive: The RL Framework (MDPs)

### Markov Decision Processes: The Math of Decisions

An MDP is a framework for sequential decision-making with five components:

**1. States (S)**: Where you are
- In ToolOrchestra: The conversation history so far
- Example: "User asked a math question. I called local search. It returned a definition of 'Alon-Tarsi number'."

**2. Actions (A)**: What you can do
- In ToolOrchestra: Call web search, call GPT-5, call math model, respond directly
- Example: "Call Qwen2.5-Math-7B with parameter: 'Calculate the Alon-Tarsi number of K_{1000,1000}'"

**3. Transitions (T)**: How states change based on actions
- In ToolOrchestra: Deterministic—if you call a tool, you get its response
- Example: Call code interpreter → Get code execution result

**4. Observations (O)**: What you see about the state
- In ToolOrchestra: Partially observable—you see tool responses but not the user's full intent
- Example: User says "solve this quickly"—are they okay with expensive tools?

**5. Rewards (R)**: How good was the outcome
- In ToolOrchestra: Multi-dimensional (accuracy, cost, latency, preferences)
- Example: Correct answer (+1), but expensive (-0.5), but user said "be thorough" (+0.3)

### The Markov Property: Why It's Called "Markov"

**Markov property**: The future depends only on the present, not the past.

Formally: P(s_{t+1} | s_t, a_t) = P(s_{t+1} | s_t, a_t, s_{t-1}, a_{t-1}, ...)

**In plain English**: If you know the current state, knowing the history doesn't give you more information.

**In ToolOrchestra**: The conversation history IS the state, so this is satisfied. The orchestrator doesn't need to remember how it got to the current conversation—the conversation itself contains all relevant information.

**Why this matters**: Markov property allows us to use dynamic programming and many RL algorithms that wouldn't work otherwise.

## 🤿 Deep Dive: Policy Gradient Methods and GRPO

### What is a Policy?

A policy π is a mapping from states to actions: π(a|s)

**Deterministic policy**: π(s) = a (always choose the same action in a given state)
**Stochastic policy**: π(a|s) = probability of choosing action a in state s

In language models, the policy IS the model:
```
π_θ(a|s) = P(next_token | context)
```

Where θ represents all the model's parameters (billions of numbers).

### Policy Gradient Methods: Optimizing Directly

**Key idea**: Instead of learning value functions (how good is each state), directly optimize the policy to maximize expected reward.

The **policy gradient theorem** (Sutton et al., 2000):
```
∇_θ J(θ) = E[∇_θ log π_θ(a|s) × A(s,a)]
```

**In English**: To improve the policy, increase the probability of actions that have positive advantage (better than average) and decrease probability of actions with negative advantage.

**Why this works for LLMs**: Language models already output probability distributions. We just need to adjust these probabilities based on which completions got high rewards.

### GRPO: Group Relative Policy Optimization

**Standard policy gradient problem**: Individual reward values vary wildly.
- Task 1: Reward = 0.5 (easy task, solved okay)
- Task 2: Reward = 0.5 (hard task, solved brilliantly)

These shouldn't be treated the same!

**GRPO solution**: For each task, generate multiple rollouts. Compare rollouts to each other, not to absolute scale.

```python
# Pseudocode for GRPO advantage calculation
def compute_advantage(rollouts_for_same_task):
    rewards = [R(rollout) for rollout in rollouts_for_same_task]
    mean_reward = mean(rewards)
    std_reward = std(rewards)
    
    advantages = []
    for reward in rewards:
        advantage = (reward - mean_reward) / std_reward
        advantages.append(advantage)
    
    return advantages
```

**Why this helps**:
1. **Automatic scaling**: Easy and hard tasks have advantages in the same range
2. **Relative comparison**: "Better than other attempts" is more meaningful than "good in absolute terms"
3. **Stability**: Normalization prevents reward scale from causing training instability

### The Full GRPO Update

Here's what actually happens during training:

**Step 1: Generate batch of tasks** (e.g., 32 math problems)

**Step 2: For each task, generate K rollouts** (e.g., 4 attempts per task)
```
Task 1: [Rollout 1.1, Rollout 1.2, Rollout 1.3, Rollout 1.4]
Task 2: [Rollout 2.1, Rollout 2.2, Rollout 2.3, Rollout 2.4]
...
```

**Step 3: Compute rewards for each rollout**
```python
R(rollout) = (
    r_outcome(rollout) × M_normalized · P
    if solved else 0
)
```

**Step 4: Compute advantages within each group**
```python
A(rollout 1.2) = (R(1.2) - mean(R(1.1), R(1.2), R(1.3), R(1.4))) / std(...)
```

**Step 5: Update policy using clipped objective**
```python
ratio = π_new(rollout) / π_old(rollout)  # How much did policy change?
clipped_ratio = clip(ratio, 1-ε, 1+ε)    # Don't change too much!

loss = -min(
    ratio × advantage,
    clipped_ratio × advantage
)
```

**The clipping is crucial**: Prevents the policy from changing too drastically in one update, which would cause instability.

## 🔬 Research Depth: Why GRPO over PPO, REINFORCE, or A3C?

### GRPO vs. PPO (Proximal Policy Optimization)

**PPO** (Schulman et al., 2017):
- Uses value function V(s) to estimate advantages
- Requires training both policy network and value network
- Advantage: A(s,a) = R(s,a) + γV(s') - V(s)

**GRPO**:
- No value function needed
- Advantages computed from group statistics
- Simpler: Only one network to train (the policy)

**Why GRPO for ToolOrchestra**:
1. **Efficiency**: Training value functions for long trajectories (50 turns) is hard
2. **Simplicity**: Fewer hyperparameters, easier to tune
3. **Natural fit**: When you have multiple rollouts per task anyway (for exploration), group comparison is natural

### GRPO vs. REINFORCE with Baseline

**REINFORCE** (Williams, 1992):
- Vanilla policy gradient: ∇J = E[∇log π(a|s) × R]
- High variance (some trajectories much better than others)
- Baseline improvement: ∇J = E[∝log π(a|s) × (R - b)]

**GRPO** can be seen as REINFORCE where baseline b is the group mean:
- b = mean reward across rollouts for same task
- Plus normalization by std for scale-invariance

**Advantage of GRPO**: The baseline is adaptive per task, automatically adjusting to task difficulty.

### Connection to Relative Reward Methods

**Key insight**: Absolute reward values are often meaningless. What matters is relative performance.

This connects to:
1. **DPO (Direct Preference Optimization)**: Learns from pairwise preferences, not absolute rewards
2. **RLHF (Reinforcement Learning from Human Feedback)**: Often uses relative rankings
3. **Self-Play in games**: Agent improves by beating previous versions, not by absolute score

**GRPO formalizes this** for multi-rollout settings where you have multiple attempts at the same task.

### Open Question: Sample Efficiency

**Current limitation**: GRPO requires multiple rollouts per task for good advantage estimates.
- ToolOrchestra uses 4 rollouts per task
- For 50-turn trajectories with expensive API calls, this gets pricey

**Research direction**: Could we use a small value network as a critic to get advantages from single rollouts? This would be a hybrid:
- GRPO's group normalization for stability
- PPO's value function for sample efficiency

**Challenge**: Value functions for 50-turn trajectories are hard to train (credit assignment problem—which early action led to eventual success?).

---


## Conclusion

Taken together, the material in this part should make it natural to view ToolOrchestra as an RL agent acting in a partially observable environment with long trajectories and structured rewards. With that foundation, the choice of GRPO and the specific training setup in later parts becomes a design decision you can actually reason about, rather than a black box.

## Academic Papers

15. **Markov Decision Processes**
    - Sutton, R.S., & Barto, A.G. (2018). "Reinforcement Learning: An Introduction" (2nd ed.). *MIT Press*
    - http://incompleteideas.net/book/the-book-2nd.html

16. **Policy Gradient Theorem**
    - Sutton, R.S., McAllester, D., Singh, S., & Mansour, Y. (2000). "Policy Gradient Methods for Reinforcement Learning with Function Approximation." *NIPS 2000*
    - https://proceedings.neurips.cc/paper/2000/file/4b86abe48d358ecf194c56c69108433e-Paper.pdf

17. **GRPO (Group Relative Policy Optimization)**
    - Shao, Z., Wang, P., Zhu, Q., et al. (2024). "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models." *arXiv:2402.03300*
    - https://arxiv.org/abs/2402.03300

18. **PPO (Proximal Policy Optimization)**
    - Schulman, J., Wolski, F., Dhariwal, P., et al. (2017). "Proximal Policy Optimization Algorithms." *arXiv:1707.06347*
    - https://arxiv.org/abs/1707.06347

19. **REINFORCE Algorithm**
    - Williams, R.J. (1992). "Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning." *Machine Learning*, 8(3-4), 229-256
    - https://link.springer.com/article/10.1007/BF00992696

20. **Actor-Critic Methods**
    - Mnih, V., Badia, A.P., Mirza, M., et al. (2016). "Asynchronous Methods for Deep Reinforcement Learning." *ICML 2016*
    - https://arxiv.org/abs/1602.01783

21. **Trust Region Policy Optimization (TRPO)**
    - Schulman, J., Levine, S., Abbeel, P., et al. (2015). "Trust Region Policy Optimization." *ICML 2015*
    - https://arxiv.org/abs/1502.05477

22. **Advantage Function Estimation**
    - Schulman, J., Moritz, P., Levine, S., et al. (2016). "High-Dimensional Continuous Control Using Generalized Advantage Estimation." *ICLR 2016*
    - https://arxiv.org/abs/1506.02438

## Blog Posts and Tutorials

23. **RL Fundamentals Tutorial**
    - OpenAI Spinning Up in Deep RL
    - https://spinningup.openai.com/en/latest/

24. **Policy Gradient Methods Explained**
    - Lilian Weng's Blog. "Policy Gradient Algorithms"
    - https://lilianweng.github.io/posts/2018-04-08-policy-gradient/

25. **PPO Explained**
    - Hugging Face Deep RL Course. "Proximal Policy Optimization"
    - https://huggingface.co/learn/deep-rl-course/unit8/introduction

26. **Advantage Functions Visual Guide**
    - "The Advantage Function in Reinforcement Learning Explained"
    - https://towardsdatascience.com/understanding-advantage-functions-in-reinforcement-learning-8f7c8de94cf8

27. **RL for LLMs**
    - Nathan Lambert. "RLHF: Reinforcement Learning from Human Feedback"
    - https://huyenchip.com/2023/05/02/rlhf.html

## GitHub Repositories

28. **CleanRL: Clean RL Implementations**
    - https://github.com/vwxyzjn/cleanrl

29. **Stable Baselines3 (PPO Implementation)**
    - https://github.com/DLR-RM/stable-baselines3

30. **TRL: Transformer Reinforcement Learning**
    - Hugging Face TRL library
    - https://github.com/huggingface/trl

31. **DeepSeek-Math Code**
    - https://github.com/deepseek-ai/DeepSeek-Math

32. **OpenAI Baselines**
    - https://github.com/openai/baselines

## Courses and Video Lectures

33. **David Silver's RL Course**
    - UCL Course on RL
    - https://www.davidsilver.uk/teaching/

34. **Berkeley Deep RL Course**
    - CS 285 by Sergey Levine
    - http://rail.eecs.berkeley.edu/deeprlcourse/

---

