"""
Phase 2.5 step 2: build a MATCHED English subset comparable to the Arabic
PRIMARY pool (tourism, human-annotated, 3-class, N=3525) -- not the full
1,038,643-review English pool, and not the combined 12,189 Arabic figure
(which would silently blend in the Jordan auxiliary binary/LLM-weak data).
See docs/decisions.md D10 for why the matching target is 3,525, not 12,189.

Matching applied on:
  - sample count (exactly 3,525, matching the Arabic primary pool)
  - sentiment distribution (stratified to the Arabic primary pool's %)
  - review-length distribution (stratified within each sentiment stratum,
    by quartile bin of word_count, to the Arabic primary pool's %)
  - domain (restricted to a tourism/park/museum/historical-site category
    filter -- the closest available proxy for the Arabic tourism domain)

NOT matched (documented, not silently ignored):
  - geography (English=Wyoming/Vermont, Arabic=Saudi Arabia -- UCSD/McAuley
    2021 release has no Middle East/Gulf coverage, confirmed in Phase 2)
  - star-rating distribution (the Arabic primary pool has no star ratings
    to compare against -- it is aspect-sentiment annotated, not rating-based)
"""
import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "results" / "tables"
SEED = 42

ar = pd.read_csv(PROCESSED / "arabic_tourism_v2.csv")
en = pd.read_csv(PROCESSED / "english_ucsd_v2.csv")

TOURISM_KEYWORDS = ["tourist attraction", "park", "museum", "historical", "monument",
                    "heritage", "memorial", "landmark", "garden", "recreation"]
domain_mask = en["category"].str.lower().apply(
    lambda s: any(k in s for k in TOURISM_KEYWORDS) if isinstance(s, str) else False)
en_domain = en[domain_mask].copy()
print(f"English domain-filtered pool (tourism/park/museum/historical proxy): {len(en_domain)} "
      f"of {len(en)} total usable English rows")

# Target sentiment distribution = Arabic primary pool's actual distribution
target_n = len(ar)  # 3525
sent_dist = ar["sentiment"].value_counts(normalize=True)
target_counts = (sent_dist * target_n).round().astype(int)
# fix rounding drift so counts sum exactly to target_n
drift = target_n - target_counts.sum()
target_counts.iloc[0] += drift
print("Target per-class counts (matching Arabic primary pool):")
print(target_counts)

# length-quartile bins from the Arabic primary pool (shared bin edges)
_, bin_edges = pd.qcut(ar["word_count"], q=4, retbins=True, duplicates="drop")
bin_edges = bin_edges.copy()
bin_edges[0] = -np.inf
bin_edges[-1] = np.inf

rng = np.random.default_rng(SEED)
sampled_parts = []
shortfall_log = []

for cls, n_target in target_counts.items():
    ar_cls = ar[ar["sentiment"] == cls].copy()
    ar_cls["len_bin"] = pd.cut(ar_cls["word_count"], bins=bin_edges, labels=False)
    bin_props = ar_cls["len_bin"].value_counts(normalize=True).sort_index()

    en_cls = en_domain[en_domain["sentiment"] == cls].copy()
    en_cls["len_bin"] = pd.cut(en_cls["word_count"], bins=bin_edges, labels=False)

    chosen = []
    for b, prop in bin_props.items():
        n_bin_target = int(round(prop * n_target))
        avail = en_cls[en_cls["len_bin"] == b]
        n_take = min(n_bin_target, len(avail))
        if n_take < n_bin_target:
            shortfall_log.append((cls, b, n_bin_target, len(avail)))
        if n_take > 0:
            chosen.append(avail.sample(n=n_take, random_state=SEED))
    sampled = pd.concat(chosen, ignore_index=True) if chosen else pd.DataFrame(columns=en_cls.columns)
    # top up/trim to hit exact target count for this class
    if len(sampled) < n_target:
        remaining_pool = en_cls.drop(index=sampled.index, errors="ignore")
        remaining_pool = en_cls[~en_cls["review_id"].isin(sampled.get("review_id", []))]
        extra_needed = n_target - len(sampled)
        if len(remaining_pool) >= extra_needed:
            extra = remaining_pool.sample(n=extra_needed, random_state=SEED)
            sampled = pd.concat([sampled, extra], ignore_index=True)
        else:
            shortfall_log.append((cls, "TOTAL", n_target, len(sampled) + len(remaining_pool)))
            sampled = pd.concat([sampled, remaining_pool], ignore_index=True)
    elif len(sampled) > n_target:
        sampled = sampled.sample(n=n_target, random_state=SEED)
    sampled_parts.append(sampled.drop(columns=["len_bin"], errors="ignore"))

matched_en = pd.concat(sampled_parts, ignore_index=True)
print(f"\nFinal matched English subset size: {len(matched_en)} (target {target_n})")
if shortfall_log:
    print("Shortfalls encountered (bin had fewer available rows than requested):")
    for s in shortfall_log:
        print("  ", s)

matched_en.to_csv(PROCESSED / "english_matched_v1.csv", index=False, encoding="utf-8-sig")

# Comparison report
report = []
report.append("# Arabic Primary vs. Matched English Subset -- Comparability Report\n")
report.append(f"Arabic primary pool (Zenodo 17011574): N={len(ar)}\n")
report.append(f"Matched English subset: N={len(matched_en)}\n\n")
report.append("## Sentiment distribution\n\n")
comp = pd.DataFrame({
    "Arabic_primary_%": (ar["sentiment"].value_counts(normalize=True) * 100).round(1),
    "English_matched_%": (matched_en["sentiment"].value_counts(normalize=True) * 100).round(1),
})
report.append(comp.to_string() + "\n\n")
report.append("## Review-length (word count) distribution\n\n")
len_comp = pd.DataFrame({
    "Arabic_primary": ar["word_count"].describe(),
    "English_matched": matched_en["word_count"].describe(),
})
report.append(len_comp.to_string() + "\n\n")
report.append("## NOT matched (documented limitation, not an oversight)\n\n")
report.append("- Geography: English=Wyoming/Vermont (US); Arabic=Saudi Arabia (tourism sites). "
              "UCSD/McAuley 2021 release has no Middle East/Gulf coverage -- confirmed during Phase 2.\n")
report.append("- Star-rating distribution: the Arabic primary pool has no star ratings at all "
              "(aspect-sentiment annotated, not rating-based), so there is nothing to match the "
              "English matched subset's rating distribution against. The English matched subset's "
              "own rating distribution is reported below for transparency.\n\n")
report.append("## English matched subset's own rating distribution (for reference, not matched against anything)\n\n")
report.append(matched_en["rating"].value_counts(normalize=True).sort_index().mul(100).round(1).to_string() + "\n")

with open(TABLES / "arabic_vs_matched_english_comparability.md", "w", encoding="utf-8") as f:
    f.write("".join(report))

print("\nWrote data/processed/english_matched_v1.csv and "
      "results/tables/arabic_vs_matched_english_comparability.md")
