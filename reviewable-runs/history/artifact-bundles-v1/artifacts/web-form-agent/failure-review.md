# Failure Review: Web Form Agent

## Failure

The reimbursement form auto-refreshed after attachment upload and silently reset the claim category, leaving the page in a state that looked complete but was prepared for the wrong reimbursement type.

## Why it is plausible

This is a classic web-agent failure: the environment changes under the agent, and a superficially complete page can still be semantically wrong.

## Taxonomy mapping

- [`../../../../evaluation/failure-mode-catalog.md`](../../../../evaluation/failure-mode-catalog.md): `Observation-action confusion`
- [`../../../../evaluation/failure-mode-catalog.md`](../../../../evaluation/failure-mode-catalog.md): `Indirect prompt injection`

## Checklist controls that should catch it

- [`../../../../evaluation/architecture-readiness-checklist.md`](../../../../evaluation/architecture-readiness-checklist.md): `Is ReAct or an equivalent loop used when tools or environment state matter?`
- [`../../../../evaluation/architecture-readiness-checklist.md`](../../../../evaluation/architecture-readiness-checklist.md): `Are irreversible actions guarded by deterministic checks and human approval?`
- [`../../../../evaluation/architecture-readiness-checklist.md`](../../../../evaluation/architecture-readiness-checklist.md): `Are inter-agent messages, files, and screenshots treated as untrusted unless proven otherwise?`

## What would reduce the failure

- require a final DOM-state diff before opening the approval gate
- make category confirmation a separate verification item after every refresh
- keep the approval packet focused on the exact visible submission state rather than on earlier extracted evidence alone

## Decision

Keep the web default architecture. Strengthen final page-state verification rather than falling back to a more fragile GUI-first design.
