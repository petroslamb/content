# Operating Agents I: When the Model Starts Doing Things

## Action, Tools, and the Boundary of Real Agency

*Operating Agents I of VI*

*The opening case in this essay is a composite of common production failures, not a report of one named company.*

---

A procurement team spent months building a language system that looked, in every meeting, like an agent. It could read vendor policies, explain spending limits, draft an approval sequence, and state exactly what should happen next. Stakeholders loved the demos because the system sounded operational. It named the right fields, the right sequence, and the right exceptions. It sounded like a machine that knew how to get work done.

Nothing happened. The system never crossed the boundary from explanation to execution. A human still had to read the plan, translate the plan into clicks and API calls, and own the consequences.

So the team added a write tool. The first run failed because the model filled `currency_code` with `USD dollars` instead of `USD`. The schema caught it. The second run reached the correct endpoint and appeared to succeed, but the downstream system had changed how it reported deferred writes. The agent treated a partial acknowledgment as completion and moved on. The purchase order never landed. Two weeks later a supplier called asking where the order was.

This is the flattering mistake that sits underneath a great deal of agent talk: natural-language plans are mistaken for agency because they sound operational. They are not operational. They are advice. Agency begins at the point where a system can change state outside the prompt and be held accountable for the result.

That change in boundary is what matters in production. Once a system acts, the important questions stop being mostly about eloquence or even about reasoning in the abstract. They become questions about interfaces. What surface can the system act on? How are arguments validated? What comes back after the action? What permissions govern the call? How would you replay the event? How would you know the action failed? Those are system-design questions, not prompt-design questions.

The hardest useful claim in this essay is simple: action representation matters more than model capability for production reliability. A stronger model attached to vague action boundaries will fail in ways that are hard to localize. A more modest model attached to typed, observable, permissioned actions can often be debugged, corrected, and improved.

---

## The Flattering Mistake

There is a common way to define an agent that quietly hides the real issue. The definition says an agent is a system that reasons in a sophisticated way: long chains of thought, multi-step deliberation, apparent planning, maybe some memory, maybe tool calling. By that standard, any system that produces an elaborate answer starts to look agentic.

That definition flatters the builder because it rewards visible cleverness. It rewards the part the audience can see.

The production definition is harsher. An agent is a system that can take a bounded action against an external surface, observe the result, and continue from what actually happened. If the system only describes what should happen, it is still a text system. If a human silently converts its prose into real-world operations, the human is still the action layer.

This is why the step from assistant to agent often feels smaller in demos than it feels in engineering. The demo only has to make intent sound plausible. The real system has to survive schema validation, permissions, retries, partial failures, stale outputs, and ambiguous acknowledgments. The burden moves from rhetoric to interface design the moment the system can actually do something.

---

## Action Changes The Whole Design Problem

Once action is real, the central design question changes from "how should the model think?" to "what surface is the model allowed to affect, in what representation, with what recovery path?" That question is much narrower than the usual autonomy talk, but it is the one that decides whether the system is legible under stress.

The literature on tool use helps here because it replaces a vague capability word with separate seams that can fail independently. Tool use is not one problem. It is a stack of smaller problems. The system has to recognize that a tool is needed. It has to select the correct tool rather than a neighbor with a similar description. It has to fill the arguments accurately. It has to execute within proper boundaries. It has to interpret the result correctly when control returns.

That decomposition matters because production failures rarely look like "the model cannot use tools." They look like the model chose the right tool and passed one field incorrectly. Or the action succeeded technically but the result signal was misread. Or the tool catalog was too flat, so the selector confused two semantically close functions. Or the write happened without an idempotency key, so a retry became a duplicate side effect. Those are seam failures. If you treat tool use as one abstract capability, you lose the ability to diagnose where the system actually broke.

The most underrated seam is the last one. Many teams design the call contract and neglect the observation contract. They define what the model can send but not what the model is allowed to conclude from the result. That is how systems mistake `200 OK` for completed work, raw logs for trustworthy state, or page text for permission to act. A usable action layer needs both halves. The invocation must be typed, and the observation must be typed as well.

---

## Choose The Narrowest Action Surface That Still Reaches The Work

Once a team accepts that action is the real boundary, the next flattering mistake appears. The mistake is to treat every new surface as an upgrade in capability. In practice, the opposite is usually true. Moving from typed APIs to browser automation to GUI control is usually a decline in observability and reliability, accepted only because the environment gives you no better option.

The default should be stricter than most teams make it: choose the narrowest typed action surface that still reaches the system you need to touch.

If a clean API exists, use it. APIs are replayable, permissionable, and inspectable. If the work is software or data transformation, code execution is often the right surface because code can be tested, sandboxed, and reviewed before side effects. If the work lives primarily in structured business data, SQL or a typed query layer is often the real action surface, even though agent discourse tends to underrate it. Browser automation is for the case where the system matters and the interface is poor. GUI automation is the last resort, not a badge of generality.

The reason this hierarchy matters is not elegance. It is diagnostics. Every step downward trades machine-readable structure for ambiguity. The more ambiguity the surface introduces, the more of your system becomes guesswork dressed up as automation.

## Action Surface Chooser

| Surface | Use it when | Why it should be the default there | Escalate only if |
|---|---|---|---|
| Typed API | The target system exposes stable programmatic operations | Strong schemas, explicit permissions, replayable calls, clear logs | The needed capability is missing from the API |
| Code execution | The task is transformation, testing, generation, or analysis | Outputs can be inspected, run in sandboxes, and verified | The task must touch a non-code system directly |
| SQL or typed queries | The work is primarily over structured enterprise data | Strong semantics, composable verification, auditable writes | The workflow depends on UI-only behavior or hidden business logic |
| Browser automation | The system matters and has no usable API | It can still be scripted and observed at the page level | DOM instability or hidden UI logic makes it too brittle |
| GUI automation | No typed or browser-level surface exists | It reaches otherwise closed systems | Any more structured surface becomes available |

The right reading of this table is not "which option is most powerful?" It is "which option lets me act with the least ambiguity?" That is the production question.

---

## The Five Places Tool Use Breaks

The most useful way to think about tool use in a live system is as five gates.

The first gate is recognizing that a tool is needed at all. Some systems stay too long in text because the model keeps trying to answer from internal plausibility instead of reaching for a live capability.

The second gate is tool selection. This is where work like *Gorilla* matters. The problem is not abstract intelligence. It is semantic discrimination across a set of nearby interfaces.

The third gate is argument filling. This is where many teams lose reliability while telling themselves they are close. They are close. That is what makes the failure costly. The system understood the task, picked the endpoint, and still created a bad write because one field drifted from the contract.

The fourth gate is safe execution. A tool that can send, delete, or write must be bounded before the model touches it. Least privilege, approval rules, and auditable execution are not safety garnish. They are part of the action design.

The fifth gate is result integration. This is where the system has to decide what the returned signal means. A poor result contract can undo otherwise strong reasoning because the next step now proceeds from a fiction.

The reason to name the gates is practical. If you can instrument them separately, you can improve them separately. If you cannot, every failure gets dumped into the vague bucket called "model behavior."

---

## The Observation Contract Closes The Loop

The strongest teams eventually discover that action is only half of the control loop. The other half is the form in which the world answers back.

If tool results come back as raw HTML, raw logs, or broad success text, the model has to infer too much. It will sometimes infer correctly. That is not the same as having a trustworthy control loop. A model should not have to guess whether a queued job is complete, whether a warning should block the next step, or whether a partial response counts as final state.

The fix is architectural. Every important action should have an observation contract as explicit as its call contract. What counts as success? What counts as partial success? What counts as retriable failure? What counts as a state that requires human review? A tool that returns a typed status object and a machine-readable error reason gives the reasoning layer something concrete to work with. A tool that dumps raw responses back into the prompt gives it noise and false confidence.

This is one reason *Toolformer* matters conceptually and *SWE-agent* matters practically. The former helps normalize the idea that models can learn to call structured tools. The latter shows why inspectable environments and testable outputs are so valuable once the model actually acts. The point is not that every agent should look like a coding agent. The point is that typed actions and typed feedback make failure local, and local failure is what improvement depends on.

---

## The Default And The Escalation Rule

Most teams should start with a narrow action layer over typed APIs, search, or code. They should validate arguments before execution, return typed observations after execution, and instrument the five tool-use gates separately. That is the default because it creates the cleanest failure surface.

The escalation rule is equally important. Broaden the surface only when the environment forces you to. Add browser control when the system that matters has no usable API. Add GUI control when even the browser is unavailable. Add more tools only when the current surface genuinely blocks necessary work, not because broader capability looks like maturity.

The hidden cost of premature surface expansion is not only security. It is diagnostic blur. Every new action surface multiplies the ways a failure can be misread.

A convincing plan is not agency. Agency begins where the system can change state and be judged on the result. That is why the first serious agent decision is not about how smart the model seems. It is about how narrow and accountable the action boundary can remain.

---

## Resources And References

### [Builder Blueprint: Action Systems and Tool Use](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/03-action-tool-use-blueprint.md)

If you want the companion technical note for this essay, use this public blueprint. It keeps the quick-choice layer, method matrix, failure modes, and build order in a format that is better for design review than for feed reading. The essay gives you the architectural argument. The blueprint gives you the operator checklist behind it.

### [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761) (2023)

*Toolformer* matters here because it normalized the idea that tool use is not an exotic add-on to language models. It is the conceptual bridge from fluent text generation to structured external action. In the essay, it supports the move away from defining agents by how impressive they sound and toward defining them by the interfaces they can use.

### [Gorilla: Large Language Model Connected with Massive APIs](https://arxiv.org/abs/2305.15334) (2023)

*Gorilla* is one of the cleanest papers for understanding tool use as a specification problem rather than a vague intelligence problem. Its core value is showing that API selection and argument construction are separable bottlenecks. That is exactly why it supports the essay's claim that production failures live at seams such as selection and argument filling, not just in the abstract category called "tool use."

### [SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](https://arxiv.org/abs/2405.15793) (2024)

*SWE-agent* matters because software engineering exposes the upside of good action surfaces unusually clearly. Code, shell commands, and tests are inspectable before and after execution. That makes failures local and improvements measurable. In this essay it serves as the strongest practical example of why typed, replayable action surfaces matter more than grander model claims.

### [BIRD: A Big Bench for Large-Scale Database Grounded Text-to-SQL](https://arxiv.org/abs/2305.03111) (2023)

*BIRD* is useful not because every reader is building text-to-SQL systems, but because it reminds builders that databases are one of the most important real action surfaces in enterprise systems. The paper helps frame SQL as an operational interface with all the usual agent concerns: argument accuracy, execution safety, and observability. That makes it a better fit for this essay than a pure benchmark citation might suggest.

### [Spider 2.0: Evaluating Language Models on Real-World Enterprise Text-to-SQL Workflows](https://arxiv.org/abs/2411.07763) (2025)

*Spider 2.0* strengthens the same point in a more enterprise-shaped direction. Its contribution is that structured data work does not stay simple when schemas, conventions, and workflow context become realistic. In this essay, that matters because it reinforces the claim that action surfaces should be chosen by reliability and observability, not by how often they appear in consumer-agent demos.

### [A Real-World WebAgent with Planning, Long Context Understanding, and Program Synthesis](https://arxiv.org/abs/2307.12856) (2024)

*WebAgent* belongs here because browser automation is often the first major escalation teams make after APIs. The paper is useful less as a general proof of browser agents and more as a reminder of what this surface costs: fragility, interface drift, and higher ambiguity in both action and observation. That is why the essay places browser control below typed APIs and code.

### [OmniParser for Pure Vision Based GUI Agent](https://arxiv.org/abs/2408.00203) (2024)

*OmniParser* matters because GUI automation is the edge case that reveals the whole hierarchy. Once a system is acting through screenshots and visual parsing, it has gained reach at the cost of structure. That makes it the right last-resort citation for this essay. It helps show that moving toward more permissive surfaces is usually not an upgrade in elegance or control. It is a concession to the environment.
