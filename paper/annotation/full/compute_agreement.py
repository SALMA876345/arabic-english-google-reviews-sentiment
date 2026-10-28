"""
3-rater agreement analysis for the full 757-review RQ3 human-validation round.
Reads the LOCKED raw completed files from completed_raw/ (never modifies them).
Writes machine-readable outputs to agreement_outputs/.

Computes, for PRIMARY SENTIMENT (kept entirely separate from mixed_sentiment_flag,
per instruction -- mixed is a secondary variable, never merged into the main label):
  - overall unanimous/majority/disagreement rates, Fleiss' kappa, Krippendorff's
    alpha, pairwise raw agreement + Cohen's kappa
  - the same, split by language (Arabic, English)
  - disagreement structure: which class-pairs (Pos/Neu, Neg/Neu, Pos/Neg) drive
    2/3 disagreements, overall and per language

For MIXED_SENTIMENT_FLAG (secondary variable):
  - overall/pairwise agreement, Fleiss' kappa, Krippendorff's alpha
  - per-annotator mixed=yes frequency
  - Arabic vs English mixed agreement

For CONFIDENCE (metadata, never treated as ground truth or converted to a label):
  - per-annotator distribution
  - cross-tab of confidence vs whether that row was a 3/3-unanimous or
    non-unanimous sentiment case (does low confidence associate with disagreement)

Run: python paper/annotation/full/compute_agreement.py
"""
import json
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score
from statsmodels.stats.inter_rater import fleiss_kappa, aggregate_raters
import krippendorff

HERE = Path(__file__).resolve().parent
RAW = HERE / "completed_raw"
OUT = HERE / "agreement_outputs"
ANNOTATORS = ["annotator_1", "annotator_2", "annotator_3"]
SENTIMENT_LABELS = ["Positive", "Neutral", "Negative"]
MIXED_LABELS = ["yes", "no"]


def load_all():
    master = pd.read_csv(HERE / "human_validation_757_master.csv")
    merged = master[["review_id", "language"]].copy()
    for name in ANNOTATORS:
        df = pd.read_csv(RAW / f"{name}_completed.csv")
        sub = df[["review_id", "sentiment_label", "confidence", "mixed_sentiment_flag"]].copy()
        sub = sub.rename(columns={c: f"{c}_{name}" for c in sub.columns if c != "review_id"})
        merged = merged.merge(sub, on="review_id", how="left")
    assert merged.isna().sum().sum() == 0, "Unexpected NaNs after merge -- integrity check should have caught this."
    return merged


def fleiss_and_alpha(df, cols, labels):
    code = {lab: i for i, lab in enumerate(labels)}
    coded = df[cols].apply(lambda col: col.map(code)).values.astype(int)  # items x raters, integer codes
    rating_table, _ = aggregate_raters(coded, n_cat=len(labels))
    fk = fleiss_kappa(rating_table, method="fleiss")
    alpha = krippendorff.alpha(reliability_data=coded.T, level_of_measurement="nominal")  # raters x items
    return fk, alpha


def compute_block(df, value_cols, labels, name):
    """value_cols: dict annotator -> column name for the variable being analyzed."""
    cols = [value_cols[a] for a in ANNOTATORS]

    def agreement_type(row):
        vals = [row[c] for c in cols]
        n_unique = len(set(vals))
        return "unanimous" if n_unique == 1 else ("majority" if n_unique == 2 else "disagreement")

    df = df.copy()
    df["_agreement_type"] = df.apply(agreement_type, axis=1)
    n = len(df)
    counts = df["_agreement_type"].value_counts()
    unanimous_n = int(counts.get("unanimous", 0))
    majority_n = int(counts.get("majority", 0))
    disagreement_n = int(counts.get("disagreement", 0))

    fk, alpha = fleiss_and_alpha(df, cols, labels)

    pairwise_raw = {}
    pairwise_kappa = {}
    for a, b in combinations(ANNOTATORS, 2):
        ca, cb = value_cols[a], value_cols[b]
        pairwise_raw[f"{a}_vs_{b}"] = float((df[ca] == df[cb]).mean())
        pairwise_kappa[f"{a}_vs_{b}"] = float(cohen_kappa_score(df[ca], df[cb]))

    return {
        "block": name,
        "n": n,
        "unanimous_3of3_n": unanimous_n,
        "unanimous_3of3_rate": unanimous_n / n,
        "majority_2of3_n": majority_n,
        "majority_2of3_rate": majority_n / n,
        "at_least_2of3_rate": (unanimous_n + majority_n) / n,
        "disagreement_3way_n": disagreement_n,
        "disagreement_3way_rate": disagreement_n / n,
        "fleiss_kappa": float(fk),
        "krippendorff_alpha_nominal": float(alpha),
        "pairwise_raw_agreement": pairwise_raw,
        "pairwise_cohen_kappa": pairwise_kappa,
    }, df["_agreement_type"]


def class_pair_breakdown(df, sent_cols, agreement_type_series, label_suffix=""):
    """For majority (2/3) rows, which two classes are the majority-vs-minority pair?
    For disagreement (3-way) rows, just count them (all 3 classes present)."""
    pairs = {f"{a}_vs_{b}": 0 for a, b in combinations(SENTIMENT_LABELS, 2)}
    three_way = 0
    for idx, row in df.iterrows():
        atype = agreement_type_series.loc[idx]
        if atype == "unanimous":
            continue
        vals = sorted([row[c] for c in sent_cols])
        unique_vals = sorted(set(vals))
        if atype == "majority":
            # exactly 2 distinct labels present among the 3 votes
            key = "_vs_".join(unique_vals)
            if key in pairs:
                pairs[key] += 1
            else:
                pairs["_vs_".join(reversed(unique_vals))] += 1
        else:
            three_way += 1
    pairs["three_way_all_classes"] = three_way
    return pairs


def confidence_block(df):
    conf_cols = [f"confidence_{a}" for a in ANNOTATORS]
    dist = {a: df[f"confidence_{a}"].value_counts(normalize=True).to_dict() for a in ANNOTATORS}

    sent_cols = [f"sentiment_label_{a}" for a in ANNOTATORS]

    def row_type(row):
        vals = [row[c] for c in sent_cols]
        return "unanimous" if len(set(vals)) == 1 else "non_unanimous"

    df = df.copy()
    df["_row_type"] = df.apply(row_type, axis=1)

    low_conf_by_type = {}
    for a in ANNOTATORS:
        cross = df.groupby("_row_type")[f"confidence_{a}"].value_counts(normalize=True).unstack(fill_value=0)
        low_conf_by_type[a] = cross.to_dict(orient="index")

    return {"confidence_distribution_per_annotator": dist,
            "low_confidence_rate_by_unanimous_vs_nonunanimous": low_conf_by_type}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    df = load_all()
    sent_cols = {a: f"sentiment_label_{a}" for a in ANNOTATORS}
    mixed_cols = {a: f"mixed_sentiment_flag_{a}" for a in ANNOTATORS}

    # ---------------- PRIMARY SENTIMENT: overall ----------------
    overall_sent, overall_atype = compute_block(df, sent_cols, SENTIMENT_LABELS, "overall_sentiment")
    with open(OUT / "overall_agreement_sentiment.json", "w", encoding="utf-8") as f:
        json.dump(overall_sent, f, indent=2)
    print("=== OVERALL SENTIMENT ===")
    print(json.dumps(overall_sent, indent=2))

    # ---------------- PRIMARY SENTIMENT: by language ----------------
    by_language = {}
    for lang in ["arabic", "english"]:
        sub = df[df.language == lang]
        block, atype_sub = compute_block(sub, sent_cols, SENTIMENT_LABELS, f"sentiment_{lang}")
        by_language[lang] = block
    with open(OUT / "language_specific_agreement_sentiment.json", "w", encoding="utf-8") as f:
        json.dump(by_language, f, indent=2)
    print("\n=== BY LANGUAGE (SENTIMENT) ===")
    print(json.dumps(by_language, indent=2))

    # ---------------- Disagreement structure: class-pair breakdown ----------------
    sc = list(sent_cols.values())
    overall_pairs = class_pair_breakdown(df, sc, overall_atype)
    ar_mask = df.language == "arabic"
    en_mask = df.language == "english"
    _, ar_atype = compute_block(df[ar_mask], sent_cols, SENTIMENT_LABELS, "ar_tmp")
    _, en_atype = compute_block(df[en_mask], sent_cols, SENTIMENT_LABELS, "en_tmp")
    ar_atype.index = df[ar_mask].index
    en_atype.index = df[en_mask].index
    ar_pairs = class_pair_breakdown(df[ar_mask], sc, ar_atype)
    en_pairs = class_pair_breakdown(df[en_mask], sc, en_atype)

    disagreement_structure = {"overall": overall_pairs, "arabic": ar_pairs, "english": en_pairs}
    with open(OUT / "disagreement_class_pair_breakdown.json", "w", encoding="utf-8") as f:
        json.dump(disagreement_structure, f, indent=2)
    pd.DataFrame(disagreement_structure).to_csv(OUT / "disagreement_class_pair_breakdown.csv")
    print("\n=== DISAGREEMENT CLASS-PAIR BREAKDOWN ===")
    print(json.dumps(disagreement_structure, indent=2))

    # ---------------- MIXED SENTIMENT FLAG (secondary, kept separate) ----------------
    overall_mixed, _ = compute_block(df, mixed_cols, MIXED_LABELS, "overall_mixed_flag")
    by_language_mixed = {}
    for lang in ["arabic", "english"]:
        sub = df[df.language == lang]
        block, _ = compute_block(sub, mixed_cols, MIXED_LABELS, f"mixed_{lang}")
        by_language_mixed[lang] = block
    mixed_freq = {a: float((df[f"mixed_sentiment_flag_{a}"] == "yes").sum()) for a in ANNOTATORS}
    mixed_block = {"overall": overall_mixed, "by_language": by_language_mixed,
                   "mixed_yes_frequency_per_annotator": mixed_freq}
    with open(OUT / "mixed_sentiment_flag_agreement.json", "w", encoding="utf-8") as f:
        json.dump(mixed_block, f, indent=2)
    print("\n=== MIXED SENTIMENT FLAG (SECONDARY VARIABLE) ===")
    print(json.dumps(mixed_block, indent=2))

    # ---------------- CONFIDENCE (metadata only) ----------------
    conf_block = confidence_block(df)
    with open(OUT / "confidence_analysis.json", "w", encoding="utf-8") as f:
        json.dump(conf_block, f, indent=2, default=str)
    print("\n=== CONFIDENCE ANALYSIS (metadata, not ground truth) ===")
    print(json.dumps(conf_block, indent=2, default=str))

    # ---------------- Pairwise summary CSV (sentiment + mixed, easy to drop into a table) ----------------
    rows = []
    for a, b in combinations(ANNOTATORS, 2):
        rows.append({
            "pair": f"{a}_vs_{b}",
            "sentiment_raw_agreement": overall_sent["pairwise_raw_agreement"][f"{a}_vs_{b}"],
            "sentiment_cohen_kappa": overall_sent["pairwise_cohen_kappa"][f"{a}_vs_{b}"],
            "mixed_raw_agreement": overall_mixed["pairwise_raw_agreement"][f"{a}_vs_{b}"],
            "mixed_cohen_kappa": overall_mixed["pairwise_cohen_kappa"][f"{a}_vs_{b}"],
        })
    pd.DataFrame(rows).to_csv(OUT / "pairwise_agreement_summary.csv", index=False)

    # ---------------- Overall summary CSV (one row per block, for quick manuscript tables) ----------------
    summary_rows = [
        {"block": "overall_sentiment", **{k: v for k, v in overall_sent.items()
                                           if k not in ("pairwise_raw_agreement", "pairwise_cohen_kappa", "block")}},
        {"block": "arabic_sentiment", **{k: v for k, v in by_language["arabic"].items()
                                          if k not in ("pairwise_raw_agreement", "pairwise_cohen_kappa", "block")}},
        {"block": "english_sentiment", **{k: v for k, v in by_language["english"].items()
                                           if k not in ("pairwise_raw_agreement", "pairwise_cohen_kappa", "block")}},
        {"block": "overall_mixed_flag", **{k: v for k, v in overall_mixed.items()
                                            if k not in ("pairwise_raw_agreement", "pairwise_cohen_kappa", "block")}},
    ]
    pd.DataFrame(summary_rows).to_csv(OUT / "summary_all_blocks.csv", index=False)

    print(f"\nAll outputs written to {OUT}")
    return {
        "overall_sentiment": overall_sent, "by_language": by_language,
        "disagreement_structure": disagreement_structure, "mixed": mixed_block, "confidence": conf_block,
    }


if __name__ == "__main__":
    main()
