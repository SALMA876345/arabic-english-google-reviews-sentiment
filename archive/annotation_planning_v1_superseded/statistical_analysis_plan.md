# Statistical Analysis Plan — Matched-Protocol Validation Slice (Post-Annotation)

**Status: PLANNED, NOT EXECUTED.** No human labels exist yet. This document specifies exactly what will be computed once annotation + adjudication is complete, so the analysis is pre-specified rather than designed after seeing results.

## 1. Primary analysis: re-score existing model predictions against the new human labels

This is the main payoff of completing annotation. Every model already trained (Phase 3A classical/LoRA, Phase 3B full-FT, per `results/predictions/` and `results/phase3b_kaggle_gpu/`) already produced predictions on these exact 757 main-slice rows (they are the frozen test set). **No new model inference is needed** — only re-scoring existing predictions against the new gold labels instead of the original (human-annotated-for-Arabic / rating-derived-for-English) labels.

For each existing model × language:
- Recompute macro-F1, per-class P/R/F1, confusion matrix against `adjudicated_label` (new) vs. against `original_label` (old) — report both, side by side.
- This directly tests whether the Phase 3 findings (e.g., "classical numerically beats LoRA but not significantly," "Neutral is hardest") hold up under better-constructed ground truth, or were partly artifacts of label noise (particularly plausible for English, given the rating_text_disagreement finding in `docs/error_analysis.md`).

## 2. Per-language description of the new labels

- Macro-F1 is not applicable here (there's no "prediction" — these ARE the labels) — instead report: class distribution of `adjudicated_label` per language, confidence distribution, mixed_sentiment_flag rate per language.
- Compare the new label's class distribution to the original label's class distribution per language (a simple cross-tab) — this is itself informative about how much rating-derived labels diverge from human judgment in aggregate, not just row-by-row.

## 3. Inter-annotator agreement

- Primary: Cohen's κ (unweighted), on the 757 main-slice rows, overall and split by language (Arabic subset, English subset) — computed by `build_adjudication_sheet.py`, consistent with the project's existing κ-reporting convention (cf. κ=0.87 for Zenodo 17011574, κ=0.853/0.809 for the code-switch audit).
- Secondary (optional, not required): linear-weighted κ, since Negative-Neutral-Positive has a natural ordering and adjacent-category disagreement (e.g., Neutral vs. Positive) is less severe than opposite-category disagreement (Negative vs. Positive) — report alongside unweighted κ if computed, never as a replacement for it.
- Report the 9 code-switch diagnostic rows' agreement **separately**, labeled qualitative-only, never pooled into the main-slice κ (consistent with their treatment everywhere else in this project).

## 4. Rating-vs-human disagreement (English only — Arabic has no star ratings to compare against)

- Cross-tab: rating-derived label (1-2★=Neg/3★=Neu/4-5★=Pos) vs. `adjudicated_label`, reporting raw disagreement rate and a confusion-matrix-style breakdown.
- This gives, for the first time, a **clean, human-verified** quantification of the rating_text_disagreement phenomenon the error analysis could previously only infer indirectly from model errors (`docs/error_analysis.md` §E2's ~50-60% estimate was a plausible inference, not a direct measurement — this closes that gap).

## 5. Human-vs-original-human agreement (Arabic only)

- Arabic's original labels are themselves human-annotated (by Zenodo 17011574's original authors, κ=0.87 reported in their own paper). Cross-tabbing the new annotator(s)' labels against the original labels here is effectively an **independent replication check** of the source dataset's own annotation quality, not a label-provenance-confound diagnostic (there's no provenance gap to find on the Arabic side — both are human-annotated). Report this distinctly from the English rating-disagreement analysis; do not describe them with the same language, since they answer different questions.

## 6. Confidence intervals

- Reuse `src/evaluation/metrics.py::bootstrap_macro_f1_ci` (already implemented, n≥30 threshold already satisfied for both languages: n=369 Arabic, n=388 English) for every re-scored model×language macro-F1.

## 7. Paired vs. unpaired significance testing — the critical methodological distinction for this slice

- **Within-language, model-vs-model comparisons** (e.g., "does TF-IDF+LogReg's macro-F1 against the new labels differ from XLM-R's?"): use the project's existing **paired** bootstrap (`paired_bootstrap_macro_f1_diff`) — valid here because both models are scored on the *same* test rows.
- **Cross-language comparisons** (e.g., "is the Arabic macro-F1 different from the English macro-F1, both measured against the new matched-protocol labels?"): **this requires an unpaired/two-sample method, NOT the existing paired-bootstrap function as-is.** There is no natural item-level pairing between an Arabic review and an English review — they are different items entirely. Use an independent two-sample bootstrap: resample Arabic rows and English rows separately (with replacement, within their own language), compute each language's macro-F1 per resample, and build a bootstrap distribution of the *difference*. This is a different (simpler) procedure than the paired version and must not be confused with it in the eventual methods section.
- Apply Holm-Bonferroni correction only within a clearly pre-specified family (e.g., "all model×language re-scoring comparisons," separately from "the one cross-language gap test") — do not pool an arbitrarily large set of comparisons into one family just because they're now computable; per `src/evaluation/metrics.py`'s existing convention, define the family *before* looking at the p-values.
- **Do not test everything just because it's now possible.** The scientifically motivated tests are: (a) does the model ranking from Phase 3 change under the new labels, (b) is the Arabic-vs-English macro-F1 gap (under matched-protocol labels) significant, (c) is the rating-vs-human disagreement rate meaningfully different from zero (trivially yes if >0 cases exist — report the rate and a CI on it, not a significance test against an uninteresting null).

## 8. What this analysis can and cannot conclude (cross-reference to the main audit, §6)

Even a statistically significant Arabic-vs-English gap computed under matched-protocol labels **only rules out the label-provenance/annotator-identity confound**. It does **not** rule out geography, sub-domain, review-length distribution, or source-platform/era differences between the two pools — all of which remain structurally present in this slice regardless of annotation quality (see `paper/annotation/README.md` §6 and the main audit's §7/§6 for the full confound inventory). State this explicitly in the results write-up; do not let a significant p-value be read as "proof Arabic is harder."
