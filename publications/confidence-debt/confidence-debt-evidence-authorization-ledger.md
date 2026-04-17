# Confidence Debt Evidence Authorization Ledger

## Purpose

This ledger sits between the source library and the blueprint.

- `papers/index.md` answers: what sources do we have?
- this ledger answers: what claims are those sources allowed to license?
- `blueprint.md` answers: what essay architecture follows from the authorized claims?

The goal is to prevent nearby evidence from becoming load-bearing evidence by accident. A source can be relevant without authorizing the claim the draft wants to make.

## Support Levels

Use these labels consistently:

- `Direct`: the source directly supports the claim.
- `Hinge`: the source supports a necessary bridge in the argument.
- `Analogical`: the source is suggestive but does not prove the claim.
- `Synthesis`: the claim integrates several supported claims but is not directly proven by one source.
- `Speculative`: useful idea, not safe as an asserted claim.

## Claim Map

| ID | Claim | Sources | Support | Authorized Wording | Caveat | Draft Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | Confidence debt names a workflow-level trust gap, not model overconfidence alone. | eip-verify artifacts; Simhi et al.; Rich et al.; overreliance literature | Synthesis | A system incurs confidence debt when output is trusted downstream before evidence warrants that trust. | No single source coins the full frame. | Definition |
| C2 | Polished AI summaries can outrank stronger row-level evidence unless workflows impose adjudication rules. | eip-verify artifacts: scored run, contradiction register, evidence ledger | Direct | In the eip-verify case, the polished summary would have propagated without an evidence hierarchy and contradiction register. | First-party case; inspectable but narrow. | Opening and artifact layer |
| C3 | Claim auditability is the right artifact-layer control surface. | From Fluent to Verifiable; PaperTrail; First Principles Framework; Compliance-by-Construction Argument Graphs; eip-verify | Synthesis with direct components | Promoted claims need visible evidence state, contradiction state, and expiry condition. | The exact eip-verify pattern is one instantiation, not a universal standard. | Doctrine gate 1 |
| C4 | Provenance displays alone do not guarantee better reviewer behavior. | PaperTrail | Direct | Evidence displays can reduce subjective trust while still leaving a trust-behavior gap. | Do not overstate PaperTrail beyond its studied setting. | Human-layer caveat |
| C5 | Benchmark scores become confidence debt when they are converted into deployment claims beyond what the benchmark measured. | tau-bench; WebSuite; WebForge; Towards a Science of AI Agent Reliability; ReliabilityBench | Synthesis with direct components | A benchmark score should license only the kind of trust the evaluation design actually measured. | This is an interpretive rule, not a finding from one paper. | Evaluation layer |
| C6 | A deployment-facing evaluation gate should measure a reliability envelope, not only pass rate. | ReliabilityBench; Beyond pass@1; Canonical Path Deviation; Measuring Agents in Production; AgentCompass | Synthesis with direct components | Before deployment, teams should measure repeated-run stability, perturbation robustness, fault tolerance, long-horizon decay, and trace-level failure modes. | No universal thresholds. Domains must set release criteria. | Doctrine gate 2 |
| C7 | Repeated-run stability, perturbation robustness, and fault tolerance are concrete reliability dimensions for agent deployment. | ReliabilityBench | Direct | ReliabilityBench evaluates `R(k, epsilon, lambda)`: repeated execution, task perturbation, and production-like infrastructure faults. | One benchmark/framework; not a complete deployment certification regime. | Evaluation layer |
| C8 | Capable agents can fail through trajectory drift, not just lack of task capability. | Canonical Path Deviation | Direct | Long-horizon agent failures can arise when runs drift away from canonical successful action paths. | Applies to studied tool-use setting; use as mechanism, not universal law. | Evaluation layer mechanism |
| C9 | Production agent reliability depends on system design, bounded autonomy, and monitoring, not model choice alone. | Measuring Agents in Production; AgentCompass; Runtime Governance; Trustworthy Agentic AI Requires Deterministic Architectural Boundaries; COCO | Synthesis with direct components | Production readiness requires bounded autonomy, structured workflows, runtime monitoring, error localization, and recovery/rollback paths. | The exact stack is an integration across adjacent work. | Evaluation-to-deployment bridge |
| C10 | Human correction capacity is a workflow property that can be preserved or eroded. | AI Assistance Reduces Persistence; How AI Impacts Skill Formation; Mitigating Epistemic Debt; The Competence Shadow | Synthesis with direct components | AI assistance can improve immediate output while weakening later persistence, understanding, debugging, or correction capacity. | Evidence spans lab and domain-specific studies; avoid universal claims. | Human layer |
| C11 | The human-layer control should be software-mediated co-audit, not generic exhortation to be careful. | Co-audit; Cognitive Forcing Functions; Evaluative AI; PaperTrail; Measuring and Mitigating Overreliance; Taxonomy of Questions; Scaffolded Cognitive Friction | Synthesis with direct components | The reviewer should receive an audit workspace that surfaces claims, assumptions, omissions, contradictions, and counter-hypotheses before acceptance. | The integrated workspace has not been validated as one system. | Doctrine gate 3 |
| C12 | Plan-focused assumption prompts are a concrete way to reduce passive acceptance. | Cognitive Forcing Functions for Execution Plans | Direct | Assumption-focused cognitive forcing can reduce overreliance without adding measured cognitive load in the studied plan-review setting. | Do not generalize every prompt type or domain. | Co-audit design detail |
| C13 | Hypothesis-driven decision support is a constructive alternative to recommendation-first support. | From Evidence to Decision | Direct/Hinge | Interfaces should show evidence for and against candidate judgments rather than only issuing recommendations. | Evidence is from specific decision-support domains. | Rival hinge and co-audit |
| C14 | The three-gate doctrine is the essay's operating synthesis. | C3, C6, C11 | Synthesis | Confidence debt is controlled by claim auditability before trust, reliability release gates before deployment, and co-audit software before human acceptance. | Not validated end to end. Present as doctrine assembled from adjacent literatures. | Ending doctrine |
| C15 | Cross-layer compounding remains the central evidence risk. | eip-verify micro-case; Competence Shadow; automation-bias literature; C3/C6/C11 | Synthesis | The structural conditions for cross-layer compounding exist, and one worked case illustrates the pattern. | Do not claim a complete causal chain has been proven across artifacts, evaluation, and human oversight. | Cascade section and limits |
| C16 | Responsible-looking deployment controls can become confidence-debt transfer points. | Measuring Agents in Production; Documenting Deployment with Fabric; Evaluation-Driven Development and Operations; Eval Factsheets; Audit Cards; NIST AI RMF / GenAI | Synthesis with direct practice components | Documented deployment practice often compresses readiness into artifacts, evaluation evidence, bounded execution, and human review; confidence debt begins when those controls transfer trust beyond the evidence limits they preserve. | The sources document practices and documentation gaps. They do not directly measure trust transfer as a causal outcome. | Debate bridge and early thesis sharpening |

## Source Burden

| Source | Job | Role | Must Appear? | Notes |
| :--- | :--- | :--- | :--- | :--- |
| eip-verify evidence artifacts | Provide the inspectable opening case and artifact-layer contradiction. | Body | Yes | Strongest concrete asset. |
| Simhi et al., Trust Me, I'm Wrong | Support confidence/correctness decoupling. | Reference or light body | Optional | Useful but not central once the eip-verify case carries the opening. |
| From Fluent to Verifiable / AAR | Anchor claim-level auditability. | Body or doctrine | Yes | Use for provenance coverage, soundness, contradiction transparency, audit effort. |
| PaperTrail | Anchor claim-evidence interfaces and the trust-behavior gap. | Body or doctrine | Yes | Important for both artifact and human gates. |
| First Principles Framework | Support epistemic status and temporal validity. | Hinge | Optional | Strong for expiry condition, but may be too much for main prose. |
| Compliance-by-Construction Argument Graphs | Support evidence-linked formal argument records. | Hinge | Optional | Use if the artifact gate needs more authority. |
| tau-bench | Show repeated-run reliability collapse behind pass rate. | Body | Yes | Existing evaluation opener still works. |
| WebSuite and WebForge | Show richer evaluation surfaces make toplines less sufficient. | Body | Yes | Keep compressed. |
| Towards a Science of AI Agent Reliability | Provide reliability dimensions. | Body | Yes | Bridges old evaluation section to release gate. |
| ReliabilityBench | Anchor the deployment reliability envelope. | Body | Yes | Highest-value new evaluation source. |
| Beyond pass@1 / long-horizon reliability | Add long-horizon decay, variance, graceful degradation, meltdown. | Body or hinge | Yes | Use selectively to avoid metric sprawl. |
| Canonical Path Deviation | Explain capable-but-unreliable trajectory failure. | Body or hinge | Yes | Gives the evaluation gate a mechanism. |
| Measuring Agents in Production | Ground production practice: bounded autonomy, structured workflows, oversight. | Hinge | Yes | Bridges evaluation to deployment. |
| Documenting Deployment with Fabric | Ground real-world AI governance patterns: workflow diagrams, oversight levels, thresholds, policies, standards, regulation, and signoff. | Hinge | Optional/bridge | Use for the responsible-shipping-stack bridge, not as evidence that governance mechanisms are effective. |
| Evaluation-Driven Development and Operations | Support evaluation as lifecycle governance rather than a terminal checkpoint. | Hinge | Optional/bridge | Good for the claim that eval results must remain connected to operational evidence. |
| Eval Factsheets | Support evaluation documentation limits: assumptions, validity conditions, judge selection, contamination checks, statistical validation. | Hinge | Optional/bridge | Use if sharpening the score/dashboard critique. |
| Audit Cards | Support evaluation reporting context and decision-making interpretation. | Hinge | Optional/bridge | Already local; useful for documentation-as-governance surface. |
| AgentCompass | Support trace monitoring, error taxonomy, localization, fix recipes. | Hinge | Yes | Supports post-deployment actionability. |
| Runtime Governance / deterministic boundaries / COCO | Support governed execution, rollback, control planes. | Reference or hinge | Optional | Useful for blueprint; may overload the essay body. |
| AI Assistance Reduces Persistence | Open human layer with causal evidence. | Body | Yes | Keep as vivid human-layer turn. |
| How AI Impacts Skill Formation | Show interaction pattern matters. | Body | Yes | Mechanism for competence preservation/erosion. |
| Mitigating Epistemic Debt | Show scaffolded vs unrestricted assistance divergence. | Body | Yes | Links to debt language. |
| The Competence Shadow | Formalize compounding inside machine-pruned search spaces. | Body | Yes | Strongest bridge to cascade. |
| Co-audit | Name the human-layer software category. | Doctrine | Yes | Turns "human oversight" into an interface requirement. |
| Cognitive Forcing Functions | Provide tested reviewer action, especially assumption prompt. | Doctrine | Yes | Concrete design detail for co-audit. |
| From Evidence to Decision | Provide hypothesis-driven alternative to recommendation-first interfaces. | Hinge | Yes | Also serves rival-hinge section. |
| Measuring and Mitigating Overreliance | Frame overreliance as a deployment measurement problem. | Hinge | Optional | Position paper, useful but not decisive. |
| Taxonomy of Questions / Scaffolded Cognitive Friction | Support targeted reflection prompts. | Reference or hinge | Optional | Keep out of body unless co-audit section feels thin. |
| Appropriate reliance and pathology papers | Show rival frames are real but within-layer. | Hinge | Optional | Use only enough to keep borders credible. |

## Local Intake Status

The package-local paper inventory has been updated in [`papers/index.md`](papers/index.md). That index owns local PDF and markdown paths; this ledger owns claim authorization. Do not duplicate path tables here unless a source becomes ambiguous.

Actionability-pass sources now intaken and converted include:

- artifact gate: PaperTrail, First Principles Framework, Compliance-by-Construction Argument Graphs
- reliability release gate: ReliabilityBench, Beyond pass@1, Canonical Path Deviation, Measuring Agents in Production, AgentCompass, runtime governance, deterministic boundaries, COCO
- co-audit gate: Co-audit, Cognitive Forcing Functions, Measuring and Mitigating Overreliance, Critical Reflection Taxonomy, Support Relations

Debate-bridge sources now intaken and converted include:

- shipping-practice bridge: Documenting Deployment with Fabric, Evaluation-Driven Development and Operations, Eval Factsheets

The shipping-practice bridge is formalized in [`confidence-debt-shipping-practice-warrant-ledger.md`](confidence-debt-shipping-practice-warrant-ledger.md). Use it only to support the claim that responsible-looking deployment practice has real transfer tokens: artifacts, evaluation evidence, bounded execution, monitoring, and human approval. It does not authorize claiming a measured causal chain from those tokens to failure.

The main known gap is no longer local availability of the evidence. The gap is epistemic: the three-gate stack remains an argued synthesis rather than an end-to-end validated deployment system.

## Synthesis Boundary

| Synthesis Claim | What Sources Prove | What They Do Not Prove | Safe Framing |
| :--- | :--- | :--- | :--- |
| Confidence debt is a cross-layer propagation pattern. | Artifact contradictions, score over-reading, and human correction erosion each exist as documented problems. | No single study proves the full artifact-evaluation-human cascade across deployments. | "A structural inference from converging evidence, illustrated by one worked case." |
| The three gates are the right operating doctrine. | Each gate has adjacent literature and partial implementations. | The three-gate stack has not been evaluated end to end. | "A defensible operating doctrine assembled from adjacent literatures." |
| Claim auditability controls artifact-layer debt. | Claim provenance, contradiction transparency, evidence ledgers, and argument graphs are supported directions. | No source proves the exact eip-verify framework is complete. | "One concrete instantiation of claim auditability." |
| Reliability release controls evaluation-layer debt. | Reliability surfaces, long-horizon decay, path deviation, production monitoring, and runtime governance are concrete methods. | No universal deployment threshold exists. | "Teams need a measured reliability envelope before turning scores into deployment claims." |
| Co-audit controls human-layer debt. | Co-audit tools, CFFs, evaluative AI, and reflection prompts can support human review. | Evidence display alone does not guarantee behavior change, and the integrated workspace is unvalidated. | "The human layer needs software that requires structured correction, not just warnings." |

## Forbidden Claims

- Do not claim the three-gate doctrine has been empirically validated as one complete system.
- Do not claim confidence debt is just model overconfidence, calibration failure, or user overreliance.
- Do not claim all AI assistance produces confidence debt.
- Do not claim every domain requires identical safeguards.
- Do not prescribe universal reliability thresholds, autonomy limits, rollback criteria, or co-audit prompts.
- Do not imply that provenance displays alone fix overreliance.
- Do not imply that co-audit interfaces reliably change behavior at production scale unless a stronger field study is added.
- Do not treat the first-party eip-verify case as cross-domain proof. It is an inspectable worked case.
- Do not claim the artifact-score-approval stack is universal across all AI deployment or that teams knowingly launder confidence.
- Do not cite every relevant paper in the body. Sources must do body work, hinge work, or stay in references.

## Blueprint Instructions

- The final doctrine must be the three gates, stated compactly enough that a reader can reuse it.
- The artifact layer may use the eip-verify framework as the concrete case, but should name the broader control surface as claim auditability.
- The evaluation layer should move from "benchmark interpretation" to "reliability release." The test is whether the system's reliability envelope has been measured before a score becomes a deployment claim.
- The human layer should move from "preserve correction capacity" to "build a co-audit layer." The test is whether the reviewer gets software support for seeing assumptions, unsupported claims, omissions, contradictions, and counter-hypotheses.
- The cascade section must keep its epistemic status honest: the essay has a strong structural argument, not an end-to-end causal proof.
- The ending should not become a compliance checklist. It should give the reader one operating object: claim auditability, reliability release, co-audit.

## Open Evidence Gaps

- Strongest missing evidence: end-to-end studies where artifact confidence, evaluation interpretation, and human oversight interact in one deployment pipeline.
- Useful next evidence: field studies of claim-level auditability or provenance tools inside production workflows.
- Useful next evidence: large-scale co-audit studies that measure behavior change, not only subjective trust.
- Useful next evidence: runtime monitoring or rollback studies where reliability gates control promotion, rollback, or escalation.

## Intake Notes

The actionability-pass sources needed for candidate R3 are reflected in `papers/index.md` and converted into local markdown where available. If a later rewrite promotes a source currently marked optional or reference-only into body evidence, re-check the index and add intake before making it load-bearing.
