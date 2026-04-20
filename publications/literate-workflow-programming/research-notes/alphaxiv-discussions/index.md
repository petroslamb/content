# alphaXiv Discussion Index

This index tracks alphaXiv assistant sessions that materially shaped the `literate-workflow-programming/` package.

Use this index differently from `papers/index.md`:

- papers are evidence
- assistant sessions are research discussions and pressure tests
- local extraction notes are the citable package artifact
- raw remote history remains recoverable through the alphaXiv session id

## Retrieval

List recent homepage sessions:

```bash
.venv/bin/alphaxiv assistant list --json --limit 100
```

Recover a full session history:

```bash
.venv/bin/alphaxiv assistant history <session-id>
```

## Tracked Sessions

| Date | Session | Status | Local Extraction | Why It Matters |
| :--- | :--- | :--- | :--- | :--- |
| 2026-04-20 | `019dabcb-1fff-7d63-b509-f3ecf087b2ac` / `Robust autonomy workflow design` | Distilled as cluster | [`019dabc6-019dabcb-icm-workflow-cluster.md`](019dabc6-019dabcb-icm-workflow-cluster.md) | ICM follow-up cluster that pushed the package toward enforcement, least-privilege context, runtime validation, and semantic debugging. |
| 2026-04-20 | `019dabc9-1e0e-72e1-8d5f-9c19b676fd14` / `ICM Folder vs Framework` | Distilled as cluster | [`019dabc6-019dabcb-icm-workflow-cluster.md`](019dabc6-019dabcb-icm-workflow-cluster.md) | ICM follow-up cluster that clarified the folder-vs-framework boundary for sequential, human-reviewed workflows. |
| 2026-04-20 | `019dabc8-7190-7403-9a1e-22e00ca2e2e3` / `ICM vs. Prod Agent Repo` | Distilled as cluster | [`019dabc6-019dabcb-icm-workflow-cluster.md`](019dabc6-019dabcb-icm-workflow-cluster.md) | ICM follow-up cluster that tested whether ICM-like folders are enough for a production repo. |
| 2026-04-20 | `019dabc6-5b80-7537-bb7b-ce33954cc023` / `Agent harness design test` | Distilled as cluster | [`019dabc6-019dabcb-icm-workflow-cluster.md`](019dabc6-019dabcb-icm-workflow-cluster.md) | ICM follow-up cluster that compared folder contracts with harness design concerns. |
| 2026-04-20 | `019dac64-2079-70cb-98cd-07677f1310e5` / `Markdown Workflow Compiler` | Distilled | [`019dac64-markdown-workflow-compiler.md`](019dac64-markdown-workflow-compiler.md) | First direct discussion of markdown workflow docs, skills, indexes, imports, package state, and reviewable logs as an English programming/compiler substrate. |
| 2026-04-20 | `019dac7e-9593-70a6-bb54-167db4667d47` / `Literate Workflow Thesis Test` | Distilled | [`019dac7e-literate-workflow-thesis-test.md`](019dac7e-literate-workflow-thesis-test.md) | Pressure-tested the package thesis against the P0 intake batch and produced the spec/source/log hierarchy that now drives the package. |

## Intake Rule

When an alphaXiv assistant session contributes a claim, decision, vocabulary choice, or paper shortlist:

1. add the session id and title here
2. create a compact extraction note
3. link the extraction note from the relevant package research note
4. keep the raw transcript out of the tracked package unless the exact exchange becomes necessary evidence

The extraction note should state what was asked, what papers were in scope, what was adopted, what was rejected, and where the idea entered the package.

## Backfill Boundary

The 2026-04-20 backfill is intentionally bounded to the sessions already named in this package's research notes. Older alphaXiv sessions from other packages should be backfilled only when they directly affected a retained package claim or published argument.
