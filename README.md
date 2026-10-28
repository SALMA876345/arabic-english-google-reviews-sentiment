# Evaluation-Label Reliability in Bilingual Sentiment Classification

Research repository for a study of Arabic-English Google-Maps-style review sentiment classification, centered on **evaluation-label reliability**: how much the construction of the evaluation reference label — rating-derived, single-pass human-annotated, or independently human-adjudicated — affects measured model performance, model rankings, and statistical conclusions.

Many review-based sentiment datasets use labels derived directly or indirectly from a star rating, or from a single annotation pass whose own reliability is rarely checked. This project builds an independent, multi-annotator **human-adjudicated reference set** for a fixed 757-review Arabic-English test slice, and measures exactly what changes — in per-class performance, model rankings, and paired statistical significance tests — when sixteen previously-trained model realizations are re-evaluated against it instead of against the original labels. The human-adjudicated reference set is not presented as an infallible ground truth; its own construction, agreement statistics, and limitations (including a single-adjudicator limitation) are reported in full.

## Main findings

- 757-review frozen bilingual evaluation slice (369 Arabic, 388 English), independently labeled by three bilingual annotators (2,271 primary annotations) and a blinded fourth adjudicator, who independently resolved all 179 non-unanimous cases without access to the original labels, ratings, prior annotator decisions, or vote counts.
- The original evaluation labels agreed with the resulting human-adjudicated reference set on **82.6%** of reviews (Cohen's κ = 0.662); disagreement was concentrated almost entirely in the Neutral class, where **82.9%** of originally Neutral-labeled reviews were revised to Positive or Negative.
- Re-evaluating 16 previously-trained model realizations (classical baselines, language-specific transformers, a multilingual model, and bidirectional zero-shot cross-lingual transfer) against the reference set lowered Macro-F1 for **13 of 16** of them, and reordered model rankings substantially for the Arabic evaluation condition and modestly for the English condition — not read as evidence that either language is inherently harder to classify.
- Of four pairwise model comparisons found statistically significant (Holm-corrected) under the original labels, **3 lost significance** under the human-adjudicated reference set, **1 survived**, and **1 previously non-significant comparison became significant**.

Full results, tables, and the complete evidentiary chain are in `paper/MANUSCRIPT_DRAFT.md` and `results/human_gold_evaluation/`.

## Repository structure

```
paper/            manuscript draft, blueprint, and the audit-trail notes (licensing, provenance,
                  reproducibility manifest, literature verification) under paper/notes/
paper/annotation/ the human annotation + adjudication study: protocols, instructions, agreement
                  outputs, and (where redistribution permits) the labeled data itself
results/          results/tables, results/figures (Phase 3A/3B original metrics),
                  results/phase3b_kaggle_gpu (Phase 3B GPU predictions + stats),
                  results/human_gold_evaluation (the human-adjudicated-reference re-evaluation:
                  scripts 01-07, metrics, statistical tests, confusion matrices)
src/              preprocessing/, evaluation/ (metrics.py), utils/
scripts/          training/evaluation entry points (run_baselines.py, run_transformers.py, etc.)
configs/          models.yaml, training.yaml, experiments.yaml
data/             dataset inventory, frozen split manifests; raw/processed review data is
                  present locally but excluded from version control (see Data availability)
docs/             dataset audit, methodology, decisions log, known limitations, label provenance
backend/, frontend/  a demonstration FastAPI + React inference API (supplementary; see below)
```

## Datasets

| Dataset | Role | Language | License |
|---|---|---|---|
| Saudi tourism reviews (Zenodo 17011574, Alahmadi 2025) | Primary Arabic pool | Arabic | CC-BY-4.0 |
| Jordanian-Arabic restaurant reviews (Zenodo 22061934, Sammour 2026) | Auxiliary (training augmentation + a separate binary evaluation task; zero Neutral examples, not pooled into the primary 3-class comparison) | Arabic (Jordanian dialect) | CC-BY-4.0 |
| Google Local Review Dataset (McAuley Lab, UCSD) | Primary English pool, domain/sentiment-matched subset | English | No redistribution license found on the official source page (verified directly, 2026) |

The Arabic and English pools are matched on sentiment distribution and approximate review length only — not on geography, domain collection process, or original label-construction method (single-pass human annotation for Arabic vs. rating-derived for English). Any Arabic/English comparison in this project is reported descriptively, never as evidence of inherent language difficulty. Full provenance: `paper/notes/DATASET_PROVENANCE.md`.

## Models

- Classical baselines: TF-IDF + Logistic Regression, TF-IDF + SVM
- MARBERT (Arabic-specialized transformer)
- XLM-R (multilingual transformer): per-language standalone, jointly-trained multilingual, and bidirectional zero-shot cross-lingual transfer

Two independent training configurations are used and **never merged or compared as isolating a single factor**: Phase 3A (CPU-only laptop, LoRA fine-tuning, unweighted loss, 64-token sequences) and Phase 3B (GPU, full fine-tuning, weighted loss, 128-token sequences). These differ in fine-tuning method, class weighting, sequence length, and hardware simultaneously — any score difference between the two tracks is a bundled-configuration comparison, never a GPU-vs-CPU, LoRA-vs-full-fine-tuning, or weighted-vs-unweighted-loss causal claim on its own. Two Arabic Phase 3B primary realizations (standalone MARBERT and standalone XLM-R) lost their original row-level predictions; every result that uses their reproducibility rerun instead is labeled `rerun realization` throughout, never presented as the lost primary run.

## Human annotation and adjudication

Three independent bilingual annotators each labeled all 757 reviews of the frozen test slice (2,271 primary annotations total), blinded to rating, original label, model prediction, and each other's decisions, in an independently randomized order per annotator. A fourth, independent bilingual adjudicator — blinded additionally to the three annotators' identities, their vote counts, and the majority outcome — resolved all 179 reviews without unanimous agreement, using only the review text and language. The resulting **human-adjudicated reference set** is explicitly not treated as infallible ground truth: its own construction (including the single-adjudicator limitation — all 179 cases were resolved by one person, with no second-adjudicator reliability check) is disclosed in full in `paper/annotation/full/README.md` and `paper/MANUSCRIPT_DRAFT.md` §4.

## Reproducibility

- Seeds: training/statistical seed = `42`; annotator presentation-order seeds = `1001`/`2002`/`3003`; adjudication presentation-order seed = `9009`.
- Statistical re-evaluation: paired bootstrap 95% CI and a genuine paired permutation/randomization test, 10,000 iterations each, Holm-Bonferroni correction within explicitly justified comparison families — scripts in `results/human_gold_evaluation/01_build_comparison_dataset.py` through `07_patch_rerun_labeling.py`.
- The human-adjudicated reference set's fixed identity: `paper/annotation/full/human_gold_757.csv`, SHA-256 `7b53ca621d237106413e27395010ad9ba2417d733b2bc5694d49749a03be53fd`.
- Frozen dataset splits: `data/splits/frozen_v1/` (group-aware by place/business; immutable manifests).
- Full recovered/unrecoverable software-and-hardware environment inventory: `paper/notes/REPRODUCIBILITY_MANIFEST.md`.

```
pip install -r requirements.txt
python scripts/evaluate.py                                    # Phase 3A metrics from saved predictions
python results/human_gold_evaluation/01_build_comparison_dataset.py  # ... through 07_patch_rerun_labeling.py
```

## Paper

Working manuscript (Abstract through Conclusion, drafted and internally audited): [`paper/MANUSCRIPT_DRAFT.md`](paper/MANUSCRIPT_DRAFT.md). A camera-ready PDF/DOCX has not yet been produced — see the project's final status report for what remains before a submission-ready document exists. Supporting audit trail: `paper/notes/` (scientific framing, dataset provenance, literature verification, consistency audit, reproducibility manifest).

## Data availability

- **Code, protocols, and aggregate results** (this repository, minus the exclusions below) are available as-is.
- **Arabic-side dataset derivatives** are released/releasable under CC-BY-4.0 with attribution.
- **English raw review text, English review identifiers, and human-adjudicated annotations keyed to English review identifiers are not publicly released, pending clarification of the source dataset's redistribution status.** This is a release decision, not a claim that redistribution is legally prohibited — no such prohibition has been verified either way.
- **English-trained model checkpoints** (including the demonstration backend's deployment model) are likewise not released pending the same clarification.

Full policy and the live-verification record: `paper/notes/DATA_LICENSING_AND_RELEASE.md`.

## Demonstration API (supplementary, not a research result)

A FastAPI backend (`backend/`) and React/Vite frontend (`frontend/`) provide an interactive demonstration of the deployment model. This is engineering scaffolding for inspecting model behavior, not evidence of model accuracy or effectiveness — its own automated tests and ad-hoc checks are described in the backend's own docs as end-to-end functional sanity checks only. See `backend/` and `frontend/` for setup; neither is part of this project's scientific contribution.

## Citation

A formal citation (authors, venue, DOI) is not yet available — this work has not been submitted or published. If you reference this repository in the meantime, cite it as:

```
[Author name(s) to be added]. "Evaluation-Label Reliability in Bilingual Sentiment Classification:
How Human-Adjudicated Reference Labels Change Model Rankings and Statistical Conclusions."
Unpublished manuscript, 2026. Repository: [GitHub URL to be added].
```

See `CITATION.cff` for a machine-readable version of the same placeholder.
