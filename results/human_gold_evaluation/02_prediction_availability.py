"""
Section D (availability half) of the Human-Gold label analysis phase.

Builds an explicit, verified inventory of every candidate row-level
prediction file BEFORE any metric is computed. No retraining; read-only
with respect to results/predictions/ and results/phase3b_kaggle_gpu/.

For each candidate file, verifies:
  - file exists
  - row count / unique id count
  - exact match to the required frozen test id set for that language
  - zero duplicate ids, zero missing ids, zero unexpected ids
  - label mapping sanity: where a *_label_id column exists alongside a
    *_sentiment string column, the id<->string mapping is internally
    consistent for every row
"""
import json
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SPLITS = REPO_ROOT / "data" / "splits" / "frozen_v1"
PRED_3A = REPO_ROOT / "results" / "predictions"
PRED_3B = REPO_ROOT / "results" / "phase3b_kaggle_gpu"

LABEL_SET = {"Negative", "Neutral", "Positive"}


def load_ids(fname):
    data = json.load(open(SPLITS / fname, encoding="utf-8"))
    return set(data["review_ids"])


AR_TEST = load_ids("arabic_tourism_test_ids.json")
EN_TEST = load_ids("english_matched_test_ids.json")

# (model_key, phase, language, realization, path, pred_col, true_col_for_sanity)
CANDIDATES = [
    ("E1_xlmr_lora", "3A_laptop_LoRA", "arabic", "lora_primary", PRED_3A / "E1_xlmr_test.csv", "predicted_label", "true_label"),
    ("E1_marbert_lora", "3A_laptop_LoRA", "arabic", "lora_primary", PRED_3A / "E1_marbert_test.csv", "predicted_label", "true_label"),
    ("E1_tfidf_logreg", "3A_laptop_LoRA", "arabic", "baseline_primary", PRED_3A / "E1_tfidf_logreg_test.csv", "predicted_label", "true_label"),
    ("E1_tfidf_svm", "3A_laptop_LoRA", "arabic", "baseline_primary", PRED_3A / "E1_tfidf_svm_test.csv", "predicted_label", "true_label"),
    ("E5_enTrain_arTest_lora", "3A_laptop_LoRA", "arabic", "zeroshot_primary", PRED_3A / "E5_enTrain_arTest_test.csv", "predicted_label", "true_label"),
    ("E2_xlmr_lora", "3A_laptop_LoRA", "english", "lora_primary", PRED_3A / "E2_xlmr_test.csv", "predicted_label", "true_label"),
    ("E2_tfidf_logreg", "3A_laptop_LoRA", "english", "baseline_primary", PRED_3A / "E2_tfidf_logreg_test.csv", "predicted_label", "true_label"),
    ("E2_tfidf_svm", "3A_laptop_LoRA", "english", "baseline_primary", PRED_3A / "E2_tfidf_svm_test.csv", "predicted_label", "true_label"),
    ("E5_arTrain_enTest_lora", "3A_laptop_LoRA", "english", "zeroshot_primary", PRED_3A / "E5_arTrain_enTest_test.csv", "predicted_label", "true_label"),
    ("E1_xlmr_fullft", "3B_GPU_fullFT", "arabic", "RERUN_REALIZATION_not_primary", PRED_3B / "E1_xlmr_arabic_reproducibility_test_predictions.csv", "pred_sentiment", "true_sentiment"),
    ("E1_marbert_fullft", "3B_GPU_fullFT", "arabic", "RERUN_REALIZATION_not_primary", PRED_3B / "E1_marbert_arabic_reproducibility_test_predictions.csv", "pred_sentiment", "true_sentiment"),
    ("E4_multilingual_xlmr_arabic", "3B_GPU_fullFT", "arabic", "primary", PRED_3B / "E4_multilingual_xlmr_arabic_test_predictions.csv", "pred_sentiment", "true_sentiment"),
    ("E5B_zeroshot_en_to_ar", "3B_GPU_fullFT", "arabic", "primary", PRED_3B / "E5B_english_to_arabic_test_predictions.csv", "pred_sentiment", "true_sentiment"),
    ("E2_xlmr_fullft", "3B_GPU_fullFT", "english", "primary", PRED_3B / "E2_xlmr_fullft_gpu_3ep_test_predictions.csv", "pred_sentiment", "true_sentiment"),
    ("E4_multilingual_xlmr_english", "3B_GPU_fullFT", "english", "primary", PRED_3B / "E4_multilingual_xlmr_english_test_predictions.csv", "pred_sentiment", "true_sentiment"),
    ("E5A_zeroshot_ar_to_en", "3B_GPU_fullFT", "english", "primary", PRED_3B / "E5A_arabic_to_english_test_predictions.csv", "pred_sentiment", "true_sentiment"),
    # Known gaps -- documented, not silently skipped:
    ("E1_xlmr_fullft_PRIMARY", "3B_GPU_fullFT", "arabic", "primary", None, None, None),
    ("E1_marbert_fullft_PRIMARY", "3B_GPU_fullFT", "arabic", "primary", None, None, None),
]


def label_mapping_sanity(df, pred_col, true_col):
    """Where an *_id column is present alongside the string column, confirm the mapping is internally consistent."""
    id_col_candidates = [c for c in df.columns if c.endswith("_label_id")]
    if not id_col_candidates:
        return "n/a (no id column)"
    issues = []
    for id_col, str_col in [("true_label_id", true_col), ("pred_label_id", pred_col)]:
        if id_col not in df.columns or str_col not in df.columns:
            continue
        mapping = df[[id_col, str_col]].drop_duplicates()
        grouped = mapping.groupby(id_col)[str_col].nunique()
        if (grouped > 1).any():
            issues.append(f"{id_col} maps to >1 string value")
    return "consistent" if not issues else "; ".join(issues)


def main():
    rows = []
    for key, phase, lang, realization, path, pred_col, true_col in CANDIDATES:
        test_ids = AR_TEST if lang == "arabic" else EN_TEST
        if path is None:
            rows.append({
                "model_key": key, "phase": phase, "language": lang, "realization": realization,
                "file_path": None, "status": "MISSING -- original primary row-level predictions lost (documented, D17/known_limitations.md)",
                "n_rows": None, "n_unique_ids": None, "ids_match_frozen_test": None,
                "n_duplicate_ids": None, "n_missing_ids": None, "n_unexpected_ids": None,
                "label_values_valid": None, "label_mapping_sanity": None,
            })
            continue
        if not path.exists():
            rows.append({
                "model_key": key, "phase": phase, "language": lang, "realization": realization,
                "file_path": str(path), "status": "MISSING -- file not found",
                "n_rows": None, "n_unique_ids": None, "ids_match_frozen_test": None,
                "n_duplicate_ids": None, "n_missing_ids": None, "n_unexpected_ids": None,
                "label_values_valid": None, "label_mapping_sanity": None,
            })
            continue

        df = pd.read_csv(path)
        ids = set(df.review_id)
        n_dup = len(df) - df.review_id.nunique()
        n_missing = len(test_ids - ids)
        n_unexpected = len(ids - test_ids)
        ids_match = (ids == test_ids)
        bad_pred = (~df[pred_col].isin(LABEL_SET)).sum() if pred_col in df.columns else "col_missing"
        bad_true = (~df[true_col].isin(LABEL_SET)).sum() if true_col in df.columns else "col_missing"
        label_values_valid = (bad_pred == 0 and bad_true == 0)
        mapping_sanity = label_mapping_sanity(df, pred_col, true_col)

        status = "VALID" if (ids_match and n_dup == 0 and label_values_valid and mapping_sanity in ("n/a (no id column)", "consistent")) else "INVALID -- see detail columns"

        rows.append({
            "model_key": key, "phase": phase, "language": lang, "realization": realization,
            "file_path": str(path.relative_to(REPO_ROOT)), "status": status,
            "n_rows": len(df), "n_unique_ids": df.review_id.nunique(), "ids_match_frozen_test": ids_match,
            "n_duplicate_ids": n_dup, "n_missing_ids": n_missing, "n_unexpected_ids": n_unexpected,
            "label_values_valid": label_values_valid, "label_mapping_sanity": mapping_sanity,
        })

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUT / "prediction_availability.csv", index=False)
    print(out_df.to_string(index=False))

    valid = out_df[out_df.status == "VALID"]
    invalid_or_missing = out_df[out_df.status != "VALID"]
    print(f"\n{len(valid)}/{len(out_df)} candidate prediction sources are VALID for Human-Gold evaluation.")
    print(f"Excluded/missing: {list(invalid_or_missing.model_key)}")

    with open(OUT / "prediction_availability_summary.json", "w", encoding="utf-8") as f:
        json.dump({
            "valid_model_keys": valid.model_key.tolist(),
            "excluded_or_missing_model_keys": invalid_or_missing.model_key.tolist(),
        }, f, indent=2)


if __name__ == "__main__":
    main()
