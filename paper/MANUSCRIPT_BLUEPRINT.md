# Manuscript Blueprint

**Status:** planning document only. No manuscript prose, no new experiments, no changed results. Every claim, number, and artifact reference below is sourced from existing, already-verified project files (`paper/notes/FINAL_SCIENTIFIC_FRAMING.md`, `results/human_gold_evaluation/`, `paper/annotation/full/`, `docs/`). This document is the single blueprint subsequent manuscript-writing sessions must follow; if evidence changes, this file must be updated before prose is adjusted to match.

---

## 1. Central paper story (frozen)

**Primary contribution:** evaluation-label reliability in bilingual (Arabic-English) sentiment classification, and its measured effect on model evaluation, ranking stability, and statistical conclusions.

**Supporting role of multilingual/cross-lingual modeling:** the two independent training tracks (CPU/LoRA; GPU/full fine-tuning), the monolingual/multilingual/zero-shot experimental grid, and the classical baselines are the *testbed* through which label reliability's effect is demonstrated -- they are not themselves the destination claim.

**Explicitly rejected framings:** Arabic-vs-English inherent difficulty; a leaderboard/model-comparison paper; a code-switching paper; a deployment paper. These are each addressed as a secondary thread or explicitly bounded as non-claims (Section 9).

---

## 2. Candidate titles (ranked)

1. **"Evaluation-Label Reliability in Bilingual Sentiment Classification: How Human-Adjudicated Reference Labels Change Model Rankings and Statistical Conclusions"** -- *recommended.* Leads with the primary contribution, names the method (human-adjudicated reference labels) without claiming infallibility, states the measurable outcome (rankings, statistical conclusions) rather than a result value.
2. "How Reliable Are Sentiment Evaluation Labels? A Human-Adjudicated Reference Study for Arabic-English Reviews"
3. "Rethinking Evaluation Labels in Multilingual Sentiment Analysis: An Arabic-English Human-Adjudication Study"
4. "From Rating-Derived to Human-Adjudicated Labels: Measuring Evaluation-Label Reliability in Arabic-English Sentiment Classification"
5. "Label Reliability and Ranking Stability in Multilingual Sentiment Classification: An Arabic-English Case Study"
6. "The Effect of Human-Adjudicated Reference Labels on Sentiment Model Evaluation: Evidence from Arabic-English Reviews"
7. "Evaluation-Label Reliability and Model-Ranking Stability in Multilingual Review Sentiment Analysis"
8. "Human Adjudication and the Stability of Sentiment-Model Conclusions: A Bilingual Review Case Study"

**Rationale for #1:** it is the only candidate that puts the measured *effect* (rankings, statistical conclusions) in the title rather than only the *method* (titles 2-4, 6-8 risk reading as "another annotation-quality paper" without signaling the downstream consequence that is this paper's actual novel finding). None use "first," "state-of-the-art," or "ground truth."

---

## 3. Final Research Questions (publication-ready wording)

**RQ1.** How reliable are the evaluation labels conventionally used for Arabic-English review sentiment classification -- rating-derived heuristics for English, single-pass human annotation for Arabic -- relative to a human-adjudicated reference set constructed from three independent bilingual annotators and a blinded fourth adjudicator?

**RQ2.** To what extent does replacing the original evaluation labels with the human-adjudicated reference set change measured model performance (accuracy, Macro-F1, per-class F1) and the relative ranking of previously-trained sentiment models?

**RQ3.** Does re-evaluating multilingual, language-specific, and cross-lingual zero-shot sentiment models against the human-adjudicated reference set change which pairwise performance differences are statistically significant?

**RQ4.** How does model performance on the Neutral sentiment class behave under human-adjudicated labels, given Neutral's low support in the reference set and the high rate of label revision observed for originally-Neutral-labeled reviews -- and what does this imply about the boundary between evaluation-label instability and genuine model weakness?

**Standing restriction (applies to all four RQs):** any Arabic-vs-English comparison surfaced while answering these RQs is reported descriptively (as a property of the disagreement/ranking-change pattern observed in each sub-corpus), never as evidence that one language is inherently harder to classify than the other.

---

## 4. Manuscript structure

| # | Section | Purpose | Evidence/artifacts | Key result/argument | Claims allowed | Claims to avoid |
|---|---|---|---|---|---|---|
| 1 | Introduction | Motivate the label-reliability question; state RQ1-4; preview the central finding | `FINAL_SCIENTIFIC_FRAMING.md` | Evaluation labels are often trusted uncritically; this paper measures what happens when they are not | "We measure the effect of label reliability on evaluation outcomes in a concrete bilingual setting" | "First study of..."; any Arabic/English difficulty framing; code-switching as a motivating hook (it is not the paper's subject) |
| 2 | Related Work | Position against annotation-reliability, rating-derived-label, multilingual-sentiment, and ranking-instability literature | Section 10 search plan (citations not yet retrieved) | The gap is specifically *measuring the downstream effect* of label reliability on model rankings/significance in a bilingual review setting, not annotation reliability alone | "To our knowledge, few studies directly connect annotator disagreement to post-hoc ranking instability in this domain" (hedged, pending literature verification) | Any specific citation not yet retrieved and verified; novelty claims stronger than the literature search supports |
| 3 | Data and Dataset Audit | Describe the three source datasets, licensing status, and the code-switching audit | `DATASET_PROVENANCE.md`, `DATA_LICENSING_AND_RELEASE.md`, `docs/codeswitch_audit.md` | Arabic primary (3,525, CC-BY-4.0, human-annotated); English primary (3,525 matched subset of 1,038,643 usable, rating-derived, unresolved license); Jordan auxiliary (binary, LLM-weak + 300 gold); code-switch audit found only 9/1,050,832 genuine instances, 77.1% of heuristic candidates were a UI translation artifact | State counts, label sources, and the code-switch finding as a measurement-methodology result | Any performance claim from the 9 code-switch examples; implying the English license is resolved |
| 4 | Human Annotation and Adjudication | Describe the 3-annotator + blind-4th-adjudicator design and its own reliability | `paper/annotation/full/README.md`, `ADJUDICATION_PROTOCOL.md`, `agreement_outputs/` | 757 reviews x 3 annotators = 2,271 primary annotations; 578 unanimous (76.4%), 179 adjudicated; Fleiss' κ=0.6499, Krippendorff's α=0.6500, mixed-sentiment κ=0.269 (dropped); single-adjudicator limitation disclosed | "Substantial" (not "near-perfect" or "high") agreement; explicit single-adjudicator limitation | "Human-Gold" used without first defining it as a human-adjudicated reference set; any claim of annotator/adjudicator infallibility |
| 5 | Experimental Methodology | Describe the two training tracks, models, and experiment grid | `configs/training.yaml`, `configs/models.yaml`, `configs/experiments.yaml`, `docs/decisions.md` D14-D17 | Phase 3A (laptop/LoRA) and Phase 3B (Kaggle GPU/full fine-tuning) are separate, non-merged tracks differing in fine-tuning method, class weighting, and sequence length simultaneously | "Configuration bundle A vs. configuration bundle B," named factor-by-factor | Any causal "GPU made it better" framing |
| 6 | Evaluation Protocol and Statistical Analysis | Describe the paired bootstrap CI and paired permutation test, Holm correction families, and the primary-vs-rerun handling | `results/human_gold_evaluation/README_PROVENANCE.md`, `04_statistical_tests.py` | Two distinct procedures (bootstrap resampling CI/heuristic-p; genuine paired permutation test), 10,000 iterations each, seed=42, Holm-corrected per family; rerun realizations explicitly flagged | Permutation-test p-values called permutation-test p-values; bootstrap p called a resampling heuristic | Calling the bootstrap heuristic a permutation test; mixing realizations within one inferential comparison |
| 7 | Results | Present the core findings in the Section 5 architecture below | `results/human_gold_evaluation/*` | See Section 5 | As qualified in the claim map (Section 9) | Any claim not in the claim map |
| 8 | Error and Label-Stability Analysis | Deep-dive on Neutral, qualitative error examples, deterministic selection rule | `error_analysis_by_class_language.csv`, `qualitative_error_examples.csv` | Neutral mean F1 0.396->0.176; dominant error pattern is over-prediction of Neutral by Phase 3B models relative to its much-smaller true size | Deterministic, disclosed example-selection rule; no annotator identity exposed | Causal mechanism claims for *why* Neutral is unstable |
| 9 | Discussion | Synthesize what the label-reliability finding means for how sentiment-model claims should be evaluated generally | All of the above | A model-ranking or significance claim is only as trustworthy as the evaluation label it is computed against | Methodological recommendation (re-validate evaluation labels before trusting a ranking), stated as a recommendation, not a universal law | Overgeneralizing beyond sentiment classification or beyond this domain |
| 10 | Limitations | State every open limitation plainly | `known_limitations.md` items 1-28, `final_publication_readiness_audit.md` | Single-adjudicator reference set; untested Phase 3A class-weighting confound; lost primary MARBERT/XLM-R predictions; unresolved English license; unrecoverable Kaggle environment versions; RQ3-style confounds never removed | Full, itemized disclosure | Burying a limitation in a subordinate clause elsewhere in the paper instead of here |
| 11 | Reproducibility / Data Availability | State exactly what is released, what is not, and why | `REPRODUCIBILITY_MANIFEST.md`/`.json`, `DATA_LICENSING_AND_RELEASE.md` | Code and Arabic-side data releasable; English raw text/IDs/linked labels and English-trained checkpoints withheld pending licensing resolution | Exact, itemized release table (Section 11 below) | Promising release of anything not yet cleared |
| 12 | Conclusion | Restate the central finding and its implication, briefly | Section 1 | Evaluation-label reliability measurably changes sentiment-model conclusions in this setting | Same as Introduction, past tense | Any new claim not already stated in Results/Discussion |

---

## 5. Results architecture (by argument, not experiment chronology)

| Seq | Subsection | Content | Primary source |
|---|---|---|---|
| A | Human annotation reliability | 3-annotator agreement (Fleiss' κ, Krippendorff's α, pairwise Cohen's κ, unanimous/majority/3-way counts); mixed-sentiment flag dropped (κ=0.269) | `agreement_outputs/overall_agreement_sentiment.json` |
| B | Original labels vs. human-adjudicated reference labels | Overall/Arabic/English agreement %, Cohen's κ, named transitions (6-way) | `comparison_dataset_757.csv`, `label_agreement_overall_by_language.json` |
| C | Effect on class distributions | Original {Neg 181, Neu 117, Pos 459} vs. reference {Neg 201, Neu 42, Pos 514}; 82.9% Neutral revision rate (89.3% Arabic, 77.1% English) | same |
| D | Effect on model performance | 16-model before/after Macro-F1/accuracy table; mean delta -0.025 (Phase 3A) vs. -0.101 (Phase 3B), concentrated in Arabic | `original_vs_human_gold_comparison.csv` |
| E | Model-ranking stability | Arabic ranking reorders substantially (GPU models fall from top-3 to mid/bottom); English ranking largely stable (top-2 swap only) | derived from (D) |
| F | Statistical-conclusion stability | 3 of 4 previously-significant comparisons lose significance; 1 survives (MARBERT rerun); 1 new comparison becomes significant (XLM-R rerun vs. MARBERT rerun) [corrected 2026-10-27 from an earlier "2 of 4" miscount] | `statistical_tests_human_gold.csv`, `results/tables/significance_tests.json`, Phase 3B original bootstrap CSVs |
| G | Neutral-class analysis | Mean Neutral-F1 0.396->0.176; support caveat (42/757, 9 Arabic/33 English); over-prediction pattern in Phase 3B models | `human_gold_metrics_all_models.csv`, `error_analysis_by_class_language.csv` |
| H | Multilingual/cross-lingual findings | E4 multilingual not significantly different from monolingual, before or after; zero-shot's "weaker" finding substantially weakens post-adjudication | `statistical_tests_human_gold.csv` |

**Placement rule (per explicit instruction):** A-C (the Human-Gold construction and disagreement findings) appear *before* D-H (the model-performance consequences) in Results -- the paper's argument is "here is how unreliable the original labels were, and here is what that unreliability did to the model story," not "here are the models, and here is a footnote about label quality."

---

## 6. Proposed tables

| # | Title | Purpose | Source artifact | Columns (indicative) | Placement |
|---|---|---|---|---|---|
| T1 | Dataset composition and provenance | Ground the corpus for the reader | `DATASET_PROVENANCE.md` | source, DOI/ID, raw/usable/retained counts, language, label source, task role, license status | Main |
| T2 | Three-annotator agreement statistics | Establish annotation reliability | `agreement_outputs/overall_agreement_sentiment.json` | n, unanimous/majority/3-way counts and rates, Fleiss' κ, Krippendorff's α, pairwise Cohen's κ, mixed-flag κ | Main |
| T3 | Original-label vs. human-adjudicated agreement and transitions | Core RQ1 evidence | `comparison_dataset_757.csv`, `label_agreement_overall_by_language.json` | scope (overall/AR/EN), agree %, disagree %, Cohen's κ, 6 named transitions | Main |
| T4 | Class distribution shift | Core RQ1/RQ4 evidence | `label_agreement_overall_by_language.json` | class, original count/%, reference-set count/%, by language | Main |
| T5 | Model performance before/after human-adjudicated re-evaluation (condensed) | Core RQ2 evidence | `original_vs_human_gold_comparison.csv` | model, phase, **realization** (primary/rerun), language, Macro-F1 original, Macro-F1 reference-set, delta | Main |
| T6 | Model ranking, original vs. reference-set, by language | Core RQ2 evidence | derived from T5 | rank, model, Macro-F1 (two columns, two labelings) | Main |
| T7 | Statistical significance, original vs. reference-set labeling | Core RQ3 evidence | `statistical_tests_human_gold.csv` + `results/tables/significance_tests.json` + Phase 3B original bootstrap CSVs | family, model_a (+realization), model_b (+realization), significant under original?, significant under reference-set? (both bootstrap-Holm and permutation-Holm) | Main |
| T8 | Per-class F1, focus on Neutral | Core RQ4 evidence | `human_gold_metrics_all_models.csv` | model, language, Negative/Neutral/Positive F1 (original and reference-set), Neutral support | Main |
| T9 | Full prediction-availability and realization audit | Reproducibility/completeness | `prediction_availability.csv` | model_key, phase, language, realization, file, row/id checks, status | Supplementary |
| T10 | Full per-model confusion matrices | Completeness | `confusion_matrix_<model>_<original_label\|human_gold>.csv` (16 x 2) | true x predicted, 3x3 | Supplementary |
| T11 | Full pairwise statistical test results (all 18 comparisons, both tests, both p-values) | Completeness/auditability | `statistical_tests_human_gold.csv/json` | family, model_a/b + realizations, Macro-F1 each, observed diff, bootstrap CI + Holm p, permutation p + Holm p | Supplementary |
| T12 | Code-switch candidate audit breakdown | Supports Section 3/dataset-audit claim | `docs/codeswitch_audit.md` | category, count, % of 109 | Supplementary |
| T13 | Reproducibility manifest summary | Transparency | `REPRODUCIBILITY_MANIFEST.md/.json` | item, value or "NOT RECOVERABLE..." | Supplementary |
| T14 | Error breakdown by true/predicted class and language, all models | Supports Section 8 | `error_analysis_by_class_language.csv` | model, language, realization, true class, predicted class, count | Supplementary |

**Rerun visibility rule:** T5, T6, T7, T9, T11, and T14 all carry an explicit `realization` column/qualifier wherever an Arabic MARBERT/XLM-R standalone model appears -- no table in this plan presents a rerun figure without the qualifier in the same row.

---

## 7. Proposed figures

| # | Scientific purpose | Data source | Axes/encoding | Caption message (draft intent, not final text) | Placement |
|---|---|---|---|---|---|
| F1 | Show where original-label disagreement concentrates | `full_transition_table_overall.csv` | Alluvial/Sankey: original class (left) -> reference-set class (right), flow width = count | "Disagreement between original and human-adjudicated labels is concentrated almost entirely in originally-Neutral reviews." | Main |
| F2 | Show the performance consequence of relabeling, across all models | `original_vs_human_gold_comparison.csv` | Slope/dumbbell plot: one line per model from (original Macro-F1) to (reference-set Macro-F1), colored by phase/track | "Macro-F1 drops for most models under human-adjudicated evaluation, and the drop is larger for the GPU full-fine-tuning track than the LoRA track." | Main |
| F3 | Show ranking instability directly | T6 | Bump/slopegraph: rank position under original labels (left) vs. reference-set labels (right), one line per model, separate panels per language | "The Arabic model ranking reorders substantially under human-adjudicated evaluation; the English ranking is comparatively stable." | Main |
| F4 | Show Neutral's behavior with its support caveat visible in the figure itself | `human_gold_metrics_all_models.csv` | Bar or forest plot: per-model Neutral F1 (original vs. reference-set), with the support count (n=9 Arabic / n=33 English) annotated directly on the axis, not only in the caption | "Neutral F1 falls further under human-adjudicated evaluation across every model; support is small and must be read alongside the estimate." | Main |
| F5 | Illustrate adjudicator confidence distribution | adjudication merge output | Stacked bar: confidence (high/medium/low) by case type (majority vs. three-way) and language | Supports Section 4's methodology description | Supplementary |
| F6 | Full confusion-matrix detail for the 2-3 most-discussed models | `confusion_matrix_*` | Heatmap grid | Supports Section 8's error analysis | Supplementary |
| F7 | Show the code-switch heuristic's failure mode | `docs/codeswitch_audit.md` counts | Funnel: 109 candidates -> 5 categories -> 9 genuine | "A common script-mixing heuristic is dominated by a platform display artifact in this domain, not genuine code-switching." | Supplementary |

**No figure is proposed for the deployment artifact** -- consistent with Section 1's rejection of a deployment framing.

---

## 8. Contribution statement (bullet-level plan, not prose)

- A 757-review, 3-independent-bilingual-annotator human validation study (2,271 primary annotations) of Arabic and English Google-Maps-domain reviews, with a pre-registered, blinded fourth-adjudicator resolution of all 179 non-unanimous cases -- explicitly not presented as an infallible ground truth, and its own single-adjudicator limitation disclosed.
- A direct, quantified demonstration that re-evaluating 16 previously-trained sentiment models against this human-adjudicated reference set changes (a) per-class performance (Neutral F1 falls further), (b) model rankings (substantially in Arabic, modestly in English), and (c) statistical-significance conclusions (3 of 4 previously-significant comparisons no longer hold, 1 survives, and 1 previously non-significant comparison becomes significant).
- A methodological contribution: two explicitly non-conflated statistical procedures (paired bootstrap CI vs. a genuine paired permutation/randomization test) applied to Macro-F1 model comparisons, with primary-vs-rerun model realizations kept visibly distinct throughout.
- A secondary empirical contribution on multilingual/cross-lingual transfer: multilingual joint training is not significantly different from monolingual training in either language, under either labeling; zero-shot cross-lingual transfer's apparent weakness substantially narrows under human-adjudicated evaluation.
- A dataset/measurement-methodology finding: a common code-switch-detection heuristic's candidate set was dominated (77.1%) by a platform UI translation-display artifact rather than genuine code-switching, leaving only 9 genuine instances in a 1,050,832-document corpus.

---

## 9. Claim map

| Manuscript claim | Supporting result | Exact artifact | Statistical support | Required qualification |
|---|---|---|---|---|
| Original evaluation labels disagree with the human-adjudicated reference set in ~17% of cases overall | 625/757 agree (82.6%), κ=0.662 | `label_agreement_overall_by_language.json` | Cohen's κ | State both agreement % and κ together; κ alone without % is less interpretable to a general NLP audience |
| Disagreement concentrates in originally-Neutral reviews | 82.9% of originally-Neutral reviews revised (89.3% AR, 77.1% EN) | `disagreement_rate_conditional.csv` | Descriptive | State as a conditional rate, not as "Neutral labels were wrong" |
| Re-evaluation changes model rankings | Arabic top-3 reorders into mid/bottom; English top-2 swap only | `original_vs_human_gold_comparison.csv` | Descriptive | Name realization (primary/rerun) for every Arabic MARBERT/XLM-R mention |
| Re-evaluation changes statistical conclusions | 3/4 previously-significant comparisons lose significance; 1 survives; 1 new comparison becomes significant [corrected 2026-10-27] | `statistical_tests_human_gold.csv` vs. `results/tables/significance_tests.json` + Phase 3B bootstrap CSVs | Paired permutation test, Holm-corrected | Always state "under the permutation test, Holm-corrected" -- do not cite the bootstrap-heuristic p as the significance criterion |
| Neutral is the lowest-performing class | Mean F1 0.396 (original) -> 0.176 (reference-set) across 16 models | `human_gold_metrics_all_models.csv` | Descriptive mean across models | Attach support counts (42/757 overall, 9 AR/33 EN) every time; no causal-mechanism claim |
| Multilingual training is competitive with monolingual | Not significant in either language, either labeling | `statistical_tests_human_gold.csv` (Phase3B_Arabic, Phase3B_English families) | Paired permutation test, Holm-corrected | "Not significantly different" is not "equivalent"; state the point estimates alongside the non-significance |
| Zero-shot transfer is weaker | Significant in 3/4 comparisons (original) -> 1/4 (reference-set) | `results/tables/significance_tests.json` + `statistical_tests_human_gold.csv` | Paired permutation test, Holm-corrected, both periods | Report both numbers; do not report only the original-label figure |
| Phase 3B (GPU) apparent gains over Phase 3A (LoRA) shrink under human-adjudicated evaluation | Mean Macro-F1 delta -0.101 vs. -0.025 | `original_vs_human_gold_comparison.csv` grouped by phase | Descriptive | Non-causal: fine-tuning method, class weighting, and sequence length differ simultaneously; consistent-with, not proof-of, label-overfitting mechanism |
| Code-switching is empirically rare and hard to detect reliably | 9/1,050,832 genuine; 77.1% heuristic false-positive rate from a UI artifact | `docs/codeswitch_audit.md` | Inter-rater κ=0.809 (binary) on the audit itself | Never attach a performance number to the 9 examples |
| Arabic and English disagreement/ranking-change patterns differ | Arabic ranking reorders more than English's | Section 5(E) | Descriptive only | Explicit non-causal, non-difficulty disclaimer every time this is mentioned |

---

## 10. Related-work search plan (categories and queries -- no citations invented)

1. **Sentiment-label reliability / annotation quality effects on evaluation.** Queries: "label noise sentiment analysis evaluation"; "annotation reliability downstream model evaluation NLP"; "effect of label quality on reported model performance."
2. **Annotation disagreement and adjudication methodology.** Queries: "inter-annotator agreement adjudication protocol NLP"; "Fleiss kappa sentiment annotation three annotators"; "blind adjudication disagreement resolution annotation."
3. **Rating-derived sentiment labels and their failure modes.** Queries: "star rating as sentiment label noise"; "rating-text disagreement sarcasm sentiment"; "review rating proxy label validity."
4. **Multilingual and cross-lingual sentiment analysis.** Queries: "multilingual sentiment classification transformer"; "cross-lingual zero-shot sentiment transfer Arabic English"; "joint multilingual training vs monolingual sentiment."
5. **Arabic sentiment analysis.** Queries: "Arabic sentiment analysis review dataset transformer"; "MARBERT Arabic sentiment classification"; "Arabic dialect sentiment annotation agreement."
6. **Evaluation-set quality and dataset artifacts in NLP benchmarks.** Queries: "benchmark label errors NLP"; "dataset artifact evaluation set reliability"; "re-annotating test sets changes model ranking."
7. **Model-ranking instability caused by evaluation-label changes.** Queries: "label errors change leaderboard ranking"; "re-labeling test set model comparison significance"; "evaluation label noise statistical significance machine learning."
8. **Code-switching detection and review-domain text.** Queries: "code-switching detection heuristic false positive"; "Arabic-English code-switched sentiment dataset"; "script mixing detection social media text."

**Instruction for the drafting phase:** every citation that eventually appears in Related Work must be independently retrieved and verified (title, venue, year, claim actually made) before being written into the manuscript -- consistent with this project's standing no-fabrication rule applied in every prior phase.

---

## 11. Data availability and licensing plan (as currently resolvable)

| Artifact | Public release status |
|---|---|
| Code (preprocessing, training, evaluation, statistical, annotation-tooling scripts) | Releasable |
| Arabic-side data derivatives (Zenodo 17011574, CC-BY-4.0; Zenodo 22061934) | Releasable with attribution |
| English raw review text | **Not released** |
| English review IDs / split membership | **Not released** |
| Human-adjudicated annotations keyed to English review IDs | **Not released** (same reasoning as IDs -- rejoinable to restricted text) |
| English-trained model checkpoints (Phase 3B English, deployment model) | **Not released** |
| Arabic-trained model checkpoints | Releasable in principle (data license permits); still subject to normal institutional/author release decisions |
| Aggregate English-side metrics, tables, and figures (no row-level artifact) | Releasable -- this is how English-side results are reported in the manuscript itself |

This status reflects `DATA_LICENSING_AND_RELEASE.md` exactly and must not be independently re-decided during drafting. The McAuley Lab contact recommended there remains a pending external action and should be attempted before any camera-ready/public release step (not before manuscript submission, which does not itself require redistributing the restricted artifacts).

---

## 12. Supplementary-material plan

**Moves to supplementary:**
- Complete Phase 3A experiment grid (all per-model/per-run detail beyond the condensed main-paper table)
- Full Phase 3B training configuration detail
- All 32 confusion matrices (16 models x original/reference-set)
- Full statistical-test table (all 18 pairwise comparisons, both test types, both raw and Holm-adjusted p-values)
- Deployment demo description (end-to-end functional sanity checks only; explicitly not an evaluation result) -- a short paragraph at most, not a section
- Code-switching audit full detail (all 109 candidates' category breakdown, reviewer methodology, κ)
- Extended annotation diagnostics (confidence distributions, per-pair pairwise κ detail, adjudicator-vs-majority agreement breakdown by class)
- Full reproducibility manifest

**Stays in main paper:** the 14 main-paper items from Section 6/7's tables and figures, the contribution statement, the core claim map's claims, and a concise (1-2 paragraph) acknowledgment that a demonstration API/UI exists, pointing to supplementary material for detail.

---

## 13. Target-journal profile (no journal selected)

The manuscript should target a venue with these properties:
- NLP / applied AI / language technology scope (not a general ML venue that would deprioritize annotation-methodology content).
- A track record of accepting substantial empirical-methodology papers (not only leaderboard-style model papers) -- this paper's central contribution is a methodology-and-measurement finding, not a new model or SOTA claim.
- Explicit appropriateness for multilingual sentiment / evaluation-methodology research (so reviewers are primed to value the label-reliability framing rather than asking "why isn't this an Arabic NLP venue only" or "where is the new model").
- Sufficient page budget/appendix policy to accommodate both the annotation-methodology detail (Section 4) and the statistical-analysis detail (Section 6) without compressing either past legibility.

**Decisions deferred until a target is actually selected:** exact section/subsection numbering and heading style, citation style (numeric vs. author-year), table/figure placement rules (inline vs. end-of-manuscript), abstract/structured-summary length limits, supplementary-material submission format (single PDF vs. separate files), and any venue-specific reproducibility/data-availability statement template.

---

## 14. Status

This blueprint is complete. No manuscript prose has been written. No experiment was run or result changed while producing it.
