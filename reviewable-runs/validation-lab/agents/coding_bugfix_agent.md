# Synthetic Agent Card: Coding Bugfix Agent

**Status:** `synthetic validation artifact`

- task class: bounded repository bugfix
- control loop: inspect -> patch -> test -> review
- allowed tools: shell, file inspection, edit, test runner
- evidence surface: failing tests, source files, diffs
- verification mode: targeted regression plus nearby checks
- approval boundary: merge or destructive repo action
- dominant risk: passing the target test while leaving nearby regression risk under-checked
