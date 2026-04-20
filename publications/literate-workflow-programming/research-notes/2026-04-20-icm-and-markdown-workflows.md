# Workflow System Research Memo - ICM, Skills, Harnesses, and the Repo

Date: 2026-04-20

Status: research and brainstorming surface, not a strategy update.

## Intake Done

The paper `2603.16021v2.pdf` was moved into this package's evidence surface:

- PDF: [`../papers/2603.16021v2.pdf`](../papers/2603.16021v2.pdf)
- Markdown: [`../papers/markdown/2603.16021v2.md`](../papers/markdown/2603.16021v2.md)
- Index: [`../papers/index.md`](../papers/index.md)

The markdown conversion is readable. It has normal PDF extraction noise around page headers and tables, but the argument, limitations, future directions, and references are usable.

One metadata wrinkle matters. The local v2 PDF calls the protocol `Interpretable Context Methodology` (`ICM`), while the alphaXiv abstract still refers to `Model Workspace Protocol` (`MWP`). For this memo, treat `ICM` as the canonical name because that is what the local PDF and title use.

## Research Question

The immediate question is not whether this repo should copy ICM. The useful question is sharper:

Can this repo turn its existing workflow docs, skill bundles, lifecycle manifests, harness contract, policy file, and reviewable-run logs into a harness-native workflow system without falling into the two traps the literature keeps exposing: passive context bloat and unenforced natural-language control?

That question sits exactly between the new ICM paper and the earlier `illusion-of-swarm` essay.

ICM says a folder can replace a framework for sequential, human-reviewed workflows. `illusion-of-swarm` says many same-model multi-agent systems are expensive coordination scaffolds that can collapse into a single agent plus skills until skill selection becomes too crowded or ambiguous. This repo is already living inside that tension. It is mostly a single-agent-plus-skills operating environment, but it has enough workflows, stages, docs, and operational surfaces that the real risk is no longer lack of structure. The risk is semantic overload.

## alphaXiv Work

I used alphaXiv deterministic retrieval first, then assistant synthesis.

Deterministic retrieval included:

- `2603.16021` - Interpretable Context Methodology: Folder Structure as Agentic Architecture
- `2603.05344` - Building Effective AI Coding Agents for the Terminal
- `2512.05470` - Everything is Context: Agentic File System Abstraction for Context Engineering
- `2602.20478` - Codified Context: Infrastructure for AI Agents in a Complex Codebase
- `2603.25723` - Natural-Language Agent Harnesses
- `2603.20380` - ALARA for Agents
- `2602.11988` - Evaluating AGENTS.md
- `2604.08224` - Externalization in LLM Agents
- `2601.04748` - When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail
- `2504.11703` - Progent: Programmable Privilege Control for LLM Agents
- `2505.20127` - Agentic AI Process Observability
- `2508.02736` - AgentSight
- `2604.05278` - Spec Kit Agents
- `2601.20404` - On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents
- `2511.12884` - Agent READMEs
- `2603.00822` - ContextCov
- `2604.03088` - SkVM

The first alphaXiv assistant call only returned a retrieval trace. A long follow-up timed out. I then switched to shorter streamed assistant passes. The useful assistant synthesis argued that ICM validates filesystem/context externalization, but that this repo should not trust passive markdown contracts by themselves. The assistant especially pushed four tensions: AGENTS.md files can hurt or help depending on minimality, ICM lacks structural least-privilege enforcement, fixed stage scoping may need runtime validation, and reviewable logs should evolve toward semantic debugging rather than just execution receipts.

Assistant sessions created for the ICM paper:

- `019dabcb-1fff-7d63-b509-f3ecf087b2ac` - Robust autonomy workflow design
- `019dabc9-1e0e-72e1-8d5f-9c19b676fd14` - ICM Folder vs Framework
- `019dabc8-7190-7403-9a1e-22e00ca2e2e3` - ICM vs. Prod Agent Repo
- `019dabc6-5b80-7537-bb7b-ce33954cc023` - Agent harness design test

Distilled discussion note: [`alphaxiv-discussions/019dabc6-019dabcb-icm-workflow-cluster.md`](alphaxiv-discussions/019dabc6-019dabcb-icm-workflow-cluster.md)

## The ICM Claim

ICM's central move is simple and useful. A sequential workflow does not always need an orchestration framework. If each stage has a folder, a contract, inputs, outputs, reference material, and a human review boundary, the filesystem can carry much of the control logic. One model can read different context at each stage instead of different agents coordinating through a framework.

The paper's five design principles map cleanly onto this repo:

- one stage, one job
- plain text as the interface
- layered context loading
- every intermediate output as an edit surface
- configure the factory, not the product

The paper's future-work section is even more important than its current protocol. It identifies three missing pieces: incremental compilation, semantic debugging, and source integrity. Those are exactly where this repo's workflow system should probably go next. The current repo already has the beginnings of incremental compilation through lifecycle stages and package-local artifacts. It has the beginnings of semantic debugging through reviewable-run logs. It has the beginnings of source integrity through tracked workflow docs and skill bundles. But those pieces are not yet connected into a strong control layer.

## Where This Repo Already Goes Beyond ICM

ICM is a workspace pattern. This repo is closer to a lifecycle operating system.

The important difference is that this repo already separates several layers that ICM leaves informal:

- `workflows/` defines shared process.
- `workflows/skills/` defines execution help.
- `scripts/` provides stable command surfaces.
- `status.yaml` records package lifecycle state.
- `harness_contract.yaml` gives a machine-readable operating surface.
- `harness_policy.yaml` defines approval and mutation boundaries.
- `reviewable-runs/logs/` records bounded runs.
- package READMEs define local navigation.
- `papers/` and `papers/markdown/` preserve evidence.

That means the repo is not merely using folders as prompts. It is already compiling folder/doc conventions into machine-resolvable launch packs and lifecycle decisions. ICM stops at "the workspace is a folder." The repo has already moved toward "the workspace is a folder plus a contract plus a policy plus logs plus validators."

That is the productizable part.

The strategic plan says the repo is moving from content environment to harness-native system. The ICM paper supports that direction, but it also shows why Phase 1.5 cannot close on documentation alone. A folder hierarchy can orient a human and guide a strong model. It does not guarantee that a weaker model, a different harness, or a long-running agent will obey the intended boundary.

## The Layer Mapping

ICM's five layers can be mapped onto the repo, but not one-to-one:

| ICM layer | ICM meaning | Repo analogue | Gap |
| :--- | :--- | :--- | :--- |
| Layer 0 | global identity | `AGENTS.md`, root `README.md`, `harness_contract.yaml` | Too much local operator policy still lives in prose rather than executable checks. |
| Layer 1 | workspace routing | package READMEs, `status.yaml`, `stage:next`, `stage:resolve` | Routing is mostly publication-package oriented; workflow/framework packages like `phased-strategy/` are outside the manifest system. |
| Layer 2 | stage contract | workflow frontmatter, `required_context`, `expected_outputs`, `done_when`, launch packs | Contracts do not yet declare context budgets, allowed tools, context hashes, or verification clauses. |
| Layer 3 | reference material | workflow docs, skill bundles, voice guide, templates, package plans | Reference surfaces can be too broad. They are selected by convention more than by enforced scope. |
| Layer 4 | working artifacts | drafts, papers, markdown conversions, artifacts, logs, packets | Artifacts exist, but provenance between source context and output is still thin. |

The most useful takeaway is that the repo should not copy ICM's exact folder shape. It should use ICM as a vocabulary for making the existing harness contract stricter.

## Contradiction With `illusion-of-swarm`

`illusion-of-swarm` argued that many multi-agent systems are workarounds for routing, state, and coordination limits. The anchor paper `2601.04748` showed that some multi-agent setups can be collapsed into a single agent with skills, but skill selection can break around a semantic-confusion threshold.

ICM looks like the friendly version of that thesis. It says: do not build a framework or a swarm when a staged filesystem can guide one agent through different roles.

But ICM also makes the `illusion-of-swarm` warning more urgent. If every stage contract, workflow doc, skill file, voice guide, paper index, package README, and AGENTS instruction becomes part of the available action space, a single agent can drown in a different way. The system no longer has agent chatter overhead. It has context-routing overhead.

The better synthesis:

A workflow is a namespace.

That sentence is the direct bridge between the two projects. In `illusion-of-swarm`, "agent" often meant namespace: a boundary that prevents tool and role confusion. In this repo, workflow stages and skills are becoming namespaces. The question is whether those namespaces remain crisp enough for a single agent to route through them without confusion.

If the repo keeps growing by adding more passive markdown, it recreates the same semantic-confusability problem that multi-agent systems tried to escape. If it turns workflow docs into compact contracts with executable guardrails, it becomes a credible single-agent-plus-skills system rather than a filesystem-shaped prompt pile.

## Contradictions And Failure Modes

### 1. Context Files Are Not Automatically Good

`2602.11988` reports that repository-level context files can reduce task success and increase inference cost when they add unnecessary requirements. `2601.20404` points the other way, reporting lower median runtime and lower output-token consumption with AGENTS.md in a PR workflow. `2511.12884` shows why both can be true: agent context files are evolving configuration code, but they often emphasize functional guidance while under-specifying security and performance.

The local implication is not "delete AGENTS.md." It is "treat AGENTS.md and skill files as load-bearing configuration code." They need minimality, ownership, drift control, and ideally executable checks for the instructions that matter.

### 2. Passive Markdown Contracts Do Not Enforce Boundaries

ICM's stage contract tells the model what to load and what to output. ALARA and Progent expose the missing enforcement layer. Tool access, context access, and mutation rights should not be suggestions inside prose. They should be declared and enforced outside the model.

This matters for the repo because `harness_policy.yaml` is already a start, but the stage contracts do not yet have per-stage `allowed_tools`, `allowed_paths`, `context_budget`, or `required_context_layers` fields. Today, a stage can say what context it needs. It does not strictly deny everything else.

### 3. Static Stage Scoping May Be Too Rigid

ICM assumes the right context can be pre-partitioned into stage folders. Terminal-agent work such as `2603.05344` points to a different pattern: lazy tool discovery, adaptive context compaction, model routing, and event-driven reminders. That literature treats context as a runtime resource, not only a folder shape.

The repo should not jump straight to adaptive compaction. It should first make context selection explicit and measurable. Static scoping is a good baseline. It becomes a problem only when the system cannot tell whether a stage loaded too much, too little, or the wrong thing.

### 4. Observability Is Not Traceability

ICM's claim that every intermediate file is inspectable is true but incomplete. Opening a file tells you what exists now. It does not tell you which instruction, source file, context snapshot, model run, or tool action produced a specific sentence.

Reviewable Runs already solves part of that problem. But current lightweight logs record command boundaries, evidence, and verification more than semantic provenance. They are operational receipts. The next step is to make them source maps.

### 5. Human Review Gates Do Not Transfer Directly To Harness Autonomy

ICM is strongest when a human reviews output after every stage. Phase 1.5 asks something harder: can a harness choose the next valid action, execute bounded work, and leave a reviewable record with minimal prompt glue?

For that, "the human can edit this output" is not enough. The stage needs validators, stop conditions, proof criteria, and escalation rules. This repo has those ideas in workflow frontmatter and reviewable-run templates, but they are still uneven across guided stages.

### 6. Model-Agnostic Claims Need Skill Portability Work

ICM says the protocol is model-agnostic because it is just files and markdown. SkVM pushes against that. Skills behave differently across model and harness pairs. A skill is not just text; it is text plus runtime semantics plus model capability.

The repo-local skill layer should be treated as source code for agents. That implies compatibility checks, capability assumptions, and perhaps generated skill docs from the harness contract rather than hand-maintained instruction bundles.

### 7. Reviewable Logs Can Become Paperwork

Reviewable Runs is one of the repo's best answers to ICM's traceability gap. It can also become a bureaucratic layer if every routine action produces too much ceremony.

The current split between lightweight logs and retained proofs is right. The research angle is to keep logs minimal while adding the missing provenance fields that make them debuggable. Do not promote every run. Make the routine log more useful.

### 8. Workflow/Framework Packages Need Their Own Harness Surface

`phased-strategy/` is not under `publications/`, so the current package lifecycle scripts do not see it as a stage-driven package. That is correct in the current repo model, but it becomes a strategic limitation if workflow/framework packages are where the operating system evolves.

The research question: should workflow/framework packages get a lighter manifest type, separate from publication `status.yaml`, so the harness can reason about strategic and infrastructure packages without forcing them into the essay lifecycle?

## Candidate Angles For Later Writing

### Angle A: The Folder Is Not The Architecture

ICM's cleanest line is that the workspace is a folder. For this repo, that is no longer enough. The real architecture is the relationship between folder, contract, policy, validator, and run record. A folder gives the model somewhere to look. A harness contract tells it what looking means.

This could become the main thesis if we write about the workflow system as a product primitive.

### Angle B: Context Is A Liability Until It Is Scoped

The AGENTS.md papers make the context-engineering story less comfortable. More context can improve runtime and reduce wasted output in some PR workflows, but it can also lower task success when it adds unnecessary obligations. That means context should be treated like permissions: grant the minimum necessary to finish this stage.

This is the ALARA principle applied to writing and publishing workflows.

### Angle C: Reviewable Runs As Semantic Debuggers

ICM identifies semantic debugging as future work. This repo already has a reviewable-run layer that could become that debugger. The missing mechanism is provenance: source context hashes, parent artifact IDs, stage contract versions, and verification records that connect a flawed output back to the source material or instruction that likely caused it.

This is probably the strongest internal product angle.

### Angle D: A Workflow Is A Namespace

The earlier multi-agent essay argued that agents often act as namespaces. This repo suggests a stronger replacement: workflows, stages, and skills can provide the namespace without creating new agent personas. That is the practical synthesis between ICM and `illusion-of-swarm`.

The risk is namespace sprawl. Too many overlapping workflow docs and skill files recreate the same disambiguation failure under a different name.

### Angle E: From Human Gates To Validation Gates

ICM is a human-in-the-loop method. This repo wants harness-native autonomy. The bridge is not removing humans; it is converting some human gates into explicit validation gates. A stage should know when it is allowed to stop, when it must escalate, and what evidence it must leave behind.

This angle is useful for Phase 1.5 proof-run design.

### Angle F: Skills Are Code, Not Prompt Snippets

SkVM and ContextCov both point in this direction. Skills and instruction files should be parsed, checked, versioned, and measured. Treating them as prose is convenient but unstable. Treating them as code opens the path to compatibility checks, generated docs, and execution profiles.

This could drive Phase 1.6 generated skill docs.

### Angle G: Productization Is The Loss Of Informality

ICM's appeal is informality: anyone can edit a folder. SaaS/product-readiness requires some of that informality to disappear. The product question is not how to preserve every bit of local flexibility. It is which parts of the local system become durable contracts and which remain operator judgment.

That angle directly challenges the current strategic plan and may be useful before Phase 2.

### Angle H: Edit The Source, Not The Output

ICM's source-integrity section says recurring output edits should flow back into source-level changes. The repo already does this manually through voice guides, workflow docs, and skills. The future version would log repeated correction patterns and suggest source changes only after enough evidence accumulates.

Do not automate this yet. Build provenance first.

## Concrete Workflow-System Implications

### 1. Add Per-Stage Capability Fields

Current workflow frontmatter has `required_context`, `expected_outputs`, `done_when`, `approval_gate`, `runner_mode`, and related launch data. Add fields like these later, after a design pass:

```yaml
context_layers:
  required: [0, 1, 2, 3, 4]
  denied: []
allowed_paths:
  - workflows/alphaxiv-research/README.md
  - publications/{package}/papers/
allowed_tools:
  - alphaxiv.search
  - alphaxiv.paper
context_budget_tokens: 8000
verify:
  - name: source_index_updated
    command: ...
```

The point is not to create a heavy framework. The point is to let the harness deny undeclared context and undeclared tools before the model sees them.

### 2. Add Context Snapshots To Launch Packs And Logs

Each launch pack and lifecycle log should eventually include:

- context file paths
- content hashes
- workflow contract version or hash
- skill file version or hash
- status.yaml before/after hash
- parent artifact IDs when a stage consumes previous output

This is the minimum step toward semantic debugging.

### 3. Convert Some Prose Rules Into Executable Checks

ContextCov is the relevant model. Not every instruction deserves a check, but some do:

- do not mutate external systems without approval
- do not force-add hidden folders
- do not overwrite live drafts before promotion
- do not mark certain guided stages done without review
- do not publish or distribute without approval

Some of these are already policy or prompt rules. The next step is enforcement where feasible.

### 4. Create A Context Minimality Review

Before adding more local skills or AGENTS instructions, run a small review:

- Which instruction is needed on almost every task?
- Which instruction belongs in a stage contract instead?
- Which instruction belongs in a skill file instead?
- Which instruction can be enforced by a script instead of told to the model?
- Which instruction is obsolete or duplicative?

This is the most direct response to the mixed AGENTS.md evidence.

### 5. Treat Reviewable Runs As The Phase 1.5 Debugger

The proof-run template already tracks prompt glue, repo-discovery failures, approval-boundary behavior, and invented artifacts. Add a companion "context trace" view before building any dashboard. A CLI-readable JSON surface is enough.

Do not build a UI yet. The research points to better trace primitives, not a prettier inspection layer.

### 6. Add A Workflow/Framework Manifest Type

Publication packages have `status.yaml`. Workflow/framework packages currently do not. `phased-strategy/`, `workflows/`, and `reviewable-runs/` may need a lighter manifest if the harness is expected to operate on them as first-class system components.

Possible fields:

```yaml
kind: workflow_framework
surface: phased-strategy
owned_artifacts:
  - strategic_plan.md
  - phase-1-1-5-closure-checklist.md
  - papers/
current_questions:
  - Phase 1.5 proof-run closure
  - operator-shell design
  - workflow/skill productization
```

This should remain separate from publication lifecycle stages.

### 7. Design A Proof Run Around This Memo

This task itself is close to a Phase 1.5 research-heavy proof run, except the prompt included a lot of repo-specific instruction from the user. A later proof should ask a fresh harness to start from the tracked contract and this memo, then propose and implement one narrow workflow-system improvement.

The scoring question should be: did the harness discover the right surfaces without bespoke explanation?

### 8. Do Not Build These Yet

Do not build adaptive context compression yet. Load less first.

Do not build an operator dashboard yet. Improve logs and traceability first.

Do not build automatic source rewriting from human edits yet. Provenance has to exist first.

Do not flatten every workflow into ICM-style numbered folders. The repo already has a stronger package/workflow/script/skill separation.

Do not treat natural-language harnesses as proof that plain English is enough. The useful direction is natural language plus executable runtime contracts.

## Source Shortlist

### Anchor

- `2603.16021` - Validates filesystem and markdown as serious orchestration surfaces for sequential, human-reviewed workflows. Its limitations and future-work sections are the most useful parts for this repo.

### Direct repo parallels

- `2603.25723` - Natural-language harnesses. Supports the idea that harness logic can be portable and editable, but only when paired with explicit contracts, durable artifacts, and a runtime.
- `2603.05344` - Terminal agents. Supports terminal-native harnesses, lazy tool discovery, context compaction, memory, and event-driven reminders.
- `2512.05470` - Agentic filesystem abstraction. Supports persistent, governed context artifacts rather than transient prompt assembly.
- `2602.20478` - Codified context. Useful for hot/cold memory distinctions and project-specific conventions across sessions.
- `2604.05278` - Spec Kit Agents. Good support for phase-level context-grounding hooks and validation hooks.

### Contradictory pressure

- `2602.11988` - Context files can reduce success and increase cost when they add unnecessary requirements.
- `2601.20404` - AGENTS.md can reduce runtime and output tokens in PR workflows, complicating any simple anti-context conclusion.
- `2511.12884` - Agent context files behave like evolving configuration code and tend to under-specify non-functional guardrails.
- `2603.20380` - ALARA makes least-privilege context/tool scoping explicit.
- `2504.11703` - Progent supports deterministic privilege control around tools.
- `2603.00822` - ContextCov supports turning passive instructions into executable constraints.

### Observability and provenance

- `2505.20127` - Process observability for behavioral variability.
- `2508.02736` - AgentSight supports bridging high-level intent and low-level effects.
- `2603.16021` Section 6 - Semantic debugging, source maps, and source integrity.

### Skills and single-agent frame

- `2601.04748` - Single-agent-with-skills can replace some multi-agent systems, but skill selection hits semantic capacity limits.
- `2604.03088` - SkVM treats skills as code across heterogeneous models and harnesses, which challenges the idea that skills are portable raw markdown.
- `2604.08224` - Externalization review frames memory, skills, protocols, and harnesses as external cognitive infrastructure.

## Strongest Working Thesis

This repo should treat ICM as evidence that filesystem structure is a legitimate agentic architecture, but not as evidence that folders and markdown are enough. The repo's real product primitive is stricter: a workflow is a namespace, a skill is executable context, and a reviewable run is the debugger.

The next phase should therefore be less about adding more docs and more about compiling the docs that matter into enforceable context, tool, validation, and provenance contracts.

## Questions To Review Later

1. Should `phased-strategy/`, `workflows/`, and `reviewable-runs/` gain a lightweight framework manifest, separate from publication `status.yaml`?
2. Which workflow frontmatter fields are worth adding first: `allowed_tools`, `allowed_paths`, `context_budget_tokens`, `verify`, or context hashes?
3. Should `check:harness` validate not only contract shape but also instruction minimality and duplicate context surfaces?
4. Can reviewable-run logs become useful semantic source maps without becoming heavy proof packets?
5. Which local instructions in `AGENTS.md` belong in executable policy instead of prose?
6. What is the smallest proof run that would test whether a harness can improve the workflow system from tracked context alone?
7. Does Phase 1.6 need generated skill docs first, or per-stage least-privilege manifests first?
8. Should the repo explicitly frame workflows as namespaces in the strategic plan?
