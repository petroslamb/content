# P1 Synthesis: Validation Gates Make Specs Real

Date: 2026-04-21

Status: research synthesis, article-frame decision

## Decision

The article should lead with this frame:

Agent workflow specs become meaningful source only when coupled to validation gates, policy enforcement, and semantic debugging traces.

The P1 batch strengthens the specification-language side of the package, but it also makes the narrower argument harder to avoid. A specification language is the visible surface. Validation is the hinge that turns the surface into engineering. Policy enforcement and trace-backed debugging are what keep the system from collapsing back into advisory prose.

That gives the article a cleaner shape than the original broad literate-programming metaphor. The piece can still use literate programming as the historical resonance, but the defensible current claim is a source/runtime/debugging stack for agent workflows.

## Reading Against The P0 Frame

The P0 batch established the source hierarchy: specifications and stage contracts should be primary, while run logs are traces that explain what happened relative to that source. The P1 batch answers where the stack gets pressure next.

| Paper | What It Adds | Boundary |
| :--- | :--- | :--- |
| Open Agent Specification (Agent Spec), `2510.04173` | A framework-agnostic agent and workflow representation can define components, control flow, data flow, runtime adapters, and evaluation across runtimes. | Supports portability and common representation. It does not prove that repo markdown is enough without parsers, adapters, and validation. |
| Declarative workflow DSL, `2512.19769` | Agent workflow logic can be separated from implementation and deployment, compiled to an intermediate representation, statically checked, run across backends, and inspected through diffs. | Strongest P1 evidence for workflow source as configuration. It is an enterprise DSL result, not a proof that loose markdown should be treated as executable. |
| FASTRIC, `2512.18940` | Prompt protocols can be expressed as finite-state structures and checked through procedural conformance over traces. | Supports prompt-level specification and trace analysis. It also warns that specification formality is model-dependent. |
| ALARA, `2603.20380` | Context, agent, and tool definitions become enforceable when represented as parsable files that structurally scope tool access and context. | Supports least-privilege context engineering. It shifts the article away from context volume and toward enforcement at the tool boundary. |
| Progent, `2504.11703` | Tool privileges can be governed by a deterministic policy DSL with runtime blocking, fallback actions, and state-aware policy updates. | Supports policy-as-code for agents. It narrows the security claim to the execution boundary, not model behavior in general. |
| Single-Agent With Skills, `2601.04748` | Multi-agent roles can sometimes be compiled into skills, but skill selection breaks under library size and semantic confusability. | Bridges this package to `illusion-of-swarm`. It supports skills-as-code and namespace pressure, not a universal collapse of multi-agent systems. |

## Lead Architecture

The article should describe three layers.

First, the visible layer is specification. Agent Spec, AgentSPEX, declarative workflow DSLs, FASTRIC, ICM, and natural-language harnesses all point toward explicit workflow artifacts that can be read, versioned, reused, or adapted. This is the part that makes the literate-programming analogy attractive.

Second, the hinge is validation. TDAD, ContextCov, the declarative DSL paper, FASTRIC, and Agent Spec all require some form of checking: tests, static validation, runtime type checks, conformance metrics, generated constraints, or evaluation harnesses. Without that layer, a workflow file is an instruction artifact, not a source artifact.

Third, the operational proof is debugging trace. Reviewable Runs, `spec-diff`, logging, replay, and provenance only matter if they map behavior back to the source specification. The trace should not become the source of truth. Its job is to reveal where the execution drifted from the declared state.

## What `spec-diff` Proves Here

The package-local `spec-diff` prototype is not a compiler. It is a small repo-native proof of the hinge. It takes a declared workflow state, reads the package evidence surface, and reports drift in a form reviewers can inspect. The P1 intake made that proof stronger because the validator caught ordinary in-progress drift before the index was repaired, then verified the repaired state.

The second proof threshold was one successful `spec-diff`-style run outside this package. That threshold was tested the same day against `publications/illusion-of-swarm/`: the validator caught real index and evidence-orientation drift, the repair stayed inside `papers/index.md`, and the final report passed. That is strong enough to discuss a retained proof candidate. It is still not ready for a shared root command until the promotion decision is made explicitly.

## Parked Claims

Several claims should stay out of the lead article frame for now.

- Markdown imports remain advisory until the repo has a real dependency resolver or context-packet compiler.
- Package-as-object semantics remain useful local vocabulary, but the papers support explicit state, harnesses, and schemas more directly than object identity for folders.
- Repo-wide validator promotion should wait for an explicit promotion decision. The `illusion-of-swarm` proof candidate is useful evidence, not an automatic root-interface change.
- Literate programming should remain a frame, not the asserted technical category. The paper-backed category is structured natural-language and declarative workflow source coupled to validators and traces.

## Next Use

Use this synthesis as the article lead decision in the live brief and claim ledger. P2 papers should now be read for context-file limits, terminal-native harnesses, and observability, not to reopen the lead frame unless they directly break this source/runtime/debugging stack.
