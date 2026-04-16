# Thesis Stress-Test — Gate 1

## Test 1: Independence Test

Question: Are the three layers genuinely connected or merely analogical? Is there evidence of confidence at one layer causing failure at another?

### Result: PASS

The layers are causally connected, not merely analogical. The connection runs through a source-channel-sink structure:

- **Artifact layer** (source): AI generates confident outputs that outrun their evidence base. The eip-verify case demonstrates this directly: polished summaries contradicted row-level evidence and would have propagated without adjudication rules.
- **Evaluation layer** (channel): Benchmark scores and aggregate metrics are the primary mechanism by which artifact-level confidence gets formalized and exported. A benchmark score is confidence debt in portable form. It travels to procurement teams, deployment reviews, and policy frameworks. The web search confirms this: benchmark scores are routinely used as proxies for readiness in procurement and deployment decisions. The EU, AAAI, and multiple regulatory bodies now use benchmark-based frameworks to assess AI robustness.
- **Human layer** (sink): Once confident AI output reaches the human operator, two things compound. First, the operator consumes the output's inherited confidence without seeing what was compressed away upstream. Second, repeated AI assistance can erode the operator's independent correction capacity (persistence loss, skill formation erosion, competence shadow compounding).

The eip-verify case already contains a micro-instance of the full cascade: a confident summary (artifact layer) survived review (human layer) in part because no independent benchmark validated the underlying evidence (evaluation gap). That is not an analogy. It is a worked example of the three-layer failure within one project.

The broader literature confirms the cascade structure. Multiple 2024-2025 sources describe:

- Automation bias compounding through multi-stage pipelines, where "a minor error at an early stage can be amplified as it travels through subsequent stages"
- "Intermediate judgments" on AI advice actually reinforcing automation bias, strengthening psychological commitment to the system and making later correction harder
- "Agency decay" and professional deskilling caused by consistent cognitive offloading to AI, making later oversight structurally weaker
- "Silent degradation" in AI documentation pipelines, where the system continues producing plausible output while quality drifts without detection

These are not three independent problems that happen to rhyme. They describe a causal pathway: confident artifact generates trust, trust propagates through evaluation, propagated trust reaches a human whose correction capacity has been degraded by the same assistance.

### Micro-instance: eip-verify as a worked cascade

1. The AI generated a confident verification summary → artifact layer confidence debt incurred
2. No independent benchmark or evaluation framework tested the summary's claims against row-level artifacts → evaluation layer gap: confidence propagated without calibration
3. The reviewer consumed the polished summary rather than tracing each mapping to source code → human layer: correction capacity was insufficient because the confident artifact pre-empted deep inspection
4. The summary would have been forwarded as proof → confidence debt called at the point of consequence

---

## Test 2: Rival Absorption Test

Question: Does "calibration," "appropriate reliance," or "overconfidence" absorb the full phenomenon without needing a cross-layer account?

### Result: PASS

These rival frames are real and important. They do not absorb the cross-layer phenomenon.

**Calibration** operates within one layer. Better model calibration can reduce the frequency of confidently wrong outputs at the artifact layer. It does not prevent an aggregate benchmark score from being over-read at the evaluation layer. It does not restore correction capacity at the human layer once it has been eroded.

**Appropriate reliance** operates at the human-system interface. It addresses whether a person weights machine advice correctly in the moment. It does not address whether the evidence that reached the person was already over-compressed, or whether the person's capacity to weight it well has been structurally degraded by prior assistance.

**Overconfidence** (as a model property) is a single-point diagnosis. Confidence debt is a workflow-level propagation pattern. Overconfidence describes what the model does. Confidence debt describes what happens when the output travels downstream through evaluation, deployment, and human oversight without the evidence catching up.

The rival frames are all within-layer interventions. They do not address the cross-layer cascade. Better model calibration at the artifact layer is necessary but not sufficient because it does not prevent evaluation-layer over-reading or human-layer erosion. Better reliance calibration at the human layer is necessary but not sufficient because it does not address the fact that the evidence the human received was already over-compressed by the time it arrived.

Confidence debt names the workflow-level gap. The rivals name within-layer symptoms.

---

## Test 3: Cut Test

Question: Can one layer be removed entirely without the essay losing structural coherence?

### Result: PASS (with one important finding)

**Remove artifact layer**: the essay becomes "benchmark scores get over-read, and the human can't catch it." That is essentially corrective-competence plus clean-interface-illusion. The essay loses its strongest asset: the first-party inspectable case. It also loses the most visceral opening (the summary-vs-evidence contradiction). Structural loss is severe.

**Remove evaluation layer**: the essay becomes "confident artifacts outrun evidence, and humans can't catch the errors." At first glance this seems functional. But the evaluation layer does specific structural work: it is the propagation channel. It explains HOW artifact-level confidence reaches the human layer. Without it, the connection between "AI produces overconfident summaries" and "humans lose correction capacity" is an inferred association, not a demonstrated pipeline. The evaluation layer is the bridge.

**Remove human layer**: the essay becomes "confident artifacts plus over-read benchmarks." That is essentially evidence-governance plus clean-interface-illusion. The essay loses all human stakes. It becomes a methodological complaint about measurement infrastructure. This is precisely the ceiling that clean-interface-illusion hit at 8.6.

Each layer does structural work that the other two cannot replace:

- Artifact layer provides the concrete, inspectable source of confidence debt
- Evaluation layer provides the propagation mechanism (how confidence gets formalized and exported)
- Human layer provides the consequence and the irreversibility (why propagated confidence becomes dangerous)

The finding: the evaluation layer is the most tempting to cut because it sits between two more vivid sections. But it functions as the causal bridge. If the draft needs compression, shorten the evaluation section rather than cutting it. This section should be the leanest of the three but cannot be absent.

---

## Gate 1 Verdict

**PASS. All three tests clear.**

The cross-layer thesis is structurally real, not merely analogical. The layers are causally connected through a source-channel-sink structure. The rival frames are genuine but operate within individual layers and do not absorb the cross-layer cascade. Each layer does irreplaceable structural work.

The research pass also surfaced supporting language from the broader literature: "agency decay," "silent degradation," "satisficing trap," and "resilience-based metrics" are all described in the 2024-2025 literature as cross-stage or pipeline-level phenomena, not single-point diagnoses. This is converging independent support for the cross-layer framing.

One structural insight from the cut test should inform the blueprint: the evaluation layer is the bridge, not the highlight. Keep it lean in the draft. The artifact layer (opening) and the human layer (escalation) carry the emotional and intellectual weight. The evaluation layer carries the causal connection.

## Next Gate

Proceed to Gate 2: Evidence Fusion.
