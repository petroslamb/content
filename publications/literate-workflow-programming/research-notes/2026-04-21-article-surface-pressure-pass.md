# Article Surface Pressure Pass

Date: 2026-04-21

Status: surface-completion synthesis, not paper intake.

## Purpose

This pass pushed beyond the first claim-state gap note to reach the article surface claimed in [`../literate-workflow-programming.md`](../literate-workflow-programming-flagship/literate-workflow-programming.md).

The target was not a new lead. The target was a cleaner surface:

- where the article's vocabulary is separated
- where the strongest extensions and contradictions are visible
- where the remaining parked claims are explicitly bounded

## Method

Broad alphaXiv assistant synthesis kept drifting. The reliable pattern was narrower:

1. deterministic alphaXiv summary or abstract retrieval
2. single-paper grounded assistant probe
3. local adoption only when the grounded assistant output matched the retrieved summary or abstract

This note therefore treats the assistant as a pressure surface, not as primary evidence.

## Term Boundaries

| Term | Safest Meaning Here | Strongest Anchors | Boundary |
| :--- | :--- | :--- | :--- |
| context engineering | governed construction, storage, retrieval, delivery, and evaluation of context artifacts under window, provenance, and human-governance constraints | `2512.05470`, `2602.20478`, `2603.05344` | broader than workflow source; context engineering does not by itself prove that workflow files are source code |
| natural-language harness | runtime orchestration logic externalized into editable natural-language contracts, adapters, roles, and validation hooks | `2603.25723`, `2604.05278` | not a generic README or static policy file |
| agent specification language | explicit workflow, state, and control representation that can be adapted, validated, or executed across runtimes | `2510.04173`, `2512.19769`, `2604.13346` | not the whole of context engineering |
| prompt specification language | formal interaction procedures whose conformance can be checked over traces | `2512.18940` | narrower than an agent workflow language |
| skills-as-code | externalized procedural expertise that needs capability binding, routing, verification, and often compilation/runtime adaptation | `2604.03088`, `2602.12670`, `2604.01687`, `2604.08224` | not raw portable markdown by default |
| literate programming for agents | the article's synthesis label for inspectable specification surfaces plus validators, traces, provenance, and human-readable context in one workflow system | ICM plus harness/spec/trace papers | not a paper-native standard or settled category |

## Surface Extensions

### 1. Context Engineering Is The Broader Substrate

`2512.05470` and `2602.20478` make the broader context-architecture story stronger. They support governed file-system abstractions, persistent context repositories, hot/cold memory splits, and load-bearing context infrastructure.

This matters because the article should not collapse context engineering into workflow source. Context engineering is the broader substrate. Workflow source is the narrower claim about inspectable specifications, validators, and traces.

### 2. Validation Is Lifecycle Infrastructure

`2604.05278` and `2411.13768` both strengthen the article's hinge claim about validation. Spec Kit Agents adds phase-level context-grounding and validation hooks. EDDOps adds evaluation as a continuous, lifecycle-spanning feedback loop rather than a single test gate.

This supports a stronger sentence than the package had before:

Validation is not only a test at the end of execution. It is the lifecycle infrastructure that keeps specifications connected to the environment they are supposed to govern.

### 3. Trace Checking, Provenance, And Auditability Form A Stack

`2603.23806` and `2603.29848` support specification-based trace checking and trajectory-level failure localization. `2602.13855` pushes the stack further by making claim-level auditability and semantic provenance explicit architectural targets.

The safe decomposition is:

- trace checking: did the run follow the declared behavioral rules?
- failure localization: where in the trajectory did the system drift or break?
- claim-level auditability: can a generated claim be traced back to evidence and reasoning structure?

The article should say current Reviewable Runs sit in the first layer and parts of the second. They do not yet satisfy the third.

### 4. Skills Are Useful Before They Are Portable

`2602.12670` shows curated skills can materially improve agent performance. `2604.01687` shows verified, self-evolved skills can outperform human-curated baselines on benchmark tasks. Neither result removes the portability caveat from SkVM or the semantic-selection limit from Single-Agent With Skills.

That means the stronger article sentence is:

Skills can clearly help before the system has solved portability, routing, and namespace pressure. The article should attack the stronger claim that skills are already a portable production substrate when expressed as raw markdown.

### 5. Workflow-As-Namespace Is Safe. Package-As-Object And Imports Still Are Not.

`2604.13108` shows formal architecture descriptors have direct navigational value. `2512.05470`, `2602.20478`, and `2604.08224` all support externalized context structures that guide navigation, retrieval, and coordination.

This is enough to defend the narrower synthesis:

Workflow-structured context bundles can act as navigational namespaces for a single agent.

It is not enough to defend:

- packages as objects in a strong software-theory sense
- imports as compiler-like semantics rather than repo experiments

Those claims stay parked.

### 6. Control Surfaces Need Static Contradiction Checks

`2603.08993` matters because it shows contradictions, redundancies, and ambiguities inside agent control prompts are detectable as architecture problems. The paper also warns that models may smooth over contradictions at runtime, so static detection does not automatically prove visible user harm.

That gives the article a clean addition:

Workflow-source systems need static contradiction checking over their control surfaces, but static contradiction findings are validation signals, not direct evidence of runtime harm.

## Reached Article Surface

The article surface is now coherent enough to state in one pass:

Workflow specifications are the visible surface. Context engineering is the broader substrate that feeds them. Validation is the hinge that keeps them attached to the environment. Policy enforcement and contradiction checks keep the control surface coherent. Reviewable traces and drift checks make the system debuggable. Claim-level auditability is the next provenance layer. Skills belong in the story as an externalized procedural layer, but only with explicit routing, verification, and capability binding. "Literate workflow programming" remains the article's synthesis label for that stack, not the name of an already-settled paper category.

## What Still Stays Parked

- package-as-object semantics
- imports as compiler-level dependency semantics
- repo-wide validator promotion
- full Evidence Governance contradiction-ledger machinery beyond the curated register
- any claim that current Reviewable Runs already provide full semantic provenance

## Consequence For Drafting

The article can now safely separate its sections this way:

1. Why inspectable workflow specs are now plausible source surfaces
2. Why validation and enforcement, not prose alone, make the surface meaningful
3. Why traces, contradiction checks, and auditability complete the debugging stack
4. Why skills belong as a bounded extension rather than as a universal portability claim
