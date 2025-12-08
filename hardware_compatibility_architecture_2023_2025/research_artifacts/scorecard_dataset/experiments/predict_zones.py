"""
Explainable modeling experiments for the hardware friction scorecard.

This script:
  - Loads `scored_architectures.csv`.
  - Builds a small, interpretable feature set (gate scores, H/E, era, log10(max params)).
  - Trains simple models (multinomial logistic regression + shallow decision tree)
    to predict the friction `Zone`.
  - Evaluates them with stratified k-fold cross-validation and prints
    paper-friendly summaries (metrics, coefficients, and tree rules).

The CSV is treated as canonical; this script never writes back to it.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd

try:
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold
    from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error
    from sklearn.tree import DecisionTreeClassifier, export_text
except Exception as e:  # pragma: no cover - environment dependency
    raise SystemExit(
        "This script requires scikit-learn. "
        "Install it in a venv with:\n\n"
        "  pip install scikit-learn\n\n"
        f"Import error was: {e}"
    )


THIS_DIR = Path(__file__).resolve().parent
CSV_PATH = THIS_DIR.parent / "scored_architectures.csv"


def _clean_score_series(series: pd.Series) -> pd.Series:
    """Convert score columns like '**5**' to numeric 5."""
    return pd.to_numeric(series.astype(str).str.replace("**", "", regex=False), errors="coerce")


def _parse_max_param(val: object) -> float:
    """Return max parameter count in billions for a row, or NaN if none."""
    if val is None:
        return float("nan")
    s = str(val).strip()
    if not s or s == "[]":
        return float("nan")
    try:
        arr = json.loads(s)
        if isinstance(arr, list) and arr:
            return float(max(float(x) for x in arr))
    except Exception:
        return float("nan")
    return float("nan")


def _zone_to_index(zone: str) -> int:
    """
    Map the `Zone` string (e.g., '🟢 Green', '🟡 Yellow') to an ordinal index:
      Red=0, Orange=1, Yellow=2, Green=3.
    """
    z = (zone or "").strip()
    if not z:
        return -1
    emoji = z[0]
    mapping = {
        "🔴": 0,
        "🟠": 1,
        "🟡": 2,
        "🟢": 3,
    }
    return mapping.get(emoji, -1)


def build_dataset() -> Tuple[pd.DataFrame, pd.Series]:
    """
    Load the CSV and construct:
      - X: feature matrix
      - y: ordinal Zone indices (0..3)
    """
    df = pd.read_csv(CSV_PATH)

    # Core gate scores.
    for col in ["GA", "MAL", "PAR", "STI", "IM"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # H/E as numeric aggregates.
    if "H" in df.columns:
        df["H_num"] = _clean_score_series(df["H"])
    else:
        df["H_num"] = df["GA"] + df["MAL"] + df["PAR"]

    if "E" in df.columns:
        df["E_num"] = _clean_score_series(df["E"])
    else:
        df["E_num"] = df["STI"] + df["IM"]

    # Parameter scale features.
    df["max_param"] = df["Param_Billions"].apply(_parse_max_param)
    # Log10 of parameter count; fill missing with median to avoid skewing.
    df["log10_max_param"] = np.log10(df["max_param"])
    df["log10_max_param"].replace([np.inf, -np.inf], np.nan, inplace=True)
    median_log = df["log10_max_param"].median()
    df["log10_max_param"].fillna(median_log if not np.isnan(median_log) else 0.0, inplace=True)

    # Era as one-hot.
    era_dummies = pd.get_dummies(df["Era"], prefix="Era")

    # Optional production-viability label if needed later.
    zones_idx = df["Zone"].apply(_zone_to_index)

    # Assemble final feature matrix.
    feat_cols = ["GA", "MAL", "PAR", "STI", "IM", "H_num", "E_num", "log10_max_param"]
    X = pd.concat([df[feat_cols], era_dummies], axis=1)

    # Drop any rows with invalid zone index.
    mask_valid = zones_idx >= 0
    X = X[mask_valid].reset_index(drop=True)
    y = zones_idx[mask_valid].reset_index(drop=True)

    return X, y


def run_logistic_cv(X: pd.DataFrame, y: pd.Series, k: int = 5) -> None:
    """Stratified k-fold CV for multinomial logistic regression on Zone."""
    skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)

    all_y_true: List[int] = []
    all_y_pred: List[int] = []

    fold = 1
    for train_idx, test_idx in skf.split(X, y):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        clf = LogisticRegression(
            multi_class="multinomial",
            solver="lbfgs",
            max_iter=2000,
        )
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        all_y_true.extend(y_test.tolist())
        all_y_pred.extend(y_pred.tolist())

        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="macro")
        mae = mean_absolute_error(y_test, y_pred)

        print(f"[LogReg] Fold {fold}: acc={acc:.3f}, macro-F1={f1:.3f}, MAE(Zone)={mae:.3f}")
        fold += 1

    acc = accuracy_score(all_y_true, all_y_pred)
    f1 = f1_score(all_y_true, all_y_pred, average="macro")
    mae = mean_absolute_error(all_y_true, all_y_pred)

    print("\n[LogReg] Overall (stratified k-fold):")
    print(f"  Accuracy:      {acc:.3f}")
    print(f"  Macro-F1:      {f1:.3f}")
    print(f"  MAE (Zone):    {mae:.3f}")

    # Fit once on full data for coefficient interpretation.
    clf_full = LogisticRegression(
        multi_class="multinomial",
        solver="lbfgs",
        max_iter=2000,
    )
    clf_full.fit(X, y)

    print("\n[LogReg] Coefficients (multinomial, per class vs baseline):")
    for class_idx, coef in enumerate(clf_full.coef_):
        coef_pairs = sorted(
            zip(X.columns, coef),
            key=lambda t: abs(t[1]),
            reverse=True,
        )
        top = ", ".join(f"{name}={val:+.3f}" for name, val in coef_pairs[:8])
        print(f"  Class {class_idx}: {top}")


def run_tree_cv(X: pd.DataFrame, y: pd.Series, k: int = 5) -> None:
    """Stratified k-fold CV for a shallow decision tree on Zone."""
    skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)

    all_y_true: List[int] = []
    all_y_pred: List[int] = []

    fold = 1
    for train_idx, test_idx in skf.split(X, y):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        tree = DecisionTreeClassifier(
            max_depth=3,
            min_samples_leaf=3,
            random_state=fold,
        )
        tree.fit(X_train, y_train)
        y_pred = tree.predict(X_test)

        all_y_true.extend(y_test.tolist())
        all_y_pred.extend(y_pred.tolist())

        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="macro")
        mae = mean_absolute_error(y_test, y_pred)

        print(f"[Tree] Fold {fold}: acc={acc:.3f}, macro-F1={f1:.3f}, MAE(Zone)={mae:.3f}")
        fold += 1

    acc = accuracy_score(all_y_true, all_y_pred)
    f1 = f1_score(all_y_true, all_y_pred, average="macro")
    mae = mean_absolute_error(all_y_true, all_y_pred)

    print("\n[Tree] Overall (stratified k-fold):")
    print(f"  Accuracy:      {acc:.3f}")
    print(f"  Macro-F1:      {f1:.3f}")
    print(f"  MAE (Zone):    {mae:.3f}")

    # Fit one shallow tree on all data and print human-readable rules.
    tree_full = DecisionTreeClassifier(
        max_depth=3,
        min_samples_leaf=3,
        random_state=0,
    )
    tree_full.fit(X, y)

    print("\n[Tree] Human-readable rules (depth ≤ 3):")
    print(export_text(tree_full, feature_names=list(X.columns)))


def main() -> None:
    print(f"Loading scorecard from: {CSV_PATH}")
    X, y = build_dataset()
    print(f"Dataset shape: X={X.shape}, y={y.shape}")

    print("\n=== Multinomial Logistic Regression on Zone (ordinal) ===")
    run_logistic_cv(X, y, k=5)

    print("\n=== Shallow Decision Tree on Zone (ordinal) ===")
    run_tree_cv(X, y, k=5)


if __name__ == "__main__":  # pragma: no cover
    main()

