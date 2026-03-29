# Chapter 14 Blueprint: Multi-Agent Design

## Use This Blueprint When

Use this blueprint when one workflow is no longer enough and the team is considering additional agents, specialist roles, or review layers. The key question is not whether more agents sound more advanced. It is whether new boundaries will create cleaner role separation, safer authority, or stronger review than the best single-agent baseline.

## The Decision

Every multi-agent design has to answer four questions:

1. Is one strong orchestrator still enough?
2. If not, what responsibility actually deserves separation?
3. What artifact should pass between roles?
4. Where does human review remain a first-class part of the topology?

If those questions are vague, the extra agents are probably decorative.

## Default Position

The default multi-agent stance should stay conservative.

- Start with one orchestrator and bounded tools.
- Split only where tools, permissions, deliverables, or evaluation logic genuinely differ.
- Prefer typed artifact handoffs over free-form conversation.
- Add review or debate roles only where reliability gains are measurable.
- Treat protocol richness as a late concern rather than an opening move.

Multi-agent design is an escalation path in workflow decomposition, not a synonym for intelligence.

## Default Build

### Step 1: Prove The Single-Agent Baseline

Before adding roles, make the best one-agent workflow legible. If the baseline is weak, the topology will only spread confusion across more nodes.

### Step 2: Split By Responsibility, Not By Naming

Add specialists only when they own distinct tools, permissions, output formats, or evaluation standards. Two agents doing the same work under different titles are not a real split.

### Step 3: Define The Handoff Artifact

The handoff should be a typed plan, patch, review package, proposal, extracted dataset, or other inspectable artifact. Handoffs built only from open-ended conversation are harder to review, debug, and govern.

### Step 4: Add Review Layers Sparingly

Critic or reviewer roles earn their place when the task is valuable enough that independent inspection improves reliability. Debate and consensus roles belong only where disagreement itself is informative.

### Step 5: Keep Humans Inside The Topology

Human review should remain explicit wherever approval, policy interpretation, or costly judgment is still required. In practical systems the human is often the highest-clearance node, not an embarrassing leftover from incomplete automation.

## Escalate When

- Distinct roles genuinely need different tools or permissions.
- Work naturally moves through staged artifacts rather than one continuous loop.
- Independent review would catch failures the main path routinely misses.
- Disagreement between competing views is itself useful evidence.
- The system is becoming independent enough that communication protocol and discovery standards start to matter.

## Alternatives And When They Win

| Pattern | Best use | Why it wins | Main risk |
| --- | --- | --- | --- |
| Single orchestrator | most bounded workflows | cheapest and easiest to debug | overload if too many incompatible responsibilities accumulate |
| Orchestrator plus specialists | distinct tools or permissions | bounded delegation under central control | fake specialists that do not own anything real |
| Role-based pipeline | staged artifact-heavy work | strong reviewability and clean handoffs | rigidity where work varies too much |
| Critic or reviewer overlay | high-value outputs | targeted reliability improvement | extra cost with little gain on easy work |
| Debate or consensus group | hard judgment tasks | surfaces disagreement and alternatives | expensive and easy to romanticize |

## What To Measure

- Improvement over the best single-agent baseline
- Coordination overhead
- Latency and cost per handoff
- Failure localization, meaning how quickly the broken role can be found
- Human supervision burden
- Artifact quality at each boundary

If the topology does not improve task quality, governance, or debugging clarity over the simpler baseline, it is not justified.

## Failure Review

- Adding agents before the one-agent baseline is understood
- Splitting by persona instead of by responsibility
- Using conversation where an artifact contract should exist
- Giving all roles the same permissions
- Using debate where simple verification or review would be cheaper
- Introducing protocol complexity before there are truly independent components

## Reading Sequence

1. `../../essays/multi-agent/04-multi-agent-boundaries-and-handoffs.md`
2. `../../essays/multi-agent/companion.md`
3. `../../reference/papers/metagpt.md`
4. `../../reference/papers/chatdev.md`
5. `../../reference/papers/autogen.md`
6. `../../reference/papers/mad.md`
7. `../../reference/papers/reconcile.md`

Return to survey sections `14.1.2`, `14.2.1`, `14.3.4`, `14.4`, `14.5`, `14.6.1`, and `14.6.3` when the immediate design question expands into topology, decision, or protocol choices.

## Bottom Line

Treat every extra agent as a purchase that must keep proving its value. Start with one orchestrator, split only where authority or deliverables really differ, and make handoffs cold enough that both machines and humans can inspect them without reading a novel.
