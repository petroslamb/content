# Synthetic Agent Card: Web Form Agent

**Status:** `synthetic validation artifact`

- task class: browser-based form completion
- control loop: observe -> summarize -> act -> re-check state -> hold for approval
- allowed tools: browser control, screenshot or DOM inspection, attachment handling
- evidence surface: visible page state, receipts, portal fields
- verification mode: state verification before and after action
- approval boundary: final submit, purchase, or external commitment
- dominant risk: claiming success from a visible message while final state is actually wrong
