# alphaXiv Research

This is the canonical tracked workflow for paper discovery and source discussion using `alphaxiv-py`.

## Purpose

Use alphaXiv to:

- discover papers
- inspect one paper in detail
- build a shortlist
- use the assistant after deterministic retrieval

The assistant is not the first step. Retrieval is.

## Core Principle

Use this order:

1. deterministic retrieval first
2. assistant second
3. package-local paper intake after shortlist decisions

That means:

- `search` for keyword-driven lookup
- `feed` for recent or ranked discovery
- `paper` commands for detailed inspection
- `assistant` only after you have grounded the problem

## Auth Expectations

Public retrieval is enough for much of the workflow, but assistant usage often requires browser-backed login.

Use:

```bash
.venv/bin/alphaxiv auth login-web
```

Treat this as persistent setup for the assistant, not something to rerun before every command.

If assistant chats start feeling slow or overloaded, start a fresh assistant session and carry forward only the minimal recap or paper IDs you still need. Do not keep extending one long chat by default.

## Evidence-Backed Defaults

- Shortlist before synthesis. The assistant is for comparison and explanation after retrieval, not a substitute for retrieval.
- Keep practical anchor papers visible while researching. The recurring successful pattern in this repo is not a loose memo; it is a grounded reading path tied to concrete papers and why they matter.
- Once you know a paper belongs in the project, move it into the package paper-intake workflow quickly instead of leaving it in alphaXiv-only context.

## Canonical Research Flow

1. discover candidates with `search` or `feed`
2. inspect promising papers with `paper show`, `paper abstract`, `paper summary`, `paper overview`, `paper text`, or `paper pdf`
3. build a shortlist before synthesis
4. use `assistant start` or `assistant reply` only once the shortlist or comparison target is clear
5. move selected papers into the package paper-intake workflow
6. if the assistant session becomes sluggish, open a fresh one rather than stretching the same chat indefinitely

## How This Fits The Repo

alphaXiv is the preferred discovery and paper-discussion layer when you are still deciding what belongs in a package’s `papers/` directory.

Once a paper is selected:

1. save the PDF into the package
2. convert it using the paper-intake workflow
3. update the package paper index or source index

## Related Docs And Skill Bundle

- [`../paper-intake/README.md`](../paper-intake/README.md)
- [`../skills/alphaxiv/`](../skills/alphaxiv/)
