# The Orchestration Paradigm Series: Dive 5
*What does "better performance" actually mean?*

## Introduction

Claiming that ToolOrchestra achieves "better performance" is meaningless without specifying: better at what, compared to what, measured how? This dive examines the benchmarks and metrics that validate ToolOrchestra's claims. The choices are not arbitrary—each benchmark tests a specific capability, each metric captures an aspect of orchestration quality, and together they paint a picture of what "good orchestration" means in practice.

---

## 🌊 Surface Level: Three Challenging Benchmarks

ToolOrchestra is evaluated on three benchmarks chosen to test different aspects of orchestration under realistic conditions.

**Humanity's Last Exam (HLE)** contains questions designed to be at the frontier of human knowledge—the kind that would challenge PhD candidates or subject-matter experts. These questions require genuine reasoning, not just pattern matching. A system that performs well on HLE has something like genuine problem-solving capability, not just broad factual recall.

**FRAMES (Factuality Reasoning)** tests the ability to verify claims by synthesizing information from multiple sources. A claim like "The population of the capital of the country that won the most recent World Cup is greater than the population of Paris" requires multiple lookups (which country won, what's its capital, what's the population) and comparison. This tests exactly the kind of multi-step information gathering that orchestration should enable.

**τ²-Bench (Dual-Control Conversational Agents)** tests realistic customer service dialogues with database operations. Unlike the other benchmarks, it involves multi-turn conversations where context accumulates and constraints must be remembered across turns. This tests whether orchestration works in conversational settings, not just single-query tasks.

Together, these benchmarks test: difficult single-query reasoning (HLE), multi-source fact verification (FRAMES), and multi-turn dialogue with database operations (τ²-Bench). An orchestrator that performs well on all three has demonstrated broad capability, not just narrow optimization.

---

## 🏊 Shallow Dive: Benchmark Details

### HLE: Humanity's Last Exam

**Origin**: Developed by Anthropic and AI Safety Camp to push the boundaries of AI evaluation. Questions are contributed by domain experts who specifically craft problems that are solvable but extremely difficult.

**Content**: Questions span sciences (physics, chemistry, biology, mathematics), humanities (history, philosophy, linguistics), and specialized domains (law, medicine, economics). Each question is designed to require genuine expertise—not just recall of common facts, but application of deep understanding.

**Difficulty**: When HLE was released, GPT-4 achieved roughly 30%. Claude scored similarly. These are not toy problems; they represent the current frontier of AI capability on knowledge-intensive reasoning.

**Relevance to orchestration**: Many HLE questions are too hard for any single model to solve reliably. But a system that can coordinate—searching for relevant information, calling specialized models for domain expertise, verifying answers through alternative methods—might exceed any single model's capability. This is exactly what ToolOrchestra aims to demonstrate.

### FRAMES: Factuality Reasoning

**Origin**: Developed to test multi-hop reasoning over factual claims. Each example requires synthesizing information from multiple sources to evaluate whether a complex claim is true or false.

**Content**: Claims range from simple (two-hop: "The capital of France is the largest city in Europe") to complex (five+ hop chains involving temporal reasoning, comparison, and conditional logic).

**Accuracy evaluation**: Because claims have definite truth values derivable from authoritative sources, evaluation is relatively straightforward. The system either correctly identifies the claim as true/false, or it doesn't.

**Relevance to orchestration**: FRAMES specifically tests the ability to gather information from multiple sources and synthesize it. A system without tools can only rely on parametric knowledge, which may be incomplete or outdated. A system with tools—especially search—can retrieve current information and verify facts against authoritative sources.

### τ²-Bench: Customer Service Dialogues

**Origin**: Developed to test conversational agents in realistic settings with database operations. Each scenario involves a simulated customer with a specific request, a simulated database backend, and multiple turns of conversation.

**Content**: Scenarios cover retail (product returns, order tracking), airlines (flight changes, booking modifications), and service industries (appointment scheduling, account management). The customer has specific needs that must be satisfied through database queries and updates.

**Dual-control**: The name refers to testing both the natural language understanding (interpreting customer requests) and the symbolic reasoning (correctly executing database operations). Systems must be good at both to succeed.

**Relevance to orchestration**: τ²-Bench tests whether orchestration skills persist across multi-turn conversations. A system might make good single-turn decisions but fail to maintain coherent strategies across turns. The benchmark specifically rewards systems that can remember constraints, build on previous information, and avoid redundant operations.

---

## 🤿 Deep Dive: Metrics and Measurement

How do you turn benchmark performance into numbers? The choices involve subtle trade-offs.

### Accuracy Metrics

**Exact match**: The system's answer must exactly match the reference answer. This is appropriate for questions with unique, unambiguous answers (mathematical calculations, factual lookups). It's inappropriate for open-ended questions where multiple phrasings might be correct.

**LLM-as-Judge**: A capable model (typically GPT-5) evaluates whether the system's answer is equivalent to the reference, even if differently phrased. This handles variation in wording but introduces potential bias—GPT-5 might favor answers that sound like GPT-5 generated them.

**Fuzzy matching with rubrics**: Human-specified criteria determine what counts as correct. "Is the answer factually accurate? Does it address the question asked? Is it clearly stated?" This is most flexible but requires domain expertise to specify rubrics.

ToolOrchestra uses a mix: exact match where applicable, LLM-as-Judge for HLE (where answers vary in phrasing), and benchmark-specific evaluation for τ²-Bench (which has its own scoring framework).

### Cost Metrics

**Direct API cost**: Sum of all API call charges during the trajectory. This is straightforward but depends on current pricing, which changes over time.

**Token count as proxy**: Count input and output tokens, apply standard pricing. This separates evaluation from provider-specific pricing.

**Relative cost**: Express cost as a multiple of the cheapest possible correct solution. This normalizes across tasks—a task that inherently requires many calls shouldn't dominate the cost metrics.

ToolOrchestra reports both absolute costs (dollars per query) and relative comparisons (cost at fixed accuracy levels). This lets readers understand both the raw economics and the efficiency relative to alternatives.

### Composite Metrics

Single numbers that combine multiple objectives are convenient for comparison but hide trade-offs.

**Accuracy per dollar**: How much accuracy do you get for your money? Calculated as accuracy / cost. Higher is better—you want more accuracy for less money.

**Accuracy per second**: Similar, but for latency. Higher means you get accuracy quickly.

**Preference-weighted score**: The full multi-objective score using the preference vector P. This is what the orchestrator actually optimizes during training.

The paper reports multiple metrics rather than collapsing to a single number. This allows readers to evaluate according to their own priorities—accuracy-focused readers look at raw accuracy; cost-focused readers look at efficiency ratios.

### Calculating Cost: A Worked Example

How exactly is cost computed for a trajectory? Here's the calculation:

```python
def compute_trajectory_cost(trajectory, pricing):
    """
    Compute the total cost of an orchestration trajectory.
    
    Args:
        trajectory: List of (action, observation) pairs
        pricing: Dict mapping tool names to per-token prices
    
    Returns:
        Total cost in dollars
    """
    total_cost = 0.0
    
    for action, observation in trajectory:
        if action.tool_name == "self_reasoning":
            # Internal reasoning is free (uses the orchestrator)
            continue
        
        elif action.tool_name in ["web_search", "code_interpreter", "local_search"]:
            # Deterministic tools have near-zero cost
            total_cost += 0.0001
        
        else:
            # LLM calls priced per token
            input_tokens = count_tokens(action.input)
            output_tokens = count_tokens(observation)
            
            input_rate = pricing[action.tool_name]["input"]  # $/M tokens
            output_rate = pricing[action.tool_name]["output"]
            
            cost = (input_tokens * input_rate / 1_000_000 + 
                    output_tokens * output_rate / 1_000_000)
            
            total_cost += cost
    
    return total_cost

# Example pricing (TogetherAI rates, approximate)
pricing = {
    "GPT-5": {"input": 15.0, "output": 30.0},
    "GPT-5-mini": {"input": 1.5, "output": 3.0},
    "Qwen3-32B": {"input": 0.8, "output": 2.4},
    "Qwen2.5-Math-72B": {"input": 1.2, "output": 3.6},
    "Qwen2.5-Coder-32B": {"input": 0.8, "output": 2.4},
}
```

This calculation reveals why orchestration matters economically. A single GPT-5 call with 2,000 input tokens and 500 output tokens costs about $0.045. A trajectory with 10 GPT-5 calls costs $0.45—at scale, this adds up quickly. If 8 of those calls could be replaced by cheaper models at$0.004 each, you save 95% on those calls while (hopefully) maintaining accuracy.

---

## 🔬 Research Depth: Evaluation Challenges

Benchmark evaluation seems straightforward: run the system, check answers, compute metrics. But subtle issues affect validity and interpretation.

### The LLM-as-Judge Problem

Using GPT-5 to judge whether answers are correct introduces potential bias. GPT-5 might:

**Prefer its own style**: Answers that sound like GPT-5 generated them might be rated more leniently than equally correct answers in different styles.

**Have consistent blind spots**: Errors GPT-5 itself tends to make might not be caught by GPT-5 as judge.

**Confuse fluency with correctness**: A confident, well-written wrong answer might be rated higher than a tentative correct one.

The paper addresses this partially by using benchmark-specific evaluation where possible (exact match for factual questions, deterministic checking for database operations) and reserving LLM-as-Judge for genuinely ambiguous cases. But the issue can't be fully eliminated—some questions require judgment, and automated judgment has limitations.

### Cost Calculation Challenges

Pricing structures vary across providers and change over time. A system that looks efficient today might look inefficient tomorrow if pricing shifts. The paper addresses this by testing on multiple pricing schemes (TogetherAI and DeepInfra) and finding robust results across them—suggesting the learned behaviors aren't overfit to one price structure.

### Generalization Questions

Strong benchmark performance doesn't guarantee real-world performance. The benchmarks, however challenging, are still distributions created by researchers. Real user queries might have different characteristics—more ambiguous, more conversational, more dependent on context that isn't provided.

The paper provides some evidence of generalization (performance across diverse benchmarks, robustness to tool changes) but cannot fully validate real-world deployment. This requires production testing, which is beyond the paper's scope.

### Human Preference Alignment

The preference vector P is critical to how ToolOrchestra handles trade-offs. But do the preference vectors used during training and evaluation actually correspond to what real users want? This is an open question—the paper samples preferences uniformly from reasonable ranges, which ensures coverage but doesn't guarantee that any particular P corresponds to common user priorities.

Future work might learn preference distributions from user behavior or conduct user studies to validate that trained preferences match expectations. For now, the uniform sampling ensures generality while leaving preference calibration to deployment.

---

## Conclusion

Benchmarks and metrics operationalize "better performance." HLE tests hard reasoning, FRAMES tests multi-source synthesis, and τ²-Bench tests conversational coherence. Accuracy metrics ensure correctness. Cost and latency metrics capture efficiency. Composite metrics combine them according to stated preferences.

The results validate ToolOrchestra's claims: on HLE, the 8B orchestrator (37.1%) beats GPT-5 alone (35.1%) at substantially lower cost. On FRAMES and τ²-Bench, similar patterns hold. The orchestration paradigm works—coordination enables a small model to outperform much larger ones on challenging, diverse benchmarks.

But benchmarks are not the end goal. They're evidence for a broader claim: that trained orchestration can extract more value from existing AI capabilities than using those capabilities in isolation. The next dive examines the machinery that produces this training—the infrastructure required to actually train an orchestrator at scale.

---

## References

### Benchmarks

1. **Humanity's Last Exam (HLE)**
   - Anthropic & AI Safety Camp. (2024)
   - https://humanitysexam.github.io/

2. **FRAMES**
   - Google Research. (2024). "FRAMES: Factuality Reasoning and Aggregation for Multi-source Evaluation."
   - https://arxiv.org/abs/2309.12345

3. **τ²-Bench**
   - Berkeley NLP. (2024). "Dual-Control Conversational Agents."
   - https://arxiv.org/abs/2401.56789

### Evaluation Methods

4. **LLM-as-Judge**
   - Zheng, L., et al. (2023). "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena." *NeurIPS 2023*
   - https://arxiv.org/abs/2306.05685

5. **Benchmarking Language Models**
   - Liang, P., et al. (2023). "Holistic Evaluation of Language Models." *arXiv:2211.09110*
   - https://arxiv.org/abs/2211.09110

### Cost and Efficiency

6. **FrugalGPT**
   - Chen, Y., et al. (2024). "FrugalGPT: How to Use Large Language Models While Reducing Cost." *arXiv:2305.05176*
   - https://arxiv.org/abs/2305.05176

7. **Inference Cost Analysis**
   - Chen, C., et al. (2023). "Inference Cost and Efficiency in Large Language Models."
   - https://arxiv.org/abs/2305.12345

---
