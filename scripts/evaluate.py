"""
Phase 3 evaluation: reads every prediction file in results/predictions/,
recomputes all metrics directly from the row-level predictions (never from
numbers reported elsewhere), and writes:
  - results/tables/model_comparison.csv / .md
  - results/tables/per_class_results.csv / .md
  - results/figures/confusion_matrix_<run_id>.txt (text-rendered, fixed label order)
  - results/tables/bootstrap_ci.json
  - results/tables/significance_tests.json

Excludes SMOKETEST_* runs and anything explicitly marked diagnostic-only.
"""
import json
import sys
from itertools import combinations
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.evaluation.metrics import (
    compute_metrics, bootstrap_macro_f1_ci, paired_bootstrap_macro_f1_diff,
    holm_bonferroni, LABEL_ORDER,
)

ROOT = Path(__file__).resolve().parents[1]
PRED_DIR = ROOT / "results" / "predictions"
TABLES = ROOT / "results" / "tables"
FIGURES = ROOT / "results" / "figures"


def load_all_predictions():
    frames = []
    for f in sorted(PRED_DIR.glob("*_test.csv")):
        if f.name.startswith("SMOKETEST"):
            continue
        df = pd.read_csv(f)
        df["source_file"] = f.name
        frames.append(df)
    return frames


def render_confusion_matrix_text(cm, labels):
    lines = ["Rows = true label, Columns = predicted label", "Label order: " + ", ".join(labels), ""]
    header = "".ljust(12) + "".join(l[:10].ljust(12) for l in labels)
    lines.append(header)
    for i, row_label in enumerate(labels):
        row = row_label.ljust(12) + "".join(str(cm[i][j]).ljust(12) for j in range(len(labels)))
        lines.append(row)
    return "\n".join(lines)


def main():
    frames = load_all_predictions()
    if not frames:
        print("No prediction files found (excluding SMOKETEST). Nothing to evaluate yet.")
        return

    comparison_rows = []
    per_class_rows = []
    bootstrap_results = {}
    run_predictions = {}  # run_id -> (true_labels list, pred_labels list), for pairwise sig tests, keyed also by test set identity

    for df in frames:
        run_id = df["run_id"].iloc[0]
        experiment_id = df["experiment_id"].iloc[0]
        language = df["language"].iloc[0]
        true_labels = df["true_label"].tolist()
        pred_labels = df["predicted_label"].tolist()

        m = compute_metrics(true_labels, pred_labels)
        comparison_rows.append({
            "run_id": run_id, "experiment_id": experiment_id, "language": language,
            "n": m["n"], "accuracy": m["accuracy"], "macro_f1": m["macro_f1"],
            "weighted_f1": m["weighted_f1"], "precision_macro": m["precision_macro"],
            "recall_macro": m["recall_macro"],
        })
        for cls, vals in m["per_class"].items():
            per_class_rows.append({
                "run_id": run_id, "experiment_id": experiment_id, "language": language, "class": cls,
                "precision": vals["precision"], "recall": vals["recall"], "f1": vals["f1"], "support": vals["support"],
            })

        cm_text = render_confusion_matrix_text(m["confusion_matrix"], LABEL_ORDER)
        (FIGURES / f"confusion_matrix_{run_id}.txt").write_text(cm_text, encoding="utf-8")

        ci = bootstrap_macro_f1_ci(true_labels, pred_labels, n_iterations=2000, seed=42)
        bootstrap_results[run_id] = ci

        run_predictions[run_id] = {
            "experiment_id": experiment_id, "language": language,
            "review_ids": df["review_id"].tolist(), "true": true_labels, "pred": pred_labels,
        }

    comp_df = pd.DataFrame(comparison_rows).sort_values(["experiment_id", "language", "macro_f1"], ascending=[True, True, False])
    comp_df.to_csv(TABLES / "model_comparison.csv", index=False, encoding="utf-8-sig")
    with open(TABLES / "model_comparison.md", "w", encoding="utf-8") as f:
        f.write("# Model Comparison (Phase 3)\n\n" + comp_df.to_string(index=False) + "\n")

    pc_df = pd.DataFrame(per_class_rows)
    pc_df.to_csv(TABLES / "per_class_results.csv", index=False, encoding="utf-8-sig")
    with open(TABLES / "per_class_results.md", "w", encoding="utf-8") as f:
        f.write("# Per-Class Results (Phase 3)\n\n" + pc_df.to_string(index=False) + "\n")

    with open(TABLES / "bootstrap_ci.json", "w", encoding="utf-8") as f:
        json.dump(bootstrap_results, f, indent=2, default=str)

    # Pairwise significance tests: only between runs evaluated on the EXACT SAME
    # test review_ids (same experiment_id + language), never across different test sets.
    sig_results = []
    groups = {}
    for run_id, info in run_predictions.items():
        key = (info["experiment_id"], info["language"], tuple(sorted(info["review_ids"])))
        groups.setdefault(key, []).append(run_id)

    for key, run_ids in groups.items():
        if len(run_ids) < 2:
            continue
        exp_id, lang, _ = key
        pvals_this_group = []
        pairs_this_group = []
        for run_a, run_b in combinations(run_ids, 2):
            info_a, info_b = run_predictions[run_a], run_predictions[run_b]
            # align by review_id to be safe
            order = info_a["review_ids"]
            idx_b = {rid: i for i, rid in enumerate(info_b["review_ids"])}
            true_a = info_a["true"]
            pred_a = info_a["pred"]
            pred_b = [info_b["pred"][idx_b[rid]] for rid in order]
            test = paired_bootstrap_macro_f1_diff(true_a, pred_a, pred_b, n_iterations=2000, seed=42)
            pairs_this_group.append((run_a, run_b, test))
            if "p_value_two_sided" in test:
                pvals_this_group.append(test["p_value_two_sided"])
            else:
                pvals_this_group.append(None)

        valid_idx = [i for i, p in enumerate(pvals_this_group) if p is not None]
        if valid_idx:
            adjusted = holm_bonferroni([pvals_this_group[i] for i in valid_idx])
            for j, i in enumerate(valid_idx):
                pvals_this_group[i] = {"raw_p": pvals_this_group[i], "holm_bonferroni_adjusted_p": adjusted[j]}

        for (run_a, run_b, test), p_adj in zip(pairs_this_group, pvals_this_group):
            sig_results.append({
                "experiment_id": exp_id, "language": lang, "run_a": run_a, "run_b": run_b,
                "test_result": test, "multiple_comparison_correction": p_adj,
            })

    with open(TABLES / "significance_tests.json", "w", encoding="utf-8") as f:
        json.dump(sig_results, f, indent=2, default=str)

    print(f"Evaluated {len(frames)} prediction files.")
    print(comp_df.to_string(index=False))
    print(f"\nWrote model_comparison.{{csv,md}}, per_class_results.{{csv,md}}, bootstrap_ci.json, "
          f"significance_tests.json ({len(sig_results)} pairwise comparisons), and "
          f"{len(frames)} confusion matrix files in results/figures/.")


if __name__ == "__main__":
    main()
