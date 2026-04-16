# Evidence Fusion — Gate 2

## Test 1: Assignment Test

Question: Does each body section have at least two papers (or project evidence surfaces) that directly support its layer of the thesis?

### Section 1: The Polished Lie (artifact layer / opening)

- First-party eip-verify artifacts: 81 scored rows, 47 direct-adjudication rows, 8 contradictions, 3 downgraded claims → DIRECT
- Simhi et al. "Trust Me, I'm Wrong" (confidence survives when the underlying answer is unstable) → DIRECT
- MedRAGChecker (claim-level verification as alternative to answer-level plausibility) → HINGE SUPPORT
- Sackett et al. Evidence Based Medicine (artifact hierarchy precedent) → THEORY SUPPORT

Assignment: strong. Two direct sources plus two support sources.

### Section 3: The Evaluation Layer

- tau-bench repeated-run result → DIRECT (shows score compression of reliability information)
- WebSuite (failure attribution and localization) → DIRECT
- WebForge (richer environments making toplines less sufficient) → DIRECT
- Towards a Science of AI Agent Reliability (reliability dimensions outrun single metrics) → DIRECT
- TheAgentCompany (bounded task completion reported in deployment language) → SUPPORTING
- REAL (bounded usefulness) → SUPPORTING
- LiveMCPBench (tool retrieval at scale) → SUPPORTING
- From Task Solving to Robust Real-World Adaptation → SUPPORTING

Assignment: strong. Four direct sources, four supporting. This section may need cutting rather than reinforcement.

### Section 4: The Human Layer

- AI Assistance Reduces Persistence (2604.04721) → DIRECT (causal evidence, strongest opening exhibit for this section)
- How AI Impacts Skill Formation (2601.20245) → DIRECT (mechanism: interaction pattern determines erosion vs. preservation)
- Mitigating Epistemic Debt (2602.20206) → DIRECT (intervention layer: unrestricted vs. scaffolded assistance diverge on removal)
- The Competence Shadow (2603.25197) → DIRECT (formal compounding argument: machine-pruned search space)

Assignment: strong. Four direct sources, all doing body work.

### Section 5: The Compounding Turn

- eip-verify micro-instance (summary → no benchmark → reviewer consumed polished version) → DIRECT (first-party worked cascade)
- Competence Shadow compounding argument (losses stack because human inspects machine-pruned space) → DIRECT (formal theory of cross-layer compounding)
- Broader 2024-2025 literature on automation bias compounding in multi-stage pipelines → SUPPORTING (web search confirmed multiple independent descriptions of cascade dynamics)

Assignment: adequate. Two direct sources and converging environmental literature. This is the section with the thinnest dedicated evidence, as expected. The micro-instance from eip-verify is the strongest anchor. The competence shadow's formal compounding argument provides the cross-layer theory. The environmental literature confirms the pattern is recognized independently.

### Section 6: Rival Hinge

- Can Domain Experts Rely on AI (2502.03482) → DIRECT (shows reliance failure cuts both ways)
- Stuck on Suggestions (2603.11821) → DIRECT (automation bias and anchoring under expert conditions)
- When Two Wrongs Don't Make a Right (2411.01007) → DIRECT (confirmation bias and time pressure)
- From Evidence to Decision (2402.01292) → HINGE (constructive alternative: hypothesis-driven vs. recommendation-driven)

Assignment: strong. Three direct sources plus one constructive hinge.

### Verdict: PASS

Every section has at least two direct sources. The compounding turn (Section 5) is the leanest, as predicted, but the eip-verify micro-instance plus the competence-shadow formal argument provide enough structural support. The evaluation-layer section has surplus evidence and should be compressed.

---

## Test 2: Type-Compatibility Test

Question: Can the first-party evidence (eip-verify) and the third-party behavioral studies coexist under one argument without epistemic type confusion?

### Assessment

The three evidence types carry different epistemic authority:

- **First-party project data** (eip-verify): inspectable, reproducible, pinned to specific commits. The reader can verify the claims. Authority comes from transparency and replicability.
- **Third-party benchmark papers** (tau-bench, WebSuite, WebForge, etc.): peer-reviewed or preprint, widely cited, specific empirical results. Authority comes from independent replication and methodological rigor.
- **Third-party behavioral studies** (persistence, skill formation, epistemic debt, competence shadow): randomized trials and observational studies across domains. Authority comes from causal design and sample sizes. Weakness: most are laboratory settings, not field deployments.

The combined essay must handle these type differences explicitly. Proposed approach:

1. **Opening (artifact layer)**: First-party evidence carries the opening because it is the most inspectable and least disputed. The reader starts with something they can verify.
2. **Middle (evaluation layer)**: Third-party benchmark papers carry this section. They provide the generalization that one project cannot.
3. **Escalation (human layer)**: Behavioral studies carry this section. Their laboratory setting is a weakness, but the causal design (randomized trials) gives them specific authority that observational field data would not.
4. **Compounding turn**: Uses the first-party case as a micro-instance, supported by the competence-shadow formal argument. This section explicitly acknowledges that the full cascade is a structural inference from converging evidence, not a single-study demonstration.

The essay should never smooth the type differences away. Each section should announce what kind of evidence it is presenting and what authority that evidence carries. The first-party case anchors the concrete. The benchmark papers provide scale. The behavioral studies provide human stakes. The compounding turn synthesizes them under explicit epistemic honesty.

### Verdict: PASS

The types are compatible if handled honestly. The risk would be treating them as equivalent. The draft must preserve the distinction.

---

## Test 3: Surplus Test

Question: Which inherited papers do NOT do body or hinge work in the combined essay and should be cut to footnote or dropped?

### Papers that earn body or hinge position:

- eip-verify first-party artifacts → body (Section 1, Section 5)
- Simhi et al. → body support (Section 1)
- tau-bench → body (Section 3)
- WebSuite → body (Section 3)
- WebForge → body (Section 3)
- Towards a Science of AI Agent Reliability → body (Section 3)
- AI Assistance Reduces Persistence → body (Section 4)
- How AI Impacts Skill Formation → body (Section 4)
- Mitigating Epistemic Debt → body (Section 4)
- The Competence Shadow → body (Section 4, Section 5)
- Can Domain Experts Rely on AI → hinge (Section 6)
- From Evidence to Decision → hinge (Section 6)

### Papers that should be footnote or cut:

- **MedRAGChecker**: supports the claim-level verification concept but the eip-verify case demonstrates this independently. Footnote at most.
- **Sackett et al. EBM**: useful precedent for evidence hierarchies but not essential when the eip-verify case provides a worked example. Footnote at most.
- **TheAgentCompany**: bounded usefulness data, but the evaluation section already has four stronger papers. Cut or single-sentence mention.
- **REAL**: same as TheAgentCompany. Cut or single-sentence mention.
- **LiveMCPBench**: tool-retrieval at scale is useful but not essential to the evaluation-layer argument. Cut or single-sentence mention.
- **From Task Solving to Robust Real-World Adaptation**: useful framing paper but the evaluation section doesn't need it when Reliability Science already carries the layer. Cut or footnote.
- **Stuck on Suggestions**: automation bias in pathology, but the hinge section already has sufficient support. Can be cut if space pressure demands.
- **When Two Wrongs Don't Make a Right**: confirmation bias and time pressure, but same as above. Can be cut if needed.

### Verdict: PASS

The combined evidence set is large but manageable. Twelve papers or evidence surfaces earn body or hinge position. Eight are cuttable. The draft should carry approximately 12 sources, not 20. The cut order in the blueprint already handles this correctly.

---

## Gate 2 Verdict

**PASS. All three tests clear.**

The evidence sets fuse cleanly under the cross-layer thesis. Every section has at least two direct sources. The type differences are manageable if the draft handles them honestly. The surplus is identified and the cut order is clear.

Key constraint for the draft: the evaluation section (Section 3) has the most evidence and the least emotional weight. It should be the leanest body section. The compounding turn (Section 5) has the least dedicated evidence but the most structural importance. It should rely on the eip-verify micro-instance and the competence-shadow formal argument rather than trying to accumulate additional papers.

## Next Gate

Proceed to Gate 3: Blueprint North-Star Check.
