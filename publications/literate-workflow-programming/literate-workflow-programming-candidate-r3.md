# Candidate Draft

This bounded candidate must remain a sibling to the live draft. Do not overwrite `publications/literate-workflow-programming/literate-workflow-programming.md`.

Packet manifest: `publications/literate-workflow-programming/literate-workflow-programming-essay-iteration-packet-r3.json`
Current live draft: `publications/literate-workflow-programming/literate-workflow-programming.md`

# Literate Workflow Programming

When a validator reports that the package state, the governing brief, and the evidence surface no longer agree, the obvious old instinct is to keep digging for the hidden implementation bug. That instinct is now often wrong. The failure may already be in the human-readable workflow layer: the staged contract, the package manifest, the policy surface, the handoff file that defines what the system is allowed to do. Once a runtime can interpret those artifacts, validators can test them, and traces can point back to them, they stop being mere notes. If you keep treating them as commentary while they already govern behavior, you will keep debugging the wrong layer.

That is the useful claim here, and it is both narrower and sharper than the usual "markdown as code" slogan. The literature does not justify the fantasy that prose-heavy files magically execute themselves. It does justify something more operational: workflow specifications become source-like when other layers can load them, constrain them, test them, and expose failures against them. The important change is not that markdown became a programming language. It is that a human-readable specification layer is increasingly becoming the stable object operators edit, inspect, review, and debug, while older instincts still assume the real system must live somewhere else.

Several recent papers make that shift visible from different angles. Interpretable Context Methodology organized agent behavior around staged markdown contracts, folder structure, and preserved artifacts. Natural-Language Agent Harnesses externalized orchestration into editable contracts and adapters. AgentSPEX made the workflow surface explicit with typed steps, branching, modules, state, replay, and verification hooks. Bootstrapping Coding Agents supplied the strongest philosophical correction: the artifact of record should be the specification, not the residue produced from it. Read together, these systems are not telling us that passive text is executable. They are telling us that once the workflow surface is interpretable and replayable, pretending it is still just documentation becomes an engineering mistake.

That mistake gets more expensive once validation and policy enter the picture. Workflow files are not source-like because they are readable. They become source-like because other layers can enforce what they say. ContextCov extracts executable checks from instruction files. ALARA and Progent move context and tool authority into a control layer that can actually bind runtime behavior. Test-Driven AI Agent Definition and AgentFixer widen the same pressure into hidden checks, regression logic, diagnosis, and repair. This is the hinge of the whole architecture. Without validators and policy, the workflow surface is aspiration. With them, the workflow surface becomes a governable object. Keep debugging only the hidden runtime and you will miss the place where the system is actually being shaped.

The role of traces looks different once that hinge is in place. Logs feel like deepest truth because they show exactly what happened, but they are only useful when the system still knows what should have happened. AgentPex is useful because it evaluates execution against source-derived rules. FASTRIC does something similar at the protocol layer. The local `spec-diff` proof in this repo matters for the same reason. It does not prove semantic equivalence or broad conformance. It proves something more modest and more revealing: declared package state can drift from the evidence and governance surface it claims to control, and that drift can be reported as a source-linked finding. That is why traces belong in this story as debugging surfaces rather than as primary source. A run log can show that a workflow violated its own procedure. It cannot, by itself, tell you whether you were even looking in the right layer.

Skills belong in the same architecture, but only under the same discipline. The literature is strong enough now to treat skills as more than decorative instructions, yet still too weak to justify the claim that raw markdown skills are already portable substrate. AgentSPEX, SkVM, and the skills-as-code work all point toward externalized procedural units that can be selected, adapted, and composed. Single-Agent With Skills sharpens the limit at the same time. Skills only become reliable building blocks when a runtime can bind capabilities explicitly, govern selection, and check execution against something stronger than optimistic prose. That matters here because the same error returns: if the surrounding runtime treats the human-readable artifact as soft commentary, the system will fail exactly where operators think they have already been precise.

Once workflow specifications are treated as governing surfaces, one pressure becomes unavoidable. You need provenance richer than file history or trace retention. Claim-Level Auditability is the strongest signal in that direction because it asks whether a promoted claim preserves not just where it appeared, but whether evidence supports it, conflicts with it, or leaves a live gap. The current repo does not fully satisfy that bar. It has validators, traces, contradiction surfaces, and bounded drift checks. Those are real pieces of a semantic debugging stack. They still fall short of claim-level provenance graphs, provenance coverage metrics, and contradiction-aware audit paths that survive across rewrites and promotions. That is not an embarrassment. It is the next honest engineering demand once you admit that workflow surfaces are no longer just notes.

Seen from that angle, literate workflow programming becomes a useful name for a stack rather than a slogan for markdown maximalism. The literate part is that the governing layer remains human-readable. The programming part is that this layer is increasingly interpreted, validated, constrained, and debugged like source. The practical correction is simple. Stop assuming the real system lives only in hidden implementation while workflow artifacts stay safely informal. In governed agent systems, that assumption is already stale. If we keep editing source-like workflow layers as if they were only commentary, we will keep diagnosing failures too late and in the wrong place.

## Limits

This draft does not claim that markdown alone is executable, that stricter formalization monotonically improves behavior, or that current Reviewable Runs already provide full claim-level provenance. It keeps package-as-object semantics, markdown import semantics, and repo-wide validator promotion parked. It also keeps the skills claim bounded: skills can be source-like workflow units, but current markdown skills are not being presented as already portable production substrate.

## References

- `2603.16021` Interpretable Context Methodology
- `2603.25723` Natural-Language Agent Harnesses
- `2604.13346` AgentSPEX
- `2603.17399` Bootstrapping Coding Agents
- `2603.08806` Test-Driven AI Agent Definition
- `2603.00822` ContextCov
- `2603.20380` ALARA
- `2504.11703` Progent
- `2603.23806` AgentPex
- `2603.29848` AgentFixer
- `2602.13855` Claim-Level Auditability
- `2601.04748` Single-Agent With Skills
- `2512.19769` Declarative workflow DSL
- `2512.18940` FASTRIC
