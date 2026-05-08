# content-agent-handoff

Use this skill when a `content-agent` generated subagent request assigns bounded
workflow work and requires a worker-authored result artifact.

## Authority

The request artifact, workflow YAML, package status, root policy, gate
contracts, and integration decisions are authoritative. This skill is an
operator aid only. Do not infer extra read paths, write paths, tools, or
approval authority from this file.

## Worker Procedure

1. Read the request artifact first.
2. Use only the declared input paths, request metadata, and explicitly allowed
   repo docs needed to execute the handoff.
3. Write only the declared workflow outputs and result artifact paths.
4. Echo the request `source_hashes` exactly in the result unless the proper
   verdict is `stale`.
5. Use a verdict from the request's declared verdict enum.
6. Keep findings line-grounded with a repo path and positive line number.
7. Run every command listed in `verification_requirements.commands[]` exactly
   as declared.
8. Record those command results in result frontmatter under
   `verification.commands[]`.
9. Repair malformed result metadata before returning control.
10. Return only the minimal final response requested by the request
    `exit_protocol`.

## Result Frontmatter

For Phase 2.7a requests, include verification evidence like:

```yaml
verification:
  commands:
    - command: ./content-agent validate --workflow essay_iteration --package example --format json
      exit_code: 0
      success: true
      short_failure_summary: none
```

Each command entry must include:

- `command`: non-empty string.
  Use the exact command string from `verification_requirements.commands[]`.
- `exit_code`: integer when the process ran. Use `null` only when the command
  could not launch and the result verdict is not `pass`.
- `success`: boolean.
- `short_failure_summary`: non-empty string. Use `none` only when
  `success: true`.

## Negative Outcomes

A `fail`, `defer`, or `stale` verdict still needs a valid result artifact. Do
not skip source hashes, findings, or verification evidence just because the
substantive outcome is negative.

Use `stale` when request source hashes no longer match the relevant current
files. Use `defer` when the request cannot be completed without a human or
missing dependency. Use `fail` when the requested check or work completed and
found a blocking problem.

## Integration Boundary

Do not write or claim an integration decision unless the request explicitly
assigns that role. For the default handoff path, the parent session owns
accepting, rejecting, or deferring worker results under
`reviewable-runs/integration-decisions/`.
