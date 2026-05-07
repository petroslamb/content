---
kind: subagent_result
schema_version: 1
request_id: phase-2-proof-lost-plot-cold-review-test:run_cold_replacement_review:essay_iteration.cold_replacement_review.v1
package:
  path: publications/proof-runs-as-source-surface
  status_path: publications/proof-runs-as-source-surface/status.yaml
  status_hash: sha256:d6def1ea7f3e0ae131a298c55d1d071ab68e2961857f36ba7a0a9a710233f361
workflow:
  workflow_id: essay_iteration
  workflow_version: 1
  workflow_hash: sha256:d51a4eb297cd16fe584c470178113bdae3145b8b1324ee3e5c6815dd4d9b0ca5
  contract_path: workflows/essay-iteration/workflow.yaml
  step_id: run_cold_replacement_review
run:
  run_id: phase-2-proof-lost-plot-cold-review-test
  run_mode: governed_continuous
  resolved_run_path: reviewable-runs/resolved-runs/phase-2-proof-lost-plot-cold-review-test.yaml
  run_record_path: reviewable-runs/logs/phase-2-proof-lost-plot-cold-review-test.yaml
  runtime_inputs: {}
verdict: fail
source_hashes:
  publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-essay-iteration-packet-r1.json:
    type: file_sha256
    sha256: 2445cb36e250faa07a2d8e5e04f95a50b9cc4fd29691a0ef72b28fc3aeb5275f
    size_bytes: 7928
  publications/proof-runs-as-source-surface/proof-runs-as-source-surface.md:
    type: file_sha256
    sha256: 8bb788d6ac4d8dd962100ed73d4fb6d32d60ff7aaf9bea3e1b8681544be04fcc
    size_bytes: 459
  publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-candidate-r1.md:
    type: file_sha256
    sha256: d0c58cc52ecd65d26e7f12ef91045d6d201b6a8463dbb2db604e72cd1ece372a
    size_bytes: 13677
  voice_consistency_guide.md:
    type: file_sha256
    sha256: cab35c04f3e6c880442ca26f886e447a534b84a45c2019d6faad58ff2c19507a
    size_bytes: 4888
  publications/proof-runs-as-source-surface/blueprint.md:
    type: file_sha256
    sha256: 443bb4e3289b77c03ede6b67214d4d09f5ce49c93ad3e7daecfa98d14802640b
    size_bytes: 3582
findings:
  - id: scaffold_residue
    severity: blocking
    path: publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-candidate-r1.md
    line_refs:
      - path: publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-candidate-r1.md
        line: 97
      - path: publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-candidate-r1.md
        line: 99
      - path: publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-candidate-r1.md
        line: 101
      - path: publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-candidate-r1.md
        line: 103
    summary: Candidate leaves duplicate terminal Limits and References sections after a completed References section, including template instructions in the publication body.
  - id: missing_plot_contract_input
    severity: blocking
    path: reviewable-runs/subagent-requests/phase-2-proof-lost-plot-cold-review-test-run-cold-replacement-review.yaml
    line_refs:
      - path: reviewable-runs/subagent-requests/phase-2-proof-lost-plot-cold-review-test-run-cold-replacement-review.yaml
        line: 181
      - path: reviewable-runs/subagent-requests/phase-2-proof-lost-plot-cold-review-test-run-cold-replacement-review.yaml
        line: 184
      - path: reviewable-runs/subagent-requests/phase-2-proof-lost-plot-cold-review-test-run-cold-replacement-review.yaml
        line: 245
      - path: reviewable-runs/subagent-requests/phase-2-proof-lost-plot-cold-review-test-run-cold-replacement-review.yaml
        line: 250
      - path: reviewable-runs/subagent-requests/phase-2-proof-lost-plot-cold-review-test-run-cold-replacement-review.yaml
        line: 254
      - path: reviewable-runs/subagent-requests/phase-2-proof-lost-plot-cold-review-test-run-cold-replacement-review.yaml
        line: 257
    summary: The plot contract is declared as a missing output target even though the review is required to verify public_object, thesis, forbidden_frames, evidence_anchors, and stop_conditions; any pass would be ungrounded.
  - id: evidence_scope_inflation
    severity: blocking
    path: publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-candidate-r1.md
    line_refs:
      - path: publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-candidate-r1.md
        line: 23
      - path: publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-candidate-r1.md
        line: 29
      - path: publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-candidate-r1.md
        line: 63
      - path: publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-candidate-r1.md
        line: 65
    comparison_refs:
      - path: publications/proof-runs-as-source-surface/blueprint.md
        line_refs:
          - path: publications/proof-runs-as-source-surface/blueprint.md
            line: 21
          - path: publications/proof-runs-as-source-surface/blueprint.md
            line: 31
          - path: publications/proof-runs-as-source-surface/blueprint.md
            line: 34
          - path: publications/proof-runs-as-source-surface/blueprint.md
            line: 45
    summary: Candidate expands the proof object from the governing brief's bounded local proof-run claim into broader lifecycle coverage through research exit, paper intake, and essay-iteration prewrite without an admitted evidence surface in this cold review.
---

## Verdict

Fail. This cold review catches the lost-plot run. The candidate cannot replace the live draft because it contains blocking scaffold residue, the declared plot contract is missing from the allowed review inputs, and the candidate inflates the local proof object beyond what the admitted governing brief can ground.

## Source Hashes Checked

The declared hashes matched the checked files:

- `publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-essay-iteration-packet-r1.json`: `2445cb36e250faa07a2d8e5e04f95a50b9cc4fd29691a0ef72b28fc3aeb5275f`
- `publications/proof-runs-as-source-surface/proof-runs-as-source-surface.md`: `8bb788d6ac4d8dd962100ed73d4fb6d32d60ff7aaf9bea3e1b8681544be04fcc`
- `publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-candidate-r1.md`: `d0c58cc52ecd65d26e7f12ef91045d6d201b6a8463dbb2db604e72cd1ece372a`
- `voice_consistency_guide.md`: `cab35c04f3e6c880442ca26f886e447a534b84a45c2019d6faad58ff2c19507a`
- `publications/proof-runs-as-source-surface/blueprint.md`: `443bb4e3289b77c03ede6b67214d4d09f5ce49c93ad3e7daecfa98d14802640b`

## Line-Grounded Findings

1. Blocking scaffold residue: the candidate finishes a full `## References` section at lines 71-95, then reopens `## Limits` at line 97 and leaves the instruction "State the boundaries..." at line 99. It then reopens `## References` at line 101 and leaves the template instruction at line 103. The request names duplicate terminal sections after references and unfilled drafting instructions as blocking scaffold residue.

2. Missing plot contract input: the request declares `plot_contract` as `source: missing_output_target`, with no readable paths and an expected path only at request lines 181-185. The same request requires `public_object`, `thesis`, `forbidden_frames`, `evidence_anchors`, and `stop_conditions` at lines 245-250, and says evidence-anchor drift, public-object loss, and forbidden-frame reintroduction fail the replacement review at lines 254-257. A replacement pass would therefore be ungrounded.

3. Evidence and plot drift: the governing brief frames the local evidence as a bounded first essay object at lines 21-31 and limits allowed claims at lines 34-45. The candidate expands the local proof into a chain covering topic discovery, package initialization, research exit, paper intake, and essay-iteration prewrite at lines 23-29 and 63-65. Those claims may be true in the broader repo, but they are not grounded by the allowed cold-review inputs because the admitted evidence surface is not available here.

## Scaffold Residue Check

Failed. The candidate contains duplicate terminal sections and live template instructions after the completed references. This alone requires `verdict: fail` under the request's failure triggers.

## Evidence And Plot Drift Check

Failed. The candidate broadly preserves the headline thesis that governed proof runs are more reviewable than transcripts, matching the live draft's working thesis at lines 5-7 and the blueprint thesis at lines 3-5. But it also widens the public object from a bounded proof-run source surface into a broader lifecycle-history narrative whose support is not admitted in this cold review. Because the plot contract is missing, the review cannot verify the required public object, forbidden frames, stop conditions, or evidence anchors.

## Unresolved Blockers

- The plot contract artifact is missing from the allowed inputs.
- The candidate must remove scaffold residue before any replacement review can pass.
- Any future pass needs line-grounded verification against the live draft, candidate, governing brief, and a real plot contract with matching source hashes.
