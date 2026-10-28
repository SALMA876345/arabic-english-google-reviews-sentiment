# Human-Gold Label Analysis + Model Re-Evaluation -- Provenance

**Phase:** Human-Gold label analysis and existing-prediction re-evaluation (no retraining).
**Input (frozen, unmodified):** `paper/annotation/full/human_gold_757.csv`
SHA-256: `7b53ca621d237106413e27395010ad9ba2417d733b2bc5694d49749a03be53fd` (re-verified at the start of `01_build_comparison_dataset.py`; the script aborts if this does not match).

## What this phase did NOT do

- No model was retrained, fine-tuned, or re-run. Every metric below comes from previously saved row-level prediction files under `results/predictions/` (Phase 3A, laptop/LoRA) and `results/phase3b_kaggle_gpu/` (Phase 3B, GPU full fine-tuning).
- `human_gold_757.csv`, `human_validation_757_master.csv`, every annotator/adjudicator raw file, every frozen split under `data/splits/frozen_v1/`, and every existing Phase 3A/3B result file (`results/tables/*`, `results/phase3b_kaggle_gpu/master_final_results.csv`, etc.) were read-only inputs and are untouched.
- The two Arabic Phase 3B primary runs (standalone MARBERT and standalone XLM-R) whose original row-level predictions were lost are reported as explicitly MISSING in `prediction_availability.csv` -- not reconstructed, approximated, or silently substituted with the reproducibility reruns. Where the reruns are used instead, every output row is labeled `RERUN_REALIZATION_not_primary`.

## Scripts (run in this order) and what each produced

| # | Script | Produces |
|---|---|---|
| 1 | `01_build_comparison_dataset.py` | `comparison_dataset_757.csv`, `label_agreement_overall_by_language.json`, `confusion_matrix_original_vs_humangold_*.csv`, `disagreement_rate_conditional.csv`, `full_transition_table_*.csv` |
| 2 | `02_prediction_availability.py` | `prediction_availability.csv`, `prediction_availability_summary.json` |
| 3 | `03_evaluate_against_human_gold.py` | `human_gold_metrics_all_models.csv`, `original_vs_human_gold_comparison.csv`, `confusion_matrix_<model>_<original_label\|human_gold>.csv`, `model_predictions_vs_human_gold/<model>.csv` |
| 4 | `04_statistical_tests.py` | `statistical_tests_human_gold.csv`, `statistical_tests_human_gold.json` |
| 5 | `05_error_analysis.py` | `error_analysis_by_class_language.csv`, `qualitative_error_examples.csv` |

All scripts are idempotent and read-only with respect to every file outside `results/human_gold_evaluation/`.

## Software versions (this run)

- Python 3.11.9
- pandas 2.2.3
- numpy 2.4.4
- scikit-learn 1.7.2
- scipy 1.17.1

## Seeds

- Paired bootstrap CI (Section F): seed=42, n_iterations=10,000, per comparison.
- Paired permutation/randomization test (Section F): seed=42, n_iterations=10,000, per comparison (a separate RNG stream per comparison, same seed value for reproducibility -- not the same draws as the bootstrap, since the resampling scheme differs).
- All metric computation reuses `src/evaluation/metrics.py::compute_metrics` / `holm_bonferroni` unmodified (the same module Phase 3A/3B used), so the metric *definitions* are identical before and after Human-Gold; only the evaluation reference label changes.

## Statistical method note (per explicit instruction)

Two distinct procedures are reported in `statistical_tests_human_gold.*` and must not be conflated:
1. **Paired bootstrap resampling** (`bootstrap_resampling_p_heuristic`, `ci_lower_2.5`, `ci_upper_97.5`): resamples test rows with replacement; the accompanying p-value is a resampling-distribution heuristic (proportion of bootstrap diffs crossing zero, doubled), not a permutation-test p-value. Retained here only for the 95% CI and for continuity with the Phase 3A/3B methodology.
2. **Paired permutation/randomization test** (`permutation_p_two_sided`): for each iteration, independently swaps which model's prediction occupies "slot A" vs "slot B" for each row (Bernoulli p=0.5), holding the Human-Gold true label fixed, and recomputes the Macro-F1 difference under the null of exchangeability. The reported p-value uses the standard add-one-smoothed exact-permutation-test formula. This is the test referred to as "a defensible paired randomization/permutation test" in this phase's instructions; (1) is not a substitute for it.

Holm-Bonferroni correction is applied separately within each of the 4 comparison families (`Phase3A_Arabic_E1`, `Phase3A_English_E2`, `Phase3B_Arabic`, `Phase3B_English`), and separately to the bootstrap-heuristic p-values and to the permutation p-values.
