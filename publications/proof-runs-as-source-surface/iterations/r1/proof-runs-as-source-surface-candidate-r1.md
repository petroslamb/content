# Proof Runs Are the Source Surface

A raw transcript can be useful memory. It can show what an agent saw, what it tried, and where the conversation bent under pressure. But a transcript is not a proof surface. It does not, by itself, say which workflow had authority, which context was admitted, which tools were allowed, which checks passed, which gate stopped movement, or which approval later resumed the run.

That distinction matters once an agent is no longer only drafting prose in a scratchpad. The moment it can initialize a package, mutate source files, move lifecycle state, resume from a gate, or prepare a public publication path, the question changes. We are no longer asking whether the model sounded competent. We are asking whether the repository can explain why a human should trust the next movement.

The trustworthy artifact is the governed proof run. It is the object that binds a declared workflow to admitted context, bounded tools, validation output, review gates, and retained evidence. It gives the human reviewer something more concrete than confidence and something less vague than a chat history. It shows the shape of the run before it asks for permission to continue.

The proof run is not a claim that the agent is autonomous in the strong sense. It is a narrower claim. It says: here is the contract the runtime resolved, here is the state it read, here is the policy it applied, here is the evidence it wrote, here is the gate where it stopped, and here is the record of the decision that resumed it. That is the source surface.

## The Architecture Is The Argument

Phase 2 only becomes legible when its authority is separated into layers. A `workflow.yaml` declares the behavior. A package `status.yaml` declares where a package is in its lifecycle. `harness_policy.yaml` supplies the allowed posture around paths, tools, validation, gates, lifecycle movement, and external mutation. `gate_contracts.yaml` defines the gates as reusable contracts. `pipeline_profiles.yaml` tells the runtime what route a package class is expected to follow.

None of those files proves anything alone. A workflow contract without package state is only an abstract playbook. A status file without a workflow is only a label. A gate contract without a run record is only a promise to stop later. The system becomes trustworthy when `content-agent` resolves the surfaces together and emits durable evidence.

That is why `content-agent` should be understood as runtime, not as a second workflow language. Its job is to execute declared behavior, not invent hidden behavior. It reads the workflow, admits the required context, checks the route, runs scriptable steps when allowed, records deferred steps when human or model judgment is required, writes run records, and materializes review gates before governed movement continues.

The evidence layer is where the architecture becomes inspectable. `reviewable-runs/resolved-runs/` records the resolved contract and context. `reviewable-runs/logs/` records what the run did. `reviewable-runs/gates/` records the stop point, the approval dimensions, and the resume instruction. The proof is not a single file. It is the correspondence between these files.

## What The Local Proof Shows

The current package exists because a governed topic-discovery run made a bounded handoff. The run resolved the `topic_discovery` workflow against the `literate-workflow-programming` umbrella package. It admitted the discovery trigger and prior archive context. It recorded the paper search surfaces, the candidate essay slate, and the handoff decision. It then stopped at the `topic_viability` gate before package initialization.

That stop was the point. The runtime did not quietly initialize a new publication package because the model liked the idea. It wrote a review gate with lifecycle movement required, recorded that no external mutation was attempted, and waited. Only after approval did the continuation initialize `publications/proof-runs-as-source-surface/`.

The same pattern repeated at research exit. The package gathered a paper shortlist, wrote a research-exit gate, and stopped before marking research done. After approval, the package admitted the primary papers locally as PDFs and markdown conversions, updated its evidence surface, and moved into essay iteration. The prewrite pass then seeded a packet, hardened a blueprint, wrote a claim-boundary ledger, settled the prewrite gate, and stopped again before opening a bounded candidate.

This is modest, but it is the right kind of modest. The run does not prove that an agent can publish safely. It proves that local lifecycle movement can be routed through declared contracts, visible gates, explicit approval dimensions, and retained artifacts. That is the first useful bar for autonomous content work.

## Why The Research Points In This Direction

The broader research literature is converging on the same pressure from a different angle. SWE-AGI frames autonomous software construction as a specification-driven task and shows both the promise and the remaining scaling problem: agents can perform impressive long-horizon work, but hard specification-intensive systems still expose reliability limits (Zhang et al., 2026). The useful lesson for content work is not that coding benchmarks transfer directly. It is that serious autonomy needs an authoritative specification surface and a deterministic evaluation boundary.

Spec Kit Agents makes the operational version of that argument. Its workflow adds context-grounding hooks and validation hooks around spec-driven development so that agents do not merely produce coherent intermediate artifacts that fail against the repository (Taghavi and Bhavani, 2026). Phase 2 makes the same bet inside a publication repo. Context admission is explicit. Validation is a named hook. The runtime cannot treat plausible prose as enough.

SWE-Bench Pro supplies the caution. Long-horizon industrial tasks remain hard, even when the benchmark is designed around human-verified, context-rich issues (Deng et al., 2025). That matters because publication work has its own long-horizon failure modes: source drift, claim inflation, unresolved gates, stale package state, and unsafe distribution movement. A proof run does not remove these risks. It makes them reviewable before movement continues.

The Productivity-Reliability Paradox pushes the same point at the methodology level. If AI work increases local output while increasing review burden or reducing system reliability, then speed is not the governing metric (Farrag, 2026). Specification discipline becomes the constraint. In this repo, that discipline appears as declared workflow contracts, package state, gate contracts, validation scripts, and run records.

Talk Freely, Execute Strictly gives the sharpest vocabulary for the boundary. Conversational flexibility and execution determinism pull in different directions, and schema-gated execution separates what a person can ask from what a system is allowed to run (Strickland et al., 2026). Phase 2 is not a scientific workflow system, but the architectural instinct is the same: let language remain flexible while execution authority passes through a machine-checkable boundary.

SPECA adds the audit lesson. The point of a specification is not only to guide action. It can produce explicit properties, make failures traceable to pipeline phases, and turn a vague model error into a ranked engineering target (Kamba et al., 2026). A content proof run is not a security audit, but it borrows the same shape: make the property visible, make the evidence durable, and make the failure mode reviewable.

## Gates Are The Boundary

It is tempting to treat gates as process overhead. That misses their function. A gate is the system admitting that probabilistic work has reached a boundary where further movement needs a different kind of authority.

Before a gate, the agent can search, draft, resolve, validate, and record within the workflow's allowed envelope. At the gate, the system changes posture. It asks whether quality, lifecycle movement, promotion, or external mutation is required. It records which dimensions were approved and which were not. It makes the resume action explicit.

This matters because content work mixes many kinds of movement that should not share one approval. Approving a topic is not approving publication. Approving a prewrite gate is not approving live-draft replacement. Approving a local lifecycle transition is not approving an external Substack mutation. The gate contract keeps those permissions apart.

That separation is the core trust mechanism. It lets the repository say yes to one movement without accidentally saying yes to everything downstream. It also lets the next reviewer reconstruct the boundary after the fact. The proof run is therefore not just evidence that work happened. It is evidence that the system knew where work had to stop.

## What This Gives The Human Reviewer

The human reviewer gets a narrower but stronger object than a transcript. They can inspect the workflow contract, the resolved run, the run record, the gate, the decision record, and the resume record. They can see which context was admitted and which optional context was missing. They can see which validation command passed. They can see whether external mutation was attempted.

This changes the review question. Instead of asking, "Do I believe this agent?" the reviewer can ask, "Does this evidence authorize this specific next movement?" The first question invites personality judgment. The second invites operational judgment.

That is why proof runs belong in the source tree. They are not merely logs. They are part of the repository's memory of authority. They let later agents and humans reconstruct why a package exists, why it entered a stage, what evidence supported the move, and which claims remained forbidden.

## Limits

This essay does not claim that Phase 2 has proven autonomous publication reliability. It has not. The current proof covers local governed runtime behavior through topic discovery, package initialization, research exit, paper intake, and essay-iteration prewrite. Release readiness, public publication, archive sync, YouTube production, and distribution still need their own governed evidence.

It also does not claim that gates prove quality by themselves. A gate can only record the evidence, approval dimensions, and decision at a boundary. The quality of the artifact still depends on the artifact, the validator, and the reviewer. A weak review behind a strong gate remains weak.

The final boundary is architectural. `content-agent` must not become a hidden source of truth. If the runtime starts inventing behavior outside `workflow.yaml`, the proof model collapses. The source surface works only because declared workflow, package state, policy, gates, profile, runtime execution, and retained evidence remain distinct.

## References

#### [SWE-AGI: Benchmarking Specification-Driven Software Construction with MoonBit in the Era of Autonomous Agents](https://arxiv.org/abs/2602.09447)

Zhang et al. frame autonomous software construction as end-to-end work from explicit specifications under a fixed API scaffold. The paper supports the essay's claim that serious agent autonomy needs specification discipline and deterministic evaluation, while its hard-task failures preserve the reliability caveat.

#### [Spec Kit Agents: Context-Grounded Agentic Workflows](https://arxiv.org/abs/2604.05278)

Taghavi and Bhavani add context-grounding and validation hooks around spec-driven agent workflow phases. The paper supports Phase 2's separation between declared workflow, admitted repository context, and validation hooks.

#### [SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?](https://arxiv.org/abs/2509.16941)

Deng et al. show that long-horizon industrial software tasks remain difficult for current agents even in richer benchmark settings. The paper supplies the pressure against turning local proof-run success into broad autonomy claims.

#### [The Productivity-Reliability Paradox: Specification-Driven Governance for AI-Augmented Software Development](https://arxiv.org/abs/2605.01160)

Farrag argues that AI-assisted development can raise local productivity while increasing reliability and review burdens when specification discipline is weak. The paper supports the essay's claim that governance surfaces matter more than raw model output.

#### [Talk Freely, Execute Strictly: Schema-Gated Agentic AI for Flexible and Reproducible Scientific Workflows](https://arxiv.org/abs/2603.06394)

Strickland et al. separate conversational flexibility from execution authority through schema-gated orchestration. The paper gives the cleanest external vocabulary for Phase 2's gate boundary.

#### [Beyond Code Reasoning: Specification-Anchored Auditing of Multi-Implementation Distributed Protocols](https://arxiv.org/abs/2604.26495)

Kamba et al. show how specification-derived properties can make audit findings and false positives traceable to pipeline phases. The paper supports the claim that explicit specifications can turn opaque model behavior into reviewable evidence.

## Limits

State the boundaries, counterpressure, or what the essay will not claim.

## References

Include real endmatter or references, not just a companion pointer. Use author-year citations in the body where sources carry claims. For cited papers, prefer h4 headings linked to the arXiv paper or canonical source, followed by a short paragraph explaining each source's core contribution to this essay.
