"""
Phase 2.5 step 1: rebuild the three primary sources with STABLE review_id,
word-count, and group/category metadata needed for matching, dedup-safe
splitting, and the manual code-switch audit. Supersedes build_corpus_stats.py's
combined_usable_corpus.csv (which had no stable IDs).

Outputs (data/processed/):
  - arabic_tourism_v2.csv       (primary Arabic pool, human-annotated, 3-class)
  - arabic_jordan_v2.csv        (auxiliary Arabic pool, LLM-weak + human-gold, binary)
  - english_ucsd_v2.csv         (English pool, rating-derived, with category + gmap_id)
  - combined_usable_v2.csv      (all three, stable schema)
  - mixed_candidates_v2.csv     (the script-heuristic "mixed" rows, for manual audit)
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
PROCESSED.mkdir(parents=True, exist_ok=True)

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
    return df, before - len(df)


def word_count(text: str) -> int:
    return len(str(text).split())


def script_group(text: str) -> str:
    s = str(text)
    ar_chars = len(ARABIC_RANGE.findall(s))
    la_chars = len(LATIN_RANGE.findall(s))
    total = ar_chars + la_chars
    if total < 10:
        return "ambiguous_short"
    ar_frac = ar_chars / total
    la_frac = la_chars / total
    if ar_frac >= 0.9:
        return "arabic_only"
    if la_frac >= 0.9:
        return "english_only"
    if ar_frac >= 0.1 and la_frac >= 0.1:
        return "mixed_arabic_english"
    return "arabic_only" if ar_frac > la_frac else "english_only"


# ---------------------------------------------------------------------------
# 1. Arabic tourism (Zenodo 17011574) -- PRIMARY Arabic pool
# ---------------------------------------------------------------------------
print("=== Arabic tourism (primary) ===")
df_t = pd.read_excel(RAW / "arabic_tourism_17011574" / "golden_data_set_processed_google_reviews-2.xlsx")
TEXT_COL_T = "processed_reviews"
OVERALL_COL = "التجربة بشكل عام_golden"
OTHER_ASPECTS = [c for c in df_t.columns if c.endswith("_golden") and c != OVERALL_COL]
PLACE_COL = "اسم المكان"


def doc_label(row):
    if pd.notna(row[OVERALL_COL]):
        return row[OVERALL_COL]
    vals = [row[c] for c in OTHER_ASPECTS if pd.notna(row[c])]
    if not vals:
        return None
    s = sum(vals)
    return 1.0 if s > 0 else (-1.0 if s < 0 else 0.0)


df_t["doc_label_raw"] = df_t.apply(doc_label, axis=1)
df_t = df_t.reset_index(drop=True)
df_t["review_id"] = ["AR-TOUR-%05d" % i for i in range(len(df_t))]
usable_t = df_t[df_t["doc_label_raw"].notna() & df_t[TEXT_COL_T].notna() & (df_t[TEXT_COL_T].str.strip() != "")].copy()
label_map = {1.0: "Positive", 0.0: "Neutral", -1.0: "Negative"}
usable_t["sentiment"] = usable_t["doc_label_raw"].map(label_map)
usable_t["label_source"] = "human_annotated"
usable_t["language_group_src"] = "arabic_primary"
usable_t["group_id"] = usable_t[PLACE_COL]
usable_t["rating"] = pd.NA
usable_t["category"] = usable_t["الفئة"] if "الفئة" in usable_t.columns else pd.NA
usable_t["word_count"] = usable_t[TEXT_COL_T].map(word_count)
usable_t = usable_t.rename(columns={TEXT_COL_T: "text"})[
    ["review_id", "text", "sentiment", "label_source", "language_group_src", "group_id", "rating", "category", "word_count"]]
usable_t, dup_t = dedup(usable_t, "text")
print(f"usable={len(usable_t)} dedup_removed={dup_t}")

# ---------------------------------------------------------------------------
# 2. Jordanian-Arabic restaurant (Zenodo 22061934) -- AUXILIARY Arabic pool
# ---------------------------------------------------------------------------
print("\n=== Jordan restaurant (auxiliary) ===")
df_j = pd.read_csv(RAW / "arabic_jordan_restaurant_22061934" / "full_annotated_dataset_8671.csv")
df_gold = pd.read_csv(RAW / "arabic_jordan_restaurant_22061934" / "gold_standard_300_v2.csv")
gold_ids = set(df_gold["review_id"])

usable_j = df_j[df_j["text"].notna() & (df_j["text"].str.strip() != "") & df_j["Sentiment"].notna()].copy()
usable_j["review_id"] = usable_j["review_id"].map(lambda i: f"AR-JOR-{i:05d}")
usable_j["sentiment"] = usable_j["Sentiment"]
usable_j["label_source"] = df_j.loc[usable_j.index, "review_id"].map(lambda i: "human_annotated" if i in gold_ids else "llm_weak_label")
usable_j["language_group_src"] = "arabic_auxiliary"
usable_j["group_id"] = pd.NA  # no business/place identifier available in this release
usable_j["rating"] = pd.NA
usable_j["category"] = usable_j["Aspect"]
usable_j["word_count"] = usable_j["text"].map(word_count)
usable_j = usable_j[["review_id", "text", "sentiment", "label_source", "language_group_src", "group_id", "rating", "category", "word_count"]]
usable_j, dup_j = dedup(usable_j, "text")
print(f"usable={len(usable_j)} dedup_removed={dup_j} (NOTE: binary only, zero Neutral, confirmed)")

# ---------------------------------------------------------------------------
# 3. English UCSD/McAuley (Wyoming + Vermont) -- with category + gmap_id
# ---------------------------------------------------------------------------
print("\n=== English UCSD/McAuley (Wyoming+Vermont) ===")


def rating_to_sentiment(r):
    if r in (1, 2):
        return "Negative"
    if r == 3:
        return "Neutral"
    if r in (4, 5):
        return "Positive"
    return None


# load metadata: gmap_id -> category list
meta = {}
for state_file in ["meta-Wyoming.json.gz", "meta-Vermont.json.gz"]:
    path = RAW / "english_ucsd_googlelocal" / state_file
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            meta[d.get("gmap_id")] = d.get("category") or []

rows = []
for state_abbr, state_file in [("WY", "review-Wyoming.json.gz"), ("VT", "review-Vermont.json.gz")]:
    path = RAW / "english_ucsd_googlelocal" / state_file
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for i, line in enumerate(f):
            d = json.loads(line)
            text = d.get("text")
            rating = d.get("rating")
            if text and str(text).strip() and rating is not None:
                gmap_id = d.get("gmap_id")
                rows.append({
                    "review_id": f"EN-{state_abbr}-{i:07d}",
                    "text": text,
                    "sentiment": rating_to_sentiment(rating),
                    "label_source": "rating_derived",
                    "language_group_src": "english",
                    "group_id": gmap_id,
                    "rating": rating,
                    "category": ";".join(meta.get(gmap_id, []) or []),
                    "word_count": word_count(text),
                })

df_e = pd.DataFrame(rows)
usable_e = df_e[df_e["sentiment"].notna()].copy()
usable_e, dup_e = dedup(usable_e, "text")
print(f"usable={len(usable_e)} dedup_removed={dup_e}")

# ---------------------------------------------------------------------------
# 4. Script-group classification + save
# ---------------------------------------------------------------------------
combined = pd.concat([usable_t, usable_j, usable_e], ignore_index=True)
combined["script_group"] = combined["text"].map(script_group)

usable_t.to_csv(PROCESSED / "arabic_tourism_v2.csv", index=False, encoding="utf-8-sig")
usable_j.to_csv(PROCESSED / "arabic_jordan_v2.csv", index=False, encoding="utf-8-sig")
usable_e.to_csv(PROCESSED / "english_ucsd_v2.csv", index=False, encoding="utf-8-sig")
combined.to_csv(PROCESSED / "combined_usable_v2.csv", index=False, encoding="utf-8-sig")

mixed = combined[combined["script_group"] == "mixed_arabic_english"][
    ["review_id", "text", "sentiment", "label_source", "language_group_src", "script_group"]]
mixed.to_csv(PROCESSED / "mixed_candidates_v2.csv", index=False, encoding="utf-8-sig")

print(f"\nTotals: arabic_primary={len(usable_t)} arabic_auxiliary={len(usable_j)} english={len(usable_e)}")
print(f"mixed candidates for manual audit: {len(mixed)}")
print(f"English rows with resolved category metadata: {(combined.loc[combined.language_group_src=='english','category']!='').sum()} / {len(usable_e)}")
