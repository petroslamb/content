# Harness Proof Run Template

Use this template to test whether a general-purpose agent harness can operate this repo from the tracked contract, workflow docs, and command surface without bespoke hand-holding.

This is a Phase 1.5 closure template, not a replacement for the core Reviewable Runs records. Use it as the wrapper around the lightest review surface that makes the run reconstructable.

## Run Identity

| Field | Value |
| :--- | :--- |
| Run id | `YYYY-MM-DD_short-name` |
| Package or idea | |
| Operator / harness | |
| Model or runtime | |
| Source thread or trace | |
| Start boundary | |
| Stop boundary | |
| Boundary type | `handoff`, `commit`, `release`, `submit`, `publish`, or `explicit non-approval reason` |
| Phase 1.5 proof class | `research-heavy`, `polish-publish`, `media-distribution`, or `other` |

## Starting Prompt

Record the exact user prompt or automation prompt that started the run.

```text

```

## Allowed Context

List only the tracked surfaces the harness was allowed or expected to discover from.

- `AGENTS.md` / local operator instructions:
- `README.md`:
- `harness_contract.yaml`:
- `harness_policy.yaml`:
- Package README / `status.yaml`:
- Workflow docs:
- Skills:
- Scripts / npm entrypoints:

## Task Boundary

What one objective was the harness supposed to complete?

- Objective:
- Explicit non-goals:
- Stop condition:
- External side effects allowed:
- External side effects forbidden:
- Required approval before mutation:

## Command Surface Used

List the repo-native commands the harness used. Prefer exact commands over summaries.

```bash

```

## Manual Glue Score

| Measure | Count / Rating | Notes |
| :--- | :---: | :--- |
| User prompts after start | | Count only prompts needed to keep the run moving |
| Repo explanations from user | | Count explanations not already present in tracked docs |
| Manual command executions by user | | Include browser/auth handoffs |
| Permission or sandbox handoffs | | Count narrow permission asks or user-exec handoffs |
| Repo-discovery failures | | Missed canonical docs, wrong path assumptions, ignored policy |
| Invented artifacts or unsupported claims | | Should be zero for a passing proof |
| Approval-boundary mistakes | | Should be zero for a passing proof |

Suggested closure rating:

- `PASS`: minimal prompt glue, correct boundary behavior, no unsupported artifacts, correct final state
- `PARTIAL`: useful run, but one or two repair prompts or repo-discovery failures were needed
- `FAIL`: harness could not operate from the tracked contract or crossed a boundary incorrectly

## Execution Summary

Write a short factual trace of what happened.

1.
2.
3.

## Evidence And State Used

List the source files, package state, workflow docs, external outputs, or platform state that actually mattered.

| Evidence | Why It Mattered | Freshness / Provenance |
| :--- | :--- | :--- |
| | | |

## Verification

Name the checks run and their results.

| Check | Result | Notes |
| :--- | :---: | :--- |
| `npm run check:harness` | | |
| `git diff --check` / scoped equivalent | | |
| Package-specific validator | | |
| External platform state check | | |
| Final `git status --short` | | |

## Approval And Boundary Behavior

- Was approval required?
- Was approval obtained before the controlled action?
- If approval was not required, why not?
- Did the harness stop at the correct boundary?
- If blocked by sandbox/auth/network, did it ask for narrow permission or provide exact user-exec commands?

## Failure Or Friction Review

Classify every material problem.

| Problem | Class | Corrective Direction |
| :--- | :--- | :--- |
| | `workflow-doc gap`, `contract gap`, `policy gap`, `skill gap`, `script gap`, `sandbox/auth`, `model discipline`, or `package-local gap` | |

## Phase 1.5 Gate Answers

| Gate | Answer | Evidence |
| :--- | :---: | :--- |
| Could the harness determine the next valid action without repo explanation? | `yes`, `partial`, or `no` | |
| Could it start from an idea or package target and produce bounded outputs with correct logs and approval behavior? | `yes`, `partial`, or `no` | |
| Did it succeed with minimal prompt glue and no repo-specific hand-holding beyond the tracked contract? | `yes`, `partial`, or `no` | |

## Final Decision

- Closure rating: `PASS`, `PARTIAL`, or `FAIL`
- Promote to retained proof? `yes` / `no`
- If not promoted, where does the routine record live?
- Required workflow/script/skill hardening:
- Next proof run to attempt:
