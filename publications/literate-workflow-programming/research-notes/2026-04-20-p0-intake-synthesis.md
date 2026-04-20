# P0 Intake Synthesis: Workflow Docs As Source, Logs As Trace

Date: 2026-04-20

Package: `publications/literate-workflow-programming/`

alphaXiv discussion: [`alphaxiv-discussions/019dac7e-literate-workflow-thesis-test.md`](alphaxiv-discussions/019dac7e-literate-workflow-thesis-test.md)

## Scope

This note summarizes the first deliberate intake batch for the package. The batch keeps the ICM anchor and adds the P0 papers from the index:

- `2603.25723` Natural-Language Agent Harnesses
- `2604.13346` AgentSPEX
- `2603.17399` Bootstrapping Coding Agents
- `2603.08806` Test-Driven AI Agent Definition
- `2603.00822` ContextCov
- `2604.03088` SkVM

The purpose is not to draft the article yet. It is to decide what vocabulary survives first contact with the literature and what repo experiment should come next.

## What The Batch Supports

The strongest version of the thesis is not "markdown is magic" and not "logs are the new source code." The defensible claim is narrower:

> Human-readable workflow specifications are becoming source artifacts for agent systems when they are structured enough to be interpreted, compiled, validated, replayed, or checked against runtime traces.

That frame is supported by the batch:

- ICM supports the filesystem/markdown side: folders route stage context, markdown carries stage contracts, and layered loading keeps context scoped.
- Natural-Language Agent Harnesses supports externalized harness logic: high-level control can live outside controller code when a runtime executes it through contracts, durable artifacts, and adapters.
- AgentSPEX supports the language/runtime side: workflow definitions can have typed steps, branching, loops, reusable submodules, explicit state, explicit context management, checkpointing, replay, and logging.
- ContextCov supports enforcement: passive agent instruction files can be transformed into executable guardrails, runtime command checks, and architectural validators.
- TDAD supports testing: behavioral specifications can compile into tests, prompt artifacts, regression checks, and semantic mutation tests.
- SkVM supports skills-as-code: skills need compilation/runtime machinery across model and harness targets instead of being dumped into context as raw markdown.
- Bootstrapping Coding Agents supports the strongest source-of-truth claim: the specification is the stable artifact, while implementations can be regenerated.

## What The Batch Narrows Or Contradicts

The phrase "literate workflow programming" is promising but risky. The literature supports structured natural-language specifications, declarative workflow languages, executable harnesses, validators, and skill runtimes. It does not yet prove that ordinary markdown notes form a programming language.

Three corrections follow:

1. The source of truth should be the spec, not the run log.
2. Reviewable logs matter as traces, source maps, and debugging surfaces, not as primary source.
3. Skills and imports need a compilation/binding story before they can be treated as production-ready runtime substrate.

The import idea remains under-supported by the P0 batch. ICM has layered context loading and path-based structure. AgentSPEX has reusable workflow calls. SkVM has capability binding. None of them gives a clean markdown import mechanism. That means imports should be treated as an experiment, not a proven design.

Package state is also under-theorized in this batch. AgentSPEX and SkVM discuss runtime state, checkpointing, environment binding, and execution artifacts, but not the package-as-object idea directly. We can keep the object metaphor internally, but it needs stronger evidence or a repo-native experiment.

## Vocabulary To Use For Now

Prefer:

- `workflow specification`
- `agent harness`
- `stage contract`
- `context layer`
- `capability binding`
- `validator`
- `runtime trace`
- `source map`
- `spec drift`
- `semantic debugging`

Use with caution:

- `literate programming`
- `markdown programming language`
- `imports`
- `package object`
- `compiler`

The safer article frame is:

> Agent workflow systems are converging on a software-engineering stack for natural-language specifications: source files, modules, context loading, validators, runtimes, traces, and drift checks.

The bolder article frame is:

> Markdown is becoming a literate programming surface for agent workflows.

The bolder version is only defensible if our repo demonstrates that prose-heavy markdown specs can be compiled, checked, and traced.

## Reviewable Runs Angle

The user's sentence still holds:

> reviewable logs should evolve toward semantic debugging rather than just execution receipts

The P0 batch sharpens it:

- From AgentSPEX: logs/checkpoints/replay are part of workflow runtime design.
- From NLAH: durable artifacts make harness behavior studyable and comparable.
- From ContextCov: violations should be detected against declared constraints.
- From TDAD: regressions should be tested against behavioral specifications.
- From Bootstrapping: the spec remains primary; the log proves what happened relative to the spec.

So a reviewable run should not merely say "these commands ran." It should answer:

- Which source spec/stage contract was active?
- Which imports/context layers were resolved?
- Which validators applied?
- Which outputs were produced?
- Where did actual behavior drift from expected behavior?
- Which trace entries map back to which source clauses?

That is the semantic-debugging direction.

## Recommended Repo Experiment

The next experiment should be `spec-diff` for one real workflow, probably paper intake or alphaxiv research.

Minimal version:

1. Compile the workflow doc plus package status into an expected-state manifest.
2. Record the actual run as a reviewable-run trace.
3. Compare expected state to actual state.
4. Report drift as source-linked findings.

Example expected-state manifest fields:

- package path
- stage name
- workflow doc path
- default skill path
- required context paths
- resolved imports or context layers
- expected output paths
- validator commands
- done-when checks

Example drift findings:

- required context missing
- output produced outside the declared evidence surface
- paper index entry points to a missing file
- converted markdown exists without source PDF
- launch pack exists but final run log missing
- validator command failed or was skipped

This experiment gives the package an empirical spine. It directly tests whether workflow specs, indexes, validators, and reviewable logs form a source-and-trace system rather than a metaphor.

## Near-Term Research Tasks

1. Read the P0 batch in detail and extract exact claims into `claim-ledger.md`.
2. Intake P1 only after the `spec-diff` experiment is sketched, so the next literature batch can answer a sharper question.
3. Keep "imports" parked as a prototype idea until we can state whether imports are path includes, semantic dependencies, capability bindings, or runtime links.
4. Keep the phased strategy insulated. Extract only the `spec-diff` experiment back into `phased-strategy/` if it changes proof-run requirements.
