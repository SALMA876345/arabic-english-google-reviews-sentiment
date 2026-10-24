"""Shared metrics computation for Phase 3 -- single source of truth so every
experiment's numbers are computed the same way and can be cross-checked
against the saved prediction files (the Reproducibility Auditor's job).
"""
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support, confusion_matrix,
)

LABEL_ORDER = ["Negative", "Neutral", "Positive"]


def compute_metrics(true_labels, pred_labels):
    y_true = list(true_labels)
    y_pred = list(pred_labels)
    acc = accuracy_score(y_true, y_pred)
    p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(
        y_true, y_pred, labels=LABEL_ORDER, average="macro", zero_division=0)
    p_weighted, r_weighted, f1_weighted, _ = precision_recall_fscore_support(
        y_true, y_pred, labels=LABEL_ORDER, average="weighted", zero_division=0)
    p_c, r_c, f1_c, support_c = precision_recall_fscore_support(
        y_true, y_pred, labels=LABEL_ORDER, average=None, zero_division=0)
    per_class = {
        LABEL_ORDER[i]: {"precision": p_c[i], "recall": r_c[i], "f1": f1_c[i], "support": int(support_c[i])}
        for i in range(len(LABEL_ORDER))
    }
    cm = confusion_matrix(y_true, y_pred, labels=LABEL_ORDER)
    return {
        "n": len(y_true),
        "accuracy": acc,
        "precision_macro": p_macro,
        "recall_macro": r_macro,
        "macro_f1": f1_macro,
        "weighted_f1": f1_weighted,
        "per_class": per_class,
        "confusion_matrix": cm.tolist(),
        "label_order": LABEL_ORDER,
    }


def bootstrap_macro_f1_ci(true_labels, pred_labels, n_iterations=2000, seed=42):
    """Bootstrap 95% CI for macro-F1 by resampling test rows with replacement."""
    y_true = np.array(true_labels)
    y_pred = np.array(pred_labels)
    n = len(y_true)
    if n < 30:
        return {"note": "sample too small for a meaningful bootstrap CI (n<30)", "n": n}
    rng = np.random.default_rng(seed)
    scores = []
    for _ in range(n_iterations):
        idx = rng.integers(0, n, size=n)
        _, _, f1, _ = precision_recall_fscore_support(
            y_true[idx], y_pred[idx], labels=LABEL_ORDER, average="macro", zero_division=0)
        scores.append(f1)
    scores = np.array(scores)
    return {
        "point_estimate": float(np.mean(scores)),
        "ci_lower_2.5": float(np.percentile(scores, 2.5)),
        "ci_upper_97.5": float(np.percentile(scores, 97.5)),
        "n_iterations": n_iterations,
        "seed": seed,
        "n": n,
    }


def paired_bootstrap_macro_f1_diff(true_labels, pred_labels_a, pred_labels_b, n_iterations=2000, seed=42):
    """Paired bootstrap test for whether model A's macro-F1 differs from model B's,
    on the SAME frozen test rows. Returns observed diff, CI, and a two-sided p-value
    (proportion of bootstrap diffs crossing zero relative to the observed sign)."""
    y_true = np.array(true_labels)
    pa = np.array(pred_labels_a)
    pb = np.array(pred_labels_b)
    n = len(y_true)
    if n < 30:
        return {"note": "sample too small for a meaningful significance test (n<30)", "n": n}
    rng = np.random.default_rng(seed)

    def macro_f1(yt, yp):
        _, _, f1, _ = precision_recall_fscore_support(yt, yp, labels=LABEL_ORDER, average="macro", zero_division=0)
        return f1

    observed_diff = macro_f1(y_true, pa) - macro_f1(y_true, pb)
    diffs = []
    for _ in range(n_iterations):
        idx = rng.integers(0, n, size=n)
        diffs.append(macro_f1(y_true[idx], pa[idx]) - macro_f1(y_true[idx], pb[idx]))
    diffs = np.array(diffs)
    # two-sided p-value: proportion of bootstrap diffs at or beyond zero in the
    # opposite direction of the observed difference, doubled
    if observed_diff >= 0:
        p = 2 * np.mean(diffs <= 0)
    else:
        p = 2 * np.mean(diffs >= 0)
    p = min(p, 1.0)
    return {
        "observed_diff_macro_f1": float(observed_diff),
        "ci_lower_2.5": float(np.percentile(diffs, 2.5)),
        "ci_upper_97.5": float(np.percentile(diffs, 97.5)),
        "p_value_two_sided": float(p),
        "n_iterations": n_iterations,
        "seed": seed,
        "n": n,
    }


def holm_bonferroni(p_values):
    """Returns adjusted p-values (Holm-Bonferroni step-down), same order as input."""
    arr = np.array(p_values)
    order = np.argsort(arr)
    m = len(arr)
    adjusted = np.empty(m)
    running_max = 0.0
    for rank, idx in enumerate(order):
        adj = (m - rank) * arr[idx]
        running_max = max(running_max, adj)
        adjusted[idx] = min(running_max, 1.0)
    return adjusted.tolist()
