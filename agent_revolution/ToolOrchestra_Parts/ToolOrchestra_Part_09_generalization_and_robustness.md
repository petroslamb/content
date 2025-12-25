# The Orchestration Paradigm Series: Dive 9
*Does it work on tools it's never seen?*

## Introduction

Every machine learning system faces the same existential question: does it work outside the training distribution? A model that only performs well on exactly the kind of data it was trained on is useless in practice, because real-world data never perfectly matches training data.

ToolOrchestra confronts this question in an unusually stark form. The orchestrator learns to coordinate a specific set of tools at specific prices in specific configurations. What happens when you hand it different tools? Different prices? Completely different types of tasks? If the answer is "it breaks," then ToolOrchestra is an interesting research artifact but not a deployable system. If the answer is "it adapts," then something deeper is happening—the orchestrator has learned generalizable coordination skills, not just memorized patterns.

This dive examines what happens when ToolOrchestra leaves the comfort of its training environment. The results are surprisingly strong, and understanding them reveals what the orchestrator has actually learned.

---

## 🌊 Surface Level: The Acid Test

Here is the fundamental challenge. ToolOrchestra was trained on a specific configuration: GPT-5, several Qwen models, code interpreters, and search tools, all at TogetherAI's pricing. Every training example used these tools, these prices, these capabilities.

Now consider deployment scenarios:

**Scenario 1: A new model releases.** Claude Opus 4.1 wasn't in training. Should the orchestrator know how to use it? What about specialized models like Codestral for code or OpenMath-Llama for mathematics?

**Scenario 2: Prices change.** Cloud providers adjust pricing constantly. Next month, GPT-5 might cost twice as much. Next year, it might cost half. Can the orchestrator adapt without retraining?

**Scenario 3: Task domains shift.** Training was on ToolScale (database operations, customer service, scheduling) and HLE (academic questions). What about medical diagnosis? Legal research? Scientific experiment design?

The paper tests the first two scenarios explicitly. Scenario 3 is tested implicitly through the benchmark diversity. The results are encouraging across all three—and understanding why requires understanding what the orchestrator actually learned.

---

## 🏊 Shallow Dive: Three Types of Generalization

### Unseen Tools: The Description-Based Matching

The most dramatic test: give ToolOrchestra tools it has literally never seen during training, and measure whether it can still orchestrate effectively.

**The experimental setup.** Section 6.3 of the paper replaces training tools with alternatives: Claude Opus 4.1 instead of GPT-5, o3-mini instead of Qwen, Codestral instead of Qwen-Coder, OpenMath-Llama instead of Qwen-Math. The orchestrator has never seen these tools, has never generated calls to them, has never observed their responses.

**The results.** On HLE (Humanity's Last Exam), performance drops from 37.1% with familiar tools to 22.0% with unfamiliar ones. That's a 15.1% absolute drop—significant but not catastrophic. And crucially, 22.0% with unfamiliar tools still beats GPT-5 alone (16.4%) and Claude alone (17.8%). The orchestrator coordinating unfamiliar tools outperforms familiar models working in isolation.

**How is this possible?** The orchestrator never saw Claude during training. It never learned "call Claude for difficult reasoning tasks." Yet it successfully routes to Claude when appropriate. Something generalizable was learned.

The mechanism appears to be description-based matching. Each tool comes with a description explaining its capabilities. The orchestrator processes these descriptions and matches them to task requirements. "Claude Opus 4.1: Advanced reasoning model with strong performance on complex analytical tasks." When the orchestrator encounters a complex analytical task, it recognizes the match—not because it memorized the tool name, but because it learned the pattern "complex reasoning → advanced reasoning model."

### Unseen Pricing: Relative Not Absolute

A subtler test: keep the tools the same but change their prices. This tests whether the orchestrator memorized absolute costs ("GPT-5 costs $0.03 per call") or learned relative cost reasoning ("GPT-5 is expensive compared to local tools").

**The experimental setup.** Appendix H describes training with TogetherAI pricing and testing with DeepInfra pricing. The relative orderings are similar (GPT-5 is more expensive than small models) but the absolute values differ significantly.

**The results.** HLE accuracy drops from 37.1% to 36.9%—a 0.2% difference that's within noise. The orchestrator adapts to new pricing essentially perfectly.

**Why does this work so well?** The most likely explanation is that the orchestrator learned cost-aware decision patterns at a relative level. It learned "start with cheap tools, escalate to expensive ones if needed" rather than "start with tools costing less than $0.001." As long as the relative orderings are similar, the learned patterns transfer.

This is good news for deployment. Prices change constantly. An orchestrator that needed retraining with every pricing update would be impractical. An orchestrator that generalizes to similar relative orderings is deployable.

### Unseen Task Types: Compositional Transfer

The benchmarks themselves test task generalization, though less systematically than tool and price generalization.

**Training domain:** ToolScale covers 10 domains—airline, finance, retail, human resources, hospitality, academic, media, software, manufacturing, and government. These involve database operations, scheduling, customer service, and multi-step procedural tasks.

**Test domains:** HLE contains PhD-level academic questions across sciences and humanities. FRAMES tests factual reasoning with multi-hop questions. τ²-Bench tests customer service dialogues. None of these exactly matches ToolScale's training distribution.

**The results.** Strong performance across all three benchmarks suggests the orchestrator learned general orchestration strategies, not domain-specific heuristics. The pattern "search for factual information, compute to verify, escalate for difficult reasoning" transfers across domains because it's about task structure, not domain content.

---

## 🤿 Deep Dive: Mechanisms of Generalization

The empirical results establish that generalization happens. But how? Several mechanisms likely contribute.

### Description-Based Tool Understanding

The most important mechanism is the orchestrator's ability to understand tool descriptions rather than memorize tool names.

Consider a training example where the orchestrator learns: "For mathematical proofs, call Qwen2.5-Math-72B." If this were the full extent of learning, it wouldn't transfer to OpenMath-Llama because the names don't match. But the actual learning is more nuanced: "For mathematical proofs, look for tools described as strong at formal mathematical reasoning."

At test time, the orchestrator sees a new tool description: "OpenMath-Llama: Specialized for mathematical problem solving including algebraic manipulation, geometry, and formal proofs." The tokens "formal proofs" trigger the same attention patterns as during training. The orchestrator routes appropriately despite never having seen this tool.

This is essentially a form of in-context learning applied to tool coordination. The model uses its general language understanding to interpret tool descriptions and match them to task requirements. The orchestration skill is learned (when to call a math model); the application to specific tools is inferred from context.

### Abstract Strategy Learning

Beyond matching task types to tool types, the orchestrator learns abstract orchestration strategies that transfer across configurations.

**Strategy 1: Cost escalation.** Start with cheap tools, escalate to expensive ones only if needed. This strategy doesn't depend on which specific tools are cheap or expensive—it's a meta-pattern that applies whenever tools have varying costs.

**Strategy 2: Verification.** When uncertain, cross-check with a different tool or method. This doesn't depend on which tools exist—it's about the structure of uncertainty reduction.

**Strategy 3: Specialization matching.** For specialized tasks, prefer specialized tools. For general tasks, prefer general tools. This pattern transfers to any tool configuration that has some specialized and some generalist options.

These strategies are learned implicitly through the reward signal. Rollouts that use cost escalation tend to achieve good cost-efficiency. Rollouts that verify tend to achieve good accuracy. The gradient updates reinforce these patterns without ever explicitly representing them as rules.

### In-Context Adaptation

The orchestrator's long context window (24,000 tokens) enables within-episode learning. If the first tool call fails, the orchestrator observes the failure and adjusts subsequent calls. This is adaptation without parameter updates—pure in-context learning.

Consider a scenario where the orchestrator calls an unfamiliar tool and receives an unexpectedly poor response. In the next turn, it might try a different tool, or approach the problem differently. This trial-and-error adaptation happens within single episodes, requiring no retraining.

Evidence for this mechanism: the 15% performance drop with unfamiliar tools is smaller than expected if the orchestrator were purely memorizing tool behaviors. Some of that gap is closed by within-episode adaptation—learning what the new tools can and cannot do by observing their first few responses.

---

## 🔬 Research Depth: Generalization Theory and Limits

### What Learning Theory Tells Us

From a learning theory perspective, ToolOrchestra's generalization can be understood through the lens of sample complexity and distribution shift.

**Sample complexity.** The orchestrator was trained on approximately 4,000 tasks × 100+ tool configurations = 400,000+ training examples. This dense coverage of the joint (task, configuration) space enables interpolation: when faced with a new point, there are nearby training points to draw from.

**Distribution shift.** Tool and price changes create covariate shift (the input distribution changes) but not concept shift (the relationship between inputs and optimal actions remains similar). A tool described as "good at math" should be called for math problems regardless of which specific tool it is. Because the underlying decision rule is stable, the learned policy transfers.

These theoretical perspectives align with the empirical findings. Dense training coverage plus stable decision rules equals robust generalization.

### Where Generalization Fails

The paper doesn't emphasize failure modes, but they surely exist. Understanding the limits helps practitioners know when to expect problems.

**Radically different tool types.** The training tools are language models, search engines, and code interpreters. If you introduced a completely novel tool type—say, a robotic arm or a chemical simulation—the orchestrator might struggle to route appropriately because its training included nothing similar.

**Inverted price structures.** The generalization to new pricing assumes relative orderings are similar. If a future configuration made GPT-5 cheaper than local tools, the learned cost-escalation strategies would become counterproductive.

**Adversarial descriptions.** Tool descriptions are assumed to be accurate. A malicious tool with a misleading description ("Expert at mathematics" for a tool that actually can't do math) would receive inappropriate calls. The orchestrator doesn't verify claims; it trusts descriptions.

**Extreme distribution shift.** The benchmarks test distributions that, while different from training, are not wildly different. HLE is academic questions; ToolScale had academic domains. Future benchmarks with truly alien task distributions (physical world reasoning? formal theorem proving? multi-week projects?) might reveal limits not yet observed.

### Toward Formal Guarantees

Currently, generalization claims are empirical: "it worked on these benchmarks." Stronger claims would require formal guarantees, which remain elusive for neural networks generally and RL systems specifically.

One path toward guarantees: characterize the class of tool configurations over which learned policies are optimal. If we could define a "similar enough" criterion—configurations where descriptions, costs, and capabilities follow patterns seen in training—we might prove that policies generalize to all similar-enough configurations.

Another path: composition guarantees. If the orchestrator learns modular skills (cost reasoning, task-tool matching, verification), and if those modules compose correctly, then generalization to new combinations might be provable. Compositional generalization theory exists but hasn't been applied to orchestration.

Both paths are speculative. For now, empirical validation remains the primary evidence that generalization works.

---

## What This Means For Deployment

The generalization results have practical implications for anyone considering ToolOrchestra-style systems.

**Tool updates are okay.** You don't need to retrain when providers release new models. As long as new tools have informative descriptions, the orchestrator can route to them appropriately. Performance might be slightly suboptimal (the 15% gap with unfamiliar tools), but it won't break.

**Price changes are okay.** You definitely don't need to retrain when prices shift. The orchestrator's relative cost reasoning transfers almost perfectly. This makes deployment practical in environments where pricing is volatile.

**Domain expansion requires caution.** Moving to dramatically new task types may require additional training or fine-tuning. The generalization is good but not unlimited. Validate on new domains before deploying.

**Description quality matters.** Since routing decisions depend on parsing tool descriptions, those descriptions must be accurate and informative. Vague descriptions ("A useful model") or inaccurate ones ("Expert at X" for something bad at X) will degrade routing quality.

---

## Conclusion

The answer to "does it work on tools it's never seen?" is a qualified yes. ToolOrchestra's coordination strategies transfer robustly to new tools with similar capabilities, new prices with similar relative orderings, and new task domains with similar structures. The qualification is that dramatic departures from training—radically novel tool types, inverted cost structures, or adversarial configurations—may break generalization.

What does the orchestrator actually learn? Not a lookup table mapping tool names to situations. Rather, it learns how to read tool descriptions and match capabilities to requirements. It learns abstract strategies—cost escalation, verification, specialization matching—that apply across configurations. And it learns to adapt within episodes when initial approaches don't work.

This generalization is what makes ToolOrchestra a practical system rather than a benchmarking curiosity. Real deployments involve tool updates, price changes, and novel tasks. A system that requires retraining for each such change would be impractical. A system that adapts gracefully is deployable.

The next dive examines what happens when we look backward rather than outward: where does ToolOrchestra fit in the landscape of prior work, and what future directions does it point toward?

---

## References

### Generalization Theory

1. **PAC Learning**
   - Valiant, L.G. (1984). "A Theory of the Learnable." *Communications of the ACM*, 27(11), 1134-1142
   - https://dl.acm.org/doi/10.1145/1968.1972

2. **VC Dimension**
   - Vapnik, V.N., & Chervonenkis, A.Y. (1971). "On the Uniform Convergence of Relative Frequencies." *Theory of Probability & Its Applications*
   - https://epubs.siam.org/doi/10.1137/1116025

3. **Rademacher Complexity**
   - Bartlett, P.L., & Mendelson, S. (2002). "Rademacher and Gaussian Complexities." *Journal of Machine Learning Research*, 3, 463-482
   - https://www.jmlr.org/papers/v3/bartlett02a.html

### Distribution Shift

4. **Dataset Shift in Machine Learning**
   - Quionero-Candela, J., et al. (2009). MIT Press
   - https://mitpress.mit.edu/9780262170055/

5. **WILDS Benchmark**
   - Koh, P.W., et al. (2021). "WILDS: A Benchmark of in-the-Wild Distribution Shifts." *ICML 2021*
   - https://arxiv.org/abs/2012.07421

### In-Context Learning

6. **Language Models are Few-Shot Learners (GPT-3)**
   - Brown, T., et al. (2020). *NeurIPS 2020*
   - https://arxiv.org/abs/2005.14165

7. **In-Context Learning Survey**
   - Dong, Q., et al. (2022). "A Survey on In-Context Learning." *arXiv:2301.00234*
   - https://arxiv.org/abs/2301.00234

### Compositional Generalization

8. **SCAN Benchmark**
   - Lake, B.M., & Baroni, M. (2018). "Generalization without Systematicity." *ICML 2018*
   - https://arxiv.org/abs/1711.00350

9. **Compositional Generalization Survey**
   - Hupkes, D., et al. (2020). "Compositionality Decomposed." *arXiv:1908.08351*
   - https://arxiv.org/abs/1908.08351

### Robustness

10. **Out-of-Distribution Detection in NLP**
    - Yang, J., et al. (2024). "A Survey on Out-of-Distribution Detection." *arXiv:2305.03236*
    - https://arxiv.org/abs/2305.03236

---
