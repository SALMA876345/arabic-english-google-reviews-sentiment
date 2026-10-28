"""
Section F of the Human-Gold label analysis phase.

For model pairs with valid row-level predictions, evaluated on the SAME
Human-Gold examples (369 Arabic or 388 English), compute:
  (1) a paired bootstrap 95% CI for the Macro-F1 difference (resampling
      test ROWS with replacement) -- same family of method as before,
      but now n_iterations=10000 and run against Human-Gold labels.
  (2) a genuine paired permutation/randomization test: for each of
      n_iterations draws, independently (Bernoulli p=0.5) swap each row's
      (pred_A, pred_B) assignment between "slot A" and "slot B" while
      holding the true (Human-Gold) label fixed, recompute the Macro-F1
      difference under the swapped assignment, and build a null
      distribution. p = (#{|null_diff| >= |observed_diff|} + 1) / (n_iter + 1).
      This is NOT the same statistic as (1) -- it directly tests
      exchangeability of which model produced which prediction, which is
      what a permutation test for paired classifier comparison requires;
      the bootstrap in (1) is a resampling-based CI/heuristic-p and must
      not be described as a permutation test.
Families (each gets its own Holm-Bonferroni correction, mirroring the
pairing structure of the pre-Human-Gold significance_tests.json /
phase3b *_paired_bootstrap_holm_results.csv so the before/after comparison
is apples-to-apples):
  - Phase3A_Arabic_E1 (laptop/LoRA): xlmr, marbert, tfidf_logreg, tfidf_svm
  - Phase3A_English_E2 (laptop/LoRA): xlmr, tfidf_logreg, tfidf_svm
  - Phase3B_Arabic (GPU full-FT): xlmr_rerun, marbert_rerun, multilingual, zeroshot_en_to_ar
  - Phase3B_English (GPU full-FT): xlmr, multilingual, zeroshot_ar_to_en
"""
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))
from evaluation.metrics import holm_bonferroni, LABEL_ORDER  # noqa: E402

OUT = Path(__file__).resolve().parent
STORE = OUT / "model_predictions_vs_human_gold"
SEED = 42
N_ITER = 10000

FAMILIES = {
    "Phase3A_Arabic_E1": ["E1_xlmr_lora", "E1_marbert_lora", "E1_tfidf_logreg", "E1_tfidf_svm"],
    "Phase3A_English_E2": ["E2_xlmr_lora", "E2_tfidf_logreg", "E2_tfidf_svm"],
    "Phase3B_Arabic": ["E1_xlmr_fullft", "E1_marbert_fullft", "E4_multilingual_xlmr_arabic", "E5B_zeroshot_en_to_ar"],
    "Phase3B_English": ["E2_xlmr_fullft", "E4_multilingual_xlmr_english", "E5A_zeroshot_ar_to_en"],
}


def macro_f1(y_true, y_pred):
    _, _, f1, _ = precision_recall_fscore_support(y_true, y_pred, labels=LABEL_ORDER, average="macro", zero_division=0)
    return f1


def load_pair(key_a, key_b):
    df_a = pd.read_csv(STORE / f"{key_a}.csv")
    df_b = pd.read_csv(STORE / f"{key_b}.csv")
    merged = df_a.merge(df_b, on="review_id", suffixes=("_a", "_b"), validate="one_to_one")
    assert len(merged) == len(df_a) == len(df_b), f"{key_a} vs {key_b}: row count mismatch after merge"
    assert (merged.human_gold_sentiment_a == merged.human_gold_sentiment_b).all(), \
        f"{key_a} vs {key_b}: Human-Gold labels disagree after merge -- different id sets?"
    y_true = merged["human_gold_sentiment_a"].to_numpy()
    pa = merged["pred_a"].to_numpy()
    pb = merged["pred_b"].to_numpy()
    return y_true, pa, pb


def paired_bootstrap_ci(y_true, pa, pb, seed, n_iter):
    rng = np.random.default_rng(seed)
    n = len(y_true)
    observed = macro_f1(y_true, pa) - macro_f1(y_true, pb)
    diffs = np.empty(n_iter)
    for i in range(n_iter):
        idx = rng.integers(0, n, size=n)
        diffs[i] = macro_f1(y_true[idx], pa[idx]) - macro_f1(y_true[idx], pb[idx])
    if observed >= 0:
        p = 2 * np.mean(diffs <= 0)
    else:
        p = 2 * np.mean(diffs >= 0)
    p = min(float(p), 1.0)
    return {
        "observed_diff_macro_f1": float(observed),
        "ci_lower_2.5": float(np.percentile(diffs, 2.5)),
        "ci_upper_97.5": float(np.percentile(diffs, 97.5)),
        "bootstrap_resampling_p_heuristic": p,
        "n_iterations": n_iter, "seed": seed, "n": n,
    }


def paired_permutation_test(y_true, pa, pb, seed, n_iter):
    rng = np.random.default_rng(seed)
    n = len(y_true)
    observed = macro_f1(y_true, pa) - macro_f1(y_true, pb)
    null_diffs = np.empty(n_iter)
    for i in range(n_iter):
        swap = rng.random(n) < 0.5
        perm_a = np.where(swap, pb, pa)
        perm_b = np.where(swap, pa, pb)
        null_diffs[i] = macro_f1(y_true, perm_a) - macro_f1(y_true, perm_b)
    p_exact = (np.sum(np.abs(null_diffs) >= abs(observed)) + 1) / (n_iter + 1)
    return {
        "observed_diff_macro_f1": float(observed),
        "permutation_p_two_sided": float(p_exact),
        "n_iterations": n_iter, "seed": seed, "n": n,
        "null_distribution_mean": float(np.mean(null_diffs)),
        "null_distribution_std": float(np.std(null_diffs)),
    }


def main():
    all_rows = []
    for family, keys in FAMILIES.items():
        family_rows = []
        for key_a, key_b in itertools.combinations(keys, 2):
            y_true, pa, pb = load_pair(key_a, key_b)
            boot = paired_bootstrap_ci(y_true, pa, pb, SEED, N_ITER)
            perm = paired_permutation_test(y_true, pa, pb, SEED, N_ITER)
            family_rows.append({
                "family": family, "model_a": key_a, "model_b": key_b,
                "macro_f1_a": float(macro_f1(y_true, pa)), "macro_f1_b": float(macro_f1(y_true, pb)),
                **boot,
                "permutation_p_two_sided": perm["permutation_p_two_sided"],
                "permutation_n_iterations": perm["n_iterations"],
                "permutation_null_mean": perm["null_distribution_mean"],
                "permutation_null_std": perm["null_distribution_std"],
            })
        # Holm correction per family, applied separately to the bootstrap-heuristic p and to the permutation p
        raw_boot_p = [r["bootstrap_resampling_p_heuristic"] for r in family_rows]
        raw_perm_p = [r["permutation_p_two_sided"] for r in family_rows]
        adj_boot = holm_bonferroni(raw_boot_p)
        adj_perm = holm_bonferroni(raw_perm_p)
        for r, ab, ap in zip(family_rows, adj_boot, adj_perm):
            r["bootstrap_p_holm_adjusted"] = ab
            r["permutation_p_holm_adjusted"] = ap
            r["significant_permutation_holm_0.05"] = ap < 0.05
        all_rows.extend(family_rows)

    out_df = pd.DataFrame(all_rows)
    out_df.to_csv(OUT / "statistical_tests_human_gold.csv", index=False)
    with open(OUT / "statistical_tests_human_gold.json", "w", encoding="utf-8") as f:
        json.dump(all_rows, f, indent=2, default=str)

    cols = ["family", "model_a", "model_b", "macro_f1_a", "macro_f1_b", "observed_diff_macro_f1",
            "ci_lower_2.5", "ci_upper_97.5", "bootstrap_p_holm_adjusted",
            "permutation_p_two_sided", "permutation_p_holm_adjusted", "significant_permutation_holm_0.05"]
    print(out_df[cols].to_string(index=False))
    print(f"\nWrote statistical_tests_human_gold.csv/.json "
          f"({len(out_df)} pairwise comparisons across {len(FAMILIES)} families, "
          f"seed={SEED}, n_iterations={N_ITER} for both the bootstrap CI and the permutation test).")


if __name__ == "__main__":
    main()
