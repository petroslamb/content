# Dive 7: Tool Use and Model Coordination
## Introduction

This part zooms in on the actual tool-usage behaviors that emerge once the orchestrator is trained. It analyzes patterns like when to self-solve, when to delegate, and how to combine multiple tools or models into effective problem-solving strategies.


## 🌊 Surface Level: The Art of Knowing When to Delegate

**The core skill**: Knowing which tool to use when.

**Three categories of decisions**:
1. **Self-solve vs. delegate**: Can I answer this myself or do I need help?
2. **Which tool**: If delegating, which tool is best for this subtask?
3. **When to stop**: Have I gathered enough information, or do I need more?

**Example decision tree**:
```
Question: "What is the capital of France?"
├─ Can answer directly? YES → "Paris"
└─ Need tool? NO

Question: "What is the capital of the newest country in the world?"
├─ Can answer directly? NO (might not know newest country)
├─ Need tool? YES
├─ Which tool? Web search (time-sensitive info)
└─ After search: Can answer? YES → "Juba (South Sudan)"

Question: "Calculate integral of e^(-x^2) from 0 to infinity"
├─ Can answer directly? MAYBE (might make error)
├─ Need tool? YES (complex math)
├─ Which tool? Math model OR Code interpreter
└─ Cost consideration: Code interpreter cheaper → Use that first
```

## 🏊 Shallow Dive: Tool Selection Patterns

### Pattern 1: Hierarchical Delegation

**Strategy**: Start with cheap tools, escalate if needed.

**Example from Orchestrator-8B**:
```
Turn 1: Call local_search("concept definition")
    ↓ Result: Found basic definition
    ↓ Assess: Is this enough?
    
Turn 2: Reason with definition
    ↓ Result: Stuck on application to specific case
    ↓ Assess: Need expert help
    
Turn 3: Call Qwen2.5-Math-7B("Apply to K_{1000,1000}")
    ↓ Result: Gets formula but makes computational error
    ↓ Assess: Need verification
    
Turn 4: Call code_interpreter("Verify calculation")
    ↓ Result: Finds error
    ↓ Assess: Need correction
    
Turn 5: Call GPT-5("Review and correct")
    ↓ Result: Correct answer
    ↓ Assess: Done!
```

**Cost breakdown**:
- Turn 1: $0.0001 (local search)
- Turn 2: $0 (self-reasoning)
- Turn 3: $0.003 (small math model)
- Turn 4: $0.0001 (code interpreter)
- Turn 5: $0.05 (GPT-5)
- **Total: $0.0532**

**Compare to calling GPT-5 directly**:
- Single turn: $0.08 (higher cost)
- Might work, but less reliable (no verification)

**The principle**: Escalation ladder
1. Free tools (local search, code)
2. Cheap models (7B specialists)
3. Medium models (32B generalists)
4. Expensive models (GPT-5, Claude)

### Pattern 2: Parallel Consultation

**Strategy**: Call multiple tools, synthesize results.

**Example**:
```
Question: "Is this medical claim accurate?"

Fork into parallel tracks:
├─ Track 1: web_search("medical claim verification")
├─ Track 2: local_search(medical_database)
└─ Track 3: Call Qwen3-32B("Analyze claim")

Gather results:
- Web: "Source A says yes, Source B says no"
- Local: "Our database has conflicting studies"
- Qwen: "Claim is partially true, with caveats"

Synthesize:
- Call GPT-5("Reconcile conflicting evidence, provide nuanced answer")
```

**When to use**:
- Uncertain which tool will have best information
- Need to verify information from multiple sources
- Different tools provide different perspectives

**Cost consideration**: 
- More expensive (multiple calls)
- But higher confidence in result

### Pattern 3: Iterative Refinement

**Strategy**: Use cheap tool, refine with expensive tool only if needed.

**Example**:
```
Draft: Qwen2.5-Coder-32B("Write function to solve problem")
    ↓ Test: code_interpreter(execute draft)
    ↓ Result: Fails test case 3

Refine: Qwen2.5-Coder-32B("Fix to handle edge case")
    ↓ Test: code_interpreter(execute refined version)
    ↓ Result: Still fails test case 3

Escalate: GPT-5("Review code, identify issue, fix")
    ↓ Test: code_interpreter(execute GPT-5 version)
    ↓ Result: All tests pass!
```

**Benefit**: 
- Qwen attempts cost $0.006 total
- GPT-5 final fix costs $0.05
- Total: $0.056

**Compare to GPT-5 directly**: 
- Might work in one call ($0.05)
- But Orchestrator approach is more reliable (iterative testing)
- Total cost similar, higher success rate

## 🤿 Deep Dive: How the Model Learns These Patterns

### Learning Through Reward Shaping

**The key insight**: Reward structure determines learned behavior.

**Scenario 1: Accuracy-only reward**
```python
R(τ) = 1 if correct else 0
```

**Learned behavior**:
- Always call most capable model (GPT-5)
- Ignore cost
- Result: High accuracy, high cost

**Scenario 2: Accuracy minus cost**
```python
R(τ) = 1 if correct else 0
R(τ) -= 0.1 * cost  # Penalty for cost
```

**Learned behavior**:
- Balance accuracy and cost
- But: Fixed trade-off (0.1 weight)
- Can't adapt to user preferences

**Scenario 3: ToolOrchestra's preference-aware reward**
```python
R(τ) = M_normalized · P if correct else 0
# P includes user's cost sensitivity
```

**Learned behavior**:
- Adapts to user preferences
- If P[cost] = 1.0 (user cares about cost):
  - Learn to use cheap tools first
- If P[cost] = 0.1 (user doesn't care about cost):
  - Use expensive tools more freely

### Emergence of Tool-Specific Knowledge

**Fascinating observation**: Model learns which tools are good at what.

**Example from training**:
```
Early training (step 100):
Task: "Solve differential equation"
Attempt: Call GPT-5 → Correct (reward: +1)

Later training (step 5000):
Task: "Solve differential equation"
Attempt: Call Qwen2.5-Math-72B → Correct (reward: +1.2, higher due to lower cost)

Final training (step 10000):
Task: "Prove mathematical theorem"
Learned: Qwen2.5-Math-72B good for solving, but GPT-5 better for proving
```

**How does model learn this?**
1. Tries different tools on different tasks
2. Some combinations work better (higher reward)
3. Gradient updates increase probability of successful combinations
4. Over time, learns correlation between task type and best tool

**Implicit knowledge representation**:
The model doesn't have explicit rules like:
```
if task_type == "mathematical_proof":
    use_tool = "GPT-5"
```

Instead, knowledge is distributed across attention patterns:
```
Attention layer sees tokens: "prove", "theorem", "mathematical"
Attention activates neurons associated with "formal reasoning"
These neurons correlate with "call GPT-5" in training data
Output distribution shifts toward calling GPT-5
```

**Evidence from the paper**:
Table 15 shows tool usage patterns differ by task:
- Math-heavy tasks → More calls to Math-72B
- Coding tasks → More calls to Coder-32B
- Ambiguous tasks → More calls to GPT-5

The model learned task-tool matching without explicit supervision!

### Generalization to Unseen Tools

**The surprising result** (Section 6.3): Model works with tools not seen in training.

**How is this possible?**

**Hypothesis 1: Learning from descriptions**
```python
# During training, model sees:
tool_description_Qwen2.5-Math-72B = """
Advanced mathematical reasoning model.
Strong at: calculus, linear algebra, number theory
Weak at: applied statistics, data analysis
"""

# At test time, model sees new tool:
tool_description_DeepSeek-Math-7B = """
Specialized mathematical model for problem solving.
Strong at: algebra, geometry, basic calculus
Weak at: advanced topics, formal proofs
"""

# Model learns to match tasks to description patterns
task = "Solve basic algebra problem"
# Attention matches "basic" + "algebra" to DeepSeek description
# Calls DeepSeek-Math-7B
```

**Hypothesis 2: Learning abstract orchestration skills**
- Not just learning "call Qwen for math"
- But learning "call specialized model for specialized task"
- This generalizes to new specialized models

**Hypothesis 3: In-context learning**
- Model has seen diverse tool sets during training
- Learns to adapt to available tools from context
- At test time, uses same adaptation mechanism

**Evidence**:
- Performance drop is small (~5% on HLE) with unseen tools
- Suggests robust generalization, not memorization

## 🔬 Research Depth: Meta-Learning and Tool Orchestration

### Connection to Meta-Learning

**Meta-learning**: "Learning to learn"
- Train on many tasks
- Learn how to quickly adapt to new tasks

**Tool orchestration as meta-learning**:
- Train on many tool configurations
- Learn how to quickly adapt to new tool sets

**Formal framework (MAML - Model-Agnostic Meta-Learning)**:
```
θ* = argmax_θ E_task [
    R(task, θ - α∇L(task, θ))
]
```

**In English**: Find parameters θ that, after a small update on a new task, perform well.

**ToolOrchestra implicitly does this**:
- Diverse tool configurations = diverse tasks
- Model learns general orchestration strategy
- Can adapt to new tool configurations

**Explicit meta-learning extension** (future work):
```python
# Meta-training
for episode in meta_training:
    tool_config = sample_tool_configuration()
    
    # Inner loop: Adapt to this configuration
    adapted_model = fine_tune_on_config(tool_config, steps=5)
    
    # Outer loop: Evaluate adaptation
    reward = evaluate(adapted_model, tool_config)
    
    # Update base model to be better at adapting
    update_meta_parameters(reward)
```

**Potential benefits**:
- Even faster adaptation to new tools
- Explicit optimization for generalization
- Could work with single example of new tool

### Tool Discovery and Dynamic Tool Sets

**Current limitation**: Tools must be pre-specified.

**Future direction**: Discover and integrate new tools on-the-fly.

**How this could work**:

**Tool discovery**:
```python
# Agent encounters unfamiliar problem
task = "Analyze protein folding structure"

# Search for relevant tools
tool_search = web_search("protein folding analysis tools")
found_tools = ["AlphaFold API", "Rosetta software", "PyMOL"]

# Generate descriptions for new tools
for tool in found_tools:
    description = describe_tool(tool)
    integrate_tool(tool, description)

# Now use newly discovered tools
result = call_tool("AlphaFold API", task_parameters)
```

**Challenges**:
1. **Safety**: How to verify new tool is safe to call?
2. **Schema inference**: How to determine parameters without documentation?
3. **Reliability**: How to trust results from unknown tool?
4. **Cost**: Unknown tools might be expensive

**Research directions**:

**1. Tool retrieval**:
- Embed task and tool descriptions
- Retrieve most relevant tools from large library
- Related to: RAG (Retrieval-Augmented Generation)

**2. Few-shot tool learning**:
- Given 1-3 examples of tool usage
- Learn to use tool correctly
- Related to: In-context learning, few-shot learning

**3. Tool composition**:
- Combine multiple simple tools to create complex capability
- Example: Combine web_search + extract_structured_data + visualize
- Related to: Program synthesis, compositional generalization

### Hierarchical Tool Orchestration

**Current**: Flat orchestration (orchestrator → tools)

**Future**: Hierarchical orchestration (orchestrator → sub-orchestrators → tools)

**Architecture**:
```
Level 3: Meta-orchestrator (8B model)
         Decides: Science task vs. Code task vs. General reasoning
           ↓
Level 2: Specialized orchestrators (3B models each)
         Science-orchestrator: Chooses between bio/chem/physics tools
         Code-orchestrator: Chooses between languages/frameworks
         General-orchestrator: Handles broad reasoning
           ↓
Level 1: Actual tools
         Bio tools, Chem tools, Physics tools
         Python tools, JavaScript tools
         Search, calculators, databases
```

**Benefits**:
1. **Modularity**: Replace one sub-orchestrator without retraining everything
2. **Specialization**: Each level focuses on narrower domain
3. **Efficiency**: Only activate relevant sub-orchestrators
4. **Interpretability**: Clearer decision hierarchy

**Challenges**:
1. **Credit assignment**: Which level gets credit for success?
2. **Communication**: How do levels share information?
3. **Training**: How to train hierarchy end-to-end?

**Connection to**:
- Hierarchical RL (Options framework, HAM)
- Mixture of Experts (sparse activation)
- Feudal Networks (manager-worker hierarchy)

---


## Conclusion

The analysis in this part is meant to make the orchestrator’s behavior feel less mysterious: the escalation ladders, parallel calls, and iterative refinement loops are all emergent patterns grounded in the reward design and training setup you’ve already seen. Recognizing those patterns gives you an intuitive vocabulary for debugging, extending, or critiquing orchestration behaviors in your own systems.

## Academic Papers

127. **ReAct (Reasoning + Acting)**
     - Yao, S., et al. (2023). "ReAct: Synergizing Reasoning and Acting in Language Models." *ICLR 2023*
     - https://arxiv.org/abs/2210.03629

128. **Toolformer**
     - Schick, T., et al. (2023). "Toolformer: Language Models Can Teach Themselves to Use Tools." *NeurIPS 2023*
     - https://arxiv.org/abs/2302.04761

129. **Chain-of-Thought Prompting**
     - Wei, J., et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." *NeurIPS 2022*
     - https://arxiv.org/abs/2201.11903

130. **Tree of Thoughts**
     - Yao, S., et al. (2024). "Tree of Thoughts: Deliberate Problem Solving with Large Language Models." *NeurIPS 2024*
     - https://arxiv.org/abs/2305.10601

131. **Graph of Thoughts**
     - Besta, M., et al. (2024). "Graph of Thoughts: Solving Elaborate Problems with Large Language Models." *AAAI 2024*
     - https://arxiv.org/abs/2308.09687

132. **HuggingGPT (Multi-Model Coordination)**
     - Shen, Y., et al. (2023). "HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face." *NeurIPS 2023*
     - https://arxiv.org/abs/2303.17580

133. **Gorilla (API Learning)**
     - Patil, S.G., et al. (2023). "Gorilla: Large Language Model Connected with Massive APIs." *arXiv:2305.15334*
     - https://arxiv.org/abs/2305.15334

134. **ToRA (Tool-Integrated Reasoning)**
     - Gou, Z., et al. (2024). "ToRA: A Tool-Integrated Reasoning Agent for Mathematical Problem Solving." *ICLR 2024*
     - https://arxiv.org/abs/2309.17452

135. **Code-as-Tool**
     - Gao, L., et al. (2023). "PAL: Program-aided Language Models." *ICML 2023*
     - https://arxiv.org/abs/2211.10435

136. **Chameleon (Multi-Tool Composition)**
     - Lu, P., et al. (2024). "Chameleon: Plug-and-Play Compositional Reasoning with Large Language Models." *NeurIPS 2024*
     - https://arxiv.org/abs/2304.09842

## Blog Posts and Tutorials

137. **ReAct Tutorial**
     - "Building ReAct Agents from Scratch"
     - https://blog.langchain.dev/react-agents/

138. **Tool Use Best Practices**
     - "A Guide to Tool Use in LLMs"
     - https://www.anthropic.com/news/tool-use-ga

139. **Model Coordination Patterns**
     - "Orchestrating Multiple AI Models"
     - https://martinfowler.com/articles/model-orchestration.html

140. **Chain-of-Thought Deep Dive**
     - "Understanding Chain-of-Thought Reasoning"
     - https://www.promptingguide.ai/techniques/cot

## GitHub Repositories

141. **ReAct Implementation**
     - https://github.com/ysymyth/ReAct

142. **Toolformer Code**
     - https://github.com/lucidrains/toolformer-pytorch

143. **HuggingGPT (JARVIS)**
     - https://github.com/microsoft/JARVIS

144. **Gorilla API Store**
     - https://github.com/ShishirPatil/gorilla

145. **ToRA Code**
     - https://github.com/microsoft/ToRA

146. **PAL Code**
     - https://github.com/reasoning-machines/pal

147. **Chameleon Implementation**
     - https://github.com/lupantech/chameleon-llm

148. **LangChain Agents**
     - Comprehensive agent framework
     - https://github.com/langchain-ai/langchain/tree/master/libs/langchain/langchain/agents

149. **AutoGen (Multi-Agent Framework)**
     - https://github.com/microsoft/autogen

---

