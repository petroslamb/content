# Operating Agents I: When the Model Starts Doing Things

A procurement team built an internal system that looked, in every review meeting, like an agent. It could read supplier policy, explain approval logic, draft the purchase-order payload, and tell an operator exactly what should happen next. The demos were impressive because the system sounded operational. It named the right fields, the right exceptions, and the right downstream systems.

Nothing happened until a human translated that prose into clicks and API calls.

So the team gave the system write access to the procurement service. The first failure was boring. The model filled `currency_code` with `USD dollars` instead of `USD`, and the schema rejected the request. The second failure was worse. A downstream service had changed how it reported deferred writes. The agent treated a partial acknowledgment as completion, moved on, and the order never landed. The supplier discovered the gap before the team did.

The real agent problem starts there. The step from assistant to agent is not the moment the model sounds more capable. It is the moment language becomes accountable state change.

Once a system can act, the design problem narrows and hardens. The important questions are no longer mainly about fluency or about reasoning in the abstract. They are about interfaces. What surface is the system allowed to touch? How are arguments validated? What comes back after the action? What permissions govern the call? How would you replay the event? How would you tell the difference between a completed write and a polite lie from the environment?

The strongest practical claim in this chapter is simple: action representation matters more than model capability for production reliability. *Toolformer* made tool use legible as part of a model's operating pattern. *Gorilla* made tool use look more like an interface-specification problem than a vague intelligence problem. *SWE-agent* showed why typed environments, executable artifacts, and machine-checkable feedback change the reliability conversation once the system actually acts (Schick et al.; Patil et al.; Yang et al.). Put a strong model behind a vague action boundary and you will often get expensive failures that are hard to localize. Put a more ordinary model behind typed, observable, permissioned actions and you usually get something you can debug.

## Agency Starts At The Action Boundary

There is a flattering definition of agency that quietly distorts the engineering work. It says an agent is a system with sophisticated reasoning, long traces, tool access, memory, maybe planning, maybe a general feeling of autonomy. By that standard, elaborate prose already looks agentic.

The production definition is harsher and more useful. An agent is a system that can take a bounded action against an external surface, observe the result, and continue from what actually happened. If the system only describes the workflow and a human silently performs the workflow, the human is still the action layer.

That is why the jump from assistant to agent looks smaller in a demo than it feels in engineering. A demo only has to make intent sound plausible. A live system has to survive schemas, permission scopes, retries, stale outputs, deferred writes, partial failures, and ambiguous acknowledgments. The burden moves from rhetoric to interface design the moment the system can change state outside the prompt.

## Choose The Narrowest Surface That Still Reaches The Work

Once action is real, teams often make the next mistake quickly. They treat every broader surface as an upgrade in capability. In practice the opposite is usually true. Moving from typed APIs to browser automation to full GUI control is usually a decline in observability and reliability, tolerated only because the environment leaves you no cleaner path.

Use the narrowest action surface that still reaches the work.

If a stable API exists, use it. If the work is software or repeatable transformation, code execution is often the right action surface because code can be tested, inspected, and replayed. If the work lives mainly in structured business data, SQL or a typed query layer is often the real operating surface even though consumer agent writing rarely treats it that way. Browser action matters when the system of record is web-native and no usable API exists. GUI action is a fallback for closed environments, not a badge of generality (Li et al.; Lei et al.; Deng et al.; Gu et al.).

The practical question is not which surface looks most agentic. It is which surface gives the strongest contract around scope, execution, and observation.

## Tool Use Breaks At Seams, Not In Capability Scores

The literature on tool use matters because it breaks a vague capability word into smaller failures that can be named and instrumented.

First the system has to realize that a tool is needed at all. Many systems stay too long in text because the model keeps trying to answer from plausibility instead of reaching for a live capability. That is still the useful lesson of *Toolformer*.

Then it has to choose the right tool. *Gorilla* remains useful here. The problem is not broad intelligence. It is discrimination across nearby interfaces.

Then it has to bind the arguments correctly. This is where many teams get fooled. The system understood the task, picked the right endpoint, and still created a bad write because one field drifted from the contract. That is not a mystical model failure. It is an argument-construction failure that should be visible in the logs and preventable at the schema boundary.

Then it has to execute inside the right boundary. A tool that can submit, delete, or send is not just another convenience. Least privilege, approval rules, and auditable execution are part of the action design itself.

Then it has to interpret the returned signal. This last seam is where otherwise competent systems fail in expensive ways. A queued job is read as a completed job. A warning is treated as success. A raw page message is treated as permission to proceed. If the result contract is weak, the next reasoning step proceeds from fiction.

If those seams are not named separately, every failure gets dumped into the lazy bucket called model behavior.

## The Observation Contract Is Half The Action Layer

Many teams design the call contract and neglect the observation contract. They decide what the model can send, but not what the model is allowed to conclude from what comes back.

That omission is costly. If tool results arrive as raw HTML, raw logs, or broad success text, the model has to infer too much. It may infer correctly often enough to look competent, which is exactly why this failure survives. A trustworthy action loop should not depend on whether the model guesses correctly about deferred writes, warning states, or retriable errors.

Important actions need observation contracts as explicit as their invocation contracts. What counts as success. What counts as partial success. What counts as a state that requires review.

```json
{
  "status": "deferred",
  "write_applied": false,
  "reason_code": "WAITING_APPROVAL",
  "requires_review": true,
  "next_allowed_action": "poll_after_approval"
}
```

A status object like that gives the reasoning layer something usable. A dump of raw environment text gives it noise and false confidence.

## Use Action To Reduce Uncertainty

The action chapter becomes most useful where it stops treating action as the end of a pipeline and starts treating it as a way to reduce uncertainty before that uncertainty becomes expensive.

Before submitting a purchase order, validate the payload against the schema. Before relying on retrieved policy, check freshness. Before assuming a background job finished, poll the status endpoint. Before retrying a failed call, inspect what the endpoint actually expects. Good agents do not only act to complete a task. They also act to learn what state they are actually in.

That shift matters because it changes what the next essay has to solve. Once a workflow can act reliably enough to matter, continuity pressure arrives immediately. The system now needs rules for what it should remember about its own past.

## Action Surface Chooser

| Surface | Use it when | What it buys you | Escalate only if |
|---|---|---|---|
| Typed API | The target system exposes stable operations | Strong schemas, scoped permissions, replayable calls, clean logs | The needed capability is missing |
| Code execution | The task is transformation, testing, or reproducible generation | Executable output, local verification, easier rollback | The task must touch an external UI |
| SQL or typed queries | The work lives in structured data | Strong semantics, auditable results, measurable failure | The task depends on state not exposed by the data layer |
| Browser automation | The system of record is web-native and lacks a useful API | Reach into real web workflows | The site is too brittle or visually ambiguous |
| GUI automation | Every cleaner interface is unavailable | Access to otherwise closed systems | A stronger interface becomes available |

Broader surfaces are usually more expensive and less legible. Treat them that way.

## The Review Standard

The most durable contribution of the action literature is not that models can now call tools. It is that tool use changes what reliability means. Once the system can act, quality is no longer only about whether the output reads well. It is about whether the action boundary is typed, the permissions are bounded, the result is interpretable, and the whole event can be reconstructed after failure.

That is why the practical center of the chapter sits in structured digital action. Physical action, multimodal orchestration, and action-learning frontiers matter, but they belong in the surrounding layer rather than at the center of a public builder essay. Most teams today do not need a sweeping theory of action. They need a stricter rule for when language becomes real work.

## Resources And References

### [Builder Blueprint: Action Systems and Tool Use](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/03-action-tool-use-blueprint.md)

This blueprint turns the essay's argument into defaults, escalation rules, and anti-patterns for choosing action surfaces and designing observation contracts.

### [Action Companion](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/action/companion.md)

The companion restores the wider action chapter: tool discovery and creation, action-learning frontiers, broader surface taxonomy, and the surrounding paper terrain that would have weakened the public essay's center.

### [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761)

Toolformer matters because it normalized the idea that tool use can be part of a model's operating pattern rather than a purely external wrapper.

### [Gorilla: Large Language Model Connected with Massive APIs](https://arxiv.org/abs/2305.15334)

Gorilla matters because it makes tool use look like interface selection and argument construction rather than a mystical intelligence benchmark.

### [SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](https://arxiv.org/abs/2405.15793)

SWE-agent matters because it shows how strong interfaces, replayability, and executable feedback change the reliability conversation once the system acts.

### [BIRD: A Big Bench for Large-Scale Database Grounded Text-to-SQL](https://arxiv.org/abs/2305.03111) and [Spider 2.0: Evaluating Language Models on Real-World Enterprise Text-to-SQL Workflows](https://arxiv.org/abs/2411.07763)

These papers matter because they treat structured data work as a first-class action surface with real execution and observability constraints.

### [A Real-World WebAgent with Planning, Long Context Understanding, and Program Synthesis](https://arxiv.org/abs/2307.12856) and [OmniParser for Pure Vision Based GUI Agent](https://arxiv.org/abs/2408.00203)

These papers matter because they show the two most common escalation surfaces once typed digital interfaces run out: browser automation and GUI fallback.
