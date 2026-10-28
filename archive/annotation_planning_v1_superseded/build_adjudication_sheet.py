"""
RUN THIS ONLY AFTER BOTH annotator_1_blinded.csv AND annotator_2_blinded.csv
HAVE BEEN FILLED IN BY REAL HUMAN ANNOTATORS.

Not executed as part of the RQ3 audit (2026-10-26) -- no human labels exist yet.
This script is prepared so annotation can proceed immediately once annotators
are available, without re-deriving the merge/agreement logic from scratch.

What it does:
  1. Merges the two annotators' sentiment_label columns back onto review_id.
  2. Computes Cohen's kappa (unweighted) over the 757 main_stratified rows
     (the 9 codeswitch_diagnostic rows are reported separately, consistent
     with their qualitative-only status elsewhere in this project).
  3. Writes disagreement_for_adjudication.csv -- every row where the two
     annotators' sentiment_label differs, for a third-pass adjudicator to
     resolve (same pattern as docs/codeswitch_audit.md's reviewer A/B/
     arbitration process).
  4. Writes agreement_report.md with the kappa value(s) and basic diagnostics.

Does NOT invent an adjudicated_label -- that column is left blank for a
human adjudicator to fill, exactly like the two annotator columns before them.
"""
import sys
from pathlib import Path

import pandas as pd
from sklearn.metrics import cohen_kappa_score

HERE = Path(__file__).resolve().parent


def main():
    a1_path = HERE / "annotator_1_blinded.csv"
    a2_path = HERE / "annotator_2_blinded.csv"
    for p in (a1_path, a2_path):
        if not p.exists():
            sys.exit(f"Missing {p} -- nothing to adjudicate yet.")

    a1 = pd.read_csv(a1_path)
    a2 = pd.read_csv(a2_path)

    if a1["sentiment_label"].apply(lambda x: isinstance(x, str) and x.strip() != "").sum() == 0:
        sys.exit("annotator_1_blinded.csv has no filled labels yet -- annotation not started.")
    if a2["sentiment_label"].apply(lambda x: isinstance(x, str) and x.strip() != "").sum() == 0:
        sys.exit("annotator_2_blinded.csv has no filled labels yet -- annotation not started.")

    merged = a1.merge(a2, on=["review_id", "language", "text"], suffixes=("_ann1", "_ann2"))
    assert len(merged) == len(a1) == len(a2), "Row count mismatch between the two annotator sheets."

    master = pd.read_csv(HERE / "master_reference_DO_NOT_SHOW_ANNOTATORS.csv")
    merged = merged.merge(master[["review_id", "slice_type", "original_label", "original_label_source", "rating"]],
                           on="review_id", how="left")

    main_rows = merged[merged["slice_type"] == "main_stratified"].copy()
    cs_rows = merged[merged["slice_type"] == "codeswitch_diagnostic"].copy()

    kappa_main = cohen_kappa_score(main_rows["sentiment_label_ann1"], main_rows["sentiment_label_ann2"])
    kappa_main_ar = cohen_kappa_score(
        main_rows.loc[main_rows.language == "arabic", "sentiment_label_ann1"],
        main_rows.loc[main_rows.language == "arabic", "sentiment_label_ann2"])
    kappa_main_en = cohen_kappa_score(
        main_rows.loc[main_rows.language == "english", "sentiment_label_ann1"],
        main_rows.loc[main_rows.language == "english", "sentiment_label_ann2"])

    disagreements = main_rows[main_rows["sentiment_label_ann1"] != main_rows["sentiment_label_ann2"]].copy()
    disagreements["adjudicated_label"] = ""  # blank -- a human fills this, never this script
    disagreements["adjudicator_notes"] = ""
    disagreements[[
        "review_id", "language", "text", "sentiment_label_ann1", "sentiment_label_ann2",
        "confidence_ann1", "confidence_ann2", "mixed_sentiment_flag_ann1", "mixed_sentiment_flag_ann2",
        "adjudicated_label", "adjudicator_notes",
    ]].to_csv(HERE / "disagreement_for_adjudication.csv", index=False, encoding="utf-8-sig")

    cs_disagreements = cs_rows[cs_rows["sentiment_label_ann1"] != cs_rows["sentiment_label_ann2"]]

    with open(HERE / "agreement_report.md", "w", encoding="utf-8") as f:
        f.write("# Inter-Annotator Agreement Report\n\n")
        f.write(f"Main stratified slice (n={len(main_rows)}): Cohen's kappa = {kappa_main:.3f}\n")
        f.write(f"  - Arabic subset (n={(main_rows.language=='arabic').sum()}): kappa = {kappa_main_ar:.3f}\n")
        f.write(f"  - English subset (n={(main_rows.language=='english').sum()}): kappa = {kappa_main_en:.3f}\n")
        f.write(f"Disagreements requiring adjudication: {len(disagreements)} "
                f"({len(disagreements)/len(main_rows)*100:.1f}% of main slice)\n\n")
        f.write(f"Code-switch diagnostic (n={len(cs_rows)}, reported separately, qualitative only): "
                f"{len(cs_disagreements)} disagreements\n")

    print(f"Wrote disagreement_for_adjudication.csv ({len(disagreements)} rows needing a human adjudicator)")
    print(f"Wrote agreement_report.md (kappa_main={kappa_main:.3f})")


if __name__ == "__main__":
    main()
