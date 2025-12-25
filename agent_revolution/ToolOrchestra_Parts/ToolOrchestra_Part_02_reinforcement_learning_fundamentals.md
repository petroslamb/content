# The Orchestration Paradigm Series: Dive 2
*What is GRPO and why does it work for tool use?*

## Introduction

The previous dive established the problem: language models, even very capable ones, make poor choices when asked to orchestrate tools. They exhibit systematic biases—favoring models similar to themselves, deferring excessively to expensive options, or failing to balance cost against accuracy. Prompting alone cannot fix these behaviors because the decision-making patterns required for good orchestration were never part of the models' training.

This dive explains how ToolOrchestra learns those patterns. The technique is called reinforcement learning, and the specific algorithm is GRPO—Group Relative Policy Optimization. By the end, you will understand why reinforcement learning is necessary for orchestration, how GRPO works at every level of detail, and how it connects to the broader landscape of algorithms for training intelligent behavior.

---

## 🌊 Surface Level: Learning From Trial and Error

Consider how you might teach a dog to fetch. You throw the ball. The dog does something—maybe it runs after the ball, maybe it ignores you entirely, maybe it brings back a shoe. You respond according to the result: treats and praise for fetching the ball, nothing for ignoring you, gentle redirection for the shoe. The dog learns that certain behaviors lead to rewards and adjusts accordingly.

This process describes the essence of reinforcement learning. An agent (the dog) takes actions (running toward things) in an environment (the park). After each action, the agent receives feedback (treats or not). Through many repetitions, the agent learns which actions lead to rewards in which situations. No one writes down the rules for the dog to follow; the dog discovers the rules through experience.

ToolOrchestra learns the same way. The orchestrator (agent) starts with a task—say, a difficult math problem. It takes actions: maybe it first searches the web for relevant formulas, then calls a math model to compute an answer, then calls a verifier to check the result. After the trajectory is complete, we evaluate: Did the orchestrator solve the problem? How much did it cost? How long did it take? Did it respect the user's preferences for cheap versus accurate solutions?

The answers to these questions become the feedback. Good trajectories—those that solve the problem efficiently and respect preferences—get reinforced. Poor trajectories get discouraged. Through thousands of such trials across diverse tasks, the orchestrator learns when to call expensive models versus cheap ones, when to verify versus trust direct answers, when to search versus compute.

This is fundamentally different from how most language models are trained. Standard training shows a model millions of examples of good text and asks the model to imitate them. That works for generating fluent sentences, but orchestration requires something more: the ability to try different strategies, observe which work, and adjust accordingly. Imitation alone cannot teach a strategy the model has never seen. Reinforcement learning can.

The specific algorithm ToolOrchestra uses is called GRPO. The details matter for those who want to understand or replicate the work, and we will explore them in the deeper sections. But the core idea is simple: try many different approaches to each task, compare them to each other, and learn from the comparison.

---

## 🏊 Shallow Dive: The Framework of Sequential Decisions

### From Dog Training to Formal Structure

To turn dog training intuition into a precise algorithm, we need a formal framework. The standard framework for sequential decision-making is called a Markov Decision Process, or MDP. Despite the intimidating name, the concept is straightforward—it simply formalizes the idea that an agent perceives situations, takes actions, and receives rewards.

An MDP has five components, each of which maps directly to the orchestration setting.

**States** describe where the agent is. For ToolOrchestra, a state is the entire conversation history so far: the original task, every tool call the orchestrator has made, and every response those tools have returned. The state captures everything the orchestrator knows at each moment.

**Actions** describe what the agent can do. For ToolOrchestra, an action is any tool call the orchestrator might make: search the web for information, call GPT-5 with a subproblem, execute code to verify a calculation, or output a final answer. The action space is vast—essentially any valid tool invocation with any parameters.

**Transitions** describe how the environment responds to actions. In ToolOrchestra, transitions are mostly deterministic: if you call a calculator, you get the calculation result; if you call a search engine, you get search results. Some stochasticity exists—language model responses vary slightly—but the environment is largely predictable.

**Observations** describe what the agent can see. ToolOrchestra operates in a partially observable setting: the orchestrator sees tool responses but doesn't have direct access to the "true" answer or the user's complete intent. It must infer whether its strategy is working from the information each tool returns.

**Rewards** describe how good the outcome was. This is where ToolOrchestra's innovation lies. The reward combines multiple objectives: accuracy (did we solve the task?), cost (how much did we spend on API calls?), latency (how long did it take?), and preference alignment (did we respect the user's stated priorities?). We will explore this multi-objective reward design in the next dive.

### The Markov Property

The "Markov" in Markov Decision Process refers to a specific property: the future depends only on the present state, not on how we got there. If you know the current state completely, knowing the prior history adds nothing.

In ToolOrchestra, this property is satisfied by design. The state is the entire conversation history—every prior action and observation. So by construction, the state contains all relevant information. The orchestrator doesn't need to remember "how it arrived" at the current state separately from the state itself; the arrival path is encoded in the history.

This property matters because many efficient algorithms exist for MDPs that wouldn't work if the future depended on hidden history. It's a technical condition that ToolOrchestra's design ensures is met.

### Policies: The Strategy of Action

A **policy** is a strategy for choosing actions in states. Formally, it's a function that takes a state and produces a distribution over possible actions: given this situation, how likely am I to take each possible action?

In ToolOrchestra, the policy is the orchestrator model itself. Given the conversation history (state), the model produces tokens that specify which tool to call with what parameters (action). The probability of producing those specific tokens is the policy's probability of that action.

Training the orchestrator means adjusting this policy—the billions of parameters that determine how likely each possible action is in each possible state—so that high-reward actions become more likely.

### The Goal: Maximize Expected Reward

The objective of reinforcement learning is to find a policy that maximizes expected total reward over trajectories. A trajectory is a sequence: state, action, reward, next state, next action, next reward, and so on until the task ends.

For ToolOrchestra, a trajectory might be:
1. Receive task (state 1)
2. Call local search (action 1) → get definition (state 2)
3. Call math model (action 2) → get tentative answer (state 3)
4. Call code verifier (action 3) → verification fails (state 4)
5. Call GPT-5 (action 4) → get corrected answer (state 5)
6. Output answer (final action) → receive reward based on correctness, cost, preferences

The algorithm's job is to make the sequence of actions that lead to high rewards more likely and those that lead to low rewards less likely.

---

## 🤿 Deep Dive: Policy Gradients and GRPO

### Direct Policy Optimization

One family of approaches to reinforcement learning learns a value function—an estimate of how good each state is—and uses that to derive which actions to take. Another family, **policy gradient methods**, skips the value function and directly optimizes the policy.

The key insight of policy gradient methods is mathematically elegant. We want to adjust the policy parameters (the model's weights) to increase expected reward. The gradient of expected reward with respect to the parameters can be estimated from samples:

∇J(θ) ≈ E[ ∇log π_θ(action|state) × Advantage(state, action) ]

In words: to improve the policy, increase the probability of actions that have positive advantage (better than average) and decrease the probability of actions with negative advantage. The gradient ∇log π_θ(action|state) tells us how to adjust the weights to change action probabilities. The advantage tells us in which direction to push.

This is called the **policy gradient theorem**, and it underlies nearly all modern reinforcement learning for language models.

### The Advantage: Better or Worse Than Average?

The advantage of an action measures how much better it is compared to the average behavior from that state. An action with a large positive advantage is unusually good. An action with a large negative advantage is unusually bad.

Computing advantages requires knowing what "average" means. One approach is to learn a value function that estimates expected future reward from each state, then compare actual returns to this estimate. Another approach, which GRPO uses, is simpler: generate multiple rollouts from the same starting point and compare them directly.

### GRPO: Group Relative Policy Optimization

GRPO, introduced in the DeepSeekMath paper, takes the comparison approach to its logical conclusion. For each task, GRPO generates multiple rollouts—multiple attempts at solving the same problem. It computes the reward for each rollout, then normalizes:

Advantage(rollout) = (Reward(rollout) - mean of batch) / std of batch

This has several appealing properties.

**Automatic scaling**: An easy task might have rewards clustered around 0.9; a hard task might have rewards clustered around 0.3. With absolute rewards, the easy task would dominate gradient updates. With normalization, both tasks contribute equally based on their relative performance variance.

**Relative comparison**: What matters isn't whether a rollout is "good" in some absolute sense, but whether it's better than the alternatives. A rollout that scores 0.5 is excellent if the alternatives scored 0.2, but poor if they scored 0.8. GRPO captures this directly.

**No value function needed**: Some algorithms require training a separate model to estimate state values. GRPO gets advantages from group statistics, eliminating this complexity.

### The Full GRPO Training Loop

Here is what ToolOrchestra training looks like in practice:

For each training iteration:

1. **Sample a batch of tasks** from ToolScale or other training data.

2. **For each task, generate K rollouts** (K=8 in ToolOrchestra). Each rollout is the orchestrator attempting the task with temperature-based sampling—some randomness to explore different strategies.

3. **Compute rewards for each rollout**. This includes checking whether the answer is correct, tallying the cost of all tool calls, measuring latency, and computing preference alignment based on the user preference vector.

4. **Compute advantages within each group** (all rollouts for the same task). Subtract the group mean, divide by the group standard deviation. This yields normalized advantages that are comparable across tasks.

5. **Apply filters for stability**:
   - If all rollouts in a group have very similar rewards (std < 0.1), skip the group—the gradient signal is too weak to be useful.
   - If a rollout contains malformed tool calls, exclude it—training on malformed outputs would reinforce bad formatting.
   - If a rollout doesn't produce an extractable answer, exclude it.

6. **Update the policy using clipped gradients**. For each rollout, compute the policy gradient weighted by its advantage. But clip the update: if the policy is about to change too much from its previous version, cap the change. This prevents destabilizing large jumps.

The clipping is described by the formula:

Loss = -min(ratio × advantage, clip(ratio, 1-ε, 1+ε) × advantage)

where ratio = π_new / π_old is how much the probability of the rollout changed. This is the same clipping used in PPO (Proximal Policy Optimization), a widely used algorithm that GRPO builds upon.

### Why GRPO for ToolOrchestra?

ToolOrchestra could have used other algorithms. PPO is popular and well-understood. REINFORCE is simpler. Actor-critic methods are sample-efficient. Why GRPO?

The answer lies in the specific challenges of orchestration learning:

**Long trajectories**: Orchestration rollouts can have 50+ turns. Learning value functions for such long sequences is difficult—the credit assignment problem (which early action caused eventual success or failure?) becomes severe. GRPO sidesteps this by comparing complete trajectories rather than trying to assign value to intermediate states.

**Multiple rollouts are natural**: To explore the orchestration space, you want to try different strategies on the same problem. GRPO leverages these multiple rollouts for advantage estimation, turning a necessity into an advantage.

**Simplicity**: GRPO requires only the policy network, not a separate value network. This simplifies implementation and hyperparameter tuning.

The trade-off is sample efficiency. GRPO needs multiple rollouts per task to estimate advantages well. For orchestration, where rollouts involve expensive API calls, this cost is real. But the stability gains appear to outweigh the sample cost.

---

## 🔬 Research Depth: Connections and Open Questions

### Connection to Other RL Algorithms

GRPO can be understood as a particular point in a space of policy gradient methods.

**REINFORCE** (Williams, 1992) is the simplest policy gradient: use raw returns as the learning signal. High variance makes training unstable.

**REINFORCE with baseline** subtracts a baseline from returns to reduce variance. The baseline is typically the average return. GRPO uses the batch mean as this baseline, applied per-task.

**Actor-critic methods** learn a value function (the critic) to provide lower-variance baseline estimates at each step. This improves sample efficiency but adds complexity.

**PPO** (Schulman et al., 2017) adds clipping to prevent destabilizing updates. GRPO inherits PPO's clipping.

GRPO's novelty is combining per-task normalization (comparing rollouts within a task rather than globally) with PPO-style clipping. This combination suits settings where task difficulty varies widely and multiple rollouts per task are available.

### Connection to Weak-to-Strong Learning

An intriguing connection exists to the "weak-to-strong generalization" research agenda. In weak-to-strong, the question is whether weak supervision can elicit strong capabilities from capable models. ToolOrchestra inverts this: a weak model (8B orchestrator) learns to elicit strong capabilities by supervising when and how to invoke strong models.

The orchestrator doesn't have GPT-5's knowledge. But it learns a complementary skill: knowing when GPT-5's knowledge is worth its cost. This meta-cognitive capability is orthogonal to raw problem-solving capability, and the orchestrator's weakness in one doesn't prevent excellence in the other.

This suggests a research direction: systematically mapping which capabilities are orthogonal. Can a 1B model learn to orchestrate 100B models? What's the limit?

### Open Questions

Several questions remain open for future research:

**Sample efficiency**: Can we reduce the number of rollouts needed per task? GRPO uses 8. Could a hybrid approach—using a cheap value function for some signal plus GRPO's relative comparison—improve efficiency?

**Credit assignment**: Within a 50-turn trajectory, which decisions mattered? Currently, all decisions in a successful trajectory get reinforced, including any mistakes that happened to be corrected later. More refined credit assignment could accelerate learning.

**Exploration**: How do we ensure the orchestrator explores enough different strategies? Current training uses temperature sampling for stochasticity, but this is random exploration. Directed exploration—systematically trying tools the orchestrator avoids—might discover better strategies.

**Curriculum**: Should training start with easy tasks and progress to harder ones? Should it start with cheap tool configurations and progress to expensive ones? Curriculum learning has helped in other RL settings but isn't explored in the ToolOrchestra paper.

---

## Conclusion

Reinforcement learning provides the machinery for ToolOrchestra to learn orchestration strategies that could never be distilled from static examples. By trying different approaches, observing which produce high rewards, and updating its policy accordingly, the orchestrator acquires decision-making patterns that prompt engineering cannot instill.

GRPO—the specific algorithm used—is well-suited to the orchestration setting: long trajectories, multiple rollouts per task, and widely varying task difficulties. Its relative comparison approach provides stable training signals without the complexity of learned value functions.

With the algorithmic foundation established, the next dive examines what exactly the orchestrator is trying to optimize. The reward design in ToolOrchestra is not a single number but a carefully constructed combination of accuracy, cost, latency, and preference alignment—a multi-objective optimization problem that requires its own careful treatment.

---

## References

### Foundational RL

1. **Reinforcement Learning: An Introduction**
   - Sutton, R.S., & Barto, A.G. (2018). 2nd Edition. MIT Press
   - http://incompleteideas.net/book/the-book-2nd.html

2. **Policy Gradient Theorem**
   - Sutton, R.S., McAllester, D., Singh, S., & Mansour, Y. (2000). "Policy Gradient Methods for Reinforcement Learning with Function Approximation." *NeurIPS 2000*
   - https://proceedings.neurips.cc/paper/2000/file/4b86abe48d358ecf194c56c69108433e-Paper.pdf

### GRPO and Related Algorithms

3. **GRPO (DeepSeekMath)**
   - Shao, Z., Wang, P., Zhu, Q., et al. (2024). "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models." *arXiv:2402.03300*
   - https://arxiv.org/abs/2402.03300

4. **PPO (Proximal Policy Optimization)**
   - Schulman, J., Wolski, F., Dhariwal, P., et al. (2017). "Proximal Policy Optimization Algorithms." *arXiv:1707.06347*
   - https://arxiv.org/abs/1707.06347

5. **REINFORCE**
   - Williams, R.J. (1992). "Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning." *Machine Learning*, 8(3-4), 229-256
   - https://link.springer.com/article/10.1007/BF00992696

6. **TRPO**
   - Schulman, J., Levine, S., Abbeel, P., et al. (2015). "Trust Region Policy Optimization." *ICML 2015*
   - https://arxiv.org/abs/1502.05477

### Advantage Estimation

7. **GAE (Generalized Advantage Estimation)**
   - Schulman, J., Moritz, P., Levine, S., et al. (2016). "High-Dimensional Continuous Control Using Generalized Advantage Estimation." *ICLR 2016*
   - https://arxiv.org/abs/1506.02438

### RL for Language Models

8. **RLHF Tutorial**
   - Chip Huyen. "RLHF"
   - https://huyenchip.com/2023/05/02/rlhf.html

9. **OpenAI Spinning Up**
   - OpenAI. "Spinning Up in Deep RL"
   - https://spinningup.openai.com/en/latest/

10. **TRL Library**
    - HuggingFace. Transformer Reinforcement Learning
    - https://github.com/huggingface/trl

---
