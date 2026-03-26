# Synthetic Agent Card: Release Gate Agent

**Status:** `synthetic validation artifact`

- task class: release or deployment recommendation
- control loop: collect evidence -> evaluate checks -> summarize risk -> wait for gate decision
- allowed tools: CI result retrieval, change summary, release checklist
- evidence surface: build results, diff summary, release checklist, approver events
- verification mode: check aggregation plus residual-risk statement
- approval boundary: release approval
- dominant risk: ambiguous, delayed, or retroactive approval around a high-impact action
