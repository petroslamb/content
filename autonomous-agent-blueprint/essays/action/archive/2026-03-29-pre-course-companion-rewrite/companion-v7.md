# Action Companion

Two workflows can solve the same business task and still inhabit different engineering worlds. One approves a request through a typed API with explicit schemas, scoped permissions, and machine-readable outcomes. The other achieves the same visible result by driving a browser, reading page state, and inferring whether the site means "done," "queued," or "something changed but the page did not say it plainly." Both may appear agentic in a demo. Only one gives the builder a boundary sturdy enough to diagnose when the result goes wrong.

That difference is why action design keeps punishing loose thinking. Once a workflow can write, submit, execute, or modify state, reliability becomes a property of the surface as much as of the model. Fluency drops in importance. Reconstruction, permissions, recovery behavior, and environmental feedback become the real operating questions.

The public essay keeps the law hard and narrow. This companion owns the surrounding terrain: surface comparison, seam-level diagnosis, approval and recovery design, and the broader action frontier that would have diluted the public chapter if it stayed there.

## Surface Choice Decides What Counts As Reliability

Teams often compare action surfaces as though they were just different delivery channels for the same capability. They are not. A typed API, a constrained data interface, a browser workflow, and a GUI automation loop create different operating conditions even when they point at the same task.

Take a simple approval flow. If the system can call a typed API, reliability means argument validation, least privilege, clean status returns, and replayable writes. If the same workflow has to operate through SQL or another constrained data interface, reliability now depends on query safety, transaction boundaries, row-level scope, and whether the system can prove what changed. If it has to work through a browser, reliability depends on page state, selectors, timing, and whether the site exposes enough structure to distinguish queued work from completed work. If it has to work through a GUI, the workflow inherits visual ambiguity, layout drift, hidden state, and weaker recoverability. The task may still be "approve the request." The engineering object is no longer the same.

That is why the escalation rule stays strict. Start with the narrowest surface that still reaches the work. Move from API to constrained code or data interfaces only when the task naturally lives there. Move to browser only when the system of record exposes no cleaner path. Move to GUI only when every better boundary is unavailable. This is not conservatism for its own sake. It is how the action layer stays auditable.

## The Pipeline Still Fails At Specific Seams

The field still collapses action into one big capability word. Production systems do not fail that way. They fail at seams.

One seam is tool need detection. The workflow stays in prose too long and answers from plausibility when it should have reached for live state. Another is tool selection. Several interfaces look close enough that the wrong one gets chosen even though the task was understood. Another is argument construction. The right endpoint gets called with the wrong field shape, stale enum, or mismatched units. Then comes execution scope. A tool that can search documentation should not quietly sit next to one that can submit irreversible changes with the same trust posture. The last seam is result integration. Raw output comes back from the environment, and the workflow treats a warning, queue state, or partial success as permission to proceed.

That seam-by-seam view is more useful than almost any benchmark summary because it tells you what to instrument. If the model keeps choosing the wrong tool, enrich the catalog and narrow the retrieval problem. If it chooses correctly but writes malformed arguments, fix schemas and validation. If it keeps moving forward on ambiguous state, strengthen the observation contract. The anti-pattern is to call all of this agent behavior and then reach for a bigger model.

## Approval And Recovery Belong Inside The Boundary

Teams often talk as though approval and recovery sit after action design, as cleanup layers added once the real interface work is done. The causal order is the reverse. Approval is part of the surface the moment an action has a meaningful cost. Recovery is part of the surface the moment the environment can return partial success, queued work, or ambiguous state.

A well-designed action boundary therefore does more than describe a call. It says which writes can happen automatically, which require review, what evidence must be attached before execution, and what the system should do when the environment answers with something weaker than success or failure. Idempotent writes, dry runs, reversible operations, partial-completion states, and explicit retry policy are not decoration. They are what keep action from turning one bad generation into an expensive incident.

This is another place where typed interfaces win more often than the field likes to admit. They make approval points and recovery states easier to declare. Browser and GUI layers can still be valuable, but they often bury partial completion inside human-facing signals that are harder to classify and harder to replay.

That difference should change how a team evaluates the surface. It is not enough to ask whether the workflow completed the task. The review has to ask whether the boundary exposed enough structured state for a human or downstream system to trust the result. If the answer is no, the surface may still be dazzling in a demo and unfit for production.

## A Useful Contrast: API, Data, Browser, GUI

The cleanest operator comparison in this terrain is not between papers. It is between surfaces builders routinely confuse.

Typed API action is the gold standard when it exists. The interface says what can happen, what arguments are valid, and what the environment will return. The workflow can gate writes, replay calls, and reason over structured outcomes.

Constrained code and data action deserve more respect than the field gives them. A workflow that issues queries, validates rows, and writes through strict transactions is not doing less agentic work than one that clicks through a browser. It is often doing more governable work. Builders should stop treating SQL, typed records, and constrained automation as boring edge cases. They are frequently the best place to put real autonomy.

Browser action is a fallback, not an upgrade. It becomes necessary when the system of record is web-native and the usable API is missing, incomplete, or politically unavailable. Browser agents can still be effective, but they inherit timing issues, brittle selectors, visual clutter, and thinner feedback loops. The system is acting through a representation designed for people, not for machines.

GUI action is the expensive last resort. It matters for legacy software, closed tools, and interface-bound environments, but it should be treated as a tax. More reach. Less legibility. More generality. Weaker contracts. Teams that jump there too early usually do so because computer use sounds like the most advanced version of agency. In practice it is often just the least structured surface available.

## The Frontier Is Real, But It Is Not The Default

There is real value beyond the conservative center. Specialist orchestration matters once one general layer is not enough. Tool creation inside the loop matters once the workflow repeatedly finds missing affordances. Computer-use work still deserves attention because some important software refuses to expose machine-friendly boundaries. None of that changes the default build order.

The useful second-pass lesson is restraint informed by range. Know what the frontier is proving. Do not confuse that with what a sane production system should start with. Most teams still get farther by making one action boundary legible than by chasing the most general surface in the literature.

The durable prestige metric is not apparent generality. It is reconstructibility under scrutiny. The best action layer is usually not the one with the broadest reach. It is the one that can prove what changed, why it was allowed to change, and how a reviewer would replay the boundary if something later went wrong.

## Analytical References

**[Toolformer note](../../reference/papers/toolformer.md).** This note is the cleanest source on why tool invocation matters as a conceptual bridge rather than as a product flourish. It is useful when a builder needs to explain why reaching for a tool is part of competence and not merely a wrapper around text generation.

**[Gorilla note](../../reference/papers/gorilla.md).** This note is about API discrimination and argument construction. It helps when the workflow understands the task but still fails at endpoint choice, field shape, or spec drift.

**[SWE-agent note](../../reference/papers/swe_agent.md).** This note is about agent-computer interfaces that make action replayable. It is the right reference when the argument turns on machine-checkable feedback, inspectable steps, and narrower action boundaries that localize failure.

**[WebAgent note](../../reference/papers/webagent.md).** This note is about browser-native action when the environment refuses to expose a cleaner interface. It is useful as a cautionary source on why browser action inherits brittleness rather than magically granting maturity.

**[AppAgent note](../../reference/papers/appagent.md).** This note is about GUI and app-surface action in closed environments. It matters when the builder needs a reference for why general computer use expands reach while weakening contracts and recovery.

## Sources Behind This Chapter

The core sources behind this chapter are [*Toolformer*](https://arxiv.org/abs/2302.04761), [*Gorilla*](https://arxiv.org/abs/2305.15334), and [*SWE-agent*](https://arxiv.org/abs/2405.15793). They matter together because they move action away from the vague category of tool use and toward the stricter question of what kind of interface still lets a builder diagnose failure. Toolformer makes invocation legible, Gorilla sharpens the problem into interface choice and argument construction, and SWE-agent shows what happens when the environment answers in a replayable way.

The adjacent terrain extends that same logic across broader surfaces. Browser and GUI agents matter because they expose what happens when the environment refuses to cooperate with machine-friendly contracts. Structured data interfaces matter because they show that narrower, harsher surfaces often produce better automation than more theatrical ones. These topics belong in the companion because the public chapter needed to stay centered on the doctrine law and the decision rule.

The broader picture of the chapter is surface discipline under consequence. The [public essay](./01-action-tool-use-v7.md) keeps only the hard law and the seam-level diagnosis. The [action blueprint](../../core/practical-chapter-blueprints/03-action-tool-use-blueprint.md) turns that law into build order and anti-patterns. The paper notes are where the interested reader can go back to the source layer and see how tool invocation, interface selection, and replayable environments became one operating rule about accountable state change.
