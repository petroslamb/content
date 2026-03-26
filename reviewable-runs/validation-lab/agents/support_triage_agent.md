# Synthetic Agent Card: Support Triage Agent

**Status:** `synthetic validation artifact`

- task class: internal support issue triage
- control loop: gather context -> retrieve prior guidance -> classify -> propose next step
- allowed tools: ticket retrieval, knowledge search, tagging, draft response
- evidence surface: ticket text, policy snippets, prior known issue records
- verification mode: classification checks, source matching, confidence threshold
- approval boundary: usually none for internal tagging, but explicit reason must be visible
- dominant risk: retrieval-heavy runs that look grounded while hiding missing provenance
