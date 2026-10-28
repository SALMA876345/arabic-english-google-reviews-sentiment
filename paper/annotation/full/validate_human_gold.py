"""
Strict integrity/validation gate for human_gold_757.csv. Read-only -- does not
modify any file. Exits non-zero on any failure.

Checks required by the Human-Gold construction spec:
  - exactly 757 rows, 757 unique review_ids
  - Arabic = 369, English = 388
  - no missing human_gold_sentiment
  - allowed labels only: Positive / Neutral / Negative
  - exactly 578 rows sourced unanimous_3of3, exactly 179 independent_adjudication
  - review_id set exactly equals frozen Arabic test ids + frozen English test ids
  - zero overlap with frozen train ids, zero overlap with frozen val ids
  - review text unchanged vs human_validation_757_master.csv (which is itself
    built from the frozen test splits)
"""
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent  # .../full/
REPO_ROOT = ROOT.parent.parent.parent    # repo root
SPLITS = REPO_ROOT / "data" / "splits" / "frozen_v1"
VALID_SENTIMENT = {"Positive", "Neutral", "Negative"}

failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)


def load_ids(fname):
    data = json.load(open(SPLITS / fname, encoding="utf-8"))
    return set(data["review_ids"])


def main():
    gold = pd.read_csv(ROOT / "human_gold_757.csv")
    master = pd.read_csv(ROOT / "human_validation_757_master.csv")

    # -- basic shape --
    check(len(gold) == 757, f"Expected 757 rows, found {len(gold)}")
    check(gold.review_id.nunique() == 757, f"Expected 757 unique review_ids, found {gold.review_id.nunique()}")

    ar_count = (gold.language == "arabic").sum()
    en_count = (gold.language == "english").sum()
    check(ar_count == 369, f"Expected 369 Arabic rows, found {ar_count}")
    check(en_count == 388, f"Expected 388 English rows, found {en_count}")

    check(gold.human_gold_sentiment.isna().sum() == 0, "Missing human_gold_sentiment values present")
    bad_labels = gold[~gold.human_gold_sentiment.isin(VALID_SENTIMENT)]
    check(len(bad_labels) == 0, f"Invalid human_gold_sentiment values: {bad_labels[['review_id','human_gold_sentiment']].to_dict('records')}")

    src_counts = gold.human_gold_source.value_counts().to_dict()
    check(src_counts.get("unanimous_3of3", 0) == 578, f"Expected 578 unanimous_3of3 rows, found {src_counts.get('unanimous_3of3', 0)}")
    check(src_counts.get("independent_adjudication", 0) == 179, f"Expected 179 independent_adjudication rows, found {src_counts.get('independent_adjudication', 0)}")
    check(sum(src_counts.values()) == 757, "human_gold_source counts do not sum to 757")

    # -- ID set vs frozen test splits --
    frozen_ar_test = load_ids("arabic_tourism_test_ids.json")
    frozen_en_test = load_ids("english_matched_test_ids.json")
    frozen_test_ids = frozen_ar_test | frozen_en_test
    check(len(frozen_test_ids) == 757, f"Frozen Arabic+English test ids do not sum to 757, found {len(frozen_test_ids)}")

    gold_ids = set(gold.review_id)
    check(gold_ids == frozen_test_ids,
          f"Human-Gold review_id set does not exactly match frozen test ids: "
          f"missing={frozen_test_ids - gold_ids}, unexpected={gold_ids - frozen_test_ids}")

    # -- leakage checks vs train/val --
    frozen_ar_train = load_ids("arabic_tourism_train_ids.json")
    frozen_ar_val = load_ids("arabic_tourism_val_ids.json")
    frozen_en_train = load_ids("english_matched_train_ids.json")
    frozen_en_val = load_ids("english_matched_val_ids.json")
    train_ids = frozen_ar_train | frozen_en_train
    val_ids = frozen_ar_val | frozen_en_val

    train_leak = gold_ids & train_ids
    val_leak = gold_ids & val_ids
    check(len(train_leak) == 0, f"Train leakage detected: {train_leak}")
    check(len(val_leak) == 0, f"Val leakage detected: {val_leak}")

    # -- text fidelity vs master (itself built from frozen test splits) --
    master_text = master.set_index("review_id")["text"]
    text_mismatches = []
    for _, row in gold.iterrows():
        rid = row["review_id"]
        if rid not in master_text.index:
            text_mismatches.append((rid, "MISSING_FROM_MASTER"))
        elif row["text"] != master_text.loc[rid]:
            text_mismatches.append((rid, "TEXT_DIFFERS"))
    check(len(text_mismatches) == 0, f"Text mismatches vs frozen master: {text_mismatches[:10]}")

    # -- report --
    print(f"Rows: {len(gold)} | Unique IDs: {gold.review_id.nunique()}")
    print(f"Arabic: {ar_count} | English: {en_count}")
    print(f"human_gold_source counts: {src_counts}")
    print(f"ID set matches frozen test splits exactly: {gold_ids == frozen_test_ids}")
    print(f"Train leakage: {len(train_leak)} | Val leakage: {len(val_leak)}")
    print(f"Text mismatches vs frozen master: {len(text_mismatches)}")

    print("\nOverall class distribution:")
    print(gold.human_gold_sentiment.value_counts().to_string())
    print(f"\nOverall class distribution (%):")
    print((gold.human_gold_sentiment.value_counts(normalize=True) * 100).round(1).to_string())

    print("\nArabic class distribution:")
    ar_dist = gold[gold.language == "arabic"].human_gold_sentiment.value_counts()
    print(ar_dist.to_string())
    print((ar_dist / ar_dist.sum() * 100).round(1).to_string())

    print("\nEnglish class distribution:")
    en_dist = gold[gold.language == "english"].human_gold_sentiment.value_counts()
    print(en_dist.to_string())
    print((en_dist / en_dist.sum() * 100).round(1).to_string())

    print("\nProvenance x class crosstab:")
    print(pd.crosstab(gold.human_gold_source, gold.human_gold_sentiment).to_string())

    if failures:
        print("\nVALIDATION FAILED:")
        for f in failures:
            print(f" - {f}")
        sys.exit(1)

    print("\nALL HUMAN-GOLD VALIDATION CHECKS PASSED.")


if __name__ == "__main__":
    main()
