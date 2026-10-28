"""
RUN THIS ONLY AFTER the adjudicator has exported a COMPLETE adjudication CSV
from adjudicator_interface.html (all 179 cases, both adjudicated_sentiment
and adjudication_confidence filled).

NOT executed as part of package preparation -- no adjudication exists yet.

Merges the adjudicator's blind output back with the hidden research-side
master_adjudication_sheet.csv by review_id. Preserves every source distinctly:
  - annotator_1_sentiment / annotator_2_sentiment / annotator_3_sentiment (original, locked)
  - majority_label (vote outcome, not adjudication)
  - adjudicated_sentiment, adjudication_confidence, adjudication_reason (the new blind decision)
  - agreement_type (majority / disagreement, preserved from before adjudication)

Never overwrites any of these columns into one another. Writes
adjudication_merged.csv -- the permanent, fully-auditable record for the
179 previously non-unanimous cases.

Usage: place the adjudicator's exported file at this directory as
`adjudication_completed.csv` (same schema as adjudication_blinded.csv, with
the three blank columns now filled), then run:
    python paper/annotation/full/adjudication/merge_adjudication_results.py
"""
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
VALID_SENTIMENT = {"Positive", "Neutral", "Negative"}
VALID_CONFIDENCE = {"high", "medium", "low"}


def main():
    completed_path = HERE / "adjudication_completed.csv"
    if not completed_path.exists():
        sys.exit(f"Missing {completed_path} -- run this only after the adjudicator exports a completed file "
                  f"(rename/save their export to this exact filename first).")

    completed = pd.read_csv(completed_path)
    if len(completed) != 179:
        sys.exit(f"Expected 179 rows, found {len(completed)} -- adjudication file looks wrong, aborting.")

    filled_sent = completed["adjudicated_sentiment"].apply(lambda x: isinstance(x, str) and x.strip() != "").sum()
    filled_conf = completed["adjudication_confidence"].apply(lambda x: isinstance(x, str) and x.strip() != "").sum()
    if filled_sent < 179 or filled_conf < 179:
        sys.exit(f"Adjudication is not fully complete ({filled_sent}/179 sentiment, {filled_conf}/179 confidence "
                  f"filled) -- refusing to merge an incomplete round.")

    bad_sent = ~completed.adjudicated_sentiment.isin(VALID_SENTIMENT)
    bad_conf = ~completed.adjudication_confidence.isin(VALID_CONFIDENCE)
    if bad_sent.sum() or bad_conf.sum():
        sys.exit(f"Invalid values found (bad sentiment: {bad_sent.sum()}, bad confidence: {bad_conf.sum()}) "
                  f"-- aborting rather than merging malformed data.")

    hidden = pd.read_csv(HERE / "master_adjudication_sheet.csv")
    assert len(hidden) == 179
    assert set(hidden.review_id) == set(completed.review_id), \
        "Adjudicated review_id set does not match the 179 non-unanimous cases -- aborting."

    # Drop the hidden sheet's own blank adjudicated_sentiment/adjudication_reason
    # placeholders before merging in the real ones, to avoid duplicate-column suffixing.
    hidden_base = hidden.drop(columns=["adjudicated_sentiment", "adjudication_reason"])
    merged = hidden_base.merge(
        completed[["review_id", "adjudicated_sentiment", "adjudication_confidence", "adjudication_reason"]],
        on="review_id", how="left")

    assert merged["adjudicated_sentiment"].isna().sum() == 0, "Merge produced missing adjudicated_sentiment -- aborting."

    col_order = [
        "review_id", "language", "text",
        "annotator_1_sentiment", "annotator_1_confidence", "annotator_1_mixed",
        "annotator_2_sentiment", "annotator_2_confidence", "annotator_2_mixed",
        "annotator_3_sentiment", "annotator_3_confidence", "annotator_3_mixed",
        "agreement_type", "majority_label",
        "adjudicated_sentiment", "adjudication_confidence", "adjudication_reason",
    ]
    merged = merged[col_order]
    merged.to_csv(HERE / "adjudication_merged.csv", index=False, encoding="utf-8-sig")

    print(f"Wrote {HERE / 'adjudication_merged.csv'} ({len(merged)} rows)")
    print("All three original annotator columns, majority_label, agreement_type, and the new "
          "adjudicated_sentiment/confidence/reason are preserved as distinct columns -- nothing overwritten.")

    # Quick diagnostic (not a claim, just visible agreement with majority for transparency)
    agree_with_majority = (merged["adjudicated_sentiment"] == merged["majority_label"]).sum()
    print(f"\nDiagnostic only: adjudicated_sentiment matches majority_label in {agree_with_majority}/179 rows "
          f"({agree_with_majority/179*100:.1f}%). This is NOT a validity claim -- majority agreement is expected "
          f"to be common and is not evidence the adjudicator was 'right' or 'wrong'.")


if __name__ == "__main__":
    main()
