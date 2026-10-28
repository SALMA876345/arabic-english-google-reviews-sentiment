# Primary-vs-Rerun Labeling Audit

**Scope:** every artifact in `results/human_gold_evaluation/` and every documentation file referencing Human-Gold results was checked for whether it ever presents the Arabic standalone MARBERT (`E1_marbert_fullft`) or Arabic standalone XLM-R (`E1_xlmr_fullft`) **rerun** predictions as if they were the lost original **primary** Phase 3B results. No historical primary metric was altered by this audit; only additive clarifications were made where a gap was found.

| Artifact | Checked | Rerun qualifier present before this audit? | Correction applied |
|---|---|---|---|
| `02_prediction_availability.py` / `prediction_availability.csv` | Yes | Yes -- `realization` column explicitly reads `RERUN_REALIZATION_not_primary` for both models | None needed |
| `03_evaluate_against_human_gold.py` / `human_gold_metrics_all_models.csv` | Yes | Yes -- `realization` column carried through | None needed |
| `original_vs_human_gold_comparison.csv` | Yes | Yes -- `realization` column + `same_prediction_realization` flag | None needed |
| `04_statistical_tests.py` | Yes | Script groups models by key only, no inline realization comment | Not modified (code, not a reported artifact); covered by the output-file fix below |
| `statistical_tests_human_gold.csv` / `.json` | Yes | **No** -- `model_a`/`model_b` were bare keys with no realization tag in the row itself | **Fixed:** added `realization_a` / `realization_b` columns (`07_patch_rerun_labeling.py`); no p-value, CI, or diff was changed |
| `error_analysis_by_class_language.csv` | Yes | **No** -- `model_key` bare, `phase` value (`3B_GPU_fullFT`) shared by both rerun and primary models in that phase, no per-row disambiguation | **Fixed:** added `realization` column; no error count was changed |
| `qualitative_error_examples.csv` | Yes | **No** -- `model_key` bare, no phase or realization column at all | **Fixed:** added `realization` column; no example text or classification was changed |
| `prediction_availability_summary.json` | Yes | Partial -- `valid_model_keys` listed bare, realization only visible by cross-referencing the CSV | **Fixed:** added `valid_model_keys_with_realization` mapping |
| `master_results_human_gold.json` | Yes | Inherits from the files above | Rebuilt after the fixes above (`06_build_master_results.py` re-run); now carries the fix everywhere its source files did |
| `README_PROVENANCE.md` | Yes | Yes -- explicit paragraph on realization distinction in prose | None needed |
| `REPORT.md` | Yes | Yes -- every MARBERT/XLM-R-standalone mention in context already says "rerun" inline | None needed |
| `docs/known_limitations.md` #22 | Yes | Yes -- already states the rerun-vs-primary distinction explicitly for the original Phase 3A/3B significance testing | None needed (pre-existing, correct) |
| `docs/decisions.md` D17 | Yes | Yes -- explicit paragraph | None needed (pre-existing, correct) |
| `paper/notes/final_publication_readiness_audit.md` | Yes | Yes -- Section 6 of that audit states the distinction explicitly | None needed |
| `paper/notes/FINAL_SCIENTIFIC_FRAMING.md` (this phase) | Yes | Written with the qualifier from the outset | N/A -- new document |

## Historical primary figures (unchanged, reconfirmed, never substituted)

| Model | Original primary macro-F1 (Arabic, original labels) | Rerun macro-F1 (same metric) | Human-Gold figure available for the primary realization? |
|---|---|---|---|
| Standalone MARBERT | 0.785025 | 0.765263 | **No -- row-level predictions for the primary run are lost; no Human-Gold number exists or is claimed for it.** |
| Standalone XLM-R | 0.740295 | 0.740126 | **No -- same reason.** |

Both primary figures remain exactly as originally reported in `configs/models.yaml`'s `phase3b_transformers` section and `results/phase3b_kaggle_gpu/master_final_results.csv`; this audit did not touch either value.

## Conclusion

4 of 14 checked artifacts had a real, concrete labeling gap (a reader of that single file in isolation, without cross-referencing `prediction_availability.csv`, could not tell a rerun model from a primary one). All 4 are fixed with additive columns; the rest were already correctly labeled. No primary metric was altered anywhere.
