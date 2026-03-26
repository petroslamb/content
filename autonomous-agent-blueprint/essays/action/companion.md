# Action Companion

Most teams say they want an agent that can "use tools." What they usually need is something narrower and harder: a system that can cross one boundary into the world without becoming opaque the moment it does. Action design keeps punishing loose thinking for that reason. The instant a workflow can write, submit, execute, or modify state, the quality bar changes. Fluency stops mattering first. Reconstruction, permissions, and environmental feedback start mattering more.

The useful distinction is not between systems that have tools and systems that do not. It is between systems that act through governable surfaces and systems that act through surfaces so messy that every failure gets blamed on the model. That is what makes action one of the most practical parts of the package. It drags agent talk out of abstractions and forces a choice about where work should actually happen.

The public essay keeps the law narrow. This companion owns the surrounding terrain: surface comparison, seam-level diagnosis, and the broader action surface that would have diluted the public chapter.

## Surface Choice Decides What Counts As Reliability

Teams often compare action surfaces as though they were just different delivery channels for the same capability. They are not. A typed API, a browser workflow, and a GUI automation loop create different operating conditions even when they point at the same business task.

Take a simple approval workflow. If the system can call a typed API, reliability means argument validation, least privilege, clean status returns, and replayable writes. If it has to work through a browser, reliability now depends on page state, selectors, timing, and whether the site exposes enough structured feedback to distinguish queued work from completed work. If it has to work through a GUI, the system inherits visual ambiguity, layout drift, hidden state, and weaker recoverability. The task may still be "approve the request." The engineering object is no longer the same.

The practical escalation rule therefore stays strict. Start with the narrowest surface that still reaches the work. Move from API to browser only when the required operation is not exposed cleanly. Move from browser to GUI only when every cleaner interface is unavailable. Do not call that conservatism. It is how you keep the action layer auditable.

## The Tool Pipeline Fails In Specific Places

The field still collapses tool use into one big capability word. Production systems do not fail that way. They fail at seams.

One seam is tool need detection. The system stays in prose too long and answers from plausibility when it should have reached for live state. Another is tool selection. Several interfaces look close enough that the wrong one gets chosen even though the task was understood. Another is argument construction. The right endpoint gets called with the wrong field shape, stale enum, or mismatched units. Then comes execution scope. A tool that can search docs should not quietly sit next to one that can submit changes with the same trust posture. The last seam is result integration. Raw output comes back from the environment, and the workflow treats a warning, queue state, or partial success as permission to proceed.

That seam-by-seam view is more useful than almost any benchmark summary because it tells you what to instrument. If the model keeps choosing the wrong tool, enrich the catalog and narrow the retrieval problem. If it chooses correctly but writes malformed arguments, fix schemas and validation. If it keeps moving forward on ambiguous state, strengthen the observation contract. The anti-pattern is to call all of this "agent behavior" and then reach for a bigger model.

## Approval And Recovery Are Part Of The Action Surface

Teams often talk as though approval and recovery sit after action design, as clean-up layers added once the real interface work is done. The causal order is the reverse. Approval is part of the surface the moment an action has a meaningful cost. Recovery is part of the surface the moment the environment can return partial success, queued work, or ambiguous state.

A well-designed action boundary therefore does more than describe a call. It says which writes can happen automatically, which require another review stage, what evidence must be attached before execution, and what the system should do when the environment answers with something weaker than success or failure. Idempotent writes, dry runs, reversible operations, partial-completion states, and explicit retry policy are not operational decoration. They are what keep action from turning one bad generation into an expensive incident.

This is another place where typed APIs win more often than the field admits. They make approval points and recovery states easier to declare. Browser and GUI layers can still be valuable, but they often bury partial completion inside human-facing signals that are harder to classify and harder to replay.

That difference changes how a team should evaluate the surface. It is not enough to ask whether the agent completed the task. The review has to ask whether the boundary exposed the right state for a human or downstream system to trust the result. If the answer is no, the action surface may be usable in a demo and still unfit for production.

## A Useful Contrast: API, Browser, GUI

The cleanest operator comparison in this terrain is not between papers. It is between action surfaces that builders routinely confuse.

Typed API action is the gold standard when it exists. The interface says what can happen, what arguments are valid, and what the environment will return. The workflow can gate writes, replay calls, and reason over structured outcomes.

Browser action is a fallback, not an upgrade. It becomes necessary when the system of record is web-native and the usable API is missing, incomplete, or politically out of reach. Browser agents can still be effective, but they inherit timing issues, brittle selectors, visual clutter, and thinner feedback loops. The system is now acting through a representation designed for people, not for machines.

GUI action is the expensive last resort. It matters for legacy software, closed tools, and interface-bound environments, but it should be treated as a tax. More reach, less legibility. More generality, weaker contracts. A team that jumps there too early usually does so because "computer use" sounds like the most advanced version of agency. In practice it is often just the least structured surface available.

This is where the field still gets the story wrong. It likes to narrate broader action surfaces as signs of maturity. Builders should read them as signs that the environment has stopped cooperating.

## Frontier Work Is Real, But It Is Not The Default

There is real value beyond the conservative center. Specialist orchestration matters once one general layer is not enough. Tool creation inside the loop matters once the system repeatedly finds missing affordances. Computer-use work still deserves attention because some important software refuses to expose machine-friendly boundaries. None of that changes the default build order.

The right second-pass lesson is restraint informed by range. Know what the frontier is proving. Do not confuse that with what a sane production system should start with. Most teams still get farther by making one action boundary legible than by chasing the most general surface in the literature.

One last correction matters here. Structured data work is often treated as a minor branch of tool use when it should be treated as one of the main enterprise action surfaces. A workflow that issues queries, validates rows, and writes through constrained data interfaces is not doing "less agentic" work than one that clicks around a browser. It is often doing more governable work. Builders should stop treating SQL, typed records, and constrained data actions as boring edge cases. They are frequently the best place to put real automation.

That point deserves to stay visible because it changes what teams should celebrate. The most mature action layer is often not the one with the broadest apparent reach. It is the one that can prove what changed, why it was allowed to change, and how a reviewer would replay the boundary if something later goes wrong. The durable prestige metric is reconstructibility, not apparent generality, under scrutiny.

## Sources Behind This Chapter

The core papers here are [*Toolformer*](https://arxiv.org/abs/2302.04761), [*Gorilla*](https://arxiv.org/abs/2305.15334), and [*SWE-agent*](https://arxiv.org/abs/2405.15793). Together they define the chapter's center of gravity. Toolformer makes tool invocation visible as a boundary decision, Gorilla sharpens the problem into interface choice and argument construction, and SWE-agent shows what happens when the environment answers in a replayable way. Read together, they push action away from the vague category of "tool use" and toward the stricter question of what kind of surface still lets a builder diagnose failure.

The next ring of material widens that argument rather than replacing it. Browser and computer-use work such as WebAgent and OmniParser matter because they expose what is lost when the surface gets broader and more human-shaped. They are useful precisely because they show the cost of leaving typed interfaces behind: weaker contracts, thinner observation, and harder recovery. They belong in the companion because they deepen the surface-comparison argument without changing the doctrine that cleaner interfaces should be the default.

The broader picture of this chapter is therefore not "APIs good, browsers bad." It is that action design lives at the boundary where consequence begins and where state has to stay reconstructible. Use the [public essay](../action/01-action-tool-use-v6.md) for the hard law, the [action blueprint](../../core/practical-chapter-blueprints/03-action-tool-use-blueprint.md) for build order and recovery rules, and the paper notes when you want the source-level texture behind those choices.
