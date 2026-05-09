# Reddit Discussion Lab

## Package

- Package: `evidence-governance/your-ai-is-confidently-wrong-and`
- Source essay or post: `publications/evidence-governance/your-ai-is-confidently-wrong-and/your-ai-is-confidently-wrong-and.md`
- Run id: `phase-2-8-proof-reddit-discussion-confidently-wrong`
- Current Reddit mode: `draft_hold`
- Last updated: `2026-05-09`

## Experiment Hypothesis

This run tests whether the essay's evidence-governance argument can become a Reddit-native operator discussion without requiring readers to accept the essay frame first. The best seed should start from a concrete contradiction inside an AI verification run, invite practitioners to describe how they resolve summary-versus-evidence conflicts, and avoid owned links or promotion language.

The run is proof evidence only. It does not approve posting, commenting, voting, lifecycle movement, or workflow promotion.

## Examples Consulted

| Example | Borrowed Mechanic | What To Avoid |
| :--- | :--- | :--- |
| `Two failure modes I caught in my AI lab in one day. Both involve the system silently lying about its own state.` | Start with a falsifiable incident where the system's reported state diverges from underlying evidence. | Do not lead with the coined frame `evidence governance`. |
| `AI is getting better at doing things, but still bad at deciding what to do?` | Put the contradiction in ordinary language so non-specialists can participate. | Do not over-explain the full hierarchy before the question. |
| `How do folks manage worktrees when working with multiple agents in parallel?` | Ask for lived workflow practice from people operating with agents. | Do not ask readers to endorse the publication thesis. |
| `open source AI assistants ranked by tool call reliability` | Make the evaluation surface concrete and challengeable. | Do not cite paper lists before readers know what practical problem is being discussed. |
| `what actually broke when you tried red teaming your AI systems?` | Ask for failure stories and debugging details instead of opinions. | Do not turn the post into a polished essay abstract. |

## Tone And Engagement Mechanics

- Title shape: plain operator question or concrete failure scene, not article headline.
- Participation invitation: readers can answer from their own agent, eval, QA, compliance, or code-review workflows.
- Useful tension: teams want AI-generated summaries because they save time, but the summary may be the least authoritative artifact when it conflicts with logs, CSVs, traces, tests, or citations.
- Voice target: short, casual, technically literate, no fake roughness, no Substack link in the body.
- Account-health note: no package-local Reddit ledger or account-health record was present for this package. Because current account health was not established in declared inputs, the run holds all drafts locally rather than selecting `post_now_native`.

## Essay Mining

| Essay Element | Reddit-Native Version | Notes |
| :--- | :--- | :--- |
| Coined frame | `evidence governance` becomes `what wins when the summary and evidence disagree?` | Use the frame only after the problem is visible. |
| Failure scene | AI verifier said all obligations were mapped, while its own locations pointed to an ABI wrapper, test file, and RPC helper rather than protocol logic. | Strongest concrete opening. |
| Operator pain | A polished AI narrative can silently override contradictory underlying data when no rule forces review of the receipts. | Broad enough for AI evals, agents, compliance, and code review. |
| Concrete distinction | Raw artifacts/logs/CSVs/traces should outrank validation docs, which should outrank generated summaries when tiers conflict. | One clear distinction; avoid full five-component pattern in the post. |
| Reader question | How are teams deciding which artifact wins when AI-generated summary and evidence disagree? | Answerable without reading the essay. |
| Follow-up angle | Making wrongness findable may matter more than improving headline accuracy for production workflows. | Useful for comments if thread asks for more detail. |

## Title Candidates

| Candidate | Problem Concreteness | Answerability | Subreddit Fit | Tension | Native Voice | Decision |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `my AI verifier said everything was mapped, but its own evidence pointed at the wrong files. what should win?` | 3 | 3 | 3 | 3 | 3 | Strong draft, hold for account-health check |
| `when an AI summary disagrees with its own logs, do you trust the summary, the logs, or neither?` | 3 | 3 | 3 | 3 | 3 | Strong draft, broadest fit |
| `are teams writing rules for AI-generated evidence, or just trusting the cleanest-looking summary?` | 2 | 3 | 2 | 3 | 2 | Revise toward a more concrete incident |
| `what is your rule when an agent says done but the underlying artifacts say maybe not?` | 3 | 3 | 3 | 3 | 3 | Good comment-first or post seed |
| `is making AI wrongness findable more important than making the model right slightly more often?` | 2 | 3 | 2 | 3 | 2 | Hold; more thesis-like |
| `where do you keep the receipts for AI-generated analysis?` | 2 | 3 | 2 | 2 | 3 | Useful short title, needs sharper body |

## Scored Drafts

Rubric axes: problem concreteness, answerability, subreddit fit, tension, distinction value, native voice, link risk. Each axis is scored 0-3.

### Draft A

Target community: `r/LLMDevs` or another practitioner community focused on agent/eval workflows.

Score: 21/21

Decision: `draft_hold`

```text
my AI verifier said everything was mapped, but its own evidence pointed at the wrong files. what should win?

i ran into a failure mode that feels bigger than one tool. the generated summary said all obligations were mapped correctly. the underlying locations pointed at an ABI wrapper, a test file, and an RPC helper instead of the protocol logic the tool was supposed to verify.

both artifacts came from the same AI-assisted run. the summary was cleaner, but the evidence was stronger.

for teams using agents or AI eval tooling: do you have a rule for which artifact wins when the summary and the receipts disagree? logs over summaries? traces over validation docs? manual review every time?
```

### Draft B

Target community: `r/artificial` or a broad AI-builder discussion community.

Score: 19/21

Decision: `draft_hold`

```text
when an AI summary disagrees with its own logs, do you trust the summary, the logs, or neither?

i keep seeing a version of this where the AI output looks coherent at the top level, but the supporting artifacts tell a messier story. the dangerous part is that the summary is usually what humans read first.

one rule i am testing is: raw artifacts beat validation notes, and validation notes beat generated summaries when they conflict.

does anyone have a different rule that works in practice, or is this still mostly handled by vibes and spot checks?
```

### Draft C

Target community: `r/LLMDevs`, comment-first candidate under threads about AI agents, evals, or code-review automation.

Score: 20/21

Decision: `comment_first`

```text
what is your rule when an agent says done but the underlying artifacts say maybe not?

tests catch some of this, but not all of it. in analysis workflows, the failure can be subtler: the summary claims success, while the CSV, trace, citation, or code location underneath points somewhere that does not support the claim.

i am starting to think "done" should require an evidence hierarchy, not just a clean final message.

how are people handling this in real agent workflows?
```

## Posting Decision

Decision: `draft_hold`, with Draft C usable as `comment_first` only after a specific live thread is selected and action-time approval is granted.

Reasoning:

- The run produced three standalone Reddit-native seeds above the default threshold.
- The strongest title/body pair is Draft A because it starts from the essay's concrete failure scene and asks for operator practice.
- No existing package-local Reddit ledger or current account-health record was available in declared context, so `post_now_native` is not justified.
- No external mutation was approved or attempted.
- No Substack or owned link belongs in the post body by default.

Next local step before any external action: create or update a package-local Reddit experiment ledger with account-health state, target subreddit, moderation risk, and exact approval status.

## Approval Boundary

- External posting approved: `no`
- Exact approved copy: none
- Composer verification: not performed
- Link placement: no owned link in body; optional link comment would require separate approval after a live thread earns context
- External mutation status: none attempted

## Outcome Readback

No Reddit post, comment, vote, modmail, or other external mutation was performed in this proof run, so there is no live outcome readback.

| Date | URL | Upvotes | Comments | Strongest Objection | Best Reply Signal | Next Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-05-09 | n/a | n/a | n/a | n/a | n/a | Hold local drafts until account-health and approval gates are satisfied. |
