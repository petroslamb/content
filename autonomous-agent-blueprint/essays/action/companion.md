# Action Companion

Most teams say they want an agent that can "use tools." What they usually need is something narrower and harder: a system that can cross one boundary into the world without becoming opaque the moment it does. That is why action design keeps punishing loose thinking. The instant a workflow can write, submit, execute, or modify state, the quality bar changes. Fluency stops mattering first. Reconstruction, permissions, and environmental feedback start mattering more.

The useful distinction is not between systems that have tools and systems that do not. It is between systems that act through governable surfaces and systems that act through surfaces so messy that every failure gets blamed on the model. That is what makes action one of the most practical parts of the package. It drags agent talk out of abstractions and forces a choice about where work should actually happen.

## Surface Choice Decides What Counts As Reliability

Teams often compare action surfaces as though they were just different delivery channels for the same capability. They are not. A typed API, a browser workflow, and a GUI automation loop create different operating conditions even when they point at the same business task.

Take a simple approval workflow. If the system can call a typed API, reliability means argument validation, least privilege, clean status returns, and replayable writes. If it has to work through a browser, reliability now depends on page state, selectors, timing, and whether the site exposes enough structured feedback to distinguish queued work from completed work. If it has to work through a GUI, the system inherits visual ambiguity, layout drift, hidden state, and weaker recoverability. The task may still be "approve the request." The engineering object is no longer the same.

That is why the practical escalation rule stays strict. Start with the narrowest surface that still reaches the work. Move from API to browser only when the required operation is not exposed cleanly. Move from browser to GUI only when every cleaner interface is unavailable. Do not call that conservatism. It is how you keep the action layer auditable.

## The Tool Pipeline Fails In Specific Places

The field still collapses tool use into one big capability word. Production systems do not fail that way. They fail at seams.

One seam is tool need detection. The system stays in prose too long and answers from plausibility when it should have reached for live state. Another is tool selection. Several interfaces look close enough that the wrong one gets chosen even though the task was understood. Another is argument construction. The right endpoint gets called with the wrong field shape, stale enum, or mismatched units. Then comes execution scope. A tool that can search docs should not quietly sit next to one that can submit changes with the same trust posture. The last seam is result integration. Raw output comes back from the environment, and the workflow treats a warning, queue state, or partial success as permission to proceed.

That seam-by-seam view is more useful than almost any benchmark summary because it tells you what to instrument. If the model keeps choosing the wrong tool, enrich the catalog and narrow the retrieval problem. If it chooses correctly but writes malformed arguments, fix schemas and validation. If it keeps moving forward on ambiguous state, strengthen the observation contract. The anti-pattern is to call all of this "agent behavior" and then reach for a bigger model.

## A Useful Contrast: API, Browser, GUI

The cleanest operator comparison in this terrain is not between papers. It is between action surfaces that builders routinely confuse.

Typed API action is the gold standard when it exists. The interface says what can happen, what arguments are valid, and what the environment will return. The workflow can gate writes, replay calls, and reason over structured outcomes.

Browser action is a fallback, not an upgrade. It becomes necessary when the system of record is web-native and the usable API is missing, incomplete, or politically out of reach. Browser agents can still be effective, but they inherit timing issues, brittle selectors, visual clutter, and thinner feedback loops. The system is now acting through a representation designed for people, not for machines.

GUI action is the expensive last resort. It matters for legacy software, closed tools, and interface-bound environments, but it should be treated as a tax. More reach, less legibility. More generality, weaker contracts. A team that jumps there too early usually does so because "computer use" sounds like the most advanced version of agency. In practice it is often just the least structured surface available.

This is where the field still gets the story wrong. It likes to narrate broader action surfaces as signs of maturity. Builders should read them as signs that the environment has stopped cooperating.

## Frontier Work Is Real, But It Is Not The Default

There is real value beyond the conservative center. Specialist orchestration matters once one general layer is not enough. Tool creation inside the loop matters once the system repeatedly finds missing affordances. Computer-use work matters because some important software still refuses to expose machine-friendly boundaries. None of that changes the default build order.

The right second-pass lesson is restraint informed by range. Know what the frontier is proving. Do not confuse that with what a sane production system should start with. Most teams still get farther by making one action boundary legible than by chasing the most general surface in the literature.

One last correction matters here. Structured data work is often treated as a minor branch of tool use when it should be treated as one of the main enterprise action surfaces. A workflow that issues queries, validates rows, and writes through constrained data interfaces is not doing "less agentic" work than one that clicks around a browser. It is often doing more governable work. Builders should stop treating SQL, typed records, and constrained data actions as boring edge cases. They are frequently the best place to put real automation.

## Resources And References

### [Action Essay: Operating Agents I: When the Model Starts Doing Things](../action/01-action-tool-use-v5.md)

Read the essay first for the sharp public claim about when agency begins. It keeps the center of gravity on accountable state change and on the observation contract that makes action reviewable.

### [Builder Blueprint: Action Systems and Tool Use](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/03-action-tool-use-blueprint.md)

The blueprint is where this topic becomes a build sequence: surface selection, execution design, observation design, recovery, and evaluation. Use it when you need to choose a surface rather than just understand why the choice matters.

### [Foundation Agents: Practical Chapters Guide](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/reference/chapters-guide.md)

The guide is the quickest route to the wider map behind the essay. It keeps the action topic anchored to digital execution, surface choice, and seam-level failure analysis instead of vague autonomy claims.

### [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761) (2023)

Toolformer matters because it reframed tool invocation as part of model behavior rather than a purely external wrapper trick. The paper was trying to solve a basic problem: language models were good at describing work but weak at deciding when external capability was needed. Its architectural move was to normalize the idea that calling out to a tool is part of competence.

That lesson still matters. Builders should inherit the behavioral insight, not the fantasy that every workflow should become self-discovered tool use inside one model loop.

### [Gorilla: Large Language Model Connected with Massive APIs](https://arxiv.org/abs/2305.15334) (2023)

Gorilla matters because it treats action as an interface-understanding problem. The paper was not really solving "agency" in the abstract. It was solving API discrimination and argument construction at scale. That is why it remains practical. Many real failures that look like bad reasoning are bad interface binding.

The paper should influence catalog design, schema discipline, and argument validation. It should not be read as a reason to dump an enormous ungoverned tool universe in front of one model and hope retrieval solves policy.

### [SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](https://arxiv.org/abs/2405.15793) (2024)

SWE-agent matters because it shows what happens when the action surface itself becomes governable. The paper was trying to solve software work through a constrained interface of code edits, shell actions, tests, and machine-checkable feedback. Its key move was to make action executable, inspectable, and recoverable.

That is why it is one of the most important papers in this cluster. It proves that a narrower, harsher interface often beats a broader, more theatrical one. Builders should copy the insistence on replayability and environmental confirmation even outside software workflows.

### [A Real-World WebAgent with Planning, Long Context Understanding, and Program Synthesis](https://arxiv.org/abs/2307.12856) (2024)

WebAgent matters because it treats the browser as a real action surface rather than just a retrieval source. It was solving task completion on live web systems, where the environment answers through page state rather than clean APIs.

The paper should influence teams that truly need browser fallback. It should not be read as proof that browser action is preferable whenever it is more general.

### [OmniParser for Pure Vision Based GUI Agent](https://arxiv.org/abs/2408.00203) (2024)

OmniParser matters because GUI action fails first at perception. The paper was trying to turn raw visual interfaces into machine-usable objects so the rest of the control loop could function at all. Its architectural move is upstream of action: if the environment cannot be parsed into usable state, the best planner in the world still acts blindly.

That is why it belongs here. Builders should take it as a reminder that GUI action is a perception tax layered on top of an already weak interface contract.
