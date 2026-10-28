# Phase 3 Report — Controlled Model Training, Evaluation, Error Analysis

**Date:** 2026-10-24
**Status:** All completed experiments trained once, evaluated once on the frozen test set, audited by an independent adversarial pass. No test-set performance was inspected before model/hyperparameter selection (validation-only). No results fabricated, smoothed, or cherry-picked.

## 1. Which experiments actually ran?
- **E1** (Arabic-only): TF-IDF+LogReg, TF-IDF+SVM, MARBERT(LoRA), XLM-R(LoRA) — all 4 ran.
- **E2** (English-only): TF-IDF+LogReg, TF-IDF+SVM, XLM-R(LoRA) — all 3 ran.
- **E3** (matched comparison): not a separate training run — a reporting/comparison exercise over E1+E2 results, as designed.
- **E4** (combined multilingual training): attempted 3 times (batch sizes 4, 4, 2), **failed all 3 with OOM — NOT completed.**
- **E5** (cross-lingual robustness): both directions ran (inference-only, reusing E1/E2's trained adapters).
- **E6** (real-world code-switch): ran as a **qualitative diagnostic only** on the 9 verified genuine examples (MARBERT); XLM-R inference on this set failed 3x with OOM and was not obtained.
- **E7** (external SESA-CSD): **not run** — no confirmed public access (established in Phase 2.5, unchanged).
- **E8** (full-English scale): **not attempted** — deprioritized after E4 already consumed the compute/time budget allotted to supplementary-scale experiments; marked `NOT RUN — COMPUTE/TIME CONSTRAINT`.
- **E_jordan_binary_aux**: ran (TF-IDF+LogReg; MARBERT variant not attempted, same compute constraint).

## 2. Which models actually trained?
TF-IDF+LogisticRegression, TF-IDF+LinearSVC (full training, validation-tuned), MARBERT (LoRA adapters, ~0.3% of parameters trainable), XLM-RoBERTa-base (LoRA adapters). **No model was fully fine-tuned** — full fine-tuning OOM'd on this project's CPU-only, 8.3GB-RAM machine; every transformer result in this report is LoRA-adapted (`docs/decisions.md` D14, `configs/models.yaml`).

## 3. Exact dataset used by each experiment?
Per `docs/experimental_dataset_protocol.md`: E1 = Arabic tourism primary pool (train 2,786/val 370/test 369, human-annotated, κ=0.87). E2 = English matched subset (train 2,785/val 352/test 388, rating-derived). E4 (not completed) would have used both plus Jordan's 8,364 LLM-weak rows for training augmentation. E5 reuses E1/E2's test sets with the other language's trained adapter. E6 = the 9-row code-switch diagnostic set. E_jordan_binary_aux = 8,364 LLM-weak train rows, 300 human-gold test rows (binary, zero Neutral).

## 4. Best validation-selected model?
Selected on validation macro-F1 only, before any test inspection: **TF-IDF+LogisticRegression** for both E1 (val F1=0.7492, beating SVM's 0.7452, MARBERT's 0.5823, XLM-R's 0.5751) and E2 (val F1=0.6770, beating SVM's 0.6540, XLM-R's 0.6394). `class_weight="balanced"` won every single grid-search comparison for the classical models — see item 6 below for why this matters to the model-family comparison.

## 5. Arabic test Macro-F1?
TF-IDF+LogReg: **0.7048** (accuracy 0.786). Full E1 ranking: SVM 0.7048, LogReg 0.7048 (tied to 4 decimals, confirmed not a bug), XLM-R 0.6233, MARBERT 0.6177.

## 6. English test Macro-F1?
TF-IDF+LogReg: **0.6871** (accuracy 0.760). Full E2 ranking: LogReg 0.6871, SVM 0.6506, XLM-R 0.6110.

## 7. Per-class results?
Full table: `results/tables/per_class_results.csv`. Positive is the strongest class everywhere (support-dominant, 61% of the Arabic pool). Negative is moderate. **Neutral is the weakest class for every model in every experiment** — see Q8.

## 8. Neutral-class performance?
Collapses hardest in the LoRA transformers: Neutral F1 is 0.167 (MARBERT/E1), 0.278 (XLM-R/E1), 0.194 (XLM-R/E2) — driven by very low recall (0.11-0.18), meaning the transformers rarely predict Neutral at all. Classical baselines do noticeably better (Neutral F1 0.39-0.53). **This is likely not purely a transformer-capacity issue**: the classical models explicitly used validation-selected class weighting (`class_weight="balanced"` won every grid cell), while the transformer training loop used unweighted cross-entropy loss by default — class weighting was never tested for the transformers due to time constraints. This confound is logged in `known_limitations.md` #20 and must not be resolved by assertion in the manuscript.

## 9. Did Transformers outperform classical baselines?
**No, numerically** — classical baselines scored higher macro-F1 on both E1 and E2. **But this difference is NOT statistically significant** after Holm-Bonferroni correction for multiple comparisons: every baseline-vs-transformer gap that looked significant unadjusted (raw p=0.015-0.048) has adjusted p≥0.09 (`results/tables/significance_tests.json`, independently re-verified by the adversarial reviewer). **Honest conclusion: classical ML scored numerically higher under this phase's LoRA/CPU/class-weighting constraints, but the sample size here cannot statistically distinguish this from no real difference.** This must not be reported as "classical ML beats transformers for this task" — that overclaims what a non-significant result supports.

## 10. Did multilingual training help?
**Unknown — E4 did not complete.** Three attempts at decreasing batch size (4, 4, 2) all failed with out-of-memory errors, the last on a request for only ~1.5MB on an 8.3GB-RAM machine — evidence of volatile memory pressure from other processes on this shared machine, not a fixable batch-size issue (`docs/decisions.md` D15). This research question remains open.

## 11. Cross-lingual robustness result?
Both directions show a real transfer-loss drop versus in-language training: Arabic-trained XLM-R → English test = 0.5455 macro-F1 (vs. 0.6110 for an XLM-R trained directly on English); English-trained XLM-R → Arabic test = 0.5411 (vs. 0.6233 for in-language Arabic XLM-R). **Zero-shot cross-lingual transfer underperforms in-language training by roughly 0.07-0.08 macro-F1 points in both directions** — a plausible, consistent finding, though not formally significance-tested against the in-language runs (a gap noted by the adversarial reviewer; not computed due to time).

## 12. What happened on the 9 real code-switch examples?
Qualitative only (n=9, no quantitative metric reported — see `codeswitch_audit.md`). MARBERT predicted 7/9 matching the (non-gold) source label; the 2 mismatches were also the 2 lowest-confidence predictions (0.43, 0.38, near the 1/3 random baseline) and the 2 shortest/sparsest-context cases — consistent with the general `short_ambiguous` error pattern, not evidence of a code-switching-specific failure. XLM-R inference on this set could not be obtained (3x OOM). Full detail: `docs/error_analysis.md` §E6.

## 13. Was SESA-CSD evaluated?
No — no confirmed public access, unchanged from the Phase 2.5 finding.

## 14. Was E8 run?
No — `NOT RUN — COMPUTE/TIME CONSTRAINT`, per the project's own explicit allowance for this outcome.

## 15. Main statistically supported findings?
(a) Classical-vs-transformer macro-F1 differences on E1/E2 are not statistically significant after multiple-comparison correction. (b) Neutral is the hardest class everywhere, with a confirmed, large effect size (F1 gaps of 0.2-0.3+ between classical and transformer models). (c) Frozen train/val/test splits have zero duplicate-text leakage and zero place/business group overlap, independently re-verified.

## 16. Main negative findings?
(a) Full transformer fine-tuning is infeasible on the available hardware — forced a LoRA substitution. (b) E4 (combined multilingual training) could not be completed after 3 attempts. (c) XLM-R inference on the 9 code-switch examples failed 3x. (d) LoRA-adapted transformers numerically underperformed classical baselines on both E1 and E2 (not statistically significant, but a real, reportable pattern under these constraints). (e) Transformer training never tested class weighting, a methodological gap, not a finding about the models themselves.

## 17. Main error categories?
`mixed_sentiment` (genuinely split-sentiment reviews) dominates errors in both languages and both model families (35-79% of errors depending on model/language). English additionally shows `rating_text_disagreement` as a major driver (15-19% of errors; ~50-60% of all English errors trace back to the rating-derivation labeling mechanism, not model weakness). Negation and implicit sentiment are handled somewhat better by transformers than by TF-IDF in both languages. Code-switching is confirmed, again, to be a non-factor in the error sets (consistent with `codeswitch_audit.md`). Full detail: `docs/error_analysis.md`.

## 18. Remaining threats to validity?
- LoRA vs. full fine-tuning capacity confound (Q9, Q10).
- Untested class-weighting asymmetry between classical and transformer training (Q8, `known_limitations.md` #20).
- E4 incomplete — multilingual-training question open.
- Cross-language comparison (RQ3/E3) remains confounded by dataset origin per `dataset_audit.md` §7 — the matched-protocol manual-validation slice (766 rows) is still **pending annotation**, unchanged from Phase 2.5.
- English test labels are rating-derived, not human-verified (Q17's rating_text_disagreement finding is direct evidence this matters).
- Small Arabic test set (n=369) limits statistical power for subtler effects.
- Geographic/domain mismatch (Saudi tourism vs. Wyoming/Vermont general local businesses) persists, as documented since Phase 2.5.

## 19. Are the results reproducible?
Yes, with one caveat. Seed=42 throughout; every run logged in `experiments/registry.csv` with hyperparameters; `configs/training.yaml`/`models.yaml` record both the original plan and what was actually run; `requirements.txt` is pinned. **Caveat:** E4's and E6(XLM-R)'s OOM failures are a function of this specific machine's fluctuating free memory at the time of each attempt (observed free RAM ranged ~0.3GB to ~1.3GB across the session) — re-running on a machine with reliably more free memory would likely succeed where these failed, so "reproducible" here means "the same code/data/seed will reproduce the same result on comparable hardware," not "will reproduce the same OOM failures."

## 20. Is the project ready for manuscript writing?

**READY FOR PHASE 4 — MANUSCRIPT**, with the following conditions carried forward explicitly, not resolved by this report: (1) every transformer result must be labeled LoRA-adapted, never presented as standard fine-tuning; (2) the "classical beats transformer" framing must be stated as numerically-higher-but-not-statistically-significant, never as a clean win; (3) E4/E8/SESA-CSD/E6-quantitative must be reported as not completed, with reasons, not omitted; (4) the RQ3 cross-language claim remains exploratory/confounded pending the still-unannotated manual validation slice; (5) the untested class-weighting asymmetry (Q8) must be named as an open confound. None of these are blocking issues — the adversarial review found no fabrication, leakage, or falsified numbers anywhere, and two labeling-discipline gaps it did find (`docs/decisions.md` D16) have been fixed. They are exactly the caveats a results-chapter and limitations section are for.
