"""
Phase 2.5 step 3 (REVISED, supersedes the group-naive build_validation_slice.py):
group-aware train/val/test freeze for the primary Arabic (tourism) and
matched English pools, so the same place/business never appears in both
train and test. The resulting TEST group membership becomes the manual-
annotation candidate set (docs/annotation_guidelines.md) -- group integrity
takes priority over hitting an exact row count or exact sentiment %, which
are reported as achieved, not forced.

Jordan (auxiliary, no business identifier available in the release) and
the full English pool are handled separately per docs/experimental_dataset_protocol.md.
"""
import numpy as np
import pandas as pd
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
SPLITS = ROOT / "data" / "splits" / "frozen_v1"
PROCESSED_FROZEN = ROOT / "data" / "processed" / "frozen_v1"
ANNOT = ROOT / "data" / "annotations"
SPLITS.mkdir(parents=True, exist_ok=True)
PROCESSED_FROZEN.mkdir(parents=True, exist_ok=True)
SEED = 42

TARGET_FRAC = {"train": 0.79, "val": 0.10, "test": 0.11}


def group_split(df, group_col, seed):
    """Assign whole groups to train/val/test via greedy proportion-filling.
    Groups with no id (NaN) are treated as singleton groups (one row each)."""
    rng = np.random.default_rng(seed)
    df = df.copy()
    if df[group_col].isna().any():
        missing_mask = df[group_col].isna()
        df.loc[missing_mask, group_col] = ["__singleton_%d__" % i for i in range(missing_mask.sum())]

    group_sizes = df.groupby(group_col).size().sample(frac=1.0, random_state=seed)  # shuffle group order
    total = len(df)
    targets = {k: v * total for k, v in TARGET_FRAC.items()}
    current = {"train": 0, "val": 0, "test": 0}
    assignment = {}
    for g, size in group_sizes.items():
        # assign to whichever split is furthest below its target (in absolute rows)
        deficits = {k: targets[k] - current[k] for k in current}
        choice = max(deficits, key=deficits.get)
        assignment[g] = choice
        current[choice] += size

    df["split"] = df[group_col].map(assignment)
    return df, current


def report_sentiment(df, name):
    print(f"\n{name} achieved split sizes and sentiment %:")
    for split in ["train", "val", "test"]:
        sub = df[df["split"] == split]
        pct = (sub["sentiment"].value_counts(normalize=True) * 100).round(1).to_dict()
        print(f"  {split}: n={len(sub)} ({len(sub)/len(df)*100:.1f}%) sentiment%={pct}")


# ---------------------------------------------------------------------------
# Arabic tourism (primary) -- group by place name
# ---------------------------------------------------------------------------
ar = pd.read_csv(PROCESSED / "arabic_tourism_v2.csv")
ar_split, ar_counts = group_split(ar, "group_id", SEED)
report_sentiment(ar_split, "Arabic tourism (primary)")

# ---------------------------------------------------------------------------
# English matched subset -- group by gmap_id (business)
# ---------------------------------------------------------------------------
en = pd.read_csv(PROCESSED / "english_matched_v1.csv")
en_split, en_counts = group_split(en, "group_id", SEED)
report_sentiment(en_split, "English matched subset")

# ---------------------------------------------------------------------------
# Dedup check: confirm no duplicate text hash crosses a train/test boundary
# ---------------------------------------------------------------------------
import hashlib, re


def norm(t):
    return re.sub(r"\s+", " ", str(t).strip().lower())


for name, d in [("Arabic tourism", ar_split), ("English matched", en_split)]:
    d["_hash"] = d["text"].map(lambda t: hashlib.md5(norm(t).encode()).hexdigest())
    dup_hashes = d["_hash"].value_counts()
    dup_hashes = dup_hashes[dup_hashes > 1]
    cross_split_leaks = 0
    for h in dup_hashes.index:
        if d.loc[d["_hash"] == h, "split"].nunique() > 1:
            cross_split_leaks += 1
    print(f"{name}: {len(dup_hashes)} residual duplicate-hash groups, "
          f"{cross_split_leaks} of which cross a split boundary (should be 0, dedup already applied upstream)")
    d.drop(columns=["_hash"], inplace=True)

# ---------------------------------------------------------------------------
# Save frozen data + manifests
# ---------------------------------------------------------------------------
ar_split.to_csv(PROCESSED_FROZEN / "arabic_tourism_frozen.csv", index=False, encoding="utf-8-sig")
en_split.to_csv(PROCESSED_FROZEN / "english_matched_frozen.csv", index=False, encoding="utf-8-sig")

manifest = {"seed": SEED, "target_fractions": TARGET_FRAC, "group_split": True}
for name, d, gcol in [("arabic_tourism", ar_split, "group_id"), ("english_matched", en_split, "group_id")]:
    for split in ["train", "val", "test"]:
        ids = d.loc[d["split"] == split, "review_id"].tolist()
        with open(SPLITS / f"{name}_{split}_ids.json", "w", encoding="utf-8") as f:
            json.dump({"dataset": name, "split": split, "seed": SEED, "n": len(ids), "review_ids": ids}, f, indent=1)

with open(SPLITS / "manifest.json", "w", encoding="utf-8") as f:
    json.dump({
        "seed": SEED,
        "target_fractions": TARGET_FRAC,
        "method": "group-aware greedy assignment (whole place/business groups never split across train/val/test)",
        "datasets": {
            "arabic_tourism": {"n": len(ar_split), "groups": "place name (اسم المكان)",
                                "n_groups": ar_split["group_id"].nunique()},
            "english_matched": {"n": len(en_split), "groups": "gmap_id (business)",
                                 "n_groups": en_split["group_id"].nunique()},
        },
        "frozen_date": "2026-10-24",
        "note": "TEST split membership (by review_id) must not change after this point regardless of model performance. See docs/decisions.md D11.",
    }, f, indent=2)

print("\nWrote data/processed/frozen_v1/*.csv and data/splits/frozen_v1/*.json manifests")

# ---------------------------------------------------------------------------
# Update the manual-annotation candidate set to match the GROUP-AWARE test split
# ---------------------------------------------------------------------------
ar_test = ar_split[ar_split["split"] == "test"].copy()
ar_test["language"] = "arabic"
en_test = en_split[en_split["split"] == "test"].copy()
en_test["language"] = "english"
main_slice = pd.concat([ar_test, en_test], ignore_index=True, sort=False)
main_slice["is_difficult_short"] = main_slice["word_count"] <= 5
main_slice["slice_type"] = "main_stratified"

cs_ids = ["AR-JOR-01270", "AR-JOR-04350", "AR-JOR-04600", "AR-JOR-06216", "AR-JOR-07320",
          "AR-JOR-07449", "AR-JOR-07691", "EN-VT-0213840", "EN-VT-0613379"]
jordan = pd.read_csv(PROCESSED / "arabic_jordan_v2.csv")
english_full = pd.read_csv(PROCESSED / "english_ucsd_v2.csv")
cs_rows = pd.concat([
    jordan[jordan["review_id"].isin(cs_ids)].assign(language="arabic"),
    english_full[english_full["review_id"].isin(cs_ids)].assign(language="english"),
], ignore_index=True)
cs_rows["is_difficult_short"] = cs_rows["word_count"] <= 5
cs_rows["slice_type"] = "codeswitch_diagnostic"

full_candidate_set = pd.concat([main_slice, cs_rows], ignore_index=True, sort=False)
full_candidate_set[["review_id", "language", "slice_type"]].to_csv(
    ANNOT / "validation_slice_candidate_ids.csv", index=False, encoding="utf-8-sig")

template_cols = ["review_id", "language", "text", "word_count", "slice_type", "is_difficult_short"]
template = full_candidate_set[template_cols].copy()
template["annotator_label"] = ""
template["annotator_confidence"] = ""
template["annotator_notes"] = ""
template.to_csv(ANNOT / "annotation_template_pending.csv", index=False, encoding="utf-8-sig")

print(f"\nFINAL (group-aware) manual-annotation candidate set: {len(full_candidate_set)} "
      f"({len(main_slice)} main [{len(ar_test)} AR + {len(en_test)} EN] + {len(cs_rows)} code-switch diagnostic)")
print("These main-slice review_ids ARE the frozen TEST set for arabic_tourism and english_matched.")
