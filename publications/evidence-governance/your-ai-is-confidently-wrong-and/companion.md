# Evidence Governance: Project Findings & Technical Companion

*This document provides the detailed evidence base for the Evidence Governance flagship essay. It captures the empirical findings from the **eip-verify** project (Ethereum protocol verification).*

## Project Scope

The project analyzed three Ethereum Improvement Proposals (EIPs) and mapped their obligations to state transitions in the Ethereum Execution Specs (Python) and implementations in Geth (Go).

- **EIP-1559**: Fee market overhaul.
- **EIP-2930**: Access list transactions.
- **EIP-7702**: P-fork extension (negative control).

## Dataset Summary

- **Rows analyzed**: 81
- **Direct-adjudication rows**: 47 (reviewed by humans against source code)
- **Model tiers tested**: Claude 3 Opus, Sonnet 3.5, and Haiku.

## Per-Model Performance (47 direct-adjudication rows)

| Model | Rows | Avg Score (/10) | Valid | Follow-up needed |
|---|---:|---:|---:|---:|
| Opus | 20 | 9.4 | 80% | 20% (4 rows) |
| Sonnet | 12 | 9.0 | 92% | 8% (1 row) |
| Haiku | 15 | 5.0 | 13% | 87% (13 rows) |

### Key Findings on Follow-up Burden

- **Aggregate follow-up rate**: 38.3% (18/47 rows).
- **Concentration**: 72.2% of the follow-up burden (13 of 18 rows) came from the cheapest model (Haiku).
- **Adjudication-grade performance**: Opus and Sonnet showed significantly higher validity, suggesting that model choice is a primary governance decision.

## Scored Evidence Artifacts

- **[Scored Dataset](https://github.com/petroslamb/ethereum-protocol-verification/blob/ca15d40/docs/evaluations/sample_scored_run.csv)** (81 mappings)
- **[Contradiction Register](https://github.com/petroslamb/ethereum-protocol-verification/blob/ca15d40/docs/evaluations/contradictions.csv)** (8 tracked contradictions)
- **[Evidence Ledger](https://github.com/petroslamb/ethereum-protocol-verification/blob/ca15d40/docs/evaluations/evidence_ledger.md)** (Claim-level tracking)
- **[Scoring Rubric](https://github.com/petroslamb/ethereum-protocol-verification/blob/ca15d40/docs/evaluations/scoring_rubric.md)** (5-dimension quality assessment)

## EIP-Specific Findings

1. **The Negative Control (EIP-7702)**: The pipeline correctly identified EIP-7702 as unimplemented in Geth v1.13.14, demonstrating the system's ability to handle negative evidence.
2. **Phase Boundary Benefits**: Dividing the verification into distinct phases (Obligation Extraction, Spec Mapping, Client Mapping) prevented error propagation and allowed for single-phase replays.
3. **Draft Location Drift**: Semantic matching was required over simple ID matching, as LLMs frequently re-numbered obligations between runs.

---
*Evidence artifacts pinned to commit [`ca15d40`](https://github.com/petroslamb/ethereum-protocol-verification/tree/ca15d40).*
