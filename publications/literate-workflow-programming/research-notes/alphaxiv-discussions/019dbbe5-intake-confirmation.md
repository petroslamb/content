# alphaXiv Discussion: Intake confirmation

Date: 2026-04-23

Session id: `019dbbe5-e129-73af-8e57-7ac3408671f9`

Title: `Folder Intake: literate-workflow-programming`

Full history:

```bash
.venv/bin/alphaxiv assistant history 019dbbe5-e129-73af-8e57-7ac3408671f9
```

## Question Asked

Confirm which papers from the recent missing-paper pass should actually be intaken into the `harness_papers/` folder, with only three allowed outputs: direct donor, strong adjacent, or exclude from intake.

## Papers Or Claims In Scope

- `2408.04820` / `Natural Language Outlines for Code: Literate Programming in the LLM Era`
- `2502.17441` / `Renaissance of Literate Programming in the Era of LLMs`
- `2510.09073` / `Literate Tracing`
- `2405.06907` / `AIOS Compiler: LLM as Interpreter for Natural Language Programming and Flow Programming of AI Agents`
- `2508.13948` / `Prompt Orchestration Markup Language`
- Package claim boundary: literate workflow source surfaces rather than generic prompt-engineering infrastructure

## Extracted Takeaways

- `2408.04820` and `2502.17441` were reaffirmed as direct donors worth local intake.
- `2510.09073` and `2405.06907` were reaffirmed as strong adjacent papers worth local intake.
- `2508.13948` was explicitly excluded for now because it pushes the package toward prompt styling and markup infrastructure rather than literate workflow source surfaces.

## Adopted

- Intake exactly four papers into `harness_papers/`: `2408.04820`, `2502.17441`, `2510.09073`, and `2405.06907`.
- Leave `2508.13948` out of the local harness library for now.

## Rejected Or Parked

- Do not let POML become a stealth expansion of the package into general prompt-orchestration tooling.

## Where It Entered The Package

- `../../harness_papers/index.md`

## Current Status

- Distilled
