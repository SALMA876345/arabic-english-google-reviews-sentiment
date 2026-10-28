"""
Builds THREE independently-ordered, fully-blinded annotator CSVs from
human_validation_757_master.csv. All three get the SAME 757 review_ids but a
DIFFERENT deterministic shuffle (documented seeds below) -- reduces the
chance that a shared presentation-order effect or fatigue pattern affects
all three annotators identically, while remaining fully reproducible.

Visible columns only: review_id, language, text, sentiment_label, confidence,
mixed_sentiment_flag, notes (last four blank). No rating, no original_label,
no label_source, no model prediction, no source_group_id is carried over.

Run from the repository root: python paper/annotation/full/build_blinded_sheets.py
"""
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "paper" / "annotation" / "full"

ANNOTATOR_SEEDS = {
    "annotator_1": 1001,
    "annotator_2": 2002,
    "annotator_3": 3003,
}


def build_sheet(master, seed, out_name):
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(master))
    sheet = master.iloc[order][["review_id", "language", "text"]].reset_index(drop=True).copy()
    sheet["sentiment_label"] = ""
    sheet["confidence"] = ""
    sheet["mixed_sentiment_flag"] = ""
    sheet["notes"] = ""
    path = OUT / out_name
    sheet.to_csv(path, index=False, encoding="utf-8-sig")
    return sheet, path


def main():
    master = pd.read_csv(OUT / "human_validation_757_master.csv")
    assert len(master) == 757

    sheets = {}
    paths = {}
    for name, seed in ANNOTATOR_SEEDS.items():
        sheet, path = build_sheet(master, seed, f"{name}_blinded.csv")
        sheets[name] = sheet
        paths[name] = path
        print(f"{name}: seed={seed} -> {path.name}")

    # ---- Verification ----
    id_sets = {name: set(s.review_id) for name, s in sheets.items()}
    master_ids = set(master.review_id)
    for name, ids in id_sets.items():
        assert ids == master_ids, f"{name}'s review_id set does not match the master"
        assert len(sheets[name]) == 757

    print("\nAll three annotators' review_id sets identical to master and to each other: "
          f"{id_sets['annotator_1'] == id_sets['annotator_2'] == id_sets['annotator_3']}")

    orders = {name: s["review_id"].tolist() for name, s in sheets.items()}
    pairs = [("annotator_1", "annotator_2"), ("annotator_1", "annotator_3"), ("annotator_2", "annotator_3")]
    for a, b in pairs:
        differs = orders[a] != orders[b]
        print(f"Presentation order {a} != {b}: {differs} (must be True)")
        assert differs

    for name, s in sheets.items():
        blank_cells = sum(s[c].apply(lambda x: isinstance(x, str) and x.strip() != "").sum()
                           for c in ["sentiment_label", "confidence", "mixed_sentiment_flag", "notes"])
        print(f"{name}: non-blank label cells = {blank_cells} (must be 0)")
        assert blank_cells == 0
        leaked_cols = set(s.columns) & {"rating", "original_label", "label_source", "source_group_id", "word_count"}
        print(f"{name}: hidden columns present = {leaked_cols} (must be empty set)")
        assert len(leaked_cols) == 0

    print()
    for name, path in paths.items():
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"{path.name}: SHA-256 = {sha}")


if __name__ == "__main__":
    main()
