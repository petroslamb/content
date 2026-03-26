# Source Index

This file maps the local literature corpus to the repo's practical architecture guidance. Each paper is assigned one primary chapter here for navigation, even when the paper is useful across multiple chapters.

## Survey Anchor

| Local file | Source | Year | Practical role | Link | Confidence |
| --- | --- | --- | --- | --- | --- |
| `advances-and-challenges-in-foundation-agents.md` | Advances and Challenges in Foundation Agents: From Brain-Inspired Intelligence to Evolutionary, Collaborative, and Safe Systems | 2025 | survey anchor that provides the original chapter map for the repo | https://arxiv.org/abs/2504.01990 | High |

## Memory

| Local file | Paper | Year | Method category | Practical role | Canonical link | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| `papers/memgpt.md` | MemGPT: Towards LLMs as Operating Systems | 2023 | tiered memory management | core mental model for context versus external memory | https://arxiv.org/abs/2310.08560 | High |
| `papers/generative_agents.md` | Generative Agents: Interactive Simulacra of Human Behavior | 2023 | episodic memory and reflection | reference for memory, salience, and reflection loops | https://arxiv.org/abs/2304.03442 | High |
| `papers/memorybank.md` | MemoryBank: Enhancing Large Language Models with Long-Term Memory | 2023 | decay and retention policy | reference for forgetting and refresh policies | https://arxiv.org/abs/2305.10250 | High |
| `papers/mem0.md` | Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory | 2025 | production memory service | deployment-oriented long-term memory reference | https://arxiv.org/abs/2504.19413 | High |
| `papers/hipporag.md` | HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models | 2025 | graph-aware retrieval memory | relational retrieval reference when plain vector search is too shallow | https://arxiv.org/abs/2405.14831 | High |
| `papers/voyager.md` | Voyager: An Open-Ended Embodied Agent with Large Language Models | 2023 | procedural memory and skill library | reference for turning repeated success into reusable skills | https://arxiv.org/abs/2305.16291 | High |

## Reasoning and Planning

| Local file | Paper | Year | Method category | Practical role | Canonical link | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| `papers/react.md` | ReAct: Synergizing Reasoning and Acting in Language Models | 2022 | reason-act-observe loop | default control loop for tool-using agents | https://arxiv.org/abs/2210.03629 | High |
| `papers/least_to_most_prompting.md` | Least-to-Most Prompting Enables Complex Reasoning in Large Language Models | 2022 | progressive decomposition prompting | ordered decomposition default for difficult multi-step reasoning | https://arxiv.org/abs/2205.10625 | High |
| `papers/step_back_prompting.md` | Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models | 2023 | abstraction-first prompting | reset pattern when the model jumps too quickly into brittle local reasoning | https://arxiv.org/abs/2310.06117 | High |
| `papers/self_consistency.md` | Self-Consistency Improves Chain of Thought Reasoning in Language Models | 2022 | consensus sampling | reliability overlay when one reasoning trace is too brittle | https://arxiv.org/abs/2203.11171 | High |
| `papers/llm_plus_p.md` | LLM+P: Empowering Large Language Models with Optimal Planning Proficiency | 2023 | planner-augmented reasoning | bridge from language reasoning to formal planning when the task needs stronger structure | https://arxiv.org/abs/2304.11477 | High |
| `papers/self_refine.md` | SELF-REFINE: Iterative Refinement with Self-Feedback | 2023 | draft-critique-revise loop | cheap iterative improvement pattern for structured outputs | https://arxiv.org/abs/2303.17651 | High |
| `papers/reflexion.md` | Reflexion: Language Agents with Verbal Reinforcement Learning | 2023 | self-improving critique memory | bridge between reasoning critique and learnable episodic memory | https://arxiv.org/abs/2303.11366 | High |
| `papers/chain_of_verification.md` | Chain-of-Verification Reduces Hallucination in Large Language Models | 2023 | verification | default factual reliability overlay | https://arxiv.org/abs/2309.11495 | High |
| `papers/tree_of_thoughts.md` | Tree of Thoughts: Deliberate Problem Solving with Large Language Models | 2023 | branching reasoning search | search-style escalation for tasks with real dead ends and alternatives | https://arxiv.org/abs/2305.10601 | High |
| `papers/lats.md` | Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models | 2024 | search-heavy planning | escalation path for difficult planning tasks | https://arxiv.org/abs/2310.04406 | High |

## Action Systems and Tool Use

| Local file | Paper | Year | Method category | Practical role | Canonical link | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| `papers/toolformer.md` | Toolformer: Language Models Can Teach Themselves to Use Tools | 2023 | tool-use behavior | conceptual bridge from language-only generation to tool invocation | https://arxiv.org/abs/2302.04761 | High |
| `papers/gorilla.md` | Gorilla: Large Language Model Connected with Massive APIs | 2023 | API tool use | tool specification and argument-construction reference | https://arxiv.org/abs/2305.15334 | High |
| `papers/hugginggpt.md` | HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face | 2023 | controller over specialist tools | orchestration reference for multimodal and specialist tool stacks | https://arxiv.org/abs/2303.17580 | High |
| `papers/webagent.md` | A Real-World WebAgent with Planning, Long Context Understanding, and Program Synthesis | 2024 | web action | core reference for browser-based digital action | https://arxiv.org/abs/2307.12856 | High |
| `papers/mind2web.md` | Mind2Web: Towards a Generalist Agent for the Web | 2023 | web action benchmark | generalist web-agent evaluation reference | https://arxiv.org/abs/2306.06070 | High |
| `papers/mobile_agent.md` | Mobile-Agent: Autonomous Multi-Modal Mobile Device Agent with Visual Perception | 2024 | mobile interface action | reference for multimodal device-level action | https://arxiv.org/abs/2401.16158 | Medium |
| `papers/appagent.md` | AppAgent: Multimodal Agents as Smartphone Users | 2023 | GUI action | smartphone interaction reference when APIs are unavailable | https://arxiv.org/abs/2312.13771 | Medium |
| `papers/omniparser.md` | OmniParser for Pure Vision Based GUI Agent | 2024 | GUI perception | reference for turning pixels into usable GUI structure | https://arxiv.org/abs/2408.00203 | Medium |
| `papers/swe_agent.md` | SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering | 2024 | coding agent | core reference for code execution, tests, and repo interaction | https://arxiv.org/abs/2405.15793 | High |
| `papers/opendevin.md` | OpenHands: An Open Platform for AI Software Developers as Generalist Agents | 2025 | coding-agent platform | generalist developer-agent platform reference | https://arxiv.org/abs/2407.16741 | Medium |
| `papers/bird.md` | Can LLM Already Serve as a Database Interface? A BIg Bench for Large-Scale Database Grounded Text-to-SQLs | 2023 | database action | benchmark and design reference for database-facing agents | https://arxiv.org/abs/2305.03111 | High |
| `papers/spider_2_0.md` | Spider 2.0: Evaluating Language Models on Real-World Enterprise Text-to-SQL Workflows | 2025 | enterprise SQL evaluation | realistic evaluation reference for data-facing agents | https://arxiv.org/abs/2411.07763 | High |

## Optimization and Self-Improvement

| Local file | Paper | Year | Method category | Practical role | Canonical link | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| `papers/opro.md` | Large Language Models as Optimizers | 2024 | prompt optimization | reference for treating prompts as optimization targets | https://arxiv.org/abs/2309.03409 | High |
| `papers/textgrad.md` | TextGrad: Automatic "Differentiation" via Text | 2024 | textual optimization feedback | reference for converting critique into structured optimization signals | https://arxiv.org/abs/2406.07496 | High |
| `papers/aflow.md` | AFLOW: Automating Agentic Workflow Generation | 2025 | workflow optimization | search over workflow structure after a baseline exists | https://arxiv.org/abs/2410.10762 | Medium |
| `papers/gptswarm.md` | GPTSwarm: Language Agents as Optimizable Graphs | 2024 | workflow graph optimization | graph-shaped workflow optimization reference | https://arxiv.org/abs/2402.16823 | Medium |
| `papers/mt_bench_chatbot_arena.md` | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena | 2023 | evaluation pattern | reference for scalable model-based evaluation loops | https://arxiv.org/abs/2306.05685 | Medium |

## Multi-Agent Design

| Local file | Paper | Year | Method category | Practical role | Canonical link | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| `papers/autogen.md` | AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation | 2023 | multi-agent orchestration | programmable conversation fabric for multi-agent systems | https://arxiv.org/abs/2308.08155 | High |
| `papers/metagpt.md` | MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework | 2024 | role-based collaboration | core reference for artifact-driven multi-agent workflows | https://arxiv.org/abs/2308.00352 | High |
| `papers/chatdev.md` | ChatDev: Communicative Agents for Software Development | 2023 | role-based pipeline | artifact-oriented software-team simulation reference | https://arxiv.org/abs/2307.07924 | High |
| `papers/mad.md` | Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate | 2024 | debate-style reliability | reference for disagreement-driven answer improvement | https://arxiv.org/abs/2305.19118 | High |
| `papers/reconcile.md` | RECONCILE: Round-Table Conference Improves Reasoning via Consensus among Diverse LLMs | 2023 | consensus reasoning | structured disagreement and reconciliation reference | https://arxiv.org/abs/2309.13007 | High |

## Safety

| Local file | Paper | Year | Method category | Practical role | Canonical link | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| `papers/greshake_indirect_prompt_injection.md` | Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection | 2023 | prompt injection | foundational trust-boundary paper for external content | https://arxiv.org/abs/2302.12173 | High |
| `papers/injecagent.md` | InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents | 2024 | prompt-injection evaluation | benchmark and test reference for tool-integrated prompt injection | https://arxiv.org/abs/2403.02691 | High |
| `papers/toolemu.md` | Identifying the Risks of LM Agents with an LM-Emulated Sandbox | 2024 | sandboxed safety evaluation | core reference for evaluating risky tool behavior safely | https://arxiv.org/abs/2309.15817 | High |
| `papers/agentpoison.md` | AGENT POISON: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases | 2024 | memory poisoning | threat model for durable memory and knowledge stores | https://arxiv.org/abs/2407.12784 | High |
| `papers/poisonedrag.md` | PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models | 2024 | retrieval poisoning | core reference for corpus corruption threats | https://arxiv.org/abs/2402.07867 | High |
| `papers/badrag.md` | BadRAG: Identifying Vulnerabilities in Retrieval Augmented Generation of Large Language Models | 2024 | retrieval security | retrieval attack-surface reference | https://arxiv.org/abs/2406.00083 | High |
| `papers/jamming.md` | Machine Against the RAG: Jamming Retrieval-Augmented Generation with Blocker Documents | 2025 | retrieval jamming | availability-focused retrieval threat reference | https://arxiv.org/abs/2406.05870 | High |
| `papers/agentsmith.md` | Agent Smith: A Single Image Can Jailbreak One Million Multimodal LLM Agents Exponentially Fast | 2024 | inter-agent contamination and multimodal jailbreak propagation | core source for cross-agent contamination through messages, files, and images | https://arxiv.org/abs/2402.08567 | High |
