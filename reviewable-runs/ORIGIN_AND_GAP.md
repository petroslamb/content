# Origin And Gap

This package exists because the blueprint package had a real missing layer.

The `autonomous-agent-blueprint` blueprints already require most of the ingredients that later became reviewable runs:

- bounded control loops
- replayable and inspectable actions
- episodic traces and prior-failure memory
- explicit verification before important actions
- approval gates for meaningful side effects
- post-incident replay, audit, and root-cause review

What the blueprints did not define clearly was the minimum run-level review surface that ties those requirements together for one meaningful execution.

That was the gap.

## The Original Need

The blueprint package explains how to build serious agents. It says a serious system should reason through a task, use tools in a controlled way, verify important outputs, and escalate to humans when the cost of error is real.

But once a system does all that, a reviewer still needs to ask:

- what exactly was the task
- what happened
- what evidence mattered
- how the result was checked
- who approved the risky step
- what failed or could fail

Those questions were not yet given a canonical run-level contract.

## The First Attempt

The first worked-example layer in this repository used packet-oriented artifact bundles. That historical material now lives under `history/artifact-bundles-v1/`.

That older layer already had the right instinct:

- input or task brief
- planner trace
- evidence or state record
- verification report
- approval record
- failure review

But it still read more like an artifact bundle than a framework.

## The Shift To Reviewable Runs

The key conceptual shift was simple:

The goal is not to teach that a serious system emits six neat markdown files. The goal is to teach that a serious system makes a run reviewable.

That change matters because it turns the framework away from document theater and toward reconstructability:

- the records might be markdown
- or database rows
- or UI events
- or logs plus stored state
- or postmortem documents

What matters is that a meaningful run can be reconstructed credibly enough for review.

## Why This Package Is Separate

This framework is now separated from `autonomous-agent-blueprint` because it is no longer just one downstream note in a literature-driven package.

It is a repo-grown framework with its own:

- origin
- problem statement
- vocabulary
- model
- examples
- evaluation surface
- template surface

The blueprint package remains the upstream architecture source. This package is the downstream run-review framework that grew out of those needs.

## Gap Statement

The clean statement of the gap is this:

The blueprints define a bounded, verified, approval-gated agent architecture, but they do not by themselves define what records a serious run must expose or reconstruct for human review.

Reviewable runs is that missing run-level contract.

## What Problem It Solves

This package is trying to solve four practical problems at once:

1. traces alone are usually too thin for high-trust review
2. logging, evaluation, and governance often get discussed separately even though operators need them together
3. architecture docs often stop before showing what one inspectable run should look like
4. teams need a lighter and more operationally honest concept than "explainability"

The package answer is not model introspection. It is structured run reconstructability.
