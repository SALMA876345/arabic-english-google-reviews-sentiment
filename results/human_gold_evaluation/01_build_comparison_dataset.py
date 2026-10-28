"""
Section A/B/C of the Human-Gold label analysis phase.

Read-only with respect to all prior artifacts: does not modify
human_gold_757.csv, human_validation_757_master.csv, any Phase 3A/3B result,
or any frozen split. Writes new outputs only under results/human_gold_evaluation/.

Step A: re-verify the frozen Human-Gold hash and integrity, then build a
        review-level comparison dataset (original_label vs human_gold_sentiment)
        with both columns kept distinct.
Step B: overall/Arabic/English agreement, Cohen's kappa, confusion matrix,
        6 named transitions, class distributions.
Step C: disagreement rate conditional on original class / Human-Gold class /
        language, full transition table.
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score, confusion_matrix

REPO_ROOT = Path(__file__).resolve().parents[2]
ANNOT = REPO_ROOT / "paper" / "annotation" / "full"
OUT = Path(__file__).resolve().parent
SPLITS = REPO_ROOT / "data" / "splits" / "frozen_v1"

EXPECTED_HASH = "7b53ca621d237106413e27395010ad9ba2417d733b2bc5694d49749a03be53fd"
LABEL_ORDER = ["Negative", "Neutral", "Positive"]


def load_ids(fname):
    data = json.load(open(SPLITS / fname, encoding="utf-8"))
    return set(data["review_ids"])


def section_a():
    gold_path = ANNOT / "human_gold_757.csv"
    actual_hash = hashlib.sha256(gold_path.read_bytes()).hexdigest()
    assert actual_hash == EXPECTED_HASH, f"Human-Gold hash mismatch! expected {EXPECTED_HASH}, got {actual_hash}"

    gold = pd.read_csv(gold_path)
    assert len(gold) == 757, f"Expected 757 rows, found {len(gold)}"
    assert gold.review_id.nunique() == 757, "Duplicate review_ids in Human-Gold"
    assert (gold.language == "arabic").sum() == 369, "Arabic count != 369"
    assert (gold.language == "english").sum() == 388, "English count != 388"

    ar_test = load_ids("arabic_tourism_test_ids.json")
    en_test = load_ids("english_matched_test_ids.json")
    frozen_ids = ar_test | en_test
    assert set(gold.review_id) == frozen_ids, "Human-Gold ids do not exactly match frozen test ids"
    assert gold.human_gold_sentiment.isna().sum() == 0, "Missing Human-Gold labels present"

    master = pd.read_csv(ANNOT / "human_validation_757_master.csv")
    assert len(master) == 757 and master.review_id.nunique() == 757
    assert master.original_label.isna().sum() == 0, "Missing original_label values in master"

    merged = gold[["review_id", "language", "text", "human_gold_sentiment", "human_gold_source", "agreement_type"]].merge(
        master[["review_id", "original_label", "label_source", "rating"]], on="review_id", how="left", validate="one_to_one")
    assert merged.original_label.isna().sum() == 0, "Merge produced missing original_label -- id mismatch"
    assert len(merged) == 757

    merged["agree"] = merged["original_label"] == merged["human_gold_sentiment"]

    out_path = OUT / "comparison_dataset_757.csv"
    merged.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"[A] Human-Gold hash verified: {actual_hash}")
    print(f"[A] Wrote {out_path} ({len(merged)} rows)")
    return merged


def agreement_block(df):
    n = len(df)
    agree_n = int(df.agree.sum())
    disagree_n = n - agree_n
    kappa = cohen_kappa_score(df.original_label, df.human_gold_sentiment, labels=LABEL_ORDER)
    cm = confusion_matrix(df.original_label, df.human_gold_sentiment, labels=LABEL_ORDER)
    cm_df = pd.DataFrame(cm, index=[f"original_{l}" for l in LABEL_ORDER], columns=[f"human_gold_{l}" for l in LABEL_ORDER])
    return {
        "n": n,
        "agree_count": agree_n,
        "agree_pct": round(agree_n / n * 100, 2),
        "disagree_count": disagree_n,
        "disagree_pct": round(disagree_n / n * 100, 2),
        "cohen_kappa": float(kappa),
        "confusion_matrix_original_rows_humangold_cols": cm_df.to_dict(),
    }, cm_df


def section_b(merged):
    result = {}
    cms = {}
    result["overall"], cms["overall"] = agreement_block(merged)
    for lang in ["arabic", "english"]:
        sub = merged[merged.language == lang]
        result[lang], cms[lang] = agreement_block(sub)

    transitions_named = {
        "Positive_to_Neutral": int(((merged.original_label == "Positive") & (merged.human_gold_sentiment == "Neutral")).sum()),
        "Positive_to_Negative": int(((merged.original_label == "Positive") & (merged.human_gold_sentiment == "Negative")).sum()),
        "Neutral_to_Positive": int(((merged.original_label == "Neutral") & (merged.human_gold_sentiment == "Positive")).sum()),
        "Neutral_to_Negative": int(((merged.original_label == "Neutral") & (merged.human_gold_sentiment == "Negative")).sum()),
        "Negative_to_Neutral": int(((merged.original_label == "Negative") & (merged.human_gold_sentiment == "Neutral")).sum()),
        "Negative_to_Positive": int(((merged.original_label == "Negative") & (merged.human_gold_sentiment == "Positive")).sum()),
    }
    result["transitions_named"] = transitions_named

    orig_dist = merged.original_label.value_counts().reindex(LABEL_ORDER).fillna(0).astype(int)
    gold_dist = merged.human_gold_sentiment.value_counts().reindex(LABEL_ORDER).fillna(0).astype(int)
    result["original_class_distribution"] = orig_dist.to_dict()
    result["human_gold_class_distribution"] = gold_dist.to_dict()
    for lang in ["arabic", "english"]:
        sub = merged[merged.language == lang]
        result[f"original_class_distribution_{lang}"] = sub.original_label.value_counts().reindex(LABEL_ORDER).fillna(0).astype(int).to_dict()
        result[f"human_gold_class_distribution_{lang}"] = sub.human_gold_sentiment.value_counts().reindex(LABEL_ORDER).fillna(0).astype(int).to_dict()

    with open(OUT / "label_agreement_overall_by_language.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, default=str)
    for key, cm_df in cms.items():
        cm_df.to_csv(OUT / f"confusion_matrix_original_vs_humangold_{key}.csv")
    print(f"[B] overall agreement: {result['overall']['agree_count']}/{result['overall']['n']} ({result['overall']['agree_pct']}%), kappa={result['overall']['cohen_kappa']:.4f}")
    print(f"[B] arabic agreement: {result['arabic']['agree_count']}/{result['arabic']['n']} ({result['arabic']['agree_pct']}%), kappa={result['arabic']['cohen_kappa']:.4f}")
    print(f"[B] english agreement: {result['english']['agree_count']}/{result['english']['n']} ({result['english']['agree_pct']}%), kappa={result['english']['cohen_kappa']:.4f}")
    print(f"[B] transitions: {transitions_named}")
    return result


def section_c(merged):
    rows = []
    for lang_label, sub in [("overall", merged), ("arabic", merged[merged.language == "arabic"]), ("english", merged[merged.language == "english"])]:
        for cls in LABEL_ORDER:
            orig_sub = sub[sub.original_label == cls]
            if len(orig_sub) > 0:
                rows.append({
                    "scope": lang_label, "conditioned_on": "original_label", "class": cls,
                    "n": len(orig_sub), "disagree_n": int((~orig_sub.agree).sum()),
                    "disagree_rate_pct": round((~orig_sub.agree).mean() * 100, 2),
                })
            gold_sub = sub[sub.human_gold_sentiment == cls]
            if len(gold_sub) > 0:
                rows.append({
                    "scope": lang_label, "conditioned_on": "human_gold_sentiment", "class": cls,
                    "n": len(gold_sub), "disagree_n": int((~gold_sub.agree).sum()),
                    "disagree_rate_pct": round((~gold_sub.agree).mean() * 100, 2),
                })
    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUT / "disagreement_rate_conditional.csv", index=False)

    full_transitions = pd.crosstab(merged.original_label, merged.human_gold_sentiment)
    full_transitions.to_csv(OUT / "full_transition_table_overall.csv")
    for lang in ["arabic", "english"]:
        sub = merged[merged.language == lang]
        pd.crosstab(sub.original_label, sub.human_gold_sentiment).to_csv(OUT / f"full_transition_table_{lang}.csv")

    print("[C] Wrote disagreement_rate_conditional.csv and full_transition_table_*.csv")
    print(out_df.to_string(index=False))
    return out_df


def main():
    merged = section_a()
    section_b(merged)
    section_c(merged)
    print("\nSection A/B/C complete. No prior artifact modified; all outputs written under results/human_gold_evaluation/.")


if __name__ == "__main__":
    main()
