# Five Reddit Post Candidates

## Batch

- Date: 2026-05-06
- Source: `workflows/reddit-discussion-lab/seed-bank.md`, local essay packages, and the working Reddit example set
- Mode: prepared drafts, not approved for posting
- Link policy: no owned links in post body
- Posting policy: one post per community. Test one post, work the replies, then decide whether the next candidate should be posted, held, or converted into comments.

## Reset Notes

This file was rebuilt after the first batch came out too uniform and too thin.

The earlier plan, `live problem -> concrete distinction -> open question`, is useful but insufficient. It produces competent prompts, not necessarily compelling Reddit posts. The stronger standard is:

```text
source gem -> community role -> example mechanic -> earned contribution -> unresolved edge
```

Where:

- `source gem` means a real anomaly, paper result, case, or operator scene from the essay
- `community role` means who the reader gets to be in the thread: builder, reviewer, researcher, skeptic, operator, maintainer
- `example mechanic` means the post follows a specific successful Reddit shape rather than a generic house style
- `earned contribution` means the post gives one useful idea before asking the question
- `unresolved edge` means the reader can improve, dispute, classify, or falsify the post

No fake typos, no fake roughness, no owned links, no automation, and no external posting without action-time approval.

## Source Mining

| Candidate | Source Essay / Package | Strongest Reddit-Native Idea | Evidence Spine | Target |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `confidence-debt` | A polished AI verification report disagreed with the row-level evidence, and the polished artifact was the easier one to trust. | eip-verify contradiction ledger, claim auditability, PaperTrail, confidence-debt evidence hierarchy | `r/LLMDevs` |
| 2 | `specification-surface-source-of-truth` | In AI coding, the diff can be the wrong first review object because the governing intent may be outside the governed system. | Specification Gap, ContextCov, AgentSPEX, spec-driven development, professional-control evidence | `r/AI_Agents` |
| 3 | `binding-gap` | Some LLM errors preserve the right pieces while losing the exact role, source, or numeric attachment needed for faithful use. | Reversal Curse as binding problem, entity binding mechanisms, semantic-role work, meta-analysis extraction failures | `r/LanguageTechnology` after `r/MachineLearning` blocked |
| 4 | `illusion-of-swarm` | Multi-agent systems may be runtime products, routing workarounds, or training rigs, and those are different claims. | MAS-to-single-agent-with-skills, skill-selection collapse, semantic confusability, scaling-agent-system results | `r/artificial` |
| 5 | `autonomy-tax` | AI often moves verification work onto senior people faster than it removes work from the organization. | Copilot OSS review-load study, call-center novice productivity split, governance and observability cost frame | `r/ExperiencedDevs` |

## Holds And Constraints

- `r/aiengineering` remains held for prepared copy because current local notes say its rules include no bots or LLM use for posts/answers. Use only after a manual human rewrite.
- `r/MachineLearning` needs `[D]` discussion framing and body text with actual analysis. Do not post a bare arXiv link. On 2026-05-06, the composer stayed blocked even with valid title tags and flair, so Pair 3 was adapted for `r/LanguageTechnology` instead.
- `r/ExperiencedDevs` is higher risk. Rule-check timing and post flair in the browser before using it.
- `Corrective Competence` is not used as a standalone essay source here. Its live draft is intentionally blank except for thesis lock, so using it directly would recreate the weak fifth post. Its evidence seam is useful only where the post itself is carried by concrete studies.

## Pair 1: Confidence Debt

Target community: `r/LLMDevs`

Decision: strongest first test. It is specific, lived, technically inspectable, and close to the comment tone that already got traction.

### Example Post

Source: [Two failure modes I caught in my AI lab in one day. Both involve the system silently lying about its own state.](https://www.reddit.com/r/artificial/comments/1t4cx88/two_failure_modes_i_caught_in_my_ai_lab_in_one/)

Example mechanic:

- starts from something the author actually caught
- gives the reader a concrete failure scene before any theory
- names the hidden common class only after the incidents are legible
- asks builders how they instrument or prevent the failure

### Our Post

Title:

```text
one ai verification run gave me two artifacts that disagreed
```

Body:

```text
i ran into a version of this in an ai-assisted verification project that has been hard to unsee.

the generated report said the protocol obligations were mapped. it was tidy enough to forward. the row-level evidence was uglier. some mappings pointed at abi helpers, test fixtures, or rpc glue instead of the protocol logic the system was supposed to verify.

across 81 scored mappings and 47 direct-adjudication rows, we tracked 8 contradictions and downgraded 3 claims. the important part was not that the model made mistakes. that happens. the part that bothered me was that the most usable artifact was also the artifact least able to defend its own claims.

if the summary had moved first, everyone downstream would have inherited confidence that the evidence layer had already contradicted.

the repair was to stop letting summaries settle disputes. raw evidence outranked summaries. contradictions became rows instead of vibes. a claim needed an evidence state before it was allowed to travel.

for people building agent or eval workflows, what artifact is allowed to overrule the agent's final answer in your setup? trace, test, row evidence, second model, human review, something else?
```

Why this is tighter:

- It uses a real artifact conflict, not a generic "done" complaint.
- It gives enough numbers to feel grounded without turning into a paper list.
- The contribution is a usable rule: decide what artifact can settle a claim.
- The question invites concrete workflow answers rather than agreement with `confidence debt`.

## Pair 2: Specification Surface

Target community: `r/AI_Agents`

Decision: post after Pair 1 only if the account is still in a normal trust state. This is richer than a task-list question because it starts from review authority and uses the paper result as the hinge.

Posting note: Posted to `r/AI_Agents` on 2026-05-06 after feed check showed active discussion about stricter review standards for AI-generated code.

### Example Post

Source: [How do folks manage worktrees when working with multiple agents in parallel?](https://www.reddit.com/r/LLMDevs/comments/1t50mxb/how_do_folks_manage_worktrees_when_working_with/)

Example mechanic:

- asks about a concrete coordination pain builders already have
- describes the current setup and where it breaks
- leaves room for tools, policies, or lightweight habits
- does not pretend the author has solved it

### Our Post

Title:

```text
when an agent opens a PR, what do you review before the diff?
```

Body:

```text
the awkward part of agent coding, for me, is that the diff is often not the first thing that needs review.

you get a normal-looking PR. tests pass. the summary sounds reasonable. then someone asks what the agent was actually supposed to preserve. the answer is split across a ticket, a chat prompt, an agents.md file, some old acceptance criteria, and one design assumption that never made it into a durable artifact.

that is where the review gets weird. the code is visible, but the authority behind the code is scattered.

the paper that made this click for me was the specification-gap experiment with code agents. when the shared spec was stripped down, separate agents failed to integrate much more sharply. a conflict detector could identify some structural mismatches, but restoring the full specification was what recovered the system. that feels close to what happens in real PR review. detection helps, but missing shared decisions still have to live somewhere.

the direction i am more interested in now is not bigger context files. it is which parts of context deserve authority. some instructions should stay docs. some should become executable checks, contracts, trace policies, or tests. ContextCov and AgentSPEX are interesting to me because they move instructions into enforcement instead of leaving them as prose the agent may or may not obey.

for teams actually using coding agents, where do you put the decisions a second agent or a reviewer should not have to infer again? tests, contracts, agent readmes, workflow specs, trace checks, architecture docs, something else?
```

Why this is tighter:

- It does not suggest "use a task checklist" as the answer.
- The lived problem is PR review authority, not abstract coordination.
- The paper claim gives the post a real turn after the third sentence.
- The open question asks where authority belongs, not which file format is fashionable.

## Pair 3: Binding Gap

Target community: `r/LanguageTechnology` after `r/MachineLearning` composer blockage

Decision: best replacement for the weak benchmark post. This was originally the ML-facing candidate because it is mechanism-oriented and paper-backed, but the `r/MachineLearning` composer stayed blocked on 2026-05-06. The posted route was `r/LanguageTechnology`, which is smaller but better targeted for NLP, semantic roles, information extraction, and LLM evaluation taxonomy.

### Example Post

Source: [open source AI assistants ranked by tool call reliability](https://www.reddit.com/r/LLMDevs/comments/1t4e9ym/open_source_ai_assistants_ranked_by_tool_call/)

Example mechanic:

- turns a vague quality question into a concrete evaluation surface
- gives readers a metric they can attack, improve, or extend
- pulls discussion toward failure taxonomy instead of product preference
- works because the thread has something measurable at the center

### Our Post

Title:

```text
[D] should LLM evals separate binding failures from hallucination?
```

Body:

```text
i am trying to decide whether a class of LLM errors deserves its own eval slice, or whether it is already covered by hallucination, compositionality, provenance, or relational generalization.

the pattern is this. the model preserves the right semantic material, but loses the role, source, or numeric attachment that makes the answer usable. it has the entities but not the direction. the paper but not the sentence it supports. the variables and effect size but not the correct tuple.

the clean behavioral anchor is the Reversal Curse. Wang and Sun 2025, arXiv 2504.01928, argue that reversal failures are not just a data-augmentation oddity but reflect inconsistency and entanglement in conceptual binding. "Tom's wife is Mary" and "who is Mary's husband" contain the same fact, but the role assignment has to survive inversion.

the mechanistic papers make the category harder to dismiss. Feng and Steinhardt 2023, arXiv 2310.17191, show entity-attribute binding as an internal mechanism where causal interventions change the pairing behavior. Dai, Heinzerling, and Inui 2024, arXiv 2409.05448, identify an ordering subspace that directly affects which entity binds to which attribute. this is why i am hesitant to treat every near-miss as generic hallucination. some of the issue seems to be attachment, not just missing knowledge.

the bridge to normal language is thematic roles. Denning, Guo, Snefjella, and Blank 2025, arXiv 2504.16884, find that LLMs can extract agent/patient information, but that role information influences sentence representations much more weakly than it does in humans. Aljaafari, Carvalho, and Freitas 2025, arXiv 2511.20910, push from the other side by localizing semantic-role circuits. so role structure is not absent. it is present but apparently not always dominant enough.

the high-stakes version is Tan and D'Souza 2026, arXiv 2602.10881, on LLM-based evidence extraction for meta-analysis. that task is not just "find the variable" or "find the effect size". the model has to preserve which variable, role, method, and effect size belong together. their error pattern, role reversals, cross-analysis drift, instance compression, numeric misattribution, looks like exactly the kind of failure that aggregate accuracy hides.

the boundary papers matter too. Saynova et al 2024, arXiv 2410.14405, show that correct factual completions can come from different mechanisms, including exact recall, heuristics, guesswork, or generic language modeling pressure. Boulos et al 2026, arXiv 2603.03541, separate retrieval and generation failures in RAG-style medical QA. both are useful pressure against overclaiming. a binding-style metric should not relabel retrieval miss, ignored context, or ordinary fabrication.

the eval split i want is something like ingredient recall vs binding fidelity vs final answer accuracy. if a model sees the right entities and numbers but attaches them to the wrong role/source/tuple, that should not be counted the same way as a retrieval miss or an unsupported fabrication. RAG-X style retrieval/generation diagnosis is adjacent, but i am not sure it isolates this attachment layer cleanly.

is there already a benchmark or metric family that does this well? or would most ML people say binding-heavy extraction is already covered by existing compositionality/provenance/hallucination evaluations?
```

Why this is tighter:

- It respects `r/MachineLearning` by naming both the supporting and boundary papers.
- The contribution is a proposed eval decomposition, not a slogan.
- The post gives ML readers something to contest: whether attachment errors deserve a separate metric family.
- It avoids an owned link and keeps the term subordinate to papers, mechanisms, and measurable failure types.

## Pair 4: Illusion Of The Swarm

Target community: `r/artificial`

Decision: broad discussion seed with enough research claims to avoid being another "agents are hype" thread. It should not go to `r/MachineLearning` before Pair 3 because Binding Gap is a cleaner ML fit.

Posting note: Posted to `r/artificial` on 2026-05-06 after patching the live composer to name the UBC paper directly and use the exact 53.7 percent / 49.5 percent figures.

### Example Post

Source: [AI agents vs AI chatbots: what are companies actually building?](https://www.reddit.com/r/artificial/comments/1t53331/ai_agents_vs_ai_chatbots_what_are_companies/)

Example mechanic:

- starts from a category confusion people already argue about
- asks what is actually being built, not what the marketing category says
- separates production reality from vocabulary
- lets readers bring examples without needing to accept the author's taxonomy

### Our Post

Title:

```text
are multi-agent systems actually staying multi-agent after people optimize them?
```

Body:

```text
i am trying to separate three things that get called multi-agent systems as if they are the same object.

one is a real runtime architecture. different models, trust boundaries, permissions, environments, or actors need to stay separate.

one is a routing workaround. the system is split into planner, researcher, coder, reviewer, or domain agents because a flat tool or skill space gets too confusing for one model to choose from cleanly.

one is a training rig. multiple agents debate, explore, correct, or generate traces, but the useful part may later be distilled into a single agent, a skill library, or a better router.

the UBC paper When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail made this feel less semantic to me. it shows some multi-agent setups being compiled into a single agent with skills, with 53.7 percent lower token use and 49.5 percent lower latency while keeping comparable quality. but the same paper also shows where this stops being easy. flat skill selection degrades nonlinearly as the library grows, and semantic confusability seems to matter more than size alone.

so i do not think the interesting question is "one agent or many agents". it is which boundary is load-bearing.

for people building or following these systems, which multi-agent boundaries have actually survived optimization? capability boundaries, permission boundaries, tool namespaces, critic/verifier separation, parallel search, human ownership, something else?
```

Why this is tighter:

- It withholds the conclusion and gives three categories readers can argue with.
- It uses the strong numbers from the essay without dumping a bibliography.
- It does not solve the problem for the reader. It asks which boundaries survive.
- The post can pull both skeptics and builders into examples.

## Pair 5: Autonomy Tax / Human Bandwidth

Target community: `r/ExperiencedDevs`

Decision: high-risk but potentially valuable if posted with rule care. This replaces the unclear Corrective Competence draft with a concrete senior-engineer review-load question.

### Example Post

Source: [Agent skill which will automatically raise PR](https://www.reddit.com/r/LLMDevs/comments/1t4prcq/agent_skill_which_will_automatically_raise_pr/)

Example mechanic:

- begins from a workflow automation people can picture
- turns the automation into a trust-boundary question
- invites maintainers to talk about review burden and guardrails
- works because the automation is concrete enough to disagree about

### Our Post

Title:

```text
has ai changed who does the boring review work on your team?
```

Body:

```text
i do not mean the usual "did it make developers faster" question. i mean who absorbed the verification work after the output got cheaper.

the pattern i keep coming back to is that ai often raises throughput before it raises review capacity. in one open-source study around Copilot adoption, core developers produced less of their own original code and reviewed more code from less-experienced contributors. the numbers that stuck with me were about 19 percent less original output and 6.5 percent more review. different domain, but the call-center evidence has a similar shape: novices get the biggest productivity lift, experienced people less so.

that sounds less like replacement and more like load transfer. more plausible work reaches the people who can tell whether it is actually right.

on engineering teams, i would expect this to show up as seniors spending more time on ai-shaped diffs, generated tests that test the wrong thing, integration cleanup, rollback decisions, and "looks fine but why did it change this file" reviews. maybe the gain still dominates. but if nobody measures the senior-review load, the productivity story is missing the part that pays for the confidence.

for experienced devs using ai heavily, has your review work actually gone down? or did the boring verification work move toward the people with the most context?
```

Why this is tighter:

- It is intelligible without the unpublished Corrective Competence essay.
- The question is lived for senior developers and maintainers.
- It has concrete study claims but keeps the ask practical.
- It leaves room for disagreement: some teams may have reduced review load through tests, contracts, smaller batches, or better ownership.

## Recommended Test Order

1. `r/LLMDevs` with Pair 1. It is the strongest because it is specific, grounded, and reply-friendly.
2. `r/LanguageTechnology` with Pair 3. This replaced the blocked `r/MachineLearning` route and was posted on 2026-05-06.
3. `r/artificial` with Pair 4. Posted on 2026-05-06 after feed check showed active agent infrastructure and agent-market discussion.
4. `r/AI_Agents` with Pair 2. Posted on 2026-05-06 after feed check showed active builder/workflow discussion.
5. `r/ExperiencedDevs` with Pair 5 only after rule and timing check. This post should be held if the community is hostile to AI process threads that day.

## Approval Boundary

These are drafts. Before any external posting:

- open the target subreddit in the browser
- check current rules, flair, and feed temperature
- paste the exact title and body back for approval
- do not add owned links unless asked in replies
- do not post multiple owned threads in sequence
