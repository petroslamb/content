# Rewrite Ledger: V5 Essays to V6 Doctrine Series

Internal drafting support for the `Operating Agents` `v6` rewrite.

This pass should not optimize for generic platform polish first. It should optimize for the real purpose of the package: turning agent literature into an operating doctrine for builders.

## Working Goal

This bundle exists to turn agent literature into an operating doctrine for builders.

The `v6` question is not "can these posts read like better magazine essays?" The question is "can a serious builder use this series to make better architecture decisions, diagnose failures faster, and name the right boundary in a review?"

## What A+++ Means For This Bundle

For `Operating Agents`, `A+++` means doctrine-level public writing:

- each core essay delivers one hard law, not just a competent summary
- each essay names the common builder mistake it is trying to eliminate
- each essay gives one decision rule and one escalation rule
- each essay anchors its law in one vivid failure archetype
- each essay turns a slice of literature into reusable operating language
- the bundle reads as one coherent doctrine, but each chapter can still win its own argument

The memorability test is practical. A builder should be able to quote one sentence from each chapter in a design review next week.

## Why V5 Stalled

The `v5` package improved the framing and cleaned up several obvious problems, but it still stalled below the desired bar because the essays were trying to do too many jobs at once.

- blueprint loyalty: the public essays kept preserving too much of the blueprint's completeness
- literature pressure: the body sometimes still behaved like compressed survey synthesis instead of metabolized doctrine
- bundle plumbing: launch framing, companion references, and map logic sometimes stayed too visible inside the public pieces
- mixed form: some essays were still part essay, part field guide, part classification note

`v6` should solve that by making each essay do one dominant public job while letting companions and blueprints carry the surrounding terrain.

## Non-Negotiable V6 Rules

- `v6` files are new files. Keep `v5` as the archived live baseline until the rewrite is complete.
- Each chapter must open with a failure, pressure, or contested claim, not package plumbing.
- Each chapter must have one dominant law that governs what stays in the body and what gets cut.
- Each chapter must include:
  - one law
  - one enemy mistake
  - one decision rule
  - one escalation rule
  - one failure archetype
- Use only the papers that carry real argumentative weight in the body. Move broader taxonomy to the companion.
- Keep at most one compact table or structured artifact per essay, and only when it speeds an actual decision.
- Endmatter should point to the next useful layer, not replay a mini literature review.
- Distinctive cadence matters. The bundle should not reuse the same sentence machinery, opening shape, or concluding shape by default.

## Series Doctrine

The six core doctrine laws should read cleanly as a stack:

- Launch: reliable agents come from explicit operating layers, not capability stacking
- Action: language becomes agency only when it becomes accountable state change
- Memory: memory is governance over time, not storage
- Reasoning: most production reasoning failures are control failures before they are intelligence failures
- Multi-agent: extra agents multiply ambiguity unless they create a real boundary
- Safety: agent safety is trust-boundary design, not refusal theater
- Optimization: the workflow is the object

If a draft wanders from its law, cut the wandering material or move it to the companion.

## Bundle-Level Build Plan

### Phase 1: Lock The Doctrine Skeletons

Before drafting prose, write a one-page skeleton for each `v6` essay with exactly these fields:

- doctrine law
- enemy mistake
- failure archetype
- decision rule
- escalation rule
- body sections
- anchor papers for the body
- material pushed to companion

Do not start by line-editing `v5`.

### Phase 2: Rewrite The Weakest Core Pieces First

Rewrite in this order:

1. launch note
2. reasoning
3. multi-agent
4. memory
5. action
6. safety
7. optimization

That order attacks the chapters most likely to collapse back into blueprint mode first, then re-tunes the stronger essays against the same doctrine standard.

### Phase 3: Run The Bundle Differentiation Pass

After first drafts exist, read the full set in sequence and cut anything that feels interchangeable:

- repeated sentence machinery
- repeated table logic
- repeated "why this matters" framing
- repeated companion or blueprint explanation
- repeated enterprise-anecdote cadence

The bundle should feel unified, not templated.

### Phase 4: Apply The Publication Layer

Only after the doctrine pass is complete:

- tighten tables and artifacts
- compress endmatter
- tune openings and endings for public readability
- update companions, coverage map, and folder READMEs only where the new doctrine requires it

## Essay Plans

### 00 Launch Note

- Target file: `essays/launch-note/00-launch-note-v6.md`
- Dominant job: preface the doctrine without sounding internal
- Doctrine law: reliable agents come from explicit operating layers, not capability stacking
- Enemy mistake: starting the agent conversation with model taste instead of system boundaries
- Failure archetype: a team keeps swapping models and prompt wording while the real failure lives in vague action and approval design
- Decision rule: if a workflow still relies on human compensation to look reliable, the architecture is not finished
- Escalation rule: move from model discussion to layer diagnosis the moment the system touches tools, approvals, or stored state
- Body shape:
  - opening failure
  - why most agent writing starts in the wrong place
  - what this doctrine stack is trying to make visible
  - one short explanation of publication order versus architecture order
  - the standard
- Cuts:
  - do not let repo plumbing dominate the body
  - do not let the launch note behave like a miniature seventh essay
  - keep resources minimal

### 01 Action

- Target file: `essays/action/01-action-tool-use-v6.md`
- Dominant job: define the assistant-agent boundary in operational terms
- Doctrine law: language becomes agency only when it becomes accountable state change
- Enemy mistake: treating tool use as a capability flourish instead of an interface design problem
- Failure archetype: a procurement workflow treats queued state as completed work and silently loses a real order
- Decision rule: choose the narrowest action surface that still reaches the work
- Escalation rule: escalate from API to code, SQL, browser, or GUI only when the cleaner surface cannot reach the task
- Body anchor papers: Toolformer, Gorilla, SWE-agent
- Material pushed to companion: wider action taxonomy, physical action, action learning, multimodal frontier
- Artifact allowance: one compact chooser table or one compact contract example

### 03 Memory

- Target file: `essays/memory/03-memory-v6.md`
- Dominant job: turn memory from a storage topic into a governance topic
- Doctrine law: memory is governance over time, not storage
- Enemy mistake: trying to solve stale or contaminated state with retrieval tuning alone
- Failure archetype: a policy assistant keeps surfacing retired or outdated rules because the store has no retirement or authority policy
- Decision rule: separate working, semantic, episodic, and procedural memory because they fail differently and need different controls
- Escalation rule: move to richer retrieval structures only after write policy, provenance, freshness, and forgetting discipline are already explicit
- Body anchor papers: MemGPT, MemoryBank, one of Reflexion or Mem0
- Material pushed to companion: wider cognitive analogy, richer retrieval taxonomy, deeper graph-memory frontier
- Artifact allowance: one compact layer map or one typed memory object

### 02 Reasoning

- Target file: `essays/reasoning/02-reasoning-planning-v6.md`
- Dominant job: teach scaffold diagnosis, not method coverage
- Doctrine law: most production reasoning failures are control failures before they are intelligence failures
- Enemy mistake: shopping for a stronger model when the task is badly staged
- Failure archetype: a claims workflow compresses dependent checks into one polished answer and fails under review
- Decision rule: diagnose the failure shape first, then install the lightest scaffold that corrects it
- Escalation rule: decomposition -> ReAct -> verification -> planner handoff -> search
- Body anchor papers: Least-to-Most, ReAct, Chain-of-Verification, plus one planner-handoff paper if needed
- Material pushed to companion: self-refinement breadth, wider search taxonomy, abstraction-reset methods, long method catalog
- Structural requirement: this essay must have one unmistakable spine and no survey feel
- Artifact allowance: no chooser matrix unless a late draft proves prose cannot carry the decision logic

### 04 Multi-Agent

- Target file: `essays/multi-agent/04-multi-agent-v6.md`
- Dominant job: make role splitting feel like a serious boundary choice instead of architecture theater
- Doctrine law: extra agents multiply ambiguity unless they create a real boundary
- Enemy mistake: adding roles to compensate for weak decomposition, weak artifacts, or weak approval design
- Failure archetype: a reporting or operations pipeline becomes slower and harder to localize after conversational role splits blur responsibility
- Decision rule: add a second role only when it buys one of three things: permission boundary, independent critique, or typed artifact handoff
- Escalation rule: keep the default single-agent until one of those three boundaries is clearly missing
- Body anchor papers: AutoGen as warning, MetaGPT or ChatDev for artifact handoffs, one critique paper
- Material pushed to companion: topology catalog, protocol layers, collective-intelligence framing, evaluation breadth
- Structural requirement: open with a concrete failure or sharp architecture dispute, not neutral classification
- Artifact allowance: no matrix; if structure is needed, use three short architecture sections

### 05 Safety

- Target file: `essays/safety/05-safety-v6.md`
- Dominant job: redefine safety as boundary design for agent workflows
- Doctrine law: agent safety is trust-boundary design, not refusal theater
- Enemy mistake: treating prompt carefulness as the primary safety mechanism
- Failure archetype: untrusted retrieved content turns into an internal artifact and then into a real side effect
- Decision rule: model every channel by what trust it carries and what it can reach
- Escalation rule: widen autonomy only after trust separation, tool scope, handoff skepticism, and approval are already explicit
- Body anchor papers: Greshake et al., PoisonedRAG, ToolEmu
- Material pushed to companion: broader hallucination framing, perception-specific threats, wider safety-scaling discussion
- Artifact allowance: one compact trust map or one channel policy object

### 06 Optimization

- Target file: `essays/optimization/06-optimization-v6.md`
- Dominant job: force teams to optimize the workflow instead of the most visible wording
- Doctrine law: the workflow is the object
- Enemy mistake: prompt churn without a stable objective or failure taxonomy
- Failure archetype: a useful workflow spends weeks in prompt editing while the real problems live in evaluation design, contracts, and routing
- Decision rule: lock the evaluation set and repair contracts before you tune wording
- Escalation rule: evaluation -> contracts and evidence -> prompts -> bounded feedback loops -> workflow search
- Body anchor papers: OPRO, MT-Bench and Chatbot Arena, one bounded self-improvement paper
- Material pushed to companion: wider search and self-improvement taxonomy
- Artifact allowance: one numbered intervention ladder, no broad comparison table

## Acceptance Gates

### Chapter-Level Gate

Every `v6` essay must pass all of these checks:

- the doctrine law appears in the first fifth of the piece
- the body keeps returning to one enemy mistake
- the failure archetype is concrete enough to remember later
- at least one sentence can be lifted into a design review without extra explanation
- papers are treated as argumentative support, not as a parade of mentions
- the companion clearly owns the material that would otherwise turn the essay back into taxonomy

### Bundle-Level Gate

The full set should pass these checks:

- the six core essays read like a stack of doctrine, not a stack of summaries
- each chapter gives a distinct design law and a distinct enemy mistake
- a builder can explain the whole bundle from memory using six laws
- the launch note behaves like a preface, not a scored pillar
- no chapter depends on tables or endmatter to carry its main argument
- the series voice is varied enough that no chapter feels templated from another

## Review Questions

Use these questions before calling `v6` done:

- What architecture argument does this chapter help a builder win?
- What bad default does this chapter make harder to defend?
- What sentence from this chapter is worth quoting?
- What material is still in the essay only because the blueprint once held it?
- What did we cut to protect the doctrine?
