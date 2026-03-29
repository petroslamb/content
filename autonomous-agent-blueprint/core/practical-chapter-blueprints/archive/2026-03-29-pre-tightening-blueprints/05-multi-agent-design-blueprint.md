# Chapter 14 Blueprint: Multi-Agent Design

## Why This Chapter Matters

The multi-agent chapter matters because it asks a question many teams answer too casually: when should one agent become several? The practical answer is not "whenever we want more intelligence." It is "when role separation, structured handoff, or independent review clearly improve the workflow."

This chapter is useful because it separates serious workflow decomposition from agent theater.

## Survey Subsections To Prioritize

- `14.1.2 Heterogeneous Agents`
- `14.2.1 Static Topologies`
- `14.3.4 Task-oriented Interaction`
- `14.4 Human-Agent Collaboration`
- `14.5 Decision-Making in Multi-Agent Systems`
- `14.6.1 Types of Agent Messages`
- `14.6.3 Next-Generation Communication Protocols`

The task-oriented interaction and human collaboration sections are the most practical parts.

## The Practical Question

The chapter is answering four questions:

1. Is one agent enough?
2. If not, what roles should be split?
3. How should those roles exchange work?
4. Where does human supervision remain mandatory?

Those are workflow-design questions, not philosophical ones.

## Core Literature And What Each Paper Adds

### `MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework`

MetaGPT is one of the clearest role-based pipeline papers. It matters because agents exchange artifacts and documents rather than only conversation. That makes it architecturally valuable.

Use it when the system naturally decomposes into specialist roles with structured deliverables.

### `ChatDev: Communicative Agents for Software Development`

ChatDev is another strong role-based collaboration system. It matters because it uses staged software-team roles as the organizing frame.

Use it when you want a pipeline view of multi-agent collaboration rather than a pure dialogue view.

### `AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation`

AutoGen matters because it made multi-agent conversation programmable and reusable. Its practical value is flexibility, but that flexibility also makes it easier to overbuild.

Use it when conversation is needed as a coordination fabric, but constrain it with clear roles and stop conditions.

### `Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate`

MAD is best treated as a reliability paper more than a general architecture paper. It matters when multiple agents are being used to disagree productively.

Use it when the goal is better answer quality through adversarial comparison, not role decomposition.

### `RECONCILE: Round-Table Conference Improves Reasoning via Consensus among Diverse LLMs`

RECONCILE matters because it makes debate more structured and confidence-aware. It pushes multi-agent reliability toward a stronger decision process.

Use it when consensus and disagreement need to be managed explicitly.

### Protocol Layer Notes

The chapter guide mentions MCP and A2A as protocol-adjacent infrastructure. Those are important conceptually, but the local chapter literature here is stronger on workflow patterns than on mature inter-agent protocol design.

## If Your Problem Looks Like X, Choose Y

- If one agent can still own the task with bounded tools, keep one agent.
- If distinct roles have different tools or permissions, choose orchestrator plus specialists.
- If work naturally moves through staged artifacts, choose a role-based pipeline.
- If reliability needs independent review, add a critic overlay.
- If disagreement itself is informative, use debate or consensus methods sparingly.

## Method Comparison Matrix

| Pattern | Best use | Main strength | Main risk | Escalate when |
| --- | --- | --- | --- | --- |
| Single orchestrator | most bounded workflows | cheapest and clearest baseline | overloaded responsibilities | role separation becomes real |
| Orchestrator plus specialists | distinct tools or permissions | bounded delegation with clear control | fake specialists that do the same work | handoffs become artifact-heavy |
| Role-based pipeline | staged document or software work | strong artifact flow and reviewability | rigidity where tasks vary a lot | independent review is still weak |
| Critic or reviewer overlay | high-value outputs | targeted reliability improvement | extra cost with little gain on easy tasks | disagreement itself adds insight |
| Debate or consensus group | hard judgment tasks | surfaces disagreement and alternative views | expensive and easy to overuse | only when simple review no longer suffices |

## The Chapter's Main Architectural Insight

The strongest practical insight is that multi-agent systems solve three different problems:

- role separation
- reliability through critique
- task decomposition through artifact handoffs

These should not be confused. A planner-reviewer pair is not the same architecture as a role-based software pipeline, and neither is the same as a debate system.

## The Default Multi-Agent Blueprint

### Default Position

Start with one orchestrator if possible. Multi-agent design is an escalation path, not the baseline.

### Add Specialists Only When Role Separation Is Real

Specialists should exist when they have distinct tools, permissions, output formats, or evaluation logic. If two agents do the same kind of work with different names, the split is probably unnecessary.

### Prefer Artifact Handoffs Over Free-Form Chat

The most practical multi-agent systems exchange typed outputs, plans, documents, patches, or decisions. This keeps coordination legible and debuggable.

### Use Debate Sparingly

Debate or critique agents are useful when the task justifies independent review. They are expensive and should be applied where reliability is worth the cost.

### Keep Humans As Explicit Participants

Human review should appear as a first-class role in workflows where approval, interpretation, or policy judgment cannot be safely delegated.

## Design Patterns

### Orchestrator Plus Specialists

One coordinator delegates bounded work to specialist roles. This is the default multi-agent pattern for most practical systems.

### Role-Based Pipeline

A fixed staged flow with distinct deliverables at each stage. This is a strong fit for software, document, and research workflows.

### Critic Or Reviewer Overlay

A critic agent reviews outputs from a primary agent or pipeline stage. This is best for higher-stakes decisions or high-value artifacts.

### Debate Or Consensus Group

Multiple agents produce competing views that are then reconciled. This should be reserved for tasks where disagreement is genuinely informative.

## Failure Modes

- splitting into multiple agents before the single-agent baseline is understood
- using free-form conversation where typed artifacts would work better
- giving all agents the same permissions
- using debate where simple verification would be cheaper
- adding specialist roles without specialist evaluation criteria

## Evaluation

A practical multi-agent system should be judged by:

- end-task quality
- coordination overhead
- latency and cost per handoff
- failure localization, meaning how easy it is to find the broken role
- improvement over the best single-agent baseline

If a multi-agent topology does not beat a strong single-agent workflow, it is complexity without justification.

## Recommended Build Order

1. Build the single-agent baseline first.
2. Identify which failures are actually role-separable.
3. Split only the roles that need different tools, permissions, or deliverables.
4. Add typed handoff contracts.
5. Add review or debate roles only where reliability gains are measurable.

## Anti-Patterns

- Do not start with large agent teams.
- Do not let conversation substitute for interface design.
- Do not assume more agents means more intelligence.
- Do not build specialist roles without specialist metrics.

## Reading Sequence For This Chapter

1. `../../essays/multi-agent/04-multi-agent-v6.md`
2. `../../essays/multi-agent/companion.md`
3. `papers/metagpt.md`
4. `papers/chatdev.md`
5. `papers/autogen.md`
6. `papers/mad.md`
7. `papers/reconcile.md`

## Bottom Line

The practical chapter blueprint is conservative by design: one agent first, specialists second, structured handoffs over chatter, and debate only when reliability needs it. Multi-agent design is workflow decomposition, not magic emergence.
