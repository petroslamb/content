# Claim Ledger

This ledger keeps the research package honest before any claim is promoted into an essay, workflow refactor, or phased-strategy update.

| Claim | Current Status | Evidence Surface | Caveat / Test |
| :--- | :--- | :--- | :--- |
| Markdown workflow docs, skills, indexes, imports, and logs may form a literate programming substrate for agent workflows. | Narrowed hypothesis | ICM, Natural-Language Agent Harnesses, AgentSPEX, TDAD, SkVM, ContextCov | The defensible claim is structured workflow specifications as source artifacts. "Literate programming" remains a stretch unless prose-heavy markdown can be compiled, checked, and traced. |
| The repo should treat packages as objects, workflows and skills as functions, policies/imports as declarative contracts, and reviewable runs as traces. | Working design frame | Local repo architecture, ICM, AgentSPEX, SkVM, P0 synthesis note | Useful as architecture vocabulary, but "package as object" is not directly established by the P0 literature. |
| Imports should start as declared dependencies, not automatic markdown concatenation. | Provisional design rule | ICM context layers, AgentSPEX workflow calls, SkVM capability binding | The P0 literature does not give a markdown import model. Treat imports as a repo experiment, not a paper-backed claim. |
| Reviewable Runs could evolve from execution receipts into source-map-like semantic debugging records. | Strong candidate experiment | ICM, Natural-Language Agent Harnesses, AgentSPEX, TDAD, ContextCov, P0 synthesis note | Logs should remain derived traces. The spec/stage contract should be the source of truth. Test with a `spec-diff` experiment. |
| Context files are useful only when scoped, minimal, and enforceable. | Strong candidate claim | `2602.11988`, `2601.20404`, `2511.12884`, ALARA, ContextCov | Evidence is mixed by task type; do not claim AGENTS.md-style files are universally good or bad. |
| "A workflow is a namespace" is the bridge from `illusion-of-swarm` to this package. | Author synthesis | `2601.04748`, ICM, local workflow system | Interpretation, not a direct paper claim. Needs careful wording. |
| The specification is primary and the run log is secondary. | Strong candidate claim | `2603.17399`, AgentSPEX, TDAD, ContextCov | Avoid letting reviewable-run enthusiasm invert the hierarchy. Logs should prove, debug, and map execution back to source. |
| Skills need compilation or capability binding before they are production substrate. | Strong candidate claim | SkVM, AgentSPEX, Natural-Language Agent Harnesses | This pressures the current raw-markdown skill model. The repo can still use markdown skills, but should not claim portability without a binding/validation layer. |
