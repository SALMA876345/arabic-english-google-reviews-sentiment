"""
Phase 3 error analysis, step 1 (extraction, not judgment): pulls every
misclassified test-set row for a given run, joins back the source data for
context (word_count, rating if available, script_group), and computes
cheap heuristic SIGNAL flags that a human/agent reviewer then uses to
assign real linguistic categories. This script does NOT itself assign
final error categories -- it only prepares the systematic review candidate
set so no cases are cherry-picked (every error row is included).

Usage:
  python scripts/error_analysis.py --run_id run_E1_tfidf_svm_001 --out E1_svm
  python scripts/error_analysis.py --run_id E1_xlmr --out E1_xlmr
"""
import argparse
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.utils.data_io import load_arabic_tourism, load_english_matched

ROOT = Path(__file__).resolve().parents[1]
PRED_DIR = ROOT / "results" / "predictions"
ERROR_DIR = ROOT / "results" / "error_analysis"
ERROR_DIR.mkdir(parents=True, exist_ok=True)

ARABIC_RANGE = re.compile(r"[؀-ۿݐ-ݿ]")
LATIN_RANGE = re.compile(r"[A-Za-z]")
EMOJI_RANGE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]")
NEGATION_EN = re.compile(r"\b(not|no|never|n't|without|lack|isn't|wasn't|didn't|doesn't)\b", re.IGNORECASE)
NEGATION_AR = re.compile(r"(لا|ما|لم|ليس|غير|مو|مافي|ماكو)")


def script_mix_flag(text):
    s = str(text)
    ar = len(ARABIC_RANGE.findall(s))
    la = len(LATIN_RANGE.findall(s))
    total = ar + la
    if total < 10:
        return "ambiguous_short"
    if ar / total >= 0.9:
        return "arabic_only"
    if la / total >= 0.9:
        return "english_only"
    return "mixed"


def signals(text):
    s = str(text)
    return {
        "has_emoji": bool(EMOJI_RANGE.search(s)),
        "has_negation_marker": bool(NEGATION_EN.search(s) or NEGATION_AR.search(s)),
        "script_mix": script_mix_flag(s),
        "word_count": len(s.split()),
        "is_short": len(s.split()) <= 5,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_id", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    pred_files = list(PRED_DIR.glob("*_test.csv"))
    pred_df = None
    for f in pred_files:
        df = pd.read_csv(f)
        if (df["run_id"] == args.run_id).any():
            pred_df = df[df["run_id"] == args.run_id]
            break
    if pred_df is None:
        raise ValueError(f"run_id {args.run_id} not found in any prediction file")

    errors = pred_df[pred_df["correct"] == False].copy()
    language = pred_df["language"].iloc[0]
    source = load_arabic_tourism() if language == "arabic" else load_english_matched()
    errors = errors.merge(source[["review_id", "rating", "text"]], on="review_id", how="left")
    sig_df = errors["text"].apply(signals).apply(pd.Series)
    errors = pd.concat([errors.reset_index(drop=True), sig_df.reset_index(drop=True)], axis=1)

    errors["rating_text_disagreement_flag"] = errors.apply(
        lambda r: (pd.notna(r.get("rating")) and (
            (r["rating"] in (4, 5) and r["true_label"] == "Negative") or
            (r["rating"] in (1, 2) and r["true_label"] == "Positive")
        )), axis=1)

    errors["manual_category"] = ""   # to be filled by systematic review (agent/human), not auto-assigned
    errors["category_confidence"] = ""
    errors["category_notes"] = ""

    out_path = ERROR_DIR / f"error_cases_{args.out}.csv"
    errors.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"Extracted {len(errors)} error cases (of {len(pred_df)} total test rows) for run_id={args.run_id}")
    print(f"Wrote {out_path} -- manual_category column is BLANK, pending systematic review (no cherry-picking: ALL errors included)")


if __name__ == "__main__":
    main()
