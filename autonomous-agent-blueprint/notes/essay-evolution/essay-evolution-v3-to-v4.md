# Rewrite Ledger V3

Internal drafting support for the `Operating Agents` `v3` package. This version restores visible authority through full inline citations and longer source tails, varies the opening move across the series, and treats optimization as a bonus post rather than the emotional closer of the core run.

## Launch Note

- Thesis: Most agent writing still starts with the model, but the practical break between a demo and a deployable system lives in the operating layers around action, reasoning, memory, coordination, safety, and evaluation.
- Target reader payoff: A skeptical builder understands why this series is not another model roundup and why the reading order is a build order.
- Central scenario: The reader has already built something that demos well and becomes expensive once side effects, long horizons, or approvals enter the picture.
- Must-keep source assets: `00-series-preface.md`, `foundation-agents-practical-distillation.md`, `foundation-agents-practical-chapters-guide.md`, `architecture review checklist`.
- Cuts to make from `v2`: Do not let the launch note sound like a miniature seventh essay. Keep the frame crisp, but restore visible source weight and the bridge into the blueprint layer.
- Final end-section sources: survey framing, practical chapters guide, practical distillation, architecture review checklist.

## Part I: Action

- Thesis: The step from assistant to agent is not a model upgrade. It is the moment language becomes accountable state change.
- Target reader payoff: The reader gets a practical way to choose action surfaces and diagnose tool-use failures by seam rather than by vague complaints about model behavior.
- Central scenario: A procurement workflow that sounded operational in demos, then failed on schema accuracy and partial acknowledgments once it was allowed to write.
- Must-keep source assets: `01-action-tool-use.md`, `03-action-tool-use-blueprint.md`, `failure-mode catalog`, `papers/toolformer.md`, `papers/gorilla.md`, `papers/swe_agent.md`, `papers/spider_2_0.md`.
- Cuts to make from `v2`: Keep the core narrative, but reduce repeated definitions of agency and restore explicit source support inside the body.
- Final end-section sources: builder blueprint, Toolformer, Gorilla, SWE-agent, BIRD, Spider 2.0, WebAgent, OmniParser.

## Part II: Reasoning

- Thesis: Most reasoning failures in production are scaffold failures. Teams keep shopping for a smarter mind when the real problem is the wrong structure.
- Target reader payoff: The reader gets a diagnosis framework that maps failure shapes to the lightest scaffold that fixes them.
- Central scenario: A claims-processing workflow that looked fluent, skipped dependencies, and improved only after the task was split into explicit checks and verification.
- Must-keep source assets: `02-reasoning-planning.md`, `02-reasoning-planning-blueprint.md`, `failure-mode catalog`, `papers/react.md`, `papers/least_to_most_prompting.md`, `papers/chain_of_verification.md`, `papers/tree_of_thoughts.md`, `papers/lats.md`.
- Cuts to make from `v2`: Replace the familiar enterprise-failure cold open with a direct thesis opening, keep one table, and make the piece feel diagnostic rather than survey-like.
- Final end-section sources: builder blueprint, ReAct, Least-to-Most, Chain-of-Verification, Self-Consistency, Tree of Thoughts, LATS.

## Part III: Memory

- Thesis: Memory is not storage. It is governance over what the agent is allowed to keep, retrieve, reuse, and forget across time.
- Target reader payoff: The reader gets a durable memory architecture instead of another argument for larger context windows or larger vector stores.
- Central scenario: A policy assistant that began returning outdated but plausible answers because old and new states were competing in the same unmanaged store, plus a coding-agent example where history clutter blocked procedural learning.
- Must-keep source assets: `03-memory.md`, `01-memory-blueprint.md`, `use-cases/enterprise-agent.md`, `use-cases/coding-agent.md`, `papers/memgpt.md`, `papers/generative_agents.md`, `papers/memorybank.md`, `papers/reflexion.md`, `papers/mem0.md`, `papers/voyager.md`, `papers/hipporag.md`.
- Cuts to make from `v2`: Change the opening shape, keep the four-layer map, and restore a serious evidence tail with one full paragraph per anchor source.
- Final end-section sources: builder blueprint, MemGPT, Generative Agents, MemoryBank, Reflexion, Mem0, Voyager, HippoRAG.

## Part IV: Multi-Agent

- Thesis: Multi-agent systems solve three different problems, and most disappointing multi-agent systems are built by confusing them.
- Target reader payoff: The reader can distinguish role separation, reliability through critique, and task decomposition through artifact handoffs, then choose the right topology only when a second agent buys a real boundary.
- Central scenario: A reporting pipeline that became slower and harder to debug after it was split into several named roles with soft conversational handoffs.
- Must-keep source assets: `04-multi-agent.md`, `05-multi-agent-design-blueprint.md`, `papers/metagpt.md`, `papers/chatdev.md`, `papers/autogen.md`, `papers/mad.md`, `papers/reconcile.md`, `architecture review checklist`.
- Cuts to make from `v2`: Open with the three-problems thesis immediately, push artifact handoffs harder, and make the human role feel architectural rather than tacked on.
- Final end-section sources: builder blueprint, MetaGPT, ChatDev, AutoGen, MAD, RECONCILE, architecture review checklist.

## Part V: Safety

- Thesis: Agent safety is interface architecture. The system is only as safe as the boundaries between content, memory, tools, handoffs, and approvals.
- Target reader payoff: The reader gets a concrete attack-chain model and a boundary-by-boundary control map tied to real agent capabilities.
- Central scenario: A support or operations agent reads hostile content, retrieves poisoned material, preserves it, and turns it into an internal action chain.
- Must-keep source assets: `05-safety.md`, `06-safety-blueprint.md`, `failure-mode catalog`, `papers/greshake_indirect_prompt_injection.md`, `papers/injecagent.md`, `papers/poisonedrag.md`, `papers/badrag.md`, `papers/jamming.md`, `papers/agentsmith.md`, `papers/toolemu.md`.
- Cuts to make from `v2`: Keep the attack-chain opener, deepen the middle, and restore full source weight without losing pace.
- Final end-section sources: builder blueprint, Greshake et al., InjecAgent, PoisonedRAG, BadRAG, Jamming, Agent Smith, ToolEmu.

## Bonus: Optimization

- Thesis: Most agent optimization is fake. If you cannot name which layer is failing and measure it against a stable objective, you are editing the system, not optimizing it.
- Target reader payoff: The reader gets a conservative improvement order that starts with evaluation and contracts, then moves outward toward workflow search and bounded self-improvement.
- Central scenario: A live document workflow spent weeks in prompt churn while the real problem lived in evaluation design, schema quality, and weak metadata.
- Must-keep source assets: `06-optimization.md`, `04-optimization-self-improvement-blueprint.md`, `architecture review checklist`, `failure-mode catalog`, `papers/opro.md`, `papers/textgrad.md`, `papers/reflexion.md`, `papers/aflow.md`, `papers/gptswarm.md`, `papers/mt_bench_chatbot_arena.md`, `papers/voyager.md`.
- Cuts to make from `v2`: Treat the post as a bonus, open polemically, keep the operational order explicit, and support the argument with denser inline citation.
- Final end-section sources: builder blueprint, OPRO, TextGrad, Reflexion, Voyager, AFLOW, GPTSwarm, MT-Bench and Chatbot Arena.
