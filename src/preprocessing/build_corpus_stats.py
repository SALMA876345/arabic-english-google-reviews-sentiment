"""
Phase 2 step 1: load the three primary raw sources, apply the documented
label-derivation rules from docs/methodology_plan.md, and compute real
summary statistics (no placeholders). Writes:
  - data/processed/arabic_tourism.csv
  - data/processed/arabic_jordan_restaurant.csv
  - data/processed/english_ucsd_sample.csv
  - results/tables/phase2_corpus_stats.md
"""
import gzip
import json
import re
import hashlib
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "results" / "tables"
PROCESSED.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)

SEED = 42  # project-wide seed, see configs/

ARABIC_RANGE = re.compile(r"[؀-ۿݐ-ݿ]")
LATIN_RANGE = re.compile(r"[A-Za-z]")


def normalize_for_dedup(text: str) -> str:
    t = str(text).strip().lower()
    t = re.sub(r"\s+", " ", t)
    return t


def dedup(df: pd.DataFrame, text_col: str):
    norm = df[text_col].map(normalize_for_dedup)
    h = norm.map(lambda s: hashlib.md5(s.encode("utf-8")).hexdigest())
    before = len(df)
    df = df.loc[~h.duplicated(keep="first")].copy()
    removed = before - len(df)
    return df, removed


def script_group(text: str) -> str:
    """CMI-style heuristic script classification (methodology_plan.md S4-5).
    Not a definitive linguistic classifier -- a first-pass heuristic."""
    s = str(text)
    ar_chars = len(ARABIC_RANGE.findall(s))
    la_chars = len(LATIN_RANGE.findall(s))
    total = ar_chars + la_chars
    if total < 10:
        # too little alphabetic signal to classify confidently
        return "ambiguous_short"
    ar_frac = ar_chars / total
    la_frac = la_chars / total
    if ar_frac >= 0.9:
        return "arabic_only"
    if la_frac >= 0.9:
        return "english_only"
    if ar_frac >= 0.1 and la_frac >= 0.1:
        return "mixed_arabic_english"
    # dominated by one script but with a small trace of the other
    return "arabic_only" if ar_frac > la_frac else "english_only"


# ---------------------------------------------------------------------------
# 1. Arabic tourism (Zenodo 17011574) -- aspect-level -> document-level
# ---------------------------------------------------------------------------
print("=== Arabic tourism (Zenodo 17011574) ===")
tourism_path = RAW / "arabic_tourism_17011574" / "golden_data_set_processed_google_reviews-2.xlsx"
df_t = pd.read_excel(tourism_path)
TEXT_COL_T = "processed_reviews"
OVERALL_COL = "التجربة بشكل عام_golden"
OTHER_ASPECTS = [c for c in df_t.columns if c.endswith("_golden") and c != OVERALL_COL]

raw_t = len(df_t)


def doc_label(row):
    if pd.notna(row[OVERALL_COL]):
        return row[OVERALL_COL]
    vals = [row[c] for c in OTHER_ASPECTS if pd.notna(row[c])]
    if not vals:
        return None
    s = sum(vals)
    if s > 0:
        return 1.0
    if s < 0:
        return -1.0
    return 0.0  # exact tie -> neutral, documented fallback rule


df_t["doc_label_raw"] = df_t.apply(doc_label, axis=1)
usable_t = df_t[df_t["doc_label_raw"].notna() & df_t[TEXT_COL_T].notna() & (df_t[TEXT_COL_T].str.strip() != "")].copy()
label_map = {1.0: "Positive", 0.0: "Neutral", -1.0: "Negative"}
usable_t["sentiment"] = usable_t["doc_label_raw"].map(label_map)
usable_t["label_source"] = "human_annotated"
usable_t["language_group_src"] = "arabic"
usable_t = usable_t.rename(columns={TEXT_COL_T: "text"})[["text", "sentiment", "label_source", "language_group_src"]]
usable_t, dup_t = dedup(usable_t, "text")
print(f"raw={raw_t} usable={len(usable_t)} dropped_no_label={raw_t - len(df_t[df_t['doc_label_raw'].notna()])} dedup_removed={dup_t}")

# ---------------------------------------------------------------------------
# 2. Jordanian-Arabic restaurant (Zenodo 22061934) -- binary Pos/Neg, no Neutral
# ---------------------------------------------------------------------------
print("\n=== Jordanian-Arabic restaurant (Zenodo 22061934) ===")
jordan_path = RAW / "arabic_jordan_restaurant_22061934" / "full_annotated_dataset_8671.csv"
gold_path = RAW / "arabic_jordan_restaurant_22061934" / "gold_standard_300_v2.csv"
df_j = pd.read_csv(jordan_path)
df_gold = pd.read_csv(gold_path)
gold_ids = set(df_gold["review_id"])

raw_j = len(df_j)
usable_j = df_j[df_j["text"].notna() & (df_j["text"].str.strip() != "") & df_j["Sentiment"].notna()].copy()
usable_j["sentiment"] = usable_j["Sentiment"]
usable_j["label_source"] = usable_j["review_id"].map(lambda i: "human_annotated" if i in gold_ids else "llm_weak_label")
usable_j["language_group_src"] = "arabic"
usable_j = usable_j.rename(columns={})[["text", "sentiment", "label_source", "language_group_src"]]
usable_j, dup_j = dedup(usable_j, "text")
print(f"raw={raw_j} usable={len(usable_j)} dedup_removed={dup_j}")
print("Sentiment classes present:", sorted(usable_j['sentiment'].unique()), "-- NOTE: this source has NO Neutral class at all")

# ---------------------------------------------------------------------------
# 3. English UCSD/McAuley Google Local -- Wyoming + Vermont, rating-derived
# ---------------------------------------------------------------------------
print("\n=== English UCSD/McAuley Google Local (Wyoming + Vermont) ===")


def rating_to_sentiment(r):
    if r in (1, 2):
        return "Negative"
    if r == 3:
        return "Neutral"
    if r in (4, 5):
        return "Positive"
    return None


rows = []
raw_e = 0
for state_file in ["review-Wyoming.json.gz", "review-Vermont.json.gz"]:
    path = RAW / "english_ucsd_googlelocal" / state_file
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            raw_e += 1
            d = json.loads(line)
            text = d.get("text")
            rating = d.get("rating")
            if text and str(text).strip() and rating is not None:
                rows.append({"text": text, "sentiment": rating_to_sentiment(rating),
                             "label_source": "rating_derived", "language_group_src": "english"})

df_e = pd.DataFrame(rows)
usable_e = df_e[df_e["sentiment"].notna()].copy()
usable_e, dup_e = dedup(usable_e, "text")
print(f"raw={raw_e} usable_with_text_and_rating={len(df_e)} after_dedup={len(usable_e)} dedup_removed={dup_e}")

# ---------------------------------------------------------------------------
# 4. Combine and compute final stats
# ---------------------------------------------------------------------------
print("\n=== Combined corpus ===")
combined = pd.concat([usable_t, usable_j, usable_e], ignore_index=True)
combined["script_group"] = combined["text"].map(script_group)

n_total = len(combined)
sentiment_pct = (combined["sentiment"].value_counts(normalize=True) * 100).round(1)
label_source_pct = (combined["label_source"].value_counts(normalize=True) * 100).round(1)
script_counts = combined["script_group"].value_counts()

arabic_raw_total = raw_t + raw_j
arabic_usable_total = len(usable_t) + len(usable_j)
english_raw_total = raw_e
english_usable_total = len(usable_e)
dedup_total = dup_t + dup_j + dup_e
mixed_count = int(script_counts.get("mixed_arabic_english", 0))

summary_lines = []
summary_lines.append(f"Arabic raw:                 {arabic_raw_total:,}")
summary_lines.append(f"Arabic usable:              {arabic_usable_total:,}")
summary_lines.append("")
summary_lines.append(f"English raw:                {english_raw_total:,}")
summary_lines.append(f"English usable:             {english_usable_total:,}")
summary_lines.append("")
summary_lines.append(f"Arabic-English mixed:       {mixed_count:,}")
summary_lines.append("")
for cls in ["Positive", "Neutral", "Negative"]:
    pct = sentiment_pct.get(cls, 0.0)
    summary_lines.append(f"{cls}:" + " " * (29 - len(cls) - 1) + f"{pct:.1f}%")
summary_lines.append("")
label_name_map = {"human_annotated": "Human labels", "rating_derived": "Rating-derived", "llm_weak_label": "LLM weak labels"}
for key, name in label_name_map.items():
    pct = label_source_pct.get(key, 0.0)
    summary_lines.append(f"{name}:" + " " * (29 - len(name) - 1) + f"{pct:.1f}%")
summary_lines.append("")
summary_lines.append(f"Duplicates removed:         {dedup_total:,}")

print("\n".join(summary_lines))

# Save processed data
usable_t.to_csv(PROCESSED / "arabic_tourism.csv", index=False, encoding="utf-8-sig")
usable_j.to_csv(PROCESSED / "arabic_jordan_restaurant.csv", index=False, encoding="utf-8-sig")
usable_e.to_csv(PROCESSED / "english_ucsd_sample.csv", index=False, encoding="utf-8-sig")
combined.to_csv(PROCESSED / "combined_usable_corpus.csv", index=False, encoding="utf-8-sig")

# Save table + full breakdown
with open(TABLES / "phase2_corpus_stats.md", "w", encoding="utf-8") as f:
    f.write("# Phase 2 Corpus Statistics (real, computed from downloaded data)\n\n")
    f.write("```\n" + "\n".join(summary_lines) + "\n```\n\n")
    f.write("## Per-source breakdown\n\n")
    f.write(f"- Arabic tourism (Zenodo 17011574): raw={raw_t}, usable={len(usable_t)}, "
            f"dropped (no derivable label)={raw_t - len(df_t[df_t['doc_label_raw'].notna()])}, "
            f"dedup_removed={dup_t}, label_source=human_annotated (kappa=0.87)\n")
    f.write(f"- Jordan restaurant (Zenodo 22061934): raw={raw_j}, usable={len(usable_j)}, "
            f"dedup_removed={dup_j}, label_source=300 human_annotated (gold) + "
            f"{len(usable_j) - usable_j['label_source'].eq('human_annotated').sum()} llm_weak_label. "
            f"**No Neutral class exists in this source** (binary Positive/Negative only, confirmed by direct inspection).\n")
    f.write(f"- English UCSD/McAuley (Wyoming+Vermont subset): raw_lines={raw_e}, "
            f"usable (non-null text + rating)={len(df_e)}, after_dedup={len(usable_e)}, "
            f"dedup_removed={dup_e}, label_source=rating_derived (1-2=Neg,3=Neu,4-5=Pos), "
            f"**not human-validated against a gold sample in this pass -- see known_limitations.md**\n\n")
    f.write("## Script-group distribution (CMI-style heuristic, methodology_plan.md S4-5)\n\n")
    f.write(script_counts.to_frame("count").to_string() + "\n\n")
    f.write("## Sentiment class distribution (combined corpus)\n\n")
    f.write(sentiment_pct.to_frame("pct").to_string() + "\n\n")
    f.write("## Label-source distribution (combined corpus)\n\n")
    f.write(label_source_pct.to_frame("pct").to_string() + "\n")

print(f"\nWrote results/tables/phase2_corpus_stats.md and data/processed/*.csv")
