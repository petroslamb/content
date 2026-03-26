# Chapter 8 Blueprint: Action Systems and Tool Use

## Why This Chapter Matters

This is the chapter where the paper becomes unmistakably agentic. Reasoning alone does not make a system an agent. Action does. The chapter is practical because it forces a sharper question: what is the action space, how is action represented, and how does the system safely execute it?

For builders, this is the difference between a chatbot that describes work and a system that actually performs work in software.

## Survey Subsections To Prioritize

- `8.3.1 Action Space Paradigm`
- `8.3.2 Action Learning Paradigm`
- `8.3.3 Tool-Based Action Paradigm`

If the target is software or enterprise work, the language and digital action sections matter much more than the physical section.

## The Practical Question

The chapter is answering three design questions:

1. What surface should the agent act on?
2. How should those actions be represented?
3. How should action selection, execution, and observation be wired back into reasoning?

These are the questions that determine whether the system is inspectable and reliable or merely impressive in demos.

## Core Literature And What Each Paper Adds

### `Toolformer: Language Models Can Teach Themselves to Use Tools`

Toolformer is the conceptual bridge from language-only generation to explicit tool use. It shows that tool invocation can be part of the model's operating pattern rather than an afterthought.

Use it to understand why tool use is not just an integration problem but also a behavior-shaping problem.

### `Gorilla: Large Language Model Connected with Massive APIs`

Gorilla matters because it frames tool use as API understanding and argument construction. Many failures in production tool use are not about broad intelligence; they are about selecting the wrong tool or filling the wrong parameters.

Use it when designing tool specs, schemas, and retrieval over tool catalogs.

### `HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face`

HuggingGPT is a controller paper. Its practical contribution is to treat the LLM as an orchestrator over specialist capabilities rather than as a monolithic worker.

Use it when a task requires multimodal or specialist tools rather than a single generic tool layer.

### `A Real-World WebAgent with Planning, Long Context Understanding, and Program Synthesis`

WebAgent matters because it demonstrates digital action over real websites rather than toy interfaces. It is an early proof that browsing, interaction, and planning can be part of task execution.

Use it when designing web-execution agents or research assistants that must do more than retrieve snippets.

### `Mind2Web: Towards a Generalist Agent for the Web`

Mind2Web is both a benchmark and an architectural reference. It matters because it frames web action as a generalist problem rather than a handcrafted one-off agent.

Use it when evaluating whether a web agent is robust beyond a narrow scripted path.

### `Mobile-Agent: Autonomous Multi-Modal Mobile Device Agent with Visual Perception`

Mobile-Agent extends tool use into multimodal device interaction. Its importance is that action surfaces are not always typed APIs or text commands.

Use it when the real environment is a mobile or highly visual UI.

### `AppAgent: Multimodal Agents as Smartphone Users`

AppAgent reinforces the same lesson in a smartphone context: GUI interaction is a serious action surface when APIs are not enough.

Use it when legacy or closed applications force the agent into interface-level interaction.

### `OmniParser for Pure Vision Based GUI Agent`

OmniParser is a bottleneck paper. It matters because GUI action depends on converting pixels and layout into machine-usable structure.

Use it when computer-use agents fail because the interface is visually ambiguous rather than conceptually difficult.

### `SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering`

SWE-agent is one of the most practical action papers in the entire folder. It treats code, shell commands, tests, and environment feedback as the core action space.

Use it whenever the target domain is software engineering or anything close to code execution and testable artifacts.

### `OpenHands: An Open Platform for AI Software Developers as Generalist Agents`

The local `papers/opendevin.*` material corresponds to OpenHands. Its importance is that it pushes the code-agent idea toward a more general developer platform rather than a narrow benchmark system.

Use it as an adjacent reference to SWE-agent for developer-agent platform design.

### `Can LLM Already Serve as a Database Interface? A BIg Bench for Large-Scale Database Grounded Text-to-SQLs`

BIRD matters because it centers database action as a real enterprise surface. This is important because many valuable workflows are not web agents or coding agents; they are structured-data agents.

Use it when the agent must query, transform, or reason over business data.

### `Spider 2.0: Evaluating Language Models on Real-World Enterprise Text-to-SQL Workflows`

Spider 2.0 matters because it shifts SQL agents toward real enterprise complexity instead of narrow benchmark prompts.

Use it when evaluating text-to-SQL or analytics automation under realistic workflow conditions.

## If Your Problem Looks Like X, Choose Y

- If a clean API exists, choose typed tool calls first.
- If the task must be reproducible and testable, choose code as the action surface.
- If the workflow is data-centric, choose database or SQL action.
- If the site has no usable API but exposes a stable web flow, choose browser action.
- If no cleaner integration exists and the environment is visual, use GUI action only as a fallback.

## Method Comparison Matrix

| Action surface | Best use | Main strength | Main risk | Escalate when |
| --- | --- | --- | --- | --- |
| Typed API tools | business systems with good interfaces | replayable and inspectable | weak schemas or wrong arguments | the required system has no usable API |
| Code execution | software and data tasks | executable, testable, replayable | unsafe scope if poorly sandboxed | the target system is external and UI-bound |
| Database or SQL action | analytics and structured data work | strong structure and measurable outputs | schema drift and unsafe queries | tasks depend on web or GUI state instead |
| Browser action | web-native workflows | works where APIs are incomplete | brittle selectors and page changes | DOM access is not enough or the system is highly visual |
| GUI action | closed or legacy interfaces | reaches otherwise inaccessible systems | highest fragility and weakest observability | only when every cleaner surface is unavailable |

## The Chapter's Main Architectural Insight

The chapter's best insight is the action representation ladder:

- plain text
- code
- tool invocations in actual environments

The practical default is to move upward on that ladder whenever the environment allows it. Plain text is the weakest action representation because it is hard to replay and hard to verify. Code and typed tool calls are stronger because they are executable and inspectable.

The chapter also decomposes tool use into five subproblems:

- tool need detection
- tool selection
- argument filling
- safe execution
- integration of results back into reasoning

That is a far better blueprint than treating "tool use" as one undifferentiated capability.

## The Default Action Blueprint

### Action Surface Selection

Choose the narrowest action surface that still reaches the business system:

- APIs first
- databases second when the task is data-centric
- code execution when reproducibility matters
- browser automation when APIs do not exist
- GUI automation only when nothing more stable is available

### Action Representation

Represent actions as typed calls, SQL, executable code, or constrained UI operations. Every action should be logged with parameters, result, timestamp, and authorization context.

### Execution Layer

Run actions in a sandboxed or least-privilege environment. The action layer should validate inputs before execution and normalize outputs after execution.

### Observation Layer

Convert tool results into typed observations rather than dumping raw text back into the model. The cleaner the observation contract, the more stable the ReAct loop becomes.

### Recovery Layer

Track retries, failures, and fallback routes explicitly. Tool errors should create machine-readable state, not just free-form apologies.

## Design Decisions That Matter Most

### When to use code as action

Use code when the system's output should be executable, testable, or replayable. Code is especially strong in software, data manipulation, and repeatable transformation tasks.

### When to use browser action

Use browser action when APIs are incomplete or unavailable and the task genuinely depends on website interaction.

### When to use GUI action

Use GUI action only when the product or legacy system gives you no cleaner integration surface. It is powerful but brittle.

### When to specialize tools

Specialize tools when domains differ enough that tool semantics, failure handling, or schemas are meaningfully distinct. Generic tool layers are attractive until argument accuracy and recovery quality start failing.

## Evaluation

A practical action layer should be measured by:

- tool selection accuracy
- argument accuracy
- action success rate
- recovery rate after failure
- retry count
- latency and cost per action
- replayability and auditability

The right action metric is not just "did the final answer look good." It is whether the system executed the right steps safely and reproducibly.

## Failure Modes

- using plain-text action plans where typed actions are possible
- granting broad permissions to generic agents
- mixing planning and execution privileges in one unrestricted node
- failing to normalize tool outputs
- treating GUI action as a stable first choice
- ignoring action metrics in favor of end-task vibes

## Recommended Build Order

1. Start with typed tool calls over APIs or search.
2. Add code execution for tasks that need reproducibility.
3. Add browser or SQL action where the environment demands it.
4. Add GUI automation only for constrained legacy cases.
5. Expand tool catalogs only after measuring tool-use failure modes.

## Anti-Patterns

- Do not start with general computer use as the default action surface.
- Do not let one agent hold every tool and every permission.
- Do not treat raw tool output as final truth.
- Do not ship action layers without logs and replayability.

## Reading Sequence For This Chapter

1. `../../essays/action/01-action-tool-use-v5.md`
2. `../../essays/action/companion.md`
3. `papers/toolformer.md`
4. `papers/gorilla.md`
5. `papers/hugginggpt.md`
6. `papers/webagent.md`
7. `papers/mind2web.md`
8. `papers/swe_agent.md`
9. `papers/bird.md`
10. `papers/spider_2_0.md`
11. `papers/mobile_agent.md`
12. `papers/appagent.md`
13. `papers/omniparser.md`
14. `papers/opendevin.md`

## Bottom Line

The chapter's practical message is that action should be structured, bounded, and measurable. The transition from assistant to agent happens when the system can take replayable actions in software, not when it sounds more autonomous.
