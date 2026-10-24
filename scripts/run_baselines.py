"""Phase 3 classical baselines: TF-IDF + LogisticRegression / LinearSVC.

For each of E1 (Arabic tourism) and E2 (English matched) and each of the two
classical model families, this script:
  1. Fits TF-IDF on TRAIN only.
  2. Grid-searches ngram_range x C x class_weight (spaces defined in
     configs/training.yaml) -- fit on train, select on validation macro-F1.
     Test is never touched during this search.
  3. Retrains the winning configuration on train, runs inference exactly once
     on the frozen test split.
  4. Saves row-level predictions (results/predictions/*.csv), appends a
     registry row (experiments/registry_baselines.csv), and records final
     test metrics (results/tables/baseline_results_raw.json).

Confidence/score semantics:
  - LogisticRegression: confidence_or_score = predict_proba(...).max(axis=1)
    -- a genuine calibrated-by-training probability for the predicted class.
  - LinearSVC: LinearSVC has no predict_proba. confidence_or_score here is the
    RAW decision_function margin for the predicted class (max over the
    one-vs-rest decision function), NOT a probability. This is reported
    explicitly so it is never misread as a calibrated probability.

Run with: python scripts/run_baselines.py
"""
import json
import sys
import time
from datetime import datetime, timezone
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from utils.data_io import (  # noqa: E402
    LABEL_ORDER,
    SEED,
    load_arabic_tourism,
    load_english_matched,
    save_predictions,
    split_xy,
)
from evaluation.metrics import compute_metrics  # noqa: E402

RESULTS_TABLES = ROOT / "results" / "tables"
RESULTS_TABLES.mkdir(parents=True, exist_ok=True)
REGISTRY_PATH = ROOT / "experiments" / "registry_baselines.csv"
GRIDSEARCH_LOG_PATH = RESULTS_TABLES / "baseline_gridsearch_log.txt"

REGISTRY_COLUMNS = [
    "run_id", "experiment_id", "model", "model_version", "dataset_version",
    "train_count", "validation_count", "test_count", "random_seed",
    "hyperparameters", "training_time_sec", "hardware", "timestamp",
    "git_commit", "status",
]


def load_training_config():
    with open(ROOT / "configs" / "training.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_vectorizer(tfidf_cfg, ngram_range):
    return TfidfVectorizer(
        max_features=tfidf_cfg["max_features"],
        min_df=tfidf_cfg["min_df"],
        sublinear_tf=tfidf_cfg["sublinear_tf"],
        ngram_range=tuple(ngram_range),
    )


def hparam_complexity_key(C, class_weight):
    """Lower = simpler, for tie-breaking: lower C first, then no class_weight
    (None) before 'balanced'."""
    cw_rank = 0 if class_weight is None else 1
    return (C, cw_rank)


def grid_search(model_family, train_texts, train_labels, val_texts, val_labels,
                 tfidf_cfg, model_cfg, log_lines, log_prefix):
    """Fit TF-IDF on train only; try every (ngram_range, C, class_weight)
    combo; fit on train, score (macro-F1) on validation. Returns the full
    results table and the selected (best) config dict."""
    ngram_spaces = tfidf_cfg["ngram_search_space"]
    C_space = model_cfg["C_search_space"]
    cw_space = model_cfg["class_weight_search_space"]

    rows = []
    for ngram_range in ngram_spaces:
        vectorizer = build_vectorizer(tfidf_cfg, ngram_range)
        X_train = vectorizer.fit_transform(train_texts)
        X_val = vectorizer.transform(val_texts)

        for C, class_weight in product(C_space, cw_space):
            if model_family == "logreg":
                clf = LogisticRegression(
                    C=C, max_iter=model_cfg["max_iter"],
                    class_weight=class_weight, random_state=SEED,
                )
            elif model_family == "svm":
                clf = LinearSVC(
                    C=C, class_weight=class_weight, random_state=SEED,
                )
            else:
                raise ValueError(f"unknown model_family {model_family}")

            clf.fit(X_train, train_labels)
            val_pred = clf.predict(X_val)
            metrics = compute_metrics(val_labels, val_pred)
            row = {
                "ngram_range": tuple(ngram_range),
                "C": C,
                "class_weight": class_weight,
                "val_macro_f1": metrics["macro_f1"],
                "val_accuracy": metrics["accuracy"],
                "val_weighted_f1": metrics["weighted_f1"],
            }
            rows.append(row)
            line = (
                f"{log_prefix} ngram={tuple(ngram_range)} C={C} "
                f"class_weight={class_weight} -> val_macro_f1={metrics['macro_f1']:.6f} "
                f"val_acc={metrics['accuracy']:.6f} val_weighted_f1={metrics['weighted_f1']:.6f}"
            )
            print(line)
            log_lines.append(line)

    # Selection: highest val_macro_f1; ties -> simpler hyperparameters
    # (lower C, then no class_weight over 'balanced'); if still tied,
    # prefer the smaller ngram_range (unigram over bigram) as the simpler model.
    def sort_key(r):
        ngram_rank = 0 if r["ngram_range"] == (1, 1) else 1
        return (
            -r["val_macro_f1"],
            r["C"],
            0 if r["class_weight"] is None else 1,
            ngram_rank,
        )

    rows_sorted = sorted(rows, key=sort_key)
    best = rows_sorted[0]
    return rows, best


def run_one(experiment_id, language, dataset_version, df, model_family,
            model_display_name, out_name, train_cfg, log_lines):
    tfidf_cfg = train_cfg["classical"]["tfidf"]
    model_cfg = train_cfg["classical"][model_family]

    train_texts, train_labels, _, _ = split_xy(df, "train")
    val_texts, val_labels, _, _ = split_xy(df, "val")
    test_texts, test_labels, test_ids, test_label_sources = split_xy(df, "test")

    log_prefix = f"[{experiment_id}/{model_family}]"
    print(f"\n=== Grid search: {log_prefix} ===")
    log_lines.append(f"\n=== Grid search: {log_prefix} ===")

    grid_rows, best = grid_search(
        model_family, train_texts, train_labels, val_texts, val_labels,
        tfidf_cfg, model_cfg, log_lines, log_prefix,
    )

    summary = (
        f"{log_prefix} SELECTED: ngram={best['ngram_range']} C={best['C']} "
        f"class_weight={best['class_weight']} (val_macro_f1={best['val_macro_f1']:.6f})"
    )
    print(summary)
    log_lines.append(summary)

    # Retrain on train with the winning config; infer on test exactly once.
    t0 = time.time()
    vectorizer = build_vectorizer(tfidf_cfg, best["ngram_range"])
    X_train = vectorizer.fit_transform(train_texts)
    X_test = vectorizer.transform(test_texts)

    if model_family == "logreg":
        clf = LogisticRegression(
            C=best["C"], max_iter=model_cfg["max_iter"],
            class_weight=best["class_weight"], random_state=SEED,
        )
        clf.fit(X_train, train_labels)
        test_pred = clf.predict(X_test)
        proba = clf.predict_proba(X_test)
        class_order = list(clf.classes_)
        pred_idx = [class_order.index(p) for p in test_pred]
        scores = [proba[i, pred_idx[i]] for i in range(len(test_pred))]
        score_type = "calibrated_probability"
    elif model_family == "svm":
        clf = LinearSVC(C=best["C"], class_weight=best["class_weight"], random_state=SEED)
        clf.fit(X_train, train_labels)
        test_pred = clf.predict(X_test)
        decision = clf.decision_function(X_test)  # shape (n, n_classes) for 3 classes
        if decision.ndim == 1:
            # binary-degenerate case, shouldn't happen with 3 classes
            scores = np.abs(decision).tolist()
        else:
            class_order = list(clf.classes_)
            pred_idx = [class_order.index(p) for p in test_pred]
            scores = [decision[i, pred_idx[i]] for i in range(len(test_pred))]
        score_type = "decision_function_margin_NOT_a_probability"
    else:
        raise ValueError(model_family)

    training_time_sec = time.time() - t0

    pred_path = save_predictions(
        review_ids=test_ids,
        languages=[language] * len(test_ids),
        true_labels=test_labels,
        pred_labels=list(test_pred),
        scores=scores,
        label_provenances=test_label_sources,
        experiment_id=experiment_id,
        run_id=f"run_{experiment_id}_{out_name.split('_', 1)[1].rsplit('_test', 1)[0]}_001",
        out_name=out_name,
    )
    print(f"Saved predictions ({score_type}) -> {pred_path}")
    log_lines.append(f"Saved predictions ({score_type}) -> {pred_path}")

    metrics = compute_metrics(test_labels, list(test_pred))

    hyperparams_str = (
        f"ngram={best['ngram_range']};C={best['C']};"
        f"class_weight={best['class_weight']}"
    )
    run_id = f"run_{experiment_id}_{out_name.split('_', 1)[1].rsplit('_test', 1)[0]}_001"
    registry_row = {
        "run_id": run_id,
        "experiment_id": experiment_id,
        "model": model_display_name,
        "model_version": f"sklearn-{__import__('sklearn').__version__}",
        "dataset_version": dataset_version,
        "train_count": len(train_texts),
        "validation_count": len(val_texts),
        "test_count": len(test_texts),
        "random_seed": SEED,
        "hyperparameters": hyperparams_str,
        "training_time_sec": round(training_time_sec, 4),
        "hardware": "cpu",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "git_commit": "uncommitted_no_git_history",
        "status": "completed",
    }

    return {
        "run_id": run_id,
        "best_hparams": best,
        "metrics": metrics,
        "registry_row": registry_row,
        "grid_rows": grid_rows,
        "score_type": score_type,
        "pred_path": str(pred_path),
    }


def append_registry(rows):
    df_new = pd.DataFrame(rows, columns=REGISTRY_COLUMNS)
    if REGISTRY_PATH.exists():
        df_existing = pd.read_csv(REGISTRY_PATH)
        df_out = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_out = df_new
    df_out.to_csv(REGISTRY_PATH, index=False)


def main():
    train_cfg = load_training_config()
    log_lines = []

    datasets = [
        ("E1", "arabic", "frozen_v1", load_arabic_tourism()),
        ("E2", "english", "frozen_v1", load_english_matched()),
    ]
    model_specs = [
        ("logreg", "tfidf_logreg", "logreg"),
        ("svm", "tfidf_svm", "svm"),
    ]

    all_results = {}
    registry_rows = []

    for experiment_id, language, dataset_version, df in datasets:
        for model_family, model_display_name, short_name in model_specs:
            out_name = f"{experiment_id}_{model_display_name}_test"
            result = run_one(
                experiment_id, language, dataset_version, df,
                model_family, model_display_name, out_name, train_cfg, log_lines,
            )
            all_results[f"{out_name}.csv"] = result["metrics"]
            registry_rows.append(result["registry_row"])

            final_line = (
                f"[{experiment_id}/{model_family}] TEST RESULTS -- "
                f"macro_f1={result['metrics']['macro_f1']:.6f} "
                f"accuracy={result['metrics']['accuracy']:.6f} "
                f"weighted_f1={result['metrics']['weighted_f1']:.6f} "
                f"(score_type={result['score_type']})"
            )
            print(final_line)
            log_lines.append(final_line)

    # Write grid-search / results log
    GRIDSEARCH_LOG_PATH.write_text("\n".join(log_lines), encoding="utf-8")
    print(f"\nGrid-search log written to {GRIDSEARCH_LOG_PATH}")

    # Write final metrics JSON
    metrics_path = RESULTS_TABLES / "baseline_results_raw.json"
    metrics_path.write_text(json.dumps(all_results, indent=2), encoding="utf-8")
    print(f"Final test metrics written to {metrics_path}")

    # Append registry rows
    append_registry(registry_rows)
    print(f"Registry rows appended to {REGISTRY_PATH}")


if __name__ == "__main__":
    main()
