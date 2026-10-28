"""
RUN THIS ONLY AFTER adjudication/merge_adjudication_results.py has produced
adjudication/adjudication_merged.csv (i.e. all 179 non-unanimous cases have
been blindly adjudicated and merged).

NOT executed as part of package preparation -- adjudication has not happened
yet. This script refuses to run (exits with an error) if adjudication_merged.csv
is missing, incomplete, or malformed.

Constructs human_gold_757.csv:
  - For the 578 unanimous (3/3) cases: human_gold_sentiment = the unanimous label.
  - For the 179 non-unanimous cases: human_gold_sentiment = adjudicated_sentiment
    (from the blind adjudication round), NEVER majority_label.

Every row also carries a `human_gold_source` column (`unanimous_3of3` or
`independent_adjudication`) and the original `agreement_type` so the two
construction paths remain distinguishable forever -- this file is never
presented as if every label came from the same process.

Does NOT compare against original/rating-derived labels, model predictions,
or any Phase 3A/3B result. Does NOT evaluate any model. That is explicitly a
separate, later, not-yet-approved step.
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent  # .../full/
VALID_SENTIMENT = {"Positive", "Neutral", "Negative"}


def main():
    merged_path = ROOT / "adjudication" / "adjudication_merged.csv"
    if not merged_path.exists():
        sys.exit(f"Missing {merged_path} -- run merge_adjudication_results.py first, "
                  f"after the adjudicator has completed all 179 cases.")

    adjudicated = pd.read_csv(merged_path)
    if len(adjudicated) != 179:
        sys.exit(f"Expected 179 adjudicated rows, found {len(adjudicated)} -- aborting.")
    bad = ~adjudicated.adjudicated_sentiment.isin(VALID_SENTIMENT)
    if bad.sum():
        sys.exit(f"{bad.sum()} invalid adjudicated_sentiment values found -- aborting.")

    full = pd.read_csv(ROOT / "adjudication" / "classification_all_757.csv")
    assert len(full) == 757

    unanimous = full[full.agreement_type == "unanimous"].copy()
    assert len(unanimous) == 578, f"Expected 578 unanimous rows, found {len(unanimous)}."
    # sanity: for a unanimous row all three annotator columns must agree
    a1, a2, a3 = unanimous["annotator_1_sentiment"], unanimous["annotator_2_sentiment"], unanimous["annotator_3_sentiment"]
    assert ((a1 == a2) & (a2 == a3)).all(), "Found a 'unanimous' row where the three labels do not actually match -- aborting."
    unanimous["human_gold_sentiment"] = unanimous["annotator_1_sentiment"]
    unanimous["human_gold_source"] = "unanimous_3of3"
    # agreement_type already present on `full` / `unanimous` as "unanimous"

    non_unanimous = full[full.agreement_type != "unanimous"][["review_id", "language", "text", "agreement_type", "majority_label"]].copy()
    assert set(non_unanimous.review_id) == set(adjudicated.review_id), \
        "Non-unanimous review_id set does not match the adjudicated set -- aborting."
    non_unanimous = non_unanimous.merge(
        adjudicated[["review_id", "adjudicated_sentiment", "adjudication_confidence", "adjudication_reason"]],
        on="review_id", how="left")
    non_unanimous["human_gold_sentiment"] = non_unanimous["adjudicated_sentiment"]
    non_unanimous["human_gold_source"] = "independent_adjudication"
    # agreement_type preserved from the frozen master ("majority" or "disagreement")

    gold_cols = ["review_id", "language", "text", "human_gold_sentiment", "human_gold_source", "agreement_type"]
    combined = pd.concat([unanimous[gold_cols], non_unanimous[gold_cols]], ignore_index=True)

    assert len(combined) == 757
    assert combined.review_id.nunique() == 757
    assert combined.human_gold_sentiment.isna().sum() == 0

    out_path = ROOT / "human_gold_757.csv"
    combined.to_csv(out_path, index=False, encoding="utf-8-sig")

    print(f"Wrote {out_path}: {len(combined)} rows")
    print(combined["human_gold_source"].value_counts().to_string())
    print(combined["human_gold_sentiment"].value_counts().to_string())
    print("\nThis file is the human-gold label set for the 757-review matched-protocol slice. "
          "It has NOT been compared to original/rating-derived labels or any model prediction -- "
          "that is a separate, later step, not performed by this script.")


if __name__ == "__main__":
    main()
