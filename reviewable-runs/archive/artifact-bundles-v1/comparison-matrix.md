# Cross-Case Comparison Matrix

> Historical note: This matrix belongs to the archived v1 case-study layer. The current default comparison lives in [`../../examples/teaching/comparison-matrix.md`](../../examples/teaching/comparison-matrix.md).

Use this file to decide whether the enterprise, coding, or web archetype is your closest starting point.

| Dimension | Enterprise policy memo | Coding bugfix agent | Web form agent |
| --- | --- | --- | --- |
| Control loop | decompose -> retrieve/tool -> draft artifact -> verify -> approval | inspect -> patch -> test -> diff review -> approval | observe -> summarize -> act -> verify page state -> approval |
| Memory design | semantic retrieval plus episodic review history | working memory plus repo-scoped episodic and procedural memory | short working memory plus episodic navigation traces |
| Action surface | typed retrieval and bounded enterprise tools | shell, file edits, search, tests, diff generation | DOM-aware browser actions with bounded submissions |
| Verification style | evidence grounding, schema checks, policy checks, CoVe-style review | targeted tests, static checks, diff review, scope checks | page-state verification, extraction checks, submission-state confirmation |
| Approval model | approval before publishing or external circulation | approval before merge or destructive repo change | approval before purchase, submission, or external message |
| Safety boundary emphasis | retrieved docs are untrusted data, not instructions | repo scope, mutating command controls, generated-code distrust | hostile page content, prompt injection, and action gating |
| Main failure mode | stale or superseded policy evidence enters the memo | narrow test selection misses a regression | dynamic page state or hostile content causes a wrong submission path |
| Escalation trigger | retrieval ambiguity or policy conflicts remain high | the patch touches multiple subsystems or flaky failures persist | the site is visually unstable or lacks reliable DOM controls |

## Quick Decision Rule

- Start from the enterprise archetype when the main output is a typed or reviewable knowledge artifact.
- Start from the coding archetype when code execution and test feedback are the strongest verification layer.
- Start from the web archetype when live page state is the main environment and approval before submission matters.
