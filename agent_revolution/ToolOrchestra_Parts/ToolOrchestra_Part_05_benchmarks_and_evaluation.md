# Dive 5: Benchmarks and Evaluation
## Introduction

This part looks at how we actually test whether ToolOrchestra works, and what "better" means in practice. It unpacks the benchmarks, metrics, and evaluation choices used to compare the orchestrator against strong baselines on hard, realistic tasks.


## 🌊 Surface Level: How Do We Test the Orchestrator?

Three challenging benchmarks:

1. **HLE (Humanity's Last Exam)**: PhD-level questions across all disciplines
2. **FRAMES**: Multi-hop fact-checking requiring multiple sources
3. **τ²-Bench**: Real-world function calling in conversations

Think of these as:
- HLE: Final exam for a PhD student
- FRAMES: Investigative journalism (verify facts from multiple sources)
- τ²-Bench: Customer service rep using various tools

## 🏊 Shallow Dive: Understanding Each Benchmark

### HLE: Humanity's Last Exam

**Paper**: Phan et al., 2025

**Motivation**: Create questions so hard that they represent the "last exam" before AI surpasses human experts.

**Characteristics**:
- Questions from PhD qualifying exams
- Fields: Math, physics, chemistry, biology, history, literature, philosophy
- Designed to require deep understanding, not memorizable facts
- 10-14% require images (ToolOrchestra uses text-only subset)

**Example question** (simplified):
```
What is the Alon-Tarsi number of the complete bipartite graph K_{1000,1000}?

Background: This requires:
1. Knowing what Alon-Tarsi number means (graduate combinatorics)
2. Understanding properties of bipartite graphs
3. Either computing or finding the specific formula
4. Applying it to this large instance
```

**Why it's hard for AI**:
- Requires specialized knowledge not in typical training data
- Can't be solved by simple pattern matching
- Need to search for definitions, theorems, apply multi-step reasoning
- Even GPT-5 gets only ~35% correct

**Why it's good for testing orchestrators**:
- Requires multiple tools: web search for definitions, math models for computation, code for verification
- Shows when model knows to delegate to specialists vs. solving directly
- Cost-accuracy trade-off is clear

### FRAMES: Factuality Reasoning

**Paper**: Krishna et al., 2024

**Motivation**: Test end-to-end retrieval-augmented generation (RAG) including retrieval quality, reasoning, and factuality.

**Characteristics**:
- 824 questions requiring 2-15 Wikipedia articles
- Types: Numerical reasoning, tabular data, temporal reasoning, multi-constraint
- Must find relevant sources AND reason correctly over them
- Gold answers are verifiable facts

**Example question**:
```
Question: "Which movie won more Oscars: 
          The Lord of the Rings: Return of the King or Titanic?"

Required steps:
1. Search for "Lord of the Rings Return of the King Oscars"
2. Extract: Won 11 Oscars
3. Search for "Titanic Oscars"
4. Extract: Won 11 Oscars  
5. Compare: Tie (both won 11)
6. Answer: "Both won the same number (11 Oscars)"
```

**Why it's hard for AI**:
- Requires precise factual information (can't guess)
- Must retrieve from correct sources (not all web pages accurate)
- Reasoning must be logically sound
- Answer format must be exact

**Why it's good for testing orchestrators**:
- Shows retrieval tool usage (web search vs. local search)
- Demonstrates when to call generalist models vs. when evidence is sufficient
- Tests efficiency (don't call expensive models for simple fact lookup)

### τ²-Bench: Dual-Control Conversational Agents

**Paper**: Barres et al., 2025

**Motivation**: Test agents in realistic conversational settings where both user and agent can take actions.

**Characteristics**:
- Three domains: Telecom, Retail, Airline
- Turn-based conversations
- Both agent and simulated user can take actions
- Success requires understanding user intent + using right tools + conversing naturally

**Example conversation** (abbreviated):
```
User: "I need to check my flight status"
Agent: "I can help with that. What's your flight number?"
User: "AA1234"
Agent: [Calls get_flight_status("AA1234")]
Tool: {"status": "On time", "departure": "3:30 PM", "gate": "B12"}
Agent: "Your flight AA1234 is on time, departing at 3:30 PM from gate B12"
```

**Failure modes tested**:
- Wrong tool called (e.g., calling check_baggage instead of get_flight_status)
- Right tool, wrong parameters (e.g., passing name instead of flight number)
- Not calling tools when needed (trying to answer from memory)
- Calling tools unnecessarily (e.g., checking status for an already departed flight)

**Why it's hard for AI**:
- Must track conversation context
- Must extract parameters from natural language
- Must decide when tool call is necessary
- Must format tool responses naturally

**Why it's good for testing orchestrators**:
- Tests function calling capabilities directly
- Shows if model wastes calls to expensive models (e.g., calling GPT-5 to format simple responses)
- Evaluates efficiency in multi-turn scenarios

## 🤿 Deep Dive: Evaluation Metrics and Methodology

### Primary Metric: Accuracy

For all three benchmarks, primary metric is accuracy (% correct).

But "correct" means different things:

**HLE correctness**:
```python
def check_hle_answer(predicted, gold):
    # Use GPT-5 as judge
    prompt = f"""
    Gold answer: {gold}
    Predicted answer: {predicted}
    
    Are these semantically equivalent?
    Consider mathematical equivalence, different phrasings, etc.
    
    Output: YES or NO
    """
    
    judge_response = gpt5(prompt)
    return judge_response.strip() == "YES"
```

**Challenges**:
- Math notation: "1/2" vs. "0.5" vs. "½"
- Names: "USA" vs. "United States" vs. "United States of America"
- Judge errors: GPT-5 occasionally makes mistakes

**FRAMES correctness**:
```python
def check_frames_answer(predicted, gold, evidence):
    # Stricter: Must match fact exactly
    # Evidence is provided as ground truth
    
    # Extract structured answer
    pred_structured = extract_structured(predicted)
    gold_structured = extract_structured(gold)
    
    # Check match
    return pred_structured == gold_structured
```

**More strict than HLE** because:
- Factual questions have definitive answers
- Evidence is provided (can check against gold sources)
- No room for interpretation

**τ²-Bench correctness**:
```python
def check_tau2_answer(conversation_history):
    # Check multiple criteria:
    criteria = {
        "task_completion": False,
        "tool_usage": False,
        "conversation_flow": False
    }
    
    # Did agent accomplish user's goal?
    criteria["task_completion"] = check_task_complete(conversation_history)
    
    # Did agent use tools correctly?
    criteria["tool_usage"] = check_tool_calls_valid(conversation_history)
    
    # Was conversation natural?
    criteria["conversation_flow"] = check_naturalness(conversation_history)
    
    # All must pass
    return all(criteria.values())
```

**Most complex evaluation** because:
- Conversational (not single answer)
- Multiple success criteria
- Subjective elements (naturalness)

### Secondary Metrics: Cost and Latency

These are crucial for ToolOrchestra's thesis (efficient orchestration).

**Cost calculation**:
```python
def calculate_cost(trajectory):
    cost = 0.0
    
    for turn in trajectory:
        if turn.tool == "GPT-5":
            input_tokens = count_tokens(turn.input)
            output_tokens = count_tokens(turn.output)
            cost += (input_tokens / 1_000_000) * 15  # $15 per M input tokens
            cost += (output_tokens / 1_000_000) * 30  # $30 per M output tokens
            
        elif turn.tool == "Qwen2.5-Coder-32B":
            input_tokens = count_tokens(turn.input)
            output_tokens = count_tokens(turn.output)
            cost += (input_tokens / 1_000_000) * 0.8  # Third-party API price
            cost += (output_tokens / 1_000_000) * 2.4
            
        elif turn.tool == "web_search":
            cost += 0.01  # Per search cost
            
        elif turn.tool == "code_interpreter":
            cost += 0.0001  # Negligible (local execution)
    
    return cost
```

**Latency calculation**:
```python
def calculate_latency(trajectory):
    latency = 0.0
    
    for turn in trajectory:
        start_time = turn.start_timestamp
        end_time = turn.end_timestamp
        latency += (end_time - start_time)
    
    return latency  # In seconds
```

**Important**: These measure wall-clock time, not just compute time. Includes:
- Network latency for API calls
- Model inference time
- Tool execution time
- System overhead

### Composite Metrics: Cost-Effectiveness

**The key question**: How much accuracy per dollar?

**Metric 1: Accuracy per dollar**
```python
accuracy_per_dollar = accuracy / average_cost_per_question
```

Higher is better. Orchestrator-8B should have highest score.

**Metric 2: Cost at target accuracy**
```python
# For each model, find cost needed to reach X% accuracy
# (by varying max_turns parameter)

models = ["Orchestrator-8B", "GPT-5", "Claude-Opus-4.1"]
target_accuracy = 0.35

for model in models:
    cost = find_cost_at_accuracy(model, target_accuracy)
    print(f"{model}: ${cost} to reach {target_accuracy*100}% accuracy")
```

From the paper (HLE benchmark):
- Orchestrator-8B: $0.30 to reach 35% accuracy
- GPT-5: $0.80 to reach 35% accuracy
- Claude Opus 4.1: $0.95 to reach 35% accuracy

**2.5x more cost-effective** than GPT-5!

**Metric 3: Pareto frontier position**

Plot all models on accuracy vs. cost graph. Pareto frontier = models that aren't dominated by others.

From Figure 6 in paper:
```
Accuracy
40% |              • Orchestrator-8B (Pareto optimal)
35% |         • GPT-5 (Pareto optimal)
    |       • Claude (dominated by GPT-5)
30% |  • Qwen3-235B (dominated by Orchestrator)
    |
    +--------------------------------
       $0.30    $0.60    $0.90   Cost
```

Orchestrator-8B dominates all others in cost-effectiveness region.

## 🔬 Research Depth: Evaluation Challenges and Biases

### Challenge 1: Judge Bias in LLM-as-Judge

**The problem**: Using GPT-5 to evaluate GPT-5 creates potential bias.

**Known biases** (from MT-Bench paper, Zheng et al., 2023):
1. **Position bias**: Judges prefer first answer in pair comparison
2. **Verbosity bias**: Judges prefer longer, more detailed answers
3. **Self-enhancement bias**: Judges prefer outputs similar to their own style
4. **Refusal bias**: Judges penalize "I don't know" even when appropriate

**ToolOrchestra's mitigation**:
- Use GPT-5 only for semantic equivalence, not quality judgment
- Provide both answers without revealing which is which
- Focus on factual correctness, not style
- Use execution-based verification when possible (code, database state)

**Remaining limitation**: No perfect solution. Some error rate in judgment is inevitable.

**Open question**: Would ensemble of judges (GPT-5 + Claude + human spot-checking) improve reliability?

### Challenge 2: Cost Calculation Fairness

**The problem**: Comparing costs across models with different hosting is tricky.

**Considerations**:
- Open models: Hosting cost depends on provider, hardware, utilization
- Proprietary models: Published API pricing, but discounts available
- Local models: Hardware depreciation, electricity, maintenance

**ToolOrchestra's approach**: Use third-party API pricing for all models
- Justification: Reflects real-world cost for most users
- Provider: TogetherAI for open models
- Limitation: Doesn't reflect large-scale deployment costs

**Alternative approaches**:
1. **FLOPs-based**: Count floating-point operations
   - Pro: Hardware-independent
   - Con: Doesn't reflect real costs (memory, networking matter)

2. **Latency-based**: Use time as proxy for cost
   - Pro: Correlates with real user experience
   - Con: Varies by hardware, doesn't capture GPU idling costs

3. **Amortized hardware**: Calculate cost per inference on specific hardware
   - Pro: Reflects real deployment
   - Con: Different for every setup

**No perfect solution**. Cost comparison is inherently approximate.

### Challenge 3: Generalization Testing

**The key question**: Does performance on these 3 benchmarks predict performance on new tasks?

**Evidence for generalization**:
- Three benchmarks are quite different (academia, fact-checking, customer service)
- Orchestrator-8B outperforms on all three
- Testing with unseen models (Section 6.3) shows robustness

**Evidence against generalization**:
- All three are "question-answering" style tasks
- None test long-form generation (writing essays)
- None test interactive embodied tasks (robot control)
- None test creative tasks (art, music generation)

**Broader question**: What is the right test suite for general orchestration ability?

**Proposed additional benchmarks**:
1. **Agentic workflows**: SWE-Bench (code editing), WebArena (web navigation)
2. **Long-horizon tasks**: GAIA (research tasks), FanOutQA (many parallel calls)
3. **Interactive environments**: ALFWorld (household tasks), VirtualHome (simulation)
4. **Creative tasks**: LongForm (essay writing), StoryGen (narrative generation)

### Challenge 4: Human Preference Alignment

**The gap**: Accuracy + cost + latency doesn't capture all of user preferences.

**Other factors users care about**:
- **Explanability**: Can I understand why the agent made these choices?
- **Controllability**: Can I intervene mid-trajectory?
- **Safety**: Will the agent do something unintended?
- **Transparency**: What sources did the agent actually use?
- **Consistency**: Does the agent give similar answers to similar questions?

**ToolOrchestra's preference mechanism** addresses some of these:
- User can specify tool preferences (e.g., "prefer local search" = more private/transparent)
- User can specify cost preferences (controllability)

**But doesn't capture**:
- Explanation preferences ("explain your reasoning")
- Safety constraints ("never modify the database without confirmation")
- Ethical preferences ("don't use biased sources")

**Connection to RLHF**: Reinforcement Learning from Human Feedback (Christiano et al., 2017)
- Idea: Learn reward function from human preferences
- Applied to: ChatGPT, Claude (constitutional AI)
- Could apply to: Tool orchestration preferences

**How this would work**:
```python
# Instead of explicit preference vector P
# Learn reward model from preference comparisons

# Collect human preferences:
# "I prefer trajectory A over trajectory B because..."
preferences = collect_human_comparisons(trajectories)

# Train reward model
reward_model = train_on_preferences(preferences)

# Use learned reward in RL
R(τ) = reward_model(τ) if solved else 0
```

**Advantages**:
- Captures nuanced preferences humans can't articulate
- Generalizes to new scenarios
- Continuously updatable

**Challenges**:
- Expensive to collect human preferences
- Preferences vary across users
- Preferences may be context-dependent

**Open question**: Can we learn personalized reward models that adapt to individual users over time?

---


## Conclusion

This part shows that evaluation for orchestrators has to go beyond simple correctness numbers and include cost, latency, and realistic interaction patterns. With the benchmark details in hand, you can interpret ToolOrchestra’s reported gains as genuine improvements in system-level behavior rather than artifacts of cherry-picked metrics.

## Academic Papers

81. **HLE (Humanity's Last Exam)**
    - Phan, L., et al. (2025). "Humanity's Last Exam." *OpenAI Research*
    - https://openai.com/research/hle

82. **FRAMES (Factuality Reasoning)**
    - Krishna, K., et al. (2024). "FRAMES: A Framework for Reasoning and Multi-hop Evidence Synthesis." *arXiv:2409.12048*
    - https://arxiv.org/abs/2409.12048

83. **τ²-Bench (Conversational Agents)**
    - Barres, L., et al. (2025). "τ²-Bench: A Benchmark for Tool-Augmented Task-Oriented Dialogue." *arXiv:2506.13847*
    - https://arxiv.org/abs/2506.13847

84. **ToolBench (Original Tool Benchmark)**
    - Qin, Y., Liang, S., Ye, Y., et al. (2024). "ToolBench: An Open Platform for Training, Serving, and Evaluating Large Language Model for Tool Learning." *arXiv:2307.16789*
    - https://arxiv.org/abs/2307.16789

85. **GAIA (General AI Assistant Benchmark)**
    - Mialon, G., et al. (2023). "GAIA: A Benchmark for General AI Assistants." *arXiv:2311.12983*
    - https://arxiv.org/abs/2311.12983

86. **AgentBench (Agent Evaluation)**
    - Liu, X., et al. (2023). "AgentBench: Evaluating LLMs as Agents." *arXiv:2308.03688*
    - https://arxiv.org/abs/2308.03688

87. **WebArena (Web Navigation)**
    - Zhou, S., et al. (2024). "WebArena: A Realistic Web Environment for Building Autonomous Agents." *ICLR 2024*
    - https://arxiv.org/abs/2307.13854

88. **SWE-Bench (Software Engineering)**
    - Jimenez, C.E., et al. (2024). "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" *ICLR 2024*
    - https://arxiv.org/abs/2310.06770

89. **HumanEval (Code Evaluation)**
    - Chen, M., et al. (2021). "Evaluating Large Language Models Trained on Code." *arXiv:2107.03374*
    - https://arxiv.org/abs/2107.03374

90. **MMLU (Massive Multitask Language Understanding)**
    - Hendrycks, D., et al. (2021). "Measuring Massive Multitask Language Understanding." *ICLR 2021*
    - https://arxiv.org/abs/2009.03300

91. **BigBench (Beyond the Imitation Game)**
    - Srivastava, A., et al. (2022). "Beyond the Imitation Game: Quantifying and Extrapolating the Capabilities of Language Models." *arXiv:2206.04615*
    - https://arxiv.org/abs/2206.04615

## Blog Posts and Tutorials

92. **LLM Benchmarking Guide**
    - "How to Benchmark Language Models"
    - https://huggingface.co/blog/evaluating-llms

93. **LLM-as-Judge Best Practices**
    - "Using LLMs as Judges: A Critical Analysis"
    - https://eugeneyan.com/writing/llm-as-judge/

94. **Benchmark Contamination**
    - "Data Contamination in LLM Benchmarks: A Growing Concern"
    - https://blog.eleuther.ai/contamination/

95. **Evaluation Metrics for Agents**
    - "How to Evaluate AI Agents"
    - https://lilianweng.github.io/posts/2023-06-23-agent/

96. **Cost-Effectiveness Analysis**
    - "Measuring the True Cost of LLM Inference"
    - https://www.semianalysis.com/p/the-inference-cost-of-search-agents

## GitHub Repositories

97. **HLE Evaluation Code**
    - https://github.com/openai/hle

98. **FRAMES Dataset and Eval**
    - https://github.com/google-research/frames

99. **Tau2-Bench**
    - https://github.com/tau2bench/tau2bench

100. **ToolBench Code**
     - https://github.com/OpenBMB/ToolBench

101. **WebArena Environment**
     - https://github.com/web-arena-x/webarena

102. **SWE-Bench Repository**
     - https://github.com/princeton-nlp/SWE-bench

103. **Open LLM Leaderboard**
     - https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard

104. **lm-evaluation-harness**
     - Standardized evaluation framework
     - https://github.com/EleutherAI/lm-evaluation-harness

105. **Chatbot Arena**
     - Human preference evaluation
     - https://github.com/lm-sys/FastChat

## Tools and Platforms

106. **Weights & Biases for Experiment Tracking**
     - https://wandb.ai/

107. **MLflow**
     - https://mlflow.org/

108. **Evidently AI (Model Monitoring)**
     - https://www.evidentlyai.com/

---

