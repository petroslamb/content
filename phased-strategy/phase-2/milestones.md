# Phase 2 Milestones

Phase 2 is now ordered around executable contracts, validation, traces, and gates first. The CLI and cockpit come after those foundations stabilize.

## Subphase Read

| Subphase | Job | Depends On | Done When |
| :--- | :--- | :--- | :--- |
| **2.1 Executable Workflow Contract** | Make `workflow.yaml` the primary machine contract for target workflows. | Phase 1.5 contract surfaces and current workflow frontmatter. | Target workflows have authored `workflow.yaml` files with ordered steps, required context, allowed tools/paths, outputs, verification, gates, and trace requirements. |
| **2.2 Enforcement and Validation Layer** | Make undeclared context, tools, and paths denyable, and define stage validation hooks. | Stable `workflow.yaml` contract. | Stage execution can detect undeclared inputs and produce bounded validation or drift findings instead of relying on prose discipline alone. |
| **2.3 Trace and Provenance Minimums** | Add the minimum trace and promoted-output state needed for semantic debugging. | Stable workflow and validation contracts. | Run records carry context hashes, workflow version/hash, parent artifact ids, validation results, gate ids, and the minimal promoted-output state needed for contradiction/provenance awareness. |
| **2.4 Gate Runtime and `content-agent`** | Create resumable gate artifacts and a thin CLI over the stable contract. | Stable workflow, validation, and trace artifacts plus the gate protocol. | `content-agent` can `status`, `next`, `run`, `review`, and `init` without becoming a second orchestration language. |
| **2.5 Local Cockpit** | Add a thin browser reader/approver over filesystem-backed truth. | Stable gate store and trace records. | A local cockpit shows package state, pending gates, and recent runs without becoming the source of truth. |
| **2.6 Editorial Automation** | Add structured style/compliance reporting and source-improvement suggestions. | Stable stage execution path and article-polish boundaries. | Editorial automation produces reports and suggestions, not autonomous rewrite authority. |

## Execution Order

The intended order is the same as the subphase numbering:

1. contract
2. enforcement and validation
3. traces and small provenance state
4. gate runtime and thin CLI
5. cockpit
6. editorial automation

That ordering is deliberate. Phase 2 should not start with a CLI or dashboard that sits on unstable workflow semantics.

## Subphase Notes

### 2.1 Executable Workflow Contract

This is the anchor subphase. It decides what the platform can execute and what it must refuse.

The machine contract must cover:

- ordered steps
- required context
- allowed tools
- allowed paths
- outputs
- verification hooks
- approval gates
- trace requirements

### 2.2 Enforcement and Validation Layer

This is where the publication’s strongest thesis lands operationally. Specs become meaningful only when the runtime can enforce and validate them.

The initial target is not perfect conformance. It is bounded denial and bounded checking:

- undeclared tools should be rejectable
- undeclared paths should be rejectable
- undeclared context should be visible as a violation
- source-linked drift checks should exist where they are high value

### 2.3 Trace and Provenance Minimums

This subphase should add enough trace structure for semantic debugging without demanding full provenance graphs.

The platform minimum is:

- context file paths and hashes
- workflow version/hash
- parent artifact ids
- validation results
- gate ids
- minimal contradiction/provenance state for promoted outputs

### 2.4 Gate Runtime and `content-agent`

`content-agent` should be thin first.

It should wrap stable lifecycle machinery rather than absorbing unstable orchestration logic. The initial command surface is:

- `content-agent status`
- `content-agent next`
- `content-agent run`
- `content-agent review`
- `content-agent init`

### 2.5 Local Cockpit

The cockpit is a reader and approver over file-backed truth, not a new control plane.

Its job is to expose:

- package state
- pending review gates
- recent runs

### 2.6 Editorial Automation

This is deliberately late. It depends on a stable runtime path and clear boundaries around what a report may do.

The starting point is:

- voice/style reports
- structured violations
- source-improvement suggestions based on repeated correction patterns

Not autonomous promotion and not autonomous rewriting.

## Phase 2 Gate Read

Before Phase 2 can honestly close, the repo should show:

1. stable `workflow.yaml` contracts for the platform-targeted lifecycle stages
2. stage execution that can deny or surface undeclared context, tools, and paths
3. resumable review gates that are visible outside terminal logs
4. trace records rich enough to support source-linked debugging
5. at least three full essay lifecycles completed through the platform path rather than legacy direct scripts
