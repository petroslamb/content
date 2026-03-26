# V6 Doctrine Packs

These packs lock the doctrinal center for each `v6` essay before drafting. If a draft wanders outside this frame, the extra material should move to the companion or be cut.

## Launch

- Law: reliable agents come from explicit operating layers, not capability stacking
- Enemy mistake: blaming model capability for failures that were created by vague boundaries, weak observation, or late approval
- Failure mode: action reliability and governance reviewability failures hidden inside "the model looked strong"
- Failure archetype: a team keeps swapping models and rewriting prompts while the real incident comes from queued work being treated as completed work
- Decision rule: if a workflow still relies on human compensation to look reliable, the architecture is not finished
- Escalation rule: stop talking about model taste and start diagnosing layers the moment the system touches tools, approvals, durable state, or hostile content
- Architecture argument this chapter helps win: agent reliability should be discussed as system design, not as model shopping
- Bad default it makes harder to defend: "use a better model" as the first remedy for operational failure
- Quotable sentence: The model is usually the most visible part of the system and often the least useful place to start the postmortem.
- Anchor papers or source surfaces: `advances-and-challenges-in-foundation-agents.md`, `reference/practical-distillation.md`, `reviewable-runs/evaluation/architecture-readiness-checklist.md`
- Dossier or use-case surface: the enterprise and web reviewable-run dossiers as proof that reviewable architecture lives outside the model
- Move to companion or package surfaces: extended source map, chapter-to-chapter routing, wider repo explanation, deeper sequencing rationale

## Action

- Law: language becomes agency only when it becomes accountable state change
- Enemy mistake: treating tool use as a vague capability upgrade instead of an interface and observation design problem
- Failure mode: wrong tool or wrong arguments, plus queued-versus-complete confusion
- Failure archetype: a procurement workflow writes malformed arguments, then silently loses a real order because queued state is read as completion
- Decision rule: choose the narrowest action surface that still reaches the work
- Escalation rule: move from typed APIs to code, SQL, browser, or GUI only when the cleaner surface cannot perform the task
- Architecture argument this chapter helps win: action reliability is governed more by the boundary than by model prestige
- Bad default it makes harder to defend: broader action surfaces are always a sign of more mature agency
- Quotable sentence: The assistant-agent boundary is not crossed when the model sounds operational. It is crossed when language can change state outside the prompt.
- Anchor papers: `toolformer.md`, `gorilla.md`, `swe_agent.md`
- Dossier or use-case surface: `reviewable-runs/examples/teaching/web-form-agent/README.md`, `implementation/use-cases/coding-agent.md`
- Move to companion: broader action taxonomy, browser and GUI frontier detail, physical action, action-learning literature, structured data as an extended action surface

## Memory

- Law: memory is governance over time, not storage
- Enemy mistake: trying to repair stale or contaminated memory with retrieval tuning alone
- Failure mode: stale memory reuse and wrong memory layer
- Failure archetype: a policy assistant keeps surfacing retired and superseded policy because the store has no retirement, provenance, or authority policy
- Decision rule: separate working, semantic, episodic, and procedural memory because they fail differently and need different controls
- Escalation rule: do not reach for richer retrieval structures until write policy, provenance, freshness, forgetting, and derivation are already explicit
- Architecture argument this chapter helps win: persistent state is a governance problem before it is a retrieval problem
- Bad default it makes harder to defend: larger stores and better embeddings are enough to create memory
- Quotable sentence: A system that never forgets does not become wiser over time. It becomes harder to trust.
- Anchor papers: `memgpt.md`, `memorybank.md`, `mem0.md`
- Dossier or use-case surface: `reviewable-runs/examples/teaching/enterprise-policy-memo/README.md`, `implementation/use-cases/enterprise-agent.md`
- Move to companion: human-memory analogy, Generative Agents depth, Reflexion as experience memory, procedural memory depth, graph-heavy retrieval, neuro-inspired memory framing

## Reasoning

- Law: most production reasoning failures are control failures before they are intelligence failures
- Enemy mistake: shopping for a stronger model when the workflow is badly staged
- Failure mode: first-pass overconfidence, planning without grounding, and search overkill
- Failure archetype: a claims workflow compresses dependent checks into one polished answer, then fails under review because the live state was never queried and the first answer never earned trust
- Decision rule: diagnose the failure shape first, then install the lightest scaffold that corrects it
- Escalation rule: decomposition -> ReAct -> verification -> planner handoff -> search
- Architecture argument this chapter helps win: reasoning quality is largely a function of scaffold choice and review structure, not of raw model fluency
- Bad default it makes harder to defend: heavier reasoning methods are automatically more serious or more reliable
- Quotable sentence: If the workflow asks one generation to do the work of several, a better model only hides the mistake longer.
- Anchor papers: `least_to_most_prompting.md`, `react.md`, `chain_of_verification.md`, `llm_plus_p.md`
- Dossier or use-case surface: `reviewable-runs/examples/teaching/enterprise-policy-memo/README.md`, `implementation/use-cases/enterprise-agent.md`
- Move to companion: Self-Refine, Reflexion, Self-Consistency, Step-Back, Tree of Thoughts, LATS, broader planning taxonomy

## Multi-Agent

- Law: extra agents multiply ambiguity unless they create a real boundary
- Enemy mistake: adding roles to compensate for weak decomposition, weak artifacts, or weak approval design
- Failure mode: agent theater and unstructured handoff drift
- Failure archetype: a split escalation workflow becomes slower and harder to localize because role handoffs stay conversational, permissions stay identical, and no typed evidence packet survives to the reviewer
- Decision rule: add another agent only when it buys one of three things: a permission boundary, an independent critique, or a typed artifact handoff
- Escalation rule: keep the default single-agent until one of those three boundaries is clearly missing and measurable
- Architecture argument this chapter helps win: multi-agent design is justified by boundary economics, not by spectacle or role count
- Bad default it makes harder to defend: more agents naturally mean more capability
- Quotable sentence: A second agent is not free intelligence. It is a boundary purchase, and the bill arrives as coordination debt.
- Anchor papers: `autogen.md`, `metagpt.md`, `mad.md`
- Dossier or use-case surface: `implementation/use-cases/enterprise-agent.md`, `reviewable-runs/evaluation/failure-mode-catalog.md`
- Move to companion: broader topology catalog, ChatDev, RECONCILE, protocol layer discussion, human-agent collaboration depth, evaluation breadth

## Safety

- Law: agent safety is trust-boundary design, not refusal theater
- Enemy mistake: treating a careful system prompt as the primary safety control
- Failure mode: indirect prompt injection, retrieval poisoning, and inter-agent contamination
- Failure archetype: untrusted retrieved content is treated as internal instruction, preserved, handed off, and finally converted into a real side effect
- Decision rule: model every channel by what trust it carries and what it can reach
- Escalation rule: widen autonomy only after trust separation, least privilege, handoff skepticism, deterministic checks, and approval are explicit
- Architecture argument this chapter helps win: safety belongs inside the workflow topology and tool boundary, not in a last-layer filter
- Bad default it makes harder to defend: prompt carefulness and a refusal policy are enough for integrated agents
- Quotable sentence: Once untrusted content can move through memory, tools, and handoffs, safety stops being a prompt-writing problem and becomes an interface problem.
- Anchor papers: `greshake_indirect_prompt_injection.md`, `poisonedrag.md`, `toolemu.md`
- Dossier or use-case surface: `reviewable-runs/examples/teaching/web-form-agent/README.md`, `implementation/use-cases/enterprise-agent.md`
- Move to companion: InjecAgent, AgentPoison, BadRAG, Agent Smith, supply-chain risk, perception threats, broader safety-scaling context

## Optimization

- Law: the workflow is the object
- Enemy mistake: prompt churn without a stable objective or failure taxonomy
- Failure mode: prompt churn without measurement and premature workflow search
- Failure archetype: a useful workflow spends weeks editing prompts while the real problems sit in evaluation design, schemas, routing, and evidence quality
- Decision rule: lock the evaluation set and repair contracts before tuning wording
- Escalation rule: evaluation -> contracts and evidence -> prompts -> bounded feedback loops -> workflow search
- Architecture argument this chapter helps win: optimization is a system-level measurement problem before it is a prompt-level creativity problem
- Bad default it makes harder to defend: visible prompt edits are the main optimization lever
- Quotable sentence: If the objective is still moving, prompt work is just recency bias with better formatting.
- Anchor papers: `opro.md`, `mt_bench_chatbot_arena.md`, `voyager.md`
- Dossier or use-case surface: `reviewable-runs/examples/teaching/coding-bugfix-agent/README.md`, `reviewable-runs/evaluation/architecture-readiness-checklist.md`
- Move to companion: TextGrad, Reflexion, AFLOW, GPTSwarm, judge calibration depth, broader workflow-search literature

## Kill-Switch Criteria

- If Launch still reads like package plumbing after the first draft, cut routing material until only the doctrine preface remains.
- If Reasoning still reads like a method survey after the first draft, remove every paragraph that does not directly defend scaffold diagnosis and move it to the companion.
- If Multi-Agent still reads like neutral classification after the first draft, strengthen the composite failure and cut any explanation that does not buy a sharper boundary argument.
- If any chapter cannot produce one sentence a builder could quote in design review, the draft is not ready for bundle-level revision.
