# Chapter 8 Blueprint: Action Systems and Tool Use

## Use This Blueprint When

Use this blueprint when language stops being descriptive and starts changing state through software. The key question is not whether the agent can act in the abstract. It is what surface it should act on, how that action should be represented, and how the result should be observed, checked, and replayed.

## The Decision

Action design has to answer three questions:

1. What is the narrowest action surface that reaches the target system?
2. In what representation should actions be expressed?
3. How do execution, observation, recovery, and approval fit back into the loop?

These questions decide whether the workflow is reviewable or theatrical.

## Default Position

The default action policy should be strict.

- Prefer the narrowest machine-readable surface available.
- Prefer typed calls, SQL, or executable code over free-form text.
- Treat action contracts, observation contracts, and permission boundaries as part of one design.
- Add browser action only when usable APIs are absent.
- Add GUI action only when every cleaner surface is unavailable.

An agent becomes operational when it can produce bounded, replayable state change. That is the real threshold between assistant behavior and agent behavior.

## Default Build

### Surface Selection

Choose the cleanest available interface in this order:

1. Typed API tools
2. Database or SQL interfaces for data-centric work
3. Code execution when reproducibility and testability matter
4. Browser automation when the web flow is the real system of record
5. GUI automation only for constrained legacy or closed systems

### Action Representation

Represent actions as typed calls, SQL, executable code, or constrained UI steps. Plain-text action plans should be treated as an intermediate artifact, not the final execution object.

### Execution Boundary

Run actions in a least-privilege, sandboxed environment. Separate read, write, and destructive actions by policy. Action selection and action authorization should not collapse into one hidden step.

### Observation Boundary

Return normalized, typed observations to the reasoning loop rather than dumping raw tool output back into the model. Good action systems are as much about clean observations as clean calls.

### Recovery And Approval

Represent failure states explicitly: invalid arguments, unavailable tool, stale selector, partial success, permission refusal, exhausted retry budget. Approval belongs at the action boundary wherever the downside of silent automation exceeds the cost of inspection.

## Escalate When

- A clean API is unavailable but the web system still exposes stable enough structure.
- The task is fundamentally data-centric and should move to SQL or structured query instead of general tool use.
- The work must be reproducible, testable, or reviewable as code.
- Browser flows are still insufficient because the environment exposes only human-facing UI state.
- Tool selection and argument construction are failing because the catalog, schemas, or permission model are too weak.

## Alternatives And When They Win

| Surface | Best use | Why it wins | Main risk |
| --- | --- | --- | --- |
| Typed API tools | business systems with good interfaces | strongest replayability and inspection | wrong tool or wrong parameters if schemas are weak |
| Database or SQL action | analytics and structured data work | measurable outputs and strong contracts | schema drift or unsafe query behavior |
| Code execution | software and repeatable data tasks | executable, testable, and reviewable | unsafe scope without strong containment |
| Browser action | web-native workflows without usable APIs | reaches real systems of record | brittle selectors and weaker contracts |
| GUI action | closed or legacy interfaces | reaches surfaces nothing else can | highest fragility and weakest observability |

## What To Measure

- Tool selection accuracy
- Argument accuracy
- Action success rate
- Recovery rate after failure
- Retry count
- Latency and cost per action
- Replayability and auditability

The right action metric is whether the system executed the right step safely and reproducibly, not whether the final answer sounded competent.

## Failure Review

- Using free-form text where typed action was possible
- Giving one agent every tool and every permission
- Treating raw tool output as final truth
- Failing to normalize observations before returning them to the loop
- Using browser or GUI action where a narrower surface existed
- Shipping action layers without logs, replay, and approval seams

## Reading Sequence

1. `../../essays/action/01-action-tool-use.md`
2. `../../essays/action/companion.md`
3. `../../reference/papers/toolformer.md`
4. `../../reference/papers/gorilla.md`
5. `../../reference/papers/hugginggpt.md`
6. `../../reference/papers/webagent.md`
7. `../../reference/papers/mind2web.md`
8. `../../reference/papers/swe_agent.md`
9. `../../reference/papers/bird.md`
10. `../../reference/papers/spider_2_0.md`
11. `../../reference/papers/mobile_agent.md`
12. `../../reference/papers/appagent.md`
13. `../../reference/papers/omniparser.md`
14. `../../reference/papers/opendevin.md`

Return to survey sections `8.3.1`, `8.3.2`, and `8.3.3` when you need the wider action and tool taxonomy behind these defaults.

## Bottom Line

Choose the narrowest surface that can still do the job, represent actions in a form that software can validate and replay, and make observation, recovery, and approval explicit. Structured action is what makes agent behavior real.
