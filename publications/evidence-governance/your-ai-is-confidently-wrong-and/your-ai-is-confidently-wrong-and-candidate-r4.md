# Your AI Is Confidently Wrong: You Have No Rule for What to Do About It

**One verification project forced a simpler lesson than the doctrine version: when summaries and artifacts disagree, trust becomes a workflow problem.**

---

## The Moment of Contradiction

One `eip-verify` run produced two outputs that should never have been allowed to sit beside each other without consequence.

The summary claimed that all obligations were properly mapped to specification and client implementation code. The lower-level evidence told a different story. In the same run family, spot-checks turned up client mappings that pointed to ABI helpers, test files, and RPC glue rather than to the protocol logic the run was supposed to verify. The prose sounded clean. The row-level evidence was not. Both came from the same system. Both were written with confidence. They did not deserve the same trust.

That is the case this essay is about. One verification project, one set of artifacts, one recurring failure mode: polished narrative outrunning the evidence that was supposed to support it. Anything larger than that would ask the evidence to carry more than it can hold.

The uncomfortable part was not that the model was wrong. The uncomfortable part was that, without a rule for adjudicating the disagreement, the polished summary would have won. It was easier to read, easier to forward, and easier to mistake for proof.

---

## What Counted as Evidence

The strongest evidence in this project is not the whole scored sheet. It is the subset that was directly adjudicated against actual run artifacts and source code.

The current proof pack contains 81 scored rows. Of those, 47 are direct-adjudication rows. Those are the rows that matter most for this essay. They were reviewed against concrete artifacts: phase outputs, qualitative validation notes, transcript-level spot-checks, execution-specs paths, and geth paths. The remaining 34 rows are compare-derived expansion. They are useful as instability signals, but they do not carry the same weight. Blur that distinction on the page and the prose gets smoother while the case gets weaker.

That split matters because this repository can support opposite stories if you read it lazily. A run summary can look complete. A README can sound triumphant. A CSV can be fully populated. None of that settles whether the cited locations actually implement the claim. Inside `eip-verify`, that forced a working hierarchy. Raw or row-level artifacts outrank evaluation summaries. Evaluation summaries outrank narrative readmes. Once you see the same repo produce both a confident compliance story and contradictory spot-check evidence, this stops sounding like bureaucratic fussiness and starts sounding like survival.

That is also why the strongest version of the case is narrower than the doctrine version. I can show what happened in this project because the artifacts are inspectable. I cannot honestly claim that the same workflow has already been validated across domains I did not run.

---

## What the Runs Actually Showed

The central empirical finding was not that the system became dramatically more correct. The central finding was that it became easier to inspect, replay, and dispute.

Across the direct-adjudication subset, Haiku, Sonnet, and Opus did not just differ by score. They differed by failure mode. Haiku was the noisy run family. In the scored subset, 13 of its 15 direct-adjudication rows required follow-up. The spot-check transcript shows why: client mappings often landed in ABI bindings, tests, engine-adjacent code, or other peripheral surfaces instead of core implementation paths. Opus and Sonnet were far stronger, but their risk looked different. They were more likely to produce mappings that were functionally plausible while still compressing away constraints, missing a key condition, or treating a questionable obligation as settled.

That distinction matters more than leaderboard language. A noisy model creates filtration work. A plausible but incomplete model creates adjudication work. The first failure wastes attention. The second threatens to slip through review because the output already sounds like something a competent person might have written.

A second pattern was just as operationally important: obligation IDs were not stable across runs. Statement-level matching was required to compare reruns coherently. That means a naive row-by-row diff by ID is not an evaluation method. It is a way to manufacture false disagreement. Once the project started doing semantic alignment instead of ID alignment, some apparent instability disappeared, but another kind remained: the models were still choosing different statements, locations, and flows for what looked like the same underlying requirement.

The project also surfaced a harder category than simple invalidity. Some obligations were disputed. EIP1559-OBL-030 is the recurring example. The models treated it like a normal requirement. Later validation treated the requirement itself as questionable relative to fork-block behavior in the spec. That is not a routine hallucination and not a simple location mismatch. It is a semantic dispute about what should count as an obligation in the first place. Once that kind of case appears, `valid` versus `invalid` is not enough. You need room in the evidence layer for contested objects that remain live until adjudicated.

This is why the strongest claim from the current pack is about trustworthiness bottlenecks. The runs do not justify a grand theory of model ceilings. They do justify a narrower and more useful claim: if you let these outputs move downstream without row-level adjudication rules, they will present uncertainty in polished form and force humans to disentangle it late.

---

## What the Negative Control Taught

The EIP-7702 runs matter because they make one part of the problem painfully concrete: environment metadata can flip the story.

One workflow summary treated EIP-7702 as missing in geth and listed the absence of `SetCodeTxType` support as a broad finding. Another run family, under a different client context, came back effectively clean except for one nuanced note. If you read only one narrative summary, either conclusion can look decisive. Once you inspect the run context, the contradiction becomes legible. Client ref and environment were doing real work.

That is a more serious lesson than it first appears. It means a claim about implementation status is not just a model-output claim. It is a run-context claim. Strip away the metadata and the sentence can survive while its truth conditions disappear. In a normal writing workflow this looks like a citation problem. In an audit workflow it is worse: the same conclusion can be wrong for reasons that are not visible in the prose itself.

This was one of the moments where the project stopped looking like an LLM-evaluation story and started looking like an evidence-governance story. The model did not need a better personality. The system needed stronger rules for what kind of artifact was allowed to settle a claim.

---

## The Rules the Project Forced

The five-component frame came later. It was not the starting insight. It was the name given afterward to the controls the project had to invent in order to keep the outputs from governing themselves.

The first control was an evidence hierarchy. When a summary said one thing and lower-level artifacts said another, the summary lost. That sounds obvious once it is written down. Before the rule exists, teams drift toward whichever artifact is easiest to read and easiest to defend in a meeting.

The second control was row-level scoring. The project needed a way to mark a mapping as mostly right, partially right, unsupported, or semantically disputed without collapsing all of that into a single vibes-based verdict. The rubric exists to stop phrases like "looks plausible" from carrying more authority than they deserve.

From there the contradiction register became unavoidable. Once the same repository started producing incompatible claims, contradiction could no longer be treated as embarrassment or noise. It had to become a tracked object with a topic, competing sources, and a resolution note. Otherwise the polished narrative would keep absorbing the conflict and carrying on as if nothing had happened.

The claim ledger made the rest bite. A public-facing claim needed an evidence trail, a confidence level, and any known counterevidence. Without that, the project could still accumulate good internal notes while shipping overconfident public prose. That is the failure mode this essay is trying to name.

The phase boundaries mattered for a quieter reason. The phased pipeline did not solve correctness. It solved lineage. It made replay possible. It shrank the surface you had to inspect when something looked wrong. That is a more modest achievement than "the model understands Ethereum," but it is also more durable.

The literature helped explain these moves after the fact. Simhi and colleagues sharpen the confidence-versus-correctness problem. MedRAGChecker makes the case for claim-level verification rather than answer-level plausibility. Evidence-based medicine explains why hierarchical evidence rules are sometimes the only way to keep polished expertise from overruling messier but stronger artifacts. Those lines of work matter here. They make the project legible. They do not convert one pilot into a universal standard.

---

## What Changed Once We Used Them

The simplest way to describe the change is that the project stopped rewarding confidence alone.

Eight contradictions were surfaced across the 81 scored mappings. Three claims were downgraded. The direct-adjudication subset showed an aggregate follow-up burden of 18 out of 47 rows. That sounds like an indictment until you decompose it. Thirteen of those 18 follow-up rows came from Haiku. Remove the noisy tier and the burden drops sharply. That does not prove the workflow is cheap. It proves something more operationally useful: model selection is part of governance, not just procurement.

That shift is the real product of the case. Before the evidence layer, "cheap model versus expensive model" looks like a straightforward cost question. After the evidence layer, it becomes a cost-to-trust question. A model that produces cheap but noisy mappings can move the budget from API usage to reviewer time without announcing that trade. The project only made that visible because it stopped treating fluent output as the same thing as trustworthy evidence.

This is also where the phrase "findably wrong" becomes useful. The project did not eliminate wrong answers. It improved the conditions under which wrong answers could be surfaced, disputed, and prevented from silently hardening into public claims. That is a humbler outcome than a capability breakthrough. It is also a more honest one.

---

## What This Case Does Not Prove

This essay does not prove that the five-component frame is already a validated cross-domain doctrine. It does not prove that correctness improved in any general sense. It does not prove that 81 scored rows constitute a benchmark-grade dataset. It does not prove that compare-derived proxy rows should be treated like direct manual adjudication. It does not prove measured minutes-per-obligation, because that timing study still needs a controlled rerun protocol.

It proves something narrower. In one verification project, using one family of artifacts, the main operational bottleneck was not output generation. It was deciding what deserved to be trusted once the outputs began contradicting each other. The evidence layer made that bottleneck visible and gave the project a way to act on it.

That is enough to support a case-study flagship. It is not enough to certify a doctrine essay at the highest bar. If the stronger essay is still the goal, the next move is not more compression. It is more evidence: controlled reruns, measured adjudication time, balanced compare blocks, and at least one additional environment where the same rules survive contact with a different task.

---

## The Discipline

The lesson I trust most from `eip-verify` is not that the model was hopeless and not that the framework is complete. It is that trust decays into theater when the artifacts are allowed to disagree without consequence.

Once that happens, the question changes. You stop asking whether the system sounds convincing. You start asking which artifact is allowed to settle the claim, who is allowed to downgrade it, and what happens when the evidence refuses to line up cleanly. Those are workflow questions. They are also moral questions in a plain sense. They determine whether a team is willing to publish the harder sentence instead of the cleaner one.

That is why the real cost in this case was not compute. It was adjudication discipline. The expensive act was not generating the report. It was looking at a polished claim, tracing it back to the row-level evidence, and being willing to say: this one does not clear.

## References

- **Project evidence pack.** [`sample_scored_run.csv`](https://github.com/petroslamb/ethereum-protocol-verification/blob/ca15d40/docs/evaluations/sample_scored_run.csv), [`contradictions.csv`](https://github.com/petroslamb/ethereum-protocol-verification/blob/ca15d40/docs/evaluations/contradictions.csv), [`evidence_ledger.md`](https://github.com/petroslamb/ethereum-protocol-verification/blob/ca15d40/docs/evaluations/evidence_ledger.md), [`scoring_rubric.md`](https://github.com/petroslamb/ethereum-protocol-verification/blob/ca15d40/docs/evaluations/scoring_rubric.md), and [`metrics_summary.md`](https://github.com/petroslamb/ethereum-protocol-verification/blob/ca15d40/docs/evaluations/metrics_summary.md). These are the main adjudication surfaces behind the essay.
- **Validation surfaces.** [`QUALITATIVE_EVALUATION.md`](https://github.com/petroslamb/ethereum-protocol-verification/blob/ca15d40/docs/QUALITATIVE_EVALUATION.md), [`qualitative_validation_transcript.md`](https://github.com/petroslamb/ethereum-protocol-verification/blob/ca15d40/examples/qualitative_validation_transcript.md), and the EIP-7702 workflow summaries for [run 21570420032](https://github.com/petroslamb/ethereum-protocol-verification/blob/ca15d40/examples/workflow_runs/21570420032/verification-report-7702/summary.md) and [run 21571909617](https://github.com/petroslamb/ethereum-protocol-verification/blob/ca15d40/examples/workflow_runs/21571909617/verification-report-7702/summary.md). These matter because they tie the case back to actual run behavior rather than to narrative summary alone.
- **Simhi, A., et al. (2025).** *Trust Me, I'm Wrong: LLMs Hallucinate with Certainty Despite Knowing the Answer.* Useful here because it explains why confidence can survive even when the underlying answer is unstable.
- **Ji, Y., et al. (2026).** *MedRAGChecker: Claim-Level Verification for Biomedical Retrieval-Augmented Generation.* Useful because it supports the move from answer-level plausibility to claim-level adjudication.
- **Sackett, D. L., et al. (1996).** *Evidence Based Medicine: What It Is and What It Isn't.* Useful here as precedent for the narrower point that artifact hierarchies become necessary when polished expert narrative and stronger evidence conflict.
