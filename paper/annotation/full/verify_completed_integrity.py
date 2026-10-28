"""
Integrity verification for the three completed human annotation files, BEFORE
any agreement analysis runs. Reads from completed_raw/ (the immutable, hashed
copies) and reports pass/fail for every required check. Does not modify
anything; does not compute agreement statistics (that is compute_agreement.py's
job, run only after this passes).
"""
import hashlib
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
RAW = HERE / "completed_raw"
ANNOTATORS = ["annotator_1", "annotator_2", "annotator_3"]

VALID_SENTIMENT = {"Positive", "Neutral", "Negative"}
VALID_CONFIDENCE = {"high", "medium", "low"}
VALID_MIXED = {"yes", "no"}


def main():
    frames = {}
    hashes = {}
    for name in ANNOTATORS:
        path = RAW / f"{name}_completed.csv"
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        frames[name] = pd.read_csv(path)

    print("=== SHA-256 hashes (locked raw files) ===")
    for name, h in hashes.items():
        print(f"{name}_completed.csv: {h}")

    master = pd.read_csv(HERE / "human_validation_757_master.csv")
    master_ids = set(master.review_id)

    all_pass = True

    def check(label, condition):
        nonlocal all_pass
        status = "PASS" if condition else "FAIL"
        if not condition:
            all_pass = False
        print(f"[{status}] {label}")
        return condition

    print("\n=== Per-file checks ===")
    id_sets = {}
    for name, df in frames.items():
        n = len(df)
        n_unique = df.review_id.nunique()
        check(f"{name}: row count == 757 (actual: {n})", n == 757)
        check(f"{name}: unique review_id count == 757 (actual: {n_unique})", n_unique == 757)
        check(f"{name}: zero duplicate review_id", df.review_id.duplicated().sum() == 0)
        check(f"{name}: review_id set matches master exactly", set(df.review_id) == master_ids)
        id_sets[name] = set(df.review_id)

        n_ar = (df.language == "arabic").sum()
        n_en = (df.language == "english").sum()
        check(f"{name}: Arabic count == 369 (actual: {n_ar})", n_ar == 369)
        check(f"{name}: English count == 388 (actual: {n_en})", n_en == 388)

        missing_sent = df.sentiment_label.isna().sum() + (df.sentiment_label.astype(str).str.strip() == "").sum()
        missing_conf = df.confidence.isna().sum() + (df.confidence.astype(str).str.strip() == "").sum()
        missing_mixed = df.mixed_sentiment_flag.isna().sum() + (df.mixed_sentiment_flag.astype(str).str.strip() == "").sum()
        check(f"{name}: zero missing sentiment_label (actual missing: {missing_sent})", missing_sent == 0)
        check(f"{name}: zero missing confidence (actual missing: {missing_conf})", missing_conf == 0)
        check(f"{name}: zero missing mixed_sentiment_flag (actual missing: {missing_mixed})", missing_mixed == 0)

        bad_sent = ~df.sentiment_label.isin(VALID_SENTIMENT)
        bad_conf = ~df.confidence.isin(VALID_CONFIDENCE)
        bad_mixed = ~df.mixed_sentiment_flag.isin(VALID_MIXED)
        check(f"{name}: all sentiment_label values valid (bad: {bad_sent.sum()})", bad_sent.sum() == 0)
        check(f"{name}: all confidence values valid (bad: {bad_conf.sum()})", bad_conf.sum() == 0)
        check(f"{name}: all mixed_sentiment_flag values valid (bad: {bad_mixed.sum()})", bad_mixed.sum() == 0)

    print("\n=== Cross-file checks ===")
    check("All three review_id sets identical to each other",
          id_sets["annotator_1"] == id_sets["annotator_2"] == id_sets["annotator_3"])

    # language agreement across all three files, keyed by review_id
    merged = frames["annotator_1"][["review_id", "language"]].rename(columns={"language": "lang_1"})
    merged = merged.merge(frames["annotator_2"][["review_id", "language"]].rename(columns={"language": "lang_2"}), on="review_id")
    merged = merged.merge(frames["annotator_3"][["review_id", "language"]].rename(columns={"language": "lang_3"}), on="review_id")
    lang_mismatch = merged[(merged.lang_1 != merged.lang_2) | (merged.lang_1 != merged.lang_3)]
    check(f"language field agrees across all three files for every review_id (mismatches: {len(lang_mismatch)})",
          len(lang_mismatch) == 0)

    merged_master = merged.merge(master[["review_id", "language"]].rename(columns={"language": "lang_master"}), on="review_id")
    master_mismatch = merged_master[merged_master.lang_1 != merged_master.lang_master]
    check(f"language field agrees with master for every review_id (mismatches: {len(master_mismatch)})",
          len(master_mismatch) == 0)

    print(f"\n=== OVERALL: {'ALL CHECKS PASSED' if all_pass else 'SOME CHECKS FAILED -- DO NOT PROCEED'} ===")
    return all_pass, hashes


if __name__ == "__main__":
    ok, hashes = main()
    exit(0 if ok else 1)
