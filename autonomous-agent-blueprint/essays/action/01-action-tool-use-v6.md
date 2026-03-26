# Operating Agents I: When the Model Starts Doing Things

A procurement team built an internal system that looked, in every review meeting, like an agent. It could read supplier policy, explain approval logic, draft the purchase-order payload, and tell an operator exactly what should happen next. The demos were impressive because the system sounded operational. It named the right fields, the right exceptions, and the right downstream systems.

Nothing happened until a human translated that prose into clicks and API calls.

So the team gave the system write access to the procurement service. The first failure was boring. The model filled `currency_code` with `USD dollars` instead of `USD`, and the schema rejected the request. The second failure was worse. A downstream service had changed how it reported deferred writes. The agent treated a partial acknowledgment as completion, moved on, and the order never landed. The supplier discovered the gap before the team did.

That is where agency begins in practice. Not when the model sounds more capable. When language becomes accountable state change.

## The Boundary Is The System

There is a flattering way to talk about tool use that quietly ruins design work. It says an agent is a system with sophisticated reasoning, memory, and the ability to call tools when needed. That definition is so broad that an elaborate assistant already looks agentic. It is also too soft to help a builder decide what has changed.

The harsher definition is better. An agent is a workflow that can take a bounded action against an external surface, observe the result, and continue from what actually happened. If the system only describes the workflow and a human silently performs the workflow, the human is still the action layer.

That change also raises the quality bar. Once a system can act, the decisive questions are no longer mainly about fluency. They are about boundary design. What surface is the system allowed to touch. How are arguments validated. What comes back after the action. What permissions govern the call. How would you replay the event. How would you tell the difference between completed work and a polite lie from the environment.

This is the first law of the bundle because it is the first law most demos let you ignore. Language starts to look like work long before it can survive doing work.

## Toolformer, Gorilla, And SWE-agent Changed The Argument

The action literature became practically useful when it stopped treating tool use as a mystical extension of model intelligence and started treating it as an operating pattern with visible seams.

[*Toolformer*](https://arxiv.org/abs/2302.04761) mattered because it attacked a simple problem that kept getting flattened in public discussion. Models were too willing to answer from plausibility when an external capability was needed. The paper's important move was not that it solved every tool workflow. It normalized the idea that reaching for a tool is part of competence rather than an embarrassing external wrapper.

[*Gorilla*](https://arxiv.org/abs/2305.15334) arrived when plugin talk and API excitement were running ahead of operational discipline. Its real contribution was to narrow tool use down to interface discrimination and argument construction. That sounds less glamorous than "agentic behavior." It is also much closer to how production failures actually appear. The task was understood. The wrong endpoint was chosen. The right endpoint was called with the wrong field shape. A changing spec outran a stale interface assumption.

[*SWE-agent*](https://arxiv.org/abs/2405.15793) changed the conversation again by showing what happens when the action surface itself becomes inspectable. Code edits, shell actions, tests, and machine-checkable feedback make the agent's moves replayable in a way that prose never is. The lesson is broader than software. Narrower and harsher interfaces often beat broader and more theatrical ones because they make failure local, and local failure is what improvement depends on.

Taken together, these papers moved the argument away from "can the model use tools" and toward a colder question: what kind of action boundary lets a system fail in ways a builder can still diagnose.

## Most Action Failures Happen At Named Seams

Production systems do not fail at tool use in the abstract. They fail at seams.

Sometimes the seam is tool need detection. The workflow stays in prose too long and answers from plausibility when it should have reached for live state. Sometimes the seam is tool selection. Several interfaces look close enough that the wrong one gets chosen even though the task itself was understood. Sometimes the seam is argument construction. The right surface gets called with the wrong enum, unit, or field shape, which is exactly what happened to `currency_code` in the procurement workflow.

Then comes execution scope. A tool that can search docs should not share the same trust posture as a tool that can submit a purchase order, delete a record, or send a customer-facing message. Least privilege is not a security afterthought here. It is part of the action architecture itself.

The last seam is result interpretation, and it is the one teams underrate most often. A queued job is read as a completed job. A warning is treated as success. A partially rendered browser state is treated as permission to proceed. A raw environment message becomes control policy by accident. If the observation side of the boundary is weak, the next reasoning step proceeds from fiction.

That seam-by-seam view is more useful than almost any benchmark summary because it tells you what to instrument. If the system keeps choosing the wrong tool, strengthen the catalog and the retrieval layer around it. If it chooses correctly but fills arguments badly, fix schemas and validation. If it keeps moving forward on ambiguous state, strengthen the observation contract. The lazy move is to call all of this "model behavior" and go shopping again.

## The Observation Contract Is Half The Action Layer

Many teams define what the model can send and barely define what the model is allowed to conclude from what comes back.

That omission is costly. If tool results arrive as raw HTML, raw logs, or broad success language, the model has to infer too much. It may infer correctly often enough to look competent, which is exactly why the failure survives. A trustworthy action loop should not depend on whether the model happens to guess correctly about deferred writes, warning states, or retriable errors.

Important actions need observation contracts as explicit as their invocation contracts.

```json
{
  "status": "queued",
  "write_applied": false,
  "reason_code": "WAITING_APPROVAL",
  "requires_review": true,
  "next_allowed_action": "poll_after_approval"
}
```

That object is doing more than reporting state. It is telling the reasoning layer what reality now allows. A raw text message saying "request received" does not do that. It forces the model to invent the missing policy in its own head.

Broader action surfaces are usually a decline in reliability rather than an upgrade in capability. A typed API gives you argument checks, scoped permissions, and cleaner return objects. Code execution can give you replayability and local verification when the work is transformation or software. Browser action becomes necessary when the system of record exposes no cleaner path, but it inherits brittle page state and thinner feedback. GUI action is the expensive last resort for closed environments. The reach may be wider. The contract is weaker.

The right escalation rule is therefore severe: start with the narrowest surface that still reaches the work. Wider surfaces are not prestige. They are taxes.

## Action Should Reduce Uncertainty Before It Creates Consequence

The deepest practical use of action is not simply to finish the workflow. It is to reduce uncertainty before uncertainty becomes expensive.

Validate the payload before the write. Poll the real status endpoint before trusting a queued job. Query the live record before reasoning from stale memory. Ask the environment what changed instead of narrating what probably changed. The best action loops do not only perform tasks. They force the system back into contact with state.

Action sits at the front of this bundle because it is the place where agent rhetoric stops being cheap. Once a workflow can act, continuity pressure arrives immediately. The next problem is no longer whether the system can do something. It is what parts of its own past it should be allowed to keep and trust when the next task begins.
