# Governance Record: Failure Review

If the patch later regressed adjacent behavior, the failure review would immediately hit a gap:

- the causal observation behind the patch is not preserved
- reviewers could replay the commands, but not the judgment basis
- root cause would have to be rederived from scratch
