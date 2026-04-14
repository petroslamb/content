# Your AI Is Confidently Wrong: You Have No Rule for What to Do About It

**Generation is cheap. Trust is expensive. The expense isn't compute: it's honesty.**

---

## The Moment of Contradiction

Our AI verification tool analyzed a complex codebase and produced two outputs from the same run.

The summary: *"All obligations properly mapped to specification and client implementation code."*

The underlying data: location fields pointing to an ABI wrapper, a test file, and an RPC helper. None of these implement the protocol logic the tool was supposed to verify.

Both documents were AI-generated. Both were confident. They flatly contradicted each other.

And we had no rule for which one to trust.

No procedure for tracking the disagreement. No way to prevent it from silently propagating into a compliance report. The polished narrative would have won because polished narratives always win when nobody is forced to check the receipts. This wasn't a model failure. It was an *evidence governance* failure. It is happening right now in any organization that ships AI-generated analysis without deciding, in advance, what counts as proof.

---

## The Auditability Gap

I spent a month building **eip-verify**, an AI tool for Ethereum protocol verification. The task was to check whether client code correctly implements protocol specifications across five iterations and 47 directly adjudicated obligation mappings.

The core finding surprised me: **The system got dramatically better at exposing where it might be wrong. It did not get dramatically better at being right.**

Over five iterations, the *inspectability* became excellent. I could trace every claim to the exact prompt, transcript, and code snippet that produced it. I could replay any phase independently. I could spot contradictions between the summary and the data.

The *accuracy* was operationally useful at best. The strongest model scored 80% valid. The cheapest scored 13%. More importantly, 72% of the total follow-up burden (the human time required to check the AI) came from the cheapest model alone.

Most teams building with AI are optimizing the wrong variable. They are trying to make the model right more often. Our data showed that you should first make the model's *wrongness findable*. Findable wrongness is manageable. Confident wrongness is catastrophic.

This principle is not specific to Ethereum. Any domain where an LLM produces both a summary and the evidence behind it faces the same structural problem. The surface is always more polished than the substance. Without a rule for what to do when they disagree, the surface wins.

---

## Medicine’s Evidence Crisis

In the 1990s, medicine had its own version of this problem. Expert opinions sounded authoritative. Case reports were vivid. When randomized controlled trials contradicted both, nobody had a rule for which source to trust. Polished expertise overrode messy data. Patients paid for it.

The solution was not to train better experts. It was to build an **evidence hierarchy**: a mechanical rule that removes judgment from the conflict-resolution step. Systematic reviews over RCTs. RCTs over cohort studies. Cohort studies over case reports. No exceptions. No appeals to authority.

This reshaped how medicine evaluates evidence. We are currently ignoring this lesson.

Right now, AI-generated analysis has the same structural problem medicine had before evidence-based practice. Recent research confirms each piece independently: models hallucinate with certainty even when they know the answer (Simhi et al., 2025). Multi-signal verification beats pass/fail (Ji et al., 2026). Claim-level auditability is emerging as a field (Rasheed et al., 2026).

We lack a widely adopted pattern that integrates these pieces into an operational workflow. The practitioner's question remains: *when this specific run's summary contradicts its own data, which artifact wins?*

We built the answer.

---

## The Evidence Governance Pattern

We assembled five interlocking components. No single component is original. The integration is the product.

### 1. Evidence Hierarchy
Raw artifacts (CSVs, transcripts, prompts) beat validation documents (scored assessments), which beat narrative summaries. When tiers conflict, the strongest wins. This single rule would have caught our opening contradiction. The CSV data overrules the polished summary. Three claims in our project were downgraded this way.

### 2. Multi-dimensional Scoring
Every output is scored on five dimensions: statement fidelity, spec location, implementation location, flow plausibility, and evidence sufficiency. This replaces "looks plausible" with structured, repeatable judgment. Two reviewers scoring the same output should converge.

### 3. Contradiction Register
Disagreements between artifacts become first-class workflow objects. They are tracked with an ID, conflicting claims, sources, and a resolution rule. We surfaced eight contradictions across 81 scored mappings. Before the register, all would have been resolved silently by whoever spoke last.

### 4. Claim Ledger
Every external claim links to supporting evidence, a confidence tag, and known counterevidence. Claims can only be promoted when evidence improves. They must be downgraded when it weakens. No ledger entry means no external claim. This is the enforcement that makes the rest structural.

### 5. The Operating Loop
Run → Score → Log contradictions → Fix → Re-score → Repeat. Each cycle either promotes confidence or surfaces new contradictions. Both are productive. The loop works even when things get worse because deterioration is now visible.

---

## What Actually Happened

Before these rules, a polished AI narrative overrode contradictory data. Nobody noticed because there was no rule for which source to prefer. Claims that should have been flagged shipped as stated.

After deploying the pattern:
- Eight contradictions surfaced across 81 mappings. All were previously invisible.
- Three claims were downgraded based on tier-conflict resolution.
- Model-tier asymmetry became visible. Cheap models produced triage-grade output. Only stronger models supported claim promotion.

The aggregate follow-up burden was 38.3%. This sounds expensive until the governance system revealed that 72% of that burden was concentrated in the cheapest model tier. Without it, follow-up drops to 15%. That insight transformed an undifferentiated cost problem into an actionable routing decision: use stronger models where claims matter.

The pattern did not make the AI smarter. It made the AI's errors findable. It made the team accountable for what they chose to do with those errors.

---

## The Human Discipline

There is an irony to this project. Much of the evidence governance infrastructure (the rubrics, the contradiction register, the claim ledger) was itself built with AI assistance.

The AI is mediocre at the verification task. It is surprisingly good at building the scaffolding that exposes its own mediocrity. That is not a bug. That is the actual product.

The question was never "how accurate is the AI?" It was always "do the humans have the discipline to use the scaffolding instead of cherry-picking the results that sound best?"

This discipline is the hardest part. It is harder than the engineering. Harder than the prompts. Harder than choosing the right model. Foundationally, the expense of AI isn't compute. It is the willingness to downgrade your own claims when the evidence says you should.

If you ship AI-generated analysis and do not yet have a contradiction register, start one this week. If you already track contradictions, gate your next external claim on the ledger. The pattern costs a CSV and an afternoon.

---

*The tool is open source: **[eip-verify on GitHub](https://github.com/petroslamb/ethereum-protocol-verification/tree/ca15d40)**. Detailed data, model metrics, and EIP results are available in the **[Technical Companion](companion.md)**.*
