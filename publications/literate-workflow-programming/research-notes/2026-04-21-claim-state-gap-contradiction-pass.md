# Claim-State Gap And Contradiction Pass

Date: 2026-04-21

Status: targeted research pass, not paper intake.

## Purpose

This pass pushed the Claim-State Authorization system after the first contradiction register and scorecard were created.

The question was not whether to reopen the article lead. The lead still holds:

Agent workflow specs become meaningful source only when coupled to validation gates, policy enforcement, and semantic debugging traces.

The useful question was narrower: which current claims gain support, which claims need caveats, and which contradictions should be made explicit before drafting?

## alphaXiv Work

I used deterministic alphaXiv retrieval first, then smaller assistant sessions to pressure-test contradiction clusters.

Deterministic retrieval covered the existing P2 queue:

- `2603.05344` - Building Effective AI Coding Agents for the Terminal
- `2512.05470` - Everything is Context
- `2602.20478` - Codified Context
- `2604.08224` - Externalization in LLM Agents
- `2604.05278` - Spec Kit Agents
- `2505.20127` - Agentic AI Process Observability
- `2508.02736` - AgentSight
- `2602.11988` - Evaluating AGENTS.md
- `2601.20404` - On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents
- `2511.12884` - Agent READMEs
- `2508.11126` - AI Agentic Programming

The broad assistant pass fetched the relevant abstracts but timed out before producing a useful synthesis. I then split the work into smaller cluster passes:

- Context-file contradiction: `2602.11988`, `2601.20404`, `2511.12884`, `2603.20380`, `2603.00822`
- Observability and provenance: `2505.20127`, `2508.02736`, `2512.18940`, `2603.16021`
- Skills and externalization: `2604.03088`, `2601.04748`, `2604.08224`, `2603.05344`

After the package update, I attempted one more fresh assistant audit of the extracted delta. The first retry failed because the browser-backed token expired during synthesis, and a temporary API-key-only run was rejected by alphaXiv for assistant writes. After a browser-login refresh, the audit finally returned, but it introduced claims that were not supported by the retrieved paper summaries, including an `attention-sink` framing for `2601.20404`, a `semantic source maps` reading of `2602.11988`, and a `namespace control is solved` reading of `2604.03088`. Treat that final sanity check as adversarial pressure, not as adopted synthesis.

The local extraction is tracked in [`alphaxiv-discussions/019db0b1-019db0b4-claim-state-gap-pass.md`](alphaxiv-discussions/019db0b1-019db0b4-claim-state-gap-pass.md).

## Search Sweep

After the cluster passes, I ran deterministic search queries for nearby gaps. The sweep found several candidates worth adding to the intake queue:

| Paper | Why It Matters |
| :--- | :--- |
| `2603.23806` AgentPex / Willful Disobedience | Direct trace-compliance evidence: extracts behavioral rules from prompts and evaluates agentic traces for procedural failures. |
| `2603.29848` AgentFixer | Failure detection and fix recommendation for agentic systems; trace comparison improves localization over failed-trace-only analysis. |
| `2603.08993` Arbiter | System-prompt interference detector; directly relevant to contradiction, redundancy, and ambiguity inside prompt/control surfaces. |
| `2604.13108` Formal Architecture Descriptors | Architecture descriptors reduce agent navigation overhead; useful pressure on whether markdown/JSON/YAML formats matter less than formal navigational structure. |
| `2602.12670` SkillsBench | Curated skills improve agent performance, but benefits vary by model/task configuration. |
| `2604.01687` CoEvoSkills | Self-evolved skills may outperform human-curated skills when verified, complicating any simple "raw markdown skills fail" claim. |
| `2411.13768` Evaluation-Driven Development and Operations of LLM Agents | Continuous evaluation loop for agent systems; supports validation as a lifecycle mechanism rather than a one-time check. |
| `2602.13855` Claim-Level Auditability | Semantic provenance graphs for claim-evidence links; useful for contradiction state and trace state in research agents. |

These are queue additions, not ingested evidence. Do not treat them as body citations until paper intake is complete.

## Findings

### 1. Context-File Utility Is Metric-Dependent

The existing claim that context files are useful only when scoped, minimal, and enforceable is directionally right, but too flat.

`2602.11988` reports that repository-level context files can reduce task success and raise cost. `2601.20404` reports that AGENTS.md files can reduce output tokens and completion time. `2511.12884` explains why both can be true: agent context files behave like living configuration, but readability and non-functional requirements remain weak.

Resolution rule:

Context-file utility depends on task risk and metric. For low-risk PR-flow efficiency, context files may help even before strict enforcement. For correctness-critical, safety-critical, or policy-sensitive work, the stricter rule activates: minimal scope, provenance, validation, and enforceable constraints.

Package effect:

Add a new contradiction-register entry for metric/task split. Do not claim AGENTS.md-style context is globally helpful or globally harmful.

### 2. Formality Does Not Monotonically Improve Conformance

FASTRIC is stronger than a generic trace paper because it measures procedural conformance against prompt-protocol specifications. But it also warns against a naive "more formal is always better" story. Its results show model-specific formality ranges, including a collapse at the highest formality level for one large model.

This matters for `spec-diff`.

Resolution rule:

`spec-diff` should be framed as a bounded source/evidence drift proof candidate, not as proof that more formal workflow specs automatically improve agent behavior. Conformance failures should route to semantic debugging rather than being treated as simple pass/fail verdicts.

Package effect:

Add a contradiction-register entry for specification formality vs conformance. Keep `spec-diff` article-ready only for the narrower evidence-surface drift claim.

### 3. Observability Strengthens Trace Claims But Does Not Replace Provenance

Agentic process observability and AgentSight strengthen the need for traces that connect high-level intent to low-level effects. AgentPex and AgentFixer add a more direct path: traces can be checked for rule compliance, failure localization, and fix recommendations.

The gap is integration. The papers describe pieces of a debugging stack. They do not prove that this repo's current reviewable-run logs already provide semantic provenance.

Resolution rule:

Reviewable Runs can be called traces and proof surfaces. They cannot yet be called full semantic source maps unless they record source context, contract version, validation result, contradiction state, and output provenance.

Package effect:

CSA-C2 remains article-ready. CSA-C5 remains article-ready only for local drift detection. CSA-C6 stays caveated until the provenance layer exists.

### 4. Skills Work, But Skill Systems Fail Differently Than Markdown Docs

SkVM and Single-Agent With Skills support the current caveat: raw markdown skills are not portable production substrate. The search sweep complicates the claim in a useful way. SkillsBench says curated skills can substantially improve performance. CoEvoSkills suggests verified self-evolved skills may outperform human-curated skills.

The problem is not "skills do not work." The problem is that skills become production substrate only when selection, capability binding, verification, and harness adaptation are handled explicitly.

Resolution rule:

Treat skills as a code-like substrate with two failure modes:

- portability failure across model/harness pairs
- selection failure when the skill namespace becomes too large or semantically confusable

Package effect:

CSA-C4 remains use-with-caveat. Add a contradiction-register entry for skill usefulness vs skill portability/selection limits.

### 5. Claim-Level Auditability Is A Strong Candidate For The Next Contradiction-State Upgrade

`2602.13855` is not intaken here, but it is strongly adjacent. It argues that claim-level auditability requires semantic provenance linking claims to evidence, not just fluent output or action logs.

This is a better next-paper candidate for CSA-C6 than a broad observability survey because it speaks directly to claims, evidence, and provenance.

Resolution rule:

Do not promote contradiction state as a completed local capability. Promote it as the next semantic-debugging requirement, with claim-level auditability as the most relevant candidate evidence.

## Updated Claim Decisions

| Claim | Decision |
| :--- | :--- |
| CSA-C1 workflow specs need validation, policy, and traces | Stable. P2 supports the lead rather than reopening it. |
| CSA-C2 logs are traces, not source of truth | Strengthened. Observability papers support the need for trace interpretation. |
| CSA-C3 markdown workflow files need binding, validation, policy, provenance | Stable but more caveated. Context utility is task-risk and metric dependent. |
| CSA-C4 skills are code-like but raw markdown skills are not portable production substrate | Still caveated. New skill benchmark/evolution papers can strengthen the section after intake. |
| CSA-C5 `spec-diff` is a local source-linked drift proof candidate | Stable only in narrow form. Do not generalize it into broad conformance proof. |
| CSA-C6 contradiction state belongs in semantic debugging | Stronger as a next-step requirement, still not a completed local capability. |

## Next Intake Recommendation

Do not run a broad P2 intake. Run a focused P2a intake in this order:

1. `2602.11988`, `2601.20404`, `2511.12884` for the context-file metric split.
2. `2603.23806`, `2603.29848`, `2602.13855` for trace compliance, failure localization, and claim-level auditability.
3. `2602.12670`, `2604.01687` only if the article needs a stronger skills section.

Everything else can remain queued unless the draft asks for it.
