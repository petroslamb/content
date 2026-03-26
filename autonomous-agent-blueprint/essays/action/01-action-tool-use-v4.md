# Operating Agents I: When the Model Starts Doing Things

A procurement team built an internal system that looked, in every review meeting, like an agent. It could read supplier policy, explain approval logic, draft the purchase-order payload, and tell an operator exactly what should happen next. The demos were impressive because the system sounded operational. It named the right fields, the right exceptions, and the right downstream systems.

Nothing happened until a human translated that prose into clicks and API calls.

So the team gave the system write access to the procurement service. The first failure was boring. The model filled `currency_code` with `USD dollars` instead of `USD`, and the schema rejected the request. The second failure was worse. A downstream service had changed how it reported deferred writes. The agent treated a partial acknowledgment as completion, moved on, and the order never landed. The supplier discovered the gap before the team did.

That is where the real agent problem starts. The step from assistant to agent is not the moment the model sounds more capable. It is the moment language stops being commentary on the task and starts becoming accountable state change.

Once a system can act, the design problem narrows and hardens. The important questions are no longer mainly about fluency or about reasoning in the abstract. They are about interfaces. What surface is the system allowed to touch? How are arguments validated? What comes back after the action? What permissions govern the call? How would you replay the event? How would you tell the difference between a completed write and a polite lie from the environment?

The strongest practical claim in this chapter is simple: **action representation matters more than model capability for production reliability**. [*Toolformer*](https://arxiv.org/abs/2302.04761) made tool use legible as part of the model's operating pattern. [*Gorilla*](https://arxiv.org/abs/2305.15334) made tool use look more like an interface-specification problem than a vague intelligence problem. [*SWE-agent*](https://arxiv.org/abs/2405.15793) showed why typed environments, executable artifacts, and machine-checkable feedback change the reliability conversation once the system actually acts. Put a strong model behind a vague action boundary and you will often get expensive failures that are hard to localize. Put a more ordinary model behind typed, observable, permissioned actions and you usually get something you can debug.

## Companion Note

This essay presents a focused narrative for a broad audience. For the full technical scope—including what this essay intentionally leaves out, how it maps to the chapter blueprint, and recommended deeper reading—see the [companion note](companion.md).

## The Assistant-Agent Boundary Is Representational, Not Capability-Based

The flattering definition of agency quietly distorts the engineering work. It says an agent is a system with sophisticated reasoning, long traces, tool access, memory, maybe planning, maybe a general feeling of autonomy. By that standard, elaborate prose already looks agentic.

The production definition is harsher and more useful. An agent is a system that can take a bounded action against an external surface, observe the result, and continue from what actually happened. If the system only describes the workflow and a human silently performs the workflow, the human is still the action layer.

That is why the jump from assistant to agent looks smaller in a demo than it feels in engineering. A demo only has to make intent sound plausible. A live system has to survive schemas, permission scopes, retries, stale outputs, deferred writes, partial failures, and ambiguous acknowledgments. The burden moves from rhetoric to interface design the moment the system can change state outside the prompt.

The transition is not about model improvement. It is about moving up the **action representation ladder**:

- **Plain text** is the weakest representation. It can describe an intended step, but it cannot execute, replay, or verify with discipline.
- **Code** is stronger. It can be executed, tested, and inspected. [*SWE-agent*](https://arxiv.org/abs/2405.15793) shows how software environments provide strong replayability and observability.
- **Typed tool invocations in real environments** are stronger still. APIs, SQL queries, and constrained operations carry schemas, permissions, and machine-readable results.

Moving up this ladder is a phase transition. Each rung closes failure modes that the lower rung cannot fix. An agent that acts through typed, observable, permissioned surfaces is more reliable than an agent with a "better" model that acts through free-form text or brittle GUI control.

## Inside-Out vs Outside-In: How Action Shapes Perception

The most profound insight from the survey's action chapter comes from cognitive science: the debate between **outside-in** and **inside-out** frameworks for understanding intelligent behavior.

The traditional **outside-in** view holds that causal influence begins with external stimuli. The environment excites peripheral receptors, signals propagate inward, and behavior emerges as a downstream effect. This matches our default mental model of agents: they wait for input, process it, and respond. It is a reactive stance.

Buzsáki's **inside-out** framework proposes the opposite: it is the agent's own actions that shape the meaning and consequences of incoming signals. The agent continuously generates predictions and motor commands, sending "corollary discharge" or "action copies" to sensory areas. These internally generated signals serve as references that inform the agent which sensory changes are self-initiated rather than imposed by the outside world. In this view, cause shifts from external event to internally launched initiative; external stimuli play a confirmatory or corrective role.

This has staggering implications for agent design:

- **Reactive (outside-in)** agents are passive. They wait for perfect information before acting. They treat every input as gospel. They do not distinguish between changes they caused and changes that came from the environment.
- **Proactive (inside-out)** agents act to reduce uncertainty. They generate their own feedback. They track which parts of their state are self-caused. They use action to shape what they perceive.

In practical terms, an inside-out agent might:
- Proactively verify assumptions before they become expensive errors
- Issue test queries to confirm a retrieved document is current before using it
- Execute idempotent probes to discover whether a resource is available before committing to a plan
- Maintain a "self-caused" flag on state changes so it can distinguish its own effects from environmental updates

The cognitive science literature shows that without these internal reference signals, raw sensory data becomes ambiguous or even useless. Sleep paralysis illustrates this: motor commands fail to reach muscles, but external stimuli still bombard senses; the brain lacks self-generated references to interpret input, leading to unreality. Similarly, if an external agent moves your eye without your brain issuing a motor command, the visual scene appears to move.

For AI agents, this means: **perception is not an end in itself; it is a means of updating and refining the agent's own action-driven hypotheses about the environment**. An agent that does not track what *it* has done cannot disentangle self-caused from externally-caused state changes. That confusion is a major source of loops, duplicate work, and corrupted state.

The survey notes that most contemporary AI systems still function predominantly in reactive mode. Shifting to an inside-out model reframes perception as causally downstream of action. That is not just philosophy—it is an architecture decision with concrete implications for how agents maintain state, verify assumptions, and avoid feedback loops.

## Tool Learning: Discovery, Creation, Usage

The survey frames tool learning as having three key aspects—a taxonomy that provides clearer architectural boundaries than the "five seams" commonly discussed.

### Tool Discovery

Identifying and selecting the appropriate tools from a large pool. This is often a retrieval problem: given a task, which tool(s) should be considered? Approaches split into:

- **Retrieval-based**: select from an existing tool library. [*HuggingGPT*](https://arxiv.org/abs/2303.17580) uses LLMs as controllers that select models from Hugging Face. ToolkenGPT optimizes tool embeddings for retrieval.
- **Generative-based**: fine-tune LLMs to learn tool selection from instruction data. [*ToolFormer*](https://arxiv.org/abs/2302.04761) and ToolLLM collect corpora with API calls and train models to generate appropriate tool invocations.

The discovery challenge is not just matching; it is understanding the task's requirements and mapping them to tool capabilities, possibly composing multiple tools in sequence.

### Tool Creation

Generating new tools when existing ones are insufficient. This moves beyond calling functions to writing them. Examples:

- [*PAL*](https://arxiv.org/abs/2212.10035) generates programs as intermediate reasoning steps
- [*LATM*](https://arxiv.org/abs/2305.11165) and [*Creator*](https://arxiv.org/abs/2309.09069) use LLMs to create code for user intentions, often with a verifier to validate created tools
- [*SciAgent*](https://arxiv.org/abs/2402.13298) crafts new tools for scientific discovery

Tool creation turns the agent from a tool *user* into a tool *designer*, which raises new questions about specification, testing, and reliability.

### Tool Usage

Effective employment of discovered or created tools. This is where most current work lives, with three key dimensions of expansion:

1. **Vertical specialization**: Domain-specific tools for robotics, science, healthcare
2. **Horizontal integration**: Combining multiple toolkits across modalities (vision, language, control)
3. **Embodiment**: Physical interaction through robotic tools and sensors

The survey emphasizes that tool learning distinguishes human intelligence from that of other animals. Enabling agents to operate in digital and physical environments by harnessing tools is a fundamental step toward human-level intelligence.

## Action Surface Hierarchy: Not All Tools Are Equal

The practical takeaway remains: choose the narrowest action surface that still reaches the work. But the survey gives us a richer taxonomy of *where* tools live:

| Domain | Typical surfaces | Representative systems | Escalate to when |
|--------|------------------|------------------------|------------------|
| **Language** | Function calls, API schemas, code generation | ToolFormer, Gorilla, ToolLLM | Need richer modality or execution environment |
| **Digital** | Web interactions, GUI manipulation, mobile device control | WebAgent, Mobile-Agent, AppAgent, OmniParser | Physical interaction becomes necessary |
| **Physical** | Robotic arms, sensors, actuator control | SayCan, RT-2, TidyBot, surgical robotics frameworks | Domain requires laboratory-scale instrumentation |
| **Scientific** | Specialized computational/analytical tools | ChemCrow (18 chemistry tools), HoneyComb, SciToolAgent (500+ tools), SciAgent | Need domain-specific knowledge graphs or hypothesis generation |

The key insight: **The domain determines the natural action surface**. Enterprise work that deals with structured data belongs in Language/SQL space. Work that must execute code belongs in code execution. Work that lives in websites belongs in browser automation. Work that manipulates physical objects belongs in embodied control. Work that requires specialized scientific computation belongs in domain-specific tool suites.

This is not a preference order; it is a match-making problem. The error is using a generic surface (browser automation) when a stronger, more structured surface (SQL, API, code) is available.

## The Five Seams of Tool Use (Still Useful)

While the survey's three-aspect framework is higher-level, the five-seams model remains valuable for diagnostics:

1. **Tool need detection** — Does the model recognize that a tool is required? (Toolformer normalized this)
2. **Tool selection** — Which tool from the available set? (Gorilla: this is API discrimination, not general intelligence)
3. **Argument filling** — Are parameters bound correctly according to schema? (Schema mismatches are common)
4. **Safe execution** — Does the call happen within bounded permissions, with proper authorization and sandboxing?
5. **Result integration** — Is the observation contract clear? Can the system distinguish queued vs completed, partial vs final, warning vs success?

These seams cut across the discovery/creation/usage aspects. For instance, tool discovery is primarily about seam 2 (selection). Tool creation is about expanding the available set before seam 1. Tool usage encompasses seams 3-5.

## Multi-Turn RL: The Emerging Training Paradigm

The survey dedicates substantial space to a recent shift: **multi-turn reinforcement learning for agent training**. This is an important development that the blueprint and essays mostly omit.

Traditional RL treats complete actions as steps. RL on LLMs treats token generation as the fundamental step, creating challenges in credit assignment for long-horizon tasks. Recent work addresses this with multi-turn RL frameworks:

- **RAGEN** ([Li et al., 2024](https://arxiv.org/abs/2405.16416)): modular multi-turn RL with StarPO-S algorithm, trajectory filtering, critic incorporation, gradient stabilization
- **VAGEN**: extends RAGEN to visual-knowledge agents
- **StepSearch**: multi-turn QA dataset with step-wise PPO and process supervision
- **ReSearch** ([Lee et al., 2024](https://arxiv.org/abs/2405.20198)): integrates search operations into reasoning, dynamically influenced by prior steps
- **Search-R1**: multi-query generation through step-by-step reasoning with real-time feedback
- **WebAgent-R1**: GRPO adaptation for web environments with dynamic context compression
- **SkyRL**: high-throughput RL pipeline for multi-turn tool usage (applied to SWE-Bench)
- **MT-GRPO** and **GiGPO**: fine-grained turn-level advantage estimation for precise credit assignment

Why does this matter for a practical essay? Because it shows where the field is heading: **agents are no longer trained on static datasets but through interaction**. The multi-turn RL paradigm aims to unify reasoning and tool-use capabilities by letting agents learn from experience rather than from supervised demonstrations alone.

The challenges identified are substantial:
- Credit assignment across token vs turn levels
- Data efficiency (environment interactions are expensive and potentially unsafe)
- Reward design (many real-world applications lack clearly definable rewards)
- Current focus on QA/search/code where rule-based rewards exist

But the direction is clear: future agent systems will increasingly rely on interaction-based training to develop robust tool-use policies. This is the bridge from "agent can call tools" to "agent learns which tools to call and in what sequence through experience."

## The Efficiency-Evaluation Trade-off

The survey's summary calls out two challenges that should shape every action design:

**Efficiency**: Real-time applications cannot tolerate the latency introduced by complex action systems. Strategies:
- Filter irrelevant/redundant information early
- Zero-shot prompting to streamline reasoning
- High-speed caching for relevant knowledge
- Parallel tool invocation when independent

**Evaluation**: How do you determine the correct action when multiple sources conflict? How do you verify that the chosen tool and arguments are appropriate? The survey calls for:
- Robust evaluation systems to measure action system performance
- Transparent decision-making processes
- Verification protocols to reduce incorrect action prediction
- Exposure of the decision process so operators can understand *why* a particular tool was selected

These are not academic concerns. They map directly to the blueprint's emphasis on reviewable runs and the architecture checklist's question about reconstruction capability.

## Future Challenges That Matter

The survey lists five open problems that should influence how we think about action systems today:

1. **Efficiency** (latency in real-time scenarios)
2. **Evaluation** (verification, transparency, conflicting sources)
3. **Multi-modality** (understanding actions beyond language instructions—GUI operations, embodied tools)
4. **Privacy** (federated learning, model distillation to protect sensitive data during tool use)
5. **Safety** (ethical implications, preventing erroneous or malicious actions, especially with physical tools)

Plus the overarching question: **How to balance foundation models vs external tools?** There is an increasing trend to enhance intrinsic model capabilities. When should the model know something vs when should it call a tool? This is not just an optimization; it is an architectural boundary with reliability implications.

## Inside-Out Acting: A New Thesis

The conventional view treats tool use as: given a task, decide which external capability to invoke. The inside-out perspective adds a crucial twist: **the agent should act to reduce its own uncertainty before that uncertainty causes downstream harm**.

What does this mean concretely?

- Before submitting a purchase order, verify the currency code format by executing a validation tool *probe*, not just trusting the LLM's internal representation
- Before relying on retrieved policy, execute a freshness check: "Is this document superseded by a newer version?" as a separate tool call whose result determines whether to proceed
- When an observation returns ambiguous status (e.g., "queued" vs "completed"), the agent should proactively poll or check status rather than proceeding on the most generous interpretation
- When a tool call fails with a schema mismatch, the agent should generate a *diagnostic query* ("what fields does this endpoint actually accept?") rather than retrying the same malformed call

In each case, the agent is not just executing the task. It is *using action to calibrate its own perception*—to turn ambiguous environmental signals into unambiguous state updates. That is inside-out acting.

The procurement team's failure with "USD dollars" is not just an argument filling error. It is a failure to treat the schema contract as *something to be verified through action* before the write is attempted. An inside-out agent would have: (1) drafted the payload, (2) executed a validation tool in sandbox to check schema compliance, (3) corrected based on feedback, (4) only then executed the real write. That pattern—probe → observe → adjust → commit—is the inside-out loop.

## Practically Speaking: Action Surface Chooser (Enhanced)

| Surface | Domain fit | Primary strength | Escalate when | Inside-Out pattern |
|---------|------------|------------------|---------------|--------------------|
| Typed API | Enterprise systems with stable interfaces | Replayable, inspectable, scoped permissions | Required capability missing from API | Validate payload against schema *before* execution; probe for feature flags |
| Code execution | Software, data transformation, reproducible tasks | Executable output, easier rollback, testable | Must touch external UI-bound system | Run in sandbox first; check exit codes; verify side effects before accepting |
| SQL / queries | Structured data analytics | Strong semantics, auditable, measurable | Task depends on visual/interactive state | Validate query syntax + explain plan *before* execution; check row counts match expectations |
| Browser automation | Web-native workflows with no API | Works where APIs incomplete | DOM drift, visual ambiguity, captcha | Verify page state after each action; detect unexpected redirects; checkpoint before sensitive operations |
| GUI automation | Legacy/closed applications with visual UI only | Access to otherwise inaccessible systems | Stability of selectors/layout | Use computer vision confidence thresholds; verify visual state changed as expected; have human validation fallback |

**The inside-out rule:** Whatever surface you choose, build a *probe-observe-adjust* loop before committing to irreversible actions. Action is not just for doing work; it is for calibrating the agent's own state representation.

## Escalation Spine

**Default:** Typed APIs or code execution, depending on task domain. These surfaces give you schemas, permissions, replayability, and clean observations. They also support inside-out probing: validation tools, sandbox execution, dry runs.

**Escalate to browser automation** when the system of record has no usable API but is web-based and stable enough to support interaction. Signal: you need page-level state that the backend does not expose. Expect brittleness; compensate with more aggressive state verification after each action.

**Escalate to GUI automation** only when every cleaner surface is unavailable. Signal: legacy or closed applications with visual UI but no automation hooks. Treat this as a fallback with known brittleness. Add confidence scoring and human-in-the-loop validation.

**Create new tools** when existing tools cannot express the required operations. This is a higher-order escalation: the agent must be able to generate, test, and validate code-like specifications that become executable artifacts.

**Never escalate upward** from typed APIs to free-form text or from code to browser—that is a step backward in observability.

## What to Skip (For Now)

**Out of scope for this practical cut:**

- **Physical action** (robotics, real-world manipulation). The companion covers broader action learning and perception-action coupling. For most builders today, the practical center sits in structured digital action.
- **Action learning paradigms** beyond tool调用 (multi-turn RL training, reward modeling). These are research frontiers; the deployable center is still single-turn tool invocation with human-crafted prompts.
- **Perception-action coupling** in embodied settings (sensor fusion, motor control loops). Relevant for robotics, less so for enterprise software agents.
- **General computer use as a default**. The "computer use" metaphor bundles radically different forms under one label. The serious stance is stricter: pick the narrowest surface that reaches the task.

**If you find yourself reaching for these, ask instead:** Can the environment provide a stronger surface? Is there an API, a query interface, or an executable layer that would make the action more inspectable? Have you exhausted the inside-out calibration patterns (probe → verify → adjust) on the current surface?

## Resources And References

### [Builder Blueprint: Action Systems and Tool Use](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/03-action-tool-use-blueprint.md)

This blueprint translates the essay's argument into concrete defaults, escalation rules, and anti-patterns. It is the operator layer for making action decisions.

### Theoretical Foundations

#### [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761) (2023)

Toolformer changed the conceptual burden of proof: tool use can be part of the model's operating pattern rather than an external wrapper. It does not solve workflow design but makes tool invocation architecturally normal (Schick et al.)

#### [Gorilla: Large Language Model Connected with Massive APIs](https://arxiv.org/abs/2305.15334) (2023)

Gorilla treats tool use as an argument-construction problem. Failures are often wrong function selection or wrong parameter binding, not general intelligence deficits. It pushes attention toward schemas, retrieval over tool descriptions, and exact invocation (Patil et al.)

#### [SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](https://arxiv.org/abs/2405.15793) (2024)

SWE-agent demonstrates the value of a strong action interface with replayability and observability. Files, commands, tests, and logs create an auditable loop. The deeper lesson: many teams should seek software-like interfaces for non-software work (Yang et al.)

### Tool Categories and Frontiers

#### [HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face](https://arxiv.org/abs/2303.17580) (2023)

HuggingGPT treats the LLM as a controller over specialized capabilities. It widens the meaning of action without collapsing it into unstructured orchestration. Valuable when a task requires multimodal or specialist tools rather than a single generic tool layer (Shen et al.)

#### [A Real-World WebAgent with Planning, Long Context Understanding, and Program Synthesis](https://arxiv.org/abs/2307.12856) (2024)

WebAgent demonstrates digital action over real websites. Browser action is a common escalation surface with real robustness costs (Deng et al.)

#### [OmniParser for Pure Vision Based GUI Agent](https://arxiv.org/abs/2408.00203) (2024)

OmniParser shows why GUI action is the clearest example of reach increasing while structure and control decrease. It is a fallback for closed environments (Gu et al.)

#### [ChemCrow: Augmenting large-language models with chemistry tools](https://arxiv.org/abs/2304.05376) (2023)

ChemCrow demonstrates tool-driven domain specialization. Integrating 18 expert-designed tools (OPSIN, calculators, chemistry software) enables complex chemical reasoning and synthesis planning (Bran et al.)

#### [SciToolAgent: Scientific Toolaugent with over 500 tools](https://arxiv.org/abs/2406.11999) (2024)

SciToolAgent shows how multi-tool integration can revolutionize research domains. It integrates web APIs, ML models, function calls, databases, and more (Xi et al.)

### Multi-Turn RL (Emerging Paradigm)

#### [RAGEN: Reinforcement Learning for Multi-turn Agent Interactions](https://arxiv.org/abs/2405.16416) (2025)

RAGEN designs a modular multi-turn RL system for LLM agents with trajectory-level optimization, StarPO-S algorithm, and robustness techniques (trajectory filtering, critic incorporation, gradient stabilization) (Li et al.)

#### [ReSearch: Learning to Search with Reasoning via Reinforcement Learning](https://arxiv.org/abs/2405.20198) (2024)

ReSearch integrates search operations into the reasoning process, where each search is dynamically influenced by prior reasoning steps and shapes future reasoning in multi-turn interactions. Enables strong QA performance without supervised training data (Lee et al.)

#### [WebAgent-R1: Reinforcement Learning for Web Agents](https://arxiv.org/abs/2502.18577) (2025)

WebAgent-R1 modifies GRPO for multi-turn RL training and applies asynchronous trajectory rollouts with dynamic context compression. Enables learning from direct online web interaction with binary rewards (Liu et al.)

### Structured Data Action

#### [BIRD: A Big Bench for Large-Scale Database Grounded Text-to-SQL](https://arxiv.org/abs/2305.03111) (2023)

BIRD frames SQL as a real enterprise action surface with accuracy, execution-safety, and observability constraints (Li et al.)

#### [Spider 2.0: Evaluating Language Models on Real-World Enterprise Text-to-SQL Workflows](https://arxiv.org/abs/2411.07763) (2025)

Spider 2.0 shows how quickly structured-data action becomes enterprise-shaped once schemas, conventions, and workflow context are realistic (Lei et al.)

### Summary and Distinguished References

The action chapter's most profound contribution is not the tool-use ladder itself but the **inside-out vs outside-in** theoretical framing. This cognitive science insight implies that effective agents must use action to calibrate their own perceptual states—proactive verification, probing, and state validation before committing to irreversible steps.

The **tool learning triad** (discovery, creation, usage) provides a higher-level architectural segmentation that complements the five-seams diagnostic model.

**Multi-turn RL** represents the research frontier: moving from single-turn tool invocation to experience-based policy improvement. This is where action systems will evolve in the next 2-3 years.

**Future challenges** (efficiency, evaluation, multi-modality, privacy, safety, model-tool balance) are not academic—they should inform every action design decision today.
