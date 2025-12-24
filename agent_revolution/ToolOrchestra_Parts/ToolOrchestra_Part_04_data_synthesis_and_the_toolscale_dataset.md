# The Orchestration Paradigm Series: Dive 4
*How do you generate verifiable training data?*
## Introduction

This part focuses on data: how to create rich, verifiable training environments when real multi-tool datasets are scarce. It introduces the ToolScale synthesis pipeline and shows how carefully-constructed synthetic tasks can still teach robust orchestration behavior.


## 🌊 Surface Level: Creating Training Data

**The problem**: To train the orchestrator with RL, we need thousands of examples where:
- User asks a question
- Multiple tools are available
- We can verify if the answer is correct

Such data doesn't exist at scale!

**The solution**: Automatically generate synthetic but realistic data.

**The approach**:
1. Create fake databases (like Yelp restaurants, but simulated)
2. Create tools that interact with these databases
3. Generate tasks that require using these tools
4. Verify tasks are solvable

## 🏊 Shallow Dive: The Two-Phase Synthesis Pipeline

### Phase 1: Environment Creation

Think of this like creating a video game level before recording gameplay footage.

**Step 1.1: Choose a domain**
- Examples: E-commerce, Healthcare, Travel, Finance
- 10 domains total in ToolScale

**Step 1.2: Generate database schema**
```python
# Example for E-commerce
schema = {
    "products": {
        "product_id": "string",
        "name": "string",
        "price": "float",
        "category": "string",
        "inventory": "int",
        "seller_id": "string"
    },
    "orders": {
        "order_id": "string",
        "customer_id": "string",
        "items": "list of product_ids",
        "total": "float",
        "status": "enum[pending, shipped, delivered]"
    }
}
```

**Step 1.3: Generate database entries**
- Use LLM to create realistic entries
- Ensure consistency (e.g., order total matches sum of item prices)
- Validate each entry meets schema

**Step 1.4: Generate tool functions**
```python
def search_products(category=None, max_price=None):
    """Search for products matching criteria"""
    # Implementation interacts with generated database
    
def place_order(customer_id, product_ids):
    """Place an order for customer"""
    # Implementation modifies database
    
def check_inventory(product_id):
    """Check if product in stock"""
    # Implementation queries database
```

### Phase 2: Task Generation

Now we create specific tasks a user might have.

**Step 2.1: Generate intents**
An LLM looks at the available tools and proposes common intents:
- "Find and purchase a product"
- "Check order status"
- "Compare prices across categories"
- "Restock low-inventory items"

**Step 2.2: Convert intents to specific tasks**
Given the actual database content:

Intent: "Find and purchase a product"

Becomes specific task:
```
Instruction: "I'm looking for a laptop under $1000. 
            Can you find one and place an order for me? 
            My customer ID is CUST_12345."

Required actions: 
    1. search_products(category="laptops", max_price=1000)
    2. place_order(customer_id="CUST_12345", product_ids=[result_id])

Expected process info:
    - Must mention price of selected laptop
    - Must confirm order placement
    - Should mention estimated delivery

Gold outcome:
    - Database orders table has new entry for CUST_12345
    - Product inventory decremented by 1
```

**Step 2.3: Increase difficulty (evolution)**
An LLM adds complexity:
- "Find a laptop under $1000 **that has at least 16GB RAM and is from a seller with >4.5 stars**"
- This requires more tool calls (check product specs, check seller ratings)

**Step 2.4: Quality filtering**

Test if task is solvable:
```python
def validate_task(task):
    # Criterion 1: Execute gold actions - no errors?
    try:
        execute(task.gold_actions)
    except Exception:
        return False  # Reject task
    
    # Criterion 2: Can LLM solve it? (try 8 times)
    success_count = 0
    for _ in range(8):
        result = run_llm_agent(task)
        if check_solution(result, task):
            success_count += 1
    
    if success_count == 0:
        return False  # Too hard, reject
    
    # Criterion 3: Can be solved without tools?
    result = run_llm_without_tools(task)
    if check_solution(result, task):
        return False  # Too easy, reject
    
    return True  # Good task!
```

Only tasks passing all criteria are included in ToolScale.

## 🤿 Deep Dive: The Quality Control Pipeline

### Challenge 1: Ensuring Coherent Database Entries

**Problem**: LLM-generated data can be inconsistent.

Example of **bad** entry:
```json
{
    "user_id": "U123",
    "name": "John Smith",
    "email": "jane@example.com",  ← Name/email mismatch
    "registration_date": "2025-03-15",
    "last_login": "2024-01-10"  ← Logged in before registration!
}
```

**Solution**: Multi-step validation

**Validation prompt**:
```
Schema: {schema}
Entry: {entry}

Check:
1. All fields match schema types?
2. Values internally consistent?
3. Data logically reasonable?

Output: {"field": "issue"} or "PASS"
```

**If validation fails**: Regenerate entry or use LLM to fix specific issues.

**Statistics from paper**: 
- Initial pass rate: ~60%
- After one fixing iteration: ~90%
- After two fixing iterations: ~98%

### Challenge 2: Ensuring Solvable Tasks

**The three criteria** (from the paper):

**Criterion 1: Execution correctness**
```python
def check_execution_correctness(task):
    # Snapshot database state
    db_before = deepcopy(database)
    
    # Execute gold action sequence
    for action in task.gold_actions:
        try:
            execute(action)
        except Exception as e:
            return False, f"Action failed: {e}"
    
    # Verify expected changes
    db_after = database
    
    if task.expected_changes:
        for change in task.expected_changes:
            if not verify_change(db_before, db_after, change):
                return False, "Expected change not found"
    
    return True, "Execution successful"
```

**Criterion 2: Process fidelity**
```python
def check_process_fidelity(trajectory, task):
    required_info = task.required_mentions
    
    # Example: Task requires mentioning product price
    if "product_price" in required_info:
        price_pattern = r'\$?\d+\.\d{2}'
        if not re.search(price_pattern, trajectory):
            return False
    
    # Check all required info mentioned
    for info_item in required_info:
        if not mentioned_in_trajectory(info_item, trajectory):
            return False
    
    return True
```

**Criterion 3: Operation completeness**
```python
def check_operation_completeness(trajectory, task):
    # Extract operations from trajectory
    trajectory_ops = extract_operations(trajectory)
    
    # Get operations from gold actions
    gold_ops = extract_operations(task.gold_actions)
    
    # Check if trajectory operated on same entities
    trajectory_entities = {op.entity_id for op in trajectory_ops}
    gold_entities = {op.entity_id for op in gold_ops}
    
    # Must operate on all entities in gold
    if not gold_entities.issubset(trajectory_entities):
        return False
    
    return True
```

**All three must pass** for trajectory to be considered correct.

### Challenge 3: Avoiding Trivial or Impossible Tasks

**Too easy**: Can be solved without tools
```
Bad task: "What is 2+2?"
- LLM can answer directly
- No tools needed
- Doesn't teach orchestration
```

**Too hard**: Even with tools, unreliably solvable
```
Bad task: "Find the secret password in the encrypted database"
- Even with correct tools, LLM fails
- Pass@8 = 0 (fails all 8 attempts)
- Would just confuse training
```

**Just right**: Requires tools, but solvable
```
Good task: "Find all products under $50 in Electronics, 
           then recommend the one with best reviews"
- Requires: search_products(), get_reviews()
- LLM can reason about results
- Pass@8 = 5-7 (solvable but not trivial)
```

**Selection criterion**: Keep tasks with 3 ≤ Pass@8 ≤ 7
- Below 3: Too hard
- Above 7: Too easy (or solvable without tools)

### The Statistics of ToolScale

From Table 5 in the paper:

| Domain | Tools | DB Entries | Tasks |
|--------|-------|------------|-------|
| Finance | 22 | 686 | 396 |
| Sport | 19 | 423 | 247 |
| E-commerce | 15 | 577 | 343 |
| Medicine | 19 | 920 | 622 |
| Entertainment | 24 | 852 | 561 |
| Railway | 25 | 790 | 414 |
| Restaurant | 23 | 683 | 348 |
| Education | 21 | 816 | 426 |
| Travel | 15 | 752 | 331 |
| Weather | 14 | 549 | 375 |

**Total**: ~197 tools, ~7048 database entries, ~4063 tasks

**Diversity metrics**:
- Average tools per domain: 19.7
- Average DB entries per domain: 704.8
- Average tasks per domain: 406.3
- Task complexity: 2-8 tool calls per task

## 🔬 Research Depth: Synthetic Data in Modern AI

### The Rise of Synthetic Data

**Historical context**: 
- 2010s: "Real data is king" - ImageNet, COCO, human annotations
- 2020s: "Synthetic data is viable" - GAIA, Phi models, Llama data

**Key papers on synthetic data**:

1. **Phi-4-mini** (Microsoft, 2025)
   - Trains 4B model primarily on synthetic data
   - Matches much larger models on reasoning
   - Key insight: Quality > quantity for reasoning tasks

2. **Textbooks Are All You Need** (Gunasekar et al., 2023)
   - Phi-1: Trained on synthetic "textbook-quality" code
   - Outperforms models 10x larger
   - Shows that synthetic data can be higher quality than web scrapes

3. **Self-Instruct** (Wang et al., 2022)
   - Uses LLMs to generate their own instruction-following data
   - Bootstrap from small seed set
   - Creates 52K instructions automatically

**ToolScale's contribution**: Extends synthetic data to **multi-turn tool-use scenarios with verifiable outcomes**.

### The Verification Problem

**Key challenge**: How do you know synthetic data is correct?

**Three approaches**:

**1. Human verification** (expensive, doesn't scale)
- Example: MMLU, HumanEval
- Cost: ~$0.50-$5 per example
- ToolScale would cost $2000-$20,000 to verify manually

**2. Rule-based verification** (brittle, limited coverage)
- Example: Code execution (pass/fail tests)
- Limitation: Only works when outputs are deterministic
- ToolScale partial use: Database state checking

**3. LLM-as-judge verification** (scalable, but imperfect)
- Example: AlpacaEval, MT-Bench
- Limitation: Judge can be wrong (especially on hard tasks)
- ToolScale use: Filter obviously bad examples, but also use execution

**ToolScale's hybrid approach**:
```
Use LLMs to generate → Use rules to check executability → 
Use LLMs to solve → Use rules to verify solution → 
Manual spot-checking of 5% → Final dataset
```

This combines strengths of all three approaches.

### Synthetic vs. Real Data: The Trade-offs

**Advantages of synthetic data**:
1. **Scalability**: Generate millions of examples automatically
2. **Control**: Specify exact difficulty, coverage, diversity
3. **Verification**: Can build verification into generation process
4. **Privacy**: No real user data, no privacy concerns
5. **Diversity**: Can ensure even coverage of rare cases

**Disadvantages of synthetic data**:
1. **Distribution shift**: Synthetic ≠ real-world
2. **Artifacts**: LLM-generated data has patterns (e.g., overly polite)
3. **Feedback loops**: Train on LLM data → model inherits LLM biases
4. **Validity**: Hard to ensure synthetic tasks represent real needs

**ToolOrchestra's mitigation strategies**:
- Generate diverse domains (10 different domains)
- Use multiple LLMs for generation (avoid single-model artifacts)
- Validate with execution (not just LLM judgment)
- Test on real benchmarks (HLE, FRAMES, τ²-Bench)

The strong performance on real benchmarks suggests the synthetic training data generalizes well.

### Open Research Questions

1. **Optimal synthetic/real ratio**: Would mixing some real tool-use data improve performance? What ratio?

2. **Domain coverage**: ToolScale has 10 domains. How many domains needed to generalize to arbitrary new domains?

3. **Task complexity curriculum**: Should training start with easy synthetic tasks and progressively get harder? This is **curriculum learning**.

4. **Adversarial synthetic data**: Could we intentionally generate "adversarial" tasks that current model fails on, then retrain? This is **active learning** meets **adversarial training**.

5. **Synthetic data quality metrics**: How do we measure synthetic data quality before expensive training? Current approach: Train and test. Could we predict quality beforehand?

---


## Conclusion

This part’s main takeaway is that high-quality synthetic environments, when carefully validated, can stand in for expensive real-world data and still teach nuanced orchestration strategies. Understanding how ToolScale is built and filtered also helps you judge where the orchestrator is likely to be strong, and where new domains might require additional environment design.

## Academic Papers

57. **Self-Instruct (Synthetic Data Pioneer)**
    - Wang, Y., Kordi, Y., Mishra, S., et al. (2023). "Self-Instruct: Aligning Language Models with Self-Generated Instructions." *ACL 2023*
    - https://arxiv.org/abs/2212.10560

58. **Phi Models (Synthetic Data Success)**
    - Gunasekar, S., Zhang, Y., Aneja, J., et al. (2023). "Textbooks Are All You Need." *arXiv:2306.11644*
    - https://arxiv.org/abs/2306.11644
    - Li, Y., Bubeck, S., Eldan, R., et al. (2023). "Textbooks Are All You Need II: phi-1.5 Technical Report." *arXiv:2309.05463*
    - https://arxiv.org/abs/2309.05463

59. **Phi-4-mini (Latest Synthetic Data)**
    - Abdin, M., et al. (2025). "Phi-4-mini Technical Report: Compact yet Powerful Multimodal Language Models via Mixture-of-LoRAs." *arXiv:2503.01743*
    - https://arxiv.org/abs/2503.01743

60. **Synthetic Data for Code**
    - Rozière, B., Gehring, J., Gloeckle, F., et al. (2024). "Code Llama: Open Foundation Models for Code." *arXiv:2308.12950*
    - https://arxiv.org/abs/2308.12950

61. **AlpacaEval (LLM-as-Judge)**
    - Li, X., Zhang, T., Dubois, Y., et al. (2023). "AlpacaEval: An Automatic Evaluator of Instruction-following Models." *GitHub Repository*
    - https://github.com/tatsu-lab/alpaca_eval

62. **MT-Bench (Judge Evaluation)**
    - Zheng, L., Chiang, W.L., Sheng, Y., et al. (2023). "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena." *NeurIPS 2023*
    - https://arxiv.org/abs/2306.05685

63. **Data Quality for LLMs**
    - Zhou, C., Liu, P., Xu, P., et al. (2024). "LIMA: Less Is More for Alignment." *NeurIPS 2024*
    - https://arxiv.org/abs/2305.11206

64. **Synthetic Data Challenges**
    - Shumailov, I., Shumaylov, Z., Zhao, Y., et al. (2024). "AI Models Collapse When Trained on Recursively Generated Data." *Nature*
    - https://www.nature.com/articles/s41586-024-07566-y

65. **Data Contamination Detection**
    - Golchin, S., & Surdeanu, M. (2023). "Time Travel in LLMs: Tracing Data Contamination in Large Language Models." *arXiv:2308.08493*
    - https://arxiv.org/abs/2308.08493

## Blog Posts and Tutorials

66. **Synthetic Data Generation Guide**
    - "Generating Synthetic Data for Machine Learning"
    - https://www.microsoft.com/en-us/research/blog/synthetic-data-generation/

67. **LLM Data Synthesis**
    - Scale AI. "Synthetic Data for LLM Training"
    - https://scale.com/blog/synthetic-data-llm-training

68. **Self-Instruct Tutorial**
    - "Creating Your Own Instruction Dataset"
    - https://crfm.stanford.edu/2023/03/13/alpaca.html

69. **Quality vs Quantity in Training Data**
    - "Why Data Quality Matters More Than Data Quantity"
    - https://eugeneyan.com/writing/data-quality/

70. **Validation Strategies**
    - "How to Validate Synthetic Training Data"
    - https://towardsdatascience.com/validating-synthetic-training-data-5f2c8b0f3c3d

## GitHub Repositories

71. **Self-Instruct Code**
    - https://github.com/yizhongw/self-instruct

72. **Alpaca Dataset Generation**
    - https://github.com/tatsu-lab/stanford_alpaca

73. **Evol-Instruct (WizardLM)**
    - https://github.com/nlpxucan/WizardLM/tree/main/Evol_Instruct

74. **Magpie (Alignment Data from Scratch)**
    - https://github.com/magpie-align/magpie

75. **Data Cleaning Pipelines**
    - https://github.com/EleutherAI/pile

76. **ToolAlpaca (Tool Use Dataset)**
    - Tang, Q., Deng, Z., Lin, H., et al. (2023). "ToolAlpaca: Generalized Tool Learning for Language Models."
    - https://github.com/tangqiaoyu/ToolAlpaca

77. **APIBench (Tool Evaluation)**
    - https://github.com/ShishirPatil/gorilla

## Tools and Platforms

78. **Gretel.ai (Synthetic Data Platform)**
    - https://gretel.ai/

79. **Mostly AI (Synthetic Data)**
    - https://mostly.ai/

80. **DataCebo (Synthetic Data for Tabular)**
    - https://datacebo.com/

---

