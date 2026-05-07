# Candidate Essay Slate: agent harnesses

## Scope And Input Discipline

- Workflow step: `topic_discovery.rank_candidate_essay_objects`
- Runtime publication ambition: `north_star_flagship`
- Declared ranked paper pool used: `reviewable-runs/logs/agent-harnesses-topic-discovery-rank-candidate-essay-objects-candidate-paper-pool.md`
- Declared/observed ranked paper pool sha256: `fe4821951ec32a7a3495e6a4a38585876d08fe49d49a70c1a14afff27dac21d9`
- Missing consumed input: `assistant_discussion_notes`
- Constraint: no assistant notes were fabricated or inferred.

## Ranking Lens

For a north-star flagship essay, prioritize essay objects that can carry a broad claim: agent progress is increasingly determined by non-model infrastructure that can be externalized, inspected, evaluated, governed, and optimized. The ranked paper pool already identifies this as the strongest supported claim and warns against collapsing control harnesses, evaluation harnesses, fuzz harnesses, and context-management harnesses into one undifferentiated term.

## Ranked Candidate Essay Objects

### 1. Harness As The New Research Object

- Core thesis: the agent harness is becoming the editable scientific object around which agent capability, safety, reproducibility, and transfer are organized.
- Primary evidence base: `Natural-Language Agent Harnesses`, `Architectural Design Decisions in AI Agent Harnesses`, and `Agentic Harness Engineering`.
- Evidence delta: this object can connect harness externalization, architecture taxonomies, and optimization results into one flagship thesis rather than a survey of isolated agent scaffolds.
- Use lines: ranked pool lines 52-65 and 160-164.
- Why rank first: it is the only candidate with a clean anchor-artifact-optimization arc and a sufficiently general claim for a north-star piece.
- Kill criteria: kill or demote if the draft cannot define "harness" in a way that stays distinct from prompt, scaffold, benchmark, and app wrapper by the end of the opening section.

### 2. The Control Plane Around The Model

- Core thesis: the decisive engineering surface for agents is shifting from model invocation to the surrounding control plane: context, tools, execution, safety, orchestration, and audit.
- Primary evidence base: `Architectural Design Decisions in AI Agent Harnesses`, `Building Effective AI Coding Agents for the Terminal`, `ClawVM`, `SafeHarness`, and `SafeAgent`.
- Evidence delta: this object gives readers a concrete map of the system surfaces hidden behind the word "agent".
- Use lines: ranked pool lines 57-70, 104-114, and 140-142.
- Why rank second: it has strong architecture and product grounding, but it risks becoming a taxonomy piece unless tied tightly to an argument about control and governance.
- Kill criteria: kill if the essay becomes a feature inventory rather than an argument about where agency is actually mediated.

### 3. Harnesses That Improve Harnesses

- Core thesis: harnesses are no longer static wrappers; observability and evaluation loops make them optimization targets in their own right.
- Primary evidence base: `Agentic Harness Engineering`, `Synthesizing Multi-Agent Harnesses for Vulnerability Discovery`, `VeRO`, and `Meta-Harness`.
- Evidence delta: this object lets the essay argue that agent progress will come from the recursive system around agents, not just larger models or better prompts.
- Use lines: ranked pool lines 62-65, 72-75, 87-100, and 158-164.
- Why rank third: it is high-upside and distinctive, but narrower than the flagship object unless framed as a chapter inside the broader harness-as-research-object thesis.
- Kill criteria: kill if the evidence reads as benchmark-specific uplift without a generalizable mechanism.

### 4. Harness As Safety And Governance Boundary

- Core thesis: the harness is where permission, state, tool use, rollback, filtering, privilege separation, and audit become enforceable system properties.
- Primary evidence base: `SafeHarness`, `SafeAgent`, `ClawVM`, `Architectural Design Decisions in AI Agent Harnesses`, and the safety controls in `Building Effective AI Coding Agents for the Terminal`.
- Evidence delta: this object can make the governance stakes concrete without relying on abstract AI safety language.
- Use lines: ranked pool lines 57-70, 104-114, 140-142, and 166-170.
- Why rank fourth: it is a strong section-level object, but as the main essay it may over-narrow the publication into security architecture.
- Kill criteria: kill as main object if the draft cannot tie safety mechanisms back to capability, reproducibility, and evaluation rather than treating them as compliance add-ons.

### 5. Fuzz Harnesses And Security Agents As The Mature Edge Case

- Core thesis: security and fuzzing show the mature version of harness thinking because tasks already require tools, feedback, coverage, retries, repair, and reproducible environments.
- Primary evidence base: `Synthesizing Multi-Agent Harnesses for Vulnerability Discovery`, `Coverage-Guided Multi-Agent Harness Generation for Java Library Fuzzing`, `AutoHarness`, `HarnessAgent`, and `Clover`.
- Evidence delta: this object supplies concrete mechanisms and prevents the essay from staying at the level of product abstractions.
- Use lines: ranked pool lines 72-85, 128-138, and 151-155.
- Why rank fifth: it is evidence-rich but too domain-specific to serve as the north-star flagship unless the publication deliberately pivots toward security research.
- Kill criteria: kill as main object if fuzz harness meaning starts to crowd out agent-control harness meaning.

### 6. Evaluation Harnesses Are Not Control Harnesses

- Core thesis: the field needs a sharper distinction between harnesses that run agents and harnesses that measure agents, because both shape outcomes but in different ways.
- Primary evidence base: `VeRO`, `Holistic Agent Leaderboard`, `Terminal-Bench`, `ProdCodeBench`, and `Towards More Standardized AI Evaluation`.
- Evidence delta: this object can discipline terminology and make measurement infrastructure legible.
- Use lines: ranked pool lines 87-95, 116-126, 158-164, and 166-170.
- Why rank sixth: it is useful boundary work, but as a flagship essay it is more corrective than generative.
- Kill criteria: kill if the piece becomes mostly about benchmark design rather than agent-system construction.

## Recommended Slate Decision

Proceed with candidate 1, `Harness As The New Research Object`, and use candidates 2, 3, 4, and 6 as internal sections or pressure tests. Keep candidate 5 as a concrete evidence sidebar or comparative domain section, not the main object.

## Exclusions For This Step

- Exclude general agent orchestration, MCP, governance, and security papers that do not make the harness itself the explicit control surface.
- Exclude search near-misses already marked weaker than core anchors in the ranked paper pool.
- Exclude assistant-discussion-derived claims because the request declared that input missing.

## Downstream Kill Criteria For The Whole Essay

- The opening cannot define the harness as distinct from prompt, scaffold, benchmark, and app wrapper.
- The evidence cannot support a claim broader than coding-agent tooling.
- Evaluation and control harnesses collapse into the same concept.
- The paper set produces a taxonomy without a falsifiable argument about why harnesses matter.
- Safety appears only as risk mitigation rather than as part of the harness's operating boundary.
