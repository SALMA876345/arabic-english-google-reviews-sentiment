# Human-Gold Label Analysis + Model Re-Evaluation -- Report

No model was retrained. All numbers below come from previously saved row-level predictions, re-scored against `human_gold_757.csv` (SHA-256 `7b53ca621d237106413e27395010ad9ba2417d733b2bc5694d49749a03be53fd`). See `README_PROVENANCE.md` for exact scripts, seeds, and software versions. Full machine-readable detail: `master_results_human_gold.json`.

## B/C. Original labels vs. Human-Gold: disagreement, not "noise" until defined as such

Operational definition used throughout: **"disagreement with the Human-Gold reference set"** = `original_label != human_gold_sentiment`. No disagreement is assumed to be an "error" in the original label; Human-Gold is a human-adjudicated reference, not an infallible ground truth.

| Scope | Agreement | Disagreement | Cohen's kappa |
|---|---|---|---|
| Overall (n=757) | 625 (82.6%) | 132 (17.4%) | 0.662 |
| Arabic (n=369) | 310 (84.0%) | 59 (16.0%) | 0.660 |
| English (n=388) | 315 (81.2%) | 73 (18.8%) | 0.660 |

Named transitions (original -> Human-Gold), overall:
Positive->Neutral 11, Positive->Negative 4, Neutral->Positive 61, Neutral->Negative 36, Negative->Neutral 11, Negative->Positive 9.

**The overwhelming majority of disagreement is concentrated in reviews originally labeled Neutral.** Disagreement rate conditional on the *original* class: Negative 11.1%, **Neutral 82.9%**, Positive 3.3% (Arabic: 8.0% / **89.3%** / 1.3%; English: 13.2% / **77.1%** / 5.4%). In other words, nearly everything originally called Neutral was revised to something else under independent human adjudication, in both languages, while originally Positive/Negative labels were revised only rarely. Conditional on the *Human-Gold* class, Neutral itself still shows elevated disagreement (52.4% overall) because so few Human-Gold-Neutral cases exist (42 of 757) and most come from revised Negative/Positive originals, not from confirmed-Neutral originals.

Class distribution shift: original {Negative 181, Neutral 117, Positive 459} -> Human-Gold {Negative 201, Neutral 42, Positive 514}. Neutral shrank by ~64%; Negative and Positive both grew, consistent with the transition counts above (Neutral mostly redistributed to Positive and Negative, not the reverse).

This pattern is consistent with -- but does not on its own prove a mechanism for -- the earlier, independently measured finding that the original 3-annotator mixed-sentiment-flag kappa (0.269) was too low to trust: Neutral is evidently the class where the original label construction (rating-derived for English, single-pass human annotation for Arabic) and independent human judgment disagree most. No causal claim is made about *why*.

## D. Prediction availability

16 of 18 candidate prediction sources are valid (exact id match, zero duplicates, zero missing, valid label vocabulary). The 2 missing are the Arabic Phase 3B **primary** standalone MARBERT and XLM-R runs, whose row-level predictions were already known to be lost (`docs/decisions.md` D17) -- not reconstructed here. Every number below from those two architectures instead uses the documented reproducibility **rerun**, labeled `RERUN_REALIZATION_not_primary` in every output row; the original primary scores (MARBERT 0.785025, XLM-R 0.740295) are **not** touched or replaced anywhere. Full table: `prediction_availability.csv`.

## E. Original-label vs. Human-Gold metrics -- the central finding

Full table: `original_vs_human_gold_comparison.csv`. Headline: **macro-F1 drops under Human-Gold for 13 of 16 models**, and the drop is much larger for Phase 3B (GPU, full fine-tuning) than for Phase 3A (laptop, LoRA):

| Phase | Mean macro-F1 delta (Human-Gold minus original) |
|---|---|
| 3A laptop/LoRA | -0.025 (Arabic -0.040, English -0.006) |
| 3B GPU full-FT | -0.101 (Arabic -0.146, English -0.041) |

The three models that *gained* macro-F1 under Human-Gold are all Phase 3A: `E5_enTrain_arTest_lora` (+0.074), `E2_xlmr_lora` (+0.012), `E5_arTrain_enTest_lora` (+0.017) -- all LoRA models, none of the GPU full-FT models.

**Per-class pattern behind the drop:** mean Neutral-F1 across all 16 models falls from 0.396 (original) to 0.176 (Human-Gold), while Negative-F1 rises slightly (0.748->0.798) and Positive-F1 is roughly flat (0.879->0.875). Error-analysis detail (`error_analysis_by_class_language.csv`) shows every Phase 3B GPU model substantially **over-predicts Neutral** relative to the now-much-smaller Human-Gold Neutral class (e.g. `E4_multilingual_xlmr_arabic`: 99 of 369 Arabic predictions are Neutral when the Human-Gold Neutral class has only 9 true members; `E1_xlmr_fullft` rerun: 102 false-Neutral predictions). Phase 3A LoRA models over-predict Neutral far less. This is consistent with -- but not proof of -- the GPU full-FT models having fit the original labels' larger, apparently less-reliable Neutral class more closely than the LoRA models did; no causal mechanism is asserted, and this is not a controlled ablation (fine-tuning method, class weighting, and hardware all differ simultaneously, per the existing non-causal framing requirement in `configs/training.yaml`).

## Model ranking under Human-Gold (macro-F1)

**Arabic** -- reorders substantially:
- Original: E4 multilingual (0.768) > MARBERT rerun (0.765) > XLM-R rerun (0.740) > TF-IDF (0.705) > EN->AR zero-shot (0.680) > XLM-R LoRA (0.623) > MARBERT LoRA (0.618) > EN->AR LoRA zero-shot (0.541)
- Human-Gold: MARBERT rerun (0.626) > EN->AR LoRA zero-shot (0.615) ~ XLM-R LoRA (0.615) > MARBERT LoRA (0.601) > E4 multilingual (0.595) > TF-IDF logreg (0.586) > XLM-R rerun (0.582) > TF-IDF svm (0.573) > EN->AR GPU zero-shot (0.568, now *last*)
- The GPU zero-shot model falls from 5th to last; a laptop LoRA zero-shot model rises into 2nd place; the TF-IDF baseline moves from clearly behind every transformer to the middle of the pack, ahead of 2 of 3 Phase 3B transformers.

**English** -- comparatively stable:
- Original: E4 multilingual (0.740) > XLM-R full-FT (0.728) > TF-IDF logreg (0.687) > AR->EN zero-shot (0.680) > TF-IDF svm (0.651) > XLM-R LoRA (0.611) > AR->EN LoRA zero-shot (0.546)
- Human-Gold: XLM-R full-FT (0.692) > E4 multilingual (0.686) > AR->EN zero-shot (0.648) > TF-IDF logreg (0.647) > TF-IDF svm (0.640) > XLM-R LoRA (0.623) > AR->EN LoRA zero-shot (0.562)
- Only the top-2 swap order (by 0.006); the rest of the ordering is unchanged.

Per **Section I**, this Arabic/English asymmetry in ranking stability is reported descriptively only. It is not evidence that Arabic is inherently harder or that the original Arabic label construction ("human_annotated", single-pass) is inherently worse than English's ("rating_derived") -- the two language datasets differ in geography, domain, source, and label history, and the ranking-stability gap could reflect any of those confounds, not language per se.

## F. Statistical testing (full detail: `statistical_tests_human_gold.csv/.json`)

Two distinct procedures, not conflated (see `README_PROVENANCE.md`): a paired bootstrap resampling CI/heuristic-p (10,000 iterations), and a genuine paired permutation/randomization test (10,000 iterations, row-level model-identity swap under the null). Holm-Bonferroni applied within each of 4 families.

**Significant after Holm (permutation test, alpha=0.05), evaluated on Human-Gold:**
- Phase3B_Arabic: MARBERT rerun > XLM-R rerun (adj. p=0.0012)
- Phase3B_Arabic: MARBERT rerun > EN->AR zero-shot (adj. p=0.0160)
- Nothing else -- including E4 multilingual vs. any other Arabic model, and every English Phase3B/Phase3A comparison -- reaches significance after correction.

**Compare to the pre-Human-Gold (original-label) significance results** (`results/tables/significance_tests.json`, `results/phase3b_kaggle_gpu/*_paired_bootstrap_holm_results.csv`): under original labels, 3 Arabic comparisons were significant (XLM-R rerun, MARBERT rerun, and E4 multilingual all significantly beat EN->AR zero-shot) and 1 English comparison was significant (E4 multilingual beat AR->EN zero-shot). **CORRECTED (re-verified directly against `statistical_tests_human_gold.csv`): under Human-Gold, 3 of those 4 previously-significant findings no longer hold** (XLM-R rerun vs. zero-shot; E4 multilingual vs. zero-shot in both Arabic and English), and only **1 of the original 4 survives** (MARBERT rerun vs. EN->AR zero-shot). A fifth comparison that was NOT significant under original labels (XLM-R rerun vs. MARBERT rerun) becomes significant under Human-Gold, favoring MARBERT. The surviving/newly-significant pattern is specific to MARBERT rerun, not the group of "real models" as a whole. (This corrects an earlier arithmetic error in this same paragraph, which miscounted the comparisons listed in its own parenthetical as "2 of 4" when three were actually named.)

## G. Error analysis

See `error_analysis_by_class_language.csv` and `qualitative_error_examples.csv` (deterministic selection: for every model and every (true-class, predicted-class) error cell, the first 3 review_ids in ascending lexicographic order -- applied identically everywhere, no cherry-picking, no annotator identity exposed anywhere in these files). Dominant error pattern across every model: predicting Negative or Positive as Neutral, and (for Phase 3B models especially) predicting Neutral far more often than Human-Gold ever calls for.

## H. Reassessment of prior conclusions

1. **Is Neutral still the hardest class?** Yes, more clearly than before. Mean Neutral-F1 falls further under Human-Gold (0.396->0.176) than under original labels, where it was already the lowest-scoring class. This conclusion is **strengthened**, not weakened.
2. **Do model rankings change?** Yes, substantially for Arabic (GPU full-FT models fall from dominating the top of the ranking to the middle/bottom; a LoRA zero-shot model and the TF-IDF baseline rise); only marginally for English (top-2 swap by a small margin, rest of order unchanged).
3. **Does multilingual training (E4) remain competitive with language-specific training?** Yes -- and this conclusion is **stable**: E4 vs. the matched standalone model was not statistically significant under original labels in either language, and remains not significant under Human-Gold in either language (Arabic: E4 vs. MARBERT rerun adj. p=0.163; English: E4 vs. XLM-R full-FT adj. p=0.779). The point estimates re-order (E4 was numerically ahead in both languages under original labels; it is now numerically behind in both), but neither gap is large enough to call significant either before or after.
4. **Does zero-shot transfer remain weaker?** This conclusion must be **weakened**. Under original labels, zero-shot was significantly worse than every other Arabic model and significantly worse than E4 multilingual in English. Under Human-Gold, zero-shot is no longer significantly different from XLM-R rerun or E4 multilingual in Arabic, or from either real model in English; it remains significantly worse only against MARBERT rerun in Arabic. Zero-shot is still numerically the weakest or near-weakest model in most rankings, but the statistical case for "zero-shot is reliably worse" is substantially thinner post-Human-Gold.
5. **How much did original-label construction affect reported performance?** Substantially, and asymmetrically by training track: mean macro-F1 fell -0.101 for Phase 3B (GPU full fine-tuning) models and -0.025 for Phase 3A (laptop LoRA) models when re-scored against Human-Gold. This is the single largest finding of this phase.
6. **Which conclusions remain stable?** Neutral-is-hardest (strengthened); multilingual-training-is-competitive-not-clearly-better-or-worse (stable); the general Arabic/English non-causal-confound framing (unaffected, and explicitly preserved below).
7. **Which conclusions must be weakened, changed, or removed?** The zero-shot-is-significantly-weaker claim must be weakened to "zero-shot is numerically weaker in most comparisons but the statistical case mostly does not survive Human-Gold re-evaluation, with one exception (MARBERT rerun, Arabic)." Any implicit framing of Phase 3B's original-label scores as straightforwardly "the best models" must be qualified: their advantage over Phase 3A and over the TF-IDF baseline shrinks or reverses under Human-Gold, concentrated in Arabic.

## I. RQ3 confound restriction (reaffirmed, not relaxed by this phase)

Human validation improves the Arabic and English evaluation labels' reliability; it does **not** resolve, control for, or speak to the pre-existing confound between the two language datasets (geography, domain, source, label-construction history). No claim is made or implied anywhere in this phase that Arabic is inherently harder or easier than English. The differing degree of ranking disruption between the two languages under Human-Gold is reported descriptively only, consistent with this restriction.

## Limitations

- Phase 3B's two lost Arabic primary runs are evaluated via their reproducibility reruns only; this is explicitly flagged everywhere in the outputs and is not a substitute for the lost primary row-level predictions.
- The paired statistical tests compare models within the same track (Phase 3A vs. Phase 3A, Phase 3B vs. Phase 3B) using the same pairing structure as before Human-Gold, for direct before/after comparability; this phase does not newly test Phase 3A models against Phase 3B models against each other, which would mix fine-tuning method, class weighting, and hardware as confounds beyond what a single significance test can cleanly attribute.
- n=369 (Arabic) / n=388 (English) remain the limiting factor for statistical power; several numerically large point-estimate differences (e.g. E4 multilingual vs. MARBERT rerun in Arabic, raw permutation p=0.041) do not survive Holm correction.
- Human-Gold itself is a human-adjudicated reference set, not claimed to be infallible ground truth (per `paper/annotation/full/README.md`); "disagreement with Human-Gold" is the operational definition used throughout this report, not "error" or "noise" in an absolute sense.
