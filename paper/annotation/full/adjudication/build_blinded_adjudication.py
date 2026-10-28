"""
Builds the FULLY BLINDED adjudication package from the existing research-side
master_adjudication_sheet.csv (179 non-unanimous rows). Strips every hidden
field -- no A1/A2/A3 labels, no majority_label, no agreement_type, no rating,
no original label, no model anything -- leaving only review_id, language, text,
plus blank fields for the adjudicator to fill: adjudicated_sentiment,
adjudication_confidence, adjudication_reason. Note: NO mixed_sentiment_flag
field is included here -- mixed sentiment stays exploratory (kappa=0.269) and
is not re-collected during adjudication.

Presentation order uses its OWN seed (9009), distinct from the three original
annotators' seeds (1001/2002/3003), so adjudication order has no relationship
to any prior annotation order.

Run: python paper/annotation/full/adjudication/build_blinded_adjudication.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent  # .../adjudication/
ADJUDICATION_SEED = 9009


def main():
    hidden = pd.read_csv(HERE / "master_adjudication_sheet.csv")
    assert len(hidden) == 179
    assert hidden.review_id.nunique() == 179
    assert set(hidden.agreement_type.unique()) <= {"majority", "disagreement"}

    blinded_cols = hidden[["review_id", "language", "text"]].copy()

    rng = np.random.default_rng(ADJUDICATION_SEED)
    order = rng.permutation(len(blinded_cols))
    blinded = blinded_cols.iloc[order].reset_index(drop=True)

    blinded["adjudicated_sentiment"] = ""      # Positive / Neutral / Negative -- TO BE FILLED
    blinded["adjudication_confidence"] = ""    # high / medium / low
    blinded["adjudication_reason"] = ""        # free text, optional/short

    # ---- Verification before writing ----
    assert len(blinded) == 179
    assert blinded.review_id.nunique() == 179
    assert set(blinded.review_id) == set(hidden.review_id)
    forbidden_cols = {"annotator_1_sentiment", "annotator_2_sentiment", "annotator_3_sentiment",
                       "annotator_1_confidence", "annotator_2_confidence", "annotator_3_confidence",
                       "annotator_1_mixed", "annotator_2_mixed", "annotator_3_mixed",
                       "agreement_type", "majority_label", "rating", "original_label", "label_source"}
    leaked = forbidden_cols & set(blinded.columns)
    assert len(leaked) == 0, f"Hidden fields leaked into blinded sheet: {leaked}"
    blank_cells = sum(blinded[c].apply(lambda x: isinstance(x, str) and x.strip() != "").sum()
                       for c in ["adjudicated_sentiment", "adjudication_confidence", "adjudication_reason"])
    assert blank_cells == 0, "Adjudication fields must start blank."

    blinded.to_csv(HERE / "adjudication_blinded.csv", index=False, encoding="utf-8-sig")

    print(f"Wrote {HERE / 'adjudication_blinded.csv'}: {len(blinded)} rows")
    print(f"Columns (must be exactly review_id, language, text, adjudicated_sentiment, "
          f"adjudication_confidence, adjudication_reason): {list(blinded.columns)}")
    print("Verification: no hidden fields present, zero pre-filled values, "
          "review_id set matches the 179 non-unanimous cases exactly.")


if __name__ == "__main__":
    main()
