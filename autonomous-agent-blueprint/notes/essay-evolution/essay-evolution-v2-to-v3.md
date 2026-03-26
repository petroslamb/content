# Rewrite Ledger V2

Internal drafting support for the `Operating Agents` rewrite package. This file is not part of the public series. Its job is to keep the seven public pieces differentiated and to stop the essays from drifting back into the same shape.

## Launch Note

- Thesis: Most agent writing starts with the model, but the real line between prototype and deployment is the control layer around action, reasoning, memory, handoffs, safety, and measurement.
- Target reader payoff: A skeptical builder immediately understands why this series is not another model roundup and why the reading order is a build order.
- Central scenario: The reader has already built something that demos well and fails the moment real side effects, long horizons, or approvals appear.
- Must-keep source assets: `00-series-preface.md`, `foundation-agents-practical-distillation.md`, `foundation-agents-practical-chapters-guide.md`.
- Cuts to make from the current draft: Do not let the launch note become a miniature seventh essay. Cut the long reference tail and compress the build-order explanation.
- Final end-section sources: none.

## Part I: Action

- Thesis: The step from assistant to agent is not a model upgrade. It is the moment language becomes accountable state change.
- Target reader payoff: The reader gets a practical way to choose action surfaces and diagnose tool-use failures by seam instead of by vague model complaints.
- Central scenario: An enterprise procurement flow that sounded operational in demos, then failed on schema accuracy and partial acknowledgments once it was allowed to write.
- Must-keep source assets: `01-action-tool-use.md`, `03-action-tool-use-blueprint.md`, `use-cases/enterprise-agent.md`, `papers/toolformer.md`, `papers/gorilla.md`, `papers/swe_agent.md`, `papers/spider_2_0.md`.
- Cuts to make from the current draft: Reduce repeated definitions of agency, shorten the surface hierarchy setup, and compress the source tail.
- Final end-section sources: Toolformer, Gorilla, SWE-agent, Spider 2.0.

## Part II: Reasoning

- Thesis: Most reasoning failures in production are scaffold failures. Teams keep shopping for a smarter mind when the real problem is the wrong structure.
- Target reader payoff: The reader gets a failure-to-scaffold diagnosis framework with a conservative escalation path.
- Central scenario: A document-review agent that keeps skipping one dependency and looks competent until a real reviewer checks the output.
- Must-keep source assets: `02-reasoning-planning.md`, `02-reasoning-planning-blueprint.md`, `failure-mode catalog`, `papers/react.md`, `papers/chain_of_verification.md`, `papers/tree_of_thoughts.md`, `papers/lats.md`.
- Cuts to make from the current draft: Reduce the feel of method cataloging, keep one clear table, and trim repeated warnings about search.
- Final end-section sources: ReAct, Least-to-Most, Chain-of-Verification, Tree of Thoughts, LATS.

## Part III: Memory

- Thesis: Memory is not storage. It is governance over what the agent is allowed to keep, retrieve, reuse, and forget across time.
- Target reader payoff: The reader gets a durable memory architecture instead of another argument for larger context windows or larger vector stores.
- Central scenario: A policy assistant that begins returning outdated but plausible answers because old and new policy states were allowed to compete in the same unmanaged store.
- Must-keep source assets: `03-memory.md`, `01-memory-blueprint.md`, `use-cases/enterprise-agent.md`, `use-cases/coding-agent.md`, `papers/memgpt.md`, `papers/mem0.md`, `papers/memorybank.md`, `papers/voyager.md`.
- Cuts to make from the current draft: Trim repeated statements about policy, add one coding-oriented example, and compress the source tail.
- Final end-section sources: MemGPT, Generative Agents, MemoryBank, Mem0, Voyager.

## Part IV: Multi-Agent

- Thesis: Multi-agent systems solve three different problems, and confusing those problems is why so many agent teams become expensive theater.
- Target reader payoff: The reader can distinguish role separation, critique, and artifact-driven decomposition, then choose the right topology only when a second agent buys a real boundary.
- Central scenario: A research or reporting pipeline that got worse after being split into named roles with soft conversational handoffs.
- Must-keep source assets: `04-multi-agent.md`, `05-multi-agent-design-blueprint.md`, `use-cases/enterprise-agent.md`, `papers/metagpt.md`, `papers/chatdev.md`, `papers/autogen.md`, `papers/mad.md`, `papers/reconcile.md`.
- Cuts to make from the current draft: Expand the three-problem frame, reduce generic anti-hype wording, and keep the conclusion sharper.
- Final end-section sources: MetaGPT, ChatDev, AutoGen, RECONCILE.

## Part V: Safety

- Thesis: Agent safety is not primarily about careful prompts. It is about whether the system treats content, memory, tools, handoffs, and approvals as separate trust boundaries.
- Target reader payoff: The reader leaves with a concrete attack-chain model and a clear control map tied to real capability surfaces.
- Central scenario: A support or operations agent reads hostile content, retrieves poisoned material, writes the wrong artifact, and passes contamination into the next tool or agent.
- Must-keep source assets: `05-safety.md`, `06-safety-blueprint.md`, `failure-mode catalog`, `papers/greshake_indirect_prompt_injection.md`, `papers/poisonedrag.md`, `papers/agentsmith.md`, `papers/toolemu.md`, `papers/injecagent.md`.
- Cuts to make from the current draft: Replace generic middle sections with a more vivid attack chain, compress repeated statements that prompt safety is insufficient, and shorten the source tail.
- Final end-section sources: Greshake et al., InjecAgent, PoisonedRAG, Agent Smith, ToolEmu.

## Part VI: Optimization

- Thesis: If you cannot name which layer is failing and measure it against a stable objective, you are not optimizing an agent. You are editing it.
- Target reader payoff: The reader gets an operational improvement order and a way to turn correction logs, retries, and approval data into a measured workflow program.
- Central scenario: A production document-classification system that spends weeks in prompt churn while the real problem lives in evaluation design, schema quality, and weak metadata.
- Must-keep source assets: `06-optimization.md`, `04-optimization-self-improvement-blueprint.md`, `architecture review checklist`, `use-cases/enterprise-agent.md`, `use-cases/coding-agent.md`, `use-cases/web-agent.md`, `papers/opro.md`, `papers/textgrad.md`, `papers/reflexion.md`, `papers/mt_bench_chatbot_arena.md`.
- Cuts to make from the current draft: Rebuild the opening and middle, reduce procedural tone, and make the evaluation layer the controlling argument rather than one section among many.
- Final end-section sources: OPRO, TextGrad, Reflexion, AFLOW, MT-Bench and Chatbot Arena.
