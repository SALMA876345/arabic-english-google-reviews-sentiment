"""
Analysis of the adjudication process itself (not model evaluation, not a
validity claim about which side was "right"). Read-only, uses
adjudication_merged.csv. Reports:
  - for the 161 majority cases: adjudicator agreement/disagreement with the
    2/3 majority_label, overall, by language, and by majority class
  - for the 18 three-way cases: the adjudicator's selected class distribution
  - adjudicator confidence distribution overall and by language
"""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent

merged = pd.read_csv(HERE / "adjudication_merged.csv")
assert len(merged) == 179

majority = merged[merged.agreement_type == "majority"].copy()
threeway = merged[merged.agreement_type == "disagreement"].copy()
assert len(majority) == 161, f"Expected 161 majority cases, found {len(majority)}"
assert len(threeway) == 18, f"Expected 18 three-way cases, found {len(threeway)}"

print("=" * 70)
print(f"MAJORITY CASES (n={len(majority)})")
print("=" * 70)

agree = (majority.adjudicated_sentiment == majority.majority_label)
n_agree = agree.sum()
n_disagree = len(majority) - n_agree
print(f"Adjudicator agrees with 2/3 majority: {n_agree}/{len(majority)} ({n_agree/len(majority)*100:.1f}%)")
print(f"Adjudicator disagrees with 2/3 majority: {n_disagree}/{len(majority)} ({n_disagree/len(majority)*100:.1f}%)")

print("\nBy language:")
for lang, grp in majority.groupby("language"):
    a = (grp.adjudicated_sentiment == grp.majority_label).sum()
    print(f"  {lang}: agree {a}/{len(grp)} ({a/len(grp)*100:.1f}%), disagree {len(grp)-a}/{len(grp)} ({(len(grp)-a)/len(grp)*100:.1f}%)")

print("\nBy majority class:")
for cls, grp in majority.groupby("majority_label"):
    a = (grp.adjudicated_sentiment == grp.majority_label).sum()
    print(f"  majority_label={cls}: agree {a}/{len(grp)} ({a/len(grp)*100:.1f}%), disagree {len(grp)-a}/{len(grp)} ({(len(grp)-a)/len(grp)*100:.1f}%)")

print("\nWhen adjudicator disagrees with majority, what did they choose instead?")
dis = majority[~agree]
print(pd.crosstab(dis.majority_label, dis.adjudicated_sentiment).to_string())

print()
print("=" * 70)
print(f"THREE-WAY DISAGREEMENT CASES (n={len(threeway)})")
print("=" * 70)
print("Adjudicator's selected class distribution (no majority existed to compare against):")
print(threeway.adjudicated_sentiment.value_counts().to_string())
print("\nBy language:")
print(pd.crosstab(threeway.language, threeway.adjudicated_sentiment).to_string())

print()
print("=" * 70)
print("ADJUDICATOR CONFIDENCE (all 179 cases; NOT a correctness measure)")
print("=" * 70)
print("Overall:")
print(merged.adjudication_confidence.value_counts().to_string())
print("\nBy language:")
print(pd.crosstab(merged.language, merged.adjudication_confidence).to_string())
print("\nBy case type (majority vs three-way):")
print(pd.crosstab(merged.agreement_type, merged.adjudication_confidence).to_string())
