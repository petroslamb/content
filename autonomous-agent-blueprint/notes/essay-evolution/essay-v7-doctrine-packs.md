# V7 Doctrine Packs

These packs lock the doctrinal center for the `v7` rebuild. The `v6` bundle proved that the series had a real law stack. The `v7` job is to make that stack feel inevitable in public, reusable in design review, and distinct chapter by chapter instead of merely well disciplined.

If a `v7` draft wanders outside its pack, the extra material should move to the companion, the coverage map, or the blueprint layer.

## Launch

- Law: reliable agents come from explicit operating layers, not capability stacking
- Enemy mistake: starting the agent conversation with model taste instead of system boundaries
- Failure mode: a workflow looks impressive while vague action, weak observation, and late approval quietly determine the real incident
- Failure archetype: a team keeps swapping models and editing prompts while queued work is treated as completed work
- Decision rule: if a workflow still relies on human compensation to look reliable, the architecture is not finished
- Escalation rule: the moment a workflow touches tools, approvals, durable state, or hostile content, stop arguing about model taste and start diagnosing layers
- Architecture argument this chapter helps win: agent reliability should be discussed as system design rather than model shopping
- Bad default it makes harder to defend: "use a better model" as the first remedy for operational failure
- Quotable sentence: The model is usually the loudest part of the system and often the least useful place to start the postmortem.
- Anchor papers or source surfaces: `memgpt.md`, `react.md`, `autogen.md`, `greshake_indirect_prompt_injection.md`, `opro.md`
- Opening shape: postmortem vignette
- Ending job: install the doctrine standard and hand the reader to action without package plumbing

## Action

- Law: language becomes agency only when it becomes accountable state change
- Enemy mistake: treating tool use as a capability flourish instead of an interface and observation design problem
- Failure mode: wrong tool, wrong arguments, or queued-versus-complete confusion at the action boundary
- Failure archetype: a procurement workflow writes malformed arguments and then silently loses a real order because queued state is read as completion
- Decision rule: choose the narrowest action surface that still reaches the work
- Escalation rule: move from typed API to code or SQL, then to browser, then to GUI only when the cleaner surface cannot perform the task
- Architecture argument this chapter helps win: action reliability is governed more by the boundary than by model prestige
- Bad default it makes harder to defend: broader action surfaces are automatically more mature
- Quotable sentence: The assistant-agent boundary is crossed when language can create accountable state change outside the prompt.
- Anchor papers: `toolformer.md`, `gorilla.md`, `swe_agent.md`
- Opening shape: concrete operational failure
- Ending job: make uncertainty reduction feel like the deepest purpose of action

## Memory

- Law: memory is governance over time, not storage
- Enemy mistake: trying to solve stale or contaminated state with retrieval tuning alone
- Failure mode: stale memory reuse, wrong-layer writes, and authority that outlives its source
- Failure archetype: a policy assistant keeps surfacing retired rules because the store has no retirement, provenance, or derivation policy
- Decision rule: separate working, semantic, episodic, and procedural memory because they fail differently and deserve different controls
- Escalation rule: do not reach for richer retrieval structures until write policy, provenance, freshness, derivation, and forgetting are already explicit
- Architecture argument this chapter helps win: persistent state is a governance problem before it is a retrieval problem
- Bad default it makes harder to defend: bigger stores and better embeddings are enough to create memory
- Quotable sentence: A system that remembers without authority does not become wiser over time. It becomes harder to trust.
- Anchor papers: `memgpt.md`, `memorybank.md`, `mem0.md`
- Opening shape: quiet drift in a useful system
- Ending job: leave the reader with the present protected from the past

## Reasoning

- Law: most production reasoning failures are control failures before they are intelligence failures
- Enemy mistake: shopping for a stronger model when the workflow is badly staged
- Failure mode: first-pass overconfidence, planning without grounding, and search used as prestige cover
- Failure archetype: a claims workflow compresses dependent checks into one polished answer and fails under review because the live state was never queried and the first answer never earned trust
- Decision rule: diagnose the failure shape first, then install the lightest scaffold that corrects it
- Escalation rule: decomposition, then ReAct, then verification, then planner handoff, then search
- Architecture argument this chapter helps win: reasoning quality is largely a function of scaffold choice and review structure rather than raw model fluency
- Bad default it makes harder to defend: heavier reasoning methods are automatically more serious or more reliable
- Quotable sentence: If one generation is doing the work of several, a better model only buys a more polished mistake.
- Anchor papers: `least_to_most_prompting.md`, `react.md`, `chain_of_verification.md`, `llm_plus_p.md`, `tree_of_thoughts.md`
- Opening shape: artifact under review
- Ending job: make the escalation spine memorable enough to use in triage

## Multi-Agent

- Law: extra agents multiply ambiguity unless they create a real boundary
- Enemy mistake: adding roles to compensate for weak decomposition, weak artifacts, or weak approval design
- Failure mode: agent theater, unstructured handoff drift, and blame that gets harder to localize as the topology grows
- Failure archetype: a role-heavy software incident workflow ships the wrong rollback because permissions stay identical, handoffs stay conversational, and no typed artifact survives to review
- Decision rule: add another agent only when it buys a permission boundary, an independent critique, or a typed artifact handoff
- Escalation rule: keep the default single-agent until one of those three boundaries is clearly missing and measurable
- Architecture argument this chapter helps win: multi-agent design is justified by boundary economics rather than spectacle
- Bad default it makes harder to defend: more agents naturally mean more capability
- Quotable sentence: A second agent is not free intelligence. It is a boundary purchase, and the bill arrives as coordination debt.
- Anchor papers: `mad.md`, `metagpt.md`, `chatdev.md`, `autogen.md`, `reconcile.md`
- Opening shape: role-heavy technical workflow failure
- Ending job: normalize collapse discipline after deployment

## Safety

- Law: agent safety is trust-boundary design, not refusal theater
- Enemy mistake: treating prompt carefulness as the primary safety mechanism
- Failure mode: indirect prompt injection, retrieval poisoning, over-broad tool scope, and inter-agent contamination
- Failure archetype: untrusted retrieved content becomes an internal artifact and then a real side effect because the workflow never reset trust or narrowed reach
- Decision rule: model every channel by what trust it carries and what it can reach
- Escalation rule: widen autonomy only after trust separation, tool scope, handoff skepticism, deterministic checks, and approval are already explicit
- Architecture argument this chapter helps win: safety belongs inside workflow topology and tool boundaries rather than in a final filter
- Bad default it makes harder to defend: a careful prompt and a refusal layer are enough for integrated agents
- Quotable sentence: Once content can move through memory, tools, and handoffs, safety stops being a prompt problem and becomes an interface problem.
- Anchor papers: `greshake_indirect_prompt_injection.md`, `poisonedrag.md`, `toolemu.md`, `agentpoison.md`, `agentsmith.md`
- Opening shape: contamination chain
- Ending job: make restraint feel like a serious control rather than a timid compromise

## Optimization

- Law: the workflow is the object
- Enemy mistake: prompt churn without a stable objective or failure taxonomy
- Failure mode: visible editing on the easiest surface while the real problems live in evaluation, contracts, routing, and evidence quality
- Failure archetype: a useful workflow spends weeks rewriting prompts while downstream schemas, review burden, and failure classes drift
- Decision rule: lock the evaluation set and repair contracts before tuning wording
- Escalation rule: evaluation, then contracts and evidence, then prompts, then bounded feedback loops, then workflow search
- Architecture argument this chapter helps win: optimization is a systems measurement problem before it is a prompt craft problem
- Bad default it makes harder to defend: visible prompt edits are the main optimization lever
- Quotable sentence: If the objective is still moving, prompt work is just recency bias with better formatting.
- Anchor papers: `opro.md`, `mt_bench_chatbot_arena.md`, `voyager.md`, `textgrad.md`, `aflow.md`
- Opening shape: blunt claim followed by local optimization failure
- Ending job: leave the reader with one hard operator sentence rather than a bundle recap

## Bundle Discipline

- No more than three public essays may use a full team-failure cold open.
- Endings should accumulate. They must not all use the same "the next chapter" machinery.
- `## Selected Sources` is mandatory for every public essay.
- `## Sources Behind This Chapter` is mandatory for every companion.
- Companions extend. They do not paraphrase the public argument.
- If two chapters blur together when read in sequence, the bundle is not ready.
