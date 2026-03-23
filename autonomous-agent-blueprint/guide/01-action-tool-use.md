# Part 1: When the Model Starts Doing Things

## Action, Tools, and the Architecture of Real Agents

*Part 1 of 6: A Practical Guide to Foundation Agents*

---

A software team at a mid-size logistics company spent four months building an LLM system to handle internal purchase order processing. The system was good. You could ask it complex questions about vendor contracts, policy constraints, and spending limits, and it would give you detailed, accurate answers. It explained what should happen. It drafted what an approval workflow ought to look like. It described, in complete sentences, which steps to take.

Nothing happened. The recommendations sat in chat windows. Humans read them and then did the work anyway.

In month five, the team added a tool. Not a complicated one: an API call that could write an approved PO into the procurement system. The first run failed. The agent called the right endpoint, passed the right vendor ID, but filled the `currency_code` field with "USD dollars" instead of "USD." The schema rejected it. The agent, having no recovery logic, apologized in natural language and stopped.

They fixed the schema. The second run worked. Then a third-party vendor portal changed its API without notice. The agent selected the right tool but passed stale auth headers. No error was logged. The action appeared to succeed; the PO was silently dropped. The team found out two weeks later when a supplier called about the order.

This sequence is not a story about a bad team or a weak model. It is a story about what happens when action is added to a reasoning system without treating action as a first-class architectural component. The model passed every reasoning test. The failures were at the seams: argument filling, result observation, error handling. These are not prompt engineering problems. They are system design problems.

The transition from assistant to agent does not happen when the model improves. It happens when the action representation changes. What a system can do , and how reliably it can do it , is determined less by which model sits at the center than by how actions are structured, selected, executed, and fed back into reasoning. That is the subject of this essay.

---

## What Makes a System an Agent

There is a tempting definition of an agent as a system that reasons in a sophisticated way. Chain-of-thought output, multi-step thinking, long context , these get treated as the hallmarks of agency. They are not. A system that reasons elaborately and then produces text is still, fundamentally, a text producer. The sophistication of its internal deliberation does not change what it does in the world, which is: nothing.

An agent acts. Specifically, an agent takes actions that change state in some system external to itself. That state change might be a row inserted into a database, a pull request opened, a form submitted, a search query issued, an API called. The action produces an observable result, and that result feeds back into subsequent reasoning. This feedback loop , think, act, observe, continue , is what distinguishes an agent from a very articulate observer.

The *Advances and Challenges in Foundation Agents* survey (2025) frames this clearly in Chapter 8: "an agent is not defined by better text generation, but by what actions it can actually take and how well it can use tools." This sounds obvious. It is not. Much of what gets built and shipped under the label "agent" today is a text-generation pipeline with a chat interface and an aspirational roadmap. The failure mode is not dishonesty; it is that action was treated as a feature to add later rather than as the architectural center from the start.

The practical consequence of taking action seriously is that the design questions change entirely. The question shifts from "how should the model reason about this?" to "what can the model do, to what system, with what representation, at what risk, and with what recovery path?" Those are harder questions with more specific answers.

---

## The Action Representation Ladder

The single most useful framing in the Chapter 8 literature is the idea of an action representation ladder. Not every form of action is equally useful, and the differences are not marginal , they determine whether the system is testable, replayable, debuggable, and safe.

At the bottom is **plain text**. The agent outputs a natural-language description of what should happen: "send an email to the procurement team asking them to approve this request." This is the weakest action representation because it does nothing. It requires a human to translate intent into execution. It cannot be logged as a machine-readable event. It cannot be replayed or audited. It is, at best, a recommendation.

One step up is **code as action**. The agent writes a Python function, a shell command, a SQL query , something executable. This is dramatically stronger because code can be run, inspected, tested against expected output, and replayed on demand. It does not require translation by a human. The failure modes are explicit (syntax errors, assertion failures, runtime exceptions) rather than implicit (the human misread the recommendation). This is why software engineering was the first domain where agents delivered consistent production value: the action surface is code, code is testable, and testability is what makes improvement tractable.

At the top are **typed tool invocations** in real systems. The agent calls a function with a defined JSON schema, sends an HTTP request to a typed API, executes a parameterized SQL query, triggers a browser automation step. These representations combine the executability of code with the structured observability of formal interface contracts. Parameters are validated. Results are typed. Errors are machine-readable. Every invocation can be logged with its arguments, its result, its latency, and its authorization context.

Moving up this ladder is the practical definition of building a real agent rather than a sophisticated chatbot. It is worth stating explicitly because the temptation is always to prototype at the plain-text level, deliver a demo that looks agentic, and then discover during production engineering that the demo's "actions" were descriptions that a human was silently executing.

---

## Tool Use Is Five Problems, Not One

Once the decision to use structured tools is made, a common error follows: treating "tool use" as a single capability that the model either has or does not have. In practice, tool use decomposes into five distinct problems, each of which can fail independently.

**Tool need detection** is the question of whether the agent correctly identifies that a tool invocation is necessary at this point in the reasoning process. A model can be capable of using a tool and consistently fail to invoke it at the right moment, either calling it too early (before it has enough context to fill arguments correctly) or too late (after it has already committed to a plan it cannot execute).

**Tool selection** is the question of whether the agent picks the right tool. In systems with large tool catalogs, this is a retrieval and understanding problem. The agent must recognize which of several plausible tools is the correct match for the current subtask , not just by name similarity but by understanding the tool's semantics, expected inputs, and side effects. *Gorilla: Large Language Model Connected with Massive APIs* (2023) is the clearest research demonstration that tool use reliability depends critically on accurate API selection and argument construction, not just on the model's general reasoning capability. Production failures that look like "the model got confused" are often, on inspection, tool selection errors: the model picked a tool with a similar name but different semantics.

**Argument filling** is the question of whether the agent constructs the correct argument values. This is where the PO system's `currency_code` failure lived: the model identified the right endpoint, called the right function, and then produced an argument that failed schema validation. Argument filling errors are insidious because they often happen near the end of a successful reasoning chain, after the agent has correctly decomposed the task and selected the tool. That proximity to success makes them feel like minor polish problems. They are not. They are the most common class of tool-use failure in production systems.

**Safe execution** is the question of whether the action is performed inside appropriate boundaries , sandboxed, permissioned, logged, and bounded in scope. A tool that can write to a database, call an external API, or send a message should not run without least-privilege constraints, proper authentication, and an audit trail. The failure to design safe execution is why retriable errors sometimes cascade into irreversible ones. If a write action has no idempotency key and the agent retries on a timeout, the result is the procurement agent variant of the problem: multiple executions, one apparent success, confusion on all sides.

**Result integration** is the question of whether the tool's output is correctly parsed, interpreted, and incorporated back into the reasoning loop. This is where the stale auth header failure lived: the API returned HTTP 200 with a body indicating the PO had been dropped into a deferred queue, a condition that required reading a specific field in the response. The agent saw "200 OK," treated it as success, and moved on. Result integration requires the observation contract to be as carefully designed as the invocation contract.

These five problems do not scale together. A system can have excellent tool selection and broken argument filling. It can have safe execution and poor result integration. Diagnosing tool-use failures correctly requires knowing which seam broke , and that requires instrumenting each of the five stages separately, not just measuring end-task success rate.

---

## The Action Surface Decision

Before any of the five-problem framework matters, there is a more fundamental design decision: what surface does the agent act on? The choice of action surface determines the reliability, debuggability, cost, and risk profile of the entire system before the first model call is made.

The practical hierarchy, from most to least preferred, is:

**Typed API calls** are the default for any business system with a well-documented interface. They are replayable (the exact call can be logged and rerun), inspectable (arguments and results are structured), permissioned (API keys, OAuth scopes, and rate limits are tools for containment), and typically reversible through the API's own semantics. When a clean API exists, use it. Do not reach for a browser or a GUI because the API feels difficult , the difficulty of designing against an API is a one-time engineering cost; the fragility of browser-based action is a permanent operational cost.

**Code execution** is the action surface for software and data tasks where reproducibility is the primary value. When the agent writes a transformation script, a test suite, or a SQL query, its output is inspectable before execution, testable against expected results, and revisable without side effects. *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering* (2024) treats the code, shell, and test environment as the action surface for a software engineering agent and demonstrates that this surface makes the agent's work unusually reviewable and correctable. Code execution is also the surface that benefits most from sandboxing: running in a containerized environment limits blast radius at the architecture level rather than relying on the agent's judgment.

**Database and SQL action** is the action surface for analytics, reporting, and structured data workflows , a category that covers enormous amounts of enterprise work and is significantly underrepresented in the agent discourse. When the task is to query business data, produce a report, update a record, or run a transformation, the relevant interface is usually SQL or a structured query API. *BIRD* (2023) and *Spider 2.0* (2024) are worth citing not as benchmark curiosities but as evidence that text-to-SQL over real enterprise schemas is the actual practical bottleneck for data-centric agents: getting argument-level SQL accuracy in environments with complex schemas, foreign-key relationships, and domain-specific conventions. These papers reveal the same five-problem structure that action systems generally face, applied specifically to the database surface.

**Browser action** is appropriate when the system the agent needs to reach does not expose a usable API. Many valuable workflows live in legacy portals, third-party SaaS products, or regulatory systems that were never designed for programmatic access. For those cases, browser automation , navigating, clicking, reading DOM elements, filling forms , is often the only path. *WebAgent: A Real-World WebAgent with Planning, Long Context Understanding, and Program Synthesis* (2023) is an early demonstration of this surface working at meaningful task complexity. The major limitation is fragility: CSS selectors change, page structures are redesigned, and the agent's mapping from intent to UI action breaks silently. Browser action should be chosen because APIs are unavailable, not because the browser looks easier.

**GUI automation** is the last resort. When the system is a legacy desktop application, a closed platform, or a visual interface that cannot be accessed through any typed mechanism, visual parsing of the screen becomes the only option. *OmniParser for Pure Vision Based GUI Agent* (2024) addresses one of the hardest bottlenecks here: converting screenshots and UI layouts into machine-usable structure. GUI automation can work, but it is the highest-fragility and lowest-observability surface in the hierarchy. Actions cannot be logged in structured form, failures are visually ambiguous, and changes in the application's appearance break the agent immediately. Choose it only when every other surface is genuinely unavailable.

The non-obvious insight in this hierarchy is that moving down it is always a cost, not a capability upgrade. An agent that acts through browser automation instead of a typed API did not become more capable , it became more fragile, more expensive to maintain, and harder to debug, while gaining access to systems that have no better interface. That tradeoff is sometimes worth accepting. It should never be invisible.

---

## The Observation Contract

There is a component of the action architecture that does not appear in most tool-use frameworks, but which the blueprint literature identifies as a consistent source of production failure: the observation contract.

Each time the agent takes an action, it receives a result. The question of how that result is represented and what meaning the agent derives from it is not a reasoning question , it is an interface design question. If raw API responses, error messages, and status codes are dumped directly back into the prompt as unstructured text, the agent reads them in the same mode it reads everything else: probabilistically, with no distinction between "the API returned 200 and the job is queued for processing" and "the API returned 200 and the transaction is complete."

The observation contract solves this by specifying, for each tool invocation, exactly what information the result should carry back into the reasoning loop, in what format, at what level of abstraction. A tool that returns a success/failure flag, a typed result object, and a machine-readable error reason gives the agent's next reasoning step something it can act on. A tool that dumps raw HTTP response bodies into the prompt gives it noise.

This matters enough to be explicit in the system design. Every tool in the action layer should have not just a call contract (what arguments it accepts and what endpoint it hits) but an observation contract (what the agent receives back, how success and failure are typed, and what the agent is allowed to infer from each outcome). The observation contract is what makes the ReAct-style reasoning loop , reason, act, observe, continue , actually close.

---

## What Goes Wrong

The named failure modes from production agent systems cluster around three places in the action architecture.

**Wrong tool or wrong arguments** is the most common class of tool-use failure. The agent understands the task and reaches for a tool, but selects the wrong one from a large catalog, or selects the right one but fills a field incorrectly. The fix is almost always in the tool contract design, not in the model: better tool descriptions (concrete enough that the model can distinguish this tool from adjacent ones), tighter output schemas (structured return values rather than free-form text), and explicit argument validation before execution. When tool selection accuracy is low, the tool catalog probably needs retrieval assistance , a mechanism that helps the agent search for the right tool rather than choosing from an undifferentiated list.

**Irreversible action without enough evidence** happens when the agent takes a write, send, or delete action before the evidence threshold for that action is met. This is a design failure, not a model failure. The architecture allowed the action to be invoked before a verification step confirmed the evidence. The fix is structural: separate read capabilities from write capabilities at the permission level, require deterministic checks before high-impact actions, and require human approval before irreversible ones. The procurement agent's retry loop happened because no gate stood between the agent's determination that retrying was appropriate and its ability to submit a new purchase order.

**Observation-action confusion** happens when the agent mistakes a state description for permission to act. An environment observation , a page summary, a document snippet, a prior message , contains a description of what should happen, and the agent reads that description as justification for doing it. This is one of the mechanisms behind indirect prompt injection, discussed in detail in Part 5. At the action-architecture level, the fix is explicit trust separation: observations that come from the environment do not inherit the trust level of system instructions, and the action policy should be governed by the latter, not the former.

---

## Building an Action Layer That Works

The implementation plan that follows from this essay is deliberate about sequence. The goal is to build the action layer so that it is testable before it is powerful, rather than powerful before it is testable.

Start with typed tool calls over APIs or search. These are the narrowest and most controlled action forms. Even a simple system that can query a knowledge base and return structured results is already meaningfully agentic in the way that matters: the result is typed, observable, and reproducible. Get this right , argument accuracy, error handling, and result integration , before adding more surface area.

Add code execution for tasks that need reproducibility. If the agent will transform data, write tests, or produce computational outputs, code is the right surface. Sandbox it from the beginning, not as an afterthought. Sandboxing is not a security retrofit , it is what makes code action debuggable, because a sandboxed execution has a defined scope and a recoverable state.

Add browser or database action where the environment demands it. When the task genuinely requires interacting with a web system that has no API, or querying business data through SQL, extend the action surface to cover it. But extend it because the task requires it, not because it seems like a natural feature addition.

Add GUI automation only for constrained legacy cases where nothing else reaches the required system. And when you add it, do so with the expectation that it will require ongoing maintenance as the target interface evolves.

Throughout this build sequence, instrument each layer separately. Track tool selection accuracy, argument accuracy, action success rate, recovery rate after failure, retry count, and replayability. These are not metrics for a reporting dashboard , they are the diagnostic signals that tell you which of the five tool-use problems is failing on real tasks.

The right question to ask of any action layer is not "can the agent do this?" It is: "if the agent does this incorrectly, how do we know, and what does recovery look like?" An action system that cannot answer that question is not production-ready, regardless of benchmark performance.

---

## The Underlying Claim

The core practical contribution of this framing is simple enough to state plainly: action representation is more important than model capability for determining whether an agent system is reliable in production.

This is a testable claim. A system using typed API calls with proper argument validation, recovery logic, and observation contracts will outperform a more capable model using plain-text action descriptions in a mature production environment. The typed system is debuggable, its failures are localizable, and its improvements are measurable. The plain-text system fails in ways that are hard to distinguish from model errors, cannot be instrumented at the seam level, and cannot be improved systematically.

The procurement team's failed purchase orders were not a sign that LLMs are not ready for enterprise work. They were a sign that the action representation layer was not designed to the same standard as the rest of the system. The model did its job. The action architecture did not.

That is the gap this guide addresses , one layer at a time, in the order that reveals why each one matters.

---

*Part 2 addresses reasoning and planning: how agents structure their thinking through tasks, why reasoning failures are almost always scaffold mismatches rather than model failures, and what the cheapest correct reasoning structure looks like for each class of problem.*

---

**Source basis for this essay:** Chapter 8 of *Advances and Challenges in Foundation Agents* (2025); *Toolformer: Language Models Can Teach Themselves to Use Tools* (Schick et al., 2023) [arXiv:2302.04761](https://arxiv.org/abs/2302.04761); *Gorilla: Large Language Model Connected with Massive APIs* (Patil et al., 2023) [arXiv:2305.15334](https://arxiv.org/abs/2305.15334); *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering* (Yang et al., 2024) [arXiv:2405.15793](https://arxiv.org/abs/2405.15793); *A Real-World WebAgent with Planning, Long Context Understanding, and Program Synthesis* (Gur et al., 2023) [arXiv:2307.12856](https://arxiv.org/abs/2307.12856); *BIRD: A Big Bench for Large-Scale Database Grounded Text-to-SQLs* (Li et al., 2023) [arXiv:2305.03111](https://arxiv.org/abs/2305.03111); *Spider 2.0: Evaluating Language Models on Real-World Enterprise Text-to-SQL Workflows* (2024) [arXiv:2411.07763](https://arxiv.org/abs/2411.07763); *OmniParser for Pure Vision Based GUI Agent* (Lu et al., 2024) [arXiv:2408.00203](https://arxiv.org/abs/2408.00203); `practical-chapter-blueprints/03-action-tool-use-blueprint.md`; `agentic-architectures-blueprint.md`.
