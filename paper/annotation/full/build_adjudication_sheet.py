"""
Builds the adjudication package for every sentiment row that did NOT get 3/3
unanimous agreement (161 majority + 18 three-way-disagreement = 179 rows).

Reads only from the LOCKED completed_raw/ files (never modifies them).
Writes to adjudication/master_adjudication_sheet.csv.

adjudicated_sentiment and adjudication_reason are left BLANK -- this script
never fills them in, and majority vote is never silently treated as the
final gold label (majority_label is recorded as a separate, clearly-named
column so the distinction between "what most annotators said" and "what the
adjudicator finally decided" stays auditable, per the project's explicit
requirement).

Run: python paper/annotation/full/build_adjudication_sheet.py
"""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
RAW = HERE / "completed_raw"
OUT = HERE / "adjudication"
ANNOTATORS = ["annotator_1", "annotator_2", "annotator_3"]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    master = pd.read_csv(HERE / "human_validation_757_master.csv")
    merged = master[["review_id", "language", "text"]].copy()

    for name in ANNOTATORS:
        df = pd.read_csv(RAW / f"{name}_completed.csv")
        sub = df[["review_id", "sentiment_label", "confidence", "mixed_sentiment_flag"]].copy()
        sub = sub.rename(columns={
            "sentiment_label": f"{name}_sentiment",
            "confidence": f"{name}_confidence",
            "mixed_sentiment_flag": f"{name}_mixed",
        })
        merged = merged.merge(sub, on="review_id", how="left")

    sent_cols = [f"{a}_sentiment" for a in ANNOTATORS]

    def agreement_type(row):
        vals = [row[c] for c in sent_cols]
        n_unique = len(set(vals))
        return "unanimous" if n_unique == 1 else ("majority" if n_unique == 2 else "disagreement")

    def majority_label(row):
        vals = [row[c] for c in sent_cols]
        counts = pd.Series(vals).value_counts()
        if counts.iloc[0] >= 2:
            return counts.index[0]
        return ""  # true 3-way split -- no majority exists

    merged["agreement_type"] = merged.apply(agreement_type, axis=1)
    merged["majority_label"] = merged.apply(majority_label, axis=1)

    needs_adjudication = merged[merged["agreement_type"] != "unanimous"].copy()
    needs_adjudication["adjudicated_sentiment"] = ""   # BLANK -- human fills this in, never this script
    needs_adjudication["adjudication_reason"] = ""     # BLANK

    col_order = [
        "review_id", "language", "text",
        "annotator_1_sentiment", "annotator_1_confidence", "annotator_1_mixed",
        "annotator_2_sentiment", "annotator_2_confidence", "annotator_2_mixed",
        "annotator_3_sentiment", "annotator_3_confidence", "annotator_3_mixed",
        "agreement_type", "majority_label", "adjudicated_sentiment", "adjudication_reason",
    ]
    needs_adjudication = needs_adjudication[col_order]
    needs_adjudication.to_csv(OUT / "master_adjudication_sheet.csv", index=False, encoding="utf-8-sig")

    # Also save the full 757-row classification (all rows, including unanimous ones)
    # as a permanent audit record -- nothing here is ever overwritten by a "gold" merge.
    merged_full = merged.copy()
    merged_full["adjudicated_sentiment"] = ""
    merged_full["adjudication_reason"] = ""
    full_cols = ["review_id", "language", "text"] + [f"{a}_sentiment" for a in ANNOTATORS] + \
                [f"{a}_confidence" for a in ANNOTATORS] + [f"{a}_mixed" for a in ANNOTATORS] + \
                ["agreement_type", "majority_label", "adjudicated_sentiment", "adjudication_reason"]
    merged_full[full_cols].to_csv(OUT / "classification_all_757.csv", index=False, encoding="utf-8-sig")

    counts = merged["agreement_type"].value_counts()
    majority_n = int(counts.get("majority", 0))
    disagreement_n = int(counts.get("disagreement", 0))
    print("Agreement type counts (all 757 rows):")
    print(counts.to_string())
    print(f"\nRows needing adjudication: {len(needs_adjudication)} "
          f"({majority_n} majority [2/3] + {disagreement_n} three-way disagreement)")
    print(f"Wrote {OUT / 'master_adjudication_sheet.csv'}")
    print(f"Wrote {OUT / 'classification_all_757.csv'} (full 757-row permanent audit record)")
    print("\nadjudicated_sentiment and adjudication_reason are blank in both files -- "
          "a human adjudicator fills master_adjudication_sheet.csv only, by reading review text directly.")


if __name__ == "__main__":
    main()
