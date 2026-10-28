# Final Scientific Framing

**Status:** the project's frozen, authoritative framing as of the pre-manuscript-fixes phase. Supersedes any earlier framing implied by the project title or by `docs/research_gap.md`'s original code-switching-centered novelty claim. Manuscript prose has not yet been written; this document fixes what the prose must say, not how it says it.

## Primary contribution

**Evaluation-label reliability in bilingual (Arabic-English) review sentiment classification, and its measured effect on model evaluation, ranking stability, and statistical conclusions.**

Concretely: a 3-annotator + blind-4th-adjudicator human validation study of 757 reviews (369 Arabic, 388 English) produced a human-adjudicated reference set that disagrees with the original evaluation labels in 17.4% of cases, overwhelmingly concentrated in originally-Neutral-labeled reviews (82.9% revision rate). Re-evaluating 16 previously-trained models (two independent training tracks, 4 architectures/baselines, zero-shot and multilingual conditions) against this reference set changes which comparisons are statistically significant — 3 of the 4 previously-significant findings no longer hold, only 1 survives, and 1 previously non-significant comparison becomes significant [corrected 2026-10-27 from an earlier "2 of 4" miscount; verified against `results/human_gold_evaluation/statistical_tests_human_gold.csv`] — and substantially reorders the Arabic model ranking. This is the paper's load-bearing empirical result.

## Secondary contributions

1. **Multilingual/cross-lingual sentiment modeling under resource-constrained conditions.** Two independent training tracks (LoRA on CPU-only hardware; full fine-tuning on GPU) with a documented, non-causal account of what changed between them. Multilingual joint training (E4) is not significantly different from monolingual training in either language, under either labeling -- a real, modest, reportable finding.
2. **A code-switching measurement-methodology finding.** An exhaustive, two-rater, blind-audited inspection of 109 heuristically-flagged candidate documents found only 9 genuine Arabic-English code-switched reviews; 77.1% of the heuristic's candidates were a Google Maps UI translation-display artifact, not organic code-switching. This is reported as a finding about the difficulty of *detecting* code-switching reliably in review-platform text, not as a sentiment-modeling result.
3. **A worked example of rigorous, pre-registered, non-majority-vote adjudication design**, including the explicit justification (low mixed-sentiment κ=0.269) for why a 4th blind adjudicator was used instead of defaulting to 2/3 majority vote as gold.

## What is explicitly NOT the central contribution

- **Arabic-vs-English performance comparison.** The two language sub-corpora differ simultaneously in geography, domain, collection source, and original label-construction method (single-pass human annotation vs. rating-derived heuristic). Human validation improves label *quality* symmetrically in both languages but does not remove any of these confounds. No version of "Arabic is harder/easier than English" is supportable by this design, with or without a hedge.
- **Code-switching as a quantitative sentiment-modeling result.** n=9 genuine examples cannot support a train/test split, a confidence interval, or a significance test, and is not used for one anywhere in this project.

## Final research questions

- **RQ1 (reframed, primary):** How reliable are the evaluation labels commonly used for this task (rating-derived heuristics; single-pass human annotation), relative to a multi-annotator, blind-adjudicated reference set, in the Arabic-English Google-Maps-review domain?
- **RQ2 (primary):** Does moving evaluation from the original labels to the human-adjudicated reference set change which model comparisons are statistically significant, and does it reorder the model ranking?
- **RQ3 (reframed, descriptive, not causal):** What does the disagreement structure between original labels and the human-adjudicated reference set look like, across two independently-sourced language sub-corpora, without claiming a causal language-difficulty comparison?
- **RQ4 (retained, secondary):** Is multilingual joint training competitive with monolingual training, under the same evaluation labels?
- **RQ5 (retained, explicitly qualitative/diagnostic):** What does a systematic audit of code-switching candidates reveal about the reliability of common script-mixing heuristics in review-platform text?

## Safe claims

- Neutral obtained the lowest per-class F1 of the three sentiment classes for every one of 16 evaluated models, under both the original labels (mean F1=0.396) and the human-adjudicated reference set (mean F1=0.176) -- stated with class support counts attached (see `known_limitations.md`'s Human-Gold addendum and Section 7 wording below).
- 82.9% of originally-Neutral-labeled reviews (89.3% Arabic, 77.1% English) were revised to Positive or Negative under independent human adjudication; Positive/Negative originals were revised only 3.3%/11.1% of the time.
- Re-evaluating existing model predictions against the human-adjudicated reference set changes statistical conclusions: 3 of 4 previously-significant Arabic/English model comparisons (original labels, Holm-corrected) no longer reach significance; 1 (MARBERT rerun vs. EN->AR zero-shot) survives; and 1 previously non-significant comparison (XLM-R rerun vs. MARBERT rerun) becomes significant under the reference set.
- Mean macro-F1 drop when moving from original labels to the human-adjudicated reference set is larger for the GPU full-fine-tuning track (-0.101) than for the laptop LoRA track (-0.025), and is concentrated in Arabic (-0.146 vs. -0.040).
- Multilingual joint training (E4) is not significantly different from monolingual training in either language, under either labeling.
- A naive script-mixing heuristic's code-switch candidate set was dominated (77.1%) by a platform UI display artifact (translation pairs), not genuine code-switching; only 9 of 1,050,832 corpus documents are genuine Arabic-English code-switches.
- The 757-review annotation study achieved Fleiss' κ=0.650 (substantial agreement, Landis & Koch bands) across 3 independent annotators; 578/757 (76.4%) reviews were unanimous.

## Claims requiring qualification (use the exact qualifying language)

- **"Neutral is the hardest class"** -- never state bare. Use: *"Neutral obtained the lowest per-class F1 across every evaluated model, under both the original and human-adjudicated labels; this should be read alongside the finding that Neutral was also the class most frequently revised during independent adjudication (82.9%), and the class with the smallest support in the reference set (42/757 overall; 9/369 Arabic, 33/388 English). We interpret this as evidence of annotation-boundary instability rather than a demonstrated model-specific deficiency; we cannot separate genuine linguistic ambiguity, class rarity, and annotation-guideline placement as distinct causes with this design."*
- **"Zero-shot transfer is weaker"** -- qualify with the before/after change: significant in 3/4 comparisons under original labels, 1/4 under the human-adjudicated set; state both numbers, do not report only the original-label figure.
- **"Classical ML is competitive with / beats transformers"** -- qualify as "not significantly different after Holm correction, under either labeling" and name the untested transformer class-weighting confound (`known_limitations.md` #20) every time this is discussed.
- **"LoRA underperforms full fine-tuning"** -- qualify as "true under original labels; the gap narrows or reverses for several comparisons under the human-adjudicated reference set, especially in Arabic" -- never state the original-label gap alone as if it were the final word.
- **"Model rankings changed after human-adjudicated re-evaluation"** -- always name which specific model realization (primary vs. rerun) is involved when citing a specific rank change (see the rerun-labeling audit, `paper/notes/RERUN_LABELING_AUDIT.md`).
- **"Human-Gold"** -- define at first use as "human-adjudicated reference set (Human-Gold)"; never use the bare term as if it denotes infallible ground truth (see `paper/annotation/full/README.md` and Section 6 below).

## Prohibited / removed claims

- Any claim, hedged or not, that Arabic is inherently harder or easier to classify than English, or that one language's model "generalizes better."
- Any accuracy/F1/significance claim computed on the 9 genuine code-switch examples.
- Any claim that the human-adjudicated reference set is infallible, "true" ground truth, or free of its own annotator/adjudicator bias.
- Any claim attributing a Phase 3A-vs-3B score difference to GPU hardware specifically (fine-tuning method, class weighting, and sequence length all changed simultaneously).
- Any claim presenting a rerun realization's result (Arabic standalone MARBERT/XLM-R) as if it were the lost original primary result, in either the original-label or Human-Gold evaluation.
- Any specific deployment accuracy figure, or any claim that the deployment smoke tests constitute accuracy, validation, or effectiveness evidence (see `README.md`'s backend section, corrected in this phase).
