---
kind: claim_boundary_surface
package: "literate-workflow-programming/specification-surface-source-of-truth"
revision: 1
evidence_surface_path: "publications/literate-workflow-programming/papers"
auxiliary_evidence_paths:
  - "publications/literate-workflow-programming/harness_papers/index.md"
  - "publications/literate-workflow-programming/pivot/active/literate-workflow-programming-pivot-north-star-viability.md"
  - "publications/literate-workflow-programming/research-notes/alphaxiv-discussions/019dd4c6-reopened-specification-surface-pressure-test.md"
gate_role: research_exit_claim_boundary
---
# Specification Surface Claim Boundary Ledger

## Purpose

This ledger is the claim-boundary surface for the successor leaf `The Specification Surface Is the New Source of Truth`.

It sits between the shared paper index, the successor research handoff, and the next essay-iteration packet. It does not replace the shared umbrella claim-state surfaces. Its job is narrower: state which claims the successor leaf may carry into a bounded draft, which claims require visible caveats, and which claims remain forbidden until a later evidence pass.

## Source Surfaces

Primary local evidence surface:

- [`../papers/`](../papers/)
- [`../papers/index.md`](../papers/index.md)

Auxiliary surfaces used for successor-specific framing:

- [`../harness_papers/index.md`](../harness_papers/index.md)
- [`research-handoff.md`](research-handoff.md)
- [`../pivot/active/literate-workflow-programming-pivot-grounding-review.md`](../pivot/active/literate-workflow-programming-pivot-grounding-review.md)
- [`../pivot/active/literate-workflow-programming-pivot-north-star-viability.md`](../pivot/active/literate-workflow-programming-pivot-north-star-viability.md)
- [`../research-notes/alphaxiv-discussions/019dd4c6-reopened-specification-surface-pressure-test.md`](../research-notes/alphaxiv-discussions/019dd4c6-reopened-specification-surface-pressure-test.md)
- Generated launch pack: [`../../../reviewable-runs/logs/2026-04-29_00-12-59_literate-workflow-programming__specification-surface-source-of-truth_research_launch-pack.json`](../../../reviewable-runs/logs/2026-04-29_00-12-59_literate-workflow-programming__specification-surface-source-of-truth_research_launch-pack.json)

## Claim Map

| Claim ID | Authorized Claim | Evidence Status | Draft Permission | Boundary |
| :--- | :--- | :--- | :--- | :--- |
| SS-C1 | In AI-native development, durable authority increasingly shifts toward maintained specification surfaces, especially where agents generate, revise, test, or coordinate implementation. | Synthesis claim supported by the pivot pressure test, successor handoff, local specification-as-source papers, harness/spec-language papers, and locally intaken bridge papers `2602.00180`, `2603.24284`, and `2512.14012`. | Body claim. Use as the largest claim only with the maintained/controlled/validated surface qualifier. | Do not say generated implementation stops mattering. Do not say all prose becomes code. |
| SS-C2 | The public enemy is `vibe`: treating intent as informal prompt material while generated code remains the only serious artifact. | Supported by the successor handoff, north-star gate, the locally intaken professional-control paper `2512.14012`, specification-gap pressure, and VibeContract/QA evidence in the shared index. | Opening and antagonist claim. | Do not turn the essay into a generic vibe-coding commentary piece. Keep the target on source-of-truth authority. |
| SS-C3 | A specification surface is a written artifact that becomes operational only when it is controlled, maintained, typed, linted, validated, trace-linked, or interpreted by a runtime. | Strongly supported by local harness/specification papers, ContextCov, TDAD, AgentSPEX, Natural-Language Agent Harnesses, FASTRIC, ALARA, Progent, and the controlled-language bridge queue. | Body definition and section spine. | Do not treat ordinary README text, one-off prompts, or passive markdown as automatically governed specification surfaces. |
| SS-C3a | Natural language becomes part of a governing specification only when bound to executable lifecycle semantics, artifact contracts, state, adapters, validation, and recovery behavior. | Expert-feedback correction from Linyue Pan on 2026-05-05, consistent with the local Natural-Language Agent Harnesses evidence and the essay's runtime/harness caveat. | Paper-route boundary and future revision guardrail. | Do not treat every natural-language instruction interpreted by a harness as a governing specification. Keep the distinction between instruction/interface layer and governing specification. |
| SS-C4 | Context files and agent instruction files are evidence for emerging machine-facing project artifacts, but only under a task-risk and metric caveat. | Mixed evidence surface: Agent READMEs and context-engineering papers show living configuration behavior; Evaluating AGENTS.md and prior contradiction work block context-file boosterism. | Use with caveat. Good for a caution paragraph or pressure turn. | Do not claim AGENTS.md-style files are globally good or globally bad. |
| SS-C5 | Richer specifications matter because underspecification causes coordination, review, validation, or traceability failures. | Supported by locally intaken `2603.24284`, local validation/trace papers, ContextCov, AgentFixer, AgentPex, and the local spec-diff prototype lineage. | Body or proof section. | Do not claim richer specification alone guarantees better model behavior. Formality remains a diagnostic surface, not automatic conformance. |
| SS-C6 | Specifications, not run logs or generated outputs, are the source-of-truth candidate; traces and logs are debugging and validation surfaces. | Directly supported by Bootstrapping Coding Agents, AgentSPEX, trace-compliance papers, claim-level auditability, and the donor leaf claim-state surfaces. | Body/proof boundary claim. | Do not promote Reviewable Runs or local spec-diff output into full semantic provenance graphs. |
| SS-C7 | Controlled natural language, prompt/program state interfaces, and task contracts are bridge evidence for the broader public claim. | Supported by the successor P0/P1 reopen queue and pivot grounding review. | Use as bridge evidence after deterministic inspection or in caveated synthesis. | Quote-level body use should trigger intake or direct inspection first. |

## Source Burden

Body burden:

- `2603.17399`, `2603.25723`, `2604.13346`, `2603.00822`, `2603.08806`, `2512.18940`, `2603.23806`, `2603.29848`, and `2602.13855` carry the local source/runtime/validation/trace stack.
- `2408.04820`, tracked in `harness_papers/`, carries the strongest literal natural-language outline surface.
- `2602.00180`, `2603.24284`, and `2512.14012` are now locally intaken and carry the r2 bridge burden: specification authority outside a pure agent-harness niche, underspecification as coordination failure, and professional practice as planning, supervision, validation, and version control rather than vibe delegation.
- `2512.14805`, `2508.06942`, and `2603.15691` remain bridge queue papers for prompt/program state interfaces, controlled natural language, and VibeContract-style QA if a later pass needs more breadth.

Caveat burden:

- `2602.11988`, `2601.20404`, `2511.12884`, and `2510.21413` govern the context-file claim. They force metric-specific wording.
- FASTRIC and prior claim-state notes govern the formality caveat: explicit specifications make conformance checkable, but stricter form is not automatic behavioral improvement.

Optional or follow-on burden:

- `2604.08224`, `2604.05278`, `2603.05344`, `2602.20478`, `2512.05470`, and the harness-paper library can support a broader context/externalization section if the candidate needs it.
- Skills-specific papers remain secondary unless the essay opens a skills section.

## Synthesis Boundary

The essay may synthesize across papers to argue that source-of-truth authority is moving upstream into governed specification surfaces.

That synthesis is not a single-paper finding. It is licensed only if the draft keeps the component claims visible:

- specifications can be maintained as stable artifacts;
- harnesses and agents can interpret specification artifacts;
- validators, tests, policies, or trace links give the surface operational force;
- negative context-file evidence blocks loose natural-language boosterism;
- professional AI-assisted practice requires design control, supervision, and verification.

## Forbidden Claims

- Do not say `natural language is code`.
- Do not say natural language becomes a governing specification merely because a harness interprets it.
- Do not say loose prose, one-off prompts, or ordinary documentation are source-of-truth artifacts.
- Do not say generated code no longer matters.
- Do not say context files are automatically beneficial.
- Do not say formal specifications monotonically improve agent behavior.
- Do not say the current repo already has full claim-level provenance graphs.
- Do not turn the successor into the old `contract layer` frame.

## Drafting Instructions

- Use `specification surface` as the governing term.
- Use `vibe` as the public enemy only when it clarifies the source-of-truth error.
- Keep `controlled`, `maintained`, `validated`, `typed`, `linted`, or `trace-linked` near the largest claim.
- Treat nonlocal P0/P1 bridge papers as draft-pressure triggers for direct inspection before quotation-heavy use.
- Carry the context-file caveat beside any AGENTS.md or README claim.
- Keep local `spec-diff` as a bounded drift exhibit, not a broad conformance proof.

## Follow-On Research Triggers

- Direct use of `2602.00180`, `2603.24284`, and `2512.14012` is now allowed from the local markdown conversions, with the normal caveat that `2602.00180` has noisy first-page extraction. If the draft needs direct quotations or close readings from `2512.14805`, `2508.06942`, or `2603.15691`, run targeted intake or deterministic inspection before promotion.
- If the largest durable-authority claim starts sounding universal, reopen the specification-gap and professional-control evidence before continuing.
- If the draft turns into context-file advocacy, reopen the negative AGENTS.md evidence and cut back to the governed-surface claim.
