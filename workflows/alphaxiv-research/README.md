---
workflow_id: research
runner_mode: guided
default_skill: alphaxiv
launch_templates: []
required_context:
  - package README or leaf README
  - current research question or thesis direction
  - package evidence surface for shortlisted papers
expected_outputs:
  - shortlist of candidate papers with rationale
  - selected papers ready to move into paper intake
done_when:
  - the shortlist is grounded enough to drive package-local paper intake or source discussion
approval_gate: none
---

# alphaXiv Research

This is the canonical tracked workflow for paper discovery and source discussion using `alphaxiv-py`.

## Purpose

Use alphaXiv to:

- discover papers
- inspect one paper in detail
- build a shortlist
- refine a shortlist into an intake decision
- validate or pressure-test blueprint and draft claims against anchor papers already in scope
- use the assistant after deterministic retrieval

The assistant is not the first step. Retrieval is.

## Research Modes

alphaXiv has two distinct modes in this repo:

### Discovery mode

- Use this when the package still needs candidate papers, adjacent alternatives, or topic exploration.
- The output is a grounded shortlist, not a finished synthesis.

### Validation mode

- Use this when the package already has a blueprint, live draft, or local paper set and the problem is claim quality rather than paper scarcity.
- The output is a narrower, more defensible claim set or a changed top-level frame.

## Working Order

Use this order:

1. deterministic retrieval first
2. assistant second
3. package-local paper intake only after shortlist or validation decisions

That means:

- `search` for keyword-driven lookup and exact-anchor confirmation
- `feed` for recent or ranked discovery
- `paper show`, `paper summary`, and nearby `paper` commands for triage
- `paper pdf download` when a shortlisted paper is promoted into package intake
- `assistant` only after you have grounded the problem and stabilized the relevant anchor set

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
- When a package already has a strong local paper set, use alphaXiv in validation mode before reopening broad discovery. Validate the claims, partitions, or phrasings that might outrun the evidence instead of searching loosely for "more papers."
- Validation mode should stay narrow: inspect the exact anchor papers, then use the assistant only to pressure-test whether the current wording or synthesis is defensible.
- The assistant is useful not just for synthesis, but for pressure-testing whether the top-level framing itself should survive.

## Broad Discovery Flow

1. discover candidates with `search` or `feed`
2. inspect promising papers with `paper show`, `paper abstract`, `paper summary`, `paper overview`, `paper text`, or `paper pdf`
3. build a shortlist before synthesis
4. use `assistant start` or `assistant reply` only once the shortlist or comparison target is clear
5. move selected papers into the package paper-intake workflow
6. if the assistant session becomes sluggish, open a fresh one rather than stretching the same chat indefinitely

## Shortlist Refinement

When discovery has already produced plausible candidates, narrow the set before starting any assistant discussion:

1. use `search` or `paper similar` to confirm nearby alternatives rather than trusting the first hit
2. run `paper show` and `paper summary` on each serious candidate
3. use `paper overview` only when the summary is too compressed to separate close alternatives
4. promote only the papers that materially affect the package claim set

Shortlist refinement is still discovery work. Do not slip into framing claims until the anchor set is stable enough to compare.

## Gap-Closing Evidence Pass

When a package already has a blueprint, draft, and local paper set, use alphaXiv like this:

1. identify the claims or categories that look overstated, overlapping, or weakly evidenced
2. use `search` to confirm the exact anchor papers and nearby alternatives before assuming the current set is complete
3. inspect the exact anchors with `paper show` and `paper summary`, then escalate to other `paper` commands only where the short views are insufficient
4. use `paper pdf download` only when a new candidate is strong enough to be promoted into package intake
5. use the assistant only after retrieval to ask what claims the anchor set licenses, what nearby claims it does not license, and where the wording is outrunning the evidence
6. feed the result back into the blueprint or rewrite plan rather than treating it as an excuse to reopen broad discovery

This is still "research" in repo terms, but it is validation research rather than discovery research.

## Framing Challenge Pass

When the problem is not just a weak sentence but a possibly weak synthesis, use the assistant after the anchor set is stable to challenge the frame itself:

1. ask which higher-level framing the papers genuinely support
2. ask which stronger framing sounds plausible but is not actually earned by the evidence
3. ask what alternative framing is more defensible if the current thesis fails
4. carry the result back into the blueprint and cut or narrow the frame before rewriting

This is the default way to test whether a top-level synthesis should survive. Do not treat a good-sounding metaphor as locked in before the assistant has pressure-tested it against the actual anchors.

## How This Fits The Repo

alphaXiv is the preferred discovery and paper-discussion layer when you are still deciding what belongs in a package’s `papers/` directory.

Once a paper is selected:

1. save the PDF into the package
2. convert it using the paper-intake workflow
3. update the package paper index or source index

## Related Docs And Skill Bundle

- [`../paper-intake/README.md`](../paper-intake/README.md)
- [`../essay-iteration/README.md`](../essay-iteration/README.md)
- [`../skills/alphaxiv/`](../skills/alphaxiv/)
