{
  "title": "Confidence Flashcards",
  "cards": [
    {
      "front": "What is 'confidence debt' in an AI workflow?",
      "back": "It is the gap created when a system's output is trusted downstream before the evidence warrants that trust."
    },
    {
      "front": "How does confidence debt differ from technical debt?",
      "back": "Technical debt borrows speed by deferring structural cost, while confidence debt borrows trust by deferring evidence adjudication."
    },
    {
      "front": "What does a system borrow to incur 'epistemic debt'?",
      "back": "Assisted output is purchased by deferring understanding."
    },
    {
      "front": "In the eip-verify project, which artifact was found to be the 'most usable' despite being less accurate?",
      "back": "The polished narrative summary."
    },
    {
      "front": "Why is the 'polished version' of an AI artifact dangerous in a workflow?",
      "back": "It is easier to trust and move downstream while hiding contradictions found in row-level evidence."
    },
    {
      "front": "What governance rule did the eip-verify project implement to repair confidence debt?",
      "back": "Raw artifacts were mandated to outrank summaries and narrative readmes."
    },
    {
      "front": "How does the 'compression' of a claim contribute to the compounding of confidence debt?",
      "back": "Each downstream layer receives the confidence of a claim while losing the evidence texture and caveats that make it disputable."
    },
    {
      "front": "What is the 'First Gate' for paying down confidence debt?",
      "back": "Claim Auditability."
    },
    {
      "front": "According to Rasheed et al. (2026), what is the primary bottleneck for deep research agents once generation becomes cheap?",
      "back": "Tracing specific evidence to specific claims (auditability)."
    },
    {
      "front": "What are the four targets of 'claim auditability' suggested by Rasheed et al.?",
      "back": "Provenance coverage, provenance soundness, contradiction transparency, and audit effort at the claim level."
    },
    {
      "front": "What was the behavioral result of using the PaperTrail interface for scholarly Q&A?",
      "back": "Readers became more skeptical but did not necessarily perform the harder work of editing or verification."
    },
    {
      "front": "Why do Gilda and Gilda (2026) argue that architectural decision records need 'temporal validity'?",
      "back": "Because evidence can expire after a decision initially looks settled."
    },
    {
      "front": "What defines the 'artifact gate' in the confidence debt doctrine?",
      "back": "Deciding which kind of object (e.g., raw evidence vs. summary) is allowed to settle a claim."
    },
    {
      "front": "What is the 'Second Gate' for paying down confidence debt?",
      "back": "Reliability Release."
    },
    {
      "front": "In tau-bench, how does the pass rate for GPT-4o change from pass@1 to $pass^8$ in the retail domain?",
      "back": "It drops from approximately $61\\%$ to below $25\\%$."
    },
    {
      "front": "What is the operational difference between pass@1 and repeated-run reliability?",
      "back": "Pass@1 asks if a task can be done once; reliability asks if the system can be trusted to keep doing it."
    },
    {
      "front": "What are the three dimensions of the ReliabilityBench surface $R(k, \\epsilon, \\lambda)$?",
      "back": "Repeated-run consistency, robustness under task perturbation, and fault tolerance under production failures."
    },
    {
      "front": "How do Khanal, Tao, and Zhou (2026) define the risk of 'long-horizon' tasks for AI agents?",
      "back": "Errors accumulate over time, leading to reliability decay and variance amplification."
    },
    {
      "front": "What is 'Canonical Path Deviation' as described by Lee (2026)?",
      "back": "A failure mechanism where agent trajectories diverge from the paths typically associated with successful runs."
    },
    {
      "front": "What is a 'reliability release gate'?",
      "back": "A requirement to define an operating envelope (stability, faults, decay) before a score becomes a deployment claim."
    },
    {
      "front": "What is the 'Third Gate' for paying down confidence debt?",
      "back": "Co-Audit."
    },
    {
      "front": "According to Liu et al. (2026), how does AI assistance impact long-term human performance?",
      "back": "It improves immediate performance but reduces later unassisted performance and increases task abandonment."
    },
    {
      "front": "What interaction pattern split was found by Shen and Tamkin (2026) regarding AI and skill formation?",
      "back": "Conceptual engagement preserved skill, while treating the AI as a contractor and oneself as a reviewer impaired learning."
    },
    {
      "front": "What is the 'competence shadow' in safety engineering?",
      "back": "The risk that AI narrows the problem space, preventing humans from seeing hazards the AI omitted."
    },
    {
      "front": "How does Gordon et al. (2023) define 'co-audit'?",
      "back": "Tool-assisted human experiences specifically designed for checking AI-generated content after generation."
    },
    {
      "front": "What effect did 'plan-focused prompts' have in the study by Ghosh et al. (2026)?",
      "back": "They made assumptions explicit and reduced overreliance without increasing measured cognitive load."
    },
    {
      "front": "How does a 'hypothesis-driven' interface differ from a 'recommendation-first' interface?",
      "back": "It preserves comparisons and counterevidence rather than asking a human to simply accept or reject one answer."
    },
    {
      "front": "What is the primary goal of a co-audit workspace in high-stakes workflows?",
      "back": "To make structured correction easier than passive acceptance by exposing the AI answer as something to be worked against."
    },
    {
      "front": "How does confidence debt 'cascade' from artifacts to evaluators?",
      "back": "Evaluators inherit unexamined claims if they measure a polished artifact without checking it against raw evidence."
    },
    {
      "front": "What determines the amount of 'autonomy' a system receives in the confidence debt cascade?",
      "back": "The deployment decision, which is often based on an over-read or compressed benchmark score."
    },
    {
      "front": "What is 'appropriate reliance' as a rival frame to confidence debt?",
      "back": "A measure of how a person should weight AI advice at the specific moment of a decision."
    },
    {
      "front": "Why does the confidence debt frame begin 'earlier' than the appropriate reliance frame?",
      "back": "Reliance focus starts at the decision, while debt focus asks what evidence and reliability claims reached the user beforehand."
    },
    {
      "front": "What is the 'test' for whether a workflow has paid down confidence debt?",
      "back": "Whether the workflow preserved a concrete right of dispute for the claim, score, and answer."
    },
    {
      "front": "In the confidence debt doctrine, what must a promoted claim carry?",
      "back": "A visible evidence state, contradiction state, and expiry condition."
    },
    {
      "front": "The 'Evaluation Gate' prevents benchmark results from becoming release arguments until what is measured?",
      "back": "The relevant reliability envelope."
    },
    {
      "front": "What is the 'Human Gate's' core requirement for high-stakes AI output?",
      "back": "The provision of software that helps the reviewer see what the AI output hides or omits."
    },
    {
      "front": "Why is 'keep a human in the loop' considered a weak control for confidence debt?",
      "back": "A tired or biased reviewer looking at a fluent answer is not an effective governance mechanism without co-audit support."
    },
    {
      "front": "What does the term 'provenance soundness' refer to in claim auditability?",
      "back": "The degree to which the cited evidence actually supports the specific claim being made."
    },
    {
      "front": "What is a 'contradiction register' in the context of eip-verify?",
      "back": "A ledger tracking instances where different artifacts or evidence levels do not agree with each other."
    },
    {
      "front": "How does 'automation bias' relate to computational pathology studies?",
      "back": "Experts can be pulled toward incorrect machine advice due to anchoring on initial AI suggestions."
    },
    {
      "front": "What are the common failures of real agents that ReliabilityBench seeks to measure?",
      "back": "Timeouts, rate limits, schema drift, ambiguous instructions, and tool state changes."
    },
    {
      "front": "In long-horizon reliability, what is 'meltdown onset'?",
      "back": "The point at which accumulated errors cause an agent to move from partial progress into unrecoverable drift."
    },
    {
      "front": "Why does the doctrine suggest that co-audit workspaces should show evidence both 'for and against' a judgment?",
      "back": "To keep counter-hypotheses alive long enough for the reviewer to critically evaluate the machine's recommendation."
    },
    {
      "front": "What is the 'epistemic status' of an architectural decision?",
      "back": "The nature and strength of the knowledge or assumptions underlying that specific decision."
    },
    {
      "front": "What is the relationship between 'artifact compression' and 'evidence texture'?",
      "back": "Compression removes the texture (caveats, conflicts, nuances) as a claim moves from raw data to a summary."
    },
    {
      "front": "According to Ibrahim et al. (2025), why is mitigating overreliance necessary?",
      "back": "To build human-compatible AI systems that experts can use without being misled."
    },
    {
      "front": "What is 'audit effort' in the context of claim-level auditability?",
      "back": "The amount of work required for a human or system to verify a single claim against its evidence."
    },
    {
      "front": "How does the 'reliability envelope' differ from a 'leaderboard cell'?",
      "back": "An envelope covers a range of conditions and failure modes, whereas a leaderboard cell is often a single, clean-condition score."
    },
    {
      "front": "What is the risk of AI assistance for 'novice programmers' according to Sankaranarayanan (2026)?",
      "back": "It can create epistemic debt by allowing them to produce code without building the metacognitive skills to fix it later."
    },
    {
      "front": "What role does 'monitoring' play in the reliability release gate?",
      "back": "It ensures the system remains within its defined operating envelope post-deployment."
    },
    {
      "front": "Why is 'transparency' alone insufficient for claim auditability?",
      "back": "Generic transparency does not provide the granular, claim-level tracing needed to dispute specific outputs."
    },
    {
      "front": "In the eip-verify project, what percentage of direct-adjudication entries required follow-up in one model tier?",
      "back": "Thirteen out of fifteen entries."
    },
    {
      "front": "What does it mean for a claim to be 'promoted' in a debt-aware workflow?",
      "back": "It moves to a higher-visibility artifact (like a report) only after its evidence state is checked against lower-level artifacts."
    },
    {
      "front": "What is 'variance amplification' in long-horizon AI tasks?",
      "back": "The tendency for small initial errors to lead to increasingly large and unpredictable deviations over time."
    },
    {
      "front": "How does 'bounded autonomy' help manage confidence debt in production agents?",
      "back": "By limiting the agent's scope of action to areas where its reliability envelope is well-understood."
    },
    {
      "front": "Why is confidence debt described as a 'borrowed trust'?",
      "back": "Because the trust used to advance the output has not yet been 'earned' by rigorous evidence adjudication."
    },
    {
      "front": "What is 'AgentCompass' designed to analyze in agentic workflows?",
      "back": "It makes failures localizable and reusable across runs for post-deployment repair."
    },
    {
      "front": "In the Radiologist study by Chen et al. (2025), what was the unexpected finding regarding reliance?",
      "back": "Domain experts under-relied on a stronger AI system, showing that reliance issues are not always about over-trust."
    },
    {
      "front": "What constitutes 'raw evidence' in the eip-verify project?",
      "back": "Row-level mappings that connect protocol requirements to specific lines of implementation code."
    },
    {
      "front": "What is the primary danger of a 'recommendation-first' interface in high-stakes settings?",
      "back": "It encourages the human to passively 'rubber-stamp' the machine's primary suggestion."
    },
    {
      "front": "What is the 'right of dispute' in a governed AI execution?",
      "back": "The functional ability of a human to inspect, challenge, and correct any claim or decision made by the system."
    },
    {
      "front": "Why is 'calibration' of a model insufficient to prevent confidence debt?",
      "back": "A calibrated model can still be part of a workflow that prioritizes polished summaries over row-level evidence."
    },
    {
      "front": "In the 'Competence Shadow' theory, what is 'pruning the problem space'?",
      "back": "The process by which AI assistance excludes certain hazards or mitigations from the human's consideration set."
    },
    {
      "front": "What does the 'expiry condition' of a claim signify?",
      "back": "The point in time or change in context after which the evidence for the claim is no longer valid."
    },
    {
      "front": "What is the core takeaway of the 'Confidence Debt Doctrine'?",
      "back": "Trust becomes dangerous when output propagates downstream while the capacity to dispute it degrades."
    }
  ]
}