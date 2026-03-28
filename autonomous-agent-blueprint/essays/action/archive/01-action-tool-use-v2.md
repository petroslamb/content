# Operating Agents I: When the Model Starts Doing Things

## Action, Tools, and the Boundary of Real Agency

A procurement team built an internal system that looked, in every review meeting, like an agent. It could read supplier policy, explain approval logic, draft the purchase-order payload, and tell an operator exactly what should happen next. The demos were impressive because the system sounded operational. It named the right fields, the right exceptions, and the right downstream systems.

Nothing happened until a human translated that prose into clicks and API calls.

So the team gave the system write access to the procurement service. The first failure was boring. The model filled `currency_code` with `USD dollars` instead of `USD`, and the schema rejected the request. The second failure was worse. A downstream service had changed how it reported deferred writes. The agent treated a partial acknowledgment as completion, moved on, and the order never landed. The supplier discovered the gap before the team did.

That is where the real agent problem starts. The step from assistant to agent is not the moment the model sounds more capable. It is the moment language becomes accountable state change.

Once a system can act, the design problem narrows and hardens. The important questions are no longer mainly about fluency or even about reasoning in the abstract. They are about interfaces. What surface is the system allowed to touch? How are arguments validated? What comes back after the action? What permissions govern the call? How would you replay the event? How would you tell the difference between a completed write and a polite lie from the environment?

The strongest practical claim in this chapter is simple: action representation matters more than model capability for production reliability. A stronger model connected to a vague action boundary usually fails in ways that are hard to localize. A more ordinary model connected to typed, observable, permissioned actions can often be debugged, corrected, and improved.

## Agency Starts At Accountable State Change

There is a flattering definition of agency that quietly distorts the engineering work. It says an agent is a system with sophisticated reasoning, long traces, tool access, memory, maybe some planning, and a general feeling of autonomy. By that standard, elaborate prose already looks agentic.

The production definition is harsher and more useful. An agent is a system that can take a bounded action against an external surface, observe the result, and continue from what actually happened. If the system only describes the workflow and a human silently performs the workflow, the human is still the action layer.

That is why the jump from assistant to agent looks smaller in a demo than it feels in engineering. A demo only has to make intent sound plausible. A live system has to survive schemas, permission scopes, retries, stale outputs, deferred writes, partial failures, and ambiguous acknowledgments. The burden moves from rhetoric to interface design the moment the system can change state outside the prompt.

## Choose The Narrowest Surface That Still Reaches The Work

Once action is real, teams often make the next mistake quickly. They treat every broader surface as an upgrade in capability. In practice the opposite is usually true. Moving from typed APIs to browser automation to full GUI control is usually a decline in observability and reliability, tolerated only because the environment leaves you no cleaner path.

The default should therefore be stricter than most teams make it: choose the narrowest action surface that still reaches the work.

If a stable API exists, use it. If the work is software or repeatable transformation, code execution is often the right action surface because code can be tested, inspected, and replayed. If the work lives mainly in structured business data, SQL or a typed query layer is often the real operating surface even though consumer agent writing rarely treats it that way. Browser action is for systems that matter but do not expose usable interfaces. GUI action is a fallback for closed environments, not a badge of generality.

## Action Surface Chooser

| Surface | Use it when | What it buys you | Escalate only if |
|---|---|---|---|
| Typed API | The target system exposes stable operations | Strong schemas, clear logs, explicit permissions, replayable calls | The required capability is missing |
| Code execution | The task is transformation, testing, or generation | Executable outputs, stronger verification, easier rollback | The task must touch an external system directly |
| SQL or typed queries | The work is mostly over structured data | Strong semantics, auditable writes, measurable correctness | Hidden UI logic or non-query action dominates |
| Browser automation | The system matters and has no usable API | Reach into real web flows with page-level state | DOM drift or visual ambiguity makes it too brittle |
| GUI automation | No cleaner interface exists | Access to otherwise closed systems | Any more structured surface becomes available |

The right reading of this table is not "which option is most powerful?" It is "which option lets me act with the least ambiguity?" That is the production question.

## Tool Use Breaks At Seams, Not In The Abstract

The literature on tool use matters because it breaks a vague capability word into smaller failures that can be named and instrumented.

First the system has to recognize that a tool is needed at all. Many systems stay too long in text because the model keeps trying to answer from plausibility instead of reaching for a live capability.

Then it has to choose the right tool. This is where work like *Gorilla* matters. The problem is not broad intelligence. It is discrimination across nearby interfaces.

Then it has to fill the arguments correctly. This is where many teams get fooled. The system understood the task, picked the right endpoint, and still created a bad write because one field drifted from the contract.

Then it has to execute inside the right boundary. A tool that can submit, delete, or send is not just another convenience. Least privilege, approval rules, and auditable execution are part of the action design itself.

Then it has to interpret the returned signal. This last seam is where otherwise competent systems fail in expensive ways. A queued job is read as a completed job. A warning is treated as success. A raw page message is treated as permission to proceed. If the result contract is weak, the next reasoning step proceeds from fiction.

If those seams are not named separately, every failure gets dumped into the lazy bucket called model behavior.

## The Observation Contract Is Half The Action Layer

Many teams design the call contract and neglect the observation contract. They decide what the model can send, but not what the model is allowed to conclude from what comes back.

That omission is costly. If tool results arrive as raw HTML, raw logs, or broad success text, the model has to infer too much. It may infer correctly often enough to look competent, which is exactly why this failure survives. A trustworthy action loop should not depend on whether the model guesses correctly about deferred writes, warning states, or retriable errors.

The fix is architectural. Important actions need observation contracts as explicit as their invocation contracts. What counts as success? What counts as partial success? What counts as a state that requires review? A typed status object with normalized error reasons gives the reasoning layer something usable. A dump of raw environment text gives it noise and false confidence.

This is one reason *Toolformer* matters conceptually and *SWE-agent* matters practically. The first normalizes tool use as part of the operating pattern. The second shows why inspectable environments, executable artifacts, and test feedback are so valuable once the system actually acts. The point is not that every agent should resemble a coding agent. The point is that typed action plus typed observation makes failure local, and local failure is what improvement depends on.

## The Default That Holds Up

Most teams should start with a narrow action layer over typed APIs, search, or code. They should validate arguments before execution, return typed observations after execution, and instrument the major tool-use seams separately. That is the default because it creates the cleanest failure surface.

The escalation rule follows from the same logic. Broaden the surface only when the environment forces you to. Add browser control when the system that matters has no usable API. Add GUI control only when even the browser is not enough. Add more tools only when the current surface is a real bottleneck, not because broader capability sounds like maturity.

The hidden cost of premature surface expansion is not only security. It is diagnostic blur. Every new surface creates new ways to misunderstand what happened.

A convincing plan is not agency. Agency begins where the system can change state and be judged on the result. That is why the first serious agent decision is not about how smart the model seems. It is about how narrow and accountable the action boundary can remain.

## Resources And References

*Toolformer* matters because it changes tool use from an integration detail into part of the model's operating pattern. It is the cleanest bridge from fluent text to structured external action.

*Gorilla* matters because it turns tool use into a specification problem. Its real value is showing that tool selection and argument construction are separable bottlenecks rather than one blurry capability.

*SWE-agent* is the strongest practical paper in this cluster because code, shell commands, and tests make action and observation unusually inspectable. It shows why replayable environments change the reliability conversation.

*Spider 2.0* belongs here because enterprise data work is one of the most important real action surfaces, and the paper shows how quickly structured action becomes hard once schemas and workflows become realistic.
