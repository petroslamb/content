# Candidate Draft

This bounded candidate must remain a sibling to the live draft. Do not overwrite `publications/literate-workflow-programming/literate-workflow-programming-flagship/literate-workflow-programming.md`.

Packet manifest: `publications/literate-workflow-programming/literate-workflow-programming-flagship/iterations/r2/literate-workflow-programming-essay-iteration-packet-r2.json`
Current live draft: `publications/literate-workflow-programming/literate-workflow-programming-flagship/literate-workflow-programming.md`

# Literate Workflow Programming

Change one line in a workflow repo and the failure does not always appear where older software instincts expect it. The runtime still launches. The tools are still present. But a validator now reports that the package state, the governing brief, and the evidence surface no longer agree. The bug is not only in hidden implementation anymore. It lives in a human-readable workflow layer: the markdown contract, the package manifest, the policy surface, the staged handoff file. Once a system can interpret those artifacts, constrain behavior with them, and trace failures back to them, they stop being mere documentation. They start behaving like source.

That is the useful claim here, and it is narrower than the usual "markdown as code" slogan. The literature does not justify the fantasy that prose-heavy files magically became executable just because modern agent systems read them. What it does justify is sharper and more interesting. Workflow specifications become source-like when a runtime can load them, validators can test their consequences, policies can constrain their authority, and traces can show where execution diverged from the declared control surface. The important shift is not that markdown became a programming language. It is that a human-readable specification layer is becoming the stable object operators edit, inspect, review, and debug.

Several recent papers are converging on that layer from different directions. Interpretable Context Methodology organized agent behavior around staged markdown contracts, folder structure, and preserved intermediate artifacts. Natural-Language Agent Harnesses turned orchestration logic into editable natural-language contracts and adapters. AgentSPEX made the workflow surface more explicit still with typed steps, branching, reusable modules, state, and replay. Bootstrapping Coding Agents supplied the strongest correction: the artifact of record should be the specification, not the generated residue. Taken together, these systems do not prove that passive text executes itself. They show that once workflows are interpretable, inspectable, and replayable, the specification layer starts to look much less like commentary and much more like source.

The local `spec-diff` experiment in this repo is useful precisely because it stays small. It does not claim broad behavioral conformance or semantic equivalence. It checks something narrower and more revealing: whether declared package state still matches the evidence surface and governing artifacts it claims to control. When that drift becomes a source-linked finding, the lesson is hard to miss. The workflow surface matters because another layer can do something testable with it. That is also why validation and policy enforcement are the real hinge of this architecture. ContextCov extracts executable checks from instruction files. ALARA and Progent make context and tool authority part of an enforceable control layer. Test-Driven AI Agent Definition and AgentFixer widen the same pressure into regression logic, cross-stage checks, diagnosis, and iterative repair. Validation is not a trailing test pass here. It is the machinery that keeps an externalized specification from decaying into fiction.

Once that hinge is visible, the role of traces becomes easier to place. There is a strong temptation to treat logs as the deepest truth because they show exactly what happened. But traces become valuable only when the system still knows what should have happened. AgentPex is useful because it evaluates execution against source-derived rules. FASTRIC does similar work for prompt protocols and finite-state interaction procedures. These are good arguments for traces as semantic debugging surfaces. They are weaker arguments for traces as primary source. A run log can reveal that a workflow violated its own procedure. It cannot by itself tell you whether the procedure was well designed, well scoped, or the right object of authority in the first place.

The same bounded logic applies to skills. The literature is now strong enough to treat skills as more than decorative instructions, but not strong enough to pretend raw markdown skills are already portable substrate. AgentSPEX, SkVM, and the skills-as-code work all point toward externalized procedural units that can be selected, adapted, and composed. Single-Agent With Skills sharpens the limit at the same time. Skills only become reliable building blocks when a runtime can bind capabilities explicitly, govern selection, and check execution against something stronger than optimistic prose. So skills belong in this story, but only as a bounded support layer beside the source, validation, and trace stack.

That stack also clarifies what is still missing. Claim-Level Auditability is the strongest current signal that provenance has to mean more than file history or trace retention. A promoted claim should preserve whether evidence supports it, conflicts with it, or still leaves an unresolved gap. The current repo does not fully satisfy that bar, and pretending otherwise would weaken the essay. It has validators. It has traces. It has contradiction surfaces in some packages. It has bounded drift checks that compare declared state against observed package reality. Those are real pieces of a semantic debugging stack. They still fall short of claim-level provenance graphs, provenance coverage metrics, and contradiction-aware audit paths that survive across rewrites and promotions.

Seen from that angle, literate workflow programming becomes a usable name for a stack rather than a slogan for markdown maximalism. The literate part is that the human-readable specification layer remains central even as the system grows more operational. The programming part is that workflow behavior is increasingly shaped by inspectable source-like artifacts, bounded by validators and policies, and debugged through traces that still answer back to the specification layer. That category is real enough to study already. The stronger claims still need to wait. Passive markdown is not enough. Formality does not automatically improve behavior. Raw skills are not portable substrate just because they look modular. Reviewable runs are not yet full source maps. If we keep editing these workflow surfaces as if they were only notes when they already govern behavior, we will keep debugging the wrong layer.

## Limits

This draft does not claim that markdown alone is executable, that stricter formalization monotonically improves agent behavior, or that current Reviewable Runs already provide full claim-level provenance. It keeps package-as-object semantics, markdown import semantics, and repo-wide validator promotion parked. It also keeps the skills claim bounded: skills can be source-like workflow units, but current markdown skills are not being presented as already portable production substrate.

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
