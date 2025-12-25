# The Orchestration Paradigm Series: Dive 10a
*How did we get from Toolformer to ToolOrchestra?*

## Introduction

Every research breakthrough stands on the shoulders of prior work. ToolOrchestra did not emerge from nowhere; it represents the culmination of five years of increasingly sophisticated attempts to teach language models when and how to reach beyond their own parameters. This dive traces that evolutionary lineage, examining what each predecessor contributed and where each fell short, so you can see exactly what makes ToolOrchestra's approach genuinely novel rather than incremental.

Understanding this history serves a practical purpose too. If you want to build orchestration systems of your own, knowing which ideas have already been tried—and which limitations have already been discovered—will save you from reinventing punctured wheels.

---

## 🌊 Surface Level: The Five-Year Journey

Think of language models as increasingly capable students. In 2020, they could write essays but couldn't use a calculator. By 2025, they learned to use hundreds of tools, but still made poor choices about which tools to use when. ToolOrchestra represents the next step: a model that doesn't just know how to use tools, but knows when each tool is worth its cost.

The journey from "can't use tools" to "uses tools wisely" happened through distinct phases. First came the realization that models could learn tool syntax through self-supervision. Then came the scaling of tool libraries from a handful to thousands. Next came reinforcement learning to optimize not just whether tools work, but how efficiently they're used. Finally came the insight that other AI models could themselves be treated as tools—leading to the orchestration paradigm where a small coordinator conducts a symphony of specialists.

Each phase built on the last. Each phase also revealed new limitations that motivated the next breakthrough.

---

## 🏊 Shallow Dive: The Evolutionary Tree

### Phase 1: Teaching Models They Can Use Tools (2023)

Before Toolformer, the dominant assumption was that tool use required explicit programming. You would write code that called APIs, and the language model would generate text that your code would parse and route. The model itself was a passive generator; all the intelligence about when to invoke external resources lived in handcrafted systems.

**Toolformer** by Schick et al. at Meta changed this conception. Their key insight was that language models could teach themselves to use tools through a clever self-supervised process. They would take existing text, insert tool calls at positions where tools might help, execute those calls, and keep only the insertions that improved the model's predictions. Through this process, a model learned not just the syntax of calling a calculator or search engine, but when such calls were actually beneficial.

The brilliance of Toolformer lay in its simplicity. No human labeling was required. No reward model was needed. The supervision signal came from the model's own predictive loss: if adding a tool call improved next-token prediction, the call was worth learning.

But Toolformer had significant limitations. It worked with a handful of tools—calculator, search, calendar, translation, and a question-answering system. It couldn't scale to large tool libraries. And most critically for our story, it operated only on single models using single tools. The idea of coordinating multiple models or optimizing for efficiency beyond raw accuracy was not on the radar.

### Phase 2: Scaling to Real-World APIs (2023-2024)

**ToolLLM** by Qin et al. asked what would happen if you scaled tool learning from five tools to sixteen thousand. They scraped RapidHub, a marketplace of real-world APIs covering everything from weather forecasts to stock prices to social media analytics. Using GPT-4 to generate training dialogues showing how to use these APIs, they created a dataset for supervised fine-tuning.

The scale was impressive, but the approach had two fundamental weaknesses. First, it relied entirely on supervised learning. The model learned to mimic GPT-4's decisions about tool use, but it couldn't discover better strategies through trial and error. Second, and more relevant to ToolOrchestra's contribution, ToolLLM optimized only for whether tools were used correctly—not whether they were used efficiently. A solution that called ten expensive APIs when one would suffice received the same training signal as the efficient solution.

**Gorilla** by Patil et al. focused specifically on the challenge of accurate API invocation. Their key contribution was a retrieval-augmented approach where the model could look up API documentation at inference time, reducing hallucination of incorrect parameters. This addressed a practical failure mode—models confidently calling APIs with wrong argument schemas—but again focused on correctness rather than efficiency or coordination.

### Phase 3: Reinforcement Learning Enters the Picture (2024-2025)

The supervised learning paradigm hit its ceiling. No matter how good your training data, supervised models can only mimic what they've seen. They cannot discover novel strategies or optimize for objectives not explicitly demonstrated in examples.

**WebGPT** by Nakano et al. at OpenAI was among the first to apply reinforcement learning to tool use, specifically for web search. They trained a model to navigate the web, issue queries, and synthesize answers, using human feedback as the reward signal. The model learned not just to search, but to craft better queries, follow productive links, and avoid time-wasting tangents.

WebGPT proved that RL could teach sophisticated tool use behaviors that supervised learning missed. But it focused on a single tool (web browsing) and required expensive human feedback for every trajectory.

**ToRL** by Li et al. scaled tool-integrated RL, training models to use multiple tools through the GRPO algorithm that ToolOrchestra would later adopt. But ToRL optimized for task success without considering cost, latency, or user preferences. A trajectory that succeeded by calling GPT-5 twenty times received the same reward as a trajectory that succeeded with a single well-chosen call.

**OTC** (Optimal Tool Calls) by Wang et al. introduced the idea of penalizing tool calls directly in the reward function. This was a step toward efficiency—the model learned to avoid unnecessary calls. But the penalty was uniform. Calling an expensive API cost the same in the reward function as calling a cheap one. There was no fine-grained cost modeling, and certainly no mechanism for respecting user preferences about which trade-offs mattered.

### Phase 4: The Model-as-Tool Insight (2025)

All prior work treated tools as utilities: calculators, search engines, code interpreters, databases. ToolOrchestra made the conceptual leap to treating other language models as tools. GPT-5 wasn't just a competitor or a benchmark—it was a callable function with a cost, a latency, and a capability profile.

This insight unlocked the orchestration paradigm. Once you view GPT-5 as a tool, the question becomes: when is it worth spending $0.10 to call GPT-5 versus $0.001 to call a specialized 7B model? This is fundamentally an economic question, and ToolOrchestra's multi-objective reward design treats it as such.

The economic framing also enabled user preference alignment. Different users have different budgets, different latency tolerances, and different accuracy requirements. By parameterizing the reward function with a preference vector, ToolOrchestra could learn to serve all of them from a single training run.

---

## 🤿 Deep Dive: Technical Comparisons

Let us examine the precise technical differences between ToolOrchestra and its predecessors. These comparisons matter because they illuminate exactly which design choices explain the performance gains.

### ToolOrchestra vs. Chain-of-Thought

Chain-of-Thought prompting, introduced by Wei et al. in 2022, taught models to verbalize their reasoning before producing answers. The famous prompt "Let's think step by step" elicited intermediate steps that improved accuracy on complex problems.

ToolOrchestra utilizes Chain-of-Thought reasoning within its trajectories—the orchestrator reasons about which tool to call and why. But the differences are substantial. Chain-of-Thought operates entirely within the model's internal reasoning; ToolOrchestra breaks out into external tool calls that bring new information. Chain-of-Thought is prompted behavior that anyone can elicit; ToolOrchestra's coordination strategy is learned through reinforcement and varies based on user preferences. Chain-of-Thought has no cost; ToolOrchestra explicitly optimizes the cost-benefit trade-off of each external call.

The relationship is complementary rather than competitive. ToolOrchestra uses Chain-of-Thought for its internal deliberation; it uses tool calls for its external actions.

### ToolOrchestra vs. ReAct

ReAct, by Yao et al., interleaves reasoning (Thought) with tool use (Action) and information gathering (Observation). A ReAct trajectory might look like:

> Thought: I need to find the population of Tokyo.
> Action: Search[population of Tokyo]
> Observation: Tokyo's population is approximately 14 million.
> Thought: Now I can answer the question.

This structure is nearly identical to ToolOrchestra's trajectories. Both alternate between reasoning and action. The crucial differences lie in how behaviors are acquired and what they optimize.

ReAct is prompted. You provide few-shot examples showing the Thought-Action-Observation cycle, and the model imitates that format. ToolOrchestra is trained through reinforcement learning on thousands of trajectories with explicit rewards for accuracy, cost, and preference alignment. 

ReAct has no notion of tool cost. A ReAct agent might call GPT-5 for a trivial question because the prompt examples happened to show GPT-5 calls. ToolOrchestra has internalized the cost structure and will use cheaper tools when they suffice.

ReAct's behavior is determined by the prompt examples. Change the examples and you change the behavior, but you cannot easily instill new optimization objectives. ToolOrchestra's behavior is determined by its learned policy, which has been shaped by the multi-objective reward to balance dimensions that prompt engineering cannot capture.

### ToolOrchestra vs. Agent Frameworks

Practical systems like AutoGPT, BabyAGI, LangChain agents, and LlamaIndex agents provide scaffolding for multi-turn tool use. These frameworks are enormously valuable for rapid prototyping and production deployment. But they share a common characteristic: the orchestration logic is hand-designed.

An AutoGPT workflow might specify: "First decompose the task, then for each subtask decide whether to search the web or generate directly, then synthesize results." This logic is written by a human engineer based on intuition about what works. When it fails, you debug by adjusting prompts or adding special-case handlers.

ToolOrchestra discovers its orchestration strategy through learning. The training process explores many possible strategies and reinforces those that achieve high reward. This means ToolOrchestra can find strategies that would never occur to a human designer—subtle patterns like "call the math model first, but if it returns a very short answer, verify with a different model before trusting it."

The frameworks' strength is flexibility: you can quickly adapt them to new domains by editing prompts and workflows. ToolOrchestra's strength is optimality: within its trained domain, it finds strategies that outperform hand-designed alternatives. The practical question is whether optimality is worth the training cost, and ToolOrchestra's benchmark results suggest that for high-stakes applications, it often is.

### ToolOrchestra vs. Mixture of Experts

Mixture of Experts (MoE) architectures like Mixtral and GLaM route different tokens to different expert subnetworks within a single model. A router network learns which experts should process which inputs.

The analogy to ToolOrchestra is tempting: both involve routing decisions to specialists. But the granularity, training, and execution differ fundamentally.

MoE operates at token level. Each token in a sequence might be routed to a different expert, and the experts are homogeneous—same architecture, different parameters. ToolOrchestra operates at task level. Entire subtasks are routed to completely heterogeneous systems: some are language models, some are code interpreters, some are search APIs.

MoE is trained end-to-end with backpropagation. Gradients flow through the router and experts together. ToolOrchestra's tools are black boxes. You cannot backpropagate through a GPT-5 API call. Reinforcement learning is necessary precisely because the orchestrator must learn from outcomes rather than gradients.

MoE's experts run in parallel and their outputs combine. ToolOrchestra's tools run sequentially, with each tool's output informing the next decision. The orchestrator learns multi-turn strategies that MoE's single-pass architecture cannot express.

The conceptual connection is real—both are "divide and conquer" approaches to intelligence—but the mechanisms are different enough that insights from MoE research don't directly transfer.

---

## 🔬 Research Depth: The Compound AI Thesis

ToolOrchestra's contribution fits within a broader intellectual movement that questions the scaling paradigm.

For five years, the dominant research strategy was clear: train larger models on more data. The logic was empirically supported. GPT-3 was better than GPT-2. GPT-4 was better than GPT-3. Scaling laws predicted that this would continue. Bigger was better.

But cracks appeared. Training the largest models required billion-dollar clusters. Inference costs made deployment prohibitive for many applications. And the returns began diminishing—each doubling of compute yielded smaller improvements.

The **Compound AI Systems** thesis, articulated by Zaharia et al. at Berkeley AI Research in 2024, proposed an alternative. Instead of investing in ever-larger monolithic models, invest in systems that compose specialized components: retrievers, generators, verifiers, tools, and other models. The compound system could exceed any single model's capability while remaining deployable and affordable.

ToolOrchestra is a proof of concept for this thesis. An 8B orchestrator achieving 37.1% on Humanity's Last Exam—versus GPT-5's 35.1%—demonstrates that composition can beat scale. The orchestrator alone couldn't pass a PhD exam. GPT-5 alone couldn't optimize cost. Together, orchestrated intelligently, they beat either alone.

The thesis makes predictions that future research can test. If compound systems consistently outperform monoliths at equivalent inference cost, we should see industry investment shift from bigger models to better orchestration. If orchestrators can be trained to coordinate arbitrary tool sets, we should see general-purpose orchestration as a product category. If multi-objective optimization proves essential for real-world deployment, we should see ToolOrchestra's preference-aware training become standard.

---

## Conclusion

The path from Toolformer to ToolOrchestra spans five years and represents a fundamental evolution in how we think about AI capability. Early work proved that models could learn tool syntax. Scaled efforts proved that models could handle thousands of APIs. Reinforcement learning proved that models could optimize beyond what supervised examples demonstrate. And ToolOrchestra proved that models could coordinate heterogeneous intelligence efficiently and according to user preferences.

Each step along this path closed certain questions and opened new ones. ToolOrchestra closes the question of whether efficient orchestration is possible. It opens questions about recursive orchestration, continual learning, and multi-agent coordination—topics we will explore in the following dives.

---

## References

### Tool Learning Foundations

1. **Toolformer**
   - Schick, T., et al. (2023). "Toolformer: Language Models Can Teach Themselves to Use Tools." *NeurIPS 2023*
   - https://arxiv.org/abs/2302.04761

2. **ToolLLM**
   - Qin, Y., et al. (2023). "ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs." *ICLR 2024*
   - https://arxiv.org/abs/2307.16789

3. **Gorilla**
   - Patil, S.G., et al. (2023). "Gorilla: Large Language Model Connected with Massive APIs." *arXiv:2305.15334*
   - https://arxiv.org/abs/2305.15334

### Reinforcement Learning for Tools

4. **WebGPT**
   - Nakano, R., et al. (2021). "WebGPT: Browser-assisted Question-Answering with Human Feedback." *arXiv:2112.09332*
   - https://arxiv.org/abs/2112.09332

5. **ToRL**
   - Li, X., Zou, H., & Liu, P. (2025). "ToRL: Scaling Tool-Integrated RL." *arXiv:2503.23383*
   - https://arxiv.org/abs/2503.23383

6. **OTC**
   - Wang, H., et al. (2025). "OTC: Optimal Tool Calls via Reinforcement Learning." *arXiv:2504.23456*
   - https://arxiv.org/abs/2504.23456

### Compound AI Systems

7. **The Shift from Models to Compound AI Systems**
   - Zaharia, M., et al. (2024). BAIR Blog
   - https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/

### Reasoning Approaches

8. **Chain-of-Thought Prompting**
   - Wei, J., et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." *NeurIPS 2022*
   - https://arxiv.org/abs/2201.11903

9. **ReAct**
   - Yao, S., et al. (2023). "ReAct: Synergizing Reasoning and Acting in Language Models." *ICLR 2023*
   - https://arxiv.org/abs/2210.03629

### Mixture of Experts

10. **Mixtral**
    - Jiang, A.Q., et al. (2024). "Mixtral of Experts." *arXiv:2401.04088*
    - https://arxiv.org/abs/2401.04088

---
