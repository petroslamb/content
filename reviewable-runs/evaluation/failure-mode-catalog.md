# Failure Mode Catalog

This file catalogs the failure patterns that recur across agent systems and pairs them with likely causes and design responses.

In the reviewable-runs model, a failure review is one governance record type. It is not a universal output of every successful run. It matters after incidents, near misses, and deliberate postmortem or red-team exercises.

Applied failure reviews that use this taxonomy:

- [`../dossiers/enterprise-policy-memo/README.md`](../dossiers/enterprise-policy-memo/README.md)
- [`../dossiers/coding-bugfix-agent/README.md`](../dossiers/coding-bugfix-agent/README.md)
- [`../dossiers/web-form-agent/README.md`](../dossiers/web-form-agent/README.md)

## Memory Failures

### Memory sprawl

- Symptom: the agent stores too much low-value information and retrieval quality degrades.
- Likely cause: no write policy, no decay, no consolidation.
- Primary fix: add memory typing, pruning, and salience thresholds.

### Stale memory reuse

- Symptom: the agent keeps using outdated facts, policies, or prior assumptions.
- Likely cause: no freshness policy or provenance tracking.
- Primary fix: version memory and require source-aware retrieval.

### Wrong memory layer

- Symptom: task logs are treated like facts or playbooks are treated like chat history.
- Likely cause: no distinction between semantic, episodic, and procedural memory.
- Primary fix: separate memory classes and retrieval paths.

## Reasoning Failures

### First-pass overconfidence

- Symptom: the agent commits early to weak reasoning.
- Likely cause: no critique or verification layer.
- Primary fix: add self-refinement, CoVe, or external checks.

### Search overkill

- Symptom: the workflow becomes slow and brittle without a quality gain.
- Likely cause: search-heavy methods used on simple tasks.
- Primary fix: fall back to decomposition or ReAct unless the task truly branches.

### Planning without grounding

- Symptom: the agent reasons fluently but ignores environment feedback.
- Likely cause: verbal reasoning is not tied to observation.
- Primary fix: use a reason-act-observe loop.

## Action Failures

### Wrong tool or wrong arguments

- Symptom: the agent picks the wrong API or fills fields incorrectly.
- Likely cause: weak tool descriptions, weak schemas, weak argument checks.
- Primary fix: improve tool contracts and validation.

### Irreversible action without enough evidence

- Symptom: the agent sends, submits, writes, or deletes before verification.
- Likely cause: no approval gate and no deterministic check.
- Primary fix: require verification plus human approval for high-impact actions.

### Observation-action confusion

- Symptom: the agent mistakes a state summary for permission to act.
- Likely cause: page or environment content bleeds into the control loop.
- Primary fix: separate observation summaries from action policy.

## Optimization Failures

### Prompt churn without measurement

- Symptom: many edits, no stable quality gain.
- Likely cause: no fixed evaluation set.
- Primary fix: lock a benchmark task set before tuning.

### Premature workflow search

- Symptom: the architecture gets complex faster than it gets better.
- Likely cause: graph or topology optimization before baseline stability.
- Primary fix: optimize prompts, schemas, retrieval, and tool policies first.

## Multi-Agent Failures

### Agent theater

- Symptom: more agents exist, but no real role separation exists.
- Likely cause: multi-agent design used as a sophistication proxy.
- Primary fix: collapse back to one orchestrator or enforce real role boundaries.

### Unstructured handoff drift

- Symptom: agents pass ambiguous conversational state and errors compound.
- Likely cause: free-form coordination without typed artifacts.
- Primary fix: use structured handoffs, documents, or schemas.

## Safety Failures

### Indirect prompt injection

- Symptom: retrieved or external content changes agent behavior.
- Likely cause: instructions and data share the same trust status.
- Primary fix: trust separation plus action-policy enforcement.

### Retrieval poisoning

- Symptom: malicious or low-quality documents bias answers or actions.
- Likely cause: uncurated ingestion and weak corpus monitoring.
- Primary fix: provenance tracking, curation, anomaly review, and retrieval checks.

### Tool overreach

- Symptom: the agent uses tools with more permissions than the task requires.
- Likely cause: least privilege was not enforced.
- Primary fix: split read from write and narrow tool scopes.

### Inter-agent contamination

- Symptom: one agent's bad output, file, or screenshot becomes another agent's trusted input.
- Likely cause: inter-agent messages and attachments are treated as safe by default.
- Primary fix: treat inter-agent content and artifacts as untrusted and prefer structured handoffs with trust resets.

## Threat-Model Checklist

- [ ] Can untrusted content reach the planner unchanged?
- [ ] Can retrieved text override action policy?
- [ ] Can memory be poisoned or jammed without detection?
- [ ] Can the agent call a write-capable tool without deterministic checks?
- [ ] Can the system over-retain stale or low-value memory?
- [ ] Can one agent silently contaminate another through informal messages, files, or screenshots?
- [ ] Can a human approver see the evidence behind a proposed action?

## How To Use This File

- Use it before implementation to anticipate design risks.
- Use it during reviews to diagnose where the architecture is weak.
- Use it after incidents or near misses to label failures in a reusable way.
- Use it during deliberate exercises to decide whether a failure review should become a durable governance record.
