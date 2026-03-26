# Cross-Case Comparison Matrix

Use this file to decide whether the enterprise, coding, or web dossier is your closest starting point.

| Dimension | Enterprise policy memo | Coding bugfix agent | Web form agent |
| --- | --- | --- | --- |
| Runtime loop | retrieve -> draft -> verify -> hold for publication approval | inspect -> patch -> test -> review -> hold for merge approval | observe -> summarize -> act -> re-check page state -> hold for submission approval |
| Core system records | policy task spec, evidence table, memo verification report | bug task spec, repo evidence, test-backed verification report | browser task spec, page-state evidence, final-state verification report |
| Governance needs | approval before publication or external circulation | approval before merge or destructive repo action | approval before submit, purchase, or external commitment |
| Dominant verification mode | evidence grounding plus freshness and policy checks | executable feedback, regression coverage, and diff review | page-state confirmation, evidence matching, and final-state checks |
| Dominant failure mode | stale or superseded policy text looks current | target test passes while nearby regression risk remains | dynamic page state resets a high-impact field |
| When to start here | the output is a policy-sensitive, reviewable knowledge deliverable | repository state and tests are the strongest source of truth | live page state is the main source of uncertainty |

## Quick Rule

- Start from enterprise when the main problem is governed drafting against trusted internal knowledge.
- Start from coding when the main problem is bounded code change with cheap executable verification.
- Start from web when the main problem is stateful navigation in an untrusted environment.
