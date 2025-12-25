# The Orchestration Paradigm Series: Dive 6
# The Stability/Plasticity Dilemma

> [!NOTE]
> **System Auditor's Log:** Training an 8B parameters model with Reinforcement Learning is notoriously unstable. The model often experiences "catastrophic forgetting" or "reward hacking," where it maximizes the reward metric by degenerating into gibberish. The "infrastructure" described in the paper is not just about speed; it's about forcing convergence on a chaotic loss landscape.

The paper mentions using **16 H100 GPUs**. This is not just a flex; it is a mathematical necessity for **Variance Reduction**.

## The Variance Problem

In Policy Gradient methods (like GRPO), the gradient estimate is noisy.
$$ \nabla J \approx \frac{1}{N} \sum (R_i - b) \nabla \log \pi(a_i|s_i) $$

If the batch size ($N$) is small, the variance of this estimate is high. One "lucky" random rollout where the model guesses the right answer can trigger a massive weight update, pushing the model into a region of the parameter space that ruins its general capabilities.

To stabilize this, you need a massive batch size. You need to average over hundreds of trajectories to find the "true" direction of improvement.
*   **16 H100s** allow for a global batch size that is statistically significant.
*   **Gradient Accumulation** further virtually increases this batch size.

## Context Packing: The Silent Efficiency Hack

One specific engineering detail mentioned is **Sequence Packing** (or "packing with attention masking").

Orchestration data is " jagged."
*   Trajectory A: 500 tokens (simple lookup).
*   Trajectory B: 12,000 tokens (complex debugging).

If you pad everything to 12k tokens, you are computing attention over 95% padding tokens for Trajectory A. This wastes massive amounts of compute.

**Packing** concatenates multiple short sequences into a single 12k context window.
`[Traj A] [Traj C] [Traj D] ...`
Crucially, the **Attention Mask** must be block-diagonal. Tokens in Traj A must not "attend" to tokens in Traj C.

```python
# The Concept of Attention Masking for Packed Sequences
# Without this, the model gets confused by cross-contamination between unrelated tasks.

def create_packed_mask(sequences):
    # Create a 2D mask where 1 = attend, 0 = ignore
    
    total_len = sum(len(s) for s in sequences)
    mask = torch.zeros((total_len, total_len))
    
    current_idx = 0
    for seq in sequences:
        end_idx = current_idx + len(seq)
        
        # Block diagonal: Allow attention only within the local sequence
        mask[current_idx:end_idx, current_idx:end_idx] = 1 
        
        current_idx = end_idx
        
    return mask
```

If this mask implementation has a bug (e.g., off-by-one error), the model effectively learns to hallucinate based on unrelated data.

## The Update Ratio

Another key hyperparameter is the **Update Ratio** between the Policy Model and the Reference Model.
The Reference Model (the frozen copy) must be kept in VRAM to compute the KL divergence penalty. This effectively halves the available memory for training.

This forces a trade-off:
1.  **Offload Reference Model:** Save VRAM, but kill throughput (PCIe bottleneck).
2.  **Keep in VRAM:** Fast training, but limits batch size (increasing variance).

ToolOrchestra chooses **FSDP (Fully Sharded Data Parallel)** to shard *both* models across the 16 GPUs. This implies that the network interconnect (NVLink) is the hard bottleneck of the entire training run. If NVLink is saturated, those H100s sit idle.

---

## Annotated Bibliography

1.  **Zhao et al. (2023)** - *PyTorch FSDP: Experiences on Scaling Llama 2 Training*: Technical deep dive into Sharded Data Parallelism. Essential for understanding why the 16-GPU cluster is a hard requirement, not just a speedup.
2.  **Dao (2023)** - *FlashAttention-2*: The algorithm that makes long-context training (like Trajectory Packing) mathematically feasible by reducing memory complexity from $O(N^2)$ to linear.
3.  **Ding et al. (2024)** - *The Efficiency of Packing*: Analyzing the "block-diagonal masking" technique for sequence packing, highlighting the implementation risks of mask leakage.
