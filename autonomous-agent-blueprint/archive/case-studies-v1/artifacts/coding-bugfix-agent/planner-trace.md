# Planner Trace: Coding Bugfix Agent

## Step 1: Reproduce

- run the failing serializer test
- confirm the exact failure payload

## Step 2: Inspect

- search for `discount_percent` and serializer logic
- inspect invoice serialization path and any nearby normalization helpers
- inspect recent tests around discount handling

## Step 3: Form hypothesis

- zero-discount normalization is happening after serialization instead of before field emission
- the serializer is emitting a cosmetic block that should be suppressed for `0%`

## Step 4: Patch narrowly

- modify the serializer guard, not unrelated pricing logic
- keep the change in the invoice serialization scope

## Step 5: Verify

- rerun the target test
- run nearby invoice serialization regressions
- review the diff for accidental scope expansion

## Step 6: Hold for approval

- provide diff summary, tests run, and residual risk
