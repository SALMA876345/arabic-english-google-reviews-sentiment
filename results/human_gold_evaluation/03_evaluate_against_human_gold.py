"""
Section D (metrics half) + Section E of the Human-Gold label analysis phase.

For every VALID prediction source from 02_prediction_availability.py:
  - loads the saved row-level predictions (NO retraining)
  - merges by review_id against human_gold_757.csv
  - recomputes original-label metrics directly from the file's own true
    label column (a reproducibility check against the previously reported
    Phase 3A/3B numbers, not a new evaluation protocol)
  - computes Human-Gold metrics using the SAME saved predicted labels
    against human_gold_sentiment instead
  - keeps "original-label evaluation" and "Human-Gold evaluation" as
    distinct rows, and keeps "primary" vs "RERUN_REALIZATION" distinct,
    never collapsing or substituting one for the other
"""
import json
from pathlib import Path

import pandas as pd
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))
from evaluation.metrics import compute_metrics, LABEL_ORDER  # noqa: E402

OUT = Path(__file__).resolve().parent
ANNOT = REPO_ROOT / "paper" / "annotation" / "full"

AVAIL = pd.read_csv(OUT / "prediction_availability.csv")
VALID = AVAIL[AVAIL.status == "VALID"].copy()

COL_MAP = {
    # model_key -> (pred_col, true_col)
    "E1_xlmr_lora": ("predicted_label", "true_label"),
    "E1_marbert_lora": ("predicted_label", "true_label"),
    "E1_tfidf_logreg": ("predicted_label", "true_label"),
    "E1_tfidf_svm": ("predicted_label", "true_label"),
    "E5_enTrain_arTest_lora": ("predicted_label", "true_label"),
    "E2_xlmr_lora": ("predicted_label", "true_label"),
    "E2_tfidf_logreg": ("predicted_label", "true_label"),
    "E2_tfidf_svm": ("predicted_label", "true_label"),
    "E5_arTrain_enTest_lora": ("predicted_label", "true_label"),
    "E1_xlmr_fullft": ("pred_sentiment", "true_sentiment"),
    "E1_marbert_fullft": ("pred_sentiment", "true_sentiment"),
    "E4_multilingual_xlmr_arabic": ("pred_sentiment", "true_sentiment"),
    "E5B_zeroshot_en_to_ar": ("pred_sentiment", "true_sentiment"),
    "E2_xlmr_fullft": ("pred_sentiment", "true_sentiment"),
    "E4_multilingual_xlmr_english": ("pred_sentiment", "true_sentiment"),
    "E5A_zeroshot_ar_to_en": ("pred_sentiment", "true_sentiment"),
}


def main():
    gold = pd.read_csv(ANNOT / "human_gold_757.csv")[["review_id", "human_gold_sentiment"]]

    metric_rows = []
    pred_store = {}  # model_key -> dataframe with review_id, pred, human_gold_sentiment (for stats phase)

    for _, row in VALID.iterrows():
        key = row.model_key
        pred_col, true_col = COL_MAP[key]
        path = REPO_ROOT / row.file_path
        df = pd.read_csv(path)

        merged = df[["review_id", pred_col, true_col]].merge(gold, on="review_id", how="left", validate="one_to_one")
        assert merged.human_gold_sentiment.isna().sum() == 0, f"{key}: merge produced missing Human-Gold labels"
        assert len(merged) == row.n_rows, f"{key}: row count changed after merge"

        orig_metrics = compute_metrics(merged[true_col], merged[pred_col])
        gold_metrics = compute_metrics(merged["human_gold_sentiment"], merged[pred_col])

        for eval_type, m in [("original_label", orig_metrics), ("human_gold", gold_metrics)]:
            metric_rows.append({
                "model_key": key, "phase": row.phase, "language": row.language, "realization": row.realization,
                "evaluation_reference": eval_type, "n": m["n"], "accuracy": m["accuracy"],
                "macro_f1": m["macro_f1"], "weighted_f1": m["weighted_f1"],
                "precision_macro": m["precision_macro"], "recall_macro": m["recall_macro"],
                **{f"{cls}_precision": m["per_class"][cls]["precision"] for cls in LABEL_ORDER},
                **{f"{cls}_recall": m["per_class"][cls]["recall"] for cls in LABEL_ORDER},
                **{f"{cls}_f1": m["per_class"][cls]["f1"] for cls in LABEL_ORDER},
                **{f"{cls}_support": m["per_class"][cls]["support"] for cls in LABEL_ORDER},
            })
            cm_df = pd.DataFrame(m["confusion_matrix"], index=[f"true_{l}" for l in LABEL_ORDER], columns=[f"pred_{l}" for l in LABEL_ORDER])
            cm_df.to_csv(OUT / f"confusion_matrix_{key}_{eval_type}.csv")

        pred_store[key] = merged[["review_id", pred_col, "human_gold_sentiment"]].rename(columns={pred_col: "pred"})

    metrics_df = pd.DataFrame(metric_rows)
    metrics_df.to_csv(OUT / "human_gold_metrics_all_models.csv", index=False)

    # Before/after comparison table: original-label eval vs Human-Gold eval, same model_key
    pivot_rows = []
    for key, grp in metrics_df.groupby("model_key"):
        orig = grp[grp.evaluation_reference == "original_label"].iloc[0]
        gold_row = grp[grp.evaluation_reference == "human_gold"].iloc[0]
        pivot_rows.append({
            "model_key": key, "phase": orig.phase, "language": orig.language, "realization": orig.realization,
            "macro_f1_original_label": orig.macro_f1, "macro_f1_human_gold": gold_row.macro_f1,
            "macro_f1_delta": gold_row.macro_f1 - orig.macro_f1,
            "accuracy_original_label": orig.accuracy, "accuracy_human_gold": gold_row.accuracy,
            "accuracy_delta": gold_row.accuracy - orig.accuracy,
            "same_prediction_realization": orig.realization != "RERUN_REALIZATION_not_primary",
        })
    comparison_df = pd.DataFrame(pivot_rows).sort_values(["language", "phase", "model_key"])
    comparison_df.to_csv(OUT / "original_vs_human_gold_comparison.csv", index=False)

    # Save merged prediction+Human-Gold frames for the statistics phase (not re-derivable without re-merging)
    store_dir = OUT / "model_predictions_vs_human_gold"
    store_dir.mkdir(exist_ok=True)
    for key, df in pred_store.items():
        df.to_csv(store_dir / f"{key}.csv", index=False)

    print(metrics_df.to_string(index=False))
    print("\n=== Original-label vs Human-Gold comparison ===")
    print(comparison_df.to_string(index=False))
    print(f"\nWrote human_gold_metrics_all_models.csv, original_vs_human_gold_comparison.csv, "
          f"per-model confusion matrices, and {len(pred_store)} merged prediction files under model_predictions_vs_human_gold/.")


if __name__ == "__main__":
    main()
