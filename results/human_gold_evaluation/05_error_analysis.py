"""
Section G of the Human-Gold label analysis phase.

For every valid model, breaks down errors against Human-Gold by:
  - true Human-Gold class x predicted class (confusion detail)
  - language
  - Neutral-specific errors (both directions: true Neutral mispredicted,
    and other classes mispredicted as Neutral)

Qualitative examples use a DETERMINISTIC selection rule (stated explicitly,
applied identically to every model/cell, no cherry-picking): for each
(true_class, predicted_class) error cell, sort the erroring review_ids
lexicographically ascending and take the first 3.
No annotator identity is exposed (comparison_dataset_757.csv carries no
per-annotator columns at all).
"""
import json
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STORE = OUT / "model_predictions_vs_human_gold"
ANNOT = REPO_ROOT / "paper" / "annotation" / "full"

AVAIL = pd.read_csv(OUT / "prediction_availability.csv")
VALID = AVAIL[AVAIL.status == "VALID"].copy()

N_EXAMPLES_PER_CELL = 3


def main():
    gold_text = pd.read_csv(ANNOT / "human_gold_757.csv")[["review_id", "language", "text"]]

    summary_rows = []
    qualitative_rows = []

    for _, row in VALID.iterrows():
        key = row.model_key
        df = pd.read_csv(STORE / f"{key}.csv").merge(gold_text, on="review_id", how="left")
        df["error"] = df["pred"] != df["human_gold_sentiment"]
        errors = df[df.error]

        # true x pred breakdown
        breakdown = errors.groupby(["human_gold_sentiment", "pred"]).size().reset_index(name="count")
        for _, b in breakdown.iterrows():
            summary_rows.append({
                "model_key": key, "language": row.language, "phase": row.phase,
                "true_human_gold_class": b["human_gold_sentiment"], "predicted_class": b["pred"],
                "error_count": int(b["count"]),
            })

        neutral_true_errors = errors[errors.human_gold_sentiment == "Neutral"]
        neutral_pred_errors = errors[errors.pred == "Neutral"]
        summary_rows.append({
            "model_key": key, "language": row.language, "phase": row.phase,
            "true_human_gold_class": "Neutral", "predicted_class": "ANY_OTHER (neutral-true summary)",
            "error_count": len(neutral_true_errors),
        })
        summary_rows.append({
            "model_key": key, "language": row.language, "phase": row.phase,
            "true_human_gold_class": "ANY_OTHER (neutral-pred summary)", "predicted_class": "Neutral",
            "error_count": len(neutral_pred_errors),
        })

        # deterministic qualitative example selection
        for (true_cls, pred_cls), cell in errors.groupby(["human_gold_sentiment", "pred"]):
            chosen = cell.sort_values("review_id").head(N_EXAMPLES_PER_CELL)
            for _, ex in chosen.iterrows():
                qualitative_rows.append({
                    "model_key": key, "language": row.language,
                    "true_human_gold_class": true_cls, "predicted_class": pred_cls,
                    "review_id": ex["review_id"], "text": ex["text"],
                })

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(OUT / "error_analysis_by_class_language.csv", index=False)

    qual_df = pd.DataFrame(qualitative_rows)
    qual_df.to_csv(OUT / "qualitative_error_examples.csv", index=False, encoding="utf-8-sig")

    print(f"Wrote error_analysis_by_class_language.csv ({len(summary_df)} rows) "
          f"and qualitative_error_examples.csv ({len(qual_df)} rows, deterministic "
          f"selection: first {N_EXAMPLES_PER_CELL} review_ids per (true,pred) error cell, sorted ascending).")

    # Quick Neutral-focused print
    neutral_summary = summary_df[summary_df.true_human_gold_class.isin(["Neutral", "ANY_OTHER (neutral-true summary)"]) |
                                  summary_df.predicted_class.isin(["Neutral", "ANY_OTHER (neutral-pred summary)"])]
    print("\n--- Neutral-related error counts (true Neutral missed, or other predicted as Neutral) ---")
    print(neutral_summary.to_string(index=False))


if __name__ == "__main__":
    main()
