# The Orchestration Paradigm Series: Dive 6
*What does it take to train an orchestrator?*
## Introduction

This part dives into the nuts and bolts of training an orchestrator in practice—from warm-starting with supervised data to stabilizing long-horizon RL on large models. It connects the conceptual RL picture to the real infrastructure, filtering, and optimization tricks that make the system trainable.


## 🌊 Surface Level: How Do You Train This?

**The setup**:
- Start with a pre-trained 8B model (Qwen3-8B)
- Give it examples of tool-using tasks
- Let it try solving tasks (sometimes succeeds, sometimes fails)
- Reward successes, penalize failures
- Repeat thousands of times until it gets good

**The challenge**: Training is unstable—small changes can make everything collapse.

**The solution**: Careful filtering and stabilization techniques.

## 🏊 Shallow Dive: The Training Pipeline

### Stage 1: Supervised Fine-Tuning (Warmstart)

Before RL, the model needs a basic understanding of tool use.

**Data**: GeneralThought-430K dataset
- 430K examples of reasoning traces
- Includes some tool-use examples
- Formatted as: Question → Reasoning → Tool Call → Tool Response → Answer

**Training objective**: Standard next-token prediction
```python
loss = -log P(next_token | previous_tokens)
```

**Why this matters**: 
- Teaches basic tool-calling syntax
- Shows examples of multi-turn reasoning
- Prevents RL from starting completely randomly

**Analogy**: Teaching someone to play chess
- SFT = Learning the rules and seeing example games
- RL = Actually playing and improving from experience

### Stage 2: Reinforcement Learning

Now the real training begins.

**Batch configuration**:
- Batch size: 16 tasks
- Rollouts per task: 8 attempts
- Total rollouts per batch: 16 × 8 = 128 trajectories

**Per-batch training loop**:
```python
for epoch in range(num_epochs):
    # Sample batch of tasks
    tasks = sample_tasks(batch_size=16)
    
    for task in tasks:
        # Generate multiple attempts
        rollouts = []
        for _ in range(8):
            rollout = orchestrator.generate(
                task, 
                max_turns=50,
                temperature=0.7  # Some randomness for exploration
            )
            rollouts.append(rollout)
        
        # Compute rewards
        rewards = [compute_reward(r, task) for r in rollouts]
        
        # Compute advantages (GRPO)
        advantages = compute_grpo_advantages(rewards)
        
        # Filter unstable examples
        if std(rewards) < 0.1:
            continue  # Skip this task (homogeneity filtering)
        
        # Update policy
        for rollout, advantage in zip(rollouts, advantages):
            if is_valid_format(rollout):
                update_policy(rollout, advantage)
```

**Key parameters**:
- Learning rate: 1e-6 (very small, for stability)
- Max sequence length: 24,000 tokens (very long, for multi-turn)
- Max generation length: 8,000 tokens per turn
- Clip parameter ε: 0.2 (standard for PPO-style algorithms)

### Stage 3: Filtering for Stability

**The three filters** (from Section 3.2):

**Filter 1: Homogeneity Filtering**
```python
def should_skip_batch(rewards):
    if std(rewards) < 0.1:
        return True  # All rollouts too similar
    return False
```

**Why**: If all attempts succeed/fail similarly, gradient signal is weak and noisy.

**Filter 2: Format Consistency Filtering**
```python
def is_valid_format(rollout):
    # Check tool calls follow JSON schema
    tool_calls = extract_tool_calls(rollout)
    
    for call in tool_calls:
        if not matches_schema(call):
            return False
        if call.tool_name not in available_tools:
            return False
        if not validate_parameters(call.parameters):
            return False
    
    return True
```

**Why**: Training on malformed outputs teaches model to produce malformed outputs.

**Filter 3: Invalid Output Filtering**
```python
def produces_valid_answer(rollout):
    # Must actually produce an answer
    if not has_final_answer(rollout):
        return False
    
    # Answer must be extractable
    try:
        answer = extract_answer(rollout)
    except:
        return False
    
    # Answer must be non-empty
    if len(answer.strip()) == 0:
        return False
    
    return True
```

**Why**: Empty or non-extractable answers don't provide useful training signal.

**Impact of filtering**: 
- Without filters: Training diverges after ~1000 steps
- With filters: Stable training for 10,000+ steps

## 🤿 Deep Dive: Technical Training Details

### The KL Divergence Problem

**Key challenge in RL**: Policy shouldn't change too much per update.

**Why**: If new policy is very different from old:
- High variance in policy ratio π_new / π_old
- Can get ratio → ∞ or ratio → 0
- Causes numerical instability
- Training diverges

**The math**:
```
Policy ratio: r(τ) = π_θ(τ) / π_θ_old(τ)

If π_θ(τ) = 0.001 and π_θ_old(τ) = 0.5:
    r(τ) = 0.002 (very small)

If π_θ(τ) = 0.5 and π_θ_old(τ) = 0.001:
    r(τ) = 500 (very large!)
```

**Solution 1: Clipping** (PPO approach)
```python
clipped_ratio = clip(ratio, 1-ε, 1+ε)
# Forces ratio ∈ [0.8, 1.2] if ε=0.2

loss = -min(ratio * advantage, clipped_ratio * advantage)
```

**Why this works**: 
- If ratio > 1+ε (new policy much more likely), clip to 1+ε
- If ratio < 1-ε (new policy much less likely), clip to 1-ε
- Prevents extreme updates

**Solution 2: KL Penalty** (TRPO approach, not used here but worth knowing)
```python
loss = policy_gradient_loss + β * KL(π_θ || π_θ_old)
```

Where KL divergence measures how different the policies are.

**ToolOrchestra uses clipping** (simpler, works well in practice).

### Sequence Length Challenges

**The problem**: Orchestrator can have 50-turn trajectories
- Each turn: 200-500 tokens
- Total sequence: 10,000-25,000 tokens
- This is VERY long for language models

**Standard transformer**: Quadratic attention complexity
- Attention: O(n²) where n = sequence length
- 25,000 tokens: 625 million attention computations
- Memory: O(n²) for attention matrix

**Qwen3's solution**: Uses grouped-query attention (GQA)
- Reduces memory by sharing key/value across attention heads
- Speeds up inference
- Allows longer contexts

**Still challenging**:
- Even with GQA, 24K tokens is near limits
- Gradient computation through long sequences is memory-intensive
- Requires gradient checkpointing

**Gradient checkpointing**:
```python
# Instead of keeping all activations in memory
# Recompute them during backward pass

def forward_with_checkpointing(model, input):
    # Forward: Only save every Nth layer's activations
    checkpoints = []
    x = input
    for i, layer in enumerate(model.layers):
        x = layer(x)
        if i % checkpoint_frequency == 0:
            checkpoints.append(x.detach())
    
    return x, checkpoints

def backward_with_checkpointing(model, loss, checkpoints):
    # Backward: Recompute intermediate activations
    # Trade compute for memory
    ...
```

**Trade-off**: 
- Memory: ↓ 60% (fits in GPU)
- Compute: ↑ 30% (need to recompute)
- Overall: Worth it (otherwise doesn't fit at all)

### Distributed Training on 16 H100s

**The setup**: 
- 16 NVIDIA H100 GPUs (80GB memory each)
- Likely using FSDP (Fully Sharded Data Parallel)
- Or ZeRO-3 (Zero Redundancy Optimizer)

**How distributed training works**:

**Naive approach** (Data Parallel):
```
GPU 0: Full model copy, batch examples 0-7
GPU 1: Full model copy, batch examples 8-15
...
GPU 15: Full model copy, batch examples 120-127
```

**Problem**: Each GPU needs full model (8B params × 2 bytes/param = 16GB just for weights)

**FSDP approach** (what they likely use):
```
GPU 0: Model shard 1/16, works on all examples
GPU 1: Model shard 2/16, works on all examples
...
GPU 15: Model shard 16/16, works on all examples
```

**How it works**:
```python
# Each GPU has 1/16 of parameters

# Forward pass:
for layer in model.layers:
    # All-gather: Collect full layer from all GPUs
    full_layer = all_gather(layer_shard)
    
    # Compute
    output = full_layer(input)
    
    # Free full layer (keep only shard)
    del full_layer

# Backward pass: Similar, but for gradients

# Update:
# Each GPU updates only its shard
optimizer.step()  # Only updates local shard
```

**Advantages**:
- Memory: Each GPU holds 1/16 of model
- Can train models that wouldn't fit on single GPU
- Linear scaling (16 GPUs ≈ 16× faster)

**Communication overhead**:
- All-gather operations require GPU-GPU communication
- H100 has 900 GB/s NVLink (very fast)
- Still, communication takes ~20% of training time

### Learning Rate and Optimization

**Learning rate: 1e-6** (very small)

**Why so small?**
- RL is already high-variance
- Policy shouldn't change too quickly (KL divergence)
- Small steps = more stable

**Comparison to SFT**:
- SFT learning rate: typically 1e-5 to 1e-4 (10-100× larger)
- RL learning rate: 1e-6 to 1e-7 (this paper uses 1e-6)

**Optimizer**: Likely AdamW (not specified in paper, but standard)
```python
optimizer = AdamW(
    model.parameters(),
    lr=1e-6,
    betas=(0.9, 0.999),  # Standard Adam betas
    weight_decay=0.01     # L2 regularization
)
```

**Learning rate schedule**: Not mentioned in paper
- Likely constant (no warmup/decay needed for RL)
- Or very gentle decay (reduce by 0.5× after plateau)

## 🔬 Research Depth: RL Training Stability

### The Credit Assignment Problem

**Fundamental challenge**: Which action led to success/failure?

**Example**:
```
Turn 1: Call local_search("Alon-Tarsi number")
Turn 2: Read definition
Turn 3: Call Qwen2.5-Math-7B("Calculate for K_{1000,1000}")
Turn 4: Get wrong answer
Turn 5: Call GPT-5("Verify calculation")
Turn 6: GPT-5 corrects it
Turn 7: Output correct answer

Reward: +1 (success)
```

**Question**: Which turns should be reinforced?
- Turn 3 (calling math model) even though it failed?
- Turn 5 (calling GPT-5) that led to correction?
- Turn 1 (getting definition) that enabled everything?

**In policy gradient RL**: ALL actions in successful trajectory get reinforced
```python
for turn in trajectory:
    gradient += ∇log π(action_turn) × advantage
```

**Problem**: This can reinforce bad actions if they happened to be in successful trajectory.

**Partial solutions**:

**1. Temporal discounting** (not used in ToolOrchestra):
```python
for t, turn in enumerate(trajectory):
    discount = γ^(T-t)  # Earlier actions get less credit
    gradient += discount × ∇log π(action_t) × advantage
```

**2. Value-based advantage** (not used in ToolOrchestra):
```python
advantage_t = reward + V(state_{t+1}) - V(state_t)
# Only credit action for immediate improvement
```

**ToolOrchestra approach**: Rely on multiple rollouts
- Some rollouts will include the good action, some won't
- Good actions appear more often in successful rollouts
- GRPO advantage highlights actions that correlate with success
- Not perfect, but works in practice

**Open research question**: Can we do better credit assignment for long-horizon tool use?
- Counterfactual reasoning: "What if I hadn't called GPT-5?"
- Hindsight relabeling: "This failed trajectory would succeed if I'd called GPT-5 earlier"
- Attention-based credit: Use attention weights to assign credit

### Exploration vs. Exploitation in Tool Orchestration

**Classic RL dilemma**: 
- Explore: Try new actions to discover better strategies
- Exploit: Use known good actions to maximize reward

**In ToolOrchestra**:
- Explore: Try calling tools you haven't used much
- Exploit: Stick with tool combinations that work

**How RL encourages exploration**:

**Temperature parameter**:
```python
# During training rollouts
logits = model(context)
probs = softmax(logits / temperature)
action = sample(probs)
```

Higher temperature = more random = more exploration

**ToolOrchestra likely uses**:
- Temperature = 0.7-1.0 during training (not specified)
- Temperature = 0 during evaluation (deterministic)

**Entropy bonus** (common in RL, not clear if used here):
```python
entropy = -sum(p * log(p) for p in action_probs)
reward_with_bonus = reward + β * entropy
```

Encourages trying different actions, not always picking highest probability.

**The cost problem**: Exploration is expensive!
- Try calling GPT-5 → Costs $0.10
- Turns out it wasn't needed → Wasted money
- During training, this adds up

**Mitigation**:
- Use synthetic data (ToolScale) where API calls are free (simulated)
- Only evaluate on real benchmarks after training
- This is why synthetic data is crucial

### Catastrophic Forgetting

**The problem**: RL can make model forget what it learned in SFT.

**Example**:
- After SFT: Model can write code, do math, answer questions
- After RL: Model is great at orchestrating tools, but forgot how to do math directly

**Why it happens**:
- RL updates push model toward tool-use behaviors
- Non-tool-use skills don't get practiced during RL
- Gradient updates slowly degrade unused capabilities

**Solutions**:

**1. Replay buffer** (used in some RL systems):
```python
# Mix RL examples with SFT examples
training_batch = sample([
    *rl_rollouts,  # 80% RL data
    *sft_examples   # 20% original SFT data
])
```

**2. KL penalty to initialization**:
```python
loss = rl_loss + λ * KL(π_θ || π_pretrained)
```

Prevents policy from drifting too far from pre-trained model.

**3. Continual learning techniques**:
- Elastic Weight Consolidation (EWC): Penalize changing important weights
- Progressive Neural Networks: Add new parameters, keep old ones frozen

**ToolOrchestra approach**: Not explicitly stated
- Likely relies on: Model still sees diverse tasks during RL
- ToolScale has 10 domains, varied tasks
- Some tasks might require direct reasoning (without tools)
- This maintains general capabilities

**Evidence it works**: Model generalizes to unseen tools (Section 6.3)
- Suggests model retained general reasoning, not just tool-calling

---


## Conclusion

Looking back over this part, you should see how fragile long-horizon, tool-using RL can be without careful warm-starting, filtering, and stabilization—and why the training recipe is as important as the high-level algorithm. That perspective makes it easier to adapt the approach to your own infrastructure or extend it to even more complex orchestration setups.

## Academic Papers

109. **In-Context Learning**
     - Brown, T.B., et al. (2020). "Language Models are Few-Shot Learners." *NeurIPS 2020*
     - https://arxiv.org/abs/2005.14165

110. **Meta-Learning (MAML)**
     - Finn, C., Abbeel, P., & Levine, S. (2017). "Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks." *ICML 2017*
     - https://arxiv.org/abs/1703.03400

111. **Few-Shot Learning**
     - Snell, J., Swersky, K., & Zemel, R.S. (2017). "Prototypical Networks for Few-shot Learning." *NeurIPS 2017*
     - https://arxiv.org/abs/1703.05175

112. **Domain Adaptation**
     - Ganin, Y., & Lempitsky, V. (2015). "Unsupervised Domain Adaptation by Backpropagation." *ICML 2015*
     - https://arxiv.org/abs/1409.7495

113. **Compositional Generalization**
     - Lake, B.M., & Baroni, M. (2018). "Generalization without Systematicity: On the Compositional Skills of Sequence-to-Sequence Recurrent Networks." *ICML 2018*
     - https://arxiv.org/abs/1711.00350

114. **Transfer Learning**
     - Pan, S.J., & Yang, Q. (2010). "A Survey on Transfer Learning." *IEEE Transactions on Knowledge and Data Engineering*
     - https://ieeexplore.ieee.org/document/5288526

115. **Zero-Shot Learning**
     - Xian, Y., Lampert, C.H., Schiele, B., & Akata, Z. (2019). "Zero-Shot Learning—A Comprehensive Evaluation of the Good, the Bad and the Ugly." *IEEE TPAMI*
     - https://arxiv.org/abs/1707.00600

116. **Cost-Aware ML**
     - Bolukbasi, T., et al. (2017). "Adaptive Neural Networks for Efficient Inference." *ICML 2017*
     - http://proceedings.mlr.press/v70/bolukbasi17a.html

## Blog Posts and Tutorials

117. **Meta-Learning Explained**
     - Lilian Weng. "Meta-Learning: Learning to Learn Fast"
     - https://lilianweng.github.io/posts/2018-11-30-meta-learning/

118. **Compositional Generalization**
     - "Understanding Compositional Generalization in Neural Networks"
     - https://thegradient.pub/compositional-generalization/

119. **Transfer Learning Guide**
     - Sebastian Ruder. "Transfer Learning - Machine Learning's Next Frontier"
     - https://ruder.io/transfer-learning/

120. **Cost Optimization in ML**
     - "Optimizing Machine Learning Inference Costs"
     - https://aws.amazon.com/blogs/machine-learning/reduce-ml-inference-costs/

121. **Model Routing and Cascading**
     - "Frugal ML: How to Use Less but Get More"
     - https://anyscale.com/blog/llm-router-how-to-build-and-serve-an-llm-model-router

## GitHub Repositories

122. **Meta-Learning Implementations**
     - learn2learn (PyTorch meta-learning library)
     - https://github.com/learnables/learn2learn

123. **Domain Adaptation Code**
     - Transfer Learning Library
     - https://github.com/thuml/Transfer-Learning-Library

124. **Cost-Aware Serving**
     - LiteLLM (Multi-provider LLM gateway with cost tracking)
     - https://github.com/BerriAI/litellm

125. **Model Routing**
     - RouteLLM
     - https://github.com/lm-sys/RouteLLM

126. **Frugal ML**
     - https://github.com/facebookresearch/FrugalML

---

