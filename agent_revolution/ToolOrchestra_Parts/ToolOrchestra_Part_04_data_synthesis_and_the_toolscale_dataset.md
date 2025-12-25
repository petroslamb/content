# The Orchestration Paradigm Series: Dive 4
*How do you generate verifiable training data?*

## Introduction

Training an orchestrator requires examples of orchestration. You need thousands of trajectories showing tasks, tool sequences, and outcomes—and those trajectories must be verifiable (we know if the final answer is correct) and non-trivial (they can't be solved without tools). Real-world orchestration data at this scale essentially doesn't exist. Enterprise systems have proprietary logs. Academic datasets have dozens of examples, not thousands. And manually creating diverse orchestration examples would cost millions of dollars.

ToolOrchestra solves this with ToolScale: a synthetic data generation pipeline that produces 4,000+ high-quality, verifiable orchestration trajectories across 10 domains for pennies per example. This dive explains how ToolScale works and why synthetic data—done carefully—can train systems that generalize to real benchmarks.

---

## 🌊 Surface Level: The Data Scarcity Problem

Consider what training data for orchestration would ideally contain:

A complex task that requires multiple tools. A sequence of tool calls that efficiently solves the task. The final answer that we know is correct. Metadata about which tools were available, what they cost, and how long they took.

Where does such data come from?

**Option 1: Real user logs.** Companies operating AI assistants have exactly this data. When a user asks Claude or ChatGPT a question, and the system uses web search or code execution, the full trajectory exists in logs. But this data is proprietary, privacy-sensitive, and not released for research.

**Option 2: Manual annotation.** Hire experts to create orchestration examples. This approach has two problems: it's expensive (thousands of expert-hours to create thousands of examples) and it's biased (annotators tend to create tasks in styles they're familiar with, limiting diversity).

**Option 3: Existing research datasets.** Academic datasets for tool use exist but are small. ToolBench has hundreds of examples. WebGPT's dataset is a few thousand. None have the scale and diversity needed for training robust orchestrators.

**Option 4: Synthetic generation.** Use AI to create the training data. This sounds circular—using AI to train AI—but has proven powerful in other domains. Phi models from Microsoft achieved strong performance partly through training on synthetic textbook-quality data. Constitutional AI uses AI-generated critiques to train AI alignment.

ToolScale takes Option 4 and addresses its key challenge: verification. Synthetic data can be whatever the generator produces, including wrong answers and impossible tasks. ToolScale's innovation is a pipeline that generates tasks with guaranteed correct answers, filters for quality, and ensures non-triviality.

---

## 🏊 Shallow Dive: The ToolScale Pipeline

ToolScale generates data in two phases: first create environments (databases, tools, domain knowledge), then create tasks that use those environments.

### Phase 1: Environment Creation

Each domain gets its own simulated world with realistic structure.

**Database generation.** The pipeline prompts a capable model (GPT-5 in the original implementation) to generate domain-specific databases. For the airline domain: flights, passengers, tickets, airports, airlines. For human resources: employees, departments, positions, salaries, benefits. For retail: products, customers, orders, inventories, suppliers.

These databases aren't random. They have realistic schemas (proper foreign key relationships), realistic data (Coherent business logic—prices that make sense, schedules that don't conflict), and sufficient complexity (thousands of rows, not just toy examples). An airline database might have 50,000 flights across 200 airports with realistic routing patterns.

**Tool function generation.** For each database, the pipeline generates domain-specific tools—Python functions that query and manipulate the data. An airline database might have: `search_flights(origin, destination, date)`, `get_passenger_booking(passenger_id)`, `check_seat_availability(flight_id)`, and so on. A retail database might have: `search_products(query)`, `get_inventory(product_id, store_id)`, `check_order_status(order_id)`.

Each tool specification includes its function signature, expected behavior, and a working implementation. The tools are real Python code that can be executed against the generated databases, enabling verification.

### Phase 2: Task Generation

With environments in place, the pipeline generates tasks that exercise them.

**User intent generation.** First, generate a high-level user intent: "A customer wants to know if they can reschedule their flight to arrive before an important meeting." This captures what a realistic user might want without specifying the exact steps.

**Task specification.** From the intent, generate the specific task with all parameters filled in: "Can passenger John Smith (ID: PAX-12847) reschedule flight UA2847 on March 15 to arrive before 2 PM in Chicago? If so, what options are available and what fees apply?"

**Solvability check.** Critically, the pipeline verifies that the task is solvable. It runs a reference solution—typically GPT-5 with full access to tools—and checks whether a correct answer can be obtained. Tasks where even the reference solution fails are discarded; they might be ambiguous, contradictory, or dependent on information not in the database.

**Difficulty calibration.** The pipeline aims for tasks that are solvable but non-trivial. Tasks where the answer is immediately obvious (single tool call, direct lookup) are too easy. Tasks requiring 5+ coordinated tool calls, synthesis of multiple information sources, or multi-step reasoning are kept. This is calibrated through the "Pass@8" criterion: the task should be solvable by GPT-5 within 8 attempts but not always on the first try.

### The Verification Guarantee

ToolScale's key property is that every task has a known correct answer. This is guaranteed by construction:

The database is generated with known ground truth. The tools query the database deterministically. The reference solution produces an answer that we verify against the database directly.

For example, a flight rescheduling task has a correct answer because we know every flight in the database, their times, available seats, and pricing. We can check whether the proposed reschedule options actually exist and whether the quoted fees are correct.

This contrasts with real-world data where "correct" might be subjective, or with hallucinated synthetic data where the generator might produce plausible but wrong answers. ToolScale's answers are verifiable against a deterministic ground truth.

---

## 🤿 Deep Dive: Quality Filtering and Diversity

Generating candidate tasks is relatively easy. Ensuring quality requires careful filtering.

### Filter 1: Execution Correctness

Every generated task includes a reference solution—the sequence of tool calls that solves it. The filter checks whether executing this solution against the actual database produces the claimed answer. If there's any mismatch—wrong return values, incorrect final answer, execution errors—the task is discarded.

This catches cases where the task generation hallucinated about database contents. The generator might claim "flight UA2847 on March 15 has 12 seats available," but if the actual database has only 8, the reference solution will return wrong results and the task fails the filter.

### Filter 2: Process Fidelity

A task might have the right final answer through a wrong process—getting lucky with incorrect intermediate steps. The process fidelity filter checks whether each step in the reference solution makes sense: Are the tool calls plausible given the task? Do the tool returns match the database state? Is the reasoning connecting steps coherent?

This is somewhat more subjective than execution correctness, implemented through another LLM-as-judge pass. The judge evaluates whether the trajectory represents genuinely correct problem-solving or accidental correctness.

### Filter 3: Operation Completeness

Some tasks can be solved with fewer tool calls than intended. A task designed to require 5 tool calls might actually be solvable with 2 if the model finds a shortcut. The operation completeness filter verifies that the intended operations are actually necessary—that the task genuinely requires the complexity designed into it.

This prevents the dataset from being dominated by easy tasks that happen to look complex in their reference solutions.

### Filter 4: Pass@8 Criterion

Finally, each task is tested against the Pass@8 criterion. GPT-5 attempts the task 8 times independently. If it succeeds on all 8, the task is too easy—trivial for capable models. If it succeeds on fewer than 1, the task is too hard—even capable models can't solve it reliably. Tasks where 1-7 attempts succeed hit the sweet spot: challenging but solvable.

### Domain Distribution

After filtering, ToolScale achieves reasonable balance across its 10 domains:

| Domain | Tasks | Avg. Turns | Avg. Tools |
|--------|-------|------------|------------|
| Airline | 450 | 7.2 | 4.1 |
| Finance | 420 | 8.1 | 5.3 |
| Retail | 410 | 6.8 | 3.9 |
| HR | 380 | 5.9 | 3.2 |
| Hospitality | 390 | 6.4 | 3.7 |
| Academic | 350 | 9.1 | 5.8 |
| Media | 370 | 7.5 | 4.4 |
| Software | 400 | 8.8 | 6.1 |
| Manufacturing | 360 | 7.1 | 4.0 |
| Government | 340 | 6.2 | 3.5 |

The academic and software domains tend to have higher complexity (more turns, more tools) because they naturally involve multi-step research and technical problem-solving. Government tends to be simpler (procedural lookups). This diversity helps the trained orchestrator generalize.

---

## 🔬 Research Depth: Synthetic Data in the Age of AI

ToolScale is part of a broader trend: using AI-generated data to train AI systems.

### The Phi Phenomenon

Microsoft's Phi series of small language models demonstrated that synthetic training data could outperform web scrapes at smaller scales. Phi-1 was trained on "textbook-quality" synthetic data—text generated by larger models in the style of educational materials—and achieved remarkable performance for its size.

The insight was that data quality might matter more than quantity. A smaller dataset of carefully constructed examples could teach more effectively than a massive dataset of internet text containing noise, errors, and harmful content.

ToolScale applies this insight to orchestration. Rather than scraping whatever tool-use logs exist (sparse, noisy, biased toward particular domains), it generates tailored examples that cover the orchestration behaviors we want to train.

### The Verification Problem

Synthetic data's weakness is that it can be wrong in ways that are hard to detect. When a generator hallucinates, the hallucination might be fluent and plausible but factually false. Without verification, training on such data teaches the student model to hallucinate in the same ways.

ToolScale addresses this through its ground-truth database approach. Because every task is grounded in a deterministic database, correctness is objectively verifiable. This is unlike, say, generating "chemistry textbook" content where verifying every claim would require expert review.

The limitation is that only certain types of tasks admit such verification. Factual lookup against known databases: verifiable. Complex reasoning about open-ended questions: harder to verify. ToolScale works because orchestration can often be reduced to database operations where correctness is clear.

### Transfer to Real Benchmarks

A skeptic might ask: if ToolScale generates synthetic database tasks, why would training on it help with real benchmarks like HLE (academic questions) or FRAMES (fact verification)?

The answer is that orchestration patterns transfer. The decision of "when to search versus compute" is similar whether you're searching an airline database or searching the web. The pattern of "escalate to expensive model when cheap model fails" applies regardless of domain. The skill of "verify results by checking with alternative method" works for any verifiable task.

Evidence for transfer: ToolOrchestra achieves strong performance on HLE, FRAMES, and τ²-Bench despite none of these being in ToolScale's 10 domains. The orchestration skills generalize even when the specific task content doesn't.

### Synthetic Data Scaling

An open question is how far synthetic data can scale. ToolScale has 4,000+ tasks. Could you have 40,000? 400,000? Would more help?

There are likely diminishing returns. Additional tasks within existing domains add less than tasks in new domains. And domain coverage in ToolScale is already broad—10 diverse areas with realistic complexity. Adding an 11th domain might help less than adding the 3rd domain did.

There may also be quality ceilings. As you scale generation, the filters must work harder to maintain quality. If 1% of synthetic data has subtle bugs that pass filtering, more data means more bugs in training.

These are empirical questions that future work will address. For now, ToolScale's 4,000+ tasks are sufficient to train orchestrators that generalize to real benchmarks.

---

## Conclusion

ToolScale demonstrates that the data scarcity problem for orchestration is solvable through careful synthetic generation. The keys are: grounding in verifiable databases (so correctness is objective), multi-stage filtering (so quality is maintained), domain diversity (so generalization is encouraged), and difficulty calibration (so tasks are neither trivial nor impossible).

The cost is minimal compared to alternatives. Generating ToolScale's 4,000+ tasks requires API calls to generate environments, tasks, and reference solutions—perhaps $10,000 total in compute costs. Compare this to paying human experts to manually create and verify thousands of multi-step orchestration examples: easily $1M+ in labor costs. Synthetic generation makes research tractable.

The next dive examines the other side of the training loop: evaluation. Once you've trained an orchestrator on ToolScale, how do you measure whether it's any good?

---

## References

### Synthetic Data for LLMs

1. **Phi-1: Textbook Quality Data**
   - Gunasekar, S., et al. (2023). "Textbooks Are All You Need." *arXiv:2306.11644*
   - https://arxiv.org/abs/2306.11644

2. **Phi-2 and Phi-3**
   - Microsoft Research. (2024)
   - https://arxiv.org/abs/2404.14219

3. **Self-Instruct**
   - Wang, Y., et al. (2023). "Self-Instruct: Aligning Language Models with Self-Generated Instructions." *ACL 2023*
   - https://arxiv.org/abs/2212.10560

### Tool Learning Datasets

4. **ToolBench**
   - Qin, Y., et al. (2023). "ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs." *ICLR 2024*
   - https://arxiv.org/abs/2307.16789

5. **API-Bank**
   - Li, M., et al. (2023). "API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs." *EMNLP 2023*
   - https://arxiv.org/abs/2304.08244

### Data Quality and Verification

6. **Data Quality for ML**
   - Sambasivan, N., et al. (2021). "Everyone Wants to Do the Model Work, Not the Data Work." *CHI 2021*
   - https://research.google/pubs/pub49953/

7. **Self-Training and Synthetic Data**
   - Du, Y., et al. (2023). "Self-Training with Limited Labeled Data." *arXiv:2302.10202*
   - https://arxiv.org/abs/2302.10202

### Generalization Theory

8. **Transfer Learning**
   - Pan, S.J., & Yang, Q. (2010). "A Survey on Transfer Learning." *IEEE TKDE*
   - https://ieeexplore.ieee.org/document/5288526

---
