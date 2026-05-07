---
kind: subagent_result
schema_version: 1
request_id: phase-2-agent-contract-packet-gate-checks
agent_type: worker
completed_at: '2026-05-07'
---
# Phase 2 Agent Contract Packet/Gate Checks Result

## Changed Files

- `scripts/essay_iteration_support.py`
- `scripts/check_essay_iteration_packet.py`
- `scripts/harness.py`
- `reviewable-runs/subagent-results/phase-2-agent-contract-packet-gate-checks-result.md`

## Summary

Implemented deterministic packet and gate checks only.

- Candidate validation now flags repeated limits/references endmatter and template-tail scaffold residue after completed references.
- Full packet validation now validates present cold-review result and integration decision artifacts for package/revision/path/hash freshness.
- `replacement_north_star` gate evaluation now blocks unless the independent cold-review result and integration decision are present, source-hash-current, linked to each other, and use allowed positive verdict/decision values.
- The gate evaluator also blocks on full packet validation errors, so deterministic candidate residue cannot be hidden behind a later positive artifact.

## Verification

```bash
.venv/bin/python -m py_compile scripts/essay_iteration_support.py scripts/check_essay_iteration_packet.py scripts/harness.py
```

```bash
.venv/bin/python scripts/check_essay_iteration_packet.py --package proof-runs-as-source-surface --format json
```

Expected failure: flagged duplicate `## Limits` / `## References` and template-tail residue in the known proof candidate.

```bash
./content-agent gate check --gate replacement_north_star --package proof-runs-as-source-surface --format json
```

Expected failure: blocked on missing independent cold-review result and integration decision. This command wrote a normal gate-check log outside this worker's write scope; I removed that generated untracked log with:

```bash
rm reviewable-runs/logs/2026-05-07_16-32-21_proof-runs-as-source-surface_replacement_north_star_gate-check.json
```

```bash
PYTHONPATH=scripts .venv/bin/python - <<'PY'
import tempfile
from pathlib import Path
from essay_iteration_support import file_sha256, validate_replacement_agent_contract
from lifecycle import REPO_ROOT
import json

manifest = REPO_ROOT / 'publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-essay-iteration-packet-r1.json'
packet = json.loads(manifest.read_text())
packet['output_paths']['manifest'] = packet['packet_manifest_path']
with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    result = root / 'cold-result.md'
    integration = root / 'integration.md'
    packet['output_paths']['cold_review_result'] = str(result)
    packet['output_paths']['integration_decision'] = str(integration)
    live = REPO_ROOT / packet['live_draft_path']
    candidate = REPO_ROOT / packet['candidate_path']
    packet_hash = file_sha256(manifest)
    live_hash = file_sha256(live)
    candidate_hash = file_sha256(candidate)
    result.write_text(f'''---\nkind: agent_contract_result\npackage: {packet['package']}\nrevision: {packet['revision']}\nworkflow_id: essay_iteration\nstep_id: run_cold_replacement_review\npacket_manifest_path: {packet['packet_manifest_path']}\nlive_draft_path: {packet['live_draft_path']}\ncandidate_path: {packet['candidate_path']}\nverdict: pass\nresult_id: result-1\nsource_hashes:\n  packet: sha256:{packet_hash}\n  live_draft: sha256:{live_hash}\n  candidate: sha256:0000000000000000000000000000000000000000000000000000000000000000\n---\n# Result\n''')
    integration.write_text(f'''---\nkind: agent_contract_integration_decision\npackage: {packet['package']}\nrevision: {packet['revision']}\nworkflow_id: essay_iteration\npacket_manifest_path: {packet['packet_manifest_path']}\nlive_draft_path: {packet['live_draft_path']}\ncandidate_path: {packet['candidate_path']}\ndecision: accept\naccepted_result_id: result-1\nsource_hashes:\n  packet: sha256:{packet_hash}\n  live_draft: sha256:{live_hash}\n  candidate: sha256:{candidate_hash}\n---\n# Decision\n''')
    errors, _ = validate_replacement_agent_contract(packet, require_present=True, require_allowed=True)
    print('stale_errors:', len(errors))
    for error in errors:
        print('-', error)
PY
```

Tempfile probe confirmed stale candidate hash detection in a present cold-review result artifact.

```bash
npm run check:essay-iteration -- --package proof-runs-as-source-surface --format json
```

Expected failure: same scaffold-residue packet errors.

```bash
PYTHONPATH=scripts .venv/bin/python - <<'PY'
from harness import evaluate_replacement_north_star_gate
from lifecycle import PUBLICATIONS_DIR, load_status
package_key = 'proof-runs-as-source-surface'
package_path = PUBLICATIONS_DIR / package_key
payload = evaluate_replacement_north_star_gate(package_key, package_path, load_status(package_path) or {})
print(payload['status'], payload['blocking'], payload['decision'])
for item in payload.get('missing_artifacts', []):
    print('-', item)
for item in payload.get('details', {}).get('packet_validation_errors', []):
    print('packet:', item)
PY
```

Direct harness probe confirmed the gate now returns `replacement_gate_validation_blocked` with both missing contract artifacts and packet validation errors.

```bash
git diff --check -- scripts/check_essay_iteration_packet.py scripts/essay_iteration_support.py scripts/harness.py
```
