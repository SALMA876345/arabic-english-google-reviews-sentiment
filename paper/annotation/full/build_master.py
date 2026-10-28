"""
Builds paper/annotation/full/human_validation_757_master.csv directly from the
FROZEN test splits (data/splits/frozen_v1/*_test_ids.json + data/processed/frozen_v1/*.csv).

Does NOT resample, rebalance, or use ratings to select rows -- every row is
exactly the existing frozen test split, nothing more, nothing less. The 9
code-switch rows are explicitly excluded (they remain a separate E6 qualitative
set, see docs/codeswitch_audit.md and paper/annotation/pilot/ -- unrelated to
this file).

Run from the repository root: python paper/annotation/full/build_master.py
"""
import json
import hashlib
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
SPLITS = ROOT / "data" / "splits" / "frozen_v1"
FROZEN = ROOT / "data" / "processed" / "frozen_v1"
OUT = ROOT / "paper" / "annotation" / "full"


def load_ids(name):
    with open(SPLITS / f"{name}_test_ids.json", encoding="utf-8") as f:
        return json.load(f)


def main():
    ar_manifest = load_ids("arabic_tourism")
    en_manifest = load_ids("english_matched")

    ar_test_ids = set(ar_manifest["review_ids"])
    en_test_ids = set(en_manifest["review_ids"])
    print(f"Arabic frozen test manifest: {len(ar_test_ids)} ids")
    print(f"English frozen test manifest: {len(en_test_ids)} ids")
    assert len(ar_test_ids) == 369, f"Arabic manifest count is {len(ar_test_ids)}, expected 369"
    assert len(en_test_ids) == 388, f"English manifest count is {len(en_test_ids)}, expected 388"

    ar_frozen = pd.read_csv(FROZEN / "arabic_tourism_frozen.csv")
    en_frozen = pd.read_csv(FROZEN / "english_matched_frozen.csv")

    # Verify every manifest id exists in the frozen CSV, with split=="test", and
    # that we are NOT accidentally pulling any train/val rows.
    ar_test_rows = ar_frozen[ar_frozen.review_id.isin(ar_test_ids)]
    en_test_rows = en_frozen[en_frozen.review_id.isin(en_test_ids)]
    assert len(ar_test_rows) == len(ar_test_ids), "Some Arabic manifest IDs not found in frozen CSV"
    assert len(en_test_rows) == len(en_test_ids), "Some English manifest IDs not found in frozen CSV"
    assert (ar_test_rows["split"] == "test").all(), "Non-test-split row leaked into Arabic selection"
    assert (en_test_rows["split"] == "test").all(), "Non-test-split row leaked into English selection"
    # Also verify the inverse: no train/val row from either file is present by ID.
    ar_non_test_ids = set(ar_frozen.loc[ar_frozen.split != "test", "review_id"])
    en_non_test_ids = set(en_frozen.loc[en_frozen.split != "test", "review_id"])
    assert len(ar_test_ids & ar_non_test_ids) == 0, "Arabic train/val leakage detected"
    assert len(en_test_ids & en_non_test_ids) == 0, "English train/val leakage detected"

    ar_out = ar_test_rows[["review_id", "text", "sentiment", "label_source", "group_id", "word_count"]].copy()
    ar_out["language"] = "arabic"
    ar_out["rating"] = pd.NA
    en_out = en_test_rows[["review_id", "text", "sentiment", "label_source", "group_id", "word_count", "rating"]].copy()
    en_out["language"] = "english"

    master = pd.concat([ar_out, en_out], ignore_index=True)
    master = master.rename(columns={"sentiment": "original_label", "group_id": "source_group_id"})
    master = master[["review_id", "language", "text", "word_count", "original_label",
                      "label_source", "rating", "source_group_id"]]

    # ---- Final verification battery ----
    n_ar = (master.language == "arabic").sum()
    n_en = (master.language == "english").sum()
    n_total = len(master)
    n_dup_id = master.review_id.duplicated().sum()
    n_missing_text = master.text.isna().sum() + (master.text.astype(str).str.strip() == "").sum()
    cs_ids = {"AR-JOR-01270", "AR-JOR-04350", "AR-JOR-04600", "AR-JOR-06216", "AR-JOR-07320",
              "AR-JOR-07449", "AR-JOR-07691", "EN-VT-0213840", "EN-VT-0613379"}
    n_codeswitch_leaked = master.review_id.isin(cs_ids).sum()

    print(f"\nArabic count: {n_ar} (expected 369) -> {'OK' if n_ar == 369 else 'FAIL'}")
    print(f"English count: {n_en} (expected 388) -> {'OK' if n_en == 388 else 'FAIL'}")
    print(f"Total count: {n_total} (expected 757) -> {'OK' if n_total == 757 else 'FAIL'}")
    print(f"Duplicate review_id: {n_dup_id} (expected 0) -> {'OK' if n_dup_id == 0 else 'FAIL'}")
    print(f"Missing/empty text: {n_missing_text} (expected 0) -> {'OK' if n_missing_text == 0 else 'FAIL'}")
    print(f"Code-switch IDs accidentally included: {n_codeswitch_leaked} (expected 0) -> "
          f"{'OK' if n_codeswitch_leaked == 0 else 'FAIL'}")

    assert n_ar == 369 and n_en == 388 and n_total == 757
    assert n_dup_id == 0
    assert n_missing_text == 0
    assert n_codeswitch_leaked == 0

    master.to_csv(OUT / "human_validation_757_master.csv", index=False, encoding="utf-8-sig")

    sha = hashlib.sha256((OUT / "human_validation_757_master.csv").read_bytes()).hexdigest()
    print(f"\nWrote {OUT / 'human_validation_757_master.csv'}")
    print(f"SHA-256: {sha}")
    return sha


if __name__ == "__main__":
    main()
