# Dive 1: The Fundamental Problem
## Introduction

This part introduces the core coordination problem that ToolOrchestra is designed to solve and explains why simply prompting large models to act as orchestrators leads to systematic biases. It sets up the conceptual lens for the rest of the series by contrasting raw model capability with the separate skill of making good tool-usage decisions.


## 🌊 Surface Level: What Problem Are We Solving?

Imagine you need to solve a really hard math problem. You have three options:

1. **Hire Einstein** (expensive, takes time, but very capable)
2. **Hire a college student** (cheap, fast, but limited)
3. **Hire a coordinator** who knows when to call Einstein vs. the college student vs. use a calculator

ToolOrchestra is option 3. It trains a small AI model to be that coordinator, calling bigger, more expensive AI models only when necessary.

**Current Problem**: When we tell GPT-5 "be a coordinator," it makes poor decisions:
- It calls its own variants (GPT-5-mini) even when other tools would be better
- Smaller models call GPT-5 for everything, wasting money
- No model properly balances cost, speed, and accuracy

## 🏊 Shallow Dive: Why Existing Approaches Fail

Let's understand the biases in detail:

### Self-Enhancement Bias
**What happens**: GPT-5, when asked to coordinate tools including GPT-5-mini, calls mini 73% of the time.

**Why this is bad**: Imagine a manager who only delegates to their sibling, regardless of whether they're the right person for the job. That's what's happening here.

**Root cause**: The model was trained to produce outputs similar to its training data, which likely included many examples of GPT-5-mini outputs (since they come from the same organization). It has an implicit preference for "familiar" patterns.

### Other-Enhancement Bias
**What happens**: Qwen3-8B, when given access to GPT-5, calls it 73% of the time, even for simple tasks.

**Why this is bad**: Imagine an intern who always asks the CEO for help, even when they could handle it themselves or ask a mid-level manager.

**Root cause**: The model has learned (correctly) that GPT-5 is very capable, but hasn't learned the cost-benefit analysis. It optimizes for "highest probability of success" without considering resource constraints.

### The Instruction-Following Paradox
**The twist**: Both models were explicitly told to "balance performance and cost" in their prompts!

**Why prompts fail here**: Language models follow patterns from training data. If training data doesn't contain examples of "coordinate models stronger than yourself while considering cost," the prompt alone can't teach this behavior. It's like trying to teach someone to ride a bike by just describing it—they need actual practice with feedback.

## 🤿 Deep Dive: The Formal Problem Setup

Let's formalize why this is hard using mathematical frameworks:

### The Coordination Problem as a Sequential Decision Problem

Traditional tool use: Model M makes one-shot decisions
```
M: Input → [Tool_1, Tool_2, Tool_3] → Choose One → Output
```

Orchestration problem: Model M must coordinate over time, including models M' where capability(M') > capability(M)

```
M: Input → Plan → [Call M', Call Tool, Self-Solve] → Observe → Re-plan → ...
```

**The key difficulty**: The orchestrator M must meta-reason about:
1. Its own capabilities vs. available tools
2. The cost-benefit of delegating vs. solving directly
3. The dependencies between subtasks (can only call expensive tool after cheap tool gathers information)
4. User preferences that may conflict (fast + accurate + cheap—pick two!)

### Why This Isn't Standard Reinforcement Learning

In standard RL: Agent learns policy π(a|s) where action space A is fixed

In orchestration: 
- Action space is dynamic (available tools change)
- Actions have different costs and latencies (not uniform)
- Rewards are multi-dimensional (accuracy, cost, latency, preferences)
- The environment includes other agents (called models) whose behaviors aren't fully known

This is closer to **hierarchical RL** meets **multi-objective optimization** meets **mechanism design**.

## 🔬 Research Depth: Connections to Broader AI Research

### Connection 1: The Agency vs. Capability Distinction

Recent work distinguishes:
- **Capability**: What can the model do in principle?
- **Agency**: What does the model actually do in practice?

Example: GPT-5 has the capability to use tools efficiently, but lacks the agency (learned behavior) to do so without explicit training.

**Key Paper**: Belcak et al. (2025) "Small language models are the future of agentic AI"
- **Main claim**: For agentic tasks (planning, tool selection, coordination), model size matters less than training objective
- **Evidence**: 8B models with proper RL training outperform 70B+ models with supervised fine-tuning
- **Why**: Agentic behavior requires trial-and-error learning (RL), not pattern matching (SFT)

### Connection 2: The Exploration-Exploitation Trade-off in New Settings

Classic RL: Balance exploring new states vs. exploiting known good strategies

Orchestration RL: Must also meta-explore:
- "Should I try calling this expensive model I haven't used much?"
- "Should I experiment with a new tool sequence?"
- But exploration is expensive (literally costs money)

**Key Paper**: Zhou et al. (2024) "ARCHER: Training language model agents via hierarchical multi-turn RL"
- **Main contribution**: Hierarchical RL for LLM agents where high-level policy chooses subgoals, low-level policy executes
- **Relevance**: ToolOrchestra can be seen as hierarchical—orchestrator chooses which tool/model, that tool/model executes the subtask
- **Difference**: ARCHER focuses on single-model hierarchy, ToolOrchestra on multi-model coordination

### Connection 3: Weak-to-Strong Generalization (Inverted)

**Classic Weak-to-Strong**: Can weak supervisors train strong models?
- Paper: Burns et al. (2024) OpenAI
- Setup: Use GPT-2-level labels to fine-tune GPT-4
- Finding: Strong models can learn beyond weak supervision

**ToolOrchestra's Inversion**: Can weak orchestrators command strong models?
- Setup: 8B model coordinates GPT-5, Claude Opus
- Finding: Yes, if trained with RL to learn when/how to delegate
- Implication: Intelligence hierarchy isn't linear—coordination is orthogonal to raw capability

### Open Research Questions

1. **Recursive Orchestration**: Can orchestrators coordinate other orchestrators? What's the optimal hierarchy depth?

2. **Dynamic Tool Discovery**: Current system has fixed tool sets. Can orchestrators learn to discover and integrate new tools at test time? This relates to **continual learning** and **few-shot adaptation**.

3. **Adversarial Robustness**: What if a called tool gives misleading information? How should orchestrators handle unreliable tools?

4. **Social Choice Theory**: When user preferences conflict (want accurate AND cheap), how should orchestrators make trade-offs? This connects to **multi-objective optimization** and **Pareto efficiency**.

---


## Conclusion

In summary, this part reframes orchestration as its own learning problem, separate from simply making models larger or better at next-token prediction. You should come away with a clear picture of the biases in naive orchestration and a set of motivating questions that the later parts—on RL, rewards, data, and infrastructure—are designed to answer.

## Academic Papers

1. **ToolOrchestra (Main Paper)**
   - Su, H., Diao, S., Lu, X., et al. (2025). "ToolOrchestra: Elevating Intelligence via Efficient Model and Tool Orchestration." *arXiv:2511.21689*
   - https://arxiv.org/abs/2511.21689

2. **Self-Enhancement Bias**
   - Salewski, L., Alaniz, S., Rio-Torto, I., et al. (2024). "In-Context Impersonation Reveals Large Language Models' Strengths and Biases." *arXiv:2305.14930*
   - https://arxiv.org/abs/2305.14930

3. **Model Biases in Tool Selection**
   - Qin, Y., Liang, S., Ye, Y., et al. (2023). "ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs." *arXiv:2307.16789*
   - https://arxiv.org/abs/2307.16789

4. **Weak-to-Strong Generalization**
   - Burns, C., Izmailov, P., Kirchner, J.H., et al. (2024). "Weak-to-Strong Generalization: Eliciting Strong Capabilities with Weak Supervision." *ICML 2024*
   - https://arxiv.org/abs/2312.09390

5. **Small Models for Agency**
   - Belcak, P., & Wattenhofer, R. (2025). "Small Language Models are the Future of Agentic AI." *arXiv:2506.02153*
   - https://arxiv.org/abs/2506.02153

## Blog Posts and Tutorials

6. **Understanding Model Biases**
   - Anthropic. "Model Self-Preference in Language Models"
   - https://www.anthropic.com/research/model-self-preference

7. **Prompt Engineering Limitations**
   - OpenAI. "GPT Best Practices: When Prompting Isn't Enough"
   - https://platform.openai.com/docs/guides/prompt-engineering

8. **Tool Use in LLMs Overview**
   - HuggingFace. "Tools and Agents"
   - https://huggingface.co/docs/transformers/main/en/agents

9. **Compound AI Systems Introduction**
   - Zaharia, M., et al. (2024). "The Shift from Models to Compound AI Systems." *BAIR Blog*
   - https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/

## GitHub Repositories

10. **Tool-Using Agents Examples**
    - LangChain Tool Examples
    - https://github.com/langchain-ai/langchain/tree/master/docs/docs/modules/agents

11. **Agentic Framework Implementations**
    - AutoGPT
    - https://github.com/Significant-Gravitas/AutoGPT
    - BabyAGI
    - https://github.com/yoheinakajima/babyagi

12. **Orchestration Patterns**
    - LlamaIndex Orchestration
    - https://github.com/run-llama/llama_index/tree/main/llama-index-core/llama_index/core/agent

## Documentation

13. **OpenAI Function Calling**
    - https://platform.openai.com/docs/guides/function-calling

14. **Anthropic Tool Use**
    - https://docs.anthropic.com/en/docs/tool-use

---

