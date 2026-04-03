# The Orchestration Paradigm Series: Dive 2
# Policy Gradients in Discrete Spaces

> [!NOTE]
> **System Auditor's Log:** Reinforcement Learning (RL) in language models is often misunderstood. It is not "teaching the model to think." It is **re-weighting the probability distribution** of token sequences based on a scalar reward. In the context of orchestration, this is complicated by the "API Boundary", the fact that tool execution happens outside the model's computational graph.

To understand why ToolOrchestra uses **Group Relative Policy Optimization (GRPO)**, we must first look at the physics of backpropagation.

In a standard neural network, gradients flow backward from the loss function to the weights. This requires every operation in the chain to be differentiable.

$$ \text{Loss} \rightarrow \text{Output} \rightarrow \text{Layer}_N \rightarrow \dots \rightarrow \text{Layer}_0 $$

Tool use breaks this chain.

When the model generates a tool call (e.g., `requests.get("https://api.weather.com")`), that text is parsed and executed by an external Python interpreter. The interpreter returns a string (e.g., "72°F").

The Python interpreter is **non-differentiable**. You cannot calculate the gradient of a "requests.get" function with respect to the neural network weights. The chain is broken. The model takes an action, the world changes, and the model sees a new state. The only signal linking the action to the result is the final outcome.

## The Policy Gradient Solution

This is the classic Reinforcement Learning setup. Since we cannot backpropagate through the tool, we treat the tool call as an **Action ($A$)** taken by a **Policy ($\pi_\theta$)** in an Environment.

The objective is to maximize the expected reward:

$$ J(\theta) = E_{\tau \sim \pi_\theta}[R(\tau)] $$

where $\tau$ is the trajectory (sequence of thoughts, tool calls, and outputs).

Using the **REINFORCE** trick (or Policy Gradient Theorem), we can estimate the gradient effectively by saying: *If a trajectory led to a high reward, increase the probability of all actions taken in that trajectory.*

## Why GRPO?

Standard PPO (Proximal Policy Optimization) requires training a separate "Critic" model to estimate the value function $V(s)$. This Critic predicts how much reward the model expects to get from the current state.

Training a Critic is expensive. It effectively doubles the memory requirement (you need to hold the Policy model and the Critic model). For Large Language Models, which are already memory-constrained, this is a heavy tax.

**GRPO (Group Relative Policy Optimization)** removes the Critic.

Instead of comparing the reward to a learned baseline (the Critic's guess), GRPO compares the reward to the **group average**.

```python
# The Mechanics of GRPO
# 1. Generate a group of G outputs for the same prompt.
# 2. Score them all.
# 3. Use the group average as the baseline.

def grpo_loss(prompt, model, reward_fn, group_size=4):
    # Step 1: Rollout
    # Generate multiple distinct trajectories from the same start state
    trajectories = model.generate(prompt, num_return_sequences=group_size)
    
    # Step 2: Reward
    # Calculate scalar reward for each trajectory
    rewards = [reward_fn(t) for t in trajectories]
    
    # Step 3: Advantage Calculation
    # Normalize rewards within the group
    mean_reward = np.mean(rewards)
    std_reward = np.std(rewards)
    advantages = (rewards - mean_reward) / (std_reward + epsilon)
    
    # Step 4: Policy Update
    # Push explicitly for the trajectories that beat the group average.
    # The 'Critic' is essentially replaced by the other samples in the batch.
    return compute_policy_gradient(trajectories, advantages)
```

## The "KL Penalty" Safety Rail

The danger with RL is **Reward Hacking**. If the reward function is imperfect (it almost always is), the model will exploit it. It might learn to ignore the tool and just guess, or it might output gibberish that somehow triggers a "correct" regex match.

To prevent this, we enforce a **KL Divergence Penalty**. We compare the RL-trained model ($\pi_\theta$) to the original reference model ($\pi_{ref}$). If the RL model's probability distribution diverges too far from the reference (i.e., it starts speaking a different language or losing coherence), we subtract a penalty from the reward.

$$ R_{total} = R_{task} - \beta \cdot D_{KL}(\pi_\theta || \pi_{ref}) $$

This forces the model to stay "close" to its original training (grammatically correct, logical) while optimizing the specific orchestration objective.

In ToolOrchestra, this mechanism is what allows the 8B model to learn *strategies* like "Double Check" or "Give Up" without explicitly being told to do so. It simply tries thousands of variations, and GRPO amplifies the ones that minimize cost while maintaining accuracy.

---

## Annotated Bibliography

1.  **Schulman et al. (2017)** - *Proximal Policy Optimization Algorithms*: The baseline PPO paper. Defined the clipping objective that prevents destructive policy updates.
2.  **Shao et al. (2024)** - *DeepSeekMath: Pushing the Limits of Mathematical Reasoning*: Introduced GRPO (Group Relative Policy Optimization) to eliminate the Critic model, saving ~50% VRAM during training.
3.  **Ouyang et al. (2022)** - *Training Language Models to Follow Instructions with Human Feedback*: The canonical RLHF paper. Established the KL-divergence penalty pattern for preventing mode collapse in language models.

---

## Appendix: MDP Foundations (Optional)

> This appendix is for readers who want a primer on the Markov Decision Process formalism. Skip if you are already familiar with RL fundamentals.

### The Building Blocks

**States** describe where the agent is. For ToolOrchestra, a state is the entire conversation history: the original task, every tool call the orchestrator has made, and every response those tools have returned.

**Actions** describe what the agent can do. For ToolOrchestra, an action is any tool call the orchestrator might make: search the web, call GPT-5 with a subproblem, execute code, or output a final answer. The action space is vast.

**Transitions** describe how the environment responds to actions. In ToolOrchestra, transitions are mostly deterministic: if you call a calculator, you get the calculation result.

**Rewards** describe how good the outcome was. ToolOrchestra combines multiple objectives: accuracy, cost, latency, and preference alignment.

### The Markov Property

The "Markov" in Markov Decision Process means: the future depends only on the present state, not on how we got there.

In ToolOrchestra, this property is satisfied by design. The state *is* the entire conversation history, so it contains all relevant information. The arrival path is encoded in the history itself.

### Policies

A **policy** is a strategy for choosing actions in states. Formally, it is a function that takes a state and produces a distribution over possible actions.

In ToolOrchestra, the policy is the orchestrator model itself. Given the conversation history (state), the model produces tokens specifying which tool to call (action). Training the orchestrator means adjusting the policy parameters (the billions of weights) so that high-reward actions become more likely.

---

## Appendix: RL Methods Evolution (Optional)

> This appendix traces the lineage of policy optimization methods leading to GRPO. It is for readers familiar with RL basics who want context on why specific algorithmic choices were made.

### The Problem: Training LLMs with RL

Standard supervised learning requires ground-truth labels. But for orchestration, there is no single "correct" tool sequence. Multiple paths can solve the same problem. We need a method that:
1. Works with sparse, delayed rewards (only know if we succeeded at the end)
2. Doesn't require a separate value network (VRAM is precious)
3. Stays close to the pretrained distribution (don't forget language)

### The Evolution

| Method | Year | Key Innovation | Variance | Memory | Best For |
|:---|:---|:---|:---|:---|:---|
| **REINFORCE** | 1992 | Policy gradients via log-prob weighting | Very High | 1x | Toy problems, proofs-of-concept |
| **PPO** | 2017 | Clipped objective + learned Critic baseline | Low | **2x** | Standard RL (robotics, games) |
| **RLHF** | 2022 | PPO applied to LLM alignment | Low | **2x** | Instruction-following, safety |
| **GRPO** | 2024 | Group-average baseline, no Critic | Medium | **1x** | **LLMs with limited VRAM** |

### Why GRPO for ToolOrchestra

**The memory constraint:** An 8B orchestrator requires ~16GB in bf16. PPO's Critic is another 8B model. On 16 H100s (80GB each), fitting Policy + Critic leaves minimal room for batch size. Small batches = high gradient variance = unstable training.

**GRPO's trade-off:** Replace the learned Critic with the empirical group average. For each prompt, generate G=4-8 trajectories, compute mean reward, subtract from each trajectory's reward. This is noisier than a trained Critic but requires **zero additional parameters**.

**The variance tax:** GRPO needs ~2-4x larger batch sizes than PPO to achieve similar gradient signal-to-noise. This is why ToolOrchestra requires 16 H100s (not 4): the extra GPUs buy batch size to compensate for the noisier baseline.

### The Practical Implication

If you have unlimited VRAM (e.g., 8x H100s for a 1B model), PPO with a Critic is cleaner. If you're VRAM-constrained (8B+ models), GRPO is the only viable path without model parallelism for the Critic.

ToolOrchestra chose GRPO because the alternative was either (a) a smaller orchestrator or (b) 2x the GPU budget. Neither was acceptable.
