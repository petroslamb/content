# Part 4: One Agent Is Not Enough

## When to Split, How to Coordinate, and What Can Go Wrong

*Part 4 of 6: A Practical Guide to Foundation Agents*

---

A product team building an internal research assistant decided, midway through development, that the system needed multiple agents. The reasoning was intuitive: the agent was doing several different things , searching the web, summarizing papers, synthesizing across sources, drafting reports , and surely those should be separate agents, each specialized for its role.

They built five. A search agent, a summarizer, a synthesizer, a critic, and a report writer. They connected them through an orchestration layer with a shared conversation history. The system took four times as long per task. Errors in the summarizer's output were amplified by the synthesizer and then amplified again by the report writer. When the output was wrong, no one could tell which agent had introduced the error. And the overall output quality was measurably lower than the single-agent baseline they built the week before, because the shared conversation history became too long for any single agent to reason from coherently, and the handing-off of context between agents degraded the information at every step.

They had added agents to solve a scaling problem that did not exist and created a coordination problem that did not need to exist. The original system had one bottleneck: the summarizer was slow on long documents. The fix was caching and better chunking. Instead, they built a distributed system with five points of failure and chose coordination overhead as the price.

Multi-agent systems are not a capability upgrade. They are a decomposition strategy. The question is not "how many agents should I have?" It is "what specific problem does adding another agent solve , and is that problem actually present in my system?"

---

## Three Different Problems, Three Different Architectures

The most useful practical insight in Chapter 14 of the *Foundation Agents* survey is one that most multi-agent frameworks obscure: there are three completely different reasons to use multiple agents, and each reason implies a completely different system architecture, communication style, failure mode, and evaluation approach.

Confusing these three reasons , building a system that blends them without distinguishing them , is the source of most multi-agent failures in practice.

**Reason 1: Role separation.** Different parts of the workflow require genuinely different tools, permissions, or output formats, to the point where giving one agent all of them would be unsafe, operationally impractical, or just obviously worse. A system that runs security scans cannot safely be the same agent that deploys code , the permissions differ in ways that matter. A system that interacts with financial records needs different access rights than the system that drafts executive summaries. Role separation through multiple agents is the correct response to a real constraint: one agent cannot hold all the tools or all the trust levels without creating an unacceptable blast radius.

**Reason 2: Reliability through critique.** Independent review, disagreement, and debate can improve output quality when the task is difficult enough that a single reasoning pass is consistently unreliable. *Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate* (Liang et al., 2023) formalizes this idea: having multiple agents argue competing answers and reconcile their positions produces better outcomes on tasks where the first answer is frequently flawed. *RECONCILE: Round-Table Conference Improves Reasoning via Consensus among Diverse LLMs* (Chen et al., 2023) extends this into confidence-weighted consensus.

The key word in the previous sentence is "when." Debate improves reliability on tasks where disagreement between reasoning agents is informative , where different approaches to the task produce meaningfully different answers, and where reconciling those differences selects the better one. On easy tasks, debate is coordination overhead for a problem that does not exist. On tasks where the failure mode is not reasoning quality but grounding or information access, debate between agents that share the same knowledge limitations produces confident noise from multiple sources, which is worse than confident noise from one.

**Reason 3: Task decomposition through artifact handoffs.** Some workflows naturally divide into sequential stages where each stage produces a typed artifact that the next stage consumes. A software engineering pipeline where a planner produces a specification, a coder implements against the specification, and a reviewer checks the implementation against the specification is not using multiple agents for sophistication , it is using them because the task has three genuinely distinct phases with clear boundaries and typed outputs between them.

*MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework* (Hong et al., 2023) is the clearest implementation of this pattern in the literature. MetaGPT's important contribution is not that it uses multiple agents , it is that agents exchange artifacts (written documents, specifications, code outputs) rather than unstructured conversation. That exchange is what makes the pipeline coherent: each agent receives a typed input, produces a typed output, and the handoff between agents is a contract, not a chat message.

These three reasons lead to completely different systems. A role-separation architecture is about permissions and tool boundaries. A reliability architecture is about sampling and consensus. A pipeline architecture is about artifacts and handoffs. Building all three into one system without distinguishing which problem you are solving produces a system that is incoherent along all three dimensions.

---

## The Default Is One Agent

Given this analysis, the correct default starting point for any agent system is one agent with a well-designed control loop, a clear tool set, and explicit approval boundaries for high-impact actions.

This is not a conservative stance born of caution about AI systems. It is the most common finding in both the research literature and practical field experience: multi-agent complexity introduces coordination overhead, failure localization difficulty, and integration cost. These costs are worth paying when the problems they solve are real. They are not worth paying when they are added speculatively.

The professional instinct to reach for multi-agent architectures is understandable. They feel more sophisticated. They seem to indicate that the system has been thought through more carefully. The frameworks (AutoGen, LangGraph, CrewAI) make it easy to spin up agent roles and connect them. But architectural decisions that feel sophisticated and are easy to implement deserve scrutiny for exactly that reason , the ease of construction disguises the cost of operation.

*AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation* (Wu et al., 2023) is worth citing here precisely because it demonstrates the risk as well as the capability. AutoGen made multi-agent conversation programmable and flexible. That flexibility is real, and it has enabled real systems. But it also made it easy to build webs of agents where the coordination logic is opaque, the shared conversation history becomes unmanageable, and failure modes compound across agents without clear attribution. The flexibility creates the capability and the footgun at the same time.

The practical workflow before adding any agent beyond the first is: articulate what problem the second agent specifically solves. If the answer is "it handles X while the first agent handles Y," ask whether X and Y require different tools or different trust levels. If not, the split is probably cosmetic. If the answer is "it reviews the first agent's output," ask whether the review signal is meaningful enough to justify the cost. If review is catching errors that a lightweight self-check would catch, the review agent is overhead. The bar for adding a second agent should be higher than the bar for extending the first one.

---

## When Multi-Agent Is the Right Answer

With the conservative default established, the patterns where multi-agent architecture is genuinely justified are worth specifying precisely.

**Orchestrator plus specialists** is the most widely useful multi-agent pattern and the one most closely aligned with the role-separation rationale. A coordinator agent manages the task, breaks it into subtasks, and delegates each subtask to a specialist that has the appropriate tools and permissions for that subtask. The key constraint is that specialists should be genuinely specialized: different tools, different permission scope, and different output formats. If the specialist does what the orchestrator could have done directly, the delegation is overhead without benefit.

*ChatDev: Communicative Agents for Software Development* (Qian et al., 2023) is a good reference for this pattern with an additional property that matters: agents in ChatDev exchange structured role-based outputs, not open-ended conversation. A CEO agent produces a product specification; an architect agent produces a system design from that specification; a developer agent produces code from that design. Each handoff is typed. The structure makes the pipeline auditable , you can look at what the architect received, what it produced, and evaluate whether the transformation was correct.

**Role-based pipeline** is the correct architecture for workflows that naturally decompose into distinct sequential phases with clear deliverable boundaries between them. Software development has this property. Document review has this property. Research-and-synthesis workflows have this property when the phases (search, extract, synthesize, draft) have different enough requirements that optimizing each separately produces better results than optimizing one general-purpose agent.

**Critic or reviewer overlay** is appropriate for high-value outputs where a second independent judgment reduces the error rate meaningfully. The key is "meaningfully" , if the critic catches errors that a structured self-check would catch, use the self-check. A critic overlay is worth its cost when it catches errors that would not be caught by the primary agent's own verification step, because the error pattern requires a different perspective rather than a better prompt.

**Debate or consensus** is the most expensive and most narrowly applicable pattern. It should be reserved for tasks where the answer genuinely benefits from multiple independent reasoning paths , where the nature of the task means a single reasoning chain is systematically unreliable in ways that sampled reasoning is not. Hard normative judgments, complex ethical trade-offs, and difficult planning problems with many hidden interactions are the domains where debate is productive. Most practical agent tasks do not meet this bar.

---

## The Artifact Handoff Principle

Across all multi-agent patterns, the single most important design decision is how agents exchange work.

Free-form conversation between agents , where an agent sends a message and the next agent reads it and responds , looks natural and is easy to implement. It is also the most fragile coordination mechanism available. The receiving agent must parse the meaning of the message, infer the intent behind it, and construct a response that makes sense not just to the sending agent but to the task as a whole. Errors in one agent's output become ambiguous inputs to the next agent. Ambiguous inputs produce ambiguous outputs. Ambiguous outputs compound.

Typed artifact handoffs are the alternative. Instead of sending a conversational message, the completing agent produces a structured output: a document with defined sections, a JSON object with named fields, a code artifact with a defined interface, a specification against which the next agent evaluates. The receiving agent does not need to interpret intent , it receives a contract. Errors are visible as contract violations, not as subtle degradation in reasoning quality.

MetaGPT's contribution is ultimately this principle, not the specific set of roles it uses. The roles are an example. The artifact exchange is the architecture. Any multi-agent system that uses role-based coordination should enforce typed handoffs at every boundary between agents. If agents are exchanging free-form text, the coordination is relying on interpretation rather than structure, and interpretation errors will compound.

---

## The Human in the System

Chapter 14's subsection on human-agent collaboration is often treated as secondary to the more dramatic multi-agent coordination patterns. It should not be.

The most important "multi-agent" design decision for most enterprise systems is not whether to use an orchestrator with specialists, or whether to add a critic. It is where human judgment sits in the workflow. Human review, human approval, and human escalation are coordination mechanisms as real as any agent-to-agent handoff , and they are better suited to certain classes of decision than any agent combination.

For irreversible actions, financially significant operations, legally sensitive outputs, and compliance-critical decisions, human approval is not a limitation of the current state of the technology. It is the correct architecture for the accountability requirements of the task. The goal of the human-agent collaboration design is to place human review at the points in the workflow where human judgment is genuinely necessary and to minimize the human overhead everywhere else , not to eliminate human judgment from the system as a mark of sophistication.

A two-agent system with a well-placed human approval gate is often more reliable, more auditable, and more clearly improvable than a seven-agent system without one.

---

## What Goes Wrong

**Agent theater** is the most common multi-agent failure mode and the hardest to detect because it looks like architectural sophistication. The system has multiple agents with distinct names and descriptions. The agents do not do substantially different things. Adding or removing one of them would not noticeably change the output. The pattern usually emerges when multi-agent architecture is chosen before the single-agent baseline has been understood well enough to know which roles are genuinely distinct.

**Unstructured handoff drift** is what happens when agents exchange free-form messages without typed contracts. The first few task runs produce coherent outputs because the errors happen to be small. Over time, edge cases produce messages that carry ambiguous state, and the receiving agent reasons from that ambiguity. By task twenty, the system is producing outputs that cannot be diagnosed without reconstructing the full conversation history of every agent.

**Giving all agents the same permissions** defeats the main practical benefit of role separation, which is that different agents acting on different trust levels limits blast radius. An orchestrator and a specialist with identical tool access and identical permissions are not a multi-agent system in any practically meaningful sense , they are one system spread across two context windows.

**Using debate where simple verification would be cheaper** produces systems with high coordination cost and marginal quality improvement. The question to ask before adding a debate or consensus layer is: what specific failure mode does this address that a self-check or human review step would not?

---

## The Governing Principle

The chapter's most important practical principle, stated plainly: multi-agent architecture is workflow decomposition, not magic emergence. The capability of a multi-agent system is determined by whether the decomposition matches a real structure in the task, whether the handoffs are typed and auditable, and whether the coordination overhead is justified by the gains in quality, specialization, or reliability.

A multi-agent system that fails because two agents are doing redundant work is not a multi-agent design problem. It is a task analysis problem that produced a fictional decomposition. The fix is not a better framework. It is understanding the task well enough to know where the real boundaries are.

The research team that built five agents to replace a single-agent pipeline had not analyzed why the single-agent system was failing. If they had, they would have found a caching and chunking problem , not a coordination problem. The multi-agent system they built was the wrong solution to the wrong diagnosis, and its complexity made that diagnosis harder to find.

Build the single-agent system until you understand it well enough to know which of its failures are genuinely role-separable. Then, and only then, add the second agent.

---

*Part 5 addresses safety: why agent safety is an interface architecture problem rather than an alignment problem, what the actual attack surfaces of a deployed agent system are, and why every capability chapter in this guide has a corresponding safety chapter.*

---

**Source basis for this essay:** Chapter 14 of *Advances and Challenges in Foundation Agents* (2025); *MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework* (Hong et al., 2023) [arXiv:2308.00352](https://arxiv.org/abs/2308.00352); *ChatDev: Communicative Agents for Software Development* (Qian et al., 2023) [arXiv:2307.07924](https://arxiv.org/abs/2307.07924); *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation* (Wu et al., 2023) [arXiv:2308.08155](https://arxiv.org/abs/2308.08155); *Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate* (Liang et al., 2023) [arXiv:2305.19118](https://arxiv.org/abs/2305.19118); *RECONCILE: Round-Table Conference Improves Reasoning via Consensus among Diverse LLMs* (Chen et al., 2023) [arXiv:2309.13007](https://arxiv.org/abs/2309.13007); `practical-chapter-blueprints/05-multi-agent-design-blueprint.md`.
