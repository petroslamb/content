# Confidence Debt Shipping-Practice Warrant Ledger

## Purpose

This ledger tests the missing debate bridge for R3:

> Do documented AI deployment practices rely on artifacts, evaluation results, and human oversight or approval as the ordinary objects through which teams decide that a system is governed enough to ship?

The question is narrower than the confidence-debt thesis. It does not ask whether these practices are bad. It asks whether the essay is allowed to attack the standard responsible shipping stack without building a straw man.

## Verdict

The bridge is earned, with a boundary.

The evidence supports saying that real deployment and governance practice commonly compresses AI readiness into artifacts, evaluation results, bounded execution controls, monitoring, and human review or approval. The evidence does not directly prove that stakeholders psychologically treat these controls as settled trust, or that these controls causally produce downstream failure. That step remains the essay's synthesis.

Safe framing:

> The same artifacts that make AI deployment governable can also become the surfaces through which confidence debt moves.

Unsafe framing:

> Most teams knowingly launder confidence through governance paperwork.

## Warrant Map

| ID | Practice Claim | Evidence | Support | Authorized Wording | Caveat | Essay Use |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W1 | Production agent teams rely on bounded autonomy, structured workflows, and human evaluation as practical deployment controls. | Pan et al., *Measuring Agents in Production* | Direct | In documented production-agent practice, teams commonly constrain autonomy, use structured workflows, and rely heavily on human evaluation. | Survey/interview evidence, not a universal census of all AI deployment. | Establishes that the target is real production practice, not a straw man. |
| W2 | Human review and approval are normal parts of production-agent evaluation and execution. | Pan et al., *Measuring Agents in Production* | Direct | Human-in-the-loop evaluation dominates the studied production-agent evaluation practices, and some production systems require experts to approve execution. | Human evaluation is reported as practice; the source does not prove it is sufficient. | Supports the "approval" token in the artifact-score-approval stack. |
| W3 | Real-world AI governance is implemented as workflow-level oversight patterns: thresholds, policies, standards, regulation, signoff, and human final-output control. | Jorgensen et al., *Documenting Deployment with Fabric* | Direct | Deployed AI governance often appears as oversight embedded in workflows, including human oversight levels and institutional oversight mechanisms. | Fabric has 20 use cases and acknowledged sampling limits. | Grounds the "responsible shipping stack" in observed governance mechanisms. |
| W4 | Deployment governance uses artifacts: diagrams, summaries, documentation, model/system cards, audit cards, factsheets, and workflow records. | Fabric; Eval Factsheets; Audit Cards; Evolving AI Risk Management | Direct/Hinge | Deployment practice depends on documentation artifacts that describe systems, evaluations, limitations, oversight, and residual risk. | Documentation quality varies; documentation is not proof of control effectiveness. | Supports artifact as a real governance token, not only an eip-verify artifact. |
| W5 | Evaluation results and metrics are explicitly connected to deployment, monitoring, go/no-go decisions, and post-deployment management. | NIST AI RMF GenAI; EDDOps; Eval Factsheets; Measuring Agents in Production | Direct/Hinge | Evaluation evidence is used across the AI lifecycle, including deployment approval, monitoring, decommissioning, and operational feedback loops. | Sources support evaluation as a governance surface; they do not prove every organization uses it well. | Supports the "score/dashboard/eval result" token. |
| W6 | Evaluation artifacts often hide assumptions, validity limits, judge choices, contamination checks, statistical procedures, and deployment-context mismatch. | Eval Factsheets; Audit Cards; NIST AI RMF 1.0; NIST AI RMF GenAI; EDDOps | Direct | Evaluation results need documented context because otherwise they are easy to misapply or overinterpret. | Do not claim all evaluations are opaque; the point is that opacity is a documented risk. | Lets the essay attack conversion of eval output into deployment confidence. |
| W7 | Human oversight is a standard control but must be designed, resourced, and monitored; it is not automatically a dispute mechanism. | Fabric; Measuring Agents in Production; NIST AI RMF 1.0; overreliance and appropriate-reliance sources | Synthesis with direct components | Human oversight is a real governance control, but confidence debt asks whether the reviewer receives the evidence and interface needed to dispute the AI output. | The source set supports the risk, not a single universal failure law. | Sharpens the human-gate attack without dismissing oversight. |
| W8 | The artifact-score-approval stack can become a trust-transfer machine when evidence limits are not preserved. | W1-W7 plus R3 core evidence | Synthesis | Responsible deployment controls become confidence-debt transfer points when they move trust farther than their evidence conditions travel. | This is the essay's synthesis, not a direct empirical finding. | Early debate bridge and possible R3 surgical insertion. |

## Source Notes

### Measuring Agents in Production

This is the strongest practice bridge already in the package. It reports 20 case studies and 306 practitioner survey responses, filtered in the main analysis to deployed production or pilot systems. Its most useful findings for this bridge are: production agents tend to use bounded autonomy, structured workflows, human oversight, A/B testing, user feedback, production monitoring, and human-in-the-loop evaluation. It directly supports the claim that responsible-looking deployment practice has ordinary tokens that can carry trust.

Use it to say: production teams already deploy through controlled execution, evaluation practice, and human review.

Do not use it to say: production teams have solved reliability, or human review proves safety.

### Documenting Deployment with Fabric

Fabric is the strongest governance-practice bridge from alphaXiv. It studies 20 deployed AI use cases through practitioner interviews and co-designed workflow diagrams. It categorizes human oversight into autonomous AI, conditionally autonomous AI, human-approved AI, and human-led with AI assistance; it also categorizes institutional oversight into ad-hoc practice, organization best practice, organization policy, industry standard, and regulation.

Use it to say: deployed AI governance is enacted through workflow artifacts, thresholds, policies, signoffs, and human final-output control.

Do not use it to say: these oversight mechanisms are empirically effective. The authors explicitly leave effectiveness as future work.

### Evaluation-Driven Development and Operations

EDDOps is useful because it names the lifecycle problem. It argues that LLM-agent evaluation cannot remain a terminal pre-deployment checkpoint because agents are open-ended, system-level, and shaped by operational context. It supports the claim that evaluation must become a continuous governing function that links offline testing, online monitoring, trace evidence, and governed redevelopment.

Use it to say: a score or pre-deployment benchmark is an incomplete governance object unless it remains connected to operational evidence.

Do not use it to say: the EDDOps process has been validated as a field-standard operating model.

### Eval Factsheets and Audit Cards

These sources authorize the documentation-risk side of the bridge. Eval Factsheets says evaluation methodologies often contain hidden assumptions about distributions, validity conditions, judge selection, contamination checks, and statistical validation. Audit Cards says even rigorous evaluations can be uninformative when reporting omits context such as auditor identity, scope, methodology, access, integrity, and review mechanisms.

Use them to say: evaluation results need context before they can guide deployment decisions.

Do not use them to say: every benchmark report is misleading.

### NIST AI RMF and GenAI Profile

NIST is useful as a mainstream governance anchor, not as a source for the essay's coinage. AI RMF 1.0 explicitly warns that measurement methods can be oversimplified, gamed, relied upon unexpectedly, or fail across contexts. The GenAI Profile connects structured feedback to deployment approval, go/no-go decisions, monitoring, and decommissioning, while warning that lab and benchmark tests may not extrapolate to real-world conditions.

Use it to say: established governance language already connects metrics, feedback, deployment approval, human oversight, monitoring, and context-specific risk.

Do not use it to say: NIST has the confidence-debt frame. It does not.

## Authorized Bridge Paragraph

Modern AI release practice rarely asks anyone to trust a model blindly. It offers a more respectable sequence. The output is packaged into an artifact someone can review. The artifact is supported by evaluation results, benchmarks, traces, red-team findings, user feedback, or monitoring. The release path adds bounded autonomy, escalation, human approval, or post-deployment oversight. Each move is rational. Raw traces are unreadable, decisions need compression, and organizations need accountable checkpoints. Confidence debt begins when those checkpoints are treated as settlement rather than transfer: when the artifact loses claim-level support, the score loses its measured envelope, and the human approval loses the evidence needed to dispute the output.

## Debate Implication

This bridge lets R3 attack how current teams ship without accusing them of recklessness. The sharper claim is:

> The problem is not that responsible teams ignore governance. The problem is that governance artifacts can become the way confidence debt travels.

This is stronger than "trust should not outrun evidence" because it implicates the responsible shipping stack itself. A product lead, eval engineer, policy owner, or human-factors researcher can disagree with it. That is the debate surface.

## R3 Edit Recommendation

Do not open a full R4 yet. The evidence supports a surgical R3 patch:

1. Add a compact bridge after the definition section that names the responsible shipping stack.
2. Replace any broad "ordinary practice" phrasing with "documented deployment practice" or "responsible-looking release practice."
3. Make the attack land on transfer, not bad faith: artifacts, scores, and approvals are useful controls until they are reused beyond the evidence they preserve.
4. Keep the caveat in the cascade or limits section: the trust-transfer step is the essay's synthesis from converging practice evidence, not a directly measured causal chain.

## Forbidden Overclaims

- Do not say most teams knowingly launder confidence.
- Do not say every benchmark dashboard becomes confidence debt.
- Do not say human oversight is fake or useless.
- Do not say the artifact-score-approval stack is universal across all AI deployment.
- Do not say the bridge has been proven by an end-to-end field study.
- Do not cite Fabric as evidence of governance effectiveness; it documents governance patterns.
- Do not cite EDDOps as a validated deployment doctrine; it is a process model and reference architecture.
