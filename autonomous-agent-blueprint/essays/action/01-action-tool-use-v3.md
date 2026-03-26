# Operating Agents I: When the Model Starts Doing Things

## Action, Tools, and the Boundary of Real Agency

A procurement team built an internal system that looked, in every review meeting, like an agent. It could read supplier policy, explain approval logic, draft the purchase-order payload, and tell an operator exactly what should happen next. The demos were impressive because the system sounded operational. It named the right fields, the right exceptions, and the right downstream systems.

Nothing happened until a human translated that prose into clicks and API calls.

So the team gave the system write access to the procurement service. The first failure was boring. The model filled `currency_code` with `USD dollars` instead of `USD`, and the schema rejected the request. The second failure was worse. A downstream service had changed how it reported deferred writes. The agent treated a partial acknowledgment as completion, moved on, and the order never landed. The supplier discovered the gap before the team did.

That is where the real agent problem starts. The step from assistant to agent is not the moment the model sounds more capable. It is the moment language becomes accountable state change.

Once a system can act, the design problem narrows and hardens. The important questions are no longer mainly about fluency or about reasoning in the abstract. They are about interfaces. What surface is the system allowed to touch? How are arguments validated? What comes back after the action? What permissions govern the call? How would you replay the event? How would you tell the difference between a completed write and a polite lie from the environment?

The strongest practical claim in this chapter is simple: action representation matters more than model capability for production reliability. [*Toolformer*](https://arxiv.org/abs/2302.04761) made tool use legible as part of the model's operating pattern. [*Gorilla*](https://arxiv.org/abs/2305.15334) made tool use look more like an interface-specification problem than a vague intelligence problem. [*SWE-agent*](https://arxiv.org/abs/2405.15793) showed why typed environments, executable artifacts, and machine-checkable feedback change the reliability conversation once the system actually acts. Put a strong model behind a vague action boundary and you will often get expensive failures that are hard to localize. Put a more ordinary model behind typed, observable, permissioned actions and you usually get something you can debug.

## Agency Starts at Accountable State Change

There is a flattering definition of agency that quietly distorts the engineering work. It says an agent is a system with sophisticated reasoning, long traces, tool access, memory, maybe planning, maybe a general feeling of autonomy. By that standard, elaborate prose already looks agentic.

The production definition is harsher and more useful. An agent is a system that can take a bounded action against an external surface, observe the result, and continue from what actually happened. If the system only describes the workflow and a human silently performs the workflow, the human is still the action layer.

That is why the jump from assistant to agent looks smaller in a demo than it feels in engineering. A demo only has to make intent sound plausible. A live system has to survive schemas, permission scopes, retries, stale outputs, deferred writes, partial failures, and ambiguous acknowledgments. The burden moves from rhetoric to interface design the moment the system can change state outside the prompt.

## Choose the Narrowest Surface That Still Reaches the Work

Once action is real, teams often make the next mistake quickly. They treat every broader surface as an upgrade in capability. In practice the opposite is usually true. Moving from typed APIs to browser automation to full GUI control is usually a decline in observability and reliability, tolerated only because the environment leaves you no cleaner path.

The default should therefore be stricter than most teams make it: choose the narrowest action surface that still reaches the work.

If a stable API exists, use it. If the work is software or repeatable transformation, code execution is often the right action surface because code can be tested, inspected, and replayed, which is exactly why [*SWE-agent*](https://arxiv.org/abs/2405.15793) remains such an important practical reference. If the work lives mainly in structured business data, SQL or a typed query layer is often the real operating surface even though consumer agent writing rarely treats it that way. Papers such as [*BIRD*](https://arxiv.org/abs/2305.03111) and [*Spider 2.0*](https://arxiv.org/abs/2411.07763) matter less as leaderboard artifacts than as reminders that enterprise data work is a first-class action surface. Browser action, as shown in work like [*A Real-World WebAgent*](https://arxiv.org/abs/2307.12856), is for systems that matter but do not expose usable interfaces. GUI action, which papers such as [*OmniParser*](https://arxiv.org/abs/2408.00203) make easier to discuss, is a fallback for closed environments, not a badge of generality.

The broader action chapter is wider than the operating cut used here. It also covers action learning and the full language, digital, and physical action spectrum. Those parts matter if you are surveying the literature. For most builders today, the practical center still sits in structured digital action, which is why the essay stays there.

## Action Surface Chooser

| Surface | Use it when | What it buys you | Escalate only if |
|---|---|---|---|
| Typed API | The target system exposes stable operations | Strong schemas, explicit permissions, replayable calls, clean logs | The required capability is missing |
| Code execution | The task is transformation, testing, or generation | Executable outputs, better verification, easier rollback | The task must touch an external system directly |
| SQL or typed queries | The work is mostly over structured data | Strong semantics, auditable writes, measurable correctness | Hidden UI logic or non-query action dominates |
| Browser automation | The system matters and has no usable API | Reach into real web flows with page-level state | DOM drift or visual ambiguity makes it too brittle |
| GUI automation | No cleaner interface exists | Access to otherwise closed systems | Any more structured surface becomes available |

The right reading of this table is not "which option is most powerful?" It is "which option lets me act with the least ambiguity?" That is the production question.

## Tool Use Breaks at Seams, Not in the Abstract

The literature on tool use matters because it breaks a vague capability word into smaller failures that can be named and instrumented.

First the system has to recognize that a tool is needed at all. [*Toolformer*](https://arxiv.org/abs/2302.04761) still matters here because it normalized the idea that tool invocation can be part of the model's operating pattern rather than an awkward add-on. Many systems stay too long in text because the model keeps trying to answer from plausibility instead of reaching for a live capability.

Then it has to choose the right tool. This is where [*Gorilla*](https://arxiv.org/abs/2305.15334) is still useful. The problem is not broad intelligence. It is discrimination across nearby interfaces.

Then it has to fill the arguments correctly. This is where many teams get fooled. The system understood the task, picked the right endpoint, and still created a bad write because one field drifted from the contract. That is not a mystical model failure. It is an argument-construction failure that should be visible in the logs and preventable at the schema boundary.

Then it has to execute inside the right boundary. A tool that can submit, delete, or send is not just another convenience. Least privilege, approval rules, and auditable execution are part of the action design itself.

Then it has to interpret the returned signal. This last seam is where otherwise competent systems fail in expensive ways. A queued job is read as a completed job. A warning is treated as success. A raw page message is treated as permission to proceed. If the result contract is weak, the next reasoning step proceeds from fiction.

If those seams are not named separately, every failure gets dumped into the lazy bucket called model behavior.

## The Observation Contract Is Half the Action Layer

Many teams design the call contract and neglect the observation contract. They decide what the model can send, but not what the model is allowed to conclude from what comes back.

That omission is costly. If tool results arrive as raw HTML, raw logs, or broad success text, the model has to infer too much. It may infer correctly often enough to look competent, which is exactly why this failure survives. A trustworthy action loop should not depend on whether the model guesses correctly about deferred writes, warning states, or retriable errors.

The fix is architectural. Important actions need observation contracts as explicit as their invocation contracts. What counts as success? What counts as partial success? What counts as a state that requires review?

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

This is one reason [*Toolformer*](https://arxiv.org/abs/2302.04761) matters conceptually and [*SWE-agent*](https://arxiv.org/abs/2405.15793) matters practically. The first normalizes tool use as part of the operating pattern. The second shows why inspectable environments, executable artifacts, and test feedback are so valuable once the system actually acts. The point is not that every agent should resemble a coding agent. The point is that typed action plus typed observation makes failure local, and local failure is what improvement depends on.

## What Holds Up Under Review

Most teams should start with a narrow action layer over typed APIs, search, or code. They should validate arguments before execution, return typed observations after execution, and instrument the major tool-use seams separately. That is not a conservative aesthetic preference. It is the fastest route to a failure surface you can actually reason about.

The escalation rule follows from the same logic. Broaden the surface only when the environment forces you to. Add browser control when the system that matters has no usable API. Add GUI control only when even the browser is not enough. Add more tools only when the current surface is a real bottleneck, not because broader capability sounds like maturity.

The hidden cost of premature surface expansion is not only security. It is diagnostic blur. Every new surface creates new ways to misunderstand what happened.

A convincing plan is not agency. Agency begins where the system can change state and be judged on the result. The first serious agent decision is therefore not about how smart the model seems. It is about how narrow and accountable the action boundary can remain.

## Resources And References

### [Builder Blueprint: Action Systems and Tool Use](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/03-action-tool-use-blueprint.md)

This blueprint matters because it turns the essay's thesis into concrete action-surface, tooling, and instrumentation choices for system design.

If you want the broader chapter and survey scope behind this essay, use the [companion note](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/action/companion.md) and the [series coverage map](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/essays/operating-agents-coverage-map.md).

### [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761) (2023)

*Toolformer* matters because it helped normalize tool use as part of the model's operating pattern rather than as an afterthought glued onto chat.

### [Gorilla: Large Language Model Connected with Massive APIs](https://arxiv.org/abs/2305.15334) (2023)

*Gorilla* matters because it treats tool use as a specification problem with distinct API-selection and argument-construction bottlenecks.

### [SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](https://arxiv.org/abs/2405.15793) (2024)

*SWE-agent* matters because software engineering makes typed, replayable action surfaces unusually visible, inspectable, and measurable.

### [BIRD: A Big Bench for Large-Scale Database Grounded Text-to-SQL](https://arxiv.org/abs/2305.03111) (2023)

*BIRD* matters because it frames SQL as a real enterprise action surface with accuracy, execution-safety, and observability constraints.

### [Spider 2.0: Evaluating Language Models on Real-World Enterprise Text-to-SQL Workflows](https://arxiv.org/abs/2411.07763) (2025)

*Spider 2.0* matters because it shows how quickly structured-data action becomes enterprise-shaped once schemas, conventions, and workflow context are realistic.

### [A Real-World WebAgent with Planning, Long Context Understanding, and Program Synthesis](https://arxiv.org/abs/2307.12856) (2024)

*WebAgent* matters because browser automation is a common escalation surface and comes with more fragility and ambiguity than typed APIs, SQL, or code.

### [OmniParser for Pure Vision Based GUI Agent](https://arxiv.org/abs/2408.00203) (2024)

*OmniParser* matters because GUI action is the cleanest example of reach increasing while structure and control decrease.
