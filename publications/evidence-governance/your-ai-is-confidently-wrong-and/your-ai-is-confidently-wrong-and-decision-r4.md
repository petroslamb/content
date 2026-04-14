---
kind: essay_iteration_decision
package: "evidence-governance/your-ai-is-confidently-wrong-and"
revision: 4
judgment_policy: "evidence_gate"
live_draft_path: "publications/evidence-governance/your-ai-is-confidently-wrong-and/your-ai-is-confidently-wrong-and.md"
candidate_path: "publications/evidence-governance/your-ai-is-confidently-wrong-and/your-ai-is-confidently-wrong-and-candidate-r4.md"
recommendation: case_study_flagship_now
promotion_allowed: false
requires_human_approval: true
---
# Evidence Gate Decision

## Core Finding

The real blocker is evidence scope, not prose polish, packet policy, or one more surgical rewrite.

The current leaf has enough evidence to support a strong **case-study flagship** anchored in `eip-verify`. It does **not** yet have enough evidence to support an outstanding **doctrine flagship** that presents Evidence Governance as a broadly established operating standard.

This judgment is consistent with the package's own proof boundary:

- the current empirical base is one project, three EIPs, 81 scored rows, and 47 direct-adjudication rows in [`companion.md`](companion.md)
- the broader literature supports the shape of the synthesis, but the package memo explicitly warns against treating portability, generalization, or correctness gains as already proven in [`../evidence_governance_pattern/research_findings.md`](../evidence_governance_pattern/research_findings.md)
- the active bounded blueprint now treats the project as a case-study flagship rather than a doctrine claim in [`your-ai-is-confidently-wrong-and-blueprint-r4.md`](your-ai-is-confidently-wrong-and-blueprint-r4.md)

## Why This File

This finding belongs in the **decision surface**.

- [`your-ai-is-confidently-wrong-and.md`](your-ai-is-confidently-wrong-and.md) is the essay surface.
- [`companion.md`](companion.md) is the package-local evidence surface.
- [`your-ai-is-confidently-wrong-and-blueprint-r4.md`](your-ai-is-confidently-wrong-and-blueprint-r4.md) is the rewrite-governing surface.
- This file records the routing decision between viable next paths.

## What The Current Evidence Supports

- A real contradiction problem: narrative summaries can conflict with lower-level artifacts and still appear authoritative.
- A measurable governance result: `eip-verify` surfaced 8 contradictions, downgraded 3 claims, and exposed model-tier asymmetry in review burden.
- A strong bounded thesis: inspectability and claim governance may matter more operationally than small gains in apparent correctness.
- A credible synthesis claim: the package's five components align with independent literature on claim decomposition, conflict handling, gating, and evidence hierarchies.

## What The Current Evidence Does Not Yet Support

- Cross-domain portability of the full pattern as an established operational standard.
- Strong claims that the framework improves correctness rather than mainly improving inspectability, auditability, and adjudication quality.
- Broad claims that the same governance mechanics hold across other high-stakes domains without direct replication.
- A top-bar doctrine essay whose authority depends on more than one hard pilot plus literature alignment.

## Alternatives

### A. Case-Study Flagship Now

**Recommendation:** preferred path.

**Promise:** this essay proves what one verification project forced us to learn about governing AI-generated claims when summaries and artifacts disagree.

**What changes:**

1. Keep the public-facing title shape and opening contradiction.
2. Make `eip-verify` the center of gravity rather than a supporting anecdote.
3. Reframe the thesis from "this is the doctrine" to "this is the hard lesson from one serious pilot."
4. Use CHOKE, EBM, MedRAGChecker, and related work as support and border-setting, not as proof of universality.
5. Put the strongest project evidence in the body: 81 rows, 47 adjudications, 8 contradictions, 3 downgraded claims, burden concentration by model tier.
6. Add a real borders section naming exactly what this pilot does and does not prove.

**Why this path works now:** it stays inside the evidence the leaf already owns and can still produce a strong public object.

### B. Doctrine Flagship After Evidence Expansion

**Recommendation:** valid, but slower and evidence-dependent.

**Promise:** this essay argues that Evidence Governance is a reusable operating pattern with explicit limits, not just a lesson from one project.

**Minimum evidence package before claiming that bar:**

1. A second replication, ideally outside Ethereum.
2. Before/after evidence that the governance layer changed outcomes, not just prose confidence.
3. Explicit `audit_effort` measurement instead of follow-up counts alone.
4. Richer contradiction records with rationale and resolution evidence.
5. Claim lifecycle data such as promotion latency, downgrade conditions, and re-audit triggers.
6. At least one serious failure case or non-transfer case that strengthens the borders honestly.

**Why this path is stronger later:** it would let the essay earn doctrine status instead of borrowing doctrine tone from converging literature.

### C. Promote The Current Doctrine-Style Candidate Now

**Recommendation:** reject.

**Why not:** the current candidate compresses well, but it still asks the reader to trust a generalized doctrine whose empirical base is narrower than the rhetoric. That is exactly the kind of mismatch this package is supposed to resist.

## Recommendation

Choose **A. Case-Study Flagship Now** unless the package is about to invest directly in evidence expansion.

That path matches the leaf's current evidence, preserves the strongest public hook, and avoids pretending that one pilot has already earned the standing of a validated cross-domain standard.

If the goal remains the outstanding doctrine essay, do **not** keep polishing the current draft in place. Switch the workstream from essay iteration to evidence expansion first, then return with a new blueprint.

## File Ownership After This Decision

- Keep findings and path selection here in `decision-r4`.
- Keep metrics, artifacts, and package-local proof in [`companion.md`](companion.md).
- Path A is now instantiated in [`your-ai-is-confidently-wrong-and-blueprint-r4.md`](your-ai-is-confidently-wrong-and-blueprint-r4.md) and [`your-ai-is-confidently-wrong-and-candidate-r4.md`](your-ai-is-confidently-wrong-and-candidate-r4.md).
- If path B is chosen, create an evidence-expansion memo or blueprint in the leaf before drafting again.
