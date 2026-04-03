"""
Hand-written Zone decision rule, derived from the shallow decision tree
learned on the GA/MAL/PAR/STI/IM gates.

The function `zone_from_gates` is intended as a simple, explicit heuristic
for mapping the Gate‑1 scores to the friction Zone:

  - Inputs: GA, MAL, PAR, STI, IM (each in {0,1,2})
  - Derived: H = GA + MAL + PAR, E = STI + IM
  - Output: Zone string ('🔴 Red', '🟠 Orange', '🟡 Yellow', '🟢 Green')

This does not mutate the dataset; running this file as a script will only
evaluate the rule against existing labels in `scored_architectures.csv`.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "scored_architectures.csv"


def zone_from_gates(ga: int, mal: int, par: int, sti: int, im: int) -> str:
    """
    Canonical Zone heuristic (v1), matching the learned depth‑3 tree:

      - Let H = GA + MAL + PAR
      - Let E = STI + IM

      If E <= 3:
        If H <= 3:
          If STI <= 1:  Red
          Else:         Orange
        Else:           Yellow
      Else (E >= 4):
        If PAR <= 1:
          If MAL <= 1:  Orange
          Else:         Red
        Else (PAR >= 2): Green
    """
    h = ga + mal + par
    e = sti + im

    if e <= 3:
        if h <= 3:
            if sti <= 1:
                return "🔴 Red"
            return "🟠 Orange"
        return "🟡 Yellow"

    # e >= 4
    if par <= 1:
        if mal <= 1:
            return "🟠 Orange"
        return "🔴 Red"
    return "🟢 Green"


def _eval_against_csv() -> None:
    df = pd.read_csv(CSV_PATH)

    def to_int(series: pd.Series) -> pd.Series:
        return pd.to_numeric(series, errors="coerce").fillna(0).astype(int)

    ga = to_int(df["GA"])
    mal = to_int(df["MAL"])
    par = to_int(df["PAR"])
    sti = to_int(df["STI"])
    im = to_int(df["IM"])

    preds = [
        zone_from_gates(int(g), int(m), int(p), int(s), int(i))
        for g, m, p, s, i in zip(ga, mal, par, sti, im)
    ]

    true = df["Zone"].astype(str).str.strip()

    correct = sum(p == t for p, t in zip(preds, true))
    total = len(df)
    acc = correct / total if total else 0.0

    print(f"Evaluated zone_from_gates on {total} rows.")
    print(f"Exact Zone matches: {correct}/{total}  (accuracy={acc:.3f})")

    # Optional: show a small sample of disagreements for manual inspection.
    mismatches = df[true != preds].copy()
    mismatches = mismatches.assign(
        Zone_pred=[
            p for p, (t, _) in zip(
                preds,
                zip(true, preds),
            )
            if t != _
        ]
    )
    if not mismatches.empty:
        print("\nSample disagreements (up to 10 rows):")
        cols = ["ID", "Architecture", "GA", "MAL", "PAR", "STI", "IM", "Zone", "Zone_pred"]
        print(mismatches[cols].head(10).to_string(index=False))


if __name__ == "__main__":  # pragma: no cover
    _eval_against_csv()
