# The Orchestration Paradigm Series: Dive 6
*What does it take to train an orchestrator?*

## Introduction

The previous dives explained what ToolOrchestra is trying to learn (efficient orchestration), how it learns (reinforcement learning with GRPO), and what objective it optimizes (multi-objective reward balancing accuracy, cost, and preferences). This dive answers a different question: what does it actually take to train such a system?

Training ToolOrchestra is not as simple as running a script on a laptop. The orchestrator must process 24,000-token contexts, generate trajectories of up to 50 turns, compute rewards by actually calling tools, and update an 8-billion parameter model's weights—all while avoiding the many instabilities that can derail reinforcement learning. This dive walks through the engineering required to make that happen.

For practitioners considering similar systems, this material is immediately actionable. For researchers, it reveals which technical challenges the ToolOrchestra team faced and how they solved them. For curious readers, it provides a window into what training frontier AI systems actually involves.

---

## 🌊 Surface Level: The Training Journey in Plain Terms

Training ToolOrchestra happens in three stages. Think of it like teaching someone to be a great project manager: first, you show them examples of good project management; then, you let them practice while giving feedback; finally, you filter out the bad habits they develop along the way.

**Stage 1: Learning the basics through imitation.** Before learning to orchestrate, the model needs to learn the format of tool calls—how to structure a request to an external API, how to parse responses, and how to format final answers. This is called Supervised Fine-Tuning (SFT). The model sees examples of correctly formatted tool use and learns to produce similar output. This stage establishes basic competence: the model can call tools, but it doesn't yet know when it should.

**Stage 2: Learning when and why through practice.** With basic format mastered, the model moves to reinforcement learning. Now it attempts tasks, gets feedback on its performance (was the answer correct? was it efficient? did it respect preferences?), and adjusts its behavior accordingly. This is where the orchestration intelligence actually develops. The model learns that calling a cheap tool first is often smart, that escalating to expensive models is sometimes necessary, and that the right choice depends on the specific task and user preferences.

**Stage 3: Filtering out bad patterns.** Reinforcement learning is powerful but unstable. The model might develop problematic habits—always trying the same tool, generating malformed output, spinning in unhelpful loops. Filtering mechanisms catch these issues: trajectories that don't meet quality standards are excluded from training, batches where all attempts look the same are skipped, and outputs that don't parse correctly are rejected. Without these safeguards, training degrades rapidly.

The hardware requirements are substantial. ToolOrchestra training ran on 16 NVIDIA H100 GPUs—cutting-edge hardware that costs roughly $40,000 per month to rent. Each training run took several days. Total compute cost: likely in the low six figures. This is modest by frontier model standards but beyond hobbyist budgets.

The key insight for practitioners: if you're training a smaller orchestrator for a more limited domain, the same principles apply at smaller scale. The three-stage structure (SFT for format, RL for decisions, filtering for stability) works regardless of model size or domain specificity.

---

## 🏊 Shallow Dive: The Three Training Stages in Detail

### Stage 1: Supervised Fine-Tuning (SFT)

The starting point is a pretrained language model—in ToolOrchestra's case, Qwen-2.5-8B. This model can write coherent text but has no specific knowledge of tool calling or orchestration. The goal of SFT is to give it that knowledge efficiently.

**The training data comes from ToolScale.** This is the synthetic dataset described in Dive 4, containing thousands of tool-use trajectories across 10 domains. Each example shows a task, the sequence of tool calls that solved it, and the final answer. The SFT stage teaches the model to produce output in this format.

**SFT is relatively straightforward.** It's the same next-token prediction used in standard language model training. Show the model the context (task description, available tools), train it to predict the next tokens (the first tool call), then extend the context and repeat. After seeing enough examples, the model can generate correctly formatted tool calls.

**SFT establishes the starting point—not the destination.** The behaviors learned in SFT are imitative. The model does what the examples showed, which reflected GPT-5's orchestration style (since GPT-5 generated the ToolScale data). But GPT-5's style is not optimal for an 8B orchestrator. The 8B model has different capabilities and should make different decisions. Reinforcement learning adapts these decisions to the orchestrator's actual strengths.

### Stage 2: Reinforcement Learning with GRPO

After SFT, the model can format tool calls but doesn't know which calls to make. GRPO teaches this through trial, feedback, and adjustment.

**The setup revisited, concretely.** For each training task, the orchestrator generates 8 independent rollouts. Each rollout is a complete attempt at solving the task—potentially many turns, many tool calls, and eventually an answer (or failure to answer). For each rollout, we compute rewards by checking correctness, tallying costs, measuring latencies, and evaluating preference alignment.

**Advantages come from comparison.** Within each batch of 8 rollouts, we subtract the mean reward and divide by standard deviation. This yields normalized advantages: positive for above-average rollouts, negative for below-average. The policy update then increases probability of actions in high-advantage rollouts and decreases probability of actions in low-advantage rollouts.

**KL divergence prevents drift.** A danger in policy gradient training is that the model's behavior can change too rapidly, destabilizing learning. ToolOrchestra uses KL clipping, adopted from PPO: if the policy tries to move too far from its previous version in a single update, the change is capped. This keeps training stable but slows learning.

**Long contexts require special handling.** Orchestration trajectories can be 24,000 tokens—far longer than typical training examples. With 8 rollouts per task and limited GPU memory, standard training would run out of memory immediately. ToolOrchestra uses gradient checkpointing: intermediate activations are discarded during the forward pass and recomputed during the backward pass. This trades computation for memory, making long-context training feasible.

### Stage 3: Filtering for Stability

Raw reinforcement learning on language models is notoriously unstable. Small training anomalies can cascade into severe degradation. ToolOrchestra uses three filters to prevent this.

**Homogeneity filtering** addresses an issue where all rollouts in a batch produce nearly identical results. This might happen on very easy tasks (everyone gets it right) or very hard tasks (everyone fails). When reward standard deviation within a batch is below 0.1, the batch is skipped—there's no meaningful comparison to learn from.

**Format consistency filtering** catches cases where the model generates malformed output. If a rollout contains tool calls that don't parse correctly, or references tools that don't exist, or produces an answer that can't be extracted, that rollout is excluded. Training on malformed output would reinforce bad formatting habits.

**Outcome requirements** ensure every included rollout meets minimum standards. At minimum, the rollout must produce an extractable final answer. Some experiments added stricter requirements—only including rollouts that passed execution verification.

These filters reduce training data volume but dramatically improve stability. Without them, ToolOrchestra training tended to degrade after early progress, as the model learned to exploit reward quirks rather than genuinely solve tasks.

---

## 🤿 Deep Dive: Hardware and Implementation

### The 16 H100 Setup

ToolOrchestra training used 16 NVIDIA H100 80GB GPUs—about $1.3 million worth of hardware at retail prices, or roughly $40,000 per month to rent from cloud providers. This is not hobbyist infrastructure but is vastly more accessible than the thousand-GPU clusters used for frontier model pretraining.

**Why H100s?** The H100 is currently the most capable data center GPU, with 80GB of HBM3 memory and optimizations for transformer training. The 80GB memory matters because long-context RL requires storing many activations during forward passes. An 8B model at 24K context with batch size 8 easily exceeds what smaller GPUs can hold.

**Distributed training with FSDP.** Even 80GB isn't enough to hold the entire model plus gradients plus activations during training. ToolOrchestra uses FSDP (Fully Sharded Data Parallel), a technique that shards model parameters across multiple GPUs. Each GPU holds a fraction of the parameters and communicates with others during forward and backward passes. This enables training models larger than any single GPU can hold.

The FSDP configuration splits the model across all 16 GPUs, with each GPU processing its share of the batch. Communication overhead is significant—GPUs must synchronize gradients after each update—but modern interconnects (NVLink within nodes, InfiniBand between nodes) make this fast enough to be practical.

### Context Length and Memory Pressure

The 24,000-token context is one of ToolOrchestra's most distinctive design choices. It enables long multi-turn trajectories that capture complex orchestration strategies. But it creates severe memory pressure.

**Memory scales quadratically with context** in standard transformers (due to attention). At 24K tokens, even with FlashAttention optimizations, attention alone consumes substantial memory. Combined with the 8-wide rollout generation, naive approaches would require hundreds of gigabytes per GPU.

**Gradient checkpointing** is the primary mitigation. During the forward pass, most intermediate activations are discarded rather than stored. During the backward pass, they're recomputed as needed. This roughly triples computation time for a 3x reduction in memory. ToolOrchestra accepts this trade-off because memory is the binding constraint.

**Sequence packing** helps efficiency. Rather than padding every sequence to 24K tokens, multiple shorter sequences are packed into single forward passes. This reduces wasted computation on padding tokens, which can otherwise dominate training time for variable-length sequences.

### Training Hyperparameters

The paper reports the following key settings:

- **Learning rate**: 2e-6 (small, for stability)
- **Batch size**: 8 rollouts per task, accumulated over multiple tasks
- **KL coefficient (β)**: 0.015 (very small, allowing gradual drift)
- **Clipping parameter (ε)**: 0.2 (standard PPO value)
- **Maximum sequence length**: 24,000 tokens
- **Maximum turns per trajectory**: 50

The small learning rate and KL coefficient reflect caution about stability. Reinforcement learning on language models is sensitive to hyperparameter choices, and conservative settings reduce the risk of catastrophic training collapse.

---

## 🔬 Research Depth: Credit Assignment and Exploration

Two deep challenges underlie all RL training for orchestration: credit assignment and exploration. Understanding these helps explain why training is difficult and where future improvements might come from.

### The Credit Assignment Problem

A successful 50-turn trajectory involves 50 decisions. Which ones mattered? The orchestrator might have made 45 good decisions and 5 lucky ones, or 45 mediocre decisions and 5 brilliant ones, and we cannot easily distinguish these cases from observing only the final outcome.

GRPO assigns the same advantage to every step in a trajectory. If the trajectory succeeded, all decisions get credit; if it failed, all decisions get blame. This is crude but has advantages:

**Simplicity**: No need to model which steps contributed what fraction of success.

**Correctness in expectation**: Over many trajectories, decisions that consistently appear in good outcomes will be reinforced, and those that consistently appear in bad outcomes will be discouraged. The signal is noisy but accurate on average.

**Computational efficiency**: No auxiliary models or per-step value estimation.

The cost is sample inefficiency. Many trajectories are needed to distinguish signal from noise. A decision that appears in 100 successful and 100 unsuccessful trajectories might still be slightly good (55% success) or slightly bad (45% success), but detecting this requires many more samples than detecting a consistently good (90%) or consistently bad (10%) decision.

Alternative approaches exist. Monte Carlo tree search samples future trajectories from intermediate states to estimate their value. Learned value functions estimate future returns from each state, enabling step-by-step credit. Both add complexity and their own sources of error.

### The Exploration Challenge

GRPO generates diverse rollouts through temperature-controlled sampling. Higher temperature means more randomness in token generation, which translates to more varied strategies. But this is undirected exploration—the model tries different things at random, not strategically.

Potentially better approaches exist but aren't used in ToolOrchestra:

**Curiosity-driven exploration** rewards visiting novel states, encouraging the model to try tools it hasn't used much. This could accelerate discovery of underexplored strategies.

**Hierarchy-aware exploration** in recursive orchestration might separately explore high-level and low-level decisions, ensuring both receive adequate coverage.

**Curriculum learning** might start training on easier tasks (where many strategies succeed) before progressing to harder tasks (where only sophisticated strategies work). This could bootstrap exploration by first learning basic patterns.

Why didn't ToolOrchestra use these? They add complexity, and GRPO's simple exploration appears to work well enough. The paper's strong benchmark results suggest that random exploration with sufficient rollouts finds good strategies. But there's likely headroom for future work to improve sample efficiency through smarter exploration.

### Catastrophic Forgetting

A related concern is that RL training might degrade capabilities the base model had. The base Qwen-2.5-8B can answer many questions directly, write code, and follow instructions. If RL training focuses too heavily on orchestration, these capabilities might suffer.

ToolOrchestra addresses this implicitly through the KL penalty, which keeps the policy close to its initialization. Large capability drifts would require large KL divergence, which is penalized. But the KL penalty doesn't guarantee preservation of specific capabilities—it only limits overall distribution change.

Explicit continual learning techniques (experience replay, elastic weight consolidation) could make stronger guarantees but aren't used in the paper. This might be an area for improvement in future work, especially for production systems where orchestration training shouldn't degrade conversation ability.

---

## Conclusion

Training ToolOrchestra requires industrial-scale infrastructure (16 H100 GPUs), careful staging (SFT → RL → filtering), and numerous stability techniques (KL clipping, homogeneity filtering, gradient checkpointing). The challenge is not just computational but also algorithmic: credit assignment and exploration remain fundamentally difficult in long-horizon RL.

For practitioners building similar systems at smaller scale, the key lessons are:

1. Start with SFT on well-formatted examples to establish tool-calling competence
2. Use relative comparison (like GRPO) rather than absolute rewards for stable gradients
3. Filter aggressively for quality—training on degenerate outputs degrades everything
4. Expect substantial compute requirements that scale with context length and model size

For researchers, the training pipeline reveals several optimization opportunities: smarter credit assignment, directed exploration, and continual learning safeguards. The current approach works, but there's likely substantial headroom.

With the training infrastructure understood, the next dive will examine what the orchestrator actually learns to do: the tool coordination patterns that emerge from this training process.

---

## References

### Distributed Training

1. **FSDP (Fully Sharded Data Parallel)**
   - FairScale Library. Meta
   - https://fairscale.readthedocs.io/en/latest/

2. **ZeRO (Memory Optimization)**
   - Rajbhandari, S., et al. (2020). "ZeRO: Memory Optimizations Toward Training Trillion Parameter Models." *SC20*
   - https://arxiv.org/abs/1910.02054

### Efficient Training

3. **Gradient Checkpointing**
   - Chen, T., et al. (2016). "Training Deep Nets with Sublinear Memory Cost." *arXiv:1604.06174*
   - https://arxiv.org/abs/1604.06174

4. **FlashAttention**
   - Dao, T., et al. (2022). "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness." *NeurIPS 2022*
   - https://arxiv.org/abs/2205.14135

5. **FlashAttention-2**
   - Dao, T. (2023). "FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning." *arXiv:2307.08691*
   - https://arxiv.org/abs/2307.08691

### Policy Gradient Methods

6. **PPO**
   - Schulman, J., et al. (2017). "Proximal Policy Optimization Algorithms." *arXiv:1707.06347*
   - https://arxiv.org/abs/1707.06347

7. **GRPO**
   - Shao, Z., et al. (2024). "DeepSeekMath: Pushing the Limits of Mathematical Reasoning." *arXiv:2402.03300*
   - https://arxiv.org/abs/2402.03300

### Credit Assignment

8. **Temporal Difference Learning**
   - Sutton, R.S. (1988). "Learning to Predict by the Methods of Temporal Differences." *Machine Learning*, 3(1), 9-44
   - https://link.springer.com/article/10.1007/BF00115009

9. **Hindsight Credit Assignment**
   - Harutyunyan, A., et al. (2019). "Hindsight Credit Assignment." *NeurIPS 2019*
   - https://arxiv.org/abs/1912.02503

### Continual Learning

10. **Elastic Weight Consolidation**
    - Kirkpatrick, J., et al. (2017). "Overcoming Catastrophic Forgetting in Neural Networks." *PNAS*
    - https://arxiv.org/abs/1612.00796

---
