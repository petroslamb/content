# The Orchestration Paradigm Series: Dive 8
*How do you adapt to user priorities without retraining?*

## Introduction

Different users want different things. A researcher with grant funding cares about accuracy above all—cost is irrelevant. A startup operating on thin margins needs good-enough results at minimal cost. A real-time application needs answers within 2 seconds regardless of other considerations. How can a single trained orchestrator serve all of them?

ToolOrchestra's answer is preference conditioning: training the orchestrator to adapt its behavior based on a preference vector that specifies the user's priorities. At inference time, users provide their preferences, and the orchestrator adjusts without retraining. This dive explains how preference learning works and why it's essential for deployment.

---

## 🌊 Surface Level: Customization Without Retraining

Think of a mixing console in a recording studio. The song is recorded, but the mix can be adjusted: more bass, less reverb, louder vocals. Each listener's preference is different. Rather than recording a separate version for everyone, you record once and mix to taste.

ToolOrchestra works similarly. The orchestrator is trained once on diverse tasks and preferences. At deployment, users specify their priorities using a preference vector. The orchestrator adjusts its behavior—favoring cheap tools for cost-conscious users, expensive-but-accurate tools for quality-focused users, fast tools for latency-sensitive users.

The preference vector is simple: a set of weights indicating how much the user cares about each dimension. Common dimensions include:

**Accuracy weight**: How important is getting the right answer?  
**Cost weight**: How important is minimizing expenses?  
**Latency weight**: How important is responding quickly?  

A cost-focused user might set P = [0.5, 1.0, 0.3], meaning cost matters most. An accuracy-focused user might set P = [1.0, 0.2, 0.2], meaning accuracy dominates. The same orchestrator, trained once, responds appropriately to both.

This is not just convenience—it's practical necessity. Retraining for each user's preferences would be prohibitively expensive. A system that can adapt at inference time from a single training run is deployable at scale.

---

## 🏊 Shallow Dive: How Preferences Change Behavior

Let's trace how preference vectors influence orchestrator decisions through a concrete example.

**Task**: "What is the market cap of Apple Inc. as of close of trading yesterday?"

**User A (accuracy-focused, P = [1.0, 0.2, 0.2])**: The orchestrator prioritizes getting the correct answer. It might:
- Call web search to get current data (free, but might have stale information)
- Call a financial API for authoritative data ($0.05 per call)
- Cross-verify with a second source ($0.05 more)
- Total cost: $0.10, but high confidence in accuracy

**User B (cost-focused, P = [0.5, 1.0, 0.3])**: The orchestrator prioritizes minimizing cost. It might:
- Call web search (free)
- If search returns a confident answer, output immediately
- No verification, no premium APIs
- Total cost: $0.001, accepted risk of slightly stale data

**User C (latency-focused, P = [0.5, 0.3, 1.0])**: The orchestrator prioritizes fast response. It might:
- Try local cache first (instant, if available)
- If no cache, call the single fastest tool (web search, ~200ms)
- Output immediately without verification
- Total latency: <500ms

Same task, same orchestrator, different behaviors. The preference vector doesn't just adjust the reward calculation during training—it's provided as input at inference time, and the orchestrator has learned to condition its behavior on this input.

### The Mechanism: Preference as Input

The preference vector P is prepended to the context at each turn. The orchestrator sees:

```
User preference: [accuracy=1.0, cost=0.2, latency=0.2]
Task: What is the market cap of Apple Inc. as of close of trading yesterday?
Available tools: [web_search, financial_api, local_cache, ...]
```

During training, P varies across examples—sometimes cost-focused, sometimes accuracy-focused, sometimes balanced. The orchestrator learns to parse P and adjust its decisions accordingly.

This is a form of in-context learning applied to preferences. Just as LLMs learn to follow instructions provided in context, the orchestrator learns to follow preference specifications provided in context.

---

## 🤿 Deep Dive: Mathematics of Preference Alignment

### Preference-Conditioned Policy

The orchestrator's policy is conditioned on the preference vector:

π(action | state, P)

where P ∈ ℝ^d is the preference vector and d is the number of preference dimensions.

During training, P is sampled for each task (typically uniformly from a reasonable range). The reward depends on P:

R(trajectory | P) = P · M_normalized(trajectory)

where M is the normalized metric vector (accuracy, cost efficiency, latency efficiency).

This training signal teaches the policy to produce different behaviors for different P values. High accuracy weight → favor high-accuracy tool choices. High cost weight → favor low-cost tool choices.

### Why Preference Conditioning Works

The key property enabling this is **preference awareness**—the policy must represent P sufficiently in its internal computations to produce P-appropriate behaviors.

The attention mechanism in transformers naturally supports this. When P is in the context, attention heads can attend to it when making tool selection decisions. If the context contains "cost=1.0" (high cost sensitivity), attention to this token when deciding between "call GPT-5" versus "call local model" can shift probabilities toward the cheaper option.

**Ablation evidence**: When preferences are omitted from the context at inference time, orchestrator behavior defaults to training-average preferences—reasonable but not personalized. This confirms that the preference vector is actively used, not ignored.

### Generalization to Unseen Preferences

A critical question: does the orchestrator generalize to preference values not seen during training?

Training might sample accuracy weights uniformly from [0.3, 1.0]. What happens if a user specifies accuracy=1.5 (extra-high accuracy priority)?

**Interpolation**: Preferences between training values should generalize well. A preference of P=[0.7, 0.5, 0.3] wasn't an exact training example but represents a blend of nearby examples. The learned policy interpolates smoothly.

**Extrapolation**: Preferences beyond training range are less reliable. P=[2.0, 0.1, 0.1] (extreme accuracy priority) might produce unexpected behavior because the policy wasn't trained to represent such values. In practice, reasonable clamping to training ranges ensures expected behavior.

**Normalization helps**: Because preferences are normalized before being used in reward computation, the relative ratios matter more than absolute values. [1.0, 0.2, 0.2] behaves similarly to [5.0, 1.0, 1.0] because the ratios are the same.

---

## 🔬 Research Depth: Connections and Extensions

### Inverse Reinforcement Learning

ToolOrchestra assumes preferences are stated explicitly. But what if users can't articulate their preferences?

**Inverse Reinforcement Learning (IRL)** addresses this by inferring rewards from observed behavior. Given examples of a user's choices (which tool they manually selected, which answers they approved), IRL algorithms infer a preference vector that explains those choices.

The inferred P could then be used with ToolOrchestra's preference-conditioned policy, enabling personalization without explicit preference specification.

**Main challenge**: IRL requires observing enough user behavior to reliably infer preferences. In cold-start settings (new users with no history), some default or weakly-personalized behavior is necessary.

### Preference Learning from Comparisons

Another approach: learn preferences from comparative judgments rather than explicit weights.

"Which orchestration trajectory do you prefer: A (accurate but slow) or B (fast but uncertain)?"

The **Bradley-Terry model** represents preferences for pairwise comparisons:

P(A preferred to B) = σ(score(A) - score(B))

where σ is the sigmoid function and score is a learned function mapping trajectories to scalar values.

This is the foundation of RLHF (Reinforcement Learning from Human Feedback). A reward model learns to assign scores such that human-preferred trajectories score higher. The learned reward model can then be used to optimize orchestrator policies.

ToolOrchestra doesn't use RLHF directly—it uses explicit preference vectors—but the techniques are compatible. Future systems might combine explicit preference specification (for known priorities) with comparison-based learning (for subtle preferences users can't articulate).

### Multi-Stakeholder Preferences

Real deployments involve multiple stakeholders with different priorities:

**End users** want accurate, fast, helpful responses.
**Developers** want efficient, cost-effective operation.
**Organizations** want safe, compliant, on-brand behavior.
**Society** wants privacy, fairness, and beneficial outcomes.

How should these competing interests be balanced?

**Aggregation approaches** include:

**Weighted average**: Combine stakeholder preferences with negotiated weights. Simple but requires agreement on weights.

**Constraint-based**: Satisfy hard constraints (safety, compliance) while optimizing soft preferences (cost, speed). Treats stakeholder interests as hierarchical.

**Pareto negotiation**: Find solutions that no stakeholder can improve without hurting another. Fair but may not have unique solutions.

These are fundamentally governance questions—technical infrastructure enables many aggregation schemes, but choosing among them requires social/organizational decisions.

ToolOrchestra's technical contribution is making preferences explicit and modulable. The choice of which preferences to optimize is delegated to deployment contexts.

### Temporal and Contextual Preferences

Static preference vectors assume priorities don't change. Real preferences are dynamic:

**Temporal variation**: A user might be cost-conscious during exploratory research (many low-value queries) but accuracy-focused during final report writing (fewer high-stakes queries).

**Contextual variation**: Preferences for the same user might depend on task type, time pressure, or recent experiences.

**Adaptive approaches** could:

- Track preference history and adjust defaults based on patterns
- Infer current preferences from session context ("The user seems rushed—prioritize speed")
- Allow per-query preference adjustment ("For this question, maximize accuracy")

These extensions are natural for future work but not implemented in ToolOrchestra's current form.

---

## Conclusion

Preference conditioning makes ToolOrchestra deployable. Without it, each user population would require separate training—impractical at scale. With it, a single trained orchestrator serves diverse users by adapting its behavior based on provided preference vectors.

The mathematics are straightforward: preferences weight the multi-objective reward, and the policy learns to produce behavior that optimizes the weighted objective. The generalization is robust: interpolation between training preferences works well, and normalization makes exact values less critical than ratios.

Future extensions—inverse RL for implicit preferences, comparison-based learning for subtle preferences, multi-stakeholder aggregation for complex deployments—build naturally on this foundation. The current system is complete for explicit preference specification; extensions address the harder cases where preferences must be inferred or negotiated.

The next dive examines whether these learned behaviors generalize—whether the orchestrator works on tools, prices, and tasks never seen during training.

---

## References

### Preference Learning

1. **Preference Learning**
   - Fürnkranz, J., & Hüllermeier, E. (2010). "Preference Learning." Springer
   - https://link.springer.com/book/10.1007/978-3-642-14125-6

2. **Bradley-Terry Model**
   - Bradley, R.A., & Terry, M.E. (1952). "Rank Analysis of Incomplete Block Designs." *Biometrika*
   - https://www.jstor.org/stable/2334029

### Inverse Reinforcement Learning

3. **IRL Survey**
   - Ng, A.Y., & Russell, S. (2000). "Algorithms for Inverse Reinforcement Learning." *ICML 2000*
   - https://ai.stanford.edu/~ang/papers/icml00-irl.pdf

4. **Maximum Entropy IRL**
   - Ziebart, B.D., et al. (2008). "Maximum Entropy Inverse Reinforcement Learning." *AAAI 2008*
   - https://www.aaai.org/Papers/AAAI/2008/AAAI08-227.pdf

### RLHF

5. **Learning from Human Preferences**
   - Christiano, P.F., et al. (2017). "Deep Reinforcement Learning from Human Preferences." *NeurIPS 2017*
   - https://arxiv.org/abs/1706.03741

6. **InstructGPT**
   - Ouyang, L., et al. (2022). "Training Language Models to Follow Instructions with Human Feedback." *NeurIPS 2022*
   - https://arxiv.org/abs/2203.02155

### Multi-Objective Preferences

7. **Multi-Objective RL**
   - Roijers, D.M., et al. (2013). "A Survey of Multi-Objective Sequential Decision-Making." *JAIR*
   - https://arxiv.org/abs/1402.0590

8. **Social Choice Theory**
   - Arrow, K.J. (1951). "Social Choice and Individual Values." Wiley
   - Classic text on aggregating preferences

---
