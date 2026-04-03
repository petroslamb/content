# Optimization Companion

There are at least three different activities that teams call optimization. One is visible editing on the easiest surface. One is local repair inside a stable workflow. One is real improvement against a fixed objective with regression discipline. Only the last one deserves the name without qualification.

The confusion persists because agent systems present many tempting surfaces. The prompt is easy to tweak. The role description is easy to rewrite. A judge score is easy to chart. A new feedback loop is easy to describe as learning. None of that proves the workflow improved.

The useful second-pass reading of optimization is therefore narrower and harsher than the field likes. Improvement work is only real when the workflow is being treated as an object with stable objectives, comparable runs, and enough instrumentation to tell local gain from global drift.

The public essay keeps the law severe and compact. This companion owns the broader terrain: local-versus-global misreads, bounded feedback loops, judge discipline, and the workflow-search literature that belongs outside the public coda.

## A Concrete Optimization Misread

Take a contract-routing workflow that reads incoming documents, classifies them, extracts key fields, and decides whether they can be auto-routed or need human review.

The team sees recurring mistakes on renewal contracts and starts editing the prompt on the classification node. A few examples are added. The wording gets more specific. The node score improves on the handful of failures everyone remembers. A week later the review queue is noisier, latency is up, and the downstream extraction node is failing more often because the new prompt changed the output shape in subtle ways.

The team says optimization is hard. The real problem is simpler. They optimized a local surface before stabilizing the workflow contract around it.

That is the operator distinction this topic needs. Local optimization can be worthwhile. It becomes dangerous when the team forgets that nodes live inside a system of schemas, routing rules, retry logic, review thresholds, and downstream consumers.

## Start With The Cheapest Truth-Preserving Fix

Many real gains still come from boring surfaces first.

If a node emits inconsistent structure, fix the schema. If routing sends the wrong documents down the brittle path, fix the router. If retries are amplifying noise, fix retry logic. If the tool description hides critical argument constraints, fix the interface. If evaluation cannot tell a rare expensive regression from a minor cosmetic gain, fix the evaluation layer before touching the workflow again.

This is where the field gets the story wrong. It likes to narrate optimization as search over prompts or topologies because those are the visibly intelligent moves. In practice a lot of high-return work is contract repair. Better interfaces often beat better wording.

The escalation rule is simple. Improve the cheapest surface that can plausibly remove the failure without corrupting the measurement story. Prompt work belongs after schema, routing, retrieval, and contract quality are good enough that a prompt change means something.

## The Workflow Is The Real Optimization Object

Once a system has several nodes, review stages, and handoffs, optimization stops being about any one prompt. Nodes, edges, schemas, tools, stop conditions, and failure recovery policies can all become optimization surfaces.

That shift changes what counts as diagnosis. A weak answer may come from bad evidence rather than poor prompting. A slow workflow may come from redundant review rather than weak planning. A spiky correction burden may come from one threshold that routes too many cases into the same fragile path. Treating the workflow as the object forces teams to ask where the failure is actually being produced.

This is also why optimization work starts to look more like systems engineering than prompt craft. Once the workflow becomes the object, every local change needs a story about downstream impact. The team has to explain not only why a node improved, but why the whole workflow should be expected to improve with it.

## Human Review Load Is Part Of The Objective

A lot of optimization stories quietly cheat by treating human effort as outside the score. The model gets a little cleaner, a judge score rises, and the team declares progress while reviewers spend longer untangling edge cases, correcting malformed outputs, or handling a larger queue of false escalations.

That is not a side effect. It is part of the system objective. A workflow that marginally improves one automated node while increasing approval burden, correction time, or exception volume may have gotten worse in the only environment that matters. Review load belongs in the same measurement story as latency, accuracy, and cost because it is one of the main places where bad local optimization hides.

This is also why optimization arguments should keep circling back to who pays for the claimed gain. If the answer is the reviewer, the gain is probably not finished.

## Feedback Loops Are Useful Only While They Stay Bounded

The self-improvement literature is worth keeping, but only under tight control.

*Self-Refine* improves one output through critique and revision. *Reflexion* stores lessons from failure for later attempts. *Voyager* promotes repeated success into reusable routines. These are useful because the surfaces being changed are still bounded and reviewable. The system is not being handed permission to redesign itself wholesale.

That boundedness is the real lesson. A feedback loop earns trust when the change surface is small, the success signal is legible, and regressions are easy to spot. The anti-pattern is to call uncontrolled mutation learning once the system starts changing routing, permissions, or topology without the same discipline a human engineer would demand.

## Judges And Workflow Search Should Arrive Late

Judge systems and topology search matter for the same reason they are easy to misuse. They scale power after simpler decisions have already become legible.

LLM-as-judge helps when human review cannot cover every experiment loop. But a judge is only useful when it is calibrated against a rubric that still matters to the actual workflow. Otherwise the team begins optimizing toward a proxy with unknown blind spots.

*AFLOW* and *GPTSwarm* matter because they treat workflow shape itself as an optimization target. That is a real frontier. It is also the wrong first answer for most teams. If the baseline is still unstable, schemas still drift, or routing is still noisy, workflow search does not rescue the design. It explores a confused space faster.

One more rule keeps the whole topic honest. Track failure categories, not only aggregate scores. A routing tweak that helps easy contracts while harming rare escalations may look better on a dashboard and worse in the actual business. Optimization work gets more serious when teams can say not only that a score moved, but which failure class moved with it.

Stable interfaces deserve the same emphasis. Workflow search is only interpretable when nodes, schemas, and evaluation targets are steady enough that a topology change actually means something. Otherwise the team is comparing moving graphs against moving objectives and calling the confusion exploration.

## Analytical References

**[OPRO note](../../reference/papers/opro.md).** This note is about prompt improvement as an optimization problem. It is the key source when the argument turns on the need for a stable objective before any search or tuning begins.

**[MT-Bench and Chatbot Arena note](../../reference/papers/mt_bench_chatbot_arena.md).** This note is about model-based judging as an operational evaluation pattern. It matters when the workflow needs scalable comparison without pretending judges are magically calibrated.

**[Voyager note](../../reference/papers/voyager.md).** This note is about bounded self-improvement through skill promotion. It is useful when the optimization argument needs a believable example of improvement that does not mutate every surface at once.

**[TextGrad note](../../reference/papers/textgrad.md).** This note is about converting critique into structured optimization signals. It belongs in local-improvement discussions where the target and evaluation loop are already stable.

**[AFLOW note](../../reference/papers/aflow.md).** This note is about workflow topology as an optimization target. It matters when the team is tempted to move from prompt tuning to workflow search before the baseline is actually ready.

## Sources Behind This Chapter

The core sources behind this chapter are [*OPRO*](https://arxiv.org/abs/2309.03409), [*MT-Bench and Chatbot Arena*](https://arxiv.org/abs/2306.05685), and [*Voyager*](https://arxiv.org/abs/2305.16291). They matter together because they define the chapter's central triangle: a stable objective, an operational evaluation layer, and bounded improvement that earns promotion through repeated success. Those are the sources most directly behind the doctrine that optimization becomes real only once the workflow is already measurable.

The surrounding sources widen the territory into the parts of the field that tempt teams to overreach. *TextGrad* matters because it sharpens local optimization over bounded surfaces. *Reflexion* matters because it shows a feedback loop over failure. *AFLOW* and *GPTSwarm* matter because they push optimization up from prompt surfaces to workflow topology itself. They belong in the companion because they show the size of the frontier while also clarifying why the chapter insists on a conservative order of operations.

The broader picture is that optimization only looks glamorous when teams forget what object they are supposed to be improving. The [public essay](06-optimization-v7.md) keeps the doctrinal line hard. The [optimization blueprint](../../core/practical-chapter-blueprints/04-optimization-self-improvement-blueprint.md) turns it into sequencing rules. The paper notes give the interested reader the underlying search, judging, and feedback mechanisms that the companion is deliberately holding inside one slower systems argument.
