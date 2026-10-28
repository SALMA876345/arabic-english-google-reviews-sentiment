"""
Integrity gate for the completed adjudication file, run BEFORE any merge or
Human-Gold construction. Mirrors verify_completed_integrity.py's role for the
three original annotator files.

Checks:
  - exactly 179 rows, 179 unique review_ids, no duplicates
  - review_id set exactly equals the 179 non-unanimous cases (master_adjudication_sheet.csv)
  - none of the 578 unanimous review_ids appear
  - language matches the frozen master (classification_all_757.csv) per review_id
  - adjudicated_sentiment in {Positive, Neutral, Negative} (post-normalization)
  - adjudication_confidence in {high, medium, low} (case-insensitive, normalized to lowercase)
  - no missing adjudicated_sentiment / adjudication_confidence
  - no unexpected review_ids

Exits non-zero on ANY failure. Does not write any output file -- read-only gate.
"""
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
VALID_SENTIMENT = {"Positive", "Neutral", "Negative"}
VALID_CONFIDENCE = {"high", "medium", "low"}

failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)


def main():
    completed_path = HERE / "completed_raw" / "adjudicator_completed.csv"
    master_path = HERE / "master_adjudication_sheet.csv"
    full_path = HERE / "classification_all_757.csv"

    completed = pd.read_csv(completed_path)
    master = pd.read_csv(master_path)
    full = pd.read_csv(full_path)

    # -- row / uniqueness checks --
    check(len(completed) == 179, f"Expected 179 rows, found {len(completed)}")
    check(completed.review_id.nunique() == 179, f"Expected 179 unique review_ids, found {completed.review_id.nunique()}")
    check(len(completed) == completed.review_id.nunique(), "Duplicate review_ids present")

    # -- required fields present / non-missing --
    for col in ["review_id", "language", "adjudicated_sentiment", "adjudication_confidence"]:
        check(col in completed.columns, f"Missing required column: {col}")
    missing_sent = completed["adjudicated_sentiment"].isna().sum() if "adjudicated_sentiment" in completed else 179
    missing_conf = completed["adjudication_confidence"].isna().sum() if "adjudication_confidence" in completed else 179
    check(missing_sent == 0, f"{missing_sent} missing adjudicated_sentiment values")
    check(missing_conf == 0, f"{missing_conf} missing adjudication_confidence values")

    # -- ID-set checks against the 179 non-unanimous cases --
    completed_ids = set(completed.review_id)
    master_ids = set(master.review_id)
    check(completed_ids == master_ids,
          f"review_id set mismatch vs 179 non-unanimous cases: "
          f"missing={master_ids - completed_ids}, unexpected={completed_ids - master_ids}")

    unanimous_ids = set(full[full.agreement_type == "unanimous"].review_id)
    check(len(unanimous_ids) == 578, f"Expected 578 unanimous ids in frozen master, found {len(unanimous_ids)}")
    leaked_unanimous = completed_ids & unanimous_ids
    check(len(leaked_unanimous) == 0, f"{len(leaked_unanimous)} unanimous-case IDs leaked into adjudication file: {leaked_unanimous}")

    # -- language consistency vs frozen master --
    full_lang = full.set_index("review_id")["language"]
    lang_mismatches = []
    for _, row in completed.iterrows():
        rid = row["review_id"]
        if rid in full_lang.index and row["language"] != full_lang.loc[rid]:
            lang_mismatches.append(rid)
    check(len(lang_mismatches) == 0, f"Language mismatch vs frozen master for: {lang_mismatches}")

    # -- value validity (normalize confidence case only) --
    completed["adjudication_confidence_norm"] = completed["adjudication_confidence"].astype(str).str.lower()
    bad_sent = completed[~completed["adjudicated_sentiment"].isin(VALID_SENTIMENT)]
    bad_conf = completed[~completed["adjudication_confidence_norm"].isin(VALID_CONFIDENCE)]
    check(len(bad_sent) == 0, f"Invalid adjudicated_sentiment values: {bad_sent[['review_id','adjudicated_sentiment']].to_dict('records')}")
    check(len(bad_conf) == 0, f"Invalid adjudication_confidence values: {bad_conf[['review_id','adjudication_confidence']].to_dict('records')}")

    print(f"Rows: {len(completed)} | Unique IDs: {completed.review_id.nunique()}")
    print(f"ID set matches 179 non-unanimous cases exactly: {completed_ids == master_ids}")
    print(f"Unanimous-case leakage: {len(leaked_unanimous)}")
    print(f"Language mismatches: {len(lang_mismatches)}")
    print(f"Sentiment value counts:\n{completed['adjudicated_sentiment'].value_counts().to_string()}")
    print(f"Confidence value counts (normalized):\n{completed['adjudication_confidence_norm'].value_counts().to_string()}")

    if failures:
        print("\nINTEGRITY CHECK FAILED:")
        for f in failures:
            print(f" - {f}")
        sys.exit(1)

    print("\nALL INTEGRITY CHECKS PASSED.")


if __name__ == "__main__":
    main()
